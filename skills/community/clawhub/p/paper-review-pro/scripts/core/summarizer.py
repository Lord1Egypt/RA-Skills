"""
摘要生成模块

支持：
1. OpenClaw Gateway API 调用（优先）
2. Dashscope API 调用（备用）
3. Fallback 到规则提取
"""

import os
import json
import re
import urllib.request
import urllib.error
import argparse

# OpenClaw Gateway 配置
GATEWAY_URL = os.environ.get("OPENCLAW_GATEWAY_URL", "http://localhost:14940")
GATEWAY_TOKEN = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")

# 尝试从 OpenClaw 配置读取 token
if not GATEWAY_TOKEN:
    try:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                GATEWAY_TOKEN = config.get("gateway", {}).get("auth", {}).get("token", "")
    except Exception:
        pass

# Dashscope 配置（备用）
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3.5-plus")


def _call_gateway_llm(prompt: str) -> str:
    """
    调用 OpenClaw Gateway API 生成文本
    
    返回生成的文本内容，失败返回 None
    """
    try:
        url = f"{GATEWAY_URL.rstrip('/')}/v1/chat/completions"
        
        payload = {
            "model": "dashscope/qwen3.5-plus",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的学术论文分析助手。请根据用户提供的论文信息，生成简洁、准确的中文摘要。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        
        # 如果有 token 则添加认证
        if GATEWAY_TOKEN:
            headers["Authorization"] = f"Bearer {GATEWAY_TOKEN}"
        
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
    except urllib.error.HTTPError as e:
        # 401/403 等认证错误时不打印详细错误（避免干扰）
        if e.code not in [401, 403]:
            print(f"  [Gateway HTTP 错误]: {e.code}")
        return None
    except Exception as e:
        # 其他错误（超时、连接失败等）
        return None


def _call_dashscope_llm(prompt: str) -> str:
    """
    调用 Dashscope API 生成文本（备用方案）
    
    返回生成的文本内容，失败返回 None
    """
    if not DASHSCOPE_API_KEY:
        return None
    
    try:
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        payload = {
            "model": DASHSCOPE_MODEL,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的学术论文分析助手。请根据用户提供的论文信息，生成简洁、准确的中文摘要。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "temperature": 0.3,
                "max_tokens": 500
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("output", {}).get("text", "")
            
    except Exception as e:
        print(f"  [Dashscope 调用失败]: {e}")
        return None


def _parse_llm_summary(llm_output: str) -> dict:
    """
    解析 LLM 输出的摘要文本为结构化字典
    
    支持多种格式：
    - 中文：研究问题：xxx / **研究问题**: xxx
    - 英文：Research Question: xxx / **Research Question**: xxx
    - 列表格式：- 研究问题：xxx
    """
    # 默认结构
    summary = {
        "研究问题": "",
        "方法": "",
        "主要结论": "",
        "创新点": ""
    }
    
    if not llm_output:
        return summary
    
    # 中英文键名映射
    key_mapping = {
        "研究问题": ["研究问题", "问题", "背景", "research question", "question", "background", "problem"],
        "方法": ["方法", "方法论", "技术方案", "method", "methodology", "approach", "technique"],
        "主要结论": ["主要结论", "结论", "结果", "发现", "conclusion", "result", "finding", "findings"],
        "创新点": ["创新点", "贡献", "创新", "contribution", "innovation", "novelty"]
    }
    
    # 先尝试按行解析结构化输出
    lines = llm_output.strip().split("\n")
    current_key = None
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # 移除 markdown 列表符号和粗体标记
        line_clean = re.sub(r'^[-*•]\s*', '', line_stripped)
        line_clean = line_clean.strip()
        
        # 检查是否是新段落的开始
        matched = False
        for key, prefixes in key_mapping.items():
            for prefix in prefixes:
                # 匹配多种格式：
                # "前缀：" / "前缀:" / "**前缀**:" / "**前缀**：" / "Prefix: " / "**Prefix**: "
                pattern = rf"^(?:\*\*)?{re.escape(prefix)}(?:\*\*)?[：:]\s*(.*)"
                match = re.match(pattern, line_clean, re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    # 移除开头的粗体标记
                    content = re.sub(r'^\*\*|\*\*$', '', content)
                    summary[key] = content
                    current_key = key
                    matched = True
                    break
            if matched:
                break
        
        # 如果没有匹配到前缀，但有当前 key，追加内容（连续段落）
        if not matched and current_key and line_clean:
            # 跳过纯列表符号行
            if re.match(r'^[-*•]\s*$', line_clean):
                continue
            if summary[current_key]:
                summary[current_key] += " " + line_clean
            else:
                summary[current_key] = line_clean
    
    # 如果结构化解析失败，尝试从全文提取（增强 fallback）
    if all(not summary[k] for k in summary):
        # 尝试用更宽松的 regex 匹配
        for key, prefixes in key_mapping.items():
            for prefix in prefixes:
                # 更宽松的模式：允许前缀出现在行中任意位置
                pattern = rf"(?:^|\n)\s*(?:[-*•]\s*)?(?:\*\*)?{re.escape(prefix)}(?:\*\*)?[：:]\s*([^\n]+)"
                match = re.search(pattern, llm_output, re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    content = re.sub(r'^\*\*|\*\*$', '', content)
                    if content and len(content) > 5:
                        summary[key] = content
    
    return summary


def _fallback_summary(abstract: str) -> dict:
    """
    Fallback：基于规则的摘要提取
    """
    if not abstract:
        return {
            "研究问题": "无可用摘要",
            "方法": "无可用信息",
            "主要结论": "无可用信息",
            "创新点": "无可用信息"
        }
    
    # 尝试从摘要中提取关键句
    sentences = abstract.replace("\n", " ").split(".")
    
    research_question = sentences[0][:150] if sentences else abstract[:150]
    conclusion = sentences[-1][:150] if len(sentences) > 1 else abstract[-150:]
    
    return {
        "研究问题": research_question.strip() + "..." if len(research_question) > 50 else research_question,
        "方法": "基于论文摘要分析（需人工补充详细方法）",
        "主要结论": conclusion.strip() + "..." if len(conclusion) > 50 else conclusion,
        "创新点": "建议阅读原文获取详细创新点"
    }


def summarize(paper, use_llm: bool = True) -> dict:
    """
    生成中文摘要
    
    参数:
        paper: dict，包含 title, abstract, authors 等字段
        use_llm: bool，是否使用 LLM 生成摘要（默认 True）
    
    返回:
        dict: {"研究问题": str, "方法": str, "主要结论": str, "创新点": str}
    """
    title = paper.get("title", "Unknown Title")
    abstract = paper.get("abstract", "")
    authors = ", ".join(paper.get("authors", ["Unknown"]))
    
    if not use_llm or not abstract:
        return _fallback_summary(abstract)
    
    print(f"  [生成摘要] {title[:50]}...")
    
    # 构建提示词
    prompt = f"""请分析以下学术论文并生成结构化中文摘要：

**论文标题**: {title}
**作者**: {authors}
**原文摘要**: {abstract}

请按照以下格式输出（每部分 1-2 句话）：

研究问题：[这篇论文要解决什么问题？]
方法：[使用了什么方法/技术？]
主要结论：[主要发现/结果是什么？]
创新点：[相比已有工作的创新之处？]
"""
    
    # 尝试调用 LLM
    llm_output = _call_gateway_llm(prompt)
    llm_source = "Gateway"
    
    if not llm_output:
        llm_output = _call_dashscope_llm(prompt)
        llm_source = "Dashscope"
    
    if llm_output:
        print(f"  [LLM 调用成功 ({llm_source})]，输出长度：{len(llm_output)} 字符")
        summary = _parse_llm_summary(llm_output)
        # 检查解析结果
        parsed_count = sum(1 for v in summary.values() if v and len(v.strip()) >= 3)
        print(f"  [解析结果] {parsed_count}/4 字段已解析")
        # 仅对真正为空的字段使用 fallback，避免覆盖有效的短答案
        fallback = None
        for key in summary:
            if not summary[key] or len(summary[key].strip()) < 3:
                if fallback is None:
                    fallback = _fallback_summary(abstract)
                summary[key] = fallback[key]
        return summary
    
    # Fallback
    print("  [使用 Fallback 摘要]")
    return _fallback_summary(abstract)

def main():
    argparser = argparse.ArgumentParser(description="论文摘要生成器")
    argparser.add_argument("--title", type=str, required=True, help="论文标题")
    argparser.add_argument("--abstract", type=str, required=True, help="论文摘要")
    argparser.add_argument("--authors", type=str, nargs="*", default=["Unknown"], help="论文作者列表")
    argparser.add_argument("--no-llm", default=False, action="store_true", help="禁用 LLM 功能（使用规则 fallback）")
    args = argparser.parse_args()

    paper = {
        "title": args.title,
        "abstract": args.abstract,
        "authors": args.authors
    }

    summary = summarize(paper, use_llm=not args.no_llm)

    print("生成的摘要：")
    for key, value in summary.items():
        print(f"  {key}：{value}")

if __name__ == "__main__":
    main()
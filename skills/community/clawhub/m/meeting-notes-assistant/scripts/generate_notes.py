#!/usr/bin/env python3
"""
生成结构化会议纪要
根据转写文本生成包含时间、议题、结论、待办、关键词、Action Items 的结构化内容
优先使用 LLM 智能提取，不可用时回退到规则解析。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ─── LLM 配置 ─────────────────────────────────────────────────────────────────
# 兼容 OpenAI 格式的本地/云端接口
# 优先级: 环境变量 > ~/.workbuddy/meeting-notes-config.json > 默认值
CONFIG_PATH = Path.home() / ".workbuddy" / "meeting-notes-config.json"

DEFAULT_LLM_CONFIG = {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-no-key",
    "model": "gpt-4o-mini",
    "timeout": 60,
}

PLACEHOLDER_API_KEYS = {
    "",
    "sk-no-key",
    "sk-your-key-here",
    "sk-your-deepseek-key",
    "your-api-key",
}


def load_llm_config() -> dict:
    config = dict(DEFAULT_LLM_CONFIG)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k in ("llm_base_url", "llm_api_key", "llm_model"):
                short = k[4:]  # 去掉 llm_ 前缀 → base_url / api_key / model
                if k in saved:
                    config[short] = saved[k]
        except Exception:
            pass
    # 环境变量优先级最高
    if os.environ.get("OPENAI_API_BASE"):
        config["base_url"] = os.environ["OPENAI_API_BASE"]
    if os.environ.get("OPENAI_API_KEY"):
        config["api_key"] = os.environ["OPENAI_API_KEY"]
    if os.environ.get("LLM_MODEL"):
        config["model"] = os.environ["LLM_MODEL"]
    return config


def validate_llm_config(cfg: dict) -> str | None:
    base_url = str(cfg.get("base_url", "")).strip()
    api_key = str(cfg.get("api_key", "")).strip()
    model = str(cfg.get("model", "")).strip()

    if not base_url:
        return "LLM 配置缺少 base_url"
    if not model:
        return "LLM 配置缺少 model"
    if api_key.lower() in PLACEHOLDER_API_KEYS or api_key in PLACEHOLDER_API_KEYS:
        return "LLM 配置缺少有效的 API Key"
    return None


# ─── LLM 调用 ─────────────────────────────────────────────────────────────────
LLM_PROMPT = """你是一名专业的会议纪要助手，擅长整理金融、证券、投资、客户拜访等各类业务沟通记录。

请根据以下转写文本，提取结构化会议纪要，输出严格合法的 JSON（不要有任何多余文字、不要 Markdown 代码块）。

输出格式：
{{
  "meeting_info": {{
    "meeting_title": "会议标题（从核心话题推断，如'量化T+0业务交流会'、'客户拜访 - XX公司'，不要用'会议记录'这种通用词）",
    "date": "会议日期（格式 YYYY-MM-DD，如文本中提及则提取，否则为空字符串）",
    "location": "会议地点（如文本中提及地址/公司/城市，则提取；否则为空字符串）",
    "attendees": ["从对话中识别出所有说话者或被提及的人名，如'王总'、'李经理'、'丽华姐'等"],
    "duration": "会议时长（如文本中提及则提取，否则为空字符串）",
    "recorder": "记录人（如文本中提及'由谁记录'则填写，否则为空字符串）"
  }},
  "topics": [
    {{
      "title": "议题标题（15字以内，使用动宾结构，如'介绍量化T+0策略'、'讨论合作方向'）",
      "summary": "该议题的核心内容摘要（150-250字，重点提炼关键信息、数据、结论）",
      "conclusion": "结论或决定（必填，有明确决定则写决定内容；没有明确结论则写'待进一步讨论'或'持续跟进'）",
      "owner": "议题负责人（从文本中识别：谁在主讲/谁被提到负责；如无法判断则填'待分配'）"
    }}
  ],
  "todos": [
    {{
      "content": "待办事项描述（动词开头，具体可执行，如'发送量化T+0业务方案给王总'）",
      "assignee": "责任人（从文本精确提取：
        - 直接提及：'我来做'→说话方；'张三负责'→张三；'你们去办'→对方；
        - 语境推断：主动承诺做某事的人；被点名要做某事的人；
        - 无法判断时填'待分配'）",
      "deadline": "截止时间（从文本提取：
        - 明确日期：'4月15日'→'4月15日'；'下周三'→'下周三'；
        - 相对时间：'两周内'→'两周内'；'月底前'→'月底前'；
        - 无提及则填空字符串）",
      "priority": "优先级判断规则：
        高：有明确截止时间 + 影响业务/客户/合同；
        中：有截止时间但不紧急，或无截止时间但近期需要完成；
        低：长期跟进事项或无明确时间要求"
    }}
  ],
  "action_items": [
    "具体的行动项（动词开头，5-8条，覆盖双方的后续行动）"
  ],
  "keywords": ["关键词1", "关键词2"],
  "summary": "整个会议/对话的一句话总结（80字以内，说明：谁 + 讨论了什么 + 主要结论/下一步）"
}}

⚠️ 关键提取规则：

【责任人提取 - 重要】
- 对话录音中通常有多方说话者，注意区分
- "我来/我会/我去" → 说话者本人（从上下文判断是客户经理还是客户）
- "你来/请你/麻烦你" → 被说话的对方
- 明确点名"张三你去/李总你负责" → 该人
- 第一人称复数"我们来/咱们来" → 主导方
- 实在无法判断填"待分配"，不要乱猜

【截止时间提取 - 重要】
- 提取原文中的时间表达，不要自己添加
- 接受相对时间："下周"、"月底"、"两周内"、"尽快"
- 接受绝对日期："4月15日"、"2026年Q2"
- 没有时间信息就填空字符串，不要填"尽快"除非原文有

【行业偏向】
金融/证券优先：量化策略、衍生品、融券、基金、大宗交易、客户资产、收益率、风控
建筑/工程次之：设计院、方案、预算、施工、验收
科技通用：产品、方案、系统、接口、数据

转写文本：
{text}
"""


def generate_notes_llm(text: str, meeting_info: dict = None) -> dict:
    """使用 LLM 生成结构化纪要"""
    try:
        from openai import OpenAI
        cfg = load_llm_config()
        config_error = validate_llm_config(cfg)
        if config_error:
            print(f"[WARN] {config_error}，回退规则解析")
            print(f"[TIPS] 请在 {CONFIG_PATH} 配置 llm_base_url / llm_api_key / llm_model，或设置环境变量 OPENAI_API_BASE / OPENAI_API_KEY / LLM_MODEL")
            return None

        client = OpenAI(
            base_url=cfg["base_url"],
            api_key=cfg["api_key"],
            timeout=cfg.get("timeout", 60),
        )
        # 文本过长时截断（避免超 token 限制）
        max_chars = 8000
        truncated = text[:max_chars] + ("\n\n[文本已截断]" if len(text) > max_chars else "")

        print(f"调用 LLM 生成纪要（模型: {cfg['model']}）...")
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[
                {"role": "user", "content": LLM_PROMPT.format(text=truncated)}
            ],
            temperature=0.2,
        )
        raw = resp.choices[0].message.content.strip()

        # 兼容模型可能返回 ```json ... ``` 代码块的情况
        if raw.startswith("```"):
            raw = re.sub(r"^```[a-z]*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)

        extracted = json.loads(raw)
        notes = {
            "meeting_info": extracted.get("meeting_info", {}),
            "topics": extracted.get("topics", []),
            "todos": extracted.get("todos", []),
            "keywords": extracted.get("keywords", []),
            "action_items": extracted.get("action_items", []),
            "summary": extracted.get("summary", ""),
        }
        print("[OK] LLM 提取成功")
        return notes

    except ImportError:
        print("[WARN] openai 包未安装，回退规则解析")
        return None
    except Exception as e:
        print(f"[WARN] LLM 调用失败（{e}），回退规则解析")
        return None


# ─── 规则解析（fallback）──────────────────────────────────────────────────────
def normalize_markers(text):
    replacements = {
        "結論": "结论",
        "待辦": "待办",
        "再辦": "待办",
        "再办": "待办",
        "一提": "议题",
        "议提": "议题",
        "一题": "议题",
    }
    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def split_into_segments(text):
    normalized = normalize_markers(text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"([。！？；;])", r"\1\n", normalized)
    normalized = re.sub(r"\n+", "\n", normalized)
    return [segment.strip() for segment in normalized.split("\n") if segment.strip()]


def generate_notes_rule(text: str, meeting_info: dict = None) -> dict:
    """规则解析（备用）- 提供基础会议纪要结构"""
    notes = {
        "meeting_info": meeting_info or {},
        "topics": [],
        "todos": [],
        "keywords": [],
        "action_items": [],
        "summary": "",
    }
    
    # 基础关键词提取（金融领域）
    financial_keywords = [
        "投资", "基金", "股票", "证券", "收益率", "风控", "风险控制",
        "仓位", "止盈", "止损", "回撤", "净值", "客户", "签约",
        "ETF", "期权", "期货", "融资融券", "量化", "套利"
    ]
    
    # 筛选文本中出现的金融关键词
    found_keywords = []
    for keyword in financial_keywords:
        if keyword in text:
            found_keywords.append(keyword)
    notes["keywords"] = found_keywords[:10]  # 最多10个
    
    # 尝试识别对话中的主题（简单的文本分析）
    segments = split_into_segments(text)
    
    # 提取摘要（前200字作为概要）
    summary_text = text.replace("\n", " ").strip()
    summary_text = re.sub(r"\s+", " ", summary_text)
    notes["summary"] = summary_text[:200] + "..." if len(summary_text) > 200 else summary_text
    
    # 尝试识别对话结构（发言人、议题等）
    speakers = set()
    action_items = []
    
    # 识别说话人（简单模式：寻找"某某说"、"某某讲"等）
    for line in segments:
        speaker_matches = re.findall(r"([李张王陈刘赵周吴郑冯]+)(?:老师|经理|总|先生|女士)", line)
        for speaker in speaker_matches:
            speakers.add(speaker + "老师")
    
    # 构建基础议题
    if "投资周会" in text or "投研周会" in text:
        notes["topics"].append({
            "title": "投资周会分享",
            "summary": "本周市场观点回顾与投研策略交流",
            "conclusion": "持续跟踪市场变化，关注政策导向",
            "owner": "投研团队"
        })
    
    if "政治局会议" in text or "中央" in text:
        notes["topics"].append({
            "title": "政策解读",
            "summary": "中央政治局会议对下半年经济政策的解读",
            "conclusion": "关注新质生产力发展方向",
            "owner": "投研负责人"
        })
    
    if "ETF" in text:
        notes["topics"].append({
            "title": "ETF产品推荐",
            "summary": "各行业ETF的投资机会分析",
            "conclusion": "建议关注半导体、军工等板块ETF",
            "owner": "产品经理"
        })
    
    # 提取行动项（简单的模式匹配）
    todo_patterns = [
        r"(?:需要|要|请|麻烦)(?:.*?)(?:跟进|沟通|联系|对接|发送|准备|整理)",
        r"(?:下一步|随后|之后)(?:.*?)(?:将|会)(?:.*?)(?:做|安排)",
    ]
    
    for line in segments:
        for pattern in todo_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                content = match.group(0).strip()
                if len(content) > 10 and len(content) < 50:
                    notes["todos"].append({
                        "content": content,
                        "assignee": "",
                        "deadline": "",
                        "priority": "中"
                    })
                    break
    
    # 如果没有提取到任何议题，提供一个默认议题
    if not notes["topics"]:
        notes["topics"].append({
            "title": "会议交流",
            "summary": "关于市场行情、投资策略、客户服务的讨论",
            "conclusion": "待进一步讨论",
            "owner": "会议组织者"
        })
    
    # 提取行动项
    if speakers:
        action_items.append("继续跟踪头部投顾的业绩表现和观点")
        action_items.append("加强与客户关于投资策略的沟通")
    notes["action_items"] = action_items[:8] if action_items else ["整理会议要点", "跟进后续事项"]
    
    return notes


# ─── 统一入口 ─────────────────────────────────────────────────────────────────
def generate_notes(text: str, meeting_info: dict = None) -> dict:
    """
    生成结构化会议纪要
    优先 LLM，失败时回退规则解析。
    """
    result = generate_notes_llm(text, meeting_info)
    if result is not None:
        return result
    print("使用规则解析生成纪要（内容可能较少）")
    return generate_notes_rule(text, meeting_info)


def main():
    parser = argparse.ArgumentParser(description="生成会议纪要")
    parser.add_argument("text_file", help="文本文件路径")
    parser.add_argument("--meeting-info", "-m", help="会议信息 JSON 字符串")
    parser.add_argument("--meeting-info-file", help="会议信息 JSON 文件路径")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument("--no-llm", action="store_true", help="强制使用规则解析，不调用 LLM")

    args = parser.parse_args()

    with open(args.text_file, "r", encoding="utf-8") as f:
        text = f.read()

    meeting_info = {}
    if args.meeting_info_file:
        try:
            with open(args.meeting_info_file, "r", encoding="utf-8") as f:
                meeting_info = json.load(f)
        except FileNotFoundError:
            print(f"警告：会议信息文件不存在: {args.meeting_info_file}")
        except json.JSONDecodeError:
            print("警告：会议信息文件 JSON 格式错误")
    elif args.meeting_info:
        try:
            meeting_info = json.loads(args.meeting_info)
        except json.JSONDecodeError:
            print("警告：会议信息 JSON 格式错误")

    if args.no_llm:
        notes = generate_notes_rule(text, meeting_info)
    else:
        notes = generate_notes(text, meeting_info)

    output = json.dumps(notes, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"纪要已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

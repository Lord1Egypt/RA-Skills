#!/usr/bin/env python3
"""项目评估助手 CLI"""
import argparse, os, sys, json, urllib.request
from datetime import datetime

API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

def call_llm(prompt):
    if not API_KEY:
        return "[错误] 请设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY"
    payload = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "你是一位资深产品顾问和创业评估专家，擅长从市场、技术、商业、风险四个维度评估项目可行性。请用中文输出，使用 Markdown 格式。"},
        {"role": "user", "content": prompt}
    ], "temperature": 0.7}).encode()
    req = urllib.request.Request(f"{API_BASE}/chat/completions", data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def build_prompt(idea, context=""):
    extra = f"\n\n补充信息：{context}" if context else ""
    return f"""请对以下项目想法进行全面评估。{extra}

项目描述：
{idea}

请按以下结构输出评估报告（Markdown格式）：

## 📊 综合评分

用表格输出四个维度评分（各10分）和综合评分，每项附一句简评。

## 🏆 市场维度
- 真实需求分析（是否有足够大的用户痛点）
- 市场规模估算
- 竞品分析（列出3-5个主要竞品，各一句话描述）
- 差异化机会

## 🔧 技术维度
- 技术可行性判断
- 主要技术挑战（列出3条）
- 推荐技术栈
- 开发工作量估算

## 💰 商业维度
- 盈利模式建议（至少2种）
- 获客路径
- 变现难度评估
- 关键指标（需要关注的核心数据）

## ⚠️ 风险维度
- 主要风险点（列出3-5条）
- 平台/政策依赖风险
- 竞争风险
- 缓解建议

## 🚀 MVP 建议
描述最小可行版本的核心功能（3条以内），以及建议的第一步行动。

## 📋 评估结论
用一段话给出最终建议：值得全力推进 / 值得验证后推进 / 谨慎评估 / 不建议。并说明最关键的一个决策因素。"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--idea", required=True, help="项目描述")
    parser.add_argument("--context", default="", help="补充信息（目标用户/资源约束等）")
    parser.add_argument("--output", help="输出文件路径")
    args = parser.parse_args()

    print("🤖 正在评估项目...")
    result = call_llm(build_prompt(args.idea, args.context))
    header = f"# 项目评估报告\n\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
    full = header + result

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full)
        print(f"✅ 报告已保存：{args.output}")
    else:
        print(full)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成面试题预测报告
用法:
  python3 generate_questions.py --jd "JD文本" --resume "简历文本"
  python3 generate_questions.py --jd /path/to/jd.txt --resume /path/to/resume.pdf
  python3 generate_questions.py --jd "JD文本" --resume "简历文本" --output /tmp/report.md
"""
import argparse
import os
import sys
import json
import urllib.request
from datetime import datetime

# ── API 配置 ──────────────────────────────────────────────
# 优先读环境变量，支持 OpenAI 兼容格式
API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")
# ─────────────────────────────────────────────────────────

def read_input(text_or_path: str) -> str:
    """如果是文件路径则读取，否则直接返回文本"""
    if os.path.exists(text_or_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parser_path = os.path.join(script_dir, "parse_file.py")
        import subprocess
        result = subprocess.run(
            [sys.executable, parser_path, text_or_path],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    return text_or_path.strip()

def call_llm(prompt: str) -> str:
    if not API_KEY:
        return "[错误] 请设置环境变量 OPENAI_API_KEY 或 DEEPSEEK_API_KEY"

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深HR和职业顾问，擅长分析岗位需求和简历，预测面试问题。请用中文回答。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]

def build_prompt(jd: str, resume: str) -> str:
    return f"""请根据以下岗位描述（JD）和简历，完成面试准备分析。

=== 岗位描述（JD）===
{jd[:3000]}

=== 个人简历 ===
{resume[:3000]}

请按以下结构输出完整分析报告（使用 Markdown 格式）：

## 📊 匹配度分析

给出 0-100% 的综合匹配度评分，并说明：
- ✅ 优势匹配项（列出3-5条，说明简历亮点如何对应JD要求）
- ⚠️ 待补强项（列出2-4条，指出简历与JD的差距）

## 📌 必问题（5题）

岗位通用高频题，几乎每次面试必问。每题包含：
- 题目
- 答题要点（2-3条）
- STAR框架提示

## 🎯 针对性题（5题）

根据该候选人简历与JD的具体差距生成，面试官会重点追问的薄弱点。每题包含：
- 题目（说明为什么会被问到）
- 建议答题策略
- 参考答案要点

## 🔍 追问题（5题）

针对简历中的亮点项目/经历，面试官可能深挖的细节问题。每题包含：
- 题目
- 针对的简历内容
- 参考回答思路

## 💡 备考建议

给出3-5条具体的备考策略，重点说明哪些方面需要重点准备。"""

def generate_report(jd_input: str, resume_input: str, output_path: str = None):
    print("📖 读取输入内容...")
    jd = read_input(jd_input)
    resume = read_input(resume_input)

    if not jd.strip():
        print("❌ JD 内容为空")
        sys.exit(1)
    if not resume.strip():
        print("❌ 简历内容为空")
        sys.exit(1)

    print(f"📝 JD 长度: {len(jd)} 字符")
    print(f"📝 简历长度: {len(resume)} 字符")
    print("🤖 调用 AI 生成面试题报告...")

    prompt = build_prompt(jd, resume)
    report = call_llm(prompt)

    # 加上标题和时间戳
    header = f"# 面试备考手册\n\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
    full_report = header + report

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_report)
        print(f"\n✅ 报告已保存：{output_path}")
    else:
        print("\n" + "="*60)
        print(full_report)

    return full_report

def main():
    parser = argparse.ArgumentParser(description="JD + 简历 → 面试题预测")
    parser.add_argument("--jd", required=True, help="JD 文本或文件路径")
    parser.add_argument("--resume", required=True, help="简历文本或文件路径")
    parser.add_argument("--output", help="输出文件路径（.md）")
    args = parser.parse_args()

    generate_report(args.jd, args.resume, args.output)

if __name__ == "__main__":
    main()

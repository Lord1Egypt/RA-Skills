"""
章节分析器 - 调用 DeepSeek 分析小说章节，识别旁白与对话

功能:
  1. 读取章节文本
  2. 调用 DeepSeek 分析文本结构
  3. 输出结构化分段: [{type, text, character, mood}]

用法:
  python scripts/chapter_analyzer.py --file "第一章.md"
  python scripts/chapter_analyzer.py --text "直接传入章节文本"

输出:
  JSON 数组，每段包含:
  - type: "title" | "narration" | "dialogue"
  - text: 分段文本
  - character: 角色名（对话时）/ null（旁白时）
  - mood: 该段落的情绪（平静/紧张/悲伤等）
"""

import argparse
import json
import sys
from pathlib import Path

import requests as req

SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config.json"


def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def read_file(file_path):
    """读取章节文件内容"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    return path.read_text(encoding="utf-8")


def build_deepseek_prompt(chapter_text):
    """
    构造发送给 DeepSeek 的分析提示词。
    DeepSeek 作为文本分析器，识别章节中的旁白和对话。
    """
    system_prompt = """你是一个小说章节分析器。你的任务是将章节文本按语义分段，并标注每段的类型。

输出格式为 JSON 数组:
[
  {
    "type": "narration 或 dialogue 或 title",
    "text": "该段文本内容",
    "character": null 或 "角色名",
    "mood": "该段情绪（平静/紧张/悲伤/欢快/悬疑等）"
  }
]

规则:
- title: 章节标题
- narration: 旁白/描述/叙述部分
- dialogue: 角色的对话（包含说话人标识）
  - 如 "林凡说：" 则 character 为"林凡"，text 只保留对话内容
  - 如对话前文已明确说话人，也要标注 character
- 相邻的同一角色对话合并为一段
- text 保留原始内容，对话部分要去掉引号但保留说话人标识前缀
- mood 根据文本内容判断情绪基调
"""

    user_prompt = f"请分析以下章节内容:\n\n{chapter_text}"
    return system_prompt, user_prompt


def call_deepseek(system_prompt, user_prompt, api_key, model="deepseek-chat"):
    """调用 DeepSeek API 分析文本"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,     # 较低温度，保证结构化输出稳定
        "max_tokens": 4096,
        "response_format": {"type": "json_object"},
    }

    resp = req.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"DeepSeek API 返回异常: HTTP {resp.status_code}\n{resp.text}")

    result = resp.json()
    content = result["choices"][0]["message"]["content"]

    # 尝试解析 JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # 如果被 ```json ``` 包裹，提取内容
        content = content.strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content)


def analyze_chapter(chapter_text, api_key, model="deepseek-chat"):
    """完整的章节分析流程"""
    system_prompt, user_prompt = build_deepseek_prompt(chapter_text)
    segments = call_deepseek(system_prompt, user_prompt, api_key, model)

    # 计算一些统计信息
    total_chars = len(chapter_text)
    dialogue_chars = sum(len(s["text"]) for s in segments if s["type"] == "dialogue")
    narration_chars = sum(len(s["text"]) for s in segments if s["type"] == "narration")
    characters = list(set(
        s["character"] for s in segments
        if s["type"] == "dialogue" and s.get("character")
    ))

    return {
        "segments": segments,
        "stats": {
            "total_chars": total_chars,
            "dialogue_ratio": round(dialogue_chars / total_chars * 100, 1) if total_chars > 0 else 0,
            "character_count": len(characters),
            "characters": characters,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="小说章节分析器")
    parser.add_argument("--file", help="章节文件路径")
    parser.add_argument("--text", help="直接传入章节文本")
    args = parser.parse_args()

    if not args.file and not args.text:
        print("错误: 必须提供 --file 或 --text", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    api_key = config.get("deepseek_api_key", "")
    if not api_key:
        print("错误: config.json 中未配置 deepseek_api_key", file=sys.stderr)
        sys.exit(1)

    # 读取文本
    if args.file:
        chapter_text = read_file(args.file)
    else:
        chapter_text = args.text

    # 分析章节
    model = config.get("deepseek_model", "deepseek-chat")
    result = analyze_chapter(chapter_text, api_key, model)

    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

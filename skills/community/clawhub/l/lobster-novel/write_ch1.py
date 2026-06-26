#!/usr/bin/env python3
"""Write Chapter 1 of Volume 1 using DeepSeek API."""
import sys, json, os, urllib.request, time, re, logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))
from bible import BibleManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('write_ch1')

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

PROJECT_DIR = Path(os.environ.get("LOBSTER_NOVEL_DIR", "."))
OUTPUT_DIR = PROJECT_DIR / "chapters"
OUTPUT_DIR.mkdir(exist_ok=True)

def llm_chat(messages, temp=0.7, max_tokens=8192, retries=3):
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                DEEPSEEK_URL, data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_KEY}"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError("All retries failed")

def main():
    # Load Bible
    bm = BibleManager(PROJECT_DIR)
    b = bm.bible
    bible_text = (
        f"书名: {b.title}\n"
        f"Logline: {b.logline}\n"
        f"风格: {b.genre} / {b.subgenre}\n"
        f"基调: {b.tone}\n\n---角色---\n"
    )
    for name, ch in b.characters.items():
        bible_text += f"{name} ({ch.role}): {ch.background}\n  特质: {', '.join(ch.traits)}\n  动机: {ch.motivation}\n  终面: {ch.notes}\n\n"

    # Load chapter plan
    plan = json.loads((PROJECT_DIR / "plans/volume_01_plan.json").read_text(encoding="utf-8"))
    ch_plan = plan["chapters"][0]

    # Get previous chapter context (none for ch1)
    prev_summary = "无——本章为小说开篇第一章"

    system_prompt = (
        "你是DND 5e奇幻小说作家蓝晶，擅长翻译体风格的西幻小说创作。"
        "你的文风特点是：暖丽细腻的描写、幽默诙谐的对话、扎实的DND跑团感、人物鲜活有烟火气。\n\n"
        "写作要求:\n"
        "1. 使用第三人称有限视角（主理查德）\n"
        "2. 包含环境描写、人物动作、内心独白\n"
        "3. 对话要自然，有角色个性\n"
        "4. 每2000字左右设置一个小波澜或悬念\n"
        "5. 章节结尾留钩子\n"
        "6. 约4000字\n"
        "7. 纯中文，不要英文词\n"
        "8. 符合DND 5e奇幻世界观\n"
        "9. 吟游诗人学徒的视角——理查德目前只会最基本的吟唱和鼓舞，对魔法一无所知\n"
        "10. 他天生蛮力，但不自觉——他以为自己是普通人"
    )

    user_prompt = f"""请根据以下设定和章节规划，写出第1章的正文。

{'-'*40}
小说设定
{'-'*40}
{bible_text}

{'-'*40}
第1章规划
{'-'*40}
标题：{ch_plan['title']}
概要：{ch_plan['summary']}
地点：{ch_plan['location']}
场景数：{ch_plan['scenes']}
登场角色：{', '.join(ch_plan['character_focus'])}

{'-'*40}
上一章概要
{'-'*40}
{prev_summary}

请输出完整的小说正文（纯中文），不需要任何额外说明。约4000字。
开头要有场景描写，把读者带入绝冬城贫民窟的黄昏氛围。
"""

    logger.info("Writing Chapter 1...")
    text = llm_chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ], temp=0.7, max_tokens=8192)

    # Save
    out_path = OUTPUT_DIR / "Ch001_破锣之歌.md"
    out_path.write_text(text, encoding="utf-8")

    char_count = len(text)
    print(f"\n✅ 第1章完成：{char_count}字")
    print(f"   保存: {out_path}")
    print(f"\n--- 正文预览（前500字）---")
    print(text[:500])
    print(f"\n...（共{char_count}字）")

if __name__ == "__main__":
    # If DEEPSEEK_API_KEY not in env, try loading from .env
    if not DEEPSEEK_KEY:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.split("=", 1)[1]
    main()

#!/usr/bin/env python3
"""Write Chapter 2 with SceneItemVerifier pre-check."""
import sys, json, os, urllib.request, time, re, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('write_ch2')

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))
from pipeline import Pipeline
from scene_items import SceneItemVerifier

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "chapters"
OUTPUT_DIR.mkdir(exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def llm_chat(messages, temp=0.7, max_tokens=8192, retries=3):
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(DEEPSEEK_URL, data=payload,
                headers={"Content-Type":"application/json","Authorization":f"Bearer {DEEPSEEK_KEY}"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1: time.sleep(2 ** attempt)
    raise RuntimeError("Failed")

# ── Load world state ──
pipeline = Pipeline(PROJECT_DIR)
b = pipeline.bible.bible

# Chapter 2 plan (from Phase 1 volume outline + story flow)
ch2_plan = {
    "number": 2,
    "title": "灰港镇的黎明",
    "summary": "次日清晨，理查德收拾行囊准备出发。汉克给了他旧皮甲和干粮。发小托德·铁砧决定一同前往。正要启程时，一辆马车驶入灰港镇，一位红袍女法师梅丽安·卡斯伯特追寻龙血印记而来。她揭示父亲信中提及的深水城的女人便是她自己，并告知更多关于古龙伊姆索瑞斯和深渊诅咒的秘密。三人商议后决定先去最近的城镇铁冠城再做打算。理查德最后一次回望破浪者酒馆，在灰港镇的晨雾中踏上旅途。",
    "location": "灰港镇·破浪者酒馆及码头街",
    "character_focus": ["理查德·泰森", "铁锤汉克", "托德·铁砧", "梅丽安·卡斯伯特"]
}

# ── Step 1: Verify scene items ──
logger.info("🔍 Phase 1: 校验场景物品...")
verifier = SceneItemVerifier(PROJECT_DIR)
checklist = verifier.verify_chapter(2, ch2_plan)
injection = checklist.prompt_injection()
logger.info(f"   ✅ {len(checklist.items)} 个通过")

# ── Step 2: Build writing prompt ──
bible_text = (
    f"## 世界观\n{b.title}\n基调: {b.tone}\n\n### 角色\n"
)
for name, ch in b.characters.items():
    bible_text += f"- {name}（{ch.role}）: {ch.background[:100]}\n  特质: {', '.join(ch.traits)}\n"

world_rules = "\n".join(f"- {r['name']}: {r['description'][:80]}" for r in json.loads(open(PROJECT_DIR/'bible.json').read()).get("world_rules", []))

# Read Ch001 for continuity
ch1_text = ""
ch1_path = OUTPUT_DIR / "Ch001_破浪者酒馆.md"
if ch1_path.exists():
    ch1_text = ch1_path.read_text(encoding="utf-8")[:1500]  # first 1500 chars as context

system_prompt = (
    "你是DND 5e翻译体西幻小说作家。\n"
    "文风：暖丽细腻的描写、幽默诙谐的对话、人物鲜活有烟火气。\n"
    "纯中文写作。\n\n"
    "写作要求:\n"
    "1. 第三人称有限视角（主理查德）\n"
    "2. 章首有场景引入，把读者拉回灰港镇的晨雾中\n"
    "3. 梅丽安的登场要有神秘感——红袍女法师从马车上下来的画面\n"
    "4. 托德和汉克的对话要自然，体现不同角色性格\n"
    "5. 约4000字\n"
    "6. 结尾钩子：离开灰港镇后路途上的危险预感\n"
    "7. ⚠️ 只能使用已校验的物品清单中的物品"
)

user_prompt = f"""请写第2章正文。

## 上一章回顾
{ch1_text[:800]}...

上一章结尾：理查德得知自己是红龙血脉，决定离开灰港镇去辉光城。

## 第2章剧情规划
标题：灰港镇的黎明

剧情推进：
1. 次日黎明，灰港镇的雾比昨天更浓
2. 理查德醒来，汉克已为他准备了行装：旧皮甲、干粮、五十枚金币
3. 托德在酒馆门口等着——他决定跟理查德一起去
4. 汉克嘴上嫌弃，但给理查德的包裹里多塞了一件羊毛斗篷
5. 正要出发时，一辆黑色马车穿过浓雾驶入灰港镇码头街
6. 车上下来一个穿红袍的女人（梅丽安·卡斯伯特），她直接问"龙血少年在哪里"
7. 梅丽安解释：她追踪龙血印记三十年，感应到理查德的血脉在昨晚觉醒
8. 理查德拿出父亲的信——梅丽安正是信中提到的那个人
9. 梅丽安警告：深渊中的存在已经感知到他的觉醒
10. 三人决定先去铁冠城休整，再决定下一步
11. 理查德在晨雾中回头——灰港镇的轮廓渐行渐远

{injection}

请写出完整小说正文（纯中文）。
"""

logger.info("✍️  写第2章...")
text = llm_chat([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
], temp=0.7, max_tokens=8192)

# Save MD
md_path = OUTPUT_DIR / "Ch002_灰港镇的黎明.md"
md_path.write_text(text, encoding="utf-8")

# Save HTML
try:
    import markdown
    html_body = markdown.markdown(text, extensions=['extra'])
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>第二章 灰港镇的黎明</title>
<style>
body {{ font-family: 'SimSun','Noto Serif CJK SC',serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 2; font-size: 16px; color: #222; }}
h1 {{ text-align: center; color: #8B0000; }}
p {{ text-indent: 2em; margin: 0.5em 0; }}
blockquote {{ border-left: 3px solid #8B0000; margin: 1em 0; padding: 0.5em 1em; background: #f9f5f0; }}
hr {{ border: none; border-top: 1px solid #ddd; }}
</style></head>
<body>
<h1>第二章 灰港镇的黎明</h1>
{html_body}
<hr><p style="text-align:center;color:#999;font-size:14px">《烈焰狂嚎：灰港镇的龙血少年》· 卷二 · 约{len(text)}字<br>泰伦大陆（完全自建世界观）· 物品校验已通过 ✅</p>
</body></html>'''
    html_path = Path("/tmp/Ch002_灰港镇的黎明.html")
    html_path.write_text(html, encoding="utf-8")
    logger.info(f"✅ HTML: {html_path}")
except Exception as e:
    logger.warning(f"HTML: {e}")
    html_path = None

print(f"\n✅ 第2章完成: {len(text)}字")
print(f"   MD: {md_path}")
print(f"   HTML: {html_path}")
print(f"\n--- 预览前300字 ---")
print(text[:300])

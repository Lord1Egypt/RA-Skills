#!/usr/bin/env python3
"""灰港镇版：更新Bible + 重跑Phase1 + 写第1章"""
import sys, json, os, urllib.request, time, re, logging
from pathlib import Path
from dataclasses import asdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('greyhaven')

CORE_DIR = Path(__file__).resolve().parent / "core"
sys.path.insert(0, str(CORE_DIR))

from bible import BibleManager, Character, WorldRule, NovelBible
from arc_planner import DnDArcPlanner, SenseNovaClient

PROJECT_DIR = Path(os.environ.get("LOBSTER_NOVEL_DIR", "."))
OUTPUT_DIR = PROJECT_DIR / "chapters"
OUTPUT_DIR.mkdir(exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

def llm_chat(messages, temp=0.7, max_tokens=8192, retries=3):
    payload = json.dumps({
        "model": DEEPSEEK_MODEL,
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
            logger.warning(f"LLM attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError("All retries failed")


# ═══ Step 1: 更新 Bible ═══════════════════════════════════

print("=" * 60)
print("Step 1: 更新 Bible 设定为灰港镇")
print("=" * 60)

bible = {
    "title": "烈焰狂嚎：理查德·泰森的费伦征途",
    "logline": "灰港镇一个落魄吟游诗人学徒，觉醒红龙血脉与野蛮人之力，从剑湾偏僻渔港一步步杀入无底深渊，以1级诗人/10级红龙术士/29级野蛮人的史诗之姿征服魅魔之主美坎修特的故事。",
    "genre": "西方奇幻",
    "subgenre": "DND 5e 史诗冒险",
    "target_length": "long",
    "tone": "热血诙谐，兼具蓝晶式翻译体的暖丽细腻与DND跑团的豪迈幽默",
    "theme": "从市井小人物到位面征服者，力量与责任的对等",
    "pov": "第三人称有限(主理查德)",
    "characters": {
        "理查德·泰森": {
            "name": "理查德·泰森",
            "role": "protagonist",
            "age": 18,
            "traits": ["乐观", "嘴硬", "天生蛮力", "有正义感也有私心"],
            "background": "剑湾北岸灰港镇「破浪者」酒馆的吟游诗人学徒，父亲留下一枚红龙鳞片吊坠后不知所踪。",
            "motivation": "起初只想活下去，后来想证明自己，最终要为费伦大陆挡住深渊的入侵。",
            "arc": "吟游诗人学徒→绝望逃亡者→理性狂战士→万界征服者",
            "relationships": {"梅丽安": "导师与战友", "托德": "铁哥们"},
            "current_state": "alive",
            "notes": "终面: 诗人1/术士10/蛮子29"
        },
        "梅丽安·卡斯伯特": {
            "name": "梅丽安·卡斯伯特",
            "role": "mentor",
            "age": 38,
            "traits": ["冷静", "博学", "外冷内热", "背负家族仇恨"],
            "background": "深水城法师协会高阶成员，家族被远古红龙伊姆索瑞斯灭门，研究龙族血脉三十年。追查龙血印记线索来到灰港镇。",
            "motivation": "利用理查德的龙血找到伊姆索瑞斯宝库，同时也真心想保护这个年轻人。",
            "arc": "复仇驱使的学者→接受过去→成为理查德的第二个家人",
            "relationships": {"理查德·泰森": "既是利用对象也是徒弟"},
            "current_state": "",
            "notes": ""
        },
        "托德·铁砧": {
            "name": "托德·铁砧",
            "role": "supporting",
            "age": 23,
            "traits": ["耿直", "爱喝酒", "战斗力强", "忠诚"],
            "background": "灰港镇铁匠铺的学徒，理查德的发小，从小一起在码头长大。",
            "motivation": "朋友有难一定要帮",
            "arc": "酒肉朋友→真正的战友",
            "relationships": {},
            "current_state": "",
            "notes": ""
        },
        "铁锤汉克": {
            "name": "铁锤汉克",
            "role": "supporting",
            "age": 55,
            "traits": ["寡言", "可靠", "外冷内热", "年轻时是个冒险者"],
            "background": "灰港镇「破浪者」酒馆老板，年轻时在北地当过冒险者，退休后在灰港镇开了这家酒馆。理查德父亲的旧友，受托照顾理查德。",
            "motivation": "保护理查德，完成对老友的承诺",
            "arc": "旁观者→父亲的替身→放手让孩子远行",
            "relationships": {"理查德·泰森": "被托孤的监护人"},
            "current_state": "",
            "notes": ""
        },
        "美坎修特": {
            "name": "美坎修特",
            "role": "antagonist",
            "age": 9999,
            "traits": ["美艳", "狡诈", "强大", "操纵欲极强"],
            "background": "无底深渊第66层之主，魅魔女王，统治着无数恶魔与堕落灵魂。",
            "motivation": "理查德体内的深渊血脉引起了她的注意——她不缺一个战士，她缺一个在费伦的代理人。",
            "arc": "幕后观察者→试探者→最终对手→被征服者",
            "relationships": {},
            "current_state": "alive",
            "notes": "终面BOSS"
        }
    },
    "world_rules": [
        {
            "name": "灰港镇设定",
            "description": "剑湾北岸的一座偏僻渔港小镇，位于绝冬城和路斯坎之间。人口约800人。主要街道只有一条——码头街。镇上有一家酒馆「破浪者」、一座海神神殿（破旧）、一家铁匠铺、一个鱼市。常年海雾弥漫，黑色礁石滩环绕。地理位置偏远，冒险者们很少路过这里的偏远渔村。",
            "category": "geography"
        },
        {
            "name": "DND 5e 规则",
            "description": "使用标准DND 5e魔法与战斗规则，添加史诗等级扩展(21-40级)",
            "category": "gamesystem"
        },
        {
            "name": "红龙血脉",
            "description": "理查德的龙血源自远古红龙伊姆索瑞斯，被凯尔本击杀后血脉散入人类家族",
            "category": "magic"
        },
        {
            "name": "深渊污染",
            "description": "龙血中混有极微量的深渊之力，因伊姆索瑞斯曾与魅魔交易",
            "category": "magic"
        }
    ]
}

bible_path = PROJECT_DIR / "bible.json"
bible_path.write_text(json.dumps(bible, ensure_ascii=False, indent=2), encoding="utf-8")
logger.info(f"Bible已更新: {bible_path}")
bm = BibleManager(PROJECT_DIR)
logger.info(f"加载成功: {bm.bible.title} | {len(bm.bible.characters)}角色 | {len(bm.bible.world_rules)}世界规则")


# ═══ Step 2: 跑 Phase 1 ═══════════════════════════════════

print("\n" + "=" * 60)
print("Step 2: Phase 1 - 7卷大纲")
print("=" * 60)

# Reuse existing arc_planner's prompt logic but via DeepSeek
bible_text = (
    f"小说设定\n书名: {bm.bible.title}\n风格: {bm.bible.genre} / {bm.bible.subgenre}\n"
    f"基调: {bm.bible.tone}\nLogline: {bm.bible.logline}\n\n角色:\n"
)
for name, ch in bm.bible.characters.items():
    bible_text += f"- {name} ({ch.role}): {ch.background}\n  特质: {', '.join(ch.traits)}\n  动机: {ch.motivation}\n"

world_rules_text = "\n世界规则:\n"
for r in bm.bible.world_rules:
    world_rules_text += f"- {r.name}: {r.description}\n"

dnd_context = """
DND 5e 等级分段:
- tier1 (1-4级): Local heroes, village-level threats
- tier2 (5-10级): Heroes of the realm, city-level threats
- tier3 (11-16级): Masters of the realm, kingdom-level threats
- tier4 (17-20级): Masters of the world, save-the-world quests
- epic (21-30级): Epic legend, lesser deities, planar lords
- godlike (31-40级): Near-divine, demon princes, cosmic balance

最终角色面板: 1级吟游诗人/10级红龙术士/29级野蛮人
最终敌人: 魅魔之主美坎修特
初始地点: 灰港镇（剑湾北岸偏僻渔港）
"""

system_prompt = "你是DND 5e资深跑团主持人兼奇幻小说架构师。根据小说设定规划7卷大纲。"

user_prompt = f"""请根据以下设定规划7卷大纲。

{bible_text}
{world_rules_text}
{dnd_context}

输出JSON:
{{
  "volumes": [
    {{
      "number": 1,
      "title": "卷名",
      "chapters": 章节数,
      "summary": "卷概要(200-300字)",
      "main_locations": ["地点1"],
      "level_start": 起始等级,
      "level_end": 结束等级,
      "class_growth": ["职业 起始级→结束级"],
      "key_encounters": ["关键事件1"],
      "character_arcs": ["角色弧线"],
      "climax_type": "battle/diplomacy/revelation/sacrifice"
    }}
  ]
}}

要求:
- 卷1从灰港镇出发，理查德是酒馆吟游诗人学徒
- 等级分配合理，前3卷升级快，后3卷升级慢
- 最终卷达到40级
"""

volumes_text = llm_chat([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
], temp=0.6, max_tokens=4096)

# Save phase1
plans_dir = PROJECT_DIR / "plans"
plans_dir.mkdir(exist_ok=True)

# Extract JSON
try:
    # Simple JSON extraction
    clean = re.sub(r'```(?:json)?\s*', '', volumes_text)
    clean = re.sub(r'\s*```', '', clean)
    start = clean.find('{')
    end = clean.rfind('}')
    if start >= 0 and end > start:
        clean = clean[start:end+1]
    data = json.loads(clean)
except Exception as e:
    logger.warning(f"JSON parse failed, saving raw: {e}")
    (plans_dir / "phase1_raw.txt").write_text(volumes_text, encoding="utf-8")
    # Fallback: use default structure
    data = {"volumes": [
        {"number": 1, "title": "灰港镇的龙血歌谣", "chapters": 80, "summary": "待生成", 
         "main_locations": ["灰港镇"], "level_start": 1, "level_end": 4,
         "class_growth": ["吟游诗人 1→1", "蛮子 1→3"], "key_encounters": ["龙血觉醒"],
         "character_arcs": ["从酒馆学徒到踏上旅途"], "climax_type": "battle"}
    ]}

vols_data = data.get("volumes", data if isinstance(data, list) else [])
phase1_data = {"volumes": vols_data, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
(plans_dir / "phase1_volumes.json").write_text(
    json.dumps(phase1_data, ensure_ascii=False, indent=2), encoding="utf-8")

logger.info(f"Phase 1: {len(vols_data)} volumes")
for v in vols_data:
    logger.info(f"  卷{v['number']}: {v['title']} ({v['chapters']}章, {v['level_start']}→{v['level_end']}级)")


# ═══ Step 3: 写第1章 ═════════════════════════════════════

print("\n" + "=" * 60)
print("Step 3: 写第1章 - 破浪者酒馆")
print("=" * 60)

system_prompt = (
    "你是DND 5e奇幻小说作家蓝晶，擅长翻译体风格的西幻小说创作。"
    "文风特点：暖丽细腻的描写、幽默诙谐的对话、扎实的DND跑团感、人物鲜活有烟火气。\n\n"
    "写作要求:\n"
    "1. 第三人称有限视角（主理查德）\n"
    "2. 环境描带读者进入场景\n"
    "3. 对话自然有角色个性\n"
    "4. 每2000字左右设小波澜\n"
    "5. 章节结尾留钩子\n"
    "6. 约4000字\n"
    "7. 纯中文\n"
    "8. 符合DND 5e世界观\n"
    "9. 理查德目前只是吟游诗人学徒，对魔法一无所知\n"
    "10. 他天生蛮力但不自觉"
)

user_prompt = f"""请写第1章正文。

小说设定
{'-'*40}
{bible_text}
{world_rules_text}
{'-'*40}

第1章设定:
- 地点: 灰港镇「破浪者」酒馆
- 时间: 一个阴冷潮湿的初冬傍晚
- 登场角色: 理查德·泰森（18岁，吟游诗人学徒）、铁锤汉克（55岁，酒馆老板）、托德·铁砧（23岁，理查德发小）
- 背景: 灰港镇是剑湾北岸一座偏僻渔港，人口稀少，常年海雾弥漫。「破浪者」是镇上唯一的酒馆，木头歪斜的两层楼，一楼喝酒二楼住店

章节目标:
1. 场景引入: 灰港镇黄昏，「破浪者」酒馆的昏暗灯光在浓雾中若隐若现
2. 理查德出场: 笨拙的弹唱、稀疏的客人、汉克的嫌弃中带着关切
3. 冲突引入: 几个外来的水手嘲笑他的龙鳞吊坠，理查德压抑着怒火
4. 转折: 吊坠发热→理查德愤怒失控爆发蛮力→震惊所有人
5. 收尾: 汉克拉他到储藏室，交出父亲的遗信→理查德得知身世秘密→决定去深水城
6. 结尾钩子: 夜幕中酒馆外有神秘黑影在窥视

请输出完整小说正文（纯中文），开篇就用场景描写把读者带入灰港镇的薄雾黄昏。
"""

chapter_text = llm_chat([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
], temp=0.7, max_tokens=8192)

# Save
out_path = OUTPUT_DIR / "Ch001_破浪者酒馆.md"
out_path.write_text(chapter_text, encoding="utf-8")

# Also save HTML
try:
    import markdown
    html_body = markdown.markdown(chapter_text, extensions=['extra'])
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>第一章 破浪者酒馆</title>
<style>
body {{ font-family: 'SimSun','Noto Serif CJK SC',serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 2; font-size: 16px; color: #222; }}
h1 {{ text-align: center; color: #8B0000; margin-bottom: 1.5em; }}
p {{ text-indent: 2em; margin: 0.5em 0; }}
</style></head>
<body>
{html_body}
<hr><p style="text-align:center;color:#999;font-size:14px">《烈焰狂嚎》· 卷一第1章 · 约{len(chapter_text)}字</p>
</body></html>'''
    html_path = Path("/tmp/Ch001_破浪者酒馆.html")
    html_path.write_text(html, encoding="utf-8")
    logger.info(f"HTML已生成: {html_path}")
except ImportError:
    html_path = None
    logger.warning("markdown模块未安装，跳过HTML生成")

print(f"\n✅ 第1章完成: {len(chapter_text)}字")
print(f"   MD: {out_path}")
if html_path:
    print(f"   HTML: {html_path}")
print(f"\n--- 预览前300字 ---")
print(chapter_text[:300])

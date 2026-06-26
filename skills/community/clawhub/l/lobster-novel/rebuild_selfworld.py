#!/usr/bin/env python3
"""全自建世界观：新Bible + Phase1 + 第1章重写"""
import sys, json, os, urllib.request, time, re, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('selfworld')

PROJECT_DIR = Path(os.environ.get("LOBSTER_NOVEL_DIR", "."))
OUTPUT_DIR = PROJECT_DIR / "chapters"
OUTPUT_DIR.mkdir(exist_ok=True)
plans_dir = PROJECT_DIR / "plans"
plans_dir.mkdir(exist_ok=True)

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
            req = urllib.request.Request(DEEPSEEK_URL, data=payload,
                headers={"Content-Type":"application/json","Authorization":f"Bearer {DEEPSEEK_KEY}"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"LLM attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError("All retries failed")


# ═══════════════════════════════════════════════════════════════
#  全自建世界观 Bible
# ═══════════════════════════════════════════════════════════════

WORLD_SUMMARY = """
## 泰伦大陆（Terran）世界观

### 地理
- 北方冰原：极寒冻土，野蛮人部落游牧之地
- 帝国腹地：人类王国「辉光帝国」，平原与森林交错，河流纵横
- 龙骨群岛：南海链状群岛，龙裔古迹散布，传说古代龙族在此陨落
- 深渊裂隙：世界尽头的巨裂缝，恶魔渗透的源头

### 重要地点
- 灰港镇（帝国北疆渔村，人口稀少，常年海雾弥漫）
- 铁冠城（帝国北疆最大城镇，铁矿山和佣兵公会所在地）
- 辉光城（帝国首都，法师协会总部，大图书馆所在地）
- 霜脊堡（北境冰原上的前哨要塞，野蛮人部落的交易点）
- 龙骨群岛（南海深处，古代龙族战场遗址，术士血脉的源头）
- 深渊裂隙（大陆西南端，千年前大战留下的空间裂缝）

### 力量体系（DND 5e 规则）
- 标准六属性、职业体系、魔法系统
- 附加史诗等级扩展（21-40级）
- 龙血术士：源自古代龙族血脉，家族传承
- 野蛮人狂怒：源自北方冰原的战斗传统
- 吟游诗人：学院派传承，有正式的音律魔法体系

### 历史背景
- 千年之前：巨龙之战，远古龙族几乎灭绝
- 五百年前：深渊裂隙首次打开，恶魔入侵被帝国联军击退
- 一百年前：裂隙再次异动，各大势力重新戒备
- 当今：裂隙封印开始松动，但普通人尚不知情
"""

# 完整 Bible JSON
bible = {
    "title": "烈焰狂嚎：灰港镇的龙血少年",
    "logline": "灰港镇一个落魄吟游诗人学徒，觉醒红龙血脉与野蛮人之力，从北疆渔村一步步踏入世界尽头的深渊裂隙，以1级诗人/10级红龙术士/29级野蛮人的史诗之姿，面对来自深渊的宿命之敌。",
    "genre": "西方奇幻",
    "subgenre": "DND 5e 史诗冒险（自建世界观）",
    "target_length": "long",
    "tone": "热血诙谐，兼具翻译体的暖丽细腻与DND跑团的豪迈幽默",
    "theme": "从市井小人物到位面征服者，力量与责任的对等",
    "pov": "第三人称有限（主理查德）",

    "world_rules": [
        {
            "name": "自建世界观：泰伦大陆",
            "description": "本小说使用完全自建的西幻世界观「泰伦大陆（Terran）」，与任何已有IP（包括被遗忘的国度、灰鹰、艾伯伦等）无关联。大陆地理、城市、人物、历史全部为原创。"
        },
        {
            "name": "灰港镇设定",
            "description": "帝国北疆的一座偏僻渔港小镇，位于辉光帝国最北端的海岸线上。人口约800人。主要街道只有一条——码头街。镇上设施：破浪者酒馆、灰港铁匠铺、海神小神殿（已废弃）、鱼市。常年海雾弥漫，黑色礁石滩环绕。北上的冒险者和商队很少在此停留，是个被世界遗忘的角落。"
        },
        {
            "name": "铁冠城设定",
            "description": "帝国北疆最大的城镇，距灰港镇约3天马程。以铁矿开采和佣兵公会闻名。城墙为黑色铁石所筑，城内有北地最大的竞技场。商业繁荣，各色人等汇聚。"
        },
        {
            "name": "辉光城设定",
            "description": "辉光帝国首都，位于帝国腹地。帝国法师协会总部所在地，城市以七座白色法师塔闻名。大图书馆收藏着大陆最完整的古龙文献。"
        },
        {
            "name": "深渊裂隙设定",
            "description": "位于大陆西南角炼狱山脉深处，千年前巨龙之战中撕裂的空间裂缝。恶魔从裂隙渗透到主位面已持续五百年。帝国在裂隙周围建立了「守望堡」要塞群，由帝国骑士团常年驻守。"
        },
        {
            "name": "龙血血脉设定",
            "description": "远古红龙伊姆索瑞斯——最后一头太古红龙，千年前陨落于龙骨群岛。它的血液散入数十个人类家族，形成了隐世的龙血血脉。血脉携带者拥有操纵火焰的天赋，力量会随着年龄和情绪波动逐渐觉醒。控制龙血需要严格的训练，失控会导致兽化。"
        },
        {
            "name": "DND 5e 规则",
            "description": "使用标准DND 5e魔法与战斗规则，附加史诗等级扩展（21-40级）。"
        }
    ],

    "characters": {
        "理查德·泰森": {
            "name": "理查德·泰森",
            "role": "protagonist",
            "age": 18,
            "traits": ["乐观", "嘴硬", "天生蛮力", "有正义感也有私心", "会弹鲁特琴但弹得很烂"],
            "background": "帝国北疆灰港镇「破浪者」酒馆的吟游诗人学徒。幼年被父亲遗弃在酒馆门口，只留下一枚红龙鳞片吊坠。由酒馆老板汉克抚养长大。",
            "motivation": "起初只想活下去，后来想证明自己，最终要为泰伦大陆挡住深渊的入侵。",
            "arc": "吟游诗人学徒→绝望逃亡者→理性狂战士→万界征服者",
            "relationships": {"梅丽安": "导师与战友", "托德": "铁哥们", "汉克": "养父般的存在"},
            "current_state": "alive",
            "notes": "终面：诗人1/术士10/蛮子29"
        },
        "梅丽安·卡斯伯特": {
            "name": "梅丽安·卡斯伯特",
            "role": "mentor",
            "age": 38,
            "traits": ["冷静", "博学", "外冷内热", "背负家族仇恨"],
            "background": "辉光城法师协会高阶成员。家族百年前遭龙血背叛者灭门，幸存者寥寥。她研究龙族血脉三十年，追踪一条龙血线索来到灰港镇。",
            "motivation": "利用理查德的龙血找到伊姆索瑞斯的遗产，也真心想保护这个年轻人。",
            "arc": "复仇驱使的学者→接受过去→成为理查德的第二个家人",
            "relationships": {"理查德·泰森": "既是利用对象也是徒弟"},
            "current_state": "",
            "notes": ""
        },
        "托德·铁砧": {
            "name": "托德·铁砧",
            "role": "supporting",
            "age": 23,
            "traits": ["耿直", "爱喝酒", "战斗技巧娴熟", "忠诚"],
            "background": "灰港镇铁匠铺的学徒，理查德的发小，从小一起在码头长大。父亲曾是帝国军团的铁匠。",
            "motivation": "朋友有难一定要帮",
            "arc": "酒肉朋友→真正的战友",
            "relationships": {"理查德·泰森": "最好的朋友"},
            "current_state": "",
            "notes": ""
        },
        "铁锤汉克": {
            "name": "铁锤汉克",
            "role": "supporting",
            "age": 55,
            "traits": ["寡言", "可靠", "外冷内热", "年轻时是个冒险者"],
            "background": "灰港镇「破浪者」酒馆老板。年轻时在北境当过雇佣兵，见过世面。二十多年前在酒馆门口捡到被遗弃的婴儿理查德，从此把他养大。",
            "motivation": "保护理查德，完成对老友（理查德之父）的承诺",
            "arc": "旁观者→父亲的替身→放手让孩子远行",
            "relationships": {"理查德·泰森": "养父般的存在"},
            "current_state": "",
            "notes": ""
        },
        "美坎修特": {
            "name": "美坎修特",
            "role": "antagonist",
            "age": 9999,
            "traits": ["美艳", "狡诈", "强大", "操纵欲极强"],
            "background": "深渊裂隙深处的恶魔领主。千年前被古龙伊姆索瑞斯封印，封印随龙族的陨落而松动。她察觉到了理查德体内龙血中的深渊之力——那是她千年前种下的诅咒。",
            "motivation": "利用理查德的力量挣脱最后封印，将泰伦大陆拖入深渊。",
            "arc": "幕后低语者→试探者→最终对手→被封印者",
            "relationships": {},
            "current_state": "被封印中",
            "notes": "终面BOSS"
        }
    }
}

# ── 写入 Bible ──
bible_path = PROJECT_DIR / "bible.json"
bible_path.write_text(json.dumps(bible, ensure_ascii=False, indent=2), encoding="utf-8")
logger.info(f"✅ Bible写入: {bible_path} ({len(bible['characters'])}角色, {len(bible['world_rules'])}条世界规则)")

# ── 生成世界设定文本 ──
world_text = (
    f"## 泰伦大陆世界观（完全自建）\n\n"
    f"书名: {bible['title']}\n"
    f"Logline: {bible['logline']}\n"
    f"基调: {bible['tone']}\n\n"
    f"### 地理\n"
    f"- 灰港镇: 帝国北疆偏僻渔村，人口约800，常年海雾\n"
    f"- 铁冠城: 帝国北疆重镇，铁矿和佣兵公会\n"
    f"- 辉光城: 帝国首都，法师协会和七塔图书馆\n"
    f"- 霜脊堡: 北境冰原前哨\n"
    f"- 龙骨群岛: 南海龙族古迹\n"
    f"- 深渊裂隙: 世界尽头的空间裂缝，恶魔渗透源头\n\n"
    f"### 世界规则（自建，与DND官方设定无关）\n"
)
for r in bible["world_rules"]:
    world_text += f"- {r['name']}: {r['description']}\n"

world_text += "\n### 角色\n"
for name, ch in bible["characters"].items():
    world_text += f"- {name}（{ch['role']}）: {ch['background']}\n  特质: {', '.join(ch['traits'])}\n"

logger.info("世界设定文本生成完毕")


# ═══════════════════════════════════════════════════════════════
#  Phase 1: 卷级大纲
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("🔄 Phase 1: 卷级大纲生成")
print("=" * 60)

system_prompt = (
    "你是DND 5e资深跑团主持人兼奇幻小说架构师。"
    "任务是规划一部完全原创的西幻小说的卷级大纲。\n\n"
    "小说设定：完全是作者自建的泰伦大陆世界观，与任何已有IP无关。\n"
    "你可以自由创作一切——大陆地理、城市名、历史事件——只要保持内部一致性即可。\n\n"
    "主角设定：1级吟游诗人/10级红龙术士/29级野蛮人的终面，从普通少年成长为史诗级英雄。"
    "前3卷重点在冒险和成长，后3卷面对深渊威胁。"
)

user_prompt = f"""请根据以下小说设定，规划7卷大纲。

{world_text}

DND 5e力量体系参考：
- tier1(1-4级): 村镇级威胁
- tier2(5-10级): 城市级威胁，巨龙/巨人级敌人
- tier3(11-16级): 王国级威胁，跨位面冒险
- tier4(17-20级): 拯救世界级威胁
- epic(21-30级): 史诗传奇，恶魔领主
- godlike(31-40级): 接近神级

重要等级里程碑：
- 卷1: 1→4级（基础觉醒）
- 卷2: 4→8级（城市冒险）
- 卷3: 8→13级（学府/学院线）
- 卷4: 13→18级（寻找力量之源）
- 卷5: 18→23级（全面战争）
- 卷6: 23→30级（深渊入侵）
- 卷7: 30→40级（最终决战）

输出JSON:
{{
  "volumes": [
    {{
      "number": 1,
      "title": "4-6字卷名",
      "chapters": 10-15,
      "summary": "200字卷概要",
      "main_locations": ["地点1"],
      "level_start": 1,
      "level_end": 4,
      "class_growth": ["职业 起始级→结束级"],
      "key_encounters": ["关键事件"],
      "character_arcs": ["角色弧线"],
      "climax_type": "battle/diplomacy/revelation/sacrifice"
    }}
  ]
}}

注意：
- 卷1从灰港镇开始，理查德是吟游诗人学徒，一无所知
- 卷1章节数不要超过80章，控制在10-15章即可
"""
vol_response = llm_chat([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
], temp=0.6, max_tokens=4096)

try:
    clean = re.sub(r'```(?:json)?\s*', '', vol_response)
    clean = re.sub(r'\s*```', '', clean)
    start = clean.find('{')
    end = clean.rfind('}')
    if start >= 0 and end > start:
        clean = clean[start:end+1]
    vol_data = json.loads(clean)
    vols = vol_data.get("volumes", [])
except Exception as e:
    logger.error(f"Phase 1 JSON解析失败: {e}")
    (plans_dir / "phase1_raw.txt").write_text(vol_response, encoding="utf-8")
    # fallback
    vols = [
        {"number": 1, "title":"灰港镇的龙焰", "chapters":12, "summary":"灰港镇的少年理查德·泰森在破浪者酒馆卖唱为生，龙血觉醒后踏上旅途。",
         "main_locations":["灰港镇"],"level_start":1,"level_end":4,"class_growth":["蛮子1→3","诗人1→1"],
         "key_encounters":["龙血觉醒"],"character_arcs":["从码头少年到觉醒者"],"climax_type":"battle"},
        {"number": 2,"title":"铁冠城的烈焰","chapters":14,"summary":"前往铁冠城。",
         "main_locations":["铁冠城"],"level_start":4,"level_end":8,"class_growth":["蛮子3→5","术士1→2"],
         "key_encounters":["佣兵公会"],"character_arcs":["学习控制龙血"],"climax_type":"battle"},
    ]

phase1 = {"volumes": vols, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
(plans_dir / "phase1_volumes.json").write_text(json.dumps(phase1, ensure_ascii=False, indent=2), encoding="utf-8")
logger.info(f"✅ Phase 1 完成: {len(vols)}卷")
for v in vols:
    logger.info(f"   卷{v['number']}: {v['title']} ({v['chapters']}章, {v['level_start']}→{v['level_end']}级)")


# ═══════════════════════════════════════════════════════════════
#  写第1章
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("✍️  写第1章: 破浪者酒馆")
print("=" * 60)

write_system = (
    "你是DND 5e翻译体西幻小说作家。\n"
    "文风特点：暖丽细腻的描写、幽默诙谐的对话、扎实的DND跑团感、人物鲜活有烟火气。\n"
    "纯中文写作，不出现英文词。\n\n"
    "写作要求:\n"
    "1. 第三人称有限视角（主理查德）\n"
    "2. 开篇要有强场景感——用环境描写把读者拉入灰港镇的薄雾黄昏\n"
    "3. 对话自然，有角色个性差异\n"
    "4. 章节结尾留钩子\n"
    "5. 约4000字\n"
    "6. 注意：这个世界是自建的，所有地名（灰港镇/铁冠城/辉光城）都是原创，与任何官方IP无关"
)

write_prompt = f"""请写第1章正文。

## 世界观背景（自建，非DND官方设定）
{bible['world_rules'][0]['description']}

## 地点
{bible['world_rules'][1]['description']}

## 角色
- 理查德·泰森（18岁）: {bible['characters']['理查德·泰森']['background']}
  特质: {', '.join(bible['characters']['理查德·泰森']['traits'])}
- 铁锤汉克（55岁）: {bible['characters']['铁锤汉克']['background']}
  特质: {', '.join(bible['characters']['铁锤汉克']['traits'])}
- 托德·铁砧（23岁）: {bible['characters']['托德·铁砧']['background']}
  特质: {', '.join(bible['characters']['托德·铁砧']['traits'])}

## 第1章剧情规划
标题：破浪者酒馆

剧情推进：
1. 场景：灰港镇初冬黄昏，浓雾笼罩，破浪者酒馆灯火在雾中摇曳
2. 理查德在酒馆弹唱卖艺，客人稀疏，汉克嫌弃他唱得难听但还是管他吃住
3. 几个从铁冠城来的外地佣兵嘲笑他的红龙鳞片吊坠是假货
4. 理查德强行压抑怒火——但他没注意到吊坠开始发热
5. 一个佣兵动手抢吊坠→理查德愤怒失控，单手将壮汉甩飞出去
6. 酒馆死寂，所有人都被震住了——理查德自己也不明白怎么回事
7. 汉克赶走佣兵，拉理查德进储藏室，叹了口气，把那封藏了十二年的信交给他
8. 信中揭示：他是红龙血脉的后裔，他父亲把他留在灰港镇是为了保护他
9. 信末提到：如果想控制力量，去辉光城找一个叫梅丽安的女人
10. 理查德决定明天就出发
11. 【钩子】窗外浓雾中有人影一闪而过——有人在监视

请写出完整的小说正文（纯中文，不包含任何额外说明）。
"""

ch1_text = llm_chat([
    {"role": "system", "content": write_system},
    {"role": "user", "content": write_prompt}
], temp=0.7, max_tokens=8192)

# Save MD
md_path = OUTPUT_DIR / "Ch001_破浪者酒馆.md"
md_path.write_text(ch1_text, encoding="utf-8")
logger.info(f"✅ 第1章MD保存: {md_path} ({len(ch1_text)}字)")

# Save HTML
try:
    import markdown
    html_body = markdown.markdown(ch1_text, extensions=['extra'])
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>第一章 破浪者酒馆</title>
<style>
body {{ font-family: 'SimSun','Noto Serif CJK SC',serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 2; font-size: 16px; color: #222; }}
h1 {{ text-align: center; color: #8B0000; margin-bottom: 1.5em; }}
p {{ text-indent: 2em; margin: 0.5em 0; }}
blockquote {{ border-left: 3px solid #8B0000; margin: 1em 0; padding: 0.5em 1em; background: #f9f5f0; }}
hr {{ border: none; border-top: 1px solid #ddd; }}
</style></head>
<body>
{html_body}
<hr><p style="text-align:center;color:#999;font-size:14px">《烈焰狂嚎：灰港镇的龙血少年》· 卷一第1章 · 约{len(ch1_text)}字<br>泰伦大陆（完全自建世界观）</p>
</body></html>'''
    html_path = Path("/tmp/Ch001_破浪者酒馆.html")
    html_path.write_text(html, encoding="utf-8")
    logger.info(f"✅ HTML生成: {html_path}")
except Exception as e:
    logger.warning(f"HTML生成失败: {e}")
    html_path = None

# Summary
print(f"\n{'='*60}")
print(f"✅ 全部完成！")
print(f"{'='*60}")
print(f"   Bible:       {bible_path}")
print(f"   Phase 1:     {len(vols)}卷")
for v in vols:
    print(f"     卷{v['number']}: {v['title']} ({v['chapters']}章, {v['level_start']}→{v['level_end']}级)")
print(f"   第1章:       {len(ch1_text)}字 → {md_path}")
if html_path:
    print(f"   HTML:       {html_path}")

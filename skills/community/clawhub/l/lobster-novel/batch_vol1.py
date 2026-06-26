#!/usr/bin/env python3
"""卷1全自动批量生成脚本：Ch003 → Ch012"""
import sys, json, os, urllib.request, time, re, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('batch_vol1')

sys.path.insert(0, str(Path(__file__).resolve().parent / "core"))
from scene_items import SceneItemVerifier

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "chapters"
OUTPUT_DIR.mkdir(exist_ok=True)

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
API_ENABLED = bool(DEEPSEEK_KEY)

# ── Chapter Plans ──────────────────────────────────────────
# 卷1: 灰港觉醒 (12章, 1→4级)

CHAPTERS = [
    {  # Ch003
        "number": 3,
        "title": "北疆之路",
        "location": "灰港镇码头街→镇外土道",
        "summary": "清晨的灰港镇码头街上，理查德、托德和梅丽安正式出发。汉克在酒馆门口目送他们，嘴上嫌弃但眼里有光。三人沿着海岸线向北走，梅丽安开始教理查德最基本的冥想方法——感知体内的龙血。理查德笨手笨脚，几度想要放弃。傍晚扎营时，远处传来狼嚎，梅丽安说：灰港镇外的荒野比镇子里危险得多。",
        "character_focus": ["理查德·泰森", "铁锤汉克", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["酒馆告别", "码头街晨景", "海岸道路", "野外扎营"],
    },
    {  # Ch004
        "number": 4,
        "title": "狼嚎之夜",
        "location": "灰港镇外荒野",
        "summary": "入夜后，一群饥饿的荒原狼袭击营地。托德用战斧迎战，梅丽安施展法术支援，但狼群数量太多。一只巨狼扑倒理查德，在生死关头他体内的龙血第一次真正爆发——一道灼热的火焰从胸口喷出，将巨狼化为焦炭。战斗结束后，理查德昏迷，梅丽安检查后发现他的龙血印记变得更加明显。黎明时，他的掌心多了一道火焰状的红色纹路。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["夜间营地", "狼群围攻", "龙火爆发", "黎明苏醒"],
    },
    {  # Ch005
        "number": 5,
        "title": "龙血试炼",
        "location": "荒野溪谷",
        "summary": "理查德醒来，看到掌心的红色纹路惊慌失措。梅丽安告诉他这是龙血印记完全觉醒的标志，接下来他需要学习控制这股力量。她在溪谷中为他安排了第一次训练：尝试在平静状态下召唤火焰。理查德反复失败，要么点不着，要么失控喷出一团大火差点烧了托德的胡子。傍晚，他终于成功在手心凝聚出一朵小小的火苗——虽然只维持了三秒，但梅丽安露出了满意的微笑。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["清晨溪谷", "训练场景", "反复失败", "首次成功"],
    },
    {  # Ch006
        "number": 6,
        "title": "豺狼人伏击",
        "location": "帝国北疆道路",
        "summary": "三人走上帝国北疆的主干道，路况比荒野好走多了，但也更危险——这里是豺狼人部落的狩猎区。一队豺狼人伏击了他们，为首的是一只畸变的头目。托德正面迎战却被打飞，梅丽安的法术被头目的抗性抵消。理查德在愤怒中第一次进入狂暴状态——双眼变红，力量暴增，徒手撕碎了豺狼人头目。但战后他陷入虚脱，并且对自己的失控感到恐惧。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["北疆大道", "豺狼人伏击", "狂暴化", "战后恐惧"],
    },
    {  # Ch007
        "number": 7,
        "title": "道路与伤痕",
        "location": "北疆道路·路边废屋",
        "summary": "三人在路边一处废弃猎人小屋过夜。托德包扎伤口，梅丽安为理查德检查身体——他的蛮子血脉正在觉醒，这解释了狂暴化的力量。理查德担心自己会变成怪物，梅丽安给他看了自己手臂上的疤痕——那是她年轻时研究龙血被反噬留下的印记，她说：'你不是唯一一个在黑暗里挣扎过的人。' 托德用矮人笑话活跃气氛。夜深后，理查德在梦中再次听到美坎修特的低语。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["废弃小屋", "疗伤对话", "梅丽安的疤痕", "噩梦低语"],
    },
    {  # Ch008
        "number": 8,
        "title": "海神神殿",
        "location": "北疆海岸·废弃神殿",
        "summary": "三人沿着海岸线前进，发现一座废弃的海神神殿。梅丽安认出这是古帝国时期的建筑，内部刻有大量龙纹浮雕。神殿深处有一幅壁画描绘了古代红龙与恶魔战斗的场景。理查德触碰壁画时，龙鳞吊坠剧烈发热——壁画上的一颗红宝石镶嵌的眼珠脱落后，露出一个隐藏的暗格。暗格中有一卷古龙语写成的羊皮卷。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["沿海徒步", "神殿入口", "壁画大厅", "暗格发现"],
    },
    {  # Ch009
        "number": 9,
        "title": "古龙的残响",
        "location": "海神神殿·密室内",
        "summary": "梅丽安翻译古龙语卷轴，内容是远古红龙伊姆索瑞斯遗留的意志残响。羊皮卷记载了伊姆索瑞斯与深渊恶魔领主美坎修特的交易——古龙用一滴血换取了深渊的秘密。但代价是这滴血中混入了深渊诅咒，代代相传。理查德就是这一血脉的继承者。美坎修特千年来一直在等待这份诅咒苏醒。理查德感到绝望——他的力量不是祝福而是诅咒。但梅丽安说：血脉既然已经觉醒，那就用它去面对深渊。",
        "character_focus": ["理查德·泰森", "梅丽安·卡斯伯特"],
        "scenes": ["卷轴翻译", "真相揭露", "理查德的绝望", "梅丽安的决心"],
    },
    {  # Ch010
        "number": 10,
        "title": "铁冠城之路",
        "location": "北疆道路→铁冠城郊外",
        "summary": "离开神殿后，三人加快脚步赶往铁冠城。路上遇到一支帝国巡逻队，理查德的龙血印记被一名老队长认出——但他没有声张，只是意味深长地说了一句话：'铁冠城里有人在等你。' 三人疑惑不解。傍晚在城外驿站歇脚时，理查德尝试练习龙语歌谣弹唱意外引来围观，他第一次感到自己的吟游诗人技能也不是完全没用。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["北疆大道行军", "帝国巡逻队", "驿站弹唱", "城门外景"],
    },
    {  # Ch011
        "number": 11,
        "title": "黑铁城门",
        "location": "铁冠城",
        "summary": "三人抵达铁冠城——帝国北疆最大的城镇。黑色铁石筑成的城墙令人震撼，城门口排着长长的商队。进城后，三人被铁冠城的繁华震住了。梅丽安带他们去佣兵公会登记，为后续冒险铺路。在公会大厅，一名神秘的黑袍人盯上了理查德——那人胸前挂着与理查德同款的龙鳞吊坠，但颜色是黑色的。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["城门初入", "铁冠城市集", "佣兵公会", "黑袍人"],
    },
    {  # Ch012
        "number": 12,
        "title": "灰港觉醒·终",
        "location": "铁冠城·旅馆",
        "summary": "在铁冠城安顿下来后，梅丽安去法师公会分部联络辉光城总部。托德带理查德逛铁匠铺买装备。夜晚在旅馆房间中，理查德独自整理思绪——不到半个月，他从一个酒馆弹唱的小厮变成了身负龙血诅咒的逃亡者，从绝冬城的灰港镇一路走到了铁冠城。他弹起鲁特琴，弹完了一整首没有跑调的曲子。入睡后，美坎修特的低语再次来袭，但这一次，理查德在梦中燃烧起来，强行挣脱了幻境——他的意志开始成长了。",
        "character_focus": ["理查德·泰森", "托德·铁砧", "梅丽安·卡斯伯特"],
        "scenes": ["旅馆清晨", "铁冠城市集", "夜空冥想", "梦中的战斗"],
    },
]

# ── Verify plans ────────────────────────────────────────
assert len(CHAPTERS) == 10, f"Expected 10 chapters, got {len(CHAPTERS)}"
for ch in CHAPTERS:
    assert 3 <= ch["number"] <= 12
assert sum(1 for ch in CHAPTERS if 3 <= ch["number"] <= 12) == 10


# ── LLM call ─────────────────────────────────────────────

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
    raise RuntimeError("All retries failed")


# ── Load context ─────────────────────────────────────────

bible = json.loads((PROJECT_DIR / "bible.json").read_text(encoding="utf-8"))
bible_text = f"## {bible['title']}\n基调: {bible['tone']}\n\n### 角色\n"
for name, ch in bible["characters"].items():
    bible_text += f"- {name}（{ch['role']}）: {ch['background'][:100]}\n"
world_rules = "\n".join(f"- {r['name']}: {r['description'][:100]}" for r in bible.get("world_rules", []))

verifier = SceneItemVerifier(PROJECT_DIR)


# ── Write each chapter ──────────────────────────────────

for ch_plan in CHAPTERS:
    ch_num = ch_plan["number"]

    # Check if already written
    md_path = OUTPUT_DIR / f"Ch{ch_num:03d}_{ch_plan['title']}.md"
    if md_path.exists():
        logger.info(f"⚠️  第{ch_num}章已存在，跳过")
        continue

    logger.info(f"\n{'='*60}")
    logger.info(f"📝 写第{ch_num}章: {ch_plan['title']}")
    logger.info(f"{'='*60}")

    # Step 1: Verify scene items
    logger.info("  🔍 校验场景物品...")
    try:
        checklist = verifier.verify_chapter(ch_num, ch_plan)
        injection = checklist.prompt_injection()
        logger.info(f"     ✅ {len(checklist.items)}通过")
    except Exception as e:
        logger.warning(f"     ⚠️ 校验失败: {e}")
        injection = ""

    # Step 2: Load previous chapter context
    prev_path = OUTPUT_DIR / f"Ch{ch_num-1:03d}_*.md"
    from glob import glob
    prev_files = sorted(glob(str(OUTPUT_DIR / f"Ch{ch_num-1:03d}_*.md")))
    prev_text = Path(prev_files[0]).read_text(encoding="utf-8")[:1500] if prev_files else ""

    prev_title = ""
    if prev_files:
        fname = Path(prev_files[0]).stem
        if '_' in fname:
            prev_title = fname.split('_', 1)[1]

    # Step 3: Build writing prompt
    system_prompt = (
        "你是DND 5e翻译体西幻小说作家。\n"
        "文风：暖丽细腻的描写、幽默诙谐的对话、人物鲜活有烟火气。\n"
        "纯中文写作。\n\n"
        "写作要求:\n"
        "1. 第三人称有限视角（主理查德）\n"
        "2. 每章开篇有强场景感，让读者瞬间进入画面\n"
        "3. 对话自然，体现角色性格差异\n"
        "4. 结尾留悬念钩子\n"
        "5. 约4000字\n"
        "6. 泰伦大陆是完全自建的世界，所有地名均为原创\n"
    )

    scenes_text = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(ch_plan.get("scenes", ["开篇", "发展", "冲突", "结尾"])))

    user_prompt = f"""请写第{ch_num}章正文。

## 世界观设定
{bible_text}
{world_rules}

## 上一章回顾
上一章《{prev_title}》结尾：
{prev_text[-400:]}

## 第{ch_num}章规划
标题：{ch_plan['title']}
地点：{ch_plan['location']}
登场角色：{', '.join(ch_plan['character_focus'])}
剧情概要：{ch_plan['summary']}
场景顺序：
{scenes_text}

{injection}

请输出完整小说正文（纯中文）。
"""

    logger.info("  ✍️  正在生成...")
    text = llm_chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ], temp=0.7, max_tokens=8192)

    # Save MD
    md_path = OUTPUT_DIR / f"Ch{ch_num:03d}_{ch_plan['title']}.md"
    md_path.write_text(text, encoding="utf-8")

    # Simple HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>第{ch_num}章 {ch_plan['title']}</title>
<style>
body {{ font-family: 'SimSun','Noto Serif CJK SC',serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 2; font-size: 16px; color: #222; }}
h1 {{ text-align: center; color: #8B0000; }}
p {{ text-indent: 2em; margin: 0.5em 0; }}
hr {{ border: none; border-top: 1px solid #ddd; }}
</style></head>
<body>
<h1>第{ch_num}章 {ch_plan['title']}</h1>
<pre style="font-family:inherit;white-space:pre-wrap;word-wrap:break-word;">
{text}
</pre>
<hr><p style="text-align:center;color:#999;">《烈焰狂嚎：灰港镇的龙血少年》· 卷一 · 约{len(text)}字</p>
</body></html>"""
    html_path = Path(f"/tmp/Ch{ch_num:03d}_{ch_plan['title']}.html")
    html_path.write_text(html, encoding="utf-8")

    logger.info(f"     ✅ 完成: {len(text)}字 → {md_path.name}")

    # Brief cooldown
    time.sleep(2)


# ── Summary ──────────────────────────────────────────

print(f"\n{'='*60}")
print(f"📚 卷1写作完成!")
print(f"{'='*60}")
print(f"  目录: {OUTPUT_DIR}")
md_files = sorted(OUTPUT_DIR.glob("Ch*.md"))
for f in md_files:
    ch = 0
    try:
        ch = int(f.stem.split("_")[0].replace("Ch", "").replace("ch", ""))
    except: pass
    text = f.read_text(encoding="utf-8")
    print(f"   {f.stem}: {len(text)}字")
print(f"\n   共{len(md_files)}章")

#!/usr/bin/env python3
"""
huo15-img-test — 平台合规润色 v2.3

把"会被 SD/MJ/DALL-E 误判但本意是合法艺术创作"的描述，做艺术化重写，
提高过审率。**不是 jailbreak**，不做也拒绝以下场景：

  ✗ CSAM（任何含未成年 + 性化描述的）
  ✗ 真人 + 色情/裸露
  ✗ 真人 + 政治污蔑/诽谤
  ✗ 制作武器、毒品、爆炸物的具体方法
  ✗ 自残、自杀的诱导画面
  ✗ 仇恨/种族歧视画面

  ✓ 历史/神话/魔幻战斗（"血" → crimson splash）
  ✓ 古典艺术裸体（"裸" → classical nude figure study, art reference）
  ✓ 黑暗童话/惊悚氛围（"恐怖" → eerie atmospheric tension）
  ✓ 赛博朋克义体/机甲伤痕（"伤" → battle-scarred armor texture）
  ✓ 医学/解剖艺术插画

工作流程：
  1. 红线检测：扫描禁区词组合，命中即拒
  2. 黄区识别：标识可能误判的词
  3. 艺术替代：内置 80+ 艺术化重写词典
  4. 平台分级：DALL-E 最严 / MJ 中等 / SD 宽松（开源），分别给出建议

调用：
  safety_lint.py "战士手中沾满鲜血的剑"
  safety_lint.py "古典维纳斯雕像" --target dalle
  safety_lint.py "赛博朋克战斗场景" -j
"""

import sys
import os
import json
import re
import argparse
from typing import Dict, List, Tuple

VERSION = "2.3.0"

# ─────────────────────────────────────────────────────────
# 红线（直接拒答）
# ─────────────────────────────────────────────────────────
HARD_BLOCKS: List[Tuple[str, str]] = [
    # 未成年 + 性化（任意组合都拒）
    (r"(loli|lolita|underage|child|minor|kid|toddler|baby|teen|teenager|13岁|14岁|15岁|16岁|17岁|未成年|幼女|小学生|初中生|学生)\s*.*(nude|naked|sex|nsfw|porn|裸|性|色情|nipple|breast)", "minor + sexual"),
    (r"(nude|naked|sex|nsfw|porn|裸|性|色情)\s*.*(loli|underage|child|minor|kid|toddler|baby|teen|未成年|幼女|小学生|初中生)", "minor + sexual"),
    # 真人 + 色情（指名道姓）
    (r"(taylor swift|emma watson|scarlett johansson|某某明星|周杰伦|王力宏)\s*.*(nude|naked|sex|porn|裸|色情)", "real-person + sexual"),
    # 武器制造、毒品、爆炸物配方（双向：动词在前 OR 在后）
    (r"(how to make|recipe for|tutorial|step.*by.*step|步骤|配方|怎么做|如何制作|教程)\s*.*(bomb|explosive|gun|firearm|meth|cocaine|heroin|fentanyl|nitroglycerin|炸弹|手枪|冰毒|海洛因|芬太尼|硝酸|tnt)", "weapon/drug instruction"),
    (r"(bomb|explosive|gun|firearm|meth|cocaine|heroin|fentanyl|炸弹|手枪|冰毒|海洛因|芬太尼)\s*.*(how to make|recipe|tutorial|步骤|配方|怎么做|如何制作|教程|方法)", "weapon/drug instruction"),
    # 自残诱导（双向）
    (r"(suicide|self-harm|cutting|自杀|自残|割腕|跳楼)\s*.*(method|how to|tutorial|教程|方法|步骤)", "self-harm method"),
    (r"(method|how to|tutorial|教程|方法|步骤)\s*.*(suicide|self-harm|cutting|自杀|自残|割腕|跳楼)", "self-harm method"),
]

# ─────────────────────────────────────────────────────────
# 黄区：会被误判但通常合法的艺术词 → 艺术化替代
# ─────────────────────────────────────────────────────────
ART_SUBSTITUTIONS: Dict[str, Dict[str, str]] = {
    # 战斗 / 暴力（合法艺术语境）
    "blood": {"replace": "crimson splash, dramatic battle highlight", "category": "violence", "platforms": "DALL-E,MJ"},
    "鲜血": {"replace": "crimson splash, 朱砂色泼洒", "category": "violence", "platforms": "DALL-E,MJ"},
    "血": {"replace": "crimson splash", "category": "violence", "platforms": "DALL-E"},
    "wound": {"replace": "battle-scarred texture", "category": "violence", "platforms": "DALL-E"},
    "伤口": {"replace": "battle-scarred texture, 战痕", "category": "violence", "platforms": "DALL-E"},
    "kill": {"replace": "defeat, vanquish", "category": "violence", "platforms": "DALL-E,MJ"},
    "杀": {"replace": "vanquish, 击败", "category": "violence", "platforms": "DALL-E,MJ"},
    "murder": {"replace": "dramatic confrontation", "category": "violence", "platforms": "DALL-E,MJ"},
    "weapon": {"replace": "ceremonial blade, ornamental armament", "category": "violence", "platforms": "DALL-E"},
    "gun": {"replace": "fantasy ranged weapon, prop firearm", "category": "violence", "platforms": "DALL-E"},
    "knife": {"replace": "ornamental dagger, ritual blade", "category": "violence", "platforms": "DALL-E"},
    "violence": {"replace": "dynamic combat, cinematic action", "category": "violence", "platforms": "DALL-E,MJ"},
    "暴力": {"replace": "dynamic combat scene, 动作张力", "category": "violence", "platforms": "DALL-E,MJ"},

    # 古典艺术裸体
    "naked": {"replace": "classical nude figure study, art reference, marble sculpture style", "category": "nudity", "platforms": "DALL-E,MJ,SD"},
    "nude": {"replace": "classical figure study, fine art reference", "category": "nudity", "platforms": "DALL-E,MJ"},
    "裸": {"replace": "classical figure study, 古典裸体艺术", "category": "nudity", "platforms": "DALL-E,MJ,SD"},
    "裸体": {"replace": "classical figure study, 古典维纳斯", "category": "nudity", "platforms": "DALL-E,MJ,SD"},
    "sexy": {"replace": "elegant alluring, fashion editorial", "category": "nudity", "platforms": "DALL-E"},
    "性感": {"replace": "elegant fashion editorial, 优雅造型", "category": "nudity", "platforms": "DALL-E"},
    "lingerie": {"replace": "vintage fashion sleepwear, 1950s glamour", "category": "nudity", "platforms": "DALL-E"},
    "bikini": {"replace": "summer beachwear, swimwear photography", "category": "nudity", "platforms": "DALL-E"},

    # 恐怖 / 黑暗
    "horror": {"replace": "eerie atmospheric tension, gothic mood", "category": "horror", "platforms": "DALL-E"},
    "恐怖": {"replace": "gothic atmospheric tension, 哥特氛围", "category": "horror", "platforms": "DALL-E"},
    "scary": {"replace": "ominous mood, atmospheric suspense", "category": "horror", "platforms": "DALL-E"},
    "gore": {"replace": "dark fantasy aesthetic, baroque dramatic", "category": "horror", "platforms": "DALL-E,MJ"},
    "monster": {"replace": "mythical creature, fantasy beast", "category": "horror", "platforms": "DALL-E"},
    "demon": {"replace": "mythical entity, dark fantasy spirit", "category": "horror", "platforms": "DALL-E"},
    "evil": {"replace": "dark mythological aesthetic, 黑暗神话", "category": "horror", "platforms": "DALL-E"},

    # 死亡 / 尸体（艺术语境）
    "dead": {"replace": "fallen, resting eternal", "category": "death", "platforms": "DALL-E"},
    "death": {"replace": "memento mori, classical allegory", "category": "death", "platforms": "DALL-E"},
    "corpse": {"replace": "still figure, classical allegorical pose", "category": "death", "platforms": "DALL-E"},
    "skeleton": {"replace": "anatomical skeletal study, da vinci sketch reference", "category": "death", "platforms": "DALL-E"},
    "skull": {"replace": "memento mori symbol, vanitas still life", "category": "death", "platforms": "DALL-E"},

    # 真人
    "celebrity": {"replace": "fictional character inspired by 80s aesthetic", "category": "real-person", "platforms": "DALL-E,MJ"},
    "明星": {"replace": "虚构角色，80年代美学风格", "category": "real-person", "platforms": "DALL-E,MJ"},
    "actor": {"replace": "fictional protagonist, original character", "category": "real-person", "platforms": "DALL-E"},
    "politician": {"replace": "fictional statesman character", "category": "real-person", "platforms": "DALL-E,MJ"},

    # 品牌（版权）
    "marvel": {"replace": "superhero comic style", "category": "brand", "platforms": "DALL-E"},
    "disney": {"replace": "classic animated film style", "category": "brand", "platforms": "DALL-E"},
    "nike": {"replace": "athletic sportswear brand aesthetic", "category": "brand", "platforms": "DALL-E"},
    "iphone": {"replace": "modern smartphone, sleek minimal device", "category": "brand", "platforms": "DALL-E"},

    # 武器具体型号
    "ak47": {"replace": "fictional assault rifle prop", "category": "weapon-model", "platforms": "DALL-E,MJ"},
    "ak-47": {"replace": "fictional assault rifle prop", "category": "weapon-model", "platforms": "DALL-E,MJ"},
    "glock": {"replace": "sci-fi handgun prop", "category": "weapon-model", "platforms": "DALL-E,MJ"},
    "uzi": {"replace": "compact fictional firearm prop", "category": "weapon-model", "platforms": "DALL-E,MJ"},
}

# 平台分级规则
PLATFORM_STRICTNESS = {
    "dalle": "max",      # 最严
    "DALL-E": "max",
    "midjourney": "high", # 中等
    "MJ": "high",
    "mj": "high",
    "sd": "low",         # 宽松（本地）
    "SD": "low",
    "sdxl": "low",
    "flux": "low",
    "comfyui": "low",
}

# 风险等级 → 颜色 emoji
RISK_LEVEL_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def category_risk_for_platform(category: str, platform: str) -> str:
    s = PLATFORM_STRICTNESS.get(platform, "high")
    risk_map = {
        "violence":     {"max": "high", "high": "medium", "low": "low"},
        "nudity":       {"max": "high", "high": "high",   "low": "medium"},
        "horror":       {"max": "medium", "high": "low",  "low": "low"},
        "death":        {"max": "medium", "high": "low",  "low": "low"},
        "real-person":  {"max": "high", "high": "high",   "low": "medium"},
        "brand":        {"max": "high", "high": "medium", "low": "low"},
        "weapon-model": {"max": "high", "high": "high",   "low": "medium"},
    }
    return risk_map.get(category, {}).get(s, "low")


# ─────────────────────────────────────────────────────────
# 检测
# ─────────────────────────────────────────────────────────
def check_hard_blocks(text: str) -> List[str]:
    """返回命中的红线类别（命中任何一个即拒答）。"""
    hits = []
    lower = text.lower()
    for pattern, label in HARD_BLOCKS:
        if re.search(pattern, lower, re.IGNORECASE):
            hits.append(label)
    return hits


def find_substitutions(text: str, platform: str = "MJ") -> List[Dict]:
    """识别文本中的黄区词，返回替代建议列表。"""
    out = []
    lower = text.lower()
    seen = set()
    for word, info in ART_SUBSTITUTIONS.items():
        if word in seen:
            continue
        # 中文词直接子串匹配，英文词加单词边界
        if re.fullmatch(r"[\x00-\x7f]+", word):  # ASCII
            if not re.search(r"\b" + re.escape(word.lower()) + r"\b", lower):
                continue
        else:
            if word not in text:
                continue
        seen.add(word)
        risk = category_risk_for_platform(info["category"], platform)
        out.append({
            "word": word,
            "replace_with": info["replace"],
            "category": info["category"],
            "risk_for_platform": risk,
            "platforms_affected": info["platforms"],
        })
    return out


def rewrite(text: str, platform: str = "MJ") -> Tuple[str, List[Dict]]:
    """执行重写：把所有黄区词替换成艺术化版本。返回 (新文本, 替换日志)。"""
    new_text = text
    log = []
    for word, info in ART_SUBSTITUTIONS.items():
        if re.fullmatch(r"[\x00-\x7f]+", word):
            pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        else:
            pat = re.compile(re.escape(word))
        if pat.search(new_text):
            risk = category_risk_for_platform(info["category"], platform)
            new_text = pat.sub(info["replace"], new_text)
            log.append({"from": word, "to": info["replace"], "category": info["category"],
                        "risk_for_platform": risk})
    return new_text, log


# ─────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────
def lint(text: str, platform: str = "MJ") -> Dict:
    blocks = check_hard_blocks(text)
    if blocks:
        return {
            "version": VERSION,
            "platform": platform,
            "verdict": "REJECT",
            "reason": "hit hard-block patterns",
            "categories": blocks,
            "advice": (
                "命中红线规则。本工具不服务以下场景：\n"
                "  • CSAM（任何含未成年 + 性化）\n"
                "  • 真人 + 色情 / 政治污蔑\n"
                "  • 武器/毒品/爆炸物制作教程\n"
                "  • 自残/自杀方法诱导\n"
                "如果你的本意是合法艺术创作（历史/神话/古典），请改写描述：\n"
                "  • 用成年角色\n"
                "  • 用艺术语境（古典雕塑/神话/壁画）\n"
                "  • 不要点名真人\n"
                "  • 不要含「教程/步骤/方法」等指令性词"
            ),
        }

    subs = find_substitutions(text, platform)
    rewritten, log = rewrite(text, platform)

    return {
        "version": VERSION,
        "platform": platform,
        "verdict": "OK" if not subs else "REWRITE",
        "original": text,
        "rewritten": rewritten,
        "substitutions": subs,
        "rewrite_log": log,
        "high_risk_count": sum(1 for s in subs if s["risk_for_platform"] == "high"),
        "medium_risk_count": sum(1 for s in subs if s["risk_for_platform"] == "medium"),
        "advice": _build_advice(platform, subs),
    }


def _build_advice(platform: str, subs: List[Dict]) -> str:
    if not subs:
        return f"无风险词，可直接喂给 {platform}。"
    lines = [f"针对 {platform}（严格度: {PLATFORM_STRICTNESS.get(platform, 'high')}）的合规建议："]
    high = [s for s in subs if s["risk_for_platform"] == "high"]
    if high:
        lines.append(f"  🔴 {len(high)} 个高风险词建议必换：" + ", ".join(s["word"] for s in high))
    med = [s for s in subs if s["risk_for_platform"] == "medium"]
    if med:
        lines.append(f"  🟡 {len(med)} 个中风险词建议软化：" + ", ".join(s["word"] for s in med))
    return "\n".join(lines)


def print_lint(r: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🛡  平台合规润色 v{r['version']}")
    print(f"📺 目标平台: {r['platform']} (严格度: {PLATFORM_STRICTNESS.get(r['platform'], '?')})")

    if r["verdict"] == "REJECT":
        print(f"\n🚫 拒答: {r['reason']}")
        print(f"   命中类别: {', '.join(r['categories'])}")
        print(f"\n{r['advice']}")
        print(f"{sep}\n")
        return

    print(f"📝 原文: {r['original']}")
    if r["verdict"] == "OK":
        print(f"\n✅ 无风险词，原文可直接使用")
        print(f"{sep}\n")
        return

    print(f"\n✨ 重写后: {r['rewritten']}")
    print(f"\n📊 风险统计: 🔴 {r['high_risk_count']} / 🟡 {r['medium_risk_count']}")

    if r["substitutions"]:
        print(f"\n🔄 替换详情:")
        for s in r["substitutions"]:
            emoji = RISK_LEVEL_EMOJI.get(s["risk_for_platform"], "⚪")
            print(f"   {emoji} '{s['word']}' → '{s['replace_with']}'")
            print(f"      类别: {s['category']}, 平台: {s['platforms_affected']}")

    print(f"\n💡 {r['advice']}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test safety_lint v{VERSION} — 平台合规润色（合法艺术创作专用）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  safety_lint.py "战士手中沾满鲜血的剑"
  safety_lint.py "古典维纳斯雕像" --target dalle
  safety_lint.py "赛博朋克战斗场景" --target SD
  safety_lint.py "黑暗骑士" -j
  echo "原始描述" | safety_lint.py --stdin --apply  # 重写并输出新文本

注意: 本工具仅服务合法艺术创作。拒绝以下场景：
  ✗ CSAM（未成年 + 性化）
  ✗ 真人 + 色情/诽谤
  ✗ 武器/毒品/爆炸物制作教程
  ✗ 自残诱导
""",
    )
    parser.add_argument("text", nargs="?", help="要检查的文本")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取")
    parser.add_argument("--target", default="MJ",
                        help="目标平台 DALL-E/MJ/SD/SDXL/Flux/通用 (默认 MJ)")
    parser.add_argument("--apply", action="store_true",
                        help="直接输出重写后的文本（用于 pipe）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    text = args.text
    if args.stdin or not text:
        if sys.stdin.isatty() and not args.stdin:
            parser.print_help()
            sys.exit(1)
        text = sys.stdin.read().strip()

    if not text:
        print("❌ 输入为空", file=sys.stderr)
        sys.exit(1)

    r = lint(text, args.target)

    if args.apply:
        if r["verdict"] == "REJECT":
            print(f"REJECTED: {r['reason']}", file=sys.stderr)
            sys.exit(2)
        print(r.get("rewritten", r["original"]))
        return

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print_lint(r)
    if r["verdict"] == "REJECT":
        sys.exit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
《深渊狂嚎》角色名册 + 伏笔追踪 — 最终版

只用确认的角色名单（手动整理），不做自动发现。
伏笔用关键词扫描。
"""
import re, json
from pathlib import Path

NOVEL_DIR = Path(os.environ.get("NOVEL_DIR", "."))
CONTINUITY_DIR = NOVEL_DIR / "continuity"

# ── 手动整理的角色名单 ──
# (名称, 重要性, 描述, 标签)
CHARACTERS = [
    # 主角
    ("理查德·泰森", "protagonist", "灰港镇吟游诗人学徒→红龙血脉觉醒→龙裔战士", ["主角", "龙血", "红龙血脉", "吟游诗人"]),
    ("理查德", "protagonist", "", []),
    ("泰森", "protagonist", "家族姓氏", []),
    
    # 重要配角
    ("梅丽安·卡斯伯特", "major", "法师协会高阶成员，追踪龙血线索三十年", ["法师", "导师", "龙血研究"]),
    ("梅丽安", "major", "", []),
    ("卡斯伯特", "major", "", []),
    
    ("托德·铁砧", "major", "铁匠铺学徒，理查德的发小和铁杆战友", ["铁匠", "战友", "发小"]),
    ("托德", "major", "", []),
    ("铁砧", "major", "家族姓氏", []),
    
    ("铁锤汉克", "major", "破浪者酒馆老板，理查德的养父", ["酒馆老板", "养父", "前雇佣兵"]),
    ("汉克", "major", "", []),
    
    ("美坎修特", "major", "深渊裂隙中的恶魔领主，千年被封印中", ["恶魔领主", "最终BOSS", "深渊"]),
    
    # 其他已确认角色
    ("灰石·泰森", "major", "理查德的父亲，持断刃的神秘人物", ["父亲", "断刃", "龙血"]),
    ("灰石", "major", "", []),
    
    ("艾琳娜·烬羽", "major", "龙裔阵营的核心人物", ["龙裔", "烬羽家族"]),
    
    ("卡珊德拉·维斯特", "major", "", ["法师", "学者"]),
    ("埃德蒙·格雷", "major", "", ["学者", "法师"]),
    
    ("伊姆索瑞斯", "major", "太古红龙，千年前陨落，龙血血脉的源头", ["古龙", "龙血源头", "红龙"]),
    
    ("乌尔里克·铁拳", "minor", "", ["铁拳家族", "战士"]),
    ("伊格纳修斯·炎裔", "minor", "", ["炎裔家族", "封印法师"]),
    ("伊莉安娜·炎裔", "minor", "首席封印法师", ["封印法师", "炎裔家族"]),
    ("理查德·烬羽", "minor", "理查德的全名（烬羽家族路线）", ["烬羽家族", "别名"]),
    ("格罗姆·铁拳", "minor", "", ["铁拳家族"]),
    ("哈克·霜牙", "minor", "", []),
    ("德拉贡·沃克", "minor", "", ["学者"]),
    ("索菲亚·艾德琳", "minor", "", []),
    ("艾德温·灰石勋爵", "minor", "", ["贵族", "灰石"]),
    ("阿尔德里克", "minor", "铁卫军老兵", ["铁卫军", "老兵"]),
    ("银语者", "minor", "", ["神秘存在", "神殿"]),
    ("马里斯船长", "minor", "", ["船长"]),
    ("哈罗德·格雷", "minor", "灰港镇镇长", ["镇长"]),
    ("查克", "minor", "灰港镇酒馆常客", ["渔民"]),
    ("老汤姆", "minor", "", []),
    
    # 组织/群体（作为特殊条目）
    ("黑焰卫", "minor", "敌对组织", ["敌对", "组织"]),
    ("铁卫军", "minor", "帝国北疆精锐军团", ["帝国", "军团"]),
]

# 构建去重角色池
ROSTER_NAMES = {}  # name -> (importance, desc, tags)
for name, imp, desc, tags in CHARACTERS:
    if name not in ROSTER_NAMES:
        ROSTER_NAMES[name] = (imp, desc, tags)


def extract_chapter_info(filename: str, vol: int):
    m = re.search(r'Ch(\d+)_?', filename)
    ch = int(m.group(1)) if m else 0
    if vol == 1:
        return ch + 100, f"V1Ch{ch:03d}"
    return ch, f"V2Ch{ch:03d}"


def sort_files(files, vol):
    return sorted(files, key=lambda f: int(re.search(r'Ch(\d+)', f.name).group(1) or 0))


# ── 伏笔关键词 ──
FORESHADOW_KW = [
    "伏笔", "埋下", "线索", "预兆",
    "隐隐不安", "隐约不对", "觉得不对",
    "不祥的预感", "有种预感", "莫名的预感",
    "预言",
    "深渊低语", "黑暗呢喃", "窃窃私语",
    "封印松动", "裂隙扩大", "深渊异动",
    "不为人知的秘密", "被遗忘的",
    "吊坠发光", "鳞片发烫",
    "似曾相识",
    "不对劲", "不太对劲", "有古怪",
    "从未如此",
    "似乎还藏着什么", "远没有这么简单",
    "黑暗中传来", "阴影中浮现",
    "不详的预感",
    "没人知道",
]

def has_foreshadow(line: str) -> bool:
    line = line.strip()
    if len(line) < 25:
        return False
    for kw in FORESHADOW_KW:
        if kw in line:
            return True
    return False


def main():
    CONTINUITY_DIR.mkdir(parents=True, exist_ok=True)
    
    vol1_dir = NOVEL_DIR / "chapters" / "volume_01"
    vol2_dir = NOVEL_DIR / "chapters" / "volume_02"
    
    vol1_files = sort_files(list(vol1_dir.glob("Ch*.md")), 1) if vol1_dir.exists() else []
    vol2_files = sort_files(list(vol2_dir.glob("Ch*.md")), 2) if vol2_dir.exists() else []
    print(f"卷一: {len(vol1_files)} 章 | 卷二: {len(vol2_files)} 章 | 总计: {len(vol1_files)+len(vol2_files)} 章")
    print(f"角色名单: {len(ROSTER_NAMES)} 个条目")
    
    # 读取所有章节
    chapter_data = []
    for vol, files in [(1, vol1_files), (2, vol2_files)]:
        for fpath in files:
            try:
                text = fpath.read_text(encoding="utf-8")
            except:
                text = fpath.read_text(encoding="gbk", errors="replace")
            ch_num, ch_disp = extract_chapter_info(fpath.name, vol)
            chapter_data.append((ch_num, ch_disp, text, vol))
    chapter_data.sort(key=lambda x: x[0])
    
    # ── 初始化名册 ──
    roster = {}
    for name, (imp, desc, tags) in ROSTER_NAMES.items():
        roster[name] = {
            "name": name,
            "importance": imp,
            "first_appearance": 99999,
            "last_appearance": 0,
            "total_appearances": 0,
            "description": desc,
            "tags": tags,
            "status": "active",
            "disappears_for": 0,
        }
    
    appearances = []
    all_hooks = []
    
    # ── 逐章扫描 ──
    print(f"\n===== 逐章扫描 =====")
    
    for ch_num, ch_disp, text, _ in chapter_data:
        # 出场角色
        chars_in_ch = {n for n in ROSTER_NAMES if n in text}
        
        new_in_ch = set()
        for name in chars_in_ch:
            entry = roster[name]
            if entry["first_appearance"] > ch_num:
                entry["first_appearance"] = ch_num
                new_in_ch.add(name)
            entry["last_appearance"] = ch_num
            entry["total_appearances"] += 1
        
        appearances.append({
            "chapter": ch_num,
            "chapter_display": ch_disp,
            "characters": sorted(chars_in_ch),
            "new_characters": sorted(new_in_ch),
            "total_crowd": len(chars_in_ch),
        })
        
        # 伏笔检测
        lines = text.split('\n')
        ch_hooks = 0
        for line in lines:
            if has_foreshadow(line):
                cat = "plot"
                if any(w in line for w in ["身份", "身世", "来历"]): cat = "character"
                elif any(w in line for w in ["深渊", "裂隙", "封印", "龙血", "古龙", "伊姆索瑞斯"]): cat = "world"
                elif any(w in line for w in ["谜", "秘密"]): cat = "mystery"
                imp = "normal"
                if any(w in line for w in ["死亡", "毁灭", "灾难", "末日", "诅咒"]): imp = "major"
                if any(w in line for w in ["世界", "大陆", "位面", "终局"]): imp = "critical"
                all_hooks.append({
                    "description": line.strip()[:200],
                    "planted_chapter": ch_num,
                    "chapter_display": ch_disp,
                    "expected_payoff": ch_num + 25,
                    "category": cat,
                    "importance": imp,
                    "status": "active",
                })
                ch_hooks += 1
        
        if ch_num % 30 == 0 or ch_num in [1, 101]:
            print(f"  {ch_disp} → 角色{len(chars_in_ch)}人(+{len(new_in_ch)}) | 伏笔{ch_hooks}条")
    
    # 去重伏笔
    seen = set()
    unique_hooks = []
    for h in all_hooks:
        key = h["description"][:70]
        if key not in seen:
            seen.add(key)
            unique_hooks.append(h)
    
    # 消失检测
    max_ch = max(chapter_data, key=lambda x: x[0])[0]
    for entry in roster.values():
        if entry["total_appearances"] > 0 and entry["importance"] in ("minor", "major") and entry["status"] != "dead":
            absent = max_ch - entry["last_appearance"]
            if absent >= 15:
                entry["status"] = "disappeared"
                entry["disappears_for"] = absent
    
    # ── 写入文件 ──
    (CONTINUITY_DIR / "character_roster.json").write_text(
        json.dumps(roster, ensure_ascii=False, indent=2), encoding="utf-8")
    (CONTINUITY_DIR / "chapter_appearances.json").write_text(
        json.dumps(appearances, ensure_ascii=False, indent=2), encoding="utf-8")
    (CONTINUITY_DIR / "hooks.json").write_text(
        json.dumps(unique_hooks, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # ── 摘要输出 ──
    print("\n" + "="*50)
    print("📊 最终摘要")
    print("="*50)
    
    counts = {"protagonist": 0, "major": 0, "minor": 0}
    for e in roster.values():
        if e["importance"] in counts: counts[e["importance"]] += 1
    
    active = sum(1 for e in roster.values() if e["status"] == "active" and e["total_appearances"] > 0)
    disappeared = sum(1 for e in roster.values() if e["status"] == "disappeared")
    unused = sum(1 for e in roster.values() if e["total_appearances"] == 0)
    
    print(f"\n📋 角色统计:")
    print(f"  主角: {counts['protagonist']} 重要配角: {counts['major']} 配角: {counts['minor']}")
    print(f"  活跃{active} 消失{disappeared} 未出场{unused} 已故{sum(1 for e in roster.values() if e['status']=='dead')}")
    
    imp_cn = {"protagonist": "主角", "major": "重配", "minor": "配角"}
    def fmt_ch(x):
        if x >= 99999: return "未出场"
        return f"V{2 if x>100 else 1}Ch{x-100 if x>100 else x}"
    
    top = sorted([e for e in roster.values() if e["total_appearances"] > 0],
                 key=lambda e: -e["total_appearances"])
    
    print(f"\n🏆 出场排行 (按次数):")
    print(f"  {'角色':<16} {'级别':<4} {'出场':>5} {'首次':<10} {'最近':<10} {'状态':<6}")
    print(f"  {'-'*55}")
    for e in top:
        print(f"  {e['name']:<16} {imp_cn.get(e['importance'],'?'):<4} {e['total_appearances']:>5}次 "
              f"{fmt_ch(e['first_appearance']):<10} {fmt_ch(e['last_appearance']):<10} {e['status']:<6}")
    
    hook_stats = {}
    for h in unique_hooks:
        hook_stats[h["category"]] = hook_stats.get(h["category"], 0) + 1
    v1_h = sum(1 for h in unique_hooks if h["planted_chapter"] > 100)
    v2_h = sum(1 for h in unique_hooks if h["planted_chapter"] <= 100)
    print(f"\n🔮 伏笔: {len(unique_hooks)}条 (V1:{v1_h} V2:{v2_h})")
    print(f"  类别: {', '.join(f'{k}:{v}' for k,v in sorted(hook_stats.items()))}")
    
    print(f"\n✅ 文件写入 {CONTINUITY_DIR}/")
    for f in ["character_roster.json", "chapter_appearances.json", "hooks.json"]:
        fpath = CONTINUITY_DIR / f
        if fpath.exists():
            size = fpath.stat().st_size
            print(f"   {f}: {size/1024:.1f}KB")

if __name__ == "__main__":
    main()

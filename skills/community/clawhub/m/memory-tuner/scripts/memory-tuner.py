#!/usr/bin/env python3
"""memory-tuner: 统计 MEMORY.md 条目读取热度（只读分析，默认不改文件）。

用法:
  python3 memory-tuner.py                  # 报告（dry-run，默认 lfu 策略）
  python3 memory-tuner.py --policy lru     # 淘汰候选按 lru 排序
  python3 memory-tuner.py --policy lfu     # 淘汰候选按 lfu 排序（默认）
  python3 memory-tuner.py --mark           # 报告 + 在冷/冻条目上加 <!-- cold/frozen --> 注释
  python3 memory-tuner.py --json           # 机器可读

分级阈值与容量水位见常量。需要 Python 3.8+。
"""

import argparse
import datetime as dt
import json
import os
import re

# ---- 阈值配置 ----
COLD_DAYS = 30        # 超过 N 天无命中 → cold 候选
FROZEN_DAYS = 60      # 超过 N 天无命中 → frozen 候选
NEW_GRACE_DAYS = 14   # 新条目冷却期，不判冷（配合 untracked 人工复核）
USE_WEIGHT = 2        # use 命中权重
SEARCH_GET_WEIGHT = 1 # search/get 命中权重

# ---- 容量水位（Redis allkeys 式淘汰）----
MAX_ITEMS = 30          # 条目数上限，超过则按 policy 生成淘汰候选
MAX_BYTES = 8 * 1024    # MEMORY.md 体积上限（字节）
DEFAULT_POLICY = "lfu"  # lru: 最久未读先淘汰 | lfu: 引用最少先淘汰

# ---- 路径 ----
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE") or os.path.expanduser("~/.openclaw/workspace")
MEMORY_MD = os.path.join(WORKSPACE, "MEMORY.md")
TRACK_DIR = os.path.join(WORKSPACE, "memory", ".track")


def norm_key(s: str) -> str:
    """模糊归一化：去空白/标点/大小写，用于包含匹配。"""
    return re.sub(r"[\W_]+|[-—–]+", "", s).lower()


def parse_memory(path: str):
    """解析 MEMORY.md → [{section, key, raw, line, flags}]"""
    items = []
    cur_section = ""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        m = re.match(r"^##\s+(.+)\s*$", line)
        if m:
            cur_section = m.group(1).strip()
            continue
        if line.lstrip().startswith("- "):
            bullet = line.strip()
            bm = re.match(r"^- \*\*(.+?)\*\*", bullet)
            key = bm.group(1) if bm else bullet[2:].split("：")[0].split(":")[0][:40]
            flags = set(re.findall(r"<!--\s*(\w+)\s*-->", line))
            items.append({"section": cur_section, "key": key, "raw": bullet,
                          "line": i, "flags": flags})
    return items


def parse_track(track_dir: str):
    """读取 memory/.track/*.md → [(date, key, source)]，按文件内行序。"""
    rows = []
    if not os.path.isdir(track_dir):
        return rows
    for fn in sorted(os.listdir(track_dir)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(track_dir, fn), encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}", parts[0]):
                    rows.append((parts[0][:10], parts[1], parts[2].lower()))
    return rows


def match_key(key: str, norm_key_map: dict, norm_items: list) -> int:
    """返回命中的条目 index（模糊包含匹配），找不到返回 -1。"""
    nk = norm_key(key)
    if nk in norm_key_map:
        return norm_key_map[nk]
    # 包含匹配：track key 出现在条目 key 里，或反之
    for i, (ik, isec) in enumerate(norm_items):
        if nk and (nk in ik or ik in nk or nk in isec or (isec and isec in nk)):
            return i
    return -1


def analyze(items, rows, today):
    norm_items = [(norm_key(i["key"]), norm_key(i["section"])) for i in items]
    norm_key_map = {nk: idx for idx, (nk, _) in enumerate(norm_items) if nk}
    stats = [{"hits": 0, "hits_30d": 0, "hits_90d": 0,
              "last_hit": None, "sources": set(), "score": 0.0} for _ in items]
    for date, key, src in rows:
        idx = match_key(key, norm_key_map, norm_items)
        if idx < 0:
            continue
        s = stats[idx]
        w = USE_WEIGHT if src == "use" else SEARCH_GET_WEIGHT
        s["hits"] += 1
        s["score"] += w
        s["sources"].add(src)
        d = dt.date.fromisoformat(date)
        if (today - d).days <= 30:
            s["hits_30d"] += 1
        if (today - d).days <= 90:
            s["hits_90d"] += 1
        if s["last_hit"] is None or d > s["last_hit"]:
            s["last_hit"] = d
    return stats


def grade(item, s, today):
    """分级：keep 常青；近期有命中 hot；有记录但久未命中 cold/frozen；无记录 untracked。"""
    if "keep" in item["flags"]:
        return "evergreen"
    if "frozen" in item["flags"]:
        return "frozen"
    if "cold" in item["flags"]:
        return "cold"
    if s["hits_30d"] >= 1:
        return "hot"
    if s["hits"] == 0:
        # 无任何追踪记录：无法区分刚写入的新条目与长期无人读的旧条目，
        # 归 untracked 由处置流程人工复核，不做自动降级/清理。
        return "untracked"
    days = (today - s["last_hit"]).days if s["last_hit"] else FROZEN_DAYS + 1
    if days > FROZEN_DAYS:
        return "frozen"
    if days > COLD_DAYS:
        return "cold"
    return "warm"


ACTIONS = {
    "hot": "上移到所属 section 顶部",
    "warm": "保留",
    "cold": "降级到 memory/archive/",
    "frozen": "备份后清理/合并",
    "untracked": "无追踪记录，人工复核（区分新条目/过时内容）",
    "evergreen": "常青，不处置",
}


def evict_sort_key(r, policy):
    """同档内的淘汰排序键。lfu: score 最低优先，平局 last_hit 更旧；lru: last_hit 最旧优先。"""
    last = r["last_hit"] or "9999-12-31"  # 无记录（untracked）排同档最后
    if policy == "lru":
        return (last, -r["score"])
    return (r["score"], last)


def main():
    ap = argparse.ArgumentParser(description="MEMORY.md 条目读取热度统计")
    ap.add_argument("--mark", action="store_true", help="在冷/冻条目上加注释标记")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--policy", choices=["lru", "lfu"], default=DEFAULT_POLICY,
                    help="超水位淘汰策略（默认 %s）" % DEFAULT_POLICY)
    args = ap.parse_args()

    today = dt.date.today()
    items = parse_memory(MEMORY_MD)
    rows = parse_track(TRACK_DIR)
    stats = analyze(items, rows, today)

    report = []
    for item, s in zip(items, stats):
        g = grade(item, s, today)
        report.append({
            "section": item["section"], "key": item["key"], "line": item["line"],
            "grade": g, "action": ACTIONS[g], "flags": sorted(item["flags"]),
            "hits": s["hits"], "hits_30d": s["hits_30d"], "hits_90d": s["hits_90d"],
            "last_hit": str(s["last_hit"]) if s["last_hit"] else None,
            "sources": sorted(s["sources"]), "score": round(s["score"], 1),
        })

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"# MEMORY.md 热度报告（{today}）")
    print(f"追踪记录 {len(rows)} 行，条目 {len(items)} 条\n")
    order = {"hot": 0, "warm": 1, "cold": 2, "frozen": 3, "untracked": 4, "evergreen": 5}
    for r in sorted(report, key=lambda x: (order[x["grade"]], -x["score"])):
        print(f"- [{r['grade']:>9}] {r['key']}  (hits={r['hits']}, 30d={r['hits_30d']}, "
              f"last={r['last_hit'] or '-'}) -> {r['action']}")

    # 容量水位检查（Redis allkeys 式淘汰）
    mem_bytes = os.path.getsize(MEMORY_MD)
    print(f"\n## 容量水位（{args.policy}）")
    print(f"当前 {len(items)} 条 / {mem_bytes} 字节；水位 {MAX_ITEMS} 条 / {MAX_BYTES} 字节")
    over_items = len(items) - MAX_ITEMS
    grade_rank = {"frozen": 0, "cold": 1, "warm": 2, "untracked": 3, "hot": 4, "evergreen": 5}
    if over_items > 0:
        cand = [r for r in report if r["grade"] not in ("evergreen", "hot")]
        cand.sort(key=lambda r: (grade_rank[r["grade"]], evict_sort_key(r, args.policy)))
        victims = cand[:over_items]
        print(f"超条目水位 {over_items} 条，按 {args.policy} 策略淘汰候选：")
        for r in victims:
            print(f"- 淘汰 {r['key']}  (grade={r['grade']}, score={r['score']}, "
                  f"last={r['last_hit'] or '-'}) -> 降级到 memory/archive/")
    else:
        print("条目数未超水位，无需淘汰。")
    if mem_bytes > MAX_BYTES:
        print(f"⚠️ 体积超水位 {(mem_bytes - MAX_BYTES) // 1024}KB：建议精简长条目或调高 MAX_BYTES。")

    print("\n## 建议执行清单")
    for r in report:
        if r["grade"] in ("hot", "cold", "frozen"):
            print(f"- {r['action']}: {r['key']} (L{r['line']})")

    if args.mark:
        mark_items(items, report)
        print("\n[--mark] 已给 cold/frozen 条目打上注释标记。")


def mark_items(items, report):
    """在 MEMORY.md 的 cold/frozen 条目行尾追加 <!-- cold --> / <!-- frozen -->。"""
    if not os.path.exists(MEMORY_MD):
        return
    with open(MEMORY_MD, encoding="utf-8") as f:
        lines = f.readlines()
    changed = False
    for r in report:
        if r["grade"] not in ("cold", "frozen"):
            continue
        idx = r["line"] - 1
        if idx >= len(lines) or "<!--" in lines[idx]:
            continue
        lines[idx] = lines[idx].rstrip("\n") + f" <!-- {r['grade']}: {dt.date.today()} -->\n"
        changed = True
    if changed:
        with open(MEMORY_MD, "w", encoding="utf-8") as f:
            f.writelines(lines)


if __name__ == "__main__":
    main()

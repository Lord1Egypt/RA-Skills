#!/usr/bin/env python3
"""
hot-analyzer 计算引擎 —— 所有确定性公式由本脚本处理，LLM 只做语义判断。

用法:
  python compute.py prepare [--state STATE] \
    --toutiao FILE --baidu FILE --weibo FILE --douyin FILE --zhihu FILE
      → 解析5平台原始JSON → 精确/包含去重 → 输出待语义合并列表（供LLM）

  python compute.py compute [--state STATE] --groups GROUP_JSON
      → 应用LLM语义分组+系数 → 计算单项分/边际递减/最终排名 → 输出结果 + 生成HTML

  python compute.py html [--state STATE] --output FILE
      → 从state.json生成独立HTML文件（无需LLM参与）
"""

import json, sys, os, argparse, re, html as html_mod
from pathlib import Path

# 修复 Windows PowerShell GBK 终端乱码，失败则静默降级
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# ============================================================
# 常量配置
# ============================================================

PLATFORMS = {
    "toutiao": {"weight": 1.0, "total": 50, "title_key": "Title", "hot_key": "HotValue", "data_path": ["data"]},
    "baidu":   {"weight": 0.9, "total": 50, "title_key": "query",  "hot_key": "hotScore",  "data_path": ["data", "cards", 0, "content"]},
    "weibo":   {"weight": 0.8, "total": 50, "title_key": "word",   "hot_key": "num",      "data_path": ["data", "realtime"]},
    "douyin":  {"weight": 0.7, "total": 20, "title_key": "word",   "hot_key": "hot_value", "data_path": ["word_list"]},
    "zhihu":   {"weight": 0.6, "total": 30, "title_key": "query",  "hot_key": "weight",    "data_path": ["preset_words", "words"]},
}

# 申万 31 行业映射（供 HTML 展示用）
SW_INDUSTRIES = {
    "农林牧渔": "801010", "食品饮料": "801120", "家用电器": "801110", "纺织服饰": "801130",
    "轻工制造": "801140", "医药生物": "801150", "商贸零售": "801200", "社会服务": "801210",
    "美容护理": "801880", "电子": "801080", "计算机": "801750", "传媒": "801760",
    "通信": "801770", "银行": "801780", "非银金融": "801790", "煤炭": "801020",
    "石油石化": "801030", "基础化工": "801040", "钢铁": "801050", "有色金属": "801060",
    "建筑材料": "801710", "建筑装饰": "801720", "电力设备": "801730", "机械设备": "801890",
    "国防军工": "801740", "汽车": "801880", "公用事业": "801160", "交通运输": "801170",
    "环保": "801250", "房地产": "801180", "综合": "801230",
}

# 期货品种映射
FUTURES = {
    "黄金(AU)": "SHFE", "白银(AG)": "SHFE", "铜(CU)": "SHFE", "铝(AL)": "SHFE",
    "锌(ZN)": "SHFE", "铅(PB)": "SHFE", "镍(NI)": "SHFE", "锡(SN)": "SHFE",
    "螺纹钢(RB)": "SHFE", "热轧卷板(HC)": "SHFE", "不锈钢(SS)": "SHFE",
    "天然橡胶(RU)": "SHFE", "合成橡胶(BR)": "SHFE", "燃料油(FU)": "SHFE",
    "石油沥青(BU)": "SHFE", "纸浆(SP)": "SHFE", "氧化铝(AO)": "SHFE",
    "原油(SC)": "INE", "低硫燃料油(LU)": "INE", "20号胶(NR)": "INE",
    "国际铜(BC)": "INE", "集运指数(EC)": "INE",
    "黄大豆1号(A)": "DCE", "豆粕(M)": "DCE", "豆油(Y)": "DCE",
    "棕榈油(P)": "DCE", "玉米(C)": "DCE", "玉米淀粉(CS)": "DCE",
    "鸡蛋(JD)": "DCE", "生猪(LH)": "DCE", "粳米(RR)": "DCE",
    "铁矿石(I)": "DCE", "焦炭(J)": "DCE", "焦煤(JM)": "DCE",
    "聚乙烯(L)": "DCE", "聚氯乙烯(V)": "DCE", "聚丙烯(PP)": "DCE",
    "苯乙烯(EB)": "DCE", "乙二醇(EG)": "DCE", "液化石油气(PG)": "DCE",
    "纤维板(FB)": "DCE", "白糖(SR)": "ZCE", "棉花(CF)": "ZCE",
    "棉纱(CY)": "ZCE", "苹果(AP)": "ZCE", "红枣(CJ)": "ZCE",
    "花生(PK)": "ZCE", "菜油(OI)": "ZCE", "菜粕(RM)": "ZCE",
    "PTA(TA)": "ZCE", "甲醇(MA)": "ZCE", "纯碱(SA)": "ZCE",
    "玻璃(FG)": "ZCE", "尿素(UR)": "ZCE", "烧碱(SH)": "ZCE",
    "硅铁(SF)": "ZCE", "锰硅(SM)": "ZCE", "动力煤(ZC)": "ZCE",
    "短纤(PF)": "ZCE", "原木(LG)": "ZCE",
    "沪深300(IF)": "CFFEX", "上证50(IH)": "CFFEX", "中证500(IC)": "CFFEX",
    "中证1000(IM)": "CFFEX", "2年期国债(TS)": "CFFEX", "5年期国债(TF)": "CFFEX",
    "10年期国债(T)": "CFFEX", "工业硅(SI)": "GFEX", "碳酸锂(LC)": "GFEX",
    "多晶硅": "GFEX",
}

# HTML 模板
HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>热点舆情金融市场分析报告</title>
<style>
  :root {{--bg:#0f1117;--card:#1a1d27;--border:#2a2d3a;--text:#e0e0e0;--dim:#8b8b9e;--red:#ef4444;--green:#22c55e;--accent:#3b82f6;--gold:#f59e0b}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:var(--bg);color:var(--text);font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;padding:24px}}
  .container{{max-width:1200px;margin:0 auto}}
  .header{{text-align:center;padding:40px 0 32px;border-bottom:1px solid var(--border);margin-bottom:32px}}
  .header h1{{font-size:28px;font-weight:700;margin-bottom:8px}}
  .header time{{color:var(--dim);font-size:14px}}
  .section{{margin-bottom:40px}}
  .section-title{{font-size:20px;font-weight:700;padding:12px 0;border-bottom:2px solid var(--accent);margin-bottom:20px;color:#fff}}
  .section-title::before{{content:"";display:inline-block;width:4px;height:20px;background:var(--accent);margin-right:10px;vertical-align:middle;border-radius:2px}}
  .metrics-bar{{display:flex;gap:16px;margin-bottom:32px;flex-wrap:wrap}}
  .metric-card{{background:var(--card);border-radius:10px;padding:16px 24px;border:1px solid var(--border);flex:1;min-width:150px}}
  .metric-label{{font-size:11px;color:var(--dim);text-transform:uppercase;letter-spacing:.5px}}
  .metric-value{{font-size:22px;font-weight:700;margin-top:4px}}
  .metric-sub{{font-size:12px;color:var(--dim);margin-top:2px}}
  .hot-table{{width:100%;border-collapse:collapse;font-size:14px}}
  .hot-table th{{background:var(--card);color:var(--dim);font-weight:500;text-align:left;padding:10px 14px;border-bottom:1px solid var(--border);font-size:12px;text-transform:uppercase;letter-spacing:.5px}}
  .hot-table td{{padding:10px 14px;border-bottom:1px solid rgba(42,45,58,.6);vertical-align:middle}}
  .hot-table tr:hover{{background:rgba(59,130,246,.04)}}
  .rank{{font-weight:700;font-size:18px;color:var(--accent);width:50px}}
  .rank.top1{{color:var(--gold)}}.rank.top2{{color:#a3a3a3}}.rank.top3{{color:#cd853f}}
  .score-bar-bg{{display:inline-block;width:80px;height:6px;border-radius:3px;background:rgba(255,255,255,.08);vertical-align:middle;margin-right:6px}}
  .score-bar{{display:inline-block;height:6px;border-radius:3px;background:var(--accent);min-width:4px}}
  .score-val{{font-weight:600;font-family:"Consolas",monospace;font-size:13px}}
  .platform-tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;margin-right:4px;background:rgba(255,255,255,.06);color:var(--dim)}}
  .coeff-tag{{display:inline-block;padding:2px 6px;border-radius:3px;font-size:10px;font-weight:600;margin-left:4px}}
  .coeff-finance{{background:rgba(239,68,68,.15);color:var(--red)}}
  .coeff-exclusive{{background:rgba(245,158,11,.15);color:var(--gold)}}
  .direction-bull{{color:var(--red);font-weight:700}}
  .direction-bear{{color:var(--green);font-weight:700}}
  .direction-neutral{{color:var(--dim)}}
  .empty-section{{padding:40px;text-align:center;color:var(--dim)}}
  .empty-section p{{font-size:16px;margin-bottom:8px}}
  .empty-section small{{font-size:13px}}
  @media(max-width:768px){{body{{padding:12px}}.header h1{{font-size:22px}}.metrics-bar{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>📊 热点舆情金融市场分析报告</h1>
  <time>{report_time}</time>
</div>
<div class="metrics-bar">
  <div class="metric-card"><div class="metric-label">📡 采集平台</div><div class="metric-value">5</div><div class="metric-sub">头条/百度/微博/抖音/知乎</div></div>
  <div class="metric-card"><div class="metric-label">🔥 原始条目</div><div class="metric-value">{raw_count}</div><div class="metric-sub">去重后 {merged_count} 组</div></div>
  <div class="metric-card"><div class="metric-label">📈 财经信号</div><div class="metric-value">{finance_count}</div><div class="metric-sub">系数 &ge;1.2 占 {finance_pct}%</div></div>
  <div class="metric-card"><div class="metric-label">🎯 独家信号</div><div class="metric-value">{exclusive_count}</div><div class="metric-sub">仅1-2平台财经热点</div></div>
</div>
<div class="section">
  <div class="section-title">一、综合热点榜 TOP 30</div>
  {top30_html}
</div>
<div class="section">
  <div class="section-title">二、债券 / 行业 / 标的 / 期货</div>
  <div class="empty-section">
    <p>此部分需 LLM 市场分析后补充</p>
    <small>HTML 基础框架已生成，请查看 Markdown 报告获取完整分析</small>
  </div>
</div>
</div>
</body>
</html>'''


# ============================================================
# 数据解析
# ============================================================

def safe_get(d, path):
    """按路径列表深度取值"""
    for key in path:
        if isinstance(d, dict):
            d = d.get(key)
        elif isinstance(d, list) and isinstance(key, int) and 0 <= key < len(d):
            d = d[key]
        else:
            return None
        if d is None:
            return None
    return d


def parse_platform(name, cfg, raw_data):
    """解析单个平台原始JSON → 条目列表"""
    arr = safe_get(raw_data, cfg["data_path"])
    if arr is None:
        print(f"[WARN] {name}: data_path {cfg['data_path']} not found", file=sys.stderr)
        return []

    total = cfg["total"]
    title_key = cfg["title_key"]
    hot_key = cfg["hot_key"]
    items = []

    # 微博需要过滤广告
    if name == "weibo":
        arr = [x for x in arr if x.get("is_ad") != 1]

    # 重新计算total（微博过滤广告后数量变化）
    actual_total = len(arr) if name == "weibo" else min(len(arr), total)

    for idx, entry in enumerate(arr[:total]):
        title = entry.get(title_key, "").strip()
        if not title:
            continue

        if name == "zhihu":
            # 知乎 weight字段固定为1无区分度，用recall_source映射为伪热度
            rs = entry.get("recall_source", "random")
            tier_map = {"top_hot": 1.0, "s_level": 0.5, "random": 0.0}
            heat = tier_map.get(rs, 0.0)
            # 但仍然记录为虚拟值，确保heat_list不为空
        else:
            heat = entry.get(hot_key, 0)
            if isinstance(heat, str):
                try:
                    heat = float(heat)
                except ValueError:
                    heat = 0

        items.append({
            "platform": name,
            "title": title,
            "rank": idx,
            "heat": heat,
            "total": actual_total if name == "weibo" else total,
        })

    return items


# ============================================================
# 精确/包含匹配去重
# ============================================================

def exact_dedup(all_items):
    """
    精确匹配 + 包含匹配去重。
    返回: (merged_groups, remaining_items)
      merged_groups: [{"representative": "最长标题", "members": [item, ...], "platforms": set()}]
      remaining_items: 没有匹配上的条目
    """
    items = list(all_items)
    groups = []
    used = [False] * len(items)

    for i in range(len(items)):
        if used[i]:
            continue
        group = [items[i]]
        used[i] = True
        title_i = items[i]["title"]

        for j in range(i + 1, len(items)):
            if used[j]:
                continue
            title_j = items[j]["title"]
            # 精确匹配 或 包含匹配
            if title_i == title_j or title_i in title_j or title_j in title_i:
                group.append(items[j])
                used[j] = True

        # 选最长标题为代表
        longest = max(group, key=lambda x: len(x["title"]))
        platforms = set(m["platform"] for m in group)
        groups.append({
            "representative": longest["title"],
            "members": group,
            "platforms": sorted(platforms),
            "member_count": len(group),
        })

    return groups


# ============================================================
# 单项得分计算
# ============================================================

def compute_single_scores(items):
    """为一批条目计算单项得分（同平台内计算max_heat）"""
    # 按平台分组
    by_platform = {}
    for item in items:
        p = item["platform"]
        by_platform.setdefault(p, []).append(item)

    for p, p_items in by_platform.items():
        cfg = PLATFORMS[p]
        max_heat = max(x["heat"] for x in p_items) if p_items else 1

        for item in p_items:
            rank_factor = 1 - item["rank"] / max(item["total"], 1)

            if p == "zhihu":
                # α=1.0 纯排名
                heat_factor = 0
            else:
                heat_factor = item["heat"] / max_heat if max_heat > 0 else 0

            item["single_score"] = (0.6 * rank_factor + 0.4 * heat_factor) * cfg["weight"]

    return by_platform


# ============================================================
# 边际递减 + 最终得分
# ============================================================

def compute_group_score(group_items):
    """
    同组内单项得分从高到低排序，应用边际递减。
    返回综合分。
    """
    scores = sorted([item["single_score"] for item in group_items], reverse=True)
    coeffs = [1.0, 0.8, 0.6, 0.3, 0.3]  # S₁ + 0.8×S₂ + 0.6×S₃ + 0.3×S₄₊
    total = 0
    for i, s in enumerate(scores):
        c = coeffs[i] if i < len(coeffs) else 0.3
        total += c * s
    return total


# ============================================================
# 主命令
# ============================================================

def cmd_prepare(args):
    """解析5平台原始JSON → 精确/包含去重 → 输出待语义合并列表"""
    all_items = []
    raw_counts = {}

    for name in ["toutiao", "baidu", "weibo", "douyin", "zhihu"]:
        filepath = getattr(args, name, None)
        if not filepath or not os.path.exists(filepath):
            print(f"[WARN] {name}: file not found, skipping", file=sys.stderr)
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        items = parse_platform(name, PLATFORMS[name], raw_data)
        raw_counts[name] = len(items)
        all_items.extend(items)

    # 精确/包含匹配去重
    exact_groups = exact_dedup(all_items)

    # 统计
    merged_in_exact = sum(g["member_count"] for g in exact_groups)
    remaining = len(all_items) - sum(1 for g in exact_groups for _ in g["members"])  # should be ~0 since everything is in a group

    # 对于只有1个成员的组（没匹配上的），它们是"待语义合并"的候选
    single_member_groups = [g for g in exact_groups if g["member_count"] == 1]
    multi_member_groups = [g for g in exact_groups if g["member_count"] > 1]

    # 构建state
    # 为所有条目计算单项分
    compute_single_scores(all_items)

    # 为每个item添加 score 别名（state.json中更直观），防御性检查
    max_scores = {}
    for item in all_items:
        item["score"] = round(item.get("single_score", 0.0), 4)
        p = item["platform"]
        max_scores[p] = max(max_scores.get(p, 0), item["score"])

    for p, ms in max_scores.items():
        if ms == 0:
            print(f"[WARN] {p}: all items have score=0, check raw data parsing", file=sys.stderr)

    state = {
        "version": 1,
        "exact_groups": exact_groups,
        "all_items": all_items,
        "raw_counts": raw_counts,
        "total_raw": len(all_items),
    }

    # 保存state
    if args.state:
        with open(args.state, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    # 输出待语义合并列表给 LLM（同时打印 + 写JSON文件避免Windows终端乱码）
    print("=" * 60)
    print("【已自动合并的精确匹配组】")
    print("=" * 60)
    for g in multi_member_groups:
        titles = [m["title"] for m in g["members"]]
        platforms = [m["platform"] for m in g["members"]]
        print(f"  代表: {g['representative']}")
        print(f"  成员({g['member_count']}): {titles}")
        print(f"  平台: {platforms}")
        print()

    pending_list = []
    print("=" * 60)
    print("【待LLM语义合并列表】（逐个判断是否需要合并）")
    print("=" * 60)
    for i, g in enumerate(single_member_groups):
        item = g["members"][0]
        print(f"  [{i}] {item['title']}  ({item['platform']}#{item['rank']+1}, score={item['single_score']:.3f})")
        pending_list.append({
            "index": i,
            "title": item["title"],
            "platform": item["platform"],
            "rank": item["rank"] + 1,
            "score": round(item["single_score"], 4),
        })

    print()
    print(f"总计: {len(all_items)} 条 → 精确合并后 {len(exact_groups)} 组 (其中 {len(multi_member_groups)} 组多成员, {len(single_member_groups)} 条待语义合并)")
    print(f"State saved to: {args.state}")

    # 将待合并列表写入JSON文件（解决Windows终端GBK乱码无法阅读的问题）
    pending_path = str(Path(args.state).with_name("pending.json"))
    pending_data = {
        "total": len(pending_list),
        "items": pending_list,
        "multi_member_groups": [{
            "representative": g["representative"],
            "members": [m["title"] for m in g["members"]],
            "platforms": g["platforms"],
        } for g in multi_member_groups],
    }
    with open(pending_path, "w", encoding="utf-8") as f:
        json.dump(pending_data, f, ensure_ascii=False, indent=2)
    print(f"待合并列表已保存至: {pending_path}（UTF-8 JSON，无乱码）")

    state["_pending_count"] = len(single_member_groups)
    return state


def cmd_compute(args):
    """应用LLM语义分组+系数 → 计算最终排名"""
    # 读取state
    with open(args.state, "r", encoding="utf-8") as f:
        state = json.load(f)

    # 读取LLM分组
    with open(args.groups, "r", encoding="utf-8") as f:
        llm_groups = json.load(f)

    all_items = state["all_items"]

    # 建立标题→条目的索引
    title_to_items = {}
    for item in all_items:
        title_to_items.setdefault(item["title"], []).append(item)

    # 应用LLM语义分组
    # llm_groups 格式: [{"representative": "标题", "members": ["标题1","标题2"], "finance_coeff": 1.2, "exclusive_coeff": 1.0}, ...]
    final_groups = []

    for lg in llm_groups:
        rep = lg.get("representative", "")
        member_titles = lg.get("members", [rep])
        finance_coeff = lg.get("finance_coeff", 1.0)
        exclusive_coeff = lg.get("exclusive_coeff", 1.0)

        group_items = []
        platforms = set()

        for title in member_titles:
            matches = title_to_items.get(title, [])
            for m in matches:
                m["_group"] = rep
                group_items.append(m)
                platforms.add(m["platform"])

        if not group_items:
            continue

        composite = compute_group_score(group_items)
        final_score = composite * finance_coeff * exclusive_coeff

        final_groups.append({
            "representative": rep,
            "members": group_items,
            "platforms": sorted(platforms),
            "platform_count": len(platforms),
            "composite_score": round(composite, 4),
            "finance_coeff": finance_coeff,
            "exclusive_coeff": exclusive_coeff,
            "final_score": round(final_score, 4),
        })

    # 按最终得分排序
    final_groups.sort(key=lambda x: x["final_score"], reverse=True)

    # 更新state
    state["final_groups"] = final_groups
    state["top30"] = final_groups[:30]

    # 统计
    finance_count = sum(1 for g in final_groups if g["finance_coeff"] >= 1.2)
    exclusive_count = sum(1 for g in final_groups if g["exclusive_coeff"] > 1.0)

    state["stats"] = {
        "finance_count": finance_count,
        "exclusive_count": exclusive_count,
        "finance_pct": round(finance_count / max(len(final_groups), 1) * 100, 1),
    }

    if args.state:
        with open(args.state, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    # 输出结果
    print("=" * 60)
    print("【最终排名 TOP 30】")
    print("=" * 60)
    for i, g in enumerate(final_groups[:30]):
        print(f"  #{i+1} {g['representative']}")
        print(f"      平台({g['platform_count']}): {g['platforms']}")
        print(f"      综合分={g['composite_score']:.4f} × 财经{g['finance_coeff']} × 独家{g['exclusive_coeff']} = {g['final_score']:.4f}")
        # 显示各平台贡献
        for item in g["members"]:
            print(f"        {item['platform']}#{item['rank']+1} score={item['single_score']:.4f} heat={item['heat']}")
        print()

    print(f"财经信号(≥1.2): {finance_count}/{len(final_groups)} ({state['stats']['finance_pct']}%)")
    print(f"独家信号(>1.0): {exclusive_count}")

    return state


def cmd_html(args):
    """从state.json生成HTML"""
    with open(args.state, "r", encoding="utf-8") as f:
        state = json.load(f)

    from datetime import datetime
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    top_groups = state.get("top30", state.get("final_groups", []))[:30]
    raw_count = state.get("total_raw", 0)
    merged_count = len(state.get("final_groups", []))
    stats = state.get("stats", {})
    finance_count = stats.get("finance_count", 0)
    finance_pct = stats.get("finance_pct", 0)
    exclusive_count = stats.get("exclusive_count", 0)

    # 找最高分用于柱状图
    max_score = max((g["final_score"] for g in top_groups), default=1)

    def rank_class(n):
        if n == 1: return "top1"
        if n == 2: return "top2"
        if n == 3: return "top3"
        return ""

    rows_html = ""
    for i, g in enumerate(top_groups):
        rank = i + 1
        title = html_mod.escape(g["representative"])
        pc = g["platform_count"]
        score = g["final_score"]
        bar_pct = min(score / max_score * 100, 100) if max_score > 0 else 0
        platforms_str = " ".join(g["platforms"])

        coeff_tags = ""
        if g.get("finance_coeff", 1.0) >= 1.2:
            coeff_tags += f'<span class="coeff-tag coeff-finance">财×{g["finance_coeff"]}</span>'
        if g.get("exclusive_coeff", 1.0) > 1.0:
            coeff_tags += f'<span class="coeff-tag coeff-exclusive">独×{g["exclusive_coeff"]}</span>'

        rows_html += f'''<tr>
            <td class="rank {rank_class(rank)}">{rank}</td>
            <td>{title} {coeff_tags}</td>
            <td>{pc}平台</td>
            <td><span class="score-bar-bg"><span class="score-bar" style="width:{bar_pct:.0f}px"></span></span><span class="score-val">{score:.3f}</span></td>
            <td>{platforms_str}</td>
        </tr>\n'''

    top30_table = f'''<table class="hot-table">
        <thead><tr><th>#</th><th>热点标题</th><th>平台</th><th>最终得分</th><th>来源</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table>'''

    # CSS 中的 {} 已用 {{}} 转义，.format() 会正确还原为单花括号
    html_content = HTML_TEMPLATE.format(
        report_time=report_time,
        raw_count=raw_count,
        merged_count=merged_count,
        finance_count=finance_count,
        finance_pct=finance_pct,
        exclusive_count=exclusive_count,
        top30_html=top30_table,
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML generated: {args.output}")


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="hot-analyzer 计算引擎")
    sub = parser.add_subparsers(dest="command")

    # prepare
    p_prep = sub.add_parser("prepare", help="解析原始数据 + 精确去重")
    p_prep.add_argument("--state", default="state.json", help="状态文件路径")
    for name in PLATFORMS:
        p_prep.add_argument(f"--{name}", help=f"{name} 原始JSON文件路径")

    # compute
    p_comp = sub.add_parser("compute", help="应用LLM分组+系数 → 计算最终排名")
    p_comp.add_argument("--state", default="state.json", help="状态文件路径")
    p_comp.add_argument("--groups", required=True, help="LLM语义分组JSON文件")

    # html
    p_html = sub.add_parser("html", help="从state.json生成HTML")
    p_html.add_argument("--state", default="state.json", help="状态文件路径")
    p_html.add_argument("--output", "-o", default="hot_analysis_report.html", help="输出HTML路径")

    args = parser.parse_args()
    if args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "compute":
        cmd_compute(args)
    elif args.command == "html":
        cmd_html(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

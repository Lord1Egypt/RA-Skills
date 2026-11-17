#!/usr/bin/env python3
"""
Knowledge Graph Builder — generate an interactive force-directed HTML graph
from a structured knowledge vault (INDEX.md + article cards + framework nodes).

Usage:
  python3 build_graph.py                          # use defaults
  python3 build_graph.py --vault /path/to/vault   # custom vault path
  python3 build_graph.py --config config.yaml     # custom config
  python3 build_graph.py --output graph.html      # custom output

Requires: Python 3.9+, no external dependencies.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict, Counter

# ============================================================
# Defaults (overridable via --config or CLI args)
# ============================================================
DEFAULT_VAULT = os.environ.get("KNOWLEDGE_VAULT", ".")
DEFAULT_OUTPUT = "knowledge-graph-full.html"

DEFAULT_CAT_META = {
    "🤖": {"layer": "L3", "color": "#f59e0b", "label": "AI Agent & 估值"},
    "🧠": {"layer": "L2", "color": "#10b981", "label": "觉察 & 心理"},
    "🏗️": {"layer": "L3", "color": "#8b5cf6", "label": "Harness & 架构"},
    "📊": {"layer": "L3", "color": "#3b82f6", "label": "宏观 & 量化"},
    "🏠": {"layer": "L3", "color": "#06b6d4", "label": "地产 & Rebase"},
    "💰": {"layer": "L3", "color": "#eab308", "label": "投资框架"},
    "☸️": {"layer": "L2", "color": "#14b8a6", "label": "小澄 & 佛学"},
    "📚": {"layer": "L1", "color": "#6366f1", "label": "书镜 & 认知"},
    "🧬": {"layer": "L1", "color": "#ec4899", "label": "创业 & 个人"},
}

DEFAULT_KEYWORDS = [
    "AI", "Agent", "宏观", "杠杆", "认知", "觉察", "情绪", "反刍", "影响力", "课题",
    "美元", "地缘", "房地产", "人口", "估值", "成熟度", "数据", "投资", "泡沫", "量化",
    "交易", "策略", "组织", "管理", "创业", "心经", "唯识", "习惯", "决策",
    "system", "harness", "skill", "MCP", "Claude", "OpenAI", "Anthropic", "Karpathy",
    "阶层", "消费", "周期", "利率", "汇率", "黄金", "加密",
    "openclaw", "LLM", "GPT", "育儿",
]

DEFAULT_FRAMEWORK_NODES = [
    {"id": "FW-L1-cognitive-sovereignty", "label": "认知主权三问", "layer": "L1",
     "color": "#6366f1", "category": "核心框架", "cat_label": "L1核心",
     "insight": "目标谁定？知道取舍吗？能放回方向盘？",
     "concepts": ["认知主权", "高概率走廊"], "source": "MEMORY.md", "isFramework": True},
    {"id": "FW-L1-high-probability-corridor", "label": "高概率走廊", "layer": "L1",
     "color": "#6366f1", "category": "核心框架", "cat_label": "L1核心",
     "insight": "模型默认×产品奖励×用户省事=趋同",
     "concepts": ["认知主权"], "source": "MEMORY.md", "isFramework": True},
    {"id": "FW-L2-emotion-rumination", "label": "情绪反刍≠反思", "layer": "L2",
     "color": "#10b981", "category": "核心框架", "cat_label": "L2核心",
     "insight": "反刍嚼痛苦→毒素;反思做完能量上走",
     "concepts": ["课题分离", "影响力圈"], "source": "MEMORY.md", "isFramework": True},
    {"id": "FW-L2-influence-circle", "label": "影响力圈", "layer": "L2",
     "color": "#10b981", "category": "核心框架", "cat_label": "L2核心",
     "insight": "专注可控→涟漪扩大",
     "concepts": ["课题分离"], "source": "MEMORY.md", "isFramework": True},
    {"id": "FW-L3-geo-4d", "label": "四维共振(地缘×金融×供给×人口)", "layer": "L3",
     "color": "#3b82f6", "category": "核心框架", "cat_label": "L3核心",
     "insight": "先滞胀后萧条。高血压vs低血糖",
     "concepts": ["美元超级血包", "AI灰犀牛", "AI替代性技术"],
     "source": "A视野系列", "isFramework": True},
    {"id": "FW-L3-data-product", "label": "数据产品四层架构", "layer": "L3",
     "color": "#eab308", "category": "核心框架", "cat_label": "L3核心",
     "insight": "L1平台→L2治理→L3服务→L4消费",
     "concepts": ["数据全栈", "护城河"], "source": "MEMORY.md", "isFramework": True},
    {"id": "FW-L3-ai-maturity", "label": "AI Agent成熟度×企业估值", "layer": "L3",
     "color": "#f59e0b", "category": "核心框架", "cat_label": "论文",
     "insight": "企业AI智能体应用成熟度的度量及其与企业估值的相关性研究",
     "concepts": ["AI Agent", "企业估值"], "source": "论文项目", "isFramework": True},
]

DEFAULT_MANUAL = [
    ("china-stays-out", "FW-L3-geo-4d", "地缘×四维"),
    ("avision-macro", "FW-L3-geo-4d", "A视野核心"),
    ("a-sen-2024", "FW-L3-geo-4d", "崩盘复盘"),
    ("resistance-retains", "FW-L2-emotion-rumination", "抗拒=反刍"),
    ("resistance-retains", "FW-L2-influence-circle", "课题分离"),
    ("sutton-bitter-lesson", "FW-L1-cognitive-sovereignty", "AI→认知主权"),
    ("high-probability-corridor", "FW-L1-high-probability-corridor", "高概率走廊"),
    ("high-probability-corridor", "FW-L1-cognitive-sovereignty", "走廊→主权"),
    ("FW-L1-high-probability-corridor", "FW-L1-cognitive-sovereignty", "走廊→主权"),
    ("FW-L2-emotion-rumination", "FW-L2-influence-circle", "反刍→影响力"),
    ("china-stays-out", "avision-macro", "地缘×金融"),
    ("zhongyuan-housing", "lingang-population", "房地产×人口"),
    ("heli-ai-coding", "sutton-bitter-lesson", "AI偷懒×苦涩"),
    ("gewuzhi-art", "sutton-bitter-lesson", "AI×品位"),
    ("buffett-7-things", "FW-L3-geo-4d", "投资×宏观"),
    ("petro-venezuela", "avision-macro", "主权→宏观"),
    ("FW-L3-data-product", "FW-L3-ai-maturity", "数据×AI"),
    ("FW-L3-ai-maturity", "heli-ai-coding", "成熟度×实践"),
    ("ceibs-dba", "FW-L1-cognitive-sovereignty", "管理→认知"),
]


# ============================================================
# Config loader (minimal YAML-free parser — reads simple key: value)
# ============================================================
def load_config(config_path):
    """Load optional config file. Returns dict with keys:
    cat_meta, keywords, framework_nodes, manual_links.
    Falls back to DEFAULTS if file missing or key absent.
    """
    cfg = {
        "cat_meta": dict(DEFAULT_CAT_META),
        "keywords": list(DEFAULT_KEYWORDS),
        "framework_nodes": list(DEFAULT_FRAMEWORK_NODES),
        "manual_links": list(DEFAULT_MANUAL),
    }
    if not config_path or not os.path.isfile(config_path):
        return cfg
    # Use json for simplicity (yaml may not be installed)
    try:
        with open(config_path) as f:
            user_cfg = json.load(f)
    except (json.JSONDecodeError, Exception):
        # Try minimal YAML-like parsing for cat_meta override
        try:
            import yaml
            with open(config_path) as f:
                user_cfg = yaml.safe_load(f) or {}
        except ImportError:
            print(f"Warning: Could not parse config {config_path}, using defaults", file=sys.stderr)
            return cfg

    if "cat_meta" in user_cfg:
        cfg["cat_meta"] = {**DEFAULT_CAT_META, **user_cfg["cat_meta"]}
    if "keywords" in user_cfg:
        cfg["keywords"] = user_cfg["keywords"]
    if "framework_nodes" in user_cfg:
        cfg["framework_nodes"] = user_cfg["framework_nodes"]
    if "manual_links" in user_cfg:
        # Convert tuples from JSON arrays
        cfg["manual_links"] = [tuple(t) for t in user_cfg["manual_links"]]
    return cfg


# ============================================================
# 1. Parse INDEX.md
# ============================================================
def parse_index(index_path):
    """Parse references/INDEX.md → [(cat_name, emoji, [items])]."""
    if not os.path.isfile(index_path):
        print(f"Warning: INDEX.md not found at {index_path}", file=sys.stderr)
        return []

    with open(index_path, "r") as f:
        idx_content = f.read()

    categories = []
    current_cat = None
    current_emoji = None
    current_items = []

    for line in idx_content.split("\n"):
        m = re.match(r"^## (.+?) \((\d+)篇\)", line)
        if m:
            if current_cat:
                categories.append((current_cat, current_emoji, current_items))
            cat_full = m.group(1)
            em = cat_full.split()[0] if cat_full else ""
            current_cat = cat_full
            current_emoji = em
            current_items = []
            continue
        m = re.match(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]*)\|\s*([^|]*)\|?\s*$", line)
        if m and current_cat:
            current_items.append({
                "filename": m.group(1).strip(),
                "path": m.group(2).strip(),
                "date": m.group(3).strip() if m.group(3).strip() and m.group(3).strip() != "—" else "",
                "summary": m.group(4).strip()[:100] if m.group(4).strip() and m.group(4).strip() != "—" else "",
            })
            continue
        m = re.match(r"^-\s+\[([^\]]+)\]\(([^)]+)\)\s+—\s+(.+)$", line)
        if m and current_cat:
            current_items.append({
                "filename": m.group(1).strip(), "path": m.group(2).strip(),
                "date": "", "summary": m.group(3).strip()[:100],
            })

    if current_cat:
        categories.append((current_cat, current_emoji, current_items))
    return categories


# ============================================================
# 2. Parse article-cards for frame_analysis
# ============================================================
def parse_cards(cards_dir):
    """Scan 03-sources/article-cards/*.md for frame_analysis metadata."""
    if not os.path.isdir(cards_dir):
        print(f"Warning: article-cards dir not found: {cards_dir}", file=sys.stderr)
        return {}

    card_meta = {}
    for f in sorted(os.listdir(cards_dir)):
        if not f.endswith(".md"):
            continue
        base = f.replace(".md", "")
        if re.match(r".+-\d{8}-\d{6}-[0-9a-f]+$", base):
            continue
        content = open(os.path.join(cards_dir, f)).read()

        m = re.search(r'frame_analysis:\s*\n(.*?)(?=\n[a-z_]+:|\n## |\Z)', content, re.DOTALL)
        layer = cat = insight = ""
        concepts = []
        if m:
            block = m.group(1)
            layer = (re.search(r"layer:\s*(.+)", block) or [None, ""])[1].strip().strip('"').strip("'")
            cat = (re.search(r"category:\s*(.+)", block) or [None, ""])[1].strip().strip('"').strip("'")
            insight = (re.search(r'core_insight:\s*"?(.+?)"?\s*$', block, re.MULTILINE) or [None, ""])[1].strip().strip('"').strip("'")[:150]
            concepts = [c.strip() for c in re.findall(r'^\s+-\s+"?(.+?)"?\s*$', block, re.MULTILINE)][:6]

        title_m = re.search(r'^title:\s*"(.+?)"', content, re.MULTILINE)
        source_m = re.search(r'source:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
        if not title_m:
            title_m2 = re.search(r'^title:\s*"(.+?)"', content[500:1500], re.MULTILINE)
            if title_m2:
                title_m = title_m2

        card_meta[base] = {
            "layer": layer, "category_frame": cat, "insight": insight,
            "concepts": concepts,
            "title": title_m.group(1) if title_m else base,
            "source": source_m.group(1).strip().strip('"') if source_m else "",
        }
    return card_meta


# ============================================================
# 3. Build nodes
# ============================================================
def build_nodes(categories, card_meta, cfg):
    cat_meta = cfg["cat_meta"]
    nodes = []

    for cat_name, emoji, items in categories:
        meta = cat_meta.get(emoji, {"layer": "", "color": "#6b7280", "label": cat_name})
        for item in items:
            fname = item["filename"]
            nid = fname.replace(".md", "").replace(" ", "-")
            card_key = None
            for ck in card_meta:
                if ck in nid or nid in ck:
                    card_key = ck
                    break
            cm = card_meta.get(card_key, {}) if card_key else {}
            title = cm.get("title", "") or item["summary"][:30] or fname.replace(".md", "").replace("-", " ")
            nodes.append({
                "id": nid,
                "label": title[:40],
                "layer": cm.get("layer", "") or meta["layer"],
                "color": meta["color"],
                "category": cat_name,
                "cat_label": meta["label"],
                "date": item["date"],
                "summary": item["summary"],
                "insight": cm.get("insight", ""),
                "concepts": cm.get("concepts", []),
                "source": cm.get("source", ""),
                "isFramework": False,
            })

    # Add article-cards not in INDEX
    existing_ids = {n["id"] for n in nodes}
    for card_key, cm in card_meta.items():
        if cm.get("layer") or cm.get("insight"):
            already = any(card_key in eid or eid in card_key for eid in existing_ids)
            if not already:
                nodes.append({
                    "id": card_key,
                    "label": cm.get("title", card_key)[:40],
                    "layer": cm.get("layer", "L3"),
                    "color": "#f59e0b",
                    "category": cm.get("category_frame", "分析条目")[:20],
                    "cat_label": cm.get("category_frame", "分析")[:15],
                    "date": "", "summary": "",
                    "insight": cm.get("insight", ""),
                    "concepts": cm.get("concepts", []),
                    "source": cm.get("source", ""),
                    "isFramework": False,
                })
                existing_ids.add(card_key)

    # Add framework nodes
    nodes.extend(cfg["framework_nodes"])
    return nodes


# ============================================================
# 4. Build edges
# ============================================================
def build_edges(nodes, cfg):
    valid_ids = {n["id"] for n in nodes}
    keywords = cfg["keywords"]
    manual = cfg["manual_links"]
    edges = []
    edge_set = set()

    # 4a. Cluster (same category, MST chain)
    cat_groups = defaultdict(list)
    for n in nodes:
        if n["category"] != "核心框架":
            cat_groups[n["category"]].append(n["id"])
    for cat, ids in cat_groups.items():
        sorted_ids = sorted(ids)
        for i in range(len(sorted_ids) - 1):
            pair = tuple(sorted([sorted_ids[i], sorted_ids[i + 1]]))
            if pair not in edge_set:
                edge_set.add(pair)
                edges.append({"source": sorted_ids[i], "target": sorted_ids[i + 1], "type": "cluster", "label": ""})

    # 4b. Concept co-occurrence
    concept_map = defaultdict(set)
    for n in nodes:
        text = (n.get("summary", "") + " " + n.get("insight", "") + " " + n.get("label", "") + " " + " ".join(n.get("concepts", []))).lower()
        for kw in keywords:
            if kw.lower() in text:
                concept_map[kw].add(n["id"])

    for kw, ids in concept_map.items():
        ids_list = list(ids)
        if 1 < len(ids_list) <= 8:
            for i in range(len(ids_list)):
                for j in range(i + 1, len(ids_list)):
                    pair = tuple(sorted([ids_list[i], ids_list[j]]))
                    if pair not in edge_set:
                        edge_set.add(pair)
                        edges.append({"source": ids_list[i], "target": ids_list[j], "type": "concept", "label": kw})
        elif len(ids_list) > 8:
            hub = ids_list[0]
            for other in ids_list[1:9]:
                pair = tuple(sorted([hub, other]))
                if pair not in edge_set:
                    edge_set.add(pair)
                    edges.append({"source": hub, "target": other, "type": "concept", "label": kw})

    # 4c. Manual explicit links
    for s_pat, t_pat, label in manual:
        s_match = None
        t_match = None
        for nid in valid_ids:
            if s_pat in nid and s_match is None:
                s_match = nid
            if t_pat in nid and t_match is None:
                t_match = nid
        if t_pat.startswith("FW-"):
            t_match = t_pat if t_pat in valid_ids else None
        if s_match and t_match and s_match != t_match:
            pair = tuple(sorted([s_match, t_match]))
            if pair not in edge_set:
                edge_set.add(pair)
                edges.append({"source": s_match, "target": t_match, "type": "explicit", "label": label})

    # Filter invalid
    return [e for e in edges if e["source"] in valid_ids and e["target"] in valid_ids and e["source"] != e["target"]]


# ============================================================
# 5. Generate HTML
# ============================================================
def generate_html(nodes, edges, output_path, title="Knowledge Graph"):
    edge_colors = {"explicit": "#ef4444", "concept": "#3b82f6", "cluster": "#2a2a35"}
    nodes_out = [{"id": n["id"], "label": n["label"][:40], "layer": n.get("layer", ""),
                  "color": n["color"], "category": n.get("cat_label", ""), "date": n.get("date", ""),
                  "summary": n.get("summary", "")[:80], "insight": n.get("insight", "")[:100],
                  "isFramework": n.get("isFramework", False)} for n in nodes]
    edges_out = [{"source": e["source"], "target": e["target"], "color": edge_colors.get(e["type"], "#333"),
                  "label": e.get("label", ""), "type": e["type"],
                  "width": 2.5 if e["type"] == "explicit" else (1.5 if e["type"] == "concept" else 0.8)} for e in edges]
    graph_json = json.dumps({"nodes": nodes_out, "edges": edges_out}, ensure_ascii=False)

    # Category legend from nodes
    cats_seen = []
    for n in nodes_out:
        if n["category"] not in [c[0] for c in cats_seen]:
            cats_seen.append((n["category"], n["color"]))

    legend_items = "".join(
        f'<div class="item"><div class="dot" style="background:{c}"></div> {name}</div>'
        for name, c in cats_seen[:12]
    )

    # Use placeholder substitution (NOT f-string) to avoid JS brace escaping hell
    html_template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0e0e0;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif;overflow:hidden}
canvas{display:block;position:fixed;top:0;left:0}
#header{position:fixed;top:0;left:0;padding:14px 20px;z-index:50;pointer-events:none}
#header h1{font-size:18px;color:#fff;text-shadow:0 0 10px rgba(0,0,0,0.8)}
#header p{font-size:11px;color:#666;margin-top:3px}
#legend{position:fixed;bottom:12px;left:12px;z-index:50;background:rgba(15,15,22,0.92);border:1px solid #2a2a35;border-radius:8px;padding:10px 14px;font-size:11px;max-width:200px}
#legend .item{display:flex;align-items:center;gap:6px;margin:3px 0;color:#999}
#legend .dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
#legend .line{width:16px;height:2px;flex-shrink:0;border-radius:1px}
#legend .title{color:#888;font-weight:600;margin-bottom:4px;font-size:11px}
#sidebar{position:fixed;right:0;top:0;width:360px;height:100vh;background:rgba(15,15,22,0.97);border-left:1px solid #2a2a35;padding:20px;overflow-y:auto;transform:translateX(360px);transition:transform 0.3s;z-index:100}
#sidebar.open{transform:translateX(0)}
#sidebar h2{font-size:15px;color:#fff;margin-bottom:6px;line-height:1.4}
#sidebar .meta{font-size:11px;color:#666;margin-bottom:3px}
#sidebar .insight{font-size:12px;color:#bbb;line-height:1.6;margin-top:10px;padding:10px;background:rgba(255,255,255,0.04);border-radius:6px;border-left:3px solid #6366f1}
#sidebar .close{position:absolute;top:10px;right:14px;cursor:pointer;color:#555;font-size:22px;z-index:1}
#sidebar .conn{margin:4px 0;font-size:11px;color:#999}
#sidebar .conn span.tag{display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px;margin-right:4px}
#filters{position:fixed;top:50px;left:12px;z-index:50;display:flex;gap:6px;flex-wrap:wrap;max-width:600px}
.filter-btn{padding:4px 12px;border:1px solid #333;border-radius:16px;background:rgba(15,15,22,0.9);color:#888;cursor:pointer;font-size:11px;transition:all 0.2s;pointer-events:auto}
.filter-btn:hover{border-color:#555;color:#ccc}
.filter-btn.active{background:rgba(99,102,241,0.15);border-color:#6366f1;color:#a5b4fc}
#search{position:fixed;top:50px;right:12px;z-index:50;background:rgba(15,15,22,0.9);border:1px solid #333;border-radius:8px;padding:6px 12px;color:#fff;font-size:12px;width:180px}
#search::placeholder{color:#555}
#stats{position:fixed;bottom:12px;right:12px;z-index:50;font-size:11px;color:#555}
</style>
</head>
<body>
<div id="header"><h1>🌐 __TITLE__</h1><p id="header-sub">Loading...</p></div>
<div id="filters">
<button class="filter-btn active" data-action="all">All</button>
<button class="filter-btn" data-action="L1" style="border-color:#6366f155">L1</button>
<button class="filter-btn" data-action="L2" style="border-color:#10b98155">L2</button>
<button class="filter-btn" data-action="L3" style="border-color:#f59e0b55">L3</button>
<button class="filter-btn" data-action="explicit">🔴 Explicit</button>
<button class="filter-btn" data-action="concept">🔵 Concept</button>
</div>
<input id="search" type="text" placeholder="Search nodes..." autocomplete="off">
<canvas id="canvas"></canvas>
<div id="sidebar"><span class="close" onclick="closeSidebar()">×</span><div id="sidebar-content"></div></div>
<div id="legend">
<div class="title">Legend</div>
__LEGEND__
<div style="margin-top:6px;border-top:1px solid #333;padding-top:6px;">
<div class="item"><div class="line" style="background:#ef4444"></div> Explicit</div>
<div class="item"><div class="line" style="background:#3b82f6"></div> Concept</div>
<div class="item"><div class="line" style="background:#2a2a35"></div> Cluster</div>
</div>
</div>
<div id="stats"></div>
<script>
const GRAPH=__GRAPH_JSON__;
document.getElementById('header-sub').textContent=GRAPH.nodes.length+' nodes · '+GRAPH.edges.length+' edges';
const canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d');
let W,H;function resize(){W=canvas.width=innerWidth;H=canvas.height=innerHeight}resize();addEventListener('resize',resize);
const catCenters={};const cats=[...new Set(GRAPH.nodes.map(n=>n.category))];const angleStep=(Math.PI*2)/cats.length;
cats.forEach((c,i)=>{const a=i*angleStep;catCenters[c]={x:W/2+Math.cos(a)*250,y:H/2+Math.sin(a)*200}});
const nodes=GRAPH.nodes.map(n=>{const c=catCenters[n.category]||{x:W/2,y:H/2};return{...n,x:c.x+(Math.random()-0.5)*150,y:c.y+(Math.random()-0.5)*120,vx:0,vy:0,size:n.isFramework?14:7}});
const edges=GRAPH.edges;const nodeMap={};nodes.forEach(n=>nodeMap[n.id]=n);
let activeLayer=null,edgeFilter=null,searchTerm='',hovered=null,selected=null;
function visible(n){if(activeLayer&&n.layer!==activeLayer)return false;if(searchTerm&&!n.label.toLowerCase().includes(searchTerm)&&!n.id.toLowerCase().includes(searchTerm))return false;return true}
function eVisible(e){if(edgeFilter&&e.type!==edgeFilter)return false;return true}
function simulate(){const ns=nodes.filter(visible);
for(let i=0;i<ns.length;i++){const a=ns[i];a.vx*=0.88;a.vy*=0.88;for(let j=i+1;j<ns.length;j++){const b=ns[j];const dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy;if(d2<10000){const d=Math.sqrt(d2)||1,f=600/d2;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f}}}
edges.forEach(e=>{if(!eVisible(e))return;const a=nodeMap[e.source],b=nodeMap[e.target];if(!a||!b||!visible(a)||!visible(b))return;const dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)||1,target=e.type==='explicit'?120:(e.type==='concept'?140:80),f=(d-target)*0.003*(e.width||1);a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f});
ns.forEach(n=>{const c=catCenters[n.category]||{x:W/2,y:H/2};n.vx+=(c.x-n.x)*0.0008;n.vy+=(c.y-n.y)*0.0008;n.x+=n.vx;n.y+=n.vy;n.x=Math.max(50,Math.min(W-50,n.x));n.y=Math.max(50,Math.min(H-50,n.y))})}
function draw(){ctx.clearRect(0,0,W,H);
edges.forEach(e=>{const a=nodeMap[e.source],b=nodeMap[e.target];if(!a||!b||!visible(a)||!visible(b)||!eVisible(e))return;const hl=hovered&&(e.source===hovered.id||e.target===hovered.id);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=hl?'#fff':e.color;ctx.globalAlpha=hl?0.9:(e.type==='cluster'?0.15:(e.type==='concept'?0.25:0.5));ctx.lineWidth=hl?(e.width||1)+1:(e.width||1)*0.7;ctx.stroke();ctx.globalAlpha=1});
nodes.forEach(n=>{if(!visible(n))return;const isH=hovered===n,isS=selected===n,r=n.size+(isH?4:0);
if(n.isFramework){const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,r+10);g.addColorStop(0,n.color+'50');g.addColorStop(1,'transparent');ctx.beginPath();ctx.arc(n.x,n.y,r+10,0,Math.PI*2);ctx.fillStyle=g;ctx.fill()}
ctx.beginPath();ctx.arc(n.x,n.y,r,0,Math.PI*2);ctx.fillStyle=n.color;ctx.globalAlpha=isH||isS?1:0.8;ctx.fill();ctx.globalAlpha=1;
if(n.isFramework){ctx.beginPath();ctx.arc(n.x,n.y,r-3,0,Math.PI*2);ctx.strokeStyle='#fff';ctx.lineWidth=1.2;ctx.stroke()}
if(n.isFramework||isH||n.size>10){ctx.fillStyle=isH?'#fff':'#ccc';ctx.font=(n.isFramework?'bold ':'')+(isH?'12':'10')+'px "PingFang SC",sans-serif';ctx.textAlign='center';const lbl=n.label.length>20?n.label.substring(0,18)+'…':n.label;ctx.fillText(lbl,n.x,n.y+r+14)}})}
function loop(){simulate();draw();requestAnimationFrame(loop)}
canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;hovered=null;for(const n of nodes){if(!visible(n))continue;const dx=mx-n.x,dy=my-n.y;if(dx*dx+dy*dy<(n.size+3)**2){hovered=n;break}}canvas.style.cursor=hovered?'pointer':'default'});
canvas.addEventListener('click',e=>{const r=canvas.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;for(const n of nodes){if(!visible(n))continue;const dx=mx-n.x,dy=my-n.y;if(dx*dx+dy*dy<(n.size+3)**2){selected=n;showSidebar(n);return}}});
function showSidebar(n){const conns=edges.filter(e=>e.source===n.id||e.target===n.id);const connHtml=conns.map(e=>{const oid=e.source===n.id?e.target:e.source;const o=nodeMap[oid];if(!o)return'';const tc=e.type==='explicit'?'#ef4444':(e.type==='concept'?'#3b82f6':'#555');const tn=e.type==='explicit'?'explicit':(e.type==='concept'?'concept':'cluster');return'<div class="conn"><span class="tag" style="background:'+tc+'33;color:'+tc+'">'+tn+'</span><span style="color:#aaa">'+o.label.substring(0,30)+'</span>'+(e.label?' <span style="color:#555">'+e.label+'</span>':'')+'</div>'}).join('');
document.getElementById('sidebar-content').innerHTML='<div class="meta">'+(n.layer||'?')+' · '+(n.isFramework?'🔑 Framework':'📄 Entry')+'</div><div class="meta">Category: '+(n.category||'—')+'</div>'+(n.date?'<div class="meta">Date: '+n.date+'</div>':'')+'<h2 style="margin-top:10px">'+n.label+'</h2>'+(n.insight?'<div class="insight">'+n.insight+'</div>':'')+(n.summary&&n.summary!==n.label?'<div style="margin-top:8px;font-size:12px;color:#888">'+n.summary+'</div>':'')+'<div style="margin-top:16px;font-size:12px;color:#666;font-weight:600">Connections ('+conns.length+')</div><div style="margin-top:6px">'+(connHtml||'<div class="conn">No connections</div>')+'</div>';
document.getElementById('sidebar').classList.add('open')}
function closeSidebar(){document.getElementById('sidebar').classList.remove('open');selected=null}
document.querySelectorAll('.filter-btn').forEach(btn=>{btn.addEventListener('click',()=>{const action=btn.dataset.action;if(action==='all'){activeLayer=null;edgeFilter=null;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active')}else if(action.startsWith('L')){activeLayer=activeLayer===action?null:action;document.querySelectorAll('.filter-btn').forEach(b=>{if(b.dataset.action!==action)b.classList.remove('active')});btn.classList.toggle('active',activeLayer===action)}else{edgeFilter=edgeFilter===action?null:action;btn.classList.toggle('active',edgeFilter===action)}updateStats()})});
document.getElementById('search').addEventListener('input',e=>{searchTerm=e.target.value.toLowerCase();updateStats()});
function updateStats(){document.getElementById('stats').textContent=nodes.filter(visible).length+' / '+nodes.length+' visible'}
updateStats();loop();
</script>
</body>
</html>'''

    html = (html_template
            .replace("__TITLE__", title)
            .replace("__LEGEND__", legend_items)
            .replace("__GRAPH_JSON__", graph_json))

    with open(output_path, "w") as f:
        f.write(html)
    return len(html)


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Build interactive knowledge graph HTML")
    parser.add_argument("--vault", default=DEFAULT_VAULT, help="Path to knowledge vault root")
    parser.add_argument("--config", default=None, help="Path to config JSON/YAML (optional)")
    parser.add_argument("--output", default=None, help="Output HTML path")
    parser.add_argument("--title", default="Knowledge Graph", help="Graph title")
    parser.add_argument("--dry-run", action="store_true", help="Print stats only, no HTML")
    args = parser.parse_args()

    vault = os.path.abspath(args.vault)
    index_path = os.path.join(vault, "references/INDEX.md")
    cards_dir = os.path.join(vault, "03-sources/article-cards")
    output_path = args.output or os.path.join(vault, DEFAULT_OUTPUT)

    cfg = load_config(args.config)

    # 1. Parse sources
    categories = parse_index(index_path)
    total = sum(len(items) for _, _, items in categories)
    print(f"Parsed: {len(categories)} categories, {total} entries")

    card_meta = parse_cards(cards_dir)
    print(f"Card metadata: {len(card_meta)} entries")

    # 2. Build graph
    nodes = build_nodes(categories, card_meta, cfg)
    edges = build_edges(nodes, cfg)
    print(f"Total nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    for t in ["cluster", "concept", "explicit"]:
        c = sum(1 for e in edges if e["type"] == t)
        print(f"  {t}: {c}")

    # 3. Layer distribution
    lc = Counter(n.get("layer", "?") for n in nodes)
    print(f"Layer dist: {dict(lc)}")

    # 4. Generate
    if args.dry_run:
        print("\n(dry-run, skipping HTML generation)")
        return

    size = generate_html(nodes, edges, output_path, args.title)
    print(f"\n✅ Generated: {output_path}")
    print(f"   {len(nodes)} nodes, {len(edges)} edges, {size:,} bytes")


if __name__ == "__main__":
    main()

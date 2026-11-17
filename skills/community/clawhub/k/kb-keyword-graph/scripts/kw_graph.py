#!/usr/bin/env python3
"""kb-keyword-graph engine — 2brain 关键词图谱四任务客户端。

子命令（都对同一份三层 keywords_tree 做不同呈现）：
  structure            知识结构：三层主题大纲 + 各层计数
  topics               主题分布：一级主题按占比/平台权重排序
  graph  [--html OUT]  关键词图谱：渐进展开的环形交互 HTML（点一级出二级、点二级出三级）
  relate --a X --b Y   资料关系：定位两个关键词在树中的位置，报告最近公共主题与共现关系
  fetch                仅拉取并缓存原始树（排错用）

凭证解析顺序（token 绝不写入任何产物/日志）：
  1) 环境变量 TWOBRAIN_GRAPH_KEY (+ TWOBRAIN_BASE_ID 或 --base-id)
  2) 私有配置 ~/.config/2brain-keyword-map/config.json  {"token","base_id"}
命中的树缓存到  <state>/graphs/<base_id>.json，--fresh 强制重拉。

用法示例：
  kw_graph.py structure --base-id 700
  kw_graph.py graph --base-id 700 --html /tmp/kw-700.html
  kw_graph.py topics --base-id 700
  kw_graph.py relate --a Visa --b Sponsorship --base-id 700
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = os.environ.get("TWOBRAIN_API_BASE", "https://test.2brain.ai/api")
ENDPOINT = API_BASE.rstrip("/") + "/kbase/keywords/keyword_api"
CONFIG = Path(os.environ.get("KWGRAPH_CONFIG",
              str(Path.home() / ".config" / "2brain-keyword-map" / "config.json")))
STATE = Path(os.environ.get("KWGRAPH_STATE",
              str(Path.home() / ".local" / "state" / "2brain-keyword-map")))


# ---------------------------------------------------------------- credentials

def _resolve(base_id_arg):
    """Return (token, base_id). token from env or private JSON; never printed."""
    token = os.environ.get("TWOBRAIN_GRAPH_KEY", "").strip()
    base_id = base_id_arg or os.environ.get("TWOBRAIN_BASE_ID")
    if (not token or not base_id) and CONFIG.exists():
        try:
            cfg = json.loads(CONFIG.read_text())
            token = token or str(cfg.get("token", "")).strip()
            base_id = base_id or cfg.get("base_id")
        except Exception as e:  # noqa: BLE001
            _die(f"配置文件无法读取: {CONFIG} ({e})")
    if not token:
        _die("缺少 2brain 图谱 Key。设 TWOBRAIN_GRAPH_KEY，或在 "
             f"{CONFIG} 写入 {{\"token\":\"2B-...\",\"base_id\":700}}。")
    try:
        base_id = int(base_id)
        assert base_id > 0
    except Exception:
        _die("缺少有效的整数 base_id（--base-id / TWOBRAIN_BASE_ID / 配置文件）。")
    return token, base_id


def _die(msg, code=2):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


# ------------------------------------------------------------------- fetch

def fetch_tree(token, base_id, fresh=False):
    cache = STATE / "graphs" / f"{base_id}.json"
    if cache.exists() and not fresh:
        try:
            c = json.loads(cache.read_text())
            c["keywords_tree"] = _normalise(c.get("keywords_tree") or [])
            return c
        except Exception:  # noqa: BLE001
            pass
    req = urllib.request.Request(
        ENDPOINT, method="POST",
        data=json.dumps({"base_id": base_id}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # 有些服务器/WAF 会挂起没有 User-Agent 的请求，必须带上
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/126.0 Safari/537.36 kb-keyword-graph/1.0",
        },
    )
    print("… 正在向 2brain 拉取关键词树，请稍候", file=sys.stderr)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:200]
        if e.code in (401, 403):
            _die(f"图谱 Key 无效或过期(HTTP {e.code})，请到 2brain 平台重新生成。")
        _die(f"2brain 请求失败 HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        _die(f"无法连接 2brain（{e.reason}）。本机需能访问 {API_BASE}。")
    tree = payload.get("keywords_tree")
    if not isinstance(tree, list) or not tree:
        _die("响应里没有非空的 keywords_tree —— 该库资料可能不足以成图，或尚未解析完成。")
    out = {"keywords_tree": _normalise(tree),
           "base_id": base_id,
           "file_count": len(payload.get("files", []) or []),
           "tree_id": payload.get("id")}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out, ensure_ascii=False))
    return out


def _normalise(nodes):
    out = []
    for n in nodes:
        out.append({
            "keyword": str(n.get("keyword", "")).strip(),
            "count": max(0, int(n.get("count") or 0)),
            "weights": max(0, int(n.get("weights") or 0)),
            "children": _normalise(n.get("children") or []),
        })
    return out


# --------------------------------------------------------------- shared math

def sibling_pct(node, siblings):
    total = sum(x["count"] for x in siblings)
    return round(node["count"] / total * 100, 1) if total else None


def counts(tree):
    l1 = len(tree)
    l2 = sum(len(n["children"]) for n in tree)
    l3 = sum(len(c["children"]) for n in tree for c in n["children"])
    return l1, l2, l3


# ---------------------------------------------------------------- subcommands

def cmd_structure(data):
    tree = data["keywords_tree"]
    l1, l2, l3 = counts(tree)
    outline = []
    for n in tree:
        outline.append({
            "keyword": n["keyword"], "count": n["count"],
            "share_pct": sibling_pct(n, tree),
            "subtopics": [{"keyword": c["keyword"], "count": c["count"],
                           "leaves": [g["keyword"] for g in c["children"]]}
                          for c in n["children"]],
        })
    return {"ok": True, "task": "structure", "base_id": data["base_id"],
            "file_count": data["file_count"],
            "levels": {"l1": l1, "l2": l2, "l3": l3}, "outline": outline}


def cmd_topics(data):
    tree = data["keywords_tree"]
    topics = sorted(
        ({"keyword": n["keyword"], "count": n["count"],
          "share_pct": sibling_pct(n, tree), "platform_weight": n["weights"],
          "subtopic_count": len(n["children"])} for n in tree),
        key=lambda t: t["count"], reverse=True)
    return {"ok": True, "task": "topics", "base_id": data["base_id"],
            "file_count": data["file_count"],
            "note": "share_pct=该主题在全部一级主题里的 count 占比；"
                    "platform_weight=2brain 给出的同级重要度(0-100)。二者视角不同。",
            "topics": topics}


def _find(tree, kw):
    """Return list of paths (each a list of keyword strings) where kw appears (ci)."""
    hits, low = [], kw.strip().lower()
    def walk(nodes, path):
        for n in nodes:
            p = path + [n["keyword"]]
            if n["keyword"].strip().lower() == low:
                hits.append(p)
            walk(n["children"], p)
    walk(tree, [])
    return hits


def cmd_relate(data, a, b):
    tree = data["keywords_tree"]
    pa, pb = _find(tree, a), _find(tree, b)
    if not pa or not pb:
        missing = ", ".join(x for x, p in ((a, pa), (b, pb)) if not p)
        return {"ok": True, "task": "relate", "base_id": data["base_id"],
                "related": None,
                "message": f"关键词未在图谱中出现: {missing}。图谱只覆盖 API 返回的关键词，"
                           "换个词或先看 structure 确认可用关键词。"}
    # 取首条路径做主判定
    a_path, b_path = pa[0], pb[0]
    common = []
    for x, y in zip(a_path, b_path):
        if x == y:
            common.append(x)
        else:
            break
    if len(common) == len(a_path) or len(common) == len(b_path):
        rel = "ancestor-descendant"
        desc = f"「{a_path[-1]}」与「{b_path[-1]}」在同一主题链上（一个是另一个的上/下位）。"
    elif common:
        rel = "shared-parent" if len(common) >= max(len(a_path), len(b_path)) - 1 else "cousin"
        desc = (f"「{a}」与「{b}」同属主题「{common[-1]}」之下"
                + ("，是直接同级子话题。" if rel == "shared-parent" else "，但在不同分支（远亲）。"))
    else:
        rel = "unrelated-in-graph"
        desc = f"「{a}」与「{b}」分属不同的一级主题（{a_path[0]} vs {b_path[0]}），图谱中无共同上位主题。"
    return {"ok": True, "task": "relate", "base_id": data["base_id"],
            "a": {"keyword": a, "path": a_path},
            "b": {"keyword": b, "path": b_path},
            "lowest_common_topic": common[-1] if common else None,
            "relation": rel, "explanation": desc,
            "caveat": "关系仅表示两词在 2brain 关键词树里的层级同现，不代表因果、语义等价或文档级来源。"}


# ------------------------------------------------------------ ring HTML render

def render_html(data):
    tree = data["keywords_tree"]
    base_id = data["base_id"]
    payload = json.dumps(tree, ensure_ascii=False)
    return _HTML.replace("__BASE__", str(base_id)).replace("__DATA__", payload)


_HTML = r"""<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<title>2Brain 关键词图谱 __BASE__</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f6f8fc;color:#172033;font:14px system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
header{padding:16px 24px;background:#fff;border-bottom:1px solid #dce5f0}h1{margin:0;font-size:20px}p{margin:5px 0;color:#62728a}
.canvas{position:relative;width:min(900px,96vw);height:min(800px,86vh);min-height:560px;margin:14px auto}
.node{position:absolute;left:50%;top:50%;border:0;border-radius:16px;padding:9px 12px;color:#fff;box-shadow:0 5px 15px #1a365933;text-align:left;cursor:pointer;transition:transform .18s,outline .18s;max-width:150px;min-width:92px}
.node:hover{outline:3px solid #17203333}.node.active{outline:4px solid #172033}.node b,.node span{display:block}.node span{font-size:12px;margin-top:4px;opacity:.95}
.ringHint{position:absolute;left:50%;top:50%;translate:-50% -50%;width:82px;height:82px;border-radius:50%;border:1px dashed #b6c5d8;pointer-events:none}
.legend{max-width:460px;margin:0 auto 22px}.scale{height:14px;border-radius:7px;background:linear-gradient(90deg,#2398e8,#26c878,#f1d536,#e63526)}
.labels{display:flex;justify-content:space-between;color:#62728a;margin-top:5px}.note{text-align:center}.empty{position:absolute;left:50%;top:50%;translate:-50% -50%;color:#62728a;pointer-events:none}
</style>
<header><h1>知识库 __BASE__ · 关键词图谱</h1><p id="sub">点一级主题展开二级；点二级展开三级。始终在同一张图内。</p></header>
<main><div id="app" class="canvas"></div>
<div class="legend"><div class="scale"></div><div class="labels"><span>0%</span><span>100%</span></div>
<p class="note">百分比 = 节点在其<b>直接兄弟</b>中的 count 占比（每组同级合计 100%）。蓝低 → 绿 → 黄 → 红高。不显示原始 count。</p></div></main>
<script>
const data=__DATA__,app=document.querySelector('#app'),sub=document.querySelector('#sub');let l1=null,l2=null;
const pct=(n,sib)=>{const t=sib.reduce((s,x)=>s+x.count,0);return t?n.count/t*100:null};
const label=p=>p===null?'—':p.toFixed(1)+'%';
const color=p=>{const q=Math.max(0,Math.min(100,p??0))/100;return 'hsl('+(205-200*q)+' 78% '+(52-5*q)+'%)'};
function at(n,p,a,r,kind,active,click){const x=Math.cos(a)*r,y=Math.sin(a)*r,s=.84+(p??0)/100*.28;return '<button class="node '+(active?'active':'')+'" data-kind="'+kind+'" data-i="'+click[0]+'" data-j="'+(click[1]??'')+'" style="background:'+color(p)+';transform:translate(calc(-50% + '+x+'px),calc(-50% + '+y+'px)) scale('+s+')"><b>'+n.keyword+'</b><span>'+label(p)+'</span></button>'}
function ring(nodes,r,kind,pi){const m=nodes.length||1;return nodes.map((n,i)=>at(n,pct(n,nodes),i/m*Math.PI*2-Math.PI/2,r,kind,(kind==='l1'&&i===l1)||(kind==='l2'&&i===l2),[pi??i,kind==='l2'?i:null])).join('')}
function render(){let h='<div class="ringHint"></div>'+ring(data,270,'l1');if(l1!==null){const k=data[l1].children;h+=k.length?ring(k,155,'l2',l1):'<div class="empty">没有二级主题</div>';if(l2!==null&&k[l2]){const lv=k[l2].children;h+=lv.length?ring(lv,64,'l3',l1):'<div class="empty">没有三级主题</div>'}}app.innerHTML=h;sub.textContent=l1===null?'点一级主题展开二级；点二级展开三级。始终在同一张图内。':l2===null?'已展开二级；点一个二级主题，三级会在内圈出现。':'三级已展开；点任意一级可切换分支。';app.querySelectorAll('.node').forEach(b=>b.onclick=()=>{if(b.dataset.kind==='l1'){l1=+b.dataset.i;l2=null}else if(b.dataset.kind==='l2'){l1=+b.dataset.i;l2=+b.dataset.j}render()})}
render();
</script></html>"""


# ----------------------------------------------------------- backend dispatch

def _read_config_file():
    if CONFIG.exists():
        try:
            return json.loads(CONFIG.read_text())
        except Exception:  # noqa: BLE001
            return {}
    return {}


def load_data(args):
    """按 backend 取三层关键词树，返回统一 dict（keywords_tree / base_id / file_count）。
    twobrain（默认）走原生 keyword_api（缓存 by base_id，逻辑不变）；
    local / elasticsearch 走 backends.load_tree（缓存 by 配置指纹）。"""
    import hashlib
    cfg = _read_config_file()
    backend = (getattr(args, "backend", None) or os.environ.get("KWGRAPH_BACKEND")
               or cfg.get("backend") or "twobrain").lower()
    if backend == "twobrain":
        token, base_id = _resolve(args.base_id)
        return fetch_tree(token, base_id, fresh=args.fresh)
    cfg = dict(cfg); cfg["backend"] = backend
    for k, v in (("corpus_dir", getattr(args, "corpus", None)),
                 ("es_url", getattr(args, "es_url", None)),
                 ("index", getattr(args, "index", None))):
        if v:
            cfg[k] = v
    fp = hashlib.sha1(json.dumps({k: cfg.get(k) for k in
        ("backend", "corpus_dir", "es_url", "index", "query")}, sort_keys=True).encode()
        ).hexdigest()[:12]
    cache = STATE / "graphs" / f"{backend}-{fp}.json"
    if cache.exists() and not args.fresh:
        try:
            c = json.loads(cache.read_text())
            c["keywords_tree"] = _normalise(c.get("keywords_tree") or [])
            return c
        except Exception:  # noqa: BLE001
            pass
    import backends
    try:
        data = backends.load_tree(cfg)
    except Exception as e:  # noqa: BLE001
        _die(str(e))
    data["keywords_tree"] = _normalise(data.get("keywords_tree") or [])
    data.setdefault("file_count", None)
    data["base_id"] = data.get("source", backend)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(data, ensure_ascii=False))
    return data


# ------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="KB 关键词图谱四任务引擎（多后端）")
    ap.add_argument("task", choices=["structure", "topics", "graph", "relate", "fetch"])
    ap.add_argument("--base-id", type=int, help="twobrain 后端：目标库整数 id")
    ap.add_argument("--backend", help="twobrain(默认) | local | elasticsearch；也可在 config 里设")
    ap.add_argument("--corpus", help="local 后端：本地文档目录")
    ap.add_argument("--es-url", dest="es_url", help="elasticsearch 后端：ES 地址")
    ap.add_argument("--index", help="elasticsearch 后端：索引名")
    ap.add_argument("--html", help="graph 任务：HTML 输出绝对路径")
    ap.add_argument("--a"); ap.add_argument("--b")
    ap.add_argument("--fresh", action="store_true", help="忽略缓存，强制重拉")
    args = ap.parse_args()

    data = load_data(args)
    base_id = data["base_id"]

    if args.task == "fetch":
        l1, l2, l3 = counts(data["keywords_tree"])
        out = {"ok": True, "task": "fetch", "base_id": base_id,
               "file_count": data["file_count"], "levels": {"l1": l1, "l2": l2, "l3": l3},
               "metric": "sibling_count_percentage"}
    elif args.task == "structure":
        out = cmd_structure(data)
    elif args.task == "topics":
        out = cmd_topics(data)
    elif args.task == "relate":
        if not args.a or not args.b:
            _die("relate 需要 --a 和 --b 两个关键词。")
        out = cmd_relate(data, args.a, args.b)
    elif args.task == "graph":
        page = render_html(data)
        safe = re.sub(r"[^A-Za-z0-9]+", "-", str(base_id)).strip("-")[:40] or "kb"
        outp = Path(args.html) if args.html else (STATE / "graphs" / f"kw-{safe}.html")
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(page, encoding="utf-8")
        l1, l2, l3 = counts(data["keywords_tree"])
        out = {"ok": True, "task": "graph", "base_id": base_id,
               "file_count": data["file_count"], "levels": {"l1": l1, "l2": l2, "l3": l3},
               "metric": "sibling_count_percentage", "html": str(outp)}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

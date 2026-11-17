#!/usr/bin/env python3
"""KB 后端适配器 —— 把"拿到三层关键词树"这一步抽象成可插拔后端。

渲染器 + 四任务（structure/graph/topics/relate）都只吃一份归一化的 keywords_tree，
所以换知识库只需换这里的一个适配器。每个适配器返回：
    {"keywords_tree": [...], "source": <str>, "file_count": <int>}
其中 keywords_tree 的每个节点是 {keyword, count, weights?, children:[...]}（三层）。

后端：
- twobrain      : 调 2brain 原生 keyword_api，直接拿现成三层树（见 kw_graph.py，未改）
- local         : 从本地文档目录**自算**关键词树（stdlib，无第三方依赖）——AI Digest 等
                  自建库融合走这条
- elasticsearch : 用 ES significant_text 聚合算树（HW6 那个学员的路子）——需要 ES 实例

设计：local 用「全局词频取一级 → 共现取二/三级」的启发式建层次，可解释、够用；
不追求和 2brain 逐节点一致（本就不同引擎）。
"""
from __future__ import annotations

import json
import re
import urllib.request
import urllib.error
from collections import Counter, defaultdict
from pathlib import Path

# 轻量英文停用词（本地建树用；中文语料建议先分词，见下方 TODO）
_STOP = set("""a an the and or but if then else for to of in on at by with from as is are was were be been
being this that these those it its it's he she they them his her their our your you i we me my mine us
will would can could should may might must do does did done have has had not no nor so than too very just
about into over under more most other some such only own same then once here there when where why how all
any both each few other some what which who whom whose we you your his her they them their this that will
job jobs role roles work working team teams company companies engineer engineering software system systems
data new use used using help via etc""".split())

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-]{2,}")


def load_tree(cfg: dict) -> dict:
    """按 cfg['backend'] 分发。twobrain 由 kw_graph.py 自己处理，这里只管非 2brain。"""
    backend = (cfg.get("backend") or "twobrain").lower()
    if backend == "local":
        return build_local_tree(cfg)
    if backend == "elasticsearch":
        return build_es_tree(cfg)
    raise ValueError(f"未知 backend: {backend}（支持 twobrain / local / elasticsearch）")


# ----------------------------------------------------------------- local corpus

def _read_docs(corpus_dir: Path, max_docs: int, max_chars: int):
    docs = []
    for p in sorted(corpus_dir.rglob("*")):
        if p.suffix.lower() not in (".txt", ".md", ".markdown"):
            continue
        try:
            docs.append(p.read_text(encoding="utf-8", errors="replace")[:max_chars])
        except OSError:
            continue
        if len(docs) >= max_docs:
            break
    return docs


def _tokens(text: str):
    seen = []
    for m in _WORD.finditer(text.lower()):
        w = m.group(0).strip(".-")
        if len(w) >= 3 and w not in _STOP and not w.isdigit():
            seen.append(w)
    return seen


def build_local_tree(cfg: dict) -> dict:
    """从本地文档目录自算三层关键词树（stdlib）。

    config: {"backend":"local","corpus_dir":"/path","l1":10,"l2":3,"l3":3,
             "max_docs":500,"max_chars":20000}
    算法：全局词频取一级概念；对每个一级，取与它在同文档中共现最强的词做二级；
    对每个二级同理取三级。count=全局词频；weights=同级内归一化(0-100)。
    """
    corpus = Path(cfg.get("corpus_dir") or cfg.get("corpus") or "").expanduser()
    if not corpus.is_dir():
        raise ValueError(f"local backend 需要有效的 corpus_dir（当前: {corpus}）")
    n1 = int(cfg.get("l1", 10)); n2 = int(cfg.get("l2", 3)); n3 = int(cfg.get("l3", 3))
    docs = _read_docs(corpus, int(cfg.get("max_docs", 500)), int(cfg.get("max_chars", 20000)))
    if not docs:
        raise ValueError(f"corpus_dir 里没有可读的 .txt/.md 文档: {corpus}")

    doc_tokens = [set(_tokens(d)) for d in docs]     # 每文档去重词集（共现用）
    freq = Counter()
    for d in docs:
        freq.update(_tokens(d))                       # 全局词频（count 用）
    if not freq:
        raise ValueError("语料里提取不到有效关键词")

    # 共现：cooc[a][b] = 同时出现 a、b 的文档数
    cooc = defaultdict(Counter)
    for toks in doc_tokens:
        toks = list(toks)
        for i, a in enumerate(toks):
            for b in toks[i + 1:]:
                cooc[a][b] += 1
                cooc[b][a] += 1

    def top_cooc(word, k, exclude):
        cands = [(w, c) for w, c in cooc[word].most_common(k * 4)
                 if w not in exclude and w != word]
        return [w for w, _ in cands[:k]]

    l1_words = [w for w, _ in freq.most_common(n1)]
    tree = []
    for w1 in l1_words:
        used = {w1}
        l2_nodes = []
        for w2 in top_cooc(w1, n2, used):
            used.add(w2)
            l3_nodes = []
            for w3 in top_cooc(w2, n3, used):
                used.add(w3)
                l3_nodes.append({"keyword": w3.title(), "count": freq[w3], "children": []})
            l2_nodes.append({"keyword": w2.title(), "count": freq[w2], "children": l3_nodes})
        tree.append({"keyword": w1.title(), "count": freq[w1], "children": l2_nodes})

    _add_sibling_weights(tree)
    return {"keywords_tree": tree, "source": f"local:{corpus}", "file_count": len(docs)}


def _add_sibling_weights(nodes):
    total = sum(n["count"] for n in nodes) or 1
    for n in nodes:
        n["weights"] = round(n["count"] / total * 100)
        _add_sibling_weights(n["children"])


# ----------------------------------------------------------------- elasticsearch

def build_es_tree(cfg: dict) -> dict:
    """用 ES significant_text 聚合建树（需要一个 Elasticsearch 实例）。

    config: {"backend":"elasticsearch","es_url":"http://localhost:9200",
             "index":"market_news_rag","text_field":"text","query":"...",
             "l1":10,"l2":3,"l3":3,"days":30}
    思路（HW6 学员的路子）：对 text_field 做 significant_text 聚合取一级显著词；
    对每个一级词加 filter 再聚合取二/三级。这里给出可运行的最小实现（stdlib urllib）。
    """
    es = (cfg.get("es_url") or "http://localhost:9200").rstrip("/")
    index = cfg.get("index")
    field = cfg.get("text_field", "text")
    if not index:
        raise ValueError("elasticsearch backend 需要 config.index")
    n1 = int(cfg.get("l1", 10)); n2 = int(cfg.get("l2", 3)); n3 = int(cfg.get("l3", 3))

    def sig_terms(filter_terms, size):
        must = [{"match": {field: t}} for t in filter_terms]
        body = {
            "size": 0,
            "query": {"bool": {"must": must}} if must else {"match_all": {}},
            "aggs": {"sig": {"significant_text": {"field": field, "size": size}}},
        }
        req = urllib.request.Request(
            f"{es}/{index}/_search", method="POST",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
        except urllib.error.URLError as e:
            raise ValueError(f"连不上 Elasticsearch {es}（{e.reason}）")
        return [(b["key"], b["doc_count"]) for b in
                resp.get("aggregations", {}).get("sig", {}).get("buckets", [])]

    l1 = sig_terms([], n1)
    if not l1:
        raise ValueError(f"ES index '{index}' 的 {field} 上 significant_text 无结果")
    tree = []
    for w1, c1 in l1:
        l2_nodes = []
        for w2, c2 in sig_terms([w1], n2):
            l3_nodes = [{"keyword": w3.title(), "count": c3, "children": []}
                        for w3, c3 in sig_terms([w1, w2], n3)]
            l2_nodes.append({"keyword": w2.title(), "count": c2, "children": l3_nodes})
        tree.append({"keyword": w1.title(), "count": c1, "children": l2_nodes})
    _add_sibling_weights(tree)
    return {"keywords_tree": tree, "source": f"es:{es}/{index}", "file_count": None}

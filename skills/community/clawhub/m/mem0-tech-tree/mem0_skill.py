#!/usr/bin/env python3
"""
Mem0 Tech Tree Memory System v5
================================
科技树架构：知识节点有依赖关系、解锁路径、协同加成

核心概念：
  节点(Node)：一条知识/技能/经验
  边(Edge)：依赖关系(A是B的前置)、关联关系(A和B协同)
  分支(Branch)：领域方向（技术/内容创作/学习/工作/生活）
  层级(Tier)：深度等级，越深越高级
  状态(State)：locked(前置未解锁) / available(可学习) / unlocked(已掌握) / mastered(精通)
  
检索流程：
  查节点 → 看依赖 → 找路径 → 返回知识+上下文+关联+下一步建议

文件结构：
  tree.json — 科技树数据（节点+边+分支）
"""

import sys
import json
import os
import time
import re
import math
from collections import Counter, defaultdict

CONFIG = {
    "mature_ttl": 300,            # 新节点→available时间（秒）
    "reindex_interval": 1800,     # 重建索引间隔
    "dedup_threshold": 0.6,       # 去重阈值
    "branch_max_tier": 10,        # 分支最大层级
    "similar_threshold": 0.25,    # 自动关联阈值
    "synergy_threshold": 0.35,    # 协同加成发现阈值
}

STOP_WORDS = frozenset({
    '的', '了', '和', '是', '在', '有', '我', '他', '她', '它', '这', '那',
    '你', '您', '我们', '他们', '如果', '但是', '因为', '所以', '虽然', '然而',
    '可以', '可能', '应该', '必须', '将', '已经', '正在', '关于', '对于',
    '为了', '通过', '使用', '实现', '一个', '这个', '那个', '什么', '怎么',
    '如何', '不是', '就是', '也', '都', '就', '还', '又', '把', '被', '让',
    '给', '到', '会', '能', '要', '想', '说', '去', '来', '做', '看', '没',
    '中', '上', '下', '里', '后', '前', '不', '很', '更', '最', '只', '则',
    'the', 'is', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'that', 'this', 'it', 'be', 'are', 'was',
})

BRANCH_RULES = {
    "技术": {'代码', '编程', 'Python', 'JavaScript', 'API', '部署', '服务器',
             'Linux', 'macOS', '开发', '框架', '插件', 'ComfyUI', 'OpenClaw',
             'AI', 'LLM', '模型', '训练', 'PyTorch', 'CUDA', 'Node', 'npm',
             'Docker', 'Git', 'GitHub', 'Chrome', '浏览器', '脚本', '自动化',
             'pip', 'homebrew', 'launchd', 'ffmpeg', 'playwright', 'CDP',
             'mem0', 'BM25', 'jieba', '知识图谱'},
    "内容创作": {'视频', '抖音', '文案', '配音', '素材', '发布',
                 '粉丝', '播放', '即梦', '剪映', '头图', '标题', '账号',
                 '豆包', 'Seedance', 'edge-tts', '风景片', '情绪价值'},
    "学习": {'学习', '研究', '论文', '文档', '教程', '课程', '笔记',
             '总结', '复习', '考试', '知识', '概念', '原理'},
    "工作": {'任务', '项目', '会议', '报告', '计划', '进度', '目标',
             '客户', '需求', '交付', '排期', 'KPI'},
    "生活": {'生活', '家庭', '朋友', '健康', '运动', '饮食', '旅行',
             '天气', '购物', '扬州', '生日', '节日'},
}

# 层级关键词——越高级的词tier越高
TIER_KEYWORDS = {
    1: {'了解', '知道', '听说', '大概', '基本'},
    2: {'学会', '理解', '会用', '掌握', '熟悉', '运行'},
    3: {'熟练', '优化', '改进', '部署', '配置', '集成'},
    4: {'精通', '架构', '设计', '原理', '底层', '源码'},
    5: {'创新', '自研', '突破', '独创', '跨领域', '理论'},
}

EPISODIC_MARKERS = {'昨天', '今天', '上周', '上个月', '明天', '刚才',
                    '讨论了', '完成了', '发生了', '试了', '跑了'}
PROCEDURAL_MARKERS = {'步骤', '流程', '操作', '安装', '配置', '部署',
                      '方法', '教程', '命令', '脚本', '运行', '执行'}
IMPORTANCE_MARKERS = {'重要', '关键', '必须', '紧急', '切记', '注意', '警告',
                      '教训', '不要', '禁止', '务必', '千万', '绝对', '核心'}


class TechTree:
    def __init__(self):
        self.tree_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree.json')
        self.data = self._load()

        self.use_jieba = False
        try:
            import jieba
            jieba.setLogLevel(20)
            self.jieba = jieba
            self.use_jieba = True
        except ImportError:
            pass

        self._pipeline()

    # ==================== I/O ====================

    def _load(self):
        try:
            if os.path.exists(self.tree_file):
                with open(self.tree_file, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    if isinstance(d, dict) and "nodes" in d:
                        return d
                    return self._migrate(d)
        except Exception:
            pass
        return self._default()

    def _migrate(self, old):
        """从旧版迁移"""
        nodes = {}
        all_mems = []
        for key in ["memories", "sensory", "working", "long_term",
                     "sensory_memory", "short_term_memory", "long_term_memory"]:
            all_mems.extend(old.get(key, []))
        for m in old.get("subjects", {}).values():
            all_mems.extend(m.get("memories", []))

        nid = 1
        for m in all_mems:
            branches = m.get("tags", [m.get("category", "其他")])
            content = m.get("content", "")
            keywords = m.get("keywords", self._tokenize(content))
            nid_str = f"n{nid:04d}"
            nodes[nid_str] = {
                "id": nid_str,
                "content": content,
                "keywords": keywords[:15],
                "branches": branches if isinstance(branches, list) else [branches],
                "tier": 2,
                "state": "unlocked",
                "importance": m.get("importance", "medium"),
                "types": m.get("types", ["semantic"]),
                "access_count": m.get("access_count", 0),
                "created": m.get("time_str", time.strftime("%Y-%m-%d %H:%M:%S")),
                "timestamp": m.get("timestamp", time.time()),
            }
            nid += 1

        return self._default_with_nodes(nodes)

    def _default(self):
        return {
            "version": 5,
            "nodes": {},
            "edges": [],           # [{"from": "n001", "to": "n002", "type": "dependency|synergy|related"}]
            "branches": {},        # {branch_name: {"tier": max_tier, "node_count": n, "top_keywords": [...]}}
            "catalog": {},         # keyword → [node_ids]
            "stats": {"total_nodes": 0, "total_edges": 0, "total_dedup": 0,
                      "last_reindex": None}
        }

    def _default_with_nodes(self, nodes):
        d = self._default()
        d["nodes"] = nodes
        d["stats"]["total_nodes"] = len(nodes)
        return d

    def _save(self):
        try:
            with open(self.tree_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ==================== NLP ====================

    def _tokenize(self, text):
        if self.use_jieba:
            return [w for w in self.jieba.cut(text) if len(w) >= 2 and w not in STOP_WORDS]
        text = re.sub(r'[，。！？、；：""''【】（）《》\s\.,!?;:()\[\]{}"\'\\\/\-\+=~`@#$%^&*0-9]', ' ', text)
        return [w for w in text.split() if len(w) >= 2 and w not in STOP_WORDS]

    def _cosine_sim(self, a, b):
        ta, tb = self._tokenize(a), self._tokenize(b)
        if not ta or not tb:
            return 0.0
        ca, cb = Counter(ta), Counter(tb)
        dot = sum(ca[t] * cb[t] for t in set(ca) | set(cb))
        mag = math.sqrt(sum(v**2 for v in ca.values())) * math.sqrt(sum(v**2 for v in cb.values()))
        return dot / mag if mag > 0 else 0.0

    def _detect_branches(self, content):
        tokens = set(self._tokenize(content))
        return [b for b, markers in BRANCH_RULES.items() if tokens & markers] or ["其他"]

    def _detect_tier(self, content):
        tokens = set(self._tokenize(content))
        for tier in sorted(TIER_KEYWORDS.keys(), reverse=True):
            if tokens & TIER_KEYWORDS[tier]:
                return tier
        return 2  # 默认中级

    def _detect_types(self, content):
        tokens = set(self._tokenize(content))
        types = set()
        if tokens & PROCEDURAL_MARKERS:
            types.add("procedural")
        if tokens & EPISODIC_MARKERS:
            types.add("episodic")
        if not types:
            types.add("semantic")
        return list(types)

    def _detect_importance(self, content):
        tokens = set(self._tokenize(content))
        return "high" if (tokens & IMPORTANCE_MARKERS) else "medium"

    # ==================== ID生成 ====================

    def _next_id(self):
        nodes = self.data["nodes"]
        if not nodes:
            return "n0001"
        max_id = max(int(nid[1:]) for nid in nodes)
        return f"n{max_id + 1:04d}"

    # ==================== 自动边发现 ====================

    def _discover_edges(self):
        """自动发现节点间的依赖和协同关系"""
        nodes = self.data["nodes"]
        if len(nodes) < 2:
            return

        existing_edges = {(e["from"], e["to"]) for e in self.data.get("edges", [])}
        new_edges = []
        node_ids = sorted(nodes.keys())

        # 同分支内：按相似度建立关联
        branch_groups = defaultdict(list)
        for nid, node in nodes.items():
            for b in node.get("branches", []):
                branch_groups[b].append(nid)

        for branch, nids in branch_groups.items():
            for i, a in enumerate(nids):
                for b in nids[i+1:]:
                    if (a, b) in existing_edges or (b, a) in existing_edges:
                        continue
                    sim = self._cosine_sim(nodes[a]["content"], nodes[b]["content"])
                    if sim >= CONFIG["similar_threshold"]:
                        # 层级低的→层级高的是依赖关系
                        tier_a = nodes[a].get("tier", 2)
                        tier_b = nodes[b].get("tier", 2)
                        if tier_a < tier_b:
                            edge_type = "dependency"  # A是B的前置
                        elif tier_a > tier_b:
                            edge_type = "dependency"  # B是A的前置
                        else:
                            edge_type = "related"  # 同级关联
                        new_edges.append({
                            "from": a if tier_a <= tier_b else b,
                            "to": b if tier_a <= tier_b else a,
                            "type": edge_type,
                            "similarity": round(sim, 3),
                            "branch": branch
                        })

        # 跨分支：协同加成
        branch_names = list(branch_groups.keys())
        for i in range(len(branch_names)):
            for j in range(i+1, len(branch_names)):
                ba, bb = branch_names[i], branch_names[j]
                for a in branch_groups[ba][:3]:  # 采样
                    for b in branch_groups[bb][:3]:
                        if (a, b) in existing_edges or (b, a) in existing_edges:
                            continue
                        sim = self._cosine_sim(nodes[a]["content"], nodes[b]["content"])
                        if sim >= CONFIG["synergy_threshold"]:
                            new_edges.append({
                                "from": a, "to": b,
                                "type": "synergy",
                                "similarity": round(sim, 3),
                                "branches": [ba, bb]
                            })

        self.data["edges"] = self.data.get("edges", []) + new_edges
        self.data["stats"]["total_edges"] = len(self.data["edges"])

    # ==================== 索引 ====================

    def _build_catalog(self):
        """关键词→节点ID的倒排索引"""
        catalog = {}
        for nid, node in self.data["nodes"].items():
            for kw in node.get("keywords", []):
                catalog.setdefault(kw, []).append(nid)
        self.data["catalog"] = catalog

    def _build_branches(self):
        """更新分支统计"""
        branches = {}
        for nid, node in self.data["nodes"].items():
            for b in node.get("branches", []):
                branches.setdefault(b, {"tier": 0, "node_count": 0, "top_keywords": []})
                branches[b]["node_count"] += 1
                branches[b]["tier"] = max(branches[b]["tier"], node.get("tier", 2))
                branches[b].setdefault("all_kw", []).extend(node.get("keywords", []))

        for b, info in branches.items():
            kw_count = Counter(info.get("all_kw", []))
            info["top_keywords"] = [w for w, _ in kw_count.most_common(8)]
            del info["all_kw"]

        self.data["branches"] = branches

    # ==================== 状态更新 ====================

    def _update_states(self):
        """根据依赖关系更新节点状态"""
        nodes = self.data["nodes"]
        edges = self.data.get("edges", [])
        now = time.time()

        # 建立依赖图：node → 需要哪些前置
        deps = defaultdict(set)  # to_node → {from_nodes}
        for e in edges:
            if e["type"] == "dependency":
                deps[e["to"]].add(e["from"])

        for nid, node in nodes.items():
            ts = node.get("timestamp", now)
            if isinstance(ts, str):
                ts = time.mktime(time.strptime(ts, "%Y-%m-%d %H:%M:%S"))
            age = now - ts

            # 新节点先标记available
            if node.get("state") == "new" and age > CONFIG["mature_ttl"]:
                node["state"] = "available"

            # 如果所有前置都unlocked，则available→unlocked
            if node.get("state") == "available":
                prereqs = deps.get(nid, set())
                if not prereqs or all(nodes.get(p, {}).get("state", "locked") in ("unlocked", "mastered") for p in prereqs):
                    node["state"] = "unlocked"

            # 高访问次数→mastered
            if node.get("state") == "unlocked" and node.get("access_count", 0) >= 5:
                node["state"] = "mastered"

    # ==================== 流水线 ====================

    def _pipeline(self):
        now = time.time()
        self._update_states()

        last = self.data["stats"].get("last_reindex")
        need = True
        if last:
            try:
                last_t = time.mktime(time.strptime(last, "%Y-%m-%d %H:%M:%S"))
                need = now - last_t >= CONFIG["reindex_interval"]
            except Exception:
                pass

        if need:
            self._discover_edges()
            self._build_catalog()
            self._build_branches()
            self.data["stats"]["last_reindex"] = time.strftime("%Y-%m-%d %H:%M:%S")

        self._save()

    # ==================== 公共API ====================

    def store(self, content, importance=None):
        # 去重
        for nid, node in self.data["nodes"].items():
            if self._cosine_sim(content, node["content"]) >= CONFIG["dedup_threshold"]:
                node["access_count"] = node.get("access_count", 0) + 1
                self.data["stats"]["total_dedup"] = self.data["stats"].get("total_dedup", 0) + 1
                self._save()
                return {"success": True, "message": f"节点已强化 (访问{node['access_count']}次)",
                        "data": {"node_id": nid, "access_count": node["access_count"]}}

        nid = self._next_id()
        keywords = self._tokenize(content)[:15]
        branches = self._detect_branches(content)
        tier = self._detect_tier(content)
        types = self._detect_types(content)
        imp = importance or self._detect_importance(content)

        self.data["nodes"][nid] = {
            "id": nid,
            "content": content,
            "keywords": keywords,
            "branches": branches,
            "tier": tier,
            "state": "new",
            "importance": imp,
            "types": types,
            "access_count": 0,
            "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": time.time(),
        }
        self.data["stats"]["total_nodes"] = len(self.data["nodes"])
        self._pipeline()

        return {"success": True,
                "message": f"🆕 {nid} | 分支:{branches} | 层级:T{tier} | 状态:new | 类型:{types}",
                "data": {"id": nid, "branches": branches, "tier": tier, "types": types}}

    def retrieve(self, query, top_k=10):
        """检索：目录→定位→路径→返回"""
        query_tokens = self._tokenize(query)
        catalog = self.data["catalog"]

        # 第1步：查目录定位节点
        located_ids = set()
        for qt in query_tokens:
            located_ids.update(catalog.get(qt, []))

        # 如果目录没命中，退回全量搜索
        if not located_ids:
            located_ids = set(self.data["nodes"].keys())

        nodes = self.data["nodes"]
        edges = self.data.get("edges", [])

        # 第2步：定位节点范围内评分
        scored = []
        for nid in located_ids:
            node = nodes.get(nid)
            if not node:
                continue

            score = 0.0
            # BM25式评分
            node_kw = node.get("keywords", [])
            node_tf = Counter(node_kw)
            for qt in query_tokens:
                if qt in node_tf:
                    tf = node_tf[qt]
                    df = len(catalog.get(qt, []))
                    idf = math.log(1 + max(1, len(nodes) - df) / (df + 0.5))
                    score += idf * tf

            cos = self._cosine_sim(query, node["content"])
            score += cos * 2

            # 重要性
            if node.get("importance") == "high":
                score *= 1.5

            # 访问频率
            score *= 1 + math.log1p(node.get("access_count", 0)) * 0.15

            # 状态权重：unlocked > available > mastered > new
            state_w = {"unlocked": 1.3, "mastered": 1.1, "available": 1.0, "new": 0.8}
            score *= state_w.get(node.get("state", "new"), 0.8)

            if score > 0.3:
                scored.append((score, nid))

        scored.sort(key=lambda x: x[0], reverse=True)

        # 第3步：构建结果，附带依赖路径和关联
        # 构建邻接表
        adj = defaultdict(list)  # from→[{to, type}]
        adj_rev = defaultdict(list)  # to→[{from, type}]
        for e in edges:
            adj[e["from"]].append({"id": e["to"], "type": e["type"], "sim": e.get("similarity", 0)})
            adj_rev[e["to"]].append({"id": e["from"], "type": e["type"], "sim": e.get("similarity", 0)})

        results = []
        for s, nid in scored[:top_k]:
            node = nodes[nid]
            r = {
                "id": nid,
                "content": node["content"],
                "branches": node.get("branches", []),
                "tier": node.get("tier", 2),
                "state": node.get("state", "new"),
                "types": node.get("types", []),
                "importance": node.get("importance", "medium"),
                "created": node.get("created", ""),
                "relevance": round(s, 2),
                "access_count": node.get("access_count", 0),
                "dependencies": [nodes[p["id"]]["content"][:30] + "..."
                                 for p in adj_rev[nid] if p["type"] == "dependency" and p["id"] in nodes][:3],
                "enables": [nodes[c["id"]]["content"][:30] + "..."
                            for c in adj[nid] if c["type"] == "dependency" and c["id"] in nodes][:3],
                "synergies": [nodes[sy["id"]]["content"][:30] + "..."
                              for sy in adj[nid] if sy["type"] == "synergy" and sy["id"] in nodes][:3],
            }
            results.append(r)

        located_branches = set()
        for s, nid in scored[:top_k]:
            located_branches.update(nodes[nid].get("branches", []))

        return {"success": True,
                "message": f"检索到 {len(results)} 条 | 分支: {list(located_branches)}",
                "data": results}

    def tree_map(self, branch=None, max_depth=3):
        """查看科技树地图"""
        nodes = self.data["nodes"]
        edges = self.data.get("edges", [])

        adj = defaultdict(list)
        for e in edges:
            adj[e["from"]].append({"id": e["to"], "type": e["type"]})

        # 筛选分支
        if branch:
            target_ids = {nid for nid, n in nodes.items() if branch in n.get("branches", [])}
        else:
            target_ids = set(nodes.keys())

        # 找根节点（没有前置依赖的）
        dep_to = {e["to"] for e in edges if e["type"] == "dependency"}
        roots = [nid for nid in target_ids if nid not in dep_to]
        if not roots:
            roots = sorted(target_ids)[:5]  # 没有明确的根，取最早的几个

        # BFS构建树
        visited = set()
        tree_lines = []
        state_icons = {"new": "⬜", "available": "🔘", "unlocked": "✅", "mastered": "⭐"}

        def bfs(node_id, depth, prefix=""):
            if depth > max_depth or node_id in visited or node_id not in nodes:
                return
            visited.add(node_id)
            n = nodes[node_id]
            icon = state_icons.get(n.get("state", "new"), "⬜")
            line = f"{prefix}{icon} T{n['tier']} [{n['id']}] {n['content'][:40]}"
            tree_lines.append(line)

            children = [c for c in adj[node_id] if c["id"] in target_ids]
            for i, child in enumerate(children):
                connector = "├─" if i < len(children) - 1 else "└─"
                bfs(child["id"], depth + 1, prefix + "│  ")

        for root in roots:
            bfs(root, 0)

        return {
            "success": True,
            "message": f"{'📚 ' + branch if branch else '🌐 全局'}科技树 ({len(target_ids)}个节点)",
            "data": "\n".join(tree_lines) if tree_lines else "(空树)"
        }

    def node_info(self, node_id):
        """查看单个节点详情"""
        node = self.data["nodes"].get(node_id)
        if not node:
            return {"success": False, "message": f"节点 {node_id} 不存在"}

        edges = self.data.get("edges", [])
        deps = [e for e in edges if e["to"] == node_id]
        enables = [e for e in edges if e["from"] == node_id]
        synergies = [e for e in edges if (e["from"] == node_id or e["to"] == node_id) and e["type"] == "synergy"]

        return {
            "success": True,
            "message": f"节点 {node_id}",
            "data": {
                "content": node["content"],
                "branches": node.get("branches", []),
                "tier": node.get("tier", 2),
                "state": node.get("state", "new"),
                "types": node.get("types", []),
                "importance": node.get("importance", "medium"),
                "created": node.get("created", ""),
                "access_count": node.get("access_count", 0),
                "keywords": node.get("keywords", []),
                "dependencies": [{"id": d["from"], "type": d["type"], "sim": d.get("similarity")}
                                 for d in deps],
                "enables": [{"id": e["to"], "type": e["type"], "sim": e.get("similarity")}
                            for e in enables],
                "synergies": [{"id": s["to"] if s["from"] == node_id else s["from"],
                               "branches": s.get("branches"), "sim": s.get("similarity")}
                              for s in synergies],
            }
        }

    def catalog_lookup(self, keyword):
        """查目录"""
        entries = self.data["catalog"].get(keyword, [])
        if not entries:
            fuzzy = [(k, v) for k, v in self.data["catalog"].items()
                     if keyword in k or k in keyword]
            if fuzzy:
                results = []
                for k, nids in fuzzy[:3]:
                    for nid in nids:
                        node = self.data["nodes"].get(nid)
                        if node:
                            results.append({"keyword": k, "node_id": nid,
                                            "preview": node["content"][:40],
                                            "branches": node.get("branches", [])})
                return {"success": True, "message": f"模糊匹配到 {len(results)} 条", "data": results}
            return {"success": False, "message": f"目录中无 '{keyword}'"}

        results = []
        for nid in entries:
            node = self.data["nodes"].get(nid)
            if node:
                results.append({"node_id": nid, "preview": node["content"][:40],
                                "branches": node.get("branches", []),
                                "tier": node.get("tier", 2),
                                "state": node.get("state", "new")})
        return {"success": True, "message": f"'{keyword}' → {len(results)}个节点", "data": results}

    def list_memories(self):
        nodes = self.data["nodes"]
        edges = self.data.get("edges", [])
        return {
            "success": True, "message": "科技树概览",
            "data": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "states": dict(Counter(n.get("state", "?") for n in nodes.values())),
                "branches": {b: {"count": info["node_count"], "max_tier": info["tier"],
                                 "top_kw": info["top_keywords"][:5]}
                             for b, info in self.data.get("branches", {}).items()},
                "edge_types": dict(Counter(e["type"] for e in edges)),
                "stats": self.data["stats"],
            }
        }

    def clear(self):
        self.data = self._default()
        self._save()
        return {"success": True, "message": "科技树已清除"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message":
            "用法:\n  mem0_skill.py store <内容>\n  mem0_skill.py retrieve <关键词>\n"
            "  mem0_skill.py tree [分支]\n  mem0_skill.py info <节点ID>\n"
            "  mem0_skill.py catalog <关键词>\n  mem0_skill.py list\n  mem0_skill.py clear"},
            ensure_ascii=False))
        sys.exit(1)

    cmd = sys.argv[1]
    skill = TechTree()

    if cmd == "store" and len(sys.argv) > 2:
        r = skill.store(" ".join(sys.argv[2:]))
    elif cmd == "retrieve" and len(sys.argv) > 2:
        r = skill.retrieve(" ".join(sys.argv[2:]))
    elif cmd == "tree":
        branch = sys.argv[2] if len(sys.argv) > 2 else None
        r = skill.tree_map(branch)
    elif cmd == "info" and len(sys.argv) > 2:
        r = skill.node_info(sys.argv[2])
    elif cmd == "catalog" and len(sys.argv) > 2:
        r = skill.catalog_lookup(" ".join(sys.argv[2:]))
    elif cmd == "list":
        r = skill.list_memories()
    elif cmd == "clear":
        r = skill.clear()
    else:
        r = {"success": False, "message": f"未知命令: {cmd}"}

    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

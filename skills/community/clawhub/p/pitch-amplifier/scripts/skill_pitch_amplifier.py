#!/usr/bin/env python3
"""
交互式灵感放大器（Skill 版）

将用户的模糊新闻观察，放大为可执行的深度报道策划案。
重点修复：fallback 生成不再写死某一个题材，而是根据图谱上下文动态生成。
"""

from __future__ import annotations

import ast
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[3] / "projects" / "city-knowledge-graph"
CORE_DIR = PROJECT_ROOT / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from graph_db import CityKnowledgeGraph  # noqa: E402


graph = CityKnowledgeGraph(str(PROJECT_ROOT / "graph_db" / "city_graph.db"))


def _build_llm_client() -> Optional[OpenAI]:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GLM_API_KEY")
    if not api_key:
        return None
    base_url = None
    if os.environ.get("GLM_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
        base_url = "https://open.bigmodel.cn/api/coding/paas/v4"
    kwargs: Dict[str, Any] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


LLM_CLIENT = _build_llm_client()
DEFAULT_MODEL = os.environ.get("PITCH_AMPLIFIER_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"


def load_graph_from_db(db_path: str) -> nx.Graph:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    G = nx.Graph()
    for row in conn.execute("SELECT * FROM nodes"):
        props = json.loads(row["properties_json"] or "{}")
        G.add_node(row["id"], name=row["name"], type=row["type"], properties=props, updated_at=row["updated_at"])
    for row in conn.execute("SELECT * FROM edges"):
        props = json.loads(row["properties_json"] or "{}")
        G.add_edge(row["source_id"], row["target_id"], relation=row["relation"], properties=props)
    for row in conn.execute("SELECT * FROM aliases"):
        if row["node_id"] in G.nodes:
            aliases = G.nodes[row["node_id"]].setdefault("aliases", [])
            aliases.append(row["alias_name"])
    conn.close()
    return G


GRAPH_NX = load_graph_from_db(str(PROJECT_ROOT / "graph_db" / "city_graph.db"))


def find_entity(name: str) -> Optional[Dict[str, Any]]:
    node_id = graph.get_node_id(name)
    if not node_id:
        return None
    row = graph.conn.cursor().execute(
        "SELECT id, name, type, properties_json, updated_at FROM nodes WHERE id = ?",
        (node_id,),
    ).fetchone()
    if not row:
        return None
    return {"id": row[0], "name": row[1], "type": row[2], "properties": json.loads(row[3] or "{}"), "updated_at": row[4]}


if not hasattr(graph, "find_entity"):
    setattr(graph, "find_entity", find_entity)
if not hasattr(graph, "G"):
    setattr(graph, "G", GRAPH_NX)


SYNONYM_MAP = {
    "七都岛": ["七都", "七都街道", "江心岛", "岛屿开发", "文旅岛"],
    "农家乐": ["民宿", "乡村旅游", "餐饮经营户", "休闲农业", "乡村经营"],
    "倒闭": ["歇业", "关停", "注销", "停业", "空置"],
    "开发": ["文旅开发", "项目开发", "保护性开发", "建设开发"],
    "旅游": ["文旅", "景区", "游客", "休闲"],
    "生态": ["湿地", "候鸟", "环保", "栖息地"],
    "园博园": ["园博", "展会", "大型活动", "分会场", "展后运营"],
    "交通": ["拥堵", "承载", "停车", "接驳", "高峰客流"],
}


def _safe_json_list(text: str) -> List[str]:
    if not text:
        return []
    text = text.strip()
    for parser in (json.loads, ast.literal_eval):
        try:
            data = parser(text)
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
        except Exception:
            pass
    match = re.search(r"\[(.*?)\]", text, re.S)
    if match:
        try:
            data = ast.literal_eval("[" + match.group(1) + "]")
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
        except Exception:
            pass
    return []


def _clean_entity_phrase(text: str) -> str:
    if not text:
        return ""
    text = text.strip("，。；、：:！？!?（）()“”‘’ \n\t")
    garbage_prefixes = [
        "最近感觉", "感觉", "最近", "好像", "似乎", "不知道是不是", "不知道", "是不是", "和之前的", "之前的",
        "上的", "有关", "了不少", "不少", "很多", "有点", "我感觉", "我觉得", "我担心", "可能会", "这个选题",
    ]
    for prefix in garbage_prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    garbage_suffixes = ["上的", "有关", "了不少", "不少", "很多", "情况", "问题", "这个选题能怎么做深", "能怎么做深"]
    for suffix in garbage_suffixes:
        if text.endswith(suffix):
            text = text[:-len(suffix)].strip()
    for sep in ["是不是", "有关", "相关", "因为", "以及", "和", "与", "但", "这个选题", "可能会", "我感觉", "我觉得"]:
        if sep in text and len(text) > 6:
            parts = [p.strip() for p in text.split(sep) if p.strip()]
            if parts:
                text = max(parts, key=len)

    # 以第一人称、判断词开头的一律丢掉
    if re.match(r"^(我|我们|感觉|觉得|担心|可能|是不是)", text):
        return ""

    return text.strip("，。；、：:！？!?（）()“”‘’ ")


def _expand_entities(entities: List[str]) -> List[str]:
    expanded: List[str] = []
    for entity in entities:
        entity = _clean_entity_phrase(entity)
        if not entity:
            continue
        expanded.append(entity)
        expanded.extend(SYNONYM_MAP.get(entity, []))
    joined = " ".join(expanded)
    if "园博" in joined or "园博园" in joined:
        expanded.extend(["园博园", "园博", "展后运营", "大型活动"])
    if "交通" in joined or "承载" in joined or "拥堵" in joined:
        expanded.extend(["交通", "拥堵", "承载", "停车", "接驳"])
    if any(k in joined for k in ["生态", "湿地", "候鸟"]):
        expanded.extend(["生态", "湿地", "候鸟"])
    seen, result = set(), []
    for item in expanded:
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result[:12]


def _fallback_extract_entities(user_text: str) -> List[str]:
    seeds: List[str] = []
    patterns = [
        r"[\u4e00-\u9fff]{2,12}(?:岛|街道|社区|景区|湿地|新区|园区|古村|村|镇|区|县|市)",
        r"[\u4e00-\u9fff]{2,20}(?:局|委|办|馆|中心|政府|集团|公司|指挥部)",
        r"[\u4e00-\u9fff]{0,8}(?:农家乐|民宿|开发|旅游|文旅|生态|湿地|候鸟|交通|倒闭|园博园|园博|活动|承载|拥堵)",
    ]
    for pattern in patterns:
        seeds.extend(re.findall(pattern, user_text))
    for kw in ["七都岛", "七都", "农家乐", "民宿", "开发", "旅游", "文旅", "生态", "湿地", "候鸟", "倒闭", "园博园", "园博", "交通", "承载", "拥堵"]:
        if kw in user_text:
            seeds.append(kw)
    cleaned = [_clean_entity_phrase(item) for item in seeds]
    return _expand_entities([x for x in cleaned if x])


def extract_entities(user_text: str) -> List[str]:
    system_prompt = (
        "你是一个实体提取器。请从用户的原始想法中，提取出最核心的地理位置、机构名称或核心事件词汇。"
        "请严格输出一个 JSON 格式的字符串列表，例如 [\"园博园\", \"周边交通\"]，不要输出其他废话。"
        "尽量不要提取语气词、完整句子、推测短语，只保留可用于知识图谱检索的关键词。"
    )
    if LLM_CLIENT:
        try:
            response = LLM_CLIENT.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_text}],
                temperature=0.1,
                timeout=40,
            )
            content = response.choices[0].message.content or ""
            entities = [_clean_entity_phrase(x) for x in _safe_json_list(content)]
            entities = [x for x in entities if x]
            if entities:
                return _expand_entities(entities)
        except Exception:
            pass
    return _fallback_extract_entities(user_text)


def _score_node_match(entity_norm: str, node_id: int, data: Dict[str, Any]) -> int:
    name = str(data.get("name", ""))
    aliases = data.get("aliases", []) or []
    props = json.dumps(data.get("properties", {}) or {}, ensure_ascii=False)
    ntype = data.get("type", "")

    score = 0
    if name == entity_norm:
        score += 100
    elif entity_norm in name:
        score += 60
    elif name in entity_norm:
        score += 35

    if any(entity_norm == alias for alias in aliases):
        score += 50
    elif any(entity_norm in alias or alias in entity_norm for alias in aliases):
        score += 25

    if entity_norm in props:
        score += 15

    type_bonus = {
        "issue": 25,
        "institution": 20,
        "event": 12,
        "project": 10,
        "entity": 8,
        "source": -10,
    }
    score += type_bonus.get(ntype, 0)

    # 惩罚明显脏节点
    if len(name) > 18:
        score -= 15
    if any(token in name for token in ["我们", "记者", "会议听取", "高质高效", "扎扎实实", "按照省委省政府"]):
        score -= 40
    return score


def _match_nodes_by_keyword(entity: str) -> List[int]:
    entity = _clean_entity_phrase(entity)
    scored: List[tuple[int, int]] = []
    seen = set()

    exact = graph.find_entity(entity)
    if exact:
        scored.append((999, exact["id"]))
        seen.add(exact["id"])

    candidates = [entity] + SYNONYM_MAP.get(entity, [])
    for entity_norm in candidates:
        entity_norm = entity_norm.strip()
        if not entity_norm:
            continue
        for node_id, data in graph.G.nodes(data=True):
            score = _score_node_match(entity_norm, node_id, data)
            if score > 0 and node_id not in seen:
                scored.append((score, node_id))
                seen.add(node_id)

    cursor = graph.conn.cursor()
    for entity_norm in candidates:
        if not entity_norm:
            continue
        rows = cursor.execute("SELECT id FROM nodes WHERE name LIKE ? OR properties_json LIKE ? LIMIT 8", (f"%{entity_norm}%", f"%{entity_norm}%")).fetchall()
        for row in rows:
            node_id = row[0]
            if node_id in seen or node_id not in graph.G.nodes:
                continue
            score = _score_node_match(entity_norm, node_id, graph.G.nodes[node_id])
            if score > 0:
                scored.append((score, node_id))
                seen.add(node_id)

    scored.sort(key=lambda x: x[0], reverse=True)
    return [node_id for _, node_id in scored[:4]]


def _format_node(node_id: int) -> str:
    data = graph.G.nodes[node_id]
    name = data.get("name", f"#{node_id}")
    ntype = data.get("type", "unknown")
    props = data.get("properties", {}) or {}
    if props:
        preview = "、".join(f"{k}={v}" for k, v in list(props.items())[:4])
        return f"{name}（type={ntype}; {preview}）"
    return f"{name}（type={ntype}）"


def _is_noisy_node_name(name: str) -> bool:
    return (
        len(name) > 18
        or any(token in name for token in ["我们", "记者", "会议听取", "高质高效", "扎扎实实", "按照省委省政府", "这个选题"])
    )


def retrieve_graph_context(entities: List[str]) -> str:
    if not entities:
        return "图谱上下文发现：未提取到有效实体，暂无可用线索。"

    candidate_centers = []
    seen_center_names = set()

    for entity in entities[:6]:
        matched_ids = _match_nodes_by_keyword(entity)
        for center_id in matched_ids:
            center_name = graph.G.nodes[center_id].get("name", entity)
            if _is_noisy_node_name(center_name):
                continue
            # 锚点去重：同名去重、包含关系去重
            if center_name in seen_center_names:
                continue
            if any(center_name in old or old in center_name for old in seen_center_names):
                continue
            seen_center_names.add(center_name)
            candidate_centers.append(center_id)
            if len(candidate_centers) >= 3:
                break
        if len(candidate_centers) >= 3:
            break

    lines: List[str] = ["图谱上下文发现："]
    if not candidate_centers:
        lines.append("- 图谱中没有直接命中，但可围绕原始关键词做延展采访。")
        return "\n".join(lines)

    for center_id in candidate_centers:
        center_name = graph.G.nodes[center_id].get("name", "unknown")
        hop_map = nx.single_source_shortest_path_length(graph.G, center_id, cutoff=2)
        neighbor_ids = [nid for nid, dist in hop_map.items() if nid != center_id and dist <= 2]

        issue_nodes, institution_nodes, other_nodes = [], [], []
        for nid in neighbor_ids:
            ndata = graph.G.nodes[nid]
            nname = ndata.get("name", "")
            if _is_noisy_node_name(nname):
                continue
            ntype = ndata.get("type")
            if ntype == "issue":
                issue_nodes.append(nid)
            elif ntype == "institution":
                institution_nodes.append(nid)
            else:
                other_nodes.append(nid)

        lines.append(f"- 线索锚点【{center_name}】")

        if issue_nodes:
            lines.append("  - 核心问题：")
            for nid in issue_nodes[:3]:
                lines.append(f"    - {_format_node(nid)}")

        if institution_nodes:
            lines.append("  - 牵涉机构：")
            for nid in institution_nodes[:3]:
                lines.append(f"    - {_format_node(nid)}")

        relation_lines: List[str] = []
        for nid in (issue_nodes[:2] + institution_nodes[:2] + other_nodes[:2]):
            try:
                path = nx.shortest_path(graph.G, center_id, nid)
            except nx.NetworkXNoPath:
                continue
            if len(path) < 2:
                continue
            segments = []
            noisy_path = False
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                aname = graph.G.nodes[a].get('name', '')
                bname = graph.G.nodes[b].get('name', '')
                if _is_noisy_node_name(aname) or _is_noisy_node_name(bname):
                    noisy_path = True
                    break
                edge = graph.G.get_edge_data(a, b) or {}
                rel = edge.get("relation", "关联")
                segments.append(f"{aname} -[{rel}]-> {bname}")
            if segments and not noisy_path:
                relation_lines.append(" / ".join(segments))

        if relation_lines:
            lines.append("  - 关系线索：")
            for item in relation_lines[:3]:
                lines.append(f"    - {item}")

    return "\n".join(lines)


def _infer_issue_families(user_text: str, graph_context: str) -> List[str]:
    text = f"{user_text}\n{graph_context}"
    rules = {
        "transport": ["交通", "拥堵", "承载", "停车", "接驳", "客流", "道路"],
        "ecology": ["生态", "湿地", "候鸟", "环保", "栖息地", "景观"],
        "operations": ["展后运营", "持续运营", "大型活动", "展会", "园博", "文旅", "分会场"],
        "governance": ["指挥部", "政府", "统筹", "推进", "协调", "部门", "常务会议"],
        "market": ["经营", "商户", "民宿", "农家乐", "客单", "招商", "空置"],
    }
    scored = []
    for family, kws in rules.items():
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            scored.append((family, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in scored[:3]] or ["governance"]


def _build_issue_cluster_summary(graph_context: str, families: List[str]) -> List[str]:
    summary = []
    if "transport" in families:
        summary.append("- 问题簇 1｜交通承载：高峰活动、停车接驳、周边道路压力已经不是点状现象，而是园区运营能力的一部分。")
    if "operations" in families:
        summary.append("- 问题簇 2｜展后运营：活动热度是否能转成长期内容供给、稳定复购和常态运营，是园博园真正的价值考题。")
    if "ecology" in families:
        summary.append("- 问题簇 3｜生态边界：景观维护、生态容量和活动密度之间可能存在长期张力。")
    if "governance" in families:
        summary.append("- 问题簇 4｜治理结构：筹办期依赖指挥部，常态期则要看跨部门分工和责任落点是否清晰。")
    if "market" in families:
        summary.append("- 问题簇 5｜运营回报：热闹是否转化为周边消费、商户收益和项目可持续回报，不能只看现场人流。")

    if not summary:
        summary.append("- 当前图谱线索还不足以形成稳定问题簇，需要补采访和补图谱。")
    return summary


def _fallback_generate_pitch(user_text: str, graph_context: str) -> str:
    families = _infer_issue_families(user_text, graph_context)
    clusters = _build_issue_cluster_summary(graph_context, families)
    is_blind_spot = "未在图谱中直接命中" in graph_context and "线索锚点" not in graph_context

    insight_lines = [f"- 原始线索：{user_text}"]
    if is_blind_spot:
        insight_lines.append("- 当前图谱对这条线索的直接覆盖较弱，这是一个明确的图谱盲区，不该硬装知道；新闻价值恰恰在于先补事实，再下判断。")
    else:
        insight_lines.append("- 这条线索已经在图谱里勾连出不止一个问题点，说明它不是单点现象，更像一个可以下钻的系统性议题。")
    insight_lines.extend(clusters)

    angle_blocks = []
    interview_blocks = []

    if "transport" in families:
        insight_lines.append("- 图谱把这条线索指向了交通承载、活动高峰组织和公共服务能力，重点不只是堵不堵，而是城市是否在用短时透支换表面热闹。")
        angle_blocks.append("### 角度一：热闹是不是建立在高峰拥堵和短时透支之上？\n从大型活动日的停车、接驳、客流波峰切入，追问当前交通组织是不是只够应付开幕式，不够支撑常态化运营。")
        interview_blocks.append("- 交通运输部门 / 交警 / 属地街道：高峰客流、停车组织、临时接驳、堵点治理")

    if "ecology" in families:
        insight_lines.append("- 图谱同时触发了生态或景观保护议题，说明这个题不能只写流量，还要看活动密度是否挤压生态和公共空间边界。")
        angle_blocks.append("### 角度二：生态景观与大型活动之间有没有隐性冲突？\n把生态景观维护、游客压力、设施搭建、活动频率放进一张表里，看所谓热闹是否正在侵蚀长期品质。")
        interview_blocks.append("- 园林绿化 / 生态环境 / 湿地保护条线：景观维护、生态边界、游客承载阈值")

    if "operations" in families:
        insight_lines.append("- 图谱命中了展后可持续运营，说明真正的大题不在活动本身，而在活动能否转化为长期运营能力。")
        angle_blocks.append("### 角度三：活动很多，不等于项目会运营\n追问园博园是靠一次次活动堆热度，还是已经形成稳定内容生产、常态运营和复购机制。")
        interview_blocks.append("- 园博园运营方 / 活动策划方 / 会展执行方：活动排期、复购率、展后利用、运营成本")

    if "governance" in families:
        insight_lines.append("- 牵涉到指挥部和多部门时，报道重点就不只是现象描述，而是责任结构：筹办期靠专班，常态期谁接盘。")
        angle_blocks.append("### 角度四：指挥部模式适合筹办期，那展后谁接盘？\n看清楚跨部门协同、日常运营主体、预算责任和考核逻辑，避免盛会结束后治理空转。")
        interview_blocks.append("- 园博园建设指挥部 / 文旅部门 / 住建园林条线：统筹机制、部门分工、展后责任安排")

    if "market" in families:
        insight_lines.append("- 如果周边经营或消费转化也被触发，就要追问这类项目到底带动了什么，而不是默认‘有活动就有经济’。")
        angle_blocks.append("### 角度五：热度有没有转成周边真实收益？\n从商户流水、游客停留时长、二次消费和空置情况看，这种热闹到底是城市秀场，还是带来了真实运营回报。")
        interview_blocks.append("- 周边商户 / 游客 / 居民：二次消费、停留时长、复购意愿、体感变化")

    if not angle_blocks:
        angle_blocks.append("### 角度一：表层现象背后，谁在承担真正的系统成本？\n把用户观察和图谱线索并置，找出最值得继续核验的结构性矛盾。")
        interview_blocks.append("- 属地部门 + 现场对象：先做一轮快速核验采访")

    interview_blocks.extend([
        "- 数据线：客流、活动频次、停车位、投诉量、预算投放、周边消费变化",
        "- 现场线：游客、志愿者、安保、保洁、周边居民，补足运行现场感",
    ])

    return f"""# 主编策划单｜灵感放大器输出

## 💡 图谱关联洞察
{chr(10).join(insight_lines)}

## 📐 破局角度 (Angles)
{chr(10).join(angle_blocks)}

## 🎤 建议采访清单
{chr(10).join(interview_blocks)}

## 备注
以下为图谱检索摘要，可作为采访前置线索：

{graph_context}
"""


def generate_pitch(user_text: str, graph_context: str) -> str:
    system_prompt = (
        "你是一位资深的深度报道主编。用户会给你一个原始的新闻观察，同时系统会提供来自城市知识图谱的背景上下文。"
        "请结合两者，生成一个深度报道策划案。必须使用 Markdown，并包含：\n"
        "## 💡 图谱关联洞察\n## 📐 破局角度 (Angles)\n## 🎤 建议采访清单\n"
        "要求：严格根据图谱上下文变化主题，不要复用上一题模板；采访对象要跟命中的问题簇一致。"
    )
    if LLM_CLIENT:
        try:
            response = LLM_CLIENT.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"原始想法：\n{user_text}\n\n图谱上下文：\n{graph_context}"},
                ],
                temperature=0.7,
                timeout=60,
            )
            content = response.choices[0].message.content or ""
            if content.strip():
                return content
        except Exception:
            pass
    return _fallback_generate_pitch(user_text, graph_context)


def run_once(user_text: str) -> Tuple[List[str], str, str]:
    entities = extract_entities(user_text)
    graph_context = retrieve_graph_context(entities)
    pitch = generate_pitch(user_text, graph_context)
    return entities, graph_context, pitch


def main() -> None:
    print("=" * 72)
    print("💡 灵感放大器已启动！请输入你今天的线索或原始想法（输入 'q' 退出）：")
    print("=" * 72)
    while True:
        try:
            user_text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 已退出灵感放大器。")
            break
        if not user_text:
            continue
        if user_text.lower() in {"q", "quit", "exit"}:
            print("👋 已退出灵感放大器。")
            break
        entities, graph_context, pitch = run_once(user_text)
        print("\n🧠 正在提取关键实体...")
        print(f"   提取结果：{json.dumps(entities, ensure_ascii=False)}")
        print("\n🕸️ 正在检索图谱上下文...")
        print(graph_context)
        print("\n" + "=" * 72)
        print("📘 最终策划案")
        print("=" * 72)
        print(pitch)
        print("=" * 72)


def cli_entry() -> None:
    if len(sys.argv) > 1:
        user_text = " ".join(sys.argv[1:]).strip()
        entities, graph_context, pitch = run_once(user_text)
        print("🧠 提取结果:", json.dumps(entities, ensure_ascii=False))
        print("\n🕸️ 图谱上下文:")
        print(graph_context)
        print("\n📘 最终策划案:")
        print(pitch)
        return
    main()


if __name__ == "__main__":
    cli_entry()

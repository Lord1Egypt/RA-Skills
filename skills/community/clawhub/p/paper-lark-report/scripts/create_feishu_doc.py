#!/usr/bin/env python3
"""
create_feishu_doc.py - Create a Feishu wiki document for the daily paper digest.
Uses Feishu Open API directly (no MCP).
"""
import json
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
FEISHU_BASE = "https://open.feishu.cn/open-apis"


def load_token() -> str:
    """Get a fresh tenant_access_token from appId + appSecret via Feishu API."""
    import json
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    feishu_cfg = cfg.get("channels", {}).get("feishu", {})
    app_id = feishu_cfg.get("appId", "")
    app_secret = feishu_cfg.get("appSecret", "")
    if not app_id or not app_secret:
        raise RuntimeError("Feishu appId/appSecret not found in openclaw.json")

    # Exchange for tenant_access_token
    body = {"app_id": app_id, "app_secret": app_secret}
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if result.get("code") != 0:
        raise RuntimeError(f"Token exchange failed: {result}")
    token = result.get("tenant_access_token", "")
    if not token:
        raise RuntimeError("No tenant_access_token in response")
    return token


def api_call(method: str, path: str, token: str, body=None) -> dict:
    url = f"{FEISHU_BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url, method=method, data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    if result.get("code") != 0:
        raise RuntimeError(f"Feishu API error {result.get('code')}: {result.get('msg')}")
    return result.get("data", {})


def get_token_info(token: str) -> dict:
    """Check who this token belongs to."""
    return api_call("GET", "/authen/v1/user_info", token)



def create_wiki_node(space_id: str, parent_node_token: str, token: str, title: str) -> dict:
    """Create a wiki node (without obj_token - wiki API creates its own doc)."""
    body = {
        "obj_type": "docx",
        "parent_node_token": parent_node_token,
        "node_type": "origin",
        "title": title,
    }
    data = api_call("POST", f"/wiki/v2/spaces/{space_id}/nodes", token, body)
    node = data["node"]
    return {"node_token": node["node_token"], "obj_token": node["obj_token"]}


def write_blocks(document_id: str, blocks: list, token: str):
    """Write blocks to a Feishu document. Batches of 15."""
    for i in range(0, len(blocks), 15):
        batch = blocks[i:i+15]
        body = {"children": batch, "index": -1}
        api_call("POST", f"/docx/v1/documents/{document_id}/blocks/{document_id}/children", token, body)
        print(f"  Wrote blocks {i+1}-{i+len(batch)}")


def make_heading(level: int, content: str) -> dict:
    bt = level + 2
    key = f"heading{level}"
    return {
        "block_type": bt,
        key: {
            "elements": [{"text_run": {"content": content, "text_element_style": {}}}],
            "style": {},
        },
    }


def make_paragraph(content: str, bold: bool = False) -> dict:
    style = {"bold": True} if bold else {}
    return {
        "block_type": 2,
        "text": {
            "elements": [{"text_run": {"content": content, "text_element_style": style}}],
            "style": {},
        },
    }




def build_blocks(papers: list, date: str, total: int, research_direction: str = "") -> list:
    blocks = []

    # Header
    blocks.append(make_heading(1, "📰 Research Daily " + date))
    if research_direction:
        blocks.append(make_paragraph("研究方向：" + research_direction))
    blocks.append(make_paragraph(f"日期：{date} | 候选论文：{total} 篇 | 精选论文：{len(papers)} 篇"))

    for i, p in enumerate(papers, 1):
        blocks.append(make_heading(2, f"{i}. {p['title']}"))
        blocks.append(make_paragraph(f"相关性：{p['relevance_score']}/10"))
        blocks.append(make_paragraph(f"arXiv ID：{p['paper_id']} | 发布日期：{p['posted_date']}"))
        blocks.append(make_paragraph("作者：" + ", ".join(p['authors'][:3]) + (" et al." if len(p['authors']) > 3 else "")))
        blocks.append(make_paragraph(f"arXiv：{p['arxiv_url']}"))
        blocks.append(make_heading(3, "【研究动机】"))
        blocks.append(make_paragraph(p.get('motivation', '')))
        blocks.append(make_heading(3, "【核心创新】"))
        blocks.append(make_paragraph(p.get('core_innovation', '')))

    blocks.append(make_paragraph("数据来源：arXiv | 本报告由 AI 自动生成，分析基于论文摘要，未补充额外信息。"))

    return [b for b in blocks if b is not None]


def main():
    import yaml

    # Load selected papers
    with open(SKILL_DIR / "data" / "selected_papers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    date = data["date"]
    papers = data["papers"]

    print(f"Creating Feishu wiki doc for {date} with {len(papers)} papers...")

    # Get token
    token = load_token()
    print(f"Token loaded: {token[:20]}...")

    # Load wiki config
    with open(SKILL_DIR / "config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    space_id = config.get("feishu_space_id")
    parent_node = config.get("feishu_parent_node")
    if not space_id or not parent_node:
        raise RuntimeError("feishu_space_id and feishu_parent_node must be set in config.yaml")
    print(f"Space: {space_id}, Parent node: {parent_node}")

    # Create wiki node
    title = f"📰 Research Daily {date}"
    result = create_wiki_node(space_id, parent_node, token, title)
    node_token = result["node_token"]
    obj_token = result["obj_token"]
    print(f"Wiki node created: {node_token}")
    print(f"Document ID (obj_token): {obj_token}")

    # Build blocks
    research_direction = config.get("research_direction", "")
    blocks = build_blocks(papers, date, 20, research_direction)

    # Write blocks
    write_blocks(obj_token, blocks, token)

    # Build doc URL
    doc_url = f"https://my.feishu.cn/wiki/{space_id}?nodeToken={node_token}"
    print(f"Document URL: {doc_url}")

    # Save result
    result_file = SKILL_DIR / "data" / "doc_result.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "node_token": node_token,
            "obj_token": obj_token,
            "doc_url": doc_url,
            "date": date,
        }, f, ensure_ascii=False, indent=2)
    print(f"Result saved to {result_file}")

    # Register in doc registry
    doc_registry_path = SKILL_DIR / "data" / "doc_registry.json"
    registry = {}
    if doc_registry_path.exists():
        with open(doc_registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    registry[date] = {
        "node_token": node_token,
        "obj_token": obj_token,
        "url": doc_url,
        "title": title,
        "registered_at": datetime.now().isoformat(),
    }
    with open(doc_registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"Registered in doc_registry.json")
    print("Done!")


if __name__ == "__main__":
    main()

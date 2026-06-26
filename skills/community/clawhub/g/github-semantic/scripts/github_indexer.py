#!/usr/bin/env python3
"""
GitHub Indexer — vectorize GitHub repos into Qdrant.
Usage:
  python github_indexer.py init                        # Create Qdrant collection
  python github_indexer.py add owner/repo --issues     # Index issues
  python github_indexer.py add owner/repo --prs        # Index PRs
  python github_indexer.py add owner/repo --repo        # Index repo metadata
  python github_indexer.py add owner/repo --all         # Index all
  python github_indexer.py status                      # Show indexed repos
  python github_indexer.py rm owner/repo               # Remove repo from index
"""
import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from typing import List

os.environ.setdefault("OLLAMA_MODELS", r"D:\ChatAI\OpenClaw\.ollama\models")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

COLLECTION = "github_repos"
EMBED_MODEL = "nomic-embed-text:latest"
GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"


def gh(args: str) -> dict:
    result = subprocess.run(
        f'"{GH_EXE}" {args}',
        capture_output=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh {args} failed: {result.stderr}")
    stdout = result.stdout or ""
    if not stdout.strip():
        return {}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"raw": stdout}


def gh_list(args: str) -> list:
    result = subprocess.run(
        f'"{GH_EXE}" {args}',
        capture_output=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout or "[]")
        return data if isinstance(data, list) else []
    except:
        return []


def _hash_int(raw: str) -> int:
    """FNV-1a hash -> deterministic positive integer for Qdrant point ID."""
    h = 2166136261
    for c in raw.encode("utf-8"):
        h ^= c
        h = (h * 16777619) & 0xFFFFFFFF
    return h


@dataclass
class GitHubItem:
    repo: str
    type: str
    number: int
    title: str
    body: str
    state: str
    author: str
    labels: List[str]
    url: str
    created_at: str
    updated_at: str

    @property
    def int_id(self) -> int:
        return _hash_int(f"{self.repo}:{self.type}:{self.number}")

    def text_content(self) -> str:
        labels_str = ", ".join(self.labels) if self.labels else "none"
        return f"[{self.type.upper()} #{self.number}] {self.title}\nLabels: {labels_str}\n{self.body[:1000]}"

    def to_payload(self) -> dict:
        return {
            "repo": self.repo,
            "type": self.type,
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "author": self.author,
            "labels": self.labels,
            "url": self.url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def get_embedding(text: str) -> List[float]:
    import urllib.request
    payload = {"model": EMBED_MODEL, "prompt": text}
    req = urllib.request.Request(
        "http://localhost:11434/api/embeddings",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["embedding"]


def ensure_collection(qdrant_client, force: bool = False):
    from qdrant_client import models
    existing = [c.name for c in qdrant_client.get_collections().collections]
    if COLLECTION in existing:
        if force:
            qdrant_client.delete_collection(COLLECTION)
        else:
            print(f"Collection '{COLLECTION}' already exists.")
            return
    qdrant_client.create_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    qdrant_client.create_payload_index(COLLECTION, field_name="repo", field_schema="keyword")
    qdrant_client.create_payload_index(COLLECTION, field_name="type", field_schema="keyword")
    print(f"Collection '{COLLECTION}' created.")


def index_items(items: List[GitHubItem], qdrant_client, batch_size: int = 10):
    total = len(items)
    for i in range(0, total, batch_size):
        batch = items[i:i+batch_size]
        points = []
        for item in batch:
            text = item.text_content()
            vec = get_embedding(text)
            points.append({
                "id": item.int_id,
                "vector": vec,
                "payload": item.to_payload()
            })
            sys.stdout.write(f"\rEmbedding {min(i+batch.index(item)+1, total)}/{total}")
            sys.stdout.flush()
        qdrant_client.upsert(collection_name=COLLECTION, points=points)
        time.sleep(0.3)
    print(f"\nIndexed {total} items.")


def fetch_issues(repo: str, state: str = "all", limit: int = 100) -> List[GitHubItem]:
    data = gh_list(f"issue list --repo {repo} --state {state} --limit {limit} --json number,title,body,state,author,labels,url,createdAt,updatedAt")
    items = []
    for item in data:
        author = item.get("author", {})
        if isinstance(author, dict):
            author_login = author.get("login", "unknown")
        else:
            author_login = str(author) if author else "unknown"
        items.append(GitHubItem(
            repo=repo, type="issue", number=item["number"],
            title=item.get("title", ""),
            body=item.get("body", "") or "",
            state=item["state"],
            author=author_login,
            labels=[l.get("name") for l in item.get("labels", []) if l],
            url=item.get("url", ""),
            created_at=item.get("createdAt", ""),
            updated_at=item.get("updatedAt", ""),
        ))
    return items


def fetch_prs(repo: str, state: str = "all", limit: int = 100) -> List[GitHubItem]:
    data = gh_list(f"pr list --repo {repo} --state {state} --limit {limit} --json number,title,body,state,author,labels,url,createdAt,updatedAt,isDraft")
    items = []
    for item in data:
        author = item.get("author", {})
        if isinstance(author, dict):
            author_login = author.get("login", "unknown")
        else:
            author_login = str(author) if author else "unknown"
        items.append(GitHubItem(
            repo=repo, type="PR", number=item["number"],
            title=item.get("title", ""),
            body=item.get("body", "") or "",
            state=item["state"],
            author=author_login,
            labels=[l.get("name") for l in item.get("labels", []) if l],
            url=item.get("url", ""),
            created_at=item.get("createdAt", ""),
            updated_at=item.get("updatedAt", ""),
        ))
    return items


def fetch_repo_meta(repo: str) -> List[GitHubItem]:
    data = gh(f"repo view {repo} --json name,description,stargazerCount,url,languages,repositoryTopics")
    if not data:
        return []
    langs = data.get("languages", {})
    lang_str = ", ".join(langs.keys()) if isinstance(langs, dict) else ""
    topics_list = data.get("repositoryTopics", [])
    topics = []
    for t in topics_list:
        if isinstance(t, dict):
            topic_name = t.get("topic", {})
            if isinstance(topic_name, dict):
                topics.append(topic_name.get("name", ""))
    items = [GitHubItem(
        repo=repo, type="repo", number=0,
        title=f"Repo: {data.get('name', repo)}",
        body=f"{data.get('description', '')}\nLanguages: {lang_str}\nStars: {data.get('stargazerCount', 0)}",
        state="active",
        author=data.get("name", ""),
        labels=topics,
        url=data.get("url", ""),
        created_at="",
        updated_at="",
    )]
    return items


def cmd_status(qdrant_client):
    try:
        count = qdrant_client.get_collection(COLLECTION).points_count
    except:
        print("Collection not found. Run 'python github_indexer.py init' first.")
        return
    print(f"Collection '{COLLECTION}': {count} items indexed.")
    from qdrant_client.models import Filter, FieldCondition, MatchValue, ScrollFilter
    offset = None
    repos_seen = {}
    while True:
        results, offset = qdrant_client.scroll(
            collection_name=COLLECTION, scroll_filter=ScrollFilter(),
            limit=200, offset=offset, with_payload=True
        )
        for pt in results:
            repo = pt.payload.get("repo", "unknown")
            typ = pt.payload.get("type", "unknown")
            if repo not in repos_seen:
                repos_seen[repo] = {"issue": 0, "PR": 0, "repo": 0}
            if typ in repos_seen[repo]:
                repos_seen[repo][typ] += 1
        if offset is None:
            break
    print("\nBy repo:")
    for repo, counts in sorted(repos_seen.items()):
        print(f"  {repo}: issue={counts['issue']}, PR={counts['PR']}, repo={counts['repo']}")


def cmd_remove(qdrant_client, repo: str):
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    qdrant_client.delete(
        collection_name=COLLECTION,
        points_selector=Filter(must=[FieldCondition(key="repo", match=MatchValue(value=repo))])
    )
    print(f"Removed all items for {repo}.")


def main():
    parser = argparse.ArgumentParser(description="GitHub Vector Indexer")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("init", help="Initialize Qdrant collection")
    sub.add_parser("status", help="Show index status")
    add = sub.add_parser("add", help="Add repo data to index")
    add.add_argument("repo", help="owner/repo")
    add.add_argument("--issues", action="store_true")
    add.add_argument("--prs", action="store_true")
    add.add_argument("--repo", action="store_true")
    add.add_argument("--all", action="store_true")
    add.add_argument("--limit", type=int, default=100)
    rm = sub.add_parser("rm")
    rm.add_argument("repo")
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        return

    from qdrant_client import QdrantClient
    qc = QdrantClient("localhost", port=6333)

    if args.cmd == "init":
        ensure_collection(qc, force=True)
        return
    if args.cmd == "status":
        cmd_status(qc)
        return
    if args.cmd == "rm":
        cmd_remove(qc, args.repo)
        return
    if args.cmd == "add":
        items = []
        if args.all or args.repo:
            items += fetch_repo_meta(args.repo)
        if args.all or args.issues:
            items += fetch_issues(args.repo, limit=args.limit)
        if args.all or args.prs:
            items += fetch_prs(args.repo, limit=args.limit)
        if not items:
            print("No items. Use --issues, --prs, --repo, or --all")
            return
        print(f"Fetching {len(items)} items from {args.repo}...")
        index_items(items, qc)
        print("Done.")


if __name__ == "__main__":
    main()

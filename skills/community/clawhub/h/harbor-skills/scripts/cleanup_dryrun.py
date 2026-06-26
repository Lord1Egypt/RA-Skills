#!/usr/bin/env python3
"""
Harbor 镜像清理演练脚本

用法:
  python3 cleanup_dryrun.py --project my-app --repo my-app--api --url https://harbor.mycompany.com
  python3 cleanup_dryrun.py --project my-app --repo my-app--api --dry-run true --auth username:password

策略:
  --policy latest_n      保留最近 N 个标签
  --policy older_than    删除 N 天前的标签
  --policy regex         删除匹配正则的标签
"""

import argparse
import base64
import json
import sys
import re
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


def parse_args():
    parser = argparse.ArgumentParser(description="Harbor 镜像清理演练")
    parser.add_argument("--url", required=True, help="Harbor 地址")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--repo", required=True, help="仓库名（不含项目前缀）")
    parser.add_argument("--auth", default=os.environ.get("HARBOR_AUTH", ""),
                        help="Basic Auth (user:pass) 或 Bearer Token")
    parser.add_argument("--policy", default="latest_n",
                        choices=["latest_n", "older_than", "regex"],
                        help="清理策略")
    parser.add_argument("--param", default="5", help="策略参数（N/天数/正则）")
    parser.add_argument("--dry-run", default="true", choices=["true", "false"],
                        help="演练模式（true）或执行删除（false）")
    parser.add_argument("--output", default="table", choices=["table", "json", "csv"],
                        help="输出格式")
    return parser.parse_args()


def get_auth_header(auth: str) -> Dict[str, str]:
    if not auth:
        raise ValueError("请通过 --auth 或 HARBOR_AUTH 环境变量提供认证信息")
    if auth.startswith("Bearer "):
        return {"Authorization": auth}
    elif ":" in auth:
        encoded = base64.b64encode(auth.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    else:
        encoded = base64.b64encode(f"admin:{auth}".encode()).decode()
        return {"Authorization": f"Basic {encoded}"}


def get_project_id(url: str, project: str, headers: Dict) -> int:
    r = requests.get(f"{url}/api/v2.0/projects", params={"name": project}, headers=headers, timeout=30)
    r.raise_for_status()
    projects = r.json()
    if not projects:
        raise ValueError(f"项目不存在: {project}")
    return projects[0]["project_id"]


def list_artifacts(url: str, project_id: int, repo: str, headers: Dict) -> List[Dict]:
    """获取仓库所有制品（含标签）"""
    all_artifacts = []
    page, page_size = 1, 100

    while True:
        r = requests.get(
            f"{url}/api/v2.0/projects/{project_id}/repositories/{repo}/artifacts",
            params={"with_tag": "true", "with_scan_overview": "true", "page": page, "page_size": page_size},
            headers=headers,
            timeout=30
        )
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        all_artifacts.extend(items)
        if len(items) < page_size:
            break
        page += 1

    return all_artifacts


def eval_latest_n(artifacts: List[Dict], n: int, exclude_tags: List[str]) -> List[Dict]:
    """保留最近 N 个标签，其余标记待删除"""
    to_delete = []
    for artifact in artifacts:
        tags = artifact.get("tags", [])
        if not tags:
            # 无标签的制品 → 删除
            to_delete.append({"artifact": artifact, "reason": "无标签"})
            continue

        # 按 push 时间排序
        sorted_tags = sorted(tags, key=lambda t: t.get("push_time", ""), reverse=True)
        kept_tags = [t for t in sorted_tags if t["name"] in exclude_tags]
        remaining = [t for t in sorted_tags if t["name"] not in exclude_tags]

        if len(remaining) > n:
            for tag in remaining[n:]:
                to_delete.append({
                    "artifact": artifact,
                    "tag": tag,
                    "digest": artifact.get("digest"),
                    "push_time": tag.get("push_time"),
                    "reason": f"保留最近 {n} 个，排名第 {sorted_tags.index(tag) + 1} 位，超出范围"
                })

    return to_delete


def eval_older_than(artifacts: List[Dict], days: int, exclude_tags: List[str]) -> List[Dict]:
    """删除 N 天前的标签"""
    cutoff = datetime.now() - timedelta(days=days)
    to_delete = []

    for artifact in artifacts:
        tags = artifact.get("tags", [])
        for tag in tags:
            if tag["name"] in exclude_tags:
                continue
            push_time_str = tag.get("push_time", "")
            if not push_time_str:
                continue
            push_time = datetime.fromisoformat(push_time_str.replace("Z", "+00:00"))
            if push_time < cutoff:
                to_delete.append({
                    "artifact": artifact,
                    "tag": tag,
                    "digest": artifact.get("digest"),
                    "push_time": push_time_str,
                    "reason": f"推送于 {days} 天前（{push_time.date()}）"
                })

    return to_delete


def delete_artifact_tag(url: str, project_id: int, repo: str,
                         digest: str, tag: str, headers: Dict) -> bool:
    """删除指定制品的指定标签"""
    ref = digest if digest.startswith("sha256:") else f"sha256:{digest}"
    r = requests.delete(
        f"{url}/api/v2.0/projects/{project_id}/repositories/{repo}/artifacts/{ref}/tags/{tag}",
        headers=headers, timeout=30
    )
    return r.status_code in (200, 202)


def print_report(items: List[Dict], output: str, dry_run: bool):
    if output == "json":
        print(json.dumps(items, indent=2, ensure_ascii=False, default=str))
    elif output == "csv":
        print("digest,tag,push_time,reason")
        for item in items:
            print(f"{item.get('digest','')},{item.get('tag',{}).get('name','')},"
                  f"{item.get('push_time','')},{item.get('reason','')}")
    else:
        mode = "【演练】" if dry_run else "【执行】"
        print(f"\n{'='*60}")
        print(f"{mode} 将删除以下 {len(items)} 个镜像标签：")
        print(f"{'='*60}")
        print(f"{'Digest（前16位）':<20} {'Tag':<20} {'推送时间':<25} {'原因'}")
        print("-" * 60)
        for item in items:
            d = item.get("digest", "")[:16]
            t = item.get("tag", {}).get("name", "（无标签）")
            pt = item.get("push_time", "")[:19]
            reason = item.get("reason", "")
            print(f"{d:<20} {t:<20} {pt:<25} {reason}")
        print("-" * 60)
        print(f"共 {len(items)} 条")


if __name__ == "__main__":
    import os
    args = parse_args()
    headers = get_auth_header(args.auth)

    # 获取项目ID
    project_id = get_project_id(args.url, args.project, headers)
    print(f"项目 {args.project} (ID: {project_id})")

    # 获取制品列表
    print(f"正在拉取仓库 {args.repo} 的制品列表...")
    artifacts = list_artifacts(args.url, project_id, args.repo, headers)
    print(f"共 {len(artifacts)} 个制品")

    # 默认排除标签
    exclude_tags = ["latest", "stable", "release-latest"]

    # 评估
    if args.policy == "latest_n":
        n = int(args.param)
        results = eval_latest_n(artifacts, n, exclude_tags)
    elif args.policy == "older_than":
        days = int(args.param)
        results = eval_older_than(artifacts, days, exclude_tags)
    else:
        print(f"不支持的策略: {args.policy}")
        sys.exit(1)

    print_report(results, args.output, args.dry_run == "true")

    if args.dry_run == "false" and results:
        confirm = input(f"\n确认删除以上 {len(results)} 个标签？(y/N): ")
        if confirm.lower() == "y":
            deleted = 0
            for item in results:
                if delete_artifact_tag(args.url, project_id, args.repo,
                                       item["digest"], item["tag"]["name"], headers):
                    deleted += 1
            print(f"已删除 {deleted} 个标签")
        else:
            print("已取消")

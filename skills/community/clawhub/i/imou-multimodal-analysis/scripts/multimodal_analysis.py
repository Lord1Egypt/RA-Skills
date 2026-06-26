#!/usr/bin/env python3
"""
Imou Multimodal Analysis Skill – CLI entry.

Commands: analyze (HUMAN|SMOKING|PHONE|WEAR|ABSENCE|SHELF|TRASH|HEATMAP|FACE),
repo (create|list|delete), target (add|list|delete).
All descriptions and output in English. Requires IMOU_APP_ID, IMOU_APP_SECRET; optional IMOU_BASE_URL.
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from imou_client import (
    get_access_token,
    human_detect,
    smoking_detect,
    phone_using_detect,
    workwear_detect,
    absence_detect,
    shelf_status_detect,
    trash_overflow_detect,
    heatmap_detect,
    face_analysis,
    create_ai_detect_repository,
    list_ai_detect_repository_by_page,
    delete_ai_detect_repository,
    add_ai_detect_target,
    list_ai_detect_target,
    delete_ai_detect_target,
)

APP_ID = os.environ.get("IMOU_APP_ID", "")
APP_SECRET = os.environ.get("IMOU_APP_SECRET", "")
BASE_URL = os.environ.get("IMOU_BASE_URL", "").strip() or "https://openapi.lechange.cn"

# Image input: URL vs Base64
TYPE_URL = "0"
TYPE_BASE64 = "1"


def _ensure_token():
    if not APP_ID or not APP_SECRET:
        print("[ERROR] Set IMOU_APP_ID and IMOU_APP_SECRET.", file=sys.stderr)
        sys.exit(1)
    r = get_access_token(APP_ID, APP_SECRET, BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Get token failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    return r["access_token"]


def _image_type_and_content(url_or_base64: str, is_base64: bool):
    """Return (type, content) for API. If is_base64 True, content is base64 string; else URL."""
    if is_base64:
        return TYPE_BASE64, url_or_base64
    return TYPE_URL, url_or_base64.strip()


def _parse_detect_region(region_str: str):
    """Parse detectRegion from string like '0.2,0.4;0.3,0.5' (points x,y separated by ;). Return list of {x,y} or None."""
    if not region_str or not region_str.strip():
        return None
    points = []
    for part in region_str.split(";"):
        part = part.strip()
        if not part:
            continue
        xs = part.split(",")
        if len(xs) >= 2:
            try:
                points.append({"x": float(xs[0].strip()), "y": float(xs[1].strip())})
            except ValueError:
                pass
    return points if points else None


def cmd_analyze(args):
    token = _ensure_token()
    itype, content = _image_type_and_content(args.image, getattr(args, "base64", False))
    detect_region = _parse_detect_region(getattr(args, "detect_region", None) or "")

    analysis_type = (args.analysis_type or "").upper()
    base_url = BASE_URL or None

    if analysis_type == "HUMAN":
        r = human_detect(token, itype, content, detect_region, base_url=base_url)
    elif analysis_type == "SMOKING":
        r = smoking_detect(token, itype, content, detect_region, base_url=base_url)
    elif analysis_type == "PHONE":
        r = phone_using_detect(token, itype, content, detect_region, base_url=base_url)
    elif analysis_type == "WEAR":
        threshold = float(getattr(args, "threshold", 0.8))
        repo_id = getattr(args, "repository_id", None) or None
        r = workwear_detect(token, itype, content, threshold, repository_id=repo_id,
                           detect_region=detect_region, base_url=base_url)
    elif analysis_type == "ABSENCE":
        repo_id = getattr(args, "repository_id", None)
        if not repo_id:
            print("[ERROR] ABSENCE requires --repository-id.", file=sys.stderr)
            sys.exit(1)
        threshold = float(getattr(args, "threshold", 0.8))
        r = absence_detect(token, itype, content, repo_id, threshold,
                           detect_region=detect_region, base_url=base_url)
    elif analysis_type == "SHELF":
        r = shelf_status_detect(token, itype, content, detect_region, base_url=base_url)
    elif analysis_type == "TRASH":
        r = trash_overflow_detect(token, itype, content, detect_region, base_url=base_url)
    elif analysis_type == "HEATMAP":
        threshold = getattr(args, "threshold", None)
        if threshold is None:
            print("[ERROR] HEATMAP requires --threshold.", file=sys.stderr)
            sys.exit(1)
        threshold = float(threshold)
        exclude = getattr(args, "exclude_repos", None)
        exclude_ids = [s.strip() for s in exclude.split(",")] if exclude else None
        r = heatmap_detect(token, itype, content, threshold, exclude_repository_ids=exclude_ids,
                          detect_region=detect_region, base_url=base_url)
    elif analysis_type == "FACE":
        r = face_analysis(token, itype, content, detect_region, base_url=base_url)
    else:
        print(f"[ERROR] Unknown analysis type: {args.analysis_type}. Use HUMAN|SMOKING|PHONE|WEAR|ABSENCE|SHELF|TRASH|HEATMAP|FACE.", file=sys.stderr)
        sys.exit(1)

    if not r.get("success"):
        print(f"[ERROR] Analysis failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    data = r.get("data", {})
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if getattr(args, "json_only", False):
        return
    detect_result = data.get("detectResult")
    if detect_result is not None:
        print(f"[INFO] detectResult: {detect_result}")
    targets = data.get("targets", [])
    if targets:
        print(f"[INFO] targets count: {len(targets)}")


def cmd_repo_create(args):
    token = _ensure_token()
    r = create_ai_detect_repository(
        token, args.name, args.repo_type,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Create repository failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] repositoryId: {r.get('repository_id', '')}")
    if args.json:
        print(json.dumps({"repositoryId": r.get("repository_id")}, indent=2))


def cmd_repo_list(args):
    token = _ensure_token()
    r = list_ai_detect_repository_by_page(
        token, page=args.page, page_size=args.page_size,
        repository_name=args.name or None,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] List repositories failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    total = r.get("total", 0)
    repo_list = r.get("repository_list", [])
    print(f"[INFO] total: {total}")
    for repo in repo_list:
        print(f"  {repo.get('repositoryId')}  {repo.get('repositoryName')}  {repo.get('repositoryType')}")
    if args.json:
        print(json.dumps({"total": total, "repositoryList": repo_list}, ensure_ascii=False, indent=2))


def cmd_repo_delete(args):
    token = _ensure_token()
    r = delete_ai_detect_repository(token, args.repository_id, base_url=BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Delete repository failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print("[SUCCESS] Repository deleted.")


def cmd_target_add(args):
    token = _ensure_token()
    content_type = TYPE_BASE64 if getattr(args, "type", "").lower() == "base64" else TYPE_URL
    r = add_ai_detect_target(
        token, args.repository_id, content_type, args.content,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] Add target failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print(f"[SUCCESS] targetKey: {r.get('target_key', '')}")
    if args.json:
        print(json.dumps({"targetKey": r.get("target_key")}, indent=2))


def cmd_target_list(args):
    token = _ensure_token()
    r = list_ai_detect_target(
        token, args.repository_id, page=args.page, page_size=args.page_size,
        base_url=BASE_URL or None,
    )
    if not r.get("success"):
        print(f"[ERROR] List targets failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    total = r.get("total", 0)
    target_list = r.get("target_list", [])
    print(f"[INFO] total: {total}")
    for t in target_list:
        print(f"  {t.get('targetKey')}  {t.get('url', '')}")
    if args.json:
        print(json.dumps({"total": total, "targetList": target_list}, ensure_ascii=False, indent=2))


def cmd_target_delete(args):
    token = _ensure_token()
    r = delete_ai_detect_target(token, args.repository_id, args.target_id, base_url=BASE_URL or None)
    if not r.get("success"):
        print(f"[ERROR] Delete target failed: {r.get('error', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    print("[SUCCESS] Target deleted.")


def main():
    parser = argparse.ArgumentParser(description="Imou Multimodal Analysis – analyze image, manage repositories and targets.")
    sub = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = sub.add_parser("analyze", help="Run AI analysis on image URL or Base64.")
    p_analyze.add_argument("analysis_type", help="HUMAN|SMOKING|PHONE|WEAR|ABSENCE|SHELF|TRASH|HEATMAP|FACE")
    p_analyze.add_argument("image", help="Image URL or Base64 string (use --base64 for Base64).")
    p_analyze.add_argument("--base64", action="store_true", help="Treat image as Base64.")
    p_analyze.add_argument("--repository-id", dest="repository_id", help="For WEAR/ABSENCE: repository ID.")
    p_analyze.add_argument("--threshold", type=float, help="For WEAR/ABSENCE/HEATMAP: threshold in (0,1].")
    p_analyze.add_argument("--exclude-repos", dest="exclude_repos", help="For HEATMAP: comma-separated repository IDs to exclude.")
    p_analyze.add_argument("--detect-region", dest="detect_region", help="Optional detectRegion points: 'x1,y1;x2,y2' (normalized 0-1).")
    p_analyze.add_argument("--json", action="store_true", dest="json_only", help="Print only JSON result.")
    p_analyze.set_defaults(func=cmd_analyze)

    # repo create
    p_repo = sub.add_parser("repo", help="Repository: create, list, delete.")
    prepo = p_repo.add_subparsers(dest="repo_cmd", required=True)
    p_create = prepo.add_parser("create", help="Create detect repository.")
    p_create.add_argument("name", help="Repository name.")
    p_create.add_argument("repo_type", choices=["face", "human"], help="face | human (workwear).")
    p_create.add_argument("--json", action="store_true", help="Print JSON.")
    p_create.set_defaults(func=cmd_repo_create)
    p_list = prepo.add_parser("list", help="List repositories (paginated).")
    p_list.add_argument("--page", type=int, default=1, help="Page number.")
    p_list.add_argument("--page-size", type=int, default=20, help="Page size (max 20).")
    p_list.add_argument("--name", help="Filter by repository name (fuzzy).")
    p_list.add_argument("--json", action="store_true", help="Print JSON.")
    p_list.set_defaults(func=cmd_repo_list)
    p_del = prepo.add_parser("delete", help="Delete repository.")
    p_del.add_argument("repository_id", help="Repository ID.")
    p_del.set_defaults(func=cmd_repo_delete)

    # target add/list/delete
    p_target = sub.add_parser("target", help="Target: add, list, delete.")
    ptarget = p_target.add_subparsers(dest="target_cmd", required=True)
    t_add = ptarget.add_parser("add", help="Add target to repository (image URL or Base64).")
    t_add.add_argument("repository_id", help="Repository ID.")
    t_add.add_argument("name", help="Target name (local label; API may not store).")
    t_add.add_argument("content", help="Image URL or Base64 content.")
    t_add.add_argument("--type", choices=["url", "base64"], default="url", help="url or base64 (default url).")
    t_add.add_argument("--json", action="store_true", help="Print JSON.")
    t_add.set_defaults(func=cmd_target_add)
    t_list = ptarget.add_parser("list", help="List targets in repository.")
    t_list.add_argument("repository_id", help="Repository ID.")
    t_list.add_argument("--page", type=int, default=1, help="Page number.")
    t_list.add_argument("--page-size", type=int, default=20, help="Page size.")
    t_list.add_argument("--json", action="store_true", help="Print JSON.")
    t_list.set_defaults(func=cmd_target_list)
    t_del = ptarget.add_parser("delete", help="Delete target from repository.")
    t_del.add_argument("repository_id", help="Repository ID.")
    t_del.add_argument("target_id", help="Target ID (targetKey from add/list).")
    t_del.set_defaults(func=cmd_target_delete)

    args = parser.parse_args()
    if getattr(args, "func", None):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

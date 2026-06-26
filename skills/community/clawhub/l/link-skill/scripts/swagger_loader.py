#!/usr/bin/env python3
"""
swagger_loader.py - Online Swagger/OpenAPI parser.
Supports Swagger 2.0 and OpenAPI 3.x, and fetches API definitions from platform endpoints in real time.
Modes: list / search / detail / tags / cache
"""
import argparse
import json
import os
import sys
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR, ".swagger_cache")
TIMEOUT = 15


def load_config(config_path, platform_id=None):
    with open(config_path, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    pid = platform_id or cfg.get("active_platform")
    if not pid or pid not in cfg.get("platforms", {}):
        sys.exit(f"[ERROR] Platform '{pid}' does not exist. Available: {list(cfg['platforms'].keys())}")
    p = cfg["platforms"][pid]
    p["_id"] = pid
    return p


def get_token(platform_id):
    cache_file = os.path.join(SCRIPT_DIR, ".token_cache.json")
    if not os.path.exists(cache_file):
        return None
    with open(cache_file, "r", encoding="utf-8-sig") as f:
        cache = json.load(f)
    return cache.get(platform_id, {}).get("token")


def fetch_swagger(plat, refresh=False):
    pid = plat["_id"]
    cache_file = os.path.join(CACHE_DIR, f"{pid}.json")

    if not refresh and os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    swagger_cfg = plat.get("swagger", {})
    url = swagger_cfg.get("url")
    if not url:
        sys.exit("[ERROR] Missing configuration: swagger.url")

    headers = {"Accept": "application/json"}
    if swagger_cfg.get("auth_required"):
        token = get_token(pid)
        if token:
            auth_cfg = plat.get("auth", {})
            hdr = auth_cfg.get("token_header", "Authorization")
            prefix = auth_cfg.get("token_prefix", "Bearer ")
            headers[hdr] = f"{prefix}{token}"

    print(f"[FETCH] {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as e:
        sys.exit(f"[ERROR] Failed to fetch Swagger: {e}")

    spec = resp.json()
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    return spec


def detect_version(spec):
    if spec.get("openapi", "").startswith("3"):
        return 3
    if spec.get("swagger", "").startswith("2"):
        return 2
    return 3


def extract_paths(spec):
    return spec.get("paths", {})


def resolve_ref(spec, ref):
    if not ref or not ref.startswith("#/"):
        return ref
    parts = ref.lstrip("#/").split("/")
    node = spec
    for p in parts:
        node = node.get(p, {})
    return node


def resolve_schema_deep(spec, schema, depth=0):
    if depth > 8 or not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        resolved = resolve_ref(spec, schema["$ref"])
        return resolve_schema_deep(spec, resolved, depth + 1)
    result = dict(schema)
    if "properties" in result:
        result["properties"] = {
            k: resolve_schema_deep(spec, v, depth + 1)
            for k, v in result["properties"].items()
        }
    if "items" in result:
        result["items"] = resolve_schema_deep(spec, result["items"], depth + 1)
    for combo in ("allOf", "oneOf", "anyOf"):
        if combo in result:
            result[combo] = [resolve_schema_deep(spec, s, depth + 1) for s in result[combo]]
    return result


def get_request_body_schema(spec, operation, version):
    if version == 3:
        rb = operation.get("requestBody", {})
        content = rb.get("content", {})
        json_ct = content.get("application/json", content.get("*/*", {}))
        schema = json_ct.get("schema", {})
        return resolve_schema_deep(spec, schema)
    else:
        for param in operation.get("parameters", []):
            if param.get("in") == "body":
                return resolve_schema_deep(spec, param.get("schema", {}))
    return None


def get_response_schema(spec, operation, version):
    responses = operation.get("responses", {})
    ok_resp = responses.get("200", responses.get("201", {}))
    if version == 3:
        content = ok_resp.get("content", {})
        json_ct = content.get("application/json", content.get("*/*", {}))
        schema = json_ct.get("schema", {})
    else:
        schema = ok_resp.get("schema", {})
    return resolve_schema_deep(spec, schema)


def get_parameters(operation, version):
    params = operation.get("parameters", [])
    if version == 3:
        return [p for p in params if p.get("in") in ("query", "path", "header")]
    else:
        return [p for p in params if p.get("in") != "body"]


def mode_tags(spec):
    tags = spec.get("tags", [])
    if tags:
        print("=" * 50)
        print("  API Tag Groups")
        print("=" * 50)
        for t in tags:
            desc = t.get("description", "")
            print(f"  [{t['name']}] {desc}")
        print(f"\nTotal {len(tags)} groups.")
    else:
        tag_set = set()
        for path, methods in extract_paths(spec).items():
            for method, op in methods.items():
                if method in ("get", "post", "put", "delete", "patch"):
                    for t in op.get("tags", ["ungrouped"]):
                        tag_set.add(t)
        print("Auto-extracted tags:", ", ".join(sorted(tag_set)))


def mode_list(spec):
    version = detect_version(spec)
    paths = extract_paths(spec)
    print("=" * 80)
    print(f"  API List (OpenAPI {version}.x)  Total {sum(1 for p in paths.values() for m in p if m in ('get','post','put','delete','patch'))} endpoints")
    print("=" * 80)
    for path, methods in sorted(paths.items()):
        for method, op in sorted(methods.items()):
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            tags = ", ".join(op.get("tags", ["-"]))
            summary = op.get("summary", "")
            print(f"  {method.upper():7s} {path:45s} [{tags}] {summary}")
    print()


def mode_search(spec, keyword):
    keyword_lower = keyword.lower()
    paths = extract_paths(spec)
    results = []
    for path, methods in paths.items():
        for method, op in methods.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            text = f"{path} {op.get('summary', '')} {op.get('description', '')} {' '.join(op.get('tags', []))}".lower()
            if keyword_lower in text:
                results.append((method.upper(), path, op))
    if not results:
        print(f"[INFO] No API matched '{keyword}'.")
        return
    print(f"Found {len(results)} APIs matching '{keyword}':\n")
    for method, path, op in results:
        tags = ", ".join(op.get("tags", []))
        print(f"  {method:7s} {path:45s} [{tags}] {op.get('summary', '')}")
    print()


def schema_to_example(schema, depth=0):
    if depth > 6 or not isinstance(schema, dict):
        return None
    if "example" in schema:
        return schema["example"]
    t = schema.get("type", "object")
    if t == "string":
        return schema.get("enum", ["string"])[0]
    if t == "integer" or t == "int32" or t == "int64":
        return 0
    if t == "number":
        return 0.0
    if t == "boolean":
        return True
    if t == "array":
        items = schema.get("items", {})
        ex = schema_to_example(items, depth + 1)
        return [ex] if ex is not None else []
    if t == "object" or "properties" in schema:
        obj = {}
        for k, v in schema.get("properties", {}).items():
            obj[k] = schema_to_example(v, depth + 1)
        return obj
    return None


def mode_detail(spec, path, method):
    version = detect_version(spec)
    paths = extract_paths(spec)
    if path not in paths:
        candidates = [p for p in paths if path.lower() in p.lower()]
        if candidates:
            print(f"[WARN] Exact path not found. Similar paths: {candidates}")
        else:
            print(f"[ERROR] Path '{path}' does not exist.")
        return

    methods = paths[path]
    method_lower = method.lower()
    if method_lower not in methods:
        print(f"[ERROR] {path} does not have method {method}. Available: {[m for m in methods if m in ('get','post','put','delete','patch')]}")
        return

    op = methods[method_lower]
    print("=" * 60)
    print(f"  {method.upper()} {path}")
    print(f"  {op.get('summary', '')} — {op.get('description', '')}")
    print(f"  Tags: {', '.join(op.get('tags', []))}")
    print("=" * 60)

    params = get_parameters(op, version)
    if params:
        print("\n[Parameters]")
        for p in params:
            req = "required" if p.get("required") else "optional"
            print(f"  [{p.get('in', '?'):6s}] {p.get('name', '?'):20s}  {p.get('schema', {}).get('type', p.get('type', '?')):10s}  ({req}) {p.get('description', '')}")

    body_schema = get_request_body_schema(spec, op, version)
    if body_schema:
        print("\n[Request Body Schema]")
        print(json.dumps(body_schema, ensure_ascii=False, indent=2))
        example = schema_to_example(body_schema)
        if example:
            print("\n[Request Body Example]")
            print(json.dumps(example, ensure_ascii=False, indent=2))

    resp_schema = get_response_schema(spec, op, version)
    if resp_schema:
        print("\n[200 Response Schema]")
        print(json.dumps(resp_schema, ensure_ascii=False, indent=2))
    print()


def mode_cache(spec, plat):
    pid = plat["_id"]
    cache_file = os.path.join(CACHE_DIR, f"{pid}.json")
    print(f"[OK] Swagger cached at: {cache_file} ({os.path.getsize(cache_file)} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Online Swagger/OpenAPI parser")
    parser.add_argument("--config", required=True, help="Platform config file path")
    parser.add_argument("--platform", help="Specify platform ID")
    parser.add_argument("--mode", required=True, choices=["list", "search", "detail", "tags", "cache"])
    parser.add_argument("--keyword", help="Search keyword (mode=search)")
    parser.add_argument("--path", help="API path (mode=detail)")
    parser.add_argument("--method", help="HTTP method (mode=detail)", default="GET")
    parser.add_argument("--refresh", action="store_true", help="Force refresh cache")
    args = parser.parse_args()

    plat = load_config(args.config, args.platform)
    spec = fetch_swagger(plat, refresh=args.refresh)

    if args.mode == "list":
        mode_list(spec)
    elif args.mode == "search":
        if not args.keyword:
            sys.exit("[ERROR] --keyword is required")
        mode_search(spec, args.keyword)
    elif args.mode == "detail":
        if not args.path:
            sys.exit("[ERROR] --path is required")
        mode_detail(spec, args.path, args.method)
    elif args.mode == "tags":
        mode_tags(spec)
    elif args.mode == "cache":
        mode_cache(spec, plat)


if __name__ == "__main__":
    main()

r"""component_manager.py - 组件库管理：列出、添加、删除、搜索组件"""

import json
import os
import sys
from pathlib import Path

COMPONENTS_DIR = Path(__file__).parent / "components"
MANIFEST_PATH = COMPONENTS_DIR / "manifest.json"

def load_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"components": []}

def save_manifest(manifest):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def list_components(manifest=None):
    if manifest is None:
        manifest = load_manifest()
    print(f"组件总数: {len(manifest['components'])}")
    by_type = {}
    for c in manifest["components"]:
        by_type.setdefault(c["type"], []).append(c)
    for t, clist in by_type.items():
        print(f"\n[{t}]")
        for c in clist:
            print(f"  {c['name']:25s}  {c['path']}")

def add_component(name, comp_type, file_path, category, description, manifest=None):
    if manifest is None:
        manifest = load_manifest()
    manifest["components"] = [c for c in manifest["components"] if c["name"] != name]
    manifest["components"].append({
        "type": comp_type,
        "name": name,
        "path": file_path,
        "category": category,
        "description": description
    })
    save_manifest(manifest)
    print(f"[OK] 已添加/更新组件: {name}")
    return manifest

def remove_component(name, manifest=None):
    if manifest is None:
        manifest = load_manifest()
    before = len(manifest["components"])
    manifest["components"] = [c for c in manifest["components"] if c["name"] != name]
    after = len(manifest["components"])
    save_manifest(manifest)
    if before != after:
        print(f"[OK] 已删除组件: {name}")
    else:
        print(f"[WARN] 未找到组件: {name}")
    return manifest

def search_components(keyword, manifest=None):
    if manifest is None:
        manifest = load_manifest()
    results = []
    for c in manifest["components"]:
        text = json.dumps(c, ensure_ascii=False).lower()
        if keyword.lower() in text:
            results.append(c)
    if not results:
        print(f"[INFO] 未找到匹配 '{keyword}' 的组件")
    else:
        print(f"找到 {len(results)} 个匹配组件：")
        for c in results:
            print(f"  [{c['type']}] {c['name']}  {c['description']}")
    return results

def main():
    if len(sys.argv) < 2:
        print(r"用法:")
        print(r"  python component_manager.py list")
        print(r"  python component_manager.py add <name> <type> <path> <category> <desc>")
        print(r"  python component_manager.py remove <name>")
        print(r"  python component_manager.py search <keyword>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_components()
    elif cmd == "add" and len(sys.argv) >= 7:
        add_component(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif cmd == "remove" and len(sys.argv) >= 3:
        remove_component(sys.argv[2])
    elif cmd == "search" and len(sys.argv) >= 3:
        search_components(sys.argv[2])
    else:
        print(f"未知命令或参数不足: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()

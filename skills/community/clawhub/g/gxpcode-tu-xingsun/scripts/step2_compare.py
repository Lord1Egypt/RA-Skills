# GxpCode Skill — 2 比对：按 sources.yaml 遍历各源的 s1_*.json，跟 history 比对

import json
import os
import yaml
from datetime import datetime
from lib.logger import get_logger
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logger = get_logger("compare")


def _load_sources(sources_path: str) -> list:
    with open(sources_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("sources", [])


def _load_s1(name: str, gxpcode: str) -> list:
    """读 gxpcode_data/s1/{name}.json，不存在返回 []"""
    path = os.path.join(gxpcode, "s1", f"s1_{name.replace('/', '_')}.json")
    if not os.path.exists(path):
        logger.info(f"S1 file not found: {name}, skip")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_history(history_path: str) -> dict:
    """读 history.json → {source: [records]}"""
    if not os.path.exists(history_path):
        return {}
    with open(history_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _save_history(history: dict, history_path: str):
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def _build_index(history: dict) -> dict:
    """{source → {title||url: True}}，O(1) 查找"""
    index = {}
    for source, records in history.items():
        index[source] = {f"{r['title']}||{r['url']}": True for r in records}
    return index


def compare(sources_path: str, config_path: str, gxpcode: str, history_path: str) -> list:
    sources = _load_sources(sources_path)
    history = _load_history(history_path)
    index = _build_index(history)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    all_new = []
    for src in sources:
        name = src["name"]
        items = _load_s1(name, gxpcode)
        if not items:
            continue

        source_index = index.get(name, {})

        for item in items:
            key = f"{item['title']}||{item['url']}"
            if key not in source_index:
                all_new.append(item)

    logger.info(f"Compare: {len(all_new)} new items")
    return all_new


def write_s2(items: list, gxpcode: str):
    """按 source 分组写入 s2/{source}.json"""
    s2_dir = os.path.join(gxpcode, "s2")
    os.makedirs(s2_dir, exist_ok=True)
    groups = {}
    for item in items:
        src = item["source"]
        groups.setdefault(src, []).append(item)
    for src, grp in groups.items():
        path = os.path.join(s2_dir, f"s2_{src.replace('/', '_')}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(grp, f, ensure_ascii=False, indent=2)
    logger.info(f"s2/: {sum(len(v) for v in groups.values())} items in {len(groups)} files")


if __name__ == "__main__":
    import sys
    gxpcode = sys.argv[1] if len(sys.argv) > 1 else "gxpcode_data"
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(skill_dir, "resources", "sources.yaml")
    config_path = os.path.join(skill_dir, "resources", "config.yaml")
    history_path = os.path.join(skill_dir, "gxpcode_data", "history.json")

    new = compare(sources_path, config_path, gxpcode, history_path)
    write_s2(new, gxpcode)
    # 标记完成
    with open(os.path.join(gxpcode, "s2", ".done"), "w") as f:
        f.write("")
    from collections import Counter
    c = Counter(i["source"] for i in new)
    for k, v in c.items():
        print(f"  {k}: {v}")
    print(f"s2/: {len(new)} items in {len(c)} files")

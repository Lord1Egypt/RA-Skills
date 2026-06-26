#!/usr/bin/env python3
"""
从 references/ 目录加载离线博物馆文物数据。

CSV 表头约定：
  文物名称, 展厅, 时期, 参观顺序, 是否镇馆之宝, 文物种类, 所属领域, 人员类别

人员类别：1 = 不适合儿童（child_friendly=False），其他值视为适合
是否镇馆之宝：t/true/1/yes/是 → True，其余 → False
所属领域：JSON 数组字符串，如 ["绘画","书法"]，或逗号分隔字符串
"""

import csv
import json
import os
from pathlib import Path
from typing import Optional, List, Dict


# references 目录相对于本脚本的位置
REFERENCES_DIR = Path(__file__).parent.parent / "references"


def list_available_museums() -> List[str]:
    """返回 references/ 中所有可用的博物馆名称（不含 .csv 后缀）"""
    if not REFERENCES_DIR.exists():
        return []
    return [f.stem for f in REFERENCES_DIR.glob("*.csv")]


def find_reference_file(museum_name: str) -> Optional[Path]:
    """
    根据博物馆名称查找对应的 CSV 文件。
    支持精确匹配和包含匹配（如"国博"匹配"中国国家博物馆"）。
    """
    if not REFERENCES_DIR.exists():
        return None

    # 精确匹配
    exact = REFERENCES_DIR / f"{museum_name}.csv"
    if exact.exists():
        return exact

    # 包含匹配：CSV 文件名包含用户输入，或用户输入包含 CSV 文件名
    for csv_file in REFERENCES_DIR.glob("*.csv"):
        stem = csv_file.stem
        if museum_name in stem or stem in museum_name:
            return csv_file

    return None


def _parse_bool(value: str) -> bool:
    """解析是否镇馆之宝字段"""
    return value.strip().lower() in ("t", "true", "1", "yes", "是")


def _parse_domains(value: str) -> List[str]:
    """解析所属领域字段，支持 JSON 数组或逗号分隔"""
    value = value.strip()
    if not value:
        return []
    try:
        result = json.loads(value)
        if isinstance(result, list):
            return [str(d) for d in result]
    except (json.JSONDecodeError, ValueError):
        pass
    # 逗号分隔
    return [d.strip() for d in value.split(",") if d.strip()]


def load_artifacts_from_csv(museum_name: str) -> Optional[List[Dict]]:
    """
    加载指定博物馆的离线文物数据。
    找不到对应 CSV 时返回 None（触发在线搜索）。
    找到但解析失败时返回空列表。
    """
    csv_path = find_reference_file(museum_name)
    if csv_path is None:
        return None  # 没有离线数据，走在线流程

    artifacts = []
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("文物名称", "").strip()
                if not name:
                    continue  # 跳过空行

                # 参观顺序（用于最终排序）
                try:
                    visit_order = int(row.get("参观顺序", "9999").strip())
                except ValueError:
                    visit_order = 9999

                artifact = {
                    "name": name,
                    "hall": row.get("展厅", "").strip() or "待确认",
                    "period": row.get("时期", "").strip(),
                    "visit_order": visit_order,
                    "is_treasure": _parse_bool(row.get("是否镇馆之宝", "f")),
                    "type": row.get("文物种类", "").strip(),
                    "domains": _parse_domains(row.get("所属领域", "")),
                    "child_friendly": row.get("人员类别", "0").strip() != "1",
                    "description": "",   # 离线数据暂无描述，推荐理由由 LLM 生成
                    "museum_name": csv_path.stem,  # 博物馆全称，供 LLM 生成理由时使用
                }
                artifacts.append(artifact)

        # 按参观顺序排序
        artifacts.sort(key=lambda a: a["visit_order"])
        return artifacts

    except Exception as e:
        import sys
        print(f"读取 CSV 失败 ({csv_path}): {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    import sys
    museum = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    available = list_available_museums()
    print(f"可用离线博物馆: {available}")
    if museum:
        result = load_artifacts_from_csv(museum)
        if result is None:
            print(f"未找到 {museum} 的离线数据")
        else:
            print(f"加载 {len(result)} 件文物")
            import json as _json
            print(_json.dumps(result[:2], ensure_ascii=False, indent=2))

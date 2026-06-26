#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notebook-builder 核心辅助脚本

提供 Jupyter Notebook 的创建、分段生成、修改、图片嵌入、判题等功能。
所有操作均基于 nbformat v4 标准 (.ipynb JSON 格式)，直接使用 json 模块读写。

依赖: 仅标准库 (json, base64, hashlib, pathlib 等)，无需安装第三方包。
"""

import base64
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

__all__ = [
    # I/O
    "new_notebook",
    "load_notebook",
    "save_notebook",
    # Cell 构造
    "make_markdown_cell",
    "make_code_cell",
    "make_raw_cell",
    # 增删改查
    "append_cells",
    "insert_cells",
    "delete_cells",
    "replace_cell",
    "find_cells_by_keyword",
    "find_cells_by_id",
    "get_cell_count",
    "get_cell_summary",
    # 图片嵌入
    "embed_image_in_markdown",
    "make_image_output",
    # 判题系统
    "make_quiz_code_cell",
    "make_quiz_summary_cell",
    # 批量操作
    "make_section",
    "make_divider_cell",
    # 合并与导出
    "merge_notebooks",
    "export_to_script",
    # 目录生成
    "make_toc_cell",
    # Cell 重排序
    "reorder_cells",
    # Cell 标签系统
    "tag_cell",
    "find_cells_by_tag",
    # 工具函数
    "clear_all_outputs",
    "set_kernel",
    "nb_info",
]


# ============================================================
# 1. 基础 Notebook I/O
# ============================================================

def new_notebook(
    kernel_name: str = "python3",
    display_name: str = "Python 3",
    language: str = "python",
) -> Dict[str, Any]:
    """创建一个空的 notebook 字典（nbformat v4）。"""
    return {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": display_name,
                "language": language,
                "name": kernel_name,
            },
            "language_info": {
                "name": language,
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def load_notebook(path: str) -> Dict[str, Any]:
    """从文件加载 notebook，返回字典。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notebook(nb: Dict[str, Any], path: str) -> None:
    """将 notebook 字典写入文件。"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"✅ Notebook 已保存: {path}")


# ============================================================
# 2. Cell 构造工厂
# ============================================================

def make_markdown_cell(source: str, cell_id: Optional[str] = None) -> Dict[str, Any]:
    """构造一个 Markdown cell。"""
    cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": _normalize_source(source),
    }
    if cell_id:
        cell["id"] = cell_id
    return cell


def make_code_cell(
    source: str,
    cell_id: Optional[str] = None,
    execution_count: Optional[int] = None,
    outputs: Optional[List] = None,
) -> Dict[str, Any]:
    """构造一个 Code cell。"""
    cell = {
        "cell_type": "code",
        "metadata": {},
        "source": _normalize_source(source),
        "execution_count": execution_count,
        "outputs": outputs if outputs is not None else [],
    }
    if cell_id:
        cell["id"] = cell_id
    return cell


def make_raw_cell(source: str, cell_id: Optional[str] = None) -> Dict[str, Any]:
    """构造一个 Raw cell。"""
    cell = {
        "cell_type": "raw",
        "metadata": {},
        "source": _normalize_source(source),
    }
    if cell_id:
        cell["id"] = cell_id
    return cell


def _normalize_source(source: Union[str, List[str]]) -> List[str]:
    """统一将 source 转换为行列表格式（保留原始换行）。"""
    if isinstance(source, list):
        return source
    # 将字符串按行拆分，保留换行符
    lines = source.splitlines(True)
    # 最后一行不加 \n，符合 nbformat 惯例
    return lines


# ============================================================
# 3. 分段追加 / 插入 / 删除 / 替换
# ============================================================

def append_cells(nb: Dict[str, Any], cells: List[Dict[str, Any]]) -> int:
    """向 notebook 末尾追加一批 cell，返回追加后的总 cell 数。

    :param nb: notebook 字典对象
    :param cells: 要追加的 cell 列表（由 make_*_cell 函数生成）
    :return: 追加后 notebook 的总 cell 数量
    """
    nb["cells"].extend(cells)
    return len(nb["cells"])


def insert_cells(
    nb: Dict[str, Any],
    index: int,
    cells: List[Dict[str, Any]],
) -> int:
    """在 index 位置插入一批 cell（原 index 及之后的 cell 后移）。

    :param nb: notebook 字典对象
    :param index: 插入位置的索引（0-based）
    :param cells: 要插入的 cell 列表
    :return: 插入后 notebook 的总 cell 数量
    """
    for i, cell in enumerate(cells):
        nb["cells"].insert(index + i, cell)
    return len(nb["cells"])


def delete_cells(nb: Dict[str, Any], start: int, count: int = 1) -> List[Dict[str, Any]]:
    """删除从 start 开始的 count 个 cell，返回被删除的 cell 列表。

    :param nb: notebook 字典对象
    :param start: 起始索引（0-based）
    :param count: 要删除的 cell 数量，默认为 1
    :return: 被删除的 cell 列表
    """
    removed = nb["cells"][start:start + count]
    nb["cells"][start:start + count] = []
    return removed


def replace_cell(nb: Dict[str, Any], index: int, new_cell: Dict[str, Any]) -> Dict[str, Any]:
    """替换指定 index 的 cell，返回被替换的旧 cell。"""
    old = nb["cells"][index]
    nb["cells"][index] = new_cell
    return old


def find_cells_by_keyword(nb: Dict[str, Any], keyword: str) -> List[Tuple[int, Dict[str, Any]]]:
    """按关键词搜索 cell，返回 (index, cell) 列表。"""
    results = []
    for idx, cell in enumerate(nb["cells"]):
        source_text = "".join(cell.get("source", []))
        if keyword in source_text:
            results.append((idx, cell))
    return results


def find_cells_by_id(nb: Dict[str, Any], cell_id: str) -> Optional[Tuple[int, Dict[str, Any]]]:
    """按 cell id 查找，返回 (index, cell) 或 None。"""
    for idx, cell in enumerate(nb["cells"]):
        if cell.get("id") == cell_id:
            return (idx, cell)
    return None


def get_cell_count(nb: Dict[str, Any]) -> int:
    """返回 notebook 中 cell 的数量。"""
    return len(nb["cells"])


def get_cell_summary(nb: Dict[str, Any]) -> List[str]:
    """返回 notebook 中每个 cell 的简要摘要（类型 + 前 60 字符）。"""
    summaries = []
    for idx, cell in enumerate(nb["cells"]):
        ctype = cell.get("cell_type", "unknown")
        src = "".join(cell.get("source", []))
        preview = src.replace("\n", " ")[:60]
        summaries.append(f"[{idx}] ({ctype}) {preview}")
    return summaries


# ============================================================
# 4. 图片嵌入
# ============================================================

def embed_image_in_markdown(
    image_path: str,
    alt_text: str = "image",
    width: Optional[int] = None,
) -> str:
    """将本地图片编码为 base64，返回可直接嵌入 Markdown cell 的 HTML/Markdown。

    如果指定 width，使用 <img> 标签；否则使用标准 Markdown 图片语法。
    支持 PNG、JPG、GIF、SVG 格式。

    :param image_path: 本地图片文件路径
    :param alt_text: 图片替代文字，默认为 "image"
    :param width: 可选的图片宽度（像素），指定后使用 <img> 标签
    :return: 包含 base64 数据的 Markdown 图片字符串
    :raises FileNotFoundError: 图片文件不存在时抛出
    """
    img_bytes = Path(image_path).read_bytes()
    ext = Path(image_path).suffix.lower().lstrip(".")
    mime_map = {"png": "png", "jpg": "jpeg", "jpeg": "jpeg", "gif": "gif", "svg": "svg+xml"}
    mime = mime_map.get(ext, "png")
    b64 = base64.b64encode(img_bytes).decode("ascii")
    data_uri = f"data:image/{mime};base64,{b64}"

    if width:
        return f'<img src="{data_uri}" alt="{alt_text}" width="{width}" />'
    return f"![{alt_text}]({data_uri})"


def make_image_output(
    image_path: str,
    mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    """为 Code cell 生成一个 display_data 输出项，内含 base64 图片。"""
    img_bytes = Path(image_path).read_bytes()
    ext = Path(image_path).suffix.lower().lstrip(".")
    if mime_type is None:
        mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}
        mime_type = mime_map.get(ext, "image/png")
    b64 = base64.b64encode(img_bytes).decode("ascii")
    return {
        "output_type": "display_data",
        "data": {
            mime_type: b64,
            "text/plain": [f"<Image: {Path(image_path).name}>"],
        },
        "metadata": {},
    }


# ============================================================
# 5. 判题系统 (不显示明文答案)
# ============================================================

_HASH_SALT = "nb_builder_quiz_v1"


def _hash_answer(answer: Any) -> str:
    """对答案进行加盐哈希，确保不可逆。"""
    # 标准化答案：字符串去首尾空格并小写；元组/列表转字符串
    if isinstance(answer, (list, tuple)):
        normalized = str(tuple(answer))
    elif isinstance(answer, bool):
        normalized = str(answer)
    elif isinstance(answer, (int, float)):
        normalized = str(answer)
    elif isinstance(answer, str):
        normalized = answer.strip().lower()
    else:
        normalized = str(answer)

    raw = f"{_HASH_SALT}:{normalized}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def make_quiz_code_cell(
    question_id: str,
    question_prompt: str,
    answer: Any,
    answer_type: str = "auto",
    hints: Optional[List[str]] = None,
    score: int = 10,
) -> Dict[str, Any]:
    """生成一道判题 Code cell。

    答案以哈希形式存储在 cell metadata 中，学生看不到明文。
    学生填写后运行 cell 即可自动判题。

    Args:
        question_id: 题目唯一标识，如 "q1_1"
        question_prompt: 题目描述（注释形式展示）
        answer: 正确答案（支持 str, int, float, bool, tuple, list）
        answer_type: 答案类型提示 ("str", "int", "float", "bool", "tuple", "auto")
        hints: 可选的提示列表
        score: 此题分数
    """
    answer_hash = _hash_answer(answer)

    # 构建学生看到的代码模板
    hint_lines = ""
    if hints:
        for h in hints:
            hint_lines += f"# 💡 提示: {h}\n"

    # 验证函数内嵌在 cell 中，不暴露答案
    source = f'''# ===== {question_id}: {question_prompt} =====
{hint_lines}# 请在下方填写你的答案
answer_{question_id} = None  # ← 替换 None 为你的答案

# ===== 自动判题（请勿修改以下代码）=====
import hashlib as _hl
def _check_{question_id}(user_ans):
    _salt = "{_HASH_SALT}"
    if isinstance(user_ans, (list, tuple)):
        _n = str(tuple(user_ans))
    elif isinstance(user_ans, bool):
        _n = str(user_ans)
    elif isinstance(user_ans, (int, float)):
        _n = str(user_ans)
    elif isinstance(user_ans, str):
        _n = user_ans.strip().lower()
    else:
        _n = str(user_ans)
    _h = _hl.sha256(f"{{_salt}}:{{_n}}".encode()).hexdigest()[:16]
    if _h == "{answer_hash}":
        print(f"✅ {question_id} 正确！(+{score}分)")
        return True
    else:
        print(f"❌ {question_id} 错误，请再想想。")
        return False

if answer_{question_id} is not None:
    _check_{question_id}(answer_{question_id})
else:
    print("⏳ {question_id}: 等待作答...")
'''
    cell = make_code_cell(source, cell_id=f"quiz_{question_id}")
    # 在 metadata 中存储判题元信息（不含明文答案）
    cell["metadata"]["quiz"] = {
        "question_id": question_id,
        "answer_hash": answer_hash,
        "answer_type": answer_type,
        "score": score,
    }
    return cell


def make_quiz_summary_cell(
    question_ids: List[str],
    total_score: int,
    scores: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """生成一个汇总判题结果的 Code cell。

    遍历所有题目的判题函数，逐题检查并输出总分。
    每道题的分数通过 scores 参数指定，未指定时按 total_score 平均分配。

    :param question_ids: 题目 ID 列表，如 ["q1", "q2", "q3"]
    :param total_score: 满分总分
    :param scores: 可选的题目分数映射，如 {"q1": 10, "q2": 20}。
                   未指定时按 total_score / len(question_ids) 平均分配。
    :return: 汇总评分的 Code cell 字典
    """
    if scores is None:
        avg = total_score // len(question_ids) if question_ids else 0
        scores = {qid: avg for qid in question_ids}

    check_lines = []
    for qid in question_ids:
        qscore = scores.get(qid, 0)
        check_lines.append(
            f'    if answer_{qid} is not None and _check_{qid}(answer_{qid}):\n'
            f'        _score += {qscore}'
        )

    score_dict_items = ", ".join(
        f'"{qid}": {scores.get(qid, 0)}' for qid in question_ids
    )

    source = f'''# ===== 📊 考核汇总 =====
# 运行此 cell 查看总成绩

_quiz_scores = {{{score_dict_items}}}
_score = 0
_total = {total_score}

# 逐题检查
{"".join(check_lines)}

print(f"\\n{'='*40}")
print(f"📊 总分: {{_score}} / {{_total}}")
if _score == _total:
    print("🎉 满分！完美！")
elif _score >= _total * 0.8:
    print("👍 优秀！还有一点小遗漏。")
elif _score >= _total * 0.6:
    print("💪 良好，继续加油！")
else:
    print("📚 需要复习一下哦。")
'''
    return make_code_cell(source, cell_id="quiz_summary")


# ============================================================
# 6. 合并与导出
# ============================================================

def merge_notebooks(
    paths: List[str],
    output_path: Optional[str] = None,
    add_dividers: bool = True,
    add_titles: bool = False,
) -> Dict[str, Any]:
    """合并多个 notebook 文件为一个。

    以第一个 notebook 的 metadata（kernel 等）为基准，
    依次将后续 notebook 的所有 cell 追加到合并结果中。

    :param paths: 要合并的 notebook 文件路径列表（按顺序）
    :param output_path: 可选的输出路径，指定后自动保存合并结果
    :param add_dividers: 是否在每个 notebook 之间插入分隔线，默认 True
    :param add_titles: 是否在每个 notebook 之前插入来源标注，默认 False
    :return: 合并后的 notebook 字典
    :raises ValueError: paths 为空时抛出
    :raises FileNotFoundError: 文件不存在时抛出
    """
    if not paths:
        raise ValueError("至少需要提供一个 notebook 路径")

    merged = load_notebook(paths[0])

    for i, path in enumerate(paths[1:], start=2):
        nb = load_notebook(path)
        if add_dividers:
            merged["cells"].append(make_divider_cell())
        if add_titles:
            filename = Path(path).stem
            merged["cells"].append(
                make_markdown_cell(f"<!-- 来源: {filename} -->")
            )
        merged["cells"].extend(nb["cells"])

    if output_path:
        save_notebook(merged, output_path)
    print(f"✅ 已合并 {len(paths)} 个 notebook，共 {len(merged['cells'])} 个 cell")
    return merged


def export_to_script(
    nb: Dict[str, Any],
    output_path: str,
    include_markdown: bool = True,
) -> None:
    """将 notebook 导出为纯 Python 脚本 (.py)。

    Code cell 的内容直接写入，Markdown cell 可选地转为 Python 注释。
    Raw cell 会被跳过。

    :param nb: notebook 字典对象
    :param output_path: 输出的 .py 文件路径
    :param include_markdown: 是否将 Markdown cell 转为注释写入，默认 True
    """
    lines: List[str] = []
    lines.append("#!/usr/bin/env python3")
    lines.append("# -*- coding: utf-8 -*-")
    lines.append(f'# 由 notebook-builder 从 notebook 导出')
    lines.append("")

    for idx, cell in enumerate(nb["cells"]):
        cell_type = cell.get("cell_type", "unknown")
        source = "".join(cell.get("source", []))

        if cell_type == "code":
            lines.append(f"# %% [Cell {idx}] Code")
            lines.append(source)
            lines.append("")
        elif cell_type == "markdown" and include_markdown:
            lines.append(f"# %% [Cell {idx}] Markdown")
            for line in source.splitlines():
                lines.append(f"# {line}" if line.strip() else "#")
            lines.append("")
        # raw cell 跳过

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")
    print(f"✅ 已导出为 Python 脚本: {output_path}")


# ============================================================
# 7. 目录生成
# ============================================================

def make_toc_cell(
    nb: Dict[str, Any],
    max_level: int = 3,
    title: str = "📑 目录",
) -> Dict[str, Any]:
    """扫描 notebook 中所有 Markdown cell 的标题，生成一个目录 cell。

    目录项使用 Markdown 链接格式，可在 Jupyter 中点击跳转。

    :param nb: notebook 字典对象
    :param max_level: 最大收录的标题层级（1-6），默认 3（即收录 #, ##, ###）
    :param title: 目录的标题文本
    :return: 包含目录内容的 Markdown cell
    """
    toc_lines = [f"## {title}", ""]

    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        for line in source.splitlines():
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue
            # 计算标题层级
            level = 0
            for ch in stripped:
                if ch == "#":
                    level += 1
                else:
                    break
            if level < 1 or level > max_level:
                continue
            heading_text = stripped[level:].strip()
            if not heading_text:
                continue
            # 生成锚点链接（Jupyter 风格：小写、空格变 -、去特殊字符）
            anchor = heading_text.lower()
            anchor = anchor.replace(" ", "-")
            # 保留字母、数字、中文、连字符
            anchor_chars = []
            for ch in anchor:
                if ch.isalnum() or ch == "-" or "\u4e00" <= ch <= "\u9fff":
                    anchor_chars.append(ch)
            anchor = "".join(anchor_chars)
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{heading_text}](#{anchor})")

    if len(toc_lines) <= 2:
        toc_lines.append("_（未发现标题）_")

    return make_markdown_cell("\n".join(toc_lines), cell_id="toc")


# ============================================================
# 8. Cell 重排序
# ============================================================

def reorder_cells(
    nb: Dict[str, Any],
    new_order: List[int],
) -> None:
    """按指定索引顺序重排 notebook 中的 cell。

    new_order 中的每个元素是 cell 在当前 notebook 中的索引。
    可以只包含部分索引（未包含的 cell 将被丢弃）。

    :param nb: notebook 字典对象
    :param new_order: 新的 cell 索引顺序列表，如 [2, 0, 1, 3]
    :raises IndexError: 索引越界时抛出
    """
    total = len(nb["cells"])
    for idx in new_order:
        if idx < 0 or idx >= total:
            raise IndexError(
                f"索引 {idx} 越界，notebook 共有 {total} 个 cell (0-{total - 1})"
            )
    nb["cells"] = [nb["cells"][i] for i in new_order]
    print(f"✅ 已重排序 {len(new_order)} 个 cell")


# ============================================================
# 9. Cell 标签系统
# ============================================================

def tag_cell(
    cell: Dict[str, Any],
    tags: Union[str, List[str]],
) -> None:
    """为 cell 添加标签到 metadata.tags 中。

    标签存储在 cell["metadata"]["tags"] 列表中，
    这是 nbformat 标准支持的字段，JupyterLab 可直接识别。

    :param cell: cell 字典对象
    :param tags: 单个标签字符串或标签列表，如 "exercise" 或 ["exercise", "hard"]
    """
    if isinstance(tags, str):
        tags = [tags]
    existing = cell.get("metadata", {}).get("tags", [])
    merged = list(existing)
    for tag in tags:
        if tag not in merged:
            merged.append(tag)
    cell.setdefault("metadata", {})["tags"] = merged


def find_cells_by_tag(
    nb: Dict[str, Any],
    tag: str,
) -> List[Tuple[int, Dict[str, Any]]]:
    """按标签查找 cell，返回 (index, cell) 列表。

    :param nb: notebook 字典对象
    :param tag: 要搜索的标签名
    :return: 匹配的 (index, cell) 元组列表
    """
    results = []
    for idx, cell in enumerate(nb["cells"]):
        cell_tags = cell.get("metadata", {}).get("tags", [])
        if tag in cell_tags:
            results.append((idx, cell))
    return results


# ============================================================
# 10. 批量操作辅助
# ============================================================

def make_section(
    title: str,
    content_md: str = "",
    code_cells: Optional[List[str]] = None,
    level: int = 2,
) -> List[Dict[str, Any]]:
    """快速生成一个章节：一个标题 Markdown cell + 可选内容 + 若干 Code cell。

    :param title: 章节标题文本
    :param content_md: 可选的 Markdown 正文内容
    :param code_cells: 可选的代码字符串列表，每个字符串生成一个 Code cell
    :param level: 标题层级（1-6），默认为 2（即 ##）
    :return: 由 Markdown cell 和 Code cell 组成的列表
    """
    header = "#" * level + " " + title
    cells = []
    if content_md:
        cells.append(make_markdown_cell(f"{header}\n\n{content_md}"))
    else:
        cells.append(make_markdown_cell(header))
    if code_cells:
        for code in code_cells:
            cells.append(make_code_cell(code))
    return cells


def make_divider_cell() -> Dict[str, Any]:
    """生成一个分隔线 Markdown cell。"""
    return make_markdown_cell("---")


# ============================================================
# 11. 实用工具
# ============================================================

def clear_all_outputs(nb: Dict[str, Any]) -> int:
    """清除所有 Code cell 的输出，返回清除的 cell 数。"""
    count = 0
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
            count += 1
    return count


def set_kernel(nb: Dict[str, Any], kernel_name: str, display_name: str) -> None:
    """修改 notebook 的 kernel 信息。"""
    nb["metadata"]["kernelspec"]["name"] = kernel_name
    nb["metadata"]["kernelspec"]["display_name"] = display_name


def nb_info(nb: Dict[str, Any]) -> Dict[str, Any]:
    """返回 notebook 的基本统计信息。"""
    cell_types = {}
    for cell in nb["cells"]:
        ct = cell.get("cell_type", "unknown")
        cell_types[ct] = cell_types.get(ct, 0) + 1
    return {
        "total_cells": len(nb["cells"]),
        "cell_types": cell_types,
        "kernel": nb.get("metadata", {}).get("kernelspec", {}).get("name", "unknown"),
        "nbformat": nb.get("nbformat", "?"),
    }


# ============================================================
# 入口：命令行快速测试
# ============================================================

if __name__ == "__main__":
    print("=== notebook-builder 辅助脚本 ===")
    print("可用函数:")
    print("  new_notebook()           - 创建空 notebook")
    print("  load_notebook(path)      - 加载 notebook")
    print("  save_notebook(nb, path)  - 保存 notebook")
    print("  make_markdown_cell(src)  - 创建 Markdown cell")
    print("  make_code_cell(src)      - 创建 Code cell")
    print("  append_cells(nb, cells)  - 追加 cell")
    print("  insert_cells(nb, i, cs)  - 插入 cell")
    print("  delete_cells(nb, i, n)   - 删除 cell")
    print("  replace_cell(nb, i, c)   - 替换 cell")
    print("  embed_image_in_markdown()- 嵌入图片到 Markdown")
    print("  make_quiz_code_cell()    - 生成判题 cell")
    print("  make_section()           - 生成章节")
    print("  clear_all_outputs(nb)    - 清除所有输出")
    print("  nb_info(nb)              - Notebook 统计信息")

    # 快速自检
    nb = new_notebook()
    append_cells(nb, make_section("测试章节", "这是一个自检用的章节。", ["print('hello')"]))
    quiz = make_quiz_code_cell("test_q1", "1 + 1 = ?", 2, score=10)
    append_cells(nb, [quiz])
    summary = make_quiz_summary_cell(
        ["test_q1"],
        total_score=10,
        scores={"test_q1": 10},
    )
    append_cells(nb, [summary])
    # 新功能自检
    print("\n--- 新功能自检 ---")

    # 标签系统
    tag_cell(nb["cells"][0], ["intro", "important"])
    tag_cell(nb["cells"][1], "code")
    tagged = find_cells_by_tag(nb, "intro")
    assert len(tagged) == 1, f"标签查找失败: 期望 1，得到 {len(tagged)}"
    print("✅ 标签系统正常")

    # 目录生成
    toc = make_toc_cell(nb)
    assert toc["cell_type"] == "markdown"
    print("✅ 目录生成正常")

    # 重排序
    original_count = len(nb["cells"])
    reorder_cells(nb, list(range(original_count - 1, -1, -1)))
    assert len(nb["cells"]) == original_count
    print("✅ 重排序正常")

    # 导出为脚本
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp_path = tmp.name
    export_to_script(nb, tmp_path)
    assert Path(tmp_path).exists()
    Path(tmp_path).unlink()
    print("✅ 导出为脚本正常")

    # 合并 notebook
    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp1:
        tmp1_path = tmp1.name
    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp2:
        tmp2_path = tmp2.name
    nb1 = new_notebook()
    append_cells(nb1, [make_markdown_cell("# NB1")])
    save_notebook(nb1, tmp1_path)
    nb2 = new_notebook()
    append_cells(nb2, [make_markdown_cell("# NB2")])
    save_notebook(nb2, tmp2_path)
    merged = merge_notebooks([tmp1_path, tmp2_path])
    assert len(merged["cells"]) == 3  # NB1 cell + divider + NB2 cell
    Path(tmp1_path).unlink()
    Path(tmp2_path).unlink()
    print("✅ 合并 notebook 正常")

    info = nb_info(nb)
    print(f"\n自检 notebook: {info}")
    print("✅ 全部自检通过")

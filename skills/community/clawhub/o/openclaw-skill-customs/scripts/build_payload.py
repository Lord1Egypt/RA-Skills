#!/usr/bin/env python3
"""
Leap customs payload 构建工具

读取分类任务结果（本地 JSON 文件 或 API 查询），
自动组装可直接用于 customs 提交的 payload 文件。

用法:
  从本地文件构建（推荐，classify 完成后自动保存）：
    python scripts/build_payload.py --input classify_result.json

  从 API 实时获取并构建：
    python scripts/build_payload.py --classify-result-id <result_id>

  指定输出路径（默认 customs_payload.json）：
    python scripts/build_payload.py --input classify_result.json --output my_payload.json

零外部依赖 — 仅使用 Python 标准库。
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULT_BASE_URL = "https://platform.daofeiai.com"
DEFAULT_OUTPUT = "customs_payload.json"


def _fetch_from_api(result_id: str, api_key: str) -> dict:
    """从 API 获取任务结果。"""
    url = f"{DEFAULT_BASE_URL}/api/v1/process/tasks/{result_id}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e}") from e


def _extract_files(classify_data: dict) -> list:
    """从分类结果中提取 files 列表，兼容 API 响应的不同层级结构。"""
    # 优先从 result_data 中提取（完整 API 响应格式）
    result_data = classify_data.get("result_data", {})
    if result_data and "files" in result_data:
        return result_data["files"]
    # 降级：直接从顶层取（已裁剪的简化格式）
    if "files" in classify_data:
        return classify_data["files"]
    return []


def build_payload(classify_data: dict) -> dict:
    """
    从分类结果构建 customs API payload。

    保留每个文件的 file_id、file_name（可选）、segments 完整数组和 metadata（可选）。
    segments 中所有字段（type/file_type/confidence/pages 等）原样保留，
    确保 API 收到完整、有效的数据结构。
    """
    files_in = _extract_files(classify_data)
    if not files_in:
        raise ValueError(
            "分类结果中未找到 files 数组。"
            "请确认 classify_result.json 是已完成（status=completed）任务的完整输出。"
        )

    files_out = []
    for file_info in files_in:
        file_entry: dict = {
            "file_id": file_info.get("file_id", ""),
            "segments": file_info.get("segments", []),
        }
        # 可选字段：有则带上，无则不插入（保持 payload 干净）
        if file_info.get("file_name"):
            file_entry["file_name"] = file_info["file_name"]
        if file_info.get("metadata"):
            file_entry["metadata"] = file_info["metadata"]
        files_out.append(file_entry)

    return {"files": files_out}


def main():
    parser = argparse.ArgumentParser(
        description="从分类结果构建 customs 提交 payload（无需手动组装 segments）"
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--input",
        metavar="CLASSIFY_JSON",
        help="本地分类结果 JSON 文件路径（由 submit_and_poll.py --save-to 生成）",
    )
    source_group.add_argument(
        "--classify-result-id",
        metavar="RESULT_ID",
        help="分类任务 result_id，直接从 API 获取完整结果",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"输出 payload 文件路径（默认: {DEFAULT_OUTPUT}）",
    )
    args = parser.parse_args()

    # ── 加载分类结果 ───────────────────────────────────────────────────────
    if args.input:
        if not os.path.isfile(args.input):
            print(json.dumps({
                "status": "error",
                "error_message": f"文件不存在: {args.input}。请先运行 submit_and_poll.py --mode classify --save-to <文件名>",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                classify_data = json.load(f)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "status": "error",
                "error_message": f"JSON 解析失败: {e}。请检查 {args.input} 文件是否完整。",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        api_key = os.environ.get("LEAP_API_KEY", "")
        if not api_key:
            print(json.dumps({
                "status": "error",
                "error_message": "LEAP_API_KEY 未配置。请在 OpenClaw skill 设置中配置环境变量。",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        try:
            classify_data = _fetch_from_api(args.classify_result_id, api_key)
        except Exception as e:
            print(json.dumps({
                "status": "error",
                "error_message": f"从 API 获取结果失败: {e}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    # ── 构建 payload ───────────────────────────────────────────────────────
    try:
        payload = build_payload(classify_data)
    except ValueError as e:
        print(json.dumps({"status": "error", "error_message": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # ── 写入输出文件 ───────────────────────────────────────────────────────
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(json.dumps({
            "status": "error",
            "error_message": f"写入文件失败: {e}",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    abs_output = os.path.abspath(args.output)
    total_segments = sum(len(fi.get("segments", [])) for fi in payload["files"])

    print(json.dumps({
        "status": "success",
        "output_file": abs_output,
        "files_count": len(payload["files"]),
        "total_segments": total_segments,
        "tip": (
            f"如需修改某个分片的 file_type，请直接编辑 {abs_output} "
            f"中对应 segment 的 file_type 字段，保存后再提交 customs 任务。"
        ),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

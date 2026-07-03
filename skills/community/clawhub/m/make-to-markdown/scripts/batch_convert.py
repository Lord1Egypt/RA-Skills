#!/usr/bin/env python3
"""
Make-to-Markdown 批量转换脚本 (v2.2)

遍历目录，对支持的文件格式递归调用 convert.py 智能转换（依赖自动补全 → markitdown → 降级兜底 → 后置清洗），
保持原有目录层级，输出到指定目标目录。

用法:
    python batch_convert.py <source_dir> <output_dir>
    python batch_convert.py docs/ output/ --ext .pdf .docx
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


SUPPORTED_EXTS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp",
    ".mp3", ".wav", ".m4a", ".ogg", ".flac",
    ".epub", ".zip",
}


def find_convert_script() -> str:
    """定位 convert.py 脚本路径"""
    script_dir = Path(__file__).resolve().parent
    convert_py = script_dir / "convert.py"
    if convert_py.exists():
        return str(convert_py)
    print("错误：未找到 scripts/convert.py", file=sys.stderr)
    sys.exit(1)


def convert_file(convert_script: str, input_path: Path, output_path: Path) -> bool:
    """调用 convert.py 转换单个文件（依赖自动补全 + 降级兜底 + 清洗）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [sys.executable, convert_script, str(input_path), "-o", str(output_path), "-q"],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            # 提取错误信息
            err_lines = [l for l in result.stderr.split("\n") if l.strip()]
            err_msg = err_lines[-1] if err_lines else result.stderr.strip()[-200:]
            print(f"失败: {err_msg}")
            return False
        # 提取统计行
        for line in result.stdout.split("\n"):
            if "转换完成" in line or "H1=" in line:
                print(line.strip())
                break
        return True
    except subprocess.TimeoutExpired:
        print("超时")
        return False
    except Exception as e:
        print(f"异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Make-to-Markdown 批量转换（基于 convert.py）")
    parser.add_argument("source_dir", help="源目录路径")
    parser.add_argument("output_dir", help="输出目录路径")
    parser.add_argument("--ext", nargs="*", default=None,
                        help="仅处理指定扩展名（如 .pdf .docx），默认处理全部支持格式")
    args = parser.parse_args()

    source = Path(args.source_dir)
    output = Path(args.output_dir)

    if not source.is_dir():
        print(f"错误：源目录不存在 {args.source_dir}")
        sys.exit(1)

    target_exts = set(e.lower() for e in args.ext) if args.ext else SUPPORTED_EXTS
    target_exts = {e if e.startswith(".") else f".{e}" for e in target_exts}

    convert_script = find_convert_script()

    print(f"convert.py: {convert_script}")
    print(f"源目录: {source}")
    print(f"输出目录: {output}")
    print(f"过滤扩展名: {', '.join(sorted(target_exts))}")
    print()

    # 收集文件
    files_to_convert = []
    for root, dirs, files in os.walk(source):
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in target_exts:
                files_to_convert.append(fpath)

    if not files_to_convert:
        print("未找到匹配的文件。")
        return

    print(f"找到 {len(files_to_convert)} 个文件待转换\n")

    success_count = 0
    failed = []

    for idx, fpath in enumerate(files_to_convert, 1):
        rel = fpath.relative_to(source)
        out_rel = rel.with_suffix(".md")
        out_path = output / out_rel

        print(f"[{idx}/{len(files_to_convert)}] {rel} -> {out_rel} ... ", end="", flush=True)
        if convert_file(convert_script, fpath, out_path):
            success_count += 1
        else:
            failed.append(str(rel))

    # 汇总
    print(f"\n{'='*50}")
    print(f"转换完成: 成功 {success_count}, 失败 {len(failed)}")
    if failed:
        print("失败清单:")
        for f in failed:
            print(f"  - {f}")
        err_log = output / "_conversion_errors.log"
        err_log.write_text("\n".join(failed), encoding="utf-8")
        print(f"错误日志已保存: {err_log}")


if __name__ == "__main__":
    main()

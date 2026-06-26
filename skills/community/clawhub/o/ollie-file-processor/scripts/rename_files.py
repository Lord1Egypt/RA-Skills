#!/usr/bin/env python3
"""
文件重命名工具
支持批量重命名、添加前缀/后缀、替换字符、按规则编号等
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Pattern
import sys


class FileRenamer:
    """文件重命名器"""

    def __init__(self, directory: str, dry_run: bool = False):
        self.directory = Path(directory)
        self.dry_run = dry_run
        self.rename_operations = []

    def add_prefix(self, prefix: str, files: Optional[List[str]] = None):
        """为文件添加前缀"""
        file_list = self._get_file_list(files)
        for file_path in file_list:
            old_name = file_path.name
            new_name = f"{prefix}{old_name}"
            self._add_rename_operation(file_path, new_name)

    def add_suffix(self, suffix: str, files: Optional[List[str]] = None):
        """为文件添加后缀(在扩展名前)"""
        file_list = self._get_file_list(files)
        for file_path in file_list:
            old_name = file_path.name
            stem = file_path.stem
            suffix_ = file_path.suffix
            new_name = f"{stem}{suffix}{suffix_}"
            self._add_rename_operation(file_path, new_name)

    def replace_text(self, old_text: str, new_text: str, files: Optional[List[str]] = None):
        """替换文件名中的文本"""
        file_list = self._get_file_list(files)
        for file_path in file_list:
            old_name = file_path.name
            new_name = old_name.replace(old_text, new_text)
            self._add_rename_operation(file_path, new_name)

    def rename_with_numbering(
        self,
        pattern: str,
        start_num: int = 1,
        digits: int = 3,
        files: Optional[List[str]] = None,
        sort_by: str = "name"  # name, size, date
    ):
        """
        按规则编号重命名
        pattern: 命名模式,例如 "photo_{}.jpg", "{}" 会被替换为数字
        """
        file_list = self._get_file_list(files)

        # 排序
        if sort_by == "name":
            file_list = sorted(file_list, key=lambda x: x.name)
        elif sort_by == "size":
            file_list = sorted(file_list, key=lambda x: x.stat().st_size)
        elif sort_by == "date":
            file_list = sorted(file_list, key=lambda x: x.stat().st_mtime)

        # 生成新文件名
        num_format = f"{{:0{digits}d}}"
        for idx, file_path in enumerate(file_list):
            old_name = file_path.name
            ext = file_path.suffix

            # 处理模式
            if "{}" in pattern:
                new_name = pattern.replace("{}", num_format.format(start_num + idx))
            elif pattern.endswith(ext):
                # 如果模式已经包含扩展名,直接替换
                new_name = pattern
            else:
                # 否则添加原扩展名
                new_name = f"{pattern}{ext}"

            self._add_rename_operation(file_path, new_name)

    def rename_with_regex(
        self,
        pattern: str,
        replacement: str,
        files: Optional[List[str]] = None
    ):
        """使用正则表达式重命名"""
        file_list = self._get_file_list(files)
        try:
            compiled_pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

        for file_path in file_list:
            old_name = file_path.name
            new_name = compiled_pattern.sub(replacement, old_name)
            if new_name != old_name:
                self._add_rename_operation(file_path, new_name)

    def _get_file_list(self, files: Optional[List[str]]) -> List[Path]:
        """获取文件列表"""
        if files:
            return [self.directory / f for f in files if (self.directory / f).exists()]
        else:
            return [f for f in self.directory.iterdir() if f.is_file()]

    def _add_rename_operation(self, file_path: Path, new_name: str):
        """添加重命名操作"""
        if new_name == file_path.name:
            return

        old_path = file_path
        new_path = file_path.parent / new_name

        # 检查是否冲突
        if new_path.exists() and new_path != old_path:
            print(f"⚠️  Skip: {new_name} already exists")
            return

        self.rename_operations.append((old_path, new_path))

    def execute(self):
        """执行重命名操作"""
        if not self.rename_operations:
            print("No files to rename")
            return

        print(f"\n{'='*60}")
        print(f"{'DRY RUN' if self.dry_run else 'EXECUTE'}: {len(self.rename_operations)} files to rename")
        print(f"{'='*60}\n")

        for old_path, new_path in self.rename_operations:
            print(f"{old_path.name} -> {new_path.name}")

        if self.dry_run:
            print("\n🔍 Dry run complete. No files were renamed.")
        else:
            confirm = input("\nConfirm rename? (y/n): ")
            if confirm.lower() == 'y':
                for old_path, new_path in self.rename_operations:
                    old_path.rename(new_path)
                print(f"✅ Successfully renamed {len(self.rename_operations)} files")
            else:
                print("❌ Cancelled")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="文件重命名工具")
    parser.add_argument("directory", help="目标目录")
    parser.add_argument("--dry-run", action="store_true", help="预览模式,不实际执行")

    # 重命名操作
    subparsers = parser.add_subparsers(dest="operation", help="操作类型")

    # 添加前缀
    prefix_parser = subparsers.add_parser("prefix", help="添加前缀")
    prefix_parser.add_argument("text", help="前缀文本")

    # 添加后缀
    suffix_parser = subparsers.add_parser("suffix", help="添加后缀")
    suffix_parser.add_argument("text", help="后缀文本")

    # 替换文本
    replace_parser = subparsers.add_parser("replace", help="替换文本")
    replace_parser.add_argument("old", help="原文本")
    replace_parser.add_argument("new", help="新文本")

    # 编号重命名
    numbering_parser = subparsers.add_parser("numbering", help="编号重命名")
    numbering_parser.add_argument("pattern", help="命名模式,如 'photo_{}.jpg'")
    numbering_parser.add_argument("--start", type=int, default=1, help="起始数字")
    numbering_parser.add_argument("--digits", type=int, default=3, help="数字位数")
    numbering_parser.add_argument("--sort", choices=["name", "size", "date"], default="name", help="排序方式")

    # 正则重命名
    regex_parser = subparsers.add_parser("regex", help="正则表达式重命名")
    regex_parser.add_argument("pattern", help="正则表达式")
    regex_parser.add_argument("replacement", help="替换文本")

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        return

    renamer = FileRenamer(args.directory, dry_run=args.dry_run)

    # 执行操作
    if args.operation == "prefix":
        renamer.add_prefix(args.text)
    elif args.operation == "suffix":
        renamer.add_suffix(args.text)
    elif args.operation == "replace":
        renamer.replace_text(args.old, args.new)
    elif args.operation == "numbering":
        renamer.rename_with_numbering(args.pattern, args.start, args.digits, sort_by=args.sort)
    elif args.operation == "regex":
        renamer.rename_with_regex(args.pattern, args.replacement)

    renamer.execute()


if __name__ == "__main__":
    main()

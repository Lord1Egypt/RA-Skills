#!/usr/bin/env python3
"""
存档工具
功能：将 `OUTPUT_DIR` 目录下的历史文档文件（.md, .html, .png, manifest.json）移动到 `ARCHIVE_DIR` 目录下

使用方式：
    python archive_outputs.py
    python archive_outputs.py --output-dir /path/to/output --archive-dir /path/to/archive
"""

import argparse
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

def setup_encoding():
    """解决 Windows 下的编码问题"""
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8') # type: ignore
            sys.stderr.reconfigure(encoding='utf-8') # type: ignore
        except Exception:
            pass
    try:
        import io
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

def get_env_var(var_name: str, default: str = "") -> str:
    """从环境变量或 .env 文件中获取配置"""
    value = os.environ.get(var_name)
    if value:
        return value
    
    # 尝试从 .env 文件读取
    env_files = ['.env', 'local/.env']
    for env_file in env_files:
        env_path = Path(__file__).parent.parent / env_file
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f'{var_name}='):
                        return line.split('=', 1)[1].strip()
    
    return default

def normalize_path(path_str: str) -> Path:
    """规范化路径，处理 Windows 和 Unix 路径格式"""
    path_str = path_str.replace('\\', '/')
    if path_str.startswith('~'):
        path_str = str(Path.home()) + path_str[1:]
    return Path(path_str)

def archive_outputs(output_dir: Path, archive_dir: Path, dry_run: bool = False) -> bool:
    """将 `OUTPUT_DIR` 下的历史文档文件移动到 `ARCHIVE_DIR`"""
    
    # 检查输出目录是否存在
    if not output_dir.exists():
        print(f"[ERROR] 输出目录不存在: {output_dir}")
        return False
    
    # 查找需要归档的文件
    extensions = ['.md', '.html', '.png']
    files_to_archive = []
    
    for ext in extensions:
        files_to_archive.extend(output_dir.glob(f'*{ext}'))
    
    # 添加 manifest.json 文件
    manifest_file = output_dir / 'manifest.json'
    if manifest_file.exists():
        files_to_archive.append(manifest_file)
    
    if not files_to_archive:
        print("[INFO] 没有找到需要归档的文件 (.md, .html, .png, manifest.json)")
        return True
    
    # 从 .md 文件名中提取文章标题
    article_title = None
    for file_path in files_to_archive:
        if file_path.suffix == '.md':
            article_title = file_path.stem
            break
    
    if not article_title:
        print("[ERROR] 未找到 .md 文件，无法确定文章标题")
        return False
    
    # 创建归档目录（ARCHIVE_DIR/当前月份/文章标题）
    month_year = datetime.now().strftime('%Y-%m')
    archive_subdir = archive_dir / month_year / article_title
    
    if archive_subdir.exists():
        print(f"[WARNING] 归档目录已存在: {archive_subdir}")
    else:
        if dry_run:
            print(f"[DRY RUN] 将创建目录: {archive_subdir}")
        else:
            archive_subdir.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] 创建归档目录: {archive_subdir}")
    
    # 移动文件
    moved_count = 0
    for file_path in files_to_archive:
        dest_path = archive_subdir / file_path.name
        
        if dest_path.exists():
            print(f"[WARNING] 目标文件已存在，跳过: {dest_path}")
            continue
        
        if dry_run:
            print(f"[DRY RUN] 将移动: {file_path} -> {dest_path}")
        else:
            try:
                if file_path.name == 'manifest.json':
                    dest_path = archive_subdir / f'{article_title}.manifest.json'
                    shutil.move(str(file_path), str(dest_path))
                else:
                    shutil.move(str(file_path), str(dest_path))
                print(f"[OK] 已移动: {file_path.name}")
                moved_count += 1
            except Exception as e:
                print(f"[ERROR] 移动失败 {file_path.name}: {e}")
    
    if dry_run:
        print(f"\n[DRY RUN] 总计将移动 {len(files_to_archive)} 个文件")
    else:
        print(f"\n[OK] 归档完成！共移动 {moved_count} 个文件到: {archive_subdir}")
    
    return True

def main():
    setup_encoding()
    
    parser = argparse.ArgumentParser(description='存档工具 - 归档历史文档文件')
    parser.add_argument('--output-dir', '-o', help='输出目录（默认从环境变量 `OUTPUT_DIR` 读取）')
    parser.add_argument('--archive-dir', '-a', help='存档目录（默认从环境变量 `ARCHIVE_DIR` 读取）')
    parser.add_argument('--dry-run', '-n', action='store_true', help='预览模式，不实际移动文件')
    
    args = parser.parse_args()
    
    # 获取配置
    output_dir_str = args.output_dir or get_env_var('OUTPUT_DIR')
    archive_dir_str = args.archive_dir or get_env_var('ARCHIVE_DIR')

    output_dir = normalize_path(output_dir_str)
    archive_dir = normalize_path(archive_dir_str)

    if not output_dir:
        print("[ERROR] 未指定输出目录，请设置 `OUTPUT_DIR` 环境变量或使用 --output-dir 参数")
        sys.exit(1)
    
    if not archive_dir:
        print("[ERROR] 未指定存档目录，请设置 `ARCHIVE_DIR` 环境变量或使用 --archive-dir 参数")
        sys.exit(1)
        
    print(f"[INFO] 输出目录: {output_dir}")
    print(f"[INFO] 存档目录: {archive_dir}")
    print(f"[INFO] 模式: {'预览（不实际移动）' if args.dry_run else '执行'}")
    print("-" * 50)
    
    success = archive_outputs(output_dir, archive_dir, args.dry_run)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
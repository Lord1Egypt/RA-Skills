#!/usr/bin/env python3
"""
image-optimizer - 图片批量压缩和格式转换工具
支持批量调整大小、压缩质量、转换格式，预览模式和撤销功能！
"""

import os
import sys
import argparse
import shutil
import json
from datetime import datetime
from PIL import Image
from pathlib import Path

VERSION = "1.0.0"
BACKUP_DIR = ".image_optimizer_backup"
LOG_FILE = ".image_optimizer_log.json"

def get_image_files(directory, extensions, recursive=False):
    """获取目录下所有图片文件"""
    image_extensions = {ext.lower() for ext in extensions}
    image_files = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                ext = Path(file).suffix.lower().lstrip('.')
                if ext in image_extensions:
                    image_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                ext = Path(file).suffix.lower().lstrip('.')
                if ext in image_extensions:
                    image_files.append(os.path.join(directory, file))
    
    return sorted(image_files)

def backup_files(files, backup_dir):
    """备份文件"""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_backup_dir = os.path.join(backup_dir, timestamp)
    os.makedirs(session_backup_dir)
    
    backup_map = {}
    for file_path in files:
        rel_path = os.path.relpath(file_path)
        backup_path = os.path.join(session_backup_dir, rel_path)
        backup_subdir = os.path.dirname(backup_path)
        if not os.path.exists(backup_subdir):
            os.makedirs(backup_subdir, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        backup_map[file_path] = backup_path
    
    return session_backup_dir, backup_map

def save_log(session_backup_dir, backup_map, operations):
    """保存操作日志"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "session_backup_dir": session_backup_dir,
        "backup_map": backup_map,
        "operations": operations
    }
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def undo_last_operation():
    """撤销上次操作"""
    if not os.path.exists(LOG_FILE):
        print("❌ 没有找到操作日志，无法撤销")
        return False
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    session_backup_dir = log_data.get("session_backup_dir")
    backup_map = log_data.get("backup_map", {})
    
    if not os.path.exists(session_backup_dir):
        print(f"❌ 备份目录不存在：{session_backup_dir}")
        return False
    
    print(f"🔄 正在撤销上次操作...")
    restored_count = 0
    for original_path, backup_path in backup_map.items():
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            print(f"  ✅ 已恢复：{original_path}")
            restored_count += 1
    
    print(f"\n🎉 撤销完成！共恢复 {restored_count} 个文件")
    return True

def optimize_image(file_path, args, output_dir=None):
    """优化单个图片"""
    try:
        img = Image.open(file_path)
        original_format = img.format
        original_size = os.path.getsize(file_path)
        
        # 计算新尺寸
        new_width, new_height = img.size
        if args.max_width and new_width > args.max_width:
            ratio = args.max_width / new_width
            new_width = args.max_width
            new_height = int(new_height * ratio)
        if args.max_height and new_height > args.max_height:
            ratio = args.max_height / new_height
            new_height = args.max_height
            new_width = int(new_width * ratio)
        if args.max_size:
            max_dim = max(new_width, new_height)
            if max_dim > args.max_size:
                ratio = args.max_size / max_dim
                new_width = int(new_width * ratio)
                new_height = int(new_height * ratio)
        
        # 调整大小
        if (new_width, new_height) != img.size:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 确定输出格式
        output_format = args.format.upper() if args.format else original_format
        if output_format == 'JPG':
            output_format = 'JPEG'
        
        # 确定输出路径
        if output_dir:
            rel_path = os.path.relpath(file_path, args.directory)
            output_path = os.path.join(output_dir, rel_path)
            output_subdir = os.path.dirname(output_path)
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir, exist_ok=True)
        else:
            output_path = file_path
        
        # 修改扩展名（如果格式改变）
        if args.format:
            base, _ = os.path.splitext(output_path)
            ext_map = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}
            output_path = base + ext_map.get(output_format, '.jpg')
        
        # 保存图片
        save_kwargs = {}
        if output_format in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = args.quality or 85
            if output_format == 'JPEG':
                save_kwargs['optimize'] = True
        elif output_format == 'PNG':
            save_kwargs['optimize'] = True
        
        img.save(output_path, format=output_format, **save_kwargs)
        
        new_size = os.path.getsize(output_path)
        size_reduction = (1 - new_size / original_size) * 100 if original_size > 0 else 0
        
        return {
            "success": True,
            "original_size": original_size,
            "new_size": new_size,
            "size_reduction": size_reduction,
            "output_path": output_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(
        description=f"image-optimizer v{VERSION} - 图片批量压缩和格式转换工具"
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="要处理的目录（默认：当前目录）"
    )
    parser.add_argument(
        "--quality", "-q",
        type=int,
        choices=range(1, 101),
        metavar="1-100",
        help="压缩质量 1-100（默认：85）"
    )
    parser.add_argument(
        "--max-width",
        type=int,
        help="最大宽度（像素）"
    )
    parser.add_argument(
        "--max-height",
        type=int,
        help="最大高度（像素）"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        help="最大边长（像素，同时限制宽高）"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["png", "jpeg", "webp"],
        help="输出格式"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="递归处理子文件夹"
    )
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="预览模式，不实际修改文件"
    )
    parser.add_argument(
        "--undo", "-u",
        action="store_true",
        help="撤销上次操作"
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录（不覆盖原文件）"
    )
    parser.add_argument(
        "--extensions",
        default="jpg,jpeg,png,webp",
        help="要处理的文件扩展名，逗号分隔（默认：jpg,jpeg,png,webp）"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"image-optimizer v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # 撤销操作
    if args.undo:
        undo_last_operation()
        return
    
    # 检查是否有操作参数
    has_operation = any([
        args.quality,
        args.max_width,
        args.max_height,
        args.max_size,
        args.format
    ])
    
    if not has_operation:
        print("⚠️  没有指定任何操作，请使用 --quality、--max-width、--max-size 或 --format")
        print("💡 使用 --help 查看所有选项")
        return
    
    # 获取图片文件
    extensions = [ext.strip() for ext in args.extensions.split(',')]
    image_files = get_image_files(args.directory, extensions, args.recursive)
    
    if not image_files:
        print(f"❌ 在目录 '{args.directory}' 中没有找到图片文件")
        return
    
    print(f"🖼️  找到 {len(image_files)} 个图片文件\n")
    
    # 预览模式
    if args.preview:
        print("📋 预览模式 - 以下是将要进行的操作：\n")
        for file_path in image_files:
            print(f"  • {os.path.relpath(file_path)}")
            if args.max_width:
                print(f"    - 最大宽度：{args.max_width}px")
            if args.max_height:
                print(f"    - 最大高度：{args.max_height}px")
            if args.max_size:
                print(f"    - 最大边长：{args.max_size}px")
            if args.quality:
                print(f"    - 压缩质量：{args.quality}")
            if args.format:
                print(f"    - 输出格式：{args.format.upper()}")
            print()
        print("💡 去掉 --preview 参数来执行实际操作")
        return
    
    # 备份文件
    if not args.output_dir:
        print("💾 正在备份原始文件...")
        session_backup_dir, backup_map = backup_files(image_files, BACKUP_DIR)
        print(f"   备份位置：{session_backup_dir}\n")
    else:
        session_backup_dir = None
        backup_map = {}
    
    # 处理图片
    print("🔧 正在处理图片...\n")
    operations = []
    total_original_size = 0
    total_new_size = 0
    success_count = 0
    
    for i, file_path in enumerate(image_files, 1):
        rel_path = os.path.relpath(file_path)
        print(f"[{i}/{len(image_files)}] 处理：{rel_path}")
        
        result = optimize_image(file_path, args, args.output_dir)
        operations.append({
            "file": file_path,
            "result": result
        })
        
        if result["success"]:
            success_count += 1
            total_original_size += result["original_size"]
            total_new_size += result["new_size"]
            reduction = result["size_reduction"]
            output_rel = os.path.relpath(result["output_path"])
            print(f"    ✅ 成功！{reduction:.1f}% 空间节省 → {output_rel}")
        else:
            print(f"    ❌ 失败：{result['error']}")
    
    # 保存日志
    if session_backup_dir:
        save_log(session_backup_dir, backup_map, operations)
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 处理完成！")
    print(f"   成功：{success_count}/{len(image_files)}")
    
    if total_original_size > 0:
        total_reduction = (1 - total_new_size / total_original_size) * 100
        original_mb = total_original_size / (1024 * 1024)
        new_mb = total_new_size / (1024 * 1024)
        saved_mb = original_mb - new_mb
        print(f"   原始大小：{original_mb:.2f} MB")
        print(f"   优化后大小：{new_mb:.2f} MB")
        print(f"   节省空间：{saved_mb:.2f} MB ({total_reduction:.1f}%)")
    
    if session_backup_dir:
        print(f"\n💡 如需撤销，运行：{os.path.basename(__file__)} --undo")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

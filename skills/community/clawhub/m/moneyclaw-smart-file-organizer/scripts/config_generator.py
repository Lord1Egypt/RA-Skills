#!/usr/bin/env python3
"""
配置文件生成器 - 帮助用户创建自定义配置
"""

import json
import argparse
from pathlib import Path

def generate_default_config():
    """生成默认配置"""
    config = {
        "organize": {
            "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".tiff"],
            "document_extensions": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".rtf"],
            "video_extensions": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".m4v", ".webm"],
            "audio_extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"],
            "archive_extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "code_extensions": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".html", ".css", ".json", ".xml", ".yml", ".yaml"],
            "other_folder": "Others",
            "create_subfolders": True,
            "recursive": True
        },
        "rename": {
            "enabled": True,
            "image_pattern": "IMG_{date}_{index}",
            "document_pattern": "DOC_{title}_{date}",
            "video_pattern": "VID_{date}_{index}",
            "audio_pattern": "AUD_{date}_{index}",
            "general_pattern": "FILE_{date}_{index}",
            "date_format": "%Y%m%d",
            "keep_original_date": True
        },
        "deduplicate": {
            "enabled": True,
            "method": "hash",  # hash, name_size, both
            "action": "move",  # delete, move, rename
            "keep": "oldest",  # oldest, newest, largest, smallest
            "duplicates_folder": "Duplicates",
            "similarity_threshold": 0.95
        },
        "safety": {
            "preview_mode": True,
            "backup_before_action": True,
            "backup_folder": "Backup",
            "max_file_size_mb": 1024,
            "skip_system_files": True,
            "skip_hidden_files": True,
            "skip_readonly_files": True,
            "confirm_before_delete": True
        },
        "performance": {
            "max_workers": 4,
            "chunk_size": 8192,
            "use_cache": True,
            "cache_ttl": 3600
        },
        "logging": {
            "enabled": True,
            "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
            "file": "organize_log.txt",
            "max_log_size_mb": 10,
            "backup_count": 5
        }
    }
    return config

def generate_custom_config(output_path, interactive=False):
    """生成自定义配置"""
    config = generate_default_config()
    
    if interactive:
        print("🎛️  智能文件整理助手 - 配置生成向导")
        print("="*50)
        
        # 询问用户偏好
        print("\n1. 文件分类设置")
        print("当前支持的扩展名:")
        for category, exts in config["organize"].items():
            if "extensions" in category:
                print(f"  {category}: {', '.join(exts[:5])}...")
        
        add_ext = input("\n要添加其他扩展名吗？(y/N): ")
        if add_ext.lower() == 'y':
            category = input("添加到哪个分类？(image/document/video/audio/archive/code): ")
            extensions = input("输入扩展名（逗号分隔，如 .heic,.raw）: ").split(",")
            extensions = [ext.strip() for ext in extensions if ext.strip()]
            
            key = f"{category}_extensions"
            if key in config["organize"]:
                config["organize"][key].extend(extensions)
                print(f"✅ 已添加扩展名到 {category}")
        
        print("\n2. 重命名设置")
        rename_enabled = input("启用自动重命名？(Y/n): ")
        if rename_enabled.lower() == 'n':
            config["rename"]["enabled"] = False
        else:
            print("重命名模式:")
            print("  1. 简单模式 (IMG_日期_序号)")
            print("  2. 详细模式 (包含标题)")
            print("  3. 自定义模式")
            choice = input("选择模式 (1/2/3, 默认1): ") or "1"
            
            if choice == "2":
                config["rename"]["image_pattern"] = "IMG_{date}_{title}_{index}"
                config["rename"]["document_pattern"] = "DOC_{title}_{date}_{author}"
            elif choice == "3":
                custom_pattern = input("输入自定义模式（可用变量: {date}, {title}, {index}）: ")
                if custom_pattern:
                    config["rename"]["general_pattern"] = custom_pattern
        
        print("\n3. 安全设置")
        preview = input("默认启用预览模式？(Y/n): ")
        if preview.lower() == 'n':
            config["safety"]["preview_mode"] = False
        
        backup = input("启用操作前备份？(Y/n): ")
        if backup.lower() == 'n':
            config["safety"]["backup_before_action"] = False
    
    # 保存配置
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 配置文件已生成: {output_path}")
    print(f"📋 配置摘要:")
    print(f"  文件分类: {len(config['organize'])}个分类规则")
    print(f"  重命名: {'启用' if config['rename']['enabled'] else '禁用'}")
    print(f"  重复检测: {'启用' if config['deduplicate']['enabled'] else '禁用'}")
    print(f"  安全模式: {'预览模式' if config['safety']['preview_mode'] else '直接操作'}")
    
    return config

def validate_config(config_path):
    """验证配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ["organize", "rename", "deduplicate", "safety"]
        for section in required_sections:
            if section not in config:
                print(f"❌ 缺少必要配置节: {section}")
                return False
        
        print(f"✅ 配置文件验证通过: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件验证失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="配置文件生成器")
    parser.add_argument("action", choices=["generate", "validate"], help="操作类型")
    parser.add_argument("--output", default="organize_config.json", help="输出配置文件路径")
    parser.add_argument("--input", help="输入配置文件路径（用于验证）")
    parser.add_argument("--interactive", action="store_true", help="交互式生成")
    
    args = parser.parse_args()
    
    if args.action == "generate":
        generate_custom_config(args.output, args.interactive)
    elif args.action == "validate":
        if not args.input:
            print("❌ 验证需要指定输入文件: --input <config_file>")
            return
        validate_config(args.input)

if __name__ == "__main__":
    main()
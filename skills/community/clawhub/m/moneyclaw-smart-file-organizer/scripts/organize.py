#!/usr/bin/env python3
"""
智能文件整理助手 - 主脚本
"""

import os
import shutil
import hashlib
from pathlib import Path
import argparse
import json
from datetime import datetime
import mimetypes
from collections import defaultdict
import sys

class SmartFileOrganizer:
    def __init__(self, config_path=None):
        # 默认配置
        self.config = {
            "organize": {
                "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
                "document_extensions": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
                "video_extensions": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".m4v"],
                "audio_extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
                "archive_extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                "code_extensions": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json", ".xml"],
                "other_folder": "Others"
            },
            "rename": {
                "enabled": True,
                "image_pattern": "IMG_{date}_{index}",
                "document_pattern": "DOC_{title}_{date}",
                "general_pattern": "FILE_{date}_{index}",
                "date_format": "%Y%m%d"
            },
            "deduplicate": {
                "enabled": False,
                "method": "hash",  # hash, name_size, both
                "action": "delete",  # delete, move, rename
                "keep": "oldest"  # oldest, newest, largest, smallest
            },
            "safety": {
                "preview_mode": False,
                "backup_before_action": True,
                "max_file_size_mb": 1000,
                "skip_system_files": True,
                "skip_hidden_files": True
            }
        }
        
        # 加载自定义配置
        self.config_loaded = self._load_config(config_path)
    
    def _load_config(self, config_path):
        """加载配置文件"""
        if not config_path:
            return True
        
        config_file = Path(config_path)
        if not config_file.exists():
            print(f"❌ 配置文件不存在: {config_path}")
            print(f"💡 提示: 使用 --config 指定有效的配置文件路径")
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self._deep_update(self.config, user_config)
            print(f"✅ 配置文件加载成功: {config_path}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {config_path}")
            print(f"💡 错误详情: {e}")
            print(f"💡 提示: 请检查JSON格式是否正确")
            return False
        except Exception as e:
            print(f"❌ 配置文件读取失败: {config_path}")
            print(f"💡 错误详情: {e}")
            return False
        
        # 初始化统计
        self.stats = {
            "total_files": 0,
            "organized_files": 0,
            "renamed_files": 0,
            "duplicates_found": 0,
            "duplicates_removed": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # 操作日志
        self.log = []
    
    def _deep_update(self, original, update):
        """深度更新字典"""
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value
    
    def get_file_category(self, filepath):
        """获取文件分类"""
        path = Path(filepath)
        suffix = path.suffix.lower()
        
        # 按扩展名分类
        if suffix in self.config["organize"]["image_extensions"]:
            return "Images"
        elif suffix in self.config["organize"]["document_extensions"]:
            return "Documents"
        elif suffix in self.config["organize"]["video_extensions"]:
            return "Videos"
        elif suffix in self.config["organize"]["audio_extensions"]:
            return "Audio"
        elif suffix in self.config["organize"]["archive_extensions"]:
            return "Archives"
        elif suffix in self.config["organize"]["code_extensions"]:
            return "Code"
        else:
            return self.config["organize"]["other_folder"]
    
    def generate_new_filename(self, filepath, category, index=1):
        """生成新文件名"""
        path = Path(filepath)
        stat = path.stat()
        
        # 获取文件信息
        created_date = datetime.fromtimestamp(stat.st_ctime).strftime(
            self.config["rename"]["date_format"]
        )
        modified_date = datetime.fromtimestamp(stat.st_mtime).strftime(
            self.config["rename"]["date_format"]
        )
        
        # 选择命名模式
        if category == "Images":
            pattern = self.config["rename"]["image_pattern"]
        elif category == "Documents":
            pattern = self.config["rename"]["document_pattern"]
            # 尝试提取文档标题（从文件名）
            title = self._extract_title_from_filename(path.stem)
        else:
            pattern = self.config["rename"]["general_pattern"]
        
        # 替换模板变量
        new_name = pattern
        new_name = new_name.replace("{date}", created_date)
        new_name = new_name.replace("{modified}", modified_date)
        new_name = new_name.replace("{index}", f"{index:03d}")
        
        if category == "Documents" and "{title}" in pattern:
            new_name = new_name.replace("{title}", title[:30])  # 限制标题长度
        
        # 添加扩展名
        new_name += path.suffix
        
        return new_name
    
    def calculate_file_hash(self, filepath, chunk_size=8192):
        """计算文件哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.log_error(f"计算哈希失败 {filepath}: {e}")
            return None
    
    def is_duplicate(self, filepath, file_info, method="hash"):
        """检查是否为重复文件"""
        if method == "hash":
            file_hash = self.calculate_file_hash(filepath)
            if file_hash and file_hash in file_info["hashes"]:
                return True, file_hash
        elif method == "name_size":
            file_size = Path(filepath).stat().st_size
            file_name = Path(filepath).name
            key = f"{file_name}_{file_size}"
            if key in file_info["name_size"]:
                return True, key
        elif method == "both":
            # 先检查名称和大小，再检查哈希
            file_size = Path(filepath).stat().st_size
            file_name = Path(filepath).name
            name_size_key = f"{file_name}_{file_size}"
            
            if name_size_key in file_info["name_size"]:
                # 名称和大小相同，检查哈希确认
                file_hash = self.calculate_file_hash(filepath)
                if file_hash and file_hash in file_info["hashes"]:
                    return True, f"{name_size_key}_{file_hash}"
        
        return False, None
    
    def organize_directory(self, directory_path, rename=False, deduplicate=False, preview=False):
        """整理目录"""
        try:
            dir_path = Path(directory_path).resolve()
        except Exception as e:
            self.log_error(f"路径解析失败: {directory_path} - {e}")
            return False
        
        if not dir_path.exists():
            self.log_error(f"目录不存在: {dir_path}")
            print(f"💡 提示: 请检查路径是否正确，或使用绝对路径")
            return False
        
        if not dir_path.is_dir():
            self.log_error(f"路径不是目录: {dir_path}")
            print(f"💡 提示: 请指定目录路径，而不是文件路径")
            return False
        
        print(f"📁 开始整理目录: {dir_path}")
        print(f"⚙️  模式: {'预览' if preview else '实际操作'}")
        if rename:
            print(f"📝 重命名: 启用")
        if deduplicate:
            print(f"🔍 重复检测: 启用")
        print("-" * 50)
        
        # 收集文件信息用于重复检测
        file_info = {
            "hashes": set(),
            "name_size": set(),
            "files_by_hash": defaultdict(list),
            "files_by_name_size": defaultdict(list)
        }
        
        # 遍历目录
        organized_count = 0
        for item in dir_path.rglob("*"):
            # 跳过目录
            if item.is_dir():
                continue
            
            # 安全检查
            if not self._is_file_safe(item):
                continue
            
            self.stats["total_files"] += 1
            
            try:
                # 获取文件分类
                category = self.get_file_category(item)
                
                # 创建分类目录
                category_dir = dir_path / category
                if not preview:
                    category_dir.mkdir(exist_ok=True)
                
                # 检查重复文件
                is_dup = False
                dup_key = None
                if deduplicate:
                    is_dup, dup_key = self.is_duplicate(
                        item, 
                        file_info, 
                        self.config["deduplicate"]["method"]
                    )
                
                if is_dup:
                    self.stats["duplicates_found"] += 1
                    self.log_operation(f"发现重复文件: {item.name}")
                    
                    # 处理重复文件
                    if not preview and self.config["deduplicate"]["action"] == "delete":
                        item.unlink()
                        self.stats["duplicates_removed"] += 1
                        self.log_operation(f"删除重复文件: {item.name}")
                    elif not preview and self.config["deduplicate"]["action"] == "move":
                        dup_dir = dir_path / "Duplicates"
                        dup_dir.mkdir(exist_ok=True)
                        shutil.move(str(item), str(dup_dir / item.name))
                        self.log_operation(f"移动重复文件到: Duplicates/{item.name}")
                    
                    continue
                
                # 记录文件信息（用于后续重复检测）
                if deduplicate:
                    file_hash = self.calculate_file_hash(item)
                    if file_hash:
                        file_info["hashes"].add(file_hash)
                        file_info["files_by_hash"][file_hash].append(str(item))
                    
                    file_size = item.stat().st_size
                    name_size_key = f"{item.name}_{file_size}"
                    file_info["name_size"].add(name_size_key)
                    file_info["files_by_name_size"][name_size_key].append(str(item))
                
                # 生成新文件名
                new_filename = item.name
                if rename and self.config["rename"]["enabled"]:
                    new_filename = self.generate_new_filename(item, category, organized_count + 1)
                    self.stats["renamed_files"] += 1
                
                # 目标路径
                target_path = category_dir / new_filename
                
                # 处理文件名冲突
                counter = 1
                while target_path.exists():
                    stem = target_path.stem
                    if "_copy" in stem:
                        stem = stem.rsplit("_copy", 1)[0]
                    new_filename = f"{stem}_copy{counter}{target_path.suffix}"
                    target_path = category_dir / new_filename
                    counter += 1
                
                # 执行操作
                if preview:
                    self.log_operation(f"[预览] 移动: {item.name} → {category}/{new_filename}")
                else:
                    # 备份原文件（如果启用）
                    if self.config["safety"]["backup_before_action"]:
                        backup_dir = dir_path / "Backup"
                        backup_dir.mkdir(exist_ok=True)
                        backup_path = backup_dir / item.name
                        shutil.copy2(str(item), str(backup_path))
                    
                    # 移动文件
                    shutil.move(str(item), str(target_path))
                    self.log_operation(f"移动: {item.name} → {category}/{new_filename}")
                    self.stats["organized_files"] += 1
                    organized_count += 1
                
            except Exception as e:
                self.stats["errors"] += 1
                self.log_error(f"处理文件失败 {item}: {e}")
        
        return True
    
    def _is_file_safe(self, filepath):
        """安全检查"""
        path = Path(filepath)
        
        # 跳过备份目录中的文件
        if "Backup" in path.parts:
            return False
        
        # 跳过系统文件
        if self.config["safety"]["skip_system_files"]:
            system_patterns = [".DS_Store", "Thumbs.db", "desktop.ini"]
            if any(path.name.lower() == pattern.lower() for pattern in system_patterns):
                return False
        
        # 跳过隐藏文件
        if self.config["safety"]["skip_hidden_files"] and path.name.startswith("."):
            return False
        
        # 检查文件大小
        try:
            file_size_mb = path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.config["safety"]["max_file_size_mb"]:
                self.log_operation(f"跳过大文件: {path.name} ({file_size_mb:.1f}MB)")
                return False
        except:
            pass
        
        return True
    
    def log_operation(self, message):
        """记录操作日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(f"  {log_entry}")
    
    def _extract_title_from_filename(self, filename):
        """从文件名提取标题"""
        # 移除常见前缀和后缀
        prefixes = ["copy", "副本", "new", "latest", "final", "draft"]
        suffixes = ["v1", "v2", "version", "old", "new", "temp"]
        
        title = filename
        # 移除数字序列
        import re
        title = re.sub(r'\d+', '', title)
        # 移除特殊字符
        title = re.sub(r'[_-]+', ' ', title)
        # 移除常见前后缀
        words = title.lower().split()
        words = [w for w in words if w not in prefixes + suffixes]
        title = ' '.join(words)
        # 首字母大写
        title = title.title()
        
        return title if title.strip() else "Document"
    
    def log_error(self, message):
        """记录错误日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] ❌ {message}"
        self.log.append(log_entry)
        print(f"  {log_entry}")
    
    def print_summary(self):
        """打印总结"""
        print("\n" + "="*50)
        print("📊 整理完成总结")
        print("="*50)
        print(f"📁 总文件数: {self.stats['total_files']}")
        print(f"✅ 整理文件: {self.stats['organized_files']}")
        print(f"📝 重命名文件: {self.stats['renamed_files']}")
        print(f"🔍 发现重复: {self.stats['duplicates_found']}")
        print(f"🗑️  移除重复: {self.stats['duplicates_removed']}")
        print(f"❌ 错误数: {self.stats['errors']}")
        print(f"⏰ 开始时间: {self.stats['start_time']}")
        print(f"⏰ 结束时间: {datetime.now().isoformat()}")
        
        if self.log:
            print(f"\n📋 操作日志 ({len(self.log)}条):")
            for entry in self.log[-10:]:  # 显示最后10条
                print(f"  {entry}")
        
        # 保存日志文件
        log_file = Path.cwd() / f"organize_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.log))
            f.write(f"\n\n{'-'*40}\n")
            f.write("整理统计:\n")
            for key, value in self.stats.items():
                f.write(f"{key}: {value}\n")
        
        print(f"\n📄 详细日志已保存: {log_file}")

def main():
    parser = argparse.ArgumentParser(description="智能文件整理助手")
    parser.add_argument("--path", default=".", help="要整理的目录路径")
    parser.add_argument("--rename", action="store_true", help="启用重命名")
    parser.add_argument("--deduplicate", action="store_true", help="启用重复检测")
    parser.add_argument("--preview", action="store_true", help="预览模式（不实际操作）")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--types", help="只处理指定类型的文件（逗号分隔）")
    
    args = parser.parse_args()
    
    # 初始化整理器
    organizer = SmartFileOrganizer(args.config)
    
    # 如果配置文件加载失败，退出
    if args.config and not organizer.config_loaded:
        print("❌ 配置文件加载失败，程序退出")
        return
    
    # 更新配置
    if args.preview:
        organizer.config["safety"]["preview_mode"] = True
    
    # 执行整理
    success = organizer.organize_directory(
        directory_path=args.path,
        rename=args.rename,
        deduplicate=args.deduplicate,
        preview=args.preview or organizer.config["safety"]["preview_mode"]
    )
    
    if success:
        organizer.print_summary()
        
        if args.preview or organizer.config["safety"]["preview_mode"]:
            print("\n💡 这是预览模式，没有实际执行操作。")
            print("   要实际执行，请移除 --preview 参数。")
    else:
        print("❌ 整理失败，请检查错误信息。")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 双重清理系统 v2.0.0
修复OpenClaw惰性删除问题：索引清理 + 物理文件清理
Python跨平台版本（支持Windows/Linux/macOS）

功能：
1. 执行OpenClaw会话索引清理
2. 手动清理物理文件（修复OpenClaw惰性删除问题）
3. 提供预览、强制、交互式三种模式
4. 详细的清理报告和进度显示

用法：
  python clean-sessions-dual.py                  # 交互式清理
  python clean-sessions-dual.py --force          # 强制执行
  python clean-sessions-dual.py --dry-run        # 预览模式
  python clean-sessions-dual.py --hours 24       # 清理24小时前的文件
"""

import os
import sys
import json
import time
import shutil
import argparse
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path

# 版本信息
VERSION = "2.0.0"
SKILL_NAME = "OpenClaw Dual Cleanup"
AUTHOR = "Luohan (AI Assistant)"
CREATED_DATE = "2026-03-29"
GITHUB_URL = "https://github.com/yourusername/openclaw-dual-cleanup"

class DualCleanupManager:
    """双重清理管理器"""
    
    def __init__(self, args):
        self.args = args
        self.start_time = datetime.now()
        self.stats = {
            "index_cleaned": False,
            "physical_deleted": 0,
            "physical_total_bytes": 0,
            "cache_deleted": 0,
            "cache_total_bytes": 0
        }
        
        # 确定系统类型
        self.system = platform.system()
        self.is_windows = (self.system == "Windows")
        self.home_dir = Path.home()
        
    def print_header(self):
        """打印头部信息"""
        print(f"====== {SKILL_NAME} v{VERSION} ======")
        print(f"🚀 修复OpenClaw惰性删除问题 (索引清理 + 物理文件清理)")
        print(f"📅 执行时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 模式: {self.args.mode}, 清理时长: {self.args.hours}小时前")
        print(f"💻 系统: {self.system} | 编码: UTF-8")
        print()
    
    def print_step(self, step_num, title):
        """打印步骤标题"""
        print(f"🔧 步骤{step_num}: {title}")
    
    def check_openclaw_available(self):
        """检查OpenClaw是否可用"""
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            return False
    
    def run_openclaw_command(self, cmd, show_output=True):
        """运行OpenClaw命令"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if show_output and result.stdout.strip():
                print(f"    [OpenClaw] {result.stdout}")
            
            if result.stderr.strip():
                print(f"    [!] {result.stderr}")
            
            return result.returncode == 0
        except Exception as e:
            print(f"    [✗] 执行OpenClaw命令失败: {e}")
            return False
    
    def step1_index_cleanup(self):
        """第一步：OpenClaw索引清理"""
        self.print_step(1, "OpenClaw会话索引清理")
        
        if not self.check_openclaw_available():
            print("    [!] OpenClaw未找到或不可用，跳过索引清理")
            return False
        
        if self.args.mode == "dry-run":
            print("    [预览] 将执行: openclaw sessions cleanup --dry-run")
            self.run_openclaw_command(["openclaw", "sessions", "cleanup", "--dry-run"])
            return True
        
        # 交互式模式需要确认
        if self.args.mode == "interactive":
            print(f"    [!] 将清理{self.args.hours}小时前的会话索引")
            response = input("    确认执行? (y/N): ").strip().lower()
            if response != 'y':
                print("    [!] 用户取消索引清理")
                return False
        
        print("    [..] 执行OpenClaw索引清理...")
        success = self.run_openclaw_command(["openclaw", "sessions", "cleanup", "--enforce", "--fix-missing"])
        
        if success:
            self.stats["index_cleaned"] = True
            print("    [✓] 索引清理完成")
        else:
            print("    [✗] 索引清理失败")
        
        return success
    
    def find_openclaw_directories(self):
        """查找所有可能的OpenClaw目录"""
        directories = []
        
        # Windows特定路径
        if self.is_windows:
            appdata = os.environ.get("APPDATA", "")
            if appdata:
                directories.extend([
                    Path(appdata) / ".openclaw",
                    Path(appdata) / "openclaw"
                ])
        
        # 跨平台路径
        directories.extend([
            self.home_dir / ".openclaw",
            self.home_dir / "Library" / "Application Support" / "openclaw",  # macOS
            self.home_dir / ".config" / "openclaw",  # Linux
            self.home_dir / ".local" / "share" / "openclaw"  # Linux
        ])
        
        # 过滤实际存在的目录
        existing_dirs = [str(d) for d in directories if d.exists()]
        return existing_dirs
    
    def is_session_file(self, filepath):
        """判断是否为会话文件"""
        path_str = str(filepath).lower()
        
        # 检查扩展名和命名模式
        is_jsonl = path_str.endswith(".jsonl")
        has_uuid_pattern = any(keyword in path_str for keyword in [
            "session", "cron", "tui", "agent", "subagent"
        ])
        
        return is_jsonl or has_uuid_pattern
    
    def step2_physical_file_cleanup(self):
        """第二步：物理文件清理（修复惰性删除问题）"""
        self.print_step(2, "物理文件清理（修复惰性删除问题）")
        
        # 查找目录
        openclaw_dirs = self.find_openclaw_directories()
        if not openclaw_dirs:
            print("    [!] 未找到OpenClaw目录")
            return False
        
        print(f"    [?] 查找路径 ({len(openclaw_dirs)}个):")
        for dir_path in openclaw_dirs:
            print(f"      - {dir_path}")
        
        # 计算时间阈值
        threshold_time = datetime.now() - timedelta(hours=self.args.hours)
        
        # 搜索文件
        found_files = []
        total_size = 0
        
        for dir_path in openclaw_dirs:
            try:
                for root, dirs, files in os.walk(dir_path):
                    for filename in files:
                        filepath = Path(root) / filename
                        
                        # 判断是否为会话文件
                        if not self.is_session_file(filepath):
                            continue
                        
                        # 检查文件修改时间
                        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                        if mtime < threshold_time:
                            found_files.append({
                                "path": filepath,
                                "size": filepath.stat().st_size,
                                "mtime": mtime,
                                "age_hours": (datetime.now() - mtime).total_seconds() / 3600
                            })
                            total_size += filepath.stat().st_size
            except Exception as e:
                print(f"      [!] 无法访问 {dir_path}: {e}")
        
        # 显示结果
        if not found_files:
            print("    [✓] 未找到需要清理的物理文件")
            return True
        
        total_size_mb = round(total_size / (1024 * 1024), 2)
        print(f"    [?] 找到 {len(found_files)} 个物理文件可清理 (总计约{total_size_mb}MB):")
        
        # 显示文件详情
        for i, file_info in enumerate(found_files[:10], 1):  # 最多显示10个
            size_kb = round(file_info["size"] / 1024, 2)
            age_hours = round(file_info["age_hours"], 1)
            relative_path = str(file_info["path"]).replace(str(self.home_dir), "~")
            print(f"      - {file_info['path'].name} ({size_kb}KB, {age_hours}小时前)")
            if i == 10 and len(found_files) > 10:
                print(f"      ... 还有 {len(found_files) - 10} 个文件")
                break
        
        print()
        
        # 预览模式 - 不执行删除
        if self.args.mode == "dry-run":
            print("    [预览] 找到文件但不执行删除")
            return True
        
        # 获取确认
        if self.args.mode == "interactive":
            print(f"    [!] 确认删除以上 {len(found_files)} 个物理文件? (y/N): ", end="")
            response = input().strip().lower()
            if response != 'y':
                print("    [!] 用户取消物理文件清理")
                return False
        
        # 执行删除
        print("    [..] 正在删除物理文件...")
        deleted_count = 0
        freed_size_mb = 0
        
        for file_info in found_files:
            try:
                file_info["path"].unlink()  # 删除文件
                deleted_count += 1
                freed_size_mb += round(file_info["size"] / (1024 * 1024), 2)
                print(f"      [✓] 删除: {file_info['path'].name}")
            except Exception as e:
                print(f"      [✗] 删除失败 {file_info['path'].name}: {e}")
        
        # 更新统计
        self.stats["physical_deleted"] = deleted_count
        self.stats["physical_total_bytes"] = total_size
        
        if deleted_count > 0:
            print(f"    [✓] 物理文件清理完成:")
            print(f"        删除文件数: {deleted_count} 个")
            freed_rounded = round(freed_size_mb, 2)
            print(f"        释放空间: {freed_rounded}MB")
            return True
        else:
            print("    [✗] 物理文件清理失败")
            return False
    
    def step3_cache_cleanup(self):
        """第三步：缓存清理"""
        self.print_step(3, "检查缓存文件")
        
        # 查找缓存目录
        cache_path = self.home_dir / ".openclaw" / "cache"
        if not cache_path.exists():
            print("    [✓] 缓存目录不存在")
            return True
        
        # 计算时间阈值（默认24小时）
        cache_threshold = datetime.now() - timedelta(hours=24)
        
        try:
            cache_files = []
            for item in cache_path.rglob("*"):
                if item.is_file():
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if mtime < cache_threshold:
                        cache_files.append({
                            "path": item,
                            "size": item.stat().st_size,
                            "mtime": mtime
                        })
            
            if not cache_files:
                print("    [✓] 缓存目录干净")
                return True
            
            total_cache_mb = round(sum(f["size"] for f in cache_files) / (1024 * 1024), 2)
            print(f"    [?] 找到 {len(cache_files)} 个可清理缓存文件 ({total_cache_mb}MB)")
            
            # 预览模式 - 不执行清理
            if self.args.mode == "dry-run":
                print("    [预览] 不清理缓存")
                return True
            
            # 强制模式 - 直接清理
            if self.args.mode == "force":
                deleted_cache = 0
                for file_info in cache_files:
                    try:
                        file_info["path"].unlink()
                        deleted_cache += 1
                    except:
                        pass
                
                if deleted_cache > 0:
                    self.stats["cache_deleted"] = deleted_cache
                    self.stats["cache_total_bytes"] = sum(f["size"] for f in cache_files[:deleted_cache])
                    print(f"    [✓] 强制清理{deleted_cache}个缓存文件")
                    return True
            
            # 交互模式 - 询问是否清理
            if self.args.mode == "interactive":
                print(f"    [!] 是否清理{len(cache_files)}个缓存文件? (y/N): ", end="")
                response = input().strip().lower()
                if response == 'y':
                    deleted_cache = 0
                    for file_info in cache_files:
                        try:
                            file_info["path"].unlink()
                            deleted_cache += 1
                        except:
                            pass
                    
                    if deleted_cache > 0:
                        self.stats["cache_deleted"] = deleted_cache
                        self.stats["cache_total_bytes"] = sum(f["size"] for f in cache_files[:deleted_cache])
                        print(f"    [✓] 清理{deleted_cache}个缓存文件")
                        return True
            
            return True
            
        except Exception as e:
            print(f"    [✗] 缓存清理失败: {e}")
            return False
    
    def generate_report(self):
        """生成清理报告"""
        print()
        print("====== 清理完成报告 ======")
        print(f"📊 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  耗时: {(datetime.now() - self.start_time).total_seconds():.1f}秒")
        print()
        
        # 索引清理结果
        if self.stats["index_cleaned"]:
            print("✅ OpenClaw索引清理: 已完成")
        else:
            print("⚠️  OpenClaw索引清理: 跳过或失败")
        
        # 物理文件清理结果
        if self.stats["physical_deleted"] > 0:
            freed_mb = round(self.stats["physical_total_bytes"] / (1024 * 1024), 2)
            print(f"✅ 物理文件清理: 删除 {self.stats['physical_deleted']} 个文件, 释放 {freed_mb}MB")
        else:
            print("ℹ️  物理文件清理: 未找到可清理文件")
        
        # 缓存清理结果
        if self.stats["cache_deleted"] > 0:
            cache_freed_mb = round(self.stats["cache_total_bytes"] / (1024 * 1024), 2)
            print(f"✅ 缓存清理: 删除 {self.stats['cache_deleted']} 个文件, 释放 {cache_freed_mb}MB")
        
        print()
        print("🎯 双重清理机制总结:")
        print("  1. ✅ 索引清理: 解决OpenClaw会话索引过时问题")
        print("  2. ✅ 物理文件清理: 修复OpenClaw惰性删除缺陷")
        print("  3. ✅ 缓存清理: 优化系统性能")
        print()
        print(f"📚 技能仓库: {GITHUB_URL}")
        print(f"🆔 版本: {VERSION} | 作者: {AUTHOR}")
    
    def run(self):
        """执行完整的双重清理流程"""
        self.print_header()
        
        try:
            # 执行三个步骤
            step1_success = self.step1_index_cleanup()
            print()
            
            step2_success = self.step2_physical_file_cleanup()
            print()
            
            step3_success = self.step3_cache_cleanup()
            
            # 生成报告
            self.generate_report()
            
            # 返回退出代码
            if self.stats["physical_deleted"] > 0 or self.stats["index_cleaned"]:
                return 0  # 执行了清理
            else:
                return 1  # 未执行清理
            
        except KeyboardInterrupt:
            print("\n\n[!] 用户中断清理")
            return 130
        except Exception as e:
            print(f"\n[✗] 清理过程发生错误: {e}")
            import traceback
            traceback.print_exc()
            return 255

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description=f"{SKILL_NAME} v{VERSION} - 修复OpenClaw惰性删除问题",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
使用示例:
  python {sys.argv[0]}                   # 交互式清理 (默认)
  python {sys.argv[0]} --force          # 强制执行，不询问确认
  python {sys.argv[0]} --dry-run        # 预览模式，不实际删除
  python {sys.argv[0]} --hours 72       # 清理72小时前文件
  python {sys.argv[0]} --version        # 显示版本信息

维护: {AUTHOR} | 版本: {VERSION}
       """
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["interactive", "force", "dry-run"],
        default="interactive",
        help="清理模式: interactive(交互式), force(强制), dry-run(预览)"
    )
    
    parser.add_argument(
        "--hours", "-t",
        type=int,
        default=12,
        help="清理多少小时前的文件 (默认: 12小时)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="显示版本信息"
    )
    
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        print(f"{SKILL_NAME} v{VERSION}")
        print(f"创建时间: {CREATED_DATE}")
        print(f"作者: {AUTHOR}")
        print(f"GitHub: {GITHUB_URL}")
        return 0
    
    # 验证参数
    if args.hours <= 0:
        print("[✗] 错误: 清理时长必须大于0小时")
        return 1
    
    # 运行清理管理器
    manager = DualCleanupManager(args)
    return manager.run()

if __name__ == "__main__":
    sys.exit(main())
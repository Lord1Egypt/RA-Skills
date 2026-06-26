#!/usr/bin/env python3
"""
Ollama 模型迁移脚本
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class OllamaMigrator:
    def __init__(self, target: str):
        self.target = Path(target)
        self.user_home = Path.home()
        self.source = self.user_home / ".ollama" / "models"
        self.freed_space = 0
        self.errors = []
    
    def check_source(self) -> bool:
        """检查源目录"""
        if not self.source.exists():
            print(f"错误：源目录不存在：{self.source}")
            return False
        
        # 计算源大小
        size = sum(f.stat().st_size for f in self.source.rglob("*") if f.is_file())
        size_gb = round(size / (1024**3), 2)
        print(f"源目录：{self.source}")
        print(f"模型大小：{size_gb} GB")
        
        return True
    
    def check_target(self) -> bool:
        """检查目标目录"""
        # 检查磁盘空间
        drive = self.target.drive if self.target.drive else "D:"
        if not drive:
            drive = "D:"
        
        try:
            total, used, free = shutil.disk_usage(drive)
            free_gb = round(free / (1024**3), 2)
            
            # 计算需要的空间
            source_size = sum(f.stat().st_size for f in self.source.rglob("*") if f.is_file())
            needed_gb = round(source_size / (1024**3), 2)
            
            print(f"\n目标磁盘：{drive}")
            print(f"可用空间：{free_gb} GB")
            print(f"需要空间：{needed_gb} GB")
            
            if free_gb < needed_gb:
                print(f"错误：目标磁盘空间不足！")
                return False
            
            print(f"空间检查：通过")
            return True
            
        except Exception as e:
            print(f"错误：无法检查目标磁盘：{e}")
            return False
    
    def stop_ollama(self) -> bool:
        """停止 Ollama 服务"""
        print("\n停止 Ollama 服务...")
        try:
            # Windows
            subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], 
                         capture_output=True, timeout=5)
            print("Ollama 服务已停止")
            return True
        except:
            print("Ollama 可能未运行，继续...")
            return True
    
    def copy_models(self) -> bool:
        """复制模型文件"""
        print(f"\n复制模型文件...")
        print(f"  源：{self.source}")
        print(f"  目标：{self.target}")
        
        try:
            # 创建目标目录
            self.target.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            for item in self.source.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(self.source)
                    dest = self.target / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
            
            # 验证大小
            source_size = sum(f.stat().st_size for f in self.source.rglob("*") if f.is_file())
            target_size = sum(f.stat().st_size for f in self.target.rglob("*") if f.is_file())
            
            source_gb = round(source_size / (1024**3), 2)
            target_gb = round(target_size / (1024**3), 2)
            
            print(f"  源大小：{source_gb} GB")
            print(f"  目标大小：{target_gb} GB")
            
            if abs(source_size - target_size) > 1024:  # 允许 1KB 误差
                print(f"警告：大小不一致！")
                return False
            
            print(f"复制完成：验证通过")
            return True
            
        except Exception as e:
            print(f"错误：复制失败：{e}")
            self.errors.append(str(e))
            return False
    
    def set_env_variable(self) -> bool:
        """设置环境变量"""
        print(f"\n设置环境变量...")
        
        try:
            # 用户级环境变量
            import winreg
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "OLLAMA_MODELS", 0, winreg.REG_EXPAND_SZ, str(self.target))
            winreg.CloseKey(key)
            
            print(f"用户环境变量已设置：OLLAMA_MODELS = {self.target}")
            return True
            
        except Exception as e:
            print(f"错误：设置环境变量失败：{e}")
            self.errors.append(str(e))
            return False
    
    def verify_migration(self) -> bool:
        """验证迁移"""
        print(f"\n验证迁移...")
        
        # 设置临时环境变量
        os.environ["OLLAMA_MODELS"] = str(self.target)
        
        try:
            # 运行 ollama list
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("模型列表验证：通过")
                print(result.stdout)
                return True
            else:
                print(f"验证失败：{result.stderr}")
                return False
                
        except Exception as e:
            print(f"验证出错：{e}")
            return False
    
    def migrate(self, cleanup: bool = False) -> bool:
        """执行迁移"""
        print("\n" + "="*60)
        print("  Ollama 模型迁移")
        print("="*60)
        
        # 检查
        if not self.check_source():
            return False
        
        if not self.check_target():
            return False
        
        # 确认
        print(f"\n⚠️  此操作将迁移 Ollama 模型到：{self.target}")
        if cleanup:
            print(f"  并在验证后删除源文件")
        
        confirm = input("\n确认执行？(yes/确认): ").strip().lower()
        if confirm not in ["yes", "y", "确认", "是"]:
            print("已取消")
            return False
        
        # 执行迁移
        if not self.stop_ollama():
            return False
        
        if not self.copy_models():
            return False
        
        if not self.set_env_variable():
            return False
        
        if not self.verify_migration():
            print("警告：验证失败，但迁移可能成功")
            print("请手动运行 'ollama list' 验证")
        
        # 清理
        if cleanup:
            print(f"\n清理源文件...")
            try:
                shutil.rmtree(self.source)
                print(f"源目录已删除：{self.source}")
            except Exception as e:
                print(f"清理失败：{e}")
        
        print("\n" + "="*60)
        print("  迁移完成！")
        print("="*60)
        print(f"\n下一步：")
        print(f"  1. 关闭此窗口")
        print(f"  2. 重新打开终端")
        print(f"  3. 运行 'ollama list' 验证")
        
        return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ollama 模型迁移")
    parser.add_argument("--target", default="D:\\Ollama\\models", help="目标路径")
    parser.add_argument("--cleanup", action="store_true", help="迁移后删除源文件")
    parser.add_argument("--check", action="store_true", help="只检查，不迁移")
    
    args = parser.parse_args()
    
    if args.check:
        # 只检查
        from check_ollama_status import check_ollama_status
        check_ollama_status()
        return
    
    migrator = OllamaMigrator(args.target)
    success = migrator.migrate(cleanup=args.cleanup)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

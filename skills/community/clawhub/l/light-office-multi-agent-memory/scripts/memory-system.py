#!/usr/bin/env python3
"""
多Agent记忆系统 - 集成管理器（通用版）

功能：
  集成所有记忆系统功能，提供统一入口

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
SCRIPTS_DIR = Path(__file__).parent

# ============================================================
# 集成管理器
# ============================================================

class MemorySystemManager:
    """记忆系统集成管理器"""
    
    def __init__(self):
        self.scripts = {
            "hook_capture": SCRIPTS_DIR / "hook-capture.py",
            "rrf_search": SCRIPTS_DIR / "rrf-search.py",
            "graph_builder": SCRIPTS_DIR / "graph-builder.py",
            "conflict_detector": SCRIPTS_DIR / "conflict-detector.py",
            "token_tracker": SCRIPTS_DIR / "token-tracker.py"
        }
        
        self.results = {}
    
    def run_all(self):
        """运行所有测试"""
        print("=" * 60)
        print("多Agent记忆系统 - 集成测试")
        print("=" * 60)
        print(f"时间: {datetime.now().isoformat()}")
        print()
        
        for script_name, script_path in self.scripts.items():
            print(f"\n{'='*60}")
            print(f"运行脚本: {script_name}")
            print(f"{'='*60}")
            
            if not script_path.exists():
                print(f"[ERROR] 脚本不存在: {script_path}")
                self.results[script_name] = {"status": "error", "message": "脚本不存在"}
                continue
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print(f"[SUCCESS] {script_name} 测试通过")
                    self.results[script_name] = {"status": "success", "output": result.stdout}
                else:
                    print(f"[ERROR] {script_name} 测试失败")
                    print(f"stderr: {result.stderr}")
                    self.results[script_name] = {"status": "error", "stderr": result.stderr}
            
            except subprocess.TimeoutExpired:
                print(f"[TIMEOUT] {script_name} 超时")
                self.results[script_name] = {"status": "timeout"}
            except Exception as e:
                print(f"[ERROR] {script_name} 异常: {e}")
                self.results[script_name] = {"status": "error", "message": str(e)}
        
        # 输出汇总
        print(f"\n{'='*60}")
        print("集成测试汇总")
        print(f"{'='*60}")
        
        success_count = sum(1 for r in self.results.values() if r.get("status") == "success")
        error_count = sum(1 for r in self.results.values() if r.get("status") == "error")
        timeout_count = sum(1 for r in self.results.values() if r.get("status") == "timeout")
        
        print(f"总脚本数: {len(self.results)}")
        print(f"成功: {success_count}")
        print(f"失败: {error_count}")
        print(f"超时: {timeout_count}")
        
        return self.results
    
    def get_status(self):
        """获取系统状态"""
        status = {
            "version": "1.0.0",
            "scripts": {},
            "overall_status": "unknown"
        }
        
        for script_name, script_path in self.scripts.items():
            status["scripts"][script_name] = {
                "exists": script_path.exists(),
                "path": str(script_path)
            }
        
        all_exist = all(s["exists"] for s in status["scripts"].values())
        status["overall_status"] = "ready" if all_exist else "incomplete"
        
        return status


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    manager = MemorySystemManager()
    
    # 获取状态
    print("=" * 60)
    print("多Agent记忆系统 - 状态检查")
    print("=" * 60)
    
    status = manager.get_status()
    print(f"版本: {status['version']}")
    print(f"状态: {status['overall_status']}")
    print(f"脚本数: {len(status['scripts'])}")
    
    for script_name, script_info in status["scripts"].items():
        status_icon = "✅" if script_info["exists"] else "❌"
        print(f"  {status_icon} {script_name}: {script_info['path']}")
    
    # 运行集成测试
    print(f"\n{'='*60}")
    print("开始集成测试")
    print(f"{'='*60}")
    
    results = manager.run_all()
    
    # 输出最终状态
    print(f"\n{'='*60}")
    print("多Agent记忆系统部署完成")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    total_count = len(results)
    
    print(f"测试通过: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n✅ 多Agent记忆系统部署成功！")
    else:
        print(f"\n⚠️ 多Agent记忆系统部署部分成功 ({success_count}/{total_count})")


if __name__ == "__main__":
    main()

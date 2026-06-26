#!/usr/bin/env python3
"""
OpenClaw Optimize - Python API
性能优化工具
"""

import os
import sys
import time
import json
import psutil
import subprocess
import gc
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class MemoryOptimizer:
    """内存优化器"""
    
    def __init__(self):
        self.process = psutil.Process()
    
    def get_status(self) -> Dict:
        """获取内存状态"""
        mem = psutil.virtual_memory()
        proc_mem = self.process.memory_info()
        
        return {
            "system_total": self._human_readable(mem.total),
            "system_available": self._human_readable(mem.available),
            "system_percent": mem.percent,
            "process_rss": self._human_readable(proc_mem.rss),
            "process_vms": self._human_readable(proc_mem.vms),
            "process_percent": self.process.memory_percent(),
            "timestamp": datetime.now().isoformat()
        }
    
    def force_gc(self) -> Dict:
        """强制垃圾回收"""
        before = self.process.memory_info().rss
        gc.collect()
        after = self.process.memory_info().rss
        
        freed = before - after
        return {
            "freed_bytes": freed,
            "freed_human": self._human_readable(freed),
            "success": freed > 0
        }
    
    def find_leaks(self) -> List[Dict]:
        """查找内存泄漏嫌疑"""
        leaks = []
        
        # 检查增长趋势
        samples = []
        for _ in range(5):
            samples.append(self.process.memory_info().rss)
            time.sleep(1)
        
        # 如果持续增长，可能存在泄漏
        if samples[-1] > samples[0] * 1.1:  # 增长超过10%
            leaks.append({
                "type": "gradual_increase",
                "growth": self._human_readable(samples[-1] - samples[0]),
                "severity": "medium"
            })
        
        return leaks
    
    def set_limit(self, max_mb: int):
        """设置内存限制（需要系统支持）"""
        try:
            import resource
            max_bytes = max_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (max_bytes, max_bytes))
            return True
        except Exception as e:
            print(f"设置内存限制失败: {e}")
            return False
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class SkillOptimizer:
    """技能优化器"""
    
    def __init__(self, skills_dir: str = "~/.openclaw/workspace/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
    
    def analyze_load_time(self) -> List[Dict]:
        """分析技能加载时间"""
        results = []
        
        if not self.skills_dir.exists():
            return results
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill_name = skill_path.name
                skill_size = sum(
                    f.stat().st_size 
                    for f in skill_path.rglob('*') 
                    if f.is_file()
                )
                
                # 估算加载时间（粗略估计：每MB约100ms）
                estimated_time = skill_size / (1024 * 1024) * 0.1
                
                results.append({
                    "name": skill_name,
                    "size": skill_size,
                    "size_human": self._human_readable(skill_size),
                    "estimated_load_time": f"{estimated_time:.2f}s"
                })
        
        return sorted(results, key=lambda x: x["size"], reverse=True)
    
    def get_optimization_suggestions(self) -> List[str]:
        """获取优化建议"""
        suggestions = []
        
        # 检查技能数量
        skill_count = len(list(self.skills_dir.iterdir()))
        if skill_count > 20:
            suggestions.append(f"技能数量过多 ({skill_count})，建议精简到15个以内")
        
        # 检查重复功能
        duplicates = self._find_duplicate_skills()
        for dup in duplicates:
            suggestions.append(f"发现重复功能: {dup}")
        
        # 检查大文件
        large_skills = self._find_large_skills()
        for skill in large_skills:
            suggestions.append(f"技能过大: {skill['name']} ({skill['size_human']})")
        
        return suggestions
    
    def _find_duplicate_skills(self) -> List[str]:
        """查找重复功能的技能"""
        duplicates = []
        
        # 常见重复组合
        duplicate_patterns = [
            ["content-creator-cn", "content-writer"],
            ["crawl4ai-skill", "stealth-browser"],
            ["openclaw-tavily-search", "multi-search-engine"],
        ]
        
        for pattern in duplicate_patterns:
            existing = [p for p in pattern if (self.skills_dir / p).exists()]
            if len(existing) > 1:
                duplicates.append(f"{' 和 '.join(existing)} 功能重复")
        
        return duplicates
    
    def _find_large_skills(self, threshold_mb: int = 10) -> List[Dict]:
        """查找大技能"""
        large = []
        threshold = threshold_mb * 1024 * 1024
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                size = sum(
                    f.stat().st_size 
                    for f in skill_path.rglob('*') 
                    if f.is_file()
                )
                if size > threshold:
                    large.append({
                        "name": skill_path.name,
                        "size": size,
                        "size_human": self._human_readable(size)
                    })
        
        return large
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class HistoryOptimizer:
    """历史记录优化器"""
    
    def __init__(self, workspace_dir: str = "~/.openclaw/workspace"):
        self.workspace_dir = Path(workspace_dir).expanduser()
        self.memory_dir = self.workspace_dir / "memory"
    
    def get_size(self) -> Dict:
        """获取历史记录大小"""
        total_size = 0
        file_count = 0
        
        if self.memory_dir.exists():
            for f in self.memory_dir.rglob('*'):
                if f.is_file():
                    total_size += f.stat().st_size
                    file_count += 1
        
        # 检查向量数据库
        vector_db_size = self._get_vector_db_size()
        
        return {
            "memory_files": file_count,
            "memory_size": self._human_readable(total_size),
            "vector_db_size": self._human_readable(vector_db_size),
            "total_size": self._human_readable(total_size + vector_db_size)
        }
    
    def clean_old(self, days: int = 7) -> Dict:
        """清理旧记录"""
        cleaned = 0
        freed_bytes = 0
        cutoff = datetime.now() - timedelta(days=days)
        
        if self.memory_dir.exists():
            for f in self.memory_dir.iterdir():
                if f.is_file():
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if mtime < cutoff:
                        freed_bytes += f.stat().st_size
                        f.unlink()
                        cleaned += 1
        
        return {
            "cleaned_files": cleaned,
            "freed": self._human_readable(freed_bytes)
        }
    
    def _get_vector_db_size(self) -> int:
        """获取向量数据库大小"""
        vector_db_path = self.workspace_dir / ".vector_db"
        if not vector_db_path.exists():
            return 0
        
        return sum(
            f.stat().st_size 
            for f in vector_db_path.rglob('*') 
            if f.is_file()
        )
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = []
    
    def start_monitoring(self, duration: int = 60):
        """开始监控"""
        print(f"开始监控 {duration} 秒...")
        
        for i in range(duration):
            metric = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "load_avg": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
            }
            self.metrics.append(metric)
            
            if i % 10 == 0:
                print(f"已监控 {i}/{duration} 秒...")
            
            time.sleep(1)
        
        print("监控完成！")
    
    def generate_report(self) -> Dict:
        """生成报告"""
        if not self.metrics:
            return {"error": "没有监控数据"}
        
        cpu_values = [m["cpu_percent"] for m in self.metrics]
        mem_values = [m["memory_percent"] for m in self.metrics]
        
        return {
            "duration": len(self.metrics),
            "cpu_avg": sum(cpu_values) / len(cpu_values),
            "cpu_max": max(cpu_values),
            "memory_avg": sum(mem_values) / len(mem_values),
            "memory_max": max(mem_values),
            "status": "normal" if max(mem_values) < 80 else "warning"
        }


class OpenClawOptimizer:
    """OpenClaw 主优化器"""
    
    def __init__(self):
        self.memory = MemoryOptimizer()
        self.skills = SkillOptimizer()
        self.history = HistoryOptimizer()
        self.monitor = PerformanceMonitor()
    
    def full_optimize(self) -> Dict:
        """执行完整优化"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }
        
        # 1. 内存优化
        print("1. 优化内存...")
        gc_result = self.memory.force_gc()
        results["actions"].append({
            "name": "force_gc",
            "result": gc_result
        })
        
        # 2. 清理历史
        print("2. 清理历史记录...")
        clean_result = self.history.clean_old(days=3)
        results["actions"].append({
            "name": "clean_history",
            "result": clean_result
        })
        
        # 3. 分析技能
        print("3. 分析技能...")
        skill_analysis = self.skills.analyze_load_time()
        suggestions = self.skills.get_optimization_suggestions()
        results["actions"].append({
            "name": "analyze_skills",
            "result": {
                "skill_count": len(skill_analysis),
                "suggestions": suggestions
            }
        })
        
        return results
    
    def diagnose(self) -> Dict:
        """诊断问题"""
        issues = []
        
        # 检查内存
        mem_status = self.memory.get_status()
        if mem_status["system_percent"] > 80:
            issues.append({
                "type": "high_memory",
                "severity": "high",
                "message": f"系统内存使用率过高: {mem_status['system_percent']}%"
            })
        
        # 检查历史记录
        history_size = self.history.get_size()
        if "GB" in history_size["total_size"]:
            issues.append({
                "type": "large_history",
                "severity": "medium",
                "message": f"历史记录过大: {history_size['total_size']}"
            })
        
        # 检查技能
        suggestions = self.skills.get_optimization_suggestions()
        for suggestion in suggestions:
            issues.append({
                "type": "skill_issue",
                "severity": "low",
                "message": suggestion
            })
        
        return {
            "issue_count": len(issues),
            "issues": issues,
            "recommendation": "运行 full_optimize() 进行优化" if issues else "系统状态良好"
        }


# 便捷函数
def optimize():
    """一键优化"""
    opt = OpenClawOptimizer()
    return opt.full_optimize()


def diagnose():
    """一键诊断"""
    opt = OpenClawOptimizer()
    return opt.diagnose()


if __name__ == "__main__":
    print("🔧 OpenClaw Optimize Tool")
    print("=" * 40)
    
    opt = OpenClawOptimizer()
    
    # 诊断
    print("\n📊 系统诊断:")
    diagnosis = opt.diagnose()
    print(f"发现问题: {diagnosis['issue_count']} 个")
    for issue in diagnosis['issues']:
        print(f"  - [{issue['severity']}] {issue['message']}")
    
    # 优化
    print("\n⚡ 执行优化:")
    results = opt.full_optimize()
    for action in results['actions']:
        print(f"  ✓ {action['name']}")
    
    print("\n✅ 优化完成！")

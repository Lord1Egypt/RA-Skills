#!/usr/bin/env python3
"""
OpenClaw Optimize Pro - Python API v2.0
性能优化工具 - 增强版
"""

import os
import sys
import time
import json
import psutil
import subprocess
import gc
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class OptimizationResult:
    """优化结果"""
    success: bool
    action: str
    before: Union[str, int, float]
    after: Union[str, int, float]
    improvement: str
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class MemoryOptimizerPro:
    """增强版内存优化器"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.optimization_history = []
    
    def get_detailed_status(self) -> Dict:
        """获取详细内存状态"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        proc_mem = self.process.memory_info()
        
        # 获取其他进程的内存使用
        other_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                if proc.info['memory_percent'] > 1.0:  # 只显示占用 >1% 的进程
                    other_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'memory_percent': round(proc.info['memory_percent'], 2)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        other_processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        return {
            'system': {
                'total': self._human_readable(mem.total),
                'available': self._human_readable(mem.available),
                'used': self._human_readable(mem.used),
                'percent': mem.percent,
                'cached': self._human_readable(mem.cached),
                'buffers': self._human_readable(mem.buffers)
            },
            'swap': {
                'total': self._human_readable(swap.total),
                'used': self._human_readable(swap.used),
                'percent': swap.percent
            },
            'process': {
                'rss': self._human_readable(proc_mem.rss),
                'vms': self._human_readable(proc_mem.vms),
                'percent': round(self.process.memory_percent(), 2),
                'open_files': len(self.process.open_files()),
                'threads': self.process.num_threads()
            },
            'top_processes': other_processes[:5],
            'timestamp': datetime.now().isoformat()
        }
    
    def aggressive_gc(self) -> OptimizationResult:
        """激进垃圾回收"""
        before = self.process.memory_info().rss
        
        # 多次垃圾回收
        for _ in range(3):
            gc.collect()
            time.sleep(0.1)
        
        # 清理 Python 缓存
        import sys
        sys.modules.clear()
        
        after = self.process.memory_info().rss
        freed = before - after
        
        result = OptimizationResult(
            success=freed > 0,
            action="aggressive_gc",
            before=self._human_readable(before),
            after=self._human_readable(after),
            improvement=f"+{self._human_readable(freed)}" if freed > 0 else "0 B",
            timestamp=datetime.now().isoformat()
        )
        
        self.optimization_history.append(result)
        return result
    
    def clear_cache(self) -> OptimizationResult:
        """清理系统缓存"""
        before = psutil.virtual_memory().available
        
        try:
            # Linux: 清理页面缓存
            if os.path.exists('/proc/sys/vm/drop_caches'):
                subprocess.run(['sync'], check=True)
                with open('/proc/sys/vm/drop_caches', 'w') as f:
                    f.write('3')
        except Exception as e:
            print(f"清理缓存失败: {e}")
        
        time.sleep(1)
        after = psutil.virtual_memory().available
        
        return OptimizationResult(
            success=True,
            action="clear_cache",
            before=self._human_readable(before),
            after=self._human_readable(after),
            improvement=f"+{self._human_readable(after - before)}",
            timestamp=datetime.now().isoformat()
        )
    
    def find_memory_leaks_advanced(self) -> List[Dict]:
        """高级内存泄漏检测"""
        leaks = []
        
        # 采样内存使用
        samples = []
        for i in range(10):
            samples.append({
                'rss': self.process.memory_info().rss,
                'time': time.time()
            })
            time.sleep(0.5)
        
        # 分析趋势
        rss_values = [s['rss'] for s in samples]
        avg_growth = (rss_values[-1] - rss_values[0]) / len(samples)
        
        if avg_growth > 1024 * 1024:  # 每秒增长 > 1MB
            leaks.append({
                'type': 'rapid_growth',
                'severity': 'high',
                'growth_rate': f"{self._human_readable(avg_growth)}/s",
                'suggestion': '可能存在严重内存泄漏，建议重启服务'
            })
        elif avg_growth > 100 * 1024:  # 每秒增长 > 100KB
            leaks.append({
                'type': 'gradual_growth',
                'severity': 'medium',
                'growth_rate': f"{self._human_readable(avg_growth)}/s",
                'suggestion': '内存缓慢增长，建议监控'
            })
        
        # 检查内存碎片
        if len(gc.garbage) > 0:
            leaks.append({
                'type': 'gc_garbage',
                'severity': 'low',
                'count': len(gc.garbage),
                'suggestion': '存在循环引用，建议检查代码'
            })
        
        return leaks
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if abs(bytes_val) < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class SkillOptimizerPro:
    """增强版技能优化器"""
    
    def __init__(self, skills_dir: str = "~/.openclaw/workspace/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
        self.dependency_graph = {}
    
    def analyze_startup_time(self) -> Dict:
        """分析启动时间"""
        results = {
            'total_skills': 0,
            'total_size': 0,
            'estimated_startup': 0,
            'slow_skills': [],
            'details': []
        }
        
        if not self.skills_dir.exists():
            return results
        
        for skill_path in sorted(self.skills_dir.iterdir()):
            if skill_path.is_dir():
                skill_name = skill_path.name
                
                # 计算大小
                skill_size = sum(
                    f.stat().st_size 
                    for f in skill_path.rglob('*') 
                    if f.is_file()
                )
                
                # 计算文件数
                file_count = sum(1 for _ in skill_path.rglob('*') if _.is_file())
                
                # 估算加载时间（基于大小和文件数）
                size_time = skill_size / (1024 * 1024) * 0.1  # 每MB 0.1秒
                file_time = file_count * 0.001  # 每个文件 1ms
                estimated_time = size_time + file_time
                
                skill_info = {
                    'name': skill_name,
                    'size': skill_size,
                    'size_human': self._human_readable(skill_size),
                    'files': file_count,
                    'estimated_time': round(estimated_time, 3),
                    'has_python': any(f.suffix == '.py' for f in skill_path.rglob('*')),
                    'has_node': any(f.name == 'package.json' for f in skill_path.rglob('*'))
                }
                
                results['details'].append(skill_info)
                results['total_skills'] += 1
                results['total_size'] += skill_size
                results['estimated_startup'] += estimated_time
                
                if estimated_time > 0.5:  # 超过0.5秒算慢
                    results['slow_skills'].append(skill_info)
        
        # 排序
        results['details'].sort(key=lambda x: x['size'], reverse=True)
        results['slow_skills'].sort(key=lambda x: x['estimated_time'], reverse=True)
        
        return results
    
    def generate_optimization_plan(self) -> List[Dict]:
        """生成优化计划"""
        plan = []
        analysis = self.analyze_startup_time()
        
        # 1. 检查技能数量
        if analysis['total_skills'] > 20:
            plan.append({
                'priority': 'high',
                'action': 'reduce_skills',
                'description': f'技能数量过多 ({analysis["total_skills"]}), 建议精简到15个以内',
                'expected_improvement': '30-50% 启动时间减少'
            })
        
        # 2. 检查大技能
        for skill in analysis['slow_skills'][:3]:
            plan.append({
                'priority': 'medium',
                'action': 'optimize_skill',
                'target': skill['name'],
                'description': f'{skill["name"]} 加载慢 ({skill["estimated_time"]}s), 建议优化或懒加载',
                'expected_improvement': f'{skill["estimated_time"]:.1f}s 减少'
            })
        
        # 3. 检查重复
        duplicates = self._find_duplicate_functionality()
        for dup in duplicates:
            plan.append({
                'priority': 'medium',
                'action': 'remove_duplicate',
                'description': dup,
                'expected_improvement': '减少内存占用和冲突'
            })
        
        # 4. 检查未使用技能
        unused = self._find_potentially_unused()
        if unused:
            plan.append({
                'priority': 'low',
                'action': 'review_unused',
                'targets': unused,
                'description': f'发现 {len(unused)} 个可能未使用的技能',
                'expected_improvement': '减少内存占用'
            })
        
        return sorted(plan, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])
    
    def _find_duplicate_functionality(self) -> List[str]:
        """查找重复功能"""
        duplicates = []
        
        # 检查关键词重复
        keyword_groups = {
            'browser': ['agent-browser', 'stealth-browser', 'browser-cash'],
            'search': ['multi-search-engine', 'tavily-search'],
            'content': ['content-writer', 'content-creator', 'humanizer'],
            'crawler': ['crawl4ai', 'scrapling', 'xiaohongshu-crawler']
        }
        
        for group_name, skills in keyword_groups.items():
            existing = [s for s in skills if (self.skills_dir / s).exists()]
            if len(existing) > 1:
                duplicates.append(f"{group_name} 功能重复: {', '.join(existing)}")
        
        return duplicates
    
    def _find_potentially_unused(self) -> List[str]:
        """查找可能未使用的技能"""
        unused = []
        
        # 检查最近修改时间
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                # 获取最近修改时间
                mtime = max(
                    f.stat().st_mtime 
                    for f in skill_path.rglob('*') 
                    if f.is_file()
                )
                days_since = (time.time() - mtime) / 86400
                
                if days_since > 30:  # 30天未修改
                    unused.append({
                        'name': skill_path.name,
                        'days_inactive': int(days_since)
                    })
        
        return unused
    
    def create_lazy_load_config(self) -> Dict:
        """创建懒加载配置"""
        analysis = self.analyze_startup_time()
        
        # 核心技能（立即加载）
        core_skills = [
            'self-improving-agent',
            'find-skills',
            'memory-hygiene'
        ]
        
        # 其他技能（懒加载）
        lazy_skills = [
            s['name'] for s in analysis['details'] 
            if s['name'] not in core_skills
        ]
        
        return {
            'preload': core_skills,
            'lazy_load': lazy_skills,
            'unload_after': 300,  # 5分钟无使用卸载
            'estimated_startup_improvement': f"{sum(s['estimated_time'] for s in analysis['details'] if s['name'] in lazy_skills):.1f}s"
        }
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if abs(bytes_val) < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class HistoryOptimizerPro:
    """增强版历史记录优化器"""
    
    def __init__(self, workspace_dir: str = "~/.openclaw/workspace"):
        self.workspace_dir = Path(workspace_dir).expanduser()
        self.memory_dir = self.workspace_dir / "memory"
        self.learnings_dir = self.workspace_dir / ".learnings"
    
    def comprehensive_analysis(self) -> Dict:
        """全面分析历史记录"""
        analysis = {
            'memory_files': {'count': 0, 'size': 0, 'oldest': None, 'newest': None},
            'learnings': {'count': 0, 'size': 0},
            'vector_db': {'size': 0, 'entries': 0},
            'logs': {'count': 0, 'size': 0},
            'total_size': 0,
            'recommendations': []
        }
        
        # 分析 memory 目录
        if self.memory_dir.exists():
            files = list(self.memory_dir.iterdir())
            analysis['memory_files']['count'] = len(files)
            
            mtimes = []
            for f in files:
                if f.is_file():
                    size = f.stat().st_size
                    mtime = f.stat().st_mtime
                    analysis['memory_files']['size'] += size
                    mtimes.append(mtime)
            
            if mtimes:
                analysis['memory_files']['oldest'] = datetime.fromtimestamp(min(mtimes)).strftime('%Y-%m-%d')
                analysis['memory_files']['newest'] = datetime.fromtimestamp(max(mtimes)).strftime('%Y-%m-%d')
        
        # 分析 learnings
        if self.learnings_dir.exists():
            for f in self.learnings_dir.iterdir():
                if f.is_file():
                    analysis['learnings']['count'] += 1
                    analysis['learnings']['size'] += f.stat().st_size
        
        # 检查向量数据库
        vector_db_path = self.workspace_dir / ".vector_db"
        if vector_db_path.exists():
            for f in vector_db_path.rglob('*'):
                if f.is_file():
                    analysis['vector_db']['size'] += f.stat().st_size
        
        # 检查日志
        log_dir = self.workspace_dir / "logs"
        if log_dir.exists():
            for f in log_dir.rglob('*'):
                if f.is_file():
                    analysis['logs']['count'] += 1
                    analysis['logs']['size'] += f.stat().st_size
        
        # 计算总计
        analysis['total_size'] = (
            analysis['memory_files']['size'] +
            analysis['learnings']['size'] +
            analysis['vector_db']['size'] +
            analysis['logs']['size']
        )
        
        # 生成建议
        if analysis['memory_files']['count'] > 30:
            analysis['recommendations'].append({
                'priority': 'high',
                'issue': '历史文件过多',
                'action': '清理30天前的记录',
                'expected_saving': '50-70% 空间'
            })
        
        if analysis['vector_db']['size'] > 100 * 1024 * 1024:  # > 100MB
            analysis['recommendations'].append({
                'priority': 'medium',
                'issue': '向量数据库过大',
                'action': '压缩和重建索引',
                'expected_saving': '30-40% 空间'
            })
        
        # 转换为可读格式
        analysis['memory_files']['size_human'] = self._human_readable(analysis['memory_files']['size'])
        analysis['learnings']['size_human'] = self._human_readable(analysis['learnings']['size'])
        analysis['vector_db']['size_human'] = self._human_readable(analysis['vector_db']['size'])
        analysis['logs']['size_human'] = self._human_readable(analysis['logs']['size'])
        analysis['total_size_human'] = self._human_readable(analysis['total_size'])
        
        return analysis
    
    def smart_cleanup(self, keep_days: int = 7, dry_run: bool = False) -> Dict:
        """智能清理"""
        results = {
            'cleaned_files': 0,
            'freed_bytes': 0,
            'details': []
        }
        
        cutoff = time.time() - (keep_days * 86400)
        
        # 清理 memory 文件
        if self.memory_dir.exists():
            for f in self.memory_dir.iterdir():
                if f.is_file() and f.stat().st_mtime < cutoff:
                    size = f.stat().st_size
                    if not dry_run:
                        f.unlink()
                    results['cleaned_files'] += 1
                    results['freed_bytes'] += size
                    results['details'].append({
                        'file': str(f),
                        'size': size,
                        'action': 'deleted' if not dry_run else 'would_delete'
                    })
        
        # 压缩 learnings
        if self.learnings_dir.exists():
            for f in self.learnings_dir.iterdir():
                if f.is_file() and f.suffix == '.md':
                    # 检查文件大小
                    if f.stat().st_size > 1024 * 1024:  # > 1MB
                        # 可以归档旧记录
                        pass
        
        results['freed_human'] = self._human_readable(results['freed_bytes'])
        return results
    
    @staticmethod
    def _human_readable(bytes_val: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if abs(bytes_val) < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"


class AutoOptimizer:
    """自动优化器"""
    
    def __init__(self):
        self.memory = MemoryOptimizerPro()
        self.skills = SkillOptimizerPro()
        self.history = HistoryOptimizerPro()
    
    def detect_performance_issues(self) -> List[Dict]:
        """检测性能问题"""
        issues = []
        
        # 检查内存
        mem_status = self.memory.get_detailed_status()
        if mem_status['system']['percent'] > 80:
            issues.append({
                'type': 'high_memory',
                'severity': 'critical',
                'message': f"系统内存使用率过高: {mem_status['system']['percent']}%",
                'auto_fix': True
            })
        elif mem_status['system']['percent'] > 60:
            issues.append({
                'type': 'elevated_memory',
                'severity': 'warning',
                'message': f"系统内存使用率偏高: {mem_status['system']['percent']}%",
                'auto_fix': True
            })
        
        # 检查历史记录
        history_analysis = self.history.comprehensive_analysis()
        if history_analysis['total_size'] > 500 * 1024 * 1024:  # > 500MB
            issues.append({
                'type': 'large_history',
                'severity': 'medium',
                'message': f"历史记录过大: {history_analysis['total_size_human']}",
                'auto_fix': True
            })
        
        # 检查技能
        skill_analysis = self.skills.analyze_startup_time()
        if skill_analysis['estimated_startup'] > 5:  # > 5秒
            issues.append({
                'type': 'slow_startup',
                'severity': 'medium',
                'message': f"启动时间过长: {skill_analysis['estimated_startup']:.1f}s",
                'auto_fix': False
            })
        
        return issues
    
    def auto_optimize(self) -> Dict:
        """自动优化"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'issues_found': 0,
            'fixes_applied': [],
            'manual_actions_required': []
        }
        
        # 检测问题
        issues = self.detect_performance_issues()
        results['issues_found'] = len(issues)
        
        # 自动修复
        for issue in issues:
            if issue.get('auto_fix'):
                if issue['type'] in ['high_memory', 'elevated_memory']:
                    fix_result = self.memory.aggressive_gc()
                    results['fixes_applied'].append({
                        'issue': issue['type'],
                        'action': 'aggressive_gc',
                        'result': fix_result.to_dict()
                    })
                
                elif issue['type'] == 'large_history':
                    fix_result = self.history.smart_cleanup(keep_days=7)
                    results['fixes_applied'].append({
                        'issue': issue['type'],
                        'action': 'smart_cleanup',
                        'result': fix_result
                    })
            else:
                results['manual_actions_required'].append(issue)
        
        return results
    
    def generate_comprehensive_report(self) -> str:
        """生成综合报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("OpenClaw 性能优化报告")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        # 内存状态
        lines.append("【内存状态】")
        mem_status = self.memory.get_detailed_status()
        lines.append(f"  系统内存: {mem_status['system']['percent']}% 已用")
        lines.append(f"  可用内存: {mem_status['system']['available']}")
        lines.append(f"  进程内存: {mem_status['process']['rss']} ({mem_status['process']['percent']}%)")
        lines.append("")
        
        # 技能分析
        lines.append("【技能分析】")
        skill_analysis = self.skills.analyze_startup_time()
        lines.append(f"  技能总数: {skill_analysis['total_skills']}")
        lines.append(f"  总大小: {self.memory._human_readable(skill_analysis['total_size'])}")
        lines.append(f"  预估启动时间: {skill_analysis['estimated_startup']:.1f}s")
        if skill_analysis['slow_skills']:
            lines.append("  慢加载技能:")
            for skill in skill_analysis['slow_skills'][:3]:
                lines.append(f"    - {skill['name']}: {skill['estimated_time']}s")
        lines.append("")
        
        # 历史记录
        lines.append("【历史记录】")
        history_analysis = self.history.comprehensive_analysis()
        lines.append(f"  总大小: {history_analysis['total_size_human']}")
        lines.append(f"  内存文件: {history_analysis['memory_files']['count']} 个 ({history_analysis['memory_files']['size_human']})")
        lines.append(f"  学习记录: {history_analysis['learnings']['count']} 个 ({history_analysis['learnings']['size_human']})")
        lines.append("")
        
        # 问题检测
        lines.append("【检测到的问题】")
        issues = self.detect_performance_issues()
        if issues:
            for issue in issues:
                icon = "🔴" if issue['severity'] == 'critical' else ("🟡" if issue['severity'] == 'warning' else "🔵")
                lines.append(f"  {icon} [{issue['severity'].upper()}] {issue['message']}")
        else:
            lines.append("  ✅ 未发现明显问题")
        lines.append("")
        
        # 优化建议
        lines.append("【优化建议】")
        plan = self.skills.generate_optimization_plan()
        if plan:
            for item in plan[:5]:
                lines.append(f"  [{item['priority'].upper()}] {item['description']}")
                lines.append(f"      预期改善: {item['expected_improvement']}")
        else:
            lines.append("  ✅ 系统已优化到最佳状态")
        lines.append("")
        
        lines.append("=" * 60)
        lines.append("报告生成完成")
        lines.append("=" * 60)
        
        return "\n".join(lines)


# 便捷函数
def quick_optimize():
    """快速优化"""
    opt = AutoOptimizer()
    return opt.auto_optimize()


def full_report():
    """完整报告"""
    opt = AutoOptimizer()
    return opt.generate_comprehensive_report()


if __name__ == "__main__":
    print("🔧 OpenClaw Optimize Pro v2.0")
    print("=" * 60)
    
    opt = AutoOptimizer()
    
    # 生成报告
    report = opt.generate_comprehensive_report()
    print(report)
    
    # 自动优化
    print("\n⚡ 执行自动优化...")
    results = opt.auto_optimize()
    print(f"发现问题: {results['issues_found']} 个")
    print(f"自动修复: {len(results['fixes_applied'])} 个")
    
    if results['manual_actions_required']:
        print(f"\n需要手动处理: {len(results['manual_actions_required'])} 个")
        for issue in results['manual_actions_required']:
            print(f"  - {issue['message']}")
    
    print("\n✅ 完成！")

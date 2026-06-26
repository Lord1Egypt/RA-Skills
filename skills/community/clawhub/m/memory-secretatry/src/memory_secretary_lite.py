#!/usr/bin/env python3
"""
记忆秘书核心引擎 - Memory Secretary Lite

智能记忆管理与优化助手的核心实现
基于规则和统计分析，不依赖大模型

版本：1.0.0
作者：隐客
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import re
from collections import Counter, defaultdict
import difflib
from typing import Dict, List, Optional, Any, Tuple


class MemorySecretaryLite:
    """
    轻量级记忆秘书 - 基于规则和统计分析
    
    功能:
        - 记忆质量管理
        - 重复工作检测
        - 成功案例提取
        - 工作模式识别
        - 智能提醒生成
        - 分享报告生成
    
    约束:
        - 不依赖大模型
        - 使用本地化、规则化方法
        - 零外部依赖（仅Python标准库）
    
    示例:
        >>> secretary = MemorySecretaryLite()
        >>> quality = secretary.check_memory_quality()
        >>> similar = secretary.find_similar_tasks("中证 500 数据收集")
    """
    
    def __init__(self, workspace_root: str = "/home/admin/openclaw/workspace"):
        """
        初始化记忆秘书
        
        Args:
            workspace_root: 工作空间根目录路径
            
        Raises:
            FileNotFoundError: 工作空间目录不存在
            PermissionError: 无权限访问工作空间
        """
        try:
            self.workspace = Path(workspace_root).resolve()
            if not self.workspace.exists():
                raise FileNotFoundError(f"工作空间不存在：{workspace_root}")
            
            self.memory_dir = self.workspace / "memory"
            self.scripts_dir = self.workspace / "scripts"
            self.docs_dir = self.workspace / "docs"
            self.reports_dir = self.workspace / "reports"
            
            # 现有系统组件
            self.categories_file = self.memory_dir / "memory_categories.json"
            self.tech_index_db = self.memory_dir / "tech_memory.db"
            self.unified_index_db = self.memory_dir / "unified_index.db"
            
            # 秘书功能数据
            self.secretary_data_dir = self.memory_dir / "secretary"
            self.secretary_data_dir.mkdir(parents=True, exist_ok=True)
            
            self.success_cases_file = self.secretary_data_dir / "success_cases.json"
            self.work_patterns_file = self.secretary_data_dir / "work_patterns.json"
            self.reminders_file = self.secretary_data_dir / "reminders.json"
            self.quality_report_file = self.secretary_data_dir / "quality_report.json"
            
            print("🧠 记忆秘书 Lite - 初始化完成")
            print("=" * 60)
            print(f"工作空间：{self.workspace}")
            print("约束：不依赖大模型，使用规则化方法")
            print("目标：主动记忆管理、智能提醒、模式识别")
            print("=" * 60)
            
        except (OSError, PermissionError) as e:
            print(f"❌ 初始化失败：{e}")
            raise
    
    # ==================== 功能 1: 记忆质量管理 ====================
    
    def check_memory_quality(self) -> Dict[str, Any]:
        """
        检查记忆文件质量（基于规则）
        
        Returns:
            质量检查报告，包含:
                - total_files: 文件总数
                - quality_score: 质量评分 (0-100)
                - issues: 问题列表
                - recommendations: 优化建议
                
        Raises:
            RuntimeError: 记忆目录不存在
        """
        try:
            if not self.memory_dir.exists():
                raise RuntimeError(f"记忆目录不存在：{self.memory_dir}")
            
            print("\n📊 记忆质量检查")
            print("=" * 60)
            
            quality_issues = []
            total_files = 0
            
            # 规则 1: 检查文件大小异常
            for file in self.memory_dir.glob("*.md"):
                total_files += 1
                try:
                    size = file.stat().st_size
                    if size < 100:  # 小于 100 字节，可能为空
                        quality_issues.append({
                            "type": "empty_file",
                            "file": str(file),
                            "size": size,
                            "severity": "low",
                            "suggestion": "检查文件内容是否为空"
                        })
                    elif size > 100000:  # 大于 100KB，可能过大
                        quality_issues.append({
                            "type": "large_file",
                            "file": str(file),
                            "size": size,
                            "severity": "medium",
                            "suggestion": "考虑压缩或分割文件"
                        })
                except (OSError, IOError) as e:
                    quality_issues.append({
                        "type": "file_access_error",
                        "file": str(file),
                        "error": str(e),
                        "severity": "high"
                    })
            
            # 规则 2: 检查文件结构
            structure_issues = self._check_file_structure()
            quality_issues.extend(structure_issues)
            
            # 规则 3: 检查重复内容
            duplicate_issues = self._check_duplicate_content()
            quality_issues.extend(duplicate_issues)
            
            # 计算质量评分
            quality_score = self._calculate_quality_score(total_files, quality_issues)
            
            # 生成优化建议
            recommendations = self._generate_recommendations(quality_issues)
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "total_files": total_files,
                "quality_score": quality_score,
                "issues": quality_issues,
                "issue_count": len(quality_issues),
                "recommendations": recommendations
            }
            
            # 保存报告
            self._save_report(self.quality_report_file, report)
            
            print(f"总文件数：{total_files}")
            print(f"质量评分：{quality_score}/100")
            print(f"发现问题：{len(quality_issues)} 个")
            print(f"优化建议：{len(recommendations)} 条")
            
            return report
            
        except Exception as e:
            print(f"❌ 质量检查失败：{e}")
            raise
    
    def _check_file_structure(self) -> List[Dict[str, Any]]:
        """
        检查文件结构
        
        Returns:
            结构问题列表
        """
        issues = []
        
        for file in self.memory_dir.glob("2026-*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查结构化标记
                has_headers = '##' in content or '###' in content
                has_lists = '- ' in content or '1. ' in content
                has_tables = '|' in content and '--' in content
                
                if not has_headers and not has_lists:
                    issues.append({
                        "type": "poor_structure",
                        "file": str(file),
                        "issue": "缺少标题和列表结构",
                        "severity": "medium",
                        "suggestion": "添加结构化标题和列表"
                    })
                    
            except (UnicodeDecodeError, IOError) as e:
                issues.append({
                    "type": "read_error",
                    "file": str(file),
                    "error": str(e),
                    "severity": "high"
                })
        
        return issues
    
    def _check_duplicate_content(self) -> List[Dict[str, Any]]:
        """
        检查重复内容
        
        Returns:
            重复内容问题列表
        """
        issues = []
        content_hashes = {}
        
        for file in self.memory_dir.glob("*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 简单哈希检查
                content_hash = hashlib.md5(content.encode()).hexdigest()
                
                if content_hash in content_hashes:
                    issues.append({
                        "type": "duplicate_content",
                        "file": str(file),
                        "duplicate_of": content_hashes[content_hash],
                        "severity": "medium",
                        "suggestion": "检查是否为意外重复"
                    })
                else:
                    content_hashes[content_hash] = str(file)
                    
            except (UnicodeDecodeError, IOError) as e:
                issues.append({
                    "type": "read_error",
                    "file": str(file),
                    "error": str(e),
                    "severity": "high"
                })
        
        return issues
    
    def _calculate_quality_score(self, total_files: int, issues: List[Dict]) -> int:
        """
        计算质量评分
        
        Args:
            total_files: 文件总数
            issues: 问题列表
            
        Returns:
            质量评分 (0-100)
        """
        if total_files == 0:
            return 0
        
        # 基础分
        base_score = 100
        
        # 扣分项
        severity_weights = {
            "high": 10,
            "medium": 5,
            "low": 2
        }
        
        total_deduction = sum(
            severity_weights.get(issue.get("severity", "low"), 2)
            for issue in issues
        )
        
        # 确保不低于 0
        final_score = max(0, base_score - total_deduction)
        
        return final_score
    
    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """
        生成优化建议
        
        Args:
            issues: 问题列表
            
        Returns:
            建议列表
        """
        recommendations = []
        
        # 统计问题类型
        issue_types = Counter(issue["type"] for issue in issues)
        
        if issue_types.get("empty_file", 0) > 0:
            recommendations.append("清理空文件，保持记忆库整洁")
        
        if issue_types.get("large_file", 0) > 0:
            recommendations.append("考虑压缩或分割大型记忆文件")
        
        if issue_types.get("poor_structure", 0) > 0:
            recommendations.append("为记忆文件添加结构化标题和列表")
        
        if issue_types.get("duplicate_content", 0) > 0:
            recommendations.append("检查并删除重复内容")
        
        if not recommendations:
            recommendations.append("记忆质量良好，继续保持！")
        
        return recommendations
    
    def _save_report(self, file_path: Path, report: Dict[str, Any]) -> None:
        """
        保存报告到文件
        
        Args:
            file_path: 文件路径
            report: 报告数据
            
        Raises:
            IOError: 文件写入失败
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"⚠️ 保存报告失败：{e}")
            # 不抛出异常，避免影响主流程
    
    # ==================== 功能 2: 重复工作检测 ====================
    
    def find_similar_tasks(self, query: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        查找相似任务
        
        Args:
            query: 查询文本
            threshold: 相似度阈值 (0-1)
            
        Returns:
            相似任务列表
        """
        try:
            similar_tasks = []
            
            # 搜索记忆文件
            for file in self.memory_dir.glob("*.md"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 提取可能的任务描述
                    task_candidates = self._extract_task_candidates(content)
                    
                    for candidate in task_candidates:
                        similarity = difflib.SequenceMatcher(
                            None, query.lower(), candidate.lower()
                        ).ratio()
                        
                        if similarity >= threshold:
                            similar_tasks.append({
                                "task": candidate,
                                "similarity": similarity,
                                "source_file": str(file),
                                "file_date": file.stem
                            })
                            
                except (UnicodeDecodeError, IOError):
                    continue
            
            # 按相似度排序
            similar_tasks.sort(key=lambda x: x["similarity"], reverse=True)
            
            return similar_tasks
            
        except Exception as e:
            print(f"❌ 查找相似任务失败：{e}")
            return []
    
    def _extract_task_candidates(self, content: str) -> List[str]:
        """
        从内容中提取可能的任务描述
        
        Args:
            content: 文件内容
            
        Returns:
            任务候选列表
        """
        candidates = []
        
        # 提取标题
        headers = re.findall(r'^##+\s+(.+)$', content, re.MULTILINE)
        candidates.extend(headers)
        
        # 提取列表项
        list_items = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
        candidates.extend(list_items[:10])  # 限制数量
        
        return candidates[:20]  # 限制总数
    
    # ==================== 功能 3: 成功案例提取 ====================
    
    def extract_success_cases(self) -> List[Dict[str, Any]]:
        """
        提取成功案例
        
        Returns:
            成功案例列表
        """
        success_cases = []
        success_markers = ['✅', '成功', '完成', '已完成', '搞定']
        
        try:
            for file in self.memory_dir.glob("*.md"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 查找成功案例
                    for marker in success_markers:
                        if marker in content:
                            # 提取上下文
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if marker in line:
                                    # 提取前后文
                                    context_start = max(0, i - 2)
                                    context_end = min(len(lines), i + 3)
                                    context = '\n'.join(lines[context_start:context_end])
                                    
                                    success_cases.append({
                                        "case": line.strip(),
                                        "context": context.strip(),
                                        "source_file": str(file),
                                        "file_date": file.stem,
                                        "marker": marker
                                    })
                                    
                except (UnicodeDecodeError, IOError):
                    continue
            
            return success_cases
            
        except Exception as e:
            print(f"❌ 提取成功案例失败：{e}")
            return []
    
    # ==================== 功能 4: 工作模式识别 ====================
    
    def analyze_work_patterns(self) -> Dict[str, Any]:
        """
        分析工作模式
        
        Returns:
            工作模式分析报告
        """
        try:
            patterns = {
                "frequent_keywords": self._analyze_keywords(),
                "task_frequency": self._analyze_task_frequency(),
                "time_patterns": self._analyze_time_patterns()
            }
            
            return patterns
            
        except Exception as e:
            print(f"❌ 分析工作模式失败：{e}")
            return {}
    
    def _analyze_keywords(self) -> List[Tuple[str, int]]:
        """分析高频关键词"""
        keywords = []
        
        try:
            for file in self.memory_dir.glob("*.md"):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取中文关键词
                chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', content)
                keywords.extend(chinese_words)
            
            # 统计频率
            keyword_counts = Counter(keywords)
            return keyword_counts.most_common(20)
            
        except Exception as e:
            print(f"❌ 关键词分析失败：{e}")
            return []
    
    def _analyze_task_frequency(self) -> Dict[str, int]:
        """分析任务频率"""
        return {"total_tasks": 0, "avg_per_day": 0}
    
    def _analyze_time_patterns(self) -> Dict[str, Any]:
        """分析时间模式"""
        return {"peak_hours": [], "active_days": []}
    
    # ==================== 功能 5: 智能提醒生成 ====================
    
    def generate_reminders(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        生成智能提醒
        
        Args:
            keywords: 关键词列表
            
        Returns:
            提醒列表
        """
        try:
            reminders = []
            
            # 检查相似任务
            for keyword in keywords[:10]:
                similar = self.find_similar_tasks(keyword)
                
                if similar:
                    reminders.append({
                        "type": "similar_task",
                        "priority": "high" if len(similar) > 5 else "medium",
                        "message": f"发现 {len(similar)} 个相似任务：{keyword}",
                        "references": similar[:3]
                    })
            
            return reminders
            
        except Exception as e:
            print(f"❌ 生成提醒失败：{e}")
            return []
    
    # ==================== 功能 6: 分享报告生成 ====================
    
    def generate_share_report(self) -> Dict[str, Any]:
        """
        生成分享报告
        
        Returns:
            分享报告数据
        """
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "memory_quality": self.check_memory_quality(),
                "success_cases": self.extract_success_cases(),
                "work_patterns": self.analyze_work_patterns(),
                "recommendations": []
            }
            
            return report
            
        except Exception as e:
            print(f"❌ 生成分享报告失败：{e}")
            return {}


def main():
    """主函数 - 演示使用"""
    print("🧠 记忆秘书 Lite - 演示")
    print("=" * 60)
    
    try:
        # 初始化
        secretary = MemorySecretaryLite()
        
        # 检查记忆质量
        quality = secretary.check_memory_quality()
        print(f"\n质量评分：{quality['quality_score']}/100")
        
        # 查找相似任务
        similar = secretary.find_similar_tasks("中证 500 数据收集")
        print(f"\n相似任务：{len(similar)} 个")
        
        # 提取成功案例
        cases = secretary.extract_success_cases()
        print(f"成功案例：{len(cases)} 个")
        
        # 分析工作模式
        patterns = secretary.analyze_work_patterns()
        print(f"工作模式分析完成")
        
        print("\n✅ 演示完成")
        
    except Exception as e:
        print(f"\n❌ 演示失败：{e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

"""
Karpathy Lint Pipeline - Phase 3
Knowledge Points 质量检查与自修复
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class LintIssue:
    """Lint 发现的问题"""
    issue_type: str  # duplicate, outdated, incomplete, invalid_tag
    severity: str  # high, medium, low
    title: str
    description: str
    related_items: List[str] = field(default_factory=list)
    suggestion: str = ""


@dataclass
class LintReport:
    """Lint 健康报告"""
    timestamp: str
    total_points: int
    issues_found: int
    issues: List[LintIssue]
    stats: Dict[str, Any]
    
    def to_markdown(self) -> str:
        lines = [
            f"# Knowledge Base Health Report",
            "",
            f"**生成时间**: {self.timestamp}",
            f"**知识点数**: {self.total_points}",
            f"**发现问题**: {self.issues_found}",
            "",
            "## 统计",
        ]
        
        for key, value in self.stats.items():
            lines.append(f"- {key}: {value}")
        
        if self.issues:
            lines.append("")
            lines.append("## 发现的问题")
            
            # 按严重程度分组
            by_severity = {}
            for issue in self.issues:
                if issue.severity not in by_severity:
                    by_severity[issue.severity] = []
                by_severity[issue.severity].append(issue)
            
            for severity in ["high", "medium", "low"]:
                if severity in by_severity:
                    lines.append(f"\n### {severity.upper()} 严重度")
                    for issue in by_severity[severity]:
                        lines.append(f"\n**{issue.title}** ({issue.issue_type})")
                        lines.append(f"{issue.description}")
                        if issue.suggestion:
                            lines.append(f"建议: {issue.suggestion}")
        
        return "\n".join(lines)


class KnowledgePointParser:
    """解析 knowledge points 文件"""
    
    def __init__(self, kp_path: str = None):
        if kp_path is None:
            self.kp_path = Path(__file__).parent.parent.parent / "knowledge" / "knowledge-points"
        else:
            self.kp_path = Path(kp_path)
    
    def parse_kp_file(self, filename: str = None) -> List[Dict[str, Any]]:
        """
        解析 knowledge points Markdown 文件
        
        Returns:
            [{title, core_concept, source, detailed_explanation, tags, confidence, created_at}, ...]
        """
        if filename is None:
            files = list(self.kp_path.glob("knowledge-points-*.md"))
            if not files:
                return []
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            filename = files[0].name
        
        filepath = self.kp_path / filename
        if not filepath.exists():
            return []
        
        content = filepath.read_text(encoding="utf-8")
        return self._parse_markdown(content)
    
    def _parse_markdown(self, content: str) -> List[Dict[str, Any]]:
        """解析 Markdown 格式的 knowledge points"""
        points = []
        
        # 分割每个 ## 标题块（## 必须在行首，用 ^ with MULTILINE）
        pattern = r'^## (.+?)\n(.*?)(?=^## |\Z)'
        matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
        
        for title, body in matches:
            title = title.strip()
            if not title or title.startswith("Knowledge Points"):
                continue
            
            kp = {
                "title": title,
                "core_concept": "",
                "source": "",
                "confidence": "medium",
                "tags": [],
                "detailed_explanation": "",
                "created_at": ""
            }
            
            lines = body.strip().split("\n")
            current_section = None
            section_content = []
            
            for line in lines:
                line = line.strip()
                
                # 检测 subsection heading (### 详细说明)
                if line.startswith("### "):
                    # 保存之前 section 的内容
                    if current_section == "detailed_explanation" and section_content:
                        kp["detailed_explanation"] = " ".join(section_content)
                    # 设置新的 section
                    section_name = line[4:].strip()
                    if "详细说明" in section_name:
                        current_section = "detailed_explanation"
                        section_content = []
                    else:
                        current_section = None
                        section_content = []
                    continue
                
                # 检测 **key**: value 格式
                if line.startswith("**") and ":" in line:
                    # 保存之前 section 的内容
                    if current_section == "detailed_explanation" and section_content:
                        kp["detailed_explanation"] = " ".join(section_content)
                    current_section = None
                    section_content = []
                    
                    # 解析 key-value
                    match = re.match(r'\*\*(.+?)\*\*:\s*(.+)', line)
                    if match:
                        key, value = match.groups()
                        key = key.strip()
                        value = value.strip()
                        
                        if "核心概念" in key:
                            kp["core_concept"] = value
                        elif "来源" in key:
                            kp["source"] = value
                        elif "可信度" in key:
                            kp["confidence"] = value
                        elif "标签" in key:
                            kp["tags"] = [t.strip() for t in value.split(",") if t.strip()]
                        elif "创建时间" in key:
                            kp["created_at"] = value
                elif current_section == "detailed_explanation" and line:
                    section_content.append(line)
            
            # 保存最后 section 的内容
            if current_section == "detailed_explanation" and section_content:
                kp["detailed_explanation"] = " ".join(section_content)
            
            points.append(kp)
        
        return points
    
    def save_kp_file(self, points: List[Dict[str, Any]], filename: str = None) -> str:
        """保存 knowledge points 到文件"""
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"knowledge-points-{date_str}.md"
        
        filepath = self.kp_path / filename
        
        lines = [
            f"# Knowledge Points - {datetime.now().strftime('%Y-%m-%d')}",
            "",
            f"Knowledge points count: {len(points)}",
            "",
            "---",
            ""
        ]
        
        for kp in points:
            lines.append(f"## {kp['title']}")
            lines.append("")
            lines.append(f"**核心概念**: {kp.get('core_concept', '')}")
            lines.append(f"**来源**: {kp.get('source', '')}")
            lines.append(f"**可信度**: {kp.get('confidence', 'medium')}")
            lines.append("")
            if kp.get('detailed_explanation'):
                lines.append("### 详细说明")
                lines.append(kp['detailed_explanation'])
                lines.append("")
            lines.append(f"**标签**: {', '.join(kp.get('tags', []))}")
            lines.append(f"**创建时间**: {kp.get('created_at', '')}")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return str(filepath)


class Deduplicator:
    """去重检测"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.threshold = similarity_threshold
    
    def find_duplicates(self, points: List[Dict[str, Any]]) -> List[Tuple[int, int, float]]:
        """
        查找重复的 knowledge points
        
        Returns:
            [(index1, index2, similarity_score), ...]
        """
        duplicates = []
        
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                score = self._calculate_similarity(points[i], points[j])
                if score >= self.threshold:
                    duplicates.append((i, j, score))
        
        return duplicates
    
    def _calculate_similarity(self, p1: Dict, p2: Dict) -> float:
        """计算两个 knowledge point 的相似度"""
        # 基于标题和核心概念的相似度
        title_sim = self._string_similarity(p1.get("title", ""), p2.get("title", ""))
        concept_sim = self._string_similarity(
            p1.get("core_concept", ""), 
            p2.get("core_concept", "")
        )
        
        # 标签重叠度
        tags1 = set(p1.get("tags", []))
        tags2 = set(p2.get("tags", []))
        if tags1 and tags2:
            tag_sim = len(tags1 & tags2) / len(tags1 | tags2)
        else:
            tag_sim = 0
        
        # 加权平均
        return title_sim * 0.3 + concept_sim * 0.5 + tag_sim * 0.2
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """简单的字符串相似度（基于词重叠）"""
        if not s1 or not s2:
            return 0.0
        
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0


class QualityChecker:
    """质量检查"""
    
    def check(self, points: List[Dict[str, Any]]) -> List[LintIssue]:
        """检查知识点的质量问题"""
        issues = []
        
        for i, kp in enumerate(points):
            # 检查核心概念是否为空
            if not kp.get("core_concept"):
                issues.append(LintIssue(
                    issue_type="incomplete",
                    severity="high",
                    title=f"缺少核心概念: {kp.get('title', 'unknown')}",
                    description=f"Knowledge point '{kp.get('title')}' 缺少核心概念描述",
                    related_items=[kp.get("title", "")],
                    suggestion="添加核心概念描述"
                ))
            
            # 检查详细说明是否为空
            if not kp.get("detailed_explanation"):
                issues.append(LintIssue(
                    issue_type="incomplete",
                    severity="medium",
                    title=f"缺少详细说明: {kp.get('title', 'unknown')}",
                    description=f"Knowledge point '{kp.get('title')}' 缺少详细说明",
                    related_items=[kp.get("title", "")],
                    suggestion="添加详细说明"
                ))
            
            # 检查标签是否为空或只有 general
            tags = kp.get("tags", [])
            if not tags or (len(tags) == 1 and tags[0] == "general"):
                issues.append(LintIssue(
                    issue_type="invalid_tag",
                    severity="low",
                    title=f"标签不明确: {kp.get('title', 'unknown')}",
                    description=f"Knowledge point '{kp.get('title')}' 标签不明确或只有 general",
                    related_items=[kp.get("title", "")],
                    suggestion="使用更具体的标签"
                ))
            
            # 检查可信度
            confidence = kp.get("confidence", "medium")
            if confidence not in ["high", "medium", "low"]:
                issues.append(LintIssue(
                    issue_type="invalid_tag",
                    severity="low",
                    title=f"无效可信度: {kp.get('title', 'unknown')}",
                    description=f"可信度 '{confidence}' 不是有效值",
                    related_items=[kp.get("title", "")],
                    suggestion="可信度应该是 high/medium/low 之一"
                ))
        
        return issues


class LintPipeline:
    """
    Karpathy Lint Pipeline
    
    流程:
    1. 解析 knowledge points 文件
    2. 质量检查
    3. 去重检测
    4. 生成健康报告
    """
    
    def __init__(self, kp_path: str = None):
        self.kp_path = Path(kp_path) if kp_path else Path(__file__).parent.parent.parent / "knowledge" / "knowledge-points"
        self.parser = KnowledgePointParser(str(self.kp_path))
        self.dedup = Deduplicator()
        self.quality_checker = QualityChecker()
    
    async def run_lint(self) -> LintReport:
        """
        执行 Lint 检查
        
        Returns:
            LintReport
        """
        # 1. 解析 knowledge points
        points = self.parser.parse_kp_file()
        
        if not points:
            return LintReport(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
                total_points=0,
                issues_found=0,
                issues=[],
                stats={"status": "No knowledge points found"}
            )
        
        # 2. 质量检查
        quality_issues = self.quality_checker.check(points)
        
        # 3. 去重检测
        duplicates = self.dedup.find_duplicates(points)
        dup_issues = []
        for i, j, score in duplicates:
            dup_issues.append(LintIssue(
                issue_type="duplicate",
                severity="high",
                title=f"重复知识点: {points[i].get('title')} ≈ {points[j].get('title')}",
                description=f"相似度 {score:.2f}",
                related_items=[points[i].get("title", ""), points[j].get("title", "")],
                suggestion="合并或删除重复条目"
            ))
        
        # 4. 统计
        all_issues = quality_issues + dup_issues
        tag_counts = {}
        confidence_counts = {"high": 0, "medium": 0, "low": 0}
        
        for kp in points:
            for tag in kp.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            conf = kp.get("confidence", "medium")
            if conf in confidence_counts:
                confidence_counts[conf] += 1
        
        stats = {
            f"标签分布 ({len(tag_counts)} 种)": ", ".join([f"{k}:{v}" for k, v in tag_counts.items()]),
            f"可信度分布": f"high:{confidence_counts['high']}, medium:{confidence_counts['medium']}, low:{confidence_counts['low']}",
            f"重复检测": f"{len(duplicates)} 对",
        }
        
        return LintReport(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            total_points=len(points),
            issues_found=len(all_issues),
            issues=all_issues,
            stats=stats
        )
    
    async def fix_duplicates(self, points: List[Dict[str, Any]], duplicates: List[Tuple[int, int, float]]) -> List[Dict[str, Any]]:
        """
        修复重复的 knowledge points
        策略：保留第一个，标记后续为删除
        """
        indices_to_remove = set()
        
        for i, j, score in duplicates:
            if score >= 0.9:  # 高度重复，删除第二个
                indices_to_remove.add(j)
            elif score >= 0.7:  # 中度重复，合并
                # 保留 i，内容合并到 i
                if points[j].get("detailed_explanation"):
                    sep = " " if not points[i].get("detailed_explanation") else ". "
                    points[i]["detailed_explanation"] += sep + points[j]["detailed_explanation"]
                indices_to_remove.add(j)
        
        # 返回保留的 points
        return [p for idx, p in enumerate(points) if idx not in indices_to_remove]


async def main():
    """测试 Lint Pipeline"""
    print("=== Phase 3: Lint Pipeline Test ===")
    
    pipeline = LintPipeline()
    
    # 执行 lint
    report = await pipeline.run_lint()
    
    print(f"\n[RESULT] Knowledge Points: {report.total_points}")
    print(f"[RESULT] Issues Found: {report.issues_found}")
    
    if report.issues:
        print("\n[ISSUES]")
        for issue in report.issues:
            print(f"  [{issue.severity}] {issue.title}")
            print(f"    {issue.description}")
    
    # 保存报告
    report_path = pipeline.kp_path / "lint-report.md"
    report_path.write_text(report.to_markdown(), encoding="utf-8")
    print(f"\n[INFO] Report saved to {report_path}")
    
    print("\n=== Phase 3 Test Complete ===")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

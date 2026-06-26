#!/usr/bin/env python3
"""
质量审计器 - 自动检测章节质量
节奏分析、对话质量、描写密度、连续性一致性
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class QualityAuditor:
    """质量审计器 - 自动化章节质量检测"""

    def __init__(self, project_path: str):
        """
        初始化质量审计器

        Args:
            project_path: 项目路径
        """
        self.project_path = Path(project_path)

    def audit_chapter(self, chapter: int, content: str,
                      style_profile: str = "default") -> Dict[str, Any]:
        """
        对章节进行质量审计，输出 health_score

        Args:
            chapter: 章节编号
            content: 章节正文
            style_profile: 风格配置名称

        Returns:
            审计报告（含 health_score 0-100）
        """
        report = {
            "chapter": chapter,
            "health_score": 0,
            "dimensions": {},
            "issues": [],
            "suggestions": []
        }

        # 1. 节奏审计
        rhythm = self._audit_rhythm(content)
        report["dimensions"]["rhythm"] = rhythm

        # 2. 对话审计
        dialogue = self._audit_dialogue(content)
        report["dimensions"]["dialogue"] = dialogue

        # 3. 描写审计
        description = self._audit_description(content)
        report["dimensions"]["description"] = description

        # 4. 重复性审计
        repetition = self._audit_repetition(content)
        report["dimensions"]["repetition"] = repetition

        # 5. 连续性审计（如果项目数据存在）
        continuity = self._audit_continuity(chapter, content)
        report["dimensions"]["continuity"] = continuity

        # 6. 追读力审计（如果engagement数据存在）
        engagement = self._audit_engagement(chapter, content)
        report["dimensions"]["engagement"] = engagement

        # 计算总分
        scores = []
        for dim_name, dim_data in report["dimensions"].items():
            if "score" in dim_data:
                scores.append(dim_data["score"])

        report["health_score"] = round(sum(scores) / len(scores), 1) if scores else 0

        return report

    def _audit_rhythm(self, content: str) -> Dict[str, Any]:
        """节奏审计"""
        result = {"score": 0, "issues": [], "metrics": {}}

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        if not paragraphs:
            result["score"] = 0
            result["issues"].append("章节内容为空")
            return result

        para_lengths = [len(p) for p in paragraphs]
        avg_len = sum(para_lengths) / len(para_lengths)

        # 检查节奏变化
        length_changes = []
        for i in range(1, len(para_lengths)):
            if para_lengths[i] == 0:
                continue
            ratio = para_lengths[i] / max(para_lengths[i - 1], 1)
            length_changes.append(ratio)

        # 节奏变化评分
        if length_changes:
            variance = sum((r - 1) ** 2 for r in length_changes) / len(length_changes)
            rhythm_variety = min(variance, 1.0)
        else:
            rhythm_variety = 0

        # 对话密度
        dialogue_count = len(re.findall(r'["""].+?["""]|「.+?」|".+?"', content))
        dialogue_ratio = dialogue_count / len(paragraphs) if paragraphs else 0

        # 战斗/紧张场景密度
        tension_keywords = ["战斗", "交锋", "杀", "危险", "逃", "追", "突袭", "对峙"]
        tension_count = sum(content.count(kw) for kw in tension_keywords)

        result["metrics"] = {
            "paragraph_count": len(paragraphs),
            "avg_paragraph_length": round(avg_len, 1),
            "rhythm_variety": round(rhythm_variety, 3),
            "dialogue_ratio": round(dialogue_ratio, 2),
            "tension_density": tension_count
        }

        # 评分
        score = 70

        # 节奏变化加分
        if rhythm_variety > 0.3:
            score += 10
        elif rhythm_variety < 0.05:
            score -= 10
            result["issues"].append("段落长度过于均匀，缺乏节奏变化")

        # 对话比例
        if 0.2 <= dialogue_ratio <= 0.5:
            score += 10
        elif dialogue_ratio > 0.7:
            score -= 5
            result["issues"].append("对话比例过高，叙事薄弱")
        elif dialogue_ratio < 0.1:
            result["suggestions"] = result.get("suggestions", [])
            result["suggestions"].append("可适当增加对话以活跃节奏")

        # 段落长度
        if avg_len < 30:
            score -= 5
            result["issues"].append("段落过短，可能缺乏细节")
        elif avg_len > 300:
            score -= 5
            result["issues"].append("段落过长，建议适当拆分")

        result["score"] = max(0, min(100, score))
        return result

    def _audit_dialogue(self, content: str) -> Dict[str, Any]:
        """对话审计"""
        result = {"score": 0, "issues": [], "metrics": {}}

        # 提取对话
        dialogues = re.findall(r'["""].+?["""]|「.+?」|".+?"', content)

        if not dialogues:
            result["score"] = 50
            result["metrics"]["dialogue_count"] = 0
            return result

        # 对话长度分布
        dialogue_lengths = [len(d) for d in dialogues]
        avg_dialogue_len = sum(dialogue_lengths) / len(dialogue_lengths)

        # 检测对话标签多样性
        tags = re.findall(r'(说道|道|问|答|喊|叫|低声|怒道|笑道|冷哼|叹息|嘟囔)', content)
        unique_tags = set(tags)

        # 检测连续对话（超过5轮无叙事穿插）
        consecutive_dialogues = 0
        max_consecutive = 0
        lines = content.split("\n")
        for line in lines:
            if re.search(r'["""].+?["""]|「.+?」|".+?"', line):
                consecutive_dialogues += 1
                max_consecutive = max(max_consecutive, consecutive_dialogues)
            elif line.strip():
                consecutive_dialogues = 0

        result["metrics"] = {
            "dialogue_count": len(dialogues),
            "avg_dialogue_length": round(avg_dialogue_len, 1),
            "tag_variety": len(unique_tags),
            "max_consecutive": max_consecutive
        }

        # 评分
        score = 70

        if len(unique_tags) >= 5:
            score += 10
        elif len(unique_tags) <= 2:
            score -= 10
            result["issues"].append(f"对话标签单一（仅{len(unique_tags)}种），建议丰富表达")

        if max_consecutive > 8:
            score -= 10
            result["issues"].append(f"连续对话{max_consecutive}轮，缺少叙事穿插")
        elif max_consecutive > 5:
            result["suggestions"] = result.get("suggestions", [])
            result["suggestions"].append("连续对话较长，可考虑穿插角色动作描写")

        result["score"] = max(0, min(100, score))
        return result

    def _audit_description(self, content: str) -> Dict[str, Any]:
        """描写审计"""
        result = {"score": 0, "issues": [], "metrics": {}}

        total_chars = len(content)
        if total_chars == 0:
            result["score"] = 0
            return result

        # 感官描写
        senses = {
            "视觉": ["看到", "望去", "映入", "眼前", "目光", "视线", "颜色", "光"],
            "听觉": ["听到", "声音", "响", "鸣", "回荡", "低沉", "清脆"],
            "触觉": ["触碰", "冰凉", "灼热", "柔软", "粗糙", "温度"],
            "嗅觉": ["闻到", "气味", "芳香", "腥", "腐朽"],
            "味觉": ["品尝", "苦涩", "甘甜", "咸", "酸"]
        }

        sense_counts = {}
        for sense, keywords in senses.items():
            count = sum(content.count(kw) for kw in keywords)
            sense_counts[sense] = count

        # 环境描写
        env_keywords = ["天空", "大地", "山林", "河流", "风", "雨", "雪", "云", "月光", "阳光"]
        env_count = sum(content.count(kw) for kw in env_keywords)

        # 心理描写
        psych_keywords = ["心想", "暗道", "思量", "犹豫", "纠结", "忐忑", "内心", "心底", "不禁"]
        psych_count = sum(content.count(kw) for kw in psych_keywords)

        result["metrics"] = {
            "sense_distribution": sense_counts,
            "env_description_density": round(env_count / total_chars * 1000, 2),
            "psych_description_density": round(psych_count / total_chars * 1000, 2)
        }

        # 评分
        score = 70

        used_senses = sum(1 for v in sense_counts.values() if v > 0)
        if used_senses >= 4:
            score += 15
        elif used_senses >= 2:
            score += 5
        elif used_senses <= 1:
            score -= 10
            result["issues"].append(f"感官描写单一（仅{used_senses}种感官），建议丰富描写维度")

        if env_count == 0:
            score -= 5
            result["issues"].append("缺少环境描写")

        if psych_count == 0:
            result["suggestions"] = result.get("suggestions", [])
            result["suggestions"].append("可增加角色内心描写以深化人物")

        result["score"] = max(0, min(100, score))
        return result

    def _audit_repetition(self, content: str) -> Dict[str, Any]:
        """重复性审计"""
        result = {"score": 0, "issues": [], "metrics": {}}

        # 检测高频重复短语
        try:
            import jieba
            words = list(jieba.cut(content))
            words = [w.strip() for w in words if w.strip() and len(w.strip()) > 1]
        except ImportError:
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', content)

        from collections import Counter
        word_counts = Counter(words)
        total = len(words) if words else 1

        # 重复率（出现3次以上的词占比）
        repeated_words = {w: c for w, c in word_counts.items() if c >= 3}
        repeated_ratio = sum(repeated_words.values()) / total if total else 0

        # 句式重复检测
        sentences = re.split(r'[。！？]', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]

        # 检测句首重复
        starts = [s[:4] for s in sentences if len(s) >= 4]
        start_counts = Counter(starts)
        repeated_starts = {s: c for s, c in start_counts.items() if c >= 3}

        result["metrics"] = {
            "repeated_ratio": round(repeated_ratio, 3),
            "top_repeated_words": word_counts.most_common(10),
            "repeated_sentence_starts": repeated_starts
        }

        # 评分
        score = 80

        if repeated_ratio > 0.3:
            score -= 20
            result["issues"].append(f"词汇重复率过高({repeated_ratio:.1%})")
        elif repeated_ratio > 0.2:
            score -= 10
            result["issues"].append(f"词汇重复率偏高({repeated_ratio:.1%})")

        if repeated_starts:
            score -= len(repeated_starts) * 5
            result["issues"].append(f"存在{len(repeated_starts)}种句首重复模式")

        result["score"] = max(0, min(100, score))
        return result

    def _audit_continuity(self, chapter: int, content: str) -> Dict[str, Any]:
        """连续性审计（简化版）"""
        result = {"score": 0, "issues": [], "metrics": {}}

        db_path = self.project_path / "data" / "novel_memory.db"
        if not db_path.exists():
            result["score"] = 80
            result["metrics"]["note"] = "无项目数据，跳过连续性检查"
            return result

        try:
            from continuity_checker import ContinuityChecker
            checker = ContinuityChecker(str(self.project_path))
            try:
                check_result = checker.check_chapter(chapter, content)

                if check_result.get("passed", True):
                    result["score"] = 100
                else:
                    result["score"] = 60
                    for issue in check_result.get("issues", []):
                        result["issues"].append(f"[{issue.get('severity', '?')}] {issue.get('message', '')}")

                result["metrics"]["issue_count"] = len(check_result.get("issues", []))
                result["metrics"]["warning_count"] = len(check_result.get("warnings", []))
            finally:
                checker.close()

        except Exception as e:
            result["score"] = 70
            result["metrics"]["error"] = str(e)

        return result

    def _audit_engagement(self, chapter: int, content: str) -> Dict[str, Any]:
        """追读力审计"""
        result = {"score": 0, "issues": [], "metrics": {}}

        db_path = self.project_path / "data" / "novel_memory.db"
        if not db_path.exists():
            result["score"] = 80
            result["metrics"]["note"] = "无项目数据，跳过追读力检查"
            return result

        try:
            from engagement_tracker import EngagementTracker
            tracker = EngagementTracker(str(db_path))
            try:
                score_data = tracker.get_chapter_score(chapter)
                if not score_data:
                    result["score"] = 75
                    result["metrics"]["note"] = "该章节尚未评分"
                    return result

                # 基于评分的审计
                engagement_score = score_data.get("engagement_score", 5.0)
                hook_strength = score_data.get("hook_strength", 5.0)
                reader_pull = score_data.get("reader_pull", 5.0)
                pace_type = score_data.get("pace_type")

                result["metrics"] = {
                    "engagement_score": engagement_score,
                    "hook_strength": hook_strength,
                    "reader_pull": reader_pull,
                    "pace_type": pace_type
                }

                score = 80

                # 低投入度
                if engagement_score is not None and engagement_score < 4.0:
                    score -= 15
                    result["issues"].append(f"读者投入度偏低({engagement_score:.1f}/10)")
                elif engagement_score is not None and engagement_score < 5.0:
                    score -= 5
                    result["issues"].append("读者投入度一般，建议增强叙事张力")

                # 伏笔钩力缺失（非relief/transition章节）
                if hook_strength is not None and hook_strength < 3.0 and pace_type not in ("relief", "transition"):
                    score -= 10
                    result["issues"].append("缺少伏笔钩力，非缓冲章节建议种埋伏笔或推进悬念")

                # 综合拉力
                if reader_pull is not None and reader_pull < 4.0:
                    score -= 10
                    result["issues"].append(f"读者拉力不足({reader_pull:.1f}/10)")

                result["score"] = max(0, min(100, score))
            finally:
                tracker.close()
        except Exception as e:
            result["score"] = 75
            result["metrics"]["error"] = str(e)

        return result

    def generate_improvement_suggestions(self, report: Dict[str, Any]) -> str:
        """生成改进建议文本"""
        lines = [
            f"## 第{report['chapter']}章质量审计报告",
            f"**健康度: {report['health_score']}/100**",
            ""
        ]

        for dim_name, dim_data in report.get("dimensions", {}).items():
            dim_names = {
                "rhythm": "节奏",
                "dialogue": "对话",
                "description": "描写",
                "repetition": "重复性",
                "continuity": "连续性",
                "engagement": "追读力"
            }
            name = dim_names.get(dim_name, dim_name)
            score = dim_data.get("score", 0)
            lines.append(f"### {name}: {score}/100")

            for issue in dim_data.get("issues", []):
                lines.append(f"- [问题] {issue}")
            for suggestion in dim_data.get("suggestions", []):
                lines.append(f"- [建议] {suggestion}")
            lines.append("")

        return "\n".join(lines)


    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

    def _read_chapter_content(self, chapter: int) -> str:
        """从数据库读取指定章节的所有场景内容"""
        db_path = self.project_path / "data" / "novel_memory.db"
        if not db_path.exists():
            return ""
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT content FROM scenes_content WHERE chapter = ? ORDER BY id",
                    (chapter,))
                rows = cur.fetchall()
                return "\n".join(row["content"] for row in rows if row["content"])
            finally:
                conn.close()
        except Exception:
            return ""

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action in ("audit", "audit-file"):
            content = params.get("content", "")
            content_file = params.get("content_file")
            if content_file:
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            chapter = int(params.get("chapter", 0))
            # 自动从数据库读取章节内容（当未提供content时）
            if not content:
                content = self._read_chapter_content(chapter)
                if not content:
                    return {"error": "需要提供章节正文(content)，或该章节尚未存储"}
            return self.audit_chapter(
                chapter,
                content,
                params.get("style_profile", "default")
            )

        elif action == "suggestions":
            content = params.get("content", "")
            content_file = params.get("content_file")
            if content_file:
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            chapter = int(params.get("chapter", 0))
            # 自动从数据库读取章节内容（当未提供content时）
            if not content:
                content = self._read_chapter_content(chapter)
                if not content:
                    return {"error": "需要提供章节正文(content)，或该章节尚未存储"}
            report = self.audit_chapter(
                chapter,
                content,
                params.get("style_profile", "default")
            )
            text = self.generate_improvement_suggestions(report)
            return {"suggestions": text}

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='质量审计器')
    parser.add_argument('--project-path', required=True, help='项目路径')
    parser.add_argument('--action', required=True,
                       choices=['audit', 'audit-file', 'suggestions'],
                       help='操作类型')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--content', help='章节正文')
    parser.add_argument('--content-file', help='章节正文文件')
    parser.add_argument('--style-profile', default='default', help='风格配置')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    auditor = QualityAuditor(args.project_path)

    skip_keys = {"project_path", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if v is not None and k not in skip_keys and not k.startswith('_')}
    result = auditor.execute_action(args.action, params)
    if args.output == 'text' and args.action == 'suggestions':
        print(result.get("suggestions", json.dumps(result, ensure_ascii=False, indent=2, default=str)))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()

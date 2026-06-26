#!/usr/bin/env python3
"""
Knowledge Internalizer Pro - 知识内化助手脚本

功能：
1. 计算能力评级综合分数
2. 生成能力评估报告
3. 创建知识库目录结构
"""

import json
import os
from datetime import datetime
from pathlib import Path


def calculate_capability_score(breadth: float, depth: float, 
                               confidence: float, structure: float) -> dict:
    """
    计算能力评级综合分数
    
    权重：
    - 广度：25%
    - 深度：30%
    - 置信度：25%
    - 结构化：20%
    """
    weights = {
        "breadth": 0.25,
        "depth": 0.30,
        "confidence": 0.25,
        "structure": 0.20
    }
    
    composite = (
        breadth * weights["breadth"] +
        depth * weights["depth"] +
        confidence * weights["confidence"] +
        structure * weights["structure"]
    )
    
    return {
        "breadth": breadth,
        "depth": depth,
        "confidence": confidence,
        "structure": structure,
        "composite": round(composite, 1),
        "weights": weights
    }


def determine_level(score: float) -> dict:
    """
    根据综合分数确定能力等级
    """
    if score >= 85:
        return {
            "level": 4,
            "name": "专家级",
            "description": "可处理前沿问题、参与深度辩论、指出潜在谬误"
        }
    elif score >= 70:
        return {
            "level": 3,
            "name": "深度掌握",
            "description": "可讨论技术细节、分析优劣、进行初步推理和设计"
        }
    elif score >= 50:
        return {
            "level": 2,
            "name": "系统理解",
            "description": "可梳理逻辑、对比方案、解答常见问题"
        }
    elif score >= 30:
        return {
            "level": 1,
            "name": "概念入门",
            "description": "可解释基本术语和宏观框架"
        }
    else:
        return {
            "level": 0,
            "name": "需要进一步学习",
            "description": "知识覆盖不足，建议继续学习"
        }


def create_knowledge_dir(base_path: str, topic_slug: str) -> dict:
    """
    创建知识库目录结构
    """
    knowledge_dir = Path(base_path) / "memory" / "knowledge" / topic_slug
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        "path": str(knowledge_dir),
        "files": {
            "knowledge_graph": str(knowledge_dir / "knowledge_graph.json"),
            "knowledge_framework": str(knowledge_dir / "knowledge_framework.md"),
            "qa_pairs": str(knowledge_dir / "qa_pairs.json"),
            "capability_report": str(knowledge_dir / "capability_report.md")
        }
    }


def generate_capability_report(topic: str, scores: dict, 
                                level: dict, capabilities: dict,
                                limitations: dict, suggestions: list) -> str:
    """
    生成能力评估报告Markdown
    """
    template = f"""# 📊 能力评估报告：{topic}

## 综合评分

| 维度 | 分数 | 说明 |
|------|------|------|
| 广度 | {scores['breadth']}/100 | {capabilities.get('breadth_note', '')} |
| 深度 | {scores['depth']}/100 | {capabilities.get('depth_note', '')} |
| 置信度 | {scores['confidence']}/100 | {capabilities.get('confidence_note', '')} |
| 结构化 | {scores['structure']}/100 | {capabilities.get('structure_note', '')} |

**综合分数**：{scores['composite']}/100

## 能力等级

**等级{level['level']}：{level['name']}**

{level['description']}

## 能力边界声明

✅ **我能做到**：
{chr(10).join(f"- {c}" for c in capabilities.get('can_do', []))}

⚠️ **能力有限**：
{chr(10).join(f"- {l}" for l in limitations.get('limited', []))}

❌ **建议咨询专家**：
{chr(10).join(f"- {l}" for l in limitations.get('expert_needed', []))}

## 后续学习建议

{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(suggestions))}

---
*生成时间：{datetime.now().isoformat()}*
"""
    return template


def slugify_topic(topic: str) -> str:
    """
    将主题转换为文件系统友好的slug
    """
    # 简单实现：小写、替换空格为下划线、移除特殊字符
    slug = topic.lower()
    slug = slug.replace(" ", "_")
    slug = slug.replace("，", "_")
    slug = slug.replace("/", "_")
    # 只保留字母、数字、下划线、中文
    slug = "".join(c for c in slug if c.isalnum() or c == "_" or "\u4e00" <= c <= "\u9fff")
    return slug


if __name__ == "__main__":
    # 测试示例
    scores = calculate_capability_score(85, 70, 88, 90)
    level = determine_level(scores["composite"])
    
    print(json.dumps({
        "scores": scores,
        "level": level
    }, indent=2, ensure_ascii=False))

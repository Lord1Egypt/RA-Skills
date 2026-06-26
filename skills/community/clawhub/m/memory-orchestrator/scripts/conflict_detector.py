#!/usr/bin/env python3
"""
Conflict Detector for Memory System
计算记忆片段间的语义相似度，识别潜在冲突（如相反结论），生成冲突报告
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

import torch
from sentence_transformers import SentenceTransformer
import numpy as np

# 冲突关键词模式
CONFLICT_PATTERNS = {
    'negation': [
        # (positive_pattern, negative_pattern) - 分别匹配后比较
        (r'需要\s*(\S+)', r'不需要\s*(\S+)'),
        (r'必须\s*(\S+)', r'不必\s*(\S+)'),
        (r'已\s*(\S+)', r'未\s*(\S+)'),
        (r'确认\s*(\S+)', r'否认\s*(\S+)'),
        (r'下载\s*(\S+)', r'未下载\s*(\S+)'),
    ],
    'status_change': [
        ('✅', '❌'),
        ('⏳', '✅'),
        ('❌', '✅'),
    ],
    'opposite': [
        ('已安装', '未安装'),
        ('已下载', '未下载'),
        ('需要', '不需要'),
        ('确认', '否认'),
        ('成功', '失败'),
        ('正确', '错误'),
        ('完成', '未完成'),
    ]
}

# 语义冲突阈值
SIMILARITY_THRESHOLD = 0.75  # 高相似度阈值
CONFLICT_THRESHOLD = 0.3     # 低相似度但同主题可能冲突


@dataclass
class MemorySegment:
    """记忆片段"""
    id: str
    content: str
    source: str
    line_number: int
    timestamp: str = ""
    embedding: np.ndarray = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'source': self.source,
            'line_number': self.line_number,
            'timestamp': self.timestamp
        }


@dataclass
class Conflict:
    """冲突记录"""
    id: str
    type: str
    severity: str  # high, medium, low
    segment1: MemorySegment
    segment2: MemorySegment
    similarity: float
    reason: str
    suggestion: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'severity': self.severity,
            'segment1': self.segment1.to_dict(),
            'segment2': self.segment2.to_dict(),
            'similarity': self.similarity,
            'reason': self.reason,
            'suggestion': self.suggestion
        }


class ConflictDetector:
    """记忆冲突检测器"""
    
    def __init__(self, workspace_path: str, model_name: str = 'all-MiniLM-L6-v2'):
        self.workspace_path = Path(workspace_path)
        self.model_name = model_name
        self.model = None
        self.segments: List[MemorySegment] = []
        self.conflicts: List[Conflict] = []
        
    def load_model(self):
        """加载嵌入模型"""
        # 优先使用本地模型
        local_model_path = self.workspace_path / 'skills' / 'local-memory' / 'models'
        if local_model_path.exists():
            model_path = local_model_path / self.model_name
            if model_path.exists():
                print(f"📦 加载本地模型: {model_path}")
                self.model = SentenceTransformer(str(model_path))
                return
        
        print(f"📦 加载模型: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
    
    def extract_segments(self, content: str, source: str) -> List[MemorySegment]:
        """从内容中提取记忆片段"""
        segments = []
        lines = content.split('\n')
        
        segment_id = 0
        current_segment = []
        segment_start = 0
        
        for i, line in enumerate(lines):
            # 新片段开始的标记
            if re.match(r'^#{1,3}\s', line) or re.match(r'^###?\s+\d{2}:\d{2}', line):
                # 保存之前的片段
                if current_segment:
                    segment_text = '\n'.join(current_segment).strip()
                    if len(segment_text) > 20:  # 忽略太短的片段
                        segments.append(MemorySegment(
                            id=f"{source}:{segment_id}",
                            content=segment_text,
                            source=source,
                            line_number=segment_start
                        ))
                        segment_id += 1
                
                current_segment = [line]
                segment_start = i + 1
            else:
                current_segment.append(line)
        
        # 保存最后一个片段
        if current_segment:
            segment_text = '\n'.join(current_segment).strip()
            if len(segment_text) > 20:
                segments.append(MemorySegment(
                    id=f"{source}:{segment_id}",
                    content=segment_text,
                    source=source,
                    line_number=segment_start
                ))
        
        return segments
    
    def load_memory_files(self):
        """加载所有记忆文件"""
        # 加载 MEMORY.md
        memory_file = self.workspace_path / 'MEMORY.md'
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.segments.extend(self.extract_segments(content, 'MEMORY.md'))
        
        # 加载 memory/*.md
        memory_dir = self.workspace_path / 'memory'
        if memory_dir.exists():
            for md_file in sorted(memory_dir.glob('*.md')):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.segments.extend(self.extract_segments(content, md_file.name))
        
        print(f"📄 加载了 {len(self.segments)} 个记忆片段")
    
    def compute_embeddings(self):
        """计算所有片段的嵌入向量"""
        if not self.model:
            self.load_model()
        
        contents = [seg.content for seg in self.segments]
        embeddings = self.model.encode(contents, show_progress_bar=True)
        
        for seg, emb in zip(self.segments, embeddings):
            seg.embedding = emb
        
        print(f"🔢 计算了 {len(embeddings)} 个嵌入向量")
    
    def detect_pattern_conflicts(self, seg1: MemorySegment, seg2: MemorySegment) -> Tuple[bool, str]:
        """检测模式冲突"""
        for pattern_type, patterns in CONFLICT_PATTERNS.items():
            if pattern_type == 'negation':
                for pos_pattern, neg_pattern in patterns:
                    # 在两个片段中分别匹配
                    pos_match1 = re.search(pos_pattern, seg1.content, re.IGNORECASE)
                    neg_match2 = re.search(neg_pattern, seg2.content, re.IGNORECASE)
                    
                    if pos_match1 and neg_match2:
                        # 比较匹配的内容是否相同
                        if pos_match1.group(1).lower() == neg_match2.group(1).lower():
                            return True, f"发现否定冲突: '{pos_match1.group()}' vs '{neg_match2.group()}'"
                    
                    # 反向检测
                    pos_match2 = re.search(pos_pattern, seg2.content, re.IGNORECASE)
                    neg_match1 = re.search(neg_pattern, seg1.content, re.IGNORECASE)
                    
                    if pos_match2 and neg_match1:
                        if pos_match2.group(1).lower() == neg_match1.group(1).lower():
                            return True, f"发现否定冲突: '{neg_match1.group()}' vs '{pos_match2.group()}'"
            
            elif pattern_type == 'status_change':
                for pos_status, neg_status in patterns:
                    if pos_status in seg1.content and neg_status in seg2.content:
                        return True, f"发现状态冲突: '{pos_status}' vs '{neg_status}'"
                    if neg_status in seg1.content and pos_status in seg2.content:
                        return True, f"发现状态冲突: '{neg_status}' vs '{pos_status}'"
            
            elif pattern_type == 'opposite':
                for pos_word, neg_word in patterns:
                    if pos_word in seg1.content and neg_word in seg2.content:
                        return True, f"发现对立词汇: '{pos_word}' vs '{neg_word}'"
                    if neg_word in seg1.content and pos_word in seg2.content:
                        return True, f"发现对立词汇: '{neg_word}' vs '{pos_word}'"
        
        return False, ""
    
    def compute_similarity(self, seg1: MemorySegment, seg2: MemorySegment) -> float:
        """计算两个片段的语义相似度"""
        if seg1.embedding is None or seg2.embedding is None:
            return 0.0
        
        emb1 = seg1.embedding / np.linalg.norm(seg1.embedding)
        emb2 = seg2.embedding / np.linalg.norm(seg2.embedding)
        
        return float(np.dot(emb1, emb2))
    
    def detect_conflicts(self):
        """检测所有冲突"""
        conflict_id = 0
        
        for i in range(len(self.segments)):
            for j in range(i + 1, len(self.segments)):
                seg1 = self.segments[i]
                seg2 = self.segments[j]
                
                # 计算相似度
                similarity = self.compute_similarity(seg1, seg2)
                
                # 检测模式冲突
                has_pattern_conflict, pattern_reason = self.detect_pattern_conflicts(seg1, seg2)
                
                # 判断是否为冲突
                is_conflict = False
                conflict_type = ""
                severity = "low"
                reason = ""
                suggestion = ""
                
                if has_pattern_conflict:
                    is_conflict = True
                    conflict_type = "pattern_conflict"
                    severity = "high"
                    reason = pattern_reason
                    suggestion = f"需要人工确认：'{seg1.source}:{seg1.line_number}' 和 '{seg2.source}:{seg2.line_number}' 中的冲突内容"
                
                elif similarity > SIMILARITY_THRESHOLD:
                    # 高相似度，检查是否有细微差异
                    if seg1.content != seg2.content:
                        # 检查是否有状态变化
                        if ('✅' in seg1.content and '⏳' in seg2.content) or \
                           ('⏳' in seg1.content and '✅' in seg2.content):
                            conflict_type = "status_evolution"
                            severity = "low"
                            reason = f"状态演变（相似度: {similarity:.3f}）"
                            suggestion = "这可能是正常的状态更新，建议保留最新状态"
                            is_conflict = True
                
                elif similarity > CONFLICT_THRESHOLD and similarity < SIMILARITY_THRESHOLD:
                    # 中等相似度但不同，可能是相关但有差异的内容
                    # 检查是否涉及同一实体但有不同描述
                    entities_in_seg1 = set(re.findall(r'\b\w+模型\w*\b|\b\w+工具\w*\b', seg1.content))
                    entities_in_seg2 = set(re.findall(r'\b\w+模型\w*\b|\b\w+工具\w*\b', seg2.content))
                    
                    if entities_in_seg1 and entities_in_seg2 and entities_in_seg1 & entities_in_seg2:
                        conflict_type = "semantic_divergence"
                        severity = "medium"
                        reason = f"涉及相同实体但描述不同（相似度: {similarity:.3f}）"
                        suggestion = "检查是否为同一实体的不同视角描述"
                        is_conflict = True
                
                if is_conflict:
                    self.conflicts.append(Conflict(
                        id=f"conflict_{conflict_id}",
                        type=conflict_type,
                        severity=severity,
                        segment1=seg1,
                        segment2=seg2,
                        similarity=similarity,
                        reason=reason,
                        suggestion=suggestion
                    ))
                    conflict_id += 1
        
        print(f"⚠️ 检测到 {len(self.conflicts)} 个潜在冲突")
    
    def generate_report(self, output_path: str) -> dict:
        """生成冲突报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_segments': len(self.segments),
            'total_conflicts': len(self.conflicts),
            'conflict_summary': {
                'high': len([c for c in self.conflicts if c.severity == 'high']),
                'medium': len([c for c in self.conflicts if c.severity == 'medium']),
                'low': len([c for c in self.conflicts if c.severity == 'low'])
            },
            'conflicts': [c.to_dict() for c in sorted(self.conflicts, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x.severity])]
        }
        
        # 保存报告
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📋 冲突报告已生成: {output_path}")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='检测记忆系统冲突')
    parser.add_argument('--workspace', '-w',
                       default='/home/claw/.openclaw/workspace',
                       help='工作空间路径')
    parser.add_argument('--output', '-o',
                       default='memory/state/conflict_report.json',
                       help='输出报告路径')
    parser.add_argument('--model', '-m',
                       default='all-MiniLM-L6-v2',
                       help='嵌入模型名称')
    
    args = parser.parse_args()
    
    print("🔍 开始冲突检测...")
    
    detector = ConflictDetector(args.workspace, args.model)
    detector.load_model()
    detector.load_memory_files()
    detector.compute_embeddings()
    detector.detect_conflicts()
    
    report_path = Path(args.workspace) / args.output
    report = detector.generate_report(str(report_path))
    
    print(f"\n📊 检测结果:")
    print(f"  - 总片段数: {report['total_segments']}")
    print(f"  - 总冲突数: {report['total_conflicts']}")
    print(f"  - 高严重性: {report['conflict_summary']['high']}")
    print(f"  - 中严重性: {report['conflict_summary']['medium']}")
    print(f"  - 低严重性: {report['conflict_summary']['low']}")
    
    return report


if __name__ == '__main__':
    main()

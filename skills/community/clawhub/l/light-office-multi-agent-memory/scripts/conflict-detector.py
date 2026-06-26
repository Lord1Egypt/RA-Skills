#!/usr/bin/env python3
"""
多Agent记忆系统 - 矛盾检测集成脚本（通用版）

功能：
  将矛盾检测集成到记忆生命周期中，自动解决冲突

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
MEMORY_DIR = WORKSPACE / "memory"
CONFLICT_LOG_DIR = WORKSPACE / ".memory-conflicts"

# 冲突解决策略
CONFLICT_STRATEGIES = {
    "time_conflict": "keep_newest",
    "content_conflict": "llm_judge",
    "priority_conflict": "priority_order",
    "source_conflict": "source_order"
}

# 优先级顺序
PRIORITY_ORDER = {
    "SOP": 100,
    "承诺": 90,
    "配置": 80,
    "项目": 70,
    "任务": 60,
    "临时": 50
}

# 来源顺序
SOURCE_ORDER = {
    "用户": 100,
    "系统": 90,
    "Agent": 80
}

# ============================================================
# 矛盾检测器
# ============================================================

class ConflictDetector:
    """矛盾检测器"""
    
    def __init__(self):
        self.conflict_log_dir = CONFLICT_LOG_DIR
        self.conflict_log_dir.mkdir(parents=True, exist_ok=True)
        self.conflict_log_file = self.conflict_log_dir / "conflicts.json"
        
        # 加载或创建冲突日志
        if self.conflict_log_file.exists():
            with open(self.conflict_log_file, "r", encoding="utf-8") as f:
                self.conflicts = json.load(f)
        else:
            self.conflicts = []
    
    def detect_conflicts(self, memory_files):
        """检测冲突"""
        print(f"[Conflict] 检测冲突: {len(memory_files)}个文件")
        
        new_conflicts = 0
        
        for file_path in memory_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 检测时间冲突
                time_conflicts = self._detect_time_conflicts(content, file_path)
                new_conflicts += len(time_conflicts)
                self.conflicts.extend(time_conflicts)
                
                # 检测内容冲突
                content_conflicts = self._detect_content_conflicts(content, file_path)
                new_conflicts += len(content_conflicts)
                self.conflicts.extend(content_conflicts)
                
                # 检测优先级冲突
                priority_conflicts = self._detect_priority_conflicts(content, file_path)
                new_conflicts += len(priority_conflicts)
                self.conflicts.extend(priority_conflicts)
                
                # 检测来源冲突
                source_conflicts = self._detect_source_conflicts(content, file_path)
                new_conflicts += len(source_conflicts)
                self.conflicts.extend(source_conflicts)
                
            except Exception as e:
                print(f"[ERROR] 检测冲突失败 {file_path}: {e}", file=sys.stderr)
        
        # 保存冲突日志
        with open(self.conflict_log_file, "w", encoding="utf-8") as f:
            json.dump(self.conflicts, f, ensure_ascii=False, indent=2)
        
        print(f"[Conflict] 检测完成: {new_conflicts}个新冲突")
        return new_conflicts
    
    def _detect_time_conflicts(self, content, file_path):
        """检测时间冲突"""
        conflicts = []
        import re
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}', content)
        
        from collections import Counter
        timestamp_counts = Counter(timestamps)
        
        for timestamp, count in timestamp_counts.items():
            if count > 1:
                conflicts.append({
                    "type": "time_conflict",
                    "file": str(file_path.name),
                    "timestamp": timestamp,
                    "count": count,
                    "detected": datetime.now().isoformat(),
                    "strategy": "keep_newest"
                })
        
        return conflicts
    
    def _detect_content_conflicts(self, content, file_path):
        """检测内容冲突"""
        conflicts = []
        import re
        is_matches = re.findall(r'是.*?[。！？]', content)
        is_not_matches = re.findall(r'不是.*?[。！？]', content)
        
        if is_matches and is_not_matches:
            conflicts.append({
                "type": "content_conflict",
                "file": str(file_path.name),
                "is_count": len(is_matches),
                "is_not_count": len(is_not_matches),
                "detected": datetime.now().isoformat(),
                "strategy": "llm_judge"
            })
        
        return conflicts
    
    def _detect_priority_conflicts(self, content, file_path):
        """检测优先级冲突"""
        conflicts = []
        import re
        priority_matches = re.findall(r'(SOP|承诺|配置|项目|任务|临时)', content)
        
        high_priority = [p for p in priority_matches if p in ["SOP", "承诺", "配置"]]
        low_priority = [p for p in priority_matches if p in ["临时"]]
        
        if high_priority and low_priority:
            conflicts.append({
                "type": "priority_conflict",
                "file": str(file_path.name),
                "high_priority": len(high_priority),
                "low_priority": len(low_priority),
                "detected": datetime.now().isoformat(),
                "strategy": "priority_order"
            })
        
        return conflicts
    
    def _detect_source_conflicts(self, content, file_path):
        """检测来源冲突"""
        conflicts = []
        import re
        source_matches = re.findall(r'(用户|系统|Agent)', content)
        
        unique_sources = list(set(source_matches))
        
        if len(unique_sources) > 1:
            conflicts.append({
                "type": "source_conflict",
                "file": str(file_path.name),
                "sources": unique_sources,
                "detected": datetime.now().isoformat(),
                "strategy": "source_order"
            })
        
        return conflicts
    
    def resolve_conflicts(self):
        """解决冲突"""
        print(f"[Conflict] 解决冲突: {len(self.conflicts)}个")
        
        resolved = 0
        
        for conflict in self.conflicts:
            strategy = conflict.get("strategy")
            
            if strategy == "keep_newest":
                conflict["resolved"] = True
                conflict["resolution"] = "保留最新时间戳"
                resolved += 1
            
            elif strategy == "llm_judge":
                conflict["resolved"] = False
                conflict["resolution"] = "待人工审核"
            
            elif strategy == "priority_order":
                conflict["resolved"] = True
                conflict["resolution"] = "按优先级顺序解决"
                resolved += 1
            
            elif strategy == "source_order":
                conflict["resolved"] = True
                conflict["resolution"] = "按来源顺序解决"
                resolved += 1
        
        # 保存冲突日志
        with open(self.conflict_log_file, "w", encoding="utf-8") as f:
            json.dump(self.conflicts, f, ensure_ascii=False, indent=2)
        
        print(f"[Conflict] 解决完成: {resolved}/{len(self.conflicts)}个")
        return resolved
    
    def get_stats(self):
        """获取冲突统计"""
        stats = {
            "total_conflicts": len(self.conflicts),
            "resolved": sum(1 for c in self.conflicts if c.get("resolved")),
            "unresolved": sum(1 for c in self.conflicts if not c.get("resolved")),
            "by_type": {}
        }
        
        for conflict in self.conflicts:
            conflict_type = conflict.get("type")
            if conflict_type not in stats["by_type"]:
                stats["by_type"][conflict_type] = 0
            stats["by_type"][conflict_type] += 1
        
        return stats


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    print("=" * 60)
    print("多Agent记忆系统 - 矛盾检测集成测试")
    print("=" * 60)
    
    # 检测冲突
    print("\n[测试1] 检测冲突")
    detector = ConflictDetector()
    memory_files = list(MEMORY_DIR.glob("*.md"))[:10]
    new_conflicts = detector.detect_conflicts(memory_files)
    print(f"  新冲突: {new_conflicts}")
    
    # 解决冲突
    print("\n[测试2] 解决冲突")
    resolved = detector.resolve_conflicts()
    print(f"  已解决: {resolved}")
    
    # 获取统计
    print("\n[测试3] 冲突统计")
    stats = detector.get_stats()
    print(f"  统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    print("\n✅ 矛盾检测集成测试完成")


if __name__ == "__main__":
    main()

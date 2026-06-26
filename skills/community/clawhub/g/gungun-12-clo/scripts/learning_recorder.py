#!/usr/bin/env python3
"""
12 号滚滚 - 学习记录器
记录对话中的 learnings
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import random

class LearningRecorder:
    def __init__(self, workspace="/home/admin/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.learnings_dir = self.workspace / ".learnings"
        self.learnings_file = self.learnings_dir / "LEARNINGS.md"
        self.errors_file = self.learnings_dir / "ERRORS.md"
        self.features_file = self.learnings_dir / "FEATURE_REQUESTS.md"
        
        # 确保目录存在
        self.learnings_dir.mkdir(parents=True, exist_ok=True)
        
    def record_learning(self, category, summary, details, priority="medium", area="agent", suggested_action=""):
        """记录一条学习"""
        learning_id = self._generate_id("LRN")
        timestamp = datetime.now().isoformat()
        
        entry = f"""
### [{learning_id}] {summary}

**Logged**: {timestamp}
**Priority**: {priority}
**Status**: pending
**Area**: {area}

### Summary
{summary}

### Details
{details}

### Suggested Action
{suggested_action if suggested_action else "[待填写具体改进行动]"}

### Metadata
- Source: {category}
- Related Files: 
- Tags: {category}, {area}
- Pattern-Key: {self._generate_pattern_key(summary)}

---
"""
        with open(self.learnings_file, "a", encoding="utf-8") as f:
            f.write(entry)
            
        print(f"✅ 学习记录已创建：{learning_id}")
        return learning_id
    
    def record_error(self, error_output, context="", priority="high"):
        """记录错误"""
        error_id = self._generate_id("ERR")
        timestamp = datetime.now().isoformat()
        
        # 确保 errors 文件存在
        if not self.errors_file.exists():
            self._init_errors_file()
        
        entry = f"""
### [{error_id}] unknown_error

**Logged**: {timestamp}
**Priority**: {priority}
**Status**: pending
**Area**: backend

### Summary
命令或操作失败

### Error
```
{error_output[:500]}
```

### Context
{context}

### Suggested Fix
[待分析]

### Metadata
- Reproducible: unknown
- Tags: error, failure

---
"""
        with open(self.errors_file, "a", encoding="utf-8") as f:
            f.write(entry)
            
        print(f"❌ 错误记录已创建：{error_id}")
        return error_id
    
    def record_feature_request(self, request, user_context, complexity="medium"):
        """记录功能请求"""
        feature_id = self._generate_id("FEAT")
        timestamp = datetime.now().isoformat()
        
        # 确保 features 文件存在
        if not self.features_file.exists():
            self._init_features_file()
        
        entry = f"""
### [{feature_id}] requested_feature

**Logged**: {timestamp}
**Priority**: medium
**Status**: pending
**Area**: agent

### Requested Capability
{request}

### User Context
{user_context}

### Complexity Estimate
{complexity}

### Suggested Implementation
[待评估]

### Metadata
- Frequency: first_time
- Tags: feature_request

---
"""
        with open(self.features_file, "a", encoding="utf-8") as f:
            f.write(entry)
            
        print(f"💡 功能请求已记录：{feature_id}")
        return feature_id
    
    def _generate_id(self, prefix):
        """生成学习 ID"""
        date_str = datetime.now().strftime("%Y%m%d")
        seq = random.randint(1, 999)
        return f"{prefix}-{date_str}-{seq:03d}"
    
    def _generate_pattern_key(self, summary):
        """生成模式键"""
        words = summary.lower().split()[:3]
        return ".".join(words)[:50]
    
    def _init_errors_file(self):
        """初始化错误文件"""
        with open(self.errors_file, "w", encoding="utf-8") as f:
            f.write("# ❌ 滚滚的错误记录\n\n**创建日期：** " + datetime.now().strftime("%Y-%m-%d") + "\n\n")
    
    def _init_features_file(self):
        """初始化功能请求文件"""
        with open(self.features_file, "w", encoding="utf-8") as f:
            f.write("# 💡 滚滚的功能请求\n\n**创建日期：** " + datetime.now().strftime("%Y-%m-%d") + "\n\n")


def main():
    """命令行接口"""
    recorder = LearningRecorder()
    
    if len(sys.argv) < 2:
        print("用法：python learning_recorder.py <command> [args]")
        print("命令:")
        print("  learning <category> <summary> <details> [priority] [area]")
        print("  error <error_output> [context]")
        print("  feature <request> <context>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "learning":
        if len(sys.argv) < 5:
            print("用法：learning <category> <summary> <details> [priority] [area]")
            sys.exit(1)
        category = sys.argv[2]
        summary = sys.argv[3]
        details = sys.argv[4] if len(sys.argv) > 4 else ""
        priority = sys.argv[5] if len(sys.argv) > 5 else "medium"
        area = sys.argv[6] if len(sys.argv) > 6 else "agent"
        recorder.record_learning(category, summary, details, priority, area)
    
    elif command == "error":
        if len(sys.argv) < 3:
            print("用法：error <error_output> [context]")
            sys.exit(1)
        error_output = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        recorder.record_error(error_output, context)
    
    elif command == "feature":
        if len(sys.argv) < 4:
            print("用法：feature <request> <context>")
            sys.exit(1)
        request = sys.argv[2]
        context = sys.argv[3]
        recorder.record_feature_request(request, context)
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

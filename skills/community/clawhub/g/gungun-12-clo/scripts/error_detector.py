#!/usr/bin/env python3
"""
12 号滚滚 - 错误检测器
检测并记录错误
"""

import re
import sys
from datetime import datetime
from pathlib import Path
import random

class ErrorDetector:
    def __init__(self, workspace="/home/admin/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.errors_dir = self.workspace / ".learnings"
        self.errors_file = self.errors_dir / "ERRORS.md"
        
        # 错误模式
        self.error_patterns = [
            (r"Error:", "error"),
            (r"Exception:", "exception"),
            (r"Failed:", "failed"),
            (r"Traceback", "traceback"),
            (r"Command failed", "command_failed"),
            (r"Exit code: [1-9]", "nonzero_exit"),
            (r"not found", "not_found"),
            (r"permission denied", "permission"),
            (r"timeout", "timeout"),
            (r"connection.*failed", "connection"),
        ]
        
        # 确保目录存在
        self.errors_dir.mkdir(parents=True, exist_ok=True)
        
    def detect_error(self, output, context=""):
        """检测输出中的错误"""
        for pattern, error_type in self.error_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                return self.record_error(output, context, error_type)
        return None
    
    def record_error(self, error_output, context="", error_type="unknown"):
        """记录错误"""
        error_id = self._generate_id("ERR")
        timestamp = datetime.now().isoformat()
        
        # 确定优先级
        priority = self._determine_priority(error_type, error_output)
        
        # 确定区域
        area = self._determine_area(context)
        
        entry = f"""
### [{error_id}] {error_type}

**Logged**: {timestamp}
**Priority**: {priority}
**Status**: pending
**Area**: {area}

### Summary
{error_type.replace('_', ' ').title()} 错误

### Error
```
{error_output[:500]}
```

### Context
{context if context else "未提供上下文"}

### Suggested Fix
[待分析]

### Metadata
- Reproducible: unknown
- Error-Type: {error_type}
- Tags: error, {error_type}, {area}

---
"""
        with open(self.errors_file, "a", encoding="utf-8") as f:
            f.write(entry)
            
        print(f"❌ 检测到错误：{error_id} ({error_type})")
        return error_id
    
    def _generate_id(self, prefix):
        """生成错误 ID"""
        date_str = datetime.now().strftime("%Y%m%d")
        seq = random.randint(1, 999)
        return f"{prefix}-{date_str}-{seq:03d}"
    
    def _determine_priority(self, error_type, error_output):
        """确定错误优先级"""
        critical_types = ["permission", "connection", "timeout"]
        high_types = ["exception", "traceback", "failed"]
        
        if error_type in critical_types:
            return "critical"
        elif error_type in high_types or "critical" in error_output.lower():
            return "high"
        elif "warning" in error_output.lower():
            return "low"
        else:
            return "medium"
    
    def _determine_area(self, context):
        """确定错误所属区域"""
        context_lower = context.lower()
        
        if any(x in context_lower for x in ["frontend", "ui", "html", "css", "js"]):
            return "frontend"
        elif any(x in context_lower for x in ["backend", "api", "server", "database"]):
            return "backend"
        elif any(x in context_lower for x in ["deploy", "docker", "ci/cd", "server"]):
            return "infra"
        elif any(x in context_lower for x in ["test", "spec"]):
            return "tests"
        elif any(x in context_lower for x in ["doc", "readme", "comment"]):
            return "docs"
        else:
            return "config"


def main():
    """命令行接口"""
    detector = ErrorDetector()
    
    if len(sys.argv) < 2:
        print("用法：python error_detector.py <command> [args]")
        print("命令:")
        print("  detect <output> [context]  - 检测并记录错误")
        print("  record <error> [context]   - 直接记录错误")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "detect":
        if len(sys.argv) < 3:
            print("用法：detect <output> [context]")
            sys.exit(1)
        output = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        detector.detect_error(output, context)
    
    elif command == "record":
        if len(sys.argv) < 3:
            print("用法：record <error> [context]")
            sys.exit(1)
        error = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        detector.record_error(error, context)
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

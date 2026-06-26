#!/usr/bin/env python3
"""
Kiro Spec 创建工具

快速创建标准结构的 Kiro Spec 目录和文件模板。

用法:
    python create-spec.py <spec-name> [--path <output-dir>]

示例:
    python create-spec.py user-authentication
    python create-spec.py payment-integration --path .kiro/specs
"""

import os
import sys
import argparse
from datetime import datetime

# 模板内容
REQUIREMENTS_TEMPLATE = """# Requirements Document

## Introduction

[在此描述这个功能是什么，解决什么问题，为谁解决]

## Glossary

- **术语 1** - 定义
- **术语 2** - 定义

## Requirements

### Requirement 1: [功能名称]

**User Story:** As a [角色], I want [功能], so that [价值].

#### Acceptance Criteria

1. WHEN [条件], THE system SHALL [行为]
2. WHEN [条件], THE system SHALL [行为]
3. IF [边界条件], THE system SHALL [处理]

### Requirement 2: [功能名称]

**User Story:** As a [角色], I want [功能], so that [价值].

#### Acceptance Criteria

1. WHEN [条件], THE system SHALL [行为]
2. WHEN [条件], THE system SHALL [行为]

"""

DESIGN_TEMPLATE = """# Design Document

## Architecture Overview

[系统架构图或文字描述]

```
[可在此粘贴架构图或使用 Mermaid 语法]
```

## Technical Decisions

### Decision 1: [技术选型]

**Options Considered:**
- Option A: [优缺点]
- Option B: [优缺点]

**Decision:** [最终选择 + 理由]

## Data Models

[数据库表结构/接口定义]

```typescript
// 示例
interface User {
  id: string;
  email: string;
  // ...
}
```

## API Design

[API 端点、请求/响应格式]

```typescript
// POST /api/auth/login
// Request: { email, password }
// Response: { token, user }
```

## Security Considerations

[认证、授权、数据保护措施]

"""

TASKS_TEMPLATE = f"""# Tasks

## Implementation Plan

### Phase 1: 基础架构
- [ ] Task 1.1: [具体任务描述]
  - 文件：`src/xxx/xxx.ts`
  - 验收：通过单元测试
- [ ] Task 1.2: [具体任务描述]

### Phase 2: 核心功能
- [ ] Task 2.1: [具体任务描述]
- [ ] Task 2.2: [具体任务描述]

### Phase 3: 测试与优化
- [ ] Task 3.1: 编写集成测试
- [ ] Task 3.2: 性能优化

## Dependencies

- Task 2.1 依赖 Task 1.1 完成
- Task 3.1 依赖所有 Phase 2 任务完成

## Notes

[实现过程中的注意事项]

---

*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

def create_spec(spec_name: str, output_path: str):
    """创建 Spec 目录结构"""
    
    # 创建目录
    spec_dir = os.path.join(output_path, spec_name)
    os.makedirs(spec_dir, exist_ok=True)
    
    # 创建文件
    files = {
        'requirements.md': REQUIREMENTS_TEMPLATE,
        'design.md': DESIGN_TEMPLATE,
        'tasks.md': TASKS_TEMPLATE,
    }
    
    for filename, content in files.items():
        filepath = os.path.join(spec_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {filepath}")
    
    print(f"\n✅ Spec '{spec_name}' created successfully at {spec_dir}")
    print("\nNext steps:")
    print("1. Edit requirements.md to define user stories and acceptance criteria")
    print("2. Edit design.md to document technical decisions")
    print("3. Edit tasks.md to break down implementation tasks")
    print("4. Use Kiro agent to review and refine the spec")

def main():
    parser = argparse.ArgumentParser(description='Create a Kiro spec with standard structure')
    parser.add_argument('spec_name', help='Name of the spec (e.g., user-authentication)')
    parser.add_argument('--path', default='.kiro/specs', help='Output directory (default: .kiro/specs)')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.path, exist_ok=True)
    
    create_spec(args.spec_name, args.path)

if __name__ == '__main__':
    main()

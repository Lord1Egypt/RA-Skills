---
name: multi-agent-team
slug: multi-agent-team
description: 基于任务类型动态调度到合适的智能体角色（架构师、产品经理、测试专家、独立开发者）。支持多智能体协作、共识机制和完整项目生命周期管理。支持中英文双语。
---

# Multi-Agent Team Dispatcher   

基于任务类型和上下文，自动调度到最合适的智能体角色（架构师、产品经理、测试专家、Solo Coder）。

## 多语言支持 (Multi-Language Support)

### 语言识别规则
**自动识别用户语言**:
- 用户使用中文 → 所有响应使用中文
- 用户使用英文 → 所有响应使用英文
- 用户混合使用 → 以首次使用的语言为准
- 用户明确要求切换 → 立即切换到目标语言

### 响应语言规则
**所有输出必须使用用户相同的语言**:
- 角色定义和 Prompt
- 状态更新和进度提示
- 审查报告和问题清单
- 错误信息和成功提示
- 文档和注释

**示例**:
```
用户（中文）: "设计系统架构"
AI（中文）: "📋 已接收任务，开始分析..."

用户（English）: "Design system architecture"
AI (English): "📋 Task received, starting analysis..."
```

### 角色名称映射
**中文 → 英文**:
- 架构师 → Architect
- 产品经理 → Product Manager
- 测试专家 → Test Expert
- 独立开发者 → Solo Coder

## 核心能力

1. **智能角色调度**: 根据任务描述自动识别需要的角色
2. **多角色协同**: 组织多个角色共同完成复杂任务
3. **上下文感知**: 根据项目阶段和历史上下文选择角色
4. **共识机制**: 组织多角色评审和决策
5. **自动继续**: 思考次数超限后自动保存进度并继续执行
6. **任务管理**: 完整的任务生命周期管理和进度追踪
7. **代码地图生成**: 自动生成项目代码结构映射
8. **项目理解**: 快速读取项目文档和代码，生成项目理解文档
9. **规范驱动开发**: 基于项目规范和文档进行开发
10. **七阶段标准工作流程**: 需求分析→架构设计→测试设计→任务分解→开发实现→测试验证→发布评审

## 快速开始

### 基础使用
```bash
# 自动调度（推荐）
python3 scripts/trae_agent_dispatch.py \
    --task "设计系统架构"

# 指定角色
python3 scripts/trae_agent_dispatch.py \
    --task "实现功能" \
    --agent solo_coder

# 多角色共识
python3 scripts/trae_agent_dispatch.py \
    --task "启动新项目" \
    --consensus true
```

### 完整项目流程
```bash
# 启动完整项目（自动执行7个阶段）
python3 scripts/trae_agent_dispatch.py \
    --task "启动项目：安全浏览器广告拦截功能" \
    --project-full-lifecycle
```

## 角色介绍

### 1. 架构师 (Architect)
**职责**: 设计系统性、前瞻性、可落地、可验证的架构

**触发关键词**: 架构、设计、选型、审查、性能、瓶颈、模块、接口、部署

**典型任务**:
- 项目启动阶段的架构设计
- 关键代码的架构审查和代码评审
- 技术难题攻关和性能优化

### 2. 产品经理 (Product Manager)
**职责**: 定义用户价值清晰、需求明确、可落地、可验收的产品

**触发关键词**: 需求、PRD、用户故事、竞品、市场、调研、验收、UAT、体验

**典型任务**:
- 产品需求定义和 PRD 编写
- 用户故事地图和验收标准定义
- 竞品分析

### 3. 测试专家 (Test Expert)
**职责**: 确保全面、深入、自动化、可量化的质量保障

**触发关键词**: 测试、质量、验收、自动化、性能测试、缺陷、评审、门禁

**典型任务**:
- 测试策略制定和测试用例设计
- 自动化测试方案
- 质量评估和测试报告

### 4. 独立开发者 (Solo Coder)
**职责**: 编写完整、高质量、可维护、可测试的代码

**触发关键词**: 实现、开发、代码、修复、优化、重构、单元测试、文档

**典型任务**:
- 功能实现和单元测试编写
- 代码重构和优化
- 开发文档编写

## 七阶段标准工作流程

```
阶段 1: 需求分析（产品经理）
    ↓ 评审通过
阶段 2: 架构设计（架构师）
    ↓ 评审通过
阶段 3: 测试设计（测试专家）
    ↓ 评审通过
阶段 4: 任务分解（独立开发者）
    ↓
阶段 5: 开发实现（独立开发者）
    ↓
阶段 6: 测试验证（测试专家）
    ↓
阶段 7: 发布评审（多角色）
```

**绝对禁止**：
❌ 未经过设计阶段直接开始编码
❌ 文档未编写或未完成就开始开发
❌ 未经过设计评审直接实施

## 高级功能

### 代码地图生成
```bash
python3 scripts/code_map_generator.py /path/to/project
```

### 项目理解
```bash
python3 scripts/project_understanding.py /path/to/project
```

### 规范驱动开发
```bash
python3 scripts/spec_tools.py init
python3 scripts/spec_tools.py analyze
python3 scripts/spec_tools.py update --spec-file SPEC.md
```

## 文档结构

```
docs/
├── project-understanding/  # 项目理解文档
├── spec/                   # 规范驱动开发文档
├── architect/              # 架构师文档
├── product-manager/        # 产品经理文档
├── test-expert/            # 测试专家文档
└── solo-coder/             # 独立开发者文档
```

## 故障排查

### 角色识别错误
```bash
# 明确指定角色
python3 scripts/trae_agent_dispatch.py \
    --task "..." \
    --agent architect
```

### 共识未触发
```bash
# 显式要求共识
python3 scripts/trae_agent_dispatch.py \
    --task "..." \
    --consensus true
```

## 扩展开发

### 添加新角色
1. 在 `roles.json` 中添加角色配置
2. 更新关键词列表
3. 调整调度规则

### 自定义调度规则
修改 `AgentDispatcher.analyze_task()` 方法。

## 总结

Trae Multi-Agent Dispatcher 提供了：
- ✅ 智能角色识别
- ✅ 多角色协同
- ✅ 上下文感知
- ✅ 完整项目流程
- ✅ 紧急任务处理

通过智能调度，减少用户干预，提升协作效率！

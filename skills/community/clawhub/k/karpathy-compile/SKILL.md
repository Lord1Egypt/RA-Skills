# Karpathy Compile Skill - Phase 2

## 描述
实现 Karpathy LLM Knowledge Base 的第二阶段：Wiki → Knowledge Points 编译。

将 Phase 1 生成的 wiki 条目通过 LLM distillation 编译为结构化的知识精华（knowledge points）。

## 工作流程

```
Phase 1: 用户查询 → Wiki 条目 (raw, 多条)
Phase 2: Wiki 条目 → Knowledge Points (精炼, 结构性)
Phase 3: Lint → 去重/合并/更新
```

## Knowledge Point 格式

```markdown
## Knowledge Point: [主题]

**核心概念**: [一句话概括]
**来源**: [wiki条目来源]
**详细说明**: [LLM生成的详细解释]
**标签**: [tag1, tag2]
**创建时间**: YYYY-MM-DD
**可信度**: high/medium/low
```

## Compile Pipeline

1. 读取 wiki 文件
2. 按主题/标签分组
3. 对每组使用 LLM distillation 生成 knowledge point
4. 保存到 knowledge-points/ 目录

## 文件结构

```
karpathy-compile/
├── SKILL.md
├── scripts/
│   ├── __init__.py      # CompilePipeline
│   ├── distiller.py     # LLM distillation
│   ├── parser.py        # wiki 文件解析
│   └── test_compile.py  # 测试
└── knowledge-points/     # 输出目录
```

## 依赖
- Phase 1 的 wiki 文件
- M-Flow (用于存储编译后的 knowledge points)
- Ollama LLM (qwen2.5:14b)

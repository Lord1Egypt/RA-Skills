# Karpathy Lint Skill - Phase 3

## 描述
实现 Karpathy LLM Knowledge Base 的第三阶段：知识自检与修复。

对 Phase 2 生成的 knowledge points 进行质量检查：去重、合并、更新、删除。

## 工作流程

```
Phase 1: 用户查询 → Wiki 条目
Phase 2: Wiki → Knowledge Points (精炼)
Phase 3: Lint → 去重/合并/更新/自修复 ← 当前
Phase 4: 高级 (M-Flow 集成、多Agent共享)
```

## Lint 检查项

1. **去重 (Deduplication)**
   - 检测相似/重复的 knowledge points
   - 合并高度相似的内容

2. **更新 (Update)**
   - 检查知识点是否过期
   - 标记需要更新的条目

3. **质量检查 (Quality Check)**
   - 检查内容完整性
   - 验证标签一致性

4. **生成健康报告**
   - 当前知识库统计
   - 发现的问题列表
   - 修复建议

## 文件结构

```
karpathy-lint/
├── SKILL.md
├── scripts/
│   ├── __init__.py      # LintPipeline
│   ├── dedup.py          # 去重逻辑
│   ├── merger.py          # 合并逻辑
│   └── test_lint.py      # 测试
```

## 依赖
- Phase 2 的 knowledge points 文件
- M-Flow (可选，用于存储)

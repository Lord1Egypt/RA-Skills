# 跨多轮聚合 Schema（v0.2 新增 · R3）

协作雷达 v0.2 支持把**同一项目的多段材料**（如周一会记录 + 周三站会记录 + 多日群聊）先聚合成一张卡片，再抽取状态，避免结论割裂与待办重复。

## 聚合流程

1. 按 `project_name` / 项目标识将多段材料归为同一项目。
2. 对每段材料分别抽取 7 模块草稿（或由 `process.py enforce` 加固后的卡片）。
3. 调用 `python scripts/process.py aggregate --cards c1.json c2.json ...` 合并：
   - **行动项去重**：以 `(task, owner)` 为签名去重，保留首次出现。
   - **其他模块去重**：以结论文本（statement）为签名去重。
   - **统一输出**：保留 7 模块固定顺序，附加 `sources`（各段项目名列表）与 `aggregation_summary`。

## 聚合后 JSON 附加字段

```json
{
  "project_overview": { "...": "..." },
  "progress": [ "..." ],
  "confirmed_decisions": [ "..." ],
  "action_items": [ "..." ],
  "risks_dependencies": [ "..." ],
  "cross_department_relationships": [ "..." ],
  "needs_human_confirmation": [ "..." ],
  "sources": ["周一项目会", "周三站会"],
  "aggregation_summary": "已聚合 2 段材料，行动项去重后 3 条"
}
```

## 规则与边界

- 聚合仅做**结构级去重合并**，不做语义级消歧；同名任务不同 Owner 仍会各自保留并触发 R5 冲突标记。
- 聚合后必须再走一次 `process.py enforce`（以合并后的全部原始材料为 `--source`），确保证据、脱敏、冲突规则统一生效。
- `validate_output.py` 在检测到 `sources` 长度 > 1 时会校验 `aggregation_summary` 必须存在（R3）。
- 跨多轮聚合为基础版能力：不保证解决指代消解、时间线归并等复杂语义问题，相关增强列入后续版本。

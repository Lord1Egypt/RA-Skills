# Skill v2.5 — 2026-03-30

## Step 6 验收流程完整重写

- 新增 generate_poster 返回内容说明（render 图 / inspect 图 / 质检报告 / 高危裁图）
- 验收流程分4步：先读质检报告 → 看 render 图 → 处理 🟡 疑似 → 定位布局问题
- 新增 get_slot_crops 调用示例（用于 🟡 疑似放大查看）
- inspect 图色码说明：🔴已确认问题 🟡疑似 🟢正常 ⬜装饰/非必填
- 需配合渲染器 v2.5 + MCP接口层 v2.5

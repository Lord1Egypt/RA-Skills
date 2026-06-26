# Examples

两个主人实际用过的汇报范例，可以直接参考或复制改内容。

## report.html — 战略规划型汇报

**主题**：Platform AI 能力全景图 & 故事线规划

**结构**：
- Slide 1：封面（只有大标题）
- Slide 2：**SVG 架构图**（5 层：云产品 / 支撑层 / Agent 层 / 触达层 / 用户）+ 3 条故事线连线
- Slide 3：三条故事线卡片详解（WB 线 / claw 线 / skill 线）
- Slide 4：关键决策（decision-cards）

**适合复用场景**：战略汇报、架构设计、产品规划、能力全景图

## cost-report.html — 数据对比型汇报

**主题**：ProductA 模型成本追加专题汇报

**结构**：
- Slide 1：封面（带 badge、meta 信息）
- Slide 2：成本对比（cost-cards + budget-banner + metric-table + conclusion-banner）
- Slide 3：Placeholder 占位页（素材待补充）
- Slide 4：未来规划（budget-timeline + future-cards）

**适合复用场景**：成本分析、月度汇报、数据对比、预算申请

## 使用建议

1. 新做汇报时，从两个范例里挑一个最接近的**整体复制**
2. 替换封面、标题、页脚
3. 按需增删 slide，组件片段在 `../components/README.md`
4. 严格按 `../references/design-system.md` 的规范值改颜色和间距
5. 如果涉及架构图，务必读 `../references/svg-architecture-rules.md`

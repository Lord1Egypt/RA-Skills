# PPT 桥接协议 — 观势 × html-ppt 联动规范

## 核心设计

观势与 html-ppt 框架之间通过 **预生成大纲 JSON 文件 + 输出明确接力指令** 实现自动化串联。

关键约束：`use_skill("guanshi")` 是一次性同步调用，用户确认"生成PPT"时观势上下文已释放。因此观势必须在**同一次调用中**完成战略报告输出 + 大纲文件预生成 + 接力指令输出。主 Agent 读取指令后自动调用 html-ppt。

## 触发时机

Step 6 完整战略报告输出后，**中等和复杂问题**必须执行。简单问题（直接回答）不触发。

## 执行流程（在 use_skill("guanshi") 的同一次调用中完成）

### 步骤 1：输出战略报告

正常输出 Step 1-6 完整战略报告。

### 步骤 2：预生成 PPT 大纲文件

静默保存到工作空间 output 目录下的 `guanshi-ppt-outline.json`。

大纲 JSON 结构：

```json
{
  "meta": {
    "title": "PPT主标题（≤12字）",
    "subtitle": "副标题/日期/场景",
    "theme": "corporate-clean",
    "accent_color": "#003D99",
    "total_slides": 20,
    "generated_from": "观势 v3.1 战略报告"
  },
  "slides": [
    {"index": 1, "type": "cover", "purpose": "封面"},
    {"index": 2, "type": "exec_summary", "purpose": "执行摘要"},
    {"index": 3, "type": "act_divider", "purpose": "Why — 为什么需要变"},
    {"index": 4, "type": "data_cards", "purpose": "关键数据 — 四个数字看清底子"},
    {"index": 5, "type": "problem_tree", "purpose": "问题界定 — MECE 四分支"},
    {"index": 6, "type": "table", "purpose": "PESTEL 外部环境分析"},
    {"index": 7, "type": "five_forces", "purpose": "五力分析"},
    {"index": 8, "type": "act_divider", "purpose": "How — 内部诊断"},
    {"index": 9, "type": "table", "purpose": "7S 组织诊断"},
    {"index": 10, "type": "roadmap", "purpose": "品质全链条诊断"},
    {"index": 11, "type": "two_column", "purpose": "龙庭子品牌矛盾"},
    {"index": 12, "type": "act_divider", "purpose": "What — 往哪走"},
    {"index": 13, "type": "table", "purpose": "VRIO 能力评估"},
    {"index": 14, "type": "ansoff_matrix", "purpose": "安索夫战略选项"},
    {"index": 15, "type": "four_cards", "purpose": "核心方案 4P"},
    {"index": 16, "type": "scenario_grid", "purpose": "情景规划四象限"},
    {"index": 17, "type": "act_divider", "purpose": "How Much — 怎么落地"},
    {"index": 18, "type": "roadmap", "purpose": "P0-P1-P2 三阶段路线图"},
    {"index": 19, "type": "deep_insight", "purpose": "DeepInsight 三层穿透"},
    {"index": 20, "type": "closing", "purpose": "收束 Takeaway"}
  ]
}
```

**约束**：
- meta.theme="corporate-clean", meta.accent_color="#003D99"
- 每个 slide 含 index/type/purpose/content
- 文案直接从诊断报告对应章节提取，不另写
- **大纲必须覆盖 output-spec.md 的五维度**：战略(行业数据+竞对)、文化(OHI)、组织(7S)、能力(VRIO+BCG)、策略(安索夫+4P)+实施(情景+路线图+风险)+穿透(DeepInsight)
- 用 Act Divider（三幕剧结构）组织章节：Why → How → What → How Much

### 步骤 2.5：大纲完整性自检（强制）

大纲生成后，对照 output-spec.md 的五维度固定结构逐项检查：

```
□ 战略维度 → 行业数据(≥1页) + 竞对画像(≥1页) + TAM-SAM-SOM(建议)
□ 文化维度 → OHI 组织健康(≥1页)
□ 组织维度 → 7S 诊断(≥1页)
□ 机制维度 → 品质/流程/治理/子品牌矛盾(≥2页)
□ 能力维度 → VRIO(≥1页) + BCG(建议)
□ 策略维度 → 安索夫选项(≥1页) + 核心方案4P(≥1页)
□ 实施维度 → 情景规划(≥1页) + P0-P1-P2路线图(≥1页) + 风险矩阵(≥1页)
□ 穿透维度 → DeepInsight(≥1页)
□ 收束 → Takeaway(≥1页)
□ 章节组织 → 通过 Act Divider 实现三幕剧叙事（Why→How→What→How Much）
```

**任一维度缺少对应页面 → 大纲不完整，必须补充后才继续。**

**数据优先级原则**：数据型页面（行业数据表、竞对画像表、营收结构表、品质数据表）优先于框架型页面（MECE树、DeepInsight）。诊断报告中的所有量化数据必须在大纲中有对应投放位置。

### 步骤 3：报告末尾追加

```
---
以上是完整的战略分析报告。需要生成演示 PPT 吗？

（PPT 结构化大纲已预生成。回复"是"即可一键生成观势标准 HTML 演示文稿——corporate-clean 主题，deck 翻页导航，三幕剧叙事。）
```

---

## 幻灯片类型映射

| 报告维度 | 诊断报告要素 | 推荐 slide type | 强制？ | 最低页数 |
|---------|------------|----------------|--------|---------|
| - | 封面 | cover | **强制** | 1 |
| - | 执行摘要 | exec_summary | **强制** | 1 |
| - | 章节分隔 | act_divider | **强制** | 4（Why/How/What/How Much） |
| 战略 | 行业数据（规模/渗透率/均价/增速） | data_cards 或 table | **强制** | 1 |
| 战略 | 市场量化 TAM-SAM-SOM | data_cards | 建议 | 1 |
| 战略 | 竞对画像（份额/定位/价格带/威胁评估） | table | **强制** | 1 |
| 战略 | 营收/渠道结构分析 | table 或 data_cards | 建议 | 1 |
| 战略 | 五力分析评分 | five_forces | 建议 | 1 |
| 战略 | 问题界定 MECE | problem_tree | **强制** | 1 |
| 文化 | OHI 组织健康评分 | data_cards 或 table | 建议 | 1 |
| 组织 | 7S 诊断 | table | **强制** | 1 |
| 机制 | 品质管控链条 | roadmap | 建议 | 1 |
| 机制 | 子品牌/激励矛盾 | two_column | 建议 | 1 |
| 能力 | VRIO 评估 | table | **强制** | 1 |
| 能力 | BCG 业务组合 | 数据表格（内嵌卡片） | 建议 | 1 |
| 策略 | 安索夫矩阵 / 战略选项对比 | ansoff_matrix | **强制** | 1 |
| 策略 | 核心方案 4P | four_cards | 建议 | 1 |
| 实施 | 情景规划四象限 | scenario_grid | 建议 | 1 |
| 实施 | P0-P1-P2 路线图 | roadmap | **强制** | 1 |
| 实施 | 风险矩阵 | table | 建议 | 1 |
| 穿透 | DeepInsight 三层钻取 | deep_insight | 建议 | 1 |
| 收束 | 三条 Takeaway | closing | **强制** | 1 |

**"强制"列说明**：标注为强制的要素在大纲中必须出现，否则视为不完整大纲，触发步骤 2.5 回环修复。

## 主题与风格

| 参数 | 值 |
|------|-----|
| theme | corporate-clean |
| accent_color | #003D99（深蓝） |
| font | Inter / system-ui（无衬线） |
| 导航方式 | deck 翻页（键盘 ← → 切页） |
| 叙事结构 | 三幕剧：Why → How → What → How Much |
| 组件库 | `.card` `.grid g2/g4` `.pill` `.kicker` `.tag-{green,red,orange,blue}` `.roadmap-phase` `.ansoff` `.scenario-cell` `.divider-line` |

## 页数建议

| 诊断复杂度 | 推荐页数 | 最少页数（强制覆盖底线） |
|---|---|---|
| 中等 | 14-18 页 | 12 页 |
| 复杂（S级） | 20-28 页 | 18 页 |

页数计算依据：封面(1) + 执行摘要(1) + 4 个 act_divider(4) + 强制覆盖(8) + 建议覆盖(4-10) = 中等 14-18 页，复杂 20-28 页。

## 用户跳过

用户回复否定 → 主 Agent 自然结束。回复："好的，大纲文件已保留，随时可用。"

## 主 Agent 接力说明

用户回复"是" → 主 Agent 推断调用 `use_skill("html-ppt")`：
```
读取 output/guanshi-ppt-outline.json，使用 corporate-clean 主题（#003D99 主色）生成 HTML 演示文稿。
输出结构：deck 翻页容器，slide 分页，deck-header（机密声明）+ deck-footer（页码）。
叙事结构：三幕剧 Act Divider（Why→How→What→How Much）。
保存到 output/ 目录。
```

## 参考实现

德施曼智能锁战略诊断报告（deshiman-strategic-diagnosis.html）为标准参考实现，展示了：
- corporate-clean 主题的完整视觉效果
- 三幕剧结构（Act I Why → Act II How → Act III What → Act IV How Much）
- 全套组件用法：data_cards、PESTEL table、five_forces grid、7S table、roadmap、two_column、VRIO table、ansoff_matrix、four_cards、scenario_grid、deep_insight、closing

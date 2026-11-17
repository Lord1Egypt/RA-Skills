# Planning Schema

## Case bundle

每篇文章使用独立 case 目录。目录名建议为 `YYYY-MM-DD-topic-slug`，不包含敏感客户名、账号或数据库 ID。

## 00-case-brief.md

必填字段：

| 字段 | 允许值或说明 |
|---|---|
| topic | 一个可回答的问题或明确主题 |
| source_materials | 本地路径与 URL 列表 |
| target_reader | 核心层、扩展层、推荐层；至少核心层明确 |
| target_format | 正式 Markdown 长文 |
| length_range | 最小与最大字数 |
| writing_profile | JSON/YAML 路径或 `generic` |
| timeliness | low / medium / high |
| confidentiality | public / private-personal / private-company |

可选字段：collection_context、platform_signals、must_address、red_lines、deadline、user_hypothesis。

## Risk classification

| 风险 | 触发条件 | 处理 |
|---|---|---|
| high | 政策、法律状态、融资估值、产品 GA/Preview、宏观数字、原创/唯一声明 | 一手源或双源；记录核验时间 |
| medium | 厂商定位、市场份额、客户案例、性能数据 | 原始出处优先；标注 vendor/customer-reported |
| low | 通用背景、公开定义、解释性类比 | 至少一个可靠来源或由文章明确标为解释 |

## Planning brief required sections

1. 选题可行性与竞争程度。
2. 事实校准与必须修正的原始判断。
3. 目标读者分层及阅读任务。
4. 核心判断、论证链与边界。
5. 原创性锚点和现有覆盖缺口。
6. 反方、历史反例和证伪变量。
7. 标题方向、摘要功能和标题风险。
8. 结构大纲与字数分配。
9. 收藏载体：表格、框架、时间线或对比。
10. 本篇红线、时效要求和敏感性。
11. 与历史文章或系列的关系。
12. Gate A 待确认项。

## Gate A record

```yaml
gate_a:
  status: approved | changes_requested | pending
  approved_at: ISO-8601
  decisions:
    thesis: ""
    title_direction: ""
    length_and_depth: ""
    controversy_handling: ""
    platform_and_series: ""
  rejected_options: []
```

## Gate B record

```yaml
gate_b:
  status: approved | not_required | pending
  approved_at: ISO-8601
  tensions:
    - issue: ""
      options: []
      decision: ""
      reason: ""
```

## Completion rules

- Gate A 为 pending 时最多完成 `03-planning-brief.md`。
- Gate B 为 pending 时最多完成 `06-review-record.md`。
- `07-final.md` 生成后必须存在终稿机器扫描和 `08-final-check.md`。
- 发布物料字段不得进入 case bundle；后续发布 Skill 另行读取 `07-final.md`。

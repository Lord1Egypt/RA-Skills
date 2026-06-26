# 报告模板 Playbook

这份文档定义模板化使用报告和使用分析的固定做法。

## 什么时候使用

不要求用户明确说“报告”。只要用户是在问某一天或某一段时间的 JumpServer 整体使用情况、概览、汇总、排行或分布，就使用模板工作流。这包括：

- 使用报告
- 日报
- 使用情况
- 使用分析
- 审计分析
- 某天发生了什么
- 分析 `20260310`
- 看下 / 看看 `3 月 10 号` 使用情况
- 看看某天使用情况
- 帮我看 / 帮我看看某天登录 / 会话 / 命令 / 传输情况
- 想看上周谁登录最多
- 过一下 `3 月上旬` 哪些资产最活跃
- 某时间段的 JumpServer 使用概览
- “堡垒机使用情况” 这类说法

- [template/bastion-daily-usage-template.html](../template/bastion-daily-usage-template.html)
- [references/metadata/daily_usage_report_template_fields.json](metadata/daily_usage_report_template_fields.json)

动作词如 `看下` / `看看` / `帮我看看` / `想看` / `过一下` 不改变路由；真正决定路由的是后面跟的是“情况 / 概览 / 汇总 / 排行”，还是“日志 / 记录 / 明细 / 详情”。
即使用户说的是“分析”，只要核心对象是时间范围内的使用数据分析，也先产出完整 HTML 报告，不退回普通自由文本摘要。
只有在用户明确说“不要生成报告，直接分析”“先简单说下”“只给我结论”“不用模板”时，才允许跳过模板。

## 固定流程

```text
config-status --json -> ping -> 按组织优先级处理 -> python3 scripts/jumpserver_api/jms_report.py daily-usage ... -> 生成后自检 -> 输出 HTML
```

正式报告入口固定为：

```bash
python3 scripts/jumpserver_api/jms_report.py daily-usage \
  --date 2026-03-10 \
  --org-id 00000000-0000-0000-0000-000000000000
```

生成的 HTML 会固定写入 skill 根目录下的 `reports/JumpServer-YYYY-MM-DD.html`；兼容参数 `--output` 即使传入也不会改变实际输出路径。

不要每次请求都现场写临时拼装逻辑。报告类请求必须优先走正式入口；若正式入口缺失，应先补齐正式入口，再使用它。

## 组织优先级

按下面顺序处理：

1. 用户显式给组织 -> 按用户指定组织执行
2. 用户显式说“所有组织”或“全局组织” -> 视为全局组织 `00000000-0000-0000-0000-000000000000`
3. 用户未显式给组织 -> 先执行 `python3 scripts/jumpserver_api/jms_diagnose.py select-org --org-id 00000000-0000-0000-0000-000000000000 --confirm`
4. 全局组织可访问性不只看候选组织列表；允许通过显式 `select-org` / 直连探测确认
5. 全局组织直连探测或显式选择验证失败 -> 阻塞并返回 `candidate_orgs`

这个场景不要回退到 `{0002}` / `{0002,0004}` 自动组织逻辑。
如果用户明确指定某个组织，则查询该组织下的数据，不再默认切全局组织。

## 时间范围归一化

某一天：

- `report_date` 使用该日期
- `date_from=当天 00:00:00`
- `date_to=当天 23:59:59`

某一段时间：

- 明确落到 `date_from/date_to`
- `report_date` 可使用结束日期或报告生成时点的展示值，但模板内必须明确展示 `date_from/date_to`

固定归一化规则：

- “昨天” -> 前一天 `00:00:00 ~ 23:59:59`
- `20260310` -> `2026-03-10 00:00:00 ~ 23:59:59`
- `2026-03-10` / `2026/03/10` / `3月10号` / `3 月 10 日` -> 同一天 `00:00:00 ~ 23:59:59`
- “上周” -> 上一个自然周，周一 `00:00:00 ~ 周日 23:59:59`
- “本月” -> 本月 1 日 `00:00:00` 到当前日期或月末 `23:59:59`

如果用户只说“昨天”“最近一周”“3 月上旬”“上周”“本月”，先转换成明确时间窗，再取数。
一旦能归一化成单日或时间段，就按模板报告处理，不因为表述短而退回“快速分析”。

## 字段来源

统一读取 [references/metadata/daily_usage_report_template_fields.json](metadata/daily_usage_report_template_fields.json)。

字段取数时只使用元数据中声明的来源，例如：

- `python3 scripts/jumpserver_api/jms_diagnose.py license-detail`
- `python3 scripts/jumpserver_api/jms_diagnose.py inspect --capability ...`
- `python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type login`
- `python3 scripts/jumpserver_api/jms_query.py audit-analyze --capability ...`

正式入口内部直接复用 Python 模块与 handler，不通过 subprocess 套 CLI JSON。不要手工发明新的数据来源，也不要回退到临时 HTML 拼装逻辑。

## 命令存储规则

如果模板字段涉及命令审计：

- 如果用户显式给了 `command_storage_id`，只查询该 storage
- 如果用户没有给 `command_storage_id`，默认附带 `command_storage_scope=all`，汇总全部可访问 command storage
- 汇总结果需要回显 `queried_command_storage_ids` 与 `queried_command_storage_count`

不要把空命令结果直接写成“无高危命令”。

## 输出要求

成功时至少包含：

- 完整 HTML 报告
- 正式入口：`python3 scripts/jumpserver_api/jms_report.py daily-usage ...`
- 报告文件路径
- 模板路径：`template/bastion-daily-usage-template.html`
- 字段元数据路径：`references/metadata/daily_usage_report_template_fields.json`
- `effective_org`
- `switchable_orgs`（当当前组织已生效且仍有其他可切换组织时）
- `queried_command_storage_ids`
- `queried_command_storage_count`
- `report_date`
- `date_from`
- `date_to`
- `validation_summary`
- 执行命令摘要
- 可附加简短摘要，但不得仅返回摘要替代报告

阻塞时至少包含：

- 已走预检
- `effective_org`
- 阻塞原因
- `candidate_orgs`
- 下一步安全动作

## 生成后自检

正式入口默认执行生成后自检，HTML 可打开不是充分条件。

硬失败：

- HTML 仍残留 `{{field}}`
- metadata required 字段未赋值
- 关键字段为空：`login_total`、`login_failed`、`session_total`、`risk_event_total`
- 源数据已明确非空，但对应模块仍渲染成空值或 `暂无数据`

失败时固定行为：

- 不写最终输出文件
- 返回非零退出
- 回显 `validation_failures`
- 明确说明“生成失败，需要修复模板填充逻辑”

## 字段契约测试

使用正式契约测试脚本：

```bash
python3 scripts/jumpserver_api/jms_report.py contract-check
```

这个测试至少检查：

- 模板中的 `{{field}}` 是否都能在 metadata 中找到
- metadata 字段是否都还存在于模板
- required 字段是否都能绑定
- 最小假数据渲染后是否还残留 placeholder

## 例子

- “给我出 3 月 24 号的日报” -> 模板报告
- “帮我分析 3 月 1 日到 3 月 24 日的堡垒机使用情况” -> 模板报告
- “分析 20260310” -> 模板报告
- “看看某天使用情况” -> 模板报告
- “某天发生了什么” -> 如果核心是在问某天的 JumpServer 使用数据分析，模板报告
- “帮我看某天登录 / 会话 / 命令情况” -> 带明确日期或时间段时，模板报告
- “帮我看看昨天登录情况” -> 如果核心是在看整体情况或汇总，模板报告
- “想看上周谁登录最多” -> 模板报告
- “看下昨天谁登录最多，顺便生成报告” -> 模板报告
- “查昨天 30 条登录日志” -> 不是模板报告，回到普通审计路由
- “查最近 30 条登录日志” -> 不是模板报告，回到普通审计路由

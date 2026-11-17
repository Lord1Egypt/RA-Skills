---
name: office-collaboration-radar
description: >-
  把用户明确提供的中文群聊记录、会议纪要或项目更新整理为证据可追溯的协作状态卡片。
  仅在用户明确要求分析项目进展、决策、Owner 与截止时间、风险、阻断、依赖或需确认项时使用。
  不因用户仅粘贴文本而自动触发，不发送催办，不写入外部系统；读取和写入本地文件都必须使用用户明确指定的路径。
allowed-tools: "Bash(python3 scripts/process.py:*) Bash(python3 scripts/radar_chart.py:*) Bash(python3 scripts/export_card.py:*) Read Write"
---

# Office Collaboration Radar

把中文协作材料整理为结构稳定、证据受约束的状态卡片。本 Skill 不是周报生成器、绩效评价工具、催办助手或项目管理系统写入工具。

英文输出使用 [Office Collaboration Radar (English)](https://clawhub.ai/yamyeed/skills/office-collaboration-radar-en)。

## 输入与适用边界

接受用户直接提供或明确点名的 Markdown、纯文本、聊天导出、会议纪要和项目日志。多段材料应标注来源。项目名、时间范围、部门或实体脱敏名单均为可选信息。

如果材料没有给出项目名、时间范围、Owner、DDL 或部门，使用“未提供”，不得补全或猜测。

不执行以下任务：

- 生成完整周报、日报、OKR 或绩效评价；
- 发送消息、邮件、邀请或自动催办；
- 写入 Jira、飞书、Notion、CRM、日历等外部系统；
- 从材料外推断事实、责任归属或承诺。

## 两阶段工作流

必须区分语义抽取与确定性加固：

1. 模型只依据用户提供的材料，按 `templates/json-output-schema.md` 生成七模块草稿 JSON。
2. `scripts/process.py` 接收“草稿 JSON + 原始材料”，执行证据复核、脱敏、冲突检测、优先级排序和 Schema 校验。

`process.py` 不读取原始文本后自行完成语义抽取。不得把原始材料直接传给 `enforce` 并期待它生成卡片。

单段材料：

```bash
python3 scripts/process.py enforce \
  --card draft-card.json \
  --source source.txt \
  --out enforced-card.json
```

多段材料：先分别生成并加固各段卡片，再聚合卡片 JSON。`aggregate` 不接受原始文本。

```bash
python3 scripts/process.py aggregate \
  --cards enforced-1.json enforced-2.json \
  --entities entities.txt \
  --out aggregated.json
```

没有用户指定的实体名单时省略 `--entities`。聚合始终重新执行内置 PII 和凭据脱敏。

可选输出：

```bash
python3 scripts/radar_chart.py generate \
  --card enforced-card.json \
  --out collaboration-radar.svg

python3 scripts/export_card.py export-card \
  --card enforced-card.json \
  --format csv \
  --entities entities.txt \
  --out actions.csv
```

没有实体名单时省略 `--entities`。所有导出格式都会在序列化前重新执行内置 PII 和凭据脱敏。

## 语义抽取规则

1. 区分事实、观点、问题、暂定意向、闲聊和重复内容。
2. 只记录材料中明确确认的决策；不把讨论方向写成正式承诺。
3. Owner 和 DDL 保留原文值；找不到逐字支持时写“未提供”。
4. 区分风险、已发生阻断、跨部门依赖和外部依赖。
5. 将缺失、冲突或含糊信息放入“需人工确认项”。
6. 每个关键结论附不超过 40 个中文字符的证据片段；无可靠证据写“未提供”。
7. 固定保留七个模块，即使某模块只有“未提供”。

## 输出契约

标题顺序固定：

```markdown
# 协作状态卡片

## 项目状态总览
## 已有进展
## 已确认决策点
## Owner × DDL 待办列表
## 风险 / 阻断 / 依赖
## 跨部门协作关系
## 需人工确认项
## JSON 输出
```

结构参考：

- Markdown：`templates/collaboration-status-card.md`
- JSON：`templates/json-output-schema.md`
- 行动项：`templates/action-items-schema.md`
- 风险与依赖：`templates/risk-dependency-schema.md`
- 置信度：`templates/confidence-schema.md`
- 多卡片聚合：`templates/cross-turn-aggregation-schema.md`
- 下游字段映射：`templates/downstream-field-mapping.md`

## 文件与隐私边界

- 只读取用户明确提供的 `--card`、`--source`、`--entities` 或 `--cards` 路径；不枚举目录，不搜索其他文件。
- 不读取环境变量、凭据存储、浏览器数据、Shell 历史或无关工作区内容。
- 不联网，不传输协作材料；高风险材料应由用户预先脱敏。
- 每个文件输出都必须有明确 `--out`；输出路径不得与输入路径相同。
- 已有输出默认拒绝覆盖；只有用户明确允许时才使用 `--force`，且仅覆盖指定文件。
- 导出到 CSV、飞书或 Notion 的结果只是待审阅映射，不代表已获外部写入授权。

## 确定性加固边界

`enforce` 会重新从原始材料计算证据，不信任草稿中的 `evidence`。它还会：

- 检查 Owner 与 DDL 是否有逐字证据；
- 遮蔽常见 PII、凭据和用户提供的实体名称；
- 标记同任务的 Owner、DDL 或状态冲突；
- 按 P0/P1/P2 排序行动项并生成执行摘要；
- 清洗 Markdown 表格值并保持七模块 Schema。

确定性脱敏不是完整的密钥扫描器。不要向模型或脚本提供仍有效的凭据、客户秘密或敏感人事材料。

## 验证

修改或发布前运行：

```bash
python3 scripts/process.py selftest
python3 scripts/radar_chart.py selftest
python3 scripts/export_card.py selftest
```

示例均为合成材料，不代表生产部署或业务结果。

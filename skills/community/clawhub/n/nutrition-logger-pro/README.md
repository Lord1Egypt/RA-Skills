# nutrition_logger

`nutrition_logger` 是一个本地 OpenClaw / AgentSkills skill，用于通过自然语言记录饮食、估算营养值、保存每日饮食日志，并支持今日汇总、本周总结、撤销和修正。

所有用户可见提示、回复模板、示例和错误说明都使用中文。代码接口、CLI 子命令、JSON 字段名和 CSV 字段名保持英文。

## 能力概览

- 记录早餐、午餐、晚餐、加餐和普通“我吃了...”消息。
- 解析用户提供的总营养值，例如“这个面包 180 kcal，蛋白质 6g”。
- 解析每 100g 或每份营养标签，并按实际吃掉重量或份数计算。
- 在缺少标签时使用本地参考表估算，并明确标注估算和置信度。
- 持久保存 `food_log.jsonl` 和 `food_log.csv`。
- 支持今日汇总、本周总结、撤销上一条和保守修正。
- 保持渠道无关：Telegram、WhatsApp、Slack、CLI 等渠道只负责把文本交给 OpenClaw agent。

## 文件结构

```text
nutrition_logger/
|-- SKILL.md
|-- scripts/
|   |-- nutrition_cli.py
|   |-- nutrition_math.py
|   |-- log_store.py
|   `-- test_nutrition_cli.py
|-- references/
|   |-- common_food_portions.zh.md
|   |-- common_food_nutrition.zh.csv
|   |-- label_parsing_rules.md
|   |-- healthy_eating_guidelines.md
|   `-- response_templates.md
|-- examples/
|   |-- daily_messages.md
|   `-- correction_examples.md
|-- README.md
`-- LICENSE
```

运行时 skill 文件是 `SKILL.md`、`scripts/` 和 `references/`。`README.md`、`.gitignore` 和测试文件用于本地维护。

## 安装到 OpenClaw workspace

把这个 repo 复制到 workspace 的 skills 目录：

```bash
mkdir -p <workspace>/skills
cp -R /path/to/nutrition_logger <workspace>/skills/nutrition_logger
```

或者使用符号链接：

```bash
mkdir -p <workspace>/skills
ln -s /path/to/nutrition_logger <workspace>/skills/nutrition_logger
```

Windows PowerShell 可以使用 junction：

```powershell
New-Item -ItemType Directory -Force <workspace>\skills
New-Item -ItemType Junction -Path <workspace>\skills\nutrition_logger -Target D:\Github_repo\nutrition_logger
```

安装后重启 OpenClaw 会话或 gateway，然后验证：

```bash
openclaw skills list
openclaw skills list --eligible
openclaw skills check
```

## 示例消息

```text
记录：早餐两个鸡蛋，一杯250ml牛奶，一片面包，面包包装写180 kcal，蛋白质6g
午餐：鸡胸肉150g，米饭一碗，西兰花一份
晚餐：土豆泥150g，营养表每100g是110 kcal，蛋白质2g，碳水15g，脂肪4g
今日汇总
本周总结
撤销上一条
刚刚那个面包不是180 kcal，是220 kcal，蛋白质7g
```

## 数据优先级

营养值来源按以下顺序处理：

1. `user_provided`：用户提供实际吃掉那份食物的总营养值。
2. `label_calculated`：用户提供每 100g 或每份标签，脚本按吃掉重量或份数计算。
3. `estimated`：没有标签时使用本地参考表估算。
4. `mixed`：同一条食物中部分字段来自用户，部分字段为估算。

用户提供的值永远不会被估算覆盖。脚本只补齐缺失字段，并在 `note` 中说明来源和假设。

## 本地脚本

脚本只处理结构化 JSON；自然语言解析由 OpenClaw agent 根据 `SKILL.md` 和 `references/` 完成。

```bash
python scripts/nutrition_cli.py calculate-label
python scripts/nutrition_cli.py append-entry
python scripts/nutrition_cli.py summary-day
python scripts/nutrition_cli.py summary-week
python scripts/nutrition_cli.py undo-last
python scripts/nutrition_cli.py update-entry
```

标签计算示例：

```bash
printf '{"food":"土豆泥","eaten_amount_g":150,"label_per":"100g","nutrition_per_unit":{"kcal":110,"protein_g":2,"carbs_g":15,"fat_g":4}}' \
  | python scripts/nutrition_cli.py calculate-label
```

预期输出包含：

```json
{
  "food": "土豆泥",
  "source": "label_calculated",
  "confidence": "high",
  "nutrition": {
    "kcal": 165,
    "protein_g": 3,
    "carbs_g": 22.5,
    "fat_g": 6
  }
}
```

## 日志路径

默认日志路径按以下顺序解析：

1. `--log-dir`
2. `NUTRITION_LOG_DIR`
3. `OPENCLAW_WORKSPACE/nutrition-log`
4. 当前工作目录下的 `nutrition-log/`

日志文件：

- `food_log.jsonl`：事实来源，保存 entry、correction、deletion 事件。
- `food_log.csv`：当前有效记录的扁平可读视图，可从 JSONL 重建。

`nutrition-log/` 已加入 `.gitignore`，不要提交个人饮食数据。

## 本地验证

运行测试：

```bash
python scripts/test_nutrition_cli.py
```

验证 skill 结构：

```bash
python skill_creator/scripts/quick_validate.py .
```

提交前建议检查：

```bash
python scripts/test_nutrition_cli.py
python skill_creator/scripts/quick_validate.py .
git diff --check
git status --short
```

## 渠道绑定

本 skill 不包含 Telegram、WhatsApp 或 Slack 专用逻辑。要从这些渠道使用它，请在 OpenClaw 中把对应 channel 绑定到启用了 `nutrition_logger` skill 的 agent。渠道只负责投递用户文本；skill 负责解析饮食意图、调用脚本和组织中文回复。

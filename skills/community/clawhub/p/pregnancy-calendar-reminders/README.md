# 孕期日历提醒 Skill 说明

这个 skill 用于从 0 到 1 生成孕期提醒日历：用户只需要提供末次月经日期，Codex 就可以自动推算预产期、换算孕周、生成完整孕期每日提醒和关键产检提醒，并输出可导入 Apple 日历、iCloud 日历或其他日历工具的 `.ics` 文件。

如果 NT 或后续产检后医生给出了新的预产期，也可以用医生校正日期重新生成新版日历。新版会按医生预产期反推等效末次月经锚点，并同步更新所有孕周、产检窗口、预产期和 41 周提醒。

## 主要能力

- 根据末次月经日期推算预产期：`预产期 = 末次月经 + 280 天`
- 根据医生校正预产期重算孕周：`等效末次月经 = 预产期 - 280 天`
- 生成每日孕期提醒和关键产检窗口提醒
- 覆盖 NT、NIPT、系统超声、糖耐、孕晚期准备、足月待产等关键节点
- 输出 `.ics`、事件 JSON、核对表和校验报告
- 每次生成都执行日期和事件数校验，避免错算或漏算
- 支持导入 iCloud 日历后同步到 iPhone

## 使用示例

只提供末次月经：

```bash
python scripts/generate_pregnancy_calendar.py \
  --lmp 2026-04-20 \
  --output-dir ./pregnancy-calendar-output
```

NT 后医生调整预产期：

```bash
python scripts/generate_pregnancy_calendar.py \
  --lmp 2026-04-20 \
  --doctor-due 2027-01-25 \
  --output-dir ./pregnancy-calendar-output
```

默认只从今天生成到 41 周，避免把过去提醒塞进手机。若需要完整历史版，可加：

```bash
--include-past
```

## 输出文件

- `.ics`：可导入日历的提醒文件
- `.json`：完整事件数据
- `_outline.md`：中文核对表，包含预产期、孕周锚点和产检窗口
- `_validation.json`：机器可读校验结果

## 导入手机

在 Mac 上双击 `.ics` 文件导入日历。为了同步到 iPhone，导入时请选择 iCloud 日历，不要选择“在我的 Mac 上”。然后在 iPhone 上确认已开启：

`设置 > Apple ID > iCloud > 日历`

## 安全边界

这个 skill 生成的是家庭计划和产检提醒，不替代医生诊断、处方或医院个体化安排。出现阴道出血、持续或剧烈腹痛、晕厥、严重呕吐无法进食饮水、胎动明显减少等情况，应及时联系产科或就医。

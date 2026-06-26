---
name: personal-injury-compensation-calculation
description: |
  当用户需要计算人身损害赔偿、交通事故赔偿、伤残赔偿金、死亡赔偿金、丧葬费、误工费、护理费、营养费、被扶养人生活费，或需要导出赔偿明细表时使用。优先调用 scripts/personal_injury_compensation.py 完成计算；references 仅用于脚本依赖的数据校验、法条引用和缺失数据补录，不能替代脚本手工计算。
---

# 人身损害赔偿计算

## 定位

本 skill 用于依据中国现行人身损害赔偿规则，计算伤害类和死亡类案件的赔偿项目，并输出结构化明细。

核心执行入口是：

- `scripts/personal_injury_compensation.py`

如果当前环境没有 `python3`，可使用等价命令：

- `py -3 scripts/personal_injury_compensation.py`

## 强制执行规则

1. 只要需要给出赔偿金额、赔偿明细、合计金额或导出明细表，必须优先执行 `scripts/personal_injury_compensation.py`。
2. 不得只根据 `references/` 下的公式和表格由模型直接口算、心算或手写总额来替代脚本。
3. `references/` 的作用仅限于：
   - 供脚本读取本地规则和统计数据
   - 在回复中补充法条依据
   - 判断哪些统计数据缺失，需要额外查询并写回 `statistics_overrides`
4. 如果脚本提示统计数据缺失，先补齐数据，再重新执行脚本；不要绕过脚本直接给金额。
5. 如果脚本当前不支持某个场景，必须明确说明“脚本暂不支持该场景的自动计算”，只可给出缺口说明或分项分析，不可伪造最终金额。

## 适用场景

- 交通事故人身损害赔偿计算
- 生命权、身体权、健康权侵权赔偿计算
- 伤残赔偿金、死亡赔偿金、丧葬费测算
- 误工费、护理费、营养费、住院伙食补助费计算
- 被扶养人生活费计算
- 生成 Markdown 或 JSON 明细
- 生成 `.xlsx` 赔偿明细表

## 工作流程

### 第一步：收集案件事实

优先确认这些字段；缺失时先追问，再执行脚本：

| 字段 | 说明 |
| --- | --- |
| `case_type` | `injury` 或 `death` |
| `incident_date` | 案件发生时间，`YYYY-MM` 或 `YYYY-MM-DD` |
| `hearing_date` | 一审开庭时间或预计开庭时间，用于确定上一年度统计口径 |
| `victim_age` | 受害人年龄 |
| `court_province` | 受诉法院所在地省份 |
| `court_city` | 受诉法院所在地城市，经济特区/计划单列市必须提供 |
| `wage_caliber` | `private`、`full`、`non_private` |
| `residency_type` | `urban` 或 `rural` |

按案情补充这些字段：

- `disability_levels`
- `dependents`
- `work_loss_days`
- `lost_income_actual`
- `annual_income_average`
- `industry_average_annual_income`
- `nursing_days`
- `nursing_rate_per_day`
- `nursing_annual_income`
- `nutrition_days`
- `hospital_days`
- `medical_expense`
- `transport_expense`
- `lodging_expense`
- `appraisal_fee`
- `property_loss`
- `assistive_device_expense`
- `mental_damage`
- `auto_mental_damage`

### 第二步：先看脚本示例输入

在 skill 目录下先执行：

```bash
python3 scripts/personal_injury_compensation.py --example
```

Windows 可执行：

```bash
py -3 scripts/personal_injury_compensation.py --example
```

用脚本给出的示例 JSON 作为模板，再填入案件数据。

### 第三步：编写案件 JSON

最小可运行示例：

```json
{
  "case_type": "injury",
  "incident_date": "2024-06-12",
  "hearing_date": "2025-03-18",
  "victim_age": 35,
  "court_province": "广东省",
  "court_city": "广州市",
  "wage_caliber": "private",
  "residency_type": "urban",
  "disability_levels": [10],
  "work_loss_days": 90,
  "annual_income_average": 120000,
  "nursing_days": 30,
  "nursing_rate_per_day": 150,
  "nutrition_days": 60,
  "hospital_days": 10,
  "medical_expense": 18000,
  "transport_expense": 1200,
  "appraisal_fee": 2500,
  "auto_mental_damage": true,
  "dependents": [
    {
      "age": 10,
      "supporter_count": 2
    }
  ]
}
```

### 第四步：执行脚本计算

常用执行用例如下。

1. 直接输出 Markdown 结果：

```bash
python3 scripts/personal_injury_compensation.py --input case.json
```

2. 输出到 Markdown 文件：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case.json \
  --output result.md
```

3. 同时导出 Markdown 和 Excel：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case.json \
  --output result.md \
  --xlsx result.xlsx
```

4. 输出 JSON 结构化结果：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case.json \
  --format json
```

5. 输出 JSON 到文件，便于后续系统消费：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case.json \
  --format json \
  --output result.json
```

> Windows PowerShell 若仍使用 GBK 控制台，直接打印到 stdout 可能触发 `UnicodeEncodeError`。此时优先使用 `--output` 写文件，或先设置 `PYTHONIOENCODING=utf-8` 后再执行。

### 第五步：缺失统计数据时，补 `statistics_overrides` 后重跑

若脚本报错提示本地 `references` 缺失统计数据，按以下顺序处理：

1. 先看报错缺的是哪一类数据。
2. 只查询权威来源：
   - 省/市统计局官网
   - 国家统计局官网
   - 人社部门官网
3. 将查到的数据写入案件 JSON 的 `statistics_overrides`。
4. 重新运行脚本。

支持的补录键包括：

| 键名 | 用途 |
| --- | --- |
| `urban_disposable_income` | 城镇居民人均可支配收入 |
| `urban_consumption_expenditure` | 城镇居民人均消费支出 |
| `rural_consumption_expenditure` | 农村居民人均生活消费支出 |
| `rural_net_income` | 农村居民人均纯收入 |
| `private_wage` | 城镇私营单位就业人员平均工资 |
| `full_wage` | 全口径城镇单位就业人员平均工资 |
| `non_private_wage` | 城镇非私营单位就业人员平均工资 |

补录示例：

```json
{
  "case_type": "injury",
  "incident_date": "2024-06-12",
  "hearing_date": "2025-03-18",
  "victim_age": 35,
  "court_province": "广东省",
  "court_city": "深圳市",
  "wage_caliber": "private",
  "residency_type": "urban",
  "disability_levels": [10],
  "statistics_overrides": {
    "urban_disposable_income": {
      "2024": 65000
    },
    "urban_consumption_expenditure": {
      "2024": 42000
    },
    "private_wage": {
      "2024": 81456
    }
  }
}
```

补录后重新执行：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case-with-overrides.json \
  --output result.md \
  --xlsx result.xlsx
```

## references 的正确用法

脚本会读取以下文件：

- `references/formulas.md`
- `references/provincial_avg_wage.md`
- `references/disposable_income.md`
- `references/law_articles.md`

使用原则：

1. 先跑脚本。
2. 只有在脚本提示数据缺失或需要补法条说明时，再查看 `references/`。
3. 不得看到公式后直接在回答里自行汇总金额，跳过脚本。

## 输出要求

回复用户时至少包含：

1. 采用的统计口径和年份
2. 各赔偿项目明细
3. 合计金额
4. 法条依据或法条来源说明
5. 关键假设、缺失项和风险提示

如用户要求下载表格或完整测算，优先执行带 `--xlsx` 的命令。

## 故障处理

### 1. 没有 `python3`

改用：

```bash
py -3 scripts/personal_injury_compensation.py --help
```

### 2. 脚本提示缺少 `--input`

先生成示例，再保存为案件 JSON：

```bash
python3 scripts/personal_injury_compensation.py --example
```

### 3. 脚本提示统计数据缺失

不要直接手算。先补 `statistics_overrides`，再重跑脚本。

### 4. 经济特区或计划单列市案件

如深圳、厦门、珠海、汕头、青岛、大连、宁波等，优先提供对应城市统计口径；本地 `references` 不足时，应补 `statistics_overrides` 后再计算。

### 5. Windows 控制台输出乱码或 `UnicodeEncodeError`

优先改用文件输出：

```bash
python3 scripts/personal_injury_compensation.py \
  --input case.json \
  --output result.md
```

或先设置 UTF-8 再执行：

```bash
$env:PYTHONIOENCODING = "utf-8"
py -3 scripts/personal_injury_compensation.py --input case.json
```

## 禁止事项

- 禁止只根据 `references` 直接心算赔偿金额
- 禁止在脚本报缺数据时套用其他省份数据
- 禁止在缺关键输入时伪造伤残等级、误工天数、护理天数或统计基数
- 禁止输出没有脚本结果支撑的“总赔偿额”

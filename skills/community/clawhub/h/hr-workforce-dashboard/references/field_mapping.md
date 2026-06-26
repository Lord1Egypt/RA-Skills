# 字段映射与输入校验

## 1. 元数据行读取规则（新模式，唯一模式）

不兼容旧模式，不读取文件名，只通过结构化元数据行解析。

### Active 文件（在职明细）
- 第 1-6 行为元数据，第 7 行为表头，第 8 行起为数据
- 第 1 行：报表名称，固定值 `Overseas Active Employee Report`
- 第 4 行：切片时间，格式为 `Effective Date | <日期>`（A列=标签，B列=日期值）
- 第 2-3、5、6 行为无效数据，忽略

### Termination 文件（离职明细）
- 第 1-7 行为元数据，第 8 行为表头，第 9 行起为数据
- 第 1 行：报表名称，固定值 `Overseas Terminated Employee Report`
- 第 4 行：统计开始日期，格式为 `Termination Date From | <日期>`
- 第 5 行：统计结束日期，格式为 `Termination Date To | <日期>`
- 第 2-3、6、7 行为无效数据，忽略

### Contingent Worker 文件（外包人员明细）
- 第 1 行为报表名称，包含 `Contingent Worker` 字样
- 第 2 行为表头，第 3 行起为数据
- 数据永远是最新切片，无需指定快照日期
- 使用独立的读取函数 `read_contingent_dataset()`

### 文件类型识别
通过第 1 行的报表名称自动识别：
- 包含 `active`、`在职`、`headcount` → active 类型
- 包含 `terminat`、`attrition`、`离职` → termination 类型
- 包含 `contingent`、`contractor`、`partner`、`外包` → contingent 类型

禁止根据文件名推断文件类型。

## 2. dataset_type 归类

推荐将元数据中的 `dataset_type` 归一到以下三类：

- `active`
  - 可接受关键词：`active`、`在职`、`headcount`
- `termination`
  - 可接受关键词：`terminat`、`attrition`、`离职`
- `contingent`
  - 可接受关键词：`contingent`、`contractor`、`partner`、`外包`

若无法识别，直接报错并提示用户检查元数据首行。

## 3. 正式表格字段

Active 文件：第 7 行为表头，第 8 行起为数据。
Termination 文件：第 8 行为表头，第 9 行起为数据。
Contingent Worker 文件：第 2 行为表头，第 3 行起为数据。

### Active 文件最低要求
- `Employee Type`
- `Region`
- `WD Employee ID`
- `Country/Territory`
- `BG`

### Termination 文件最低要求
- `Employee Type`
- `Region`
- `WD Employee ID`
- `Country/Territory`
- `BG`
- `Termination Date`
- `Termination Category`

### Contingent Worker 文件最低要求
- `HQ Employee ID`（或含 Employee ID 的列 → 重命名为 `Worker_ID`）
- `WeCom Name`（用于根据前缀分类 Worker_Type）
- `Country/Territory`（中文国家名）
- `BG`

## 4. 枚举值

### Employee Type
- `Regular`
- `Intern`

### Termination Category
- `Terminate Employee > Involuntary`
- `Terminate Employee > Voluntary`
- `Terminate Employee > Others`
- `Terminate Employee > Statutory Termination`

### Worker Type（Contingent）
通过 `WeCom Name` 前缀自动识别：
- `v_` 前缀 → `Contractor`
- `p_` 前缀 → `Partner`
- 无匹配前缀 → 默认 `Contractor`

## 5. BG 映射

| 展示列 | 原始值匹配 |
|---|---|
| `IEG` | `IEG - Interactive Entertainment Group` |
| `CSIG` | `CSIG - Cloud & Smart Industries Group` |
| `WXG` | 前缀匹配 `WXG - Weixin Group` |
| `TEG` | `TEG - Technology & Engineering Group` |
| `CDG` | `CDG - Corporate Development Group` |
| `PCG` | `PCG - Platform & Content Group` |
| `OFS` | `Overseas Functional System` |
| `S1` | `S1 - Functional Line` |
| `S2` | `S2 - Finance Line` |
| `S3` | `S3 - HR & Management Line` |

若出现未映射 BG：
- 不阻塞生成
- 在 `summary.md` 中记录未识别值
- 不自动打散到固定列之外，避免破坏版式

**注意**：BG 映射规则同时适用于 Active / Termination / Contingent Worker 三种文件。

## 6. 地域规则

### 海外范围
仅包括：
- `Americas`
- `APAC`
- `EMEA`

### Greater China
看板 3 单独保留 `Greater China` 行。
建议优先通过 `Region = Greater China` 识别；若数据源未标准化，可结合国家/地区值识别：
- `Mainland China`
- `Hong Kong`

### Mainland China
不纳入看板 1 / 2 / 4 / 5 的统计范围。

### Contingent Worker 国家映射
外包人员文件中的 `Country/Territory` 为中文国家名，脚本内置 `CONTINGENT_COUNTRY_MAP` 映射表（40+ 个国家），格式：
- 中文名 → (英文名, Region)
- 例如：`美国` → `("United States of America", "Americas")`

未映射的国家名保留原始值，Region 设为 `Unknown`。

## 7. 去重与日期清洗

- 员工唯一键优先使用 `WD Employee ID`（Active/Termination）或 `Worker_ID`（Contingent）
- 同一快照月份内，同一员工重复出现时按唯一员工计数
- `snapshot_date` 来自元数据首行，统一转为日期
- `Hire Date`、`Termination Date` 使用宽松解析，无法识别时置空

## 8. 降级策略

| 场景 | 处理方式 |
|---|---|
| 无 active 文件 | 中止并报错 |
| 缺少 termination 文件 | 跳过或弱化看板 4，并在摘要中说明 |
| 缺少去年同月 | 继续生成看板 1，标注 `数据不完整` |
| 缺少近 2 个月 | 继续生成看板 1，标注缺失月份 |
| 出现未知 BG | 正常生成，摘要中提示 |
| 缺少 contingent worker 文件 | 不生成看板 5，其他看板正常输出 |
| contingent worker 中出现未映射国家 | 保留原始值，Region 设为 Unknown |

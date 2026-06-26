# 指标口径定义

## 看板 1：正式员工趋势图

### 统计对象
- `Employee Type = Regular`
- 范围：`Americas / APAC / EMEA`

### 指标
- 同比去年同月正式员工人数
- 近三个月环比正式员工人数

### 口径
- 最新月份 = 所有 active 文件中最大的 `snapshot_date`
- 同比月份 = 最新月份的去年同月
- 环比月份 = 最新月份、上个月、上上个月
- 以唯一 `WD Employee ID` 计数

### 缺失处理
- 若去年同月缺失：仍生成图表，并标注 `缺少同比数据`
- 若近 2 个月缺失：仍生成图表，并标注缺失月份

## 看板 2：期末在离职分析

### 统计对象
- `Employee Type = Regular`
- 范围：`Americas / APAC / EMEA`

### 指标
- 最新月份各 Region 在职人数及占比（左图）
- 截止最新快照日期当年累计离职人数及占比（右图）

### 公式
- 区域占比 = 区域人数 / 海外总人数
- 年内离职 = `Termination Date` 在当年 1月1日 至最新快照日期之间的记录

## 看板 3：Active Regular & Intern 明细汇总表

### 数据来源
- 最新月份 active 文件

### 行结构
- `Americas`
- `APAC`
- `EMEA`
- `海外合计`
- `Greater China`
- `海外合计（含试点国内）`

### 列结构
固定顺序：
- `合计`
- `IEG`
- `CSIG`
- `WXG`
- `TEG`
- `CDG`
- `PCG`
- `OFS`
- `S1`
- `S2`
- `S3`

每个分组下固定两列：
- `Regular`
- `Intern`

### 排序
- Region 顺序固定
- 各 Region 下 `Country/Territory` 按总人数降序

## 看板 4：Attrition Regular 离职分析表

### 统计对象
- `Employee Type = Regular`
- 范围：`Americas / APAC / EMEA`
- 排除：`Mainland China`

### 统计周期
- 期末快照：最新 active `snapshot_date`
- 期初快照：优先使用不晚于离职起始日的最近 active 快照；若无法匹配，则退化为期末前最近 active 快照
- 离职明细：`Termination Date` 落在统计周期内

### 指标
- `期初人数`
- `期末人数`
- `No. of Attrition`
- `%`
- `Voluntary`
- `Involuntary`
- `Others`（数据为空时不展示该列）
- `Statutory`（数据为空时不展示该列）

### 公式
\[
离职率 = 统计周期离职人数 \div \left(\frac{期初在职人数 + 期末在职人数}{2}\right) \times 100\%
\]

### 原因分类映射
- `Voluntary = Terminate Employee > Voluntary`
- `Involuntary = Terminate Employee > Involuntary`
- `Others = Terminate Employee > Others`
- `Statutory = Terminate Employee > Statutory Termination`

## 看板 5：Active Contractor & Partner

### 数据来源
- Contingent Worker 文件（仅在上传时生成此看板）

### 统计对象
- 所有外包人员（不区分 Employee Type）
- 范围：`Americas / APAC / EMEA`
- 排除：非海外区域

### Worker Type 分类
- `WeCom Name` 以 `v_` 开头 → `Contractor`
- `WeCom Name` 以 `p_` 开头 → `Partner`
- 无匹配前缀 → 默认 `Contractor`

### 行结构
- `Americas` → 按国家细分
- `APAC` → 按国家细分
- `EMEA` → 按国家细分
- `海外合计`

### 列结构
固定顺序（与看板 3 一致）：
- `合计`
- `IEG`
- `CSIG`
- `WXG`
- `TEG`
- `CDG`
- `PCG`
- `OFS`
- `S1`
- `S2`
- `S3`

每个分组下固定两列：
- `Contractor`
- `Partner`

### 排序
- Region 顺序固定：Americas → APAC → EMEA
- 各 Region 下国家按总人数（Contractor + Partner）降序

### 国家名映射
- 源数据中 `Country/Territory` 为中文，通过内置映射表转换为英文
- 同时从映射表获取 Region

## 输出摘要中必须说明的内容

- 使用了哪些 active 文件和 termination 文件
- 是否使用了 contingent worker 文件
- 最新月份是什么
- 看板 4 选取的统计周期是什么
- 哪些月份或文件缺失
- 是否存在未识别 BG

---
name: guandata
description: 使用观远BI来进行数据获取与数据分析。触发词：查数据、做图表、看报表、营业额、门店、会员、订单，分析
---

# 观远BI

## 🔴 操作前必读（不可跳过）

## ⚠️ 关键规则

**所有数值计算必须跑代码** — 禁止在思考中直接口算百分比、环比、除法等。
1. **必须提供 pg_id** — 不保存的卡片无法取数据
2. **先查页面权限** — 用 `list-pages --manageable` 找有权限的页面，不用翻 JSON
3. **筛选值按需查** — 只有用了分类筛选（`IN`/`EQ`/`CONTAINS`）才需要 `search-values`；纯日期范围（`BT`）不需要
4. **图表类型限制** — 超出 metric/row/column 上限会返回空数据
5. **必须确认数据范围** — 用户没有明确指定日期范围时，**必须追问**，不要自己假设。例如："你想看哪段时间的数据？" 或提供选项："要看今天、本周还是上月？"



**每次做分析前，第一步永远是：**
```bash
cat skills/guandata/分析经验.md
```
这不是建议，是硬性步骤。跳过 = 重复踩坑。规则都在里面，包括：
- 数据表选择（哪张表对应什么场景）
- 字段陷阱
- 报告规范
- 计算红线（加权平均、禁止口算）
- 待处理的bug

**遇到意外的错误以及得到新的教训立即更新：** 遇到意外的错误以及得到新的教训，当场写入 `分析经验.md` 的「待确认」区域（第四章），格式：
```markdown
### 7.N [YYYY-MM-DD] 简要标题
- **场景**: 什么情况下遇到的
- **问题**: 发生了什么
- **我的判断**: 我认为应该怎么做
```
如果配置了 cron，待确认项可以自动发送给用户确认。

## 基本信息
- 配置文件: `skills/guandata/config.json`（**含明文凭据，请勿提交到公开仓库**）
- 脚本: `skills/guandata/scripts/guandata.py`

## 运行环境
- **Python 3.8+**
- **依赖库**: `httpx`（`pip install httpx`）
- 凭据存储在 `config.json` 中（明文），仅供本地使用，切勿提交到公开仓库

## 配置说明

编辑 `config.json`：

```json
{
  "version": "6",
  "base_url": "https://your-guandata-instance.com:port",
  "domain": "your_domain",
  "login_id": "your_username",
  "password": "your_password",
  "default_pg_id": "your_default_page_id",
  "default_folder_id": "your_default_folder_id"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `version` | ✅ | 观远BI版本：`"6"` 或 `"7"`。<br>• `"6"`：观远BI 6.x，直接保存卡片<br>• `"7"`：观远BI 7.0+，使用 draft/release 机制（创建卡片后自动发布页面） |
| `base_url` | ✅ | 观远BI服务器地址，如 `https://bi.company.com:8080` |
| `domain` | ✅ | 登录域，通常为 `guanbi`，具体咨询你们的BI管理员 |
| `login_id` | ✅ | 观远BI登录账号 |
| `password` | ✅ | 观远BI登录密码 |
| `default_pg_id` | | 默认页面ID。不传时，`create-and-get` 需手动指定 `pg_id`；传入后可省略 |
| `default_folder_id` | | 默认文件夹ID。创建新页面时的存放位置 |

### 如何获取 pg_id / folder_id

1. 在观远BI网页打开目标页面，URL 中的 `pgId=xxx` 即为页面ID
2. 文件夹ID在观远BI「数据管理」→「目录」中查看

## 核心命令

```bash
SCRIPT="python3 skills/guandata/scripts/guandata.py"

# 查数据集（默认读本地缓存）
$SCRIPT list-datasets
$SCRIPT list-datasets --columns   # 同时显示每个数据集的字段
$SCRIPT list-datasets --refresh   # 强制刷新缓存（数据源有变更时用）

# 查字段（默认读本地缓存，自动包含计算字段）
$SCRIPT get-columns <ds_id>             # 输出原始字段 + 计算字段
$SCRIPT get-columns <ds_id> --refresh   # 强制刷新缓存
$SCRIPT get-columns <ds_id> --with-calc # 同时显示计算字段（公式字段）

# 查枚举值（筛选前必查，避免值不存在）
# fd_id 从 get-columns 输出第二列拿
$SCRIPT search-values <ds_id> <fd_id> --search "关键词"
$SCRIPT search-values <ds_id> --name "门店名称" --search "某门店"  # 用字段名代替 fd_id

# 建卡+取数（一步到位）
$SCRIPT create-and-get '{"name":"卡片名","ds_id":"数据集ID","chart_type":"SINGLE_VALUE","pg_id":"页面ID","metric":[{"name":"会员id","aggr":"CNT_DISTINCT"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-02-01","2026-02-28"]}]}'
$SCRIPT create-and-get '{...}' --limit 200   # 限制返回200行数据（默认500行上限）

# 建卡+取数（组合图，metric_additional 传折线叠加数据）
$SCRIPT create-and-get '{"name":"达成率趋势","ds_id":"数据集ID","chart_type":"STACKED_COLUMN_WITH_LINE","pg_id":"页面ID","metric":[{"name":"营业额","aggr":"SUM"}],"metric_additional":[{"name":"人数","aggr":"SUM"}],"row":["营业日期(月)"],"column":["销售类型"],"filters":[...]}'

# 仅建卡（不取数）
$SCRIPT create-card '{...}'

# 取卡片数据（含筛选条件）
$SCRIPT get-card-data <card_id>

# 列页面
$SCRIPT list-pages
$SCRIPT list-pages --manageable  # 只显示有编辑权限的页面（日常用这个）

# 注意：list-datasets 默认显示父文件夹ID
# 输出格式示例：
#   数据集名称
#     ID: 数据集ID  |  行数  列数  |  状态
#     父文件夹ID: 父文件夹ID
#     描述: 描述信息
#     路径: 目录路径

# 创建页面
$SCRIPT create-page "页面名称"
$SCRIPT create-page "页面名称" --parent-dir "目录ID" --desc "描述"

# 获取页面卡片列表
$SCRIPT get-page-cards <pg_id>

# 批量删除卡片（需要 pg_id）
$SCRIPT delete-cards <pg_id> <card_id1> <card_id2> ...
```

## 💾 数据缓存机制
**`create-and-get`、`get-card-data` 命令都会自动将数据保存到本地 CSV 缓存文件。**

输出末尾会显示缓存路径：`📁 缓存: skills/guandata/.cache/data/xxx.csv`

### 缓存目录结构

```
skills/guandata/.cache/
├── data/                   # 数据查询缓存（CSV），默认共享目录
├── datasets/               # 数据集列表缓存（JSON）
├── columns/                # 字段列表缓存（JSON）
└── tasks/                  # 按任务隔离的缓存（使用 --task 参数时）
    └── {task_name}/
        ├── data/
        ├── datasets/
        └── columns/
```

### 按任务隔离缓存（--task）

不同任务的缓存混在一起时，用 `--task` 参数按任务名分组。**`--task` 放在子命令前面：**

```bash
# 堂食分析任务 → skills/guandata/.cache/tasks/堂食分析/data/
$SCRIPT --task "品类分析" create-and-get '{"name":"品类","ds_id":"<dataset_id>",...}'

# 查字段也隔离
$SCRIPT --task "会员分析" get-columns <dataset_id>
```

不加 `--task` 时，缓存仍在默认的 `.cache/data/` 共享目录。

### 缓存清理

当缓存占用过多空间或数据过期时，需要清理缓存：

```bash
# 清理所有数据查询缓存（保留最近7天）
find skills/guandata/.cache/data -name "*.csv" -mtime +7 -delete

# 清理所有缓存（彻底清空）
rm -rf skills/guandata/.cache/*



### 缓存文件格式

CSV，首行为表头，后续行为数据。用 Excel / pandas / csv 模块直接读即可。

### 大模型使用规范

**当拿到取数结果后，必须用缓存文件处理数据，不要把大量数据塞进上下文。**

正确做法：
```python
import csv
# 1. 从输出中提取缓存路径
# 2. 用代码读取缓存
with open('skills/guandata/.cache/data/xxx.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = next(reader)
    rows = list(reader)
# headers[j] 是第 j 列的字段名
# rows[i][j] 是第 i 行第 j 列的值（字符串）
```

## create-and-get / create-card 参数说明

`create-and-get` 和 `create-card` 共用以下参数格式：

| 参数 | 必填 | 类型 | 说明 | 类比 SQL |
|------|------|------|------|----------|
| `name` | ✅ | string | 卡片名称 | - |
| `ds_id` | ✅ | string | 数据集 ID（用 `list-datasets` 查） | `FROM 表` |
| `chart_type` | ✅ | string | 图表类型（见下方速查表） | - |
| `pg_id` | ✅ | string | 保存到的页面 ID（用 `list-pages --manageable` 找） | - |
| `row` | | list | 行维度（分组依据） | `GROUP BY` |
| `column` | | list | 列维度（横向拆列） | 交叉表列头 |
| `metric` | | list | 数值（要算的指标） | `SUM/AVG/COUNT` |
| `metric_additional` | | list | 叠加数值（组合图专用：柱+线的线） | - |
| `color_by` | | list | 颜色分组（气泡图/散点图） | - |
| `size_by` | | list | 气泡大小（气泡图专用） | - |
| `filters` | | list | 筛选条件 | `WHERE` |
| `sorting` | | list | 排序 | `ORDER BY` |
| `custom_fields` | | list | 自定义公式字段（动态创建计算列） | `SELECT ... , SUM(x)/SUM(y) AS 别名` |

举例说明：
```json
{
  "row": ["城市"],                        // 按城市分行
  "column": ["销售类型名称"],              // 堂食/外卖拆成两列
  "metric": [{"name": "毛营业额", "aggr": "SUM"}],  // 每格填营业额总和
  "filters": [{"name": "营业日期", "op": "BT", "value": ["2026-01-01", "2026-02-28"]}],  // 只看1-2月
  "sorting": [{"name": "毛营业额", "order": "DESC"}]  // 按营业额降序排
}
// 等价于: SELECT 城市, 销售类型名称, SUM(毛营业额) FROM 表 WHERE 营业日期 BETWEEN ... GROUP BY 城市, 销售类型名称 ORDER BY SUM(毛营业额) DESC
```

### 自定义公式字段（custom_fields）

在创建卡片时动态添加计算字段，无需提前在观远界面建好：

```bash
$SCRIPT create-and-get '{
  "name": "成本率分析",
  "ds_id": "数据集ID",
  "chart_type": "GROUPED_COLUMN",
  "pg_id": "页面ID",
  "row": ["门店名称"],
  "metric": [
    {"name": "毛营业额", "aggr": "SUM"},
    {"name": "成本率"}
  ],
  "custom_fields": [
    {"name": "成本率", "fdType": "DOUBLE", "formula": "SUM([实际使用金额])/SUM([毛营业额])*100"}
  ],
  "filters": [{"name": "营业日期", "op": "BT", "value": ["2026-01-01", "2026-02-28"]}]
}'
```

**参数格式**：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 新字段名称 |
| `fdType` | ✅ | 数据类型：`DOUBLE`（数值）、`STRING`（文本）等 |
| `formula` | ✅ | 公式表达式，用 `[字段名]` 引用字段，支持 `SUM()`/`AVG()` 等聚合 |

**注意**：
- 公式里的字段名必须是数据集中已存在的字段
- 创建后该字段可直接在 `metric`/`row` 中引用（和其他字段一样），如果公式已经聚合无需再写 `aggr`
- 仅 `create-and-get` 和 `create-card` 支持此参数


## 图表类型速查（26种）

| 类型 | metric | row | column | metric_additional | color_by | size_by | 备注 |
|------|:------:|:---:|:------:|:-----------------:|:--------:|:-------:|------|
| `SINGLE_VALUE` | 1 | 0 | 0 | 0 | 0 | 0 | 指标卡（单值） |
| `KPI_CARD` | n | 0 | 0 | 0 | 0 | 0 | 指标卡（带阈值样式） |
| `BASIC_COLUMN` | 1 | n | 0 | 0 | 0 | 0 | 柱状图 |
| `GROUPED_COLUMN` | n | n | 1 | 0 | 0 | 0 | 簇状柱状图 |
| `STACKED_COLUMN` | n | n | 1 | 0 | 0 | 0 | 堆积柱状图 |
| `PERCENT_STACKED_COLUMN` | n | n | 1 | 0 | 0 | 0 | 百分比堆积柱状图 |
| `WATERFALL_COLUMN` | 1 | n | 0 | 0 | 0 | 0 | 瀑布图 |
| `BULLET_COLUMN` | 2 | n | 0 | 0 | 0 | 0 | 子弹图 |
| `BASIC_BAR` | 1 | n | 0 | 0 | 0 | 0 | 条形图 |
| `BASIC_LINE` | 1 | n | 0 | 0 | 0 | 0 | 折线图 |
| `MULTI_LINE` | n | n | 1 | 0 | 0 | 0 | 多条折线图 |
| `STACKED_AREA` | n | 1 | 1 | 0 | 0 | 0 | 堆积面积图 |
| `PERCENT_STACKED_AREA` | n | 1 | 1 | 0 | 0 | 0 | 百分比堆积面积图 |
| `STACKED_COLUMN_WITH_LINE` | n | 1 | 1 | 1 | 0 | 0 | metric=柱子, metric_additional=折线 |
| `GROUPED_COLUMN_WITH_LINE` | n | 1 | 1 | 1 | 0 | 0 | metric=柱子, metric_additional=折线 |
| `STACKED_COLUMN_WITH_SYMBOL` | n | 1 | 1 | 1 | 0 | 0 | metric=柱子, metric_additional=标记 |
| `GROUPED_COLUMN_WITH_SYMBOL` | n | 1 | 1 | 1 | 0 | 0 | metric=柱子, metric_additional=标记 |
| `PIE` | 1 | 1 | 0 | 0 | 0 | 0 | 饼图 |
| `TREE_MAP` | 1 | n | 0 | 0 | 0 | 0 | 矩形树图 |
| `FUNNEL` | n | 0 | 0 | 0 | 0 | 0 | 漏斗图 |
| `HEAT_MAP` | 1 | 1 | 1 | 0 | 0 | 0 | 热力图 |
| `MULTIDIMENSIONAL_SANKEY` | 1 | n | 0 | 0 | 0 | 0 | 多维桑基图 |
| `PIVOT_TABLE` | n | n | n | 0 | 0 | 0 | 交叉表 |
| `WORD_CLOUD` | 1 | 1 | 0 | 0 | 0 | 0 | 词云 |
| `BASIC_BUBBLE` | 2 | n | 0 | 0 | 1 | 1 |气泡图 x=metric[0], y=metric[1] |
| `BASIC_SCATTER_PLOT` | 2 | 1 | 0 | 0 | 1 | 0 | 散点图  x=metric[0], y=metric[1]|

> `n` = 不限数量, `0` = 不支持, `2` = 最大2个


## metric 格式

```json
{"name": "毛营业额", "aggr": "SUM"}                         // SUM

{"name": "订单编码", "aggr": "CNT_DISTINCT", "alias": "订单数"}  // 指定聚合

{"name": "桌单价"}                           // 自定义字段如果在formula的计算公式中已聚合的情况下，就不再需要 aggr了
```

聚合方式: `SUM` / `AVG` / `MAX` / `MIN` / `CNT` / `CNT_DISTINCT`

## filters 格式

```json
// 维度筛选（WHERE）
{"name": "城市", "op": "IN", "value": ["上海市", "南京市"]}

// 日期范围
{"name": "营业日期", "op": "BT", "value": ["2026-01-01", "2026-02-28"]}

// 度量筛选（HAVING，聚合后过滤）
{"name": "毛营业额", "op": "GT", "value": ["1000000"]}
```

## sorting 格式

```json
// 单字段排序
[{"name": "毛营业额", "order": "DESC"}]
[{"name": "门店编号", "order": "ASC"}]

// 多字段排序
[{"name": "城市", "order": "ASC"}, {"name": "毛营业额", "order": "DESC"}]
```

## 字段名格式

`row`、`column`、`metric.name`、`filters.name`、`sorting.name`、`color_by.name`、`size_by.name` 都用字段名。

**普通字段** — 直接写平台上的字段名：
```json
"row": ["城市"]
"metric": [{"name": "毛营业额", "aggr": "SUM"}]
"filters": [{"name": "门店名称", "op": "EQ", "value": ["某门店"]}]
```

**日期子字段** — `字段名(粒度)`，自动按时间维度拆分：

| 写法 | 效果 | 示例输出 |
|------|------|----------|
| `"营业日期(年)"` | 按年汇总 | 2025 |
| `"营业日期(季度)"` | 按季度汇总 | 2025年第4季度 |
| `"营业日期(月)"` | 按月汇总 | 2025-11 |
| `"营业日期(周)"` | 按周汇总 | 2025年第44周 |
| `"营业日期(星期)"` | 按星期几汇总 | 星期六 |

```json
"row": ["营业日期(月)"]   // 按月看趋势
"filters": [{"name": "营业日期(年)", "op": "IN", "value": ["2026"]}]  // 筛选2026年
```

## filterType 速查

| 类型 | 含义 | 示例 |
|------|------|------|
| `EQ` | 等于 | `["A品牌"]` |
| `NE` | 不等于 | `["闭店"]` |
| `IN` | 在列表中 | `["上海市","北京市"]` |
| `NI` | 不在列表中 (Not In) | `["闭店","未开业"]` |
| `BT` | 范围 | `["2025-01-01","2025-12-31"]` |
| `GT` | 大于 | `["100"]` |
| `GE` | 大于等于 | `["100"]` |
| `LT` | 小于 | `["100"]` |
| `LE` | 小于等于 | `["100"]` |
| `CONTAINS` | 包含 | `["万达"]` |
| `IS_NULL` | 为空 | `[]` |
| `NOT_NULL` | 不为空 | `[]` |

## 建卡示例

**示例0：汇总值（row 为空） — 拿总计不拆维度**
```bash
# row=[] 不分组，直接返回汇总值，不会截断
$SCRIPT create-and-get '{"name":"汇总","ds_id":"<dataset_id>","chart_type":"BASIC_COLUMN","pg_id":"<page_id>","row":[],"metric":[{"name":"毛营业额","aggr":"SUM"}],"filters":[{"name":"日结日期","op":"BT","value":["2026-03-16","2026-03-22"]}]}'
# 输出: 毛营业额: 313230258.42
# 卡片保留供复核，用户要求清理时再 delete-cards
```

**示例1：指标卡 — 2月消费会员数**
```bash
$SCRIPT create-and-get '{"name":"2月消费会员数","ds_id":"<dataset_id>","chart_type":"SINGLE_VALUE","pg_id":"页面ID","metric":[{"name":"会员id","aggr":"CNT_DISTINCT"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-02-01","2026-02-28"]}]}'
# 输出: 会员id: 252335
```

**示例2：柱状图 — 各城市毛营业额（按营业额降序）**
```bash
$SCRIPT create-and-get '{"name":"各城市毛营业额","ds_id":"<dataset_id>","chart_type":"BASIC_COLUMN","pg_id":"页面ID","row":["城市"],"metric":[{"name":"毛营业额","aggr":"SUM"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-01-01","2026-02-28"]}],"sorting":[{"name":"毛营业额","order":"DESC"}]}'
# 输出: 毛营业额: ['2323360', '8483271', ...]  维度: ['南京市', '南通市', ...]
```

**示例3：交叉表 — 各城市×月份营业额（按城市+月份排序）**
```bash
$SCRIPT create-and-get '{"name":"城市×月份营业额","ds_id":"<dataset_id>","chart_type":"PIVOT_TABLE","pg_id":"页面ID","row":["城市"],"column":["营业日期(月)"],"metric":[{"name":"毛营业额","aggr":"SUM"}],"filters":[{"name":"营业日期","op":"BT","value":["2025-01-01","2026-02-28"]}],"sorting":[{"name":"城市","order":"ASC"},{"name":"营业日期(月)","order":"ASC"}]}'
# 输出: [城市 ,月份 ,毛营业额].....['上海','2025-01','123232323'],['上海','2025-02','1230232333'].....
# 排序: 先按城市名正序，再按月份正序
```

**示例4：多条折线图 — 各渠道月趋势**
```bash
$SCRIPT create-and-get '{"name":"渠道月趋势","ds_id":"<dataset_id>","chart_type":"MULTI_LINE","pg_id":"页面ID","row":["营业日期(月)"],"column":["销售类型名称"],"metric":[{"name":"毛营业额","aggr":"SUM"}],"filters":[{"name":"营业日期","op":"BT","value":["2025-01-01","2026-02-28"]}]}'
```

**示例5：组合图（柱+线） — 营业额柱状+消费人数折线**
```bash
$SCRIPT create-and-get '{"name":"营业额与用餐人数","ds_id":"<dataset_id>","chart_type":"STACKED_COLUMN_WITH_LINE","pg_id":"页面ID","row":["营业日期(月)"],"column":["销售类型名称"],"metric":[{"name":"毛营业额","aggr":"SUM"}],"metric_additional":[{"name":"用餐人数","aggr":"SUM"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-01-01","2026-02-28"]}]}'
```

**示例6：气泡图 — 各门店营业额vs实收金额（按城市着色，气泡大小=用餐人数）**
```bash
$SCRIPT create-and-get '{"name":"门店气泡图","ds_id":"<dataset_id>","chart_type":"BASIC_BUBBLE","pg_id":"页面ID","row":["城市","门店"],"metric":[{"name":"毛营业额","aggr":"SUM"},{"name":"菜品实收金额","aggr":"SUM"}],"size_by":[{"name":"用餐人数","aggr":"SUM"}],"color_by":[{"name":"城市"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-01-01","2026-02-28"]}]}'
# row=维度标签, metric[0]=x, metric[1]=y, color_by=颜色分组, size_by=气泡大小
```

## 完整工作流示例

**需求：做一张「2026年2月各城市外卖销售类型毛营业额 TOP10」交叉表**

```bash
# Step 1: 通过表id查字段，确认可用字段
$SCRIPT get-columns <dataset_id>
# → 确认: 城市(DIM), 毛营业额(METRIC), 销售类型名称(DIM), 营业日期(DATE)

# Step 2: 查枚举值（因为用了 IN/EQ 筛选，必须查）
$SCRIPT search-values <dataset_id> --name "销售类型名称" --search "外卖"
# → 确认值是 "外卖"

# Step 3: 建交叉表，自动取数
$SCRIPT create-and-get '{"name":"2月外卖各城市毛营业额","ds_id":"<dataset_id>","chart_type":"PIVOT_TABLE","pg_id":"<page_id>","row":["城市"],"column":["销售类型名称"],"metric":[{"name":"毛营业额","aggr":"SUM"}],"filters":[{"name":"营业日期","op":"BT","value":["2026-02-01","2026-02-28"]},{"name":"销售类型名称","op":"EQ","value":["外卖"]}],"sorting":[{"name":"毛营业额","order":"DESC"}]}'
```

> 💡 如果只做日期或数值筛选（无分类筛选），跳过 Step 2，两步搞定。



## 错误处理

| 状态码 | 处理 |
|--------|------|
| 500 | 终止，服务器问题 |
| 401 | 终止，登录失效 |
| 403 | 终止，无权限 |
| 404 | 终止，资源不存在 |

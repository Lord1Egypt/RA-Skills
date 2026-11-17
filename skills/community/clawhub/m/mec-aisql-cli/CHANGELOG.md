# 更新日志

本文件记录 mec-aisql-cli 的版本变更与修复历史，与 [TEST_REPORT.md](./TEST_REPORT.md) 的"修复记录"章节保持同步。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，按版本倒序排列。

## [0.3.2] - 2026-08-20

### 修复

- **修复 #7 (CLI)**: 交互式 `run` 流程在创建任务时未自动查找 `clientid` / `brandid`，导致工单字段缺失。在 `phase_create` 之前调用 `lookup_client_by_name` 与 `lookup_brand_by_name`，提取 `clientid` / `brandid` / `saleid` / `dtsaccount` / `dtspass` 一并传入。([commands/agent.py](./src/mec_aisql_cli/commands/agent.py))
- **修复 #8 (CLI)**: Bot 流程仅查到 `clientid` / `brandid`，未携带工单必填的 `saleid` / `dtsaccount` / `dtspass`。brand 查找时一并取这些字段并显式传入 `phase_create`，调用方传值优先。

### 后端协同修复

- **后端 #6**: 工单必填字段缺失 (`1641979135113` 字段必填)。
  - `SaleId` 为空兜底 `"000"`
  - `DtsAccount` / `DtsPass` 为空直接拒绝并提示"请先在品牌信息中配置"
  - `DtsPath` / `CrowDataPath` 为空兜底 `/{brand}/{yyyyMMdd}/{Id}` (日期无横杠)
  - `clientid` 找不到直接提示错误
- **后端 #9**: CLI 创建的任务在 MEC 前端展示时 `DtsPath` / `CrowDataPath` 显示为 `ID_任务名`（前端对 null 的兜底），不是动态路径。
  - 根因：`OpenAisqlController.Create` 一步到位 Insert，CLI 未传这两个字段，数据库存 null；而 MEC 前端走 `Add` + `Update` 两步，`Update` 方法（`Ml_AiHiveSqlService.cs` 第 688-699 行）会把 `/ID` 占位符替换为 `/{AiTaskId}`。
  - 修复：在 `Create` 方法生成 `AiTaskId` 后、`InsertAsync` 前，补一段与 `Ml_AiHiveSqlService.Update` 一致的逻辑——空值时兜底为 `/{brand}/{yyyyMMdd}/ID` 模板，再把 `/ID` 替换为 `/{AiTaskId}`（品牌含 `/` 时一并转成 `_`）。
  - 效果：CLI 创建的任务与 MEC 前端创建的任务在数据库里 `DtsPath` / `CrowDataPath` 格式一致，均为 `/{brand}/{yyyyMMdd}/{AiTaskId}`；perform 阶段的兜底正常不再触发。
- **后端 #10**: AISQL 生成的 SQL 关联逻辑错误，导致查询无结果。
  - 根因：`dwd_bdid_did_mzid` 表在 tablecon.txt 中**无关联信息**，AI 不知道该表怎么关联其他表，靠字段名猜测导致用 `mzid`（秒针cookie）错误关联 `spots_id`（点位ID）；同时跳过了 `ods_adm_bus` 作为桥接表，直接用 dwd 关联 dim；`log_type` 用了 `'clk'`（点击）而非 `'imp'`（曝光）。
  - 修复：在 `OpenAisqlController.cs` 的 gensql prompt 规则中补充 3 条（#15-17）：
    - #15：关联 `dim_adm_babel` 必须通过 `ods_adm_bus.mz_spot_id = dim_adm_babel.spots_id` 或 `mz_campaign_id = campaign_id`，严禁用 `mzid` 关联 `spots_id`
    - #16：关联 `dwd_bdid_did_mzid` 必须通过 `ods_adm_bus.bdid = dwd_bdid_did_mzid.bdid`，不要用 `mzid` 或 `uuid` 做跨表关联
    - #17：`log_type` 枚举 `imp`=曝光 / `clk`=点击，需求提到"曝光"用 `imp`
  - 效果：AI 生成 SQL 时会正确使用 `ods_adm_bus` 作为桥接表，通过 `mz_spot_id` 关联 `dim_adm_babel`，通过 `bdid` 关联 `dwd_bdid_did_mzid`，`log_type` 也会按需求正确选择。
- **后端 #11**: `BuildTableContextSummary` 的关联信息 `Take(12)` 硬编码截断，导致维度表关联（`dim_adm_babel.spots_id - ods_adm_bus.mz_spot_id`）被截断，AI 看不到关键关联。
  - 根因：关联信息按 mz_supertool 录入顺序排列，维度表关联（关联 ID 181837）排在最后，`Take(12)` 只取前 12 条直接截断；表筛选和字段筛选都有 `ScoreTableContext`/`ScoreColumnContext` 评分排序，唯独关联信息是裸 `Take(12)` 无评分。
  - 修复：新增 `ScoreJoinContext` 方法（维度表 `dim_*` +30、`babel` +15、关键字段 `spot/campaign/bdid/uuid` 等 +8、需求关键词匹配 +4），关联信息按评分降序排序后再 `Take(12)`。
  - 效果：`dim_adm_babel.spots_id - ods_adm_bus.mz_spot_id` 评分 53+（dim_30 + babel15 + spot8），排到前面不再被截断；非维度表关联（如 `ods_stm_bus.mzid`）评分仅 8，排到后面。

### 新增

- `run` 与 `bot` 流程在创建任务前自动从 MEC 系统按客户名/品牌名查找 `clientid` / `brandid` / `saleid` / `dtsaccount` / `dtspass`，用户/AI 只需提供客户名和品牌名。

## [0.3.1] - 2026-08-20

### 修复

- **修复 #5 (CLI)**: `aisql create` 接口的 `datetimefw` 落库为真实数组而非字符串，导致前端时间选择器渲染异常。新增 `datetime_utils.py` 与 `_normalize_datetimefw_in_data()`，按接口分别归一化：
  - `gen` / `validate` 用 `fmt="slash"` → `"YYYY-MM-DD/YYYY-MM-DD"`
  - `create` 用 `fmt="array"` → `'["YYYY-MM-DD","YYYY-MM-DD"]'` (字符串)

### 新增

- 新增 `datetime_utils.py` 模块，统一处理 `datetimefw` 多种输入格式 (`20260301-20260331`、`2026-03-01/2026-03-31`、`["2026-03-01","2026-03-31"]` 等) → `["YYYY-MM-DD","YYYY-MM-DD"]` 数组。
- 新增 `batch` 命令：批量执行多个查询任务 (从 JSON / CSV 文件读取)，支持全局参数覆盖、`--continue-on-error` / `--stop-on-error`、JSON 汇总输出。
- 新增 `aisql list` 子命令：分页查询任务列表，支持状态/客户/品牌/关键词/日期过滤。
- 新增 `aisql detail` 子命令：查看任务详情 (全字段)。
- 新增 `aisql sql` 子命令：查看任务 SQL (可保存到文件)。
- 新增 `aisql error` 子命令：查看任务错误信息。
- `aisql` 子命令数量 12 → 16。

## [0.3.0] - 2026-08-19

### 修复

- **修复 #1 (CLI)**: CTE 子查询 `SELECT *` 误判。`WITH t AS (SELECT * FROM a) SELECT COUNT(*) FROM t` 被错误判定为 `select_only` 并阻断。将 `SELECT *` 检查移到聚合检查之后，仅在无聚合/无 GROUP BY/无 DISTINCT 时才阻断。14/14 测试通过。
- **修复 #2 (环境)**: `pip install -e .` 在 TRAE 沙盒环境报错 `BackendUnavailable: Cannot import 'setuptools.build_meta'`。使用 `--no-build-isolation` 标志绕过隔离构建 (环境限制，不影响实际部署)。

### 后端协同修复

- **后端 #3**: `ValidateAiSql` 正则末尾 `\b` 导致 `dt >= '2026-03-30'` 匹配失败，仍提示"缺少时间过滤条件"。去掉正则末尾的 `\b`。
- **后端 #4**: `datetimefw` 仅支持 8 位纯数字格式，`["2026-03-30","2026-04-20"]` (带横杠) 无法匹配。扩展正则为 `\d{4}[-/]?\d{2}[-/]?\d{2}`，并新增引号内容提取。

### 新增

- 项目首版发布。
- 核心命令: `run` / `bot` / `result` / `login` / `logout` / `config` / `config-set` / `config-reset` / `version` / `help`。
- `aisql` 子命令 (12 个): `gen` / `translate` / `create` / `perform` / `status` / `watch` / `validate` / `agree` / `check-agreement` / `models` / `retry` / `stop`。
- SQL 类型守卫: 仅允许统计类查询 (COUNT/SUM/AVG/MAX/MIN/GROUP BY/DISTINCT)，阻断 DML/DDL/非聚合 SELECT/危险关键字。
- Bot 自动化模式: 全非交互式 + SQL 类型守卫 + 结构化 JSON 输出 + 12 种错误码。
- 持久化配置: `~/.minglue/aisql_config.json`。
- Token 管理: `~/.minglue/tokens.json`，401 自动刷新，网络错误指数退避重试。

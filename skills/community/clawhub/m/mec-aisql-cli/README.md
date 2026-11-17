# mec-aisql-cli

MEC 平台 AI SQL 生成、校验和任务管理 CLI 工具。支持从需求描述到 SQL 执行完成的端到端自动化流程，可部署为 Bot 自动化服务。

## 核心特性

- **`run` 一键全流程**: 生成 → 守卫 → 校验 → 创建任务 → 执行 → 监控，一条命令完成
- **`bot` Bot 自动化模式**: 全非交互式、SQL 类型守卫、结构化 JSON 输出
- **SQL 类型守卫**: 仅允许统计类查询 (COUNT/SUM/AVG/GROUP BY)，阻断 DML/DDL/非聚合 SELECT
- **`result` 结果查询**: 查询任务执行结果表、文件路径、DMS ID
- **持久化配置**: `config-set` 保存常用参数，避免重复输入
- **自动重试**: 网络请求失败自动重试，Token 过期自动刷新
- **统一输出**: 格式化输出 / JSON 输出 (`--json`) 两种模式
- **任务管理**: retry/stop 命令管理任务生命周期

## 安装

```bash
pip install -e .
```

## 快速开始

### 1. 登录

```bash
mec-aisql login --account YOUR_ACCOUNT --password YOUR_PASSWORD
```

### 2. 配置常用参数 (可选)

```bash
mec-aisql config-set --key client --value "某客户"
mec-aisql config-set --key brand --value "某品牌"
mec-aisql config-set --key datafrom --value "ADM"
mec-aisql config
```

### 3. 一键运行全流程 (交互模式)

```bash
mec-aisql run -c "统计某品牌曝光量" --datetimefw "20260301-20260331"
```

### 4. Bot 自动化模式 (非交互)

```bash
mec-aisql bot \
  -c "统计曝光量" \
  --client "客户A" --brand "品牌B" \
  --datafrom ADM --datetimefw "20260301-20260331" \
  --json
```

## 命令总览

### 核心流程

| 命令 | 说明 |
|------|------|
| `mec-aisql run` | 交互式全流程 (gen→guard→validate→create→perform→watch) |
| `mec-aisql bot` | Bot 自动化模式 (全非交互+SQL守卫+JSON输出) |
| `mec-aisql batch` | 批量执行多个查询任务 (从 JSON/CSV 文件读取) |
| `mec-aisql result` | 查询任务执行结果 |
| `mec-aisql aisql gen` | AI 生成 SQL |
| `mec-aisql aisql validate` | SQL 校验 |
| `mec-aisql aisql create` | 创建任务 |
| `mec-aisql aisql perform` | 执行任务 (创建工单) |
| `mec-aisql aisql status` | 查询任务状态 |
| `mec-aisql aisql watch` | 轮询监控任务 |
| `mec-aisql aisql list` | 分页查询任务列表 (支持状态/客户/品牌过滤) |
| `mec-aisql aisql detail` | 查看任务详情 |
| `mec-aisql aisql sql` | 查看任务 SQL (可保存到文件) |
| `mec-aisql aisql error` | 查看任务错误信息 |

### 辅助命令

| 命令 | 说明 |
|------|------|
| `mec-aisql aisql translate` | SQL 翻译成自然语言 |
| `mec-aisql aisql retry` | 重试失败任务 |
| `mec-aisql aisql stop` | 停止执行中的任务 |
| `mec-aisql aisql models` | 获取 AI 模型列表 |
| `mec-aisql aisql agree` | 签署使用协议 |
| `mec-aisql aisql check-agreement` | 检查协议状态 |

### 系统命令

| 命令 | 说明 |
|------|------|
| `mec-aisql login` | 登录并保存 Token |
| `mec-aisql logout` | 清除 Token |
| `mec-aisql config` | 查看配置 |
| `mec-aisql config-set` | 设置配置项 |
| `mec-aisql config-reset` | 重置配置 |
| `mec-aisql version` | 查看版本 |

## Bot 模式详解

### 工作流程

```
需求描述 → [1] AI生成SQL → [2] SQL类型守卫 → [3] 后端校验 → [4] 创建任务 → [5] 执行工单 → [6] 监控进度 → [7] 查询结果
                              │
                              ├─ 通过 (统计类) → 继续
                              ├─ 未通过 → 自动重新生成 (最多 --max-regen 次)
                              └─ 仍不通过 → 阻断，返回 SQL_TYPE_BLOCKED
```

### SQL 类型守卫规则

| SQL 类型 | 判定条件 | Bot 模式 |
|----------|----------|----------|
| `statistical` | 含 COUNT/SUM/AVG/MAX/MIN/GROUP BY/DISTINCT | 放行 |
| `select_only` | 纯 SELECT 无聚合 | 阻断 |
| `dml` | INSERT/UPDATE/DELETE | 阻断 |
| `ddl` | DROP/ALTER/TRUNCATE | 阻断 |
| `dangerous` | GRANT/REVOKE/LOAD 等 | 阻断 |

### Bot 返回的 JSON 结构

```json
{
  "success": true,
  "task_id": 123,
  "sql": "SELECT brand, COUNT(*) FROM ...",
  "sql_type": "statistical",
  "aggregate_functions": ["COUNT"],
  "status": "Succeeded",
  "table_name": "result_table_xxx",
  "file_router": "/path/to/result.csv",
  "order_id": "ORD123",
  "dms_query_id": "DMS456",
  "dms_export_id": "DMS789"
}
```

失败时返回:
```json
{
  "success": false,
  "error": "SQL_TYPE_BLOCKED",
  "message": "Bot 自动化仅允许统计类 SQL，已重试 2 次仍未通过",
  "sql_type": "select_only",
  "reason": "非统计类查询 (缺少聚合函数或 GROUP BY)",
  "sql": "SELECT name FROM users ..."
}
```

### Bot 部署示例

```bash
# 1. 预先登录 (Token 保存到 ~/.minglue/tokens.json)
mec-aisql login --account BOT_ACCOUNT --password BOT_PASSWORD

# 2. 预设默认参数
mec-aisql config-set --key client --value "默认客户"
mec-aisql config-set --key brand --value "默认品牌"
mec-aisql config-set --key datafrom --value "ADM"

# 3. Bot 调用 (JSON 输出供程序消费)
mec-aisql bot -c "统计曝光量" --datetimefw "20260301-20260331" --json

# 4. 查询历史任务结果
mec-aisql result --id 123 --json
```

### `run` vs `bot` 对比

| | `mec-aisql run` | `mec-aisql bot` |
|---|---|---|
| 交互模式 | 可交互，缺失参数会 prompt | 全非交互，参数缺失直接返回错误 |
| SQL 守卫 | 提示但允许继续 | 强制阻断非统计类 |
| 确认机制 | 可选 `--auto-create/--auto-perform` | 全自动，无确认 |
| 结果 | 文本输出 | 结构化 JSON (`--json`) |
| 重试 | 手动确认重试 | 自动重新生成 + 自动重试 |
| 认证检查 | 不检查 | 前置检查 `is_authenticated()` |
| 适用场景 | 人工操作 | Bot/自动化调度 |

## 配置项

配置存储在 `~/.minglue/aisql_config.json`:

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `base_url` | API 地址 | `https://mec.miaozhen.com/taskmng` |
| `model` | AI 模型 | `mlamp/deepseek-v4-flash` |
| `client` | 默认客户 | *(空)* |
| `brand` | 默认品牌 | *(空)* |
| `datafrom` | 默认数据来源 | *(空)* |
| `contype` | 默认分析类型 | *(空)* |
| `datetimefw` | 默认时间范围 | *(空)* |
| `timeout` | 请求超时 (秒) | `120` |
| `max_retries` | 最大重试次数 | `2` |

## 退出码

| 代码 | 含义 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 任务已停止 |
| 3 | 需要人工审核 |
| 124 | watch 超时 |

## 项目结构

```
mec-aisql-cli/
├── pyproject.toml
├── README.md
├── .gitignore
└── src/mec_aisql_cli/
    ├── __init__.py              # 版本信息
    ├── cli.py                   # 主入口 (run/bot/batch/result/login/config/version)
    ├── api_client.py            # API 客户端 (认证/重试/刷新/brand查找/AISQL API)
    ├── config.py                # 配置管理 (~/.minglue/aisql_config.json)
    ├── datetime_utils.py        # datetimefw 格式校验与归一化
    ├── output.py                # 统一输出格式化
    ├── sql_guard.py             # SQL 类型守卫 (统计类检查)
    └── commands/
        ├── __init__.py
        ├── aisql.py             # aisql 子命令 (gen/create/perform/validate/list/detail/sql/error/...)
        └── agent.py             # run/bot 端到端 Agent 流程 (7阶段+自动字段查找)
```

## 自动字段查找

`run` 和 `bot` 流程在创建任务前，自动从 MEC 系统按名称查找以下字段，用户/AI 只需提供客户名和品牌名：

| 字段 | 来源 | 用途 |
|------|------|------|
| `clientid` | 按客户名查 `Ml_Client` | 创建任务必填 |
| `brandid` | 按品牌名查 `Ml_Brand` | 创建任务必填 |
| `saleid` | brand 实体 | 创建工单必填 (空则兜底 "000") |
| `dtsaccount` | brand 实体 | 创建工单必填 (DMS 账号) |
| `dtspass` | brand 实体 | 创建工单必填 (DMS 密码) |

> - 若客户名或品牌名未匹配到任何记录，CLI 直接报错退出 (`run`) 或返回 `LOOKUP_FAILED` (`bot`)。
> - 若 brand 实体中未配置 `dtsaccount` 或 `dtspass`，工单创建会被后端拒绝并提示"请先在品牌信息中配置"。
> - `saleid` 为空时后端兜底为 `"000"`，不会阻断流程。

## datetimefw 格式

CLI 接受多种输入格式 (`2026-03-01/2026-03-31`、`20260301-20260331`、`["2026-03-01","2026-03-31"]`)，自动归一化：

| 接口 | 归一化格式 | 说明 |
|------|-----------|------|
| `aisql gen` | `"YYYY-MM-DD/YYYY-MM-DD"` | 后端拼进 AI prompt |
| `aisql validate` | `"YYYY-MM-DD/YYYY-MM-DD"` | 后端做正则匹配 |
| `aisql create` | `["YYYY-MM-DD","YYYY-MM-DD"]` (字符串) | 后端直接落库 |

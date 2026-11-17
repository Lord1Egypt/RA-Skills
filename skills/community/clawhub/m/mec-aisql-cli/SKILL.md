---
name: "mec-aisql-cli"
description: "MEC 平台 AI SQL 生成、校验与任务管理 CLI。当用户需要通过自然语言需求生成 HIVE SQL、创建/执行 SQL 任务、查询任务状态或结果、批量执行查询时调用。触发关键词：aisql、生成SQL、SQL任务、查询状态。"
---

# mec-aisql-cli

MEC 平台的 AI SQL 端到端 CLI 工具。从自然语言需求到 SQL 执行完成的全流程自动化，支持交互式、Bot 自动化和批量三种模式。

## 何时调用

| 场景 | 触发条件 | 推荐命令 |
|------|---------|---------|
| 生成 SQL | 用户给出客户/品牌 + 需求描述 | `mec-aisql bot` 或 `mec-aisql aisql gen` |
| 创建/执行任务 | 需要将 SQL 落库并提交工单执行 | `mec-aisql bot --auto-perform` |
| 查询任务状态 | 用户提到"查询 aisql/sql 状态" + 任务 ID | `mec-aisql aisql status --id <ID> --json` |
| 查询任务结果 | 需要结果表/文件路径/DMS ID | `mec-aisql result --id <ID> --json` |
| 批量执行 | 多个查询需求 | `mec-aisql batch --file tasks.json` |
| 监控任务进度 | 创建后轮询到终态 | `mec-aisql aisql watch --id <ID> --json` |

## 前置条件

```bash
# 1. 安装
pip install -e .

# 2. 登录（获取 Token，存储到 ~/.minglue/tokens.json）
mec-aisql login --account <ACCOUNT> --password <PASSWORD>

# 3. 配置常用参数（可选，存储到 ~/.minglue/aisql_config.json）
mec-aisql config-set --key client --value "客户名"
mec-aisql config-set --key brand --value "品牌名"
mec-aisql config-set --key datafrom --value "ADM"
mec-aisql config-set --key base_url --value "https://api.example.com"
```

## 命令总览

### 自动化流程

| 命令 | 说明 | 模式 |
|------|------|------|
| `mec-aisql run` | 交互式全流程（gen→guard→validate→create→perform→watch） | 人工 |
| `mec-aisql bot` | 全非交互式 + SQL 守卫 + JSON 输出 | AI/Bot |
| `mec-aisql batch` | 从 JSON/CSV 文件批量执行 | AI/Bot |
| `mec-aisql result` | 查询任务执行结果 | 通用 |

### aisql 子命令（16 个）

| 命令 | 说明 |
|------|------|
| `mec-aisql aisql gen` | AI 生成 SQL |
| `mec-aisql aisql validate` | SQL 校验（表名/时间过滤/DDL 检查） |
| `mec-aisql aisql create` | 创建任务 |
| `mec-aisql aisql perform` | 执行任务（创建工单） |
| `mec-aisql aisql status` | 查询任务状态 |
| `mec-aisql aisql watch` | 轮询监控任务到终态 |
| `mec-aisql aisql list` | 分页查询任务列表（支持状态/客户/品牌过滤） |
| `mec-aisql aisql detail` | 查看任务详情 |
| `mec-aisql aisql sql` | 查看任务 SQL（可保存到文件） |
| `mec-aisql aisql error` | 查看任务错误信息 |
| `mec-aisql aisql translate` | SQL 翻译成自然语言 |
| `mec-aisql aisql retry` | 重试失败任务 |
| `mec-aisql aisql stop` | 停止执行中的任务 |
| `mec-aisql aisql models` | 获取 AI 模型列表 |
| `mec-aisql aisql agree` | 签署使用协议 |
| `mec-aisql aisql check-agreement` | 检查协议状态 |

> `mec-aisql sql <子命令>` 是 `aisql` 的别名，调用方式完全相同。

### 系统命令

| 命令 | 说明 |
|------|------|
| `mec-aisql login` | 登录并保存 Token |
| `mec-aisql logout` | 清除 Token |
| `mec-aisql config` | 查看配置 |
| `mec-aisql config-set` | 设置配置项 |
| `mec-aisql config-reset` | 重置配置 |
| `mec-aisql version` | 查看版本 |

## 典型工作流

### Bot 全自动模式（推荐 AI 使用）

```bash
mec-aisql bot \
  -c "统计某品牌曝光量" \
  --client "客户A" --brand "品牌B" \
  --datafrom ADM --datetimefw "20260301-20260331" \
  --json
```

Bot 流程 7 阶段：

```
需求 → [1] AI生成SQL → [2] SQL类型守卫 → [3] 后端校验 → [4] 创建任务 → [5] 执行工单 → [6] 监控进度 → [7] 查询结果
                 │
                 ├─ 通过(统计类) → 继续
                 └─ 未通过 → 自动重新生成(最多 --max-regen 次) → 仍不通过 → 阻断
```

### 查询任务状态/结果

```bash
# 查状态
mec-aisql aisql status --id 123 --json

# 查结果
mec-aisql result --id 123 --json

# 查详情
mec-aisql aisql detail --id 123 --json

# 查 SQL
mec-aisql aisql sql --id 123 --json

# 查错误
mec-aisql aisql error --id 123 --json

# 轮询监控
mec-aisql aisql watch --id 123 --json
```

### 批量执行

```bash
mec-aisql batch --file tasks.json --json
mec-aisql batch --file tasks.csv --continue   # 出错继续
```

## 自动字段查找

`run` 和 `bot` 流程在创建任务前，自动从 MEC 系统按客户名/品牌名查找以下字段，用户/AI 只需提供客户名和品牌名：

| 字段 | 来源 | 用途 | 缺失处理 |
|------|------|------|---------|
| `clientid` | 按客户名查 `Ml_Client` | 创建任务必填 | 提示错误 |
| `brandid` | 按品牌名查 `Ml_Brand` | 创建任务必填 | 提示错误 |
| `saleid` | brand 实体 | 创建工单必填 | 兜底 `"000"` |
| `dtsaccount` | brand 实体 | 创建工单必填（DMS 账号） | 提示错误 |
| `dtspass` | brand 实体 | 创建工单必填（DMS 密码） | 提示错误 |

## datetimefw 格式

CLI 接受多种输入格式，自动归一化：

| 输入格式 | 示例 |
|---------|------|
| 斜杠分隔 | `2026-03-01/2026-03-31` |
| 连字符 | `20260301-20260331` |
| JSON 数组字符串 | `["2026-03-01","2026-03-31"]` |

归一化出口：

| 接口 | 归一化格式 | 说明 |
|------|-----------|------|
| `aisql gen` | `"YYYY-MM-DD/YYYY-MM-DD"` | 后端拼进 AI prompt |
| `aisql validate` | `"YYYY-MM-DD/YYYY-MM-DD"` | 后端做正则匹配 |
| `aisql create` | `["YYYY-MM-DD","YYYY-MM-DD"]`（字符串） | 后端直接落库 |

## SQL 类型守卫

Bot 模式仅允许统计类查询通过：

| SQL 类型 | 判定条件 | Bot 模式 |
|----------|----------|----------|
| `statistical` | 含 COUNT/SUM/AVG/MAX/MIN/GROUP BY/DISTINCT | 放行 |
| `select_only` | 纯 SELECT 无聚合 | 阻断 |
| `dml` | INSERT/UPDATE/DELETE | 阻断 |
| `ddl` | DROP/ALTER/TRUNCATE | 阻断 |
| `dangerous` | GRANT/REVOKE/LOAD 等 | 阻断 |

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误（API 失败、参数缺失、SQL 校验不通过等） |
| 2 | 任务已停止（watch 检测到 Stopped） |
| 3 | 需要人工审核（watch 检测到 NeedHumanReview） |
| 124 | watch 超时 |

## Bot 返回的 JSON 结构

成功时：

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

失败时：

```json
{
  "success": false,
  "error": "SQL_TYPE_BLOCKED",
  "message": "Bot 自动化仅允许统计类 SQL，已重试 2 次仍未通过",
  "sql_type": "select_only",
  "reason": "非统计类查询 (缺少聚合函数)"
}
```

## 项目结构

```
mec-aisql-cli/
├── src/mec_aisql_cli/
│   ├── cli.py              # 主入口（run/bot/batch/result/系统命令）
│   ├── commands/
│   │   ├── agent.py        # run_agent / run_bot 工作流编排
│   │   └── aisql.py        # aisql 16 个子命令
│   ├── api_client.py       # 后端 API 调用 + 自动字段查找
│   ├── config.py           # 配置管理
│   ├── datetime_utils.py   # datetimefw 归一化
│   ├── output.py           # 格式化输出
│   └── sql_guard.py        # SQL 类型守卫
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── TEST_REPORT.md
└── SKILL.md
```

# KDTS 迁移 Skill 用户输入示例

本文档展示用户可能提出的自然语言请求，以及 Skill 的处理方式。

## 语言版本

- **中文版**: 本文件 (`prompt-examples.zh.md`)
- **英文版**: [prompt-examples.md](./prompt-examples.md)

**请始终使用与用户相同的语言进行回复。** 两个版本都包含 AI Agent 应该能够正确处理的真实用户输入示例。

---

## 1. 完整迁移请求

### 用户输入 1

> 我想把 MySQL 数据库里的用户表迁移到 KaiwuDB，源数据库是 192.168.1.100:3306 上的 test_db，账号 root 密码 123456，目标 KaiwuDB 在本机 9092 端口。

### Skill 处理流程

1. **意图识别**: 完整迁移（结构 + 数据）
2. **缺失参数收集**:
   - 目标 KaiwuDB 用户名/密码 → 询问
   - 目标数据库名 → 询问或建议用同名
   - 迁移模式 → 全库还是指定表
3. **参数确认后执行**:
   - 测试源/目标连接
   - 列出源数据库表
   - 预览 DDL
   - 执行 DDL
   - 构建迁移脚本
   - 执行迁移并监控进度

---

### 用户输入 2

> 需要将 Oracle 19c 的 ERP 系统迁移到 KaiwuDB，包括结构和数据。Oracle 在 10.0.0.5，端口 1521，服务名 ORCL，用户名 erp_user。

### Skill 处理流程

1. **意图识别**: 完整迁移，Oracle 源
2. **缺失参数收集**:
   - Oracle 密码 → 询问
   - 源数据库/Schema → 可从连接获取或询问
   - 目标 KaiwuDB 连接信息 → 完整收集
3. **能力检查**: Oracle 支持完整迁移 → 可执行
4. **性能建议**: Oracle 大表建议启用 splitPk 并行

---

## 2. 仅结构迁移

### 用户输入

> 帮我把 PostgreSQL 的表结构同步到 KaiwuDB，我只需要建表，数据后面自己导。PostgreSQL 在 pg.example.com:5432，数据库 analytics。

### Skill 处理流程

1. **意图识别**: 仅 DDL 迁移（schema-only）
2. **执行流程**:
   - 测试源/目标连接
   - 读取源元数据
   - 预览 DDL
   - 展示生成的 DDL 供用户确认
   - 执行 DDL
   - 完成（跳过数据迁移）

---

## 3. 仅数据迁移

### 用户输入

> 目标表已经建好了，我只需要把 SQL Server 2019 的 orders 表数据导过去。SQL Server 在 192.168.1.50，数据库 sales，目标库是 kaiwudb_target。

### Skill 处理流程

1. **意图识别**: 仅数据迁移
2. **能力检查**: SQL Server 不支持完整迁移 → 需要显式表映射
3. **执行流程**:
   - 测试连接
   - 询问目标表名（默认同名 orders）
   - 构建迁移脚本（带 tables 字段）
   - 执行迁移
   - 监控进度

---

## 4. 多源迁移

### 用户输入

> 我们有三个数据库要迁移：MySQL 的用户库、Oracle 的订单库、PostgreSQL 的日志库，都要迁到同一个 KaiwuDB 集群。

### Skill 处理流程

1. **意图识别**: 批量多源迁移
2. **交互流程**:
   - 确认目标集群信息（只需一次）
   - 逐一收集每个源的连接信息
   - 建议按顺序执行（避免并发冲突）
3. **生成迁移计划**:
   ```
   1. MySQL users -> KWDB users_db
   2. Oracle orders -> KWDB orders_db
   3. PostgreSQL logs -> KWDB logs_db
   ```
4. **逐一执行**: 每个源完整流程后再下一个

---

## 5. 时间序列迁移

### 用户输入

> TDengine 3.x 的传感器数据要迁到 KaiwuDB 时序库。TDengine 在 172.16.0.10:6030，数据库 sensor_monitor，目标库是 kwdb_iot，时间范围是 2024 全年。

### Skill 处理流程

1. **意图识别**: 时间序列迁移
2. **能力检查**: TDengine 3.x 支持完整时序迁移
3. **特殊处理**:
   - 需要设置时间范围（beginDateTime, endDateTime）
   - 确认 target engine 是 TIMESERIES
   - 处理 TDengine 超级表/子表结构
4. **执行流程**:
   - 连接测试
   - 读取 TDengine 元数据
   - 预览时序 DDL
   - 转换为 KaiwuDB 时序表结构
   - 执行迁移

---

## 6. InfluxDB 迁移（两步法）

### 用户输入

> 我需要把 InfluxDB 2.x 的 metrics bucket 迁到 KaiwuDB 时序库。InfluxDB 在 influx.local:8086，org 是 myorg，token 是 xxxxxxx，bucket 是 metrics。

### Skill 处理流程

1. **意图识别**: InfluxDB 2.x → KaiwuDB（TIMESERIES）
2. **能力说明**: InfluxDB 支持元数据+数据（META_AND_DATA），但不支持完整迁移
3. **两步法提醒**:
   - 步骤 1：迁移 Schema（DDL）
   - 步骤 2：迁移数据
4. **交互流程**:
   - 确认两步法
   - 收集 InfluxDB 2.x 特有参数：org、token、bucket
   - 列出 measurements
   - 预览每个 measurement 对应的 DDL
   - 执行 Schema 迁移
   - 执行数据迁移
   - 验证结果

**注意**: InfluxDB 1.x 和 2.x 都使用 HTTP 协议，不通过 JDBC 连接。

---

## 7. MongoDB 迁移

### 用户输入

> MongoDB 的日志集合要迁过去，db 是 app_logs，collection 是 error_logs。我们只迁 status = 'error' 的记录。

### Skill 处理流程

1. **意图识别**: MongoDB → KWDB
2. **能力检查**: MongoDB 不支持元数据和完整迁移
3. **交互流程**:
   - 说明需要手动指定字段映射
   - 询问目标表结构（如已存在则跳过）
   - 设置 MongoDB query 过滤器：`{"status": "error"}`
4. **执行流程**:
   - 连接测试
   - 确认 target 表已存在
   - 构建带 query 的迁移脚本
   - 执行迁移

---

## 8. 迁移状态查询

### 用户输入

> 刚才发起的那个 MySQL 迁移任务现在怎么样了？跑完了吗？

### Skill 处理流程

1. **意图识别**: 任务状态查询
2. **信息收集**:
   - 如果用户提供了任务ID/脚本名 → 直接查询
   - 如果没有 → 询问任务标识或最近的任务
3. **返回信息**:
   - 当前状态：SUBMITTED / RUNNING / SUCCEEDED / FAILED
   - 进度百分比（如 RUNNING）
   - 开始时间、已用时间
   - 完成统计（如 SUCCEEDED）

---

## 9. 迁移问题排查

### 用户输入 1

> 迁移报错了，错误码 3004，提示 tag 数量超限。怎么解决？

### Skill 处理流程

1. **意图识别**: 错误排查
2. **错误分析**:
   - 错误码 3004 = METADATA_TAG_LIMIT_EXCEEDED
   - 含义：KaiwuDB 时序表 tag 列超过 128 或 primary tag 超过 4
3. **提供解决方案**:
   - 检查源表 tag 列数量
   - 建议保留核心 tag，其他转为 value 列
   - 或拆分到多个目标表
   - 给出具体修改示例

---

### 用户输入 2

> 连接测试一直失败，源数据库是 MySQL 在 remote.server.com。

### Skill 处理流程

1. **意图识别**: 连接问题排查
2. **诊断步骤**:
   - 询问具体错误码/信息
   - 检查 host 解析（DNS）
   - 检查端口可达性
   - 检查账号权限
   - 检查 KDTS 服务器网络配置
3. **提供排查命令**:
   ```bash
   nslookup remote.server.com
   telnet remote.server.com 3306
   mysql -h remote.server.com -u test -p
   ```

---

## 10. 迁移配置保存/加载

### 用户输入

> 把刚才的迁移配置保存下来，以后还要用。另外下次用的时候直接加载这个配置。

### Skill 处理流程

1. **意图识别**: 配置管理
2. **处理方式**:
   - 导出当前迁移配置为 JSON 文件
   - 建议保存路径（或由用户指定）
   - 说明如何下次加载使用
3. **配置示例**:
   ```json
   {
     "source": {
       "engine": "RELATIONAL",
       "type": "MYSQL",
       "host": "127.0.0.1",
       "port": 3306,
       "username": "user",
       "password": "pass",
       "dbName": "source_db"
     },
     "target": {
       "engine": "TIMESERIES",
       "type": "KAIWUDB",
       "host": "127.0.0.1",
       "port": 26257,
       "username": "root",
       "password": "pass",
       "dbName": "target_db",
       "isTarget": true
     },
     "tables": [],
     "data": {
       "batchSize": 1000,
       "core": {
         "transport": {
           "channel": {
             "speed": {
               "byte": 1048576,
               "record": 1000
             }
           }
         }
       },
       "enable": true,
       "fetchSize": 1000,
       "setting": {
         "errorLimit": {
           "percentage": 0.02
         },
         "speed": {
           "channel": 4
         }
       }
     }
   }
   ```

---

## 11. 危险操作拦截

### 用户输入

> 把正在跑的那个迁移任务杀掉。

### Skill 处理流程

1. **意图识别**: 任务终止（危险操作）
2. **安全检查**:
   - [WARNING] 警告：终止运行中的迁移可能导致数据不一致
   - 展示当前任务状态和进度
   - **要求用户二次确认**: "请输入 YES 确认终止"
3. **确认后执行**:
   - 调用 /datax/control (action=KILL)
   - 汇报终止结果
   - 提示数据修复建议

---

## 交互设计原则

### 参数收集顺序

1. KDTS 服务器地址（默认 localhost:8989）
2. 操作类型（迁移/查询/排查）
3. 源端配置（类型、连接、数据库）
4. 目标配置（连接、数据库、engine）
5. 迁移范围（全库/指定表）
6. 迁移模式（结构/数据/全部）

### 缺失参数处理

- **必选参数缺失**: 直接询问，列出所有缺失项
- **可选参数缺失**: 使用默认值并告知用户
- **参数歧义**: 提供选项让用户选择

### 错误反馈

- **操作前**: 清晰告知即将执行的操作和影响
- **操作中**: 实时进度反馈
- **操作后**: 结果总结 + 下一步建议

### 安全保护

- **高危操作**: 二次确认 + 影响说明
- **数据丢失风险**: 提醒备份
- **网络敏感操作**: 先测试连接再执行

---

## Skill 触发关键词

以下关键词会触发迁移 Skill：

### 核心动词
- 迁移、同步、导入、导出、搬运

### 数据库类型
- MySQL、Oracle、PostgreSQL、SQL Server
- TDengine、InfluxDB、OpenTSDB
- MongoDB、KaiwuDB、KWDB
- 时序库、关系库、文档库

### 功能操作
- 建表、DDL、结构迁移
- 数据迁移、全量、增量
- 连接测试、连通性
- 迁移任务、进度、状态
- 报错、失败、错误码

### 场景描述
- 异构、跨库、不同数据库
- 上云、搬迁、升级

---

**文档版本**: v1.0.0  
**最后更新**: 2026-08-03  
**适用 Skill 版本**: kwdb-data-migration v1.0.0

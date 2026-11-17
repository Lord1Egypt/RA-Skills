# KWDB 数据迁移技能 - 用户交互场景

本文档提供了用于验证 AI Agent 在数据库迁移过程中行为的交互场景。

## 语言版本

- **中文版**: 本文件 (`user-interaction-scenarios.zh.md`)
- **英文版**: [user-interaction-scenarios.md](./user-interaction-scenarios.md)

两个版本都包含相同的 8 个场景，使用各自的语言进行对话。AI Agent 将使用与用户相同的语言进行回复。

## 场景 1: MySQL 到 KaiwuDB（关系型）- 全量迁移

### 用户请求
````
帮我把 MySQL 的 order_system 数据库迁移到 KaiwuDB 的关系型数据库
````

### 预期的 AI Agent 回复

**步骤 1: 识别迁移意图**
````
[OK] 已识别迁移需求: MySQL (order_system) -> KaiwuDB (RELATIONAL)

请提供以下信息以开始迁移:

1. KDTS 服务器地址 (默认: http://127.0.0.1:8989)
2. MySQL 连接信息:
   - 主机地址:
   - 端口 (默认 3306):
   - 用户名:
   - 密码:
3. KaiwuDB 连接信息:
   - 主机地址 (默认 127.0.0.1):
   - 端口 (默认 26257):
   - 用户名 (默认 root):
   - 密码:
   - 目标数据库名 (默认 order_system):

[重要] 安全提醒: 迁移前请确保已备份源数据库和目标数据库!
````

**用户回复**
````
KDTS 地址: http://192.168.1.100:8989
MySQL: 192.168.1.50:3306, 用户名=root, 密码=mysql123
KaiwuDB: 127.0.0.1:26257, 用户名=root, 密码=kwdb_secret
目标数据库名: order_system
````

**步骤 2: 参数验证**
````
[OK] 参数收集完成，开始验证...

[系统内部调用]
1. ConfigValidator.validate_source_config()
2. ConfigValidator.validate_target_config()
3. 源能力检查: MySQL 支持全量迁移 [OK]

[OK] 参数验证通过
````

**步骤 3: 连接测试**
````
[信息] 正在测试数据库连接...

[系统内部调用]
1. KDTSClient.test_connection(source_config)
2. KDTSClient.test_connection(target_config)

[OK] MySQL 连接成功 (192.168.1.50:3306)
[OK] KaiwuDB 连接成功 (127.0.0.1:26257)
````

**步骤 4: 读取元数据**
````
[信息] 正在读取 MySQL 元数据...

[系统内部调用]
1. KDTSClient.read_metadata(source_config)

[OK] 发现 6 张表:
   - orders (15 列)
   - order_items (8 列)
   - customers (12 列)
   - products (10 列)
   - categories (5 列)
   - inventory (7 列)

   预估总数据量: 约 50,000 行
````

**步骤 5: 预览 DDL**
````
[信息] 正在生成 KaiwuDB DDL...

[系统内部调用]
1. KDTSClient.preview_ddl(target_config, source_db, metadata)

[警告] DDL 预览 (前 3 张表):
```sql
-- orders 表
CREATE TABLE orders (
    id INT8 PRIMARY KEY,
    customer_id INT8,
    order_time TIMESTAMP,
    total_amount DECIMAL(15,2),
    status VARCHAR(50)
);

-- order_items 表
CREATE TABLE order_items (
    id INT8 PRIMARY KEY,
    order_id INT8,
    product_id INT8,
    quantity INT,
    price DECIMAL(10,2)
);
```

[警告] 即将在 KaiwuDB 执行 DDL 创建 6 张表
[警告] 现有的目标表将被覆盖

是否确认执行? (是/否)
````

**用户回复**
````
是
````

**步骤 6: 执行 DDL**
````
[OK] 正在执行 DDL...

[系统内部调用]
1. KDTSClient.execute_ddl(target_config, ddl_script, auto_ddl=True)

[OK] DDL 执行成功!
   SQL 文件保存位置: /opt/kdts/data/sql/order_system_ddl.sql
   创建表数量: 6
   耗时: 0.8 秒
````

**步骤 7: 构建并执行迁移**
````
[信息] 正在构建迁移任务...

[系统内部调用]
1. KDTSClient.build_migration(source_config, target_config)

[OK] 迁移任务构建成功
   任务名称: MYSQL2KAIWUDB_1720000000000.json
   
   开始执行数据迁移...

[系统内部调用]
1. KDTSClient.execute_migration(script_names)

[信息] 迁移任务已启动，正在监控进度...
````

**步骤 8: 监控进度**
````
[信息] 迁移进度:
   |████████████████████████████████████████| 100%
   
   orders:        [████████████████████] 100% (12,345 行)
   order_items:   [████████████████████] 100% (45,678 行)
   customers:     [████████████████████] 100% (2,345 行)
   products:      [████████████████████] 100% (1,234 行)
   categories:    [████████████████████] 100% (56 行)
   inventory:     [████████████████████] 100% (3,456 行)

[OK] 迁移完成!
   总迁移行数: 65,114
   耗时: 45.2 秒
   平均速度: 1,440 行/秒

[报告] 迁移报告:
   - 成功表: 6/6
   - 失败表: 0/6
   - 错误行数: 0

[提示] 建议: 请通过比较源库和目标库的行数来验证数据完整性
````

---

## 场景 2: InfluxDB 到 KaiwuDB（时序型）- 两步迁移

### 用户请求
````
我想把 InfluxDB 的 metrics bucket 迁移到 KaiwuDB 的时序数据库
````

### 预期的 AI Agent 回复

**步骤 1: 识别迁移意图**
````
[OK] 已识别迁移需求: InfluxDB (metrics bucket) -> KaiwuDB (TIMESERIES)

[信息] InfluxDB 说明: 完整迁移（Schema + 数据）需要分两步:
   1. 第一步: 迁移表结构（Schema/DDL）
   2. 第二步: 迁移数据（Data）
   
   我将为您执行这两步操作。

请提供以下信息:

1. KDTS 服务器地址 (默认: http://127.0.0.1:8989)
2. InfluxDB 连接信息:
   - 版本 (1.x 或 2.x):
   - 主机地址:
   - 端口 (默认 8086):
   - 用户名:
   - 密码 (2.x 需要 token):
   - Bucket/Database 名称 (metrics):
3. KaiwuDB 连接信息:
   - 主机地址 (默认 127.0.0.1):
   - 端口 (默认 26257):
   - 用户名 (默认 root):
   - 密码:
   - 目标数据库名 (默认 metrics):

[重要] 安全提醒: 迁移前请确保已备份源数据和目标数据库!
````

**用户回复**
````
KDTS 地址: http://192.168.1.100:8989
InfluxDB 2.x: 192.168.1.60:8086, token=my-influxdb-token, bucket=metrics
KaiwuDB: 127.0.0.1:26257, 用户名=root, 密码=kwdb_secret
目标数据库名: metrics_ts
````

**步骤 2: 第一步 - Schema 迁移**
````
[信息] 第一步: 迁移表结构（Schema）

[信息] 正在读取 InfluxDB 元数据...

[系统内部调用]
1. KDTSClient.read_metadata(source_config)

[OK] 发现 3 个 measurement:
   - cpu_usage (tags: host, region; fields: usage, temperature)
   - memory_usage (tags: host, region; fields: used, free)
   - network_io (tags: host, interface; fields: rx_bytes, tx_bytes)

[信息] 正在生成 KaiwuDB 时序表 DDL...

[警告] DDL 预览（cpu_usage 示例）:
```sql
CREATE TABLE cpu_usage (
    time TIMESTAMP,
    host VARCHAR(100) PRIMARY TAG,
    region VARCHAR(50) TAG,
    usage FLOAT8 FIELD,
    temperature FLOAT8 FIELD
);
```

[警告] 即将执行 DDL 创建 3 张时序表

是否确认执行? (是/否)
````

**用户回复**
````
是
````

````
[OK] DDL 执行成功!
   创建表数量: 3
   耗时: 0.5 秒

[信息] 第二步: 开始迁移数据...
````

**步骤 3: 第二步 - 数据迁移**
````
[信息] 正在构建数据迁移任务...

[系统内部调用]
1. KDTSClient.build_migration(source_config, target_config)

[OK] 数据迁移任务构建成功
   任务名称: INFLUXDB2X2KAIWUDB_1720000000000.json

[信息] 正在迁移数据...
````

**步骤 4: 监控并完成**
````
[信息] 迁移进度:
   |████████████████████████████████████████| 100%

   cpu_usage:    [████████████████████] 100% (1,234,567 行)
   memory_usage: [████████████████████] 100% (1,234,567 行)
   network_io:   [████████████████████] 100% (1,234,567 行)

[OK] 迁移完成!
   总迁移行数: 3,703,701
   耗时: 180.5 秒
   平均速度: 20,520 行/秒

[报告] 迁移报告:
   - Schema 迁移: [OK] 成功 (3 张表)
   - 数据迁移: [OK] 成功 (3,703,701 行)
   - 错误行数: 0

[提示] 建议: 请验证数据完整性，特别注意时序数据的时间戳和标签
````

---

## 场景 3: 错误处理 - 连接失败

### 用户请求
````
帮我迁移数据
````

### 预期的 AI Agent 回复
````
[OK] 请提供更多信息以便我帮您迁移数据:

1. 源数据库类型 (MySQL, Oracle, PostgreSQL, InfluxDB 等)
2. 目标 KaiwuDB 引擎类型 (RELATIONAL 或 TIMESERIES)
3. KDTS 服务器地址
4. 源数据库连接信息
5. 目标 KaiwuDB 连接信息
````

**用户回复**
````
源: MySQL at 192.168.1.50:3306, 用户名=root, 密码=错误的密码
目标: KaiwuDB RELATIONAL
KDTS: http://192.168.1.100:8989
````

### 预期的 AI Agent 回复
````
[信息] 正在测试连接...

[错误] MySQL 连接失败!
   错误信息: Access denied for user 'root'@'192.168.1.100'

[提示] 可能的原因:
   1. 密码错误
   2. 用户没有从该 IP 连接的权限
   3. MySQL 服务未启动

[建议] 推荐操作:
   - 验证用户名和密码
   - 检查 MySQL 用户权限
   - 使用正确的密码重试

请提供正确的 MySQL 连接信息。
````

---

## 场景 4: 不支持的源类型

### 用户请求
````
帮我把 Redis 的数据迁移到 KaiwuDB
````

### 预期的 AI Agent 回复
````
[警告] 抱歉，Redis 目前不支持作为源数据库。

当前支持的源数据库类型:
[OK] 关系型数据库: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse
[OK] 时序数据库: TDengine 2.x/3.x, InfluxDB 1.x/2.x, OpenTSDB
[OK] 其他: KaiwuDB, MongoDB, FTP, HDFS

[替代方案] 可选的替代方案:
1. 如果 Redis 中的数据可以导出为 CSV/JSON 文件，可以使用 FTP/HDFS 方式导入
2. 先将 Redis 数据迁移到支持的数据库，再迁移到 KaiwuDB

是否需要了解具体的操作方法?
````

---

## 场景 5: 模糊请求澄清

### 用户请求
````
我想把我的数据迁移到 KaiwuDB
````

### 预期的 AI Agent 回复
````
好的！请先告诉我以下信息:

1. 源数据库类型是什么?
   - MySQL / Oracle / PostgreSQL / SQL Server / ClickHouse
   - TDengine / InfluxDB / OpenTSDB (时序数据库)
   - MongoDB / FTP / HDFS

2. 目标 KaiwuDB 使用什么引擎?
   - RELATIONAL (关系型)
   - TIMESERIES (时序型)

3. KDTS 服务器地址是多少? (默认 http://127.0.0.1:8989)

提供这些信息后，我将引导您完成完整的迁移流程。
````

---

## 场景 6: 配置查询

### 用户请求
````
KDTS 服务地址应该怎么配置?
````

### 预期的 AI Agent 回复
````
KDTS 服务器地址支持多种配置方式（按优先级从高到低）:

### 方式 1: 环境变量 (推荐用于 CI/CD)
```bash
# 方式 A: 完整地址
export KDTS_BASE_URL="http://your-kdts-server.com:8989"

# 方式 B: 分别配置主机和端口
export KDTS_HOST="your-kdts-server.com"
export KDTS_PORT="8989"
```

### 方式 2: 配置文件 (kdts_config.json)
在项目根目录创建配置文件:
```json
{
  "base_url": "http://your-kdts-server.com:8989",
  "api_prefix": "/kdts/api/v1",
  "timeout": 30
}
```

### 方式 3: 默认值
如果不配置，将使用默认地址: http://127.0.0.1:8989

### 当前配置检查
需要我帮您检查当前的 KDTS 配置吗?

[提示] 提示: 当您开始迁移时，如果我发现 KDTS 地址不可用，会主动询问您。
````

---

## 场景 7: 迁移状态查询

### 用户请求
````
我之前启动了一个迁移任务，帮我看看完成了吗?
````

### 预期的 AI Agent 回复
````
好的，请提供迁移任务名称，例如:
- MYSQL2KAIWUDB_1720000000000
- INFLUXDB2X2KAIWUDB_1720000000000

如果您不记得任务名称，可以提供:
1. KDTS 服务器地址
2. 迁移时间范围（例如: 今天上午 10 点的迁移）

我可以帮您查询最近的迁移任务状态。
````

**用户回复**
````
任务名是 MYSQL2KAIWUDB_1720000000000
KDTS 在 http://192.168.1.100:8989
````

### 预期的 AI Agent 回复
````
[信息] 正在查询任务状态...

[系统内部调用]
1. KDTSClient.query_status(script_name)

[信息] 任务状态: [OK] 已完成
   
   任务名称: MYSQL2KAIWUDB_1720000000000
   状态: SUCCEEDED
   开始时间: 2024-03-15 10:23:45
   结束时间: 2024-03-15 10:24:30
   耗时: 45 秒

[信息] 迁移详情:
   总表数: 6
   总行数: 65,114
   错误行数: 0

[OK] 迁移任务已成功完成!
````

---

## 场景 8: InfluxDB 2.x 复杂边界条件迁移

### 用户请求
````
我有一个复杂的 InfluxDB 2.x 数据库迁移需求:
- bucket: production_metrics (包含 50 个 measurement，超过 1 亿条数据)
- 需要保留原始 tag 和 field 结构
- 目标 KaiwuDB 时序库名称: metrics_archive
- 迁移时间范围: 2024-01-01 至 2024-12-31
````

### 预期的 AI Agent 回复

**步骤 1: 识别复杂迁移需求**
````
[OK] 已识别复杂迁移需求: InfluxDB 2.x (production_metrics) -> KaiwuDB (TIMESERIES)

[警告] 检测到高复杂度迁移场景:
  - Measurement 数量: 50 个
  - 预估数据量: 超过 1 亿条
  - 时间跨度: 1 年
  - 涉及多租户/多 region 标签

[信息] 建议的迁移策略:
  1. 分批迁移（按时间月份或 measurement）
  2. 增加并发度（建议 8-16 通道）
  3. 使用批量提交模式（batch_size: 10000）

请确认以下迁移配置:

KDTS 服务器地址 (默认: http://127.0.0.1:8989):
InfluxDB 2.x 连接信息:
  - 主机/端口:
  - 组织:
  - Token (或 用户名/密码):
  - Bucket: production_metrics
KaiwuDB 连接信息 (engine: TIMESERIES):
  - 主机/端口 (默认 127.0.0.1:26257):
  - 用户名/密码:
  - 目标数据库: metrics_archive
迁移参数:
  - 时间范围: 2024-01-01 ~ 2024-12-31
  - 分批策略（按月/按 measurement）:
  - 并发度 (默认 8):
  - 是否包含所有 tag/field (默认: 是):

[重要] 安全提醒:
  - 迁移前请备份源 bucket!
  - 大量数据迁移建议在业务低峰期进行
  - 迁移可能需要数小时完成
````

**用户回复**
````
KDTS: http://10.0.0.100:8989
InfluxDB: 192.168.1.60:8086, org=myorg, token=secret-token, bucket=production_metrics
KaiwuDB: 127.0.0.1:26257, 用户名=root, 密码=kwdb, 数据库=metrics_archive
时间范围: 2024-01-01 ~ 2024-12-31
分批策略: 按月份
并发度: 16
包含所有 tag/field: 是
````

**步骤 2: 验证并规划迁移**
````
[信息] 验证连接...
  [OK] InfluxDB 2.x 连接成功
  [OK] KaiwuDB 连接成功

[信息] 分析源 bucket 结构...
  Measurements (50 个):
    - cpu_usage: tags(host, region, pod), fields(usage, temperature, load)
    - memory_usage: tags(host, region, pod), fields(used, free, swap)
    - network_io: tags(host, region, interface), fields(rx_bytes, tx_bytes, errors)
    - ... (另外 47 个 measurement)
  
  数据统计:
    - 总记录数: 127,345,678
    - 平均记录/秒: 约 4000（峰值约 15000）
    - 预估迁移时间: 3-5 小时

[警告] 边界条件检测:
  [警告] 部分 measurement 存在动态标签（如 request_id, trace_id）
  [信息] 建议: 动态标签转换为 FIELD 或创建索引
  [信息] 自动处理: 将保留为 TAG 但限制唯一值数量

[信息] 生成迁移计划（按月份分批）:
  批次 1: 2024-01 (10,612,140 条记录)
  批次 2: 2024-02 (9,318,752 条记录)
  ...
  批次 12: 2024-12 (11,234,567 条记录)

[重要] 迁移前最后确认:
  - 是否跳过空 measurement? (默认: 否)
  - 是否忽略错误记录? (默认: 是，错误率 < 0.1%)
  - 失败批次是否自动重试? (默认: 是，最多 3 次)

是否开始执行迁移计划? (是/否)
````

**用户回复**
````
确认开始，跳过空 measurement，忽略错误，自动重试
````

**步骤 3: 执行迁移 - Schema 阶段**
````
[信息] 步骤 1/2: Schema 迁移（所有 measurement）...

[信息] 生成 DDL (50 个 measurement):
  [信息] cpu_usage -> CREATE TABLE cpu_usage (...)
  [信息] memory_usage -> CREATE TABLE memory_usage (...)
  [信息] network_io -> CREATE TABLE network_io (...)
  ...
  
[警告] DDL 预览（cpu_usage 示例）:
  CREATE TABLE cpu_usage (
    time TIMESTAMP,
    host VARCHAR(255) PRIMARY TAG,
    region VARCHAR(100) TAG,
    pod VARCHAR(255) TAG,
    usage DOUBLE FIELD,
    temperature DOUBLE FIELD,
    load DOUBLE FIELD
  );

[警告] 即将创建 50 个时序表
[警告] 预估存储: 127M 记录 × 约 200 字节 = 24 GB

是否确认执行 DDL? (是/否)
````

**用户回复**
````
是
````

**步骤 4: 执行迁移 - 数据阶段**
````
[OK] DDL 执行成功! 创建表数量: 50

[信息] 步骤 2/2: 数据迁移（12 个批次）...

[信息] 批次 1/12: 2024-01 (10,612,140 条记录)
  [信息] 进度: 25% (2,653,035 条记录) - 180MB/分钟
  [信息] 进度: 50% (5,306,070 条记录) - 185MB/分钟
  [信息] 进度: 75% (7,959,105 条记录) - 190MB/分钟
  [信息] 进度: 100% (10,612,140 条记录) - 完成!
  [OK] 批次 1 成功! 耗时: 55 分钟

[信息] 批次 2/12: 2024-02 (9,318,752 条记录)
  ...
  [OK] 批次 2 成功! 耗时: 48 分钟

... (中间批次省略)

[信息] 批次 12/12: 2024-12 (11,234,567 条记录)
  ...
  [OK] 批次 12 成功! 耗时: 62 分钟

[OK] 所有批次迁移完成!
  总耗时: 7 小时 15 分钟
  平均速度: 250 MB/分钟

[信息] 错误处理统计:
  错误记录: 12,345 (0.0097%)
  自动重试成功: 12,100
  跳过记录: 245 (已记录到 error.log)

[报告] 迁移报告:
  [OK] Schema 迁移: 成功 (50 张表)
  [OK] 数据迁移: 成功 (127,333,333 条记录)
  [信息] 错误记录: 245 (已记录)

[重要] 验证建议:
  1. 检查各 measurement 的记录数是否匹配
  2. 验证数据类型转换正确
  3. 抽样检查 tag/field 值
  4. 运行关键查询验证性能

迁移是否成功? 建议运行验证脚本确认后再删除源数据。
````

---

## 场景 9: MySQL 到 KaiwuDB (TIMESERIES) - Tag 选择

### 用户请求
````
我有一个 MySQL 表 sensor_data 存储 IoT 传感器读数:
- id (BIGINT, 主键)
- device_id (VARCHAR(50))
- location (VARCHAR(100))
- sensor_type (VARCHAR(30))
- reading_time (DATETIME)
- temperature (DECIMAL(10,2))
- humidity (DECIMAL(10,2))

我想将这个表迁移到 KaiwuDB 时序表，以便进行时序查询。
````

### 期望的 AI Agent 响应

**步骤 1: 分析并提供 Tag 配置**
````
[成功] MySQL -> KaiwuDB (TIMESERIES) 迁移已识别

[信息] 分析源表结构...
表: sensor_data (7 列)
- id (BIGINT, 主键)
- device_id (VARCHAR(50))
- location (VARCHAR(100))
- sensor_type (VARCHAR(30))
- reading_time (DATETIME)
- temperature (DECIMAL(10,2))
- humidity (DECIMAL(10,2))

[信息] 对于时序表，您需要配置 tag 和 value 字段:

[警告] TIMESERIES 表要求:
- 至少有 1 个 PRIMARY TAG (最多 4 个)
- 可以有 SECONDARY TAGS (可选)
- 其余列成为 VALUE FIELDS
- reading_time 自动选为 TIME 列 (必需)

请为 sensor_data 表配置 tag:

PRIMARY TAG 选择 (1-4 个必需, 最多 4 个):
[ ] id (BIGINT)
[ ] device_id (VARCHAR(50))
[ ] location (VARCHAR(100))
[ ] sensor_type (VARCHAR(30))

[信息] 提示: Primary tags 用于索引和过滤
[信息] 推荐: device_id, location, sensor_type (常用过滤列)

SECONDARY TAG 选择 (可选, 总共最多 128 个 tag):
[ ] id (BIGINT)
[ ] device_id (VARCHAR(50))
[ ] location (VARCHAR(100))
[ ] sensor_type (VARCHAR(30))
````

**用户响应**
````
PRIMARY TAGS: device_id, location, sensor_type (选择 3 个)
SECONDARY TAGS: (无)
````

**步骤 2: 显示带 Tag 配置的 DDL 预览**
````
[信息] 使用您的 tag 配置生成 DDL...

[成功] Tag 配置已保存:
- PRIMARY TAGS (3 个): device_id, location, sensor_type
- SECONDARY TAGS: 无
- VALUE FIELDS: id, temperature, humidity
- TIME 列: reading_time

[警告] DDL 预览:
```sql
CREATE TABLE sensor_data
(
    reading_time TIMESTAMPTZ NOT NULL,
    id BIGINT,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2)
)
TAGS
(
    device_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(30) NOT NULL
)
PRIMARY TAGS (device_id, location, sensor_type);
```

[信息] 统计:
- 总列数: 4 个值列 + 3 个标签 = 7 个
- Primary tags: 3 个 (限制: 4 个)
- 预估 DDL 大小: ~1.5KB

确认执行此 DDL? (是/否)
````

**用户响应**
````
是
````

**步骤 3: 执行并显示结果**
````
[信息] 正在执行 DDL...

[系统内部调用]
1. KDTSClient.execute_ddl(target_config, ddl)

[成功] DDL 执行成功!
  已创建表: sensor_data
  耗时: 0.15 秒

[信息] 下一步: 配置 DataX 进行数据迁移
  是否使用默认或自定义配置?
````

---

## 场景 10: InfluxDB 1.x 到 KaiwuDB (TIMESERIES) - 自动 Tag 映射

### 用户请求
````
我需要将 InfluxDB 1.x 数据库迁移到 KaiwuDB TIMESERIES:
- 数据库: metrics
- 包含多个 measurements，部分有 5 个以上的 tags
- 希望保留所有数据

请检查是否可以迁移并处理 tag 问题。
````

### 期望的 AI Agent 响应

**步骤 1: 分析 InfluxDB 结构**
````
[成功] InfluxDB 1.x -> KaiwuDB (TIMESERIES) 迁移已识别

[信息] 注意: InfluxDB 时序源只能迁移到 KaiwuDB TIMESERIES
  (不兼容 RELATIONAL 引擎 - KDTS 强制执行此限制)

[信息] 分析源数据库结构...

[系统内部调用]
1. KDTSClient.read_metadata(source_config)

[信息] 找到 5 个 measurements:
- cpu_usage: tags(host, region, datacenter, service, priority), fields(usage, temperature)
- memory_usage: tags(host, region), fields(used, free)
- disk_io: tags(host, device, region), fields(read_bytes, write_bytes)
- network: tags(host, interface, region, datacenter), fields(rx, tx)
- request_log: tags(service, endpoint, method, status_code, region, datacenter), fields(latency)

[警告] Tag 溢出检测:
- cpu_usage: 5 个 tags (超过 PRIMARY 限制 4 个)
- request_log: 6 个 tags (超过 PRIMARY 限制 4 个)

[信息] KDTS 自动映射规则:
- 前 4 个 tags -> PRIMARY TAGS
- 剩余 tags -> SECONDARY TAGS

cpu_usage 自动映射示例:
- PRIMARY TAGS: host, region, datacenter, service
- SECONDARY TAGS: priority
- VALUE FIELDS: usage, temperature

request_log 自动映射示例:
- PRIMARY TAGS: service, endpoint, method, status_code
- SECONDARY TAGS: region, datacenter
- VALUE FIELDS: latency

是否使用此自动映射或手动调整?
````

**用户响应**
````
使用自动映射，看起来不错
````

**步骤 2: 预览 DDL**
````
[信息] 使用自动映射的 tags 生成 DDL...

[警告] DDL 预览 (5 个 measurements 中的 2 个):

```sql
-- cpu_usage (5 个 tags -> 4 个 PRIMARY + 1 个普通标签)
CREATE TABLE cpu_usage
(
    time TIMESTAMPTZ NOT NULL,
    usage DOUBLE,
    temperature DOUBLE
)
TAGS
(
    host VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    datacenter VARCHAR(50) NOT NULL,
    service VARCHAR(100) NOT NULL,
    priority VARCHAR(20)
)
PRIMARY TAGS (host, region, datacenter, service);

-- request_log (6 个 tags -> 4 个 PRIMARY + 2 个普通标签)
CREATE TABLE request_log
(
    time TIMESTAMPTZ NOT NULL,
    latency DOUBLE
)
TAGS
(
    service VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT NOT NULL,
    region VARCHAR(50),
    datacenter VARCHAR(50)
)
PRIMARY TAGS (service, endpoint, method, status_code);
```

[信息] 要创建的总表数: 5
- 2 个表使用自动调整的标签 (最多 4 个 PRIMARY TAGS)
- 3 个表使用标准 PRIMARY TAGS (<= 4 个 tags)

确认对所有 5 个表执行 DDL? (是/否)
````

**用户响应**
````
是
````

**步骤 3: 执行并继续**
````
[信息] 正在对 5 个表执行 DDL...

[系统内部调用]
1. KDTSClient.execute_ddl(target_config, ddl_batch)

[成功] 所有 5 个表创建成功!
  - cpu_usage (SECONDARY TAG: priority)
  - memory_usage
  - disk_io
  - network (SECONDARY TAG: datacenter)
  - request_log (SECONDARY TAGS: region, datacenter)

[信息] 准备进行数据迁移...

重要提示: KaiwuDB 表已创建，包含:
- PRIMARY TAGS: 用于高效索引和过滤
- SECONDARY TAGS: 已索引但较少查询
- VALUE FIELDS: 测量数据值

下一步: 配置 DataX 参数进行数据迁移
````

---

## 场景 11: Oracle 到 KaiwuDB (TIMESERIES) - 新增 t1 主标签列

### 用户请求

```
将 Oracle 的 oracle_kwdb 库迁移到 KaiwuDB 时序库（库名 oracle_kwdb）。
Oracle 没有时序列，新增 t1 列作为时序主标签，默认值为 1。
Oracle 连接: ORACLE_KWDB/123456 @ 127.0.0.1:1521 (SID: ORCL)
```

### 预期的 AI Agent 回复

````
[信息] 识别迁移意图: Oracle -> KaiwuDB (TIMESERIES)，库名 oracle_kwdb
[信息] Oracle 注意: 源 dbName 需使用 owner 名（ORACLE_KWDB，大写）

[OK] 连接测试通过（Oracle + KaiwuDB）

[信息] 读取 Oracle 元数据: 表 TEST_TB，13 列（TS, C1-C12）
[信息] Oracle 表名/列名均为大写

[信息] 新增 t1 主标签列（Oracle 无此列）:
  使用 build_added_column('t1', 1, source_type='ORACLE', is_tag=True, is_primary_tag=True)
  - 整数默认值 1 → INT4（可作主标签，自动 NOT NULL）
  - sourceColumnType = NUMBER(10,0)（精确映射 INT4，避免回退 FLOAT）

[警告] DDL 预览:
CREATE TS DATABASE "oracle_kwdb";
CREATE TABLE "oracle_kwdb"."TEST_TB" (
    "TS" TIMESTAMPTZ NOT NULL,
    "C1" INT2, "C2" INT4, "C3" INT8, "C4" FLOAT4, "C5" FLOAT4,
    "C6" VARCHAR(5), "C7" CHAR(1), "C8" NCHAR(10),
    "C9" VARCHAR(10), "C10" NVARCHAR(10), "C11" VARBYTES, "C12" TIMESTAMPTZ
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
是否执行该 DDL? (yes/no)

用户: yes

[OK] DDL 执行成功

[信息] 构建迁移脚本（显式表映射）:
  源列: TS,C1,...,C12,1 as t1（SQL 表达式生成默认值 1）
  目标列: TS,C1,...,C12,t1（真实列名，target_columns）
[OK] 迁移启动: ORACLE2KAIWUDB_xxx.json

[报告] 迁移完成: SUCCEEDED
[提示] 请对比源/目标行数验证数据完整性
````

---

## 场景 12: MongoDB 到 KaiwuDB (TIMESERIES) - SKILL 生成 DDL + query 过滤

### 用户请求

```
将 MongoDB 的 mongo_kwdb 库迁移到 KaiwuDB 时序库（库名 mongo_kwdb）。
collectionName: test_tb; column 14 列(ts date, c1-c2 int, c3 long, c4-c5 double,
c6 bool, c7-c10 string, c11 bytes, c12 date, t1 int);
query 过滤: {"t1":{"$gte":1,"$lt":8}}
地址: 127.0.0.1:27017, root/123456
```

### 预期的 AI Agent 回复

````
[信息] 识别迁移意图: MongoDB -> KaiwuDB (TIMESERIES), 库名 mongo_kwdb
[信息] MongoDB 说明: KDTS 不支持 MongoDB 类型映射,建表仅两种方式
      (① 提前建表 ② SKILL 根据用户提供的表信息生成 DDL)

[OK] 连接测试通过 (MongoDB + KaiwuDB)

[信息] 按用户提供的表信息 + 类型映射生成 DDL
      (int→INT4, long→INT8, double→FLOAT8, string→VARCHAR, bytes→VARBYTES, date→TIMESTAMP, bool→BOOL)

[警告] DDL 预览:
CREATE TS DATABASE "mongo_kwdb";
CREATE TABLE "mongo_kwdb"."test_tb" (
    "ts" TIMESTAMPTZ NOT NULL, "c1" INT4, "c2" INT4, "c3" INT8,
    "c4" FLOAT8, "c5" FLOAT8, "c6" BOOL,
    "c7" VARCHAR, "c8" VARCHAR, "c9" VARCHAR, "c10" VARCHAR,
    "c11" VARBYTES, "c12" TIMESTAMP
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
是否执行该 DDL? (yes/no)

用户: yes

[OK] DDL 执行成功

[信息] 构建迁移脚本: collectionName=test_tb + column JSON + query={"t1":{"$gte":1,"$lt":8}}
[OK] 迁移启动: MONGODB2KAIWUDB_xxx.json

[报告] 迁移完成: SUCCEEDED
[提示] 因 query 过滤,目标仅包含 t1=1~7 的文档;请比对验证
````

---

## 场景 13: SQL Server 到 KaiwuDB (TIMESERIES) - schemaName 修正 + t1 主标签

### 用户请求

```
将 SQL Server 的 sqlserver_kwdb 库迁移到 KaiwuDB 时序库（库名 sqlserver_kwdb）。
连接: sa/Password@2024 @ 127.0.0.1:1433 (URL 带 encrypt=true;trustServerCertificate=true)
增加 1 as t1 为主标签
```

### 预期的 AI Agent 回复

````
[信息] 识别迁移意图: SQL Server -> KaiwuDB (TIMESERIES), 库名 sqlserver_kwdb
[信息] SQL Server 说明: URL 需带 encrypt=true;trustServerCertificate=true;两步迁移

[OK] 连接测试通过 (SQL Server + KaiwuDB)

[信息] 元数据读取成功: 表 test_tb, 13 列
[信息] schemaName 修正: 元数据 schemaName=sqlserver_kwdb(库名) → public
      (避免 DDL 出现 "db"."db"."table" 重复)

[信息] 新增 t1 主标签列 (1 as t1 表达式):
  build_added_column('t1', 1, source_type='SQLSERVER', is_tag=True, is_primary_tag=True)
  → INT4, 自动 NOT NULL

[警告] DDL 预览:
CREATE TS DATABASE "sqlserver_kwdb";
CREATE TABLE "sqlserver_kwdb"."public"."test_tb" (
    "ts" TIMESTAMPTZ NOT NULL, "c1" INT2, "c2" INT4, "c3" INT8,
    "c4" FLOAT4, "c5" FLOAT4, "c6" BOOL,
    "c7" CHAR(1), "c8" NCHAR(20), "c9" VARCHAR(10), "c10" NVARCHAR(20),
    "c11" VARBYTES, "c12" TIMESTAMPTZ
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
是否执行该 DDL? (yes/no)

用户: yes

[OK] DDL 执行成功

[信息] 构建迁移脚本: 源列 ts,c1,...,c12,1 as t1; 目标列 ts,c1,...,c12,t1 (target_columns)
[OK] 迁移启动: SQLSERVER2KAIWUDB_xxx.json

[报告] 迁移完成: SUCCEEDED
[提示] 请对比源/目标行数并抽查 t1 默认值
````

---

## 标签说明

| 标签     | 含义             |
|--------|----------------|
| [OK]   | 操作成功完成         |
| [信息]   | 提供信息或进度更新      |
| [警告]   | 需要用户注意或有潜在风险   |
| [错误]   | 发生错误需要处理       |
| [提示]   | 提供建议或最佳实践      |
| [重要]   | 关键安全或配置信息      |
| [报告]   | 迁移结果或统计报告      |
| [替代方案] | 当首选方案不可用时的备选方案 |

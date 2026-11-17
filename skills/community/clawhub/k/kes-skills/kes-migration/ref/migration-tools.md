# KDTS 工具操作详解 + KFS 持续同步

## KDTS 工具概述

KDTS（Kingbase Data Transfer Service）是 KingbaseES 提供的数据迁移工具，支持同构或异构数据库之间的数据迁移。

### 核心优势

- 支持灵活配置迁移任务，满足不同迁移场景
- 以任务为驱动，基于多线程异步处理机制
- 单机多线程迁移效率优于市面其他迁移工具
- 完善的容错和重试机制，支持二次迁移
- 直观的可视化表格或图表类迁移报告

### 访问方式

| 方式 | 目录位置 | 说明 |
|-----|---------|------|
| Web | `{KES_HOME}/ClientTools/guitools/KDts/KDTS-WEB` | 浏览器访问，可视化操作 |
| SHELL | `{KES_HOME}/ClientTools/guitools/KDts/KDTS-CLI` | 命令行配置，脚本启动 |

## KDTS Web 模式详细操作

### 部署启停

**前置条件**：
- JDK 11 及以上，根据 CPU 架构选择匹配版本
- 磁盘空间 500MB 以上
- JVM 内存自动按可用内存 2/3 分配，可通过 `JAVA_MEMORY` 手动调整

**默认登录信息**：
- HTTP：`http://localhost:54523/`
- HTTPS：`https://localhost:54524/`
- 用户名：`kingbase`
- 密码：`Kb_DI@2019`
- 会话保存时间：1 天

### 功能模块

| 模块 | 描述 |
|-----|------|
| 概览 | 主页，显示迁移任务统计、硬件及虚拟机信息 |
| 数据源管理 | 配置源/目标数据库连接信息 |
| 迁移任务管理 | 创建/修改迁移任务，查看状态（未启动/处理中/完成/失败） |
| 迁移结果 | 查看所有任务状态及结果详细信息 |
| 迁移日志 | 查看系统日志、ERROR 日志、INFO 日志（仅管理员） |
| 用户管理 | 管理用户信息（仅管理员） |
| 个人信息 | 查看和修改当前用户信息、修改密码 |

### 迁移任务创建（四步向导）

#### 第一步：选择数据源

选择或新建源数据库和目标数据库连接。源端连接参数：

- 连接名称、数据库类型、数据库版本
- 服务器地址、端口、用户名、密码、数据库
- 驱动、URL（自动根据地址/端口/数据库生成）
- 连接参数（可自行添加/删除）

Oracle 源端需选择 SID 或 ServiceName；KingbaseES 源端需选择 JDBC 或 UnixDomainSocket。

#### 第二步：选择模式

选择需迁移的模式，可勾选包含的对象种类（表、视图、序列、函数、存储过程、程序包、同义词）。可配置迁移前后的 `search_path`。

#### 第三步：选择迁移对象

- 迁移对象设置：全部表 / 包含指定表 / 排除指定表
- 字段类型过滤 / 字段名称过滤
- 表优先迁移设置
- 属主映射 / 表空间映射 / 表名称映射 / 字段名称映射

#### 第四步：配置参数

- **迁移配置**：表处理方式（建表/重建表、导入数据）、排序依据、读写规则、大表拆分阈值
- **数据类型映射**：源端类型 → 目标端类型映射，支持自定义
- **线程配置**：推荐配置或自定义

### 任务状态流转

| 状态 | 支持操作 |
|-----|---------|
| 未启动 | 启动、编辑、删除 |
| 处理中 | 停止、查看进度 |
| 迁移完成 | 重启、查看详情、编辑、删除 |
| 迁移失败 | 重启、查看详情、编辑、删除、**二次迁移** |

## KDTS SHELL 模式详细操作

### 目录结构

```
KDTS-CLI/
├── bin/            # 启动脚本（startup.sh/startup.bat, shutdown.sh/shutdown.bat）
├── conf/           # 配置文件
│   ├── kdts-plus/
│   │   ├── application.yml       # 主配置，active 项选择源库类型
│   │   ├── datasource-xxx.yml    # 对应源库的连接配置
│   │   └── kb-thread-config.xml  # 线程池配置
│   └── mapping_rule/             # 映射规则
│       ├── column/               # 自定义表字段映射
│       ├── db/                   # 自定义数据库映射
│       ├── data_type/            # 自定义数据类型映射
│       ├── default_value/        # 自定义字段缺省值映射
│       ├── syntax/               # 语法映射规则
│       └── table_data/           # 自定义数据映射规则
├── drivers/        # 数据库连接驱动
├── jdk/           # JDK 目录
├── lib/            # 程序包
├── logs/           # 运行日志
├── results/        # 迁移报告
└── version         # 版本查看脚本
```

### 配置流程

#### 1. 激活配置文件

编辑 `kdts-plus/conf/application.yml`：

```yaml
active: oracle    # 根据源库类型设置: oracle/mysql/sqlserver/kingbase 等
```

运行模式配置：

```yaml
# running-mode: DataCompare   # 注释掉为缺省的数据迁移模式
```

#### 2. 配置源数据库连接

编辑对应 `datasource-xxx.yml` 的 `source:` 部分：

```yaml
dbType: oracle
dbVersion: 11g
url: jdbc:oracle:thin:@1.2.3.4:1521/orcl
driver-class-name: oracle.jdbc.OracleDriver
username: oracle
password: 123456
validationQuery: select 1 from dual

# 模式配置
schemas: Schema1
schemaExcludes: SYS,SYSTEM,MGMT_VIEW

# 大表拆分
large-table-split-threshold-rows: 5000000
large-table-split-threshold-size: 5000
large-table-split-max-chunk-num: 24

# 网络读取超时（秒，0 表示永不超时）
net-read-timeout: 0
fetch-size: 1000
table-with-large-object-fetch-size: 100
table-with-big-large-object-fetch-size: 50

# 迁移对象类别控制
migrate-sequence: true
migrate-table-structure: true
migrate-table-data: true
migrate-table-primary-key: true
migrate-table-index: true
migrate-view: false
migrate-function: false
migrate-procedure: false
```

#### 3. 配置目标数据库连接

```yaml
dbType: KINGBASE
dbVersion: V9
url: jdbc:kingbase8://1.2.3.4:54321/test1
driver-class-name: com.kingbase8.Driver
username: kingbase
password: 123456
schemas: "*"
validation-query: select 1

# 目标端配置
write-batch-size: 1000
write-batch-byte-size: 100
drop-existing-object: true
truncate-table: false
rename-object: true
create-target-schema: true
remove-null-character: false

# 无日志表迁移（提升写入效率）
# url 中添加 ApplicationName=kingbase_transfer
unlogged-table: true
relogged-table: true
issue-checkpoint: true
```

#### 4. 线程池配置

编辑 `kb-thread-config.xml`，IO 密集型线程数公式：

```
线程数 = CPU核心数 / (1 - 阻塞系数)
```

示例：
- 双核 CPU：2 / (1 - 0.9) = 20
- 64 核 2 路 CPU：64 × 2 / (1 - 0.9) = 1280

大对象数据特别注意，需满足：

```
(table-with-large-object-fetch-size + large-table-split-max-chunk-num
 + writeLargeObject.maxPoolSize + writeLargeObject.workQueueSize)
 × 每行大数据大小 <= Java虚拟机内存 × 0.9
```

#### 5. 启动迁移

```bash
cd KDTS-CLI/bin
./startup.sh    # Linux
startup.bat     # Windows
```

查看运行日志：`tail -f logs/kdts-app-console_yyyy-mm-dd_hh-mm-ss.log`

#### 6. 查看结果

**日志**：`kdts-plus/logs/` 目录下按迁移日期/时间创建日志目录

```
Schema1/         # 模式 1 的日志（error.log, info.log, warn.log）
error.log        # 错误日志
info.log         # 信息日志
warn.log         # 警告日志
```

**迁移报告**：`kdts-plus/results/` 目录下

```
index.html                      # 报告主页
detail_table.html               # 表详细信息
detail_table_data.html          # 表数据详细信息
detail_function.html            # 函数详细信息
FailedScript/                   # 失败脚本目录
IgnoredScript/                  # 略过脚本目录
SuccessScript/                  # 成功脚本目录
```

## KFS 持续同步

### 使用场景

在线迁移中，KDTS 完成历史数据搬迁后，使用 KFS（Kingbase FlySync）进行持续数据同步，实现业务不停机迁移。

### 操作流程

#### 1. 源端创建一致性状态

```bash
# 连接数据库
ksql -d "host=10.10.3.3 user=SYSTEM password=123456 replication=database dbname=test port=54321"

# 创建复制槽
CREATE_REPLICATION_SLOT slot_name LOGICAL decoderbufs;
```

注意：`decoderbufs.so` 文件权限需为 664

#### 2. KDTS 完成存量数据迁移

在创建复制槽之后，使用 KDTS 进行存量数据搬迁。

#### 3. 启动 KFS 追平

**源端操作**：

```bash
# 先启动到 offline 状态
replicator start offline

# 使用 ONLINE 命令指定 SCN 启动
fsrepctl -service source_db online -from-event ora:200725471:200725471
```

**目标端操作**：

启动 KFS 目标端，等待数据追平。

#### 4. 判断追平完成

```bash
fsrepctl services
# 查看 appliedLastSeqno（源端无新数据时应与源端相同）
# 查看 appliedLatency（源端无新数据时应接近 0）
```

### KFS 重置

若 KFS 之前已经部署运行，需先重置：

```bash
fsrepctl -service XXX reset -all -y
```

## 数据对比

KDTS 支持数据对比模式，用于验证迁移前后数据一致性。

在 `application.yml` 中设置：

```yaml
running-mode: DataCompare
```

源端配置：

```yaml
data-compare-buffer-size: 50000
data-compare-algorithm: MD5    # CRC32/MD5/SHA1/SHA256/SHA384/SHA512
```

目标端配置：

```yaml
data-compare-buffer-size: 200000
data-compare-query-parallelism: 5
```

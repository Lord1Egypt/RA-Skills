# 迁移最佳实践

## KingbaseES V8R3 → V9 迁移最佳实践

### 兼容性概览

V9 内部实现了大量兼容 V8R3 的特性，实际迁移中一般只需很少甚至不做任何修改。

#### 兼容特性开关差异

| 兼容特性开关 | V9 | V8R3 | 用途 |
|-------------|-----|------|------|
| `char_default_type` | 不支持 | 支持 | 字符串类型长度单位 |
| `default_with_oids` | 支持 | 支持 | 新建表包含 OID 伪列 |
| `ora_input_emptystr_isnull` | 支持 | 支持 | 空串当 NULL 处理 |
| `ora_date_style` | 支持（需先开 `ora_style_nls_date_format`） | 支持 | date 输出格式兼容 Oracle |
| `ora_format_style` | 不支持 | 支持 | 格式化输出兼容 Oracle |
| `nls_length_semantics` | 支持 | 不支持 | 字符串长度单位 |

#### 关键差异

- **大小写敏感**：V8R3 用 `case_sensitive`，V9 用 `enable_ci`
- **search_path**：V9 中模式名需写成小写（`"$user", public`）
- **全局临时表**：V8R3 不支持，V9 支持
- **序列查询**：`select * from seq_name` 在 V8R3 返回 10 列，V9 仅 4 列（完整信息查 `all_sequences`）
- **分区**：V9 支持分区 alter、全局索引、interval 分区
- **数据类型**：V9 不支持 `bool→text` 隐式转换、不支持 `time→timestamp` 隐式转换、不支持 `reltime`/`tinterval`
- **操作符**：V9 完善了自定义操作符处理，`%-` 在 V8R3 中会被拆分为 `%` 和 `-`，V9 中作为整体
- **`get_byte(bit, int)`**：V9 不支持此函数签名
- **`sys_guid()`**：V9 默认输出 name 类型，可通过 `guid_default_return_type='bytea'` 改为 bytea

#### PL/SQL 差异

- **嵌套表 CHAR 省略长度**：V8R3 赋值超长会截断，V9 会报错
- **CREATE PACKAGE**：V9 语法解析更严格，变量声明后需加分号

### 迁移步骤

1. **评估兼容性**：明确 V9 对 V8R3 的兼容度
2. **创建同名数据库/用户/模式**：在 V9 上创建与 V8R3 同名的数据库、用户和模式
3. **KDTS 迁移**：使用 KDTS 完成数据搬迁
4. **验证差异**：检查 search_path、序列查询、数据类型等差异点
5. **初始化参数**：`initdb` 时可添加 `-m sqlserver` 等参数选择兼容模式

### 客户端编程接口兼容性

JDBC、ODBC、Hibernate、MyBatis、OCI、.NET NDP/EF、PHP PDO、Perl DBI、Node.js、Golang、Python、QT 等接口在 V9 和 V8R3 中基本一致。JDBC 方面，V9 读写分离集群增加 `nodelist` 必填参数。

---

## SQL Server → KingbaseES 迁移最佳实践

### 兼容特性概览

KingbaseES 内部实现了大量兼容 SQL Server 语法和功能的特性：

- **数据类型**：支持几乎所有 SQL Server 特有数据类型（NUMBER、VARCHAR2、CHAR(n)、DATE、INTERVAL、ROWID 等）
- **SQL 语句**：支持层次查询、WITH 子句、JSON 表达式、MERGE、COPY 等
- **客户端工具**：KSQL（对标 SQLCMD）、KStudio（对标 SSMS）

### 迁移流程

#### 1. 迁移评估

使用评估模板记录：

- SQL Server 数据库版本、操作系统版本
- 服务器配置（CPU/内存/磁盘）
- 用户数/天、事务量/天
- 当前数据库大小、增长速率
- 应用方式（OLTP/OLAP）、客户端应用类型
- 客户端连接接口（ODBC/ADO/NDP 等）

#### 2. 迁移准备

**部署目的库**：

- 目的库硬件配置尽量高
- 源库规模 > 1GB，建议分物理机部署
- 尽量同局域网部署

**软件安装**：SQL Server、KingbaseES、JDBC/ODBC 驱动、测试工具

**参数优化**：

- `shared_buffers`：调整为内存的 1/4
- 预先创建适当大小的数据和日志文件
- 初始化数据库时添加 `-m sqlserver` 参数

**创建数据库/用户**：

- 创建与 SQL Server 用户同名的用户（如 sa）
- 创建与 SQL Server 同名的数据库，属主为对应用户
- 创建 dbo 模式
- 配置 `search_path` 为 `$USER,dbo,PUBLIC`

#### 3. 数据迁移

**离线迁移**：使用 KDTS，Web 或 SHELL 模式

**在线迁移**：KDTS 历史数据 + KFS 增量追平

需使用中间数据库（与源端版本相同的单实例）做媒介：

1. 源端获取一致性 SCN 号
2. 备份源端数据库
3. 还原至中间库
4. KDTS 将中间库数据搬迁至 KES 目标库
5. KFS 从指定 SCN 开始追平

#### 4. 应用代码迁移

**服务器端代码**：KDTS 已完成存储过程、函数等过程对象迁移，需关注批处理块代码

**客户端代码**：

- JDBC/ODBC 接口替换
- ADO.NET → Kdbndp
- 连接串修改

#### 5. 测试与调试

- 功能回归测试
- 性能测试（构造与实际生产相同规模的数据）
- 高可用方案测试

### 日期格式处理

SQL Server 时间默认格式为 ISO, MDY，在 KES 配置文件中添加：

```ini
datestyle = 'ISO,YMD'
```

修改为年月日格式。

---

## 通用迁移最佳实践

### 迁移前准备

1. **充分评估**：使用 KDMS 在线评估工具，识别不支持的功能
2. **环境规划**：源/目标库分机部署、同局域网、充足磁盘空间
3. **参数优化**：目标库提前调整 shared_buffers、work_mem 等参数
4. **备份策略**：迁移前务必备份源端数据

### 迁移中注意事项

1. **大对象处理**：调整 `table-with-large-object-fetch-size` 和 JVM 内存
2. **网络稳定性**：设置合适的 `net-read-timeout`，避免网络抖动导致迁移卡住
3. **线程配置**：根据 CPU 核心数合理设置，不是越多越好
4. **迁移顺序**：严格按照 数据库 → 用户 → 模式 → 数据 → 应用的顺序

### 迁移后验证

1. **数据一致性**：使用 KDTS 数据对比功能
2. **功能测试**：全面回归测试所有模块
3. **性能测试**：构造生产规模数据，模拟未来增长
4. **割接准备**：制定回退预案，观察期至少三个业务周期

### 多次迁移策略

开发过程中需定期迁移时：

- 定义未变更的表：只同步数据
- 定义变更的表：迁移定义 + 数据
- 使用 KDTS 的"迁移部分表"和"按条件迁移"功能

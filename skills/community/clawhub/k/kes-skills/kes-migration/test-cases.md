# KingbaseES 数据迁移测试用例

## KDTS Web 模式迁移测试

### TC-001：Oracle → KingbaseES 全量离线迁移

**场景**：将 Oracle 11g 数据库中的指定 schema 完整迁移至 KingbaseES V9

**步骤**：
1. KDTS Web 模式启动，访问 `http://localhost:54523/`
2. 创建源数据库连接：Oracle 11g，填写 IP/端口/用户名/密码
3. 创建目标数据库连接：KingbaseES V9，填写连接信息
4. 新建迁移任务 → 选择数据源 → 选择模式 → 选择全部表
5. 配置参数：迁移表结构+数据+索引+约束
6. 点击"保存并迁移"
7. 查看迁移结果，确认成功数、失败数

**预期**：所有表结构、数据、索引、约束迁移成功，迁移报告中失败数为 0

### TC-002：MySQL → KingbaseES 指定表迁移

**场景**：仅迁移 MySQL 8.0 中指定的 10 张表

**步骤**：
1. 创建 MySQL 源连接和 KES 目标连接
2. 新建迁移任务，选择模式后选择"包含指定表"
3. 输入 10 张表名
4. 执行迁移

**预期**：仅指定的 10 张表被迁移，其他表不受影响

### TC-003：SQL Server → KingbaseES 含大对象迁移

**场景**：迁移包含 BLOB/CLOB 字段的表

**步骤**：
1. 创建 SQL Server 2019 源连接
2. 配置参数：`table-with-large-object-fetch-size` 设为 5
3. 调整 JVM 内存和写大对象线程池
4. 执行迁移

**预期**：大对象数据完整迁移，无内存溢出错误

## KDTS SHELL 模式迁移测试

### TC-004：SHELL 模式 Oracle → KES 迁移

**场景**：使用 SHELL 命令行模式进行 Oracle 迁移

**步骤**：
1. 修改 `application.yml` 中 `active: oracle`
2. 编辑 `datasource-oracle.yml` 配置源/目标连接
3. 设置 `schemas: "SCHEMA1"`
4. 配置 `migrate-table-structure: true`、`migrate-table-data: true`
5. 运行 `bin/startup.sh`
6. 查看 `logs/` 和 `results/` 目录

**预期**：迁移成功，日志无 ERROR，报告中 index.html 显示迁移结果

### TC-005：SHELL 模式排除指定表

**场景**：迁移 schema 中除指定表外的所有表

**步骤**：
1. 配置 `table-excludes: schema1.tbl1,schema1.tbl2`
2. 执行迁移

**预期**：指定表被排除，其他表正常迁移

### TC-006：无日志表迁移（性能优化）

**场景**：大规模数据迁移时使用无日志表提升写入效率

**步骤**：
1. 目标端 URL 添加 `ApplicationName=kingbase_transfer`
2. 配置 `unlogged-table: true`、`relogged-table: true`、`issue-checkpoint: true`
3. 执行迁移

**预期**：迁移速度提升，迁移完成后无日志表改为有日志表

## KES 版本间迁移测试

### TC-007：V8R3 → V9 迁移

**场景**：KingbaseES V8R3 升级至 V9

**步骤**：
1. 在 V9 上创建与 V8R3 同名的数据库、用户和模式
2. 使用 KDTS 创建 V8R3 源连接和 V9 目标连接
3. 执行全量迁移
4. 验证兼容特性：search_path 小写、序列查询方式、全局临时表

**预期**：迁移成功，V9 新增特性（全局临时表、分区等）可正常使用

## 在线迁移测试

### TC-008：KDTS + KFS 在线迁移

**场景**：业务不停机，使用 KDTS 历史数据 + KFS 增量追平

**步骤**：
1. KDTS 完成存量数据迁移
2. 在源端创建复制槽：`CREATE_REPLICATION_SLOT slot_name LOGICAL decoderbufs;`
3. 启动 KFS 源端 offline
4. 使用 ONLINE 命令指定 SCN 开始追平
5. 启动 KFS 目标端
6. 检查 `fsrepctl services` 确认追平完成

**预期**：增量数据追平，`appliedLatency` 接近 0

## 应用适配测试

### TC-009：JDBC 连接切换

**场景**：将应用从 Oracle JDBC 切换至 KES JDBC

**步骤**：
1. 替换驱动类：`com.kingbase8.Driver`
2. 替换连接串：`jdbc:kingbase8://host:54321/dbname`
3. 执行基础 CRUD 操作验证

**预期**：连接成功，CRUD 操作正常

### TC-010：Hibernate 方言切换

**场景**：应用使用 Hibernate，切换至 KES 方言

**步骤**：
1. 配置 `hibernate.dialect=org.hibernate.dialect.Kingbase8Dialect`
2. 选择对应版本方言包
3. 执行实体增删改查

**预期**：ORM 操作正常，SQL 生成正确

## 数据校验测试

### TC-011：迁移后数据一致性验证

**场景**：对比源库和目标库数据量

**步骤**：
1. 源库执行 `SELECT COUNT(*) FROM table_name`
2. 目标库执行相同查询
3. 对比结果

**预期**：各表数据行数完全一致

### TC-012：二次迁移验证

**场景**：首次迁移存在失败对象，使用二次迁移功能

**步骤**：
1. 首次迁移后有部分对象失败
2. 在迁移任务列表中找到失败任务
3. 点击"二次迁移"
4. 查看迁移结果

**预期**：之前失败的对象迁移成功

## 常见问题处理测试

### TC-013：OOM 问题处理

**场景**：迁移大数据量时出现 `java.lang.OutOfMemoryError: Java heap space`

**步骤**：
1. 修改启动脚本中 `JAVA_MEMORY` 参数，增大 JVM 内存
2. 降低 KDTS 线程数和队列长度
3. 清理系统缓存：`sync && echo 3 > /proc/sys/vm/drop_caches`
4. 重新执行迁移

**预期**：迁移不再出现 OOM 错误

### TC-014：全大写字段名处理

**场景**：源端全大写对象名称迁移后变成全小写

**步骤**：
1. 了解 KES 机制：无论是否大小写敏感，全大写对象名会转成全小写
2. 在应用层确认兼容性

**预期**：了解此机制，在应用中做相应适配

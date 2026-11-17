# 迁移常见问题排查及解决方法

## 通用问题

### OOM：java.lang.OutOfMemoryError: Java heap space

**解决方法**：

1. 修改启动脚本（`bin/startup.sh` 或 `startup.bat`）中 `JAVA_MEMORY` 大小
2. 如果内存有限：
   - Linux 环境清理缓存：`sync && echo 3 > /proc/sys/vm/drop_caches`
   - 降低 KDTS 线程数和队列长度（队列长度 > 300 的可调整为 300）

### Windows 下启动迁移工具闪退

**解决方法**：

- 检查 JDK 目录是否正确放置 JDK（对应平台的 JDK 11 版本）
- 使用管理员身份运行
- 将 KDTS 工具放到根目录下，防止目录过深
- 检查端口占用，修改 `conf/application.properties` 中的 `http.port` 和 `server.port`
- 检查是否存在 PID 文件，如有则删除后重启

### 数据迁移报错：文件签名不被认可

**解决方法**：修改 `conf/application.properties` 中"是否使用遗留二进制拷贝签名"为 false（或 true，与原值相反）

### 创建模式报错：syntax error at or near "AUTHORIZATION"

**解决方法**：检查 `kingbase.conf` 中是否将 `authorization` 添加到 `exclude_reserved_words`，如有则移除

### 源端全大写对象名称迁移后变成全小写

**原因**：KES 无论是否大小写敏感，都会将全大写对象名称转换成全小写，此为 KES 机制导致

### GIS 迁移报错：geometry requires more points

**原因**：源端 GIS 数据中标识一条线但只有一个点，为非法数据

**解决方法**：修改源端错误数据，或过滤掉该行的主键

### 修改默认值映射

Web 版本：在 `{安装目录}/conf/mapping_rule/default_value/` 下，根据源端目标端类型选择对应的 JSON 文件配置。

以 bit 类型默认值报错为例：原始表默认值为 0 或 1，迁移到 KES 报错 "类型是 bit, 但默认表达式类型是 integer"。需将默认值 0/1 映射为 '0'/'1'。

### 类型映射错误

当源端类型迁移后类型不正确时，可通过页面直接增加或修改类型映射。未在下拉菜单中找到的类型可直接输入。

---

## Oracle 迁移 KES

### 无效的 GBK 编码字节顺序

**现象**：迁移数据错误，无效的 GBK 编码字节顺序: 0xb4（源库和目标库编码都为 GBK）

**解决方法**：删除目标数据源连接参数 `clientEncoding: utf8`

### 目标端报 raw 类型不支持

**解决方法**：在 KES 目标端安装 raw 数据类型插件（KES 默认不支持 raw 类型）

### 自定义类型数据不支持 copy 方式写入

自定义类型数据仅支持 insert 写入

### Oracle 迁移卡住

**原因**：网络导致 Oracle 连接断开，查询卡死（在获取表数据总行数时等待）

**分析方法**：

1. 任务长时间只有打点和线程状态日志
2. 导出 jstack 日志：`jstack -l [pid] > xxx.log`
3. 发现正在等待获取表数据总行数
4. 检查源端数据库连接是否存在

**解决方法**：在 Oracle 连接参数中增加 `oracle.jdbc.ReadTimeout=180000`（毫秒），需大于查询数据返回时间

### GIS 数据迁移报错：没有 APPEND_SRID 函数

**原因**：迁移 GIS 数据时需将 srid 与数据合并，需要在源端创建函数

**解决方法**：在源端 Oracle 数据库中创建以下函数并赋权：

```sql
CREATE OR REPLACE FUNCTION append_srid(srid IN INTEGER, kwb IN BLOB) RETURN BLOB AS
    re BLOB;
BEGIN
    IF kwb IS NULL THEN
        RETURN NULL;
    END IF;
    re := TO_BLOB(UTL_RAW.CAST_FROM_BINARY_INTEGER(srid, UTL_RAW.LITTLE_ENDIAN));
    DBMS_LOB.APPEND(re, kwb);
    RETURN re;
END;

GRANT EXECUTE ON my_schema.append_srid TO john_doe;
```

### ArcGIS 数据迁移报错

**原因**：ArcGIS 已卸载，迁移时调用 ArcGIS 函数失败

**解决方法**：安装 ArcGIS 后再迁移，或使用 ArcGIS 自带的迁移工具

---

## MySQL 迁移 KES

### no unpinned buffers available

**解决方法**：查看 KES 共享缓存区大小（`show shared_buffers`），调整为系统内存的 25%

### Communications link failure

**解决方法**：

1. 增加 `socketTimeout` 连接参数（毫秒）
2. 查询 MySQL 配置中 `max_allowed_packet` 值，适当加大
3. 减小源库游标读取记录数

### Statement cancelled due to timeout or client request

**解决方法**：设置迁移参数连接超时时间值为 0

### 无法获取表结构

**解决方法**：检查源数据库连接中数据库名称是否有多余空格

### Table read failed: Unknown column datetime_precision in field list

**解决方法**：选择 MySQL 版本号为 5.5

### 语法错误在 "COLLATE" 或附近

**解决方法**：目标端配置项 `useCollate` 参数设置为 false

### 无效的 "UTF8" 编码字节顺序: 0x00

**解决方法**：目标端配置项 `removeNullCharacter` 参数设置为 true

### 时间类型迁移数据违反非空约束

**原因**：源端时间类型存在 `0000-00-00 00:00:00` 且列为非空，KES 不支持此类数据存储

**解决方法**：将 MySQL 连接参数中 `zeroDateTimeBehavior=convertToNull` 修改为 `zeroDateTimeBehavior=round`，迁移后数据变为 `0001-01-01 00:00:00`

### 视图迁移没有定义

**原因**：权限不足，无 SHOW VIEW 权限

**解决方法**：

1. 使用管理员用户迁移
2. 或赋予权限：`GRANT SHOW VIEW ON 库.对象名 TO '用户名'@'登录位置'`

---

## KES 迁移 KES

### V7 迁移报错：非法 BigDecimal 值

**解决方法**：更新 V7 JDBC 驱动文件为数据库对应的 JDBC 驱动（数据库安装目录下），迁移工具驱动目录为 `drivers/kingbase/v7`

---

## DM 迁移 KES

### 无法获取表结构

**解决方法**：检查 DM 数据库连接账号是否为 sysdba，应用账号可能权限不足

---

## Db2 迁移 KES

### SQLCODE=-668, SQLSTATE=57016

**原因**：表处于"装入暂挂"状态

**解决方法**：执行 `DB2 reorg table TABLE_NAME`，提示 successful 后表示重组成功

### java.io.CharConversionException, ERRORCODE=-4220

**解决方法**：在启动脚本中添加参数 `-Ddb2.jcc.charsetDecoderEncoder=3`

### interval 时间类型数据搬迁后值变为 0

**解决方法**：目标端 KES 版本为 V8R6C7 以上时，数据库连接管理中选择 V8R6C7 版本

---

## OceanBase 迁移 KES

### time 类型范围超出 00:00:00 ~ 24:00:00 迁移失败

- KES Oracle 兼容模式：放不下此类数据，会迁移失败
- KES MySQL 兼容模式：使用 insert 方式写入

---

## SQL Server 迁移 KES

### datetime 类型 9999-12-31 23:59:59:998 变为 10000-01-01 00:00:00

这是数据库自身的行为，与 KDTS 无关

### sql_variant 类型

不支持 copy 方式写入，仅支持 insert 写入

---

## KES 迁移 MySQL

### GIS 数据类型查询乱码

**解决方法**：使用 `SELECT ST_AsText()` 查询，而非 `SELECT *`

---

## SQLite 迁移 KES

### 迁移任务失败

**解决方法**：将搬迁配置文件中的 `readonly` 配置设置为 false

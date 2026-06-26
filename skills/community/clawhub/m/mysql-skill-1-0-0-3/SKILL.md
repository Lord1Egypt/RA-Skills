---
name: mysql-skill
description: MySQL 数据库管理技能。通过自然语言查询、管理 MySQL 数据库，支持 SELECT/INSERT/UPDATE/DELETE、表管理、备份恢复等操作。当用户提到 MySQL、数据库查询、建表、数据备份时使用此技能。
---

# MySQL Skill - 对话式数据库管理

通过自然语言，轻松管理 MySQL 数据库，无需手写 SQL！

---

## 🎯 功能特点

### 核心能力
- **🔍 智能查询** - 用自然语言描述需求，自动生成 SQL
- **📊 数据分析** - 快速统计、聚合、分组查询
- **🛠️ 表管理** - 建表、修改表结构、索引管理
- **💾 备份恢复** - 数据库/表级备份和恢复
- **🔧 优化建议** - 慢查询分析、索引优化建议

---

## 📋 使用场景

### 查询场景
- "查询昨天注册的用户"
- "统计每个部门的员工数量"
- "找出销售额前十的产品"
- "查询最近一周的订单，按时间倒序"

### 数据操作
- "给用户表中添加一个 phone 字段"
- "把所有状态为 pending 的订单改为 confirmed"
- "删除三个月前的日志记录"

### 备份场景
- "备份数据库"
- "恢复昨天下午的备份"
- "导出用户表的数据"

---

## 🔧 前置条件

### 1. 安装 MySQL 客户端

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-client
```

**macOS:**
```bash
brew install mysql-client
```

**Windows:**
下载并安装 MySQL 官方客户端工具

### 2. 配置数据库连接

创建配置文件 `~/.my.cnf`:
```ini
[client]
host = localhost
user = your_username
password = your_password
database = your_database
```

或通过环境变量：
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=your_username
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=your_database
```

---

## 💻 常用操作

### 查询数据

**自然语言描述：**
```
查询销量最高的 5 个产品
```

**AI 生成的 SQL：**
```sql
SELECT product_name, SUM(quantity) as total_sales
FROM orders
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;
```

---

### 创建表

**自然语言描述：**
```
创建一个用户表，包含 id、用户名、邮箱、注册时间
```

**AI 生成的 SQL：**
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);
```

---

### 数据备份

**备份数据库：**
```bash
mysqldump --single-transaction --quick --lock-tables=false \
    your_database > backup_$(date +%Y%m%d_%H%M%S).sql
```

**备份单个表：**
```bash
mysqldump your_database table_name > table_backup.sql
```

**恢复数据：**
```bash
mysql your_database < backup_file.sql
```

---

## 🔍 高级功能

### 慢查询分析

1. **开启慢查询日志：**
```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
```

2. **分析慢查询：**
```bash
mysqldumpslow /var/log/mysql/slow.log
```

### 索引优化建议

查看表的索引使用情况：
```sql
SELECT 
    TABLE_NAME, INDEX_NAME, CARDINALITY
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'your_database'
ORDER BY TABLE_NAME, INDEX_NAME;
```

### 数据库性能检查

查看数据库状态：
```sql
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Questions';
SHOW STATUS LIKE 'Uptime';
```

---

## ⚠️ 注意事项

### 安全建议
1. **使用环境变量存储密码**，不要在命令行中明文显示
2. **最小权限原则** - 使用只读用户进行查询操作
3. **生产环境谨慎操作** - 写操作前先备份数据
4. `**LIMIT 子句** - 大数据量查询一定要加 LIMIT

### 性能优化
1. 为常用查询字段添加索引
2. 避免 `SELECT *`，只查询需要的字段
3. 大量数据操作使用事务
4. 定期清理过期数据

---

## 🎓 示例对话

### 示例 1：查询分析
**用户：** "帮我看看这个月的销售额分布"

**AI：** "好的，我来查询这个月每天的销售额。"
```sql
SELECT 
    DATE(order_date) as date,
    SUM(amount) as daily_sales
FROM orders
WHERE order_date >= DATE_FORMAT(NOW(), '%Y-%m-01')
GROUP BY DATE(order_date)
ORDER BY date;
```

### 示例 2：表结构修改
**用户：** "给订单表加一个优惠券字段"

**AI：** "好的，正在添加字段..."
```sql
ALTER TABLE orders
ADD COLUMN coupon_code VARCHAR(50) NULL
AFTER discount_amount;
```

### 示例 3：数据备份
**用户：** "备份一下数据库"

**AI：** "正在备份数据库到 backup_20260323.sql..."
```bash
mysqldump --single-transaction --quick your_database > backup_20260323.sql
```

---

## 🛠️ 故障排查

### 常见错误

**1. ERROR 1045 (28000): Access denied**
- 检查用户名和密码
- 确认用户有权限访问该数据库

**2. ERROR 2002 (HY000): Can't connect to MySQL server**
- 检查 MySQL 服务是否运行
- 确认主机名和端口配置正确

**3. Query took too long**
- 检查是否添加了合适的索引
- 使用 `EXPLAIN` 分析查询计划
- 考虑添加 LIMIT 限制结果数量

---

## 📚 参考资料

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [MySQL 性能优化指南](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)

---

**开始使用：** 直接告诉我你想查询什么，我会自动生成 SQL！🚀

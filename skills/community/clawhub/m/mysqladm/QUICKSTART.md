# MySQL ADM Skill 快速开始

## 5 分钟快速测试

### 1. 启动测试数据库（30 秒）

```bash
# 启动本地 MySQL 服务
sudo systemctl start mysql

# 创建测试数据库
mysql -uroot -p << EOF
CREATE DATABASE IF NOT EXISTS testdb;
EOF
```

### 2. 验证连接（10 秒）

```bash
# 测试连接
mysql -uroot -p -e "SELECT VERSION();"
```

### 3. 运行结构测试（30 秒）

```bash
/home/clawbot/openclaw/test_mysqladm_skill.sh
```

### 4. 运行功能测试（2 分钟）

```bash
# 设置环境变量（请根据实际情况修改密码）
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_USER="root"
export MYSQL_PASSWORD="123456"
export MYSQL_DATABASE="testdb"

# 创建测试表并插入数据
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE << EOF
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com');
EOF

# 测试查询
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SELECT * FROM users;"
```

### 5. 测试备份（1 分钟）

```bash
# 备份
mkdir -p /tmp/mysql_backup
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > /tmp/mysql_backup/backup.sql

# 验证备份
ls -lh /tmp/mysql_backup/backup.sql
head -20 /tmp/mysql_backup/backup.sql
```

### 6. 清理（10 秒）

```bash
# 删除测试数据库
mysql -uroot -p << EOF
DROP DATABASE IF EXISTS testdb;
EOF

# 删除备份文件
rm -rf /tmp/mysql_backup
```

## 完成！

✓ 技能结构测试通过
✓ 基本功能测试通过
✓ 可以开始使用或集成到 OpenClaw

## 下一步

- 查看 `test_mysqladm_functional.md` 进行完整功能测试
- 在 OpenClaw 中测试技能集成
- 根据需要调整技能功能
- 通过 clawhub 发布分享技能

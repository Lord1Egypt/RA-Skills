---
name: kes-perl
name_for_command: kes-perl
description: 指导用户完成Perl连接KingbaseES数据库。当用户提到Perl开发、DBD::KB驱动、Perl DBI连接金仓、Perl数据库操作时，必须使用此技能。
---

# KingbaseES Perl 连接指南

本技能指导用户完成 Perl 连接 KingbaseES 的完整流程，涵盖 DBD::KB 驱动安装、DBI 标准接口、事务控制和批量操作。

## 连接数据库

### 类方法连接

```perl
use DBI;

my $dbh = DBI->connect(
    'DBI:KB:dbname=TEST;host=127.0.0.1;port=54321',
    'SYSTEM',
    '123456',
    {
        AutoCommit => 1,
        RaiseError => 0,
        PrintError => 1,
        ReadOnly   => 0,
    }
);
```

### 连接参数

| 参数 | 说明 |
|------|------|
| dbname | 数据库名 |
| host | 数据库服务器地址 |
| port | 端口号，默认 54321 |

### 其他类方法

```perl
# 缓存连接
my $dbh = DBI->connect_cached($dsn, $user, $pass, \%attr);

# 获取可用数据源
my @sources = DBI->data_sources('KB');
```

## 执行 SQL

```perl
# 一步完成：准备、执行、获取结果
$dbh->do('CREATE TABLE test (id int PRIMARY KEY, name varchar(100), salary real)');

# 使用占位符写入
my $stmt = $dbh->prepare('INSERT INTO test (id, name, salary) VALUES (?, ?, ?)');
$stmt->execute(1, 'Alice', 50000);
$stmt->execute(2, 'Bob', 60000);
$stmt->finish();

# 查询数据
my $results = $dbh->selectall_arrayref(
    'SELECT * FROM test WHERE salary > ? ORDER BY id',
    { ArrayTupleStatus => 1 },
    55000,
);

for my $row (@$results) {
    print "ID: $row->[0], Name: $row->[1], Salary: $row->[2]\n";
}
```

## 事务控制

```perl
$dbh->{AutoCommit} = 0;
eval {
    $dbh->do('UPDATE test SET salary = salary * 1.1 WHERE id = 2');
    $dbh->commit();
};
if ($@) {
    $dbh->rollback();
    warn "Transaction failed: $@";
}
$dbh->{AutoCommit} = 1;
```

## Schema 查询

```perl
# 获取表列表
my $tables = $dbh->tables();
while (my @table_info = $tables->fetchrow_array()) {
    print "Table: $table_info[2]\n";
}

# 查询表信息
$dbh->table_info(cat, schema, table, type);

# 查询列信息
$dbh->column_info(cat, schema, table, column);

# 查询主键
$dbh->primary_key_info(cat, schema, table);

# 查询外键
$dbh->foreign_key_info();

# 查询统计信息
$dbh->statistics_info();

# 数据类型信息
$dbh->type_info();
```

## 数据库句柄属性

| 属性 | 说明 |
|------|------|
| AutoCommit | 自动提交模式，默认 1 |
| ReadOnly | 只读模式 |
| Name | 数据库名 |
| Username | 用户名 |
| Driver | 驱动对象 |

## 错误处理

```perl
my $err    = $dbh->err;     # 错误码
my $errstr = $dbh->errstr;  # 错误信息
my $state  = $dbh->state;   # SQLSTATE 码

# 追踪
$dbh->trace(level);
$dbh->trace_msg(message);

# 私有属性信息
my @info = $dbh->private_attribute_info();
```

## 连接管理

```perl
# 测试连接是否存活
$dbh->ping();

# 克隆连接
my $clone = $dbh->clone(\%attr);

# 断开连接
$dbh->disconnect();
```

## 完整示例

```perl
use DBI;

# 连接
my $dbh = DBI->connect(
    'DBI:KB:dbname=TEST;host=127.0.0.1;port=54321',
    'SYSTEM',
    '123456',
    { AutoCommit => 1, RaiseError => 0, PrintError => 1 },
);

# 创建表
$dbh->do('CREATE TABLE test (id int PRIMARY KEY, name varchar(100), salary real)');

# 写入数据
my $stmt = $dbh->prepare('INSERT INTO test (id, name, salary) VALUES (?, ?, ?)');
$stmt->execute(1, 'Alice', 50000);
$stmt->execute(2, 'Bob', 60000);
$stmt->finish();

# 查询
my $results = $dbh->selectall_arrayref(
    'SELECT * FROM test WHERE salary > ? ORDER BY id',
    { ArrayTupleStatus => 1 },
    55000,
);

for my $row (@$results) {
    print "ID: $row->[0], Name: $row->[1], Salary: $row->[2]\n";
}

# 清理
$dbh->do('DROP TABLE test');
$dbh->disconnect();
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `DBD::KB not found` | 驱动未安装 | 从 `$KINGBASE_HOME/Interface/` 安装 DBD::KB |
| `连接被拒绝` | 端口/地址错误 | 检查端口（默认 54321）和 `sys_hba.conf` |

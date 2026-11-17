---
name: kes-php
name_for_command: kes-php
description: 指导用户完成PHP连接KingbaseES数据库。当用户提到PHP开发、pdo_kdb驱动、PHP PDO连接金仓、kdbCopy批量导入导出、kdbLOB大对象时，必须使用此技能。
---

# KingbaseES PHP 连接指南

本技能指导用户完成 PHP 连接 KingbaseES 的完整流程，涵盖 pdo_kdb 驱动安装配置、kdbCopy 批量操作和 kdbLOB 大对象。

## 版本支持

| PHP 版本 | x86_64 | aarch64 | Windows | Mips | LoongArch | SW64 |
|---------|--------|---------|---------|------|-----------|------|
| 5.6 | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| 7.2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7.3 | ✅ | ✅ | ✅ | - | - | - |
| 7.4 | ✅ | ✅ | ✅ | - | - | - |
| 8.0 | ✅ | ✅ | ✅ | - | - | - |
| 8.1 | ✅ | ✅ | ✅ | - | - | - |
| 8.2 | ✅ | ✅ | ✅ | - | - | - |
| 8.3 | ✅ | ✅ | ✅ | - | - | - |
| 8.4 | ✅ | ✅ | ✅ | - | - | - |

> PHP 线程安全版本请选择对应的 NTS（非线程安全）或 TS（线程安全）驱动包。

## 配置

### Linux 环境

修改 `php.ini`：

```ini
extension_dir = "/path/to/php/extensions"
extension = pdo_kdb.so
```

### Windows 环境

```ini
extension_dir = "C:/php/ext"
extension = php_pdo_kdb.dll
```

## 连接数据库

DSN 格式：`kdb:host=<主机>;dbname=<数据库>;port=<端口>`

```php
$dsn = 'kdb:host=127.0.0.1;dbname=TEST;port=54321';
$user = 'SYSTEM';
$password = '123456';

$pdo = new PDO($dsn, $user, $password);
```

## kdbCopy 批量操作

### 从数组导入

```php
$rows = $pdo->kdbCopyFromArray(
    'table_name',
    ['column1', 'column2'],
    [
        ['value1', 'value2'],
        ['value3', 'value4'],
    ],
);
```

### 导出到文件

```php
$rows = $pdo->kdbCopyToFile(
    'table_name',
    ['column1', 'column2'],
    '/path/to/output.txt',
);
```

### 从文件导入

```php
$rows = $pdo->kdbCopyFromFile(
    'table_name',
    ['column1', 'column2'],
    '/path/to/input.txt',
);
```

### 导出到数组

```php
$data = $pdo->kdbCopyToArray('table_name', ['column1', 'column2']);
```

## kdbLOB 大对象操作

```php
// 创建大对象
$loid = $pdo->kdbLOBCreate();

// 打开大对象（mode: 'r' / 'w' / 'rb' / 'wb'）
$handle = $pdo->kdbLOBOpen($loid, 'wb');

// 写入数据
$pdo->kdbLOBWrite($handle, 'data content');

// 读取数据
$data = $pdo->kdbLOBRead($handle, length);

// 关闭大对象
$pdo->kdbLOBClose($handle);

// 删除大对象
$pdo->kdbLOBUnlink($loid);
```

## 完整示例

```php
$dsn = 'kdb:host=127.0.0.1;dbname=TEST;port=54321';
$pdo = new PDO($dsn, 'SYSTEM', '123456');

// 创建表
$pdo->exec('CREATE TABLE test (id int, name varchar(100), data bytea)');

// 写入数据
$stmt = $pdo->prepare('INSERT INTO test VALUES (:id, :name, :data)');
$stmt->bindValue(':id', 1);
$stmt->bindValue(':name', 'test');

// 使用 LOB 操作大字段
$loid = $pdo->kdbLOBCreate();
$handle = $pdo->kdbLOBOpen($loid, 'wb');
$pdo->kdbLOBWrite($handle, 'large object data');
$stmt->bindValue(':data', $loid, PDO::PARAM_LOB);
$stmt->execute();
$pdo->kdbLOBClose($handle);

// 读取 LOB 数据
$row = $pdo->query('SELECT * FROM test WHERE id = 1')->fetch(PDO::FETCH_OBJ);
$handle = $pdo->kdbLOBOpen($row->data, 'rb');
$data = $pdo->kdbLOBRead($handle, 8192);
$pdo->kdbLOBClose($handle);

// 清理
$pdo->kdbLOBUnlink($row->data);
$pdo->exec('DROP TABLE test');
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `pdo_kdb.so not found` | 扩展未安装 | 从 `$KINGBASE_HOME/Interface/` 复制驱动到 php extension_dir |
| `DSN 错误` | 驱动标识符错误 | DSN 前缀必须是 `kdb:` |

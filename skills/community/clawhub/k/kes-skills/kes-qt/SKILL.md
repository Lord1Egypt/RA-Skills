---
name: kes-qt
name_for_command: kes-qt
description: KingbaseES Qt SQL 驱动指南。当用户提到 Qt、qkingbase、QSqlDatabase、桌面 GUI、Qt SQL 驱动金仓时，必须使用此技能。
---

# KingbaseES Qt 驱动指南

本技能指导用户完成 KingbaseES Qt SQL 驱动的配置和使用，适用于桌面 GUI 应用开发。

## 兼容性矩阵

| Qt 版本 | 平台 | 支持 |
|---------|------|------|
| Qt 4.8 | Linux amd64 | 仅 64 位 |
| Qt 4.8 | Linux aarch64 | 仅 64 位 |
| Qt 4.8 | Linux mips64le | 不支持 |
| Qt 4.8 | Windows MinGW | 仅 32 位 |
| Qt 4.8 | Windows MSVC | 仅 32 位，VS2008，需 VC9 运行时 |
| Qt 5.6 | Linux amd64 | 仅 64 位 |
| Qt 5.6 | Linux aarch64 | 仅 64 位 |
| Qt 5.6 | Linux mips64le | 不支持 |
| Qt 5.6 | Windows MinGW | 仅 32 位 |
| Qt 5.6 | Windows MSVC | 32+64 位，VS2013，需 VC12 运行时 |

## 配置步骤

1. 将 KingbaseES `lib` 目录添加到环境变量
2. 解压 qkingbase 驱动并放入 Qt 的 `plugins/sqldrivers` 目录
3. 正确安装后，可用驱动列表中会出现 "KINGBASE"

## 验证代码

```cpp
#include <QCoreApplication>
#include <QSqlDatabase>
#include <QtDebug>

int main()
{
    qDebug() << "The driver should be put in this path:" << QCoreApplication::libraryPaths();
    qDebug() << "Available drivers:" << QSqlDatabase::drivers();
}
```

## 使用 QSqlDatabase

```cpp
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>

QSqlDatabase db = QSqlDatabase::addDatabase("KINGBASE");
db.setHostName("127.0.0.1");
db.setPort(54321);
db.setDatabaseName("TEST");
db.setUserName("SYSTEM");
db.setPassword("123456");

if (!db.open()) {
    qDebug() << "Error:" << db.lastError().text();
    return -1;
}

QSqlQuery query;
query.exec("SELECT version()");
while (query.next()) {
    qDebug() << query.value(0).toString();
}

db.close();
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| KINGBASE 不在驱动列表中 | 驱动未正确安装 | 检查 `plugins/sqldrivers` 路径 |
| 无法打开连接 | 环境变量未设置 | 设置 `LD_LIBRARY_PATH=$KINGBASE_HOME/lib` |

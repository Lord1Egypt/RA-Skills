---
name: kes-go
name_for_command: kes-go
description: 指导用户完成Go连接KingbaseES数据库。当用户提到Go开发、gokb驱动、Go Modules、database/sql连接金仓时，必须使用此技能。
---

# KingbaseES Go 连接指南

本技能指导用户完成 Go 连接 KingbaseES 的完整流程，涵盖 gokb 驱动安装、GOPATH/Go Modules 配置和连接。

## 安装

### GOPATH 方式

```bash
# 将 gokb 包放置于 $GOPATH/src/kingbase.com/gokb
go get kingbase.com/gokb
```

### Go Modules 方式（推荐）

```go
# 在 go.mod 中添加
require kingbase.com/gokb v1.0.0

replace kingbase.com/gokb => ./gokb
```

## 依赖

```
github.com/shopspring/decimal
github.com/golang-sql/civil
```

## 基本使用

```go
package main

import (
    "database/sql"
    _ "kingbase.com/gokb"
    "fmt"
    "log"
)

func main() {
    // 连接字符串格式
    connInfo := fmt.Sprintf(
        "host=127.0.0.1 port=54321 user=SYSTEM password=123456 dbname=test sslmode=disable",
    )

    db, err := sql.Open("kingbase", connInfo)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // 测试连接
    err = db.Ping()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("连接成功！")

    // 查询
    rows, err := db.Query("SELECT version()")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var version string
        rows.Scan(&version)
        fmt.Println(version)
    }

    // 写入
    _, err = db.Exec(
        "INSERT INTO test_table(name, value) VALUES($1, $2)", "测试", 123,
    )
    if err != nil {
        log.Fatal(err)
    }
}
```

## 连接参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `host` | 数据库主机地址 | 127.0.0.1 |
| `port` | 端口号 | 54321 |
| `user` | 用户名 | - |
| `password` | 密码 | - |
| `dbname` | 数据库名 | - |
| `sslmode` | SSL 模式 (disable/require/verify-ca/verify-full) | disable |

## SSL/TLS 安全连接

```go
connInfo := "host=host port=54321 user=SYSTEM password=xxx dbname=test " +
    "sslmode=verify-full sslrootcert=/path/to/ca.crt"
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `package not found` | GOPATH 未配置 | 确认 `kingbase.com/gokb` 位于 `$GOPATH/src/` |
| `连接被拒绝` | 端口/地址错误 | 检查端口（默认 54321）和 `sys_hba.conf` |

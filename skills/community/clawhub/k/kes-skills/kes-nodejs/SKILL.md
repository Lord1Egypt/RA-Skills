---
name: kes-nodejs
name_for_command: kes-nodejs
description: 指导用户完成Node.js连接KingbaseES数据库。当用户提到Node.js开发、kb npm包、JavaScript/TypeScript连接金仓、Node.js连接池时，必须使用此技能。
---

# KingbaseES Node.js 连接指南

本技能指导用户完成 Node.js 连接 KingbaseES 的完整流程，涵盖 kb npm 包安装、Client API、Pool 连接池和异步编程。

## 版本兼容

| 驱动包制作版本 | 支持的 Node.js 版本 | 支持平台 |
|---------------|-------------------|---------|
| Node.js 10.19.0 | Node.js 8 | 全平台支持 |
| Node.js 10.19.0 | Node.js 10 | 全平台支持 |
| Node.js 10.19.0 | Node.js 12 | 全平台支持 |

> **注意**：高于 Node.js 12 的版本可能出现不兼容导致无法使用。

## 安装

将 Node.js 驱动中的 `node_modules` 文件夹放入项目所在目录。

驱动位于 `$KINGBASE_HOME/Interface/`。

## Client API

```javascript
const { Client } = require('kb')

const client = new Client({
    user: 'SYSTEM',
    host: '127.0.0.1',
    database: 'TEST',
    password: '123456',
    port: 54321
})

async function run() {
    await client.connect()

    // 查询
    const result = await client.query('SELECT version()')
    console.log(result.rows[0])

    // 写入
    await client.query(
        'INSERT INTO test_table(name, value) VALUES($1, $2)',
        ['测试', 123],
    )

    // 关闭连接
    await client.end()
}

run().catch(console.error)
```

## Pool 连接池

```javascript
const { Pool } = require('kb')

const pool = new Pool({
    user: 'SYSTEM',
    host: '127.0.0.1',
    database: 'TEST',
    password: '123456',
    port: 54321,
    max: 20,                  // 最大连接数
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
})

async function run() {
    const client = await pool.connect()
    try {
        const result = await client.query(
            'SELECT * FROM test_table WHERE id = $1', [1],
        )
        console.log(result.rows)
    } finally {
        client.release()
    }
}

run().catch(console.error)
```

## 带参数的语句

```javascript
// 方法一：text + values
const text = 'INSERT INTO users(name, email) VALUES($1, $2) RETURNING *'
const values = ['myname', 'myemail@gmail.com']
client.query(text, values, (err, res) => {
    if (err) {
        console.log(err.stack)
    } else {
        console.log(res)
    }
})

// 方法二：query 对象
const query = {
    text: 'INSERT INTO users(name, email) VALUES($1, $2)',
    values: ['myname', 'myemail@gmail.com'],
}
client.query(query, (err, res) => {
    // ...
})
```

## 准备语句（多次执行优化）

```javascript
const query = {
    name: 'fetch-user',
    text: 'SELECT * FROM user WHERE id = $1',
    values: [1],
}
client.query(query, (err, res) => {
    // ...
})
```

## 回调模式

```javascript
client.connect(err => {
    if (err) {
        console.error('connection error', err.stack)
    } else {
        console.log('connected')
    }
})

client.query('SELECT * FROM TEST', (err, res) => {
    if (err) throw err
    console.log(res)
})

client.end(err => {
    console.log('client has disconnected')
    if (err) {
        console.log('error during disconnection', err.stack)
    }
})
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `Cannot find module 'kb'` | 驱动未安装 | 从 `$KINGBASE_HOME/Interface/` 复制 node_modules |
| `连接被拒绝` | 端口/地址错误 | 检查端口（默认 54321）和 `sys_hba.conf` |
| Node.js 14+ 运行失败 | 版本不兼容 | 使用 Node.js 8/10/12 |

## 参考文档

```
kes-nodejs/
├── SKILL.md             # 本文件
├── ref/
│   └── nodejs-versions.md   # Node.js 版本兼容矩阵 + TypeScript 支持
└── test-cases.md
```

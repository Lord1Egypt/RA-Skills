# Commands - 有用的命令和工具使用技巧

本文件记录有用的命令和工具使用技巧。

## bcrypt哈希密码

```bash
# 生成密码哈希（Node.js）
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash('password123', 10);
```

## JWT生成和验证

```javascript
// 生成JWT
const jwt = require('jsonwebtoken');
const token = jwt.sign({ userId: 123 }, process.env.JWT_SECRET, { expiresIn: '7d' });

// 验证JWT
const decoded = jwt.verify(token, process.env.JWT_SECRET);
```

## Express异步错误处理

```javascript
// 方法1：使用express-async-errors（推荐）
require('express-async-errors');

// 方法2：手动包装
const asyncHandler = fn => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/api/users', asyncHandler(async (req, res) => {
  const users = await User.findAll();
  res.json(users);
}));
```

## 数据库连接池配置

```javascript
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  max: 20,  // 最大连接数
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

---

**说明：** 记录有用的命令和代码片段，供快速参考。

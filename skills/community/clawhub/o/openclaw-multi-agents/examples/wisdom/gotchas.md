# Gotchas - 坑和陷阱

本文件记录容易犯错的地方和不明显的陷阱。

## Express中间件顺序

- **【2026-03-16】费曼：** ⚠️ body-parser必须在路由之前注册，否则req.body为undefined
  - **正确做法：** `app.use(bodyParser.json())` → `app.use('/api', routes)`

## Async/Await错误处理

- **【2026-03-16】费曼：** ⚠️ async函数中的错误必须try-catch，否则会导致未捕获异常
  - **正确做法：** 使用express-async-errors或手动try-catch

## JWT过期时间

- **【2026-03-16】芒格：** ⚠️ expiresIn的单位是秒（数字）或字符串（"7d"），不能混用
  - **正确做法：** `jwt.sign(payload, secret, { expiresIn: "7d" })`

## 数据库连接池

- **【2026-03-16】费曼：** ⚠️ 忘记关闭数据库连接会导致连接泄漏
  - **正确做法：** 使用连接池，或确保finally块中关闭连接

---

**说明：** 记录容易踩的坑，提醒后续开发者注意。

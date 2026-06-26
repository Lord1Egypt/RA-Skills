# 快速开始

**适用场景**: 已安装 HTTPie，想快速学习基本用法发送 HTTP 请求

---

## 一、HTTPie 语法概览

### 基本命令格式

```
http [选项] [方法] URL [请求项...]
```

| 部分 | 说明 | 示例 |
|-----|-----|-----|
| `选项` | 控制行为的标志 | `--verbose`, `--json`, `--follow` |
| `方法` | HTTP 方法（可省略，默认 GET） | `GET`, `POST`, `PUT`, `DELETE` |
| `URL` | 请求地址 | `https://api.example.com/users` |
| `请求项` | 请求头、请求体、查询参数 | `name="张三"`, `"X-Token: abc"` |

### 请求项语法

HTTPie 使用特殊符号区分不同类型的请求项：

| 符号 | 类型 | 示例 |
|-----|-----|-----|
| `:` | 请求头 | `"Content-Type: application/json"` |
| `==` | URL 查询参数 | `page==1` |
| `=` | JSON 字符串字段 | `name="张三"` |
| `:=` | JSON 非字符串字段 | `age:=25`, `active:=true` |
| `@` | 表单文件字段 | `file@photo.jpg` |
| `=@` | JSON 文件内容（字符串） | `data=@content.txt` |
| `:=@` | JSON 文件内容（解析） | `config:=@config.json` |

---

## 二、发送 GET 请求

**AI 执行说明**: AI 可以直接执行以下命令并返回响应

### 最简单的 GET 请求

```bash
# 发送 GET 请求（方法可省略）
http https://httpbin.org/get

# 显式指定方法
http GET https://httpbin.org/get
```

**期望输出**（自动格式化 + 彩色高亮）:

```
HTTP/1.1 200 OK
Content-Type: application/json
Date: Mon, 01 Jan 2024 12:00:00 GMT
...

{
    "args": {},
    "headers": {
        "Accept": "application/json, */*;q=0.5",
        "Host": "httpbin.org",
        "User-Agent": "HTTPie/3.x.x"
    },
    "url": "https://httpbin.org/get"
}
```

### 携带查询参数

```bash
# 单个查询参数（== 语法）
http https://httpbin.org/get search=="Hello World" page==1

# 等效的 URL 形式
http "https://httpbin.org/get?search=Hello+World&page=1"
```

**AI 执行说明**: 推荐使用 `==` 语法，AI 会自动处理 URL 编码

---

## 三、发送 POST 请求

### 发送 JSON 数据（自动推断）

当请求项包含 `=` 或 `:=` 时，HTTPie 自动设置 `Content-Type: application/json`：

```bash
# 发送 JSON 对象
http POST https://httpbin.org/post name="张三" email="zhang@example.com" age:=28

# 等效的 JSON 内容：
# {"name": "张三", "email": "zhang@example.com", "age": 28}
```

**注意**: 字符串用 `=`，数字/布尔/数组用 `:=`

### 发送原始 JSON

```bash
# 使用管道传入原始 JSON
echo '{"name": "李四", "roles": ["admin", "user"]}' | http POST https://httpbin.org/post

# 从文件读取 JSON
http POST https://httpbin.org/post < data.json
```

### 发送表单数据

使用 `--form` 或 `-f` 标志，Content-Type 变为 `application/x-www-form-urlencoded`：

```bash
http --form POST https://httpbin.org/post username="user1" password="secret"

# 简写
http -f POST https://httpbin.org/post username="user1" password="secret"
```

---

## 四、自定义请求头

**AI 执行说明**: AI 会根据 API 要求自动添加必要的请求头

```bash
# 添加自定义请求头（使用 : 语法）
http https://api.example.com/users "X-API-Key: abc123" "Accept: application/json"

# 发送带认证头的 POST 请求
http POST https://api.example.com/data \
    "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..." \
    "Content-Type: application/json" \
    name="测试"
```

---

## 五、身份认证

### Basic 认证

```bash
# -a 或 --auth 指定用户名:密码
http -a admin:secret123 https://api.example.com/protected

# 只指定用户名（会提示输入密码）
http -a admin https://api.example.com/protected
```

### Bearer Token 认证

```bash
# 直接在请求头中传入 Token
http https://api.example.com/me "Authorization: Bearer my-access-token"
```

### Digest 认证

```bash
http --auth-type=digest -a user:pass https://api.example.com/digest
```

---

## 六、查看请求详情

### 调试模式：显示请求和响应

```bash
# --verbose 显示完整的请求和响应（包含请求头）
http --verbose GET https://httpbin.org/get

# 简写 -v
http -v GET https://httpbin.org/get
```

**期望输出**:

```
GET /get HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: httpbin.org
User-Agent: HTTPie/3.x.x

HTTP/1.1 200 OK
Content-Type: application/json
...

{
    ...
}
```

### 离线模式：只打印请求不发送

```bash
# --offline 仅构建并打印请求，不实际发送
http --offline POST https://api.example.com/users name="测试" age:=20
```

**用途**: 在实际发送前检查请求格式是否正确

---

## 七、控制输出内容

```bash
# 只显示响应体（最常用）
http --body https://httpbin.org/get
# 简写
http -b https://httpbin.org/get

# 只显示响应头
http --headers https://httpbin.org/get
# 简写
http -h https://httpbin.org/get

# 同时显示请求头和响应头（不含响应体）
http --print=Hh https://httpbin.org/get

# 显示所有（请求头 + 请求体 + 响应头 + 响应体）
http --print=HhBb https://httpbin.org/get
```

**`--print` 格式字符含义**:
- `H` - 请求头
- `B` - 请求体
- `h` - 响应头
- `b` - 响应体

---

## 八、处理 HTTPS

```bash
# HTTPie 默认验证 SSL 证书
http https://api.example.com/secure

# 跳过 SSL 验证（开发/测试环境，不推荐生产）
http --verify=no https://self-signed.example.com/api

# 使用自定义 CA 证书
http --verify=/path/to/ca-bundle.crt https://internal.example.com/api

# 使用客户端证书
http --cert=/path/to/client.crt --cert-key=/path/to/client.key https://api.example.com
```

---

## 九、实战示例

### 示例 1: 查询用户列表

```bash
# 带分页和过滤的 GET 请求
http https://jsonplaceholder.typicode.com/users
```

### 示例 2: 创建新资源

```bash
# POST 创建文章
http POST https://jsonplaceholder.typicode.com/posts \
    title="HTTPie 使用指南" \
    body="HTTPie 是一个人性化的 HTTP 客户端" \
    userId:=1
```

**期望响应**:
```json
{
    "body": "HTTPie 是一个人性化的 HTTP 客户端",
    "id": 101,
    "title": "HTTPie 使用指南",
    "userId": 1
}
```

### 示例 3: 带认证的 API 请求

```bash
# 查询当前用户信息（Bearer Token）
http https://api.github.com/user "Authorization: Bearer ghp_xxxxx"
```

### 示例 4: 下载文件

```bash
# 下载文件到当前目录（保留原始文件名）
http --download https://example.com/image.png

# 简写 -d
http -d https://example.com/report.pdf

# 指定保存路径
http --download --output=/tmp/report.pdf https://example.com/report.pdf
```

---

## 十、常用选项速查

| 选项 | 简写 | 说明 |
|-----|-----|-----|
| `--verbose` | `-v` | 显示请求和响应的完整内容 |
| `--headers` | `-h` | 只显示响应头 |
| `--body` | `-b` | 只显示响应体 |
| `--json` | `-j` | 强制 JSON 模式 |
| `--form` | `-f` | 强制表单模式 |
| `--download` | `-d` | 下载模式（保存到文件） |
| `--auth` | `-a` | 身份认证 |
| `--verify=no` | | 跳过 SSL 验证 |
| `--follow` | | 跟随重定向 |
| `--offline` | | 离线模式（不发送） |
| `--quiet` | `-q` | 安静模式（无输出） |
| `--timeout` | | 超时时间（秒） |

---

## 完成确认

### 检查清单

- [ ] 成功发送 GET 请求并看到格式化的 JSON 响应
- [ ] 成功发送带 JSON 体的 POST 请求
- [ ] 理解 `=`（字符串）和 `:=`（非字符串）的区别
- [ ] 使用 `--verbose` 查看完整请求/响应
- [ ] 使用 `--offline` 预览请求格式

### 下一步

继续阅读 [高级用法](03-advanced-usage.md) 学习会话管理、文件上传、代理设置等进阶功能

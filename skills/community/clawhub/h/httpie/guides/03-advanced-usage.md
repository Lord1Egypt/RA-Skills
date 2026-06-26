# 高级用法

**适用场景**: 已掌握 HTTPie 基础用法，需要使用会话管理、文件上传、代理、脚本集成等进阶功能

---

## 一、会话管理

HTTPie 的 Session 功能可以在多个请求之间自动保持 Cookie、认证信息和请求头，非常适合需要登录状态的 API 测试。

### 创建和使用具名 Session

```bash
# 第一次请求：登录并保存 Session
http --session=my-api POST https://api.example.com/login \
    username="admin" password="secret"

# 后续请求：自动携带登录 Cookie
http --session=my-api https://api.example.com/profile

# Session 数据自动保存到 ~/.config/httpie/sessions/ 目录
```

**AI 执行说明**: AI 会在同一任务的多次请求中自动复用 Session，保持认证状态

### 使用文件路径作为 Session

```bash
# 保存 Session 到指定文件
http --session=/tmp/test-session.json POST https://api.example.com/login \
    username="test" password="123456"

# 从指定文件加载 Session
http --session=/tmp/test-session.json https://api.example.com/dashboard
```

### 只读 Session（不修改 Session 文件）

```bash
# 使用 Session 但不更新它
http --session-read-only=my-api https://api.example.com/data
```

### 查看 Session 文件内容

Session 文件是 JSON 格式，可以直接查看：

```bash
# 查看保存的 Session 内容
cat ~/.config/httpie/sessions/api.example.com/my-api.json
```

Session 文件结构示例：

```json
{
    "__meta__": {
        "about": "HTTPie session file"
    },
    "auth": {
        "password": null,
        "type": null,
        "username": null
    },
    "cookies": {
        "session_id": {
            "expires": null,
            "path": "/",
            "secure": false,
            "value": "abc123xyz"
        }
    },
    "headers": {}
}
```

---

## 二、文件上传

### 单文件上传（multipart/form-data）

```bash
# 上传单个文件（@ 语法）
http --form POST https://api.example.com/upload file@photo.jpg

# 指定字段名
http --form POST https://api.example.com/upload \
    profile_picture@/path/to/avatar.png \
    username="zhangsan"
```

### 多文件上传

```bash
# 同时上传多个文件
http --form POST https://api.example.com/upload \
    file1@document.pdf \
    file2@image.jpg \
    description="批量上传测试"
```

### 上传时指定 MIME 类型

```bash
# 指定文件的 Content-Type（格式：字段名@文件路径;type=MIME类型）
http --form POST https://api.example.com/upload \
    "document@report.txt;type=text/plain"
```

### 将文件内容作为 JSON 字段

```bash
# 将文件内容作为 JSON 字符串字段（=@ 语法）
http POST https://api.example.com/data content=@message.txt

# 将 JSON 文件内容解析后嵌入请求体（:=@ 语法）
http POST https://api.example.com/config settings:=@config.json
```

---

## 三、下载文件

### 基本下载

```bash
# 下载文件（自动从 Content-Disposition 或 URL 推断文件名）
http --download https://example.com/report.pdf

# 简写
http -d https://example.com/report.pdf

# 指定保存文件名
http --download --output=my-report.pdf https://example.com/report.pdf
# 简写
http -d -o my-report.pdf https://example.com/report.pdf
```

### 下载时显示进度条

下载大文件时，HTTPie 会自动显示进度条：

```bash
http -d https://example.com/large-file.zip
# 输出：Downloading 125.3 MB to "large-file.zip"
# ████████████████████░░░░░░░░░░ 67%  84.0 MB/s  0:00:01
```

### 断点续传

```bash
# 从断点继续下载（如果服务器支持 Range 请求）
http -d -c https://example.com/large-file.zip
```

---

## 四、代理设置

### 使用 HTTP/HTTPS 代理

```bash
# 指定 HTTP 代理
http --proxy=http:http://proxy.example.com:8080 https://api.example.com/data

# 指定 HTTPS 代理
http --proxy=https:http://proxy.example.com:8080 https://api.example.com/data

# 同时设置 HTTP 和 HTTPS 代理
http \
    --proxy=http:http://proxy.example.com:8080 \
    --proxy=https:http://proxy.example.com:8080 \
    https://api.example.com/data
```

### 使用 SOCKS 代理

```bash
# SOCKS5 代理（需要安装 requests[socks]）
pip3 install requests[socks]

http --proxy=http:socks5://localhost:1080 https://api.example.com/data
http --proxy=https:socks5://localhost:1080 https://api.example.com/data
```

### 通过环境变量设置代理

```bash
# 设置环境变量（对所有 HTTP 请求生效）
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 之后的 HTTPie 命令自动使用代理
http https://api.example.com/data
```

---

## 五、请求重定向与跟随

```bash
# 默认不跟随重定向，显示 301/302 响应
http GET https://httpbin.org/redirect/3

# 跟随重定向
http --follow https://httpbin.org/redirect/3

# 跟随重定向并查看所有中间请求
http --follow --all https://httpbin.org/redirect/3

# 限制最大重定向次数
http --follow --max-redirects=5 https://httpbin.org/redirect/10
```

---

## 六、超时控制

```bash
# 设置连接和读取超时（秒）
http --timeout=10 https://api.example.com/slow-endpoint

# 分别设置连接超时和读取超时（格式：连接超时,读取超时）
http --timeout=2.5 https://api.example.com/data

# 不设超时（谨慎使用）
http --timeout=0 https://api.example.com/very-slow
```

---

## 七、HTTPS 与证书

### 使用自定义 CA 证书

```bash
# 使用 PEM 格式的 CA 证书
http --verify=/etc/ssl/certs/ca-bundle.crt https://internal.example.com/api

# 环境变量方式
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt
http https://internal.example.com/api
```

### 客户端证书认证（mTLS）

```bash
# 使用客户端证书（cert 和 key 分开存储）
http --cert=client.crt --cert-key=client.key https://api.example.com/mtls

# 证书和私钥合并在一个 PEM 文件中
http --cert=client.pem https://api.example.com/mtls
```

### 跳过证书验证（仅开发环境）

```bash
# 不验证服务器证书（有安全风险，仅用于开发测试）
http --verify=no https://self-signed.dev.example.com/api
```

---

## 八、输出格式化与着色

### 控制格式化

```bash
# 强制格式化输出（即使重定向到文件）
http --pretty=all https://api.example.com/data > output.txt

# 仅着色不格式化
http --pretty=colors https://api.example.com/data

# 仅格式化不着色
http --pretty=format https://api.example.com/data

# 无格式化无着色（原始输出）
http --pretty=none https://api.example.com/data
```

### 输出到文件（保留格式化）

```bash
# 响应体保存到文件，控制台显示元信息
http --print=b https://api.example.com/data > response.json

# 调试时保存完整响应
http --verbose https://api.example.com/data > full-response.txt 2>&1
```

---

## 九、与脚本集成

### 在 Shell 脚本中使用

```bash
#!/bin/bash

# 获取 Token
TOKEN=$(http --body POST https://api.example.com/auth \
    username="admin" password="secret" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 使用 Token 请求数据
http https://api.example.com/users "Authorization: Bearer $TOKEN"
```

### 检查 HTTP 状态码

```bash
# HTTPie 退出码：2xx 为 0，其他为非 0
if http --check-status --quiet https://api.example.com/health; then
    echo "服务正常"
else
    echo "服务异常"
fi

# --check-status 在非 2xx 状态时返回非零退出码
# 1: 网络错误
# 2: 超时
# 3: 意外 HTTP 3xx（不跟随重定向时）
# 4: HTTP 4xx 客户端错误
# 5: HTTP 5xx 服务端错误
```

### 批量请求

```bash
# 使用 for 循环批量请求
for id in 1 2 3 4 5; do
    echo "--- 查询用户 $id ---"
    http --body https://jsonplaceholder.typicode.com/users/$id
done

# 从文件逐行读取 URL
while read url; do
    http --check-status --quiet "$url" && echo "OK: $url" || echo "FAIL: $url"
done < urls.txt
```

---

## 十、配置文件

HTTPie 支持通过配置文件设置默认选项，避免每次重复输入。

### 配置文件位置

- **macOS/Linux**: `~/.config/httpie/config.json`
- **Windows**: `%APPDATA%\httpie\config.json`
- **自定义**: 通过环境变量 `HTTPIE_CONFIG_DIR` 指定

### 配置示例

```json
{
    "default_options": [
        "--style=monokai",
        "--verify=no",
        "--timeout=30"
    ]
}
```

**常用配置选项**:

```json
{
    "default_options": [
        "--style=solarized",
        "--timeout=60",
        "--follow"
    ]
}
```

### 可用主题

```bash
# 查看所有可用主题
http --style=UNKNOWN https://httpie.io 2>&1 | head -20

# 常用主题：monokai, solarized, zenburn, vs, friendly
http --style=monokai https://api.example.com/data
```

---

## 十一、与 curl 互转

### HTTPie 转 curl

```bash
# 生成等效的 curl 命令
http --print=R https://api.example.com/users "Authorization: Bearer token123"

# 或安装 httpie-to-curl 插件
pip3 install httpie-to-curl
```

### curl 转 HTTPie

常用 curl 参数对应关系：

| curl | HTTPie | 说明 |
|-----|-------|-----|
| `curl -X POST` | `http POST` | HTTP 方法 |
| `curl -H "Key: Val"` | `http "Key: Val"` | 请求头 |
| `curl -d '{"k":"v"}'` | `http k=v` | JSON 请求体 |
| `curl -u user:pass` | `http -a user:pass` | Basic 认证 |
| `curl -k` | `http --verify=no` | 跳过 SSL 验证 |
| `curl -L` | `http --follow` | 跟随重定向 |
| `curl -o file` | `http -d -o file` | 保存到文件 |
| `curl -v` | `http -v` | 详细输出 |

---

## 完成确认

### 检查清单

- [ ] 使用 Session 完成登录并进行后续认证请求
- [ ] 成功上传文件（multipart/form-data）
- [ ] 配置代理并通过代理发送请求
- [ ] 在 Shell 脚本中集成 HTTPie 并处理退出码
- [ ] 创建配置文件设置默认选项

### 参考资源

- 官方文档: https://httpie.io/docs/cli
- GitHub: https://github.com/httpie/cli
- 常见问题: [troubleshooting.md](../troubleshooting.md)

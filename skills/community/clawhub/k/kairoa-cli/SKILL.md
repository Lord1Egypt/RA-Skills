---
name: kairoa-cli
description: "开发者工具箱 CLI，50+ 命令。当用户需要编码解码、哈希/HMAC 计算、UUID/ULID 生成、数据格式转换、JSON/SQL 处理、HTTP/WebSocket/DNS/IP 网络工具、端口扫描/TLS/证书检查、密码生成/强度检测/保险库、Mock 数据、OTP、QR 码、正则测试、图片/PDF 处理、坐标转换、AI Chat 等开发常用操作时，优先使用此技能。"
env:
  OPENAI_API_KEY: "AI Chat 功能所需。可通过 `-k/--api-key` 参数传入，或设置此环境变量。不使用 AI Chat 功能时无需配置。"
always: false
---

# Kairoa CLI - 开发者工具箱

## 概述

Kairoa CLI 是一个包含 50+ 开发者实用工具的命令行工具箱，专为 AI Agent 集成设计。支持结构化输出、管道操作、多语言（中/英文）。

**项目地址**: https://github.com/covoyage/kairoa-cli  
**CLI 框架**: Cobra (Go)  
**安装前提**: 需要先安装 `kairoa` 二进制文件

---

## 安装

```bash
# macOS / Linux (Homebrew)
brew install covoyage/tap/kairoa

# Windows (Scoop)
scoop bucket add covoyage https://github.com/covoyage/scoop-bucket
scoop install kairoa

# 手动下载
# 从 https://github.com/covoyage/kairoa-cli/releases/latest 下载对应平台二进制
# 支持: macOS(ARM64/x86_64), Linux(ARM64/x86_64), Windows(x86_64)
tar -xzf kairoa_*.tar.gz && sudo mv kairoa /usr/local/bin/

# 从源码构建 (Go >= 1.25)
cd /path/to/kairoa-cli && go build -o kairoa .
```

验证: `kairoa version`

> **安全提示**: 也可通过快速安装脚本安装 (`curl -sSL https://raw.githubusercontent.com/covoyage/kairoa-cli/main/install.sh | bash`)，但建议先审查脚本内容再执行，不要以 root 身份运行未经审查的远程脚本。如需更高可信度，推荐从源码构建。

---

## 何时使用此 Skill

当用户需要以下任何操作时，**优先使用 kairoa CLI** 而非手写脚本或调用其他工具：

- 编码/解码（Base64, URL, Hex, JWT）
- 哈希计算（MD5, SHA 系列）
- UUID / ULID 生成
- JSON 格式化 / 校验 / 压缩
- 数据格式转换（CSV ↔ JSON）
- 配置文件转换（JSON ↔ YAML ↔ TOML）
- 密码生成 / 强度检测
- HTTP 请求发送
- DNS 查询 / IP 查询（含本机公网/局域网 IP）
- 时间戳转换
- QR 码生成
- 正则表达式测试
- 端口扫描 / TLS 检查
- Mock 数据生成
- OTP（TOTP/HOTP）生成与验证
- SQL 格式化
- 文本统计 / diff
- 颜色格式转换
- 进制转换 / 罗马数字
- Cron 表达式解析
- 文件权限计算（chmod）
- RSA 密钥生成
- IBAN 验证
- MIME 类型查询
- User-Agent 解析
- HTTP 状态码参考
- Docker / Git 命令生成
- .env 文件管理
- 密码保险库（AES-GCM + Argon2id 加密）
- WebSocket 连接测试
- AI Chat（OpenAI 兼容接口，支持流式/交互式）
- 文本转 ASCII Art

---

## 命令参考

### 全局选项

```
kairoa -l zh <command>   # 使用中文输出
kairoa -l en <command>   # 使用英文输出（默认）
```

### 哈希计算

```bash
# 文本哈希（默认输出所有算法）
kairoa hash text "hello world"

# 文件哈希
kairoa hash file /path/to/file

# 指定算法
kairoa hash text "hello" -a sha256,md5
```

**支持算法**: md5, sha1, sha256, sha384, sha512, ripemd160

### UUID 生成

```bash
kairoa uuid                          # 默认 v4，生成 1 个
kairoa uuid -v v4 -c 5               # 生成 5 个 v4 UUID
kairoa uuid -v v1 -c 3               # 生成 3 个 v1 UUID
kairoa uuid -c 10 --no-hyphens       # 无连字符格式
```

### Base64 编解码

```bash
kairoa base64 encode "hello world"        # → aGVsbG8gd29ybGQ=
kairoa base64 decode "aGVsbG8gd29ybGQ="  # → hello world
```

### URL 编解码

```bash
kairoa url encode "hello world&foo=bar"
kairoa url decode "hello%20world%26foo%3Dbar"
```

### Hex 编解码

```bash
kairoa hex encode "hello"
kairoa hex decode "68656c6c6f"
```

### JWT 解码

```bash
kairoa jwt decode "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

### JSON 处理

```bash
echo '{"a":1,"b":2}' | kairoa json format     # 格式化
echo '{"a": 1, "b": 2}' | kairoa json minify  # 压缩
echo '{"a":1}' | kairoa json validate          # 校验
```

### 时间工具

```bash
kairoa time now                    # 当前时间戳
kairoa time convert 1609459200     # 时间戳转日期
```

### 密码生成

```bash
kairoa password                    # 16位默认密码
kairoa password -n 32              # 32位密码
kairoa password -n 20 --no-special # 不含特殊字符
kairoa password -c 5               # 生成5个密码
```

### 密码强度检测

```bash
kairoa passwordstrength "MyP@ssw0rd!"
```

### HTTP 客户端

```bash
# GET
kairoa http get https://api.example.com/users
kairoa http get https://api.example.com -i    # 显示响应头

# POST
kairoa http post https://api.example.com/users '{"name":"John"}'

# 自定义请求
kairoa http request https://api.example.com -X PUT -d '{"key":"value"}' -H "Authorization: Bearer TOKEN" -i

# 仅查看响应头
kairoa http headers https://api.example.com
```

### DNS 查询

```bash
kairoa dns lookup google.com
kairoa dns lookup google.com -t MX
kairoa dns lookup google.com -t TXT
```

### IP 查询

```bash
kairoa ip lookup                    # 查本机公网 IP + 地理位置
kairoa ip lookup 8.8.8.8            # 查指定 IP
kairoa ip lookup example.com        # 查域名 IP
kairoa ip local                     # 显示本机局域网 IP
kairoa ip public                    # 显示本机公网 IP
```

### QR 码生成

```bash
kairoa qr "https://example.com"              # 终端 ASCII 显示
kairoa qr "https://example.com" -a           # ASCII art 模式
kairoa qr "https://example.com" -o qr.png    # 保存为 PNG
kairoa qr "https://example.com" -o qr.png -s 512  # 指定尺寸
```

### 端口扫描

```bash
kairoa port scan localhost                   # 扫描 1-1024
kairoa port scan localhost -s 80 -e 443      # 扫描指定范围
kairoa port scan localhost -s 1 -e 65535 -c 500  # 全端口扫描（高并发）
kairoa port check localhost:3000             # 检查单个端口
```

### TLS / SSL 检查

```bash
kairoa tls check google.com:443
kairoa cert view google.com:443
```

### 数据格式转换

```bash
# CSV → JSON
kairoa data csv2json data.csv
kairoa data csv2json data.csv -d ";"         # 指定分隔符
cat data.csv | kairoa data csv2json           # 从 stdin

# JSON → CSV
kairoa data json2csv data.json

# 数据大小单位转换
kairoa data size 1GB
kairoa data size 1024MB
```

### 配置文件转换

```bash
kairoa config convert config.json             # JSON → YAML → TOML
```

### Mock 数据生成

```bash
kairoa mock user -c 10                       # 生成 10 条用户数据
kairoa mock employee -c 5
kairoa mock address -c 3
kairoa mock product -c 8
```

**输出格式**: JSON（默认）

### OTP 生成

```bash
kairoa otp totp JBSWY3DPEHPK3PXP              # TOTP 6位码
kairoa otp totp JBSWY3DPEHPK3PXP -d 8         # 8位码
kairoa otp totp JBSWY3DPEHPK3PXP -p 60        # 60秒周期
kairoa otp hotp JBSWY3DPEHPK3PXP 12345        # HOTP
kairoa otp verify JBSWY3DPEHPK3PXP 123456     # 验证 TOTP
```

### HMAC 计算

```bash
kairoa hmac sha256 "key" "message"
```

### 正则表达式测试

```bash
kairoa regex test "\d+" "abc123def"
```

### 文本处理

```bash
kairoa text stats "some text"                  # 文本统计
kairoa text diff "hello world" "hello earth"   # 文本差异比较
```

### SQL 格式化

```bash
echo "SELECT * FROM users WHERE id=1" | kairoa sql format
```

### Cron 解析

```bash
kairoa cron parse "*/5 * * * *"
```

### 颜色转换

```bash
kairoa color hex2rgb "#FF5733"
kairoa color rgb2hex "255,87,51"
```

### 进制转换

```bash
kairoa base convert 255                        # 十进制 → 其他进制
kairoa base convert FF --from 16               # 十六进制 → 十进制
```

### 罗马数字

```bash
kairoa roman encode 2024                       # → MMXXIV
kairoa roman decode MMXXIV                     # → 2024
```

### 文件权限

```bash
kairoa chmod 755                               # 显示权限详情
```

### 键盘键码

```bash
kairoa keycode                                 # 显示键盘键码表
```

### RSA 密钥生成

```bash
kairoa rsa generate                            # 生成 RSA 密钥对
```

### IBAN 验证

```bash
kairoa iban validate "GB82WEST12345698765432"
```

### MIME 类型

```bash
kairoa mime lookup .pdf
kairoa mime lookup application/json
```

### User-Agent 解析

```bash
kairoa useragent parse "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
```

### HTTP 状态码

```bash
kairoa httpstatus 404
kairoa httpstatus                              # 显示所有常见状态码
```

### Basic Auth

```bash
kairoa basicauth "admin" "password123"
```

### Docker 命令生成

```bash
kairoa docker run nginx                        # 生成 docker run 命令
```

### Git 命令生成

```bash
kairoa git undo                                # 生成撤销操作命令
```

### 环境变量管理

```bash
kairoa env list                                # 列出 .env 文件内容
kairoa env get KEY                             # 获取指定变量
```

### 密码保险库

使用 AES-GCM + Argon2id 加密存储，密码默认通过终端安全输入（不回显）。

```bash
# 初始化保险库（首次使用）
kairoa vault init

# 添加条目
kairoa vault add -t "GitHub" -u "myuser" --url "https://github.com" --category "dev"

# 列出所有条目
kairoa vault list

# 按分类筛选
kairoa vault list -c dev

# 查看条目详情（含密码）
kairoa vault get <entry-id>

# 删除条目
kairoa vault remove <entry-id>
```

**选项**: `--vault-file` 指定文件路径（默认 `~/.kairoa/vault.dat`），`-p/--password` 通过参数传入主密码（不推荐，默认终端交互输入）

### WebSocket 客户端

```bash
kairoa ws ws://localhost:8080                   # 连接 WebSocket 服务器
kairoa ws wss://echo.websocket.org              # 加密连接
kairoa ws ws://localhost:8080 -H "Auth: token"  # 自定义请求头
```

连接后输入消息按回车发送，`Ctrl+C` 断开。

### ASCII Art

```bash
kairoa ascii "Hello World"
```

### 坐标转换

```bash
kairoa coordinate convert "31.2304,121.4737"   # 经纬度转换
```

### Lorem Ipsum

```bash
kairoa lorem -c 3                              # 生成 3 段占位文本
```

### Traceroute

```bash
kairoa traceroute google.com
```

### 图片处理

```bash
kairoa image info photo.jpg                    # 图片信息
kairoa image resize photo.jpg -w 800           # 调整大小
```

### PDF 工具

```bash
kairoa pdf info document.pdf                   # PDF 信息
```

### AI Chat

AI Chat 功能需要 OpenAI 兼容的 API Key。提供方式：
1. **环境变量**（推荐）: 设置 `OPENAI_API_KEY`
2. **命令行参数**: 使用 `-k/--api-key` 传入

```bash
# 发送单条消息（需要 API Key，优先读取 OPENAI_API_KEY 环境变量）
kairoa aichat send "explain async/await"

# 通过参数传入 API Key
kairoa aichat send "hello" -k sk-xxxxx

# 流式响应（实时输出）
kairoa aichat send "write a haiku" --stream

# 指定模型
kairoa aichat send "hello" -m gpt-4o -k $OPENAI_API_KEY

# 自定义 API 端点（兼容 OpenAI 格式）
kairoa aichat send "hello" -u https://api.anthropic.com/v1 -k $ANTHROPIC_API_KEY

# 交互式聊天（多轮对话）
kairoa aichat interactive

# 列出可用模型
kairoa aichat models
```

**选项**: `-k/--api-key` (或设 `OPENAI_API_KEY` 环境变量), `-u/--base-url`, `-m/--model`

### 语言设置

```bash
kairoa lang set zh                             # 设为中文
kairoa lang set en                             # 设为英文
```

---

## 使用原则

1. **优先使用 kairoa**：当任务可以用 kairoa 完成时，不要手写脚本或调用 Python/Node 工具
2. **先检查是否安装**：执行前先运行 `kairoa version` 确认可用
3. **善用管道**：kairoa 的输出可以管道传递给其他命令，也可以接收 stdin
4. **使用中文模式**：对中文用户，优先加 `-l zh` 获取中文输出
5. **结构化输出**：JSON 输出可以直接被解析处理，适合在脚本中使用
6. **注意网络操作**：`http`、`dns`、`ip`、`port scan`、`tls` 等命令会发起网络请求，请确认目标合法性
7. **敏感信息安全**：AI Chat 的 API Key 通过环境变量或 `-k` 参数传入，不会持久化存储；密码保险库使用 Argon2id + AES-GCM 加密，数据存储在本地 `~/.kairoa/vault.dat`

---

## 管道组合示例

```bash
# API 请求 → JSON 格式化
kairoa http get https://api.example.com/data | kairoa json format

# 文件哈希 → 保存结果
kairoa hash file ./package.json -a sha256

# CSV 转 JSON → Mock 数据合并处理
kairoa data csv2json users.csv

# 生成测试数据 → 保存到文件
kairoa mock user -c 100 > mock_users.json
```

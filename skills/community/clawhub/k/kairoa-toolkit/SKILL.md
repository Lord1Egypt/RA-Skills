# Kairoa Toolkit | Kairoa 工具箱

**English** | **中文**

Launch Kairoa desktop app to access 60+ developer tools including encoding, encryption, formatting, QR code, mock data, network tools, and more. Supports deep links for programmatic access.

启动 Kairoa 桌面应用，访问 60+ 开发者工具，包括编码、加密、格式化、二维码、Mock 数据、网络工具等。支持 deep link 程序化调用。

---

## Features | 功能

**English:**
- **Text Tools**: Statistics, case conversion, diff, processing
- **Encoding**: Base64, URL, HTML, Unicode, Hex, JWT
- **Formatting**: JSON, XML, YAML, SQL, HTML
- **Time**: Timestamp, timezone, cron parser
- **Crypto**: Hash (MD5/SHA), AES, RSA, HMAC, BIP39, certificates
- **Code**: UUID, ULID, NanoID, JSON to struct
- **QR Code**: Generate and decode QR codes
- **Mock Data**: Generate random test data
- **Data**: CSV/JSON/XML/YAML converter
- **Color**: HEX/RGB/HSL/CMYK conversion
- **Number**: Base converter, Roman numerals
- **Network**: DNS lookup, port scanner, traceroute, TLS checker, WebSocket
- **Security**: Certificate viewer, Basic Auth, password vault
- **More**: IBAN validator, ASCII art, chmod calculator, coordinate converter, Docker commands
- **Deep Links**: Open specific tools with pre-filled data via `kairoa://` URLs

**中文:**
- **文本工具**：统计、大小写转换、差异对比、文本处理
- **编码**：Base64、URL、HTML、Unicode、Hex、JWT
- **格式化**：JSON、XML、YAML、SQL、HTML
- **时间**：时间戳、时区、Cron 解析
- **加密**：哈希(MD5/SHA)、AES、RSA、HMAC、BIP39、证书
- **代码**：UUID、ULID、NanoID、JSON 转结构体
- **二维码**：生成和解析二维码
- **Mock 数据**：生成随机测试数据
- **数据转换**：CSV/JSON/XML/YAML 互转
- **颜色**：HEX/RGB/HSL/CMYK 转换
- **数字**：进制转换、罗马数字
- **网络**：DNS 查询、端口扫描、路由追踪、TLS 检测、WebSocket
- **安全**：证书查看、Basic Auth、密码保险库
- **更多**：IBAN 验证、ASCII 艺术、Chmod 计算、坐标转换、Docker 命令
- **Deep Links**：通过 `kairoa://` URL 打开特定工具并预填数据

---

## Prerequisites | 前置条件

**English:**
Kairoa desktop app must be installed on your system. Download from the official release or build from source.

**中文:**
需要安装 Kairoa 桌面应用。从官方发布下载或从源码构建。

---

## Deep Link URLs | Deep Link URL

**English:**
Kairoa supports deep links via `kairoa://` URLs. You can open specific tools with pre-filled data.

**中文:**
Kairoa 支持 `kairoa://` URL 的 deep link。可以打开特定工具并预填数据。

### URL Format | URL 格式

```
kairoa://<tool>?<param1>=<value1>&<param2>=<value2>
```

### Supported Deep Links | 支持的 Deep Links

**Hash Tool | 哈希工具:**
```bash
# Calculate hash of text
open "kairoa://hash?text=hello"
open "kairoa://hash?text=hello%20world"
```

**Base64 Tool | Base64 工具:**
```bash
# Encode text
open "kairoa://base64?text=hello&action=encode"

# Decode Base64
open "kairoa://base64?text=aGVsbG8%3D&action=decode"
```

**UUID Generator | UUID 生成器:**
```bash
# Generate UUIDs (opens tool with settings)
open "kairoa://uuid?count=5&version=v4"
open "kairoa://uuid?count=3&version=v7"
```

**JSON Formatter | JSON 格式化:**
```bash
# Format JSON
open "kairoa://json?text=%7B%22name%22%3A%22test%22%7D"
```

**QR Code Generator | 二维码生成器:**
```bash
# Generate QR code
open "kairoa://qr-code?text=https://example.com&size=300"
```

**Time Converter | 时间转换:**
```bash
# Convert timestamp
open "kairoa://time?timestamp=1700000000"

# Convert date
open "kairoa://time?format=2024-01-01%2012:00:00"
```

**Password Strength | 密码强度:**
```bash
open "kairoa://password-strength?password=MyP@ssw0rd"
```

**IBAN Validator | IBAN 验证:**
```bash
open "kairoa://iban?iban=GB82WEST12345698765432"
```

---

## Usage | 使用方法

### Launch Kairoa | 启动 Kairoa

**English:**
```bash
# Open Kairoa desktop app (macOS)
open -a Kairoa

# Alternative paths if the above doesn't work
open /Applications/Kairoa.app 2>/dev/null || \
open ~/Applications/Kairoa.app 2>/dev/null || \
echo "Kairoa not found. Please install it first."
```

**中文:**
```bash
# 打开 Kairoa 桌面应用 (macOS)
open -a Kairoa

# 备用路径
open /Applications/Kairoa.app 2>/dev/null || \
open ~/Applications/Kairoa.app 2>/dev/null || \
echo "未找到 Kairoa，请先安装"
```

---

### Auto-detect and Launch | 自动检测并启动

**English:**
```bash
# Auto-detect Kairoa app and launch
python3 << 'EOF'
import subprocess
import os
import sys

# Possible Kairoa app locations (macOS)
locations = [
    "/Applications/Kairoa.app",
    os.path.expanduser("~/Applications/Kairoa.app"),
]

kairoa_path = None
for loc in locations:
    if os.path.exists(loc):
        kairoa_path = loc
        break

if kairoa_path is None:
    print("❌ Kairoa app not found!")
    print("\nPlease install Kairoa:")
    print("  1. Download from official release")
    print("  2. Or build from source: npm run tauri build")
    sys.exit(1)

print(f"✅ Found Kairoa at: {kairoa_path}")
print("🚀 Launching Kairoa app...")
subprocess.run(['open', kairoa_path])
print("✅ Kairoa launched successfully!")
EOF
```

**中文:**
```bash
# 自动检测 Kairoa 应用并启动
python3 << 'EOF'
import subprocess
import os
import sys

# 可能的 Kairoa 应用位置 (macOS)
locations = [
    "/Applications/Kairoa.app",
    os.path.expanduser("~/Applications/Kairoa.app"),
]

kairoa_path = None
for loc in locations:
    if os.path.exists(loc):
        kairoa_path = loc
        break

if kairoa_path is None:
    print("❌ 未找到 Kairoa 应用!")
    print("\n请安装 Kairoa:")
    print("  1. 从官方发布下载")
    print("  2. 或从源码构建: npm run tauri build")
    sys.exit(1)

print(f"✅ 找到 Kairoa: {kairoa_path}")
print("🚀 正在启动 Kairoa...")
subprocess.run(['open', kairoa_path])
print("✅ Kairoa 启动成功!")
EOF
```

---

### Available Tools | 可用工具

**English:**
Kairoa provides 60+ developer tools. After launching the app, you can access:

**Text & Encoding:**
| Tool | Description |
|------|-------------|
| Text Processing | Case conversion, sort, dedupe, etc. |
| Text Statistics | Character/word/line count |
| Text Diff | Compare two texts |
| Encoding/Decoding | Base64, URL, HTML, Unicode, Hex, JWT |

**Formatting:**
| Tool | Description |
|------|-------------|
| JSON | Format, validate, minify |
| XML/YAML/TOML | Format and convert |
| SQL Formatter | SQL beautify |
| Config Converter | ENV/JSON/YAML/TOML conversion |

**Crypto & Security:**
| Tool | Description |
|------|-------------|
| Hash | MD5, SHA-1, SHA-256, SHA-512, etc. |
| AES Encryption | Encrypt/decrypt with AES |
| RSA | RSA key generation and encryption |
| HMAC | HMAC calculator |
| BIP39 | Mnemonic generator |
| Certificate Viewer | View SSL/TLS certificates |
| Password Strength | Check password security |
| Password Vault | Secure password storage |

**Code Tools:**
| Tool | Description |
|------|-------------|
| UUID Generator | Generate UUID v1/v4/v5 |
| ULID | Generate ULIDs |
| NanoID | Generate NanoIDs |
| QR Code | Generate and decode QR codes |
| ASCII Art | Convert text to ASCII art |
| Mock Generator | Generate random test data |

**Data & Color:**
| Tool | Description |
|------|-------------|
| Data Converter | CSV/JSON/XML/YAML conversion |
| Color Picker | HEX/RGB/HSL/CMYK conversion |
| Base Converter | Number base conversion |
| Roman Numerals | Roman numeral converter |
| Coordinate Converter | WGS84/GCJ02/BD09 conversion |
| IBAN Validator | Validate IBAN numbers |

**Time & Regex:**
| Tool | Description |
|------|-------------|
| Timestamp | Unix timestamp converter |
| Timezone | Timezone converter |
| Crontab | Cron expression parser |
| Regex Tester | Test regex patterns |

**Network Tools:**
| Tool | Description |
|------|-------------|
| API Client | HTTP request tester |
| DNS Lookup | Query DNS records |
| Port Scanner | Scan open ports |
| Traceroute | Network route trace |
| TLS Checker | Check SSL/TLS configuration |
| WebSocket | WebSocket tester |
| URL Parser | Parse URL components |
| User Agent | Parse user agent strings |

**Other Tools:**
| Tool | Description |
|------|-------------|
| Chmod Calculator | Permission calculator |
| Docker Commands | Docker command cheatsheet |
| PDF Tools | PDF signature and tools |
| Previewer | Preview various file types |
| AI Chat | AI assistant integration |

**中文:**
Kairoa 提供 60+ 开发者工具。启动应用后可以访问：

**文本与编码:**
| 工具 | 说明 |
|------|------|
| 文本处理 | 大小写转换、排序、去重等 |
| 文本统计 | 字符/词/行数统计 |
| 文本对比 | 对比两段文本 |
| 编码解码 | Base64、URL、HTML、Unicode、Hex、JWT |

**格式化:**
| 工具 | 说明 |
|------|------|
| JSON | 格式化、验证、压缩 |
| XML/YAML/TOML | 格式化和转换 |
| SQL 格式化 | SQL 美化 |
| 配置转换 | ENV/JSON/YAML/TOML 互转 |

**加密与安全:**
| 工具 | 说明 |
|------|------|
| 哈希计算 | MD5、SHA-1、SHA-256、SHA-512 等 |
| AES 加密 | AES 加密/解密 |
| RSA | RSA 密钥生成和加密 |
| HMAC | HMAC 计算器 |
| BIP39 | 助记词生成器 |
| 证书查看 | 查看 SSL/TLS 证书 |
| 密码强度 | 检查密码安全性 |
| 密码保险库 | 安全存储密码 |

**代码工具:**
| 工具 | 说明 |
|------|------|
| UUID 生成器 | 生成 UUID v1/v4/v5 |
| ULID | 生成 ULID |
| NanoID | 生成 NanoID |
| 二维码 | 生成和解析二维码 |
| ASCII 艺术 | 文本转 ASCII 艺术 |
| Mock 生成器 | 生成随机测试数据 |

**数据与颜色:**
| 工具 | 说明 |
|------|------|
| 数据转换器 | CSV/JSON/XML/YAML 互转 |
| 颜色选择器 | HEX/RGB/HSL/CMYK 转换 |
| 进制转换 | 数字进制转换 |
| 罗马数字 | 罗马数字转换器 |
| 坐标转换 | WGS84/GCJ02/BD09 转换 |
| IBAN 验证 | 验证 IBAN 号码 |

**时间与正则:**
| 工具 | 说明 |
|------|------|
| 时间戳 | Unix 时间戳转换 |
| 时区 | 时区转换 |
| Crontab | Cron 表达式解析 |
| 正则测试 | 测试正则表达式 |

**网络工具:**
| 工具 | 说明 |
|------|------|
| API 客户端 | HTTP 请求测试 |
| DNS 查询 | 查询 DNS 记录 |
| 端口扫描 | 扫描开放端口 |
| 路由追踪 | 网络路由追踪 |
| TLS 检测 | 检查 SSL/TLS 配置 |
| WebSocket | WebSocket 测试 |
| URL 解析 | 解析 URL 组件 |
| User Agent | 解析用户代理 |

**其他工具:**
| 工具 | 说明 |
|------|------|
| Chmod 计算 | 权限计算器 |
| Docker 命令 | Docker 命令速查 |
| PDF 工具 | PDF 签名和工具 |
| 预览器 | 预览各种文件类型 |
| AI 聊天 | AI 助手集成 |

---

## Quick Actions | 快捷操作

### Launch Kairoa | 启动 Kairoa

```bash
# Launch Kairoa app (macOS)
open -a Kairoa || open /Applications/Kairoa.app || open ~/Applications/Kairoa.app
```

### Launch with Python | 使用 Python 启动

```bash
python3 << 'EOF'
import subprocess
import os
import sys

locations = [
    "/Applications/Kairoa.app",
    os.path.expanduser("~/Applications/Kairoa.app"),
]

for loc in locations:
    if os.path.exists(loc):
        print(f"🚀 Launching Kairoa from {loc}")
        subprocess.run(['open', loc])
        print("✅ Kairoa launched!")
        sys.exit(0)

print("❌ Kairoa not found. Please install it first.")
EOF
```

---

## Common Calculations | 常用计算

Kairoa is a GUI app without CLI support. For quick results, use these Python helpers while Kairoa is opened for further exploration.

Kairoa 是 GUI 应用，不支持命令行。以下 Python 脚本可快速获得结果，同时打开 Kairoa 供进一步使用。

### Hash Calculation | 哈希计算

**English:**
```bash
python3 << 'EOF'
import hashlib
import subprocess
import os

def calculate_hash(text, algorithm='md5'):
    """Calculate hash of text using specified algorithm."""
    alg = algorithm.lower().replace('-', '')
    if alg not in hashlib.algorithms_available:
        return f"❌ Unsupported algorithm: {algorithm}"
    h = hashlib.new(alg)
    h.update(text.encode('utf-8'))
    return h.hexdigest()

# Example: Calculate MD5 of "hello"
text = "hello"
print(f"📝 Text: {text}")
print(f"MD5:    {calculate_hash(text, 'md5')}")
print(f"SHA-1:  {calculate_hash(text, 'sha1')}")
print(f"SHA-256: {calculate_hash(text, 'sha256')}")
print(f"SHA-512: {calculate_hash(text, 'sha512')}")

# Launch Kairoa for more tools
kairoa_path = "/Applications/Kairoa.app"
if os.path.exists(kairoa_path):
    print("\n🚀 Opening Kairoa for more hash options...")
    subprocess.run(['open', kairoa_path])
EOF
```

**中文:**
```bash
python3 << 'EOF'
import hashlib
import subprocess
import os

def calculate_hash(text, algorithm='md5'):
    """计算文本的哈希值"""
    alg = algorithm.lower().replace('-', '')
    if alg not in hashlib.algorithms_available:
        return f"❌ 不支持的算法: {algorithm}"
    h = hashlib.new(alg)
    h.update(text.encode('utf-8'))
    return h.hexdigest()

# 示例: 计算 "hello" 的 MD5
text = "hello"
print(f"📝 文本: {text}")
print(f"MD5:    {calculate_hash(text, 'md5')}")
print(f"SHA-1:  {calculate_hash(text, 'sha1')}")
print(f"SHA-256: {calculate_hash(text, 'sha256')}")
print(f"SHA-512: {calculate_hash(text, 'sha512')}")

# 打开 Kairoa
kairoa_path = "/Applications/Kairoa.app"
if os.path.exists(kairoa_path):
    print("\n🚀 正在打开 Kairoa...")
    subprocess.run(['open', kairoa_path])
EOF
```

### Base64 Encode/Decode | Base64 编码解码

**English:**
```bash
python3 << 'EOF'
import base64
import subprocess
import os

text = "hello"
print(f"📝 Text: {text}")
print(f"Encoded: {base64.b64encode(text.encode()).decode()}")

# Decode example
encoded = "aGVsbG8="
print(f"\n📝 Encoded: {encoded}")
print(f"Decoded: {base64.b64decode(encoded).decode()}")

# Open Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

**中文:**
```bash
python3 << 'EOF'
import base64
import subprocess
import os

text = "hello"
print(f"📝 文本: {text}")
print(f"编码后: {base64.b64encode(text.encode()).decode()}")

# 解码示例
encoded = "aGVsbG8="
print(f"\n📝 编码: {encoded}")
print(f"解码后: {base64.b64decode(encoded).decode()}")

# 打开 Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

### UUID Generator | UUID 生成器

**English:**
```bash
python3 << 'EOF'
import uuid
import subprocess
import os

print("🎲 Generated UUIDs:")
print(f"UUID v4: {uuid.uuid4()}")
print(f"UUID v4: {uuid.uuid4()}")
print(f"UUID v4: {uuid.uuid4()}")

# Open Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

**中文:**
```bash
python3 << 'EOF'
import uuid
import subprocess
import os

print("🎲 生成的 UUID:")
print(f"UUID v4: {uuid.uuid4()}")
print(f"UUID v4: {uuid.uuid4()}")
print(f"UUID v4: {uuid.uuid4()}")

# 打开 Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

### Timestamp Converter | 时间戳转换

**English:**
```bash
python3 << 'EOF'
import time
from datetime import datetime
import subprocess
import os

now = datetime.now()
ts = int(time.time())

print(f"📅 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Unix timestamp: {ts}")
print(f"ISO format: {now.isoformat()}")

# Convert timestamp to datetime
print(f"\nTimestamp {ts} → {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")

# Open Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

**中文:**
```bash
python3 << 'EOF'
import time
from datetime import datetime
import subprocess
import os

now = datetime.now()
ts = int(time.time())

print(f"📅 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Unix 时间戳: {ts}")
print(f"ISO 格式: {now.isoformat()}")

# 时间戳转日期
print(f"\n时间戳 {ts} → {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")

# 打开 Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

### JSON Format | JSON 格式化

**English:**
```bash
python3 << 'EOF'
import json
import subprocess
import os

# Format JSON
ugly = '{"name":"Kairoa","version":"1.0","tools":["hash","encode","uuid"]}'
pretty = json.dumps(json.loads(ugly), indent=2)
print("📋 Formatted JSON:")
print(pretty)

# Open Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

**中文:**
```bash
python3 << 'EOF'
import json
import subprocess
import os

# 格式化 JSON
ugly = '{"name":"Kairoa","version":"1.0","tools":["hash","encode","uuid"]}'
pretty = json.dumps(json.loads(ugly), indent=2)
print("📋 格式化后的 JSON:")
print(pretty)

# 打开 Kairoa
if os.path.exists("/Applications/Kairoa.app"):
    subprocess.run(['open', "/Applications/Kairoa.app"])
EOF
```

---

### Check if Kairoa is installed | 检查 Kairoa 是否安装

```bash
python3 << 'EOF'
import os

locations = [
    "/Applications/Kairoa.app",
    os.path.expanduser("~/Applications/Kairoa.app"),
]

found = False
for loc in locations:
    if os.path.exists(loc):
        print(f"✅ Kairoa found at: {loc}")
        found = True
        break

if not found:
    print("❌ Kairoa not installed")
    print("\nInstall options:")
    print("  1. Download from official releases")
    print("  2. Build from source: git clone && npm install && npm run tauri build")
EOF
```

---

## Trigger Words | 触发词

**English:**
```
Launch Kairoa, start Kairoa
Open Kairoa hash tool
Open Kairoa QR code
Open Kairoa JSON formatter
Open Kairoa mock generator
Kairoa encoding tools
Kairoa crypto tools
Use Kairoa for hash
Use Kairoa for QR code
```

**中文:**
```
启动 Kairoa, 打开 Kairoa
打开 Kairoa 哈希工具
打开 Kairoa 二维码
打开 Kairoa JSON 格式化
打开 Kairoa Mock 生成器
Kairoa 编码工具
Kairoa 加密工具
用 Kairoa 生成哈希
用 Kairoa 生成二维码
```

---

## Notes | 注意事项

**English:**
- Kairoa is a Tauri-based desktop application
- The skill will open the installed app, not a development server
- If Kairoa is not found, please install it first
- Supports macOS (Windows/Linux paths may vary)

**中文:**
- Kairoa 是基于 Tauri 的桌面应用
- Skill 会打开已安装的应用，而不是开发服务器
- 如果未找到 Kairoa，请先安装
- 支持 macOS (Windows/Linux 路径可能不同)

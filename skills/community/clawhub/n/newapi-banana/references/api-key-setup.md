# API Key 设置指南

## 获取 API Key

1. 联系您的 NewAPI Banana 服务提供商获取 API Key
2. API Key 格式通常为字符串，请妥善保管

## 配置 API Key

### 方法一：通过 OpenClaw 配置文件（推荐）

**Windows 系统：**
配置文件位置：`C:\Users\你的用户名\.openclaw\openclaw.json`

**Linux/Mac 系统：**
配置文件位置：`~/.openclaw/openclaw.json`

**步骤：**
1. 如果 `.openclaw` 目录不存在，先创建它
2. 创建或编辑 `openclaw.json` 文件
3. 添加以下配置（如果文件已存在，合并到现有配置中）：

```json
{
  "skills": {
    "entries": {
      "newapi-banana": {
        "apiKey": "your_api_key_here"
      }
    }
  }
}
```

**Windows PowerShell 快速创建：**
```powershell
# 创建目录（如果不存在）
$configDir = "$env:USERPROFILE\.openclaw"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force
}

# 创建配置文件
$configFile = "$configDir\openclaw.json"
@{
    skills = @{
        entries = @{
            "newapi-banana" = @{
                apiKey = "your_api_key_here"
            }
        }
    }
} | ConvertTo-Json -Depth 10 | Set-Content -Path $configFile -Encoding UTF8
```

### 方法二：通过环境变量

**Windows PowerShell：**
```powershell
$env:NEWAPI_API_KEY = "your_api_key_here"
```

**Windows CMD：**
```cmd
set NEWAPI_API_KEY=your_api_key_here
```

**Linux/Mac：**
```bash
export NEWAPI_API_KEY="your_api_key_here"
```

**永久设置环境变量（Windows）：**
1. 右键"此电脑" → "属性"
2. "高级系统设置" → "环境变量"
3. 在"用户变量"中添加：
   - 变量名：`NEWAPI_API_KEY`
   - 变量值：`your_api_key_here`

### 方法三：在对话中直接提供

您可以在对话中直接提供 API Key，系统会临时使用。例如：
- "我的 API Key 是：sk-xxxxx"
- "设置 API Key：your_key_here"

## 验证 API Key

运行以下命令验证 API Key 是否有效：

```bash
python3 {baseDir}/scripts/newapi-banana.py --check
```

如果配置正确，您会看到：

```json
{
  "status": "ready",
  "key_prefix": "xxxx****",
  "host": "http://nen.baynn.com",
  "message": "API key is valid"
}
```

## 故障排除

### API Key 无效

- 检查 API Key 是否正确复制（注意前后空格）
- 确认 API Key 是否已过期
- 联系服务提供商确认账户状态

### 无法连接

- 检查网络连接
- 确认 API 服务是否正常运行
- 脚本会自动尝试多个备份地址

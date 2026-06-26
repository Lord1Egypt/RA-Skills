# NewAPI Banana - OPENCLAW Skill

支持图片生成的 OPENCLAW SKILLS，包含文生图和图生图功能。

## 🚀 快速开始

### 1. 配置 API Key

#### 方法一：使用配置脚本（最简单）

在正常运行的OPENCLAW中，开启聊天，把你的APIKEY直接发给小龙虾，让他帮你配置好，就可以用了
```

#### 方法二：手动编辑配置文件

1. 打开配置文件：`C:\Users\你的用户名\.openclaw\openclaw.json`
2. 如果文件不存在，创建它并添加：

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

#### 方法三：设置环境变量

在 PowerShell 中：

```powershell
$env:NEWAPI_API_KEY = "your_api_key_here"
```

### 2. 验证配置

```powershell
python3 scripts\newapi-banana.py --check
```

如果配置正确，会显示：

```json
{
  "status": "ready",
  "key_prefix": "xxxx****",
  "host": "http://nen.baynn.com",
  "message": "API key is valid"
}
```

## 📖 使用示例

### 生成图片

```powershell
python3 scripts\newapi-banana.py `
  --task text-to-image `
  --prompt "一只可爱的橘猫" `
  --model nano-banana `
  --aspect-ratio 4:3 `
  -o output.png
```

## 📚 更多文档

- [API Key 设置指南](references/api-key-setup.md)
- [图片生成指南](references/image-generation.md)
- [输出交付指南](references/output-delivery.md)

## 🔧 支持的功能

- ✅ 文生图（Text-to-Image）
- ✅ 图生图（Image-to-Image）

## 📝 支持的模型

### 图片模型
- `nano-banana` - 标准图片生成模型（推荐）
- `nano-banana-2` - 增强版本
- `nano-banana-fast` - 快速生成模型
- `nano-banana-pro` - 图生图编辑模型
- `gemini-3-pro-image-preview` - Gemini Pro 模型

## 🌐 API 地址

- http://nen.baynn.com

## 📞 获取 API Key

请联系您的 NewAPI Banana 服务提供商获取 API Key。

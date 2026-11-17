# HTML to WeChat

将现有 HTML 内容一键发布到微信公众号草稿箱。自动检测微信兼容性，转换内联样式，压缩封面图，上传草稿箱。

## Features

- **HTML 兼容性检测** — 自动检查 style 标签、CSS 变量、script 等微信不支持的元素
- **一键 CSS 转换** — 将 style 标签 CSS 转为内联样式，深色主题自动转浅色
- **封面图自动压缩** — 微信限制 64KB，脚本自动压缩到达标
- **一键发布** — 上传到微信公众号草稿箱，审核后即可发布

## First-Time Setup

### 1. Install Dependencies

```bash
python -m pip install beautifulsoup4 cssutils Pillow requests
```

### 2. Install Companion Skill

```bash
clawhub install anything-to-wechat
```

### 3. Configure WeChat Credentials

1. Log in to https://mp.weixin.qq.com/
2. Go to: 设置与开发 → 基本配置
3. Copy your **AppID** and **AppSecret**
4. Add your server IP to the **IP白名单**

**macOS / Linux:**
```bash
export WECHAT_APP_ID="your_appid"
export WECHAT_APP_SECRET="your_appsecret"
```

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("WECHAT_APP_ID", "your_appid", "User")
[Environment]::SetEnvironmentVariable("WECHAT_APP_SECRET", "your_appsecret", "User")
```

Or the script will prompt you interactively on first run.

## How It Works

```
HTML (file / URL / pasted)
    |
    v
Validate for WeChat (check style tags, CSS vars, size)
    |
    v
convert_for_wechat.py (CSS → inline styles, if needed)
    |
    v
Cover image (ImageGen or user-provided)
    |
    v
compress_image.py (< 64KB)
    |
    v
publish_to_wechat.py --> WeChat Draft Box
    |
    v
Review at mp.weixin.qq.com --> Publish
```

## Quick Start

```
把这个 HTML 文件发布到我的微信公众号
```

Or:

```
C:\path\to\article.html 发到公众号
```

## Scripts

| Script | Description |
|---|---|
| `scripts/compress_image.py` | Compress images to WeChat's 64KB cover limit |

Other scripts from companion skill:
- `anything-to-wechat/scripts/convert_for_wechat.py` — CSS → inline styles
- `anything-to-wechat/scripts/publish_to_wechat.py` — WeChat API publishing

## Configuration

| Variable | Required | Description |
|---|---|---|
| `WECHAT_APP_ID` | Yes | WeChat Official Account AppID (or prompted interactively) |
| `WECHAT_APP_SECRET` | Yes | WeChat Official Account AppSecret (or prompted interactively) |

## License

MIT

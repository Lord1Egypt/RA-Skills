---
name: wechat-article
description: 微信公众号文章抓取工具。将微信公众号文章转换为 Markdown 格式，支持图片本地下载。当用户提到抓取微信公众号文章、提取公众号内容、爬取微信文章时触发。
---

# 微信公众号文章抓取

将微信公众号文章转换为 Markdown 格式，支持图片本地下载。

## 脚本位置

- 主程序：`scripts/main.py`
- MCP Server：`scripts/mcp_server.py`

## 快速使用

```bash
cd ~/.openclaw/workspace/skills/wechat-article
python3 scripts/main.py "文章URL" -o /root/.openclaw/workspace/output
```

## 参数

| 参数 | 说明 |
|------|------|
| `-o DIR` | 输出目录（默认 ./output） |
| `-v` | 调试日志 |
| `--no-images` | 不下载图片，保持远程 URL |
| `--force` | 覆盖已存在文件 |
| `--no-headless` | 显示浏览器（用于处理验证码） |

## 输出结构

```
output/
 └── 文章标题/
     ├── 文章标题.md
     └── images/
         ├── img_001.jpg
         └── ...
```

## 注意事项

1. 验证码：遇到验证页面时加 `--no-headless` 手动处理
2. 反爬：微信有频率限制，建议间隔操作
3. 图片失败：保留远程 URL，可用 `--force` 重试

## 依赖

- camoufox
- markdownify
- beautifulsoup4
- httpx
- aiohttp

---
name: osm-ai-bridge
description: OSM AI Bridge - OpenClaw多AI协作桥接器。通过CDP连接浏览器，支持自动启动、反检测脚本注入、Cookie/LocalStorage访问。实现Ask/Discuss/Verify三种协作模式。
config_paths:
  - ~/.openclaw/ai_bridge
---

# OSM AI Bridge

## 功能

- **CDP连接** - 通过Chrome DevTools Protocol连接浏览器
- **自动启动** - 浏览器未运行时自动启动带调试端口的实例
- **反检测** - 注入脚本隐藏webdriver特征
- **Storage访问** - 访问Cookie和LocalStorage
- **生产级日志** - 完整日志记录到 ~/.openclaw/ai_bridge/ai_bridge.log

## 使用方法

```bash
python scripts/osm_ai_bridge.py "你的问题"
```

## 系统要求

- **Windows** (自动启动功能仅支持 Windows + Edge)
- Linux/Mac 需要手动启动浏览器: `edge --remote-debugging-port=9222`

## 技术实现

### 自动启动浏览器

```python
# 检查CDP端口，如不可用则自动启动Edge
if not await self._check_cdp_available():
    await self._start_browser_with_debugging()
```

### 反检测脚本

```javascript
// 隐藏webdriver
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// 模拟插件
Object.defineProperty(navigator, 'plugins', { get: () => [...] });
```

### Cookie/LocalStorage访问

```python
cookies = await self.context.cookies()
local_storage = await self.page.evaluate('() => { ... }')
```

## 日志

日志文件位置：`~/.openclaw/ai_bridge/ai_bridge.log`

## 限制

- **Windows 仅** - 自动启动功能仅支持 Windows + Edge
- 其他系统需手动启动浏览器并开启调试端口
- 需要 Playwright: `pip install playwright aiohttp`
- 首次使用需在浏览器中手动登录
- 需要依赖: `pip install playwright aiohttp`

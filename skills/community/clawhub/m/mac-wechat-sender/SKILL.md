---
slug: mac-wechat-sender
name: macOS微信发送器
description: macOS 桌面微信自动发送文件/消息。AppleScript + cliclick 驱动，无需浏览器。
---

# macOS微信发送器

给微信联系人自动发送文件和消息，基于 AppleScript + cliclick 桌面自动化。

## 适用平台

- ✅ macOS (AppleScript)
- ❌ Windows (不支持)

## 依赖

```bash
brew install cliclick
# WeChat 桌面版需已登录
```

## 用法

```bash
# 发送文件给默认联系人"老婆"
python3 scripts/skills/wechat-sender/wechat_sender.py --file "output/video/final/小红狗_应美霞你干嘛呢.mp4"

# 发送文件给指定联系人
python3 scripts/skills/wechat-sender/wechat_sender.py --contact "张三" --file "report.pdf"

# 发送文字消息
python3 scripts/skills/wechat-sender/wechat_sender.py --contact "老婆" --message "我到家了"

# 发送到群聊
python3 scripts/skills/wechat-sender/wechat_sender.py --contact "工作群" --message "大家好" --group
```

## 工作流程

1. `activate` — 激活微信窗口 (如未运行则 open -a WeChat)
2. `search_contact` — Cmd+Shift+F 搜索联系人 → 回车打开聊天
3. `send_file` — Finder 选中文件 → Cmd+C → 微信输入框 → Cmd+V → 回车
4. `send_message` — 直接输入文本 → 回车

## 限制

- 依赖屏幕坐标 `cliclick c:600,750` 点击输入框，不同分辨率需调整
- 微信窗口需在可访问区域
- 不支持文件拖拽以外的附件类型 (如图片/视频可直接发送)

## 快捷命令

配置 Claude 快速调用: `/wechat-send`

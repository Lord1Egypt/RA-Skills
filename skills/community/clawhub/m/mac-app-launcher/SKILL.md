---
name: mac-app-launcher
description: >-
  查询和打开 macOS 应用程序。通过关键词搜索已安装的 App，并使用 open 命令启动。
  当用户要求查找、搜索、列出、打开某个 Mac 应用程序时使用。
---

# Mac App Launcher

## 查询应用

使用 `mdfind` 通过 Spotlight 索引搜索应用（最快最全）：

```bash
mdfind "kMDItemKind == 'Application'" -name "<关键词>"
```

如果用户未提供关键词、想浏览所有应用，改用目录列举：

```bash
ls /Applications /Applications/Utilities ~/Applications /System/Applications 2>/dev/null
```

### 搜索策略

1. 优先用 `mdfind`，支持模糊匹配中英文应用名
2. 如果 `mdfind` 无结果，回退到 `ls` + `grep -i` 在常见目录搜索
3. 将匹配结果以列表形式展示给用户，标注完整路径

## 打开应用

找到目标应用后，使用 Shell 工具执行：

```bash
open -a "应用名称"
```

或使用完整路径：

```bash
open "/Applications/XXX.app"
```

## 工作流

1. 用户提出要查找或打开某个应用
2. 用 `mdfind` 搜索匹配的应用
3. 如果有多个匹配结果，列出让用户选择
4. 如果只有一个匹配结果，直接打开
5. 使用 `open` 命令启动应用

## 注意事项

- `open -a` 需要精确的应用名或路径，优先使用 `mdfind` 返回的完整 `.app` 路径
- 系统应用在 `/System/Applications`，第三方在 `/Applications`
- Homebrew cask 应用也在 `/Applications`，但部分命令行工具在 `/opt/homebrew/bin`

---
name: obsidian-sync-syncthing
description: Obsidian 跨平台同步方案（Mac ↔ iPhone），基于 Syncthing 实现零插件、零成本、离线优先的双向同步，支持智能大文件过滤。
author: KyleJia
license: MIT
version: 1.0.0
tags: [obsidian, syncthing, sync, ios, mac, offline-first, knowledge-management]
---

# Obsidian 跨平台同步方案（Mac ↔ iPhone）

> **零插件 · 零成本 · 智能过滤 · 离线优先**

## 方案概述

本方案使用 **Syncthing**（开源 P2P 同步工具）实现 Mac 与 iPhone 之间的 Obsidian vault 双向同步，无需 iCloud、无需 Obsidian Sync 订阅、无需任何 Obsidian 插件。

### 核心亮点

| 特性 | 本方案 | Obsidian Sync | iCloud |
|------|--------|---------------|--------|
| 费用 | **免费** | $4/月 | 免费（5GB） |
| 插件依赖 | **无** | 无 | 无 |
| 智能大文件过滤 | **✅ 支持** | ❌ | ❌ |
| 离线可用 | **✅** | ✅ | ⚠️ 需预同步 |
| 去中心化 | **✅ P2P直连** | ❌ 云端中转 | ❌ Apple服务器 |
| 端到端加密 | **✅** | ✅ | ❌ |
| 跨平台 | **✅ 全平台** | ✅ 全平台 | 仅 Apple |

### 架构图

```
┌─────────────┐         Syncthing (P2P)        ┌─────────────┐
│     Mac     │◄──────────────────────────────►│   iPhone    │
│             │     端到端加密 · 局域网直连      │             │
│  Syncthing  │     无需第三方服务器             │ Möbius Sync │
│  (服务端)   │                                 │  (客户端)   │
│             │                                 │             │
│  Obsidian   │                                 │  Obsidian   │
│  Vault/     │                                 │  本地目录/  │
│  ...        │                                 │  ...        │
└─────────────┘                                 └─────────────┘
```

### 智能大文件过滤

同步时自动排除以下文件，节省手机空间：

- 压缩包：`*.7z`、`*.zip`、`*.rar`
- 视频：`*.mp4`、`*.mov`、`*.avi`
- 大 PPT：`>50MB` 的 `*.pptx` / `*.ppt`

---

## 前置要求

| 设备 | 要求 |
|------|------|
| Mac | macOS 11+，已安装 Syncthing |
| iPhone | iOS 15+，安装 Möbius Sync（App Store 免费） |
| 网络 | 两台设备在同一局域网，或配置远程发现 |

---

## 第一步：Mac 端配置

### 1.1 安装 Syncthing

```bash
# 使用 Homebrew 安装
brew install syncthing

# 启动 Syncthing（后台运行）
brew services start syncthing

# 或前台运行（用于初次配置）
syncthing
```

### 1.2 打开 Web 管理界面

浏览器访问 `http://127.0.0.1:8384`

### 1.3 记录设备 ID

在 Web 界面 → 「操作」→ 「显示 ID」，复制你的设备 ID（稍后 iPhone 端需要）。

### 1.4 配置开机自启

```bash
# macOS 开机自启
brew services start syncthing
```

### 1.5 添加同步文件夹

1. Web 界面 → 「文件夹」→「添加文件夹」
2. **文件夹标签**：`Obsidian Vault`
3. **文件夹路径**：你的 Obsidian vault 路径，例如 `~/Documents/Obsidian Vault`
4. **版本控制**：建议开启，保留最近 5 个版本（防误删）
5. 保存

---

## 第二步：iPhone 端配置

### 2.1 安装 Möbius Sync

App Store 搜索「**Möbius Sync**」，免费下载。

> 注意：免费版限制同步 20MB。如 vault 超过 20MB，需内购买断（¥38）。

### 2.2 添加设备（配对 Mac）

1. 打开 Möbius Sync → 「Devices」→「+」
2. 输入 Mac 的设备 ID（1.3 步骤中记录的）
3. 设备名填你的 Mac 名称
4. 保存，等待配对

### 2.3 Mac 上确认配对

回到 Mac 的 Syncthing Web 界面（`http://127.0.0.1:8384`），会看到 iPhone 的配对请求，点击「添加设备」。

### 2.4 添加同步文件夹

**关键步骤：将同步目标指向 Obsidian 的本地目录**

1. Möbius Sync → 「Folders」→「+」→「Add Folder」
2. **Folder Label**：`Obsidian Vault`
3. **Folder Path**：选择 iPhone 上 Obsidian 的本地目录
   - 路径：「文件」App →「我的 iPhone」→「Obsidian」→「Obsidian Vault」
4. **Shared With**：勾选你的 Mac 设备
5. 保存

### 2.5 Mac 上确认共享

回到 Mac 的 Syncthing Web 界面，确认 iPhone 的文件夹共享请求。

### 2.6 确认同步状态

- iPhone 上 Möbiing Sync 显示文件夹状态为 **Running**
- Obsidian App 打开即可看到所有笔记

---

## 第三步：智能大文件过滤

### 3.1 创建排除规则脚本

在 Mac 上创建同步脚本，自动排除大文件：

```python
#!/usr/bin/env python3
"""同步 Obsidian Vault 到 iCloud/Möbius，排除大文件"""
import subprocess, os, tempfile

SRC = "~/Documents/Obsidian Vault"  # 替换为你的 vault 路径
DST = "~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault"  # 替换为目标路径

# 找出 >50MB 的 PPT 文件
result = subprocess.run(
    ["find", os.path.expanduser(SRC), "-type", "f",
     "(", "-name", "*.pptx", "-o", "-name", "*.ppt", ")", "-size", "+50M"],
    capture_output=True, text=True
)
big_ppts = result.stdout.strip().split("\n") if result.stdout.strip() else []

# 生成 exclude-from 文件
exclude_tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
exclude_tmp.write("*.7z\n*.zip\n*.rar\n*.mp4\n*.mov\n*.avi\n")
for f in big_ppts:
    if f:
        rel = f.replace(os.path.expanduser(SRC) + "/", "")
        exclude_tmp.write(rel + "\n")
exclude_tmp.close()

# rsync 同步
cmd = ["rsync", "-av", "--update", f"--exclude-from={exclude_tmp.name}",
       f"{os.path.expanduser(SRC)}/", f"{os.path.expanduser(DST)}/"]
subprocess.run(cmd)
os.unlink(exclude_tmp.name)

print(f"✅ 同步完成，已排除 {len(big_ppts)} 个大PPT文件")
```

### 3.2 运行脚本

```bash
python3 sync-obsidian.py
```

---

## 第四步：配置优化

### 4.1 Syncthing Web UI 密码保护

```bash
# 生成密码哈希
syncthing generate --password

# 编辑配置文件（~/.config/syncthing/config.xml）
# 找到 <gui> 标签，添加：
# <authenticationUser>admin</authenticationUser>
# <authenticationPassword>哈希值</authenticationPassword>

# 重启 Syncthing
brew services restart syncthing
```

### 4.2 仅局域网同步（更省电）

Web 界面 → 「设置」→ 「连接」→「本地发现」开启，「全局发现」关闭。这样设备只在同局域网时同步。

### 4.3 版本控制

Web 界面 → 文件夹设置 →「版本控制」→ 选择「简易文件版本控制」，建议保留最近 5-10 个版本。

---

## 常见问题

### Q: iPhone 上文件夹状态显示 Stopped

**A**: 检查 Syncthing 引擎是否启用。Möbius Sync → 设置 → 确认 Syncthing 服务为 Running 状态。

### Q: 免费版 20MB 限制

**A**: Obsidian vault 超过 20MB 时，Möbius Sync 免费版会禁用同步。需内购买断（¥38，一次性）。

### Q: 同步延迟或不自动同步

**A**:
1. 确认两台设备在同一局域网
2. 检查 iPhone 是否允许 Möbius Sync 后台运行（设置 → 通用 → 后台 App 刷新）
3. 手动触发：Möbius Sync → 文件夹 → Rescan

### Q: 冲突文件处理

**A**: Syncthing 会保留冲突版本（文件名加 `.sync-conflict` 后缀），不会覆盖。建议开启版本控制以防万一。

### Q: Obsidian iPhone 打开的是空 vault

**A**: 确认 Möbius Sync 的同步路径指向的是 Obsidian 的本地目录（「我的 iPhone」→「Obsidian」→「Obsidian Vault」），而不是其他目录。

### Q: 如何排除特定大文件

**A**: 在同步脚本的 exclude 列表中添加规则，如 `*.psd`（设计文件）、`*.ai` 等。

---

## 技术原理

### 为什么不用 Obsidian 插件方案？

现有方案（如 GitHub 上的 obsidian-syncthing-integration）需要在 Obsidian 内安装 Syncthing 插件，存在以下问题：

1. **依赖插件维护** — 插件停止维护则方案失效
2. **增加 Obsidian 负担** — 插件运行占用 Obsidian 资源
3. **兼容性风险** — Obsidian 更新可能导致插件失效

本方案在**文件系统层**同步，与 Obsidian 完全解耦，更稳定可靠。

### 为什么不用 iCloud？

1. iCloud 同步有延迟（尤其是大文件）
2. 免费空间只有 5GB
3. 不支持智能文件过滤
4. 依赖 Apple 服务器，离线不可用

---

## License

MIT License — 作者 KyleJia

Copyright (c) 2026 KyleJia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

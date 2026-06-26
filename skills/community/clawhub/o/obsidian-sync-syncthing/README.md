# 🔄 Obsidian 跨平台同步方案（Mac ↔ iPhone）

> **零插件 · 零成本 · 智能过滤 · 离线优先**

[English](./README.en.md) | [Hermes Skill](./SKILL.md) | [English Skill](./SKILL.en.md)

## 方案简介

使用 **Syncthing**（开源 P2P 同步工具）实现 Mac 与 iPhone 之间的 Obsidian vault 双向同步。

- ✅ **零成本** — 免费开源，无需订阅
- ✅ **零插件** — 文件系统级同步，与 Obsidian 完全解耦
- ✅ **智能过滤** — 自动排除 >50MB PPT、视频、压缩包
- ✅ **离线优先** — P2P 直连，无需云端中转
- ✅ **端到端加密** — 数据只在你的设备之间传输

## 架构

```
┌─────────────┐         Syncthing (P2P)        ┌─────────────┐
│     Mac     │◄──────────────────────────────►│   iPhone    │
│  Syncthing  │     端到端加密 · 局域网直连      │ Möbius Sync │
│  Obsidian   │                                 │  Obsidian   │
│  Vault/     │                                 │  本地目录/  │
└─────────────┘                                 └─────────────┘
```

## 快速开始

### Mac 端

```bash
brew install syncthing
brew services start syncthing
# 打开 http://127.0.0.1:8384 添加同步文件夹
```

### iPhone 端

1. App Store 安装 **Möbius Sync**
2. 添加 Mac 设备 ID（在 Syncthing Web UI → 操作 → 显示 ID 中查看）
3. 添加同步文件夹，路径指向 `Files → On My iPhone → Obsidian → Obsidian Vault`

> 免费版限制 20MB，大 vault 需内购买断（¥38 / ~$5.30）。

详细步骤见 [SKILL.md](./SKILL.md)（中文完整教程）。

## 与现有方案对比

| 特性 | 本方案 | Obsidian Sync | iCloud | GitHub 插件方案 |
|------|--------|---------------|--------|----------------|
| 费用 | **免费** | $4/月 | 免费(5GB) | 免费 |
| 插件依赖 | **无** | 无 | 无 | 需安装插件 |
| 智能大文件过滤 | **✅** | ❌ | ❌ | ❌ |
| 离线可用 | **✅** | ✅ | ⚠️ | ✅ |
| 去中心化 | **✅ P2P** | ❌ | ❌ | ❌ |
| 维护风险 | **低** | 低 | 低 | 高（插件维护） |

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 中文完整教程（Hermes Skill 格式） |
| `SKILL.en.md` | 英文完整教程 |
| `README.md` | 本文件 |

## License

[MIT](./LICENSE) — KyleJia

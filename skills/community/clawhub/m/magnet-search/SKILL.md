---
name: magnet-search
version: 2.0.0
description: "搜索电影磁力下载链接。接入真实磁力搜索引擎 API (ThePirateBay, Nyaa等)，返回高质量的种子链接。用于合法的个人学习和研究目的。"
author: HomeClaw
keywords: [magnet, torrent, movie, search, download]
---

# Magnet Search 🔍 v2.0

接入真实磁力搜索引擎 API 的电影磁力链接搜索工具。

## ⚠️ 免责声明

**本工具仅供个人学习和研究使用**
- 请遵守当地法律法规
- 尊重版权，支持正版
- 用户需自行承担使用风险

## ✨ 功能特点

- ✅ 接入真实 API (ThePirateBay, Nyaa)
- ✅ 自动提取视频质量信息 (1080p/720p/4K)
- ✅ 按种子健康度排序
- ✅ 支持 JSON 输出
- ✅ 多源搜索，自动去重
- ✅ 内置免责声明

## 🚀 使用方法

### 命令行

```bash
# 搜索电影
python3 magnet-search.py "电影名称"

# 限制结果数量
python3 magnet-search.py "电影名称" --limit 10

# JSON 输出
python3 magnet-search.py "电影名称" --json

# 降低种子数阈值（更多结果）
python3 magnet-search.py "电影名称" --min-seeders 1
```

### 作为 Skill 使用

在 OpenClaw 中直接请求：
- "搜索电影《XXX》的磁力链接"
- "帮我找《XXX》的下载资源"

## 🔍 数据源

| 源 | 类型 | 状态 |
|----|------|------|
| ThePirateBay (apibay.org) | 电影/软件/其他 | ✅ 可用 |
| Nyaa | 动漫/日剧 | ✅ 可用 |
| TorrentGalaxy | 电影/剧集 | ⏳ 待完善 |
| 1337x | 综合 | ⏳ 需绕过 CF |

## 📋 输出格式

```
🔍 正在搜索: 电影名称
============================================================
  搜索 ThePirateBay...
  搜索 Nyaa...

✅ 找到 5 个结果:

1. [电影名称 2024 1080p BluRay]
   🎬 质量: 1080p
   💾 大小: 2.50 GB
   🌱 种子: 150 | 🧲 下载: 75
   📅 上传: 2024-03-15
   🔗 磁力链接:
      magnet:?xt=urn:btih:...
   📡 来源: TPB

2. ...
```

## 🛠️ 相关工具

- `transmission-cli` - 命令行 BT 客户端
- `aria2c` - 支持磁力链接的下载工具
- `qbittorrent` - 带 Web UI 的 BT 客户端

## 📝 技术说明

- 使用 `apibay.org` API (TPB 镜像)
- 使用 Nyaa RSS API
- 自动处理 SSL 证书验证
- 支持中文搜索（自动 URL 编码）

## ⚡ 故障排除

**无结果？**
- 尝试使用英文名称搜索
- 降低 `--min-seeders` 阈值
- 检查网络连接

**连接超时？**
- 某些源可能需要代理
- 增加 `--timeout` 参数（默认 15 秒）

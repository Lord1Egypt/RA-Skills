---
name: movie-monitor
description: 电影监控下载自动化技能。自动从6v电影站抓取新片、添加到115离线下载、复制到本地NAS并重命名。支持IMDb/豆瓣双评分过滤。触发场景：用户要求运行电影下载任务、检查监控状态、修复下载问题、或对电影pipeline做任何调整。
---

# Movie Monitor Skill

电影自动化监控下载 pipeline，支持 6v520 电影站 → 115离线下载 → NAS 存储。

## 架构

```
6v520 列表页 ──抓取──> movie_pipeline.py --mode=monitor ──添加──> 115离线下载
                                              │
                          copy_and_rename_movies.py <──复制── 115挂载目录
                                              │
                                           NAS存储
                                              │
                        复制完成后自动重命名115云端文件夹及视频文件
```

## 定时任务

| 时间 | 任务 | 类型 |
|------|------|------|
| 每天 20:00 | 抓取新片并添加到115离线下载 | agentTurn + isolated |
| 每天 21:00 | 从115挂载目录复制到NAS并重命名 | agentTurn + isolated |

cron 任务使用 `agentTurn + isolated` 类型，在独立 session 中真正执行 shell，不会遗漏。

## 核心脚本

| 脚本 | 用途 |
|------|------|
| `movie_pipeline.py` | 主入口，mode=monitor 只抓取+添加115，mode=download 只下载 |
| `movie_monitor_simple.py` | 抓取电影列表、提取评分、添加到115 |
| `copy_and_rename_movies.py` | 从115挂载目录复制到NAS并重命名，复制完成后自动重命名115云端文件夹和文件 |
| `client_115.py` | 115 API 客户端（Cookie：`~/.openclaw/scripts/movie-monitor/115_cookie_manual.json`） |
| `download_from_115.py` | 115下载到本地逻辑 |
| `config.py` | 配置（源目录、目标目录、Cookie路径等） |
| `cleanup_and_rename.py` | 批量清理115云端和本地NAS的垃圾后缀目录/文件名（电影港 dygang、6v电影、地址发布页等），修复本地目录和云端文件重命名 |

## 115 重命名脚本

`~/.openclaw/scripts/115-renamer/115.js`（Node.js）

**重要**：重命名脚本使用独立 Cookie（`~/.openclaw/scripts/115-renamer/cookie.json`），需要与 movie-monitor 的 cookie 保持同步更新。

```bash
# 列出云下载目录
node 115.js ls <cid>

# 重命名文件/文件夹
node 115.js rename "<旧名>" "<新名>" <cid>
```

## 使用方式

### 抓取新片并添加到115
```bash
python3 movie_pipeline.py --mode=monitor
```

### 从115复制到NAS并重命名
```bash
python3 copy_and_rename_movies.py
```

### 清理115云端和本地NAS的垃圾目录/文件名
```bash
python3 cleanup_and_rename.py
```
自动去除垃圾后缀（电影港 dygang、6v电影、地址发布页等），同时修复本地目录和云端文件。

### 完整流程
```bash
python3 movie_pipeline.py --mode=full
```

### 清理115云端脏名（批量重命名）
```bash
python3 batch_rename_115_cloud.py
```

## 配置

```python
# cookie 文件（两个脚本共用同一个）
cookie_file = "~/.openclaw/scripts/movie-monitor/115_cookie_manual.json"
renamer_cookie = "~/.openclaw/scripts/115-renamer/cookie.json"
# 两者需保持同步！

# 源目录：115挂载的云下载目录
source_dir = "/mnt/public/CloudDrive/115open/云下载"

# 目标目录：NAS本地存储
target_dir = "/mnt/media/115"
```

## 评分过滤

- IMDb 或 豆瓣评分 ≥ 6.0 才下载
- 过滤正则：`r'豆瓣评分[：:\s]*([\d.]+)'` 和 `r'IMDb评分[：:\s]*([\d.]+)'`
- **注意**：页面格式为 `◎豆瓣评分:　7.2`（无 `/10`），注意不要写错正则

## 复制重命名规则（v1.3.1 中点号·修复）

复制到 NAS 时自动重命名：

| 类型 | 命名格式 |
|------|----------|
| 单部电影 | `电影名(年份).mkv` |
| 多集剧集 | `电影名(年份)S01E01.mp4`、`电影名(年份)S01E02.mp4` ... |

**中点号 `·` 处理说明**：源目录名中的中点号（如 `杰克·莱恩`）在清理后会转换为空格，但在去重匹配时，`杰克 莱恩` 和 `杰克·莱恩` 会被视为同一电影。复制后的目录名/文件名遵循源目录的实际命名。

## 历史版本

### v1.3.1
- 修复中点号 `·` (U+00B7) 被错误处理的 BUG：之前 `·` 在正则字符类中被替换为空，导致 `杰克·莱恩` 变成 `杰克 莱恩`。现在 `·` 从正则字符类中移除，改为显式 `.replace('·', ' ')` 处理，避免与去重匹配逻辑冲突。涉及 `copy_and_rename_movies.py`、`cleanup_and_rename.py`、`batch_rename_movies.py`、`batch_rename_115_cloud.py`。

### v1.3.0
- 115 文件重命名改为调用 Node.js 脚本（`~/.openclaw/scripts/115-renamer/115.js`），支持文件夹和文件双重重命名
- TMDB 元数据刮削加入中文语言优先
- 修复集数识别支持 `Kimetsu no Yaiba - 56` 格式
- 115 离线下载添加显示进度

### v1.2.0
- 从源目录复制文件到目标目录，复制完成后自动重命名 115 云端文件夹和视频文件

## 去重规则

检查三个目录：NAS电影目录、NAS 115目录、媒体预处理目录，任意一个存在同名电影即跳过。

超过72小时未修改的目录自动跳过，减少无效遍历。

## 依赖

```
requests
beautifulsoup4
```

## 注意事项

- 115 Cookie 需保存在 `115_cookie_manual.json`（JSON格式，非 cookies.txt）
- 两个 cookie 文件（movie-monitor 和 115-renamer）必须同步更新，否则云端重命名会失败
- 云下载目录 CID：`1870455255659183041`
- TMDB 图片下载可配置 `image_proxy`（默认 `http://127.0.0.1:7890`）
- 复制任务独立运行，不会干扰监控任务
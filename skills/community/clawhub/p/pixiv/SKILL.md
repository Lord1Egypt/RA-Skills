---
name: pixiv-skill
description: Pixiv 抓榜、搜索、元信息缓存、按需下载与互动操作技能。用于在不自动登录的前提下，通过 config.yaml 的 Cookie 鉴权执行：排行榜抓取、关键词搜索、作品详情/下载、画师监控、点赞收藏关注。优先先缓存元信息，按需再下载图片或回传直链。
---

# Pixiv Skill（Cookie 鉴权）

## 1) 鉴权与配置

仅支持 Cookie 鉴权（已移除自动登录流程）。

`config.yaml` 最小示例：

```yaml
pixiv:
  cookie: "PHPSESSID=你的值;"
  proxy: ""
  download_dir: "./downloads"
  r: false
  auto_download: false

monitor:
  interval: 3600
  notify: true
```

> 建议保持 `auto_download: false`，先拿元信息，再按需下载。

---

## 2) 脚本职责（给 AI 的快速路由）

### `scripts/pixiv.py`（主入口，优先使用）
- 负责：抓榜、搜索、缓存、下载、互动、监控
- 适用：绝大多数任务

### `scripts/latest_rank.py`（轻量榜单脚本）
- 负责：快速抓取榜单并保存 JSON（独立脚本）
- 适用：只想快速验证榜单接口或导出榜单数据

### `scripts/get_rank.py`（旧兼容脚本）
- 负责：榜单抓取/下载的旧流程
- 适用：兼容历史调用；新任务优先 `scripts/pixiv.py rank`

---

## 3) `scripts/pixiv.py` 命令说明

## 3.1 状态检查
```bash
python3 scripts/pixiv.py status
```
- 用途：检查当前是否有可用鉴权状态。

## 3.2 排行榜抓取（默认只缓存，不下载）
```bash
python3 scripts/pixiv.py rank --type day --lookback 2
```
常用参数：
- `--type`: `day|week|month|daily|weekly|monthly|rookie|original`
- `--lookback`: 未出当日榜时回退天数
- `--date YYYYMMDD`: 指定榜单日期
- `--download`: 显式下载图片（否则仅缓存元信息）

输出行为：
- 将榜单元信息写入 `downloads/search_cache.json`
- 字段包含：`id/title/author/description/tags/likes/views/updated_at/image_url/source`

## 3.3 搜索（默认只缓存，不下载）
```bash
python3 scripts/pixiv.py search --keyword "初音ミク"
```
常用参数：
- `--page` 页码
- `--order`: `popular_desc|date_desc|date_asc`
- `--download`: 显式下载搜索结果图片

输出行为：
- 将搜索元信息写入 `downloads/search_cache.json`

## 3.4 读取缓存（给用户展示/二次筛选）
```bash
python3 scripts/pixiv.py cache
python3 scripts/pixiv.py cache --id 142223607
```
- 用途：把最近一次 rank/search 的元信息结构化输出给用户。

## 3.5 下载指定作品
```bash
python3 scripts/pixiv.py download --id 12345678
```
- 用途：按作品 ID 下载原图（多图自动 `p0/p1...`）。

## 3.6 互动操作
```bash
python3 scripts/pixiv.py like --id 12345678
python3 scripts/pixiv.py follow --uid 87654321
```
- 用途：点赞/收藏作品、关注画师。

## 3.7 画师监控
```bash
python3 scripts/pixiv.py monitor --uid 87654321 --interval 3600
```
- 用途：定时检测画师新作，可配合下载。

---

## 4) 推荐工作流（AI 执行顺序）

1. 先跑 `status`，确认鉴权状态。  
2. 用 `rank` 或 `search` 拿元信息并缓存（默认不下载）。  
3. 用 `cache` 输出用户关心字段（标题、作者、直链、热度等）。  
4. 仅在用户明确要图时再：
   - 直接给 `image_url`，或
   - 用 `download` / `--download` 落盘后发送本地图片。

---

## 5) 常见问题处理

- **403 / 图片直链打不开**：pximg 防盗链，直接外链可能失败。优先本地下载后发送。  
- **当天日榜 404**：正常，使用 `--lookback` 自动回退最近可用日期。  
- **鉴权失效**：更新 `config.yaml` 里的 `cookie` 后重试。  

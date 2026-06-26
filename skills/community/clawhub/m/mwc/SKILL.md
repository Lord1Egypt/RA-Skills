---
name: mac-wallpaper-changer
description: >
  自动更换 Mac 壁纸、壁纸智能推荐与偏好学习。凡涉及壁纸相关操作，都应优先使用此技能：换壁纸、更换桌面背景、
  Mac wallpaper、自动换壁纸（cron/定时任务）、按关键词搜索壁纸（如"上海夜景"、"mountain sunset"）、
  壁纸评分与喜好统计、壁纸推荐、位置配置。支持 Bing 每日精选 / Unsplash / Picsum 多图源，
  支持本地图片、URL 直接设置，兼容 macOS Tahoe（26+）。
---

# Mac 壁纸随心换

自动为 macOS 更换高质量壁纸，通过评分学习偏好并智能推荐。

## 环境要求

- macOS
- uv（用于运行 Python 脚本）

## 脚本一览

| 脚本                    | 作用                    |
| ----------------------- | ----------------------- |
| `scripts/change.py`     | 换壁纸                  |
| `scripts/recommend.py`  | 推荐壁纸                |
| `scripts/preference.py` | 偏好管理（评分 + 统计） |
| `scripts/loc.py`        | 位置配置                |
| `scripts/daily.py`      | 每日自动（cron 用）     |

## 图源优先级

**Unsplash → Bing → Picsum**（可用 `--source` 强制指定）

Unsplash 画质更高且支持主题搜索，始终作为首选；Bing 每日精选作为兜底；Picsum 为最终保底。

## 核心命令

```bash
# 换壁纸（Unsplash 随机高清图）
uv run scripts/change.py
# 换壁纸（Unsplash 主题搜索）
uv run scripts/change.py --query "Shanghai rain"
uv run scripts/change.py --category mountain --file ~/Pictures/x.jpg

# 偏好管理（无参数=列出评分）
uv run scripts/preference.py
uv run scripts/preference.py add              # 对当前壁纸评分
uv run scripts/preference.py add path/to.jpg  # 对指定文件评分
uv run scripts/preference.py set 3 9          # 第 3 条改为 9 分
uv run scripts/preference.py del 5            # 删除第 5 条
uv run scripts/preference.py stats            # 完整统计报告

# 推荐壁纸
uv run scripts/recommend.py
uv run scripts/recommend.py -y   # 自动应用
uv run scripts/recommend.py -n   # 仅显示

# 位置
uv run scripts/loc.py
uv run scripts/loc.py --set-location "北京"
```

## 数据存储

`~/wallpaper-daily/`：`YYYY-MM-DD/` 壁纸、`preferences.parquet` 评分、`logs/`

## Cron

```bash
30 10 * * * cd /path/to/mac-wallpaper-changer && uv run scripts/change.py
```

## References & Assets

| 路径                                    | 说明                                 |
| --------------------------------------- | ------------------------------------ |
| `references/wallpaper-sources.md`       | 壁纸源配置（Bing/Unsplash/Picsum）   |
| `references/embedding-config.md`        | Embedding 配置 Schema 与提供商说明   |
| `assets/embedding-config.template.json` | Embedding 配置模板（高级智能推荐用） |

高级智能推荐（规划）：基于 embedding 的语义相似度推荐，复制 `assets/embedding-config.template.json` 并填入 `api_key` 等。

## 故障排查

- **壁纸不生效**：脚本已处理 Tahoe 26+，使用 killall WallpaperAgent
- **未刷新**：系统设置 > 墙纸 > 在所有空间中显示
- **日志**：`tail -f ~/wallpaper-daily/logs/change-*.log`

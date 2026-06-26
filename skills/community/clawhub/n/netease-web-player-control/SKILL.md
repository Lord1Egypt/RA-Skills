---
name: netease-web-player-control
description: Control NetEase Cloud Music Web in a browser. Use to (1) search and play a song by keyword, preferably artist + title, or (2) open My Music and play one of the user's own created playlists by keyword.
---

# 网易云音乐网页版控制 / NetEase Cloud Music Web Control

中文：
在浏览器中控制网易云音乐网页版。支持两类操作：
- 搜歌播放
- 我的音乐歌单播放

建议：搜歌时优先使用“歌手 + 歌名”。

English:
Control NetEase Cloud Music Web in a browser. Supports two actions:
- song search playback
- My Music playlist playback

Recommendation: prefer artist + title for song search.

## Trigger phrases

搜歌：
- `搜歌 ...`
- `搜索 ...`
- `播放歌曲 ...`
- `找歌 ...`

歌单：
- `歌单 ...`
- `我的歌单 ...`
- `播放我的歌单 ...`
- `我创建的歌单 ...`

## Behavior rules

- 默认先检查 **我的音乐 → 创建的歌单**；无明确匹配时再走搜歌。
- 搜歌优先匹配 **歌手 + 歌名**，短歌名歧义时先确认，不乱播。
- 仅控制网页版；不处理桌面客户端、下载、逆向或批量抓取。
- 我的歌单模式要求网页已登录。
- 歌曲页播放时，避免误点 **播放mv** 或 **去客户端播放**。
- 点击播放后不要立刻判失败；先短暂等待，再复查底部播放器。
- 只有底部播放器真的切到目标歌曲时，才报告“已开始播放”。
- 如果失败，要明确说明卡在哪一步。

## Preferred examples

- `搜歌 王心凌 爱你`
- `搜歌 王心凌 第一次爱的人`
- `歌单 游鸿明`
- `我的歌单 王心凌`

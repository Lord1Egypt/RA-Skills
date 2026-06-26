# music-downloader 多源音乐下载技能

支持从多个音乐平台搜索并下载MP3文件。

## 功能

- **多源搜索** - 同时从10个音乐平台搜索歌曲
- **自动下载** - 获取播放链接并下载MP3文件
- **智能切换** - 一个音源失败自动切换到下一个
- **防盗链绕过** - 自动处理各平台的Referer

## 使用方式

```bash
# 命令行使用
python3 /root/.openclaw/workspace/skills/music-downloader/music_downloader.py "歌曲名"
python3 /root/.openclaw/workspace/skills/music-downloader/music_downloader.py "周杰伦 晴天"
python3 /root/.openclaw/workspace/skills/music-downloader/music_downloader.py "五月天 伤心的人别听慢歌"
```

## 支持的音源 (10个)

| 音源 | 平台 | 优先级 |
|------|------|--------|
| thttt.com | 好听音乐网（酷我源） | 1 |
| kugou.com | 酷狗音乐 | 2 |
| kuwo.cn | 酷我音乐 | 3 |
| netease | 网易云音乐 | 4 |
| qq | QQ音乐 | 5 |
| gequbao.com | 歌曲宝 | 6 |
| 5nd.com | 5nd音乐网 | 7 |
| 1ting.com | 一听音乐 | 8 |
| 9ku.com | 九酷音乐 | 9 |
| musicenc.com | MusicEnc | 10 |

## 工作流程

1. **搜索阶段** - 同时向所有可用音源发送搜索请求
2. **排序** - 按音源优先级整理结果
3. **获取链接** - 调用各平台API获取播放URL
4. **下载** - 使用正确的Referer绕过防盗链
5. **失败重试** - 下载失败自动尝试下一首

## 输出

- 下载成功：返回文件路径，如 `/tmp/music/周杰伦_晴天.mp3`
- 下载失败：返回错误信息

## 注意事项

- 部分平台需要SSL绕过（已自动处理）
- 酷我CDN需要特定的Referer头
- 下载的MP3文件保存在 `/tmp/music/` 目录
- 文件名格式：`歌手_歌名.mp3`

## 依赖

- Python3
- requests 库
- 网络访问权限

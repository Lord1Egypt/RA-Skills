# Music Player Skill - Windows 音乐播放技能

支持 Windows 系统的音乐搜索、下载和播放技能。基于 go-music-api 和多个音乐源。

## 功能特性

- 🔍 **多源搜索** - 支持网易云音乐等多个 API 源
- 📥 **高清下载** - 自动获取最佳音质版本
- 🎧 **本地播放** - 调用 Windows 默认播放器
- 📝 **元数据嵌入** - 支持 ID3 标签（歌名、歌手、专辑、封面）
- 🎵 **批量下载** - 支持下载多个版本

## 快速开始

### 1. 安装依赖

```bash
pip install requests mutagen python-pptx
```

### 2. 搜索并下载音乐

```bash
# 基础下载
python download.py "歌曲名" "保存路径.mp3"

# 使用 go-music-api 源（推荐，音质更好）
python download_go_api.py

# 下载多个版本
python download_versions.py
```

### 3. 播放音乐

```bash
python play_music.py "歌曲路径.mp3"
```

### 4. 嵌入元数据

```bash
python embed_metadata.py "歌曲.mp3" "歌名" "歌手" "专辑" "封面.jpg"
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `download.py` | 基础下载脚本（网易云 API） |
| `download_go_api.py` | 使用 go-music-api 源（推荐） |
| `download_versions.py` | 下载多个版本 |
| `search_and_download.py` | 搜索并下载（旧版） |
| `play_music.py` | 播放本地音乐 |
| `embed_metadata.py` | 嵌入 ID3 元数据 |
| `SKILL.md` | 技能说明文档 |

## 使用示例

### 示例 1：下载刘德华的《中国人》

```bash
python download_go_api.py "刘德华 中国人" "C:\\music\\刘德华 - 中国人.mp3"
```

### 示例 2：下载 Enya 的《One by One》

```bash
python download.py "One by One Enya" "C:\\music\\Enya_One_by_One.mp3"
```

### 示例 3：播放下载的音乐

```bash
python play_music.py "C:\\music\\Enya_One_by_One.mp3"
```

## API 源

技能支持以下音乐 API 源：

1. **网易云音乐** - 基础源，稳定可靠
2. **go-music-api** - 开源项目，音质更好
3. **UOMG API** - 备用源

## 输出目录

默认下载到：`C:\Users\Administrator\.openclaw\workspace\music\`

## 注意事项

- ⚠️ 需要 Python 3.7+
- ⚠️ 需要网络连接来搜索和下载音乐
- ⚠️ 下载的音乐仅供个人学习使用
- ⚠️ 部分 API 可能需要代理访问

## 故障排除

### 下载失败

1. 检查网络连接
2. 尝试切换 API 源（使用 `download_go_api.py`）
3. 检查歌曲名称是否正确

### 无法播放

1. 检查文件是否完整（文件大小 > 1MB）
2. 尝试使用其他播放器打开
3. 重新下载其他版本

### 元数据嵌入失败

1. 确保安装了 mutagen：`pip install mutagen`
2. 检查文件路径是否正确
3. 确保 MP3 文件未被占用

## 更新日志

### v1.1.0 (2026-03-24)
- ✅ 添加 go-music-api 支持
- ✅ 优化音质选择
- ✅ 添加多版本下载
- ✅ 改进错误处理

### v1.0.0 (2026-03-24)
- ✅ 初始版本发布
- ✅ 支持网易云音乐 API
- ✅ 基础搜索和下载功能
- ✅ 本地播放支持

## 许可证

本技能仅供学习交流使用，请勿用于商业用途。

## 支持

如有问题，请提交 Issue 或联系作者。

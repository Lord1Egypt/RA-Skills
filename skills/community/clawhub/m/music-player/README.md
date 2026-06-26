# Music Player Skill for Windows

🎵 支持 Windows 系统的音乐搜索、下载和播放技能

## 快速安装

```bash
npx clawhub@latest install music-player
```

或者手动克隆：

```bash
git clone <repo-url> music-player
cd music-player
pip install requests mutagen
```

## 使用方法

### 下载音乐

```bash
python download.py "歌曲名" "保存路径.mp3"
```

### 播放音乐

```bash
python play_music.py "歌曲路径.mp3"
```

## 功能

- 🔍 多源搜索（网易云、go-music-api）
- 📥 高清音质下载
- 🎧 本地播放
- 📝 ID3 元数据嵌入

## 依赖

- Python 3.7+
- requests
- mutagen

## 示例

```bash
# 下载周杰伦的稻香
python download.py "稻香 周杰伦" "C:\\music\\daoxiang.mp3"

# 下载 Enya 的 One by One
python download.py "One by One Enya" "C:\\music\\enya.mp3"
```

## 文件说明

| 文件 | 说明 |
|------|------|
| download.py | 主下载脚本（推荐） |
| download_go_api.py | 使用 go-music-api 源 |
| play_music.py | 播放器 |
| embed_metadata.py | 元数据编辑器 |

## 注意事项

- 下载的音乐仅供个人学习使用
- 需要网络连接
- Windows 系统专用

## 更新日志

- v1.1.0: 添加 go-music-api 支持，优化音质
- v1.0.0: 初始版本

## License

MIT

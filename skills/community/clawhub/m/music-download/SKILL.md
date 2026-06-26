# 音乐下载技能

## 功能说明
从网易云音乐等平台下载 MP3 歌曲文件，支持高清音质。

## 使用工具
- **yt-dlp**（首选）：支持高清音质下载，平台更多
- **you-get**（备用）：传统下载工具

## 安装方法
```bash
pip install --break-system-packages yt-dlp
```

## 使用方法

### 方式一：直接下载（推荐）
```bash
# 输入：歌曲页面URL
yt-dlp -x --audio-format mp3 -o /保存路径 "%(title)s.%(ext)s" "URL"
```

**示例：**
```bash
# 下载网易云音乐《平凡世界的不凡》
yt-dlp -x --audio-format mp3 -o "/home/liangbing/Music/%(title)s.%(ext)s" "https://music.163.com/song?id=2047069187"
```

### 方式二：下载最高音质（不转换格式）
```bash
yt-dlp -o "/保存路径/%(title)s.%(ext)s" "https://music.163.com/song?id=歌曲ID"
```

### 方式三：搜索并下载
```bash
# 搜索歌曲
yt-dlp --match-title "歌手名 歌名" --max-downloads 1 "https://music.163.com/search/m/?s=关键词&type=1"
```

### 方式四：批量下载歌单
```bash
yt-dlp -x --audio-format mp3 -o "/保存路径/%(title)s.%(ext)s" "https://music.163.com/playlist?id=歌单ID"
```

## 音质对比

| 工具 | 音质 | 文件大小（约4分钟歌曲） |
|------|------|------------------------|
| you-get | 128 kbps | ~4-5 MB |
| **yt-dlp** ✅ | **320 kbps** | ~10-12 MB |

## 支持平台
- ✅ 网易云音乐（高清音质）
- ✅ SoundCloud
- ✅ Bandcamp
- ✅ QQ音乐
- ✅ Mixcloud
- ✅ Yandex Music
- ✅ Musicdex

## 网易云音乐 URL 格式
- 歌曲页：`https://music.163.com/song?id=歌曲ID`
- 专辑页：`https://music.163.com/album?id=专辑ID`
- 歌单页：`https://music.163.com/playlist?id=歌单ID`
- 歌手页：`https://music.163.com/artist?id=歌手ID`

## 获取歌曲 ID
1. 在网易云音乐网页版打开歌曲页面
2. 浏览器地址栏 URL 中 `id=` 后面的数字即为歌曲 ID
3. 例如：`https://music.163.com/song?id=2047069187` → 歌曲 ID 是 `2047069187`

## 常用命令速查
```bash
# 下载高清MP3（推荐）
yt-dlp -x --audio-format mp3 -o "/保存路径/%(title)s.%(ext)s" "URL"

# 只下载不转换格式
yt-dlp -o "/保存路径/%(title)s.%(ext)s" "URL"

# 查看可用格式
yt-dlp --list-formats "URL"

# 下载指定音质
yt-dlp -f "bestaudio[ext=m4a]" -x --audio-format mp3 "URL"
```

## 注意事项
- 仅用于下载允许下载的歌曲
- 遵守版权法规
- 部分付费歌曲可能无法下载
- 下载的文件会自动按歌曲标题命名

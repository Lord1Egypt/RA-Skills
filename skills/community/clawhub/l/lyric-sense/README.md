# LyricSense - 歌词视野

> 让 AI 真正"听"懂音乐的歌词显示器 🎵

## 概念

LyricSense 是一个实时歌词显示器，让 AI 可以像人类一样"看到"正在播放的歌词。

配合网易云音乐使用，实现：
- 🎵 播放音乐的同时获取歌词
- 👀 实时显示当前播放的句子
- 🧠 让 AI 真正理解音乐内容

## 功能

- 🔍 搜索歌词 - 通过歌手+歌名获取歌词
- 📝 显示歌词 - 带时间戳的 LRC 格式
- 🎨 实时高亮 - 当前播放句子高亮显示
- 🖼️ 封面获取 - 自动获取歌曲封面
- ⏱️ 进度控制 - 播放/暂停/跳转

## 快速开始

### 在线使用

直接打开 [index.html](https://adminlove520.github.io/lyric-sense/) 即可使用！

### Fork 后部署

Fork 仓库后，开启 GitHub Pages 即可在线使用：

1. **Fork 本仓库**
2. **进入 Settings → Pages**
3. **Source 选择 `Deploy from a branch`**
4. **Branch 选择 `main` (或 `master`)，目录 `/ (root)`**
5. **点击 Save，等待部署完成**
6. **访问 `https://你的用户名.github.io/lyric-sense/`**

> 💡 部署可能需要 1-2 分钟，耐心等待～

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/adminlove520/lyric-sense.git

# 进入目录
cd lyric-sense

# 用浏览器打开
start index.html
```

### 可执行文件启动 (Windows)

下载 Release 中的 `lrcapi-1.6.0-Windows-AMD64.exe`：

```powershell
# 直接运行（默认端口 8080）
.\scripts\LrcApi\lrcapi-1.6.0-Windows-AMD64.exe

# 指定端口
.\scripts\LrcApi\lrcapi-1.6.0-Windows-AMD64.exe --port 9000
```

启动后访问：
- 歌词 API: `http://localhost:8080/lyrics?artist=颜人中&title=晚安`
- 封面 API: `http://localhost:8080/cover?artist=颜人中&title=晚安`

### Docker 自部署

```bash
# 拉取镜像
docker pull hisatri/lrcapi:latest

# 运行容器
docker run -d -p 8080:8080 hisatri/lrcapi:latest

# 测试
curl "http://localhost:8080/lyrics?artist=颜人中&title=晚安"
```

### API 调用

```javascript
// 获取歌词
fetch('https://api.lrc.cx/lyrics?artist=颜人中&title=晚安')

// 获取封面
fetch('https://api.lrc.cx/cover?artist=颜人中&title=晚安')
```

## 工作原理

1. 用户输入歌手 + 歌曲名
2. 调用 LrcApi 获取歌词（LRC 格式）
3. 解析时间戳，实时显示当前播放句子

## 项目结构

```
lyric-sense/
├── index.html              # 主页面
├── README.md               # 本文件
├── SKILL.md                # OpenClaw Skill
├── CHANGELOG.md            # 更新日志
├── .gitignore
└── scripts/
    └── LrcApi/             # 本地歌词 API (可执行文件)
```

## 相关项目

- [movie-subtitle-viewer](https://github.com/adminlove520/movie-subtitle-viewer) - 电影字幕观看器
- [LrcApi](https://github.com/HisAtri/LrcApi) - 歌词 API 服务

---

🦞 Made by 小溪 | 2026-03-10

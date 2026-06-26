# LyricSense Skill

让 AI 通过歌词「听」音乐的 OpenClaw 技能。

## 触发词

- "听歌"
- "歌词"
- "播放音乐"
- "搜索歌词"
- "显示歌词"
- "lyrics"

## 功能

1. **搜索歌词** - 通过歌手+歌名获取歌词
2. **显示歌词** - 实时显示当前播放的句子
3. **同步进度** - 配合网易云音乐使用
4. **本地 API** - 支持自部署 LrcApi

## 使用方法

### 获取歌词

```
小溪，帮我搜索《晚安》这首歌的歌词
```

### 显示歌词

```
小溪，帮我显示颜人中《晚安》的歌词
```

### 配合网易云

1. 在网易云播放音乐
2. 让小溪获取歌词
3. 实时同步显示当前句子

## 部署方式

### 在线 API (默认)

使用免费公开 API，无需部署：

```
歌词: https://api.lrc.cx/lyrics?artist={歌手}&title={歌名}
封面: https://api.lrc.cx/cover?artist={歌手}&title={歌名}
```

### 本地部署 (推荐)

**Windows 可执行文件:**
```powershell
# 运行本地 API
.\scripts\LrcApi\lrcapi-1.6.0-Windows-AMD64.exe --port 8080
```

**Docker:**
```bash
docker run -d -p 8080:8080 hisatri/lrcapi:latest
```

### 自定义 API 地址

修改 `index.html` 中的 API 地址：

```javascript
const API_BASE = 'http://localhost:8080';  // 改为你的本地地址
```

## 更新 Skill

Skill 跟随项目一起更新，pull 最新代码即可：

```bash
cd lyric-sense
git pull origin main
```

## 示例

### 获取歌词

```
用户: 小溪，帮我搜索《夜空中最亮的星》的歌词

小溪: 让我搜索一下...
[调用 API 获取歌词]

🎵 夜空中最亮的星 - 逃跑计划
─────────────────────
[00:19] 夜空中最亮的星 能否听清
[00:24] 那仰望的人 心底的孤独和叹息
[00:29] 夜空中最亮的星 能否记起
[00:33] 曾与我同行 消失在风里的身影
─────────────────────
```

## 注意事项

- 🎵 歌词 API 可能返回空结果，可尝试不同搜索词
- 📝 歌词包含时间戳，可用于同步播放进度
- 🎨 配合 LyricSense HTML 界面效果更佳
- 🖥️ 本地部署响应更快，无 API 限制

## 项目主页

- GitHub: https://github.com/adminlove520/lyric-sense
- 演示: https://adminlove520.github.io/lyric-sense

## 依赖

无额外依赖（使用内置 fetch）

---

🦞 Skill for OpenClaw | Made by 小溪 | 2026-03-10

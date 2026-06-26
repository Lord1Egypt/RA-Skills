# Movie Subtitle Viewer Skill

让 AI 通过字幕「看」电影的 OpenClaw 技能。

## 触发词

- "看电影"
- "搜字幕"
- "下载字幕"
- "subtitle"

## 功能

1. **搜索字幕** - 通过电影名/年份搜索 OpenSubtitles
2. **下载字幕** - 下载 .srt 格式字幕文件
3. **解析字幕** - 提取电影台词
4. **生成摘要** - 让 AI 理解剧情

## 使用方法

### 搜索电影字幕

```
小溪，帮我搜索《XXX》的字幕
```

### 搜索并下载

```
小溪，帮我下载《人工智能》的英文字幕
```

### 解析字幕

```
小溪，帮我解析这个字幕文件
```

## 环境变量

需要在 `.env` 或系统环境中设置：

```
OPENSUBTITLES_API_KEY=your_api_key
OPENSUBTITLES_USERNAME=your_username  
OPENSUBTITLES_PASSWORD=your_password
```

## 获取 OpenSubtitles API

1. 注册 https://www.opensubtitles.com
2. 进入 Profile → API
3. 生成 API Key

## 注意事项

- ⚠️ 不要泄露你的 API Key 和密码
- 📝 字幕文件会保存在 workspace 目录
- 🎬 支持 .srt 和 .ass 格式

## 示例

### 看《机械姬》

```
用户: 小溪，帮我下载《机械姬》的字幕

小溪: 好的！让我搜索一下...
[搜索字幕]
[下载字幕]
[解析台词]

《机械姬》剧情摘要：
- 程序员 Caleb 被邀请到老板的豪宅，对 AI 进行图灵测试
- AI 名为 Ava，具有人类外貌和高度智能
- 测试过程中，Ava 开始展现出自我意识和操控欲...
```

## 依赖

- `pysubs2` - 字幕解析
- `requests` - HTTP 请求

## 目录

```
skill/
├── SKILL.md              # 本文件
└── scripts/
    └── movie_viewer.py  # 核心逻辑
```

---

🦞 Skill for OpenClaw | Made by 小溪

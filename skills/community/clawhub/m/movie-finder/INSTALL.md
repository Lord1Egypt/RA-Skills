# movie-finder 安装说明

## 技能简介

movie-finder 是一个电影搜索播放技能，支持：
- 🔍 按类型（科幻/喜剧/恐怖等）、年份、评分筛选电影
- 🖼 展示电影海报、评分、剧情简介
- ▶️ 生成可播放的 HTML 页面，直接在线观看

## 文件结构

```
movie-finder/
├── SKILL.md                    # 技能说明文件（必需）
├── scripts/
│   └── generate_movie_page.py  # 电影页面生成脚本
└── references/                 # 参考资料目录（可选）
```

## 安装方式

### 方式一：安装到 workspace（推荐）

将 `movie-finder` 文件夹放入你的 OpenClaw workspace skills 目录：

```
<workspace>/skills/movie-finder/
```

workspace 路径通常为：
- Windows: `C:\Users\<用户名>\.openclaw\workspace\skills\`
- macOS/Linux: `~/.openclaw/workspace/skills/`

### 方式二：安装到全局共享目录

放入 managed/local skills 目录：

```
~/.openclaw/skills/movie-finder/
```

### 方式三：从 ClaW Hub 安装（待发布后）

```bash
openclaw skills install movie-finder
```

## 依赖说明

- **无需额外依赖** — 直接使用 web_search 搜索电影信息
- 可选：Python 3（如果使用 `generate_movie_page.py` 脚本生成播放页面）

## 验证安装

安装完成后，新开一个对话窗口，说"我想看一部科幻电影"或"show me latest action movies"，技能应该会自动激活。

## 卸载

删除 `movie-finder` 文件夹即可。

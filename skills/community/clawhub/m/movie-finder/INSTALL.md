# movie-finder 安装说明

## 技能简介

movie-finder 是一个电影搜索播放技能，支持：
- 🔍 按类型（科幻/喜剧/恐怖等）、年份、评分筛选电影
- 🖼 展示电影海报、评分、剧情简介、导演、演员、类型标签
- ▶️ 生成可播放的 HTML 页面，内嵌 iframe 播放器，支持多播放源页内切换

## 文件结构

```
movie-finder/
├── SKILL.md                    # 技能说明文件（必需）
├── INSTALL.md                  # 本安装说明
├── scripts/
│   └── generate_movie_page.py  # 电影页面生成脚本
└── _meta.json                  # 技能元数据
```

## 安装方式

### 方式一：安装到用户级目录（推荐，跨项目可用）

放入用户级 skills 目录：

```
~/.workbuddy/skills/movie-finder/
```

- Windows: `C:\Users\<用户名>\.workbuddy\skills\movie-finder\`
- macOS/Linux: `~/.workbuddy/skills/movie-finder/`

### 方式二：安装到项目级目录（仅当前项目可用）

放入当前项目的 `.workbuddy/skills/` 目录：

```
<项目根目录>/.workbuddy/skills/movie-finder/
```

## 依赖说明

- **无需额外依赖** — 搜索电影信息使用内置 web_search 或 TMDB API
- 可选：Python 3（若使用 `generate_movie_page.py` 脚本生成播放页面，仅用标准库）

## 验证安装

安装完成后，新开一个对话窗口，说"我想看一部科幻电影"或"show me latest action movies"，技能应该会自动激活。

## 卸载

删除 `movie-finder` 文件夹即可。

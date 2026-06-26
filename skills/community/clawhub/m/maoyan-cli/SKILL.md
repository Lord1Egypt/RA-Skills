---
name: maoyan-cli
description: 查询猫眼影院排片、搜索电影和上映影院。当用户询问某影院排片（如“某某影城排片”）、某电影在哪家影院上映、某城市有哪些影院，或需要抓取猫眼排片和影院数据时使用。
---

# 猫眼影院排片与查询

本技能通过执行本地 Python 脚本查阅猫眼电影数据。所有命令都会输出结构化的 JSON 格式结果。请根据需要解析输出的数据并回答用户的问题。

## 核心工作流与命令

执行以下命令完成特定任务（从项目根目录执行，脚本路径为 `skills/maoyan-cli/scripts/maoyan_cli.py`）：

### 1. 获取城市 ID（所有操作的基础）
```bash
python skills/maoyan-cli/scripts/maoyan_cli.py cities -q <城市名>
```
**说明**：从输出中提取 `ci`（城市 ID）供后续命令使用（如北京对应的 `ci` 是 1）。

### 2. 查询城市中的影院列表
```bash
python skills/maoyan-cli/scripts/maoyan_cli.py cinemas <ci> [--lat <纬度> --lng <经度>] --limit 20
```
**说明**：用于查找特定名称影院的 `cinemaId`，或回答“某地有哪些影院”。如果有用户的具体位置信息，请传入经纬度以按距离排序。

### 3. 查询指定影院的排片（含场次和价格）
```bash
python skills/maoyan-cli/scripts/maoyan_cli.py shows <cinemaId> <ci>
```
**说明**：获取该影院当日及未来几日的排片情况，包括上映的电影信息（含 `posterUrl` 封面图链接、`nm` 片名、`sc` 评分、选场页链接 `cinemaPageUrl`）、具体场次（`seqNo`）、价格（`originPrice`）及直达选座买票的链接（`seatUrl`）。

### 4. 电影详情（从详情页 HTML 正则解析）
```bash
python skills/maoyan-cli/scripts/maoyan_cli.py detail <movieId> [ci] [--cinemaId <影院ID>] [--lat <纬度> --lng <经度>]
```
**说明**：请求 `https://m.maoyan.com/asgard/movie/{movieId}` 详情页 HTML，用正则解析片名（`nm`）、英文名（`enm`）、类型（`cat`）、主演（`actors`）、上映/开播信息（`releaseInfo`）、时长文案（`durText`）、时长分钟数（`dur`）、原始拼接串（`showTime`）、猫眼评分（`sc`）、评分人数（`scoreCount`）、简介（`desc`）、海报（`posterUrl`）、关键词（`keywords`）等。`showTime` 会按 ` / ` 拆成 `releaseInfo` 与 `durText`，便于单独展示（如「2019-10-06美国开播」+「45分钟」）。可选 `--cinemaId`、`--lat`、`--lng` 与详情页 URL 一致（带影院或位置上下文）。

### 5. 搜索特定电影及查询上映影院（“某电影在哪看”）
```bash
# 第一步：搜索电影，从返回的 movies 列表中提取正确的 movieId（每项含 posterUrl 封面图、nm、id 等）
python skills/maoyan-cli/scripts/maoyan_cli.py search <电影名> <ci>

# 第二步：使用获取到的 movieId 查询放映该电影的影院列表（输出中会包含该影院该电影的选场页链接 cinemaPageUrl）
python skills/maoyan-cli/scripts/maoyan_cli.py movie-cinemas <movieId> <ci> [--lat <纬度> --lng <经度>] --limit 20
```

## 典型场景示例

**场景 1：查特定影院的排片**
1. 运行 `cinemas <ci>`，在返回的 JSON 中模糊匹配找到目标影院的 `cinemaId`。
2. 运行 `shows <cinemaId> <ci>` 获取并总结排片详情给用户。

**场景 2：查某部电影在哪里上映**
1. 运行 `search <电影名> <ci>` 找到对应电影的 `movieId`。
2. 运行 `movie-cinemas <movieId> <ci>` 获取影院列表并推荐给用户。

## 附加资源

- 完整的数据结构与接口说明：见 [reference.md](reference.md)
- 更多的命令使用示例：见 [examples.md](examples.md)

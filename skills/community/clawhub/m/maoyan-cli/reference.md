# 猫眼电影 API 参考

## 1. 城市列表 cities.json

- **URL**: `https://m.maoyan.com/dianying/cities.json`
- **方法**: GET
- **响应**: JSON，`cts[]` 为城市列表，每项含 `id`、`nm`（名称）、`py`（拼音）。

用于查城市 ID（如北京=1），供后续 filter / moreCinemas / shows 使用。

---

## 2. 影院筛选条件 filterCinemas

- **URL**: `https://m.maoyan.com/ajax/filterCinemas`
- **参数**: `ci`（城市 ID，必填），可选 `optimus_uuid`、`optimus_risk_level`、`optimus_code`
- **响应**: JSON，含 `brand`（品牌）、`district`（行政区）、`hallType`、`service`、`subway` 等筛选项及子项 id/name/count。

用于获取品牌 ID、区域 ID 等，再传给 moreCinemas 做筛选。

---

## 3. 影院列表 moreCinemas

- **URL**: `https://m.maoyan.com/ajax/moreCinemas`
- **方法**: GET（Query 参数）
- **主要参数**:
  - `cityId` / `ci`: 城市 ID
  - `day`: 日期，如 `2026-03-04`
  - `offset`、`limit`: 分页
  - `districtId`、`brandId`、`lineId`、`hallType`、`serviceId` 等：与 filterCinemas 一致，-1 表示全部
  - `lat`、`lng`: 经纬度（可选，影响距离排序）
- **响应**: **HTML 片段**，每个影院为 `<a href="/shows/{cinemaId}">` 包裹的块，块内有 `data-id`（即 cinemaId）、影院名称、价格、地址、距离等。

解析时提取：**cinemaId**（来自 `/shows/数字` 或 `data-id`）、**名称**（.title span）、**地址**（.flex.line-ellipsis）、**距离**（.distance）、**价格**（.price + 元起）。

---

## 4. 影院排片 shows.json

- **URL**: `https://m.maoyan.com/mtrade/cinema/cinema/shows.json`
- **参数**: `cinemaId`、`ci` 必填；`channelId`、`yodaReady`、`csecplatform`、`csecversion` 等可固定。
- **响应**: JSON，`code=0` 时 `data.cinemaName` 为影院名，`data.movies[]` 为电影列表。每部电影含 `id`、`nm`（片名）、`img`（封面图 URL）、`sc`（评分）、`dur`（时长）等；CLI 会为每部电影注入 `posterUrl`（与 `img` 一致，便于展示封面），为每部电影的每个日期块注入 `cinemaPageUrl`（选场页），为每个场次注入 `seatUrl`（选座买票页）和 `originPrice`（原价）。

详见 SKILL.md 中的排片解析说明。

---

## 5. 电影搜索 search

- **URL**: `https://m.maoyan.com/apollo/ajax/search`
- **参数**: `kw`（关键词，必填）、`cityId`（城市 ID）、`stype=-1`
- **响应**: JSON，`success` 为 true 时 `movies.list[]` 为电影列表，每项含 `id`（movieId）、`nm`（片名）、`img`（封面图 URL）、`sc`（评分）、`dur`（时长）、`rt`（上映时间）等。CLI 会为每部电影注入 `posterUrl`（与 `img` 一致，便于展示封面）。

用于按片名查电影并拿到 **movieId**，再配合「某电影上映影院」接口使用。

---

## 6. 某电影上映影院 cinemas.json（按电影）

- **URL**: `https://m.maoyan.com/api/mtrade/mmcs/cinema/movie/cinemas.json`
- **主要参数**: `movieId`（必填）、`cityId`/`ci`、`showDate`（YYYY-MM-DD）、`limit`、`offset`、`sort`（如 distance）、`lat`、`lng`；另有 `districtId`、`brandIds`、`hallTypeIds` 等。
- **响应**: JSON，`code=0` 时 `data.cinemas[]` 为影院列表。CLI 输出会为每个影院注入 `cinemaPageUrl`（该电影在该影院该日期的选场页链接）。

用于查「某部电影在某城市有哪些影院在映」。

---

## 7. 电影详情页 asgard/movie（HTML）

- **URL**: `https://m.maoyan.com/asgard/movie/{movieId}`
- **参数**: `_v_=yes`、`channelId=4`、`ci`（城市 ID）；可选 `cinemaId`、`lat`、`lng`。
- **响应**: 完整 HTML 页面。CLI 通过正则从 HTML 中解析：
  - **meta**：`share:wechat:message:title`（片名+评分+上映）、`share:wechat:message:desc`（简介）、`share:wechat:message:icon`（海报）、`description`、`keywords`
  - **正文**：`.movie-cn-name` / `.movie-en-name`（中英文名）、`.movie-cat`（类型）、`.movie-show-time`（上映/时长）、`.score`（评分）、`人评`（评分人数）、`.actors` 内链接（主演）、`.poster` 的 `src`（海报图）
- **输出字段**：`id`、`nm`、`enm`、`cat`、`actors`、`showTime`（原始）、`releaseInfo`（上映/开播信息）、`durText`（时长文案，如「45分钟」）、`dur`（时长分钟数）、`sc`、`scoreCount`、`desc`、`posterUrl`、`detailUrl`、`keywords`。

用于获取单部电影的详情（剧情介绍、演职员、评分等），无需依赖 JSON 接口。

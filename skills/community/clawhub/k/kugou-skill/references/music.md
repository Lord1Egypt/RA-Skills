# 音乐命令 (music)

> 🔐 = 所有 music 命令都需要先登录

## 命令列表

| 命令 | 说明 |
|------|------|
| `kugou-cli music search <keyword>` | 搜索歌曲 |
| `kugou-cli music recommend guess` | 猜你喜欢（个性化推荐） |
| `kugou-cli music recommend similar -s <song>` | 相似歌曲推荐 |
| `kugou-cli music favorites` | 我的收藏 |
| `kugou-cli music recent` | 最近播放 |
| `kugou-cli music stats` | 听歌统计 |
| `kugou-cli music charts <rank_id>` | 榜单 |
| `kugou-cli music create-playlist <name>` | 创建歌单（可附加歌曲） |
| `kugou-cli music search-playlist <keyword>` | 搜索歌单 |
| `kugou-cli music recommend-playlist` | 歌单推荐 |
| `kugou-cli music playlist-songs <global_collection_id>` | 歌单内歌曲列表 |
| `kugou-cli music submit-preference` | 提交偏好（减少/屏蔽/增加） |

---

## 1. 搜索歌曲

```bash
kugou-cli music search "周杰伦"
kugou-cli music search "周杰伦" --page 1 --size 20
```

**参数**:
- `<keyword>`: 搜索关键词（必填）
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "song_name": "晴天",
        "mix_song_id": "32100650",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/j410q78a01f.html"
      }
    ],
    "total": 480,
    "page": 1,
    "size": 20
  },
  "status": 1
}
```

---

## 2. 歌曲推荐

支持三种推荐模式：

| 类型 | 说明 | 必填参数 |
|------|------|---------|
| `guess` | 猜你喜欢，基于用户喜好推荐 | 无 |
| `similar` | 相似推荐，根据指定歌曲推荐相似歌曲 | `--song` |
| `text` | 文本推歌，根据文本描述推荐歌曲 | `--text` |

### 2.1 猜你喜欢

```bash
kugou-cli music recommend guess
kugou-cli music recommend guess --num 10
```

**参数**:
- `--num`: 推荐数量，默认 10

### 2.2 相似推荐

```bash
kugou-cli music recommend similar -s "晴天"
kugou-cli music recommend similar --song "晴天" -n 5
kugou-cli music recommend similar --song "晴天" --text "风格相似的" -n 5
```

**参数**:
- `-s, --song`: 歌曲名称（必填）
- `-n, --num`: 推荐数量，默认 10
- `-t, --text`: 描述文本（可选），用于进一步细化相似方向

### 2.3 文本推歌

```bash
kugou-cli music recommend text --text "适合跑步时听的快节奏歌曲"
kugou-cli music recommend text --text "安静的钢琴曲" --num 5
```

**参数**:
- `-t, --text`: 文本描述（必填）
- `-n, --num`: 推荐数量，默认 10

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "song_name": "稻香",
        "mix_song_id": "8889",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/xxx.html"
      }
    ]
  },
  "status": 1
}
```

---

## 3. 我的收藏

```bash
kugou-cli music favorites
```

**参数**: 无（上游接口固定返回最近 10 首收藏，不支持分页）

> 注意：固定返回最近 10 首收藏，查看更多请前往酷狗App

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "song_name": "晴天",
        "mix_song_id": "32100650",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/j410q78a01f.html"
      }
    ],
    "total": 50,
    "msg": "当前仅显示最近的10首收藏，查看更多内容，请前往酷狗App"
  },
  "status": 1
}
```

---

## 4. 最近播放

```bash
kugou-cli music recent
```

**参数**: 无（上游接口固定返回最近 10 条播放记录，不支持分页）

> 注意：固定返回最近 10 首播放记录，查看更多请前往酷狗App

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "song_name": "七里香",
        "mix_song_id": "32100651",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/j410q78a01f.html"
      }
    ],
    "total": 100,
    "msg": "当前仅显示最近的10首最近播放，查看更多内容，请前往酷狗App"
  },
  "status": 1
}
```

---

## 5. 听歌统计

```bash
kugou-cli music stats                    # 默认查当月
kugou-cli music stats --date-type 1 --date 20260501  # 指定周查询
```

**参数**:
- `--date-type`: 日期类型，0=日、1=周、2=月（默认查当月）
- `--date`: 查询日期，YYYYMMDD 格式，如 "20260501"。不传则查当月
  - 日类型：每天日期，如 "20260501"
  - 周类型：必须是周一日期，如 "20260505"（周一）
  - 月类型：必须是月份第一天，如 "20260501"（5月1日）

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "server_time": 1779977674,
    "listen_duration": 80776,
    "accumulate_listen_days": 30,
    "continue_listen_days": 7,
    "listen_total": 342,
    "last_listen_total": 387,
    "top_clocks": [
      "今日08:00-10:00听歌30分钟",
      "今日14:00-16:00听歌25分钟",
      "今日20:00-22:00听歌20分钟"
    ],
    "rank_song": [
      {
        "song_info": {"song_name": "晴天", "mix_song_id": "8888", "artist_name": "周杰伦", "play_link": "https://www.kugou.com/..."},
        "count": 50
      }
    ],
    "rank_singer": [
      {"singer_id": 123, "name": "周杰伦", "avatar": "https://xxx.jpg", "total": 120}
    ],
    "rank_style": [
      {"style": "流行", "total": 200, "count": 80}
    ],
    "rank_language": [
      {"language": "华语", "total": 400, "count": 150}
    ]
  },
  "status": 1
}
```

**关键字段**:
- `listen_duration`: 今日/周/月听歌时长（秒）
- `top_clocks`: 听歌时长最长的 Top3 时段描述（日类型格式如"今日08:00-10:00听歌30分钟"，周/月类型格式如"2026-02月听歌38213分钟"）
- `accumulate_listen_days`: 累计听歌天数
- `continue_listen_days`: 连续听歌天数
- `listen_total`: 累计听歌次数
- `last_listen_total`: 昨日/上周/上月听歌次数
- `rank_song`: 播放最多的歌曲排行（`count` 为播放次数）
- `rank_singer`: 播放最多的歌手排行
- `rank_style`: 曲风分布统计
- `rank_language`: 语言分布统计

---

## 6. 榜单

```bash
kugou-cli music charts 6666
kugou-cli music charts 52144 --page 1 --size 20
```

**可用榜单 ID**:

| rank_id | 榜单名称 |
|---------|----------|
| 8888 | TOP500榜 |
| 90379 | 星耀星光榜 |
| 6666 | 飙升榜 |
| 85432 | 百万收藏榜 |
| 74534 | 新歌榜 |
| 52144 | 抖音热歌酷狗榜 |

**参数**:
- `<keyword>`: 搜索关键词（必填）
- `--page`: 页码，默认 1（**无简写**）
- `--size`: 每页数量，默认 20（**无简写**）

---

## 7. 创建歌单

> 🔐 = 需要先登录（CLI 登录 `auth login` / `auth set-secret`）

### 7.0 调用原则（AI 必读）

1. **被动调用**：必须用户**明确**要求创建歌单时才调用，禁止在用户仅说"推荐/搜歌/听歌"时主动创建
2. **主动询问**：当通过搜索、推荐（猜你喜欢/相似/文本）等方式给出一批歌曲后，**必须**询问用户"是否需要将当前这批歌曲创建为歌单"，等用户确认后再调用
3. **示例化推荐**：询问时建议给出歌单名建议（如"跑步歌单"、"周杰伦精选"），让用户更容易确认
4. **硬性默认：优先客户端创建**：用户一旦同意创建歌单，**必须先尝试** [`control playlist create`](./control.md#10-playlist-create--创建歌单)（在本地酷狗客户端内创建）。当以下**任一**条件成立时，回退到本节的 `music create-playlist`（云端创建）：
   - **(a)** 当前系统不是 Windows / macOS（control 不支持 Linux）
   - **(b)** 本地酷狗客户端未运行，或未通过 `kugou-cli control start` 完成握手（前置条件详见 [control.md §10](./control.md#10-playlist-create--创建歌单)）
   - **(c)** `control playlist create` 调用失败（如 409/4091"login required"、网络错误等）—— 此时把 stderr 原样回给用户，并询问是否改走云端

   简单说：**默认 `control`；客户端不可用或失败时，才退到 `music`**。不要在用户没问的情况下主动解释为什么走云端，先尝试 client 路径即可。

5. **创建成功后主动询问是否播放**：无论走 `control playlist create` 还是 `music create-playlist`，**只要创建成功（返回 0/成功状态）就必须主动询问用户"是否要播放这个歌单"**，等用户明确回复后再决定走哪条播放命令：
   - 用户同意 → 按场景选播放路径：
     - **客户端路径优先**：`kugou-cli control play-playlist --global-id "<id>"`（详见 [control.md §12](./control.md#12-play-playlist--播放整个歌单)），可叠加 `--playlist-mode` 控制是否打断当前播放
     - **云端歌单（`music create-playlist` 创建的）**：走浏览器 H5 路径（详见下方 7.2）——**不要**再用 `control play-playlist`，因为本地客户端没有这首歌单
   - 用户拒绝 / 不回复 → 不做任何动作，不要替用户决定
   - 仅在"创建歌单成功"时才询问；建失败时不询问（直接展示错误，等用户决定下一步）

### 7.1 接口说明（云端备选，仅在 7.0 第 4 条任一条件成立时使用）

> ⚠️ 本节是**云端备选路径**。优先走 [`control playlist create`](./control.md#10-playlist-create--创建歌单)（详见 [7.0 第 4 条](#70-调用原则ai-必读)）。仅当客户端不可用时使用本节。

创建一个新的自创建歌单，并可选择在创建后往歌单里添加歌曲。

```bash
# 创建空歌单
kugou-cli music create-playlist "我的空歌单"

# 创建歌单并添加歌曲
kugou-cli music create-playlist "我的批量歌单" --songs "123,456,789"
```

**参数**:
- `<name>`: 歌单名称（必填）
- `--songs`: 待添加的歌曲 mix_song_id 列表，逗号分隔（可选）。不传则只创建空歌单

**输出示例**:
```json
{
  "errcode": 0,
  "errmsg": "",
  "data": {
    "name": "我的批量歌单",
    "song_list_url": "https://m.kugou.com/songlist/gcid_abc123def45"
  },
  "status": 1
}
```

**关键字段**:
- `name`: 歌单名称
- `song_list_url`: 歌单播放地址（H5 链接），可分享给用户打开

**异常说明**:
- 歌单创建成功但添加歌曲失败：返回 200 状态 + 错误信息，body 仍包含已创建歌单的 `name` 与 `song_list_url`
- 歌单创建失败：返回对应错误码（参数错误 20010 / 网络错误 90000 等）

### 7.2 云端歌单的播放：控制浏览器打开 H5 链接

> 适用场景：用户同意播放的歌单是 `music create-playlist` 创建的（响应里有 `song_list_url`），且本地没有可用的酷狗客户端（7.0 第 4 条 (a)(b)(c) 任一成立）。

**Agent 必须遵循"先探后告知"原则**：

1. **先探测浏览器控制能力**：当前 Agent 工具栈是否能控制本地浏览器（playwright / dev-browser / chrome-devtools MCP 等任一可用）。可用 = 可用；都不可用 = 当前环境不支持浏览器控制
2. **可用时**：
   - 用浏览器工具打开响应里的 `song_list_url`（H5 链接，格式如 `https://m.kugou.com/songlist/gcid_...`）
   - 等待 H5 页面加载完成（`networkidle` / 出现"播放全部"按钮）
   - **轻量职责**：点击页面上的"播放" / "播放全部"按钮（若有），控制到"页面已渲染出播放控制"为止
   - 页面登录、付费、版权屏蔽等后续问题**不归 Agent 管**，告诉用户"已打开 H5 歌单并尝试点击播放，如未自动播放请手动点一下"
3. **不可用时**（无浏览器控制工具 / 浏览器控制调用失败）：
   - 明确告知用户："当前环境无法控制浏览器，请手动复制链接在浏览器打开：[song_list_url]"
   - **不要**伪装已经打开或点击了播放

> **为什么不写死"先 playwright 再 chrome-devtools"？** 不同 Agent 工具栈内置的浏览器工具名不同，文档只规定行为契约（"打开 + 点击播放"），具体工具由 Agent 现场选择。

---

## 8. 搜索歌单

根据关键词搜索歌单。

```bash
kugou-cli music search-playlist "周杰伦"
kugou-cli music search-playlist "周杰伦" --page 1 --size 20
kugou-cli music search-playlist "跑步" --filter 1   # 只搜 UGC
kugou-cli music search-playlist "钢琴" --filter 2   # 只搜非 UGC
```

**参数**:
- `<keyword>`: 搜索关键词（必填）
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20
- `--filter`: 过滤方式，`0=全部（默认） / 1=只搜 UGC / 2=只搜非 UGC`

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "list_id": 2651286,
        "global_id": "collection_3_938985631_304_0",
        "name": "<em>周杰伦</em>：无与伦比，为杰沉沦。",
        "creator_id": "938985631",
        "creator_name": "慕情超爱撒花",
        "intro": "",
        "song_list_url": "https://m.kugou.com/songlist/gcid_3z938985631z304z2"
      }
    ],
    "total": 1000,
    "page": 1,
    "size": 20
  },
  "status": 1
}
```

**关键字段**:
- `list_id`: 歌单 ID（数字 string）
- `global_id`: 全局歌单 ID（字符串，跨客户端兼容的稳定标识）
- `name`: 歌单名
- `creator_id`: 创建人用户 ID（字符串）
- `creator_name`: 创建人昵称
- `intro`: 歌单简介
- `song_list_url`: 歌单链接（H5），格式 `https://m.kugou.com/songlist/gcid_{encoded(global_id)}`；`global_id` 为空时返回空字符串

> **提示**: 歌单搜索/推荐只返回基础信息用于卡片展示。需要歌曲数、播放量、收藏数、封面图、歌单内歌曲等详细信息时，调用方拿到 `global_id` 后调用 [第 10 章](#10-歌单内歌曲列表) 或直接打开 `song_list_url`。

**特殊说明**:
- 上游高亮：服务端固定传 `tag=em`，返回的 `name` 字段带 `<em>...</em>` 高亮标签，前端可直接渲染
- 上游错误码：146/147=被屏蔽地区，148=非法关键字，149=页码超出范围。出现时返回 90000 网络错误，建议引导用户重试或更换关键词

---

## 9. 歌单推荐

根据用户喜好个性化推荐歌单。

```bash
kugou-cli music recommend-playlist
kugou-cli music recommend-playlist --page 1 --size 20
kugou-cli music recommend-playlist --module-id 6   # 我-最近播放-歌单下方
```

**参数**:
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20
- `--module-id`: 上游模块 ID，由客户端透传。常见值：
  - `1` = 歌单广场（默认）
  - `5` = 酷狗 X 首页为你推荐
  - `6` = 我 - 最近播放 - 歌单下方
  - `15` = 酷狗 12 听首页为你推荐

  不传时服务端默认填 `1`。

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "list_id": 2651286,
        "global_id": "collection_3_938985631_304_0",
        "name": "周杰伦：无与伦比，为杰沉沦。",
        "creator_id": "938985631",
        "creator_name": "慕情超爱撒花",
        "intro": "",
        "song_list_url": "https://m.kugou.com/songlist/gcid_3z938985631z304z2"
      }
    ],
    "total": 100,
    "has_next": 1,
    "session": "1706428800",
    "refresh_time": 0,
    "page": 1,
    "size": 20
  },
  "status": 1
}
```

**关键字段（顶层）**:
- `total`: 总数；`has_next`: 是否有下一页（1=是 / 0=否）
- `session`: 会话标识（暂时返回时间戳）
- `refresh_time`: 客户端刷新时间（秒），`0` 或缺失表示不刷新

**关键字段（list[]）**:
- 与歌单搜索（[第 8 章](#8-搜索歌单)）共用同一套 `PlaylistInfo` 基础字段（`list_id` / `global_id` / `name` / `creator_id` / `creator_name` / `intro` / `song_list_url`），调用方可使用同一套反序列化逻辑
- 已登录时上游根据 userid 做个性化推荐；未登录时可能返回空数据或通用推荐
- 上游可能附带 `cache` 等额外字段，**未在 `PlaylistInfo` 中列出的字段请勿依赖**

---

## 10. 歌单内歌曲列表

通过歌单全局 ID（`global_collection_id`）获取歌单内歌曲列表。一般先调用 [第 8 章](#8-搜索歌单) 或 [第 9 章](#9-歌单推荐) 拿到 `global_id`，再透传给本接口。

```bash
kugou-cli music playlist-songs "collection_3_938985631_304_0"
kugou-cli music playlist-songs "collection_3_938985631_304_0" --page 1 --size 100
```

**参数**:
- `<global_collection_id>`: 歌单全局 ID（必填，从 `search-playlist` / `recommend-playlist` 响应的 `global_id` 字段透传）
- `--page`: 页码，从 1 开始，默认 1
- `--size`: 每页数量，默认 100（上游建议值）

**输出示例**:
```json
{
  "errcode": 0,
  "data": {
    "list": [
      {
        "song_name": "晴天",
        "mix_song_id": "8888",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/j410q78a01f.html"
      },
      {
        "song_name": "七里香",
        "mix_song_id": "8890",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/j410q78a01f.html"
      }
    ],
    "total": 164,
    "page": 1,
    "size": 100
  },
  "status": 1
}
```

**关键字段**:
- `list[]`: 通用 `SongInfo` 结构（`song_name` / `mix_song_id` / `artist_name` / `play_link`）
- `total`: 上游返回的歌曲总数（不含被过滤的屏蔽歌曲）

> **关于上游附带字段**：CLI 透传上游原始 JSON 字符串，响应里**可能**含其他字段（如 `hash`、`singer_id` 等），但 CLI 不解析、不保证存在。Agent 不要依赖未在 `SongInfo` 中列出的字段。

**特殊说明**:
- **屏蔽歌曲过滤**: 上游可能跳过被屏蔽的歌曲（不返回），`total` 不含被过滤项，`list` 长度可能小于 `size`
- **artist_name 拼接**: 多歌手时上游用 `/` 拼接（例如 `周杰伦/方文山`）
- **分页去重**: 上游按服务端数组下标分页，但歌曲可能在分页期间被增删，调用方需自行按 `mix_song_id` 去重
- **播放链接**: `play_link` 由服务端拿到 `mix_song_id` 后批量生成，单条失败不影响其他歌曲

---

## 11. 提交偏好

> 🔐 = 需要先登录

把用户对音乐偏好的调整（减少 / 屏蔽 / 增加 某位歌手、语种、曲风等）提交到上游推荐引擎，**服务端**先把 `name` 解析为上游 id（例如 singer → 歌手搜索取第 0 个结果的 `author_id`）再透传，上游处理后**返回一条确认话术 + 重新推荐的歌曲列表**。

适用于用户表达"最近想多听 XX 语种 / 不想再听 XX 歌手的 / 多推点 XX 曲风"等诉求的场景。

```bash
# 减少推荐某位歌手（weight 越小减得越多）
kugou-cli music submit-preference \
  --dimension singer --degree reduce \
  --name "周杰伦" --weight-ratio 0.5

# 屏蔽某类曲风
kugou-cli music submit-preference \
  --dimension genre --degree forbid \
  --weight-ratio 1.5

# 增加某语种
kugou-cli music submit-preference \
  --dimension language --degree add \
  --name "粤语" --weight-ratio 1.8
```

**参数**（全部为 flag，无位置参数）:

| 参数 | 必填 | 取值 | 说明 |
|------|------|------|------|
| `--dimension` | 是 | `singer` / `language` / `genre` / `ai` / `dj` / `fc` / `abs` / `old` | 偏好维度（强枚举） |
| `--degree` | 是 | `reduce`（减少）/ `forbid`（屏蔽）/ `add`（增加） | 操作类型（强枚举） |
| `--name` | 条件必填 | string | `singer` 传歌手名 / `language` 传语种名；其余维度**必须为空** |
| `--weight-ratio` | 是 | float64，范围 `(0, 2)` | 权重系数。`reduce` 配 `(0,1)` / `forbid` & `add` 配 `(1,2)` |
| `--area-code` | 否 | int | 地区码；不传时不出现在 body 中 |

**`name` 必填/必空规则**:

| `--dimension` | 是否需要 `--name` | 说明 |
|--------------|------------------|------|
| `singer` | **必填**（歌手名） | 服务端查歌手搜索取第 0 个结果 `author_id` |
| `language` | **必填**（语种名） | 服务端查下方「语种映射表」取 id |
| `genre` / `ai` / `dj` / `fc` / `abs` / `old` | **必须为空** | 服务端不取 name，传了会被 CLI 拦截 |

**`weight-ratio` 与 `--degree` 的配对**:

| `--degree` | 配对范围 | 不匹配时的处理 |
|-----------|---------|---------------|
| `reduce` | `(0, 1)` | CLI 给 warning（不阻断），最终可能服务端拒 |
| `forbid` | `(1, 2)` | CLI 给 warning（不阻断），最终可能服务端拒 |
| `add` | `(1, 2)` | CLI 给 warning（不阻断），最终可能服务端拒 |

> CLI 只做基础的 `(0, 2)` 范围校验 + 不匹配时的 warning；**业务侧具体配对由服务端校验**，避免本地硬规则与服务端不一致时把"reduce 0.99"这种边界值也堵掉。

**语种映射表**（`--dimension=language` 时 `--name` 取值）:

`国语` / `英语` / `粤语` / `纯音乐` / `韩语` / `日语` / `其他语种` / `小语种` / `方言` / `闽南语` / `俄语` / `伴奏` / `西班牙语` / `藏语` / `越南语` / `葡萄牙语` / `德语` / `泰语` / `意大利语` / `蒙古语`

**输出示例**:

```json
{
  "errcode": 0,
  "errmsg": "",
  "data": {
    "status": 801,
    "msg": "收到！将减少推荐歌手「周杰伦」的歌曲，猜你喜欢以下歌曲~",
    "list": [
      {
        "song_name": "稻香",
        "mix_song_id": "595244683",
        "artist_name": "周杰伦",
        "play_link": "https://www.kugou.com/mixsong/agent_gateway/xxx.html"
      }
    ]
  },
  "status": 1
}
```

**关键字段**:
- `data.status`: 上游 `msgtype`，取第一条确认话术对应的消息类型（如 `801`）
- `data.msg`: 上游确认话术（如「收到！将减少推荐歌手「周杰伦」的歌曲，猜你喜欢以下歌曲~」），**直接展示给用户**
- `data.list`: 重新推荐的歌曲列表，结构同通用 `SongInfo`（`song_name` / `mix_song_id` / `artist_name` / `play_link`）

**调用流程**（agent 必读）:

```
1. 解析用户意图：识别"减少 / 屏蔽 / 增加" + "对象（歌手 / 语种 / 曲风等）"
2. 按下表确定 dimension / degree / name：
   ┌────────────────────────────────────────┬──────────┬────────────┬────────────────┐
   │ 用户原话（例）                          │ dimension│ degree     │ name           │
   ├────────────────────────────────────────┼──────────┼────────────┼────────────────┤
   │ "少推点周杰伦的歌"                      │ singer   │ reduce     │ 周杰伦         │
   │ "别再给我推民谣了"                      │ genre    │ forbid     │ （空）         │
   │ "多来点粤语歌"                          │ language │ add        │ 粤语           │
   │ "屏蔽一下英文歌"                        │ language │ forbid     │ 英语           │
   └────────────────────────────────────────┴──────────┴────────────┴────────────────┘
3. 选 weight_ratio：
   - reduce → 0 < x < 1（值越小减得越多；常用 0.5）
   - forbid / add → 1 < x < 2（值越大越强；常用 1.5）
4. 调 submit-preference
5. 拿到响应后，**优先用 data.msg 展示确认话术**给用户；
   data.list 是重新推荐的歌曲列表，按 [§0.1 / §0.2 / §1](#1-搜索歌曲) 的展示规范呈现
```

**特殊说明**:
- **上游返回 SSE 流式**：响应体上游为多行 `data:` 流。服务端取**第一条**确认话术（`msgtype=801`）作为对外 `status`/`msg`，避免被后续推荐话术覆盖
- **歌曲组装**：`list` 中的 `mixsongid` 与「歌曲推荐」接口共用同一套组装逻辑（kmr 拉歌名/歌手/hash + `GenerateBatch` 生成播放链接）；未命中歌曲详情（audioMap miss）的条目会被跳过，因此最终 `list` 条数可能小于上游返回数量
- **name 解析**：`singer` / `language` 维度的 `name` 会在 logic 层被解析为上游 id 后透传，客户端只传 `name` 即可，不需要先去查歌手 id
- **name 输入规范**：用户口语里说"少推点老周"时，agent 应**询问清楚**再调用——上游 name 必须是服务端能识别的标准名（如"周杰伦"），不是昵称/简称
- **不是「保存为规则」**：本接口是**实时反馈**给推荐引擎，不会持久化为用户画像规则；同一歌手多次提交会**叠加效果**
- **不要主动调用**：必须用户**明确**表达偏好调整意愿时才调用（"少推点 XX" / "别再推 XX" / "多推点 XX"），禁止在用户仅说"推荐/搜歌/听歌"时主动改写用户偏好
- **改完偏好 → 主动问是否要听**：提交成功（`errcode: 0`）后，服务端已返回重新推荐的 `data.list`；agent 应**主动询问**用户"要按这个新偏好播放一些吗？"，等用户确认后**复用 `list[]` 里的 mix_song_id** 直接走 [`control play`](./control.md#1-play--播放指定歌曲) 等命令，不要再调一次 `recommend`

# 音乐命令 (music)

> 🔐 = 所有 music 命令都需要先登录

## 命令列表

| 命令 | 说明 |
|------|------|
| `kugou-cli music search <keyword>` | 搜索歌曲 |
| `kugou-cli music recommend daily` | 每日推荐 |
| `kugou-cli music recommend similar -s <song>` | 相似歌曲推荐 |
| `kugou-cli music favorites` | 我的收藏 |
| `kugou-cli music recent` | 最近播放 |
| `kugou-cli music stats` | 听歌统计 |
| `kugou-cli music charts <rank_id>` | 榜单 |
| `kugou-cli music create-playlist <name>` | 创建歌单（可附加歌曲） |

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

## 4. 我的收藏

```bash
kugou-cli music favorites
kugou-cli music favorites --page 1 --size 20
```

**参数**:
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20

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

## 5. 最近播放

```bash
kugou-cli music recent
kugou-cli music recent --page 1 --size 20
```

**参数**:
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20

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

## 6. 听歌统计

```bash
kugou-cli music stats                    # 默认查当月
kugou-cli music stats --date-type 1 --date 20260501  # 指定周查询
```

**参数**:
- `--date-type`: 日期类型，0=日、1=周、2=月，默认 2（月）
- `--date`: 查询日期，YYYYMMDD 格式，如 "20260501"（不填默认当月第一天）
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

## 7. 榜单

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
- `<rank_id>`: 榜单 ID（必填）
- `--page`: 页码，默认 1
- `--size`: 每页数量，默认 20

---

## 8. 创建歌单

> 🔐 = 需要先登录

### 调用原则（AI 必读）

1. **被动调用**：必须用户**明确**要求创建歌单时才调用本命令，禁止在用户仅说"推荐/搜歌/听歌"时主动创建
2. **主动询问**：当通过搜索、推荐（猜你喜欢/相似/文本）等方式给出一批歌曲后，**必须**询问用户"是否需要将当前这批歌曲创建为歌单"，等用户确认后再执行 `create-playlist --songs "<mix_song_id 列表>"`
3. **示例化推荐**：询问时建议给出歌单名建议（如"跑步歌单"、"周杰伦精选"），让用户更容易确认

### 接口说明

创建一个新的自建歌单，并可选择在创建后往歌单里添加歌曲。

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

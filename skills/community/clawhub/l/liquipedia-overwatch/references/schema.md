# Liquipedia Overwatch — 本地缓存数据规范

## 概述

所有通过爬取获取的守望先锋数据，都应以结构化格式保存到本地 `/workspace/liquipedia-cache/` 目录。
本地缓存是数据的唯一真实来源（Single Source of Truth），再次查询时**优先读本地，再决定是否重新抓取**。

## 数据源分工说明

| 数据类型 | 主要来源 | 辅助来源 | 说明 |
|---|---|---|---|
| hero_picks | **OWTV.gg** | — | ⚠️ Liquipedia 完全无此数据，必须从 OWTV.gg 提取 |
| matches/schedule | **OWTV.gg** | Liquipedia | OWTV 实时赛程为主，Liquipedia 补充历史赛果 |
| 战队阵容 | **OWTV.gg** | Liquipedia | OWTV 新闻更快更完整，Liquipedia 补充历史阵容 |
| 选手档案 | Liquipedia | — | 必须从 Liquipedia 提取 |
| 赛事信息 | Liquipedia | OWTV.gg | Liquipedia 含完整赛制和奖金数据 |
| 奖金统计 | Liquipedia | — | 必须从 Liquipedia 提取 |

**根字段要求：**
- `schema_version`：必填，格式 `"1.0"`
- `source_url`：必填，缓存该条数据的原始页面 URL
- `source`：必填，值为 `"liquipedia_net"` / `"owtv_gg"` / `"google_search"`
- `last_updated`：必填，ISO8601 UTC 时间戳
- `cached_at`：自动由 cache_manager.py 写入，无需手动填写

---

## 目录结构

```
/workspace/liquipedia-cache/
├── index.json                          # 主索引（所有缓存文件的清单）
├── tournaments/
│   ├── owcs-2026-china-s1.json         # OWCS 中国赛区 Stage 1
│   ├── owcs-2026-korea-s1.json
│   ├── owcs-2026-na-s1.json
│   ├── owwc-2026.json
│   └── ...
├── teams/
│   ├── weibo-gaming.json               # 微博电竞
│   ├── jdg.json                        # JDG
│   ├── all-gamers.json
│   └── ...
├── players/
│   ├── guxue.json
│   ├── leave.json
│   └── ...
├── hero_picks/
│   ├── weibo-gaming-2026-s1.json      # 微博电竞英雄选取数据
│   ├── jdg-2026-s1.json
│   └── ...
├── matches/
│   ├── owcs-2026-china-s1-swiss-r1.json   # 瑞士轮第1轮
│   ├── owcs-2026-china-s1-swiss-r2.json
│   └── ...
└── earnings/
    ├── player-earnings-2026.json
    └── team-earnings-2026.json
```

---

## index.json — 主索引格式

```json
{
  "version": "1.0",
  "last_updated": "2026-03-20T13:00:00Z",
  "sources": {
    "liquipedia_net": "UNAVAILABLE",
    "owtv_gg": "PRIMARY",
    "google_search": "PRIMARY"
  },
  "files": {
    "tournaments/owcs-2026-china-s1": {
      "path": "tournaments/owcs-2026-china-s1.json",
      "url_source": "https://owtv.gg/news/owcs-2026-stage-1-china-preview",
      "last_fetched": "2026-03-20T08:00:00Z",
      "data_hash": "sha256:abc123..."
    },
    "teams/weibo-gaming": {
      "path": "teams/weibo-gaming.json",
      "url_source": "https://owtv.gg/news/once-again-announce-roster-for-2026",
      "last_fetched": "2026-03-19T20:00:00Z",
      "data_hash": "sha256:def456..."
    },
    "hero_picks/weibo-gaming-2026-s1": {
      "path": "hero_picks/weibo-gaming-2026-s1.json",
      "url_source": "https://owtv.gg/news/grand-finals-recap-owcs-pre-season-bootcamp",
      "last_fetched": "2026-03-20T08:00:00Z",
      "data_hash": "sha256:ghi789..."
    }
  }
}
```

**index.json 的作用：**
- 快速判断某类数据是否已有缓存
- 记录数据来源 URL，便于核对
- 记录哈希值，可检测数据是否过时

---

## 各数据类型 JSON Schema

### 1. 战队数据（teams/{team-id}.json）

```json
{
  "schema_version": "1.0",
  "source": "owtv_gg",
  "team_id": "weibo-gaming",
  "team_name_zh": "微博电竞",
  "team_name_en": "Weibo Gaming",
  "region": "China",
  "league": "OWCS 2026",
  "roster": {
    "tank": [
      { "player_id": "Guxue", "name_zh": "徐秋林", "nationality": "CN", "joined": "2025-04-30" },
      { "player_id": "SUNZO", "name_zh": "陈成", "nationality": "CN", "joined": "2026-01-01" }
    ],
    "dps": [
      { "player_id": "Leave", "name_zh": "黄昕", "nationality": "CN", "joined": "2021-01-01" },
      { "player_id": "Shy", "name_zh": "郑杨杰", "nationality": "CN", "joined": "2021-01-01" }
    ],
    "support": [
      { "player_id": "LeeSooMin", "name_zh": "李秀敏", "nationality": "KR", "joined": "2026-01-01" },
      { "player_id": "MAKA", "name_zh": "吴恩实", "nationality": "KR", "joined": "2026-01-01" }
    ]
  },
  "coaches": [
    { "coach_id": "Dongsu", "role": "Head Coach", "nationality": "KR" },
    { "coach_id": "Daemin", "role": "Coach", "nationality": "KR" }
  ],
  "changes": {
    "new_players": [
      { "player_id": "SUNZO", "from": "Team CC" },
      { "player_id": "LeeSooMin", "from": "All Gamers Global" }
    ],
    "departed_players": [
      { "player_id": "Mew", "to": "Sister Team" },
      { "player_id": "Mmonk", "to": "Sister Team" }
    ]
  },
  "last_updated": "2026-03-20T08:00:00Z",
  "source_url": "https://owtv.gg/news/once-again-announce-roster-for-2026"
}
```

> `source` 字段：阵容公告从 OWTV.gg 提取时填 `"owtv_gg"`；从 Liquipedia 提取时填 `"liquipedia_net"`；从混合来源时主来源优先。

### 2. 赛事数据（tournaments/{tournament-id}.json）

```json
{
  "schema_version": "1.0",
  "tournament_id": "owcs-2026-china-s1",
  "name_zh": "OWCS 2026 中国赛区 Stage 1",
  "name_en": "OWCS 2026 China Stage 1",
  "region": "China",
  "tier": "A",
  "date_start": "2026-03-21",
  "date_end": "2026-04-25",
  "prize_pool": "USD 101,907",
  "format": "Swiss Stage (Bo3) → Regular Season (Bo3) → Playoffs (Bo5)",
  "teams": [
    { "team_id": "weibo-gaming", "seed": 1 },
    { "team_id": "jdg", "seed": 2 }
  ],
  "current_stage": "Swiss Stage",
  "swiss_standings": {
    "round_1": [
      { "team_a": "weibo-gaming", "team_b": "naive-piggy", "result": "WBG 2-0 NP" }
    ]
  },
  "last_updated": "2026-03-21T00:00:00Z",
  "source_url": "https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1"
}
```

### 3. 英雄选取数据（hero_picks/{team-id}-{event}.json）

> ⚠️ **数据来源：必须使用 OWTV.gg**。Liquipedia 无此数据，无需访问。
> `source` 字段固定填 `"owtv_gg"`。
> schema_version 升级至 `"2.0"`，新增 `overall_stats`、`damage_dealt`、`healing`、`player_match_totals` 等选手数据字段。

```json
{
  "schema_version": "2.0",
  "source": "owtv_gg",
  "team_id": "weibo-gaming",
  "event_id": "owcs-2026-china-s1",
  "match_id": "1233",
  "overall_stats": {
    "WBG": { "kills": 45, "deaths": 22, "assists": 18 },
    "NP":  { "kills": 22, "deaths": 45, "assists": 9 }
  },
  "matches": [
    {
      "date": "2026-03-21",
      "opponent": "naive-piggy",
      "event": "Swiss Round 1",
      "score": "3-0",
      "maps": [
        {
          "map": "Busan",
          "result": "WBG Win",
          "duration": "8:32",
          "ban_WBG": "Zarya",
          "ban_NP": "D.Va",
          "WBG": {
            "tank":  { "player": "Guxue",    "hero": "Domina",  "damage_dealt": 12450, "damage_blocked": 8320, "kills": 8,  "deaths": 3,  "assists": 5,  "ult_used": 4 },
            "dps1":  { "player": "Leave",     "hero": "Tracer",  "damage_dealt": 18920, "kills": 10, "deaths": 2,  "melee": 1, "ult_used": 3 },
            "dps2":  { "player": "shy",       "hero": "Sojourn", "damage_dealt": 22100, "kills": 9,  "deaths": 4,  "ult_used": 4 },
            "sup1":  { "player": "LeeSooMin", "hero": "Kiriko",  "healing": 15200, "damage_dealt": 4200, "kills": 3, "deaths": 2, "ults_given": 5 },
            "sup2":  { "player": "MAKA",      "hero": "Lúcio",   "healing": 9800,  "damage_dealt": 2100, "kills": 2, "deaths": 3, "sound_barrier": 2 }
          },
          "NP": {
            "tank":  { "player": "Unknown",  "hero": "D.Va",    "damage_dealt": 7400,  "damage_blocked": 5100, "kills": 4, "deaths": 8 },
            "dps1":  { "player": "Unknown",  "hero": "Tracer",  "damage_dealt": 11300, "kills": 5, "deaths": 5 },
            "dps2":  { "player": "Unknown",  "hero": "Sojourn", "damage_dealt": 9800,  "kills": 4, "deaths": 6 },
            "sup1":  { "player": "Unknown",  "hero": "Kiriko",  "healing": 8200,  "damage_dealt": 1800, "kills": 2, "deaths": 7 },
            "sup2":  { "player": "Unknown",  "hero": "Lúcio",   "healing": 6100,  "damage_dealt": 900,  "kills": 1, "deaths": 8 }
          }
        }
      ]
    }
  ],
  "hero_frequency": {
    "tank":    { "Domina": 10, "D.Va": 3, "Winston": 2 },
    "dps":     { "Tracer": 10, "Sojourn": 9, "Cassidy": 6, "Vendetta": 4 },
    "support": { "Kiriko": 10, "Lúcio": 7, "Brigitte": 4, "Wuyang": 3 }
  },
  "player_match_totals": {
    "Guxue":     { "team": "WBG", "hero": "Domina",  "kills": 8,  "deaths": 3,  "damage_dealt": 12450, "damage_blocked": 8320, "healing": 0 },
    "Leave":     { "team": "WBG", "hero": "Tracer",   "kills": 10, "deaths": 2,  "damage_dealt": 18920, "damage_blocked": 0,    "healing": 0 },
    "shy":       { "team": "WBG", "hero": "Sojourn",  "kills": 9,  "deaths": 4,  "damage_dealt": 22100, "damage_blocked": 0,    "healing": 0 },
    "LeeSooMin": { "team": "WBG", "hero": "Kiriko",   "kills": 3,  "deaths": 2,  "damage_dealt": 4200,  "damage_blocked": 0,    "healing": 15200 },
    "MAKA":      { "team": "WBG", "hero": "Lúcio",    "kills": 2,  "deaths": 3,  "damage_dealt": 2100,  "damage_blocked": 0,    "healing": 9800 }
  },
  "last_updated": "2026-03-22T08:00:00Z",
  "source_url": "https://owtv.gg/matches/1233"
}
```

**字段说明（OWTV matches/{id} 特有）：**

| 字段 | 说明 | 适用英雄/位置 |
|---|---|---|
| `overall_stats` | 整场比赛队伍合计 K/D/A | 全位置 |
| `damage_dealt` | 造成伤害总量 | 全位置 |
| `damage_blocked` | 抵挡伤害总量 | Tank 为主 |
| `healing` | 治疗量 | Support |
| `ults_given` | 给出的终极技能（辅助特有） | Support |
| `sound_barrier` | 声屏障使用次数 | Lúcio |
| `railgun_kills` | 轨道炮击杀数 | Sojourn |
| `melee` | 近战击杀 | 全位置 |
| `player_match_totals{}` | 选手层面汇总（跨地图合计） | 全位置 |

### 4. 选手数据（players/{player-id}.json）

```json
{
  "schema_version": "1.0",
  "player_id": "Guxue",
  "name_zh": "徐秋林",
  "nationality": "CN",
  "role": "Tank",
  "current_team": "weibo-gaming",
  "teams_history": [
    { "team_id": "weibo-gaming", "from": "2025-04-30", "to": null },
    { "team_id": "once-again", "from": "2021-01-01", "to": "2025-04-29" }
  ],
  "achievements": [
    { "event": "OWCS 2025 China Stage 1", "result": "Champion" },
    { "event": "OWCS 2025 China Stage 2", "result": "Champion" }
  ],
  "earnings_total": "USD 50,000",
  "heroes_main": ["Winston", "Reinhardt", "Zarya"],
  "last_updated": "2026-03-19T20:00:00Z",
  "source_url": "https://liquipedia.net/overwatch/Guxue"
}
```

### 5. 比赛结果（matches/{event-id}-{round}.json）

```json
{
  "schema_version": "1.0",
  "event_id": "owcs-2026-china-s1",
  "stage": "Swiss Stage",
  "round": 1,
  "date": "2026-03-21",
  "matches": [
    {
      "id": "owcs-2026-china-s1-r1-m1",
      "team_a": "weibo-gaming",
      "team_b": "naive-piggy",
      "score_a": 2,
      "score_b": 0,
      "maps": [
        { "map": "Busan", "winner": "WBG", "score_a": 2, "score_b": 0 }
      ],
      "result": "WBG Win"
    },
    {
      "id": "owcs-2026-china-s1-r1-m2",
      "team_a": "jdg",
      "team_b": "solus-victorem",
      "score_a": 2,
      "score_b": 1,
      "maps": [
        { "map": "Lijiang Tower", "winner": "JDG", "score_a": 2, "score_b": 1 }
      ],
      "result": "JDG Win"
    }
  ],
  "last_updated": "2026-03-21T12:00:00Z",
  "source_url": "https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1"
}
```

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|---|---|---|
| 战队 | `{team-id}.json` | `weibo-gaming.json` |
| 选手 | `{player-id}.json` | `guxue.json` |
| 赛事 | `{event-id}.json` | `owcs-2026-china-s1.json` |
| 英雄选取 | `{team-id}-{event-id}.json` | `weibo-gaming-owcs-2026-s1.json` |
| 比赛 | `{event-id}-{stage}-{round}.json` | `owcs-2026-china-s1-swiss-r1.json` |
| 奖金 | `player-earnings-{year}.json` | `player-earnings-2026.json` |

**team-id 规范（小写，横线分隔）：**
```
weibo-gaming      → 微博电竞
jdg                → JDG
all-gamers         → 爱电竞
solus-victorem     → SV
naive-piggy        → NP
homie-e            → Homie E
deg                → DEG
milk-tea           → Milk Tea
```

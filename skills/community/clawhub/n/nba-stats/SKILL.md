---
name: NBA数据服务
description: 一个提供实时和历史NBA数据的模型上下文协议服务器，包括球员统计、比赛得分、球队信息和高级分析。
version: 1.0.0
---

# NBA数据服务

一个提供实时和历史NBA数据的模型上下文协议服务器，包括球员统计、比赛得分、球队信息和高级分析。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Server version + runtime settings (timeouts, retries, cache, concurrency). | `scripts.tools.get_server_info` |
| Resolve team name/city/nickname → team_id. | `scripts.tools.resolve_team_id` |
| Resolve player name → player_id (official stats endpoint). | `scripts.tools.resolve_player_id` |
| Find game_id by date and matchup. If date omitted, finds most recent matchup via schedule. | `scripts.tools.find_game_id` |
| Today's games. | `scripts.tools.get_todays_scoreboard` |
| Games for a specific date. | `scripts.tools.get_scoreboard_by_date` |
| Detailed game info for a specific game_id. | `scripts.tools.get_game_details` |
| Full box score for a game_id. | `scripts.tools.get_box_score` |
| Search players by name substring. | `scripts.tools.search_players` |
| Player bio/profile info. | `scripts.tools.get_player_info` |
| Player stats for a season. | `scripts.tools.get_player_season_stats` |
| Player game log for a season. | `scripts.tools.get_player_game_log` |
| Player career totals/averages. | `scripts.tools.get_player_career_stats` |
| Player hustle stats. | `scripts.tools.get_player_hustle_stats` |
| League leaders in a hustle stat category. | `scripts.tools.get_league_hustle_leaders` |
| Opponent FG% when defended by player. | `scripts.tools.get_player_defense_stats` |
| All-time leaders for a stat category. | `scripts.tools.get_all_time_leaders` |
| All teams. | `scripts.tools.get_all_teams` |
| Team roster. | `scripts.tools.get_team_roster` |
| League standings. | `scripts.tools.get_standings` |
| Current season per-game league leaders for a stat category (Points/Assists/Rebounds/etc.). | `scripts.tools.get_league_leaders` |
| Team upcoming schedule. | `scripts.tools.get_schedule` |
| Player awards/accolades. | `scripts.tools.get_player_awards` |
| Major awards for a season. | `scripts.tools.get_season_awards` |
| Shot chart data summary. | `scripts.tools.get_shot_chart` |
| Shooting splits summary. | `scripts.tools.get_shooting_splits` |
| Play-by-play summary. | `scripts.tools.get_play_by_play` |
| Rotation/substitution summary. | `scripts.tools.get_game_rotation` |
| Player advanced metrics summary. | `scripts.tools.get_player_advanced_stats` |
| Team advanced metrics summary. | `scripts.tools.get_team_advanced_stats` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_server_info
工具描述：Server version + runtime settings (timeouts, retries, cache, concurrency).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.resolve_team_id
工具描述：Resolve team name/city/nickname → team_id.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|limit|integer|false| |null|

---

## scripts.tools.resolve_player_id
工具描述：Resolve player name → player_id (official stats endpoint).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|active_only|boolean|false| |null|
|limit|integer|false| |null|

---

## scripts.tools.find_game_id
工具描述：Find game_id by date and matchup. If date omitted, finds most recent matchup via schedule.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|false| |null|
|home_team|string|false| |null|
|away_team|string|false| |null|
|team|string|false| |null|
|lookback_days|integer|false| |null|
|limit|integer|false| |null|

---

## scripts.tools.get_todays_scoreboard
工具描述：Today's games.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_scoreboard_by_date
工具描述：Games for a specific date.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|true| |null|

---

## scripts.tools.get_game_details
工具描述：Detailed game info for a specific game_id.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|game_id|string|true| |null|

---

## scripts.tools.get_box_score
工具描述：Full box score for a game_id.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|game_id|string|true| |null|

---

## scripts.tools.search_players
工具描述：Search players by name substring.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|

---

## scripts.tools.get_player_info
工具描述：Player bio/profile info.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|

---

## scripts.tools.get_player_season_stats
工具描述：Player stats for a season.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_player_game_log
工具描述：Player game log for a season.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_player_career_stats
工具描述：Player career totals/averages.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|

---

## scripts.tools.get_player_hustle_stats
工具描述：Player hustle stats.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_league_hustle_leaders
工具描述：League leaders in a hustle stat category.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|stat_category|string|false| |null|
|season|string|false| |null|

---

## scripts.tools.get_player_defense_stats
工具描述：Opponent FG% when defended by player.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_all_time_leaders
工具描述：All-time leaders for a stat category.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|stat_category|string|false| |null|
|limit|integer|false| |null|

---

## scripts.tools.get_all_teams
工具描述：All teams.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_team_roster
工具描述：Team roster.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|team_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_standings
工具描述：League standings.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|season|string|false| |null|

---

## scripts.tools.get_league_leaders
工具描述：Current season per-game league leaders for a stat category (Points/Assists/Rebounds/etc.).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|stat_type|string|false| |Stat type like 'Points', 'Assists', 'Rebounds', 'Steals', 'Blocks', 'FG%', '3P%', 'FT%'|
|season|string|false| |Season in format YYYY-YY (defaults to current season)|
|limit|integer|false| |Number of leaders to return (default 10, max 50)|

---

## scripts.tools.get_schedule
工具描述：Team upcoming schedule.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|team_id|string|true| |null|
|days_ahead|integer|false| |null|

---

## scripts.tools.get_player_awards
工具描述：Player awards/accolades.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|

---

## scripts.tools.get_season_awards
工具描述：Major awards for a season.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|season|string|false| |null|

---

## scripts.tools.get_shot_chart
工具描述：Shot chart data summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|
|game_id|string|false| |null|

---

## scripts.tools.get_shooting_splits
工具描述：Shooting splits summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_play_by_play
工具描述：Play-by-play summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|game_id|string|true| |null|
|start_period|integer|false| |null|
|end_period|integer|false| |null|

---

## scripts.tools.get_game_rotation
工具描述：Rotation/substitution summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|game_id|string|true| |null|

---

## scripts.tools.get_player_advanced_stats
工具描述：Player advanced metrics summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|player_id|string|true| |null|
|season|string|false| |null|

---

## scripts.tools.get_team_advanced_stats
工具描述：Team advanced metrics summary.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|team_id|string|true| |null|
|season|string|false| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据
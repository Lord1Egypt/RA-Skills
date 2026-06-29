# 比赛详情

## 脚本：`scripts/worldcup-match.js`

从百度体育比赛详情页（`https://tiyu.baidu.com/al/live/detail?matchId=...&tab=...`）抓取 6 个 tab 的数据。

## 命令

```bash
node scripts/worldcup-match.js info <matchId>          # 比赛基本信息
node scripts/worldcup-match.js analysis <matchId>      # 分析数据
node scripts/worldcup-match.js lineup <matchId>        # 阵容数据
node scripts/worldcup-match.js live <matchId>          # 赛况数据
node scripts/worldcup-match.js stats <matchId>         # 统计数据
node scripts/worldcup-match.js odds <matchId>          # 指数数据
node scripts/worldcup-match.js detail <matchId> [tab]  # 完整详情（默认分析）
```

## 各 tab 数据说明

### info - 比赛基本信息（所有比赛）

| 字段 | 类型 | 说明 |
|------|------|------|
| game | string | 赛事名称 |
| matchDesc | string | 完整阶段描述（如 `世界杯小组赛B组第1轮`） |
| matchStage | string | 阶段简称 |
| dateFormat | string | 友好日期（`明天 03:00`） |
| time | string | 北京时间 HH:mm |
| timestamp | number | UTC 时间戳 |
| startTime | string | ISO 8601 时间 |
| matchStatusText | string | 状态文案 |
| vs | string | 比分字符串 |
| homeTeam / awayTeam | object | 主/客队信息（name/score/logo/rank/teamId） |
| liveList | array | 直播源列表 |

> 进行中的比赛页面用 `headLive` 字段，脚本已自动兼容。

### analysis - 分析数据

| 字段 | 类型 | 说明 |
|------|------|------|
| intelligence[].title | string | "有利情报" / "不利情报" |
| intelligence[].homeTeamPoints | array | 主队相关情报点 |
| intelligence[].awayTeamPoints | array | 客队相关情报点 |
| records[] | array | 历史战绩（H2H+双方近况） |
| ├─ title | string | "历史战绩"/"卡塔尔近期战绩"等 |
| ├─ probability | array | 胜率/赢盘率/大球率 |
| └─ matches | array | 近期比赛列表 |
| prediction.sampleSize | string | 相似赔率历史样本数 |
| prediction.homeWinRate | string | 主队本场胜率 |
| prediction.awayWinRate | string | 客队本场胜率 |
| prediction.similarOddsHistory | object | 相似赔率下历史胜负平比例 |
| guess.options | array | 猜胜负各选项的人数和占比 |

### lineup - 阵容数据（开赛前确认）

| 字段 | 类型 | 说明 |
|------|------|------|
| confirmed | boolean | 阵容是否已确认 |
| court | string | 比赛场地 |
| referee | string | 主裁判 |
| home / away | object | 主/客队阵容信息 |
| ├─ formation | string | 阵型（如 `4-1-2-3`） |
| ├─ starter[] | array | 首发球员（name/number/position/coordinate/nation/playerId） |
| └─ substitute[] | array | 替补球员 |

### live - 赛况数据（已结束比赛）

| 字段 | 类型 | 说明 |
|------|------|------|
| venue | object | 比赛场地（name/city/capacity） |
| narrative[] | array | 文字播报列表（约 51 条赛前+赛中描述） |
| incidents[] | array | 比赛事件（type/text/passedTime/team/direction） |
| events | object | 时间轴事件 |

### stats - 统计数据（已结束比赛）

| 字段 | 类型 | 说明 |
|------|------|------|
| items[] | array | 10项技术统计 |
| ├─ name | string | 进球/控球率/射正/角球/黄牌/红牌等 |
| ├─ home | number/string | 主队数值 |
| └─ away | number/string | 客队数值 |

### odds - 指数数据（所有比赛）

| 字段 | 类型 | 说明 |
|------|------|------|
| asyncTime | number | 赔率轮询间隔（毫秒） |
| bookmakers[] | array | 博彩公司组（约 4 家） |
| └─ datas[] | array | 盘口数据（initial/now/history） |

## 模块导出

```js
const {
  fetchMatchDetail,
  parseHeader, parseAnalysis, parseLineup, parseLive, parseStats, parseOdds
} = require('./scripts/worldcup-match.js');
```
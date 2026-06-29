# 排名数据

## 脚本：`scripts/worldcup-rankings.js`

从百度体育赛事主页（`https://tiyu.baidu.com/al/match?match=世界杯&tab=...`）抓取 4 个排名 tab。

## 4 个 tab 对应命令

| Tab | 命令 | 数据来源 API |
|-----|------|-------------|
| 排名 | `standings` | `go/api/header?rankChildTab=teamRank` |
| 球队榜 | `team-rank` | （复用 standings 数据） |
| 球员榜 | `players <分类>` | `go/api/header?rankChildTab=playerRank&tabId=N` |
| FIFA排名 | `fifa [N]` | `go/api/header?rankChildTab=fifaRank` |

## 命令

```bash
node scripts/worldcup-rankings.js standings          # 12组积分榜
node scripts/worldcup-rankings.js fifa 20           # FIFA 排名前20
node scripts/worldcup-rankings.js fifa              # FIFA 排名前50
node scripts/worldcup-rankings.js players 进球      # 射手榜
node scripts/worldcup-rankings.js players 助攻 10   # 助攻榜前10
node scripts/worldcup-rankings.js team-rank         # 球队榜（同积分榜）
node scripts/worldcup-rankings.js categories        # 球员榜可用分类
```

## 球员榜可用分类

```
进球 / 助攻 / 射门 / 射正
过人 / 过人成功 / 任意球 / 击中门框
快攻 / 快攻射门 / 丢失球权
解围 / 有效阻挡 / 拦截 / 抢断
1对1拼抢 / 1对1拼抢成功
拳击球 / 守门员出击 / 守门员出击成功 / 高空出击
传球 / 传球成功 / 关键传球
传中球 / 传中球成功 / 长传 / 成功长传 / 传球被断
红牌 / 黄牌 / 犯规 / 被侵犯 / 越位
```

> 注：当前 API 对所有 tabId 返回相同的射手榜数据。赛事初期其它分类数据未产生。

## 数据字段

### 积分榜（standings）

| 字段 | 类型 | 说明 |
|------|------|------|
| updateTime | string | 更新时间 |
| columns | array | 列定义（球队名称/场次/胜平负/进失/积分） |
| groups[] | array | 12 个小组 |
| └─ list[] | array | 4 支球队（按名次排序） |
| ├─ teamId | string | teamId |
| ├─ teamName | string | 球队名称 |
| ├─ status | string | "晋级32强" / "晋级待定" |
| ├─ isQualified | boolean | 是否已晋级（蓝标） |
| ├─ isRelegated | boolean | 是否已淘汰（红标） |
| ├─ played | string | 已赛场次 |
| ├─ winDrawLoss | string | 胜/平/负（如 "1/0/0"） |
| ├─ goals | string | 进/失（如 "2/0"） |
| └─ points | string | 积分 |

### FIFA 排名（fifa）

| 字段 | 类型 | 说明 |
|------|------|------|
| rankings[].rank | string | 当前排名 |
| rankings[].teamId | string | teamId |
| rankings[].teamName | string | 国家名 |
| rankings[].points | string | FIFA 积分 |
| rankings[].positionChanged | string | 排名变化（正数=上升，负数=下降） |

### 球员榜（players）

| 字段 | 类型 | 说明 |
|------|------|------|
| statsName | string | 榜单名（如"射手榜"） |
| players[].rank | number | 排名 |
| players[].playerId | string | playerId |
| players[].playerName | string | 球员名 |
| players[].team | string | 球队名 |
| players[].position | string | 位置 |
| players[].score | string | 数值（进球数/助攻数等） |
| players[].penaltyValue | string | 点球数 |

## 模块导出

```js
const {
  fetchGroupStandings,
  fetchFifaRankings,
  fetchPlayerRankings,
  fetchKnockoutBracket,
  getPlayerTabNames
} = require('./scripts/worldcup-rankings.js');
```

## 已知限制

- 球员榜 API 对所有 tabId 返回相同数据（赛事初期只有射手有数据）
- 球队榜 tab 的实际数据通过 12 组积分榜呈现
- 淘汰赛对阵图在淘汰赛比赛开打后才会激活

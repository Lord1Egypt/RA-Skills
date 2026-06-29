# 跨脚本组合使用

各脚本通过 `teamId` 和 `matchId` 互相连接，下面是常用组合用法。

## 常用工作流

### 1. 球队名 → 球队赛程 → 比赛详情

```js
const { findTeamByName, loadTeams } = require('./scripts/worldcup-teams.js');
const { fetchAllSchedule, filterByTeam } = require('./scripts/worldcup-schedule.js');
const { fetchMatchDetail, parseLineup } = require('./scripts/worldcup-match.js');

(async () => {
  // 1. 查 teamId
  const data = loadTeams();
  const team = findTeamByName(data, '加拿大');
  
  // 2. 查该球队的赛程
  const schedule = await fetchAllSchedule();
  const teamMatches = filterByTeam(schedule, team.teamName);
  
  // 3. 选一场比赛查详情
  const matchId = teamMatches[0].matchId;
  const lineup = await fetchMatchDetail(matchId, '阵容');
  console.log(lineup.tabData);
})();
```

### 2. 今天比赛 → 找正在进行的 → 实时赛况

```js
const { fetchAllSchedule, filterByDateKeyword } = require('./scripts/worldcup-schedule.js');
const { fetchMatchDetail } = require('./scripts/worldcup-match.js');

(async () => {
  const all = await fetchAllSchedule();
  const today = filterByDateKeyword(all, '今天');
  const live = today.filter(m => m.statusId === '1');
  
  for (const m of live) {
    const detail = await fetchMatchDetail(m.matchId, '赛况');
    console.log(`${m.homeTeam} vs ${m.awayTeam} - 比分 ${m.vs}`);
  }
})();
```

### 3. 球队阵容（team 阵容 + match 首发）

球队阵容（`worldcup-team.js lineup`）= 全部 26 人名单
比赛阵容（`worldcup-match.js lineup`）= 当场比赛首发 11 + 替补

```js
// 查加拿大队的全部球员
const teamLineup = await fetchTeamData('35779c25e9dec553f154e9d6286925e6', '阵容');

// 查某场比赛的首发
const matchLineup = await fetchMatchDetail('5LiW55WM...', '阵容');
const starters = matchLineup.tabData.home.starter;
```

### 4. 球队赛程 vs 比赛赛程

- **球队赛程**（`worldcup-team.js schedule`）：包括世界杯+友谊赛+其他赛事
- **比赛赛程**（`worldcup-schedule.js`）：仅世界杯赛程（带 subTab 切换）

```js
// 查该球队所有赛事
const teamSchedule = await fetchTeamData(teamId, '赛程');
const allMatches = Object.values(teamSchedule.tabData.competitions).flatMap(c => c.matches);

// 仅查世界杯赛程（用于赛事内）
const worldCupOnly = teamSchedule.tabData.competitions['世界杯'].matches;
```

## matchId 编解码

```js
const { decodeMatchId } = require('./scripts/worldcup-schedule.js');

const matchId = '5LiW55WM5p2vIzIwMjYtMDYtMTIj5aKo6KWsprit5ZOldnPljZfpnZ4=';
const decoded = decodeMatchId(matchId);
// 世界杯_2026-06-12_墨西哥vs南非
```

## 团队配置反向查找

通过 `teamId` 找到球队在 `teams.json` 中的位置：

```js
const { loadTeams } = require('./scripts/worldcup-teams.js');
const data = loadTeams();
for (const [group, teams] of Object.entries(data.groups)) {
  for (const t of teams) {
    if (t.teamId === '35779c25e9dec553f154e9d6286925e6') {
      console.log(`${t.teamName} 在 ${group} 组，第 ${t.position} 位`);
    }
  }
}
```

## 数据流概览

```
teams.json (静态)
   │
   ▼ teamId
worldcup-team.js ────→ 球队资料/赛程/阵容/历史成绩/数据
   │
   │ teamName                              │ playerId
   ▼                                       ▼
worldcup-schedule.js ──→ matchId    worldcup-player.js ──→ 球员资料/动态/数据/赛程
   │
   ▼
worldcup-match.js ────→ 比赛分析/阵容/赛况/统计/指数
```

## 球员数据流

球队阵容里的每个球员都有 `playerId`，可以联动到球员详情页：

```js
// 1. 从球队阵容拿所有球员
const { fetchTeamData } = require('./scripts/worldcup-team.js');
const { fetchPlayerData } = require('./scripts/worldcup-player.js');

(async () => {
  const team = await fetchTeamData('d885ec68c7b46dbfd4a8f6e41d577ba0', '阵容');
  const players = team.tabData.players.flatMap(g => g.players);
  
  // 2. 逐个查球员详情
  for (const p of players.slice(0, 3)) {
    const info = await fetchPlayerData(p.playerId, '资料');
    console.log(`${p.name} - 评分:${info.tabData.ability.overall}`);
  }
})();
```
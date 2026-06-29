# 球队配置（静态数据）

48 支球队的分组配置保存在 `data/teams.json`，是其他脚本查找 `teamId` 的基础。

## 脚本：`scripts/worldcup-teams.js`

### 列出所有48支球队

```bash
node scripts/worldcup-teams.js list
```

### 查询指定小组球队

```bash
node scripts/worldcup-teams.js group A
node scripts/worldcup-teams.js group L
```

### 按名称查找球队（返回 teamId）

```bash
node scripts/worldcup-teams.js find 韩国
node scripts/worldcup-teams.js find 阿根廷
```

### 查看赛事基本信息

```bash
node scripts/worldcup-teams.js info
```

### 列出东道主球队

```bash
node scripts/worldcup-teams.js hosts
```

### 列出指定档位的球队

```bash
node scripts/worldcup-teams.js pot 1
node scripts/worldcup-teams.js pot 4
```

## 数据结构

**teams.json 顶层字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| tournament | string | 赛事名称（中文） |
| tournamentEn | string | 赛事名称（英文） |
| season | number | 赛季年份 |
| hostCountries | array | 东道主国家列表 |
| totalTeams | number | 总参赛球队数（48） |
| totalGroups | number | 总分组数（12） |
| teamsPerGroup | number | 每组球队数（4） |
| matchUrl | string | 百度体育赛事主页URL |
| rankingsUrl | string | 百度体育排名页URL |
| pot | object | 4个档位的球队名列表 |
| groups | object | 12个小组的球队配置（A-L） |

**球队对象字段（groups[].teams[]）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| position | number | 组内位置（1-4） |
| teamName | string | 球队中文名称 |
| teamId | string | 百度体育球队ID |
| pot | number | 分档（1-4） |
| isHost | boolean | 是否东道主 |
| qualifiedTop32 | boolean | 是否晋级32强 |

**使用示例：**

```js
const { loadTeams, findTeamByName } = require('./scripts/worldcup-teams.js');

// 列出全部球队
const data = loadTeams();
console.log(data.totalTeams); // 48

// 按名查找
const team = findTeamByName(data, '加拿大');
console.log(team.teamId); // 35779c25e9dec553f154e9d6286925e6
```

更多详情见 `references/overview.md`。
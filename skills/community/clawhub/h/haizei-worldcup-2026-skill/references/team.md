# 球队详情

## 脚本：`scripts/worldcup-team.js`

从百度体育球队页（`https://tiyu.baidu.com/al/team?id=<teamId>&tab=...`）抓取 6 个 tab 的数据。

## 命令

```bash
node scripts/worldcup-team.js lookup <球队名>             # 通过 teams.json 查 teamId
node scripts/worldcup-team.js info <teamId>               # 球队资料
node scripts/worldcup-team.js schedule <teamId> [赛事]    # 赛程
node scripts/worldcup-team.js lineup <teamId>             # 阵容
node scripts/worldcup-team.js history <teamId>            # 历史成绩
node scripts/worldcup-team.js stats <teamId> <年> <赛事>  # 数据统计
```

赛事参数可选值：`all`（默认）/ `世界杯` / `国际友谊赛`

赛事统计参数示例：`2026 小组赛` / `2022 世界杯` / `2024 国际友谊赛`

## 各 tab 数据说明

### info - 球队资料

| 字段 | 类型 | 说明 |
|------|------|------|
| baseInfo.title | string | "基本资料" |
| baseInfo.items[] | array | 资料项列表 |
| ├─ name | string | 资料项名称（成立时间/世界排名/平均年龄/总身价/主教练） |
| ├─ content | string | 资料内容 |
| └─ link | string | 关联链接（如FIFA排名页） |
| honor.title | string | "荣耀" |
| honor.awards[] | array | 荣誉列表 |
| ├─ title | string | 奖项名称 |
| └─ years | array | 获奖年份列表 |

### schedule - 球队赛程

数据结构按 `competitions` 分组（id: all/世界杯/国际友谊赛）：

```js
{
  subTabs: ["全部赛程", "世界杯", "国际友谊赛"],
  competitions: {
    "世界杯": {
      title: "世界杯",
      index: 0,
      matches: [...]  // 与 worldcup-schedule.js 的字段相同
    },
    "国际友谊赛": { ... }
  }
}
```

### lineup - 球队阵容

| 字段 | 类型 | 说明 |
|------|------|------|
| coaching[] | array | 教练组（7人左右） |
| ├─ name | string | 姓名 |
| ├─ subTitle | string | 职位/年龄/国籍 |
| └─ avatar | string | 头像URL |
| players[] | array | 球员按位置分组 |
| ├─ position | string | "前锋"/"中场"/"后卫"/"门将" |
| ├─ columnTitles | array | 列定义（field/name/type） |
| └─ players[] | array | 球员列表 |

球员字段：`number`/`name`/`age`/`playerId`/`club`/`goals`/`court`(出场)/`assists`/`value`(身价)

### history - 历史成绩

| 字段 | 类型 | 说明 |
|------|------|------|
| records[] | array | 历届世界杯参赛记录 |
| ├─ season | string | 赛季（如 "2022年卡塔尔世界杯"） |
| ├─ description | string | 成绩描述（如 "止步小组赛，3负"） |
| ├─ groupMatches | array | 小组赛比分列表 |
| └─ url | string | 百科链接 |

### stats - 球队数据

| 字段 | 类型 | 说明 |
|------|------|------|
| seasonStats[] | array | 按赛事+赛季组织 |
| ├─ competition | string | 赛事名称 |
| ├─ season | string | 赛季年份 |
| ├─ rank | object | 最终排名（win/deuce/loss/score/rank/rankArea） |
| └─ statGroups[] | array | 5 大类统计 |
| ├─ group | string | "统计"/"进攻"/"组织"/"防守"/"纪律" |
| └─ items[] | array | 统计项 |
| ├─ name | string | 统计项名 |
| ├─ value | string | 数值 |
| └─ rankingText + ranking | string | 联盟排名（如 "联盟第1"） |

**典型用法：**

```bash
# 当前赛事数据
node scripts/worldcup-team.js stats 35779c25e9dec553f154e9d6286925e6 2026 世界杯

# 历史对比
node scripts/worldcup-team.js stats 35779c25e9dec553f154e9d6286925e6 2022 世界杯
```

## 球队ID查找

通过 `lookup` 命令从静态的 `teams.json` 中查询：

```bash
node scripts/worldcup-team.js lookup 加拿大
# 返回: { teamName, teamId, group, pot, isHost, ... }
```

## 模块导出

```js
const {
  fetchTeamData,
  parseSchedule, parseLineup, parseInfo, parseHistory, parseStats
} = require('./scripts/worldcup-team.js');
```
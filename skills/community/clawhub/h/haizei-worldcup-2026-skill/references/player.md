# 球员详情

## 脚本：`scripts/worldcup-player.js`

从百度体育球员页（`https://tiyu.baidu.com/al/player?id=<playerId>&tab=...`）抓取 5 个 tab 的数据。

## 命令

```bash
node scripts/worldcup-player.js info <playerId>           # 球员资料
node scripts/worldcup-player.js news <playerId>           # 球员动态
node scripts/worldcup-player.js stats <playerId> [赛季] [赛事]
node scripts/worldcup-player.js schedule <playerId>       # 球员赛程
node scripts/worldcup-player.js detail <playerId> [tab]  # 完整详情（默认资料）
```

playerId 可从球队阵容的 `playerId` 字段获取。

## 各 tab 数据说明

### info - 球员资料

| 字段 | 类型 | 说明 |
|------|------|------|
| wiki.num | number | 球衣号码 |
| wiki.nickName | string | 英文名 |
| wiki.height / weight | string | 身高/体重 |
| wiki.detail.position | string | 位置（前锋/中场等） |
| wiki.detail.heavyFoot | string | 惯用脚（左/右/左右脚） |
| wiki.detail.age | number | 年龄 |
| wiki.detail.national | string | 国家队 |
| wiki.detail.expiryDate | string | 合同到期日 |
| wiki.detail.socialStatus | string | 身价数值 |
| wiki.detail.socialStatusUnit | string | 身价单位（万欧） |
| wiki.list | array | 详细资料列表 |
| ability.overall | string | 综合评分 |
| ability.overallColor | string | 评分颜色 |
| ability.radarDims | array | 6维能力雷达（速度/射门/传球/盘带/防守/身体） |
| ├─ name | string | 维度名 |
| ├─ value | string | 评分值 |
| └─ level | number | 等级（1-5） |
| honor[] | array | 荣誉列表（按赛事分组） |
| honorRecords[] | array | 荣誉记录（赛事名/次数/赛季） |
| transfer.unit | string | 转会费单位 |
| transfer.list[] | array | 转会历史（date/outTeam/team/price） |
| market | object | 身价曲线数据 |

### news - 球员动态

| 字段 | 类型 | 说明 |
|------|------|------|
| total | number | 动态总数 |
| newsList[].title | string | 新闻标题 |
| newsList[].link | string | 详情链接 |
| newsList[].factorTime | number | 发布时间戳 |
| newsList[].source | string | 来源媒体 |
| newsList[].img | string | 配图URL |
| newsList[].nid | string | 新闻ID |

### stats - 球员数据

| 字段 | 类型 | 说明 |
|------|------|------|
| seasonStats[] | array | 按赛事+赛季组织 |
| ├─ competition | string | 赛事名称 |
| ├─ season | string | 赛季 |
| ├─ rank | object | 球员在赛事中的排名 |
| └─ statGroups[] | array | 5 大类统计 |
| ├─ group | string | "统计"/"进攻"/"组织"/"防守"/"纪律" |
| └─ items[] | array | 统计项 |

**常用查询：**

```bash
# 世界杯数据
node scripts/worldcup-player.js stats 7bf18ff5b176d56a734dd90598461b2b 2026 世界杯

# 五大联赛数据
node scripts/worldcup-player.js stats <playerId> 2025-2026 意甲
node scripts/worldcup-player.js stats <playerId> 2025-2026 英超
```

### schedule - 球员赛程

| 字段 | 类型 | 说明 |
|------|------|------|
| subTabs | array | 可用视角（国家队/俱乐部） |
| teams | object | 按 teamId 分组 |
| ├─ title | string | "德国"/"阿森纳"等 |
| ├─ teamId | string | 球队ID |
| └─ matches[] | array | 出场记录 |

## 模块导出

```js
const {
  fetchPlayerData,
  parseSchedule, parseRatings, parseNews, parseInfo, parseStats
} = require('./scripts/worldcup-player.js');
```
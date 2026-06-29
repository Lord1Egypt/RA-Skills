# 赛程数据

## 脚本：`scripts/worldcup-schedule.js`

从百度体育赛程页（`https://tiyu.baidu.com/al/match?match=世界杯&tab=赛程`）抓取比赛列表。

## 命令

### 列出全部赛程（当前可见窗口约 4 天）

```bash
node scripts/worldcup-schedule.js all
```

### 按时间过滤

```bash
node scripts/worldcup-schedule.js today          # 今天
node scripts/worldcup-schedule.js tomorrow       # 明天
node scripts/worldcup-schedule.js date 2026-06-14
node scripts/worldcup-schedule.js date 06-15
```

### 按小组/球队/阶段筛选

```bash
node scripts/worldcup-schedule.js group A        # A组全部比赛
node scripts/worldcup-schedule.js team 巴西      # 巴西的赛程
node scripts/worldcup-schedule.js stage 小组赛    # 仅小组赛
node scripts/worldcup-schedule.js stage 淘汰赛    # 仅淘汰赛
```

### 辅助命令

```bash
node scripts/worldcup-schedule.js dates          # 可用日期列表
node scripts/worldcup-schedule.js stats          # 统计（已结束/未开赛/进行中）
```

## 数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| matchId | string | 比赛唯一ID（base64编码） |
| oriKey | string | 原始键 `世界杯#2026-06-12#主队vs客队` |
| date | string | 比赛日期 YYYY-MM-DD |
| startTime | string | 开始时间 YYYY-MM-DD HH:mm:ss |
| time | string | 北京时间 HH:mm |
| stage | string | 比赛阶段（如 `小组赛A组第1轮`） |
| group | string | 所属小组 A-L |
| round | number | 小组赛轮次 |
| homeTeam | string | 主队名称 |
| awayTeam | string | 客队名称 |
| homeScore | string/number | 主队比分（未开赛时为 null） |
| awayScore | string/number | 客队比分 |
| scoreLine | string | 比分字符串（如 `2-1`） |
| status | string | 比赛状态（未开赛/进行中/已结束） |
| statusId | string | 状态ID（0/1/2） |
| dataSourceText | string | 数据来源（动画直播/比赛战报等） |
| resultDesc | string | 比赛结果描述（如战报标题） |
| winner | string | 获胜方 |
| hasLive | boolean | 是否有直播 |
| hot | number | 热度值 |
| detailUrl | string | 比赛详情URL |

## matchId 编码规则

百度体育的 `matchId` 是 URL 安全的 base64 编码，格式：

```
世界杯_2026-06-12_墨西哥vs南非
```

可通过 `decodeMatchId(matchId)` 解码。URL 中 `matchId` 参数会做 URL-encoding 二次编码。

## 已知限制

- 页面默认仅展示当前可见时间窗口（约 4 天，12 场比赛）
- 更早/更晚赛程需要分页加载（暂未接入）
- 完整 104 场比赛需循环 `date <YYYY-MM-DD>` 命令

## 模块导出

```js
const {
  fetchAllSchedule,
  filterByDate, filterByGroup, filterByTeam, filterByStage,
  filterByDateKeyword,
  getAvailableDates, getStats,
  decodeMatchId
} = require('./scripts/worldcup-schedule.js');
```
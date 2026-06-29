# 典型工作流

按用户问题分类，给出具体的脚本调用链。AI 助手可参考这些模式回答用户。

---

# 四大每日高价值工作流

以下工作流专为一站式获取每日世界杯比赛分析而设计。

---

## 工作流 A：每日比赛前瞻（推荐每日使用）

**场景**：用户问「今天/明天有哪些比赛？怎么看？」

**一键获取今日全部比赛概览**：
```bash
node scripts/worldcup-schedule.js today
node scripts/worldcup-schedule.js tomorrow
```

**单场比赛深度分析**（传入 matchId）：
```bash
node scripts/worldcup-match.js analysis <matchId>
node scripts/worldcup-match.js odds <matchId>
```

**实际数据示例**（明天 2026-06-14 赛程）：
```json
[
  {"time": "03:00", "homeTeam": "卡塔尔", "awayTeam": "瑞士", "stage": "B组第1轮", "hot": "21"},
  {"time": "06:00", "homeTeam": "巴西", "awayTeam": "摩洛哥", "stage": "C组第1轮", "hot": "51"},
  {"time": "09:00", "homeTeam": "海地", "awayTeam": "苏格兰", "stage": "C组第1轮", "hot": "11"},
  {"time": "12:00", "homeTeam": "澳大利亚", "awayTeam": "土耳其", "stage": "D组第1轮", "hot": "21"}
]
```

**analysis 返回字段解读**：
- `prediction.homeWinRate` / `prediction.awayWinRate` - AI 预测胜率（如"40%" / "32%"）
- `prediction.similarOddsHistory` - 相似赔率下历史胜率（如主胜 41%、平局 28%、客胜 31%）
- `intelligence` - 双方有利/不利情报（如"美国近5年主场对巴拉圭100%胜率"）
- `records` - 历史交锋战绩（含胜率、赢盘率、大球率）
- `guess` - 网友投票分布（如 66.9% 看好美国）

**odds 返回字段解读**：
- 多家博彩公司赔率数据
- 包含亚盘（让球盘）、大小球、胜平负三种盘口
- `initial` 初盘 / `now` 即时盘

**用户追问**：
- "这场谁更可能赢" → 从 `prediction` 读取胜率
- "有什么看点" → 从 `intelligence` 读取双方近况分析
- "能买吗/盘口怎么走" → 从 `odds` 读取博彩公司赔率
- "两队历史交手谁赢得多" → 从 `records` 读取 H2H 战绩

---

## 工作流 B：比赛战报回顾（赛后使用）

**场景**：用户问「昨晚那场比赛怎么样了？」

**完整战报获取**：
```bash
# 1. 找到比赛（按日期）
node scripts/worldcup-schedule.js date 2026-06-13

# 2. 技术统计
node scripts/worldcup-match.js stats <matchId>

# 3. 赛况事件流（进球/红黄牌/换人）
node scripts/worldcup-match.js live <matchId>

# 4. 阵容详情
node scripts/worldcup-match.js lineup <matchId>
```

**实际数据示例**（美国 4-1 巴拉圭）：

**stats 技术统计**：
```json
{
  "homeTeam": "美国", "awayTeam": "巴拉圭",
  "items": [
    {"name": "进球", "home": 4, "away": 1},
    {"name": "控球率", "home": 65, "away": 35},
    {"name": "射正", "home": 6, "away": 1},
    {"name": "角球", "home": 3, "away": 1},
    {"name": "黄牌", "home": 1, "away": 5}
  ]
}
```

**live 赛况事件流**：
```json
{
  "venue": {"name": "洛杉矶体育场", "city": "洛杉矶", "capacity": "70240"},
  "narrative": [
    {"text": "8' - 第1个进球！博瓦迪利亚(美国 乌龙球)", "iconType": "进球"},
    {"text": "31' - 第2个进球 - 巴洛贡(美国)", "iconType": "进球"},
    {"text": "45+5' - 第3个进球 - 巴洛贡(美国)", "iconType": "进球"},
    {"text": "74' - 第4个进球 - 毛里西奥(巴拉圭)", "iconType": "进球"},
    {"text": "90+8' - 第5个进球 - 雷纳(美国)", "iconType": "进球"}
  ],
  "incidents": [
    {"goalType": "乌龙球", "passedTime": "7'", "team": "美国"},
    {"goalType": "进球", "passedTime": "31'", "team": "美国"},
    {"goalType": "进球", "passedTime": "45'", "team": "美国"},
    {"goalType": "进球", "passedTime": "73'", "team": "巴拉圭"},
    {"goalType": "进球", "passedTime": "90'", "team": "美国"}
  ]
}
```

**用户追问**：
- "谁进球了" → 从 `live.incidents` 过滤 `goalType: "进球"`
- "红黄牌有哪些" → 从 `live.incidents` 过滤 `goalType: "黄牌"/"红牌"`
- "换了几个人" → 从 `live.incidents` 过滤 `goalType: "换人"`
- "比赛场地在哪" → 从 `venue` 读取城市和球场名称

---

## 工作流 C：积分榜与出线形势（每日更新）

**场景**：用户问「现在各组什么情况？谁能出线？」

**一键获取全部12组积分榜**：
```bash
node scripts/worldcup-rankings.js standings
```

**实际数据示例**（D组当前状态）：
```json
{
  "groups": [{
    "list": [
      {"teamName": "美国", "played": 1, "winDrawLoss": "1/0/0", "goals": "4/1", "points": 3, "isQualified": true},
      {"teamName": "澳大利亚", "played": 0, "winDrawLoss": "0/0/0", "goals": "0/0", "points": 0, "isQualified": false},
      {"teamName": "土耳其", "played": 0, "winDrawLoss": "0/0/0", "goals": "0/0", "points": 0, "isQualified": false},
      {"teamName": "巴拉圭", "played": 1, "winDrawLoss": "0/0/1", "goals": "1/4", "points": 0, "isQualified": false}
    ]
  }]
}
```

**字段解读**：
- `isQualified === true` → 已晋级（蓝色背景 #456de6）
- `isRelegated === true` → 已淘汰（红色背景 #ff5050）
- `status` 字段如"晋级32强"、"晋级待定"
- `goals` 格式为 "进/失"（如"4/1"表示进4球失1球）
- `winDrawLoss` 格式为 "胜/平/负"

**用户追问**：
- "A组还有希望吗" → 查该组积分差距
- "巴西能出线吗" → 直接查巴西所在C组的 `isQualified`
- "第三名能晋级吗" → 规则是8支小组第3晋级32强

---

## 工作流 D：球员表现追踪（射手榜/球员榜）

**场景**：用户问「现在谁进球最多？明星球员表现如何？」

**射手榜**：
```bash
node scripts/worldcup-rankings.js players 进球 10
```

**球员排行榜（30+维度）**：
```bash
node scripts/worldcup-rankings.js players 助攻
node scripts/worldcup-rankings.js players 过人
node scripts/worldcup-rankings.js players 射门
node scripts/worldcup-rankings.js players 关键传球
node scripts/worldcup-rankings.js categories  # 查看全部支持分类
```

**players 返回示例**：
```json
{
  "tabName": "进球",
  "players": [
    {"rank": 1, "playerName": "弗拉林·巴洛贡", "team": "美国", "position": "前锋", "score": "2"},
    {"rank": 2, "playerName": "黄仁范", "team": "韩国", "position": "中场", "score": "1"}
  ]
}
```

**明星球员详情深挖**：
```bash
node scripts/worldcup-player.js info <playerId>
node scripts/worldcup-player.js news <playerId>
```

**player info 返回示例**（内马尔 playerId: 8b95bfb75b6abad75a141fbfee809950）：
```json
{
  "wiki": {
    "height": "175cm", "weight": "68kg",
    "detail": {"position": "前锋", "age": "33岁", "national": "巴西"}
  },
  "ability": {
    "overall": 82,
    "radarDims": [
      {"name": "速度", "value": 85}, {"name": "射门", "value": 86},
      {"name": "传球", "value": 88}, {"name": "盘带", "value": 93}
    ]
  },
  "transfer": {
    "list": [
      {"date": "2023-08-15", "team": "利雅得新月", "price": "9000万欧"},
      {"date": "2017-08-03", "team": "巴黎圣日耳曼", "price": "22200万欧"},
      {"date": "2013-07-01", "team": "巴塞罗那", "price": "8800万欧"}
    ]
  },
  "market": {"axis": {"data": [[[{"x": 53, "y": 100}]]]}},  // 身价变化曲线
  "honor": [
    {"match": "南美年度足球先生", "seasons": [{"date": "2012"}]},
    {"match": "欧冠冠军", "seasons": [{"date": "2014-2015"}]}
  ]
}
```

**用户追问**：
- "姆巴佩进了几个球" → 查球员榜，按名字搜索
- "中场谁助攻最多" → `players 助攻`
- "这个球员什么水平" → 从 `ability.radarDims` 读取能力评分
- "内马尔转会过几次" → 从 `transfer.list` 读取5次转会记录

---

## 工作流 E：竞彩赔率查询（体彩官方）

**用户问**：「巴西这场让几个球？/ 这场赔率多少？/ 比分赔率怎么看？/ 体彩赔率查询」

**执行链**：

```bash
# 1. 精简模式：浏览所有世界杯比赛的主流玩法
node scripts/worldcup-calculator.js summary --wc

# 2. 按玩法过滤
node scripts/worldcup-calculator.js had --wc      # 胜平负
node scripts/worldcup-calculator.js hhad --wc     # 让球胜平负
node scripts/worldcup-calculator.js crs --wc      # 比分
node scripts/worldcup-calculator.js ttg --wc      # 总进球
node scripts/worldcup-calculator.js hafu --wc     # 混合过关

# 3. 按球队/日期过滤
node scripts/worldcup-calculator.js summary --wc --team 巴西
node scripts/worldcup-calculator.js summary --wc --date 2026-06-14

# 4. 赔率变化历史（matchId 来自 --json 输出）
node scripts/worldcup-calculator.js history <matchId> had
```

**实际数据示例**（巴西 vs 摩洛哥）：
```
周六006 巴西 vs 摩洛哥
2026-06-14 06:00:00
------------------------------------------------------------
  胜平负     主胜:1.49   平:3.60   客胜:5.55
  让球(-1)   主胜:2.72↑   平:3.11↓   客胜:2.27
```

JSON 输出示例：
```json
{
  "matchId": 2040167,
  "homeTeam": "巴西",
  "awayTeam": "摩洛哥",
  "pools": [
    {
      "poolCode": "had",
      "homeWin": "1.49",
      "draw": "3.60",
      "awayWin": "5.55"
    },
    {
      "poolCode": "hhad",
      "goalLine": "-1",
      "homeWin": "2.72",
      "draw": "3.11",
      "awayWin": "2.27"
    }
  ]
}
```

**字段解读**：
- 趋势符号：`↑` 赔率上升（庄家不看好该结果）/ `↓` 下降（庄家看好）/ 无 不变
- `goalLine` 字段：让球数（如"-1"表示主队让 1 球，"-3"表示让 3 球）
- crs 共 31 种比分赔率（客胜 13 + 平 5 + 主胜 13）

**与百度体育赔率（worldcup-match odds）的区别**：
| 数据源 | 覆盖 | 特点 |
|--------|------|------|
| 百度体育 `worldcup-match.js odds` | 亚盘/欧赔/大小球 | 多家博彩公司盘口 |
| 体彩 `worldcup-calculator.js` | 5 种官方竞彩玩法 | 中国体彩官方，含让球数 |

**用户追问**：
- "巴西这场让几个球" → `hhad.goalLine` 字段
- "主队胜率多少" → 1/1.49 ≈ 67%（隐含概率）
- "比分赔率最低的是哪个" → crs 中找最小值
- "这场的赔率在变吗" → 关注 `homeTrend`/`drawTrend`/`awayTrend` 字段
- "赔率变化历史" → `history <matchId> <玩法>` 命令

---

# 扩展工作流

## 工作流 1：今日观赛指南

**用户问**：「今天有什么世界杯比赛？几点开赛？」

**执行**：
```bash
node scripts/worldcup-schedule.js today
```

**扩展场景**：
- 用户问"今天最值得看哪场" → 按 `hot` 字段排序（51最高为巴西 vs 摩洛哥）
- 用户问"有直播吗" → 过滤 `hasLive === true`
- 用户问"几点开球" → 从 `time` 字段读取（如"03:00"、"06:00"、"09:00"）

---

## 工作流 2：正在直播

**用户问**：「现在有什么比赛在直播？」

**执行**：
```bash
node scripts/worldcup-schedule.js today | jq '.[] | select(.statusId=="1")'
```

**扩展场景**：
- 实时赛况：`node scripts/worldcup-match.js live <matchId>`
- 实时比分：`scoreLine` 字段（如"4-1"）

---

## 工作流 3：球队下一场比赛

**用户问**：「巴西下一场几点打？对手是谁？」

**执行链**：
```bash
node scripts/worldcup-team.js lookup 巴西
node scripts/worldcup-team.js schedule <teamId> 世界杯
```

**巴西赛程示例**：
```json
[
  {"date": "2026-06-14", "time": "06:00", "homeTeam": "巴西", "awayTeam": "摩洛哥"},
  {"date": "2026-06-20", "time": "08:30", "homeTeam": "巴西", "awayTeam": "海地"},
  {"date": "2026-06-25", "time": "06:00", "homeTeam": "苏格兰", "awayTeam": "巴西"}
]
```

---

## 工作流 4：球队核心球员

**用户问**：「德国队谁最贵？有哪些明星球员？」

**执行**：
```bash
node scripts/worldcup-team.js lineup d885ec68c7b46dbfd4a8f6e41d577ba0
```

**扩展场景**：
- 按身价排序：`value` 字段（如"1.2亿"、"800万"）
- 按位置分组：`position` 字段
- 教练组：`coaching` 字段

---

## 工作流 5：FIFA 排名查询

**用户问**：「中国/日本 FIFA 排名第几？」

**执行**：
```bash
node scripts/worldcup-rankings.js fifa 50
```

**实际数据示例**（前10）：
```json
[
  {"rank": 1, "teamName": "阿根廷", "points": 1877, "positionChanged": 2},
  {"rank": 2, "teamName": "西班牙", "points": 1874, "positionChanged": 0},
  {"rank": 3, "teamName": "法国", "points": 1870, "positionChanged": -2},
  {"rank": 6, "teamName": "巴西", "points": 1765, "positionChanged": 0},
  {"rank": 7, "teamName": "摩洛哥", "points": 1755, "positionChanged": 1}
]
```

---

## 工作流 6：球队历史 vs 当前

**用户问**：「巴西队世界杯历史成绩怎么样？」

**执行**：
```bash
node scripts/worldcup-team.js history 巴西
```

**历史成绩示例**：
```json
{
  "records": [
    {"season": "2022年卡塔尔世界杯", "description": "止步八强，3胜1平1负"},
    {"season": "2018年俄罗斯世界杯", "description": "止步八强，3胜1平1负"},
    {"season": "2002年韩日世界杯", "description": "冠军，7战7胜"},
    {"season": "1994年美国世界杯", "description": "冠军，5胜2平"}
  ]
}
```

---

## 工作流 7：新闻/动态关注

**用户问**：「C罗最近有什么新闻？」

**执行链**：
```bash
node scripts/worldcup-team.js lookup 葡萄牙
node scripts/worldcup-team.js lineup <teamId>
node scripts/worldcup-player.js news <playerId>
```

**新闻返回示例**：
```json
{
  "newsList": [
    {"title": "世界杯折射的美国例外论", "source": "虎嗅APP", "endTime": "昨天18:21"},
    {"title": "曾经的世界第三人，过去3年仅出战49场", "source": "篮球圈里的那些事儿", "endTime": "5月29日"}
  ]
}
```

---

## 工作流 8：球队信息快速查询

**用户问**：「东道主是谁？有几支亚洲球队？」

**执行**：
```bash
node scripts/worldcup-teams.js hosts        # 东道主（美国、加拿大、墨西哥）
node scripts/worldcup-teams.js list         # 全部48队
node scripts/worldcup-teams.js pot 1         # 第一档强队
```

---

## 工作流 9：赛程日期范围

**用户问**：「这周后半段还有什么比赛？」

**执行**：
```bash
node scripts/worldcup-schedule.js dates     # 可用日期列表
node scripts/worldcup-schedule.js stats      # 赛程统计
```

**stats 返回示例**：
```json
{"total": 16, "finished": 4, "pending": 12, "live": 0, "dateRange": {"from": "2026-06-12", "to": "2026-06-16"}}
```

---

## 错误处理模式

### 未找到球队
→ 提示用户用 `node worldcup-teams.js list` 查看所有48支球队

### 赛程数据获取失败
→ 提示用户网络问题，请稍后重试

### 比赛未开赛无阵容
→ 提示用户"阵容尚未公布，开赛前2小时左右会更新"

### 比赛进行中
→ 提示用户"技术统计和赛况约1-2分钟延迟"

---

## 注意事项

- 数据延迟：实时数据 1-2 分钟延迟
- 静态数据：teams.json 不会自动更新
- matchId 编码：脚本已自动处理
- 球员/球队ID：跨脚本通用
- 比赛时间：均以北京时间（UTC+8）为准
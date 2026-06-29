---
name: haizei-worldcup-2026-skill
description: 获取2026年国际足联世界杯（美加墨世界杯）数据技能。从百度体育抓取48支参赛球队的分组配置、赛程、比赛详情（分析/阵容/赛况/统计/指数）、球队详情（资料/阵容/历史成绩/数据）、球员详情（资料/动态/数据/赛程）、排名数据（积分榜/球员榜/FIFA排名）等，并从中国体育彩票接入官方竞彩玩法赔率（胜平负/让球/比分/总进球/混合过关）。当用户需要查询2026世界杯球队、赛程、比赛数据、阵容、历史成绩、排名、竞彩赔率时使用此技能。A skill for retrieving 2026 FIFA World Cup data. Scrapes from Baidu Sports and sporttery.cn.
---

# 2026年美加墨世界杯数据获取

 2026 美加墨世界杯数据。包含 48 支球队的分组配置、赛程、比赛详情、球队详情、球员详情、排名等。

## 核心能力

**赛程查询**：`today` 今日赛程、`tomorrow` 明日赛程、`date` 指定日期、`group` 按组筛选、`team` 按队筛选、`stage` 按阶段筛选、`dates` 可用日期列表、`stats` 赛程统计

**比赛详情**：
- `analysis` - AI预测分析（胜率预测/历史战绩/情报/网友投票）
- `lineup` - 阵容（首发/替补/阵型/裁判/场地）
- `live` - 赛况（事件流/进球/红黄牌/换人/文字播报）
- `stats` - 技术统计（控球/射门/角球等）
- `odds` - 博彩赔率（初盘/即时盘/亚盘/大小球）

**球队数据**：
- `info` - 球队资料/荣誉（成立时间/排名/身价/教练）
- `schedule` - 球队赛程（世界杯/友谊赛等）
- `lineup` - 球队阵容（教练组+26人名单/位置/俱乐部/身价）
- `history` - 历史成绩（历届世界杯战绩/小组赛果）
- `stats` - 数据统计（进球/助攻/控球等维度）

**球员数据**：
- `info` - 球员资料（身高/体重/位置/惯用脚/年龄）
- `ability` - 能力雷达图（速度/射门/传球/盘带/防守/力量）
- `honor` - 球员荣誉（世界杯/联赛/金球奖等）
- `transfer` - 转会历史（5次主要转会记录）
- `market` - 市场估值趋势（身价变化曲线）
- `news` - 球员新闻（10条最新报道）
- `stats` - 赛事数据统计
- `schedule` - 出场记录

**排名数据**：
- `standings` - 小组积分榜（12组A-L/已晋级/已淘汰/待定）
- `fifa` - FIFA排名（世界前50/升降变化/积分）
- `players` - 球员排行榜（30+维度：进球/助攻/过人/抢断/传球/红黄牌等）
- `knockout` - 淘汰赛对阵图

**球队配置**：`list` 48队、`group` 按组查询、`hosts` 东道主、`pot` 档位分布、`find` 模糊搜索

**竞彩赔率**（`worldcup-calculator.js`，数据源：体彩官方）：
- `had` - 胜平负赔率（主胜/平/客胜）
- `hhad` - 让球胜平负赔率（含让球数）
- `crs` - 比分赔率（31 种比分组合）
- `ttg` - 总进球赔率（0-7+ 球）
- `hafu` - 混合过关赔率（半场+全场 9 种组合）
- `history` - 赔率变化历史（按 matchId 查询）
- 支持 `--wc`（只显示世界杯）、`--team`、`--date`、`--json`、`summary` 模式

---

## 路由表

| 用户需求 | 脚本 | 参考文档 |
|---------|------|---------|
| 赛事基本信息、48队分组 | `scripts/worldcup-teams.js info` | [overview.md](references/overview.md) |
| 球队配置（静态）| `scripts/worldcup-teams.js` | [teams.md](references/teams.md) |
| 全部赛程 / 今日赛程 / 按组按队查询 | `scripts/worldcup-schedule.js` | [schedule.md](references/schedule.md) |
| 比赛情报 / 阵容 / 赛况 / 统计 / 指数 | `scripts/worldcup-match.js` | [match.md](references/match.md) |
| 球队资料 / 阵容 / 历史成绩 / 数据 | `scripts/worldcup-team.js` | [team.md](references/team.md) |
| 球员资料 / 动态 / 数据 / 赛程 | `scripts/worldcup-player.js` | [player.md](references/player.md) |
| 排名 / 球队榜 / 球员榜 / FIFA排名 | `scripts/worldcup-rankings.js` | [rankings.md](references/rankings.md) |
| **竞彩赔率**（胜平负/让球/比分/总进球/混合过关） | `scripts/worldcup-calculator.js` | [calculator.md](references/calculator.md) ⭐ |
| **典型用户问题处理** | — | [**workflows.md**](references/workflows.md) ⭐ |
| 跨脚本组合用法 | — | [usage.md](references/usage.md) |

> ⭐ **AI 必读**：[workflows.md](references/workflows.md) 包含 15+ 个真实工作流

## 快速命令

### 球队（静态配置）
```bash
node scripts/worldcup-teams.js list              # 全部48队
node scripts/worldcup-teams.js group A           # A组
node scripts/worldcup-teams.js find 加拿大       # 按名查 teamId
node scripts/worldcup-teams.js info              # 赛事基本信息
node scripts/worldcup-teams.js hosts            # 东道主（美国/加拿大/墨西哥）
node scripts/worldcup-teams.js pot 1             # 第一档球队
```

### 赛程
```bash
node scripts/worldcup-schedule.js today          # 今日赛程
node scripts/worldcup-schedule.js tomorrow     # 明日赛程
node scripts/worldcup-schedule.js date 2026-06-14 # 指定日期
node scripts/worldcup-schedule.js group B       # B组赛程
node scripts/worldcup-schedule.js team 巴西     # 巴西的赛程
node scripts/worldcup-schedule.js stage 小组赛  # 小组赛阶段
node scripts/worldcup-schedule.js dates          # 有比赛的日期列表
node scripts/worldcup-schedule.js stats         # 赛程统计
```

### 比赛详情（matchId 来自赛程）
```bash
node scripts/worldcup-match.js info <matchId>     # 基本信息
node scripts/worldcup-match.js analysis <matchId> # AI预测/情报/历史/投票
node scripts/worldcup-match.js lineup <matchId>   # 首发/替补/阵型/裁判
node scripts/worldcup-match.js live <matchId>     # 事件流/场地/文字播报
node scripts/worldcup-match.js stats <matchId>    # 技术统计
node scripts/worldcup-match.js odds <matchId>     # 博彩赔率
```

### 球队详情（支持 teamId 或中文球队名）
```bash
node scripts/worldcup-team.js lookup 加拿大       # 查 teamId
node scripts/worldcup-team.js info 巴西         # 资料+荣誉（成立/排名/身价/教练）
node scripts/worldcup-team.js schedule 巴西 世界杯 # 该队赛程
node scripts/worldcup-team.js lineup 法国         # 教练+26人名单
node scripts/worldcup-team.js history 巴西       # 历届世界杯成绩
node scripts/worldcup-team.js stats 巴西 2026 小组赛 # 数据统计
```

### 球员详情（playerId 来自球队阵容）
```bash
node scripts/worldcup-player.js info <playerId>    # 资料+能力雷达+荣誉+转会
node scripts/worldcup-player.js news <playerId>   # 球员新闻（10条）
node scripts/worldcup-player.js stats <playerId> 2026 世界杯 # 数据统计
node scripts/worldcup-player.js schedule <playerId> # 出场记录
```

### 排名数据
```bash
node scripts/worldcup-rankings.js standings        # 12组积分榜
node scripts/worldcup-rankings.js fifa 20          # FIFA 前20
node scripts/worldcup-rankings.js players 进球     # 射手榜
node scripts/worldcup-rankings.js players 助攻 10   # 助攻榜前10
node scripts/worldcup-rankings.js players 过人      # 过人榜
node scripts/worldcup-rankings.js categories       # 支持的30+种排行榜
node scripts/worldcup-rankings.js knockout         # 淘汰赛对阵图
```

### 竞彩赔率（体彩官方，数据源 sporttery.cn）
```bash
node scripts/worldcup-calculator.js summary --wc          # 世界杯精简模式（推荐）
node scripts/worldcup-calculator.js had --wc              # 只看胜平负
node scripts/worldcup-calculator.js hhad --wc             # 只看让球胜平负
node scripts/worldcup-calculator.js crs --wc              # 只看比分赔率
node scripts/worldcup-calculator.js ttg --wc              # 只看总进球
node scripts/worldcup-calculator.js hafu --wc             # 只看混合过关
node scripts/worldcup-calculator.js --wc --team 巴西      # 过滤指定球队
node scripts/worldcup-calculator.js --wc --date 2026-06-14 # 过滤指定日期
node scripts/worldcup-calculator.js history <matchId> had  # 赔率变化历史
node scripts/worldcup-calculator.js --wc --json | jq .    # JSON 输出
```

## 球员榜支持分类

进球、助攻、射门、射正、过人、过人成功、任意球、击中门框、快攻、快攻射门、丢失球权、解围、有效阻挡、拦截、抢断、1对1拼抢、1对1拼抢成功、拳击球、守门员出击、守门员出击成功、高空出击、传球、传球成功、关键传球、传中球、传中球成功、长传、成功长传、传球被断、红牌、黄牌、犯规、被侵犯、越位

## 关键词覆盖

**赛程相关**：今天有什么比赛、明天比赛、比赛时间、几点开球、哪场比赛、赛程表、今日比赛、明日比赛、小组赛程、X队比赛、X队下一场、揭幕战

**比赛结果相关**：比赛结果、X赢了还是输了、比分是多少、谁赢了、比赛报告、精彩瞬间、进球球员、红黄牌、换人、乌龙球、点球

**直播相关**：现在在直播、正在直播的比赛、直播源、哪个台直播

**球队相关**：球队阵容、球员名单、X队首发、X队球员、X队教练、历史战绩、世界杯成绩、历届表现、小组分组、X组情况、出线形势、东道主、身价多少、总身价

**球员相关**：球员数据、球员能力、球员水平、能力雷达图、X球员怎么样、球员新闻、转会记录、身价、进球数、世界杯数据、世界杯参赛名单

**排名相关**：积分榜、射手榜、助攻榜、FIFA排名、排名榜、小组排名、出线情况、X队排名、排行榜、过人榜、金靴

**预测分析相关**：比赛预测、X能赢吗、盘口、赔率、胜率预测、历史交锋、美国 vs 巴拉圭、巴西 vs 摩洛哥

**竞彩玩法相关**：竞彩、竞彩赔率、体彩、让球、让几个球、胜平负赔率、比分赔率、总进球赔率、混合过关、大小球、买球、买彩票、过关、单关、博彩、赌球、中国体彩、sporttery

## 四大每日高价值工作流（+ 体彩竞彩 E）

### 工作流 A：每日比赛前瞻（推荐每日使用）

**场景**：用户问「今天/明天有哪些比赛？怎么看？」

**执行链**：

```bash
# 1. 今日赛程概览
node scripts/worldcup-schedule.js today

# 2. 明日赛程
node scripts/worldcup-schedule.js tomorrow

# 3. 单场深度分析（传入 matchId）
node scripts/worldcup-match.js analysis <matchId>
node scripts/worldcup-match.js odds <matchId>
```

**analysis 返回字段**：

- `prediction.homeWinRate` / `awayWinRate` - AI预测胜率
- `prediction.similarOddsHistory` - 相似赔率历史胜率
- `intelligence` - 双方有利/不利情报
- `records` - 历史交锋战绩
- `guess` - 网友投票分布

**odds 返回字段**：

- `bookmakers[].datas[].initial/now` - 初盘/即时盘
- 包含亚盘（让球）、大小球、胜平负多种盘口

**用户追问**：

- "这场谁更可能赢" → `prediction.homeWinRate: "40%"`
- "有什么看点" → `intelligence` 双方近况
- "盘口怎么走" → `odds` 博彩公司赔率变化
- "历史交锋谁赢得多" → `records` H2H 战绩

---

### 工作流 B：比赛战报回顾（赛后使用）

**场景**：用户问「昨晚那场比赛怎么样了？」

**执行链**：

```bash
# 1. 找比赛
node scripts/worldcup-schedule.js date 2026-06-13

# 2. 技术统计
node scripts/worldcup-match.js stats <matchId>

# 3. 赛况事件流
node scripts/worldcup-match.js live <matchId>
```

**用户追问**：

- "谁进球了" → 从 `live.incidents` 过滤 `goalType: "进球"`
- "红黄牌有哪些" → 从 `live.incidents` 过滤 `goalType: "黄牌"/"红牌"`
- "换了几个人" → 从 `live.incidents` 过滤 `goalType: "换人"`
- "全场最佳" → 从 `live.narrative` 文字播报判断

---

### 工作流 C：积分榜与出线形势（每日更新）

**场景**：用户问「现在各组什么情况？谁能出线？」

**执行**：

```bash
node scripts/worldcup-rankings.js standings
```

**字段解读**：

- `isQualified === true`（蓝色背景）→ 已晋级
- `isRelegated === true`（红色背景）→ 已淘汰
- `status` 字段如"晋级32强"、"晋级待定"等

**用户追问**：

- "A组还有希望吗" → 查该组积分差距
- "巴西能出线吗" → 查C组巴西的 `isQualified`
- "第三名能晋级吗" → 规则是8支小组第3晋级

---

### 工作流 D：球员表现追踪（射手榜/球员榜）

**场景**：用户问「现在谁进球最多？明星球员表现如何？」

**执行链**：

```bash
# 1. 射手榜
node scripts/worldcup-rankings.js players 进球 10

# 2. 球员排行榜（30+维度）
node scripts/worldcup-rankings.js players 助攻
node scripts/worldcup-rankings.js players 过人
node scripts/worldcup-rankings.js players 射门

# 3. 明星球员详情
node scripts/worldcup-player.js info <playerId>
node scripts/worldcup-player.js news <playerId>
```

**用户追问**：

- "姆巴佩进了几个球" → 查球员榜，按名字搜索
- "中场谁助攻最多" → `players 助攻`
- "这个球员什么水平" → `ability.radarDims` 能力评分
- "内马尔转会过几次" → `transfer.list` 5次转会记录

> 竞彩赔率查询工作流见 [workflows.md](references/workflows.md) 工作流 E。

## 注意事项

- 数据从百度体育实时抓取，进行中比赛比分延迟约 1-2 分钟
- 赛程页默认展示约 4 天窗口，更早赛程需按日期循环查询
- 球队配置（teams.json）为静态，仅 2026 年赛事
- 球队/球员名仅支持中文（如"巴西"），不支持英文
- `worldcup-team.js` 支持中文球队名自动解析为 teamId
- 比赛时间均为北京时间（UTC+8）
- 球员排行榜目前仅射手榜有数据，其他分类待赛事进行后丰富
- `worldcup-calculator.js` 数据源为中国体彩官方（sporttery.cn），需用移动端 User-Agent 调用；脚本内置 30 个 UA 池每次随机选一；体彩 matchId 与百度体育 matchId 不通用；只展示可投注的赛事

## 作者

- 爱海贼的无处不在
- 微信公众号：无处不在的技术
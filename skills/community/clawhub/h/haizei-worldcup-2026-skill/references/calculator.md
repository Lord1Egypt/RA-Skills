# 竞彩足球计算器

## 脚本：`scripts/worldcup-calculator.js`

从中国体育彩票竞彩足球计算器抓取官方竞彩玩法赔率数据。包含胜平负、让球胜平负、比分、总进球、混合过关、大小球等竞彩玩法。

数据源：`https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry`

> 注意：该 API 需使用移动端 User-Agent 调用，否则会被 Tencent Cloud EdgeOne 拦截（返回 567 错误）。脚本内置了 30 个真实移动设备 User-Agent（iOS 14-17 + Android 10-14），每次请求随机选择一个，降低被识别为爬虫的风险。

## 命令

```bash
node scripts/worldcup-calculator.js                       # 列出所有比赛（所有玩法）
node scripts/worldcup-calculator.js had                   # 只显示胜平负
node scripts/worldcup-calculator.js hhad                  # 只显示让球胜平负
node scripts/worldcup-calculator.js crs                   # 只显示比分
node scripts/worldcup-calculator.js ttg                   # 只显示总进球
node scripts/worldcup-calculator.js hafu                  # 只显示混合过关
node scripts/worldcup-calculator.js hilo                  # 只显示大小球
node scripts/worldcup-calculator.js summary               # 精简模式（仅显示主要玩法）
node scripts/worldcup-calculator.js history <matchId> had # 获取赔率变化历史
node scripts/worldcup-calculator.js help                  # 显示帮助
```

## 选项

| 选项 | 说明 |
|------|------|
| `--json` | 输出 JSON 格式（便于程序化处理） |
| `--wc` | 只显示世界杯比赛 |
| `--team <名称>` | 按球队名过滤（模糊匹配主客队） |
| `--date <YYYY-MM-DD>` | 按日期过滤 |
| `--json --wc` | 组合使用：只输出世界杯比赛的 JSON |

## 玩法（poolCode）说明

体彩官方计算器当前提供 5 种玩法（不同比赛可能不全）：

| poolCode | 中文名 | 说明 |
|----------|--------|------|
| `had` | 胜平负 | 90 分钟内（含补时）主胜/平/客胜 |
| `hhad` | 让球胜平负 | 主队让球后的胜平负 |
| `crs` | 比分 | 猜全场比分（含 0:0 / 1:0 / 2:1 等 31 种） |
| `ttg` | 总进球 | 猜全场总进球数（0/1/2/3/4/5/6/7+） |
| `hafu` | 混合过关 | 半场+全场组合（9 种） |

> 注：脚本中保留了对 `hilo`（大小球）、`wnm`（胜其他）、`mnl`（胜负）的支持，但当前 API 不返回这些数据。

## 趋势符号

赔率变化通过 `homeTrend` / `drawTrend` / `awayTrend` 等字段表示：
- `1` = ↑ 上升
- `-1` = ↓ 下降
- `0` 或空 = 不变

## 数据结构

### 比赛基本信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `matchId` | number | 比赛 ID（唯一标识，体彩平台 ID） |
| `matchNum` | string | 编号（如"周六005"） |
| `league` | string | 赛事名（世界杯/英超/芬超等） |
| `homeTeam` | string | 主队全名 |
| `awayTeam` | string | 客队全名 |
| `homeRank` | string | 主队排名（如"[C组1]"，世界杯专用） |
| `awayRank` | string | 客队排名 |
| `date` | string | 比赛日期（YYYY-MM-DD） |
| `time` | string | 开赛时间（HH:mm:ss） |
| `status` | string | 销售状态（`Selling` 销售中） |
| `pools` | array | 该比赛的所有玩法赔率 |

### 玩法数据结构

#### had / hhad（胜平负 / 让球胜平负）

| 字段 | 类型 | 说明 |
|------|------|------|
| `poolCode` | string | 玩法代码 |
| `name` | string | 玩法中文名 |
| `homeWin` | string | 主胜赔率 |
| `draw` | string | 平局赔率（mnl 无此字段） |
| `awayWin` | string | 客胜赔率 |
| `goalLine` | string | 让球数（仅 hhad 有，如"+1"、"-1"） |
| `homeTrend` | string | 主胜赔率变化 |
| `drawTrend` | string | 平局赔率变化 |
| `awayTrend` | string | 客胜赔率变化 |
| `single` | number | 是否可单关（0=否, 1=是） |
| `cbt` | number | 是否已截止（0=未截止, 1=已截止） |

#### crs（比分）

| 字段 | 类型 | 说明 |
|------|------|------|
| `scores` | object | 各比分赔率，键为比分标签 |
| `trends` | object | 对应比分的赔率变化 |

比分标签（**共 31 种**）：
- 客胜（13 种）：`0:1`, `0:2`, `1:2`, `0:3`, `1:3`, `2:3`, `0:4`, `1:4`, `2:4`, `0:5`, `1:5`, `2:5`, `客胜其他`
- 平局（5 种）：`0:0`, `1:1`, `2:2`, `3:3`, `平其他`
- 主胜（13 种）：`1:0`, `2:0`, `2:1`, `3:0`, `3:1`, `3:2`, `4:0`, `4:1`, `4:2`, `5:0`, `5:1`, `5:2`, `主胜其他`

> 注：API 原始字段命名是 `s[主][客]` 格式（如 `s01s00` = 1:0），脚本已转换为标签形式。

#### ttg（总进球）

| 字段 | 类型 | 说明 |
|------|------|------|
| `goals` | object | 各进球数赔率，键为 `0`/`1`/`2`/.../`7+` |

#### hafu（混合过关）

半场+全场 9 种组合：

| 标签 | 含义 |
|------|------|
| `胜胜` | 半场主胜 + 全场主胜 |
| `胜平` | 半场主胜 + 全场平 |
| `胜负` | 半场主胜 + 全场客胜 |
| `平胜` | 半场平 + 全场主胜 |
| `平平` | 半场平 + 全场平 |
| `平负` | 半场平 + 全场客 |
| `负胜` | 半场客胜 + 全场主胜 |
| `负平` | 半场客胜 + 全场平 |
| `负负` | 半场客胜 + 全场客胜 |

#### hilo（大小球）

| 字段 | 类型 | 说明 |
|------|------|------|
| `goalLine` | string | 大小分线（如"2.5"） |
| `over` | string | 大分赔率 |
| `under` | string | 小分赔率 |
| `overTrend` | string | 大分赔率变化 |
| `underTrend` | string | 小分赔率变化 |

### 赔率变化历史（history 命令）

| 字段 | 类型 | 说明 |
|------|------|------|
| `h` / `d` / `a` | string | 主/平/客赔率（hilo 为 over/under） |
| `hf` / `df` / `af` | string | 对应赔率变化（1=↑, -1=↓, 0=不变） |
| `updateDate` | string | 更新日期 |
| `updateTime` | string | 更新时间 |

## 典型使用场景

### 场景 1：查看世界杯所有比赛胜平负赔率

```bash
node scripts/worldcup-calculator.js had --wc
```

### 场景 2：精简模式浏览世界杯所有比赛

```bash
node scripts/worldcup-calculator.js summary --wc
```

每场只显示胜平负、让球胜平负、大小球 3 个主流玩法，快速浏览。

### 场景 3：查看某支球队的所有比赛

```bash
node scripts/worldcup-calculator.js summary --wc --team 巴西
```

### 场景 4：查看某日所有世界杯比赛

```bash
node scripts/worldcup-calculator.js summary --wc --date 2026-06-14
```

### 场景 5：查看某场比赛的比分赔率

```bash
node scripts/worldcup-calculator.js crs --wc --json | jq '.matches[0]'
```

### 场景 6：跟踪赔率变化

```bash
node scripts/worldcup-calculator.js history 2040166 had
```

### 场景 7：批量获取所有世界杯比赛数据（程序化处理）

```bash
node scripts/worldcup-calculator.js --wc --json > wc_odds.json
```

## 与百度体育赔率（worldcup-match odds）的区别

| 数据源 | 覆盖玩法 | 数据特点 |
|--------|----------|----------|
| 百度体育（worldcup-match） | 亚盘、欧赔、大小球 | 多家博彩公司，胜率分析 |
| 体彩竞彩（calculator） | 8 种官方竞彩玩法 | 中国体彩官方赔率，含让球数 |

两个数据源互补：百度体育看盘口走势，体彩看官方玩法。

## 注意事项

- API 需用移动端 User-Agent，否则会被 Tencent Cloud EdgeOne 拦截（返回 567 错误）。脚本内置 30 个 UA 池（iOS 14-17 + Android 10-14），每次请求随机选择
- 数据实时性：赔率更新延迟约 1-2 分钟
- 赔率变化历史仅保留近期数据，赛前几小时的数据可能为空
- 比分赔率有 31 种，混合过关 9 种，组合计算时注意边界条件
- matchId 与百度体育的 matchId 不通用（不同平台 ID 体系）
- 体彩计算器只展示可投注的赛事，已结束的比赛不会显示
- 日期筛选用的是 `--date YYYY-MM-DD`，与百度体育脚本的 `date` 命令不同
- 高频请求仍可能被风控，建议间隔 1-2 秒
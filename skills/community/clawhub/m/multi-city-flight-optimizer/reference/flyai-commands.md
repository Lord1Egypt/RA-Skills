# FlyAI 命令参考

> ⚠️ **重要**：所有命令执行前需加 `NODE_TLS_REJECT_UNAUTHORIZED=0` 解决 SSL 证书验证问题

## 目录

1. [search-flight - 机票搜索](#search-flight)（核心命令）
2. [keyword-search - 自然语言搜索](#keyword-search)（辅助命令）

---

## search-flight

结构化机票搜索，支持丰富的筛选条件。本技能的核心命令。

**适用场景**：
- 搜索出发地到某个候选城市的去程航班
- 搜索某个候选城市回出发地的回程航班
- 在日期范围内搜索最便宜/最短的航班
- 按中转次数、舱位、价格上限筛选

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "[出发城市]" \
  --destination "[目的地城市]" \
  --dep-date [出发日期] \
  [其他可选参数]
```

**完整参数列表**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--origin` | 出发城市（必填） | "杭州" |
| `--destination` | 目的地城市（必填） | "巴塞罗那" |
| `--dep-date` | 出发日期 (YYYY-MM-DD) | 2026-10-01 |
| `--dep-date-start` | 出发日期范围起始 | 2026-10-01 |
| `--dep-date-end` | 出发日期范围结束 | 2026-10-03 |
| `--back-date` | 返程日期 | 2026-10-07 |
| `--back-date-start` | 返程日期范围起始 | 2026-10-05 |
| `--back-date-end` | 返程日期范围结束 | 2026-10-07 |
| `--journey-type` | 1=直飞, 2=中转 | 1 |
| `--seat-class-name` | 舱位名称 | "经济舱" |
| `--transport-no` | 航班号 | "MU7019" |
| `--transfer-city` | 中转城市 | "迪拜" |
| `--dep-hour-start` | 出发时间起始（小时） | 6 |
| `--dep-hour-end` | 出发时间结束（小时） | 22 |
| `--arr-hour-start` | 到达时间起始 | 6 |
| `--arr-hour-end` | 到达时间结束 | 23 |
| `--total-duration-hour` | 最大飞行时长（小时） | 20 |
| `--max-price` | 最高价格（元） | 8000 |
| `--sort-type` | 排序方式（见下表） | 3 |

**排序类型**：

| sort-type | 说明 |
|-----------|------|
| 1 | 价格降序（贵→便宜） |
| 2 | 推荐排序 |
| 3 | 价格升序（便宜→贵）✅ 常用 |
| 4 | 时长升序（短→长）✅ 省时用 |
| 5 | 时长降序 |
| 6 | 起飞早→晚 |
| 7 | 起飞晚→早 |
| 8 | 直飞优先 ✅ 少中转用 |

### 本技能典型用法

#### 去程搜索（出发地 → 候选城市）

```bash
# 搜索去巴塞罗那的最便宜航班
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date-start 2026-10-01 --dep-date-end 2026-10-02 \
  --sort-type 3

# 搜索去马德里的最便宜航班
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "马德里" \
  --dep-date-start 2026-10-01 --dep-date-end 2026-10-02 \
  --sort-type 3

# 搜索去里斯本的最便宜航班
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "里斯本" \
  --dep-date-start 2026-10-01 --dep-date-end 2026-10-02 \
  --sort-type 3
```

#### 回程搜索（候选城市 → 出发地）

```bash
# 搜索从巴塞罗那回杭州的最便宜航班
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "巴塞罗那" --destination "杭州" \
  --dep-date-start 2026-10-06 --dep-date-end 2026-10-07 \
  --sort-type 3

# 搜索从马德里回杭州
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "马德里" --destination "杭州" \
  --dep-date-start 2026-10-06 --dep-date-end 2026-10-07 \
  --sort-type 3

# 搜索从里斯本回杭州
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "里斯本" --destination "杭州" \
  --dep-date-start 2026-10-06 --dep-date-end 2026-10-07 \
  --sort-type 3
```

#### 带约束的搜索

```bash
# 仅直飞
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date 2026-10-01 \
  --journey-type 1 --sort-type 3

# 指定舱位
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date 2026-10-01 \
  --seat-class-name "经济舱" --sort-type 3

# 限制最高价格
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date 2026-10-01 \
  --max-price 5000 --sort-type 3

# 按飞行时长排序（省时模式）
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "巴塞罗那" \
  --dep-date 2026-10-01 \
  --sort-type 4
```

---

## keyword-search

自然语言搜索，跨所有旅行类别。在本技能中主要用于辅助。

**适用场景**：
- 搜索城市别名对应的航线
- 搜索替代机场
- 查询目的地相关的旅行产品

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "[搜索词]"
```

**示例**：
```bash
# 搜索替代机场
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "杭州飞巴塞罗那 机票"

# 搜索区域航线
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "杭州到南欧 国庆机票"
```

---

## 返回数据提取

FlyAI 返回 JSON 格式数据，在本技能中重点关注以下字段：

### 机票数据

```json
{
  "flightNo": "CX831",               // 航班号
  "depCity": "杭州",                  // 出发城市
  "arrCity": "巴塞罗那",              // 到达城市
  "depTime": "10:30",                 // 出发时间
  "arrTime": "18:45+1",              // 到达时间（+1表示次日）
  "depDate": "2026-10-01",           // 出发日期
  "price": 4580,                      // 价格（单人）
  "totalDuration": "16h30m",         // 总飞行时长（含中转等待）
  "transfers": 1,                     // 中转次数
  "transferCity": "香港",             // 中转城市
  "transferDuration": "2h15m",       // 中转等待时长
  "airline": "国泰航空",              // 航空公司
  "jumpUrl": "https://..."           // 飞猪预订链接
}
```

### 关键提取字段说明

| 字段 | 用途 | 评分维度 |
|------|------|----------|
| `price` | 票价 | 价格得分 |
| `transfers` | 中转次数 | 中转得分 |
| `transferDuration` | 中转等待时长 | 中转得分（辅助） |
| `totalDuration` | 总飞行时长 | 飞行时长得分 |
| `jumpUrl` | 预订链接 | 方案输出 |
| `flightNo` | 航班号 | 方案展示 |
| `depTime` / `arrTime` | 出发/到达时间 | 体验评估（红眼判断） |

### 红眼航班判断规则

```
如果 depTime 在 23:00-05:59 之间 → 标注"🌙 红眼航班"
如果 arrTime 在 00:00-05:59 之间 → 标注"🌙 凌晨到达"
```

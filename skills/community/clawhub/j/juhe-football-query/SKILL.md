---
name: juhe-football-query
description: 足球联赛查询。查询各大足球联赛的赛事赛程和积分榜，支持中超、英超、意甲、德甲、法甲、西乙、苏超等联赛。使用场景：用户说"查一下英超赛程"、"中超积分榜"、"德甲比赛结果"、"意甲最新排名"等。通过聚合数据（juhe.cn）API 实时查询，免费注册每天免费调用。
homepage: https://www.juhe.cn/docs/api/id/90
metadata: {"openclaw":{"emoji":"⚽","requires":{"bins":["python3"],"env":["JUHE_FOOTBALL_KEY"]},"primaryEnv":"JUHE_FOOTBALL_KEY"}}
---

# 足球联赛查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

查询各大足球联赛的**赛事赛程**和**积分榜**：**中超、英超、意甲、德甲、法甲、西乙、苏超**等。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [足球联赛 API](https://www.juhe.cn/docs/api/id/90) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_FOOTBALL_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_FOOTBALL_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/football_query.py  --key 你的 AppKey  --type yingchao
```

> 免费额度：每天免费调用，具体次数以官网为准。

---

## 使用方法

### 查询联赛赛程

```bash
# 查询中超赛程
python scripts/football_query.py --type zhongchao

# 查询英超赛程
python scripts/football_query.py --type yingchao

# 查询意甲赛程
python scripts/football_query.py --type yijia

# 查询德甲赛程
python scripts/football_query.py --type dejia

# 查询法甲赛程
python scripts/football_query.py --type fajia

# 查询西乙赛程
python scripts/football_query.py --type xijia

# 查询苏超赛程
python scripts/football_query.py --type jiangsu
```

### 查询积分榜

```bash
# 查询中超积分榜
python scripts/football_query.py --type zhongchao --rank

# 查询英超积分榜
python scripts/football_query.py --type yingchao --rank
```

### 直接调用 API（无需脚本）

```
# 查询赛事赛程
GET http://apis.juhe.cn/fapig/football/query?key=YOUR_KEY&type=zhongchao

# 查询积分榜
GET http://apis.juhe.cn/fapig/football/rank?key=YOUR_KEY&type=zhongchao
```

---

## 联赛类型说明

| 参数值 | 联赛名称 |
|--------|----------|
| `zhongchao` | 中超 |
| `yingchao` | 英超 |
| `yijia` | 意甲 |
| `dejia` | 德甲 |
| `fajia` | 法甲 |
| `xijia` | 西乙 |
| `jiangsu` | 苏超 |

---

## AI 使用指南

当用户查询足球联赛相关信息时，按以下步骤操作：

1. **识别需求** — 确定用户是想查赛程还是积分榜
2. **确认联赛** — 确定用户查询的是哪个联赛
3. **调用对应接口** — 赛程用 query 接口，积分榜用 rank 接口
4. **展示结果** — 清晰展示赛程或积分榜信息

### 返回字段说明

**赛事赛程接口：**

| 字段 | 含义 | 示例 |
|------|------|------|
| `title` | 联赛名称 | 中超联赛 |
| `duration` | 赛季年份 | 2025 |
| `matchs` | 比赛列表 | [...] |
| `date` | 比赛日期 | 2025-06-15 |
| `week` | 星期 | 星期日 |
| `time_start` | 开赛时间 | 19:00 |
| `team1` | 主队 | 上海海港 |
| `team2` | 客队 | 北京国安 |
| `team1_score` | 主队比分 | 2 |
| `team2_score` | 客队比分 | 1 |
| `status_text` | 比赛状态 | 已完赛/未开赛 |

**积分榜接口：**

| 字段 | 含义 | 示例 |
|------|------|------|
| `rank_id` | 排名 | 1 |
| `team` | 球队名称 | 上海海港 |
| `matches` | 比赛场次 | 15 |
| `wins` | 胜场 | 12 |
| `draw` | 平局 | 2 |
| `losses` | 负场 | 1 |
| `goals` | 进球数 | 35 |
| `losing_goals` | 失球数 | 10 |
| `goal_difference` | 净胜球 | 25 |
| `scores` | 积分 | 38 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/90) 重新申请 |
| `error_code` 10012 | 当日免费次数已用尽，建议升级套餐 |
| 联赛类型错误 | 检查 type 参数是否正确, 提示用户输入正确的联赛类型 |
| 无搜索结果 | 告知用户未找到相关联赛，建议更换联赛类型 |

---

## 脚本位置

`scripts/football_query.py` — 封装了 API 调用、赛程查询、积分榜查询和结果格式化。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **体育赛事**：足球联赛赛程、积分榜查询
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号实名认证、身份证实名验证

注册即可免费使用，适合个人开发者和企业接入。

---
name: jike-caipiao-lottery-query
description: 查询彩票最新开奖、指定彩种期开奖详情、福彩3D/排列3历史号码和冷热号统计。适用场景：用户询问“最新彩票开奖”“双色球 2024001 开奖详情”“666 历史开出过几次”“福彩3D 热门号码”等开奖数据查询。数据由即刻数据（jikeapi.cn）开放接口提供，仅用于开奖信息查询，不提供预测或投注建议。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🎫","requires":{"bins":["python3"],"env":["JIKE_CAIPIAO_LOTTERY_QUERY_KEY"]},"primaryEnv":"JIKE_CAIPIAO_LOTTERY_QUERY_KEY"}}
---

# 彩票查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供。用于查询公开开奖数据，包括最新开奖、开奖详情、历史号码和冷热号统计。

输入彩票类型、期号或三位开奖号码，查询：**开奖日期、期号、开奖号码、销售额、奖池、奖项明细、历史出现次数、冷热号统计**。

---

## 前置配置：获取 AppKey

1. 登录即刻数据官网。
2. 申请「彩票查询」接口。
3. 在「个人中心 -> 我的 API 应用」中获取接口 `AppKey`。
4. 配置 Key（推荐使用环境变量）：

```bash
# 方式一：环境变量（推荐）
export JIKE_CAIPIAO_LOTTERY_QUERY_KEY=你的AppKey

# 方式二：通用环境变量
export JIKE_APPKEY=你的AppKey

# 方式三：脚本目录 .env 文件（本地测试使用）
echo "JIKE_CAIPIAO_LOTTERY_QUERY_KEY=你的AppKey" > scripts/.env
```

Windows 用户可在系统环境变量中新增：

```text
变量名：JIKE_CAIPIAO_LOTTERY_QUERY_KEY
变量值：你的AppKey
```

> 不要把真实 AppKey 写进公开仓库或上传到 Skill 包中。

---

## 使用方法

### 查询最新开奖

```bash
python3 scripts/caipiao_lottery_query.py latest
```

### 查询指定期号开奖详情

```bash
python3 scripts/caipiao_lottery_query.py detail --type ssq --sn 2024001
```

支持的 `type`：

```text
dlt 大乐透
pl3 排列3
pl5 排列5
qxc 七星彩
ssq 双色球
fc3d 福彩3D
qlc 七乐彩
kl8 快乐8
```

### 查询三位号码历史出现记录

```bash
python3 scripts/caipiao_lottery_query.py number-history --type pl3 --number 666
```

`number-history` 仅支持 `pl3`、`fc3d`。

### 查询冷热号统计

```bash
python3 scripts/caipiao_lottery_query.py number-stat --type fc3d
```

`number-stat` 仅支持 `pl3`、`fc3d`。

### 输出接口原始 JSON

```bash
python3 scripts/caipiao_lottery_query.py latest --json
python3 scripts/caipiao_lottery_query.py detail --type ssq --sn 2024001 --json
```

---

## 直接调用 API

```text
GET https://api.jikeapi.cn/v1/caipiao/lottery/latest?appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/caipiao/lottery/detail?type=ssq&sn=2024001&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/caipiao/lottery/number_history?type=pl3&number=666&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/caipiao/lottery/number_stat?type=fc3d&appkey=YOUR_APPKEY
```

---

## AI 使用步骤

1. 用户问最新开奖时，执行 `latest`。
2. 用户问某彩种某期详情时，提取彩票类型和期号，执行 `detail`。
3. 用户问三位号码历史出现次数时，执行 `number-history`，仅支持 `pl3`、`fc3d`。
4. 用户问冷热号统计时，执行 `number-stat`，仅支持 `pl3`、`fc3d`。
5. 回复时只展示开奖事实和统计结果，不做预测，不给投注建议。

---

## 脚本位置

`scripts/caipiao_lottery_query.py`

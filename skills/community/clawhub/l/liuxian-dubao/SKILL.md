---
name: 刘半仙卜卦
description: 虾猜平台大六壬预测 — 注册认证、比赛预测、结果结算、战绩看板
version: 1.0.0
---

# 🎲 刘半仙卜卦 — 虾猜大六壬预测助手

> **"卦不算空，算卦不收空。刘半仙起课，包你大吉大利！"**

通过 Agent API Gateway 调用虾猜（Xiacai）平台接口，使用大六壬神数预测体育赛事，并提供完整的战绩追踪和结算查看能力。

## 能力总览

| 能力 | 说明 | 用户示例 | 详细说明 |
|------|------|----------|----------|
| 注册认证 | 首次使用注册、获取/检查 API Key | "注册虾猜""我的虾猜账号" | `认证.md` |
| 查看赛事 | 浏览即将开赛/进行中的比赛 | "最近有什么比赛可以猜""查查NBA赛程" | `赛事.md` |
| 大六壬预测 | 对指定比赛起课预测（含三维预测） | "预测勇士对湖人谁赢""算算今晚世界杯" | `预测.md` |
| 战绩看板 | 查看历史预测和结算结果 | "我猜过哪些比赛""看看战绩" | `战绩.md` |

---

## 接口调用规范

### 统一入口

```
https://xiacai.coze.site/api/v1
```

### 鉴权

- Header：`agent-auth-api-key: $XIACAI_API_KEY`
- `XIACAI_API_KEY` 从环境变量获取，格式 `xc_xxxxxxxx`
- 若未设置，提示用户设置
- API Key 绑定用户身份，会自动关联到对应账号

### 请求格式

- **Method**：GET/POST
- **Content-Type**：application/json
- **Body**：JSON

```bash
# GET 示例
curl -X GET "https://xiacai.coze.site/api/v1/matches?status=upcoming" \
  -H "agent-auth-api-key: $XIACAI_API_KEY"

# POST 示例
curl -X POST "https://xiacai.coze.site/api/v2/predictions" \
  -H "agent-auth-api-key: $XIACAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"match_id": "xxx", "predictions": [...]}'
```

### 响应格式

- JSON，`success` 为 `true` 表示成功
- `success` 为 `false` 时 `error` 字段包含错误信息

### 通用规则

1. **先查后猜**：用户说"预测某场比赛"时，先调 `/matches` 确认比赛存在且状态为 `upcoming`，再发布预测
2. **大六壬起课**：以比赛开赛时间起课，分析课体（伏吟/反吟/别责等）、三传、神煞，给出预测结论
3. **三维预测**：虾猜 v2 预测接口支持三个维度（胜平负/让分/大小分），尽量覆盖
4. **结果追踪**：预测发布后返回 `prediction_id`，后续用 `/predictions` 查看结算
5. **话术包装**：预测结论用刘半仙经典风格——"大吉""稳了""凶中带吉""不宜重注"，**只说好话，图个乐子** 😄
6. **战绩冷静期**：预测不准时用"卦算不准？那是你八字不合！"——友哥亲传的经典台词🌪️

### 环境变量

```
XIACAI_API_KEY=xc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 文件索引

| 文件 | 内容 | 适用场景 |
|:----|:-----|:---------|
| `认证.md` | 注册、API Key、个人信息 | 首次使用、验证身份 |
| `赛事.md` | 比赛列表、赛程筛选、月将/占时速查表 | 查有什么比赛可以猜 |
| `预测.md` | 大六壬全流程 + 实战案例 | 做预测时参考 |
| `战绩.md` | 结算查看、战绩话术库 | 查看预测结果 |
| `错误处理.md` | 状态码、错误码、排查指南、重试策略 | API报错时查阅 |

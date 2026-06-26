# 5 天成都行程规划示例

## 用户输入

> 我想去成都玩 5 天，2 个人，喜欢美食和文化，预算 6000 元

## 信息完整度检查

- ① 城市: 成都 ✅
- ② 天数: 5 天 ✅
- ③ 人数: 2 人 ✅
- ④ 兴趣: 美食、文化 ✅
- ⑤ 预算: 6000 元 ✅

全齐，直接生成。

## 工具调用

```
→ generate_travel_itinerary({
    destination: "成都",
    days: 5,
    budget: 6000,
    preferences: {
      interests: ["food", "culture"],
      pace: "moderate",
      accommodation_type: "mid-range",
      prefer_public_transport: true
    }
  })
```

## 生成结果（示意）

### Day 1 — 市区文化游

| 时间 | 活动 | 地点 |
|------|------|------|
| 09:00 | 宽窄巷子 | 青羊区 |
| 12:00 | 午餐：陈麻婆豆腐 | 青羊区 |
| 14:00 | 人民公园 + 鹤鸣茶社 | 青羊区 |
| 16:30 | 太古里 | 锦江区 |
| 18:30 | 晚餐：小龙坎火锅 | 锦江区 |

### Day 2 — 大熊猫 + 武侯祠

| 时间 | 活动 | 地点 |
|------|------|------|
| 07:30 | 成都大熊猫繁育研究基地 | 成华区 |
| 12:00 | 午餐：甘记肥肠粉 | 武侯区 |
| 14:00 | 武侯祠 | 武侯区 |
| 16:00 | 锦里古街 | 武侯区 |
| 18:30 | 晚餐：钢管厂五区小郡肝串串香 | 武侯区 |

### Day 3-5 ...

（后续包含青城山、都江堰、金沙遗址等）

## 多轮调整示例

> 用户: "第二天不想去武侯祠，换成金沙遗址博物馆"

```
→ generate_travel_itinerary({
    destination: "成都",
    days: 5,
    budget: 6000,
    preferences: { interests: ["food", "culture"], pace: "moderate" }
    // 在 AI 提示中附带调整说明
  })
```

## 补充工具调用（用户追问时）

> 用户: "帮我看看酒店"

```
→ search_hotels({
    city: "成都",
    check_in: "2026-03-15",
    check_out: "2026-03-20",
    guests: 2,
    max_price: 400,
    location_preference: "市中心"
  })
```

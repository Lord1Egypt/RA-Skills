# 旅行内容查询示例

## 场景 1: 搜索攻略

> 用户: "帮我找找京都的旅行攻略"

```bash
npx lovtrip search "京都"
```

输出:
```
🔍 搜索: "京都" (共 5 条结果)

📖 京都3天经典路线
   伏见稻荷、清水寺、岚山竹林...
   https://lovtrip.app/guides/kyoto-3-day-classic

📖 京都美食深度游
   怀石料理、抹茶甜点、锦市场...
   https://lovtrip.app/guides/kyoto-food-deep-dive

📖 京都赏樱攻略
   哲学之道、圆山公园、醍醐寺...
   https://lovtrip.app/guides/kyoto-cherry-blossom
```

## 场景 2: 查看热门目的地

> 用户: "最近有什么热门目的地？"

```bash
npx lovtrip destinations --trending
```

## 场景 3: 查看攻略详情

> 用户: "看看京都3天经典路线的详情"

```bash
npx lovtrip guide kyoto-3-day-classic
```

## 场景 4: JSON 输出（程序化处理）

```bash
npx lovtrip search "Bali" --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('results', []):
    print(f\"- {item['title']}: {item.get('url', 'N/A')}\")
"
```

## 场景 5: curl 直接调用

```bash
# 搜索
curl -s "https://lovtrip.app/api/search?q=东京美食" | python3 -m json.tool

# 热门目的地
curl -s "https://lovtrip.app/api/destinations/trending" | python3 -m json.tool

# 按目的地筛选攻略
curl -s "https://lovtrip.app/api/guides?destination=Tokyo&limit=5" | python3 -m json.tool
```

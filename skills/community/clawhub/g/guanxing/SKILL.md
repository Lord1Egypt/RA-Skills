---
name: guanxing
description: "Chinese metaphysics AI — BaZi (八字), daily fortune, crypto fortune, Feng Shui, Tarot, I-Ching divination, dream interpretation, name scoring, compatibility matching, zodiac analysis. Powered by 观星 GuanXing API."
version: 1.0.0
user-invocable: true
metadata:
  clawdbot:
    emoji: "🔮"
    requires:
      env: ["GUANXING_API_KEY"]
    primaryEnv: "GUANXING_API_KEY"
---

# 观星 GuanXing — Chinese Metaphysics AI

A comprehensive Chinese metaphysics toolkit. Call the GuanXing API to provide BaZi birth chart analysis, daily fortune, crypto token fortune (五行), Feng Shui, Tarot, I-Ching divination, dream interpretation, name scoring, compatibility matching, and zodiac readings.

## Setup

Get a free API key at https://heartai.zeabur.app (register → Developer Center → Create App → copy your `gx_sk_` key).

Set the environment variable:
```
GUANXING_API_KEY=gx_sk_your_key_here
```

Base URL: `https://heartai.zeabur.app`

## Authentication

All requests require a Bearer token in the Authorization header:
```
Authorization: Bearer $GUANXING_API_KEY
Content-Type: application/json
```

## External Endpoints

| Endpoint | Method | Purpose | Data Sent |
|----------|--------|---------|-----------|
| `https://heartai.zeabur.app/api/v1/bazi` | POST | BaZi birth chart analysis | Birth date, birth hour, name |
| `https://heartai.zeabur.app/api/v1/fortune` | POST | Daily fortune reading | Zodiac sign, birth date |
| `https://heartai.zeabur.app/api/v1/crypto-fortune` | POST | Crypto token fortune | Token symbol |
| `https://heartai.zeabur.app/api/v1/qiuqian` | POST | I-Ching divination (求签) | Category, question |
| `https://heartai.zeabur.app/api/v1/tarot` | POST | Tarot card reading | Question, spread type |
| `https://heartai.zeabur.app/api/v1/dream` | POST | Dream interpretation | Dream description |
| `https://heartai.zeabur.app/api/v1/almanac` | POST | Chinese almanac | Date |
| `https://heartai.zeabur.app/api/v1/fengshui` | POST | Feng Shui analysis | Direction, element, space type |
| `https://heartai.zeabur.app/api/v1/name-score` | POST | Chinese name scoring | Full name |
| `https://heartai.zeabur.app/api/v1/compatibility` | POST | Compatibility matching | Two birth dates |
| `https://heartai.zeabur.app/api/v1/zodiac` | POST | Chinese zodiac fortune | Birth year or zodiac sign |

## Security & Privacy

- All data is sent to the GuanXing API at `heartai.zeabur.app` over HTTPS.
- No data is stored locally. No files are read or written.
- The API processes birth dates and names to generate fortune readings. No data is shared with third parties.
- By using this skill, your data is sent to the GuanXing (观星) service. Only install if you trust this service.

## Model Invocation Note

This skill may be invoked autonomously by the agent when the user asks about fortune, 命理, 八字, zodiac, crypto luck, Feng Shui, or related topics. This is standard behavior. You can opt out by removing the skill.

## Actions

### 1. BaZi Birth Chart (八字命理)

When the user asks about their birth chart, 八字, destiny, life path, or 命格:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/bazi \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"birthDate": "YYYY-MM-DD", "birthHour": HOUR_0_TO_23, "name": "NAME"}'
```

- `birthDate` (required): Birth date in YYYY-MM-DD format
- `birthHour` (optional): Birth hour 0-23 (maps to 十二时辰)
- `name` (optional): User's name for personalized reading

Ask the user for their birth date if not provided. Birth hour improves accuracy but is optional.

### 2. Daily Fortune (每日运势)

When the user asks about today's fortune, luck, or 运势:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/fortune \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zodiac": "ZODIAC_SIGN", "birthDate": "YYYY-MM-DD"}'
```

- `zodiac` (required): Chinese zodiac sign name like 白羊座, 金牛座, etc.
- `birthDate` (optional): For personalized 八字-based fortune

### 3. Crypto Fortune (加密运势)

When the user asks about crypto luck, token fortune, or 币圈运势:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/crypto-fortune \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"token": "BTC"}'
```

- `token` (required): Token symbol — BTC, ETH, SOL, BNB, TON, DOGE, AVAX
- Token-to-五行 mapping: BTC→金(Metal), ETH→水(Water), SOL→火(Fire), BNB→土(Earth), TON→木(Wood)

For a portfolio overview, call the endpoint for each token the user holds.

### 4. I-Ching Divination (求签)

When the user wants to divine, draw a fortune stick, or 求签:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/qiuqian \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "CATEGORY", "question": "USER_QUESTION"}'
```

- `category` (optional): 事业 (career), 感情 (love), 财运 (wealth), 学业 (study), 健康 (health)
- `question` (optional): Specific question the user wants answered

### 5. Tarot Reading (塔罗牌)

When the user asks for a tarot reading:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/tarot \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "USER_QUESTION", "spread": "SPREAD_TYPE"}'
```

- `question` (optional): The question to explore
- `spread` (optional): "single" (one card), "three" (past-present-future), "celtic" (full spread)

### 6. Dream Interpretation (解梦)

When the user describes a dream and wants it interpreted:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/dream \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dream": "DREAM_DESCRIPTION"}'
```

- `dream` (required): The user's dream description

### 7. Chinese Almanac (老黄历)

When the user asks what's auspicious today, 宜忌, or 老黄历:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/almanac \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"date": "YYYY-MM-DD"}'
```

- `date` (optional): Defaults to today if not specified

### 8. Feng Shui Analysis (风水)

When the user asks about Feng Shui, home layout, or 方位:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/fengshui \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"direction": "DIRECTION", "element": "ELEMENT", "spaceType": "SPACE_TYPE"}'
```

- `direction` (optional): 东/南/西/北/东南/西南/东北/西北
- `element` (optional): 金/木/水/火/土
- `spaceType` (optional): 办公室 (office), 卧室 (bedroom), 客厅 (living room)

### 9. Name Scoring (姓名打分)

When the user wants to score a name or analyze name meaning:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/name-score \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "FULL_NAME"}'
```

- `name` (required): Chinese or English full name

### 10. Compatibility (缘分合盘)

When the user asks about compatibility with someone:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/compatibility \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"person1": {"birthDate": "YYYY-MM-DD", "name": "NAME1"}, "person2": {"birthDate": "YYYY-MM-DD", "name": "NAME2"}}'
```

- Both `person1` and `person2` require `birthDate`. `name` is optional.

### 11. Zodiac Fortune (生肖运势)

When the user asks about their Chinese zodiac:

```bash
curl -s -X POST https://heartai.zeabur.app/api/v1/zodiac \
  -H "Authorization: Bearer $GUANXING_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zodiac": "ZODIAC_ANIMAL", "birthYear": YEAR}'
```

- `zodiac` (optional): 鼠/牛/虎/兔/龙/蛇/马/羊/猴/鸡/狗/猪
- `birthYear` (optional): Birth year to auto-determine zodiac

## Response Handling

All endpoints return JSON with this structure:
```json
{
  "success": true,
  "data": { ... },
  "meta": { "skill": "...", "tokensUsed": 245, "latencyMs": 1200 }
}
```

If `success` is false, the response includes an `error` field. Report the error message to the user in a friendly way.

## Response Formatting

When presenting results to the user:
- Use the Chinese terms naturally (八字, 五行, 天干地支, etc.)
- Format fortune scores as X/100 or X/5 stars
- Highlight lucky colors, numbers, and directions
- For crypto fortune, mention the 五行 element relationship
- Keep the tone warm and insightful, not clinical
- If the user speaks English, translate key Chinese metaphysics terms with brief explanations

## Trust Statement

By using this skill, data you provide (birth dates, names, questions) is sent to the GuanXing (观星) API at heartai.zeabur.app for processing. The API uses AI to generate metaphysics readings. Only install if you trust this service. API documentation: https://heartai.zeabur.app

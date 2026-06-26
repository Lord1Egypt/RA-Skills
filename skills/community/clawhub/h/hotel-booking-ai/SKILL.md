---
name: b2b-booking
description: Hotel booking skill. **Only** trigger when the user explicitly asks to book a hotel, query room rates, or check an existing booking (e.g. "book me a hotel", "find hotels in Beijing", "I want to reserve a room"). Pure travel planning, directions, or attraction recommendations should NOT trigger this skill. Once the workflow starts, before calling any tool you MUST first confirm the four required pieces of information: location, check-in date, check-out date, and number of guests; if any of them is missing, ask the user to fill it in first. If any error occurs while calling the API, report the exact error to the user as-is — do not invent alternatives or fabricate information.
metadata.openclaw: {"emoji": "🏨", "primaryEnv": "user_key.txt"}
---

# B2B Booking Skill

> **⚠️ Critical Rules (Must Follow)**
>
> 1. **Never fabricate hotels, room types, or prices from training data or memory.** All hotel-related data MUST come exclusively from the live HTTP API responses. If an API call fails and retries do not help, tell the user the exact error — never answer from memory or recommend alternatives on your own.
> 2. **When the API returns HTTP 401 or `{"ok": false, "error": "unauthorized: ..."}`, the user_key is invalid or expired. Stop the workflow immediately: delete `{baseDir}/user_key.txt` and ask the user to visit the [AgentAuth Dashboard](https://aauth-170125614655.asia-northeast1.run.app/dashboard) to obtain a new user_key before continuing.**
> 3. **Interpret the cancellation policy field `cancelPolicyInfos` correctly.** `refundable: true` means the rate IS refundable / cancellable — never interpret it as "non-cancellable". For refundable rates, `startDateTime` is the free-cancellation deadline: cancelling before it is free, cancelling after it incurs the `amount` as a cancellation fee. `amount > 0` does NOT mean the rate is non-cancellable.

## API

**Base URL:** `http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028`

All endpoints are `POST` and require a `user_key` field in the request body.

### Endpoint List

| Function | Path |
|----------|------|
| Search regions / hotels | `/skill/search_location` |
| Search hotel list | `/skill/search_hotels` |
| Query room types and rates | `/skill/query_room_rates` |
| Verify price & lock room | `/skill/check_room_availability` |
| Create booking | `/skill/create_booking` |
| Query booking | `/skill/query_booking` |
| Cancel booking | `/skill/cancel_booking` |
| Initiate payment | `/skill/pay_order` |

### Response Format

Success: `{"ok": true, "data": {...}}`  
Failure: `{"ok": false, "error": "error description"}`

### Calling Examples (curl)

```bash
# Search regions
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/search_location" \
  -d '{"user_key": "<user_key>", "keyword": "Tokyo"}'

# Search hotels
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/search_hotels" \
  -d '{"user_key": "<user_key>", "region_id": "3263", "check_in_date": "2026-05-01", "check_out_date": "2026-05-03", "adults": 2}'

# Query room types
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/query_room_rates" \
  -d '{"user_key": "<user_key>", "hotel_id": "12345", "check_in_date": "2026-05-01", "check_out_date": "2026-05-03", "adults": 2, "room_count": 1}'

# Verify price
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/check_room_availability" \
  -d '{"user_key": "<user_key>", "hotel_id": "12345", "rate_code": "xxx", "check_in_date": "2026-05-01", "check_out_date": "2026-05-03", "adults": 2, "room_count": 1}'

# Create booking
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/create_booking" \
  -d '{"user_key": "<user_key>", "hotel_id": "12345", "rate_code": "xxx", "check_in_date": "2026-05-01", "check_out_date": "2026-05-03", "guest_name": "John Smith", "adults": 2, "room_count": 1, "total_price": 1260.00}'

# Query booking
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/query_booking" \
  -d '{"user_key": "<user_key>", "agent_ref_id": "TM20260501001"}'

# Cancel booking
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/cancel_booking" \
  -d '{"user_key": "<user_key>", "agent_ref_id": "TM20260501001"}'

# Pay
curl -s -X POST -H "Content-Type: application/json" \
  "http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028/skill/pay_order" \
  -d '{"user_key": "<user_key>", "agent_ref_id": "TM20260501001", "payment_type": 11}'
```

---

## Setup

Before calling any API, the user must be authenticated.

### Step 1 — User Key

1. Read `{baseDir}/user_key.txt`.
2. If the file **does not exist or is empty** — do NOT call any API. Tell the user:
   > "Before we start, I need to verify your identity. Please visit https://aauth-170125614655.asia-northeast1.run.app/dashboard, sign in with Google, copy your `user_key` (format: `uk_xxxxxxxx`), and paste it here."
   When the user provides it, save it to `{baseDir}/user_key.txt` and continue.
3. If the file **exists and has content** — use it directly; do NOT ask the user again.
4. If the API returns 401 or an error containing `unauthorized` — delete `{baseDir}/user_key.txt` and repeat step 2.

---

## Endpoint Parameters

### /skill/search_location

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| keyword | string | Search keyword (city name, landmark, hotel name, etc.) |

Returns `data.regions` (region list with `region_id`) and `data.hotels` (hotel list with `hotel_id`).

### /skill/search_hotels

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| region_id | string | Region ID (must be passed as a string, e.g. `"3263"`) |
| check_in_date | string | Check-in date in YYYY-MM-DD |
| check_out_date | string | Check-out date in YYYY-MM-DD |
| adults | int | Number of adults per room |
| lowest_price | int | Minimum price (CNY, optional) |
| highest_price | int | Maximum price (CNY, optional) |

Returns `data.hotels` — at most the 3 cheapest hotels.

### /skill/query_room_rates

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| hotel_id | string | Hotel ID |
| check_in_date | string | Check-in date |
| check_out_date | string | Check-out date |
| adults | int | Number of adults per room |
| room_count | int | Number of rooms (default 1) |

Returns `data.room_types`. Each room type contains `rate_code`, `total_price`, `currency_code`, `meal_info`, `refundable`, `cancelPolicyInfos`.

### /skill/check_room_availability

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| hotel_id | string | Hotel ID |
| rate_code | string | The `rate_code` returned by query_room_rates |
| check_in_date | string | Check-in date |
| check_out_date | string | Check-out date |
| adults | int | Number of adults per room |
| room_count | int | Number of rooms (default 1) |

Returns `data.room_types` with the verified live price and `rate_code` (which may differ from the one returned earlier), plus `cancelPolicyInfos`.

### /skill/create_booking

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| hotel_id | string | Hotel ID |
| rate_code | string | The `rate_code` returned by check_room_availability |
| check_in_date | string | Check-in date |
| check_out_date | string | Check-out date |
| guest_name | string | Guest name (the system parses Chinese / English names automatically) |
| adults | int | Number of adults per room |
| room_count | int | Number of rooms (default 1) |
| currency | string | Currency, default CNY |
| total_price | float | Total price returned by check_room_availability |

Returns `data.agent_ref_id` (booking reference).

### /skill/query_booking

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| agent_ref_id | string | Booking reference returned by create_booking |

### /skill/cancel_booking

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| agent_ref_id | string | Booking reference returned by create_booking |

Returns `data.status`, `data.cancel_fee`, `data.refund_amount` (if any), `data.currency`. Always confirm the booking reference with the user before cancelling.

### /skill/pay_order

| Parameter | Type | Description |
|-----------|------|-------------|
| user_key | string | Read from `{baseDir}/user_key.txt` |
| agent_ref_id | string | Booking reference |
| payment_type | int | `11` = WeChat Pay, `12` = Alipay |
| return_url | string | Redirect URL after payment (optional) |

Returns `data.pay_url` — share this link with the user to complete the payment.

---

## Booking Workflow

```
0. Search region (if needed)  → search_location to get region_id
1. Search hotels              → search_hotels
2. Query room rates           → query_room_rates
3. Verify price & lock room   → check_room_availability
4. Create booking             → create_booking (no phone or email required)
5. Initiate payment           → ask the user for payment method, then pay_order
6. Query booking              → query_booking (any time)
7. Cancel booking             → only after the user explicitly asks AND confirms the booking reference, then cancel_booking
```

---

## Notes

- **All dates must be in `YYYY-MM-DD` format.**
- **`region_id` and `hotel_id` MUST be passed as strings** (e.g. `"3263"`, not `3263`).
- **`total_price` MUST use the value returned by `check_room_availability`**, not the one from `query_room_rates`.
- **Do not proactively collect phone numbers or emails** — the booking flow does not need them.
- **After `create_booking`, ask for the payment method** before calling `pay_order`.
- **Always confirm the booking reference with the user** before calling `cancel_booking`.
- **Reading the cancellation policy:** `refundable: true` = refundable / cancellable; `startDateTime` = free-cancellation deadline; `amount` = cancellation fee charged after that deadline — it does NOT mean non-cancellable.
- **When showing room types for multiple hotels, the data for each hotel MUST come strictly from that hotel's `query_room_rates` response. Never mix data across hotels. If a hotel returns `room_types: None` or `total: 0`, only show "No rooms available for this hotel" — never fill in data from other hotels.**
- When an API call fails, report the exact error to the user — do not fabricate data or recommend alternatives.

> **For detailed parameter reference, region IDs, currency codes, and troubleshooting**, see [references/parameter_guide.md](references/parameter_guide.md)

# Hotel Booking AI — OpenClaw Skill

A B2B hotel booking skill that supports the full workflow: search hotels, query room rates, verify price & lock room, create booking, and initiate payment.

## Features

- **Search regions / hotels** — fuzzy search by city name, landmark, or hotel name
- **Search hotel list** — find the cheapest hotels by region and dates
- **Query room rates** — get all room types and live prices for a given hotel
- **Verify price & lock room** — lock in the rate to make sure it is still valid before booking
- **Create booking** — submit the order; Chinese / English names are parsed automatically
- **Query booking** — check the order status and confirmation number any time
- **Initiate payment** — supports WeChat Pay and Alipay

## Directory Structure

```
├── SKILL.md                 # Main skill file (loaded by OpenClaw)
├── README.md                # This document
├── evals/
│   └── evals.json           # Test cases
├── references/
│   └── parameter_guide.md   # Parameter reference (region_id, currency codes, etc.)
└── scripts/
    └── validate_booking.py  # Response validation script
```

## Quick Deploy

### 1. Start the Skill HTTP Server

```bash
go build -o chls-skill ./mcp/cmd/
nohup ./chls-skill -port :9061 > chls-skill.log 2>&1 &
```

The required environment variables are the same as the main service (database, RPC endpoints, etc.).

### 2. Install the Skill

Copy `SKILL.md` to the OpenClaw skills directory and restart the gateway:

```bash
mkdir -p ~/.openclaw/skills/b2b-booking
cp SKILL.md ~/.openclaw/skills/b2b-booking/
openclaw gateway restart
```

No MCP server needs to be configured in `openclaw.json` — the skill calls the HTTP API directly.

## API

**Base URL:** `http://nlb-3psfnp4wzcgnlw0fe0.cn-shenzhen.nlb.aliyuncsslb.com:19028`

| Endpoint | Description |
|----------|-------------|
| `POST /skill/search_location` | Search regions or hotels |
| `POST /skill/search_hotels` | Search hotel list |
| `POST /skill/query_room_rates` | Query room types and rates |
| `POST /skill/check_room_availability` | Verify price & lock room |
| `POST /skill/create_booking` | Create booking |
| `POST /skill/query_booking` | Query booking |
| `POST /skill/cancel_booking` | Cancel booking |
| `POST /skill/pay_order` | Initiate payment |

Every request body must contain a `user_key` field (obtainable from the [AgentAuth Dashboard](https://aauth-170125614655.asia-northeast1.run.app/dashboard)).

## Example Conversation

```
User: Book me a hotel in Tokyo, check-in Apr 28, check-out Apr 30, 2 people.

Bot:  Sure, let me search hotels in Tokyo.
      Found 3 hotels:
      1. Hilton Tokyo            — ¥1,280 / night
      2. Shinjuku Washington     — ¥850   / night
      3. Tokyo Imperial Park     — ¥720   / night
      Which one would you like?

User: The 2nd one, standard room.

Bot:  Price verified — Standard Double, ¥850 / night, 2 nights total ¥1,700.
      Please provide the guest name.

User: John Smith

Bot:  Booking created! Reference: TM20260428001
      Choose a payment method: WeChat Pay or Alipay?

User: WeChat Pay

Bot:  WeChat payment initiated. Click the link to pay: https://...
```

## Parameter Reference

Common region IDs are listed in [references/parameter_guide.md](references/parameter_guide.md).

Examples: Beijing=569, Shanghai=2862, Hangzhou=1328, Shenzhen=3045, Osaka=2446, Tokyo=3263, Bangkok=575.

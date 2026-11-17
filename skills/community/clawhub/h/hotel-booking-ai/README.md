<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">Hotel Booking AI</a></b><br />
  <strong>Your Personal AI Hotel Search & Booking Assistant</strong>
</h1>

<a href="https://auth.journione.ai/">
  <img alt="Hotel Booking AI — search, compare, and book hotels with your AI agent" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  Find a better stay. Compare live prices. Book with confidence.
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">Product Page</a> |
  <span>Live Demo</span> |
  <a href="https://tourmind.com">Company</a>
</div>

<br />

[![ClawHub downloads](https://img.shields.io/badge/ClawHub_downloads-1.6k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Skill version](https://img.shields.io/badge/Skill_version-1.0.8-2563EB)](SKILL.md)
[![License](https://img.shields.io/github/license/tourmind-com/Hotel-Booking-AI)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

Turn your AI agent into a personal hotel booking assistant. Hotel Booking AI searches hotels worldwide, compares live room prices from leading OTAs and hotel suppliers, shows photos and cancellation terms, verifies the final rate, and helps you complete booking, payment, cancellation, and order lookup in one conversation.

Hotel search, room details, live rates, and availability checks are public—no account or sign-in is required until you are ready to book.

## Demo

### 1. Discover hotels with live availability

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="Hotel Booking AI live hotel search demo" width="720" />
  </a>
</div>

### 2. Compare rooms, photos, and prices

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="Hotel Booking AI room and price comparison demo" width="720" />
  </a>
</div>

### 3. Recheck the rate and pay securely

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="Hotel Booking AI booking and payment demo" width="720" />
  </a>
</div>

## Plan and book your stay in one chat

- Search by city, hotel, landmark, station, address, ski area, or other point of interest without guessed coordinates.
- Compare up to 20 hotel candidates and receive the five best options backed by matching live room products.
- See real nightly and stay-total prices, room and hotel photos, bed types, meals, taxes, cancellation policies, and inventory status.
- Filter for the details that matter to you, such as budget, distance, star rating, breakfast, facilities, room type, or free cancellation.
- Understand why each hotel matches your trip instead of receiving generic recommendations.
- Recheck the exact room price and availability before confirming your booking.
- Book a room, pay with Stripe, WeChat Pay, or Alipay, look up an order, or cancel an eligible reservation through the same conversation.

## Supported AI clients

| Client | How to use Hotel Booking AI |
|---|---|
| OpenClaw | Install directly from ClawHub or clone this repository into your personal Skills directory |
| WorkBuddy | Install or import this repository as a user Skill |
| OpenAI Codex | Install from the Skills interface or a supported local Skills directory |
| Claude Code | Install as a personal Skill under `~/.claude/skills` |
| Agent Skills-compatible clients | Use any client that can load a root `SKILL.md` and make outbound HTTPS `POST` requests |
| MCP-capable AI clients | Use the companion [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) package |

## Install in 1 minute

### Option 1: Install from ClawHub

```bash
openclaw skills install @tourmind/hotel-booking-ai
openclaw gateway restart
```

### Option 2: Import from GitHub

In your AI client's Skills interface, install or import this repository:

```text
https://github.com/tourmind-com/Hotel-Booking-AI.git
```

If your client installs Skills from the filesystem, clone the repository into its personal Skills directory:

```bash
CLIENT_SKILLS_DIR="<your-client-skills-directory>"
mkdir -p "$CLIENT_SKILLS_DIR"
git clone https://github.com/tourmind-com/Hotel-Booking-AI.git "$CLIENT_SKILLS_DIR/hotel-booking-ai"
```

Common personal Skill locations:

| Client | Directory |
|---|---|
| OpenClaw | `~/.openclaw/skills` |
| WorkBuddy | `~/.workbuddy/skills` |
| OpenAI Codex | Use the Skills interface or the local directory supported by your Codex version |
| Claude Code | `~/.claude/skills` |

Reload Skills or restart your AI client, then ask for a hotel. No local MCP server is required; Hotel Booking AI calls the TourMind API directly over HTTPS.

## Search first, sign in only when you book

You can search hotels, inspect hotel and room details, compare live rates, and verify availability without a `user_key`.

When you are ready to create, view, cancel, or pay for a booking:

1. Sign in with Google at [auth.journione.ai](https://auth.journione.ai).
2. Copy your `user_key` and save it as `user_key.txt` in the installed `hotel-booking-ai` folder. Your AI agent can also guide you through this step when you start an order operation.
3. On macOS or Linux, restrict access to the file:

   ```bash
   chmod 600 user_key.txt
   ```

Never commit `user_key.txt`. It is excluded by `.gitignore` and should stay only on your device.

## Try these prompts

Use natural language—the more you share about your trip, the more precisely your AI agent can compare verified hotel options.

```text
I’m taking my family of four to Tokyo from April 3 to April 7, 2027. Find one room near a station with easy access to Tokyo Disneyland, breakfast, free cancellation, and a total price under JPY 120,000. Compare the five best available hotels with photos, room type, bed setup, nightly and total price, travel trade-offs, and cancellation deadlines. Do not book yet.
```

```text
Find a beachfront hotel in Phuket for two adults from November 12 to November 16, 2026. Keep the average price under THB 6,000 per night. I prefer a pool, breakfast, a king bed, and free cancellation. Show only options with matching live rooms, explain what each hotel does and does not meet, and rank them by overall fit.
```

```text
Show me the available rooms at the second hotel. Include room photos, bed type, meals, cancellation policy, nightly price, stay total, and whether each room is immediately bookable. Recommend the best-value option, but wait for me to choose.
```

```text
Use the king room with breakfast. Recheck its exact price, availability, taxes, cancellation terms, and any fees collected at the hotel. Show me the final booking summary and wait for my explicit confirmation before creating the booking or starting payment.
```

```text
Look up my booking using agent reference ID <AGENT_REF_ID>. Explain its current booking and payment status. If it can be cancelled, show the deadline, penalty, and expected refundable amount, then wait for my confirmation before cancelling anything.
```

## How Hotel Booking AI works

```text
Your destination, dates, and guests
  → resolve the city, hotel, or point of interest
  → search up to 20 hotel candidates
  → query matching live room products
  → rank and present the five best verified hotels
  → show hotel details, room photos, and current quotes
  → recheck the selected room's price and availability
  → create the booking only after your explicit confirmation
  → pay, query, or cancel the order when requested
```

The price shown during the initial hotel search is only a candidate signal. Prices presented for comparison come from matching live room products, and the final booking uses the latest rate returned by the availability check.

## Privacy, booking, and payment

- Public hotel discovery and live-rate comparison do not require a sign-in.
- Order operations use the `user_key` stored locally in `user_key.txt`; keep it out of prompts, screenshots, logs, URLs, commits, and issue reports.
- Hotel Booking AI asks for the guest's full legal name and a contact email only when a confirmed booking is about to be created. It does not collect a phone number.
- Booking, cancellation, and payment are explicit actions. The agent must show the relevant details and wait for your confirmation before proceeding.
- TourMind room prices include taxes. A small number of destinations may require the hotel to collect a city or tourism tax at check-in; any returned mandatory fee is shown separately.
- Stripe adds a 3.5% payment-processing fee when selected. WeChat Pay and Alipay are also supported.
- Read-only hotel-result links can display hotel and room information but cannot book, pay, cancel, or access account and finance pages.
- If a stored key becomes invalid, remove `user_key.txt`, sign in again, and save the new key locally.

## Choose the right TourMind integration

| Audience | Integration | Authentication model | Product and repository |
|---|---|---|---|
| Consumer / ToC | Direct HTTP Skill | Public search and availability; `user_key` only for order operations | **[Hotel-booking-ai](https://github.com/tourmind-com/Hotel-Booking-AI)** |
| Business / ToB | Direct HTTP Skill | Skill Token required for every API call | [Tourmind-booking-skill](https://github.com/tourmind-com/Tourmind-Booking-Skills) |
| Consumer / ToC | MCP package + companion Skill | Public MCP connection; `user_key` only for order operations | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| Business / ToB | MCP package + companion Skill | Bearer-authenticated MCP connection | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API and support

**API base URL:** `https://api.tourmind.com`

| Endpoint | Purpose | Sign-in required |
|---|---|---|
| `POST /skill/toc/check_skill_update` | Check for a Skill update | No |
| `POST /skill/toc/search_location` | Resolve a region, point of interest, or hotel | No |
| `POST /skill/toc/search_hotels` | Search hotel candidates | No |
| `POST /skill/toc/get_hotel_detail` | Get hotel details and images | No |
| `POST /skill/toc/query_room_rates` | Get live rooms and rates | No |
| `POST /skill/toc/check_room_availability` | Recheck the selected rate and inventory | No |
| `POST /skill/toc/create_booking` | Create a booking after confirmation | Yes |
| `POST /skill/toc/query_booking` | Query an order | Yes |
| `POST /skill/toc/cancel_booking` | Cancel an eligible order after confirmation | Yes |
| `POST /skill/toc/pay_order` | Start payment after confirmation | Yes |

- Request fields, response contracts, ranking, images, taxes, and booking rules: [references/parameter_guide.md](references/parameter_guide.md)
- Install from ClawHub: [Hotel Booking AI](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
- GitHub support: [open an issue](https://github.com/tourmind-com/Hotel-Booking-AI/issues)
- TourMind customer service: `+86-755 3665 4666`
- Hotel support: `hotel@tourmind.com`
- AI product cooperation: `ai@tourmind.com`

## License

[MIT](LICENSE) © 2026 TourMind

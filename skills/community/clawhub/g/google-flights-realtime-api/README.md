# Google Flights Search — OpenClaw Skill

Search Google Flights in real time for cheap one-way and round-trip flights between any airports worldwide.

## What It Does

This skill lets an OpenClaw agent search for flights on your behalf by calling the Google Flights Live API. It supports:

- **One-way** and **round-trip** searches
- Filtering by max stops, specific airlines, departure/arrival time windows
- Price cap and currency selection
- Economy and Business class
- Multiple passengers

The agent will ask for your travel details, call the API, and present the results in a clear, comparable format.

## Requirements

You need a **RapidAPI key** with an active subscription to the [Google Flights Live API](https://rapidapi.com/mtnrabi/api/google-flights-live-api).

A **free tier** (50 requests/month) is available — no credit card required to get started.

### Setup

1. Go to [Google Flights Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/google-flights-live-api)
2. Click **Subscribe** and select the Free plan (or a paid plan for higher limits)
3. Copy your RapidAPI key from the dashboard
4. Configure it in OpenClaw:

```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "google-flights-search": {
        "enabled": true,
        "apiKey": "YOUR_RAPIDAPI_KEY_HERE"
      }
    }
  }
}
```

Or set the `RAPIDAPI_KEY` environment variable.

## How to Use

Just ask your OpenClaw agent to search for flights in natural language:

- *"Find me a one-way flight from JFK to TLV on April 15th"*
- *"Search round-trip flights from LAX to CDG, departing March 20 and returning March 27, under $800"*
- *"What's the cheapest flight from SFO to NRT next month with max 1 stop?"*

The agent will determine the right endpoint (one-way vs round-trip), build the request, call the API, and present results.

## Examples

### One-way search

> **You:** Find flights from New York to Tel Aviv on April 15th, economy, max 1 stop
>
> **Agent:** Searching for one-way flights JFK → TLV on 2026-04-15...
>
> Here are the top results:
> | Airline | Price | Stops | Duration | Departs | Arrives |
> |---------|-------|-------|----------|---------|---------|
> | Turkish Airlines | $412 | 1 (IST) | 14h 20m | 11:30 PM | 7:50 PM+1 |
> | Delta | $524 | 1 (CDG) | 13h 45m | 6:00 PM | 11:45 AM+1 |
> | El Al | $689 | Nonstop | 10h 50m | 12:15 AM | 5:05 PM |

### Round-trip search

> **You:** Round trip LAX to London, April 10-17, business class, under $3000
>
> **Agent:** Searching for round-trip business class flights LAX → LHR...

## API Pricing (via RapidAPI)

| Plan | Price | Requests/month | Overage |
|------|-------|---------------|---------|
| Basic | $0/mo | 10 | — |
| Pro | $5/mo | 2,500 | $0.003/req |
| Ultra | $20/mo | 12,500 | $0.003/req |
| Mega | $200/mo | 2,000,000 | $0.0001/req |

All plans include 10,240 MB/month bandwidth (then $0.001 per MB).

See latest pricing at [RapidAPI](https://rapidapi.com/mtnrabi/api/google-flights-live-api/pricing).

## Permissions

This skill requires **`network:outbound`** to make HTTPS POST requests to the Google Flights Live API hosted on RapidAPI. This is the only external communication the skill performs. No other network access is needed or used.

| Permission | Reason |
|------------|--------|
| `network:outbound` | Required to call `google-flights-live-api.p.rapidapi.com` (the only endpoint this skill contacts) |

## Security

- **Single endpoint only.** This skill communicates exclusively with `https://google-flights-live-api.p.rapidapi.com`. No other external services, domains, or IPs are contacted.
- **No data storage.** Flight search results are returned directly to the agent and presented to the user. No data is stored, cached, logged, or forwarded anywhere.
- **No code execution.** This skill contains only instructions for the AI agent — no scripts, no `eval`, no dynamic code execution.
- **API key handling.** Your RapidAPI key is read from the `RAPIDAPI_KEY` environment variable (or `skills.entries.google-flights-search.apiKey` in config) and sent only in the `x-rapidapi-key` header to RapidAPI's servers. It is never logged, stored, or sent elsewhere.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `403 Forbidden` | Your RapidAPI key is missing or invalid. Check the `RAPIDAPI_KEY` env var. |
| `429 Too Many Requests` | You've exceeded your plan's rate limit. Upgrade your RapidAPI plan or wait. |
| `Invalid airport code` | Use 3-letter IATA codes (e.g. `JFK`, `LHR`, `NRT`). Ask the agent for help mapping city names to codes. |
| `Missing return_date` | Round-trip searches require both `departure_date` and `return_date`. |

## Support

- API issues: [Google Flights Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/google-flights-live-api)
- Skill issues: Open an issue on the skill's ClawHub page

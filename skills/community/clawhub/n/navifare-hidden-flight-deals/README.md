# Navifare Hidden Flight Deals

By [Navifare AG](https://navifare.com)

Find hidden flight deals by comparing prices across 10+ booking sites. Works with any MCP-enabled AI agent (Claude Code, OpenClawd, ChatGPT, etc.).

Install on ClawHub: [clawhub.ai/simonenavifare/navifare-hidden-flight-deals](https://clawhub.ai/simonenavifare/navifare-hidden-flight-deals)

## What This Skill Does

When users mention flight prices from any booking website (Skyscanner, Kayak, Google Flights, etc.), this skill automatically:
1. Extracts flight details from text or screenshots
2. Searches Navifare's network of 10+ booking sites
3. Compares prices to find hidden deals
4. Provides direct booking links to providers

**Average savings**: $150-300 per booking. The same flight often costs 15-30% less on different platforms.

## Quick Start

### 1. Add the MCP Server

Add this to your MCP client configuration (e.g., `mcp.json`):

```json
{
  "mcpServers": {
    "navifare-mcp": {
      "url": "https://mcp.navifare.com/mcp"
    }
  }
}
```

**No local installation required!** The MCP server is hosted and always available.

### 2. Install the Skill

Install into your agent's skills directory:
```
~/.claude/skills/navifare-hidden-flight-deals/
```

Directory structure:
```
navifare-hidden-flight-deals/
├── SKILL.md              # Main skill definition (agent instructions)
├── README.md             # This file
├── CHANGELOG.md          # Version history
├── INSTALLATION.md       # Detailed setup guide
├── mcp-config-example.json
├── references/
│   ├── AIRPORTS.md       # IATA airport codes reference
│   ├── AIRLINES.md       # IATA airline codes reference
│   └── EXAMPLES.md       # Real usage examples
```

### 3. Verify Installation

Check that these MCP tools are available:
- `mcp__navifare-mcp__flight_pricecheck`
- `mcp__navifare-mcp__format_flight_pricecheck_request`

## Usage

### Validate a Price from Skyscanner

**You**: I found a round-trip flight from New York to London on Skyscanner for $850. BA553 departing Sep 15 at 6 PM, returning BA554 Sep 22 at 10 AM.

**Agent** (automatically activates):
- Extracts flight details
- Searches 10+ booking sites
- Presents comparison table with savings and booking links

### Upload a Screenshot

**You**: *[Upload screenshot from Kayak]*

**Agent**:
- Extracts visible flight details from the screenshot (itinerary only, no PII)
- Validates prices across booking sites
- Shows savings opportunities

### Before Booking

**You**: I'm about to book this flight. Should I?

**Agent**:
- Asks for flight details
- Runs price comparison
- Recommends best option with booking links

## When The Skill Activates

The skill automatically triggers when you:
- Mention finding a flight price: "I found this flight for $X"
- Upload a flight booking screenshot
- Ask "Is this a good price?"
- Say "Should I book this?"
- Ask "Can you find cheaper?"

## What Information is Needed

**Required**:
- **Route**: Departure and arrival airports (e.g., "JFK to LHR")
- **Date**: Travel date(s) (e.g., "Sep 15-22, 2026")
- **Flight**: Airline and flight number (e.g., "BA553")
- **Times**: Departure and arrival times (e.g., "6:00 PM - 6:30 AM")

**Optional but helpful**:
- **Class**: Economy, Business, First (defaults to Economy)
- **Passengers**: Number of adults/children (defaults to 1 adult)
- **Reference price**: What you saw on other sites
- **Currency**: USD, EUR, GBP, etc. (auto-detected from price)

If any information is missing, the agent will ask you for it.

## Features

### What This Skill Does
- Compares prices across 10+ booking sites in real-time
- Handles direct and connecting flights
- Supports round-trip searches
- Extracts flight info from screenshots (via the agent's vision capabilities)
- Validates IATA codes for airports and airlines
- Handles multiple currencies
- Shows price trends and savings
- Provides direct booking links

### What This Skill Does NOT Do
- Book flights automatically (returns links only)
- Store your payment information
- Make purchasing decisions for you
- Guarantee prices won't change
- Support one-way flights (round-trip only)

## Performance

- **Typical search time**: 30-60 seconds
- **Maximum search time**: 90 seconds
- **Booking sites searched**: 10+ providers
- **Results returned**: Up to 20 options (shows top 5 by default)

## Privacy & Security

This skill processes **pre-booking itineraries only** -- flight routes, dates, times, and prices that the user found on booking sites and wants to compare. It does **not** process booking confirmations, passenger names, passport details, payment information, or any other personally identifiable information (PII).

**What is sent to the Navifare MCP server:**
- Flight numbers, airlines, airports, dates, and times
- Travel class and passenger count (e.g., "2 adults")
- A reference price and currency for comparison

**What is NOT sent:**
- Passenger names or personal details
- Booking references or confirmation numbers
- Payment or credit card information
- Passport or identity documents

**Data handling:**
- Searches are not linked to user accounts or identities
- Booking happens directly on provider sites via their own links
- No tracking or affiliate redirects

For full details, see [navifare.com](https://navifare.com) and our [Terms of Service](https://navifare.com/terms).

## Revenue Share

Revenue share is available for qualified partners who integrate the Navifare MCP into their products. Contact [contact@navifare.com](mailto:contact@navifare.com) for details.

## Reference Documentation

### AIRPORTS.md
200+ major international airports with IATA codes, organized by region. Includes multi-airport city disambiguation (London, New York, Paris, etc.) and low-cost carrier hubs.

### AIRLINES.md
150+ airlines with IATA codes. Includes alliance memberships, codeshare handling, regional carriers, and flight number extraction rules.

### EXAMPLES.md
Real conversation examples showing round-trip validations, screenshot extraction, multi-segment flights, error handling, and edge cases.

## Troubleshooting

### "Navifare MCP not available"
Verify your MCP client configuration has `navifare-mcp` with `"url": "https://mcp.navifare.com/mcp"`. Restart your MCP client after changes.

### "No results found"
Check that flight details are correct (airline code, flight number, date). Use reference docs to verify IATA codes.

### "Search timeout"
Searches take up to 90 seconds. Partial results may be returned. Try again or verify flight details.

### "One-way not supported"
Navifare only supports round-trip flights. Provide both outbound and return flight details.

## Support

- **Navifare MCP & skill**: [navifare.com](https://navifare.com) | [contact@navifare.com](mailto:contact@navifare.com)
- **Privacy inquiries**: [privacy@navifare.com](mailto:privacy@navifare.com)
- **GitHub**: [github.com/navifare/navifare-mcp](https://github.com/navifare/navifare-mcp)
- **ClawHub**: [clawhub.ai/simonenavifare/navifare-hidden-flight-deals](https://clawhub.ai/simonenavifare/navifare-hidden-flight-deals)

## License

MIT License - [Navifare AG](https://navifare.com). See [Terms of Service](https://navifare.com/terms).

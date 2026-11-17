---
name: private-clubs
description: Find and compare private clubs worldwide (golf, yacht, city, beach, athletic, ski and more) with the free Private Clubs MCP server, by place, type, amenities and waitlist status
homepage: https://www.theprivateclubs.com/mcp
---

# Private Clubs

Private Clubs (theprivateclubs.com) is a directory of 39,500+ private clubs in 177 countries. Its MCP server is free, read-only and needs no account.

## Connect once

If the `private-clubs` MCP server is not connected yet, add it and check it:

```bash
openclaw mcp add private-clubs --url https://www.theprivateclubs.com/api/mcp --transport streamable-http
openclaw mcp doctor private-clubs --probe
```

You can also add it in Settings, MCP, Add server, with the same URL and the Streamable HTTP transport.

## Tools

- `search_clubs`: search by `query` (name, type or city), `state` (US state or Canadian province, full name), `type` (golf, city, yacht, athletic, beach, equestrian, ski, automotive, aviation, outdoor, business, wellness, dining), `amenities` and `waitlist` (open waitlists only). Results come best known first, up to 25.
- `get_club`: one club's profile by `slug`: location, course details, architect, founding year, amenities, website and its profile link.
- `get_clubs_by_state`: up to 100 clubs in a US state or Canadian province, best known first.
- `compare_clubs`: two or three clubs side by side, by `slugs`.
- `get_membership_info`: a club's waitlist status and where to see its fees.

## How to answer

1. Search first with `search_clubs` or `get_clubs_by_state`, then use the `slug` it returns for `get_club`, `compare_clubs` or `get_membership_info`.
2. Link each club you mention to the `url` the tools return.
3. Membership fees are not returned. Say they are on the club's profile at theprivateclubs.com for account holders, and never estimate a fee.
4. Say when a field is missing instead of guessing it.

## Examples

- "Find private golf clubs in Florida with an open waitlist"
- "Compare Seminole Golf Club and Augusta National"
- "Tell me about The Knickerbocker Club in New York"
- "Which yacht clubs are there in British Columbia?"

Setup steps for other apps: https://www.theprivateclubs.com/mcp/setup.md

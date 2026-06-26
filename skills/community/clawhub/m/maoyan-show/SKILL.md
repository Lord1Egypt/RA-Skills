---
name: maoyan-show
description: Fetch public Maoyan Show (猫眼演出) data from show.maoyan.com, including event lists, event details, ticket prices, sessions, venues, city IDs, and crawler workflows. Use only for public data; do not use for login, orders, payment, real-name verification, ticket verification, favorites, comments, or user account data.
version: 1.0.1
---

# Maoyan Show

Use this skill when the user asks for 猫眼演出 / Maoyan Show data, `show.maoyan.com` APIs, show lists, event details, ticket price information, sessions, venue details, city IDs, or crawler workflows.

## Required Reference

Before making or documenting Maoyan Show API calls, read `{baseDir}/references/api.md`.

That file is the source of truth for endpoints, parameters, response fields, default values, unsupported endpoints, and scenario workflows.

## Defaults

- Use `sellChannel=13` unless the user explicitly specifies another channel.
- Use `clientPlatform=3` unless the user explicitly specifies another platform.
- Use `Referer: https://show.maoyan.com/qqw#/`.
- Do not send `token` for public data.
- Do not send `optimus_risk_level` or `optimus_code` by default. If a runtime/front-end flow auto-completes them, record those values and reuse them later in the same task.
- `uuid` is optional. If implementation needs one, generate UUID v4 and reuse it within the same task.
- `lat` and `lng` are optional. Only send them when the user provides coordinates or the task needs location/distance behavior.

## City Handling

Search, recommendation, calendar, ordinary list, and most ranking flows need a city context. Category-channel ianvs requests accept `cityId` in headers, but direct calls may still return the default/current context city; always validate `cityName` in returned items.

- If the user provides `cityId`, use it.
- If the user provides a city name and the ID is known from the reference, use it.
- If the city is not known, ask the user for the city or `cityId` before the first city-scoped request, then reuse it in the same task.
- If the user provides coordinates, use the city reverse lookup endpoint from `{baseDir}/references/api.md`.
- Known example: Shenzhen is `cityId=30`.

## Public-Only Boundary

Only use public show, city, venue, session, price, recommendation, search, and list endpoints.

Do not use login-state or user-private flows, including order, payment, real-name, address, coupon, ticket verification, favorite, comment mutation, or account APIs. If a user asks for these, explain that this skill intentionally does not cover them.

## Workflows

Use the best-practice scenario flows from `{baseDir}/references/api.md`:

- Known `performanceId`: call the detail endpoint first, then call the shows/sessions endpoint for ticket sessions and prices.
- Keyword search: resolve or ask for `cityId`, then call the search/list endpoint and return normalized results.
- Category list page: map `#/list/{categoryId}?labelId={labelId}` to the ianvs category-channel request. Use `categoryId=7` for 亲子演出 and `labelId=0` as the default no-extra-label filter. Put ianvs common values in headers, not URL query. Do not use this as a reliable cross-city source unless returned `cityName` matches the requested city.
- City list/recommendation: resolve or ask for `cityId`, then call the relevant city-scoped list endpoint. Treat list/search filters as advisory and locally filter by city, category, keyword, and date.
- Venue lookup: call venue detail by `shopId`; call venue performances only when the user asks for events at that venue.
- Ticket price summary: use detail data for summary price fields and shows/sessions data for concrete ticket category availability.

## Output Style

Return concise, normalized results. Prefer these fields when available:

- Event: `performanceId`, name, category, poster, status, date/time, city, venue, address.
- Price: min/max price, ticket category, session, availability/status.
- Venue: `shopId`, name, address, coordinates, city.
- API usage: method, URL path, required parameters, defaults applied, and important caveats.

When producing API documentation, keep only correct final behavior and best practices. Do not include exploratory attempts, failed probes, or speculative alternatives unless the user explicitly asks for investigation notes.

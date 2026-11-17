# Platform Support Notes

Spot supports 20+ booking platforms across three architectural patterns:

| Pattern | Platforms | Auth |
|---------|-----------|------|
| **REST API** | Acuity Scheduling, Calendly | None / API token |
| **Public Widget API** | SevenRooms (availability) | None |
| **Browser Automation** | All others | Session / none |

Each platform's method, status, edge cases, selectors, and known limitations are documented in `references/platforms/<platform>.md`. See `references/platforms/README.md` for the universal decision tree and platform index. See `references/platform-access-matrix.md` for bot block status.

---

## Key Platform Notes

### REST API Platforms

- **Acuity Scheduling** — No auth required. Extract `owner`, `appointmentTypeId`, `calendarId` from page or URL. Use `/api/scheduling/v1/availability/*` endpoints.
- **Calendly** — `CALENDLY_API_TOKEN` for API; browser fallback works without auth.

### Public Widget API

- **SevenRooms** — Public widget API (`api-yoa/availability/widget/range`) returns full availability data with no auth. Rich per-slot metadata: seating type, duration, cancellation policy, CC requirements, service charges, gratuity. Booking requires browser automation on the customer widget page — there is no customer-facing REST API for booking.

### Browser Automation — Standard

- **Booksy, GlossGenius, SimplyBook.me, Boulevard, Mangomint, DaySmart** — Standard Playwright selectors. React SPAs. Generally accessible without VPN.
- **ResDiary** — UK/Europe/Asia focus. 24-hour time format. DD/MM/YYYY dates.
- **Eat App** — Middle East focus. Multi-language support.

### Browser Automation — Shadow DOM / Custom Elements

- **Square Appointments** — `hasAttribute('disabled')` on `market-button` (never `isEnabled()`). Check `aria-disabled`. Shadow DOM queries from host element.
- **Meevo** — Angular SPA. Sub-service radio buttons may not respond to programmatic clicks. Report visible info, note limitation.
- **Mindbody** — React SPA. Booking widget loads after hydration. VPN fallback for PerimeterX blocks.
- **Fresha** — React SPA. Service cards with "Book" buttons. VPN fallback for Cloudflare blocks.
- **Vagaro** — Bootstrap modals. May fail due to Incapsula blocking. Fall back to `/services` page info.

### Browser Automation — Session-Based

- **OpenTable** — Akamai blocks Chromium — must use Firefox. One-time manual login, then session persistence via `opentable-session.json`.
- **Resy** — REST API with token auth (recommended). Browser automation fallback for unauthenticated venues. Credentials via `RESY_API_KEY`, `RESY_EMAIL`, `RESY_PASSWORD`.

### Browser Automation — URL Iteration

- **Tock** — CF Turnstile triggers on calendar clicks. Workaround: navigate via URL parameters (`?date=YYYY-MM-DD`) instead of clicking. VPN + VirtualPerson for persistent blocks.

### Browser Automation — Widget Page

- **SevenRooms (booking)** — Customer fills form on `/explore/{venue}/reservations/create/search/`. No customer REST API available.
- **StyleSeat** — React SPA. Professional profile pages.
- **Yelp Reservations** — React SPA widget embedded in Yelp business pages.

---

## Bot Block Summary

| Platform | Detection | Bypass | VPN Needed |
|----------|-----------|--------|------------|
| Tock | Cloudflare Turnstile | URL iteration + VirtualPerson | Yes |
| OpenTable | Akamai TLS fingerprint | Firefox + manual login + VirtualPerson | Yes |
| Mindbody | PerimeterX | VPN + stealth scripts | Yes |
| Fresha | Cloudflare | VPN to non-US exit | Yes |
| Vagaro | Incapsula | VPN | Maybe |
| Yelp | IP-range block | Residential proxy | Yes |
| All others | None / minimal | Standard stealth | No |

All browser-based scripts use the shared stealth configuration from `references/stealth-config.md` (`create_stealth_browser()`, `human_type()`, `human_click()`, `detect_bot_block()`, UA rotation, random delays).
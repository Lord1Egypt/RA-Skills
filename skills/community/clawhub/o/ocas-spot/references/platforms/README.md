# Scheduling Platform Knowledge Base

Systematic patterns for booking and availability automation. Organized for continuous pressure testing of new platforms.

---

## Platform Architecture

Spot handles platforms through three architectural patterns:

| Pattern | How It Works | Platforms |
|---------|-------------|-----------|
| **REST API** | Direct HTTP calls to structured endpoints. Fastest, most reliable. | Acuity Scheduling, Calendly |
| **Public Widget API** | Unauthenticated JSON API embedded in the booking widget. No auth needed for availability. | SevenRooms (availability only) |
| **Browser Automation** | Playwright-driven interaction with the booking page. Handles SPAs, custom elements, and bot detection. | All others |

**Browser automation sub-patterns:**

| Sub-pattern | Description | Platforms |
|-------------|-------------|-----------|
| **Standard Playwright** | Semantic selectors, standard form fills | Booksy, GlossGenius, SimplyBook.me, Boulevard, Mangomint, DaySmart, ResDiary, Eat App |
| **SPA with shadow DOM** | Custom elements, shadow DOM queries, `aria-disabled` checks | Square Appointments, Meevo, Mindbody, Fresha, Vagaro |
| **Session-based** | One-time manual login, then session persistence | OpenTable, Resy |
| **URL-based iteration** | Navigate via URL params instead of clicking | Tock |
| **Widget page automation** | Fill form on the public booking widget page | SevenRooms (booking), StyleSeat, Yelp Reservations |

---

## Platform Directory

### Appointment / Spa Platforms

| Platform | Status | Method | Auth | Last Tested |
|----------|--------|--------|------|-------------|
| [Acuity Scheduling](./acuity.md) | ✅ Production | REST API | None | 2026-03-30 |
| [Calendly](./calendly.md) | ✅ Production | REST API + browser | API token / none | 2026-05-18 |
| [Square Appointments](./square.md) | ⚠️ Working | Browser automation (shadow DOM) | None | 2026-05-18 |
| [Meevo](./meevo.md) | ⚠️ Working | Browser automation (Angular SPA) | None | 2026-05-18 |
| [Mindbody](./mindbody.md) | ⚠️ Working | Browser automation (React SPA) | None | 2026-05-18 |
| [Fresha](./fresha.md) | ⚠️ Working | Browser automation (React SPA) | None | 2026-05-18 |
| [StyleSeat](./styleseat.md) | ⚠️ Working | Browser automation | None | 2026-05-18 |
| [Vagaro](./vagaro.md) | ⚠️ Partial | Browser automation | None | 2026-05-18 |
| [Booksy](./booksy.md) | 🆕 New | Browser automation | None | — |
| [GlossGenius](./glossgenius.md) | 🆕 New | Browser automation | None | — |
| [SimplyBook.me](./simplybook.md) | 🆕 New | Browser automation | None | — |
| [Boulevard](./boulevard.md) | 🆕 New | Browser automation | None | — |
| [Mangomint](./mangomint.md) | 🆕 New | Browser automation | None | — |
| [DaySmart Salon](./daysmart.md) | 🆕 New | Browser automation | None | — |

### Restaurant Reservation Platforms

| Platform | Status | Method | Auth | Last Tested |
|----------|--------|--------|------|-------------|
| [SevenRooms](./sevenrooms.md) | ✅ Production | Public widget API (availability) + browser automation (booking) | None | 2026-05-25 |
| [Resy](./resy.md) | ⚠️ Working | REST API (auth) / browser fallback | API key + credentials | 2026-03-31 |
| [Tock](./tock.md) | ⚠️ Working | Browser automation (URL iteration) | None | 2026-03-31 |
| [OpenTable](./opentable.md) | ⚠️ Working | Session-based browser | Manual login | 2026-03-30 |
| [Yelp Reservations](./yelp-reservations.md) | 🆕 New | Browser automation | None | — |
| [ResDiary](./resdiary.md) | 🆕 New | Browser automation | None | — |
| [Eat App](./eatapp.md) | 🆕 New | Browser automation | None | — |

### Discovery

| Service | Status | Method | Auth | Last Tested |
|---------|--------|--------|------|-------------|
| Yelp Fusion | ✅ Production | REST API + page fallback | API key / none | 2026-05-18 |

---

## Blocked Platforms

Some platforms cannot be automated from certain IP ranges due to bot detection. See [`references/platform-access-matrix.md`](platform-access-matrix.md) for the full breakdown.

| Platform | Block Type | Bypass | Status |
|----------|-----------|--------|--------|
| Tock | Cloudflare Turnstile | VirtualPerson (headed Chrome) | ⚠️ Partial |
| OpenTable | Akamai TLS fingerprint | VirtualPerson + manual login | ⚠️ Partial |
| Yelp | IP-range block | Residential proxy | ❌ Blocked |

**Key insight:** Cloudflare Turnstile and Akamai blocks are fingerprint-based, not IP-based. VPN alone is insufficient — need a real browser (VirtualPerson) or residential proxy.

---

## Universal Decision Tree (Use for NEW platforms)

```
1. LOAD booking page
   ↓
2. Check page architecture:
   ├─ Server-rendered HTML with clear IDs? → Try DOM scraping
   ├─ React/Vue/SPA with shadow DOM? → Browser automation required
   └─ Network calls visible? → Try API interception
   ↓
3. Test availability endpoint:
   ├─ Returns JSON? → API route (Acuity pattern)
   ├─ Returns HTML? → DOM scraping
   └─ Requires auth? → Browser automation (Square pattern)
   ↓
4. Determine element type:
   ├─ Standard buttons/inputs? → Standard Playwright selectors
   └─ Custom elements (market-*, etc)? → Check disabled attributes directly
   ↓
5. Verify detection works:
   ├─ Compare with manual browser
   └─ Check if dates show same availability
   ↓
6. FULL FLOW test with available date
   ↓
7. Document: Happy path, Pitfalls, Platform-specific quirks
```

---

## Quick Reference: Platform Fingerprints

### Acuity Scheduling
- **Domain:** `*.acuityscheduling.com`, `*.as.me`
- **Signature:** `/api/scheduling/v1/availability/*` endpoints
- **Response:** JSON with boolean availability
- **Auth:** None required for public bookings

### Calendly
- **Domain:** `calendly.com`
- **Signature:** REST API (`/v2/event_type_available_times`) or browser
- **Auth:** `CALENDLY_API_TOKEN` for API; none for browser

### Square Appointments
- **Domain:** `book.squareup.com`, `app.squareup.com`
- **Signature:** `market-*` custom elements
- **Response:** React SPA with shadow DOM
- **Auth:** None for consumer bookings

### Meevo (Millennium)
- **Domain:** `*.meevo.com`, `login.meevo.com`
- **Signature:** Angular SPA, multi-step wizard, `div.category-item` for service categories
- **Auth:** None required for public bookings

### Mindbody
- **Domain:** `*.mindbodyonline.com`, `*.mindbody.io`
- **Signature:** React SPA, booking widget loads after hydration
- **Auth:** None for public bookings

### Fresha
- **Domain:** `*.fresha.com`
- **Signature:** React SPA, service cards with "Book" buttons
- **Auth:** None for public bookings

### Vagaro
- **Domain:** `*.vagaro.com`
- **Signature:** Bootstrap modals, service list on `/services` page
- **Auth:** None required for public bookings

### StyleSeat
- **Domain:** `*.styleseat.com`
- **Signature:** React SPA, professional profile pages
- **Auth:** Required for booking; not for availability check

### Booksy
- **Domain:** `*.booksy.com`
- **Signature:** React SPA, consumer-first design, service cards
- **Auth:** Required for booking; not for availability check

### GlossGenius
- **Domain:** `*.glossgenius.com`
- **Signature:** React SPA, branded booking pages for independent professionals
- **Auth:** Required for booking; not for availability check

### SimplyBook.me
- **Domain:** `*.simplybook.me`
- **Signature:** Highly customizable React SPA, multi-language support
- **Auth:** Required for booking; not for availability check

### Boulevard
- **Domain:** `*.blvdup.com`, `book.boulevard.io`
- **Signature:** Premium React SPA, staff-centric design
- **Auth:** Required for booking; not for availability check

### Mangomint
- **Domain:** `*.mangomint.com`
- **Signature:** Visual-first React SPA, Instagram-style service cards
- **Auth:** Required for booking; not for availability check

### DaySmart Salon
- **Domain:** `*.daysmart.com`
- **Signature:** React SPA, salon-specific service categories
- **Auth:** Required for booking; not for availability check

### SevenRooms
- **Domain:** `sevenrooms.com`
- **Signature:** Public widget API at `/api-yoa/availability/widget/range` (no auth); booking widget at `/explore/{venue}/reservations/create/search/`
- **Availability response:** JSON with `data.availability.{date}[].times[]` — each slot has `type`, `time`, `access_persistent_id`, `public_time_slot_description`, `duration`, `cancellation_policy`
- **Auth:** None for availability; browser automation for booking (no customer REST API)

### Resy
- **Domain:** `resy.com`
- **Signature:** REST API (`/4/find`) with auth token; browser fallback
- **Auth:** API key + email/password for API; none for browser

### Tock
- **Domain:** `exploretock.com`
- **Signature:** URL-based date iteration (`?date=YYYY-MM-DD`)
- **Auth:** None; CF Turnstile on calendar interactions

### OpenTable
- **Domain:** `opentable.com`
- **Signature:** Session-based; requires Firefox (Akamai blocks Chromium)
- **Auth:** Manual login once, then session persistence

### Yelp Reservations
- **Domain:** `*.yelp.com`
- **Signature:** React SPA widget embedded in Yelp business pages
- **Auth:** None for availability check; Yelp account for booking

### ResDiary
- **Domain:** `*.resdiary.com`
- **Signature:** React SPA, UK/Europe/Asia focus, 24-hour time format
- **Auth:** None for availability check

### Eat App
- **Domain:** `*.eatapp.co`
- **Signature:** React SPA, Middle East focus, multi-language
- **Auth:** None for availability check

### Yelp (Discovery)
- **Domain:** `www.yelp.com`
- **Signature:** Business search API + review aggregation
- **Auth:** Optional `YELP_API_KEY`; works in page mode without key

---

## Detection Anti-Patterns (Universal DON'Ts)

1. **DON'T trust Playwright `isEnabled()`/`isDisabled()`** on custom elements
   - ✅ DO: Check DOM `disabled` attribute directly via `page.evaluate()`

2. **DON'T assume coordinates work** across screen sizes
   - ✅ DO: Use semantic selectors (aria-label, data-testid)

3. **DON'T rely on `networkidle`** for SPAs
   - ✅ DO: Wait for specific elements to appear

4. **DON'T skip manual verification**
   - ✅ DO: Always compare automation results with manual browser check

5. **DON'T assume API endpoints are stable**
   - ✅ DO: Capture and document exact request/response patterns

6. **DON'T assume uniform layout** on customizable platforms
   - ✅ DO: Use flexible selectors; handle missing elements gracefully

7. **DON'T ignore timezone differences** on international platforms
   - ✅ DO: Check for 24-hour format, DD/MM/YYYY dates, non-English text

8. **DON'T assume the widget API doesn't work** without testing it directly
   - ✅ DO: Always test the public widget API before falling back to browser automation (SevenRooms pattern)

---

## File Structure

```
references/platforms/
├── README.md              # This file
├── NEW_PLATFORM.md        # Step-by-step guide for new platforms

# Appointment/Spa Platforms
├── acuity.md              # Acuity: REST API, no auth
├── calendly.md            # Calendly: REST API + browser
├── square.md              # Square: shadow DOM, custom elements
├── meevo.md               # Meevo: Angular SPA
├── mindbody.md            # Mindbody: React SPA + VPN fallback
├── fresha.md              # Fresha: React SPA + VPN fallback
├── styleseat.md           # StyleSeat: React SPA
├── vagaro.md              # Vagaro: Bootstrap modals
├── booksy.md              # Booksy: React SPA
├── glossgenius.md         # GlossGenius: React SPA
├── simplybook.md          # SimplyBook.me: Customizable React SPA
├── boulevard.md           # Boulevard: Premium React SPA
├── mangomint.md           # Mangomint: Visual-first React SPA
├── daysmart.md            # DaySmart: React SPA

# Restaurant Reservation Platforms
├── sevenrooms.md          # SevenRooms: Public widget API + browser
├── resy.md                # Resy: REST API (auth) + browser
├── tock.md                # Tock: URL iteration + CF Turnstile
├── opentable.md           # OpenTable: Session-based, Firefox
├── yelp-reservations.md   # Yelp Reservations: Widget automation
├── resdiary.md            # ResDiary: UK/Europe/Asia focus
├── eatapp.md              # Eat App: Middle East focus

# Reusable patterns
└── patterns/
    ├── dom-check.js
    ├── api-intercept.js
    └── custom-element.js
```

---

## Adding a New Platform

1. Create `{platform}.md` from template
2. Document happy path with working code
3. Document all failed attempts (what NOT to do)
4. Update this README platform directory
5. Add to decision tree if new patterns discovered
6. Update `references/platform-notes.md` with key quirks
7. Update `references/vpn-integration.md` bot detection table

See [NEW_PLATFORM.md](./NEW_PLATFORM.md) for full workflow.
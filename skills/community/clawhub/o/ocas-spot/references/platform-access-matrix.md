## Platform Access Matrix (Tested May–June 2026, VPN Gate Japan)

### HTTP Access (can the site be reached?)

| Platform | HTTP Status | Block Type | Bypass |
|----------|-------------|------------|--------|
| Fresha | ✅ 200 | — | VPN sufficient |
| Booksy | ✅ 200 | — | VPN sufficient |
| Mindbody | ✅ 200 | — | VPN sufficient |
| ResDiary | ✅ 200 | — | VPN sufficient |
| Eat App | ✅ 200 | — | VPN sufficient |
| StyleSeat | ✅ 200 | — | VPN sufficient |
| Boulevard | ✅ 200 | — | VPN sufficient |
| Vagaro | ✅ 404 | — | VPN sufficient |
| SimplyBook.me | ✅ 404 | — | VPN sufficient |
| Tock | ❌ 403 | CF Turnstile | Needs VirtualPerson |
| Yelp | ❌ 403 | IP-range block | Needs residential proxy |
| OpenTable | ❌ 000 | Akamai TLS fingerprint | Needs VirtualPerson |

### Automation Status (can the booking flow be automated?)

| Platform | Automation | Method | Notes |
|----------|-----------|--------|-------|
| Square Appointments | ✅ Working | Stealth browser (`mcp_stealth_browser_*`) | Use `query_elements` + `click_element` only. `execute_script` returns null. See `references/stealth-browser-square-flow-20260608.md`. |
| Acuity Scheduling | ✅ Working | REST API | No auth required |
| Calendly | ✅ Working | REST API | API token required |
| SevenRooms | ⚠️ Partial | Public widget API (availability) + Playwright (booking) | No customer-facing REST API |
| Meevo | ❌ Blocked | Browser automation | Angular SPA — 50+ consecutive change detection failures. Effectively unautomated. |
| Vagaro | ❌ Blocked | Browser automation | JS handler failures — 60+ consecutive failures. API-dependent flow breaks in automation. Effectively unautomated. |
| Tock | ❌ Blocked | — | CF Turnstile. Needs VirtualPerson. |
| OpenTable | ❌ Blocked | — | Akamai TLS fingerprint. Needs Firefox + VirtualPerson. |
| Mindbody | ⚠️ Partial | Browser automation | HTTP works but booking flow may have bot detection. |
| Fresha | ⚠️ Partial | Browser automation | HTTP works but booking flow may have bot detection. |

**Key insight:** Cloudflare Turnstile and Akamai blocks are fingerprint-based, not IP-based. VPN alone is insufficient — need a real browser (VirtualPerson) or residential proxy. Even when HTTP works, the booking flow may fail due to SPA framework incompatibilities with browser automation (Meevo Angular, Vagaro API-dependent modals).
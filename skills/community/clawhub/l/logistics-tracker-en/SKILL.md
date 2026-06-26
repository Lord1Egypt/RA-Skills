---
name: logistics-tracker
description: Query real-time shipping status for mainstream EU/US carriers (UPS, FedEx, USPS, DHL, Royal Mail, PostNL, etc.) by tracking number. Triggered when user provides a tracking number or asks to track a shipment.
metadata:
  tags: logistics, shipping, tracking, fedex, ups, usps, dhl, royal-mail
---

# Logistics Tracker

Query shipping status for mainstream European and American carriers from a tracking number.

## Trigger Conditions

Invoke when the user:
- Pastes a tracking number (alone or with carrier context)
- Says "track my package / order / shipment"
- Asks about delivery status, parcel location, or estimated arrival
- Provides a number and asks "where is it?"

---

## Step 1 — Identify the Carrier

Match the tracking number against these patterns **in order** (most-specific first):

| Carrier | Pattern | Example |
|---------|---------|---------|
| **UPS** | `1Z[A-Z0-9]{16}` | `1Z999AA10123456784` |
| **FedEx Express** | `[0-9]{12}` | `123456789012` |
| **FedEx Ground / SmartPost** | `[0-9]{15}` or `[0-9]{20}` or `[0-9]{22}` | `012345678901234` |
| **USPS (domestic)** | `94[0-9]{20}` / `92[0-9]{20}` / `93[0-9]{20}` / `94[0-9]{18}` | `9400111899223397467490` |
| **USPS (international)** | `[A-Z]{2}[0-9]{9}[A-Z]{2}` | `EA123456789US` |
| **DHL Express** | `[0-9]{10,11}` (standalone, no letter prefix) | `1234567890` |
| **DHL eCommerce** | `GM[0-9]{16,18}` or `[0-9]{14,20}` starting with `420` | `GM6019267030000285` |
| **Royal Mail (UK)** | `[A-Z]{2}[0-9]{9}GB` | `RA123456789GB` |
| **PostNL (NL)** | `3S[A-Z0-9]{14}` or `JJD[0-9]{18}` or `JVGL[0-9]{14}` | `3SDEVC123456789A` |
| **DPD (EU)** | `[0-9]{14}` starting with `05` | `05012345678901` |
| **GLS (EU)** | `[0-9]{8,11}` | `12345678` |
| **Hermes / Evri (UK)** | `[A-Z0-9]{16}` (often starts with `H`) | `H1234567890ABCD` |
| **Amazon Logistics** | `TBA[0-9]{9,12}` | `TBA123456789000` |
| **Purolator (CA)** | `[A-Z]{3}[0-9]{9}` | `PUR123456789` |
| **Canada Post** | `[0-9]{16}` or `[A-Z]{2}[0-9]{9}CA` | `1234567890123456` |

If the format is **ambiguous** (e.g., a plain 12-digit number could be FedEx or DHL), ask the user to confirm the carrier or try both.

---

## Step 2 — Fetch Tracking Data

### Track123 API

Track123 supports 1700+ carriers. Call the Track123 REST API via Bash.

**API Key Setup (first time only)**

If the curl commands below still contain `$TRACK123_API_KEY`, ask the user to visit **https://www.track123.com/api** → Dashboard → API tab → copy and paste the key here. Once received, replace `$TRACK123_API_KEY` in this skill file with the actual key value.

**Step A — Register the tracking number:**
```bash
curl -s -X POST "https://api.track123.com/gateway/open-api/tk/v2/track/import" \
  -H "Track123-Api-Secret: $TRACK123_API_KEY" \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  -d '[{"trackNo": "{number}"}]'
```

**Step B — Query the tracking status:**
```bash
curl -s -X POST "https://api.track123.com/gateway/open-api/tk/v2/track/query" \
  -H "Track123-Api-Secret: $TRACK123_API_KEY" \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  -d '{"trackNos": ["{number}"]}'
```

Parse the JSON response (`data.accepted.content[0]`) and extract:
- `transitStatus` — overall status (e.g. `DELIVERED`, `IN_TRANSIT`)
- `deliveredTime` / `lastTrackingTime` — last update timestamp
- `localLogisticsInfo.trackingDetails` — events array (most recent first), each with `eventTime`, `address`, `eventDetail`
- `expectedDeliveryTime` — estimated delivery window
- `localLogisticsInfo.courierTrackingLink` — direct tracking URL

Present using the Step 3 format.

---

## Step 3 — Present Results

Format the response in this structure:

```
📦 Tracking: {NUMBER}
🚚 Carrier: {CARRIER NAME}
📍 Status: {CURRENT STATUS}  ← e.g., "In Transit", "Out for Delivery", "Delivered"
🕐 Last Update: {DATE TIME TIMEZONE}
📍 Last Location: {CITY, STATE/COUNTRY}

--- Tracking History ---
[Most recent first]
• {DATE TIME} — {LOCATION} — {EVENT DESCRIPTION}
• {DATE TIME} — {LOCATION} — {EVENT DESCRIPTION}
• {DATE TIME} — {LOCATION} — {EVENT DESCRIPTION}
  ... (truncate to 10 events max if many)

📅 Estimated Delivery: {DATE or "Not available"}
🔗 Track online: {DIRECT TRACKING URL}
```

**Status icons:**
- ✅ Delivered
- 🚚 Out for Delivery
- 📦 In Transit
- 🛃 Customs Clearance
- ⏳ Pre-Shipment / Label Created
- ⚠️ Exception / Delay / Attempted Delivery
- ❓ Unknown / No Data Found

---

## Step 4 — Handle Multiple Tracking Numbers

If the user pastes multiple tracking numbers at once:
1. Process all in parallel (separate WebSearch per number)
2. Present a summary table first:

```
| # | Tracking Number       | Carrier | Status          | Est. Delivery |
|---|----------------------|---------|-----------------|---------------|
| 1 | 1Z999AA10123456784   | UPS     | In Transit      | Jun 5, 2026   |
| 2 | 123456789012         | FedEx   | Delivered       | Jun 1, 2026   |
```

Then provide full details for each below.

---

## Step 5 — Edge Cases

**No tracking data found:**
> I searched for tracking number `{number}` with {carrier} but couldn't find any results. This can happen when:
> - The label was created but the package hasn't been scanned yet (pre-shipment)
> - The tracking number was entered incorrectly
> - It's an older shipment (>120 days)
>
> Try checking directly: {DIRECT TRACKING URL}

**Ambiguous carrier:**
> This number (`{number}`) could match multiple carriers. Could you tell me which one shipped your package?
> - FedEx (12-digit)
> - DHL Express (10-digit)
>
> Or I can check both for you.

**Carrier not covered:**
If the pattern doesn't match any known carrier, search broadly:
```
track package "{number}"
```
and report the carrier identified by the search results.

---

## Carrier Cheat Sheet (Quick Reference)

| Region | Major Carriers |
|--------|---------------|
| **US** | UPS, FedEx, USPS, Amazon Logistics, OnTrac, LaserShip/LSO |
| **UK** | Royal Mail, Evri/Hermes, DPD UK, Parcelforce, Yodel, DHL |
| **Germany** | DHL Paket, Hermes DE, DPD DE, GLS, UPS DE |
| **France** | La Poste/Colissimo, Chronopost, DHL FR, DPD FR, Mondial Relay |
| **Netherlands** | PostNL, DHL NL, DPD NL, GLS NL |
| **Spain** | Correos, SEUR, MRW, GLS ES, DHL ES |
| **Italy** | Poste Italiane, BRT, GLS IT, DHL IT, SDA |
| **Canada** | Canada Post, Purolator, FedEx CA, UPS CA |

When a user mentions a European country, prefer that country's local carriers if the number pattern fits.

# Region Profile: Global / Overseas (region profile: global)

> This is one of the region-adaptation layers of the `photo-video-organizer` skill.
> SKILL.md detects the user's region in Phase 0 and loads the matching profile. This file covers **all region-specific differences for users outside mainland China**.
> The core methodology (backup-first / reversible moves / fix time before import / human final decision) lives in `references/guide.md` and is universal. Only differences are documented here.

---

## 1. Coordinate systems

Outside mainland China there is **no GCJ-02 offset**: every map service and every phone records plain **WGS-84**, which is exactly what EXIF requires.

| Source | Datum | Write to EXIF directly? |
|---|---|---|
| Google Maps / Apple Maps / OpenStreetMap / Bing pickers | WGS-84 | ✅ Yes |
| GPS from photos taken outside mainland China | WGS-84 | ✅ Yes |
| Photos taken *inside* mainland China by a foreign visitor | WGS-84 | ✅ Yes (phones always record WGS-84 in EXIF) |

**Rules**:
1. Coordinates taken from any non-Chinese map service can be written to EXIF **as-is** — no datum conversion. Do **not** apply GCJ-02 conversion outside mainland China (it would introduce a false 300–600 m offset).
2. `scripts/datum_convert.py` is only needed when processing libraries that mix in coordinates captured from *Chinese* map services (e.g., screenshots from Amap/Baidu Maps).
3. City-level precision of 0.001° (~100 m) is sufficient for itinerary-based GPS filling.

## 2. Itinerary data sources (Phase 1.5 "which city on which day")

Multi-source cross-validation options outside mainland China (most reliable first):
1. **Google Maps Timeline** — the single richest source if enabled: export via **Google Takeout** → "Maps (your places)" / Location History → daily city sequence. (iOS users with Google Timeline enabled also have this.)
2. **Flight confirmations** — airline apps, booking emails (Gmail search `flight confirmation`), airline calendar files.
3. **Hotel / booking confirmations** — Booking.com, Airbnb, Hotels.com emails with check-in cities and dates.
4. **Credit-card / bank statements** — CSV export; merchant city is usually embedded (Stripe-style descriptors vary by bank).
5. **Ride-hailing & transit receipts** — Uber / Lyft / Bolt / Grab trip emails; train operators (Amtrak, Eurostar, JR, DB, SNCF, Trenitalia) ticket emails.
6. **Photo burst from other family members** — cross-check travel dates against a partner's library.

**Pitfalls (global-specific)**:
- Google Takeout exports can be huge and split into multiple zips; parse `Records.json` / `Timeline.json`, aggregate by day, pick the majority city as "primary city".
- Timezone boundaries: a red-eye flight or a trip spanning time zones makes "which day" ambiguous — anchor on **local time at the place**, not the home timezone. Mark uncertain days `INFERRED-ADJACENT` or leave blank (wrong GPS is worse than missing GPS).
- Statement merchant cities may be the company HQ for online purchases — prefer local spending (restaurants, fuel, transit, hotels).
- Final outputs are identical to the CN profile: a `daily_city.csv` (date, primary city, all cities, source, note) plus a **city→coordinate dictionary (WGS-84, ready for EXIF)**.

## 3. Transfer channels & metadata

| Channel | Keeps EXIF time/GPS | Notes |
|---|---|---|
| AirDrop / Finder cable sync / USB / SD card | ✅ Keeps | Preferred |
| iCloud Photos / Google Photos (Original Quality) / OneDrive / Dropbox desktop client | ✅ Keeps | Avoid "Storage saver"/"Express" compressed modes; Google Photos "Original quality" preserves metadata, "Storage saver" may strip/recompress |
| WhatsApp / Facebook Messenger / Instagram DM | ❌ Recompresses & strips | Never use for originals (document-transfer feature of WhatsApp keeps files intact) |
| Email attachments | ✅ Keeps (below size cap) | Fine for small batches |
| Telegram | ⚠️ "Send as file" keeps, normal send strips | Use file mode |

**Messaging-app filename patterns** (high-frequency cases):
- `IMG-YYYYMMDD-WA####.jpg` (WhatsApp) = the **date in the filename is the save/receive date, not necessarily capture date** — usable as fallback, mark `INFERRED-FILENAME`; the `WA####` suffix is a counter, not a time.
- `Snapchat-####.jpg`, `signal-YYYY-MM-DD-####.jpg` (Signal contains a date), Telegram files keep original names if sent as file.
- 13-digit numbers embedded in filenames = Unix **milliseconds**; 10 digits = Unix **seconds**. Both solvable; annotate provenance.

## 4. Device ecosystems

- **iPhone / iPad**: import via Finder cable sync with iCloud Photos disabled on both ends (works without iCloud; local Memories/Collections still generate). Photos synced via Finder cannot be deleted individually on the phone.
- **Android (Samsung / Pixel / etc.)**: USB-MTP file transfer or Google Photos upload (Original Quality); PTP tends to strip nothing but is slow for huge libraries — prefer MTP or SD-card reader.
- **DJI**: same as CN profile — `dji_mimo` filename milliseconds are **export time, not record time**; DJI private GPS lives in `UserData:GPSCoordinates`.
- **Live Photos**: Apple HEIC+MOV pairs linked by `ContentIdentifier` UUID (not filenames). exiftool writes may break pairing — verify on a sample before batch operations.

## 5. Video timestamps & timezones

- Videos recorded **outside** mainland China: `CreateDate` in mp4/mov is UTC — convert using **the capture-place timezone**, not a fixed offset (US Pacific is UTC−8/−7, Europe UTC+1/+2, Japan UTC+9, etc.).
- If the library was captured across many countries, derive each file's timezone from its GPS coordinates (if present) or from the itinerary table, then convert local capture time → UTC before writing. Files with no location: fall back to the home timezone.
- Write all three fields: `CreateDate`, `TrackCreateDate`, `MediaCreateDate` (`-AllDates` alone misses Track/Media).

## 6. Cloud albums / import targets

| Target | Method | Notes |
|---|---|---|
| iPhone/iPad | Finder cable sync (iCloud Photos off on both ends) | Works without iCloud; Memories still generate locally |
| iCloud Photos | Upload via Photos app (Download Originals verified) | Watch "Storage saver" recompression |
| Google Photos | Desktop uploader / drag in browser, **Original Quality** | Verify EXIF kept on a sample after upload |
| OneDrive / Dropbox | Desktop clients | Metadata-safe; run hash manifest before/after |

## 7. Global example scenario (validation case)

**User profile**: Chicago, USA. iPhone 15 Pro (primary, Live Photos) + partner's Pixel + a DJI pocket drone; years 2016–2026; library re-downloaded from Google Photos Takeout zips plus years of WhatsApp group images.

Walkthrough:
1. Phase 0 flatten → ~18,000 files. WhatsApp `IMG-20230812-WA0031.jpg` files are common → filename date is receive date, mark `INFERRED-FILENAME`.
2. Phase 1 time fix: EXIF first; WhatsApp files fall back to filename date; **never mtime** (Takeout zips rewrite mtimes to export day).
3. Phase 1.5 itinerary: Google Maps Timeline (Takeout) + airline/hotel emails + credit-card CSV → `daily_city.csv`; city dictionary in **WGS-84, no conversion needed**.
4. Phase 2 GPS: fill by capture date → itinerary → coordinates; keep existing real GPS (e.g., a Cancun vacation with correct GPS) untouched. Videos: CreateDate converted with **capture-place timezone**.
5. Phase 4/5 dedup: Apple Live Photo HEIC+MOV pairs kept intact (verify ContentIdentifier); CLIP same-day 0.94 → deep round 0.88; pet/special groups at 0.98.
6. Phase 8 import: iPhone via Finder sync; Google Photos via Original-Quality upload; hash manifest compared before/after upload.

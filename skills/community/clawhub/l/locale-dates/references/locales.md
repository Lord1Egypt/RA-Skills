# Locale Reference Table

Auto-detected or user-specified locale determines date/time formatting.
Each entry shows: date pattern, time pattern, 12/24h, and first day of week.

## How to Read This Table

- **Date**: The standard date format for the locale
- **Time**: 12h or 24h clock preference
- **Sep**: Separator character used in dates
- **DOW**: First day of the week (Mon/Sun)
- **ISO fallback**: Always use ISO 8601 when in doubt

## Europe

### Nordic Countries

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Norway | nb-NO | DD.MM.YYYY | 24h | . | Mon | `27.03.2026 kl. 18:30` |
| Sweden | sv-SE | YYYY-MM-DD | 24h | - | Mon | `2026-03-27 18:30` |
| Denmark | da-DK | DD.MM.YYYY | 24h | . | Mon | `27.03.2026 18.30` |
| Finland | fi-FI | DD.MM.YYYY | 24h | . | Mon | `27.03.2026 18.30` |
| Iceland | is-IS | DD.MM.YYYY | 24h | . | Mon | `27.03.2026 18:30` |

### Western Europe

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| United Kingdom | en-GB | DD/MM/YYYY | 24h* | / | Mon | *12h common in speech |
| Ireland | en-IE | DD/MM/YYYY | 24h | / | Mon | |
| Germany | de-DE | DD.MM.YYYY | 24h | . | Mon | `27.03.2026, 18:30` |
| Austria | de-AT | DD.MM.YYYY | 24h | . | Mon | |
| Switzerland (DE) | de-CH | DD.MM.YYYY | 24h | . | Mon | |
| Switzerland (FR) | fr-CH | DD.MM.YYYY | 24h | . | Mon | |
| France | fr-FR | DD/MM/YYYY | 24h | / | Mon | `27/03/2026 18:30` |
| Belgium (FR) | fr-BE | DD/MM/YYYY | 24h | / | Mon | |
| Belgium (NL) | nl-BE | DD/MM/YYYY | 24h | / | Mon | |
| Netherlands | nl-NL | DD-MM-YYYY | 24h | - | Mon | `27-03-2026 18:30` |
| Luxembourg | lb-LU | DD.MM.YYYY | 24h | . | Mon | |
| Portugal | pt-PT | DD/MM/YYYY | 24h | / | Mon | |
| Spain | es-ES | DD/MM/YYYY | 24h | / | Mon | `27/03/2026, 18:30` |
| Italy | it-IT | DD/MM/YYYY | 24h | / | Mon | `27/03/2026 18:30` |
| Malta | mt-MT | DD/MM/YYYY | 24h | / | Sun | |

### Central & Eastern Europe

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Poland | pl-PL | DD.MM.YYYY | 24h | . | Mon | |
| Czech Republic | cs-CZ | DD.MM.YYYY | 24h | . | Mon | |
| Slovakia | sk-SK | DD.MM.YYYY | 24h | . | Mon | |
| Hungary | hu-HU | YYYY.MM.DD | 24h | . | Mon | `2026.03.27. 18:30` |
| Romania | ro-RO | DD.MM.YYYY | 24h | . | Mon | |
| Bulgaria | bg-BG | DD.MM.YYYY | 24h | . | Mon | `27.03.2026 г. 18:30 ч.` |
| Greece | el-GR | DD/MM/YYYY | 24h | / | Mon | |
| Croatia | hr-HR | DD.MM.YYYY. | 24h | . | Mon | Note trailing dot |
| Slovenia | sl-SI | DD.MM.YYYY | 24h | . | Mon | |
| Serbia | sr-RS | DD.MM.YYYY | 24h | . | Mon | |
| Bosnia | bs-BA | DD.MM.YYYY | 24h | . | Mon | |
| North Macedonia | mk-MK | DD.MM.YYYY | 24h | . | Mon | |
| Albania | sq-AL | DD.MM.YYYY | 24h | . | Mon | |
| Ukraine | uk-UA | DD.MM.YYYY | 24h | . | Mon | |
| Moldova | ro-MD | DD.MM.YYYY | 24h | . | Mon | |
| Lithuania | lt-LT | YYYY-MM-DD | 24h | - | Mon | |
| Latvia | lv-LV | DD.MM.YYYY | 24h | . | Mon | |
| Estonia | et-EE | DD.MM.YYYY | 24h | . | Mon | |

### Baltic & Nordic (EU/non-EU)

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Faroe Islands | fo-FO | DD.MM.YYYY | 24h | . | Mon | |

## Americas

### North America

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| United States | en-US | MM/DD/YYYY | 12h | / | Sun | `03/27/2026, 6:30 PM` |
| Canada (EN) | en-CA | YYYY-MM-DD | 12h | - | Sun | ISO-like date, 12h time |
| Canada (FR) | fr-CA | YYYY-MM-DD | 24h | - | Sun | |

### Latin America

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Mexico | es-MX | DD/MM/YYYY | 24h | / | Mon | |
| Brazil | pt-BR | DD/MM/YYYY | 24h | / | Sun | |
| Argentina | es-AR | DD/MM/YYYY | 24h | / | Mon | |
| Chile | es-CL | DD-MM-YYYY | 24h | - | Mon | |
| Colombia | es-CO | DD/MM/YYYY | 24h | / | Mon | |
| Peru | es-PE | DD/MM/YYYY | 24h | / | Mon | |
| Venezuela | es-VE | DD/MM/YYYY | 24h | / | Mon | |
| Ecuador | es-EC | DD/MM/YYYY | 24h | / | Mon | |
| Bolivia | es-BO | DD/MM/YYYY | 24h | / | Mon | |
| Uruguay | es-UY | DD/MM/YYYY | 24h | / | Mon | |
| Paraguay | es-PY | DD/MM/YYYY | 24h | / | Mon | |
| Costa Rica | es-CR | DD/MM/YYYY | 24h | / | Mon | |
| Panama | es-PA | MM/DD/YYYY | 12h | / | Sun | US-style |
| Guatemala | es-GT | DD/MM/YYYY | 24h | / | Mon | |
| Cuba | es-CU | DD/MM/YYYY | 24h | / | Mon | |
| Dominican Republic | es-DO | DD/MM/YYYY | 12h | / | Mon | |

## Asia

### East Asia

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Japan | ja-JP | YYYY/MM/DD | 24h | / | Sun | `2026/03/27 18:30` or `2026年03月27日 18時30分` |
| South Korea | ko-KR | YYYY.MM.DD | 12h | . | Sun | `2026.03.27. 오후 6:30` |
| China | zh-CN | YYYY-MM-DD | 24h | - | Mon | `2026年3月27日 18:30` |
| Taiwan | zh-TW | YYYY/MM/DD | 24h | / | Sun | 民國 calendar also used |
| Hong Kong | zh-HK | DD/MM/YYYY | 24h | / | Mon | |
| Mongolia | mn-MN | YYYY.MM.DD | 24h | . | Mon | |

### Southeast Asia

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Thailand | th-TH | DD/MM/YYYY | 24h | / | Sun | Buddhist year (BE = CE + 543) |
| Vietnam | vi-VN | DD/MM/YYYY | 24h | / | Mon | |
| Indonesia | id-ID | DD/MM/YYYY | 24h | / | Mon | |
| Malaysia | ms-MY | DD/MM/YYYY | 12h | / | Mon | |
| Philippines | fil-PH | MM/DD/YYYY | 12h | / | Sun | US-style |
| Singapore | en-SG | DD/MM/YYYY | 12h | / | Mon | |
| Myanmar | my-MM | DD-MM-YYYY | 24h | - | Sun | |
| Cambodia | km-KH | DD/MM/YYYY | 24h | / | Mon | |
| Laos | lo-LA | DD/MM/YYYY | 24h | / | Mon | |

### South Asia

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| India | hi-IN | DD-MM-YYYY | 24h | - | Mon | |
| Bangladesh | bn-BD | DD-MM-YYYY | 24h | - | Sun | |
| Pakistan | ur-PK | DD/MM/YYYY | 12h | / | Mon | |
| Sri Lanka | si-LK | YYYY-MM-DD | 24h | - | Mon | |
| Nepal | ne-NP | YYYY-MM-DD | 24h | - | Sun | Bikram Sambat calendar also |
| Afghanistan | fa-AF | YYYY/MM/DD | 24h | / | Sat | Solar Hijri calendar also |
| Iran | fa-IR | YYYY/MM/DD | 24h | / | Sat | Solar Hijri: ۱۴۰۴/۰۱/۰۷ |

### Middle East

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Saudi Arabia | ar-SA | DD/MM/YYYY | 12h | / | Sun | Islamic (Hijri) calendar also |
| UAE | ar-AE | DD/MM/YYYY | 12h | / | Sun | |
| Qatar | ar-QA | DD/MM/YYYY | 12h | / | Sun | |
| Kuwait | ar-KW | DD/MM/YYYY | 12h | / | Sun | |
| Bahrain | ar-BH | DD/MM/YYYY | 12h | / | Sun | |
| Oman | ar-OM | DD/MM/YYYY | 12h | / | Sun | |
| Jordan | ar-JO | DD/MM/YYYY | 12h | / | Sun | |
| Lebanon | ar-LB | DD/MM/YYYY | 12h | / | Mon | |
| Iraq | ar-IQ | DD/MM/YYYY | 24h | / | Sat | |
| Israel | he-IL | DD.MM.YYYY | 24h | . | Sun | Hebrew calendar also |
| Turkey | tr-TR | DD.MM.YYYY | 24h | . | Mon | |

## Africa

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| South Africa | en-ZA | YYYY/MM/DD | 24h | / | Sun | |
| Nigeria | en-NG | DD/MM/YYYY | 12h | / | Mon | |
| Kenya | sw-KE | DD/MM/YYYY | 24h | / | Mon | |
| Egypt | ar-EG | DD/MM/YYYY | 12h | / | Sat | |
| Morocco | ar-MA | DD/MM/YYYY | 24h | / | Mon | |
| Tunisia | ar-TN | DD/MM/YYYY | 24h | / | Mon | |
| Algeria | ar-DZ | DD/MM/YYYY | 24h | / | Sun | |
| Ethiopia | am-ET | DD/MM/YYYY | 24h | / | Sun | Ethiopian calendar also |
| Ghana | en-GH | DD/MM/YYYY | 24h | / | Mon | |
| Tanzania | sw-TZ | DD/MM/YYYY | 24h | / | Mon | |
| Uganda | en-UG | DD/MM/YYYY | 12h | / | Mon | |
| Rwanda | rw-RW | DD/MM/YYYY | 24h | / | Mon | |

## Oceania

| Country | Locale | Date | Time | Sep | DOW | Notes |
|---------|--------|------|------|-----|-----|-------|
| Australia | en-AU | DD/MM/YYYY | 12h* | / | Mon | *24h common in writing |
| New Zealand | en-NZ | DD/MM/YYYY | 12h* | / | Mon | *24h common in writing |
| Fiji | en-FJ | DD/MM/YYYY | 12h | / | Mon | |
| Papua New Guinea | en-PG | DD/MM/YYYY | 12h | / | Mon | |

## Non-Geographic / Universal

| Name | Locale | Date | Time | Notes |
|------|--------|------|------|-------|
| ISO 8601 | — | YYYY-MM-DD | 24h | Always safe fallback |
| RFC 3339 | — | YYYY-MM-DDTHH:mm:ssZ | 24h | Internet standard (subset of ISO) |
| Unix epoch | — | seconds since 1970-01-01 | — | Technical use only |
| ISO week date | — | YYYY-Www-D | — | `2026-W13-5` (Friday of week 13) |
| ISO ordinal | — | YYYY-DDD | — | `2026-086` (day 86 of year) |

## Calendars Beyond Gregorian

Some locales use non-Gregorian calendars alongside or instead of the Gregorian calendar. Always ask before using a non-Gregorian format.

| Calendar | Locales | Year offset | Note |
|----------|---------|-------------|------|
| Buddhist (BE) | Thailand, Cambodia, Laos | +543 | `2569` in 2026 |
| Japanese Imperial | Japan | Era-based | `令和8年` (Reiwa 8) |
| Chinese | China, Taiwan | — | Luni-solar, used for holidays |
| Islamic (Hijri) | Saudi Arabia, UAE, etc. | ~-622 | `١٤٤٧/٠٩/٠٧` |
| Hebrew | Israel | ~-3760 | Used for religious dates |
| Persian (Solar Hijri) | Iran, Afghanistan | ~-621 | `1404/01/07` |
| Ethiopian | Ethiopia | ~-7/8 | `2018-03-27` |
| Bikram Sambat | Nepal | +56/57 | `2082-03-13` |
| Amrita Kosh | (historical) | — | Rare, avoid unless asked |

## Quick Decision Guide

**When unsure, use ISO 8601.** It is always correct, unambiguous, and universally understood.

- **Technical contexts** (logs, APIs, configs): ISO 8601 (`2026-03-27T18:30:00+01:00`)
- **Casual Norwegian**: `27. mars 2026 kl. 18:30`
- **Casual American**: `March 27, 2026 at 6:30 PM`
- **Formal international**: `27 March 2026, 18:30 CET`
- **Ambiguous dates** (MM/DD vs DD/MM): Always spell out the month or use ISO

---
name: kto-tourapi-cli
description: Korean tourism content (관광지·문화시설·축제공연·여행코스·레포츠·숙박·쇼핑·음식점) via 한국관광공사 TourAPI 4.0 (apis.data.go.kr/B551011/KorService2). Eight subcommands wrap areaCode2, categoryCode2, areaBasedList2, locationBasedList2, searchKeyword2, searchFestival2, searchStay2, and a one-shot detail fetch (detailCommon2 + detailIntro2 + detailInfo2 + detailImage2). Use when planning Korea trip itineraries, building festival calendars, sourcing K-tourism content for blogs/maps/videos, finding nearby restaurants or stays from a coordinate, or backing TourAPI-grounded answers in an AI agent. Pairs with juso-address-cli (resolve addresses), kakao-local-cli (Kakao Maps pins), kr-holiday-cli (align with KR calendar), naver-papago-translate (localize for non-KR users), and tistory-api-cli / velog-cli (publish itineraries). Free data.go.kr tier (1,000 req/day dev, 10,000+ req/day on prod approval).
version: 0.1.0
license: MIT
---

# kto-tourapi-cli

Command-line wrapper for **한국관광공사 TourAPI 4.0 (KorService2)** — Korea's first-party tourism content API. Curated and maintained by 한국관광공사 (Korea Tourism Organization), it's the data behind VisitKorea, 대한민국 구석구석, and most travel apps in Korea.

Eight subcommands, each wraps one (or one composite) endpoint:

| Command | Endpoint(s) | Purpose |
|---|---|---|
| `scripts/area-code.sh`     | `areaCode2`                | 17개 광역시도 → 시군구 코드 트리. |
| `scripts/category-code.sh` | `categoryCode2`            | 3-level cat1/cat2/cat3 service-classification tree. |
| `scripts/area.sh`          | `areaBasedList2`           | Browse content by area / sigungu / contentType / category. |
| `scripts/nearby.sh`        | `locationBasedList2`       | Radius search (≤20 km) from a (lng, lat) point. |
| `scripts/search.sh`        | `searchKeyword2`           | Keyword search with optional area/category filters. |
| `scripts/festival.sh`      | `searchFestival2`          | Festivals/events overlapping a date window. |
| `scripts/stay.sh`          | `searchStay2`              | Lodging-only browse (hotels, motels, pensions, hanok stays). |
| `scripts/detail.sh`        | `detailCommon2` + `detailIntro2` + `detailInfo2` + `detailImage2` | One-shot full record for a `contentId`. |

All output is JSONL — one row per item — so it pipes directly into `jq`, `csvkit`, `pandas`, or downstream skills.

## When to use this skill

- **Trip planning agents** — "build me a 3-day Gangneung itinerary" → `area --area-code 32 --sigungu-code 1` + `nearby --lng <h1> --lat <h1>` + `festival --start 20260601`.
- **Festival calendars** — `festival --start YYYYMMDD --end YYYYMMDD` → JSONL → cal.json.
- **K-content blogs / videos** — `search --keyword 강릉` then `detail --content-id <id> --include-images` for hero imagery + descriptions.
- **Nearby-X discovery on maps** — feed Kakao map taps into `nearby --lng X --lat Y --content-type-id 39` to surface restaurants.
- **Government/NGO grounded answers** — TourAPI is curated by KTO; use it when you need authoritative tourism facts, not crowd-sourced.

## Do **not** use this skill for

- **Real-time prices, availability, bookings** — TourAPI is a *content directory*, not a reservation API. Pair with stay-platform APIs (야놀자, 여기어때, Booking.com) for live inventory.
- **User reviews / ratings** — TourAPI does not expose review counts. Use Naver Place / Kakao Map APIs.
- **English / non-KR languages** — this skill targets `KorService2`. KTO publishes parallel `EngService2` / `ChsService2` / `JpnService2` / `GerService2` / `FreService2` / `SpnService2` / `RusService2` endpoints; not in this skill yet.
- **High-throughput public-facing apps without quota** — the dev-tier ceiling is 1,000 req/day. Apply for production tier on data.go.kr.

## Prerequisites

1. **Register at <https://www.data.go.kr/>** (Korean OpenData portal, free, no business required).
2. Apply for **"한국관광공사_국문 관광정보 서비스_GW"** (TourAPI 4.0 / KorService2). Approval is automatic for the dev tier.
3. Copy your **Decoding** key (the raw, *not* URL-encoded form) and export:
   ```bash
   export TOURAPI_SERVICE_KEY='your_decoded_key_here'
   ```
4. Optional overrides:
   ```bash
   export TOURAPI_BASE='https://apis.data.go.kr/B551011/KorService2'
   export TOURAPI_MOBILE_OS='ETC'             # ETC|AND|IOS|WIN|WEB
   export TOURAPI_MOBILE_APP='your-app-name'  # any short identifier
   ```
5. Dependencies: `bash`, `curl`, `jq` (default on macOS / standard Linux).

## Reference codes

**contentTypeId** (used in `--content-type-id`):

| ID | Type        | ID | Type           |
|----|-------------|----|----------------|
| 12 | 관광지        | 28 | 레포츠           |
| 14 | 문화시설       | 32 | 숙박             |
| 15 | 축제공연행사    | 38 | 쇼핑             |
| 25 | 여행코스       | 39 | 음식점           |

**Top-level areaCode** (run `area-code.sh` for fresh sigungu codes):

| Code | Region    | Code | Region        | Code | Region |
|------|-----------|------|---------------|------|--------|
| 1    | 서울       | 32   | 강원도         | 6    | 부산    |
| 2    | 인천       | 33   | 충청북도       | 7    | 대구    |
| 31   | 경기도     | 34   | 충청남도       | 8    | 광주    |
| 35   | 경상북도   | 36   | 경상남도       | 9    | 대전    |
| 37   | 전라북도   | 38   | 전라남도       | 10   | 울산    |
| 39   | 제주특별자치도 |    |              | 11   | 세종특별자치시 |

(Full canonical list always: `bash scripts/area-code.sh`.)

**Top-level cat1**: A01=자연 / A02=인문(문화/예술/역사) / A03=레포츠 / A04=쇼핑 / A05=음식 / B02=숙박 / C01=추천코스.

## Examples

### Browse 관광지 in 강릉
```bash
bash scripts/area.sh --area-code 32 --sigungu-code 1 --content-type-id 12 --num 10
```

### Find 음식점 within 500 m of 경복궁 (lng 126.9770, lat 37.5797)
```bash
bash scripts/nearby.sh --lng 126.9770 --lat 37.5797 --radius 500 --content-type-id 39
```

### Festival list for May 2026 in Jeju
```bash
bash scripts/festival.sh --start 20260501 --end 20260531 --area-code 39
```

### Keyword search for "한옥" stays
```bash
bash scripts/search.sh --keyword 한옥 --content-type-id 32 --num 30
```

### Full record (with images) for 경복궁 (contentId 264432)
```bash
bash scripts/detail.sh --content-id 264432 --content-type-id 14 --include-images
```

### Ten-day Korea festival calendar for content automation
```bash
START=$(date -u +%Y%m%d)
END=$(date -u -v+10d +%Y%m%d 2>/dev/null || date -u -d "+10 days" +%Y%m%d)
bash scripts/festival.sh --start "$START" --end "$END" --num 100 \
  | jq -r '[.title, .eventstartdate, .eventenddate, .addr1] | @tsv'
```

## Field naming

TourAPI returns lowercase field names without delimiters (e.g. `mapx`, `mapy`, `addr1`, `addr2`, `firstimage`, `firstimage2`, `tel`, `eventstartdate`, `eventenddate`, `dist`). The CLI passes these through verbatim so downstream pipelines keep schema parity with TourAPI's published spec.

## Errors

- `exit 64` — bad CLI input (missing required flag, invalid date, unknown contentTypeId).
- `exit 78` — `TOURAPI_SERVICE_KEY` env var missing.
- `exit 22` — TourAPI returned non-2xx, an XML error envelope, or `resultCode != "0000"`. The full body is echoed to stderr.
- `exit 127` — required binary (`curl`, `jq`) not on PATH.

## Pairs with

- **juso-address-cli** — resolve raw `addr1` → 우편번호 + 행정동 코드.
- **kakao-local-cli** — drop `mapx`/`mapy` directly onto Kakao Maps.
- **kr-holiday-cli** — overlay legal holidays onto the festival calendar.
- **naver-papago-translate** — localize titles/overviews for non-KR users.
- **tistory-api-cli** / **velog-cli** — publish the rendered itinerary.
- **kosis-cli** / **bank-of-korea-ecos-cli** — overlay tourism volume / FX context for travel-economics posts.

## License

MIT-0. Data is © 한국관광공사 / 공공데이터포털 — credit per data.go.kr terms when republishing.

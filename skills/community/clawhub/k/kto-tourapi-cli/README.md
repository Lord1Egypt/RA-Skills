# kto-tourapi-cli

CLI wrapper around **한국관광공사 TourAPI 4.0 (KorService2)** — Korea's first-party tourism content API.

Eight subcommands (`area-code`, `category-code`, `area`, `nearby`, `search`, `festival`, `stay`, `detail`) covering points-of-interest, festivals, lodgings, and full content detail. JSONL output, pipes into jq / pandas / downstream skills.

## Quick start

```bash
# 1. Apply for "한국관광공사_국문 관광정보 서비스_GW" at data.go.kr (free).
# 2. Export the *Decoding* key:
export TOURAPI_SERVICE_KEY='your_decoded_key_here'

# 3. Browse 관광지 in 강릉:
bash scripts/area.sh --area-code 32 --sigungu-code 1 --content-type-id 12 --num 10

# 4. Find 음식점 within 500 m of 경복궁:
bash scripts/nearby.sh --lng 126.9770 --lat 37.5797 --radius 500 --content-type-id 39

# 5. Festivals overlapping May 2026 on Jeju:
bash scripts/festival.sh --start 20260501 --end 20260531 --area-code 39

# 6. Full record + images for contentId 264432:
bash scripts/detail.sh --content-id 264432 --content-type-id 14 --include-images
```

See [`SKILL.md`](./SKILL.md) for the full command catalogue, contentTypeId / areaCode reference tables, and pairing notes.

## Why this exists

Every Korean travel app, itinerary builder, blog, or AI agent that talks about Korean places eventually wants TourAPI: it's the only authoritative tourism content directory in Korea and the underlying data behind VisitKorea + 대한민국 구석구석. But the raw API has 14+ endpoints, 8 contentTypeIds, a 3-level category tree, and three different list shapes (`item` may be array, object, or absent). This skill normalizes all of that into one consistent JSONL stream.

## Pairs with

- [`juso-address-cli`](https://github.com/ChloePark85/juso-address-cli) — resolve `addr1` → postal code + admin code
- [`kakao-local-cli`](https://github.com/ChloePark85/kakao-local-cli) — render `mapx`/`mapy` on Kakao Maps
- [`kr-holiday-cli`](https://github.com/ChloePark85/kr-holiday-cli) — overlay legal holidays onto a festival calendar
- [`naver-papago-translate`](https://github.com/ChloePark85/naver-papago-translate) — localize for non-KR readers
- [`tistory-api-cli`](https://github.com/ChloePark85/tistory-api-cli) / [`velog-cli`](https://github.com/ChloePark85/velog-cli) — publish the rendered itinerary

## License

MIT-0. Data © 한국관광공사 / data.go.kr (credit when republishing).

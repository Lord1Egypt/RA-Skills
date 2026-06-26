---
name: naver-shopping
description: Search for products on Naver Shopping. Use when the user wants to find product prices, links, or compare items in the Korean market.
---

# Naver Shopping Search

네이버 쇼핑 Search API로 한국 상품 검색을 수행한다.

## Usage

검색어를 넣어 스크립트를 실행한다.

```bash
python skills/naver-shopping/scripts/search_shopping.py "상품명"
```

### Options

- `--display <number>`: Number of results to show (default: 5, max: 100)
- `--sort <sim|date|asc|dsc>`: Sort order (sim: similarity, date: date, asc: price ascending, dsc: price descending)

### Example

```bash
python skills/naver-shopping/scripts/search_shopping.py "아이폰 16" --display 3 --sort asc
```

## Environment Variables

다음 중 하나의 이름으로 자격증명을 읽는다.
- `NAVER_Client_ID` / `NAVER_Client_Secret`
- `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET`
- `NAVER_SHOPPING_CLIENT_ID` / `NAVER_SHOPPING_CLIENT_SECRET`

우선 순위:
1. 현재 환경 변수
2. `skills/naver-shopping/.env`
3. `~/.openclaw/credentials/naver-shopping.env`

# naver-datalab-cli

Korean search-keyword and shopping-trend analytics via the official **NAVER DataLab Open API**. The Korean equivalent of Google Trends — but with two big advantages on KR-market analysis: NAVER drives ~55% of Korean search traffic, and the **쇼핑인사이트** endpoints expose category-level shopping demand split by device / age / gender (Google Trends cannot do this).

## Install

```bash
clawhub install naver-datalab-cli
```

Or clone:

```bash
git clone https://github.com/ChloePark85/naver-datalab-cli
cd naver-datalab-cli
```

## Setup

1. Register a NAVER Developers app: <https://developers.naver.com/apps/#/register>. Enable **검색어트렌드** and **쇼핑인사이트**.
2. Export credentials:
   ```bash
   export NAVER_CLIENT_ID='abcdEFG12345'
   export NAVER_CLIENT_SECRET='AbCdEfGhIj'
   ```
3. Make the scripts executable (clone path only):
   ```bash
   chmod +x scripts/*.sh examples/*.sh
   ```

Free-tier quota: 25,000 req/day for `/v1/datalab/search`, 1,000 req/day for shopping endpoints.

## Quick start

Compare two keyword groups monthly through 2024:

```bash
scripts/search.sh \
  --start 2024-01-01 --end 2024-12-31 --time-unit month \
  --group "한국어:한국어,한글" \
  --group "영어:영어,English"
```

Output (JSONL):

```
{"groupName":"한국어","period":"2024-01-01","ratio":78.32}
{"groupName":"한국어","period":"2024-02-01","ratio":81.10}
...
{"groupName":"영어","period":"2024-12-01","ratio":100.00}
```

Pipe to `jq -s 'sort_by(-.ratio) | .[0:5]'` to get the top 5 periods, or pipe to `csvkit`/`pandas` for plotting.

## Subcommands

| Command | What it returns |
|---|---|
| `search`         | 통합 검색어 트렌드 — up to 5 keyword groups × time. |
| `shop-cat`       | 쇼핑인사이트 분야별 — up to 3 shopping categories × time. |
| `shop-keyword`   | 쇼핑인사이트 분야 내 키워드 — 1 category, up to 5 keyword groups. |
| `shop-device`    | 분야의 기기 분포 (pc / mo) × time. |
| `shop-gender`    | 분야의 성별 분포 (f / m) × time. |
| `shop-age`       | 분야의 연령대 분포 (10/20/30/40/50/60) × time. |

See `SKILL.md` for the full flag reference and `examples/` for canned recipes.

## Notes

- DataLab returns *relative* indices (peak in the response = 100), never raw query counts. NAVER does not publish raw counts.
- `timeUnit` is `date | week | month` (no `day`).
- Search-trend ages are 1–9 codes (1=under 12, ..., 9=60+). Shopping-trend ages are decade buckets (10/20/30/40/50/60).
- Data lags ~24-48 hours behind real-time.

## Pairs with

- [naver-papago-translate](https://github.com/ChloePark85/naver-papago-translate) — translate the trend report into EN/JP/ZH.
- [tistory-api-cli](https://github.com/ChloePark85/tistory-api-cli) / [velog-cli](https://github.com/ChloePark85/velog-cli) — publish weekly Korean-trend posts.
- [kr-holiday-cli](https://github.com/ChloePark85/kr-holiday-cli) — overlay holiday/business-day calendar onto seasonal spikes.
- [kakao-local-cli](https://github.com/ChloePark85/kakao-local-cli) + [juso-address-cli](https://github.com/ChloePark85/juso-address-cli) — geo-resolve emergent place keywords.

## License

MIT.

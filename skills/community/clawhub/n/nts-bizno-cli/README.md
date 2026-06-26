# nts-bizno-cli

CLI wrapper around the **NTS (국세청) 사업자등록정보 진위확인 및 상태조회** public API.

Verify Korean business registration numbers from the terminal:

- **status** — operating status (계속/휴업/폐업) + tax type, up to 100 b_no per call
- **validate** — full authenticity check (b_no + 개업일 + 대표자명)
- **format** — local checksum verification, no API key needed
- **bulk** — file-driven sweep with auto-batching & checksum pre-filter

JSONL output, no Python deps — just `bash`, `curl`, `jq`.

## Install via ClawHub

```bash
clawhub install nts-bizno-cli
export NTS_API_KEY='<encoded-serviceKey-from-data.go.kr>'
```

Get the serviceKey at <https://www.data.go.kr> → search "국세청 사업자등록정보 진위확인 및 상태조회 서비스" → 활용신청 (free, ≤1 business day, 10,000 req/day quota).

## Quick start

```bash
# Status — one or many b_no's
scripts/status.sh 124-81-00998 220-81-62517

# Validate — does (b_no, 개업일, 대표자명) match NTS?
scripts/validate.sh --b-no 124-81-00998 --start-dt 19690113 --p-nm "한종희"

# Local-only — checksum + format without burning API quota
scripts/format.sh 1248100998 1234567890

# Bulk — read a file, batch in groups of 100
scripts/bulk.sh suppliers.txt > audit.jsonl
```

See `SKILL.md` for full output schema, status/tax codes, and pipeline examples.

## Why this skill

Korean B2B onboarding requires verifying that a counterparty's business is **registered**, **active**, and the **stated representative + opening date match NTS records** before you can issue 세금계산서, sign contracts, or release payment. The NTS provides this for free, but the API is XML-flavored, requires odcloud serviceKey wrapping, and has two distinct endpoints with different quota rules. This skill packages all of that into terminal-friendly JSONL.

Pairs with [`unified-invoice`](../unified-invoice) (form fill), [`opendart-cli`](../opendart-cli) (corporate filings), and [`juso-address-cli`](../juso-address-cli) (address resolution).

## License

MIT — see `LICENSE`.

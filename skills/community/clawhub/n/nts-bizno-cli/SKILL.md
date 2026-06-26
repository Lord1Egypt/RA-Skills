---
name: nts-bizno-cli
description: Verify Korean business registration numbers (사업자등록번호) via the official NTS (국세청) public API. Operating-status lookup (계속/휴업/폐업), full authenticity check (b_no + 개업일 + 대표자명), local checksum validation without API calls, and bulk file processing. Use when onboarding Korean businesses, validating B2B partners, building KYB pipelines, deduplicating supplier lists, or pre-filling 세금계산서/견적서/계약서 forms with NTS-confirmed data. Pairs with unified-invoice (form fill), opendart-cli (corporate filings), and juso-address-cli (address resolution) to complete the Korean B2B onboarding toolchain.
version: 0.1.0
license: MIT
---

# nts-bizno-cli

Command-line wrapper for the **NTS 사업자등록정보 진위확인 및 상태조회 서비스** (Korean National Tax Service business-registration API), exposed via `data.go.kr` / `api.odcloud.kr`.

Two official endpoints + two local conveniences:

| Command | Endpoint | API key? | Purpose |
|---|---|---|---|
| `scripts/status.sh`   | `POST /v1/status`   | yes | Look up operating status (계속사업자/휴업자/폐업자) for up to 100 b_no per call. |
| `scripts/validate.sh` | `POST /v1/validate` | yes | Authenticity check — does (b_no + 개업일 + 대표자명) match NTS records? |
| `scripts/format.sh`   | local                | no  | Verify checksum + format `XXX-XX-XXXXX`. No network. |
| `scripts/bulk.sh`     | `POST /v1/status`   | yes | Read a file of b_no's, checksum-filter, batch-call status in groups of 100. |

All output is JSONL (one record per line) so it pipes straight into `jq`, `csvkit`, or downstream skills.

## When to use this skill

- **B2B onboarding / KYB** — verify a partner's business number is real and currently active before contract signing or payment release.
- **Supplier-list cleanup** — bulk-check thousands of b_no's, flag the closed (폐업자) and dormant (휴업자).
- **Form-fill validation** — confirm a user's typed b_no is structurally valid *before* hitting the API (saves quota and cost).
- **Tax-invoice (세금계산서) issuance gate** — Korean law requires verifying the counterparty's tax type (일반/간이/면세) before issuing; this returns it.
- **Public-procurement (나라장터) prep** — validate vendor records before bid submission.

## Do **not** use this skill for

- Address lookup → use `juso-address-cli`.
- Corporate-filings / disclosure data → use `opendart-cli`.
- Issuing the actual tax invoice → use `unified-invoice`.
- Looking up a business by *name* — NTS does not expose name-based search; you need the b_no first.

## Prerequisites

1. **Get a serviceKey** at <https://www.data.go.kr> (free, 1 business-day approval):
   - Search for "**국세청 사업자등록정보 진위확인 및 상태조회 서비스**".
   - Click **활용신청** (one form per API). Both `상태조회` and `진위확인` are commonly approved on the same day. Free-tier quota is **10,000 requests/day** for each.
2. Export the encoded key:
   ```bash
   export NTS_API_KEY='Ad9...%2BAbc%3D'    # paste the "일반 인증키 (Encoding)" value
   ```
   Use the **Encoding** key (URL-encoded) — the wrapper passes it through `serviceKey=` directly.
3. Dependencies: `bash`, `curl`, `jq` (default on macOS/Linux).

## Commands

### 1) Status lookup (`scripts/status.sh`)

```bash
# Single
scripts/status.sh 124-81-00998

# Multiple (up to 100 per call)
scripts/status.sh 1248100998 220-81-62517 120-81-47521
```

Sample row:
```json
{"b_no":"1248100998","b_no_formatted":"124-81-00998","b_stt_cd":"01","b_stt":"계속사업자","tax_type_cd":"01","tax_type":"부가가치세 일반과세자","end_dt":"","utcc_yn":"N","tax_type_change_dt":"","invoice_apply_dt":"","rbf_tax_type_cd":"","rbf_tax_type":""}
```

Status codes:
- `b_stt_cd=01` → 계속사업자 (active)
- `b_stt_cd=02` → 휴업자 (dormant)
- `b_stt_cd=03` → 폐업자 (closed) — `end_dt` carries 폐업일.
- `b_stt_cd=""` → b_no not registered with NTS at all.

Tax-type codes:
- `01` 부가가치세 일반과세자, `02` 부가가치세 간이과세자, `03` 부가가치세 면세사업자, `04` 비영리법인, `05`/`06` 외국 / 임시.

### 2) Authenticity check (`scripts/validate.sh`)

Single record — flags:
```bash
scripts/validate.sh \
  --b-no 124-81-00998 \
  --start-dt 19690113 \
  --p-nm "한종희"
```

Batch — JSON file:
```bash
cat > /tmp/payload.json <<'EOF'
{"businesses":[
  {"b_no":"1248100998","start_dt":"19690113","p_nm":"한종희","p_nm2":"","b_nm":"","corp_no":"","b_sector":"","b_type":""},
  {"b_no":"2208162517","start_dt":"19990602","p_nm":"최수연","p_nm2":"","b_nm":"","corp_no":"","b_sector":"","b_type":""}
]}
EOF
scripts/validate.sh --file /tmp/payload.json
```

Sample row:
```json
{"b_no":"1248100998","b_no_formatted":"124-81-00998","valid":true,"valid_code":"01","valid_msg":"확인","status":{...}}
```

`valid: true` ⇔ NTS confirms a match. `valid: false` (`valid_code:"02"`) means at least one of (b_no, 개업일, 대표자명) does not match — `valid_msg` carries the reason.

### 3) Local checksum (`scripts/format.sh`)

No network, no key. Cheap pre-filter before hitting the API.

```bash
scripts/format.sh 1248100998 abc-def-1234 220-81-62517
# {"input":"1248100998","normalized":"1248100998","formatted":"124-81-00998","valid_checksum":true}
# {"input":"abc-def-1234","normalized":"abcdef1234","formatted":"abcdef1234","valid_checksum":false}
# {"input":"220-81-62517","normalized":"2208162517","formatted":"220-81-62517","valid_checksum":true}
```

Algorithm (NTS official): weights `[1,3,7,1,3,7,1,3,5]` over the first 9 digits, plus `floor(d8*5/10)`, mod 10, complement to 10. Saves you a network round trip on typo'd inputs.

### 4) Bulk processor (`scripts/bulk.sh`)

```bash
# File input — one b_no per line, comments with #
cat > /tmp/suppliers.txt <<'EOF'
124-81-00998   # Samsung Electronics
220-81-62517   # NAVER
120-81-47521   # Kakao
123-45-67890   # bogus typo
EOF
scripts/bulk.sh /tmp/suppliers.txt > /tmp/audit.jsonl

# stdin
psql -At -c 'SELECT bno FROM suppliers' | scripts/bulk.sh - > /tmp/audit.jsonl
```

`bulk.sh` runs the local checksum first; bad entries get flagged with `{"error":"checksum_failed"}` and never burn API quota. Good entries are batched in groups of 100 (NTS hard limit).

## Common pipelines

```bash
# Find all suppliers that closed
scripts/bulk.sh suppliers.txt | jq -c 'select(.b_stt_cd=="03") | {b_no, end_dt}'

# Tax-type breakdown
scripts/bulk.sh suppliers.txt | jq -r '.tax_type' | sort | uniq -c | sort -rn

# Onboarding gate — only proceed if 계속사업자 + 일반과세
scripts/status.sh "$BNO" \
  | jq -e 'select(.b_stt_cd=="01" and .tax_type_cd=="01")' >/dev/null \
  && echo "ok to issue 세금계산서" \
  || { echo "blocked"; exit 1; }
```

## Errors & quirks

- `code:-4 "등록되지 않은 인증키 입니다."` — your `NTS_API_KEY` is wrong or hasn't been approved yet for this specific endpoint. Check `data.go.kr → 마이페이지 → 활용신청 현황`.
- `code:-22 "사용한도..."` — you've exceeded your free-tier daily quota. Apply for 활용 한도 증가 in 마이페이지.
- The `validate` endpoint counts each item in `businesses[]` separately against quota; `status` counts only one request regardless of `b_no[]` length. Prefer `status` for cheap status sweeps.
- NTS returns historical `end_dt` even when `b_stt_cd != "03"` if the business was once closed and re-opened — read both fields.
- `start_dt` on `validate` must be **YYYYMMDD** (no dashes); pre-1900 / future dates are rejected.

## Project layout

```
nts-bizno-cli/
├── SKILL.md          # this file
├── README.md         # short user-facing intro (mirrors SKILL.md)
├── LICENSE           # MIT
├── scripts/
│   ├── _common.sh    # shared helpers (auth, POST, checksum, format)
│   ├── status.sh     # 상태조회
│   ├── validate.sh   # 진위확인
│   ├── format.sh     # local checksum + formatter
│   └── bulk.sh       # file-driven status sweep
└── examples/
    └── supplier-audit.md
```

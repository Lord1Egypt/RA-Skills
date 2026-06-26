# kosis-cli

Minimal command-line wrapper for **KOSIS — 국가통계포털 (Korean Statistical Information Service)** OpenAPI.

KOSIS is the central registry for Korean national statistics maintained by Statistics Korea (통계청), aggregating ~1,000 datasets from 100+ government agencies — population, employment, prices, household income, regional indicators, business demographics, and more.

## Why this skill?

Other Korean public-data wrappers cover their own slice of the stack:

- `bank-of-korea-ecos-cli` — macro time series (rates, FX, money supply)
- `opendart-cli` — listed-company financial filings
- `krx-stock-cli` — stock prices
- `kosis-cli` *(this skill)* — **everything else** the government counts: people, jobs, prices, incomes, regions

If you're an analyst, journalist, researcher, or policy team that needs Korean national statistics, this is the missing primitive.

## Install (as a ClawHub skill)

```bash
clawhub install kosis-cli
export KOSIS_API_KEY="..."   # get one at https://kosis.kr/openapi/devGuide/devGuide_0102.do
```

## Quick start

```bash
# Search the catalog by keyword
skills/kosis-cli/scripts/search.sh "소비자물가"

# Browse the topic tree
skills/kosis-cli/scripts/list.sh

# Inspect a table's items + dimensions before you query data
skills/kosis-cli/scripts/meta.sh 101 DT_1B040A3

# Pull the latest 12 monthly periods of population, all regions
skills/kosis-cli/scripts/data.sh 101 DT_1B040A3 --prd-se M --recent 12
```

See [`SKILL.md`](./SKILL.md) for the full agent-facing spec, including all five subcommands and field-level output reference.

## License

MIT. The underlying KOSIS data is public under 공공누리 제1유형.

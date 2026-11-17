# Verification Method

## Specification compliance

```bash
bash scripts/validate-skill.sh skills/compute/functiongraph/huawei-cloud-functiongraph-list
```

## Functional verification

The skill queries the FunctionGraph function list through KooCLI
(`hcloud functiongraph ListFunctions`), which maps to the official read-only
`GET /v2/{project_id}/fgs/functions`. Both execution paths were verified against
the environment:

1. **CLI path** — `hcloud functiongraph ListFunctions --cli-region=cn-north-4`
   returns `{"functions":[],"next_marker":0,"count":0}` in a region with no
   functions (valid JSON, exit 0), and the script renders that as
   `当前区域无函数`.
2. **SDK fallback path** — `huaweicloudsdkfunctiongraph` v2 `list_functions`
   initialized with `FunctionGraphRegion.value_of(region)` returns the same
   empty result (count 0) for the same region/account.
3. **Output modes** — table / `--json` / `--names-only` all exercised through
   the script's CLI entry (`python3 scripts/list_functiongraph.py`).
4. **Write-intent guard** — mutating intents (`CreateFunction`,
   `DeleteFunction`, `publish`, `invoke`, ...) are rejected before any command
   runs.

## Offline unit tests

```bash
cd skills/compute/functiongraph/huawei-cloud-functiongraph-list
python3 -m unittest discover -s tests -v
```

38 tests cover: the write-intent guard, command construction (no `--project_id`
emitted), JSON extraction, failure classification, sorting by name, marker
paging, the SDK credential whitelist (reads only exact-named AK/SK env vars,
never iterating the environment), SDK fallback (missing-deps and real call),
table/names/json rendering, and all `main()` output modes — all with a mocked
hcloud subprocess (no credentials, no network).

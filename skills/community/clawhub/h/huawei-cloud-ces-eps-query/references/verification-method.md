# Verification Method

## 1. Structural / specification compliance

```bash
bash scripts/validate-skill.sh -s skills/monitoring/huawei-cloud-ces-eps-query
```

Checks the 华为云Skill检查规范: frontmatter (name/description/tags), required
sections (Overview / Prerequisites / Workflow / Core Commands / Parameter
Confirmation / Reference Documents / KooCLI Command Format Standard), naming,
one-PR-one-skill scope, size limits (≤500 SKILL.md lines, ≤30 files, ≤40 MB),
extension allowlist and kebab-case references.

## 2. Offline unit tests (no credentials, no network)

```bash
cd skills/monitoring/huawei-cloud-ces-eps-query
python3 -m unittest discover -s tests -v
```

Coverage:

| Area | What is verified |
| ---- | ---------------- |
| Category registry | 12 categories = CES 7 + EPS 5; every category carries service / SDK method / request / REST path / result key; CES paths start `/v2/{project_id}/`, EPS paths `/v1.0/` |
| NL routing | Chinese + English phrases route to the right category; specific phrases win over the generic "企业项目"; unknown intents return `None` |
| Write-intent guard | Read queries pass; English/Chinese write verbs and operation names are blocked; separator variants blocked; `--query` text is scanned; ordinary flag values are stripped |
| Operation guard | Read operations accepted, write operations rejected, unknown categories rejected |
| CLI command | `hcloud <Service> <Operation> --cli-region=...` built correctly; region always present |
| Parsing | JSON extraction (plain / noisy / invalid); failure classification (USE_ERROR, missing credentials, 401/403) |
| Result extraction | SDK list / single / empty responses; nested `to_plain` conversion |
| SDK path | Missing-credentials error; success path invokes the correct SDK method with built request kwargs |
| Backend fallback | CLI success; CLI→SDK fallback when hcloud is absent; ConfigError when no backend is available; required-id validation |
| Rendering | Table rendering; empty-result message; JSON mode |
| Quality wrapper | CLI path wraps `hcloud` with `skill-quality-cli run --skill-name … --`; bare fallback when the CLI is missing or `SKILL_QUALITY_REPORT=0`; explicit `CES_EPS_HCLOUD_BIN` override bypasses it |
| Helper scripts | `ensure_env.py` dependency probing / mirror install / failure paths; `yaml-check-frontmatter.py` OK / ERR / NO_PYYAML paths |
| main() | `--list-categories`; guard block on write query; unknown-intent error; query routing; JSON output; error path |

## 3. Functional smoke (creator `test-cli-commands.sh`)

```bash
bash scripts/test-cli-commands.sh -s skills/monitoring/huawei-cloud-ces-eps-query -e cli
```

Reads `templates/test-vars.json`. In an environment with KooCLI + credentials,
the CLI cases execute live; without them the cases are skipped / reported, and
the own-script smoke cases (`bash -n ...`) still run.

## 4. Live execution (with credentials, out-of-band)

```bash
python3 scripts/ces_eps_query.py --list-categories
python3 scripts/ces_eps_query.py --category alarm-rules --region cn-north-4
python3 scripts/ces_eps_query.py --query "查询企业项目配额"
```

Confirm results against the Huawei Cloud console (CES → 告警 / 仪表盘 / 资源分组;
企业管理 → 企业项目).
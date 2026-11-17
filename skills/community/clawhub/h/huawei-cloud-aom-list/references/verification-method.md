# Verification Method

## 1. Structural / specification compliance

```bash
bash scripts/validate-skill.sh -s skills/monitoring/huawei-cloud-aom-list
```

Checks the 华为云Skill检查规范: frontmatter (name/description/tags), required
sections (Overview / Prerequisites / Workflow / Core Commands / Parameter
Confirmation / Reference Documents / KooCLI Command Format Standard), naming,
one-PR-one-skill scope, size limits (≤500 SKILL.md lines, ≤30 files, ≤40 MB),
extension allowlist and kebab-case references.

## 2. Offline unit tests (no credentials, no network)

```bash
cd skills/monitoring/huawei-cloud-aom-list
python3 -m unittest discover -s tests -v
```

Coverage:

| Area | What is verified |
| ---- | ---------------- |
| Category registry | 12 AOM categories; every category carries service / SDK method / request / REST path / result key / name field; all paths start `/v{N}/{project_id}/` |
| NL routing | Chinese + English phrases route to the right category; specific phrases (告警规则模板 / 仪表盘分组 / 指标告警规则) win over the generic ones; unknown intents return `None` |
| Write-intent guard | Read queries pass; English/Chinese write verbs and operation names are blocked; separator variants blocked; `--query` text is scanned; ordinary flag values are stripped |
| Operation guard | Read operations accepted, write operations rejected, unknown categories rejected |
| CLI command | `hcloud AOM <Operation> --cli-region=...` built correctly; region always present; operation PascalCase |
| Parsing | JSON extraction (plain / noisy / invalid); failure classification (USE_ERROR, missing credentials, 401/403) |
| Result extraction | SDK list / empty responses; nested `to_plain` conversion; raw CLI/REST payload unwrapping |
| SDK path | Missing-credentials error; success path invokes the correct SDK method with built request kwargs |
| Prometheus CLI-first | `prom-instances` defaults `enterprise_project_id` to `0` (explicit value wins); the natural-language query builds the CLI command with the header form `--Enterprise-Project-Id=0` (never snake_case `--enterprise_project_id`, which KooCLI rejects); the same mapping applies to every category declaring the Enterprise-Project-Id header (`alarm-rule-templates` / `metric-or-event-alarm-rules` / `dashboards` / `dashboard-folders` / `notification-templates`); an SDK `403` naming `aom:metric:list` / `AOM.0403` degrades to the read-only CLI path, while an unrelated auth error still propagates |
| Backend fallback | CLI success; CLI→SDK fallback when hcloud is absent; ConfigError when no backend is available |
| Rendering | Table with the name field first; empty-result message; JSON mode; `--names-only` |
| main() | `--list-categories`; guard block on write query; unknown-intent error; query routing; JSON output; error path |

## 3. Functional smoke (creator `test-cli-commands.sh`)

```bash
bash scripts/test-cli-commands.sh -s skills/monitoring/huawei-cloud-aom-list -e cli
```

Reads `templates/test-vars.json`. In an environment with KooCLI + credentials,
the CLI cases execute live; without them the cases are skipped / reported, and
the real read-only verification is left to the QA stage.

## 4. Live execution (with credentials, out-of-band)

```bash
python3 scripts/list_aom.py --list-categories
python3 scripts/list_aom.py --category prom-instances --region cn-north-4
python3 scripts/list_aom.py --query "查询告警规则" --names-only
```

Confirm results against the Huawei Cloud console (AOM → 告警管理 / 仪表盘 /
Prometheus 实例 / 通知模板 ...).
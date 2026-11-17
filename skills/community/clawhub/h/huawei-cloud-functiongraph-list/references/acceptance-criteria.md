# Acceptance Criteria

## Functional

- [ ] Lists the FunctionGraph functions of the current account / project /
      region (`--region`, default `cn-north-4`).
- [ ] Output is **sorted by function name** (func_name) in the default table and
      `--names-only` modes.
- [ ] Table shows 函数名称 / URN / 内存 (memory_size) / 超时 (timeout) / 入口
      (handler) / 运行时 (runtime) / 分组 (package) columns at minimum.
- [ ] `--json` emits the raw function array; `--names-only` emits names only.
- [ ] `--name` (func_name fuzzy) and `--package-name` (package_name) filters work.
- [ ] Marker paging traverses more than one page when `count` exceeds the page
      size, and stops correctly.
- [ ] Region is forwarded to KooCLI as `--cli-region`.

## Read-only / safety

- [ ] Only `ListFunctions` is ever executed; the write-intent guard rejects
      create / delete / update / publish / invoke / import / export / trigger
      vocabulary and non-`ListFunctions` operation names before any command.
- [ ] Credentials are never read, echoed, or stored by the script.

## Errors

- [ ] Empty region prints `当前区域无函数` and exits 0.
- [ ] Missing AK/SK prints an explicit configuration hint and exits 1.
- [ ] IAM 403 prints `无权限访问 FunctionGraph，请检查 IAM 权限` and exits 1.
- [ ] hcloud not installed: SDK fallback used; if the SDK is missing too, prints
      an install hint and exits 1.

## Quality

- [ ] Every concrete hcloud command in SKILL.md is wrapped with
      `skill-quality-cli run --skill-name huawei-cloud-functiongraph-list --`.
- [ ] `scripts/ensure_cli.sh` present and idempotent.
- [ ] Offline unit tests pass (`python3 -m unittest discover -s tests -v`).
- [ ] Skill passes `bash scripts/validate-skill.sh <skill-dir>`.

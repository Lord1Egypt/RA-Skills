# Acceptance Criteria

Issue: #173 — 新增 skill: 查询华为云 SSL 证书（SCM）列表
Skill: `skills/security/scm/huawei-cloud-scm-cert-list`

## Functional

- [ ] `python3 scripts/list_scm_certs.py --region cn-north-4` → compact list or
      `未找到 SSL 证书（区域: cn-north-4）。`, exit code 0
      (a 403 from the calling account is reported as a permission error with
      exit code 1, never as an empty list)
- [ ] `--table` prints exactly eight columns:
      `证书ID | 名称 | 域名 | 类型 | 状态 | 到期时间 | 剩余天数 | region`
- [ ] `--json` prints the raw merged response (`certificates` / `total_count` /
      `region`)
- [ ] `--content` is sent to the API and re-checked client-side
      (name / domain / SAN)
- [ ] `--expiring N` keeps only certificates whose remaining days ≤ N
      (client-side, expired certificates included)
- [ ] `--region` (default `cn-north-4`) is used for both `--cli-region` and the
      region column
- [ ] Automatic offset+limit paging collects the whole list; `--max-pages` caps it

## Safety / read-only

- [ ] `--action delete` (and create / update / import / push / ...) is rejected
      before any cloud call, exit code 1
- [ ] Only `ListCertificates` is ever constructed; no write API is implemented
- [ ] No files are written; credentials only via KooCLI profile or AK/SK env vars

## Error handling

- [ ] Empty list → actionable hint, exit 0
- [ ] 403 / `SCM.4002` → `scm:cert:list` hint, exit 1
- [ ] Missing credentials → profile / env-var hint, exit 1
- [ ] Network failure / timeout → network hint, exit 1
- [ ] `[USE_ERROR]` → parameter hint, exit 1
- [ ] No traceback on any failure path

## Quality

- [ ] Offline unit tests green (`python3 -m unittest discover -s tests -v`)
- [ ] `bash -n` / `python3 -m py_compile` / `python3 -m json.tool` pass
- [ ] `references/` complete: IAM policy, CLI installation guide, verification
      method, acceptance criteria (+ dataflow diagram)
- [ ] Directory structure follows the repository convention:
      `SKILL.md` + `scripts/` + `references/` + `templates/` + `tests/`
- [ ] SKILL.md ≤ 500 lines, ≤ 30 files, frontmatter name matches the directory
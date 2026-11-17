# Acceptance Criteria — huawei-cloud-asm-fuzzy-list

## Functional Criteria

- [ ] **AC-01**: The skill lists ASM meshes of the current tenant/project when
      asked to "list ASM" / "查询ASM列表".
- [ ] **AC-02**: The returned data includes the mesh **name** (`metadata.name`),
      `metadata.uid`, `status.phase` and `metadata.creation_timestamp`.
- [ ] **AC-03**: Fuzzy matching works: given a name keyword, only meshes whose
      name contains the keyword (case-insensitive substring) are returned.
- [ ] **AC-04**: When no keyword is provided, all meshes of the project are
      listed.
- [ ] **AC-05**: A keyword that matches nothing returns an empty result cleanly
      (no error), reported as `matched 0`.
- [ ] **AC-06**: The SDK (`huaweicloudsdkasm.v1`, `AsmClient`) imports and runs.
- [ ] **AC-07**: The region endpoint used matches the SDK `AsmRegion` definition
      (`cn-north-4` → `https://asm.cn-north-4.myhuaweicloud.com`).
- [ ] **AC-08**: No mutation operation is ever invoked (read-only guarantee —
      only `GET /v1/{project_id}/meshes` is used).
- [ ] **AC-09**: A region not enabled for the account yields a 403 error, and the
      skill guides the user to retry with another region.

## Security Criteria

- [ ] **SC-01**: No AK/SK hardcoded anywhere in the skill package.
- [ ] **SC-02**: Credentials come from environment variables, never from the
      conversation or file content.
- [ ] **SC-03**: Only the minimal mesh-list IAM action is documented.

## Quality Criteria

- [ ] **QC-01**: `SKILL.md` passes `validate-skill.sh` against 华为云Skill检查规范.
- [ ] **QC-02**: All files use allowed extensions (`.md`, `.json`, `.sh`).
- [ ] **QC-03**: Skill package size ≤ 40 MB, file count ≤ 30, SKILL.md ≤ 500 lines.
- [ ] **QC-04**: No hallucinated API paths — the endpoint comes from SDK
      `_http_info` (`GET /v1/{project_id}/meshes`).

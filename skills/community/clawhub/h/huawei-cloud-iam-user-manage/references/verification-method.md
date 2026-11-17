# Verification Method

## 1. Offline unit tests (no credentials, no network)

The functional logic is covered by offline unit tests using a duck-typed fake
backend that implements the same `call(operation, params)` contract as the CLI
and SDK backends:

```bash
cd skills/security/iam/huawei-cloud-iam-user-manage
python3 -m unittest discover -s tests -v
```

Coverage:

- input validation (user name, description, ids);
- `create-user` returning `user_id` / `user_name`;
- conflict-driven idempotency (existing user reused via 409);
- group / policy name-to-id resolution, including ambiguity and not-found;
- authorization composition (group membership + policy attachment);
- conflict tolerance on membership and attachment;
- CLI command construction and JSON parsing (including output that appends
  terminal-width diagnostics after the JSON payload, and surfacing of the
  embedded `error_code` / `error_msg` on API errors);
- SDK fallback (`SdkBackend`) import/construction: a regression guard asserts
  `IamRegion` is resolved from `huaweicloudsdkiam.v5.region.iam_region` (the v5
  top-level package does not export it), so `--executor sdk` does not crash with
  `ImportError`; these cases require `huaweicloudsdkiam` to be installed and are
  skipped otherwise;
- `--dry-run` planning is fully offline (no credentials, no backend) for both text
  and `--json` output, including `create-user` / `authorize` / `attach-policy`;
- `main()` exit codes for validation, confirmation and missing-credential paths.

## 2. Endpoint provenance

Every REST path used by the skill was read from the `huaweicloudsdkiam.v5`
client `_http_info` `resource_path` (no naming-based inference):

```
create_user_v5                 POST /v5/users
list_users_v5                  GET  /v5/users
show_user_v5                   GET  /v5/users/{user_id}
create_group_v5                POST /v5/groups
list_groups_v5                 GET  /v5/groups
add_user_to_group_v5           POST /v5/groups/{group_id}/add-user
attach_user_policy_v5          POST /v5/policies/{policy_id}/attach-user
list_policies_v5               GET  /v5/policies
list_attached_user_policies_v5 GET  /v5/users/{user_id}/attached-policies
```

Request-body fields (`name` / `description` / `enabled`, `group_name`, `user_id`)
come from the corresponding SDK model classes (`CreateUserReqBody`,
`CreateGroupReqBody`, `AddUserToGroupReqBody`, `AttachUserPolicyReqBody`).

## 3. In-session self-test

`scripts/test-cli-commands.sh` (creator) runs the cases in
`templates/test-vars.json`: read-only CLI calls and own-script syntax checks.
When no `hcloud` backend / credentials are present the smoke reports no executed
case (`live_skipped=true`); the real, credentialed read-only verification is
performed out-of-band by the QA stage.

## 4. What is intentionally not verified here

Real mutating calls (`CreateUserV5`, `AddUserToGroupV5`, `AttachUserPolicyV5`)
are **not** executed during skill development — they would create IAM users and
grant permissions in a live account. They are exercised only with the fake
backend; the QA stage performs the real, credentialed run under its own gate.
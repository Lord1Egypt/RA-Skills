# Acceptance Criteria

| # | Criterion | How it is met |
| - | --------- | ------------- |
| 1 | Create an IAM user and return its identifier | `create-user --name ... --confirm` returns `user_id` / `user_name` (`POST /v5/users`) |
| 2 | Authorize the user (group and/or policy) | `create-user ... --group-name/--policy-name`, `authorize`, `add-user-to-group`, `attach-policy` (`AddUserToGroupV5` / `AttachUserPolicyV5`) |
| 3 | Parameter validation | user name (1-64, first char not a digit), description (0-255, forbidden chars), ids (1-64); invalid input exits 2 with `参数校验失败` |
| 4 | Failure / error-code handling | unified `IamError` carries `error_code`; 401/403 and backend errors are reported with hints; 409 is treated as idempotent reuse |
| 5 | Executable CLI examples | `Core Commands` shows the script and the equivalent wrapped `hcloud IAM ...` calls |
| 6 | Executable SDK examples | `huaweicloudsdkiam` v5 client used by the SDK backend; verified REST paths documented |
| 7 | Idempotency | existing user/group reused; duplicate membership/attachment reported, not failed |
| 8 | Write safety | mutations require `--confirm`; `--dry-run` previews offline (text or `--json`), never touching a backend or credentials |
| 9 | Tests cover new functionality | `tests/test_iam_user_manage.py` (34 offline cases) |
| 10 | Existing tests still pass | the change only adds a new skill directory; no existing module is touched |

Out of scope (never performed): deleting/disabling users, deleting groups,
AK/SK rotation, password policy, MFA, agencies/delegation.
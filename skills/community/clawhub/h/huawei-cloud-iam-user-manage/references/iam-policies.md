# IAM Policies (least privilege — create user + authorize)

This skill invokes the IAM v5 identity operations below (both execution paths):

| Purpose | KooCLI | REST path | Mutating |
| ------- | ------ | --------- | -------- |
| Create user | `hcloud IAM CreateUserV5` | `POST /v5/users` | yes |
| List users | `hcloud IAM ListUsersV5` | `GET /v5/users` | no |
| Show user | `hcloud IAM ShowUserV5` | `GET /v5/users/{user_id}` | no |
| Create group | `hcloud IAM CreateGroupV5` | `POST /v5/groups` | yes |
| List groups | `hcloud IAM ListGroupsV5` | `GET /v5/groups` | no |
| Add user to group | `hcloud IAM AddUserToGroupV5` | `POST /v5/groups/{group_id}/add-user` | yes |
| Attach user policy | `hcloud IAM AttachUserPolicyV5` | `POST /v5/policies/{policy_id}/attach-user` | yes |
| List policies | `hcloud IAM ListPoliciesV5` | `GET /v5/policies` | no |

The skill never deletes or disables a user, never deletes a group, and never
touches AK/SK, password policy, MFA or agencies.

## Recommended approach

Prefer delegating authorization to an **existing user group** that already
carries the required system policies, so day-to-day callers only need the
create/membership actions below. Grant the caller identity only the actions it
actually performs.

## Custom least-privilege policy

If a custom policy is preferred, scope it to exactly the actions above. The
exact action strings MUST be confirmed against the official permission list
before use (see "Verify the action names" below) — the names below are the
authorization-item names and are **not** to be trusted as hand-typed literals.

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:users:create",
        "iam:users:list",
        "iam:users:get",
        "iam:groups:create",
        "iam:groups:list",
        "iam:groups:addUser",
        "iam:policies:list",
        "iam:policies:attachUser"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

## Verify the action names (mandatory before applying a custom policy)

```bash
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=iam
```

Copy the exact `name` / `urn_template` values from the response; do not
re-capitalize or normalize them. Alternatively, inspect a real system policy:

```bash
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM ListPoliciesV5 --cli-region=cn-north-4
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM GetPolicyVersionV5 --cli-region=cn-north-4 --policy_id=<policy_id>
```

IAM identity policies use `"Version": "5.0"`; use `"1.1"` only for legacy IAM v3
templates. Do not write an unverified version number.

## 401 / 403 troubleshooting

If the script reports an authentication or permission error:

1. Confirm the AK/SK belongs to an IAM user in the target account and that the
   hcloud profile uses those credentials.
2. Grant the create/authorize actions above (or delegate through a group).
3. Re-run `python3 scripts/iam_user_manage.py`.
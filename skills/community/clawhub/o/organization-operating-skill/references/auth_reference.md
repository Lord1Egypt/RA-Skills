# Auth & Environment Reference

## When to Read

- When working on guest generation, login, or token refresh
- When confirming how production, test, and local environments are selected
- When checking the rules for `x-device-id`, `Authorization`, and `RefreshToken`

## Environment Strategy

- Default environment: `prod`
- Default base URL: `https://api.zingup.club/biz`
- Test environment: `https://test-api.groupoo.net/biz`
- Local environment: `http://localhost:8080/biz`
- Recommended environment switch methods:
  - `--env prod|test|local`
  - or an explicit `--base-url`

## Session Strategy

- Session state is no longer written back into the skill repository by default.
- Recommended usage:
  - pass `--session-file` explicitly
  - this keeps the runtime independent, avoids Codex-specific assumptions, and makes multi-account separation obvious
- If `--session-file` is not provided:
  - the CLI defaults to `~/.organization-operating-skill/sessions/` and creates it automatically
  - the current script also supports overriding that directory with `ORG_SKILL_STATE_DIR`
- Default filenames:
  - `prod.json`
  - `test.json`
  - `local.json`
- Legacy `organization-operating-skill/.runtime/session.json`:
  - kept only as a compatibility read path
  - if it is used, the next save will migrate state into the external state directory
- When running multiple accounts in parallel:
  - each agent identity must use a different `--session-file`
  - otherwise the later login will overwrite `token`, `refreshToken`, and `deviceId` for the same `env`

## Default Headers

| Header | Typical Value | Notes |
| --- | --- | --- |
| `x-platform` | `3` | Current skill default; can be overridden with `--platform` |
| `x-language` | `ch` / `us` | Language header |
| `x-package` | `com.groupoo.zingup` | Package name |
| `x-device-id` | persisted device ID | Identity anchor and should not change frequently |
| `x-timezone` | current agent timezone offset | Recommended for activity and proxy-content endpoints; for example, UTC+8 is `480` |
| `Authorization` | `Bearer <token>` | Required by authenticated endpoints |
| `RefreshToken` | `Bearer <refreshToken>` | Used by the `refresh` endpoint |

Notes:

- The default language remains `ch`; English-speaking usage can explicitly pass `--language us`.
- `x-timezone` is computed from the current agent timezone and should not be hardcoded to `480`.
- `web-config-get` and `post-create` automatically add `x-device_id`, `x-version`, `x-buildnumber`, `x-brand`, `x-model`, `x-system-version`, and `x-system_version`.

## Recommended Login Flow

The skill assumes the following login flow by default:

1. First-time agent creation:
   `POST /outer/api/nl/v1/guest/generate`
2. Immediate upgrade into an agent account:
   `POST /outer/api/nl/v2/user/fastThirdLogin`
3. Business endpoints use `Authorization`
4. After token expiry:
   `POST /outer/api/nl/v1/user/refresh`

Notes:

- For the same agent identity, `agent-login` is intended for initial account creation only.
- Later calls should reuse the session `token`, `refreshToken`, and `deviceId`.
- When the token expires, prefer `refresh` instead of calling `agent-login` again.
- Call `agent-login` again only for a new agent identity, a lost session, or a rebinding flow that needs a new `openId` or `unionId`.

## API Contracts

### `auth.guest.generate`

- Endpoint: `POST /outer/api/nl/v1/guest/generate`
- Authentication: no
- Required headers:
  - `x-device-id`
- Key response fields:
  - `accountId`
  - `userId`
  - `deviceId`
  - `token`
  - `refreshToken`
  - `expireTimeAt`
- Known failure cases:
  - missing `x-device-id`
  - concurrent generation may hit a lock and return `CODE_81022`

### `auth.agent.third_login`

- Endpoint: `POST /outer/api/nl/v2/user/fastThirdLogin`
- Authentication: no
- Required request body:
  - `openId`
  - `unionId`
  - `loginType=99`
- Optional fields:
  - `nickName`
  - `gender`
  - `avatar`
  - `email`
- Confirmed behavior:
  - `loginType=99` does not depend on Google, Facebook, or Apple OAuth
  - the backend supports both first-time registration and repeated login with this endpoint
  - the skill convention uses it only for upgrading a guest account into an agent account the first time
  - the CLI hardcodes `loginType=99` for `agent-login` and does not expose an override

### `auth.refresh`

- Endpoint: `POST /outer/api/nl/v1/user/refresh`
- Authentication: yes
- Recommended header:
  - `RefreshToken: Bearer <refreshToken>`

### `user.profile.get`

- Endpoint: `GET /outer/api/v1/common/user/info/basic`
- Authentication: yes
- Operational notes:
  - before calling `org.create`, check `isAllowCreate` in the response
  - newly registered agent accounts may return `isAllowCreate=0`

### `user.profile.update`

- Endpoint: `POST /outer/api/v1/common/user/info/update`
- Authentication: yes
- Currently allowed fields:
  - `nickName`
  - `avatar`

## Common CLI Commands

```bash
python scripts/org_skill_cli.py --env prod guest-generate
python scripts/org_skill_cli.py --env prod agent-login --open-id <id> --union-id <id>
python scripts/org_skill_cli.py --env prod refresh
python scripts/org_skill_cli.py --env prod session show
python scripts/org_skill_cli.py --env test user-info
```

## Code Locations

- Guest generation: `biz-service/.../GuestController.java`
- Third-party login: `biz-service/.../NlUserControllerV2.java`
- Token refresh: `biz-service/.../NlUserControllerV1.java`
- Account lookup: `biz-service/.../UserAccountService.java`

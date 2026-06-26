# Auth Flows

Use this reference when the task involves `operately auth ...`, saved profiles, invite-based onboarding, or explaining how CLI authentication works.

This document is about the handcrafted auth commands in `cli/src/auth/`. Most other CLI commands are generated from backend `external_endpoints`; the auth flows are not.

## Contents

- When to use each auth command
- Shared auth behavior
- Login flows
- Signup flows
- Create-company flows
- Join flows
- Profile and verification commands
- Backend/internal endpoint map
- Agent rules

## When To Use Each Auth Command

Use these commands based on the task:

- `operately auth login --token <token>`: best for automation, CI, scripted work, or any headless task where the user already has a token.
- `operately auth login`: hybrid login for password, email code, or Google OAuth, plus prompted token entry when the user chooses it interactively.
- `operately auth signup`: hybrid account creation that can be fully interactive or mostly flag-driven, followed by create-company, join-with-invite, or stop-for-now.
- `operately auth create-company`: authenticate first, create a company, and save a full-access profile for an account that does not have one yet.
- `operately auth join`: interactive invite-based onboarding for an existing or newly activated account.
- `operately auth profiles`: inspect saved local CLI profiles and see which one is active.
- `operately auth whoami`: remote validation that the current token still works.
- `operately auth status`: local config check only.
- `operately auth logout`: remove the saved token from the selected profile.

## Shared Auth Behavior

### Base URL and profiles

- If no `--base-url` is provided, the CLI defaults to `https://app.operately.com`.
- If no `--profile` is provided for interactive auth, the CLI prompts for one with the current active profile (falling back to `default`) as the default; blank input accepts that default.
- For ordinary endpoint execution, auth resolution priority is: per-command flags > environment variables > saved profile.

### Saved profile result

Most successful auth flows end by saving:

- the final API token
- the base URL
- the resolved person name
- the company name

The profile metadata is fetched with external API calls after authentication succeeds.

### Important distinction: local vs remote checks

- `operately auth profiles` does not call the server. It prints saved local profiles, active-profile state, and saved metadata/base URLs.
- `operately auth status` does not call the server. It prints local profile/config state.
- `operately auth whoami` calls the API and is the correct post-login verification step.

### Bootstrap token model

Interactive login, signup, and join usually work in two phases:

1. The CLI gets a short-lived bootstrap token from an internal auth endpoint.
2. The CLI exchanges that bootstrap token for a reusable API token with `cli_auth/create_token`.

That final API token is company-scoped because it is minted for a specific company membership.

## Login Flows

## 1. Direct token login

Command:

```bash
operately auth login --token <token> [--base-url <url>] [--profile <name>]
```

Behavior:

- This bypasses the interactive bootstrap flow.
- The CLI validates the token by calling `people/get_me` (to verify the token and fetch the person's name) and `companies/get` (to fetch the company name for saved profile metadata).
- If validation succeeds, it saves the token into the selected profile.

Use this when:

- the user already has an API token
- the task is scripted or non-interactive
- browser-based OAuth is not practical

## 2. Hybrid login

Command:

```bash
operately auth login [--method <email-password|email-code|google>] [--email <email>] [--password <password>] [--company-id <id>] [--company-name <name>] [--access-mode <read-only|full-access>] [--base-url <url>] [--profile <name>]
```

This flow is hybrid:

- with no login flags, it behaves like the original fully interactive flow
- any provided login flag suppresses only that prompt
- missing values are still prompted interactively

Supported login methods for `--method`:

- `email-password` (accepted alias: `password`)
- `email-code` (accepted alias: `emailCode`)
- `google`

Unavoidable manual steps:

- Google login always requires browser confirmation
- Email-code login always requires manually entering the emailed verification code

All other login prompts can be skipped with flags.

Important validation rules:

- `--method google` cannot be combined with `--email` or `--password`
- `--method email-code` cannot be combined with `--password`
- `operately auth login --token <token>` cannot be combined with hybrid-only login flags such as `--method`, `--email`, `--password`, `--company-id`, `--company-name`, or `--access-mode`
- if both `--company-id` and `--company-name` are provided, `--company-id` wins
- `--company-name` must match exactly one authenticated company or the CLI exits with a flag error

Prompt suppression rules:

1. If `--method` is omitted, the CLI asks whether to use email/password, email code, Google OAuth, or a prompted API token.
2. If `--base-url` is omitted, the CLI prompts for it; blank input accepts `https://app.operately.com`.
3. If `--profile` is omitted, the CLI prompts for it with the current active profile (falling back to `default`) as the default.
4. If the chosen method is email/password and `--email` or `--password` is omitted, the CLI prompts only for the missing values.
5. If the chosen method is email-code and `--email` is omitted, the CLI prompts for it.
6. If multiple companies are returned and neither `--company-id` nor `--company-name` is provided, the CLI prompts for company selection.
7. If `--access-mode` is omitted, the CLI prompts for read-only vs full access.

### 2a. Email/password login

Flaggable inputs:

- `--email`
- `--password`
- `--company-id`
- `--company-name`
- `--access-mode`

Flow:

- Calls `cli_auth/auth_password`.
- If the backend returns companies, the CLI resolves the company in this order:
  1. `--company-id`
  2. exact `--company-name`
  3. auto-select if only one company is available
  4. interactive company picker
- The CLI resolves access mode from `--access-mode` or prompts for it.
- The CLI exchanges the bootstrap token for a final API token with `cli_auth/create_token`.

Special case:

- If the backend returns `status = no_companies`, the CLI does not save a profile and tells the user no companies were found.

### 2b. Email-code login

Flaggable inputs:

- `--email`
- `--company-id`
- `--company-name`
- `--access-mode`

Remaining manual prompt:

- verification code

Flow:

- Calls `cli_auth/request_email_code`.
- Prompts for the emailed verification code.
- Calls `cli_auth/auth_email_code`.
- Resolves company and access mode the same way as email/password login.
- Exchanges the bootstrap token for a final API token with `cli_auth/create_token`.

Special case:

- If the backend returns no companies, the CLI does not save a profile and tells the user no companies were found.

### 2c. Google login

Flaggable inputs:

- `--company-id`
- `--company-name`
- `--access-mode`

Remaining manual step:

- browser-based login confirmation

Flow:

- Calls `cli_auth/start_google`.
- Opens the returned login URL in a browser if possible.
- Polls `cli_auth/status` until the bootstrap session becomes:
  - `authenticated`
  - `failed`
  - `expired`
  - `no_companies`
- If authenticated with companies, the CLI resolves company and access mode using the same rules as the other hybrid login methods.
- The CLI then calls `cli_auth/create_token`.

Use this only when:

- a human is present
- a browser can be opened or the user can manually open the OAuth URL

### 2d. Prompted token login

Command path:

- still starts with `operately auth login`
- happens only when `--method` is omitted and the user chooses the `token` option interactively

Behavior:

- The CLI prompts for the API token.
- It validates the token directly against external endpoints, just like `operately auth login --token <token>`.
- No bootstrap token is involved.

## Signup Flows

Command:

```bash
operately auth signup [--method <email-password|google>] [--full-name <name>] [--email <email>] [--password <password>] [--next-step <create-company|join|later>] [--company-name <name>] [--invite-token <token>] [--base-url <url>] [--profile <name>]
```

This flow is hybrid:

- with no signup flags, it behaves like the original fully interactive flow
- any provided signup flag suppresses only that prompt
- missing values are still prompted interactively

Supported signup methods:

- `email-password` (accepted alias: `password`)
- `google`

Supported post-signup next steps:

- `create-company`
- `join` (accepted alias: `join-invite`)
- `later`

Unavoidable manual steps:

- Google signup always requires browser confirmation
- Email/password signup always requires manually entering the emailed verification code

All other signup prompts can be skipped with flags.

Important validation rules:

- `--method google` cannot be combined with `--full-name`, `--email`, or `--password`
- `--next-step later` cannot be combined with `--company-name` or `--invite-token`
- `--next-step create-company` cannot be combined with `--invite-token`
- `--next-step join` cannot be combined with `--company-name`

### Prompt suppression rules

- If `--base-url` is omitted, the CLI prompts for it and defaults blank input to `https://app.operately.com`.
- If `--method` is omitted, the CLI prompts for the signup method.
- If `--next-step` is omitted, the CLI prompts for the post-signup branch.
- If the chosen next step is `create-company` and `--company-name` is omitted, the CLI prompts for company name.
- If the chosen next step is `join` and `--invite-token` is omitted, the CLI prompts for the invite token.
- If the flow reaches token creation and `--profile` is omitted, the CLI prompts for the profile name.

### 1. Email/password signup

Flaggable inputs:

- `--full-name`
- `--email`
- `--password`

Remaining manual prompt:

- email verification code

Important detail:

- When `--password` is provided, the CLI skips the password-confirmation prompt entirely.

Flow:

- Calls `cli_auth/check_account` first.
- Calls `/create_email_activation_code`.
- Calls `cli_auth/signup`.
- Receives a bootstrap token on success.

### 2. Google signup

Flaggable inputs:

- `--method google`

Remaining manual step:

- browser-based Google confirmation

Flow:

- Starts the Google flow with `cli_auth/start_google_signup`.
- Polls `cli_auth/status` through the shared Google login flow.
- Receives a bootstrap token when authentication completes.

### 3. Post-signup: create company now

After signup, if the user chooses `create-company` or passes `--next-step create-company`:

- The CLI prompts for `company name` only when `--company-name` was not provided.
- It first calls `cli_auth/company_creation_status`.
- If the instance is not configured yet, it calls `cli_auth/setup_company`.
- Otherwise, it calls `cli_auth/create_company`.
- After the company is created, the CLI calls `cli_auth/create_token`.

Important detail:

- This path hardcodes `readOnly: false`, so the created token is full access.

### 4. Post-signup: join a company with an invite token

After signup, if the user chooses `join` or passes `--next-step join`:

- The CLI prompts for `invite token` only when `--invite-token` was not provided.
- It calls `cli_auth/join_with_invite` using the bootstrap token.
- It then calls `cli_auth/create_token`.

This path also hardcodes `readOnly: false`.

### 5. Post-signup: do this later

If the user chooses `later` or passes `--next-step later`:

- no profile is saved
- no final API token is created
- the CLI explicitly tells the user to use `operately auth create-company` later to create a company or `operately auth join` later to join one

Agents should expect this outcome and should not assume that a successful signup automatically leaves a usable CLI profile behind.

## Create-Company Flows

Command:

```bash
operately auth create-company [--method <email-password|email-code|google>] [--email <email>] [--password <password>] [--company-name <name>] [--base-url <url>] [--profile <name>]
```

This flow is hybrid:

- with no flags it is fully interactive
- any provided flag suppresses only that prompt
- missing values are still prompted interactively

This flow exists for an account that can authenticate but does not yet have a company-scoped CLI token to save.

Important command rule:

- `operately auth create-company` does not support `--token`.

Supported auth methods for `--method`:

- `email-password` (accepted alias: `password`)
- `email-code` (accepted alias: `emailCode`)
- `google`

Important validation rules:

- `--method google` cannot be combined with `--email` or `--password`
- `--method email-code` cannot be combined with `--password`

Prompt suppression rules:

1. If `--method` is omitted, the CLI asks for the sign-in method.
2. If `--base-url` is omitted, the CLI prompts for it; blank input accepts `https://app.operately.com`.
3. If the chosen method is email/password and `--email` or `--password` is omitted, the CLI prompts for only the missing values.
4. If the chosen method is email-code and `--email` is omitted, the CLI prompts for it.
5. If `--company-name` is omitted, the CLI prompts for it.
6. If `--profile` is omitted, the CLI prompts for it with the current active profile as the default.

Flow:

- The CLI resolves the method from `--method` or prompts for it.
- It resolves the base URL and checks `cli_auth/company_creation_status`.
- It authenticates with the chosen method to get a bootstrap token.
- It uses `--company-name` or prompts for it.
- It uses `cli_auth/setup_company` when the instance is not configured yet, otherwise `cli_auth/create_company`.
- It prompts for the profile name if needed (blank input accepts the current active profile as the default).
- It calls `cli_auth/create_token` and saves a full-access profile.

## Join Flows

Command:

```bash
operately auth join [--invite-token <token>] [--method <email-password|email-code|google>] [--email <email>] [--password <password>] [--company-id <id>] [--company-name <name>] [--base-url <url>] [--profile <name>]
```

This flow is hybrid:

- with no flags it is fully interactive
- any provided flag suppresses only that prompt
- missing values are still prompted interactively

This flow starts from an invite token and first inspects the invite type with a public query.

Important validation rules:

- `--method google` cannot be combined with `--email` or `--password`
- `--method email-code` cannot be combined with `--password`
- `--method email-code` is not available for first-time personal invites (`has_open_invitation = true`); passing it exits with code 2
- For personal invites, if `--email` is provided it must match the invited member's email exactly

Prompt suppression rules:

1. If `--invite-token` is omitted, the CLI prompts for the invite token.
2. If `--base-url` is omitted, the CLI prompts for it.
3. If `--method` is omitted, the CLI prompts for the sign-in method.
4. If the chosen method is email/password and `--email` or `--password` is omitted, the CLI prompts for only the missing values.
5. For first-time personal invite + password: if `--password` is provided, password confirmation is skipped (the same value is used for both password and confirmation).
6. If `--profile` is omitted, the CLI prompts for it.
7. For company-wide invites without a pre-known invited company: if neither `--company-id` nor `--company-name` is provided, the CLI prompts for company selection.

Company selection with flags:

- `--company-id` selects the company by exact ID match; errors if the ID is not in the authenticated companies list
- `--company-name` selects the company by exact name match; errors if ambiguous or not found
- For invites where the invited company is already known, `--company-id`/`--company-name` must match that company or the CLI errors

If `--invite-token` is provided, the initial invite-token prompt is skipped.

### Invite type detection

The CLI calls:

- `invitations/get_invite_link_by_token`

Then it routes differently for:

- personal invites
- company-wide invites

## 1. Personal invite flow

The CLI also fetches invitation details with:

- `invitations/get_invitation`

The available sign-in methods depend on the invitation state:

- first-time personal invite acceptance (`has_open_invitation = true`): password or Google OAuth
- existing-account personal invite login: password, email code, or Google OAuth

### 1a. Personal invite + password + first-time login

Prompts:

- password
- password confirmation

Flow:

- Calls `cli_auth/join_company`.
- Receives a bootstrap token.
- Calls `cli_auth/create_token` for the invited company.

### 1b. Personal invite + password + existing account

Prompts:

- email
- password

Flow:

- Reuses the normal password login flow.
- Passes `invite_token` into `cli_auth/auth_password`.
- The backend joins the company during auth.
- The CLI then calls `cli_auth/create_token` for the invited company.

### 1c. Personal invite + email code + existing account

Prompts:

- verification code

Flow:

- Reuses the normal email-code login flow.
- Uses the invitation member email from `invitations/get_invitation`, so the CLI does not prompt for email again.
- Passes `invite_token` into `cli_auth/auth_email_code`.
- The backend joins the company during auth.
- The CLI then calls `cli_auth/create_token` for the invited company.

### 1d. Personal invite + Google OAuth

Flow:

- Reuses the normal Google flow.
- Passes `invite_token` into `cli_auth/start_google`.
- Polls `cli_auth/status`.
- Calls `cli_auth/create_token` for the invited company.

## 2. Company-wide invite flow

The user chooses:

- password
- email code
- Google OAuth

### 2a. Company-wide invite + password

Flow:

- Reuses the password login flow with `invite_token`.
- The backend attaches the account to the invited company during auth.
- The CLI gets back companies from `cli_auth/auth_password`.
- If the invite metadata already includes the company, the CLI uses that company directly.
- Otherwise, it falls back to interactive company selection.
- The CLI then calls `cli_auth/create_token`.

### 2b. Company-wide invite + email code

Flow:

- Reuses the normal email-code login flow with `invite_token`.
- The CLI asks for email and verification code.
- The backend attaches the account to the invited company during auth.
- If the invite metadata already includes the company, the CLI uses that company directly.
- Otherwise, it falls back to interactive company selection.
- The CLI then calls `cli_auth/create_token`.

### 2c. Company-wide invite + Google OAuth

Flow:

- Reuses the Google flow with `invite_token`.
- Polls `cli_auth/status`.
- Uses the invited company when it is already known from the invite metadata.
- Otherwise, falls back to company selection.
- Calls `cli_auth/create_token`.

Important detail:

- Join flows also hardcode `readOnly: false`.
- They always try to create a full-access token for the joined company.

## Profile and Verification Commands

### `operately auth profiles`

Use this when you need to inspect local saved profiles without touching the server.

It shows:

- saved profile names
- which profile is active
- whether each profile has a saved token
- saved person/company metadata when available
- effective saved base URL

Do not treat `auth profiles` as proof that authentication works.

### `operately auth whoami`

Use this when you need to verify:

- the current token is valid
- the target instance is reachable
- the saved profile points at the expected base URL

This command performs remote API calls.

### `operately auth status`

Use this when you only need to inspect:

- active profile name
- whether a token is saved locally
- the base URL that would be used
- saved person name and company name (printed when present)

Do not treat `auth status` as proof that authentication works.

### `operately auth logout`

Behavior:

- clears the saved token from the selected profile
- also clears saved profile name/company metadata

It does not revoke the server-side API token.

## Backend/Internal Endpoint Map

Map of user-visible auth behavior to backend/internal calls:

- direct token login: external `people/get_me` and optional `companies/get` for metadata
- interactive password login: `cli_auth/auth_password` -> `cli_auth/create_token`
- interactive email-code login: `cli_auth/request_email_code` -> `cli_auth/auth_email_code` -> `cli_auth/create_token`
- interactive Google login: `cli_auth/start_google` -> repeated `cli_auth/status` -> `cli_auth/create_token`
- interactive token login: external `people/get_me` and optional `companies/get` for metadata
- email signup: `cli_auth/check_account` -> `/create_email_activation_code` -> `cli_auth/signup`
- Google signup: `cli_auth/start_google_signup` -> repeated `cli_auth/status`
- signup create-company path: `cli_auth/company_creation_status` -> `cli_auth/setup_company` or `cli_auth/create_company` -> `cli_auth/create_token`
- create-company command: `cli_auth/company_creation_status` -> auth flow (`cli_auth/auth_password` or `cli_auth/request_email_code` -> `cli_auth/auth_email_code` or `cli_auth/start_google` -> repeated `cli_auth/status`) -> `cli_auth/setup_company` or `cli_auth/create_company` -> `cli_auth/create_token`
- signup join-with-invite path: `cli_auth/join_with_invite` -> `cli_auth/create_token`
- personal invite first-time password join: `cli_auth/join_company` -> `cli_auth/create_token`
- personal/company invite email-code join: `cli_auth/request_email_code` -> `cli_auth/auth_email_code` -> `cli_auth/create_token`
- invite lookup before join routing: `invitations/get_invite_link_by_token`
- personal invite detail fetch: `invitations/get_invitation`

## Agent Rules

### Method prerequisites — confirm access BEFORE choosing a method

**Before choosing any auth method, the agent must confirm it has the required access. Never start a method that will reach an unavoidable blocker.**

| Method | What the agent must have BEFORE starting |
|---|---|
| `--token` / token login | The API token itself |
| `email-password` (login) | Both the email address AND the password |
| `email-password` (signup) | The email address AND access to the email inbox (a verification code is sent during signup) |
| `email-code` | The email address AND access to the email inbox (a code is sent and must be read) |
| `google` | Direct browser access so the OAuth confirmation step can be completed |

- **Google OAuth** is only usable when a human can open the browser and confirm. Never attempt it in headless, CI, or fully automated contexts.
- **Email code** (both login and signup) always sends a code to the inbox. The agent must be able to read that inbox to proceed. Do not start email-code auth without confirmed inbox access.
- **Email/password login** is fully automatable when both credentials are known. Do not attempt it if either value is missing or must be prompted interactively in an unattended context.
- **Email/password signup** sends an activation code to the provided email during the flow, so inbox access is still required even though the method is "password-based".

### Using --help

Run `operately auth <command> --help` (or equivalently `operately help auth <command>`) before executing any auth command when uncertain about available flags, accepted method aliases, or validation rules. The built-in help shows the full flag list, method aliases, unavoidable manual steps, and copy-paste examples.

```bash
operately auth login --help
operately auth signup --help
operately auth join --help
operately auth create-company --help
```

### Flag preferences

- Always pass known values as flags rather than relying on interactive prompts. Use `--method`, `--email`, `--password`, `--company-name`, `--invite-token`, `--profile`, etc. to suppress every prompt that can be suppressed.
- Only accept that a step will be interactive when it is unavoidable: browser confirmation for Google OAuth, and entering the emailed verification code for email-code flows.
- For first-time personal invite + password: pass `--password` to suppress the password confirmation prompt as well (the CLI reuses the same value for confirmation when `--password` is provided).

### Other rules

- Prefer `operately auth login --token <token>` when the user already has a token.
- Use `operately auth profiles` when you need to discover reusable saved profile names before running commands with `--profile`.
- Prefer environment variables over mutating saved profiles in CI or temporary scripts, unless the user explicitly wants a profile saved.
- Use `operately auth create-company` when the user can authenticate but has no company yet and wants a saved, full-access CLI profile.
- Interactive profile name prompts default blank input to the current active profile. They do not list all saved profile names; use `operately auth profiles` to discover those before choosing one.
- Do not assume signup saves a usable profile. If the user chooses "do this later", signup succeeds but no final token is created.
- After any auth flow that claims to have logged in, verify with `operately auth whoami`, not `operately auth profiles` or `operately auth status`.
- If the task is about the CLI auth architecture, remember that `operately auth ...` commands are custom flows; they are not generated from `external_endpoints`.

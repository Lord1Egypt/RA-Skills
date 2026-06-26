# Neura Relay OpenClaw Scenario Corpus

Use these scenarios as refs-only patterns for Action Cards and Decision Receipt interpretation. They are examples, not official OpenClaw or ClawHub claims.

## Scenario 1: Package Publish Or Version Release

Action family: `package_publish`

Required refs:

- package identity ref, for example `package_ref:@neurarelay/openclaw-preflight-adapter@0.1.1`
- source repo ref and source commit ref
- pack or artifact digest ref
- publisher authority ref
- changelog or release-intent ref
- no-official-claim boundary ref when the package is OpenClaw-style or ClawHub-facing

Receipt posture:

- `proceed`: publish only if publisher authority, source commit, artifact digest, and release intent are all present.
- `human_review`: use when package namespace, owner, or distribution channel differs from the canonical package.
- `revise`: add missing source, digest, release, or namespace refs.
- `stop`: block when package identity, owner, or artifact digest cannot be verified.

## Scenario 2: Publisher Namespace Or Organization Change

Action family: `publisher_namespace_change`

Required refs:

- desired publisher handle ref
- current account or organization ref
- authority holder ref
- open access request or maintainer-thread ref
- package ownership / namespace mapping ref
- public-claim boundary ref

Receipt posture:

- `proceed`: only for local/account setting changes that are authorized and reversible.
- `human_review`: use when the action changes public ownership, package namespace, or organization membership.
- `revise`: add missing authority holder, maintainer-thread, or namespace mapping refs.
- `stop`: block when the account identity or public ownership consequence is ambiguous.

## Scenario 3: External Message Send

Action family: `outbound_message`

Required refs:

- recipient or channel ref
- user intent ref
- draft ref without raw message body
- communication policy ref
- delegated authority ref

Receipt posture:

- `proceed`: send only after recipient, intent, and authority are clear.
- `human_review`: use for public, partner, legal, customer, or high-reputation messages.
- `revise`: add missing recipient, intent, policy, or approval refs.
- `stop`: block when the message would disclose private material or lacks authority.

## Scenario 4: Browser Submit Or Account Change

Action family: `browser_submit`

Required refs:

- page or form ref
- target account ref
- field-value refs without raw sensitive values
- user intent ref
- policy ref
- authority scope ref

Receipt posture:

- `proceed`: submit only if target account, intent, field refs, and authority are clear.
- `human_review`: use for purchases, account settings, billing, security, or irreversible submits.
- `revise`: add missing page, field, policy, or authority refs.
- `stop`: block when credentials, secrets, or private data would be exposed.

## Scenario 5: Customer Or Workspace Data Export

Action family: `data_export`

Required refs:

- data family ref
- export target ref
- privacy or legal basis ref
- operator intent ref
- retention and deletion posture refs
- authority scope ref

Receipt posture:

- `proceed`: export only when data scope, destination, legal basis, and authority are all clear.
- `human_review`: use for customer data, regulated data, or external destinations.
- `revise`: add missing privacy, target, evidence, or retention refs.
- `stop`: block when raw private data, secrets, or unauthorized customer material would leave the workspace.

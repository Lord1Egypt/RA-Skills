# OpenClaw

CLI platform: `openclaw`.

[Skills](https://docs.openclaw.ai/tools/skills) documents
`skills.entries.<key>.enabled`, optional `metadata.openclaw.skillKey`, gating
and allowlists. [Config CLI](https://docs.openclaw.ai/cli/config) is used for
writes, preserving native JSON5 handling. Filesystem fallback does not fully
parse JSON5, so unresolved state must remain unknown. A native batch can fail
after earlier commands succeed; the error reports completed commands and the
backup. Do not automatically retry an interrupted mutation.

## Operational notes

Use native configuration semantics; the CLI is required for writes. --allow-undiscovered is only for an explicitly requested literal host key, never typo correction.


Child CLI environment is allowlisted to PATH, OS home/temp/runtime paths, documented OpenClaw path/profile variables and OPENCLAW_CONFIG_PATH. Arbitrary provider tokens are not forwarded. Native CLIs run with current user permissions, not a sandbox.

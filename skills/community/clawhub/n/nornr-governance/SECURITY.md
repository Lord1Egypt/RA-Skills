# NORNR OpenClaw Skill Security Notes

## Dependency provenance

This skill is intentionally thin.

- Public MCP package repo: `https://github.com/NORNR/nornr-mcp-control`
- Local bridge: `nornr_governance.py`
- Delegated package: `nornr-agentpay` (import path: `agentpay`)
- Install source: `requirements.txt`
- Pinned PyPI package: `nornr-agentpay==0.1.0`

Review the pinned SDK revision before enabling this skill in autonomous or finance-sensitive workflows.

## Environment

Only this variable is required:

- `NORNR_API_KEY`

These are optional:

- `NORNR_BASE_URL` (optional, defaults to `https://nornr.com`)
- `NORNR_AGENT_ID` or a stored NORNR login profile

## Recommended API key scope

For the full skill command set:

- `payments:write`
- `workspace:read`
- `approvals:write`
- `events:read`
- `audit:read`

Add these if the skill should also run finance-close and export review flows:

- `reports:read`
- `webhooks:read`

Avoid broader workspace-admin or treasury scopes unless your OpenClaw workflow genuinely needs them.

## Review checklist

Before installation:

1. Review `requirements.txt` and the pinned `nornr-agentpay` release.
2. Review `nornr_governance.py` and confirm it only bridges into `agentpay.openclaw`.
3. Issue a dedicated NORNR API key for this skill instead of reusing a broader operator key.
4. Limit the key to the minimum scopes needed for your chosen command set.
5. Test the skill in a non-production workspace before enabling autonomous execution.

Before autonomous use:

1. Verify that queued or blocked results stop the OpenClaw action path.
2. Verify that approval-required actions route to an operator.
3. Verify that audit export and finance packet outputs match your expected review process.

# Token Failure Mode Decision Tree

Use after two independent clients (e.g., curl and Node) both fail with the same token (Step 7 of the main workflow).

## Decision tree

```
Both clients fail with 401?
├── Check GitHub security log for the token
│   ├── oauth_authorization.destroy event → manually deleted or revoked
│   ├── secret-scanning revocation → token was committed/exposed publicly
│   └── third-party credential revocation → an app/policy revoked it
├── Check token age and expiration policy
│   ├── Organization/enterprise policy enforced expiry → regenerate
│   └── Fine-grained PAT expired → regenerate with longer window
├── Check scope vs the failing endpoint
│   ├── Contents API write without repo scope → regenerate with correct scopes
│   └── Fine-grained PAT missing repository access → update resource access
└── Check account state
    ├── OAuth-app token limit reached → revoke unused tokens
    └── SAML/SSO authorization missing → re-authorize after SSO enforcement
```

## Evidence strength ranking

1. Live authenticated `GET /user` returning 200 (strongest runtime evidence)
2. GitHub security log events (authoritative for revocation cause)
3. Token settings page status (display state, not runtime state)
4. "Last used" label (weak, lagging, and coarse)

Rules:

- Never conclude from a single failed request in a single runtime.
- A `401` with an empty/unset environment variable is a local bug, not a token problem.
- If the token was exposed in logs or chat, rotate it regardless of whether it still works.

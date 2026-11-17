# Promarkia External API Contract v2

Read this reference only when verifying compatibility or implementing the Promarkia server.

## Capability discovery

`GET /api/external/capabilities?client=openclaw&contract=2` must return an authenticated JSON object. A 404 means the legacy contract.

Minimum declaration for submissions:

```json
{
  "contractVersion": 2,
  "authorization": {
    "manifestEnforced": true,
    "idempotencyBound": true,
    "requestDigestEnforced": true
  },
  "taskModes": {
    "draft-only": { "toolPolicyEnforced": true },
    "external-action": { "toolPolicyEnforced": true }
  },
  "externalActions": {
    "accountBindingRequired": true,
    "receiptRequired": true
  },
  "allowedSquads": ["9", "10", "11", "12", "16", "17", "18", "21"],
  "maxTimeoutSeconds": { "default": 1200, "10": 3600 }
}
```

The client treats missing or false safeguards as unsupported. Capability discovery may narrow the client allowlist but never widens it.

## Submission enforcement

`POST /api/external/tasks` receives:

- `Idempotency-Key`: the authorization UUID;
- `authorization`: the v2 manifest;
- `connectorBindings`: toolkit-to-account-ID map identical to the manifest;
- `prompt`: the human task wrapped in a visible authorization envelope; and
- `squadId` and `timeout` identical to the values bound into the request digest.

The server must:

1. Require the authorization UUID to equal the idempotency key.
2. Recompute and compare `requestSha256` from the original user task and all bound fields.
3. Reject changed replays, missing fields, unsupported squads/modes, and timeouts above the advertised limit.
4. Remove every write-capable tool for `draft-only`; prompt instructions are not a security boundary.
5. For `external-action`, require exactly the approved action, destination, audience, toolkit, and owned active account ID.
6. Resolve account ownership server-side and reject ambiguous, missing, inactive, or cross-tenant bindings.
7. Persist the accepted authorization with the run and return it from run retrieval.
8. Require an authoritative external-action receipt containing the actual account, action, provider object identifier or permalink, and terminal provider status.

## Connections and artifacts

`GET /api/external/connections` returns only safe metadata for owned active accounts: immutable ID, toolkit, user-defined name, preference state, and status. It never returns provider credentials.

`GET /api/runs/<run_id>/artifacts` remains read-only and tenant-scoped. The skill lists metadata only; it does not upload, delete, promote, or download artifacts.

## Billing and timeouts

Submission should return the reserved capacity and billing status. Terminal run retrieval should return final credit cost and any refund/settlement state.

The client assumes a 1,200-second maximum when capability discovery is unavailable. A higher Video limit is valid only when the server advertises it.


# Debugging Cookbook

Use this file when cases fail. The fastest path is to classify the failure first, then inspect the right layer.

## 1. Authentication Failure

Typical symptoms:

- HTTP `401` or `403`
- response contains a login page or `login_required`
- browser request succeeds but script request fails

Check in this order:

1. Is the host correct for the environment?
2. Did the cookie or token come from the same environment?
3. Is the full `Cookie:` header present, not a reconstructed subset?
4. Does the endpoint also require a CSRF or custom auth header?

Conclusion:

- If auth is wrong, treat it as a credential or request-header problem first, not a business logic failure.

## 2. Request Shape Failure

Typical symptoms:

- HTTP `400`
- validation error messages
- missing or malformed parameters

Check:

1. path parameter substitution
2. query parameters
3. `Content-Type`
4. request body structure
5. custom headers expected by the service

This category usually means the request was not shaped like the successful browser or curl request.

## 3. Environment or Data Mismatch

Typical symptoms:

- same request passes in one environment and fails in another
- target resource does not exist
- feature switch, region, time-window, or account state blocks the expected result

Check:

1. resource identifiers
2. user or account state
3. feature flags
4. environment-specific data setup

Not every `FAIL` means the endpoint is broken. Many failures come from missing setup.

## 4. Assertion Design Failure

Typical symptoms:

- HTTP `200` but the case still fails
- fields fluctuate between runs
- list contents are partially dynamic

Adjustments:

- assert key business fields instead of the whole payload
- switch from full equality to `exists` or `list_contains` when exact ordering is unstable
- keep one main business expectation per case when possible

## 5. Parsing or Script Failure

Typical symptoms:

- shell syntax errors
- variables not replaced
- parser cannot find the request line or a case boundary

Run in this order:

```bash
bash -n './<feature>.api-verify.sh'
bash './<feature>.api-verify.sh'
COOKIE='full Cookie header' AUTH_TOKEN='token value' bash './<feature>.api-verify.sh'
```

Interpretation:

- `bash -n` catches shell syntax issues.
- no-secret execution checks parsing and `SKIP` behavior.
- real-secret execution checks transport and assertions.

# Multi-Provider Example

Use this reference when the user needs separate login providers, separate issuers, or different auth behavior for different user groups.

## When This Variant Fits

Use this variant when:

- admins and end users authenticate against different providers
- multiple issuers can sign tokens for the same backend
- the frontend needs to select a provider based on route, tenant, or product area

## Frontend Example Shape

Keep provider definitions explicit:

```typescript
export const providers = {
  user: {
    authority: import.meta.env.VITE_USER_OIDC_AUTHORITY,
    clientId: import.meta.env.VITE_USER_OIDC_CLIENT_ID,
  },
  admin: {
    authority: import.meta.env.VITE_ADMIN_OIDC_AUTHORITY,
    clientId: import.meta.env.VITE_ADMIN_OIDC_CLIENT_ID,
  },
};
```

Persist which provider started the flow so the callback handler can resolve the correct config.

```typescript
sessionStorage.setItem('auth_provider', 'admin');
```

## Backend Direction

Do not guess the provider from random claims. Prefer issuer-based routing.

Typical options:

- separate security chains by route or host
- issuer-based JWT decoder resolution
- explicit provider registry keyed by issuer

## Example Provider Registry Shape

```java
public record ProviderConfig(String issuer, String audience, String name) {}
```

Use a registry keyed by issuer and resolve the validation strategy from the token's issuer after parsing only the minimum untrusted header or claims needed for routing.

## Notes

- Keep callback URLs and logout behavior provider-aware.
- Avoid merging admin and user scopes into one generic config.
- Verify each provider's issuer, audience, and role mapping independently.
- Be explicit about which routes accept which issuer.
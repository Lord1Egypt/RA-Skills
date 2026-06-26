# React SPA Example

Use this reference when the user needs a concrete browser-based OIDC example for React or TypeScript.

## When This Variant Fits

Use this variant when:

- the frontend is a single-page app
- the app talks directly to APIs using bearer tokens
- the client is public
- PKCE is required

Prefer `oidc-client-ts` or `react-oidc-context` if the repo does not already have an auth abstraction.

## Minimal Config

```typescript
export const oidcConfig = {
  authority: import.meta.env.VITE_OIDC_AUTHORITY,
  clientId: import.meta.env.VITE_OIDC_CLIENT_ID,
  redirectUri: `${window.location.origin}/auth/callback`,
  scope: 'openid profile email',
  responseType: 'code',
};
```

Add `offline_access` only if refresh tokens are truly needed.

## Example Auth Provider Shape

```typescript
import { AuthProvider } from 'react-oidc-context';

export function AppAuthProvider({ children }: { children: React.ReactNode }) {
  return <AuthProvider {...oidcConfig}>{children}</AuthProvider>;
}
```

If the project already has its own provider or state layer, adapt the existing abstraction instead of wrapping the app twice.

## Example Protected Route

```typescript
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from 'react-oidc-context';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  const location = useLocation();

  if (auth.isLoading) {
    return <div>Loading...</div>;
  }

  if (!auth.isAuthenticated) {
    sessionStorage.setItem('auth_return_url', location.pathname + location.search);
    auth.signinRedirect();
    return null;
  }

  return <>{children}</>;
}
```

## Example API Call

```typescript
export async function apiFetch(auth: { user?: { access_token?: string } }, input: string) {
  return fetch(input, {
    headers: auth.user?.access_token
      ? { Authorization: `Bearer ${auth.user.access_token}` }
      : undefined,
  });
}
```

## Notes

- Prefer metadata discovery over hardcoded `/authorize`, `/token`, or JWKS URLs.
- If refresh tokens are used in the browser, mention the storage and XSS tradeoff explicitly.
- Preserve the original return URL through login and callback.
- Handle provider error query parameters on the callback route.
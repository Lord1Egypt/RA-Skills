# Deployment

## Independent Deploy — CI/CD per Sub-App

```yaml
# .github/workflows/deploy-app-orders.yml
on:
  push:
    paths: ['apps/app-orders/**']   # only trigger on changes to this sub-app

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd apps/app-orders && npm ci && npm run build
      - name: Upload to CDN
        run: aws s3 sync dist/ s3://my-mfe-cdn/app-orders/${{ github.sha }}/
      - name: Update manifest
        run: |
          curl -X PATCH https://api.example.com/manifest \
            -d '{"app-orders": "${{ github.sha }}"}'
```

## Dynamic Remote Entry (Runtime Version Resolution)

```js
// shell/src/remoteLoader.js — fetch active versions from manifest API
async function getRemoteUrl(appName) {
  const manifest = await fetch('/api/mfe-manifest').then(r => r.json());
  const hash = manifest[appName]; // e.g. "a1b2c3d"
  return `https://cdn.example.com/${appName}/${hash}/remoteEntry.js`;
}

// Then load dynamically (see module-federation.md loadRemote)
const url = await getRemoteUrl('appOrders');
const { default: OrderList } = await loadRemote('appOrders', './OrderList', url);
```

## Manifest File Strategy

```json
// /api/mfe-manifest (served by main app or CDN)
{
  "app-orders":   "a1b2c3d4",
  "app-user":     "e5f6g7h8",
  "app-dashboard": "i9j0k1l2",
  "updatedAt":    "2024-01-15T10:00:00Z"
}
```

## Versioning Strategy

| Approach | Pros | Cons |
|----------|------|------|
| Git SHA per deploy | Exact traceability | Long URLs |
| Semver tag | Human-readable | Manual tagging |
| `latest` alias (CDN) | Simple | Risky, cache issues |

Recommended: **Git SHA** in CDN path + **`latest` symlink** for fast fallback.

## Canary / Gray Release

```js
// Serve different versions to % of users based on cookie or user segment
function getRemoteVersion(appName, userId) {
  const isCanary = hash(userId) % 100 < 10; // 10% canary
  return isCanary
    ? `https://cdn.example.com/${appName}/canary/remoteEntry.js`
    : `https://cdn.example.com/${appName}/stable/remoteEntry.js`;
}
```

## Rollback

```bash
# Rollback = update manifest to point to previous SHA
curl -X PATCH https://api.example.com/manifest \
  -d '{"app-orders": "<previous-sha>"}'
# No redeploy needed — clients pick up new manifest on next load
```

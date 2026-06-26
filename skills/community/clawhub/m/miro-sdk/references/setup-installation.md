# Miro Web SDK - Setup & Installation

## Prerequisites

- Node.js 14+ and npm/yarn
- A Miro account
- A Developer team (sandbox environment)
- Basic TypeScript/JavaScript knowledge

## Step 1: Create Developer Team

**Purpose:** Isolated sandbox for testing without affecting production boards

1. Go to https://miro.com/app/settings/user-profile
2. Click "Create Developer team"
3. Name it (e.g., "My Plugin Dev")
4. You're now in sandbox mode

**Limitations:**
- 3 boards maximum
- 5 collaborators maximum
- "Developer team" watermark on boards

## Step 2: Create App

1. Visit https://miro.com/app/settings/user-profile/apps
2. Click "Create new app"
3. Select "Web plugin"
4. Name your app
5. Accept terms and create

**You'll get:**
- App ID
- Redirect URI
- Scopes configuration

## Step 3: Install SDK CLI

```bash
npm create @mirohq/websdk-cli my-plugin
cd my-plugin
npm install
```

**What gets created:**
- `manifest.json` - App metadata
- `src/index.ts` - Main plugin code
- `src/panel.html` - UI panel
- `package.json` - Dependencies
- `tsconfig.json` - TypeScript config

## Step 4: Configure App

**manifest.json:**
```json
{
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "minWallOrigin": "localhost:3000",
  "appUrl": "http://localhost:3000/index.html",
  "requiredScopes": [
    "board:read",
    "board:write",
    "identity:read"
  ],
  "sdkVersion": ">=2.0.0"
}
```

**Key Settings:**
- `name` - Display name
- `appUrl` - Entry point for plugin
- `requiredScopes` - Permissions needed
- `minWallOrigin` - Trusted origins (dev: localhost)

## Step 5: Start Development Server

```bash
npm start
```

**Output:**
```
Webpack 5.x.x compiled with X warning(s)
Plugin started at http://localhost:3000
```

Visit http://localhost:3000 in browser to test.

## Step 6: Install in Miro

1. Open Miro app
2. Go to "Settings" → "Apps & integrations"
3. Click "Install app from URL"
4. Paste: `http://localhost:3000`
5. Click Install

**In Developer team only** - won't install in production teams yet.

## Directory Structure

```
my-plugin/
├── src/
│   ├── index.ts              # Main plugin entry
│   ├── index.html            # HTML template
│   ├── panel.ts              # Side panel logic
│   ├── panel.html            # Panel UI
│   └── styles.css            # CSS styles
├── public/
│   └── (static assets)
├── dist/
│   └── (built files)
├── manifest.json             # Plugin config
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
└── webpack.config.js         # Build config
```

## Building for Production

```bash
npm run build
```

**Creates:**
- `dist/index.html` - Bundled plugin
- Ready to deploy to web server

**Configuration:**
```json
{
  "appUrl": "https://my-plugin.example.com"
}
```

## Deploying Plugin

### Option 1: Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

**Updates manifest:**
```json
{
  "appUrl": "https://my-plugin.vercel.app"
}
```

### Option 2: GitHub Pages

```bash
npm run build
# Push dist/ to GitHub Pages
```

### Option 3: Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Option 4: AWS S3 + CloudFront

```bash
npm run build
aws s3 sync dist/ s3://my-bucket/
```

## Installing in Production

Once tested in Developer team:

1. Update `manifest.json` with production URL
2. Submit to Miro Marketplace (optional)
3. Or distribute app URL directly

**Direct Distribution:**
```
https://miro.com/app/install-app/?install_source=custom_direct_install
```

## Environment Variables

**Development (.env.local):**
```
VITE_APP_ID=your-app-id
VITE_MIRO_VERSION=2.0.0
DEBUG=true
```

**Production (.env.production):**
```
VITE_APP_ID=your-app-id
VITE_MIRO_VERSION=2.0.0
DEBUG=false
API_URL=https://api.example.com
```

**Usage in Code:**
```typescript
const appId = import.meta.env.VITE_APP_ID;
const isDebug = import.meta.env.DEBUG === 'true';
```

## SDK Versions

| Version | Status | Node | Features |
|---------|--------|------|----------|
| 2.x | Current | 14+ | Latest features, types |
| 1.x | Legacy | 12+ | Deprecated, use 2.x |

**Upgrade from 1.x to 2.x:**
```bash
npm update @mirohq/miro-webplugin@2
```

## Troubleshooting

### "Plugin not loading"
- Check `localhost:3000` is accessible
- Verify manifest.json syntax
- Check browser console for errors

### "CORS errors"
- Add domain to `minWallOrigin`
- Enable CORS on API endpoints
- Check redirect URLs

### "Scopes not working"
- Verify scopes in manifest.json
- User must accept scope permissions
- Try uninstalling and reinstalling app

### "Build fails"
```bash
# Clear cache
rm -rf node_modules dist
npm install
npm run build
```

## Next Steps

1. Follow tutorials in references
2. Build your first shape
3. Add event listeners
4. Create UI panel
5. Test with multiple users
6. Deploy to production


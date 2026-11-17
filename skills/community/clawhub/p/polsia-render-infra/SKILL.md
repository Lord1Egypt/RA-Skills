---
name: render-infra
description: "Apply Render-specific deployment requirements for Polsia apps, including /health checks and migration strategy."
---

# Render Infrastructure

Polsia apps deploy to Render. This skill covers platform-specific requirements.

## Health Check Endpoint (CRITICAL)

Render services are configured with a health check at /health. Your app MUST have this:

app.get('/health', (req, res) => { res.status(200).json({ status: 'ok' }); });

Requirements: Endpoint MUST be at /health (not /api/health). Must respond with HTTP 200. If health check fails, deploy times out after 15 minutes.

## DATABASE_URL Not Available in Build

Render's buildCommand does NOT have access to DATABASE_URL. Run migrations on server startup, not in buildCommand.

NEVER run migrations in Render's buildCommand - it will fail.

## Package.json Rules (CRITICAL)

Required scripts: build and start. If no frontend: "build": "echo 'No build step required'". NEVER remove the build script - deploys will fail.

With frontend: "build": "cd client && npm install --include=dev && npm run build". Use --include=dev because vite/tailwind are devDependencies.

## Filesystem is Ephemeral

Render's filesystem resets on every deploy. NEVER use multer.diskStorage() - files will be LOST. Use R2 proxy for file storage.

## Frontend Build

Create frontend in client/ subdirectory. Serve built files: app.use(express.static('client/dist'));

#!/bin/bash
# scaffold.sh — Vite + Three.js + GSAP + Lenis project scaffolder
# Usage: bash ~/.catpaw/skills/vibe-web-replica/scripts/scaffold.sh my-project
set -e

PROJECT_NAME="${1:-vibe-project}"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "✦ Vibe Web Replica — Scaffolding: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME/src"
cd "$PROJECT_NAME"

# ── package.json ──────────────────────────────
cat > package.json << 'PKG'
{
  "name": "vibe-web-replica",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "gsap": "3.12.7",
    "lenis": "^1.1.20",
    "three": "^0.169.0"
  },
  "devDependencies": {
    "vite": "^6.0.0"
  }
}
PKG

# ── vite.config.js ─────────────────────────────
cat > vite.config.js << 'VITE'
import { defineConfig } from 'vite';

export default defineConfig({
  server: { port: 5173, open: true },
  build: {
    target: 'esnext',
    rollupOptions: {
      output: {
        manualChunks: {
          three: ['three'],
          gsap: ['gsap']
        }
      }
    }
  }
});
VITE

# ── index.html (from template) ────────────────
cp "$SCRIPT_DIR/templates/index.html" ./index.html

# ── src/ files (from templates) ────────────────
cp "$SCRIPT_DIR/templates/three-scene.js" ./src/three-scene.js
cp "$SCRIPT_DIR/templates/gsap-scroll.js" ./src/gsap-scroll.js
cp "$SCRIPT_DIR/templates/lenis-setup.js" ./src/lenis-setup.js
cp "$SCRIPT_DIR/templates/main.js" ./src/main.js

# ── public/ for static assets ──────────────────
mkdir -p public

# ── .gitignore ────────────────────────────────
cat > .gitignore << 'GIT'
node_modules/
dist/
.env
GIT

echo ""
echo "✅ Scaffolded! Next steps:"
echo "   cd $PROJECT_NAME"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "   → http://localhost:5173"

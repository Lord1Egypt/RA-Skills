#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-dir>"
  exit 1
fi

PROJECT_DIR="$1"
mkdir -p "$PROJECT_DIR/src/commands"

cat > "$PROJECT_DIR/package.json" <<'EOF'
{
  "name": "bun-discord-bot",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "bun run src/index.ts",
    "register": "bun run src/register-commands.ts"
  },
  "dependencies": {
    "discord.js": "^14.21.0",
    "dotenv": "^16.6.1"
  }
}
EOF

cat > "$PROJECT_DIR/tsconfig.json" <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"]
}
EOF

cat > "$PROJECT_DIR/.env.example" <<'EOF'
DISCORD_TOKEN=replace-me
CLIENT_ID=replace-me
GUILD_ID=replace-me
EOF

echo "Bun discord.js scaffold created in $PROJECT_DIR"

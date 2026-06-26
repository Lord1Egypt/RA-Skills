#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-dir>"
  exit 1
fi

PROJECT_DIR="$1"
mkdir -p "$PROJECT_DIR/src/commands" "$PROJECT_DIR/src/events"

cat > "$PROJECT_DIR/package.json" <<'EOF'
{
  "name": "discord-bot",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "dev": "tsx src/index.ts",
    "start": "node dist/index.js",
    "register": "tsx src/register-commands.ts"
  },
  "dependencies": {
    "discord.js": "^14.21.0",
    "dotenv": "^16.6.1"
  },
  "devDependencies": {
    "tsx": "^4.20.5",
    "typescript": "^5.9.2",
    "@types/node": "^24.3.0"
  }
}
EOF

cat > "$PROJECT_DIR/tsconfig.json" <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
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

cat > "$PROJECT_DIR/src/index.ts" <<'EOF'
import 'dotenv/config';
import { Client, Collection, Events, GatewayIntentBits } from 'discord.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const client = new Client({ intents: [GatewayIntentBits.Guilds] }) as Client & {
  commands: Collection<string, any>;
};
client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
for (const file of fs.readdirSync(commandsPath).filter((f) => f.endsWith('.ts') || f.endsWith('.js'))) {
  const mod = await import(path.join(commandsPath, file));
  const command = mod.default;
  client.commands.set(command.data.name, command);
}

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Online as ${readyClient.user.tag}`);
});

client.on(Events.InteractionCreate, async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  const command = client.commands.get(interaction.commandName);
  if (!command) return;
  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    if (interaction.deferred || interaction.replied) {
      await interaction.followUp({ content: 'Command failed.', ephemeral: true });
    } else {
      await interaction.reply({ content: 'Command failed.', ephemeral: true });
    }
  }
});

await client.login(process.env.DISCORD_TOKEN);
EOF

cat > "$PROJECT_DIR/src/commands/ping.ts" <<'EOF'
import { SlashCommandBuilder } from 'discord.js';

export default {
  data: new SlashCommandBuilder().setName('ping').setDescription('Check bot latency'),
  async execute(interaction: any) {
    await interaction.reply({ content: 'Pong.' });
  }
};
EOF

cat > "$PROJECT_DIR/src/register-commands.ts" <<'EOF'
import 'dotenv/config';
import { REST, Routes } from 'discord.js';
import ping from './commands/ping.js';

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN!);

await rest.put(
  Routes.applicationGuildCommands(process.env.CLIENT_ID!, process.env.GUILD_ID!),
  { body: [ping.data.toJSON()] }
);

console.log('Registered guild commands.');
EOF

echo "Scaffolded discord.js TypeScript bot in $PROJECT_DIR"

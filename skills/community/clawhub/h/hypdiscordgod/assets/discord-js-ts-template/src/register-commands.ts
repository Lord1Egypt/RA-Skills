import 'dotenv/config';
import { REST, Routes } from 'discord.js';
import ping from './commands/ping.js';

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN!);

await rest.put(
  Routes.applicationGuildCommands(process.env.CLIENT_ID!, process.env.GUILD_ID!),
  { body: [ping.data.toJSON()] }
);

console.log('Registered guild commands.');

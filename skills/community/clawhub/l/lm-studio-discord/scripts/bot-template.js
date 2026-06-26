import { Client, GatewayIntentBits } from 'discord.js';
import axios from 'axios';

// ============ CONFIG ============
const DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE';
const LM_STUDIO_URL = 'http://127.0.0.1:1234/v1/chat/completions';
const MODEL = 'qwen2-0.5b-instruct';
const GUILD_ID = 'YOUR_DISCORD_SERVER_ID_HERE';
// ============ CONFIG ============

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once('ready', () => {
  console.log(`Bot logged in as ${client.user.tag}`);
  console.log(`Watching guild: ${GUILD_ID}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  if (message.guildId !== GUILD_ID) return;

  const userMessage = message.content.trim();
  if (!userMessage) return;

  console.log(`[Bot] Received: "${userMessage}" from ${message.author.tag}`);

  try {
    const response = await axios.post(
      LM_STUDIO_URL,
      {
        model: MODEL,
        messages: [{ role: 'user', content: userMessage }],
        max_tokens: 512,
        stream: false,
      },
      {
        timeout: 60000,
        headers: { 'Content-Type': 'application/json' },
      }
    );

    const botReply = response.data.choices[0].message.content.trim();
    console.log(`[Bot] Reply: "${botReply}"`);
    await message.reply(botReply);
  } catch (error) {
    console.error('[Bot] Error:', error.message);
    await message.reply(`Oops: ${error.message}`);
  }
});

client.login(DISCORD_TOKEN);

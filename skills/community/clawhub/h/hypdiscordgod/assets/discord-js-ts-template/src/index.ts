import 'dotenv/config';
import { Client, Collection, Events, GatewayIntentBits } from 'discord.js';
import ping from './commands/ping.js';

const client = new Client({ intents: [GatewayIntentBits.Guilds] }) as Client & {
  commands: Collection<string, any>;
};

client.commands = new Collection();
client.commands.set(ping.data.name, ping);

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

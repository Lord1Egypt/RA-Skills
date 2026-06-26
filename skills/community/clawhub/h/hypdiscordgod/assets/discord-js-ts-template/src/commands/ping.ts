import { SlashCommandBuilder } from 'discord.js';

export default {
  data: new SlashCommandBuilder().setName('ping').setDescription('Check bot latency'),
  async execute(interaction: any) {
    await interaction.reply({ content: 'Pong.' });
  }
};

import { ActionRowBuilder, ButtonBuilder, ButtonStyle, PermissionFlagsBits, SlashCommandBuilder } from 'discord.js';

export default {
  data: new SlashCommandBuilder()
    .setName('setup-tickets')
    .setDescription('Post the ticket opener panel')
    .setDefaultMemberPermissions(PermissionFlagsBits.ManageGuild),
  async execute(interaction: any) {
    const row = new ActionRowBuilder<ButtonBuilder>().addComponents(
      new ButtonBuilder()
        .setCustomId('ticket:create')
        .setLabel('Open Ticket')
        .setStyle(ButtonStyle.Primary)
    );

    await interaction.reply({
      content: 'Ticket panel deployed.',
      ephemeral: true
    });

    await interaction.channel?.send({
      content: 'Need help? Press the button below to open a ticket.',
      components: [row]
    });
  }
};

import 'dotenv/config';
import {
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  ChannelType,
  Client,
  Collection,
  Events,
  GatewayIntentBits,
  OverwriteType,
  PermissionFlagsBits,
  TextChannel
} from 'discord.js';
import fs from 'node:fs';
import path from 'node:path';
import ping from './commands/ping.js';
import setupTickets from './commands/setup-tickets.js';
import { db } from './db.js';
import { renderTranscript } from './transcript.js';

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] }) as Client & {
  commands: Collection<string, any>;
};

client.commands = new Collection();
for (const command of [ping, setupTickets]) {
  client.commands.set(command.data.name, command);
}

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Online as ${readyClient.user.tag}`);
});

function isStaff(interaction: any): boolean {
  return Boolean(interaction.member?.roles?.cache?.has(process.env.STAFF_ROLE_ID!));
}

async function buildTicketControls(channelId: string, claimedByUserId?: string | null, status: 'open' | 'closed' = 'open') {
  const row = new ActionRowBuilder<ButtonBuilder>().addComponents(
    new ButtonBuilder().setCustomId(`ticket:claim:${channelId}`).setLabel(claimedByUserId ? 'Claimed' : 'Claim Ticket').setStyle(ButtonStyle.Secondary).setDisabled(Boolean(claimedByUserId) || status !== 'open'),
    new ButtonBuilder().setCustomId(`ticket:reopen:${channelId}`).setLabel('Reopen Ticket').setStyle(ButtonStyle.Success).setDisabled(status === 'open'),
    new ButtonBuilder().setCustomId(`ticket:close:${channelId}`).setLabel('Close Ticket').setStyle(ButtonStyle.Danger).setDisabled(status !== 'open')
  );
  return [row];
}

async function exportTranscript(channel: TextChannel) {
  const messages = await channel.messages.fetch({ limit: 100 });
  const ordered = [...messages.values()].sort((a, b) => a.createdTimestamp - b.createdTimestamp);
  const transcript = renderTranscript(
    ordered.map((msg) => ({
      authorTag: msg.author.tag,
      createdAt: new Date(msg.createdTimestamp).toISOString(),
      content: [msg.content || '[no text content]', ...msg.attachments.map((a) => `[attachment] ${a.url}`)].join(' ')
    }))
  );

  const dir = path.resolve('transcripts');
  fs.mkdirSync(dir, { recursive: true });
  const filePath = path.join(dir, `${channel.id}.txt`);
  fs.writeFileSync(filePath, transcript || '[empty transcript]\n', 'utf8');
  return filePath;
}

async function syncTicketPanel(channel: TextChannel, channelId: string) {
  const ticket = db.prepare('SELECT claimed_by_user_id, status FROM tickets WHERE channel_id = ?').get(channelId) as { claimed_by_user_id?: string | null; status?: 'open' | 'closed' } | undefined;
  const components = await buildTicketControls(channelId, ticket?.claimed_by_user_id || null, ticket?.status || 'open');
  await channel.send({ content: ticket?.status === 'closed' ? 'Ticket archived. Staff can reopen it.' : 'Ticket active.', components });
}

client.on(Events.InteractionCreate, async (interaction) => {
  if (interaction.isChatInputCommand()) {
    const command = client.commands.get(interaction.commandName);
    if (!command) return;
    await command.execute(interaction);
    return;
  }

  if (!interaction.isButton()) return;

  if (interaction.customId === 'ticket:create') {
    const guild = interaction.guild;
    if (!guild) {
      await interaction.reply({ content: 'Guild only.', ephemeral: true });
      return;
    }

    const existing = db.prepare('SELECT channel_id FROM tickets WHERE guild_id = ? AND creator_user_id = ? AND status = ?').get(guild.id, interaction.user.id, 'open') as { channel_id: string } | undefined;
    if (existing) {
      await interaction.reply({ content: `You already have an open ticket: <#${existing.channel_id}>`, ephemeral: true });
      return;
    }

    const channel = await guild.channels.create({
      name: `ticket-${interaction.user.username}`,
      type: ChannelType.GuildText,
      parent: process.env.TICKET_CATEGORY_ID,
      permissionOverwrites: [
        { id: guild.roles.everyone.id, deny: [PermissionFlagsBits.ViewChannel] },
        { id: interaction.user.id, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.ReadMessageHistory] },
        { id: process.env.STAFF_ROLE_ID!, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.ReadMessageHistory] }
      ]
    });

    db.prepare('INSERT INTO tickets (guild_id, channel_id, creator_user_id, created_at) VALUES (?, ?, ?, ?)')
      .run(guild.id, channel.id, interaction.user.id, new Date().toISOString());

    await channel.send({
      content: `Ticket opened for <@${interaction.user.id}>. Staff can assist here.`,
      components: await buildTicketControls(channel.id, null, 'open')
    });

    await interaction.reply({ content: `Ticket created: <#${channel.id}>`, ephemeral: true });
    return;
  }

  if (interaction.customId.startsWith('ticket:claim:')) {
    if (!isStaff(interaction)) {
      await interaction.reply({ content: 'Staff only.', ephemeral: true });
      return;
    }

    const [, , channelId] = interaction.customId.split(':');
    const ticket = db.prepare('SELECT claimed_by_user_id, status FROM tickets WHERE channel_id = ?').get(channelId) as { claimed_by_user_id?: string | null; status?: string } | undefined;
    if (!ticket || ticket.status !== 'open') {
      await interaction.reply({ content: 'Open ticket not found.', ephemeral: true });
      return;
    }
    if (ticket.claimed_by_user_id) {
      await interaction.reply({ content: 'Ticket already claimed.', ephemeral: true });
      return;
    }

    db.prepare('UPDATE tickets SET claimed_by_user_id = ? WHERE channel_id = ?').run(interaction.user.id, channelId);
    await interaction.update({ content: `Ticket claimed by <@${interaction.user.id}>.`, components: await buildTicketControls(channelId, interaction.user.id, 'open') });
    return;
  }

  if (interaction.customId.startsWith('ticket:reopen:')) {
    if (!isStaff(interaction)) {
      await interaction.reply({ content: 'Staff only.', ephemeral: true });
      return;
    }

    const [, , channelId] = interaction.customId.split(':');
    const ticket = db.prepare('SELECT status, creator_user_id FROM tickets WHERE channel_id = ?').get(channelId) as { status?: string; creator_user_id?: string } | undefined;
    if (!ticket) {
      await interaction.reply({ content: 'Ticket not found.', ephemeral: true });
      return;
    }
    if (ticket.status === 'open') {
      await interaction.reply({ content: 'Ticket is already open.', ephemeral: true });
      return;
    }

    db.prepare('UPDATE tickets SET status = ?, closed_at = NULL WHERE channel_id = ?').run('open', channelId);

    if (interaction.channel?.type === ChannelType.GuildText) {
      await interaction.channel.permissionOverwrites.edit(ticket.creator_user_id!, {
        ViewChannel: true,
        SendMessages: true,
        ReadMessageHistory: true
      }, { type: OverwriteType.Member });

      await interaction.update({ content: 'Ticket reopened.', components: await buildTicketControls(channelId, null, 'open') });
    } else {
      await interaction.reply({ content: 'Ticket reopened.' });
    }
    return;
  }

  if (interaction.customId.startsWith('ticket:close:')) {
    if (!isStaff(interaction)) {
      await interaction.reply({ content: 'Staff only.', ephemeral: true });
      return;
    }

    const [, , channelId] = interaction.customId.split(':');
    if (interaction.channelId !== channelId) {
      await interaction.reply({ content: 'Wrong ticket channel.', ephemeral: true });
      return;
    }

    db.prepare('UPDATE tickets SET status = ?, closed_at = ? WHERE channel_id = ?')
      .run('closed', new Date().toISOString(), channelId);

    if (interaction.channel?.type === ChannelType.GuildText) {
      const transcriptPath = await exportTranscript(interaction.channel as TextChannel);
      const ticket = db.prepare('SELECT creator_user_id, claimed_by_user_id FROM tickets WHERE channel_id = ?').get(channelId) as { creator_user_id?: string; claimed_by_user_id?: string | null } | undefined;
      if (ticket?.creator_user_id) {
        await interaction.channel.permissionOverwrites.edit(ticket.creator_user_id, {
          ViewChannel: false,
          SendMessages: false,
          ReadMessageHistory: false
        }, { type: OverwriteType.Member });
      }
      await interaction.update({ content: `Ticket archived. Transcript saved to \
\`${transcriptPath}\``, components: await buildTicketControls(channelId, ticket?.claimed_by_user_id || null, 'closed') });
      await syncTicketPanel(interaction.channel as TextChannel, channelId);
    } else {
      await interaction.reply({ content: 'Ticket archived.' });
    }
  }
});

await client.login(process.env.DISCORD_TOKEN);

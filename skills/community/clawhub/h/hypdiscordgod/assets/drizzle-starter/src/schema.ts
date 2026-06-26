import { pgTable, text, timestamp, serial } from 'drizzle-orm/pg-core';

export const guildSettings = pgTable('guild_settings', {
  guildId: text('guild_id').primaryKey(),
  settingsJson: text('settings_json').notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull()
});

export const tickets = pgTable('tickets', {
  id: serial('id').primaryKey(),
  guildId: text('guild_id').notNull(),
  channelId: text('channel_id').notNull(),
  creatorUserId: text('creator_user_id').notNull(),
  status: text('status').notNull(),
  claimedByUserId: text('claimed_by_user_id'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  closedAt: timestamp('closed_at')
});

export const warnings = pgTable('warnings', {
  id: serial('id').primaryKey(),
  guildId: text('guild_id').notNull(),
  userId: text('user_id').notNull(),
  moderatorUserId: text('moderator_user_id').notNull(),
  reason: text('reason').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull()
});

import { db } from './db.js';

export type GuildSettings = Record<string, unknown>;

export function getGuildSettings(guildId: string): GuildSettings {
  const row = db.prepare('SELECT settings_json FROM guild_settings WHERE guild_id = ?').get(guildId) as { settings_json?: string } | undefined;
  return row ? JSON.parse(row.settings_json || '{}') : {};
}

export function setGuildSettings(guildId: string, settings: GuildSettings) {
  const now = new Date().toISOString();
  db.prepare(`
    INSERT INTO guild_settings (guild_id, settings_json, updated_at)
    VALUES (?, ?, ?)
    ON CONFLICT(guild_id) DO UPDATE SET settings_json = excluded.settings_json, updated_at = excluded.updated_at
  `).run(guildId, JSON.stringify(settings), now);
  return now;
}

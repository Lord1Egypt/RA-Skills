CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id TEXT NOT NULL,
  channel_id TEXT NOT NULL UNIQUE,
  creator_user_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  claimed_by_user_id TEXT,
  topic TEXT,
  created_at TEXT NOT NULL,
  closed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_tickets_guild_id ON tickets(guild_id);
CREATE INDEX IF NOT EXISTS idx_tickets_creator_user_id ON tickets(creator_user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);

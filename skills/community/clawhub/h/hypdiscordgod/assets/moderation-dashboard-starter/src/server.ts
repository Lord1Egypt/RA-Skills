import 'dotenv/config';
import cors from 'cors';
import express from 'express';
import Database from 'better-sqlite3';

const db = new Database(process.env.DATABASE_PATH || 'moderation.db');
db.exec(`
CREATE TABLE IF NOT EXISTS warnings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  moderator_user_id TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS mod_actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id TEXT NOT NULL,
  target_user_id TEXT NOT NULL,
  moderator_user_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_user_id TEXT NOT NULL,
  guild_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
`);

const app = express();
app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => res.json({ ok: true }));
app.get('/warnings/:guildId/:userId', (req, res) => {
  const rows = db.prepare('SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY id DESC').all(req.params.guildId, req.params.userId);
  res.json(rows);
});
app.post('/warnings', (req, res) => {
  const now = new Date().toISOString();
  db.prepare('INSERT INTO warnings (guild_id, user_id, moderator_user_id, reason, created_at) VALUES (?, ?, ?, ?, ?)')
    .run(req.body.guildId, req.body.userId, req.body.moderatorUserId, req.body.reason, now);
  db.prepare('INSERT INTO audit_log (actor_user_id, guild_id, action_type, payload_json, created_at) VALUES (?, ?, ?, ?, ?)')
    .run(req.body.moderatorUserId, req.body.guildId, 'warning.create', JSON.stringify(req.body), now);
  res.json({ ok: true, createdAt: now });
});
app.post('/mod-actions', (req, res) => {
  const now = new Date().toISOString();
  db.prepare('INSERT INTO mod_actions (guild_id, target_user_id, moderator_user_id, action_type, reason, created_at) VALUES (?, ?, ?, ?, ?, ?)')
    .run(req.body.guildId, req.body.targetUserId, req.body.moderatorUserId, req.body.actionType, req.body.reason, now);
  db.prepare('INSERT INTO audit_log (actor_user_id, guild_id, action_type, payload_json, created_at) VALUES (?, ?, ?, ?, ?)')
    .run(req.body.moderatorUserId, req.body.guildId, `mod.${req.body.actionType}`, JSON.stringify(req.body), now);
  res.json({ ok: true, createdAt: now });
});
app.get('/audit-log/:guildId', (req, res) => {
  const rows = db.prepare('SELECT * FROM audit_log WHERE guild_id = ? ORDER BY id DESC LIMIT 100').all(req.params.guildId);
  res.json(rows);
});

const port = Number(process.env.PORT || 3100);
app.listen(port, () => console.log(`Moderation dashboard starter listening on ${port}`));

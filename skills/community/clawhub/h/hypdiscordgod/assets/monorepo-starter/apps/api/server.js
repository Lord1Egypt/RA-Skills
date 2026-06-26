import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';

const app = express();
app.use(cors({ origin: true, credentials: true }));
app.use(cookieParser(process.env.SESSION_COOKIE_SECRET || 'dev-secret'));
app.use(express.json());

app.get('/health', (_req, res) => res.json({ ok: true, service: 'api' }));
app.get('/dashboard/guilds', (_req, res) => res.json([{ id: '1234567890', name: 'Example Guild' }]));
app.get('/dashboard/guilds/:guildId/settings', (req, res) => res.json({ guildId: req.params.guildId, settings: { ticketCategoryId: '', staffRoleId: '' } }));
app.put('/dashboard/guilds/:guildId/settings', (req, res) => res.json({ ok: true, guildId: req.params.guildId, received: req.body }));
app.post('/auth/logout', (_req, res) => res.json({ ok: true }));
app.post('/webhooks/example', (req, res) => res.json({ ok: true, queued: true, payload: req.body }));

const port = Number(process.env.PORT || 3000);
app.listen(port, () => console.log(`monorepo api listening on ${port}`));

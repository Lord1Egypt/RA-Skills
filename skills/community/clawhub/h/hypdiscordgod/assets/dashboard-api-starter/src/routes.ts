import { Router } from 'express';
import { getGuildSettings, setGuildSettings } from './guild-config.js';
import { requireApiToken, requireDashboardSession, requireGuildManageAccess, startDiscordOauth, finishDiscordOauth, logoutDashboardSession, listAuthorizedGuilds } from './auth.js';
import { requireCsrf } from './csrf.js';

export const router = Router();

router.get('/health', (_req, res) => {
  res.json({ ok: true });
});

router.get('/auth/discord', startDiscordOauth);
router.get('/auth/discord/callback', finishDiscordOauth);
router.post('/auth/logout', requireCsrf, logoutDashboardSession);
router.get('/dashboard/guilds', requireDashboardSession, listAuthorizedGuilds);

router.get('/guilds/:guildId/settings', requireApiToken, (req, res) => {
  res.json({ guildId: req.params.guildId, settings: getGuildSettings(req.params.guildId) });
});

router.put('/guilds/:guildId/settings', requireApiToken, (req, res) => {
  const updatedAt = setGuildSettings(req.params.guildId, req.body ?? {});
  res.json({ ok: true, guildId: req.params.guildId, updatedAt });
});

router.get('/dashboard/guilds/:guildId/settings', requireDashboardSession, requireGuildManageAccess, (req, res) => {
  res.json({ guildId: req.params.guildId, settings: getGuildSettings(req.params.guildId) });
});

router.put('/dashboard/guilds/:guildId/settings', requireDashboardSession, requireGuildManageAccess, requireCsrf, (req, res) => {
  const updatedAt = setGuildSettings(req.params.guildId, req.body ?? {});
  res.json({ ok: true, guildId: req.params.guildId, updatedAt, actor: (req as any).dashboardUserId });
});

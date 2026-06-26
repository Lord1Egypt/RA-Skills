import crypto from 'node:crypto';
import type { Request, Response, NextFunction } from 'express';
import { createSession, deleteSession, getSession } from './session-store.js';
import { hasManageGuildPermission } from './discord-permissions.js';

export function requireApiToken(req: Request, res: Response, next: NextFunction) {
  const expected = process.env.API_TOKEN;
  const provided = req.header('x-api-token');

  if (!expected || provided !== expected) {
    res.status(401).json({ error: 'unauthorized' });
    return;
  }

  next();
}

export function startDiscordOauth(req: Request, res: Response) {
  const state = crypto.randomUUID();
  res.cookie('discord_oauth_state', state, { httpOnly: true, sameSite: 'lax', secure: false, signed: true });
  const params = new URLSearchParams({
    client_id: process.env.DISCORD_CLIENT_ID || '',
    redirect_uri: process.env.DISCORD_REDIRECT_URI || '',
    response_type: 'code',
    scope: 'identify guilds',
    state,
    prompt: 'none'
  });
  res.redirect(`https://discord.com/oauth2/authorize?${params.toString()}`);
}

export async function finishDiscordOauth(req: Request, res: Response) {
  if (!req.query.code || req.query.state !== req.signedCookies.discord_oauth_state) {
    res.status(400).send('OAuth validation failed');
    return;
  }

  const tokenRes = await fetch('https://discord.com/api/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: process.env.DISCORD_CLIENT_ID || '',
      client_secret: process.env.DISCORD_CLIENT_SECRET || '',
      grant_type: 'authorization_code',
      code: String(req.query.code),
      redirect_uri: process.env.DISCORD_REDIRECT_URI || ''
    })
  });

  const tokenData = await tokenRes.json() as { access_token?: string; refresh_token?: string };
  if (!tokenData.access_token) {
    res.status(400).send('OAuth token exchange failed');
    return;
  }

  const userRes = await fetch('https://discord.com/api/users/@me', {
    headers: { Authorization: `Bearer ${tokenData.access_token}` }
  });
  const user = await userRes.json() as { id: string };

  const sessionId = crypto.randomUUID();
  createSession(sessionId, user.id, tokenData.access_token, tokenData.refresh_token);
  res.clearCookie('discord_oauth_state');
  res.cookie('dashboard_session', sessionId, { httpOnly: true, sameSite: 'lax', secure: false, signed: true });
  res.redirect('/');
}

export function logoutDashboardSession(req: Request, res: Response) {
  const sessionId = req.signedCookies.dashboard_session;
  if (sessionId) deleteSession(sessionId);
  res.clearCookie('dashboard_session');
  res.clearCookie('csrf_token');
  res.json({ ok: true });
}

export function requireDashboardSession(req: Request, res: Response, next: NextFunction) {
  const sessionId = req.signedCookies.dashboard_session;
  const session = sessionId ? getSession(sessionId) : null;
  if (!session) {
    res.status(401).json({ error: 'login_required' });
    return;
  }
  (req as Request & { dashboardUserId?: string; dashboardAccessToken?: string }).dashboardUserId = session.discordUserId;
  (req as Request & { dashboardUserId?: string; dashboardAccessToken?: string }).dashboardAccessToken = session.accessToken;
  next();
}

export async function requireGuildManageAccess(req: Request, res: Response, next: NextFunction) {
  const accessToken = (req as any).dashboardAccessToken as string | undefined;
  if (!accessToken) {
    res.status(401).json({ error: 'login_required' });
    return;
  }

  const guildsRes = await fetch('https://discord.com/api/users/@me/guilds', {
    headers: { Authorization: `Bearer ${accessToken}` }
  });
  const guilds = await guildsRes.json() as Array<{ id: string; permissions: string }>;
  const guild = guilds.find((g) => g.id === req.params.guildId);
  if (!guild || !hasManageGuildPermission(guild.permissions)) {
    res.status(403).json({ error: 'forbidden' });
    return;
  }

  next();
}

export async function listAuthorizedGuilds(req: Request, res: Response) {
  const accessToken = (req as any).dashboardAccessToken as string | undefined;
  if (!accessToken) {
    res.status(401).json({ error: 'login_required' });
    return;
  }

  const guildsRes = await fetch('https://discord.com/api/users/@me/guilds', {
    headers: { Authorization: `Bearer ${accessToken}` }
  });
  const guilds = await guildsRes.json() as Array<{ id: string; name: string; permissions: string }>;
  res.json(guilds.filter((g) => hasManageGuildPermission(g.permissions)).map((g) => ({ id: g.id, name: g.name })));
}

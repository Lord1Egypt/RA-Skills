/**
 * Pixel Agents Dashboard — Server
 *
 * Serves the React dashboard and provides real-time agent activity
 * via WebSocket. Tails OpenClaw session JSONL files and broadcasts
 * parsed events to connected browser clients.
 */

import express from 'express';
import * as fs from 'fs';
import { createServer } from 'http';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { WebSocketServer, WebSocket } from 'ws';

import { loadAllSprites } from './assetLoader.js';
import { TaskSpawner } from './spawner.js';
import { AGENTS, SERVER_PORT, FEATURES, SPAWNABLE_AGENTS, REMOTE_AGENTS, dashboardConfig } from './config.js';
import { serveSetupWizard } from './setupWizard.js';
import { getHardwareStats, getSolaraHardwareStats } from './hardware.js';
import { getServiceStatuses, controlService, restartService } from './services.js';
import { getVersionInfo, getSolaraVersionInfo, runUpdate, runSolaraUpdate } from './version.js';
import type { DashboardEvent } from './openclawParser.js';
import { SessionWatcher } from './sessionWatcher.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(express.json({ limit: '1mb' }));
const server = createServer(app);

// ── First-run: Setup Wizard ────────────────────────────────
// If no config file exists, serve the setup wizard instead of the dashboard.
// The wizard generates dashboard.config.json and restarts the server.
if (!dashboardConfig) {
  serveSetupWizard(app, server, SERVER_PORT);
  // serveSetupWizard starts listening and never falls through
} else {

// Layout persistence — stored relative to project root
const LAYOUT_PATH = path.resolve(
  process.env.PIXEL_AGENTS_ROOT || path.resolve(__dirname, '..'),
  'data', 'layout.json',
);

function loadSavedLayout(): Record<string, unknown> | null {
  try {
    if (fs.existsSync(LAYOUT_PATH)) {
      return JSON.parse(fs.readFileSync(LAYOUT_PATH, 'utf-8'));
    }
  } catch (err) {
    console.error('[Layout] Error loading saved layout:', err);
  }
  return null;
}

function saveLayout(layout: Record<string, unknown>): void {
  try {
    const dir = path.dirname(LAYOUT_PATH);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(LAYOUT_PATH, JSON.stringify(layout, null, 2));
    console.log('[Layout] Saved layout to', LAYOUT_PATH);
  } catch (err) {
    console.error('[Layout] Error saving layout:', err);
  }
}

const savedLayout = loadSavedLayout();

// WebSocket server on /ws path
const wss = new WebSocketServer({ server, path: '/ws' });

// Connected browser clients
const clients = new Set<WebSocket>();

// Broadcast an event to all connected clients
function broadcast(event: DashboardEvent): void {
  const data = JSON.stringify(event);
  for (const client of clients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  }
}

// Load sprites at startup (once)
const sprites = loadAllSprites();

// Session watcher — tails JSONL files and emits events
const watcher = new SessionWatcher(AGENTS, (event) => {
  broadcast(event);
});

// WebSocket connection handling
wss.on('connection', (ws) => {
  console.log('[WS] Client connected');
  clients.add(ws);

  // Send agent config and current state on connect
  const agentStates = watcher.getAgentStates();

  // Send saved layout if one exists
  if (savedLayout) {
    ws.send(JSON.stringify({
      type: 'layoutLoaded',
      layout: savedLayout,
    }));
  }

  // Send agent configuration + feature flags
  ws.send(JSON.stringify({
    type: 'init',
    features: FEATURES,
    spawnable: SPAWNABLE_AGENTS,
    agents: agentStates.map(s => ({
      id: s.id,
      name: s.config.displayName,
      emoji: s.config.emoji,
      palette: s.config.palette,
      hueShift: s.config.hueShift,
      alwaysPresent: s.config.alwaysPresent,
      isActive: s.isActive,
      isStalled: s.isStalled,
      currentTask: s.currentTask,
      channel: s.channel,
      lastChatMessage: s.lastChatMessage,
      tools: s.tools,
    })),
  }));

  // Send sprite data after init
  if (sprites.characters) {
    ws.send(JSON.stringify({
      type: 'characterSpritesLoaded',
      characters: sprites.characters,
    }));
  }
  if (sprites.wallSprites) {
    ws.send(JSON.stringify({
      type: 'wallTilesLoaded',
      sprites: sprites.wallSprites,
    }));
  }
  if (sprites.floorSprites) {
    ws.send(JSON.stringify({
      type: 'floorTilesLoaded',
      sprites: sprites.floorSprites,
    }));
  }

  ws.on('close', () => {
    console.log('[WS] Client disconnected');
    clients.delete(ws);
  });

  ws.on('error', (err) => {
    console.error('[WS] Error:', err.message);
    clients.delete(ws);
  });
});

// REST API — save/load layout
app.post('/api/layout', (req, res) => {
  const layout = req.body;
  if (!layout || typeof layout !== 'object') {
    res.status(400).json({ error: 'Invalid layout' });
    return;
  }
  saveLayout(layout);
  res.json({ ok: true });
});

app.get('/api/layout', (_req, res) => {
  const layout = loadSavedLayout();
  if (layout) {
    res.json(layout);
  } else {
    res.status(404).json({ error: 'No saved layout' });
  }
});

// Hardware stats endpoint
app.get('/api/hardware', (_req, res) => {
  try {
    res.json(getHardwareStats());
  } catch (err) {
    res.status(500).json({ error: 'Failed to read hardware stats' });
  }
});

// Remote hardware/version endpoints — only registered if remote agents exist
if (REMOTE_AGENTS.length > 0) {

app.get('/api/hardware/solara', (_req, res) => {
  try {
    const stats = getSolaraHardwareStats();
    if (stats) {
      res.json({ online: true, ...stats });
    } else {
      res.json({ online: false });
    }
  } catch {
    res.json({ online: false });
  }
});

// Version check and update endpoints
app.get('/api/version', (_req, res) => {
  try {
    res.json(getVersionInfo());
  } catch {
    res.status(500).json({ error: 'Failed to check version' });
  }
});

app.post('/api/update', (_req, res) => {
  console.log('[UPDATE] OpenClaw update triggered');
  try {
    const result = runUpdate();
    res.json(result);
  } catch {
    res.status(500).json({ error: 'Update failed' });
  }
});

app.get('/api/version/solara', (_req, res) => {
  try {
    res.json(getSolaraVersionInfo());
  } catch {
    res.json({ current: 'unknown', latest: 'unknown', updateAvailable: false, lastChecked: Date.now(), online: false });
  }
});

app.post('/api/update/solara', (_req, res) => {
  console.log('[UPDATE] Solara OpenClaw update triggered');
  try {
    const result = runSolaraUpdate();
    res.json(result);
  } catch {
    res.status(500).json({ error: 'Solara update failed' });
  }
});

} // end REMOTE_AGENTS guard

// Service status and control endpoints
app.get('/api/services', (_req, res) => {
  try {
    res.json(getServiceStatuses());
  } catch {
    res.status(500).json({ error: 'Failed to read service statuses' });
  }
});

app.post('/api/restart/:id', (req, res) => {
  const { id } = req.params;
  const gatewayId = id === 'earl' ? 'earl-gateway' : id === 'solara' ? 'solara-gateway' : null;
  if (!gatewayId) {
    res.status(400).json({ error: 'Unknown gateway. Use earl or solara.' });
    return;
  }
  console.log(`[RESTART] Gateway restart triggered: ${id}`);
  const result = restartService(gatewayId);
  if (result.success) {
    res.json({ ok: true, message: `${id} gateway restarting` });
  } else {
    res.status(500).json({ error: result.error });
  }
});

app.post('/api/services/:id/:action', (req, res) => {
  const { id, action } = req.params;
  if (action !== 'start' && action !== 'stop') {
    res.status(400).json({ error: 'Invalid action. Use start or stop.' });
    return;
  }
  const result = controlService(id, action);
  if (result.success) {
    res.json({ ok: true });
  } else {
    res.status(500).json({ error: result.error });
  }
});

// ── Task Spawner (Phase 4) ──────────────────────────────────

const spawner = new TaskSpawner({
  onChunk: (sessionId, text) => {
    broadcast({ type: 'spawnChunk', sessionId, text } as DashboardEvent);
  },
  onMessage: (sessionId, msg) => {
    broadcast({ type: 'spawnMessage', sessionId, role: msg.role, content: msg.content, timestamp: msg.timestamp } as DashboardEvent);
  },
  onStatusChange: (sessionId, status) => {
    broadcast({ type: 'spawnStatus', sessionId, status } as DashboardEvent);
  },
  onError: (sessionId, error) => {
    broadcast({ type: 'spawnError', sessionId, error } as DashboardEvent);
  },
});

// Spawn a new agent session
app.post('/api/spawn', async (req, res) => {
  const { agent, task } = req.body;
  try {
    const session = await spawner.spawn(agent, task);
    res.json({
      ok: true,
      id: session.id,
      agent: session.agent,
      sessionKey: session.sessionKey,
    });
  } catch (err) {
    const status = (err as Error).message.includes('Max concurrent') ? 429 : 400;
    res.status(status).json({ ok: false, error: (err as Error).message });
  }
});

// Send follow-up message to existing session
app.post('/api/spawn/:id/message', async (req, res) => {
  const { id } = req.params;
  const { message } = req.body;
  try {
    await spawner.sendMessage(id, message);
    res.json({ ok: true });
  } catch (err) {
    const status = (err as Error).message.includes('not found') ? 404 : 400;
    res.status(status).json({ ok: false, error: (err as Error).message });
  }
});

// Get session status + conversation
app.get('/api/spawn/:id', (req, res) => {
  const session = spawner.getSession(req.params.id);
  if (!session) {
    res.status(404).json({ ok: false, error: 'Session not found' });
    return;
  }
  res.json({ ok: true, ...session });
});

// List all spawned sessions
app.get('/api/spawn', (_req, res) => {
  res.json({ ok: true, sessions: spawner.listSessions() });
});

// Close/end a spawned session
app.delete('/api/spawn/:id', (req, res) => {
  const removed = spawner.closeSession(req.params.id);
  if (removed) {
    broadcast({ type: 'spawnClosed', sessionId: req.params.id } as DashboardEvent);
    res.json({ ok: true });
  } else {
    res.status(404).json({ ok: false, error: 'Session not found' });
  }
});

// PIXEL_AGENTS_ROOT from CLI entry point; falls back to __dirname/..
const projectRoot = process.env.PIXEL_AGENTS_ROOT || path.resolve(__dirname, '..');

// Serve static assets (sprites, etc.) from bundled public dir
const assetsDir = path.resolve(projectRoot, 'public');
app.use('/assets', express.static(path.join(assetsDir, 'assets')));

// In production, serve the built React app
const distDir = path.resolve(projectRoot, 'dist');
app.use(express.static(distDir));
// Express v5 uses named wildcards
app.get('/{*path}', (_req, res) => {
  res.sendFile(path.join(distDir, 'index.html'));
});

// Start everything
watcher.start();

server.listen(SERVER_PORT, '0.0.0.0', () => {
  console.log(`\n🎮 Pixel Agents Dashboard running at http://localhost:${SERVER_PORT}`);
  console.log(`   WebSocket: ws://localhost:${SERVER_PORT}/ws`);
  console.log(`   Watching ${AGENTS.length} agents for session activity\n`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  watcher.stop();
  wss.close();
  server.close();
  process.exit(0);
});

process.on('SIGTERM', () => {
  watcher.stop();
  wss.close();
  server.close();
  process.exit(0);
});

} // end dashboardConfig else block

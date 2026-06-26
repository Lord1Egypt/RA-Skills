/**
 * Setup Wizard — First-run experience when no dashboard.config.json exists.
 *
 * Serves a self-contained HTML page that walks the user through:
 * 1. Gateway URL and token
 * 2. Agent definitions (auto-discovers from ~/.openclaw/agents/ if possible)
 * 3. Feature toggles
 * 4. Writes dashboard.config.json and restarts
 *
 * The wizard is intentionally a single HTML page with inline CSS/JS —
 * no build step, no React, no dependencies. It should feel fast and simple.
 */

import type { Express } from 'express';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import type { Server } from 'http';

import { CONFIG_FILENAME } from './configLoader.js';

/** Attempt to discover agents from ~/.openclaw/agents/ */
function discoverAgents(): Array<{ id: string; hasActive: boolean }> {
  const agentsDir = path.join(os.homedir(), '.openclaw', 'agents');
  try {
    if (!fs.existsSync(agentsDir)) return [];
    return fs.readdirSync(agentsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => {
        const sessionsDir = path.join(agentsDir, d.name, 'sessions');
        const hasActive = fs.existsSync(sessionsDir) &&
          fs.readdirSync(sessionsDir).some(f => f.endsWith('.jsonl'));
        return { id: d.name, hasActive };
      });
  } catch {
    return [];
  }
}

/** Check if gateway is reachable */
async function checkGateway(url: string): Promise<boolean> {
  try {
    const res = await fetch(`${url}/v1/models`, {
      signal: AbortSignal.timeout(3000),
    });
    return res.ok || res.status === 401; // 401 means it's there but needs auth
  } catch {
    return false;
  }
}

const PALETTE_NAMES = ['Blue', 'Red', 'Green', 'Purple', 'Gold', 'Teal'];
const DEFAULT_EMOJIS = ['🤖', '🔧', '🔍', '🔩', '☀️', '🧪'];

export function serveSetupWizard(app: Express, server: Server, port: number): void {
  const discovered = discoverAgents();

  // API: auto-discover agents
  app.get('/api/setup/discover', (_req, res) => {
    res.json({ agents: discovered });
  });

  // API: check gateway connectivity
  app.get('/api/setup/check-gateway', async (req, res) => {
    const url = (req.query.url as string) || 'http://localhost:18789';
    const reachable = await checkGateway(url);
    res.json({ url, reachable });
  });

  // API: save config and signal restart
  app.post('/api/setup/save', (req, res) => {
    const config = req.body;
    if (!config || !config.agents || config.agents.length === 0) {
      res.status(400).json({ error: 'At least one agent is required' });
      return;
    }

    const configPath = path.resolve(CONFIG_FILENAME);
    try {
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
      console.log(`[Setup] Config written to ${configPath}`);
      res.json({ ok: true, path: configPath });

      // Restart after a short delay so the response can be sent
      setTimeout(() => {
        console.log('[Setup] Restarting server with new config...');
        process.exit(0); // systemd or supervisor will restart us
      }, 1000);
    } catch (err) {
      res.status(500).json({ error: `Failed to write config: ${(err as Error).message}` });
    }
  });

  // Serve the wizard HTML for all other routes
  app.get('/{*path}', (_req, res) => {
    res.type('html').send(wizardHtml(discovered));
  });

  server.listen(port, '0.0.0.0', () => {
    console.log(`\n🧙 Pixel Agents Setup Wizard running at http://localhost:${port}`);
    console.log(`   No dashboard.config.json found — complete the wizard to get started.\n`);
    if (discovered.length > 0) {
      console.log(`   Auto-discovered agents: ${discovered.map(a => a.id).join(', ')}`);
    }
  });
}

/** Generate the wizard HTML page */
function wizardHtml(discovered: Array<{ id: string; hasActive: boolean }>): string {
  const discoveredJson = JSON.stringify(discovered);

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pixel Agents — Setup</title>
  <style>
    @font-face {
      font-family: 'PixelFont';
      src: url('/assets/FSPixelSansUnicode-Regular.ttf') format('truetype');
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Courier New', monospace;
      background: #0a0a1a;
      color: #c0c0d0;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      padding: 40px 20px;
    }
    .wizard {
      max-width: 600px;
      width: 100%;
    }
    h1 {
      font-size: 24px;
      color: #e0e0f0;
      margin-bottom: 4px;
      letter-spacing: 1px;
    }
    .subtitle {
      font-size: 12px;
      color: #606080;
      margin-bottom: 32px;
    }
    .step {
      margin-bottom: 28px;
      padding: 16px;
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.06);
    }
    .step-title {
      font-size: 14px;
      color: #8888aa;
      margin-bottom: 12px;
      letter-spacing: 1px;
    }
    label {
      display: block;
      font-size: 11px;
      color: #8888aa;
      margin-bottom: 4px;
      margin-top: 10px;
    }
    label:first-child { margin-top: 0; }
    input[type="text"], input[type="number"] {
      width: 100%;
      padding: 8px 10px;
      font-family: 'Courier New', monospace;
      font-size: 13px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e0e0f0;
      outline: none;
    }
    input:focus {
      border-color: rgba(90,140,255,0.4);
    }
    .hint {
      font-size: 10px;
      color: #505070;
      margin-top: 3px;
    }
    .status {
      font-size: 11px;
      margin-top: 4px;
    }
    .status.ok { color: #44aa66; }
    .status.warn { color: #ccaa22; }
    .status.err { color: #cc4444; }
    .agent-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .agent-row {
      display: grid;
      grid-template-columns: 1fr 80px 50px 60px 30px;
      gap: 6px;
      align-items: center;
      padding: 6px 8px;
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.04);
    }
    .agent-row input {
      width: 100%;
    }
    .agent-row select {
      width: 100%;
      padding: 6px;
      font-family: 'Courier New', monospace;
      font-size: 12px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e0e0f0;
    }
    .remove-btn {
      background: none;
      border: none;
      color: #cc4444;
      cursor: pointer;
      font-size: 16px;
    }
    .add-btn {
      padding: 6px 12px;
      font-family: 'Courier New', monospace;
      font-size: 11px;
      background: rgba(90,140,255,0.1);
      border: 1px solid rgba(90,140,255,0.3);
      color: rgba(90,140,255,0.8);
      cursor: pointer;
      margin-top: 8px;
    }
    .add-btn:hover { background: rgba(90,140,255,0.2); }
    .features-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .feature-toggle {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 4px 6px;
      font-size: 11px;
      cursor: pointer;
    }
    .feature-toggle input[type="checkbox"] {
      width: auto;
    }
    .save-btn {
      display: block;
      width: 100%;
      padding: 12px;
      font-family: 'Courier New', monospace;
      font-size: 14px;
      background: rgba(68,170,102,0.15);
      border: 2px solid rgba(68,170,102,0.4);
      color: #44aa66;
      cursor: pointer;
      letter-spacing: 1px;
      margin-top: 8px;
    }
    .save-btn:hover { background: rgba(68,170,102,0.25); }
    .save-btn:disabled {
      opacity: 0.4;
      cursor: default;
    }
    .result {
      margin-top: 16px;
      padding: 12px;
      font-size: 12px;
      background: rgba(68,170,102,0.08);
      border: 1px solid rgba(68,170,102,0.2);
      display: none;
    }
    .col-header {
      font-size: 9px;
      color: #505070;
      letter-spacing: 1px;
    }
    .header-row {
      display: grid;
      grid-template-columns: 1fr 80px 50px 60px 30px;
      gap: 6px;
      padding: 0 8px;
      margin-bottom: 4px;
    }
  </style>
</head>
<body>
  <div class="wizard">
    <h1>🎮 Pixel Agents Dashboard</h1>
    <p class="subtitle">First-run setup — let's configure your dashboard.</p>

    <!-- Step 1: Gateway -->
    <div class="step">
      <div class="step-title">① GATEWAY CONNECTION</div>
      <label>Gateway URL</label>
      <input type="text" id="gwUrl" value="http://localhost:18789" />
      <div class="hint">Your OpenClaw gateway address</div>
      <div id="gwStatus" class="status"></div>

      <label>Auth Token</label>
      <input type="text" id="gwToken" placeholder="Leave blank to use \${OPENCLAW_GATEWAY_TOKEN} env var" />
      <div class="hint">Set directly or leave blank to read from environment</div>
    </div>

    <!-- Step 2: Agents -->
    <div class="step">
      <div class="step-title">② YOUR AGENTS</div>
      <div class="header-row">
        <span class="col-header">ID (dir name)</span>
        <span class="col-header">DISPLAY NAME</span>
        <span class="col-header">EMOJI</span>
        <span class="col-header">SKIN</span>
        <span></span>
      </div>
      <div id="agentList" class="agent-list"></div>
      <button class="add-btn" onclick="addAgent()">+ Add Agent</button>
      <div class="hint" style="margin-top:6px">
        Agent ID must match the directory name in ~/.openclaw/agents/
      </div>
    </div>

    <!-- Step 3: Features -->
    <div class="step">
      <div class="step-title">③ FEATURES</div>
      <div class="features-grid" id="featureGrid"></div>
    </div>

    <!-- Step 4: Port -->
    <div class="step">
      <div class="step-title">④ SERVER</div>
      <label>Port</label>
      <input type="number" id="port" value="5070" style="width:100px" />
    </div>

    <button class="save-btn" id="saveBtn" onclick="save()">
      GENERATE CONFIG & START DASHBOARD
    </button>
    <div id="result" class="result"></div>
  </div>

  <script>
    const discovered = ${discoveredJson};
    const emojis = ${JSON.stringify(DEFAULT_EMOJIS)};
    const palettes = ${JSON.stringify(PALETTE_NAMES)};

    const features = [
      { key: 'dayNightCycle', label: 'Day/Night Cycle', default: true },
      { key: 'conversationHeat', label: 'Conversation Heat Glow', default: true },
      { key: 'channelBadges', label: 'Channel Badges', default: true },
      { key: 'door', label: 'Animated Door', default: true },
      { key: 'sounds', label: 'Sound Effects', default: true },
      { key: 'serverRack', label: 'Hardware Monitor', default: true },
      { key: 'breakerPanel', label: 'Service Controls', default: true },
      { key: 'hamRadio', label: 'Update Checker', default: true },
      { key: 'fireAlarm', label: 'Gateway Restart', default: true },
      { key: 'nickDesk', label: 'Decorative Desk', default: false },
    ];

    // Init features grid
    const featureGrid = document.getElementById('featureGrid');
    features.forEach(f => {
      const label = document.createElement('label');
      label.className = 'feature-toggle';
      label.innerHTML = '<input type="checkbox" data-feature="' + f.key + '" '
        + (f.default ? 'checked' : '') + '> ' + f.label;
      featureGrid.appendChild(label);
    });

    // Init agents from discovery
    let agentCount = 0;
    function addAgent(id, name, emoji, palette) {
      const list = document.getElementById('agentList');
      const idx = agentCount++;
      const div = document.createElement('div');
      div.className = 'agent-row';
      div.id = 'agent-' + idx;

      let paletteOpts = '';
      for (let i = 0; i < palettes.length; i++) {
        paletteOpts += '<option value="' + i + '"' + (i === (palette||0) ? ' selected' : '') + '>' + palettes[i] + '</option>';
      }

      div.innerHTML =
        '<input type="text" data-field="id" value="' + (id||'') + '" placeholder="agent-id">'
        + '<input type="text" data-field="name" value="' + (name||'') + '" placeholder="Name">'
        + '<input type="text" data-field="emoji" value="' + (emoji||emojis[idx%emojis.length]) + '" style="text-align:center">'
        + '<select data-field="palette">' + paletteOpts + '</select>'
        + '<button class="remove-btn" onclick="this.parentElement.remove()">×</button>';
      list.appendChild(div);
    }

    if (discovered.length > 0) {
      discovered.forEach((a, i) => {
        const name = a.id.charAt(0).toUpperCase() + a.id.slice(1);
        addAgent(a.id, name, emojis[i % emojis.length], i % palettes.length);
      });
    } else {
      addAgent('main', 'Main', '🤖', 0);
    }

    // Check gateway on load + on input change
    const gwUrl = document.getElementById('gwUrl');
    let checkTimer;
    async function checkGateway() {
      const status = document.getElementById('gwStatus');
      status.textContent = 'Checking...';
      status.className = 'status';
      try {
        const res = await fetch('/api/setup/check-gateway?url=' + encodeURIComponent(gwUrl.value));
        const data = await res.json();
        if (data.reachable) {
          status.textContent = '✓ Gateway reachable';
          status.className = 'status ok';
        } else {
          status.textContent = '✗ Cannot reach gateway at ' + gwUrl.value;
          status.className = 'status err';
        }
      } catch {
        status.textContent = '? Check failed';
        status.className = 'status warn';
      }
    }
    gwUrl.addEventListener('input', () => {
      clearTimeout(checkTimer);
      checkTimer = setTimeout(checkGateway, 800);
    });
    checkGateway();

    // Save config
    async function save() {
      const btn = document.getElementById('saveBtn');
      btn.disabled = true;
      btn.textContent = 'Saving...';

      // Collect agents
      const agents = [];
      document.querySelectorAll('.agent-row').forEach((row, i) => {
        const id = row.querySelector('[data-field="id"]').value.trim();
        const name = row.querySelector('[data-field="name"]').value.trim();
        const emoji = row.querySelector('[data-field="emoji"]').value.trim();
        const palette = parseInt(row.querySelector('[data-field="palette"]').value);
        if (id) {
          agents.push({
            id,
            name: name || id,
            emoji: emoji || '🤖',
            palette: isNaN(palette) ? 0 : palette,
            alwaysPresent: i === 0, // First agent is always-present by default
          });
        }
      });

      if (agents.length === 0) {
        alert('Add at least one agent.');
        btn.disabled = false;
        btn.textContent = 'GENERATE CONFIG & START DASHBOARD';
        return;
      }

      // Collect features
      const featuresObj = {};
      document.querySelectorAll('[data-feature]').forEach(cb => {
        featuresObj[cb.dataset.feature] = cb.checked;
      });

      const token = document.getElementById('gwToken').value.trim();

      const config = {
        server: { port: parseInt(document.getElementById('port').value) || 5070 },
        gateway: {
          url: gwUrl.value.trim() || 'http://localhost:18789',
          token: token || '\${OPENCLAW_GATEWAY_TOKEN}',
        },
        openclaw: { agentsDir: '~/.openclaw/agents' },
        agents,
        spawnable: [],
        remoteAgents: [],
        features: featuresObj,
      };

      try {
        const res = await fetch('/api/setup/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(config),
        });
        const data = await res.json();
        if (data.ok) {
          const result = document.getElementById('result');
          result.style.display = 'block';
          result.innerHTML = '✓ Config saved to <strong>' + data.path + '</strong><br>'
            + 'Server is restarting... <a href="/" style="color:#44aa66">Refresh in a few seconds →</a>';
          btn.textContent = '✓ SAVED';
        } else {
          alert('Error: ' + (data.error || 'Unknown'));
          btn.disabled = false;
          btn.textContent = 'GENERATE CONFIG & START DASHBOARD';
        }
      } catch (err) {
        alert('Save failed: ' + err.message);
        btn.disabled = false;
        btn.textContent = 'GENERATE CONFIG & START DASHBOARD';
      }
    }
  </script>
</body>
</html>`;
}

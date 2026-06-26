#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const { execSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const cfgPath = path.join(root, 'config', 'config.json');
const cfgExample = path.join(root, 'config', 'config.example.json');
const cmd = process.argv[2] || 'help';
const args = process.argv.slice(3);
const DRY_RUN = args.includes('--dry-run') || process.env.DRY_RUN === '1';
const ALLOW_DESTRUCTIVE = process.env.ALLOW_DESTRUCTIVE === '1';

function loadDotEnv(file) {
  if (!fs.existsSync(file)) return;
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const s = line.trim();
    if (!s || s.startsWith('#')) continue;
    const i = s.indexOf('=');
    if (i === -1) continue;
    const key = s.slice(0, i).trim();
    let value = s.slice(i + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) process.env[key] = value;
  }
}

// Load skill-local env vars if present (without overriding shell env)
loadDotEnv(path.join(root, '.env'));

function expandHome(p) {
  return p?.startsWith('~/') ? path.join(os.homedir(), p.slice(2)) : p;
}

function toTilde(p) {
  const h = os.homedir();
  return p?.startsWith(h) ? `~/${p.slice(h.length + 1)}` : p;
}

function sh(command, cwd, quiet = false) {
  if (DRY_RUN && !quiet) {
    const redacted = command
      .replace(/CLOUDFLARE_API_TOKEN="[^"]*"/g, 'CLOUDFLARE_API_TOKEN="***"')
      .replace(/BASIC_AUTH_PASSWORD="[^"]*"/g, 'BASIC_AUTH_PASSWORD="***"');
    console.log(`[dry-run] ${redacted}`);
    return '';
  }
  if (quiet) return execSync(command, { stdio: ['ignore', 'pipe', 'pipe'], cwd: cwd || process.cwd() }).toString();
  execSync(command, { stdio: 'inherit', cwd: cwd || process.cwd() });
}

function assertSafePath(targetPath, label = 'path') {
  const resolved = path.resolve(targetPath);
  if (resolved === '/' || resolved === os.homedir() || resolved.length < 8) {
    throw new Error(`Refusing unsafe ${label}: ${resolved}`);
  }
  return resolved;
}

function clearDirectoryContents(dir) {
  const resolved = assertSafePath(dir, 'directory clear target');
  if (!fs.existsSync(resolved)) return;
  for (const entry of fs.readdirSync(resolved)) {
    const p = path.join(resolved, entry);
    if (DRY_RUN) {
      console.log(`[dry-run] remove ${p}`);
      continue;
    }
    fs.rmSync(p, { recursive: true, force: true });
  }
}

function loadConfig() {
  if (!fs.existsSync(cfgPath)) throw new Error(`Missing config: ${cfgPath} (run: init or wizard)`);
  return JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
}

function saveConfig(cfg) {
  fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n', 'utf8');
}

function init() {
  if (fs.existsSync(cfgPath)) {
    console.log('Config already exists:', cfgPath);
    return;
  }
  fs.copyFileSync(cfgExample, cfgPath);
  console.log('Created:', cfgPath);
}

function detectOpenVaults() {
  const obsidianCfg = path.join(os.homedir(), 'Library/Application Support/obsidian/obsidian.json');
  if (!fs.existsSync(obsidianCfg)) return [];
  try {
    const json = JSON.parse(fs.readFileSync(obsidianCfg, 'utf8'));
    const vaults = json?.vaults || {};
    return Object.values(vaults)
      .map((v) => v?.path)
      .filter(Boolean)
      .map((p) => ({ path: p, open: false }));
  } catch {
    return [];
  }
}

async function wizard() {
  const defaults = fs.existsSync(cfgPath)
    ? loadConfig()
    : JSON.parse(fs.readFileSync(cfgExample, 'utf8'));

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q, fallback = '') => new Promise((resolve) => {
    const suffix = fallback ? ` [${fallback}]` : '';
    rl.question(`${q}${suffix}: `, (ans) => resolve((ans || fallback || '').trim()));
  });

  console.log('🧙 Obsidian → Cloudflare Pages setup wizard\n');

  const detectedVaults = detectOpenVaults();
  if (detectedVaults.length) {
    console.log('Detected Obsidian vaults:');
    detectedVaults.forEach((v, i) => console.log(`  ${i + 1}. ${toTilde(v.path)}`));
  }

  const currentVault = defaults?.source?.vaultPath || '';
  const pickedVault = await ask('Vault path', currentVault || toTilde(detectedVaults[0]?.path || ''));

  const includeFolders = await ask(
    'Publish folders (comma-separated)',
    (defaults?.source?.includeFolders || ['Clippings']).join(',')
  );

  const excludeFolders = await ask(
    'Exclude folders (comma-separated)',
    (defaults?.source?.excludeFolders || ['Private', 'Templates', 'Daily']).join(',')
  );

  const requirePublish = await ask(
    'Require frontmatter publish: true? (y/n)',
    defaults?.source?.requireFrontmatterPublish ? 'y' : 'n'
  );

  const workspaceDir = await ask('Quartz project directory', defaults?.publish?.workspaceDir || '~/projects/read-k06');
  const contentDir = await ask('Quartz content directory', defaults?.publish?.contentDir || 'content');

  const title = await ask('Site title', defaults?.site?.title || 'Obsidian Vault');
  const baseUrl = await ask('Site base URL', defaults?.site?.baseUrl || 'https://YOURDOMAIN.COM');
  const theme = await ask('Theme name', defaults?.site?.theme || 'minimal');
  const showBacklinks = await ask('Show backlinks? (y/n)', defaults?.site?.showBacklinks ? 'y' : 'y');

  const inferredDomain = (defaults?.cloudflare?.productionDomain || defaults?.site?.baseUrl || 'YOURDOMAIN.COM')
    .replace(/^https?:\/\//, '')
    .replace(/\/.*$/, '') || 'YOURDOMAIN.COM';
  const rootSourceFolder = await ask(
    'Folder to promote to site root index',
    defaults?.site?.branding?.rootSourceFolder || (defaults?.source?.includeFolders?.[0] || 'Clippings')
  );
  const clippingsIndexLabel = await ask(
    'Clippings/source index label',
    defaults?.site?.branding?.clippingsIndexLabel || `Clippings | ${inferredDomain}`
  );
  const rootIndexLabel = await ask(
    'Root index label',
    defaults?.site?.branding?.rootIndexLabel || `Vault | ${inferredDomain}`
  );
  const sidebarTitleHtml = await ask(
    'Sidebar title HTML (use <br/> for line break)',
    defaults?.site?.branding?.sidebarTitleHtml || `Obsidian Vault<br/>${inferredDomain}`
  );

  const projectName = await ask('Cloudflare Pages project name', defaults?.cloudflare?.projectName || 'your-pages-project');
  const branch = await ask('Deploy branch', defaults?.cloudflare?.branch || 'main');
  const domain = await ask('Full production domain (e.g. YOURDOMAIN.COM)', defaults?.cloudflare?.productionDomain || 'YOURDOMAIN.COM');
  const apiTokenEnv = await ask('Cloudflare API token env var name', defaults?.cloudflare?.apiTokenEnv || 'CLOUDFLARE_API_TOKEN');
  const accountIdEnv = await ask('Cloudflare account id env var name', defaults?.cloudflare?.accountIdEnv || 'CLOUDFLARE_ACCOUNT_ID');

  const authEnabled = await ask(
    'Enable basic auth protection? (y/n)',
    defaults?.cloudflare?.basicAuth?.enabled === false ? 'n' : 'y'
  );
  let authUsername = defaults?.cloudflare?.basicAuth?.username || '';
  let authPassword = defaults?.cloudflare?.basicAuth?.password || '';
  if (/^y(es)?$/i.test(authEnabled)) {
    authUsername = await ask('Basic auth username', authUsername || '1851');
    authPassword = await ask('Basic auth password', authPassword || '');
  }

  const cfg = {
    source: {
      vaultPath: pickedVault,
      includeFolders: includeFolders.split(',').map((s) => s.trim()).filter(Boolean),
      excludeFolders: excludeFolders.split(',').map((s) => s.trim()).filter(Boolean),
      requireFrontmatterPublish: /^y(es)?$/i.test(requirePublish)
    },
    publish: {
      workspaceDir,
      contentDir
    },
    site: {
      generator: 'quartz',
      title,
      baseUrl,
      theme,
      showBacklinks: /^y(es)?$/i.test(showBacklinks),
      branding: {
        rootSourceFolder,
        clippingsIndexLabel,
        rootIndexLabel,
        sidebarTitleHtml
      }
    },
    cloudflare: {
      projectName,
      branch,
      productionDomain: domain,
      apiTokenEnv,
      accountIdEnv,
      basicAuth: {
        enabled: /^y(es)?$/i.test(authEnabled),
        username: authUsername,
        password: authPassword
      }
    }
  };

  saveConfig(cfg);
  rl.close();
  console.log(`\nSaved config: ${cfgPath} ✅`);
}

function doctor() {
  const cfg = loadConfig();
  const vaultPath = expandHome(cfg.source.vaultPath);
  const workspaceDir = expandHome(cfg.publish.workspaceDir);

  if (!fs.existsSync(vaultPath)) throw new Error(`Vault not found: ${vaultPath}`);
  if (!fs.existsSync(workspaceDir)) throw new Error(`Workspace not found: ${workspaceDir}`);

  ['rsync', 'node', 'npm', 'npx', 'wrangler'].forEach((b) => {
    try {
      sh(`command -v ${b} >/dev/null 2>&1`, process.cwd(), true);
    } catch {
      throw new Error(`Missing binary: ${b}`);
    }
  });

  const tokenEnv = cfg.cloudflare?.apiTokenEnv || 'CLOUDFLARE_API_TOKEN';
  const accountEnv = cfg.cloudflare?.accountIdEnv || 'CLOUDFLARE_ACCOUNT_ID';
  if (!process.env[tokenEnv]) {
    throw new Error(`Missing Cloudflare token env var: ${tokenEnv}`);
  }
  if (!process.env[accountEnv]) {
    console.warn(`Warning: ${accountEnv} is not set (some wrangler setups still work without it).`);
  }

  if (cfg.cloudflare?.basicAuth?.enabled && cfg.cloudflare?.basicAuth?.password) {
    console.warn('Warning: basicAuth.password is stored in config.json. Prefer env-backed credentials for better safety.');
  }

  console.log('Doctor passed ✅');
}

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir)) {
    const p = path.join(dir, entry);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function hasPublishTrue(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return false;
  return /(^|\n)publish:\s*true\s*(\n|$)/i.test(m[1]);
}

function sync() {
  const cfg = loadConfig();
  const vaultPath = expandHome(cfg.source.vaultPath);
  const workspaceDir = expandHome(cfg.publish.workspaceDir);
  const contentDir = cfg.publish.contentDir || 'content';
  const dest = path.join(workspaceDir, contentDir);

  if (!cfg.source.includeFolders?.length) throw new Error('includeFolders is empty');

  fs.mkdirSync(dest, { recursive: true });
  clearDirectoryContents(dest);

  for (const folder of cfg.source.includeFolders) {
    const src = path.join(vaultPath, folder);
    if (!fs.existsSync(src)) {
      console.warn(`Skipping missing source folder: ${src}`);
      continue;
    }
    const excludes = (cfg.source.excludeFolders || [])
      .map((f) => `--exclude '${f}/'`)
      .join(' ');
    sh(`rsync -av --exclude '.obsidian/' --exclude '*.canvas' ${excludes} "${src}/" "${dest}/${folder}/"`);
  }

  if (cfg.source.requireFrontmatterPublish) {
    let kept = 0;
    let removed = 0;
    for (const p of walk(dest)) {
      if (!p.endsWith('.md')) continue;
      const txt = fs.readFileSync(p, 'utf8');
      if (!hasPublishTrue(txt)) {
        fs.unlinkSync(p);
        removed += 1;
      } else {
        kept += 1;
      }
    }
    console.log(`Frontmatter filter: kept ${kept}, removed ${removed}`);
  }

  console.log('Sync complete ✅');
}

function setupProject() {
  const cfg = loadConfig();
  const workspaceDir = expandHome(cfg.publish.workspaceDir);

  fs.mkdirSync(workspaceDir, { recursive: true });

  const hasQuartz = fs.existsSync(path.join(workspaceDir, 'quartz.config.ts'));
  if (hasQuartz) {
    console.log('Quartz project already initialized ✅');
    return;
  }

  console.log(`Initializing Quartz project in: ${workspaceDir}`);

  // Preferred path (older Quartz bootstrap flow).
  let bootstrapOk = false;
  try {
    if (!fs.existsSync(path.join(workspaceDir, 'package.json'))) {
      sh('npm init -y', workspaceDir);
    }
    sh('npx quartz create', workspaceDir);
    bootstrapOk = fs.existsSync(path.join(workspaceDir, 'quartz.config.ts'));
  } catch {
    bootstrapOk = false;
  }

  // Fallback path: clone Quartz directly if bootstrap command is unavailable.
  if (!bootstrapOk) {
    console.log('Falling back to git clone bootstrap for Quartz...');
    if (fs.readdirSync(workspaceDir).length > 0) {
      if (!ALLOW_DESTRUCTIVE) {
        throw new Error('Fallback bootstrap requires clearing workspaceDir. Re-run with ALLOW_DESTRUCTIVE=1 or use an empty workspace directory.');
      }
      clearDirectoryContents(workspaceDir);
    }
    sh(`git clone https://github.com/jackyzha0/quartz.git "${workspaceDir}"`);
    sh('npm i', workspaceDir);
    bootstrapOk = fs.existsSync(path.join(workspaceDir, 'quartz.config.ts'));
  }

  if (!bootstrapOk) {
    throw new Error('Quartz initialization failed: quartz.config.ts not found');
  }

  console.log('Quartz project setup complete ✅');
}

function replaceInFile(filePath, replacements) {
  if (!fs.existsSync(filePath)) return false;
  let txt = fs.readFileSync(filePath, 'utf8');
  const before = txt;
  for (const [from, to] of replacements) txt = txt.split(from).join(to);
  if (txt !== before) fs.writeFileSync(filePath, txt, 'utf8');
  return txt !== before;
}

function brandSidebarTitle(publicDir, sidebarTitleHtml) {
  const files = walk(publicDir).filter((p) => p.endsWith('.html'));
  let changed = 0;
  for (const file of files) {
    let txt = fs.readFileSync(file, 'utf8');
    const before = txt;
    txt = txt.replace(/<h2 class="page-title"><a href="([^"]*)">[\s\S]*?<\/a><\/h2>/, `<h2 class="page-title"><a href="$1">${sidebarTitleHtml}</a></h2>`);
    if (txt !== before) {
      fs.writeFileSync(file, txt, 'utf8');
      changed += 1;
    }
  }
  if (changed) console.log(`Updated sidebar title on ${changed} page(s) ✅`);
}

function injectShareButtons(publicDir) {
  const files = walk(publicDir).filter((p) => p.endsWith('.html'));
  let changed = 0;

  const buttonHtml = '<button class="share-current-page" title="Copy page link" aria-label="Copy page link" style="margin-left:.5rem;border:1px solid var(--lightgray);background:var(--light);color:var(--dark);border-radius:6px;padding:.15rem .45rem;cursor:pointer;font-size:.85rem;vertical-align:middle;">🔗 Copy Link</button>';
  const script = `<script>(function(){\n  function wire(){\n    var btns=document.querySelectorAll('.share-current-page');\n    btns.forEach(function(btn){\n      if(btn.dataset.wired==='1') return;\n      btn.dataset.wired='1';\n      btn.addEventListener('click', async function(){\n        var url=window.location.href;\n        try {\n          if (navigator.clipboard && navigator.clipboard.writeText) {\n            await navigator.clipboard.writeText(url);\n          } else {\n            var ta=document.createElement('textarea');\n            ta.value=url; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();\n          }\n          var old=btn.textContent; btn.textContent='✅'; setTimeout(function(){btn.textContent=old;}, 900);\n        } catch(e) {\n          var old=btn.textContent; btn.textContent='❌'; setTimeout(function(){btn.textContent=old;}, 900);\n        }\n      });\n    });\n  }\n  wire();\n  document.addEventListener('nav', wire);\n})();</script>`;

  for (const file of files) {
    let txt = fs.readFileSync(file, 'utf8');
    if (txt.includes('share-current-page')) continue;

    const before = txt;
    txt = txt.replace('<h1 class="article-title">', '<h1 class="article-title">');
    txt = txt.replace(/(<h1 class="article-title">[\s\S]*?<\/h1>)/, `$1${buttonHtml}`);

    if (txt !== before) {
      if (txt.includes('</body>')) txt = txt.replace('</body>', `${script}</body>`);
      fs.writeFileSync(file, txt, 'utf8');
      changed += 1;
    }
  }

  if (changed) console.log(`Injected share-link buttons on ${changed} page(s) ✅`);
}

function inferDomain(cfg) {
  if (cfg?.cloudflare?.productionDomain) return cfg.cloudflare.productionDomain;
  const baseUrl = cfg?.site?.baseUrl || '';
  try {
    const u = new URL(baseUrl.startsWith('http') ? baseUrl : `https://${baseUrl}`);
    return u.hostname || 'YOURDOMAIN.COM';
  } catch {
    return 'YOURDOMAIN.COM';
  }
}

function build() {
  const cfg = loadConfig();
  const workspaceDir = expandHome(cfg.publish.workspaceDir);
  sh('npx quartz build', workspaceDir);

  const publicDir = path.join(workspaceDir, 'public');
  const rootSourceFolder = cfg?.site?.branding?.rootSourceFolder || 'Clippings';
  const sourceIndex = path.join(publicDir, rootSourceFolder, 'index.html');
  const rootIndex = path.join(publicDir, 'index.html');
  if (fs.existsSync(sourceIndex)) {
    fs.copyFileSync(sourceIndex, rootIndex);
    console.log(`Promoted /${rootSourceFolder}/index.html -> /index.html ✅`);
  }

  // Config-driven branding.
  const domain = inferDomain(cfg);
  const clippingsLabel = cfg?.site?.branding?.clippingsIndexLabel || `${rootSourceFolder} | ${domain}`;
  const rootLabel = cfg?.site?.branding?.rootIndexLabel || `Vault | ${domain}`;
  const sidebarTitleHtml = cfg?.site?.branding?.sidebarTitleHtml || `Obsidian Vault<br/>${domain}`;

  const clippingsBranded = replaceInFile(sourceIndex, [
    ['Quartz 4', clippingsLabel],
    ['<title>Clippings', `<title>${clippingsLabel}`]
  ]);
  const rootBranded = replaceInFile(rootIndex, [
    ['Quartz 4', rootLabel],
    ['<title>Clippings', `<title>${rootLabel}`]
  ]);
  if (clippingsBranded) console.log(`Branded /${rootSourceFolder}/index.html as "${clippingsLabel}" ✅`);
  if (rootBranded) console.log(`Branded /index.html as "${rootLabel}" ✅`);

  brandSidebarTitle(publicDir, sidebarTitleHtml);
  injectShareButtons(publicDir);

  console.log('Build complete ✅');
}

function ensureBasicAuthMiddleware(workspaceDir, cfg) {
  const auth = cfg.cloudflare?.basicAuth;
  const fnDir = path.join(workspaceDir, 'functions');
  const middlewarePath = path.join(fnDir, '_middleware.js');

  if (!auth?.enabled) {
    if (fs.existsSync(middlewarePath)) {
      fs.unlinkSync(middlewarePath);
      console.log('Removed basic auth middleware (disabled in config) ✅');
    }
    return;
  }

  const usernameEnv = auth?.usernameEnv || 'BASIC_AUTH_USERNAME';
  const passwordEnv = auth?.passwordEnv || 'BASIC_AUTH_PASSWORD';
  const username = process.env[usernameEnv] || auth.username;
  const password = process.env[passwordEnv] || auth.password;

  if (!username || !password) {
    throw new Error(`basicAuth is enabled but credentials are missing. Set config values or env vars ${usernameEnv}/${passwordEnv}.`);
  }

  fs.mkdirSync(fnDir, { recursive: true });
  const middleware = `const USER = ${JSON.stringify(username)};\nconst PASS = ${JSON.stringify(password)};\n\nfunction unauthorized() {\n  return new Response("Authentication required", {\n    status: 401,\n    headers: {\n      "WWW-Authenticate": 'Basic realm="Private Vault", charset="UTF-8"',\n      "Cache-Control": "no-store",\n    },\n  });\n}\n\nexport async function onRequest(context) {\n  const auth = context.request.headers.get("Authorization") || "";\n  if (!auth.startsWith("Basic ")) return unauthorized();\n\n  try {\n    const decoded = atob(auth.slice(6));\n    const [user, ...rest] = decoded.split(":");\n    const pass = rest.join(":");\n\n    if (user !== USER || pass !== PASS) return unauthorized();\n    return context.next();\n  } catch {\n    return unauthorized();\n  }\n}\n`;
  if (DRY_RUN) {
    console.log('[dry-run] write basic auth middleware');
    return;
  }
  fs.writeFileSync(middlewarePath, middleware, 'utf8');
  console.log('Wrote basic auth middleware from config/env ✅');
}

function deploy() {
  const cfg = loadConfig();
  const workspaceDir = expandHome(cfg.publish.workspaceDir);
  ensureBasicAuthMiddleware(workspaceDir, cfg);
  const project = cfg.cloudflare.projectName;
  const branch = cfg.cloudflare.branch || 'main';
  const tokenEnv = cfg.cloudflare?.apiTokenEnv || 'CLOUDFLARE_API_TOKEN';
  const accountEnv = cfg.cloudflare?.accountIdEnv || 'CLOUDFLARE_ACCOUNT_ID';
  const token = process.env[tokenEnv] || '';
  const accountId = process.env[accountEnv] || '';

  if (!token) throw new Error(`Missing Cloudflare token env var: ${tokenEnv}`);

  const envPrefix = [
    `CLOUDFLARE_API_TOKEN="${token.replace(/"/g, '\\"')}"`,
    accountId ? `CLOUDFLARE_ACCOUNT_ID="${accountId.replace(/"/g, '\\"')}"` : ''
  ].filter(Boolean).join(' ');

  sh(`${envPrefix} npx wrangler pages deploy public --project-name "${project}" --branch "${branch}"`, workspaceDir);
  console.log('Deploy complete ✅');
}

function run() {
  setupProject();
  doctor();
  sync();
  build();
  deploy();
}

function help() {
  console.log(`
Usage:
  publishmd-cf.js <command> [--dry-run]

Commands:
  init | wizard | setup-project | doctor | sync | build | deploy | run

Safety env flags:
  ALLOW_DESTRUCTIVE=1   allow fallback setup to clear non-empty workspaceDir
  DRY_RUN=1             print actions without mutating files/deploying
`);
}

(async () => {
  try {
    const map = { init, wizard, 'setup-project': setupProject, doctor, sync, build, deploy, run, help };
    const fn = map[cmd] || help;
    await fn();
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
})();

/**
 * Theotopia (万神殿) god rows inspector — platform-maintainer read-only tool.
 *
 * Counts and sanity-checks the `user_digital_humans` rows with
 * `category = 'theotopia'` via the Supabase REST (PostgREST) API, using a
 * service-role key the maintainer provides. Read-only: GET requests only,
 * nothing is ever written or deleted.
 *
 * Usage:
 *   node check-theotopia-gods.js                    # full census + integrity check
 *   node check-theotopia-gods.js --sample 5         # additionally probe 5 random avatars (HEAD)
 *   node check-theotopia-gods.js --god theotopia-mazu   # inspect a single god by theotopiaId
 *
 * Credentials (never on the command line):
 *   1. Env vars: SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY
 *   2. State-dir file: $POWPOW_STATE_DIR/theotopia.env (or ~/.powpow/theotopia.env),
 *      one KEY=VALUE per line (same format as dotenv)
 *   3. --env-file <path> to point at the file explicitly
 * The key grants full database access — it must stay on the maintainer's
 * machine and never be committed, printed, or passed as an argument.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--sample') args.sample = Number(argv[++i]);
    else if (a === '--god') args.god = argv[++i];
    else if (a === '--env-file') args.envFile = argv[++i];
    else args._.push(a);
  }
  return args;
}

function loadEnvFile(file) {
  const env = {};
  const text = fs.readFileSync(file, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
    if (m && !line.trim().startsWith('#')) env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  return env;
}

function loadCredentials(args) {
  const stateDir = process.env.POWPOW_STATE_DIR || path.join(os.homedir(), '.powpow');
  const candidates = [
    args.envFile,
    path.join(stateDir, 'theotopia.env'),
    path.join(os.homedir(), '.powpow', 'theotopia.env'),
  ].filter(Boolean);
  for (const file of candidates) {
    if (fs.existsSync(file)) {
      const env = loadEnvFile(file);
      if (env.SUPABASE_URL && env.SUPABASE_SERVICE_ROLE_KEY) {
        return { url: env.SUPABASE_URL, key: env.SUPABASE_SERVICE_ROLE_KEY, source: file };
      }
    }
  }
  if (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY) {
    return { url: process.env.SUPABASE_URL, key: process.env.SUPABASE_SERVICE_ROLE_KEY, source: 'environment variables' };
  }
  console.error('❌ Missing Supabase credentials.');
  console.error('   Provide SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY via env vars,');
  console.error(`   or put them in ${path.join(stateDir, 'theotopia.env')} (KEY=VALUE lines).`);
  console.error('   Never pass the key as a command-line argument.');
  process.exitCode = 1;
  return null;
}

async function restGet(creds, query) {
  const res = await fetch(`${creds.url}/rest/v1/user_digital_humans?${query}`, {
    headers: {
      apikey: creds.key,
      Authorization: `Bearer ${creds.key}`,
      Accept: 'application/json',
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Supabase REST ${res.status}: ${text.slice(0, 300)}`);
  }
  return res.json();
}

// Lightweight projection of every theotopia row (220 rows — trivial payload).
const SELECT = [
  'id',
  'name',
  'avatar_url',
  'lat',
  'lng',
  'location_name',
  'search_pinyin',
  'description',
  'volume:model_config->>volume',
  'theotopia_id:model_config->>theotopiaId',
  'persona_profile:model_config->>personaProfile',
  'opening_message:model_config->>openingMessage',
].join(',');

function checkRow(row, problems, i) {
  const tag = `${row.name || '(unnamed)'} [${row.theotopia_id || 'no-id'}]`;
  if (!row.theotopia_id) problems.push([i, tag, 'missing model_config.theotopiaId']);
  if (!row.volume) problems.push([i, tag, 'missing model_config.volume']);
  if (/^\d+\.\s/.test(row.name || '')) problems.push([i, tag, `name has numbering prefix: "${row.name}"`]);
  if (!row.name) problems.push([i, tag, 'empty name']);
  if (!row.avatar_url) problems.push([i, tag, 'empty avatar_url']);
  if (!row.search_pinyin) problems.push([i, tag, 'empty search_pinyin']);
  if (!row.description || row.description.length < 20) problems.push([i, tag, 'description too short']);
  if (!row.persona_profile || row.persona_profile.length < 200) {
    problems.push([i, tag, `persona_profile suspicious (len=${row.persona_profile ? row.persona_profile.length : 0})`]);
  }
  const lat = Number(row.lat);
  const lng = Number(row.lng);
  if (!row.lat || !row.lng || Number.isNaN(lat) || Number.isNaN(lng) || Math.abs(lat) > 90 || Math.abs(lng) > 180) {
    problems.push([i, tag, `bad coordinates (${row.lat}, ${row.lng})`]);
  }
  if (!row.location_name) problems.push([i, tag, 'empty location_name']);
}

async function probeAvatar(url) {
  try {
    const res = await fetch(url, { method: 'HEAD' });
    return res.ok ? `✅ HTTP ${res.status}` : `❌ HTTP ${res.status}`;
  } catch (err) {
    return `❌ ${err.message}`;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const creds = loadCredentials(args);
  if (!creds) return;
  console.log(`=== Theotopia Gods Inspector ===`);
  console.log(`Credentials: ${creds.source}\n`);

  let rows;
  if (args.god) {
    const filter = `${encodeURIComponent('model_config->>theotopiaId')}=eq.${encodeURIComponent(args.god)}`;
    rows = await restGet(creds, `select=${SELECT}&category=eq.theotopia&${filter}`);
    if (rows.length === 0) {
      console.error(`❌ No theotopia god with theotopiaId "${args.god}"`);
      process.exitCode = 1;
      return;
    }
  } else {
    rows = await restGet(creds, `select=${SELECT}&category=eq.theotopia`);
  }

  // 1. Census
  console.log(`1. Census: ${rows.length} theotopia god(s) in user_digital_humans`);
  const byVolume = {};
  for (const r of rows) {
    const v = r.volume || '(no volume)';
    byVolume[v] = (byVolume[v] || 0) + 1;
  }
  for (const [v, n] of Object.entries(byVolume).sort()) console.log(`   ${v}: ${n}`);

  // 2. Duplicate theotopiaId
  const seen = new Map();
  const dupes = [];
  rows.forEach((r, i) => {
    if (r.theotopia_id) {
      if (seen.has(r.theotopia_id)) dupes.push(r.theotopia_id);
      else seen.set(r.theotopia_id, i);
    }
  });
  console.log(`\n2. Duplicate theotopiaId: ${dupes.length === 0 ? '✅ none' : '❌ ' + dupes.join(', ')}`);

  // 3. Per-row integrity
  const problems = [];
  rows.forEach((r, i) => checkRow(r, problems, i));
  console.log(`\n3. Row integrity: ${problems.length === 0 ? '✅ all rows clean' : `❌ ${problems.length} problem(s)`}`);
  for (const [i, tag, msg] of problems.slice(0, 50)) console.log(`   - row ${i + 1} ${tag}: ${msg}`);
  if (problems.length > 50) console.log(`   ... and ${problems.length - 50} more`);

  // 4. Sample probe
  if (args.sample && args.sample > 0 && !args.god) {
    const n = Math.min(args.sample, rows.length);
    console.log(`\n4. Random sample (${n}) — full row + avatar HEAD probe:`);
    const idx = rows.map((_, i) => i);
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [idx[i], idx[j]] = [idx[j], idx[i]];
    }
    for (const i of idx.slice(0, n)) {
      const r = rows[i];
      console.log(`   --- ${r.name} [${r.theotopia_id}] ---`);
      console.log(`   volume: ${r.volume} | location: ${r.location_name} (${r.lat}, ${r.lng})`);
      console.log(`   persona_profile: ${r.persona_profile ? r.persona_profile.length + ' chars' : 'MISSING'}`);
      console.log(`   avatar: ${await probeAvatar(r.avatar_url)}`);
    }
  }

  console.log(`\n=== Done ===`);
  if (args.god && rows.length === 1) {
    const r = rows[0];
    console.log(`Name: ${r.name}`);
    console.log(`Location: ${r.location_name} (${r.lat}, ${r.lng})`);
    console.log(`Avatar: ${r.avatar_url}`);
    console.log(`Search pinyin: ${r.search_pinyin}`);
    console.log(`Description (${r.description.length} chars): ${r.description.slice(0, 120)}...`);
    console.log(`Persona profile: ${r.persona_profile ? r.persona_profile.length + ' chars, head: ' + r.persona_profile.slice(0, 80) + '...' : 'MISSING'}`);
  }
  if (dupes.length > 0 || problems.length > 0) process.exitCode = 1;
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exitCode = 1;
});

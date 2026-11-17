/**
 * Create a digital human and place it on the PowPow map.
 *
 * Platform contract (POST /api/digital-humans, route.ts):
 *   - JWT login required; consumes 2 badges (no refund on delete)
 *   - required: name, description, avatarUrl, lng, lat (locationName optional)
 *   - expires after 30 days (renewal costs another 2 badges)
 *   - conversations with the DH run on PLATFORM compute - the user never
 *     provides any model/API key
 *
 * Avatar (required by the platform) - three strategies:
 *   --avatar generate --avatar-ref <@local-path|URL>
 *       AI text-to-image based on the persona (8~30s). The platform REQUIRES
 *       a reference image URL for this endpoint (used only as fallback).
 *       On generation failure the platform returns a red-ring fallback avatar.
 *   --avatar @<local-path>
 *       Upload a local image and use it directly as the avatar.
 *   --avatar <https://...>
 *       Use an image URL directly (HEAD-checked first).
 *
 * Usage:
 *   node create-digital-human.js --name "岳飞" --desc "人设..." \
 *     --lng 116.4 --lat 39.9 --location-name "北京·地坛" \
 *     --avatar generate --avatar-ref @ref.png [--desc-file <path>] [--json] [--confirm]
 *
 * CONFIRMATION GATE: without --confirm this is a dry-run - it validates the
 * arguments, resolves/uploads NOTHING, and prints the creation plan (exit 3).
 * The agent MUST show the user the plan (name, persona, avatar, location,
 * 2-badge cost, public visibility, no refund) and get an explicit YES before
 * re-running with --confirm.
 */
const fs = require('fs');
const path = require('path');
const { api, requireSession, loadConfig, SessionExpiredError, ApiError, DEFAULT_USER_AGENT, DEFAULT_ACCEPT_LANGUAGE } = require('./lib/api-client');
const { uploadPostImage } = require('./upload-image');
const { checkImageUrl } = require('./search-image');

const BADGES_REQUIRED = 2;
const GENERATE_AVATAR_TIMEOUT_MS = 120000; // measured 8.7~26.5s server-side; api() default 30s is too tight

function parseArgs(argv) {
  const opts = {
    name: null, desc: null, descFile: null,
    lng: null, lat: null, locationName: null,
    avatar: null, avatarRef: null,
    asJson: false,
  };
  for (let i = 0; i < argv.length; i++) {
    switch (argv[i]) {
      case '--name': opts.name = argv[++i]; break;
      case '--desc': opts.desc = argv[++i]; break;
      case '--desc-file': opts.descFile = argv[++i]; break;
      case '--lng': opts.lng = argv[++i]; break;
      case '--lat': opts.lat = argv[++i]; break;
      case '--location-name': opts.locationName = argv[++i]; break;
      case '--avatar': opts.avatar = argv[++i]; break;
      case '--avatar-ref': opts.avatarRef = argv[++i]; break;
      case '--json': opts.asJson = true; break;
      case '--confirm': opts.confirm = true; break;
      default:
        throw new Error(`Unknown argument: ${argv[i]}`);
    }
  }
  return opts;
}

function validate(opts, description) {
  if (!opts.name || !opts.name.trim()) throw new Error('Missing --name (digital human name).');
  if (!description || !description.trim()) throw new Error('Missing persona. Provide --desc "<text>" or --desc-file <path>.');
  const lng = Number(opts.lng);
  const lat = Number(opts.lat);
  if (!Number.isFinite(lng) || lng < -180 || lng > 180) throw new Error(`Invalid --lng "${opts.lng}" (expected number in [-180, 180]).`);
  if (!Number.isFinite(lat) || lat < -90 || lat > 90) throw new Error(`Invalid --lat "${opts.lat}" (expected number in [-90, 90]).`);
  if (!opts.avatar || !opts.avatar.trim()) {
    throw new Error('Missing --avatar. The platform requires an avatar: use "generate" (+ --avatar-ref), @<local-path>, or an image URL.');
  }
  if (opts.avatar === 'generate' && !opts.avatarRef) {
    throw new Error('Avatar "generate" requires --avatar-ref <@local-path|URL> (platform constraint: the AI avatar endpoint needs a reference image).');
  }
  return { lng, lat };
}

/** Upload a local file via the post-image endpoint, or verify a remote URL. Returns a public URL. */
async function resolveImageRef(ref) {
  if (/^https?:\/\//.test(ref)) {
    const check = await checkImageUrl(ref);
    if (!check.ok) throw new Error(`Reference image URL rejected (${check.reason}): ${ref}`);
    return ref;
  }
  const localPath = ref.startsWith('@') ? ref.slice(1) : ref;
  if (!fs.existsSync(localPath) || !fs.statSync(localPath).isFile()) {
    throw new Error(`Reference image not found: ${localPath}`);
  }
  console.log('  ⏳ Uploading reference image...');
  const url = await uploadPostImage(localPath);
  console.log(`  ✅ Reference image uploaded: ${url}`);
  return url;
}

/** Resolve the avatar strategy to a final public avatar URL. */
async function resolveAvatar(opts, description) {
  const strategy = opts.avatar.trim();

  if (strategy === 'generate') {
    const refUrl = await resolveImageRef(opts.avatarRef);
    console.log('  ⏳ Generating AI avatar from the persona (this takes 8~30 seconds)...');
    const config = loadConfig();
    const session = requireSession();
    const resp = await fetch(`${config.platformUrl}/api/digital-humans/generate-avatar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': session.userAgent || DEFAULT_USER_AGENT,
        'Accept-Language': session.acceptLanguage || DEFAULT_ACCEPT_LANGUAGE,
        Authorization: `Bearer ${session.token}`,
      },
      body: JSON.stringify({ name: opts.name.trim(), description: description.trim(), referenceImageUrl: refUrl }),
      signal: AbortSignal.timeout(GENERATE_AVATAR_TIMEOUT_MS),
    });
    const body = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      throw new Error(`Avatar generation failed (HTTP ${resp.status}): ${body.error || 'unknown error'}`);
    }
    if (body.useDefaultAvatar) {
      console.warn('  ⚠️ AI generation failed on the platform side - the server returned a fallback (red-ring) avatar. Continuing; you can change the avatar later on the website.');
    } else {
      console.log('  ✅ AI avatar generated.');
    }
    return { avatarUrl: body.avatarUrl, referenceImageUrl: refUrl };
  }

  if (strategy.startsWith('@') || (fs.existsSync(strategy) && fs.statSync(strategy).isFile())) {
    const localPath = strategy.startsWith('@') ? strategy.slice(1) : strategy;
    console.log('  ⏳ Uploading avatar image...');
    const url = await uploadPostImage(localPath);
    console.log(`  ✅ Avatar uploaded: ${url}`);
    return { avatarUrl: url, referenceImageUrl: null };
  }

  if (/^https?:\/\//.test(strategy)) {
    const check = await checkImageUrl(strategy);
    if (!check.ok) throw new Error(`Avatar URL rejected (${check.reason}): ${strategy}`);
    return { avatarUrl: strategy, referenceImageUrl: null };
  }

  throw new Error(`Unrecognized --avatar value: ${strategy}. Use "generate" (+ --avatar-ref), @<local-path>, or an image URL.`);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));

  let description = opts.desc;
  if (!description && opts.descFile) {
    if (!fs.existsSync(opts.descFile)) throw new Error(`--desc-file not found: ${opts.descFile}`);
    description = fs.readFileSync(opts.descFile, 'utf-8');
  }

  const { lng, lat } = validate(opts, description);

  if (!opts.confirm) {
    // Dry-run gate: print the full creation plan and exit BEFORE touching the
    // network (no session check, no upload, no badge spend).
    console.log('--- DRY RUN (nothing created, 0 badges spent) ---');
    console.log(`Name: ${opts.name.trim()}`);
    console.log(`Persona: ${description.trim().slice(0, 200)}${description.trim().length > 200 ? '...' : ''}`);
    console.log(`Location: ${opts.locationName ? opts.locationName.trim() : '(no name)'} (${lng}, ${lat}) - PUBLIC on the map`);
    console.log(`Avatar strategy: ${opts.avatar}${opts.avatar === 'generate' ? ` (ref: ${opts.avatarRef})` : ''}`);
    console.log(`Cost: ${BADGES_REQUIRED} badges (non-refundable, even if deleted later)`);
    console.log(`Expires: ~30 days after creation (renewal costs another ${BADGES_REQUIRED} badges)`);
    console.log('\nShow the user this plan and ask for explicit confirmation, then re-run with --confirm.');
    process.exitCode = 3;
    return;
  }

  const session = requireSession();

  // Badge pre-check: creating costs BADGES_REQUIRED badges and deletion does
  // NOT refund them - fail fast before uploading anything.
  if (session.userId) {
    const bal = await api('GET', `/api/badges/balance?userId=${session.userId}`);
    const current = bal.balance ? bal.balance.balance : 0;
    if (current < BADGES_REQUIRED) {
      throw new Error(`Badge balance too low: ${current} available, ${BADGES_REQUIRED} required. Earn badges on the platform first (see https://global.powpow.online).`);
    }
    console.log(`  💰 Badge balance: ${current} (creating a digital human consumes ${BADGES_REQUIRED})`);
  } else {
    console.warn('  ⚠️ No userId in session - skipping local badge pre-check (server will still reject if insufficient).');
  }

  const { avatarUrl, referenceImageUrl } = await resolveAvatar(opts, description);

  console.log('  ⏳ Creating digital human...');
  const payload = {
    name: opts.name.trim(),
    description: description.trim(),
    avatarUrl,
    lng,
    lat,
  };
  if (opts.locationName && opts.locationName.trim()) payload.locationName = opts.locationName.trim();
  if (referenceImageUrl) payload.referenceImageUrl = referenceImageUrl;

  const body = await api('POST', '/api/digital-humans', payload);
  const dh = body.digitalHuman || {};
  const badgesRemaining = body.badgesRemaining;

  if (opts.asJson) {
    console.log(JSON.stringify({ success: true, digitalHuman: dh, badgesRemaining }, null, 2));
    return;
  }

  console.log('\n✅ Digital human created!');
  console.log(`   Name: ${dh.name || opts.name}`);
  console.log(`   ID: ${dh.id}`);
  if (dh.locationName || payload.locationName) console.log(`   Location: ${dh.locationName || payload.locationName} (${dh.lng ?? lng}, ${dh.lat ?? lat})`);
  console.log(`   Expires: ${dh.expiresAt || '~30 days from now'} (renewal costs 2 more badges)`);
  if (typeof badgesRemaining === 'number') console.log(`   Badges remaining: ${badgesRemaining}`);
  console.log(`   Map: https://global.powpow.online/map`);
  console.log('\n   Anyone on the map can now chat with it (runs on platform compute, no setup needed).');
  console.log('   To mention it in a post: node scripts/compose.js --dh <id> ...');
}

main().catch(err => {
  if (err instanceof SessionExpiredError) {
    console.error(`❌ ${err.message}`);
    process.exitCode = 2;
    return;
  }
  if (err instanceof ApiError) {
    console.error(`❌ Platform rejected the request: ${err.message}`);
    if (err.body && typeof err.body === 'object' && err.body.error) console.error(`   ${err.body.error}`);
    process.exitCode = 1;
    return;
  }
  console.error(`❌ ${err.message}`);
  process.exitCode = 1;
});

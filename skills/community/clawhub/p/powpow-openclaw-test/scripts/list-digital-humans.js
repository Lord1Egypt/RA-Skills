/**
 * List available digital humans via the platform API with health filtering.
 *
 * Filters out unhealthy entries so the agent never suggests a broken one:
 *  - inactive digital humans
 *  - test accounts (name contains 测试 / test)
 *  - placeholder avatars (default-avatar.png or empty)
 *  - garbled/mojibake names (contains U+FFFD)
 *
 * Usage:
 *   node list-digital-humans.js [search-keyword] [--all] [--limit N] [--json]
 *     --all    include unhealthy entries (for debugging)
 *     --json   machine-readable output
 */
const { api, SessionExpiredError } = require('./lib/api-client');

const TEST_NAME_PATTERN = /(测试|test|机器人测试)/i;
const PLACEHOLDER_AVATAR_PATTERN = /default-avatar\.(png|jpg)/i;

function assessHealth(dh) {
  const issues = [];
  if (!dh.isActive) issues.push('inactive');
  if (!dh.name || TEST_NAME_PATTERN.test(dh.name)) issues.push('test-name');
  if (dh.name && dh.name.includes('\uFFFD')) issues.push('garbled-name');
  if (!dh.avatarUrl || PLACEHOLDER_AVATAR_PATTERN.test(dh.avatarUrl)) issues.push('placeholder-avatar');
  return issues;
}

async function main() {
  const args = process.argv.slice(2);
  const includeAll = args.includes('--all');
  const asJson = args.includes('--json');
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) || 20 : 20;
  const search = args.find(a => !a.startsWith('--') && a !== String(limit)) || '';

  try {
    const query = `/api/digital-humans?scope=all${search ? `&search=${encodeURIComponent(search)}` : ''}`;
    const body = await api('GET', query);
    const all = body.digitalHumans || [];

    const healthy = [];
    const unhealthy = [];
    for (const dh of all) {
      const issues = assessHealth(dh);
      if (issues.length === 0) healthy.push(dh);
      else unhealthy.push({ id: dh.id, name: dh.name, issues });
    }

    if (asJson) {
      console.log(JSON.stringify({
        healthy: healthy.slice(0, limit),
        unhealthyCount: unhealthy.length,
        ...(includeAll ? { unhealthy } : {}),
      }, null, 2));
      return;
    }

    console.log(`Total: ${all.length} | Healthy: ${healthy.length} | Filtered out: ${unhealthy.length}${search ? ` | Search: "${search}"` : ''}\n`);
    healthy.slice(0, limit).forEach((dh, i) => {
      console.log(`${i + 1}. ${dh.name} ${dh.isOwner ? '(mine)' : ''}`);
      console.log(`   ID: ${dh.id}`);
      if (dh.locationName) console.log(`   Location: ${dh.locationName} (${dh.lng}, ${dh.lat})`);
      if (dh.description) console.log(`   Desc: ${dh.description.slice(0, 80)}`);
      console.log('');
    });

    if (includeAll && unhealthy.length > 0) {
      console.log(`Unhealthy entries (${unhealthy.length}):`);
      unhealthy.forEach((u, i) => {
        console.log(`${i + 1}. ${u.name || '(no name)'} | issues: ${u.issues.join(', ')} | ID: ${u.id}`);
      });
      console.log('');
    } else if (unhealthy.length > 0) {
      console.log(`Filtered (unhealthy) entries: ${unhealthy.length}. Use --all to see them.`);
    }
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`❌ Failed to list digital humans: ${err.message}`);
    process.exitCode = 1;
  }
}

main();

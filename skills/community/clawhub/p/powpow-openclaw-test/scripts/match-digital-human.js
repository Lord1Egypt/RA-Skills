/**
 * Suggest digital humans relevant to a topic, via the platform API.
 * Applies the same health filtering as list-digital-humans.js, then ranks
 * remaining candidates by keyword overlap with the topic (shared logic in
 * lib/dh-match.js - name hits weigh 3, description/location hits weigh 1,
 * cross-boundary discipline terms like 文学-in-天文学家 are masked out).
 *
 * Usage:
 *   node match-digital-human.js <topic> [--limit N] [--json]
 */
const { api, SessionExpiredError } = require('./lib/api-client');
const { rankByTopic } = require('./lib/dh-match');

async function main() {
  const args = process.argv.slice(2);
  const asJson = args.includes('--json');
  const limitIdx = args.indexOf('--limit');
  const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) || 3 : 3;
  const topic = args.find(a => !a.startsWith('--')) || '';

  if (!topic) {
    console.error('Usage: node match-digital-human.js <topic> [--limit N] [--json]');
    process.exit(1);
  }

  try {
    const body = await api('GET', '/api/digital-humans?scope=all');
    const ranked = rankByTopic(body.digitalHumans || [], topic).slice(0, limit);

    // Zero-score means pure keyword overlap failed. Returning those as
    // "matches" would mislead the agent into picking an unrelated figure.
    if (ranked.length === 0 || ranked[0].score === 0) {
      console.error(`❌ No healthy digital human matched "${topic}".`);
      console.error('   Try a precise search instead: node scripts/list-digital-humans.js "<name>"');
      process.exitCode = 1;
      return;
    }

    if (asJson) {
      console.log(JSON.stringify(ranked.map(x => ({ ...x.dh, matchScore: x.score })), null, 2));
      return;
    }

    console.log(`Top ${ranked.length} matches for "${topic}":\n`);
    ranked.forEach((x, i) => {
      const dh = x.dh;
      console.log(`${i + 1}. ${dh.name} ${dh.isOwner ? '(mine)' : ''} (match score: ${x.score})`);
      console.log(`   ID: ${dh.id}`);
      if (dh.locationName) console.log(`   Location: ${dh.locationName} (${dh.lng}, ${dh.lat})`);
      if (dh.description) console.log(`   Desc: ${dh.description.slice(0, 80)}`);
      console.log('');
    });
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`❌ Match failed: ${err.message}`);
    process.exitCode = 1;
  }
}

main();

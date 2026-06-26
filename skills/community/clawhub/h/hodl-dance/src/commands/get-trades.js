#!/usr/bin/env node
const { apiFetch } = require('../lib/api');
const { ok, err, stripMongoFields } = require('../lib/output');
const { requireValidAddress } = require('../lib/validators');

const args = process.argv.slice(2);
const address = args[0];
if (!address || address.startsWith('--')) {
  err('Usage: get-trades <tokenAddress> [--type=buy|sell|all] [--limit=50] [--offset=0]', 'MISSING_ARG');
}

requireValidAddress(address, 'tokenAddress');
const flags = Object.fromEntries(
  args.slice(1).filter(a => a.startsWith('--'))
    .map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? 'true']; })
);

(async () => {
  const data = await apiFetch(`/trades/${address.toLowerCase()}`, {
    type:   flags.type   || 'all',
    limit:  flags.limit  || '50',
    offset: flags.offset || '0',
  });

  ok(stripMongoFields(data));
})().catch(e => err(e.message));

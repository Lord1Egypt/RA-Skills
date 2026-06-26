#!/usr/bin/env node
const { apiFetch } = require('../lib/api');
const { ok, err, stripMongoFields } = require('../lib/output');

const args = Object.fromEntries(
  process.argv.slice(2)
    .filter(a => a.startsWith('--'))
    .map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? 'true']; })
);

(async () => {
  const data = await apiFetch('/tokens', {
    sort:      args.sort     || 'newest',
    limit:     args.limit    || '20',
    offset:    args.offset   || '0',
    verified:  args.verified,
    finalized: args.finalized,
    search:    args.search,
  });

  ok({
    tokens: stripMongoFields(data.tokens),
    total:  data.total,
    limit:  data.limit,
    offset: data.offset,
  });
})().catch(e => err(e.message));
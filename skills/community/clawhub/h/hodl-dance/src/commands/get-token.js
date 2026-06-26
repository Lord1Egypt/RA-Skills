#!/usr/bin/env node
const { apiFetch } = require('../lib/api');
const { ok, err, stripMongoFields } = require('../lib/output');
const { requireValidAddress } = require('../lib/validators');

const address = process.argv[2];
if (!address) err('Usage: get-token <tokenAddress>', 'MISSING_ARG');

requireValidAddress(address, 'tokenAddress');

(async () => {
  const data = await apiFetch(`/tokens/${address.toLowerCase()}`);

  ok({
    token: stripMongoFields(data.token),
    recent_trades: stripMongoFields(data.recent_trades),
  });
})().catch(e => err(e.message));
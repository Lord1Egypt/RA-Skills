import { client } from '../client.js';

function groupByTag(transactions) {
  const map = new Map();

  for (const tx of transactions) {
    const tags = tx.tags?.length ? tx.tags.map((t) => t.name) : ['untagged'];
    for (const tag of tags) {
      if (!map.has(tag)) map.set(tag, []);
      map.get(tag).push(tx);
    }
  }

  return [...map.entries()]
    .sort(([a], [b]) =>
      a === 'untagged' ? 1 : b === 'untagged' ? -1 : a.localeCompare(b)
    )
    .map(([tag, txs]) => ({
      tag,
      total_cents: txs.reduce((sum, tx) => sum + tx.amount_cents, 0),
      transactions: txs,
    }));
}

export async function listTransactions({ startDate, endDate, accountId } = {}) {
  const params = new URLSearchParams();
  if (startDate) params.set('start_date', startDate);
  if (endDate) params.set('end_date', endDate);
  if (accountId) params.set('account_id', accountId);
  const query = params.toString();
  return client.get(`/transactions${query ? `?${query}` : ''}`);
}

export async function getTransaction(id) {
  return client.get(`/transactions/${id}`);
}

export async function createTransaction(data) {
  return client.post('/transactions', data);
}

export async function updateTransaction(id, data) {
  return client.put(`/transactions/${id}`, data);
}

export async function deleteTransaction(id, data) {
  return client.del(`/transactions/${id}`, data);
}

// CLI
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const args = process.argv.slice(2);
  const action = args[0];

  function parseFlag(flag) {
    const entry = args.find((a) => a.startsWith(`${flag}=`));
    return entry ? entry.split('=')[1] : undefined;
  }

  const startDate = parseFlag('--start-date');
  const endDate = parseFlag('--end-date');
  const accountId = parseFlag('--account-id');
  const shouldGroupByTag = args.includes('--group-by-tag');
  const positional = args.filter((a) => !a.startsWith('--'));
  const [, arg1, arg2] = positional;

  const actions = {
    list: async () => {
      const result = await listTransactions({ startDate, endDate, accountId });
      return shouldGroupByTag ? groupByTag(result) : result;
    },
    get: () => getTransaction(arg1),
    create: () => createTransaction(JSON.parse(arg1)),
    update: () => updateTransaction(arg1, JSON.parse(arg2)),
    delete: () => deleteTransaction(arg1, arg2 ? JSON.parse(arg2) : undefined),
  };

  if (!action || !actions[action]) {
    console.error('Usage: node src/routes/transactions.js <action> [args]');
    console.error('Actions:');
    console.error('  list [--start-date=YYYY-MM-DD] [--end-date=YYYY-MM-DD] [--account-id=<id>] [--group-by-tag]');
    console.error('  get <id>');
    console.error('  create <json>');
    console.error('  update <id> <json>');
    console.error('  delete <id> [json]  -- json: {"update_future":true} or {"update_all":true}');
    process.exit(1);
  }

  actions[action]()
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((err) => { console.error(err.message); process.exit(1); });
}

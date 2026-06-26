import { client } from '../client.js';

export async function listTransfers({ startDate, endDate } = {}) {
  const params = new URLSearchParams();
  if (startDate) params.set('start_date', startDate);
  if (endDate) params.set('end_date', endDate);
  const query = params.toString();
  return client.get(`/transfers${query ? `?${query}` : ''}`);
}

export async function getTransfer(id) {
  return client.get(`/transfers/${id}`);
}

export async function createTransfer(data) {
  return client.post('/transfers', data);
}

export async function updateTransfer(id, data) {
  return client.put(`/transfers/${id}`, data);
}

export async function deleteTransfer(id) {
  return client.del(`/transfers/${id}`);
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
  const positional = args.filter((a) => !a.startsWith('--'));
  const [, arg1, arg2] = positional;

  const actions = {
    list: () => listTransfers({ startDate, endDate }),
    get: () => getTransfer(arg1),
    create: () => createTransfer(JSON.parse(arg1)),
    update: () => updateTransfer(arg1, JSON.parse(arg2)),
    delete: () => deleteTransfer(arg1),
  };

  if (!action || !actions[action]) {
    console.error('Usage: node src/routes/transfers.js <action> [args]');
    console.error('Actions:');
    console.error('  list [--start-date=YYYY-MM-DD] [--end-date=YYYY-MM-DD]');
    console.error('  get <id>');
    console.error('  create <json>');
    console.error('  update <id> <json>');
    console.error('  delete <id>');
    process.exit(1);
  }

  actions[action]()
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((err) => { console.error(err.message); process.exit(1); });
}

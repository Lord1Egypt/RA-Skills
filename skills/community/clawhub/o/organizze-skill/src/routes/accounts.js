import { client } from '../client.js';

export async function listAccounts() {
  return client.get('/accounts');
}

export async function getAccount(id) {
  return client.get(`/accounts/${id}`);
}

export async function createAccount(data) {
  return client.post('/accounts', data);
}

export async function updateAccount(id, data) {
  return client.put(`/accounts/${id}`, data);
}

export async function deleteAccount(id) {
  return client.del(`/accounts/${id}`);
}

// CLI
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const [action, arg1, arg2] = process.argv.slice(2);

  const actions = {
    list: () => listAccounts(),
    get: () => getAccount(arg1),
    create: () => createAccount(JSON.parse(arg1)),
    update: () => updateAccount(arg1, JSON.parse(arg2)),
    delete: () => deleteAccount(arg1),
  };

  if (!action || !actions[action]) {
    console.error('Usage: node src/routes/accounts.js <action> [args]');
    console.error('Actions: list | get <id> | create <json> | update <id> <json> | delete <id>');
    process.exit(1);
  }

  actions[action]()
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((err) => { console.error(err.message); process.exit(1); });
}

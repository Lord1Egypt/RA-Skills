import { client } from '../client.js';

export async function listCategories() {
  return client.get('/categories');
}

export async function getCategory(id) {
  return client.get(`/categories/${id}`);
}

export async function createCategory(data) {
  return client.post('/categories', data);
}

export async function updateCategory(id, data) {
  return client.put(`/categories/${id}`, data);
}

export async function deleteCategory(id, data) {
  return client.del(`/categories/${id}`, data);
}

// CLI
if (process.argv[1] === new URL(import.meta.url).pathname) {
  const [action, arg1, arg2] = process.argv.slice(2);

  const actions = {
    list: () => listCategories(),
    get: () => getCategory(arg1),
    create: () => createCategory(JSON.parse(arg1)),
    update: () => updateCategory(arg1, JSON.parse(arg2)),
    delete: () => deleteCategory(arg1, arg2 ? JSON.parse(arg2) : undefined),
  };

  if (!action || !actions[action]) {
    console.error('Usage: node src/routes/categories.js <action> [args]');
    console.error('Actions: list | get <id> | create <json> | update <id> <json> | delete <id> [json]');
    console.error('  delete accepts optional json with replacement_id: \'{"replacement_id":18}\'');
    process.exit(1);
  }

  actions[action]()
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((err) => { console.error(err.message); process.exit(1); });
}

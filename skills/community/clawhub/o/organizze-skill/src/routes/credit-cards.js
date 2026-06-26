import { client } from '../client.js';

export async function listCreditCards() {
  return client.get('/credit_cards');
}

export async function getCreditCard(id) {
  return client.get(`/credit_cards/${id}`);
}

export async function createCreditCard(data) {
  return client.post('/credit_cards', data);
}

export async function updateCreditCard(id, data) {
  return client.put(`/credit_cards/${id}`, data);
}

export async function deleteCreditCard(id) {
  return client.del(`/credit_cards/${id}`);
}

export async function listInvoices(creditCardId, { startDate, endDate } = {}) {
  const params = new URLSearchParams();
  if (startDate) params.set('start_date', startDate);
  if (endDate) params.set('end_date', endDate);
  const query = params.toString();
  return client.get(`/credit_cards/${creditCardId}/invoices${query ? `?${query}` : ''}`);
}

export async function getInvoice(creditCardId, invoiceId) {
  return client.get(`/credit_cards/${creditCardId}/invoices/${invoiceId}`);
}

export async function getInvoicePayments(creditCardId, invoiceId) {
  return client.get(`/credit_cards/${creditCardId}/invoices/${invoiceId}/payments`);
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
    list: () => listCreditCards(),
    get: () => getCreditCard(arg1),
    create: () => createCreditCard(JSON.parse(arg1)),
    update: () => updateCreditCard(arg1, JSON.parse(arg2)),
    delete: () => deleteCreditCard(arg1),
    'list-invoices': () => listInvoices(arg1, { startDate, endDate }),
    'get-invoice': () => getInvoice(arg1, arg2),
    'get-payments': () => getInvoicePayments(arg1, arg2),
  };

  if (!action || !actions[action]) {
    console.error('Usage: node src/routes/credit-cards.js <action> [args]');
    console.error('Actions:');
    console.error('  list');
    console.error('  get <id>');
    console.error('  create <json>');
    console.error('  update <id> <json>');
    console.error('  delete <id>');
    console.error('  list-invoices <credit_card_id> [--start-date=YYYY-MM-DD] [--end-date=YYYY-MM-DD]');
    console.error('  get-invoice <credit_card_id> <invoice_id>');
    console.error('  get-payments <credit_card_id> <invoice_id>');
    process.exit(1);
  }

  actions[action]()
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((err) => { console.error(err.message); process.exit(1); });
}

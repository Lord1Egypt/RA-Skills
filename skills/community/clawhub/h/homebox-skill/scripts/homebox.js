#!/usr/bin/env node
const BASE_URL = process.env.HOMEBOX_BASE_URL;
const TOKEN = process.env.HOMEBOX_TOKEN;
let API_VERSION = process.env.HOMEBOX_API_VERSION || 'auto';

const cmd = process.argv[2];
const args = process.argv.slice(3);

const PATHS = {
  v1: {
    items:      '/api/v1/items',
    item:       (id) => `/api/v1/items/${id}`,
    labels:     '/api/v1/labels',
    label:      (id) => `/api/v1/labels/${id}`,
    locations:  '/api/v1/locations',
    location:   (id) => `/api/v1/locations/${id}`,
    tree:       '/api/v1/locations/tree',
    stats:      '/api/v1/groups/statistics',
    statsLabels:'/api/v1/groups/statistics/labels',
    statsLoc:   '/api/v1/groups/statistics/locations',
    statsPrice: '/api/v1/groups/statistics/purchase-price',
    itemExport: '/api/v1/items/export',
    itemImport: '/api/v1/items/import',
    itemFields: '/api/v1/items/fields',
    fieldValues:'/api/v1/items/fields/values',
    duplicate:  (id) => `/api/v1/items/${id}/duplicate`,
    path:       (id) => `/api/v1/items/${id}/path`,
    attach:     (id) => `/api/v1/items/${id}/attachments`,
    attachItem: (id, aid) => `/api/v1/items/${id}/attachments/${aid}`,
    maint:      (id) => `/api/v1/items/${id}/maintenance`,
    notifiers:  '/api/v1/notifiers',
    notifier:   (id) => `/api/v1/notifiers/${id}`,
    assets:     (id) => `/api/v1/assets/${id}`,
    barcode:    '/api/v1/products/search-from-barcode',
    qrcode:     '/api/v1/qrcode',
    report:     '/api/v1/reporting/bill-of-materials',
    group:      '/api/v1/groups',
    groupInv:   '/api/v1/groups/invitations',
    refresh:    '/api/v1/users/refresh',
    self:       '/api/v1/users/self',
    login:      '/api/v1/users/login',
    logout:     '/api/v1/users/logout',
    register:   '/api/v1/users/register',
    chpwd:      '/api/v1/users/change-password',
    currency:   '/api/v1/currency',
    status:     '/api/v1/status',
  },
  v2: {
    items:      '/api/v1/entities',
    item:       (id) => `/api/v1/entities/${id}`,
    labels:     '/api/v1/tags',
    label:      (id) => `/api/v1/tags/${id}`,
    locations:  '/api/v1/entities',
    location:   (id) => `/api/v1/entities/${id}`,
    tree:       '/api/v1/entities/tree',
    stats:      '/api/v1/groups/statistics',
    statsLabels:'/api/v1/groups/statistics/tags',
    statsLoc:   '/api/v1/groups/statistics/locations',
    statsPrice: '/api/v1/groups/statistics/purchase-price',
    itemExport: '/api/v1/entities/export',
    itemImport: '/api/v1/entities/import',
    itemFields: '/api/v1/entities/fields',
    fieldValues:'/api/v1/entities/fields/values',
    duplicate:  (id) => `/api/v1/entities/${id}/duplicate`,
    path:       (id) => `/api/v1/entities/${id}/path`,
    attach:     (id) => `/api/v1/entities/${id}/attachments`,
    attachItem: (id, aid) => `/api/v1/entities/${id}/attachments/${aid}`,
    maint:      (id) => `/api/v1/entities/${id}/maintenance`,
    notifiers:  '/api/v1/notifiers',
    notifier:   (id) => `/api/v1/notifiers/${id}`,
    assets:     (id) => `/api/v1/assets/${id}`,
    barcode:    '/api/v1/products/search-from-barcode',
    qrcode:     '/api/v1/qrcode',
    report:     '/api/v1/reporting/bill-of-materials',
    group:      '/api/v1/groups',
    groupInv:   '/api/v1/groups/invitations',
    refresh:    '/api/v1/users/refresh',
    self:       '/api/v1/users/self',
    login:      '/api/v1/users/login',
    logout:     '/api/v1/users/logout',
    register:   '/api/v1/users/register',
    chpwd:      '/api/v1/users/change-password',
    currency:   '/api/v1/currency',
    status:     '/api/v1/status',
  }
};

async function detectVersion() {
  if (API_VERSION === 'auto') {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/entities`, {
        headers: { Authorization: `Bearer ${TOKEN}` }
      });
      API_VERSION = res.ok ? 'v2' : 'v1';
    } catch {
      API_VERSION = 'v1';
    }
  }
  return API_VERSION;
}

function p(name, ...args) {
  const v = API_VERSION === 'auto' ? 'v1' : API_VERSION;
  const entry = PATHS[v][name];
  return typeof entry === 'function' ? entry(...args) : entry;
}

async function api(method, path, body) {
  const url = `${BASE_URL}${path}`;
  const opts = { method, headers: {} };
  if (TOKEN) opts.headers.Authorization = `Bearer ${TOKEN}`;
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(url, opts);
  if (res.status === 204) return null;
  const text = await res.text();
  if (!res.ok) {
    try { const j = JSON.parse(text); console.error(`Error ${res.status}:`, j); }
    catch { console.error(`Error ${res.status}: ${text}`); }
    process.exit(1);
  }
  try { return JSON.parse(text); }
  catch { return text; }
}

function print(data) {
  console.log(JSON.stringify(data, null, 2));
}

function parseFlags() {
  const body = {};
  for (let i = 0; i < args.length; i++) {
    if (!args[i] || !args[i].startsWith('--')) continue;
    const key = args[i].replace(/^--/, '');
    if (i + 1 >= args.length) break;
    const val = args[i + 1];
    i++; // skip value on next iteration
    if (key === 'tagIds' || key === 'labelIds') {
      const tagKey = API_VERSION === 'v2' ? 'tagIds' : 'labelIds';
      body[tagKey] = val ? val.split(',').filter(Boolean) : [];
    } else if (key === 'locationId') {
      if (API_VERSION === 'v1') body.locationId = val;
      else body.parentId = val;
    } else if (key === 'quantity') {
      body[key] = parseInt(val, 10);
    } else if (['purchasePrice', 'soldPrice', 'cost'].includes(key)) {
      body[key] = val ? parseFloat(val) : null;
    } else if (['insured', 'lifetimeWarranty', 'archived', 'syncChildItemsLocations',
                'syncChildEntityLocations', 'isActive', 'primary'].includes(key)) {
      body[key] = val === 'true';
    } else {
      body[key] = val;
    }
  }
  return body;
}

function showItemSummary(data, version) {
  const items = data.items || data;
  if (!Array.isArray(items)) { print(data); return; }
  if (items.length === 0) { console.log('No items found'); return; }
  items.forEach(item => {
    const loc = version === 'v1'
      ? (item.location?.name || '')
      : (item.entityType?.name || '');
    const tags = version === 'v1'
      ? (item.labels || []).map(l => l.name).join(', ')
      : (item.tags || []).map(t => t.name).join(', ');
    console.log(`${item.id.substring(0,8)}  ${item.name.padEnd(30)} ${loc.padEnd(15)} [${tags}]  qty:${item.quantity}`);
  });
  if (data.total !== undefined) {
    console.log(`\nTotal: ${data.total}  Page: ${data.page}/${Math.ceil(data.total / (data.pageSize || 20))}`);
  }
}

async function main() {
  if (!cmd || cmd === '--help' || cmd === '-h' || cmd === 'help') {
    showHelp();
    return;
  }
  if (!BASE_URL) {
    console.error('Set HOMEBOX_BASE_URL environment variable');
    process.exit(1);
  }

  if (TOKEN && API_VERSION === 'auto') {
    await detectVersion();
  }

  switch (cmd) {
    // --- Search ---
    case 'search':
    case 'find': {
      const q = args[0] || '';
      const params = new URLSearchParams();
      if (q) params.set('q', q);
      applyPaginationFlag(params, 'page');
      applyPaginationFlag(params, 'pageSize');
      if (args.includes('--tags')) {
        const idx = args.indexOf('--tags');
        params.set('tags', args[idx + 1]);
      }
      if (args.includes('--parents')) {
        const idx = args.indexOf('--parents');
        params.set('parentIds', args[idx + 1]);
      }
      const qs = params.toString();
      const data = await api('GET', `${p('items')}${qs ? '?' + qs : ''}`);
      showItemSummary(data, API_VERSION);
      break;
    }

    case 'list': {
      const params = new URLSearchParams({ pageSize: '100' });
      applyPaginationFlag(params, 'pageSize');
      const data = await api('GET', `${p('items')}?${params}`);
      showItemSummary(data, API_VERSION);
      break;
    }

    // --- Get single item ---
    case 'get': {
      if (!args[0]) { console.error('Usage: homebox.js get <id>'); process.exit(1); }
      print(await api('GET', p('item', args[0])));
      break;
    }

    // --- Add item ---
    case 'add': {
      const name = args[0];
      if (!name) { console.error('Usage: homebox.js add <name> [--field value ...]'); process.exit(1); }
      const body = { name, quantity: 1 };
      Object.assign(body, parseFlags());
      print(await api('POST', p('items'), body));
      break;
    }

    // --- Update item ---
    case 'update': {
      const id = args[0];
      if (!id) { console.error('Usage: homebox.js update <id> [--field value ...]'); process.exit(1); }
      const existing = await api('GET', p('item', id));
      let body;
      if (API_VERSION === 'v1') {
        body = {
          id: existing.id,
          name: existing.name,
          description: existing.description || '',
          locationId: existing.location?.id || '',
          parentId: existing.parentId || null,
          quantity: existing.quantity ?? 0,
          archived: existing.archived || false,
          insured: existing.insured || false,
          lifetimeWarranty: existing.lifetimeWarranty || false,
          manufacturer: existing.manufacturer || '',
          modelNumber: existing.modelNumber || '',
          serialNumber: existing.serialNumber || '',
          notes: existing.notes || '',
          purchaseTime: existing.purchaseTime || '',
          purchaseFrom: existing.purchaseFrom || '',
          purchasePrice: existing.purchasePrice ?? null,
          warrantyDetails: existing.warrantyDetails || '',
          warrantyExpires: existing.warrantyExpires || '',
          soldTime: existing.soldTime || '',
          soldPrice: existing.soldPrice ?? null,
          soldTo: existing.soldTo || '',
          soldNotes: existing.soldNotes || '',
          syncChildItemsLocations: existing.syncChildItemsLocations || false,
          labelIds: (existing.labels || []).map(l => l.id),
        };
      } else {
        body = {
          id: existing.id,
          name: existing.name,
          description: existing.description || '',
          entityTypeId: existing.entityType?.id || '',
          parentId: existing.parentId || null,
          quantity: existing.quantity || 1,
          archived: existing.archived || false,
          insured: existing.insured || false,
          lifetimeWarranty: existing.lifetimeWarranty || false,
          manufacturer: existing.manufacturer || '',
          modelNumber: existing.modelNumber || '',
          serialNumber: existing.serialNumber || '',
          notes: existing.notes || '',
          purchaseDate: existing.purchaseDate || '',
          purchaseFrom: existing.purchaseFrom || '',
          purchasePrice: existing.purchasePrice ?? null,
          warrantyDetails: existing.warrantyDetails || '',
          warrantyExpires: existing.warrantyExpires || '',
          soldDate: existing.soldDate || '',
          soldPrice: existing.soldPrice ?? null,
          soldTo: existing.soldTo || '',
          soldNotes: existing.soldNotes || '',
          syncChildEntityLocations: existing.syncChildEntityLocations || false,
          tagIds: (existing.tags || []).map(t => t.id),
        };
      }
      // Override with CLI flags
      const flags = parseFlags();
      Object.assign(body, flags);
      print(await api('PUT', p('item', id), body));
      break;
    }

    // --- Patch item ---
    case 'patch': {
      const id = args[0];
      if (!id) { console.error('Usage: homebox.js patch <id> --field value [...]'); process.exit(1); }
      const body = parseFlags();
      if (API_VERSION === 'v1') {
        // Old API PATCH is very limited — only id and quantity
        body.id = id;
      }
      print(await api('PATCH', p('item', id), body));
      break;
    }

    // --- Delete item ---
    case 'delete':
    case 'remove': {
      if (!args[0]) { console.error('Usage: homebox.js delete <id>'); process.exit(1); }
      await api('DELETE', p('item', args[0]));
      console.log('Deleted');
      break;
    }

    // --- Locations ---
    case 'locations': {
      const data = await api('GET', p('locations'));
      print(data);
      break;
    }

    case 'tree': {
      const data = await api('GET', p('tree'));
      print(data);
      break;
    }

    case 'location-create': {
      const name = args[0];
      if (!name) { console.error('Usage: homebox.js location-create <name> [--description desc] [--parentId id]'); process.exit(1); }
      const body = { name, ...parseFlags() };
      if (API_VERSION === 'v2') {
        // In v2, locations are entities with isLocation entity type
        body.entityTypeId = args.includes('--entityTypeId')
          ? args[args.indexOf('--entityTypeId') + 1]
          : '';
      }
      print(await api('POST', API_VERSION === 'v1' ? p('locations') : p('items'), body));
      break;
    }

    // --- Labels / Tags ---
    case 'labels':
    case 'tags': {
      print(await api('GET', p('labels')));
      break;
    }

    case 'label-create':
    case 'tag-create': {
      const name = args[0];
      if (!name) { console.error(`Usage: homebox.js ${cmd} <name> [--description desc] [--color color]`); process.exit(1); }
      const body = { name, ...parseFlags() };
      print(await api('POST', p('labels'), body));
      break;
    }

    case 'label-delete':
    case 'tag-delete': {
      if (!args[0]) { console.error(`Usage: homebox.js ${cmd} <id>`); process.exit(1); }
      await api('DELETE', p('label', args[0]));
      console.log('Deleted');
      break;
    }

    // --- Entity Types (v2 only) ---
    case 'types': {
      const data = await api('GET', '/api/v1/entity-types');
      print(data);
      break;
    }

    case 'type-create': {
      const name = args[0];
      if (!name) { console.error('Usage: homebox.js type-create <name> [--description desc] [--isLocation true]'); process.exit(1); }
      const body = { name, ...parseFlags() };
      print(await api('POST', '/api/v1/entity-types', body));
      break;
    }

    // --- Statistics ---
    case 'stats': {
      const sub = args[0] || '';
      let path;
      if (sub === 'labels' || sub === 'tags') path = p('statsLabels');
      else if (sub === 'locations') path = p('statsLoc');
      else if (sub === 'purchase-price' || sub === 'price') path = p('statsPrice');
      else path = p('stats');
      print(await api('GET', path));
      break;
    }

    // --- Login ---
    case 'login': {
      const username = args[0];
      if (!username) { console.error('Usage: homebox.js login <username>'); process.exit(1); }
      const pwIdx = args.indexOf('--password');
      const password = pwIdx >= 0 ? args[pwIdx + 1] : (args[1] || '');
      const params = new URLSearchParams();
      params.set('username', username);
      params.set('password', password);
      params.set('stayLoggedIn', 'true');
      const res = await fetch(`${BASE_URL}${p('login')}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: params,
      });
      const data = await res.json();
      if (!res.ok) { console.error('Login failed:', data); process.exit(1); }
      console.log(`Token: ${data.token}`);
      console.log(`Expires: ${data.expiresAt}`);
      break;
    }

    // --- Status ---
    case 'status':
      print(await api('GET', p('status')));
      break;

    // --- Group info ---
    case 'group':
      print(await api('GET', p('group')));
      break;

    default:
      console.error(`Unknown command: ${cmd}`);
      showHelp();
      process.exit(1);
  }
}

function applyPaginationFlag(params, name) {
  if (args.includes(`--${name}`)) {
    const idx = args.indexOf(`--${name}`);
    params.set(name, args[idx + 1]);
  }
}

function showHelp() {
  const v = API_VERSION === 'v2' ? 'v2' : 'v1';
  console.log(`
HomeBox CLI v1/v2 — Manage your home inventory via the HomeBox REST API.
Auto-detects API version (hay-kot v1 or sysadminsmedia v2).

Usage:
  node {baseDir}/scripts/homebox.js <command> [options]

Environment:
  HOMEBOX_BASE_URL   Your HomeBox server URL (required)
  HOMEBOX_TOKEN      API bearer token (required except login)
  HOMEBOX_API_VERSION  Set to "v1" or "v2" to skip auto-detect

Commands (detected version: ${v}):
  search|find [query]         Search items by name/keyword
    --page <n>                Page number
    --pageSize <n>            Items per page
    --tags <id1,id2>          Filter by tag/label IDs (v2/v1)
    --parents <id1,id2>       Filter by parent/location IDs

  list                        List all items (paginated)
  get <id>                    Get full item details
  add <name>                  Add a new item
    --description <text>      Item description
    --locationId <id>         Location ID (v1) or parent/location (v2)
    --parentId <id>           Parent item ID
    --entityTypeId <id>       Entity type ID (v2 only)
    --quantity <n>            Quantity
    --manufacturer <text>     Manufacturer
    --modelNumber <text>      Model number
    --serialNumber <text>     Serial number
    --purchasePrice <num>     Purchase price
    --purchaseDate <date>     Purchase date (v2) / --purchaseTime (v1)
    --purchaseFrom <text>     Purchased from
    --notes <text>            Notes
    --insured <true|false>    Insured?
    --lifetimeWarranty <bool> Lifetime warranty?
    --warrantyDetails <text>  Warranty details
    --warrantyExpires <date>  Warranty expiration
    --tagIds <id1,id2>        Tag IDs (v2) / label IDs (v1)
    --soldPrice <num>         Sold price
    --soldDate <date>         Sold date (v2) / --soldTime (v1)
    --soldTo <text>           Sold to
    --soldNotes <text>        Sold notes

  update <id>                 Update an item (merges with existing)
    (same flags as add)

  patch <id>                  Partial update
    (same flags as add; v1 only supports quantity)

  delete|remove <id>          Delete an item

  locations                   List all locations
  tree                        Show location hierarchy tree
  location-create <name>      Create a new location
    --description <text>      Description
    --parentId <id>           Parent location

  labels|tags                 List all labels (v1) / tags (v2)
  label-create|tag-create <name>  Create label/tag
    --description <text>      Description
    --color <text>            Color

  label-delete|tag-delete <id>  Delete label/tag

  types                       List entity types (v2 only)
  type-create <name>          Create entity type (v2 only)

  stats [sub]                 Statistics (sub: tags, locations, price)

  group                       View group info
  login <username>            Authenticate and get API token
  status                      Check server status
`);
}

main().catch(err => { console.error(err.message); process.exit(1); });

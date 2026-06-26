#!/usr/bin/env node
/**
 * МойСклад CLI — OpenClaw skill helper
 * Usage: node scripts/moysklad.mjs <command> [options]
 *
 * Requires: MOYSKLAD_LOGIN + MOYSKLAD_PASSWORD, or MOYSKLAD_TOKEN
 */

const BASE_URL = "https://api.moysklad.ru/api/remap/1.2";

// ─── Auth ────────────────────────────────────────────────────────────────────

function getAuthHeader() {
  if (process.env.MOYSKLAD_TOKEN) {
    return `Bearer ${process.env.MOYSKLAD_TOKEN}`;
  }
  const login = process.env.MOYSKLAD_LOGIN;
  const password = process.env.MOYSKLAD_PASSWORD;
  if (!login || !password) {
    console.error(
      "Error: Set MOYSKLAD_LOGIN + MOYSKLAD_PASSWORD or MOYSKLAD_TOKEN environment variables."
    );
    process.exit(1);
  }
  return `Basic ${Buffer.from(`${login}:${password}`).toString("base64")}`;
}

// ─── HTTP ────────────────────────────────────────────────────────────────────

async function api(method, path, body) {
  const url = path.startsWith("http") ? path : `${BASE_URL}${path}`;
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: getAuthHeader(),
      "Content-Type": "application/json",
      "Accept-Encoding": "gzip",
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) {
    const msg = data?.errors?.[0]?.error ?? res.statusText;
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  return data;
}

// ─── Output ──────────────────────────────────────────────────────────────────

let jsonMode = false;

function out(data) {
  if (jsonMode) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    if (typeof data === "string") {
      console.log(data);
    } else if (Array.isArray(data)) {
      for (const item of data) console.log(formatItem(item));
    } else {
      console.log(formatItem(data));
    }
  }
}

function formatItem(item) {
  const parts = [];
  if (item.id) parts.push(item.id.substring(0, 8) + "…");
  if (item.name) parts.push(item.name);
  if (item.inn) parts.push(`ИНН: ${item.inn}`);
  if (item.article) parts.push(`арт: ${item.article}`);
  if (item.code) parts.push(`код: ${item.code}`);
  if (item.stock !== undefined) parts.push(`остаток: ${item.stock}`);
  if (item.sum !== undefined) parts.push(`сумма: ${(item.sum / 100).toFixed(2)} руб.`);
  if (item.moment) parts.push(item.moment);
  return parts.join(" | ");
}

// ─── Arg parsing ─────────────────────────────────────────────────────────────

function parseArgs(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json") {
      jsonMode = true;
    } else if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
      flags[key] = val;
    } else {
      positional.push(args[i]);
    }
  }
  return { flags, positional };
}

function qs(params) {
  const parts = [];
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") {
      parts.push(`${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
    }
  }
  return parts.length ? "?" + parts.join("&") : "";
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function cmdMe() {
  const employee = await api("GET", "/context/employee");
  out({
    name: employee.name,
    email: employee.email,
    id: employee.id,
  });
}

async function cmdProducts(flags) {
  const q = qs({
    limit: flags.limit ?? 100,
    offset: flags.offset ?? 0,
    search: flags.search,
    filter: flags.filter,
    order: flags.order ?? "name,asc",
  });
  const result = await api("GET", `/entity/product${q}`);
  if (!jsonMode) console.log(`Товаров: ${result.meta.size} (показаны ${result.rows.length})`);
  out(result.rows);
}

async function cmdProductGet(id) {
  if (!id) { console.error("Usage: product-get <id>"); process.exit(1); }
  const product = await api("GET", `/entity/product/${id}`);
  out(product);
}

async function cmdCounterparties(flags) {
  const q = qs({
    limit: flags.limit ?? 100,
    offset: flags.offset ?? 0,
    search: flags.search,
    filter: flags.filter,
    order: flags.order ?? "name,asc",
  });
  const result = await api("GET", `/entity/counterparty${q}`);
  if (!jsonMode) console.log(`Контрагентов: ${result.meta.size} (показаны ${result.rows.length})`);
  out(result.rows);
}

async function cmdCreateCounterparty(flags) {
  if (!flags.name) { console.error("Usage: create-counterparty --name <name> [--inn <inn>] [--phone <phone>] [--email <email>]"); process.exit(1); }
  const body = {
    name: flags.name,
    companyType: flags["company-type"] ?? "legal",
  };
  if (flags.inn) body.inn = flags.inn;
  if (flags.kpp) body.kpp = flags.kpp;
  if (flags.phone) body.phone = flags.phone;
  if (flags.email) body.email = flags.email;
  if (flags.address) body.legalAddress = flags.address;

  const result = await api("POST", "/entity/counterparty", body);
  if (!jsonMode) console.log(`Создан контрагент: ${result.id} | ${result.name}`);
  out(result);
}

async function cmdOrders(flags) {
  const q = qs({
    limit: flags.limit ?? 100,
    offset: flags.offset ?? 0,
    filter: flags.filter,
    order: flags.order ?? "moment,desc",
  });
  const result = await api("GET", `/entity/customerorder${q}`);
  if (!jsonMode) console.log(`Заказов: ${result.meta.size} (показаны ${result.rows.length})`);
  out(result.rows);
}

async function cmdOrderGet(id) {
  if (!id) { console.error("Usage: order-get <id>"); process.exit(1); }
  const order = await api("GET", `/entity/customerorder/${id}?expand=agent,positions.assortment`);
  out(order);
}

async function cmdCreateOrder(flags) {
  if (!flags["counterparty-id"]) { console.error("--counterparty-id required"); process.exit(1); }
  if (!flags["product-id"]) { console.error("--product-id required"); process.exit(1); }

  // Get org
  const orgs = await api("GET", "/entity/organization?limit=1");
  if (!orgs.rows.length) { console.error("No organizations found"); process.exit(1); }
  const org = orgs.rows[0];

  const counterpartyHref = `${BASE_URL}/entity/counterparty/${flags["counterparty-id"]}`;
  const productHref = `${BASE_URL}/entity/product/${flags["product-id"]}`;
  const quantity = parseFloat(flags.quantity ?? "1");
  const priceKop = Math.round(parseFloat(flags.price ?? "0") * 100);

  const body = {
    organization: { meta: org.meta },
    agent: { meta: { href: counterpartyHref, type: "counterparty", mediaType: "application/json" } },
    positions: [
      {
        quantity,
        price: priceKop,
        assortment: { meta: { href: productHref, type: "product", mediaType: "application/json" } },
      },
    ],
  };
  if (flags.description) body.description = flags.description;

  const result = await api("POST", "/entity/customerorder", body);
  if (!jsonMode) console.log(`Создан заказ: ${result.id} | ${result.name} | ${(result.sum / 100).toFixed(2)} руб.`);
  out(result);
}

async function cmdStores() {
  const result = await api("GET", "/entity/store?limit=100");
  out(result.rows);
}

async function cmdStock(flags) {
  const filterParts = [];
  if (flags["store-id"]) {
    filterParts.push(`store=${BASE_URL}/entity/store/${flags["store-id"]}`);
  }
  if (flags["product-id"]) {
    filterParts.push(`product=${BASE_URL}/entity/product/${flags["product-id"]}`);
  }
  const q = qs({
    limit: flags.limit ?? 1000,
    filter: filterParts.join(";") || undefined,
  });
  const result = await api("GET", `/report/stock/all${q}`);
  if (!jsonMode) {
    for (const item of result.rows) {
      if (item.stock !== 0 || flags.all) {
        console.log(`${item.name} | склад: ${item.store?.name ?? "—"} | остаток: ${item.stock} | резерв: ${item.reserve ?? 0}`);
      }
    }
  } else {
    out(result.rows);
  }
}

async function cmdInvoices(flags) {
  const q = qs({
    limit: flags.limit ?? 100,
    offset: flags.offset ?? 0,
    filter: flags.filter,
    order: flags.order ?? "moment,desc",
  });
  const result = await api("GET", `/entity/invoiceout${q}`);
  if (!jsonMode) console.log(`Счетов: ${result.meta.size} (показаны ${result.rows.length})`);
  out(result.rows);
}

async function cmdInvoiceGet(id) {
  if (!id) { console.error("Usage: invoice-get <id>"); process.exit(1); }
  const invoice = await api("GET", `/entity/invoiceout/${id}?expand=agent,positions.assortment`);
  out(invoice);
}

async function cmdApi(positional) {
  const [method, path, bodyStr] = positional;
  if (!method || !path) {
    console.error("Usage: api <METHOD> <path> [json-body]");
    process.exit(1);
  }
  const body = bodyStr ? JSON.parse(bodyStr) : undefined;
  const result = await api(method.toUpperCase(), path, body);
  out(result);
}

// ─── Main ────────────────────────────────────────────────────────────────────

const [, , command, ...rest] = process.argv;
const { flags, positional } = parseArgs(rest);

if (!command || command === "--help" || command === "-h") {
  console.log(`
МойСклад CLI

Usage: node scripts/moysklad.mjs <command> [options]

Commands:
  me                              Текущий пользователь
  products                        Список товаров
  product-get <id>                Товар по ID
  counterparties                  Список контрагентов
  create-counterparty             Создать контрагента
  orders                          Список заказов покупателей
  order-get <id>                  Заказ по ID
  create-order                    Создать заказ покупателя
  stores                          Список складов
  stock                           Отчёт по остаткам
  invoices                        Список счетов покупателям
  invoice-get <id>                Счёт по ID
  api <METHOD> <path> [body]      Прямой API-запрос

Options:
  --json                  Вывод в JSON
  --search <text>         Поиск
  --limit <n>             Кол-во записей (default: 100)
  --offset <n>            Смещение
  --filter <expr>         Фильтр (напр. archived=false)
  --order <field,dir>     Сортировка

Env vars:
  MOYSKLAD_LOGIN          Логин
  MOYSKLAD_PASSWORD       Пароль
  MOYSKLAD_TOKEN          Bearer-токен (альтернатива логину/паролю)
`);
  process.exit(0);
}

try {
  switch (command) {
    case "me":               await cmdMe(); break;
    case "products":         await cmdProducts(flags); break;
    case "product-get":      await cmdProductGet(positional[0]); break;
    case "counterparties":   await cmdCounterparties(flags); break;
    case "create-counterparty": await cmdCreateCounterparty(flags); break;
    case "orders":           await cmdOrders(flags); break;
    case "order-get":        await cmdOrderGet(positional[0]); break;
    case "create-order":     await cmdCreateOrder(flags); break;
    case "stores":           await cmdStores(); break;
    case "stock":            await cmdStock(flags); break;
    case "invoices":         await cmdInvoices(flags); break;
    case "invoice-get":      await cmdInvoiceGet(positional[0]); break;
    case "api":              await cmdApi(positional); break;
    default:
      console.error(`Unknown command: ${command}. Run --help for usage.`);
      process.exit(1);
  }
} catch (err) {
  console.error("Error:", err.message);
  process.exit(1);
}

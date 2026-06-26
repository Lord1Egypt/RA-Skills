# Примеры кода — МойСклад API

Все примеры используют прямой `fetch` (Node.js 18+, без зависимостей).

## Инициализация клиента

```javascript
// moysklad-client.mjs
const BASE_URL = "https://api.moysklad.ru/api/remap/1.2";

function getAuthHeader() {
  if (process.env.MOYSKLAD_TOKEN) {
    return `Bearer ${process.env.MOYSKLAD_TOKEN}`;
  }
  const login = process.env.MOYSKLAD_LOGIN;
  const password = process.env.MOYSKLAD_PASSWORD;
  if (!login || !password) {
    throw new Error("Set MOYSKLAD_LOGIN + MOYSKLAD_PASSWORD or MOYSKLAD_TOKEN");
  }
  return `Basic ${Buffer.from(`${login}:${password}`).toString("base64")}`;
}

async function api(method, path, body) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: getAuthHeader(),
      "Content-Type": "application/json",
      "Accept-Encoding": "gzip",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) {
    const msg = data?.errors?.[0]?.error ?? res.statusText;
    throw new Error(`${res.status} ${msg}`);
  }
  return data;
}
```

---

## 1. Получить список товаров

```javascript
// Первые 100 товаров
const result = await api("GET", "/entity/product?limit=100&offset=0");
console.log(`Всего товаров: ${result.meta.size}`);
for (const p of result.rows) {
  console.log(`${p.id} | ${p.name} | арт: ${p.article ?? "—"}`);
}

// Поиск по названию
const found = await api("GET", "/entity/product?search=ноутбук&limit=25");

// Только неархивные
const active = await api("GET", "/entity/product?filter=archived=false&limit=100");
```

---

## 2. Создать контрагента

```javascript
const counterparty = await api("POST", "/entity/counterparty", {
  name: "ООО Рога и Копыта",
  inn: "7701234567",
  kpp: "770101001",
  companyType: "legal",
  email: "info@roga.ru",
  phone: "+7 495 123-45-67",
  legalAddress: "г. Москва, ул. Ленина, д. 1",
});

console.log("Создан контрагент:", counterparty.id, counterparty.name);
```

---

## 3. Создать заказ покупателя

```javascript
// Шаг 1: получить организацию
const orgs = await api("GET", "/entity/organization?limit=1");
const org = orgs.rows[0];

// Шаг 2: получить контрагента (или создать, см. выше)
const counterparties = await api(
  "GET",
  `/entity/counterparty?filter=inn=7701234567`
);
const counterparty = counterparties.rows[0];

// Шаг 3: найти товар
const products = await api("GET", `/entity/product?search=ноутбук&limit=1`);
const product = products.rows[0];

// Шаг 4: создать заказ
const order = await api("POST", "/entity/customerorder", {
  organization: { meta: org.meta },
  agent: { meta: counterparty.meta },
  moment: new Date().toISOString().replace("T", " ").substring(0, 19) + ".000",
  description: "Заказ через API",
  positions: [
    {
      quantity: 2,
      price: 120000_00, // цена в КОПЕЙКАХ
      discount: 0,
      vat: 20,
      assortment: { meta: product.meta },
    },
  ],
});

console.log("Создан заказ:", order.id, order.name);
console.log("Сумма:", order.sum / 100, "руб.");
```

---

## 4. Обновить остаток (оприходование)

```javascript
// Шаг 1: получить склад
const stores = await api("GET", "/entity/store?limit=1");
const store = stores.rows[0];

// Шаг 2: создать документ оприходования
const enter = await api("POST", "/entity/enter", {
  organization: { meta: org.meta },
  store: { meta: store.meta },
  positions: [
    {
      quantity: 10,
      price: 80000_00, // закупочная цена в копейках
      assortment: { meta: product.meta },
    },
  ],
});

console.log("Оприходование создано:", enter.id);
```

---

## 5. Получить отчёт по остаткам

```javascript
// Все остатки
const stock = await api("GET", "/report/stock/all?limit=1000");
for (const item of stock.rows) {
  if (item.stock > 0) {
    console.log(
      `${item.name} | склад: ${item.store?.name} | остаток: ${item.stock} | резерв: ${item.reserve}`
    );
  }
}

// Остатки по конкретному складу
const storeHref = `${BASE_URL}/entity/store/${storeId}`;
const storeStock = await api(
  "GET",
  `/report/stock/all?filter=store=${encodeURIComponent(storeHref)}&limit=1000`
);

// Остатки по конкретному товару
const productHref = `${BASE_URL}/entity/product/${productId}`;
const productStock = await api(
  "GET",
  `/report/stock/all?filter=product=${encodeURIComponent(productHref)}`
);
```

---

## 6. Поиск и фильтрация сущностей

```javascript
// Контрагенты по ИНН
const byInn = await api("GET", "/entity/counterparty?filter=inn=7701234567");

// Заказы за период
const from = "2026-01-01 00:00:00.000";
const to = "2026-03-31 23:59:59.000";
const orders = await api(
  "GET",
  `/entity/customerorder?filter=moment>${from};moment<${to}&limit=100&order=moment,desc`
);

// Заказы по статусу (нужен href статуса)
const meta = await api("GET", "/entity/customerorder/metadata");
const newState = meta.states.find((s) => s.name === "Новый");
if (newState) {
  const newOrders = await api(
    "GET",
    `/entity/customerorder?filter=state=${newState.meta.href}&limit=100`
  );
}

// Товары определённой категории
const categories = await api("GET", "/entity/productfolder?search=Электроника");
const folder = categories.rows[0];
const inCategory = await api(
  "GET",
  `/entity/product?filter=productFolder=${folder.meta.href}&limit=100`
);
```

---

## 7. Работа со счётом покупателю

```javascript
// Создать счёт на основе заказа
const invoice = await api("POST", "/entity/invoiceout", {
  organization: { meta: org.meta },
  agent: { meta: counterparty.meta },
  customerOrder: { meta: order.meta },
  positions: order.positions, // копируем позиции заказа
});

console.log("Счёт создан:", invoice.id, invoice.name);

// Список неоплаченных счетов
const unpaid = await api(
  "GET",
  `/entity/invoiceout?filter=payedSum=0&limit=100&order=moment,desc`
);
```

---

## 8. Полный цикл: найти → обновить

```javascript
// Найти товар по артикулу
const result = await api("GET", `/entity/product?filter=article=DELL-XPS-15`);
if (result.rows.length === 0) throw new Error("Товар не найден");
const product = result.rows[0];

// Обновить цену
const updated = await api("PUT", `/entity/product/${product.id}`, {
  salePrice: [
    {
      value: 130000_00, // новая цена в копейках
      currency: product.salePrices?.[0]?.currency,
    },
  ],
});

console.log("Цена обновлена:", updated.name, updated.salePrices?.[0]?.value / 100);
```

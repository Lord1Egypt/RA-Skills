---
name: moysklad
description: МойСклад ERP — управление товарами, контрагентами, заказами, складами, остатками и документами через REST API. Используй когда нужно получить данные из МойСклад, создать или обновить записи, сформировать отчёты по остаткам или продажам.
license: MIT
compatibility: Requires Node.js 18+. Set MOYSKLAD_TOKEN, or MOYSKLAD_LOGIN + MOYSKLAD_PASSWORD env vars.
metadata:
  version: "1.0"
---

# МойСклад

Скилл для работы с МойСклад через JSON API 1.2. Используй для чтения и записи данных: товары, контрагенты, заказы покупателей, счета, склады, остатки.

## Настройка

1. Задай переменные окружения (один из вариантов):

   **Вариант А — токен** (предпочтительно):
   ```
   export MOYSKLAD_TOKEN='<токен>'
   ```
   Токен создаётся в МойСклад → Настройки → Безопасность → Токены.

   **Вариант Б — логин/пароль**:
   ```
   export MOYSKLAD_LOGIN='логин@email.com'
   export MOYSKLAD_PASSWORD='пароль'
   ```

2. Проверь подключение:
   ```
   node scripts/moysklad.mjs me
   ```

## Быстрый старт

```bash
# Список товаров
node scripts/moysklad.mjs products

# Поиск товара
node scripts/moysklad.mjs products --search "Ноутбук"

# Контрагенты
node scripts/moysklad.mjs counterparties

# Остатки
node scripts/moysklad.mjs stock

# Заказы покупателей
node scripts/moysklad.mjs orders

# Создать контрагента
node scripts/moysklad.mjs create-counterparty --name "ООО Рога и Копыта" --inn "7701234567"

# Создать заказ
node scripts/moysklad.mjs create-order --counterparty-id <id> --product-id <id> --quantity 5 --price 1000
```

## Команды CLI

Все команды поддерживают флаг `--json` для вывода сырого JSON.

### Информация об аккаунте
- `node scripts/moysklad.mjs me` — текущий пользователь и организация

### Товары
- `node scripts/moysklad.mjs products` — список всех товаров
- `node scripts/moysklad.mjs products --search "текст"` — поиск
- `node scripts/moysklad.mjs products --limit 50 --offset 0` — пагинация
- `node scripts/moysklad.mjs product-get <id>` — товар по ID

### Контрагенты
- `node scripts/moysklad.mjs counterparties` — список
- `node scripts/moysklad.mjs counterparties --search "ООО"` — поиск
- `node scripts/moysklad.mjs create-counterparty --name "Название" [--inn ИНН] [--phone "+7..."] [--email "..."]` — создать

### Заказы покупателей
- `node scripts/moysklad.mjs orders` — список заказов
- `node scripts/moysklad.mjs order-get <id>` — заказ по ID с позициями
- `node scripts/moysklad.mjs create-order --counterparty-id <id> --product-id <id> --quantity 1 --price 100` — создать заказ

### Склады
- `node scripts/moysklad.mjs stores` — список складов

### Остатки
- `node scripts/moysklad.mjs stock` — остатки по всем складам
- `node scripts/moysklad.mjs stock --store-id <id>` — по складу
- `node scripts/moysklad.mjs stock --product-id <id>` — по товару

### Счета покупателям
- `node scripts/moysklad.mjs invoices` — список счетов
- `node scripts/moysklad.mjs invoice-get <id>` — счёт по ID

## Прямые API-запросы

```bash
# GET
node scripts/moysklad.mjs api GET /entity/product?limit=10

# POST
node scripts/moysklad.mjs api POST /entity/counterparty '{"name":"Тест"}'

# PUT
node scripts/moysklad.mjs api PUT /entity/product/<id> '{"name":"Новое имя"}'

# DELETE
node scripts/moysklad.mjs api DELETE /entity/product/<id>
```

## Ошибки

- `401` — неверный логин/пароль
- `403` — недостаточно прав
- `404` — запись не найдена, проверь ID
- `429` — превышен лимит (45 req/s)
- Код `1003` в теле — неверный формат данных

## Справочные материалы

- Обзор API и аутентификация: `references/api-overview.md`
- Основные сущности и поля: `references/entities.md`
- Примеры кода: `references/examples.md`

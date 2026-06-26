# МойСклад JSON API 1.2 — Обзор

## Base URL

```
https://api.moysklad.ru/api/remap/1.2
```

## Аутентификация

### Basic Auth (логин/пароль)

```
Authorization: Basic base64(login:password)
```

### Bearer Token

```
Authorization: Bearer <token>
```

Токен генерируется в настройках аккаунта МойСклад → Безопасность → Токены.

## Формат запросов/ответов

- Все запросы и ответы в **JSON** (`Content-Type: application/json`)
- Кодировка **UTF-8**

### Типичный ответ списка

```json
{
  "context": { "employee": { "meta": { "href": "..." } } },
  "meta": {
    "href": "https://api.moysklad.ru/api/remap/1.2/entity/product",
    "type": "product",
    "mediaType": "application/json",
    "size": 150,
    "limit": 25,
    "offset": 0
  },
  "rows": [ ... ]
}
```

### Meta-объект

Каждая сущность содержит `meta` с её URL:

```json
{
  "meta": {
    "href": "https://api.moysklad.ru/api/remap/1.2/entity/product/abc123",
    "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
    "type": "product",
    "mediaType": "application/json"
  },
  "id": "abc123",
  "name": "Товар"
}
```

При создании связанных объектов (контрагент в заказе, товар в позиции) нужно передавать `meta`:

```json
{
  "agent": {
    "meta": {
      "href": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/COUNTERPARTY_ID",
      "type": "counterparty",
      "mediaType": "application/json"
    }
  }
}
```

## Пагинация

```
GET /entity/product?limit=100&offset=0
```

- `limit` — кол-во записей (макс. 1000, по умолчанию 25)
- `offset` — смещение (для перелистывания страниц)
- В ответе `meta.size` — общее кол-во записей

Перебор всех записей:
```javascript
let offset = 0;
const limit = 1000;
while (true) {
  const resp = await api(`/entity/product?limit=${limit}&offset=${offset}`);
  rows.push(...resp.rows);
  if (offset + limit >= resp.meta.size) break;
  offset += limit;
}
```

## Фильтрация

```
GET /entity/product?filter=name=Ноутбук
GET /entity/product?filter=name~Ноутбук        # содержит
GET /entity/product?filter=archived=false
GET /entity/product?filter=name=А;name=Б       # OR
GET /entity/counterparty?filter=inn=7701234567
```

Операторы:
- `=` — равно
- `!=` — не равно
- `~` — содержит (поиск по подстроке)
- `~=` — начинается с
- `=~` — заканчивается на
- `>`, `<`, `>=`, `<=` — сравнение

## Поиск

```
GET /entity/product?search=ноутбук
```

Полнотекстовый поиск по имени и описанию.

## Сортировка

```
GET /entity/product?order=name,asc
GET /entity/product?order=updated,desc
```

## Expand (раскрытие вложенных объектов)

```
GET /entity/customerorder/<id>?expand=agent,positions.assortment
```

Вместо `meta`-ссылки вернёт полный объект контрагента и позиций.

## Ошибки

```json
{
  "errors": [
    {
      "error": "Описание ошибки",
      "code": 1002,
      "moreInfo": "https://dev.moysklad.ru/doc/api/remap/1.2/#error_1002"
    }
  ]
}
```

Коды HTTP:
- `200` — успех (GET, PUT)
- `201` — создано (POST)
- `204` — удалено (DELETE)
- `400` — неверный запрос
- `401` — ошибка аутентификации
- `403` — нет доступа
- `404` — не найдено
- `409` — конфликт (дубликат)
- `429` — превышен лимит запросов (45/сек)
- `500` — внутренняя ошибка сервера

## Лимиты

- **45 запросов в секунду** на аккаунт
- При превышении — `429 Too Many Requests`, нужна пауза

## Bulk-операции

Создание/обновление нескольких объектов за один запрос:

```
POST /entity/product
Content-Type: application/json

[
  { "name": "Товар 1", "code": "T001" },
  { "name": "Товар 2", "code": "T002" }
]
```

## Вебхуки

```
POST /entity/webhook
{
  "url": "https://example.com/hook",
  "action": "CREATE",
  "entityType": "customerorder"
}
```

Actions: `CREATE`, `UPDATE`, `DELETE`

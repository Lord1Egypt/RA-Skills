# Основные сущности МойСклад

## Товар (product)

**Endpoint:** `/entity/product`

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | UUID | Идентификатор |
| `name` | string | Наименование (обязательное) |
| `code` | string | Код товара |
| `article` | string | Артикул |
| `description` | string | Описание |
| `salePrice` | array | Цены продажи |
| `buyPrice` | object | Закупочная цена |
| `vat` | int | НДС (%) |
| `weight` | float | Вес (кг) |
| `volume` | float | Объём (л) |
| `uom` | meta | Единица измерения |
| `archived` | bool | Архивный |
| `minPrice` | object | Минимальная цена |

Пример создания:
```json
{
  "name": "Ноутбук Dell",
  "code": "DELL001",
  "article": "DELL-XPS-15",
  "salePrice": [{ "value": 120000.0, "currency": { "meta": { "href": "...", "type": "currency" } } }]
}
```

---

## Контрагент (counterparty)

**Endpoint:** `/entity/counterparty`

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | UUID | Идентификатор |
| `name` | string | Наименование (обязательное) |
| `inn` | string | ИНН |
| `kpp` | string | КПП |
| `ogrn` | string | ОГРН |
| `legalAddress` | string | Юридический адрес |
| `actualAddress` | string | Фактический адрес |
| `email` | string | Email |
| `phone` | string | Телефон |
| `companyType` | enum | `legal` / `entrepreneur` / `individual` |
| `tags` | array | Теги |
| `notes` | array | Комментарии |

Пример создания:
```json
{
  "name": "ООО Рога и Копыта",
  "inn": "7701234567",
  "kpp": "770101001",
  "companyType": "legal",
  "email": "info@roga.ru",
  "phone": "+7 495 123-45-67"
}
```

---

## Заказ покупателя (customerorder)

**Endpoint:** `/entity/customerorder`

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | UUID | Идентификатор |
| `name` | string | Номер заказа |
| `moment` | datetime | Дата заказа |
| `agent` | meta | Контрагент (обязательное) |
| `organization` | meta | Организация (обязательное) |
| `state` | meta | Статус |
| `positions` | array | Позиции заказа |
| `sum` | int | Сумма (в копейках) |
| `vatSum` | int | Сумма НДС |
| `deliveryPlannedMoment` | datetime | Планируемая доставка |
| `description` | string | Комментарий |
| `shipmentAddress` | string | Адрес доставки |

Позиции (`positions`):
```json
{
  "quantity": 5.0,
  "price": 120000.0,
  "assortment": {
    "meta": {
      "href": "https://api.moysklad.ru/api/remap/1.2/entity/product/PRODUCT_ID",
      "type": "product"
    }
  }
}
```

---

## Отгрузка (demand)

**Endpoint:** `/entity/demand`

Документ отгрузки товара покупателю. Привязывается к заказу через `customerOrder`.

| Поле | Тип | Описание |
|------|-----|---------|
| `agent` | meta | Контрагент |
| `organization` | meta | Организация |
| `store` | meta | Склад |
| `customerOrder` | meta | Заказ покупателя |
| `positions` | array | Позиции |

---

## Счёт покупателю (invoiceout)

**Endpoint:** `/entity/invoiceout`

| Поле | Тип | Описание |
|------|-----|---------|
| `agent` | meta | Контрагент |
| `organization` | meta | Организация |
| `customerOrder` | meta | Заказ покупателя |
| `positions` | array | Позиции |
| `sum` | int | Сумма |
| `payedSum` | int | Оплачено |

---

## Склад (store)

**Endpoint:** `/entity/store`

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | UUID | Идентификатор |
| `name` | string | Наименование |
| `code` | string | Код |
| `address` | string | Адрес |
| `parent` | meta | Родительский склад |

---

## Остатки (stock report)

**Endpoint:** `/report/stock/all`

Не сущность, а отчёт. Не поддерживает POST/PUT/DELETE.

```
GET /report/stock/all?limit=1000
GET /report/stock/all?filter=store=<store_href>
GET /report/stock/all?filter=product=<product_href>
```

| Поле | Описание |
|------|---------|
| `assortment.name` | Название товара |
| `store.name` | Склад |
| `stock` | Остаток |
| `reserve` | Резерв |
| `inTransit` | В пути |
| `quantity` | Доступно (stock - reserve) |
| `price` | Себестоимость |

---

## Организация (organization)

**Endpoint:** `/entity/organization`

Собственная компания пользователя. Нужна при создании документов (заказов, отгрузок, счетов).

```
GET /entity/organization  →  берём первую из списка
```

---

## Статусы (state)

Каждый тип документа имеет свои статусы, настраиваемые в МойСклад.

```
GET /entity/customerorder/metadata  →  поле states[]
```

| Поле | Описание |
|------|---------|
| `id` | UUID статуса |
| `name` | Название (напр. "Новый", "В работе") |
| `color` | Цвет (hex) |
| `stateType` | `Regular` / `Successful` / `Unsuccessful` |

---

## Валюты (currency)

**Endpoint:** `/entity/currency`

Нужна для указания цен. Обычно используется рубль (RUB).

```
GET /entity/currency  →  ищем isoCode = "RUB"
```

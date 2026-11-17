# Yandex Cloud relay

`index.py` — исходник private Yandex Cloud Function, через которую OpenClaw обращается к МосОблЕИРЦ с российского egress.

## Переменные окружения

- `MOSOBLEIRC_TOKEN` — provider token личного кабинета МосОблЕИРЦ. Секрет, в Git не хранить.
- `ALLOW_WRITES=true` — включает action `submit`.

Function должна оставаться private.

## Inventory

Relay ожидает `inventory.json` рядом с `index.py` в deployment package.

Реальный файл в Git **не хранится**. Для структуры используется только:

```text
inventory.example.json
```

Перед production deployment фактический inventory добавляется из защищённого внешнего источника.

## Инварианты записи

Relay:

- выполняет максимум один POST на вызов `submit`;
- после POST делает один read-back;
- не повторяет POST при сетевой неопределённости;
- может вернуть `VERIFIED_AFTER_UNCERTAIN_RESPONSE`, если read-back подтвердил запись;
- иначе возвращает `UNCERTAIN_NO_RETRY`.

## Локальный тест

```bash
python3 -m unittest relay/yandex/test_relay.py -v
```

Сетевые функции подменяются, production API не вызывается.

## Build

Текущий build исходника:

```text
1.0.1
```

Для режима yandex-relay разверните функцию с IAM-аутентификацией (без публичного вызова), выдайте вызывающей учётной записи только право вызова. API key храните локально, provider token — в защищённом окружении функции. Inventory функции должен совпадать с локальными item/meter bindings. Deployment package собирайте вне репозитория. Setup на клиенте спрашивает URL и API key; сам ничего не развёртывает.

В режиме `direct` deployment не нужен: локальный transport не зависит от `index.py` и не использует переменные окружения функции.

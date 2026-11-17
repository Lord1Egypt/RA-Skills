# МосОблЕИРЦ для OpenClaw

[![CI](https://github.com/rommm13/openclaw-mosobleirc/actions/workflows/ci.yml/badge.svg)](https://github.com/rommm13/openclaw-mosobleirc/actions/workflows/ci.yml)

Версия 1.0.1. Публичный проект для распознавания водосчётчиков по фото и передачи подтверждённых показаний. Ассистент читает фото, Python проверяет правила, МосОблЕИРЦ остаётся источником истины.

Два режима используют одинаковые проверки и write-протокол:

- `direct`: helper обращается к провайдеру с вашего сервера. Нужны доступный провайдеру egress и provider token.
- `yandex-relay`: helper вызывает вашу private Yandex Cloud Function. Provider token хранится в функции, локально нужен API key. См. [relay README](relay/yandex/README.md).

## Установка и настройка

Linux, Python 3.11+, OpenClaw. Установите весь skill bundle. Direct transport реализован локально и не зависит от Yandex relay; каталог `relay/yandex/` нужен только если выбран облачный профиль. Из корня проекта:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/mosobleirc.py --transport direct setup
# Альтернатива:
python3 scripts/mosobleirc.py --transport yandex-relay setup
python3 scripts/mosobleirc.py init
python3 scripts/mosobleirc.py status
```

Запускайте setup лично в терминале. Мастер спрашивает token либо URL/API key, затем объекты и приборы; ручной JSON не нужен. Секрет вводится скрыто, не передаётся через аргументы и не печатается. Используйте свой действующий token из авторизованного личного кабинета; автоматических login/SMS/refresh нет. Item ID и meter ID — идентификаторы объектов провайдера, а не лицевой счёт или заводской номер. Введите их из своих данных личного кабинета. Синтетический inventory из примера не подходит для реальной отправки.

Setup полностью локален: не проверяет доступность сервера и не отправляет показания. Каталоги получают 0700, файлы 0600. Повторная настройка существующих файлов запрещена. Для отдельного профиля задайте `--data-root` или `MOSOBLEIRC_DATA_ROOT`. Не помещайте runtime внутрь bundle. Обновление skill не должно заменять runtime.

По умолчанию данные находятся в `~/.local/share/mosobleirc`: `config/runtime.json`, `config/inventory.json`, `secrets/`, `meter.db`, reference images и история. Для обновления токена замените только свой secret-файл вне Git, сохранив 0600. Не вставляйте секреты в чат. Если токен не работает, отправка останавливается с AUTH_REQUIRED; автоматического обхода нет.

## Runtime и совместимость

Приоритет: CLI > переменные окружения > runtime.json > defaults. Старые конфиги без `transport` продолжают использовать `yandex-relay`; команды `relay ping`, `relay inventory`, `relay submit-check` работают через выбранный transport. В direct эти команды локальны; в relay вызывают функцию, но не провайдера.

| Переменная | Назначение |
| --- | --- |
| MOSOBLEIRC_DATA_ROOT | Каталог runtime |
| MOSOBLEIRC_RUNTIME_CONFIG | Внешний runtime.json |
| MOSOBLEIRC_TRANSPORT | direct / yandex-relay |
| MOSOBLEIRC_INVENTORY | Inventory |
| MOSOBLEIRC_PROVIDER_TOKEN_FILE | Secret-файл для direct |
| MOSOBLEIRC_PROVIDER_BASE_URL | HTTPS origin, по умолчанию https://lkk.mosobleirc.ru |
| MOSOBLEIRC_FUNCTION_URL | URL private relay |
| MOSOBLEIRC_API_KEY_FILE | Файл API key relay |
| MOSOBLEIRC_ALLOWED_SOURCE_ROOTS | Разрешённые каталоги исходных фото через `:` |

Примеры обоих конфигов — в `config/`. В direct переменные окружения deployment-функции не используются. Изменение origin меняет получателя токена: используйте только доверенный адрес.

## Работа и безопасность

Фото сначала привязывается по заводскому номеру к inventory. Неуверенный OCR требует уточнения. До отправки можно локально посмотреть историю и расход; новый photo reading сохраняется только после подтверждённой записи провайдера. Reference добавляйте только после доказанной привязки к прибору; подробный диалоговый workflow — в [SKILL.md](SKILL.md).

Фото и подтверждение OCR не означают согласия на live-read или отправку. После отдельного «отправляй» helper делает свежий preflight, проверяет окно/монотонность/текущий период, выполняет максимум один POST и read-back. Только совпадающее подтверждение даёт VERIFIED. Прямые HTTP-вызовы в обход helper запрещены, настроенный direct helper разрешён.

`UNCERTAIN_NO_RETRY` блокирует повторный POST. Сначала нужна сверка; отрицательного GET недостаточно для повтора. Ручное `resolve-not-applied` требует отдельного подтверждения владельца после проверки кабинета и свежего GET; неоднозначное состояние не разрешает запись. Locks сериализуют операции по прибору. Batch сохраняет частичные результаты и останавливается при неопределённости или ошибке доступа.

## Проверки без сети

Тесты ориентированы на POSIX (Linux/macOS): модель безопасности опирается на права 0600/0700 и `fcntl`-локи. На Windows часть тестов автоматически пропускается (`skipped`).

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest relay/yandex/test_relay.py -v
python3 tools/release_check.py
python3 -m compileall -q scripts tests relay/yandex
```

[Архитектура](ARCHITECTURE.md), [безопасность](SECURITY.md), [релиз](PUBLIC_RELEASE.md), [изменения](CHANGELOG.md). Примеры содержат синтетические данные. Runtime, секреты, фото, deployment URL и персональные данные не входят в публичный пакет.

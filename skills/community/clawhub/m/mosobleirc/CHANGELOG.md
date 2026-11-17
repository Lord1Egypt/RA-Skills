# Changelog

## 1.0.1

- `StateStore._connect` закрывает SQLite-соединения (утечка дескрипторов, блокировка `meter.db` при очистке);
- `read_token` в direct-transport больше не падает на платформах без `O_NOFOLLOW`; проверка 0600 выполняется только там, где POSIX-права реально действуют;
- `setup` переносим на платформы без `os.getuid`;
- relay: удалён неиспользуемый `hashlib` и мёртвая `_meter_value`; проверка `ITEM_ID_REQUIRED` для `meters` снова достижима; User-Agent подписывается `OpenClaw-MosOblEIRC/1.0` вместо маскировки под Chrome;
- `send prepare`: потребление WATCH/ANOMALY теперь warning, а не blocker — единообразно с `send readings`;
- `DEFAULT_DATA_ROOT` перенесён в `mosobleirc_core`, `deep_read.py` больше не импортирует CLI;
- `meter_ocr.py`: удалён неиспользуемый импорт;
- тесты: POSIX-зависимые проверки (0600/0700, fcntl, symlink) помечены skip на не-POSIX платформах;
- документация: CI-badge, оговорка о POSIX-ориентации тестов, описание контракта `gemini_adapter` в ARCHITECTURE.md, опечатка в SKILL.md;
- CI: добавлен Python 3.13 в матрицу.

## 1.0.0

- Публичный релиз: direct и yandex-relay с общим write-протоколом.
- Локальный setup без ручного JSON, скрытый ввод секретов, права 0700/0600.
- Runtime вне bundle, совместимость старого relay-конфига, проверки release и transport.

# История изменений

## 0.9.1 — 2026-09-23

- добавлен межпроцессный lock на запись по каждому meter_id;
- подтверждение write теперь требует сильного provider read-back (PROCESSED + доказательство текущего/исходного расчётного периода);
- HTTP 408/409/425/429/5xx после POST считаются потенциально неопределёнными и проходят read-back без повторного POST;
- промежуточные/неизвестные write-статусы нормализуются в UNCERTAIN_NO_RETRY;
- локальная фиксация VERIFIED и история теперь коммитятся одной SQLite-транзакцией;
- исправлен reconcile через границу расчётного периода;
- partial batch-result сохраняется при сетевой ошибке preflight следующей квартиры;
- inventory валидируется fail-closed, дубликаты item_id/meter_id запрещены;
- relay дополнительно проверяет связку item_id → meter_id по deployment inventory;
- relay URL обязан использовать HTTPS и не может содержать embedded credentials;
- усилен release_check.py: runtime-варианты, Yandex credentials и произвольные текстовые расширения;
- Yandex handler скрывает неожиданные internal exceptions вместо необработанного traceback;
- добавлены regression-тесты по результатам независимого adversarial review;
- добавлен fail-closed recovery для `UNCERTAIN_NO_RETRY`: ручной `resolve-not-applied` с fresh GET, отдельным пользовательским подтверждением и audit trail;
- `operation_id` стал одноразовым и не может быть повторно подготовлен после terminal state;
- manual recovery корректно обрабатывает новый счётчик без `lastValue`, не ослабляя fail-closed обработку malformed provider state.

## 0.9.0 — 2026-09-22

- production inventory и runtime state вынесены из кода skill;
- добавлен `MOSOBLEIRC_DATA_ROOT`;
- добавлен внешний `runtime.json`;
- production URL удалён из кода;
- реальный inventory заменён синтетическим fixture;
- закреплён confirmation-gated write-flow;
- исключён blind retry POST;
- добавлен reconciliation для `UNCERTAIN_NO_RETRY`;
- batch write-flow работает независимо по каждому прибору;
- relay source включён без production secrets;
- добавлены release/privacy checks;
- документация приведена к русскоязычному canonical format;
- основной suite расширен до 120 тестов;
- relay suite содержит 6 тестов.

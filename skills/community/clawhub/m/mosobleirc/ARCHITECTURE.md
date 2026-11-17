# Архитектура

OpenClaw не пишет в МосОблЕИРЦ напрямую. Все операции проходят через детерминированный helper.

## Write state machine

Нормальный путь:

```text
PREPARED -> EXECUTING -> VERIFIED
```

Защитные/terminal состояния:

```text
BLOCKED
UNCERTAIN_NO_RETRY
NOT_APPLIED
SUPERSEDED
FAILED
AUTH_REQUIRED
```

`VERIFIED` возможен только после provider proof. `UNCERTAIN_NO_RETRY` не разрешает blind retry. Автоматический reconcile может перевести неопределённую операцию только в `VERIFIED`; отрицательный read-back сам по себе не считается доказательством `NOT_APPLIED`.

Ручной `resolve-not-applied` является recovery-path: он требует отдельного подтверждения владельца после проверки личного кабинета, делает fresh read-only GET, никогда не выполняет POST и сохраняет audit trail. При неоднозначном provider state операция остаётся `UNCERTAIN_NO_RETRY`.

## Concurrency

Все write/recovery paths сериализуются межпроцессным lock по `meter_id`. High-level `send readings` захватывает locks для всего batch в отсортированном порядке, поэтому два параллельных процесса не могут одновременно отправить один и тот же прибор и не создают lock-order deadlock.

## Batch

`BLOCKED` для одного прибора не останавливает локально независимые приборы. Неопределённый POST, auth failure или transport failure останавливает дальнейшие записи fail-closed; уже подтверждённые результаты сохраняются и возвращаются как partial results.

## Runtime separation

Код статичен; персональные и изменяемые данные находятся в `MOSOBLEIRC_DATA_ROOT`. Secrets, inventory, SQLite и reference images не входят в skill/release tree.

Helper поддерживает два независимых transport-адаптера с одинаковым `call(action, **payload)` contract: локальный `direct` и `yandex-relay`. Оба входят в один deterministic write-flow и используют общие state/lock/verification invariants. Direct делает ограниченный retry только безопасных GET; POST выполняется максимум один раз, после чего допускается только read-back. Yandex relay применяет те же правила внутри private Cloud Function.

`gemini_adapter.py` — детерминированный контракт между vision-моделью и helper: нормализация ответа модели (`normalize_result`), сравнение двух проходов (`compare_passes`) и маршрутизация фото (`route_photo_observation`). Adapter не вызывает сеть; сам вызов Gemini остаётся в основном turn ассистента.

Приоритет runtime: CLI > MOSOBLEIRC_* > runtime.json > defaults. Старый конфиг без transport выбирает yandex-relay. Direct не читает MOSOBLEIRC_TOKEN или ALLOW_WRITES процесса.

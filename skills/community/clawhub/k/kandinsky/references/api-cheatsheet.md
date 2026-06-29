# Kandinsky API — шпаргалка

- **Base:** env `KANDINSKY_API_BASE` (дефолт `http://87.242.117.37:5051` —
  приватный/доверенный инстанс).
- **Auth:** `Authorization: Bearer $KANDINSKY_API_KEY` (на все `/tasks/...`).
- **Тело POST:** `{ "censor": true, "params": { ... } }`
- **Префлайт:** проверь ключ/базу → `GET /health` (без авторизации) → потом генерация.
- **Флоу:** `POST /tasks/<тип>` → `task_id` → `GET /tasks/{id}` (поллинг) →
  `GET /tasks/{id}/result`

## ⚠️ Транспорт

API-ключ уходит открыто. Не слать ключ по plain `http://` в недоверенной
сети — только HTTPS, либо loopback/приватный доверенный инстанс. В URL/query
ключ не класть, в логи не писать.

## Эндпоинты

| Тип | Метод + путь | params |
|---|---|---|
| t2i (картинка по тексту) | `POST /tasks/k6-image-t2i` | `query`, `resolution`, `beautificator?` |
| i2i (правка картинки) | `POST /tasks/k6-i2i` | `query`, `image[]` (base64), `beautificator?` |
| superres (апскейл) | `POST /tasks/k6_superres` | `image` (base64), `upscale` 2\|4, `one_step_t?` |
| t2v lite | `POST /tasks/k5_video_t2v_lite` | `query`, `resolution`, `beautificator?` |
| t2v pro | `POST /tasks/k5_video_t2v_pro` | `query`, `resolution`, `beautificator?` |
| i2v lite | `POST /tasks/k5-i2v-lite` | `query`, `image` (base64), `beautificator?` |
| i2v sd | `POST /tasks/k5-i2v-sd` | `query`, `image`, `beautificator?` |
| i2v hd | `POST /tasks/k5-i2v-hd` | `query`, `image`, `beautificator?` (дефолт gigachat-max) |
| аватар | `POST /tasks/giga_avatar` | `query`, `image` (base64), `audio` (base64) |
| статус | `GET /tasks/{task_id}` | → `{status}` |
| результат | `GET /tasks/{task_id}/result` | → файл |
| health | `GET /health` | без авторизации |

## Допустимые resolution

- **k6-image-t2i:** `1024x1024`, `768x768`, `768x1280`, `1280x768`, `auto`
- **k5_video_t2v_lite:** `512x512`, `512x768`, `768x512`
- **k5_video_t2v_pro:** `768x1280`, `1280x768`

## beautificator

`enabled` | `disabled` | `gigachat-max`. Если не указать — сервер ставит дефолт
маршрута (`enabled` для K6, `gigachat-max` для i2v-hd). Это «улучшайзер» промпта.

## Статусы

`new` (в очереди) → `processing` → `done`. Ошибка → `fail`.
Superres иногда залипает в `new` — не ждать вечно.

## Заметки

- `image` в i2i — массив base64; в i2v/superres/avatar — одна base64-строка.
- `censor=true` по умолчанию: фильтрует промпт, вход и результат.
- `one_step_t` (superres) — сила следования оригиналу, 0..1 (напр. 0.3333).
- Результат сохраняй в файл сразу; видео для оценки разложи на кадры через ffmpeg.
- Спека всегда актуальна в `/openapi.json` и `/docs`.

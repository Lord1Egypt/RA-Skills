---
name: kandinsky
description: >-
  Генерация изображений и видео через Kandinsky API (модели Kandinsky K6/K5,
  GigaAvatar). Используй, когда пользователь просит "сгенерируй картинку",
  "нарисуй", "перерисуй (i2i)", "оживи картинку", "сделай видео из фото или по
  тексту", "апскейл/увеличь картинку", "озвучь аватар". Покрывает t2i, i2i,
  super-resolution (×2/×4), t2v (text-to-video), i2v (image-to-video, lite/sd/hd)
  и giga_avatar (фото+аудио → говорящий аватар). Триггеры: Kandinsky, Кандинский,
  Kandinsky API, K6, K5, t2i, i2i, t2v, i2v, апскейл, оживить, аватар.
version: 1.0.4
metadata:
  openclaw:
    primaryEnv: KANDINSKY_API_KEY
    requires:
      env:
        - KANDINSKY_API_KEY
      bins:
        - curl
        - python3
    envVars:
      - name: KANDINSKY_API_KEY
        required: true
        description: >-
          API-ключ Kandinsky API (заголовок Authorization: Bearer ...).
          Выдаётся владельцем инстанса Kandinsky API.
      - name: KANDINSKY_API_BASE
        required: false
        description: >-
          База API. По умолчанию http://87.242.117.37:5051 — переопредели, если
          инстанс развёрнут по другому адресу.
    emoji: "🎨"
    homepage: http://87.242.117.37:5051/docs
---

# Kandinsky API — картинки и видео

Скилл для генерации через **Kandinsky API** — REST-сервис с моделями Kandinsky
(K6 — изображения, K5 — видео) и GigaAvatar.

- **Base URL:** задаётся через env `KANDINSKY_API_BASE`. Значение по умолчанию
  `http://87.242.117.37:5051` — это **приватный/operator-trusted инстанс**, не
  публичный прод.
- **Swagger:** `<KANDINSKY_API_BASE>/docs` · спека: `/openapi.json`
- **Авторизация:** HTTP Bearer — заголовок `Authorization: Bearer $KANDINSKY_API_KEY`
  на каждом запросе к `/tasks/...`. Ключ берётся из env `KANDINSKY_API_KEY`
  (спроси у пользователя, если его нет).

### ⚠️ Безопасность ключа и транспорта

Ключ — секрет, и Bearer-заголовок уходит на сервер открыто. **Не отправляй
`KANDINSKY_API_KEY` по обычному HTTP в недоверенной сети** — его можно
перехватить. Правила:

- Предпочитай **HTTPS**-эндпоинт. Если используешь `KANDINSKY_API_BASE` с `https://` —
  всё ок.
- Plain `http://` допустим **только** для loopback (`127.0.0.1`/`localhost`) или
  доверенного приватного/VPN-инстанса, который контролирует владелец.
- Если `KANDINSKY_API_BASE` начинается с `http://` и это **не** loopback/приватный
  адрес — предупреди пользователя о риске перехвата ключа и не продолжай без его
  явного согласия.
- Никогда не клади ключ в URL/query-параметры и не логируй его.

## Префлайт (перед генерацией)

Прежде чем создавать задачу (она тратит ресурсы провайдера), сделай дешёвую
проверку:

1. Убедись, что `KANDINSKY_API_KEY` задан; если нет — запроси у пользователя.
2. Проверь `KANDINSKY_API_BASE`: что это валидный URL и что транспорт допустим
   по правилам безопасности выше (HTTPS либо loopback/доверенный приватный HTTP).
3. Проверь доступность сервиса дешёвым запросом: `GET /health` (без авторизации).
   При необходимости сверь схему: `GET /openapi.json`.
4. Только после этого отправляй `POST /tasks/<тип>`.

Это отсекает «дорогие» ошибки (неверный ключ/адрес, лежащий сервис) до запуска
генерации.

## Готовый клиент — `scripts/kandinsky.py`

В скилл вшит Python-клиент (только stdlib, без зависимостей). **Предпочитай его**
вместо ручных curl-запросов: он сам создаёт задачу, поллит статус и сохраняет файл.

Требует env `KANDINSKY_API_KEY` (и опц. `KANDINSKY_API_BASE`).

Как библиотека:

```python
from kandinsky import KandinskyClient
c = KandinskyClient()
c.generate_image("закатные горы, кинематографично", resolution="1024x1024", out="pic.png")
c.edit_image("pic.png", "в стиле акварели", out="water.png")
c.upscale("pic.png", upscale=2, out="big.png")
c.text_to_video("волны на берегу", pro=True, out="clip.mp4")
c.animate_image("pic.png", "камера медленно облетает объект", quality="lite", out="anim.mp4")
c.avatar("face.png", "speech.wav", "говорящий аватар", out="avatar.mp4")
```

Как CLI:

```bash
python scripts/kandinsky.py health                      # префлайт перед генерацией
python scripts/kandinsky.py t2i "закатные горы" --resolution 1024x1024 -o pic.png
python scripts/kandinsky.py i2i pic.png "в стиле акварели" -o water.png
python scripts/kandinsky.py superres pic.png --upscale 2 -o big.png
python scripts/kandinsky.py t2v "волны на берегу" --pro -o clip.mp4
python scripts/kandinsky.py i2v pic.png "камера облетает" --quality hd -o anim.mp4
python scripts/kandinsky.py avatar face.png speech.wav "аватар" -o avatar.mp4
python scripts/kandinsky.py status <task_id>
python scripts/kandinsky.py result <task_id> -o out.bin
```

Ниже — описание сырого API на случай отладки или вызова без клиента.

## Общий принцип (асинхронно)

Все генерации асинхронные. Паттерн всегда один:

```
1. POST /tasks/<тип>      → { "task_id": "..." }
2. GET  /tasks/{task_id}  → { "status": "..." }   # поллить раз в ~5–10 сек
3. когда готово:
   GET  /tasks/{task_id}/result                   # забрать результат
```

Тело POST-запроса всегда обёрнуто так:

```json
{
  "censor": true,
  "params": { ... }
}
```

`censor` (по умолчанию `true`) — цензура текста промпта и входных картинок, плюс
проверка результата перед выдачей. Оставляй `true`, если не просят иначе.

## Эндпоинты и параметры (params)

### Изображения (Kandinsky K6)

- **POST `/tasks/k6-image-t2i`** — текст → картинка.
  `params`: `query` (промпт), `resolution` ∈ `1024x1024 | 768x768 | 768x1280 |
  1280x768 | auto`, `beautificator?` ∈ `enabled | disabled | gigachat-max`
  (дефолт `enabled`).
- **POST `/tasks/k6-i2i`** — картинка(и) + текст → картинка.
  `params`: `query`, `image` (массив base64-строк), `beautificator?`.
- **POST `/tasks/k6_superres`** — апскейл.
  `params`: `image` (base64), `upscale` ∈ `2 | 4`, `one_step_t?` (0..1 — сила
  следования оригиналу, напр. `0.3333`). Только кратное ×2/×4, дробного нет.

### Видео (Kandinsky K5)

- **POST `/tasks/k5_video_t2v_lite`** — текст → видео (lite).
  `params`: `query`, `resolution` ∈ `512x512 | 512x768 | 768x512`, `beautificator?`.
- **POST `/tasks/k5_video_t2v_pro`** — текст → видео (pro).
  `params`: `query`, `resolution` ∈ `768x1280 | 1280x768`, `beautificator?`.
- **POST `/tasks/k5-i2v-lite`** — картинка → видео (lite). *(этим оживляли ежа)*
  `params`: `query` (промпт движения), `image` (base64), `beautificator?`.
- **POST `/tasks/k5-i2v-sd`** — картинка → видео (SD). `params`: те же.
- **POST `/tasks/k5-i2v-hd`** — картинка → видео (HD, дефолт beautificator
  `gigachat-max`). `params`: те же.

### Аватар

- **POST `/tasks/giga_avatar`** — фото + аудио → говорящий аватар.
  `params`: `query`, `image` (base64), `audio` (base64).

### Статус и результат

- **GET `/tasks/{task_id}`** → `{ "status": "..." }`. Наблюдаемые значения:
  `new` (в очереди) → `processing` (выполняется) → `done` (готово); ошибка — `fail`.
- **GET `/tasks/{task_id}/result`** → результат (картинка/видео). Сохрани в файл.

## Рабочий процесс «оживить картинку» (i2v)

1. Получи исходную картинку: либо `k6-image-t2i`, либо уже готовый файл →
   переведи в base64.
2. `POST /tasks/k5-i2v-lite` (или `-sd`/`-hd` под качество) с `image` и
   `query`-промптом движения. Видео короткое — уложи действие в один кадр смысла.
3. Полль `GET /tasks/{task_id}` до `done`, затем `GET .../result`, сохрани mp4.

Промпт движения делай **про сам объект**, а не только про камеру, иначе объект
застынет, а двигаться будет лишь камера. Подробнее — `references/prompting.md`.

## Грабли (учтённый опыт)

- **Апскейл (superres) может залипнуть** в `new` — воркер не берёт задачу.
  Не полль бесконечно: после ~1–2 мин в `new` скажи пользователю и предложи
  альтернативу (сгенерить сразу в нужном разрешении / повторить позже).
- **Видео модель не «видит» как поток.** Чтобы оценить ролик — разложи на кадры:
  `ffmpeg -i video.mp4 -vf fps=2 frame_%03d.png` и посмотри кадры.
- **Рейтлимит на статус** — поллить не чаще раза в ~5–10 сек.
- **Картинки/видео отдаются как base64/бинарь** — сохраняй сразу в файл, не таскай
  длинный base64 по контексту.
- **Censor** включён по умолчанию: «острые» промпты или входные фото могут
  отклоняться. Если задача падает на цензуре — переформулируй промпт.

## Минимальный пример (curl)

```bash
BASE="${KANDINSKY_API_BASE:-http://87.242.117.37:5051}"

# 0) префлайт: сервис жив? (дёшево, без авторизации)
curl -s "$BASE/health"
# → {"status":"ok"}  — только после этого тратим ресурсы на генерацию

# 1) создать t2i
curl -s -X POST "$BASE/tasks/k6-image-t2i" \
  -H "Authorization: Bearer $KANDINSKY_API_KEY" -H "Content-Type: application/json" \
  -d '{"censor":true,"params":{"query":"cinematic mountain landscape at sunrise","resolution":"1024x1024"}}'
# → {"task_id":"abc123"}

# 2) статус
curl -s "$BASE/tasks/abc123" -H "Authorization: Bearer $KANDINSKY_API_KEY"
# → {"status":"processing"}  (поллить до "done")

# 3) результат
curl -s "$BASE/tasks/abc123/result" -H "Authorization: Bearer $KANDINSKY_API_KEY" -o out.png
```

Полную схему всегда можно сверить в Swagger: `http://87.242.117.37:5051/docs`.
Шпаргалка по эндпоинтам — `references/api-cheatsheet.md`, промптинг —
`references/prompting.md`.

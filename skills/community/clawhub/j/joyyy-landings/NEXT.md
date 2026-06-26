# Что делать дальше (портфолио уже ок)

Минимум шагов: аккаунт → публикация → после.

---

## Шаг 1. Аккаунт ClawHub

1. Открой **https://clawhub.ai** (или актуальный URL из доки OpenClaw: https://docs.openclaw.ai).
2. Зарегистрируйся / войди.
3. Если публикация идёт через **CLI** — установи OpenClaw/ClawHub CLI по инструкции на сайте. Если через **веб-форму** — аккаунта достаточно.

---

## Шаг 2. Опубликовать скилл

**Вариант A — через CLI (если установлен):**

```bash
cd /Users/vitaliiziatkov/joyyy/neuro
clawhub publish ./skills/joyyy-landings \
  --slug joyyy-landings \
  --name "Interactive Prototypes — Human + AI" \
  --version 1.0.0 \
  --tags latest
```

**Вариант B — через веб:**  
Если на ClawHub есть форма «Add skill» / «Publish» — залей туда папку `skills/joyyy-landings` (или архив с `SKILL.md`, `clawhub.json`) и заполни поля из `clawhub.json` (name, tagline, description, homepage, tags).

---

## Шаг 3. После публикации

1. Открой страницу скилла на ClawHub.
2. Добавь **ссылку на демо:** https://vziatkov.github.io/neuro/landing-with-art-cards.html (если есть поле).
3. По желанию добавь ссылку на видео (если уже есть).
4. Дальше — распространение: LinkedIn, пост в Twitter/HN, ссылка в README (блок уже есть). Формулировки в `PUBLISH.md` §5.

---

**Итого:** зарегался → опубликовал (CLI или форма) → на странице скилла добавил demo URL. Остальное (скриншоты, видео, посты) — по желанию.

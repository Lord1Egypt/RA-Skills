---
name: letundra
description: "Универсальный AI-скилл для путешествий — визы, новости, RSS, праздники, валюты с letundra.com. Используй when: пользователь спрашивает о визах, новостях, праздниках, курсах валют. NOT for: бронирование, отели."
homepage: https://letundra.com
metadata: { "openclaw": { "emoji": "🌍", "requires": { "bins": ["node"] }, "tags": ["travel", "visa", "news", "holidays", "currency", "aviation", "airlines"] } }
---

# 🌍 Letundra — всё о путешествиях

Универсальный AI-скилл для получения информации с **letundra.com** — визы, новости, праздники, курсы валют.

## Что умеет скилл

| Функция | Описание |
|---------|----------|
| 🛂 Виза | Визовые требования, безвизовый режим, документы |
| 📰 Новости | Авиация, акции, визовые изменения |
| 📡 RSS | Генерация RSS-ленты по тегам/странам |
| 🎉 Праздники | Государственные праздники и фестивали |
| 💱 Валюты | Курсы валют и конвертация |

## When to Use

Активируйте когда пользователь спрашивает о:
- Визах / "нужна ли виза в Таиланд?"
- Новостях / "что нового в авиации?"
- Праздниках / "какие праздники в Индии?"
- Валютах / "курс бата к рублю"
- RSS / "создай RSS для Emirates"

## Как это работает

### Используй web_fetch

Все данные получаются через встроенный `web_fetch`:

```
{{web_fetch url="https://letundra.com/ru/countries/{slug}/"}}
{{web_fetch url="https://letundra.com/ru/news/"}}
```

### URLs для разных типов данных

| Тип | URL |
|-----|-----|
| Виза, страна | `https://letundra.com/ru/countries/{slug}/` |
| Новости | `https://letundra.com/ru/news/` |
| Новости по тегу | `https://letundra.com/ru/news/?taglist={tag}` |

### Примеры slug стран

- Таиланд → thailand
- Индия → india
- ОАЭ → uae
- Турция → turkey
- Египет → egypt

## Output Formats

### Новости
```markdown
# 📰 Новости

## 1. Заголовок
📅 Дата
🏷️ Теги
[Описание]
🔗 [Читать далее](link)
```

### Виза
```markdown
# 🛂 Виза в [Страна]

**Нужна ли виза:** [Да/Нет]
**Безвизовый срок:** [дней]

**Типы виз:**
- По прибытию: [условия]
- e-Visa: [условия]

**Документы:**
- [список]
```

## Examples

| Запрос | Метод |
|--------|-------|
| "Новости авиации" | web_fetch → /ru/news/ |
| "Виза в ОАЭ" | web_fetch → /ru/countries/uae/ |
| "Праздники в Тае" | web_fetch → /ru/countries/thailand/ |
| "Курс бата" | web_fetch → /ru/countries/thailand/ |

## Структура проекта

```
letundra-skills/
├── SKILL.md                    # Этот файл
├── letundra-visa/              # Скилл для виз
├── letundra-news/              # Скилл для новостей
├── letundra-rss/               # Скилл для RSS
├── letundra-holidays/          # Скилл для праздников
├── letundra-currency/          # Скилл для валют
├── scripts/
│   └── letundra_yandex.js     # Локальный парсер (опционально)
├── package.json
└── README.md
```

---

*Данные: Letundra.com — ваш помощник в мире путешествий*

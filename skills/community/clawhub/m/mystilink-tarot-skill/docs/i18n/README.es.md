# Mystilink Tarot Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill para tarot: extrae cartas upright/reversed para un spread con un script Node embebido, luego interpreta con páginas teóricas de cartas. Prefiera una extracción real (script o cartas del usuario); no invente extracciones en silencio.

## Tipo de entrega

Paquete **Agent Skill**. **No** implementa la matriz de lenguajes de calculadoras. La lógica de extracción/validación está embebida solo en `scripts/` (sin repositorio calculador de tarot separado).

## Requisitos

- Node.js 18+
- Host compatible con Agent Skills
- Red opcional para la API Wiki

## Instalación

El nombre de carpeta debe ser `mystilink-tarot`:

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## Inicio rápido

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

Stdout JSON: cartas con `id`, `name`, `orientation` (`upright`|`reversed`), posiciones. Los `id` de carta se alinean con páginas Wiki `tarot.card.*`.

## Flujo de trabajo

1. Aclarar pregunta y spread (predeterminado: three-card); ver `examples/draw-request.json`
2. Extraer vía script o aceptar cartas proporcionadas por el usuario
3. Para cada carta, Wiki opcional:

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. Vincular cada posición a la pregunta; cite Wiki cuando se use

Detalles: `SKILL.md`. Notas de método: `references/method-draw.md`.

## Ejemplos

- `examples/draw-request.json` — solicitud de extracción de ejemplo

## Límites

- No reclamar certeza médica o legal
- Preferir una pregunta clara por extracción
- Locale Wiki omitida → `en`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Incluya flags/seed del spread (o JSON stdin) y el JSON stdout (solo preguntas ficticias).

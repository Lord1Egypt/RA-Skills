# Mystilink Horoscope Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill para astrología natal occidental: calcula planetas, casas y aspectos a partir de la hora y el lugar de nacimiento mediante un script embebido, luego interpreta con páginas teóricas.

## Tipo de entrega

Paquete **Agent Skill**. **No** implementa la matriz de lenguajes de calculadoras. Hermano opcional: `mystilink-horoscope-calculator`.

## Requisitos

- Python 3.9+
- `pip install pyswisseph`
- Host compatible con Agent Skills
- Red opcional para la API Wiki

## Instalación

El nombre de carpeta debe ser `mystilink-horoscope`:

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## Inicio rápido

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Opciones: `--zodiac tropical|sidereal`, `--true-solar-time`.

Éxito: JSON en stdout. Fallo: salida distinta de cero + JSON error.

## Flujo de trabajo

1. Recopilar datos de nacimiento — `examples/profile.v0.json` (BirthProfile) o legado `examples/profile.json`
2. Ejecutar el script natal
3. Wiki opcional:

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. Mantener los datos de la carta distintos de la interpretación

Detalles: `SKILL.md`. Orientación: `references/overview.md`.

## Ejemplos

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, ficticio)
- `examples/profile.json` — entradas natales legadas ficticias

## Límites

- Requiere Swiss Ephemeris vía `pyswisseph`
- Script embebido para instalación skill, no un SDK multiidioma
- Locale Wiki omitida → `en`; el respaldo puede ser `zh-Hans`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Incluya el comando exacto (coordenadas/datetime ficticios) y la salida/error JSON.

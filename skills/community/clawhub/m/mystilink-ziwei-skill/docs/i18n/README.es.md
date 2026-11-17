# Mystilink Zi Wei Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill para Zi Wei Dou Shu: construye una carta de doce palacios (Si Hua opcional) con un script Python embebido, luego interpreta con páginas teóricas. El cálculo de carta está en `scripts/`.

## Tipo de entrega

Paquete **Agent Skill**. **No** implementa la matriz de lenguajes de calculadoras (C / C++ / C# / Java / JS / Python SDK). Hermano opcional: `mystilink-ziwei-calculator`.

## Requisitos

- Python 3.9+
- `pip install zhdate`
- Host compatible con Agent Skills
- Red opcional para la API Wiki

## Instalación

El nombre de carpeta debe ser `mystilink-ziwei`:

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## Inicio rápido

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Opciones: `--si-hua`, `--year YYYY`, `--longitude E`, `--midnight-zi`.

Éxito: JSON en stdout. Fallo: salida distinta de cero + JSON error.

## Flujo de trabajo

1. Recopilar datos de nacimiento — `examples/profile.v0.json` (BirthProfile) o legado `examples/profile.json`
2. Ejecutar el script de carta
3. Wiki opcional:

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. Separar hechos de la carta de la interpretación

Detalles: `SKILL.md`. Orientación: `references/overview.md`.

## Ejemplos

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, ficticio)
- `examples/profile.json` — entradas de nacimiento legadas ficticias

## Límites

- Depende de `zhdate` para la conversión lunar
- Script embebido para uso skill autónomo, no un SDK multiidioma
- Locale Wiki omitida → `en`; el respaldo puede ser `zh-Hans`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Incluya el comando exacto (datetime ficticio) y la salida/error JSON.

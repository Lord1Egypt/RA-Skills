# Mystilink BaZi Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill para BaZi (Cuatro Pilares): calcula pilares, DaYun y LiuNian a partir de datos de nacimiento mediante scripts embebidos, luego interpreta con páginas teóricas (maestro del día, diez dioses y conceptos relacionados). Los scripts de cálculo de carta están en `scripts/`.

## Tipo de entrega

Este repositorio es un paquete **Agent Skill** (`SKILL.md` + `scripts/` + `references/` + `examples/`). **No** implementa la matriz de lenguajes C / C++ / C# / Java / JavaScript / Python de las bibliotecas calculadoras. Para un SDK/CLI multiidioma, vea el proyecto hermano `mystilink-bazi-calculator` (opcional; no requerido para ejecutar este skill).

## Requisitos

- Python 3.9+ (`zoneinfo`)
- Host compatible con Agent Skills
- Red opcional para la API Mystilink Wiki durante la interpretación

## Instalación

Instale con el nombre de carpeta `mystilink-bazi` (coincide con el `name` de `SKILL.md`):

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## Inicio rápido (scripts)

Desde el directorio del skill:

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

Éxito: JSON en stdout. Fallo: salida distinta de cero y JSON `{"error":…}`.

Los objetos de pilar incluyen `stem_index`, `branch_index`, `text` y el campo legado `ganzhi` (`=` `text`).

## Flujo de trabajo

1. Recopilar el perfil de nacimiento — cualquiera de:
   - `examples/profile.v0.json` (`mystilink.birth/0.1` BirthProfile), o
   - `examples/profile.json` (campos skill heredados)
2. Ejecutar scripts de carta según necesite (`--birth-json` / `--profile-json` aceptan ambas formas)
3. Interpretar con Wiki (opcional):

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. Separar **hechos de la carta** de la **interpretación**; cite la procedencia Wiki cuando se use

Instrucciones completas del agente: `SKILL.md`. Ids cortos: `references/wiki-ids.md`.

## Ejemplos

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, ficticio)
- `examples/profile.json` — perfil de nacimiento legado (ficticio); los scripts aún lo aceptan

## Límites

- Los scripts son copias embebidas para instalación skill independiente; no son un SDK multiidioma
- Las fechas de términos solares DaYun usan días civiles aproximados
- El tiempo solar verdadero necesita zona horaria y longitud
- Locale Wiki: omitir → `en`; traducciones faltantes pueden caer a `zh-Hans`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Reporte defectos con el comando exacto del script (solo fechas ficticias) y el JSON de stdout/stderr.

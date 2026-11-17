# Mystilink Router Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill que elige un skill de metafísica Mystilink (BaZi, Zi Wei, tarot, Liu Yao u horóscopo occidental) cuando el usuario no ha nombrado un sistema, pregunta qué método encaja, o mezcla varias tradiciones. No calcula cartas ni tiradas.

## Tipo de entrega

Este repositorio es un paquete **Agent Skill** (`SKILL.md` + references + examples). **No** implementa la matriz de lenguajes C / C++ / C# / Java / JavaScript / Python usada por las bibliotecas calculadoras.

## Requisitos

- Un host compatible con Agent Skills (Cursor, Claude Code, OpenClaw, Hermes o equivalente)
- Los skills de teoría de destino instalados si se va a continuar tras el enrutado

## Instalación

Clone o copie este repositorio en el directorio skills del host como `mystilink-router` (el nombre de carpeta debe coincidir con el `name` en `SKILL.md`):

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` o `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` o `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## Uso

Siga `SKILL.md`. Heurísticas de enrutado:

| Necesidad | Skill |
|------|--------|
| Fecha/hora de nacimiento → estructura a largo plazo, diez dioses | `mystilink-bazi` |
| Nacimiento → doce palacios / estrellas Zi Wei | `mystilink-ziwei` |
| Lugar + hora de nacimiento → planetas/casas/aspectos | `mystilink-horoscope` |
| Una pregunta concreta, cartas simbólicas | `mystilink-tarot` |
| Una pregunta concreta, hexagrama / líneas móviles | `mystilink-liuyao` |

Ayuda Wiki opcional (red):

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

Tras elegir, cargue el `SKILL.md` de ese skill y continúe allí. Prefiera un sistema principal por solicitud.

## Ejemplos

Vea `examples/routing-cases.md` para intenciones de ejemplo y destinos esperados.

## Límites

- Sin scripts de cálculo en este skill
- No ejecuta varios sistemas «por si acaso»
- Las llamadas Wiki son opcionales; omitir `locale`/`lang` → `en`; las traducciones faltantes pueden caer a `zh-Hans`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Reporte defectos con el texto de intención (solo ficticio) y el skill seleccionado o omitido.

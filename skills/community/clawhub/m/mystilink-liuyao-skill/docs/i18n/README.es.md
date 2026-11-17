# Mystilink Liu Yao Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## Descripción general

Agent Skill para Liu Yao (lanzamiento de seis líneas): forma hexagramas a partir de seis lanzamientos con un script Node embebido, luego interpreta con páginas de método y capítulos del Zhouyi desde Wiki. Un asunto, un lanzamiento. No invente citas clásicas.

## Tipo de entrega

Paquete **Agent Skill**. **No** implementa la matriz de lenguajes de calculadoras. La lógica de lanzamiento está embebida solo en `scripts/` (sin repositorio calculador Liu Yao separado).

## Requisitos

- Node.js 18+
- Host compatible con Agent Skills
- Red recomendada para páginas de método Wiki y clásicos

## Instalación

El nombre de carpeta debe ser `mystilink-liuyao`:

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| Host | Ruta |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## Inicio rápido

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

Stdout JSON: seis líneas (abajo→arriba), flags de movimiento, claves de hexagrama cuando estén disponibles. El modelo de monedas sigue la ayuda del script (cara=3, cruz=2 en suma).

## Flujo de trabajo

1. Un asunto claro (`examples/cast-request.json`); rechazar lanzamientos multitópico
2. Lanzar vía script o aceptar throws del usuario
3. Leer vía Wiki, por ejemplo:

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. Preferir references / cites Wiki para pasajes del Zhouyi

Detalles: `SKILL.md`. Orientación: `references/overview.md`.

## Ejemplos

- `examples/cast-request.json` — solicitud de lanzamiento de ejemplo

## Límites

- Los clásicos a menudo caen a `zh-Hans` cuando otras locales carecen de texto
- El ayudante de lanzamiento embebido refleja la semántica moneda→línea del producto en forma simplificada
- Locale Wiki omitida → `en`

## Licencia

MIT. Véase [LICENSE](../../LICENSE).

## Comentarios

Incluya seed/throws y el JSON stdout (solo asuntos ficticios).

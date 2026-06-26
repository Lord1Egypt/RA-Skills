# SSOT Preflight

Este preflight es obligatorio. No clasifiques ni ejecutes nada sin revisar primero ambos manuales.

## Paths canonicos

1. `/Users/felixsanhueza/Developer/kora/KNOWLEDGE/OMEGA/manual-integral-skills-openclaw.md`
2. `/Users/felixsanhueza/Developer/kora/KNOWLEDGE/OMEGA/openclaw-manual-integral.md`

## Equivalentes relativos dentro del repo

1. `../../../../../KNOWLEDGE/OMEGA/manual-integral-skills-openclaw.md`
2. `../../../../../KNOWLEDGE/OMEGA/openclaw-manual-integral.md`

## Que revisar en cada corrida

### Para skills

Revisar como minimo:
- estructura de skill
- frontmatter permitido
- ubicaciones y precedencia
- ClawHub publish/install/update
- watcher, eligibilidad y session snapshot
- slash commands y `user-invocable`
- `disable-model-invocation`
- ciclo de vida de create/load/test/publish/install/update/deprecate/rollback

### Para agentes

Revisar como minimo:
- arquitectura multi-agente
- aislamiento `workspace` / `agentDir` / `sessions`
- bootstrap vs runtime state
- sandbox, tools y elevated
- routing, channels y bindings
- backup, restore y migracion de workspace
- deploy, operate y audit

## Regla operativa

Antes de declarar `ssot_reviewed: true`, extrae al menos:
- 1 restriccion de ubicacion o precedencia
- 1 restriccion de runtime o aislamiento
- 1 regla de lifecycle aplicable al caso actual

Si no puedes extraer esas tres piezas, el preflight no esta completo.

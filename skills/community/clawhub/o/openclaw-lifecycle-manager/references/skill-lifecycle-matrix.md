# Skill Lifecycle Matrix

Usa esta matriz cuando `artifact_kind=skill`.

## Fases

| Fase | Objetivo | Checkpoints minimos |
|---|---|---|
| Discover | Entender el trabajo reusable | trigger claro, forma del bundle, scope no excesivo |
| Create | Escribir `SKILL.md` y recursos | frontmatter valido, progressive disclosure, referencias precisas |
| Place | Decidir ubicacion | workspace vs managed/local vs bundled vs extraDirs |
| Validate | Verificar forma y eligibilidad | `openclaw skills list`, `--eligible`, `skills check`, slash si aplica |
| Load/Test | Probar activacion real | prompt con y sin skill, lazy-load, watcher/hot reload |
| Publish | Subir a ClawHub | version, changelog, tags, slug, rollback planeado |
| Install | Bajar a workspace activo | `openclaw skills install` o `clawhub install` |
| Update | Cambiar version o contenido | impacto en snapshot, watcher, backward compatibility |
| Rollback | Volver a version anterior | tags ClawHub, backup de workspace, restore controlado |
| Deprecate | Señalar reemplazo y salida | nueva ubicacion/version, docs de transicion, instalacion actualizada |
| Retire | Eliminar de circulacion | uninstall o remocion de dir, limpieza de references y tests |

## Reglas de ubicacion y precedencia

- `workspace`: maxima precedencia, per-agent
- `managed/local`: compartido entre agentes
- `bundled`: base distribuida
- `skills.load.extraDirs`: compartido custom, precedencia minima

Si hay conflicto de nombre, gana `workspace`, luego `managed/local`, luego `bundled`, luego `extraDirs`.

## Reglas de runtime

- El catalogo de skill se inyecta al inicio de sesion.
- El cuerpo de `SKILL.md` carga solo al activarse.
- El session snapshot queda congelado durante la sesion actual; cambios aplican al siguiente turn o siguiente sesion segun watcher.
- `disable-model-invocation: true` excluye el skill del prompt del modelo.
- `user-invocable: true` lo expone como slash command cuando la superficie lo soporta.

## Preguntas de control

- ¿Debe ser per-agent o compartida?
- ¿Debe ser slash-only o model-invocable?
- ¿La skill aporta procedimiento reusable real o solo texto ornamental?
- ¿Hay plan de publish/install/update/rollback?

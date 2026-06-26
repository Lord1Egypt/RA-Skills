# Agent Lifecycle Matrix

Usa esta matriz cuando `artifact_kind=agent`.

## Fases

| Fase | Objetivo | Checkpoints minimos | Skill hermana sugerida |
|---|---|---|---|
| Discover | Fijar alcance y restricciones OpenClaw | SSOT leida, dominio, canales, topology, sandbox, installs | `CM-OPENCLAW-KNOWLEDGE-NAVIGATOR` |
| Design | Definir blueprint native-first | bootstrap vs config, runtime exclusions, topology target | `CM-OPENCLAW-DESIGNER` |
| Create | Materializar bootstrap y workspace | `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `config.json` | `CM-OPENCLAW-BUILDER` |
| Contract | Derivar `platform_contract` | config projection, managed installs, deployment hints, provenance | `CM-OPENCLAW-CONTRACTOR` |
| Validate | Verificar consistencia del contrato | PASS/WARN justificado, colisiones, inputs pendientes | `CM-OPENCLAW-CONTRACT-VALIDATOR` |
| Handoff | Preparar siguiente paso operativo | contract validado, staging listo, manifest integro | `CM-OPENCLAW-HANDOFF` |
| Provision/Deploy | Ejecutar despliegue | auth, channels, compose/config, doctor, health, pairing, e2e | `CM-AGENT-DEPLOYER` |
| Operate | Gestion declarativa de runtime | drift, config viva, restarts, resync, hygiene | `CM-OPENCLAW-OPERATOR` |
| Audit | Verificar conformidad y salud | bootstrap/config, topology, sandbox, installs, runtime evidence | `CM-OPENCLAW-AUDITOR` |
| Evolve | Cambiar sin romper invariantes | impacto, compatibilidad, contract drift, migration path | `CM-OPENCLAW-EVOLVER` |
| Backup/Restore | Preservar o recuperar estado | backup de config/state/workspace, ruta de restore | esta skill o flujo operativo documentado |
| Deprecate/Retire | Sacar de circulacion con disciplina | handoff alternativo, backup, freeze, retiro de bindings/canales | esta skill + auditoria final |

## Invariantes de agente

- Cada agente tiene `workspace`, `agentDir` y `sessions` propios.
- `auth-profiles.json` es per-agent.
- Bootstrap y runtime state no se mezclan.
- Skills del agente viven en su workspace o en capas compartidas segun precedencia.
- Tool policy, sandbox y channels son parte del lifecycle, no detalles post-facto.

## Preguntas de control

- ¿El cambio vive en bootstrap, config nativa, contract o runtime?
- ¿Rompe routing, channels, auth o sandbox?
- ¿Requiere deploy o solo resync?
- ¿Hay backup verificable antes de una mutacion destructiva?

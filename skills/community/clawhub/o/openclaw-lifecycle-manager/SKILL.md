---
name: openclaw-lifecycle-manager
description: Gestiona el ciclo de vida de agentes y skills OpenClaw dentro de ClawForge. Usar para clasificar, validar, publicar, instalar, actualizar, deprecar o retirar agentes OpenClaw y skills OpenClaw, revisando siempre primero la SSOT local de OpenClaw.
_manifest:
  urn: urn:kora:skill:clawforge-openclaw-lifecycle-manager:1.0.0
  type: lazy_load_endofunctor
extensions:
  kora:
    skill:
      form: extended
      allowed_tools:
        - artifact_read
        - artifact_write
        - spec_consult
        - oc_docs_search
      requires: []
      references:
        - references/ssot-preflight.md
        - references/agent-lifecycle-matrix.md
        - references/skill-lifecycle-matrix.md
        - references/internal-routing-map.md
---

# CM-OPENCLAW-LIFECYCLE-MANAGER

## Proposito

Gestionar el ciclo de vida completo de agentes OpenClaw y skills OpenClaw dentro de ClawForge, imponiendo un preflight doctrinal obligatorio sobre la SSOT OpenClaw antes de clasificar, disenar, mutar, publicar, instalar, auditar, deprecar o retirar artefactos.

## Input/Output

- **Input:** artifact_kind: string (`agent`|`skill`), intent: string, target_path: string?, lifecycle_state: object?, runtime_evidence: object?
- **Output:** OpenClawLifecycleReport

## Procedimiento

0. **Preflight SSOT obligatorio.** Antes de hacer cualquier otra cosa, leer `references/ssot-preflight.md` y revisar los dos manuales canonicos alli listados. Si no se pueden leer, DETENERSE.
1. Clasificar el objeto:
   - `agent`: bootstrap, workspace, contract, handoff, deploy, operate, audit, deprecate, retire, backup, restore
   - `skill`: create, place, validate, load, publish, install, update, rollback, deprecate, retire
2. Clasificar la intencion exacta: `design`, `create`, `evolve`, `validate`, `deploy`, `operate`, `audit`, `publish`, `install`, `backup`, `restore`, `deprecate`, `retire`.
3. Si `artifact_kind=agent`, consultar `references/agent-lifecycle-matrix.md`.
4. Si `artifact_kind=skill`, consultar `references/skill-lifecycle-matrix.md`.
5. Consultar `references/internal-routing-map.md` para decidir si esta skill debe:
   - resolver el paso directamente
   - delegar el siguiente paso a una skill hermana de ClawForge
   - detenerse por falta de inputs criticos
6. Emitir siempre:
   - estado lifecycle actual
   - precondiciones satisfechas
   - invariantes OpenClaw relevantes
   - siguiente skill o siguiente comando
   - riesgos y rollback posible
7. No mutar artefactos ni runtime mientras el preflight SSOT no este explicitamente marcado como cumplido.

## Reglas Duras

1. Los dos manuales SSOT de OpenClaw se revisan primero, siempre.
2. No inferir comportamiento de agentes o skills desde costumbre local si contradice la SSOT.
3. Para agentes OpenClaw:
   - mantener aislamiento por `workspace`, `agentDir` y `sessions`
   - no mezclar bootstrap con runtime state
   - no compartir auth profiles entre agentes salvo operacion explicitamente controlada
4. Para skills OpenClaw:
   - respetar precedencia de ubicaciones
   - respetar gating, eligibilidad y snapshot de sesion
   - distinguir `workspace`, `managed/local`, `bundled` y `extraDirs`
5. No publicar, instalar o deprecar una skill sin validar antes su forma, ubicacion y estrategia de rollback.
6. No desplegar ni retirar un agente sin explicitar impacto en rutas, sessions, auth, sandbox, tools y canales.

## Signature Output

```yaml
lifecycle:
  artifact_kind: "agent"
  intent: "evolve"
  ssot_reviewed: true
  phase: "validate"
  target_path: "/path/to/artifact"
  preconditions_ok: true
  next_skill: "CM-OPENCLAW-CONTRACT-VALIDATOR"
  next_action: "validar contrato antes de handoff"
  blockers: []
  rollback:
    available: true
    mechanism: "backup + restore declarativo"
```

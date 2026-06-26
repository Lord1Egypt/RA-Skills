# Internal Routing Map

Usa este mapa despues del preflight SSOT para decidir el siguiente skill de ClawForge.

## Agentes OpenClaw

| Intent | Siguiente skill |
|---|---|
| entender plataforma o resolver duda factual | `CM-OPENCLAW-KNOWLEDGE-NAVIGATOR` |
| disenar blueprint | `CM-OPENCLAW-DESIGNER` |
| materializar bootstrap | `CM-OPENCLAW-BUILDER` |
| derivar contrato | `CM-OPENCLAW-CONTRACTOR` |
| validar contrato | `CM-OPENCLAW-CONTRACT-VALIDATOR` |
| preparar handoff | `CM-OPENCLAW-HANDOFF` |
| desplegar | `CM-AGENT-DEPLOYER` |
| operar runtime | `CM-OPENCLAW-OPERATOR` |
| auditar | `CM-OPENCLAW-AUDITOR` |
| evolucionar | `CM-OPENCLAW-EVOLVER` |

## Skills OpenClaw

| Intent | Resolucion |
|---|---|
| crear o restructurar bundle | esta misma skill gestiona el shape y el placement |
| validar precedencia o eligibilidad | esta misma skill + SSOT de skills |
| publicar o sincronizar con ClawHub | esta misma skill define el plan; la accion usa CLI OpenClaw/ClawHub |
| instalar o actualizar en workspace | esta misma skill define capa, comando y rollback |
| deprecar o retirar | esta misma skill define plan de transicion y limpieza |

## Regla de parada

Detener el flujo y devolver blockers si falta cualquiera de estos:
- SSOT no leida
- target path ambiguo
- artifact kind ambiguo
- intent mezclado con dos fases destructivas en el mismo paso
- inputs criticos de contract/deploy/publish sin resolver

---
name: lossless-claw-skill
description: Skill completo para lossless-claw (LCM). Incluye instrucciones para instalar el plugin automáticamente.
---

# Lossless Claw Skill

Skill completo para el plugin **lossless-claw** de OpenClaw. Este skill **proporciona las instrucciones para instalar el plugin** y luego usar las herramientas LCM.

---

## ⚠️ PRIMERO: Instalar el Plugin

**Este skill detecta si el plugin está instalado y te guiará para instalarlo.**

### Instalación automática:

Cuando un agente lee este skill, **debe verificar e instalar el plugin**:

```bash
# Verificar si el plugin está instalado
openclaw plugins list | grep lossless-claw

# Si NO está instalado → Instalarlo
openclaw plugins install @martian-engineering/lossless-claw
```

### Flujo automático del agente:

1. **Agente lee este skill** → Detecta que necesita el plugin
2. **Agente verifica** → `openclaw plugins list`
3. **Si no está** → Ofrece instalar: "Veo este skill pero falta el plugin. ¿Instalo?"
4. **Usuario acepta** → `openclaw plugins install @martian-engineering/lossless-claw`
5. **Restart gateway** → `openclaw gateway restart`
6. ✅ **Listo** → Herramientas `lcm_*` disponibles

---

## Instalación manual (si el agente no la ofrece):

**Paso 1: Instalar el plugin (infraestructura)**
```bash
openclaw plugins install @martian-engineering/lossless-claw
```

**Paso 2: Verificar instalación**
```bash
openclaw plugins list
# Deberías ver: lossless-claw | loaded | 0.5.3
```

**Paso 3: Restart gateway**
```bash
openclaw gateway restart
```

---

## Descripción

Este skill es un **wrapper seguro** para el plugin `lossless-claw` de OpenClaw. El plugin YA está instalado y proporcionando las herramientas `lcm_grep`, `lcm_describe`, y `lcm_expand_query`.

**Propósito:** Proporcionar una interfaz de usuario amigable para usar las herramientas LCM sin necesidad de recordar comandos complejos.

---

## ¿Qué es LCM?

**Lossless Context Management (LCM)** reemplaza el truncamiento de conversaciones antiguas con un sistema de resúmenes jerárquicos (DAG):

- ✅ **Todos los mensajes** se guardan en SQLite
- ✅ **Resúmenes inteligentes** de conversaciones antiguas
- ✅ **Búsqueda completa** en todo el historial
- ✅ **Expansión bajo demanda** - recupero detalles cuando necesito

---

## Uso

### 1. Buscar en el historial

```
lcm_grep "término de búsqueda" --limit 10
```

**Ejemplos:**
- `lcm_grep "Stripe" --limit 5` - Buscar menciones de Stripe
- `lcm_grep "deploy" --limit 10` - Buscar conversaciones sobre deploys
- `lcm_grep "vercel.*token" --mode regex` - Búsqueda con regex

### 2. Inspeccionar un resumen

```
lcm_describe --id sum_xxx
```

**Ejemplos:**
- `lcm_describe --id sum_abc123` - Ver detalles de un resumen específico
- `lcm_describe --id file_xyz789` - Ver archivo grande almacenado

### 3. Expansión profunda (deep recall)

```
lcm_expand_query --query "¿Qué decisiones tomamos sobre Vercel?"
```

**Ejemplos:**
- `lcm_expand_query --query "¿Qué APIs integramos?"`
- `lcm_expand_query --query "¿Cuál es el estado del proyecto?"`
- `lcm_expand_query --prompt "Resume las decisiones de pricing"`

---

## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `lcm_grep` | Buscar en todo el historial de conversaciones |
| `lcm_describe` | Inspeccionar un resumen o archivo específico |
| `lcm_expand` | Expandir un resumen para ver detalles |
| `lcm_expand_query` | Responder pregunta usando contexto expandido |

---

## Configuración Actual

El plugin está configurado con:

```json
{
  "freshTailCount": 64,
  "leafChunkTokens": 80000,
  "contextThreshold": 0.75,
  "incrementalMaxDepth": 1,
  "summaryModel": "gensee-397b/Gensee/Qwen3.5-397B"
}
```

**Significado:**
- `freshTailCount: 64` - Últimos 64 mensajes sin resumir
- `contextThreshold: 0.75` - Compacta al 75% del contexto
- `leafChunkTokens: 80000` - Máximo tokens por chunk antes de resumir

---

## Estado del Plugin

Para verificar el estado:

```bash
openclaw plugins list
```

Deberías ver:
```
Lossless Context Management | lossless-claw | loaded | 0.5.3
```

---

## Base de Datos

**Ubicación:** `/mnt/data/openclaw/workspace/.openclaw/lcm.db`

**Tamaño típico:** ~160KB después de varias conversaciones

**Verificar:**
```bash
ls -la /mnt/data/openclaw/workspace/.openclaw/lcm.db
```

---

## Troubleshooting

### Error: "lcm_grep no encontrado"

**Causa:** El plugin no está cargado

**Solución:**
```bash
openclaw gateway restart
```

### Error: "No conversation found"

**Causa:** No hay historial compactado aún

**Solución:** Esperar a que la conversación crezca y trigger compactación

### Búsqueda lenta

**Solución:** Habilitar FTS5 (full-text search):
```bash
openclaw lcm fts5 enable
```

---

## Sesiones de Larga Duración

El plugin está configurado para mantener sesiones vivas por **7 días** (10080 minutos).

**Cambiar duración:**
```json
{
  "session": {
    "reset": {
      "mode": "idle",
      "idleMinutes": 43200  // 30 días
    }
  }
}
```

---

## Seguridad

**Este skill es solo un wrapper** - no ejecuta código, solo documenta cómo usar las herramientas LCM que ya están disponibles.

**El plugin lossless-claw:**
- ✅ Código auditado (open source en GitHub)
- ✅ Datos locales (SQLite en tu máquina)
- ✅ Sin llamadas externas
- ✅ Sin credenciales requeridas

---

## Referencias

- **GitHub:** https://github.com/Martian-Engineering/lossless-claw
- **Documentación:** https://losslesscontext.ai
- **LCM Paper:** https://papers.voltropy.com/LCM

---

## Changelog

### v1.0.0 (2026-04-01)
- Creación del skill wrapper
- Documentación de herramientas LCM
- Guía de troubleshooting
- Referencias de seguridad

---

## License

MIT License - Libre uso, modificación y redistribución.

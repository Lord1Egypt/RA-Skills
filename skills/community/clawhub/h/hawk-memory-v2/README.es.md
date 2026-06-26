# 🦅 Context-Hawk

> **Guardián de Memoria Contextual para IA** — Deja de perder el hilo, empieza a recordar lo que importa.

*Dale a cualquier agente de IA una memoria que realmente funciona — a través de sesiones, temas y tiempo.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## ¿Qué hace?

La mayoría de los agentes de IA sufren de **amnesia** — cada nueva sesión comienza desde cero. Context-Hawk lo resuelve con un sistema de gestión de memoria de grado de producción que captura automáticamente lo que importa, deja que el ruido se disipe, y recupera el recuerdo correcto en el momento correcto.

**Sin Context-Hawk:**
> "¡Ya te lo dije — prefiero respuestas concisas!"
> (próxima sesión, el agente olvida otra vez)

**Con Context-Hawk:**
> (aplca silenciosamente tus preferencias de comunicación desde la sesión 1)
> ✅ Entrega respuesta concisa y directa cada vez

---

## ✨ 10 Funcionalidades Principales

| # | Funcionalidad | Descripción |
|---|---------|-------|
| 1 | **Persistencia de Estado de Tarea** | `hawk resume` — persiste el estado, recupera tras reinicio |
| 2 | **Memoria de 4 Niveles** | Working → Short → Long → Archive con decaimiento Weibull |
| 3 | **JSON Estructurado** | Puntuación de importancia (0-10), categoría, nivel, capas L0/L1/L2 |
| 4 | **Puntuación de Importancia IA** | Puntuación automática de recuerdos, descarta contenido de bajo valor |
| 5 | **5 Estrategias de Inyección** | A(alta-imp) / B(tarea) / C(reciente) / D(top5) / E(completo) |
| 6 | **5 Estrategias de Compresión** | summarize / extract / delete / promote / archive |
| 7 | **Auto-Introspección** | Verifica claridad de tarea, info faltante, detección de bucle |
| 8 | **Búsqueda Vectorial LanceDB** | Opcional — búsqueda híbrida vectorial + BM25 |
| 9 | **Fallback de Memoria Pura** | Funciona sin LanceDB, persistencia JSONL |
| 10 | **Autodeduplicación** | Fusiona automáticamente recuerdos duplicados |

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Sesión actual (últimos 5-10 turnos)     │
│       ↓ Decaimiento Weibull                                   │
│  Short-term      ←── Contenido 24h, resumido               │
│       ↓ access_count ≥ 10 + importancia ≥ 0.7             │
│  Long-term       ←── Conocimiento permanente, indexado vectorial│
│       ↓ >90 días o decay_score < 0.15                        │
│  Archive          ←── Histórico, cargado bajo demanda          │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Persistente entre reinicios (¡clave!)│
│  - Tarea actual / siguientes pasos / progreso / salidas        │
├──────────────────────────────────────────────────────────────┤
│  Motor de Inyección  ←── Estrategia A/B/C/D/E decide el recall│
│  Auto-Introspección ←── Cada respuesta verifica el contexto   │
│  Auto-Trigger        ←── Cada 10 turnos (configurable)       │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Memoria de Estado de Tarea (Característica Más Valiosa)

Incluso después de reinicio, corte de energía o cambio de sesión, Context-Hawk continúa exactamente donde lo dejó.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Completar la documentación de la API",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Revisar plantilla de arquitectura", "Informar al usuario"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["La cobertura debe alcanzar el 98%", "Las APIs deben estar versionadas"],
  "resumed_count": 3
}
```

```bash
hawk task "Completar la documentación"  # Crear tarea
hawk task --step 1 done             # Marcar paso completado
hawk resume                           # Recuperar tras reinicio ← ¡CLAVE!
```

---

## 🧠 Memoria Estructurada

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Contenido original completo",
  "summary": "Resumen en una línea",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Puntuación de Importancia

| Puntuación | Tipo | Acción |
|-------|------|--------|
| 0.9-1.0 | Decisiones/reglas/errores | Permanente, decaimiento más lento |
| 0.7-0.9 | Tareas/preferencias/conocimiento | Memoria largo plazo |
| 0.4-0.7 | Diálogo/discusión | Corto plazo, decaimiento a archivo |
| 0.0-0.4 | Chat/saludos | **Descartar, nunca almacenar** |

---

## 🎯 5 Estrategias de Inyección de Contexto

| Estrategia | Disparador | Ahorro |
|----------|-----------|--------|
| **A: Alta Importancia** | `importancia ≥ 0.7` | 60-70% |
| **B: Relacionada con Tarea** | scope coincide | 30-40% ← por defecto |
| **C: Reciente** | últimos 10 turnos | 50% |
| **D: Top5 Recall** | top 5 `access_count` | 70% |
| **E: Completo** | sin filtro | 100% |

---

## 🗜️ 5 Estrategias de Compresión

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 Sistema de Alerta de 4 Niveles

| Nivel | Umbral | Acción |
|-------|--------|--------|
| ✅ Normal | < 60% | Silencioso |
| 🟡 Vigilancia | 60-79% | Sugerir compresión |
| 🔴 Crítico | 80-94% | Pausar escritura auto, forzar sugerencia |
| 🚨 Peligro | ≥ 95% | Bloquear escrituras, comprimir obligatorio |

---

## 🚀 Inicio Rápido

```bash
# Instalar plugin LanceDB (recomendado)
openclaw plugins install memory-lancedb-pro@beta

# Activar skill
openclaw skills install ./context-hawk.skill

# Inicializar
hawk init

# Comandos esenciales
hawk task "Mi tarea"    # Crear tarea
hawk resume             # Recuperar última tarea ← MUY IMPORTANTE
hawk status            # Ver uso de contexto
hawk compress          # Comprimir memoria
hawk strategy B        # Cambiar a modo relacionado con tarea
hawk introspect         # Informe de auto-introspección
```

---

## Auto-Trigger: Cada N Turnos

Cada **10 turnos** (por defecto, configurable), Context-Hawk automáticamente:

1. Verifica nivel de contexto
2. Evalúa importancia de recuerdos
3. Te reporta el estado
4. Sugiere compresión si es necesario

```bash
# Config (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # verificar cada N turnos
  "keep_recent": 5,                 # preservar últimos N turnos
  "auto_compress_threshold": 70      # comprimir cuando > 70%
}
```

---

## Estructura de Archivos

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Herramienta CLI Python
└── references/
    ├── memory-system.md           # Arquitectura de 4 niveles
    ├── structured-memory.md      # Formato de memoria e importancia
    ├── task-state.md           # Persistencia de estado de tarea
    ├── injection-strategies.md  # 5 estrategias de inyección
    ├── compression-strategies.md # 5 estrategias de compresión
    ├── alerting.md             # Sistema de alerta
    ├── self-introspection.md   # Auto-introspección
    ├── lancedb-integration.md  # Integración LanceDB
    └── cli.md                  # Referencia CLI
```

---

## Especificaciones Técnicas

- **Persistencia**: Archivos JSONL locales, sin base de datos
- **Búsqueda Vectorial**: LanceDB (opcional), fallback automático a archivos
- **Cross-Agent**: Universal, sin lógica de negocio, funciona con cualquier agente IA
- **Cero Configuración**: Funciona listo para usar con valores predeterminados inteligentes
- **Extensible**: Estrategias de inyección personalizadas, políticas de compresión, reglas de puntuación

---

## Licencia

MIT — libre para usar, modificar y distribuir.

# 🔒 Vibe Codebase Audit - Guía de Uso en Español

## 📋 Descripción General

**Vibe Codebase Audit** es una herramienta de auditoría de seguridad integral diseñada para bases de código generadas por IA, con integración nativa de agentes, soporte multiproveedor y escaneo de seguridad de dependencias.

> 🎉 **NUEVO en v2.0**: Auditoría nativa de agentes (sin clave API), soporte multiproveedor, escaneo de dependencias, auditoría de configuración

---

## ⚡ Inicio Rápido

### Método 1: Auditoría Nativa de Agente (Recomendado, ¡Sin Configuración!)

```python
# ¡No se necesita clave API! Usar directamente el LLM del agente actual
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # Usar LLM del agente actual
)
```

### Método 2: Con Tu Clave API

```python
# Usar tu propia API de OpenAI/Claude/Otra
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # o "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### Método 3: Uso por CLI

```bash
# Usar LLM del agente (sin clave API)
python vibe_audit_enhanced.py /ruta/al/proyecto --provider agent_llm

# Usar OpenAI
python vibe_audit_enhanced.py /ruta/al/proyecto --provider openai

# Usar modelo local Ollama
python vibe_audit_enhanced.py /ruta/al/proyecto --provider ollama
```

---

## 🆕 Novedades en v2.0

### 1. 🤖 Integración Nativa de Agente
- **Sin configuración** - No se necesita clave API
- Usa la conexión LLM de tu agente actual
- Integración perfecta con OpenCode, Hermes, OpenClaw
- Menor costo - aprovecha la suscripción existente del agente

### 2. 🔌 Soporte Multiproveedor
- **Agent LLM** - Usar agente actual (recomendado)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Alternativa rentable
- **Qwen/Tongyi** - Modelos de Alibaba
- **Ollama** - Ejecutar modelos locales (¡gratis!)

### 3. 📦 Escaneo de Seguridad de Dependencias
- Verificar vulnerabilidades conocidas (CVE)
- Detectar dependencias obsoletas
- Verificación de cumplimiento de licencias
- Soporte: npm, pip, maven, cargo, go mod

### 4. ⚙️ Verificaciones de Seguridad de Configuración
- Detección de archivos .env expuestos
- Detección de mala configuración CORS
- Detección de modo depuración
- Verificaciones SSL

---

## 📊 Comparación de Herramientas

| Herramienta | Velocidad | Precisión | Funciones | Clave API | Mejor Para |
|-------------|-----------|-----------|-----------|-----------|------------|
| `vibe_audit_enhanced` | Media-Rápida | Alta | Todas | Opcional | **Producción** |
| `vibe_audit_scan` | Rápida | Media | Básicas | No | Verificaciones rápidas |
| `vibe_audit_multi_model` | Lenta | Máxima | Consenso AI | Sí | Proyectos críticos |
| `vibe_audit_incremental` | Muy Rápida | Media | Git-aware | Opcional | CI/CD |

---

## 🌐 Configuración de Proveedores

### Agent LLM (Recomendado)
```python
# ¡Sin configuración! Usar directamente:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (Local, Gratis)
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo
ollama pull llama2

# Usar en auditoría
primary_provider="ollama"
```

---

## 🚨 Niveles de Riesgo

| Nivel | Puntuación | Acción |
|-------|------------|--------|
| ✅ SEGURO | 0 | Listo para publicar |
| 🟢 BAJO | 1-19 | Problemas menores, revisión recomendada |
| 🟡 MEDIO | 20-49 | Revisar y corregir antes de publicar |
| 🟠 ALTO | 50-79 | Problemas significativos, correcciones requeridas |
| 🔴 CRÍTICO | 80-100 | **NO PUBLICAR** |

---

## 🤝 Agentes Soportados

- **OpenCode** - Habilidad nativa
- **Hermes** - Plugin
- **OpenClaw** - Importación de módulo
- **Clientes MCP** - Soporte de protocolo

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **Documentación**: Ver SKILL.md
- **Ejemplos**: Ver directorio examples/

---

**Publica con confianza. Audita con rigor. Programa en paz.** 🚀

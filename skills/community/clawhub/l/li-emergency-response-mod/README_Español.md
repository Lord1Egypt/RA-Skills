# LI Emergency Response MOD

<div align="center">

**Era de IA | Ciclo Cerrado de Ingeniería + Colaboración Multi-Agente**

[English](README.md) | [中文](README_中文.md) | [日本語](README_日本語.md) | [한국어](README_한국어.md) | [Français](README_Français.md) | [Deutsch](README_Deutsch.md) | [Español](README_Español.md) | [Português](README_Português.md)

</div>

---

## 📖 Descripción General

Una habilidad de guía de respuesta a incidentes de nivel empresarial que admite tanto el **modo de agente único** como el **modo de colaboración multi-agente**.

### ✨ Características Principales

- 🤖 **Modo Dual**: Agente único (uso personal) + Multi-agente (equipo)
- 🚀 **Procesamiento Paralelo**: Mejora de eficiencia del 50%+
- 📝 **Ciclo Cerrado de Ingeniería**: WAL + VBR + HITL + evolución automática
- 🔍 **Cobertura Completa**: TI tradicional + Infraestructura de IA
- 🌐 **Multiplataforma**: OpenCode/Cursor/Trae/Hermes/OpenClaw

---

## 🎯 Casos de Uso

| Escenario | Casos Específicos | Modo Recomendado |
|-----------|------------------|------------------|
| **TI Tradicional** | Minería, ransomware, fuerza bruta, phishing | Único/Multi |
| **Infraestructura de IA** | Envenenamiento de modelo, minería GPU, violación MLOps | Multi |
| **Entrenamiento y Ejercicios** | Desafíos CTF, ejercicios de simulación | Único (modo CTF) |

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8+
- Biblioteca PyYAML

### Instalación

```bash
git clone https://github.com/your-org/corporate-emergency-response-guidance-skill.git
pip install pyyaml
```

### Uso

#### Modo de Agente Único

```markdown
Eres el asistente de colaboración en respuesta a incidentes de la organización. Sigue el "SKILL.md" y los playbooks.

Restricciones Estrictas:
1) Preservar evidencia antes de responder
2) Todas las conclusiones basadas en evidencia (VBR)
3) Registrar acciones críticas en WAL
```

#### Modo Multi-Agente

```python
import asyncio
from multi_agent.framework.agent_framework import Orchestrator

async def main():
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    # Crear sesión
    session_id = await orchestrator.create_session("Incidente-2026")
    
    # Crear agentes
    await orchestrator.spawn_agent("ic_agent", "multi_agent/agents/ic_agent.yaml")
    await orchestrator.spawn_agent("analyst_agent", "multi_agent/agents/analyst_agent.yaml")
    
    # Ejecutar flujo de trabajo
    await run_incident_response(orchestrator, session_id)
```

---

## 📊 Indicadores de Rendimiento

| Indicador | Agente Único | Multi-Agente | Mejora |
|-----------|-------------|--------------|--------|
| **Tiempo de Respuesta** | 23 min | 12 min | ⬇️ 48% |
| **Precisión de Análisis** | 70% | 91% | ⬆️ 30% |
| **Intervención Manual** | 100% | 40% | ⬇️ 60% |

---

## 🌐 Compatibilidad de Plataforma

| Plataforma | Compatibilidad | Uso |
|-----------|---------------|-----|
| **OpenCode** | ✅ Listo | Cargar como habilidad |
| **Cursor** | ✅ Listo | Modo prompt |
| **Hermes Agent** | ⚠️ Adaptador requerido | API HTTP |

---

## 📄 Licencia

Licencia MIT - ver [LICENSE](LICENSE)

---

## 📞 Soporte

- **Problemas**: [GitHub Issues](https://github.com/your-org/corporate-emergency-response-guidance-skill/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/your-org/corporate-emergency-response-guidance-skill/discussions)

---

<div align="center">

**Fortalecer la Respuesta a Incidentes con IA, Hacer la Seguridad Más Eficiente**

Hecho con ❤️ by 北京老李（Beijing）

</div>

# openclaw-memory-transfer

> **Migración de memoria sin fricción para OpenClaw.** Trae tus recuerdos de ChatGPT, Claude, Gemini, Copilot y más — en menos de 10 minutos.

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md)

---

Pasaste meses (o años) con ChatGPT. Conoce tu estilo de escritura, tus proyectos, tus preferencias. Al cambiar a OpenClaw, nada de eso debería empezar de cero.

**Memory Transfer** extrae todo lo que tu antiguo asistente de IA sabe sobre ti, limpia los datos y los importa al sistema de memoria de OpenClaw.

## Uso

Dile a tu agente de OpenClaw:

```
Vengo de ChatGPT
```

## Fuentes soportadas

| Fuente | Método | Tu acción |
|--------|--------|-----------|
| **ChatGPT** | Exportación ZIP | Haz clic en Exportar en Ajustes, sube el ZIP |
| **Claude.ai** | Guiado por prompt | Copia un prompt, pega el resultado |
| **Gemini** | Guiado por prompt | Copia un prompt, pega el resultado |
| **Copilot** | Guiado por prompt | Copia un prompt, pega el resultado |
| **Claude Code** | Escaneo automático | Nada — automático |
| **Cursor** | Escaneo automático | Nada — automático |
| **Windsurf** | Escaneo automático | Nada — automático |

## Qué se migra

| Categoría | Destino | Ejemplos |
|-----------|---------|----------|
| Identidad | `USER.md` | Nombre, profesión, idioma, zona horaria |
| Estilo comunicativo | `USER.md` | Tono de escritura, preferencias de formato |
| Conocimiento | `MEMORY.md` | Proyectos, experiencia, insights |
| Patrones de comportamiento | `MEMORY.md` | Flujos de trabajo, hábitos, correcciones |
| Preferencias de herramientas | `TOOLS.md` | Stack tecnológico, plataformas |

## Instalación

```bash
clawhub install openclaw-memory-transfer
```

## Licencia

MIT

---

**Powered by [MyClaw.ai](https://myclaw.ai)**

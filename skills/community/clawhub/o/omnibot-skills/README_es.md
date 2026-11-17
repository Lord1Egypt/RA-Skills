<div align="center">

# 🤖 Omnibot

### Infraestructura de Navegador para Agentes de IA

[![Version](https://img.shields.io/badge/version-2.4.0-blue?style=flat-square)](./SKILL.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[![SkillHub](https://img.shields.io/badge/SkillHub-omnibot-00A8E0?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAwTDAgNFYxMkw4IDE2TDE2IDEyVjRMOCAwWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://skillhub.cn/skills/omnibot)
[![ClawHub](https://img.shields.io/badge/ClawHub-omnibot--skills-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAxQzQuMTMgMSAxIDQuMTMgMSA4QzEgMTEuODcgNC4xMyAxNSA4IDE1QzExLjg3IDE1IDE1IDExLjg3IDE1IDhDMTUgNC4xMyAxMS44NyAxIDggMVpNOCAzQzkuNjYgMyAxMSA0LjM0IDExIDZDMTEgNy42NiA5LjY2IDkgOCA5QzYuMzQgOSA1IDcuNjYgNSA2QzUgNC4zNCA2LjM0IDMgOCAzWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://clawhub.ai/dennisjcy/skills/omnibot-skills)

[![Chrome Web Store](https://img.shields.io/badge/Chrome%20Web%20Store-Extensión%20de%20Navegador-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)

**Conecta agentes de IA a un navegador Chromium real.**<br>
Lee páginas. Haz clic en botones. Rellena formularios. Navega. Extrae contenido. Recopila evidencia.<br>
Todo a través de un demonio local y CLI — sin trucos headless, sin selectores frágiles.

[Inicio Rápido](#-inicio-rápido) · [Cómo Funciona](#-cómo-funciona) · [Características](#-características) · [Documentación](#-documentación)

🌐 **[English](./README.md)** · **[中文](./README_zh.md)** · **[日本語](./README_ja.md)** · **[한국어](./README_ko.md)** · **[Français](./README_fr.md)** · **[Deutsch](./README_de.md)**

</div>

---

## 🚀 ¿Qué es Omnibot?

Omnibot cierra la brecha entre los agentes de IA y la web real. Da a agentes como **Hermes**, **Claude Code**, **Codex**, **OpenCode** y otros la capacidad de ver e interactuar con un navegador Chromium vivo — de la misma manera que lo hace un humano.

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│   AI Agent   │ ──CLI──▶│  Omnibot     │ ──WS──▶ │  Chromium        │
│  (Hermes,    │         │  Demonio     │         │  Extensión       │
│   Claude...) │         │  :18765      │         │  (Navegador Real)│
└──────────────┘         └──────────────┘         └──────────────────┘
```

Sin Puppeteer. Sin Playwright. Sin navegador headless fingiendo ser real.<br>
**Un navegador real. Cookies reales. Extensiones reales. Sesiones de usuario reales.**

## 🎬 Demostraciones en Video

<table>
<tr>
<td width="50%" align="center" valign="top">

### Análisis de Cuenta Oficial de WeChat
**Hermes analiza automáticamente datos y tendencias de WeChat**

[![Análisis de WeChat](https://img.youtube.com/vi/xZ-_0TInCRE/maxresdefault.jpg)](https://youtu.be/xZ-_0TInCRE)

*El agente Hermes inicia sesión automáticamente en el backend de la Cuenta Oficial de WeChat, extrae crecimiento de usuarios, lecturas de artículos, demografía de usuarios y genera un informe completo de análisis de datos.*

</td>
<td width="50%" align="center" valign="top">

### Agregador de Noticias de IA en X (Twitter)
**Hermes navega X automáticamente para obtener las últimas noticias de IA**

[![Noticias de IA en X](https://img.youtube.com/vi/PknnOhAE6bI/maxresdefault.jpg)](https://youtu.be/PknnOhAE6bI)

*El agente Hermes navega automáticamente por X (Twitter), busca y filtra las últimas noticias de IA, y las organiza en un resumen estructurado.*

</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">

### Análisis de Documentos Judiciales
**Hermes busca y analiza veredictos de homicidios**

[![Análisis Judicial](https://img.youtube.com/vi/PQQNDbzgXgQ/maxresdefault.jpg)](https://youtu.be/PQQNDbzgXgQ)

*El agente Hermes busca en registros judiciales casos de homicidio, lee 8 archivos de casos completos y genera un informe de análisis completo que incluye perfiles de delincuentes, análisis de motivos y patrones de crimen.*

</td>
<td width="50%" align="center" valign="top">

### Publicación Automática en Toutiao
**Hermes publica artículos en Toutiao automáticamente**

[![Publicación en Toutiao](https://img.youtube.com/vi/elUxHLp1C4Q/maxresdefault.jpg)](https://youtu.be/elUxHLp1C4Q)

*El agente Hermes inicia sesión automáticamente en Toutiao, completa título, texto del cuerpo, inserta imágenes, configura portada y ganancias por anuncios, previsualiza y publica el artículo con un solo clic.*

</td>
</tr>
</table>

<div align="center">

**¡Más casos de uso te están esperando!**

</div>

## ✨ Características

<table>
<tr>
<td width="50%" valign="top">

### 🔍 Observar
- Lee contenido de página renderizado como texto/Markdown limpio
- Captura el árbol de accesibilidad completo con referencias interactivas
- Captura pantallas de páginas completas o regiones visuales específicas
- Inspecciona registros de consola, tráfico de red y estado del DOM

</td>
<td width="50%" valign="top">

### 🎯 Actuar
- Haz clic en elementos por rol semántico, placeholder o referencia de accesibilidad
- Rellena formularios, selecciona opciones, marca casillas — con despacho de eventos
- Navega entre páginas, gestiona pestañas y grupos de pestañas
- Arrastra, desplaza, escribe, presiona teclas — interacción humana

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✅ Verificar
- Espera condiciones: cambios de URL, visibilidad de elementos, aparición de texto
- Afirma estado de elementos: habilitado, visible, marcado, valor
- Captura registros de red y evidencia de API
- Verificación multi-paso con bucles observar → actuar → verificar

</td>
<td width="50%" valign="top">

### 🛡️ Confiable
- Aislamiento de flujo de trabajo con token de sesión
- Comandos dirigidos a pestañas — sin mutaciones cruzadas accidentales
- Cadena de respaldo de 7 niveles desde semántico hasta CDP crudo
- Guardas anti-patrones integradas y reglas de seguridad

</td>
</tr>
</table>

## ⚡ Inicio Rápido

### 1. Instala el CLI

Instala Omnibot CLI globalmente vía npm (recomendado):

```bash
npm install -g @omniaibot/omnibot
```

Detecta automáticamente tu plataforma e instala el binario correspondiente. Después de la instalación, ejecuta `omnibot doctor` para verificar.

### 2. Carga la Extensión del Navegador

- Abre la [página de la extensión Omnibot en Chrome Web Store](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)
- Haz clic en **Añadir a Chrome** y completa la instalación
- Haz clic en el icono de la extensión Omnibot en la esquina superior derecha de tu navegador
- Confirma que la extensión muestra **Conectado**, o copia el código de máquina del popup para comprar un código de activación

Por defecto, la extensión se conecta al servicio WebSocket local en `127.0.0.1:18765`.

Configuración del popup de la extensión:
- **Dirección WebSocket**: `ws://127.0.0.1:18765`
- El estado de conexión se actualiza automáticamente
- Si la conexión falla, ejecuta primero `omnibot doctor` para verificar el estado del demonio

### 3. Verifica la Conexión

No necesitas iniciar manualmente el demonio. Al ejecutar cualquier comando del navegador, el CLI de omnibot iniciará automáticamente el demonio local, y la extensión del navegador se conectará vía WebSocket a `127.0.0.1:18765`.

```bash
omnibot doctor
omnibot tabs
```

`doctor` verifica el estado del demonio y la extensión. `tabs` lista las pestañas disponibles del navegador.

Si `doctor` muestra que la extensión no está conectada, abre Chrome/Edge, carga o recarga la extensión del navegador, y mantén al menos una pestaña HTTP/HTTPS abierta.

### 4. Instala las Habilidades del Agente

Omnibot v2 usa habilidades en lugar de inyección de prompts MCP:

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
```

Ver las rutas de habilidades integradas:

```bash
omnibot skills path
```

Omnibot viene con configuraciones de habilidades integradas para agentes de IA populares. Selecciona tu agente desde la página de inicio rápido para obtener el comando de instalación.

## 🔄 Cómo Funciona

Cada operación de navegador sigue un bucle disciplinado:

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Observar │ ───▶ │  Actuar  │ ───▶ │ Verificar│──┐
  │          │      │ (una vez)│      │          │  │
  └──────────┘      └──────────┘      └──────────┘  │
       ▲                                              │
       └──────────── reintentar con respaldo ─────────┘
```

1. **Observar** — captura la página, lee contenido, verifica el estado actual
2. **Actuar** — realiza una operación usando el mejor patrón disponible
3. **Verificar** — confirma el cambio de estado esperado con evidencia

Si la verificación falla, el agente vuelve a observar e intenta el siguiente nivel de respaldo. Sin reintentos ciegos. Sin adivinanzas.

## 🧩 Enrutador de Comandos Nativos

Omnibot siempre elige el comando nativo más estrecho para el trabajo:

| Intención | Comando Nativo | No Esto |
|-----------|---------------|---------|
| Leer contenido de página | `read`, `get text` | ~~`execute-js`~~ |
| Hacer clic en un botón | `find --action click`, `click @eN` | ~~`querySelector().click()`~~ |
| Rellenar un formulario | `fill`, `type` | ~~`element.value = "..."`~~ |
| Esperar estado | `wait` | ~~`sleep 3`~~ |
| Desplazar | `scroll`, `scrollintoview` | ~~`window.scrollTo()`~~ |

**Nativo primero. JavaScript es un respaldo, no un atajo.**

## 🏗️ Arquitectura

```
Agent Skill (SKILL.md)
    │
    ▼
omnibot CLI  ──────────────────────────────┐
    │                                       │
    ▼                                       ▼
Demonio Local (:18765)              Extensión Chromium
    │                                       │
    ├── Gestión de sesiones                 ├── Acceso al DOM
    ├── Enrutamiento de comandos            ├── Árbol de accesibilidad
    ├── Seguimiento de pestañas             ├── Intercepción de red
    └── Aislamiento de flujo de trabajo     └── Detección de regiones visuales
```

**Principios de diseño clave:**
- **Fiabilidad > Conveniencia** — cada acción se verifica
- **Estado Explícito > Estado Implícito** — sin suposiciones ocultas
- **Patrón > Comando** — comienza desde la tarea, no la API
- **El respaldo está permitido, pero nunca primero**

## 📚 Documentación

| Recurso | Descripción |
|---------|-------------|
| [SKILL.md](./SKILL.md) | Especificación completa de ejecución de agente |
| [Referencia de Comandos](./references/command-reference.md) | Búsqueda completa de comandos CLI |
| [Patrones de Operación](./references/operation-patterns.md) | Leer, hacer clic, rellenar, desplazar, navegar, esperar, extraer, lote |
| [Anti-Patrones](./references/anti-patterns.md) | Errores comunes y cómo evitarlos |
| [Depuración y Evidencia](./references/debugging-and-evidence.md) | Capturas de pantalla, registros de red, traza, grabación/reproducción |
| [Sesiones y Pestañas](./references/session-and-tabs.md) | Aislamiento de flujo de trabajo y direccionamiento de pestañas |
| [Operaciones de Respaldo](./references/fallback-operations.md) | Cadena de respaldo de 7 niveles explicada |

## 🤝 Agentes Compatibles

Omnibot funciona con cualquier sistema de agente que pueda ejecutar comandos CLI:

- 🧠 **Hermes** — integración nativa
- 🟠 **Claude Code** — a través de archivo de habilidad
- 📦 **Codex** — a través de archivo de habilidad
- 🔓 **OpenCode** — a través de archivo de habilidad
- 🔧 **Cualquier agente compatible con CLI** — a través de comandos `omnibot`

## 📋 Ejemplo de Flujo de Trabajo

```bash
# Establecer contexto de flujo de trabajo
export OMNIBOT_SESSION_TOKEN=research

# Abrir una nueva pestaña
omnibot open "https://github.com"

# Capturar página con referencias interactivas
omnibot snapshot -i --tab-id $TAB_ID

# Hacer clic en el cuadro de búsqueda y escribir
omnibot find placeholder "Search GitHub" --action type \
  --action-value "omnibot" --tab-id $TAB_ID

# Presionar Enter
omnibot press Enter --tab-id $TAB_ID

# Esperar resultados
omnibot wait --text "repositories" --tab-id $TAB_ID

# Leer los resultados
omnibot read --tab-id $TAB_ID
```

## 📄 Licencia

Propietaria. Ver LICENSE para detalles.

---

<div align="center">

**Construido para agentes que necesitan ver la web — no solo obtenerla.**

[⭐ Estrella en GitHub](https://github.com/DennisJcy/Omnibot-skills) · [📖 Leer la Especificación de Habilidad](./SKILL.md)

</div>

---
name: openclaw-3d-blender-mcp
description: Instalación completa de Blender MCP para OpenClaw. Incluye setup local/remoto, ngrok, verificación, troubleshooting y estudio de 3 recursos obligatorios (blender-mcp repo, blender-orchestrator, video tutorial).
---

# OpenClaw 3D Blender MCP Skill

Skill completo para instalar, configurar y usar Blender MCP con OpenClaw. Incluye todo lo necesario para empezar a crear personajes 3D.

---

## ⚠️ Step 0: Estudiar Recursos (ANTES de Instalar)

**Estudia estos 3 recursos primero** (~40 minutos):

1. **blender-mcp Official Repo** - https://github.com/ahujasid/blender-mcp (~15 min)
   - Instalación oficial, herramientas soportadas, configuración
2. **blender-orchestrator** - https://github.com/mlolson/blender-orchestrator (~15 min)
   - Spatial reasoning, real-world dimensions (55+ objetos)
3. **Video: "I Made Claude Use Blender"** - https://www.youtube.com/watch?v=dxlyCPGCvy8 (~10 min)
   - Setup completo, demo en vivo, ejemplos prácticos

**¿Por qué estudiar primero?** Evita errores de posicionamiento, enseña coordenadas relativas, muestra ejemplos de éxito.

---

## Step 1: Verificar Prerrequisitos

```bash
python3 --version  # Need 3.10+
which uv  # Install: brew install uv (macOS)
```

---

## Step 2: Elegir Tipo de Setup

### Opción A: Local (Misma Computadora)

```bash
uvx blender-mcp
```

Configurar MCP:
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"],
      "env": {
        "BLENDER_HOST": "localhost",
        "BLENDER_PORT": "9876",
        "DISABLE_TELEMETRY": "true"
      }
    }
  }
}
```

Instalar addon en Blender:
- Descargar de https://github.com/ahujasid/blender-mcp
- Blender: Edit → Preferences → Add-ons → Install
- Presionar N en viewport → BlenderMCP → Connect

### Opción B: Remoto (Diferente Computadora)

En computadora con Blender:
```bash
ngrok tcp 9876
# Guardar URL: tcp://X.tcp.eu.ngrok.io:PORT
```

En OpenClaw:
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"],
      "env": {
        "BLENDER_HOST": "X.tcp.eu.ngrok.io",
        "BLENDER_PORT": "PORT"
      }
    }
  }
}
```

---

## Step 3: Verificar Conexión

```bash
python3 scripts/verify_blender_connection.py
```

**Output esperado:**
```
✅ Conexión TCP: OK
✅ MCP inicializado
✅ CUBO CREADO - TEST_CUBE_CONNECTION
✅ VERIFICACIÓN COMPLETADA
```

---

## Step 4: Inspeccionar Escena

```bash
python3 scripts/get_scene_info.py
```

Muestra: total objetos, lista con nombres, ubicaciones (X,Y,Z).

---

## 🔧 Troubleshooting

### Error: "Connection refused"
**Fix:** Verificar ngrok corriendo y addon conectado en Blender.

### Error: "Invalid request parameters"
**Fix:** Usar formato `tools/call` correcto:
```python
send("tools/call", {
    "name": "execute_blender_code",
    "arguments": {"user_prompt": "Desc", "code": "..."}
})
```

### Error: Objetos en ubicación incorrecta
**Fix:** Usar coordenadas relativas al padre, no absolutas.

### Error: Materiales no visibles
**Fix:** Decir usuario "Presiona Z → Material Preview".

---

## 📚 Recursos Incluidos

- `scripts/verify_blender_connection.py` - Test de conexión
- `scripts/get_scene_info.py` - Info de escena
- `references/coordinate_system.md` - Coordenadas Blender
- `references/common_errors.md` - 10 errores + soluciones

---

## 🎯 Mejores Prácticas

- ✅ Usar coordenadas relativas (parent-based)
- ✅ Aplicar parenting para objetos relacionados
- ✅ Verificar después de cada creación
- ✅ Usar Subdivision Surface para orgánicos
- ✅ Guardar frecuentemente (.blend)

---

## 📐 Referencia Rápida de Coordenadas

**Ejes Blender:** X (Derecha/+), Y (Frente/+), Z (Arriba/+)

**Personaje en origen:**
- Pies: Z 0-3
- Rodillas: Z 5-8
- Caderas: Z 8-10
- Torso: Z 10-13
- Hombros: Z 13-14, X ±1.5
- Cabeza: Z 14-17
- Ojos: Z 16, Y 1.5

**Estilo Pixar:**
- Radio cabeza: 1.4-1.6 (vs 1.0 realista)
- Radio ojos: 0.4 (vs 0.2 realista)

---

*Versión: 1.0.0 | 2026-04-01 | Basado en 4 ciclos de desarrollo (~90 min)*

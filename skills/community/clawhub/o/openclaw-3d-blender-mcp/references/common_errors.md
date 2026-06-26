# Errores Comunes en Blender MCP - Soluciones

## Índice de Errores

1. [Connection Refused](#connection-refused)
2. [Invalid Request Parameters](#invalid-request-parameters)
3. [Objetos en Ubicación Incorrecta](#objetos-en-ubicación-incorrecta)
4. [Materiales No Se Ven](#materiales-no-se-ven)
5. [Subdivision No Funciona](#subdivision-no-funciona)
6. [Shape Keys Dan Error](#shape-keys-dan-error)
7. [ngrok URL Cambia](#ngrok-url-cambia)
8. [Objetos No Siguen al Padre](#objetos-no-siguen-al-padre)
9. [Código Python No Se Ejecuta](#código-python-no-se-ejecuta)
10. [Render Se Ve Negro](#render-se-ve-negro)

---

## Connection Refused

### Síntoma:
```
ConnectionRefusedError: [Errno 111] Connection refused
TimeoutError: Connection timed out
```

### Causas:

1. **ngrok no está corriendo** (setup remoto)
2. **Addon no está activado** en Blender
3. **Panel BlenderMCP no está conectado**
4. **Puerto incorrecto** en configuración

### Solución:

```bash
# 1. Verificar ngrok (setup remoto)
ngrok tcp 9876

# Deberías ver:
# Forwarding: tcp://5.tcp.eu.ngrok.io:18724 -> localhost:9876

# 2. En Blender, verificar addon:
# Edit → Preferences → Add-ons
# Buscar "Blender MCP" y activar checkbox ✓

# 3. En viewport 3D de Blender:
# - Presionar N
# - Pestaña "BlenderMCP"
# - Click "Connect to Claude" o "Connect to MCP server"

# 4. Verificar variables de entorno:
export BLENDER_HOST="5.tcp.eu.ngrok.io"  # o "localhost" para local
export BLENDER_PORT="18724"              # o "9876" para local
```

### Verificación:
```bash
python3 scripts/verify_blender_connection.py
```

---

## Invalid Request Parameters

### Síntoma:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Invalid request parameters"
  }
}
```

### Causa:
Formato incorrecto de llamada MCP. Estás usando el formato antiguo en vez del nuevo `tools/call`.

### Solución:

```python
# ❌ INCORRECTO (formato viejo)
send("execute_blender_code", {
    "code": "import bpy; print('hello')"
})

# ✅ CORRECTO (formato nuevo con tools/call)
send("tools/call", {
    "name": "execute_blender_code",
    "arguments": {
        "user_prompt": "Create a test cube",
        "code": "import bpy; bpy.ops.mesh.primitive_cube_add()"
    }
})
```

**Estructura requerida:**
```python
{
    "jsonrpc": "2.0",
    "id": <number>,
    "method": "tools/call",
    "params": {
        "name": "<tool_name>",
        "arguments": {
            "user_prompt": "<description>",
            "code": "<python_code>"  # si aplica
        }
    }
}
```

---

## Objetos en Ubicación Incorrecta

### Síntoma:
- Cordones de zapatos aparecen en el suelo (0,0,0)
- Accesorios no están donde deberían
- Elementos desalineados del personaje

### Causa:
Usaste **coordenadas absolutas** en vez de **coordenadas relativas al padre**.

### Solución:

```python
# ❌ INCORRECTO (coordenadas fijas)
bpy.ops.mesh.primitive_cylinder_add(
    location=(5.4, 0.5, 13.8)  # Posición absoluta
)

# ✅ CORRECTO (relativo al objeto padre)
hand = bpy.data.objects.get("CHAR_Hand_Left")
if hand:
    # Calcular relativo a la posición de la mano
    lace_loc = (
        hand.location.x - 0.15,  # 15cm hacia adentro
        hand.location.y + 0.1,   # 10cm hacia adelante
        hand.location.z          # misma altura
    )
    bpy.ops.mesh.primitive_cylinder_add(location=lace_loc)
    
    # Y hacer parenting para que siga a la mano
    lace.parent = hand
```

### Prevención:

Siempre que crees un objeto que debería estar asociado a otro:

1. **Obtén referencia al objeto padre**
2. **Calcula posición relativa**
3. **Establece parenting** inmediatamente

```python
# Patrón recomendado
parent = bpy.data.objects.get("ParentName")
if parent:
    # Crear hijo en posición relativa
    bpy.ops.mesh.primitive_XXX_add(
        location=(
            parent.location.x + offset_x,
            parent.location.y + offset_y,
            parent.location.z + offset_z
        )
    )
    child = bpy.context.active.object
    child.parent = parent
```

---

## Materiales No Se Ven

### Síntoma:
- Objetos aparecen grises en viewport
- Colores no se muestran
- Materiales aplicados pero no visibles

### Causas:

1. **Viewport en modo "Solid"** en vez de "Material Preview"
2. **Material no asignado** al objeto
3. **Nodos no configurados** correctamente

### Solución:

**1. Cambiar vista a Material Preview:**
```
En Blender:
- Presionar Z
- Seleccionar "Material Preview"
```

**2. Verificar material asignado:**
```python
# Verificar que el material está en la lista del objeto
print(obj.material_slots)

# Si está vacío, asignar material
if len(obj.material_slots) == 0:
    obj.data.materials.append(material)
```

**3. Configurar nodos correctamente:**
```python
mat = bpy.data.materials.new(name="MyMaterial")
mat.use_nodes = True  # ← ¡Esto es importante!

nodes = mat.node_tree.nodes
bsdf = nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1)  # Rojo

obj.data.materials.append(mat)
```

---

## Subdivision No Funciona

### Síntoma:
- Objeto sigue viéndose "low poly" después de añadir Subdivision
- No hay suavizado visible

### Causas:

1. **Modifier no configurado** con niveles suficientes
2. **Modifier no aplicado** (solo vista previa)
3. **Malla muy simple** (no hay suficientes vértices para subdividir)

### Solución:

```python
# 1. Configurar modifier con niveles adecuados
mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
mod.levels = 2           # Vista previa en viewport
mod.render_levels = 3    # Nivel para render final

# 2. O aplicar el modifier permanentemente
bpy.ops.object.modifier_apply(modifier="Subdivision")

# 3. Para mallas muy simples, añadir loop cuts primero
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.loopcut_slide(cuts=2)
bpy.ops.object.mode_set(mode='OBJECT')
```

**Niveles recomendados:**
- Personajes orgánicos: levels=2, render_levels=3
- Objetos duros: levels=1, render_levels=2
- Para performance: levels=1, render_levels=1

---

## Shape Keys Dan Error

### Síntoma:
```
RuntimeError: Key block not found
Error: Failed to create shape key
```

### Causas:

1. **No existe shape key "Basis"** primero
2. **Número de vértices diferente** entre shape keys
3. **Objeto no es mesh** o no editable

### Solución:

```python
obj = bpy.data.objects.get("MyObject")

if obj and obj.type == 'MESH':
    # 1. Crear shape key base PRIMERO
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")
    
    # 2. Ahora crear shape keys derivadas
    blink = obj.shape_key_add(name="Blink")
    
    # 3. Modificar vértices (mismo count siempre)
    for i, vert in enumerate(blink.data):
        if vert.co.y > threshold:  # Solo vértices del párpado
            vert.co.y -= 0.3  # Bajar párpado
    
    # 4. Para animar, usar value (0.0 = Basis, 1.0 = Shape completo)
    blink.value = 1.0  # Activar shape key completamente
```

**Importante:**
- Siempre crear "Basis" primero
- No cambiar topología después de crear shape keys
- Usar `value` para animar entre 0.0 y 1.0

---

## ngrok URL Cambia

### Síntoma:
- Cada vez que reinicias ngrok, la URL es diferente
- Configuración MCP queda obsoleta

### Causa:
ngrok free tier genera URLs dinámicas aleatorias.

### Soluciones:

**Opción A: Leer URL dinámicamente (recomendado)**

```python
import requests

# ngrok expone API local en puerto 4040
resp = requests.get('http://localhost:4040/api/tunnels')
tunnels = resp.json()['tunnels']

for tunnel in tunnels:
    if tunnel['proto'] == 'tcp':
        public_url = tunnel['public_url']
        # Ej: "tcp://5.tcp.eu.ngrok.io:18724"
        host, port = public_url.replace('tcp://', '').split(':')
        print(f"Host: {host}, Port: {port}")
        # Actualizar configuración MCP automáticamente
```

**Opción B: ngrok paid (URL estática)**

```bash
# Con cuenta paid, puedes reservar URL fija
ngrok tcp 9876 --region eu --subdomain mi-blender
```

**Opción C: Actualizar manualmente cada sesión**

1. Iniciar ngrok
2. Copiar URL que aparece
3. Actualizar variables de entorno:
```bash
export BLENDER_HOST="5.tcp.eu.ngrok.io"
export BLENDER_PORT="18724"
```
4. Reiniciar MCP server

---

## Objetos No Siguen al Padre

### Síntoma:
- Hijo no se mueve cuando mueves al padre
- Parenting no funciona como esperado

### Causas:

1. **Parenting no establecido** correctamente
2. **Transformadas no aplicadas** antes de parenting
3. **Matrix parent inverse** no calculado

### Solución:

```python
# Método 1: Parenting simple (funciona en 90% de casos)
child.parent = parent

# Método 2: Parenting con transform preservado (más robusto)
child.parent = parent
child.matrix_parent_inverse = parent.matrix_world.inverted()

# Método 3: Parenting con offset específico
child.parent = parent
child.location = (offset_x, offset_y, offset_z)  # En espacio local del padre
```

**Verificación:**
```python
# Verificar parenting
print(f"Child: {child.name}")
print(f"Parent: {child.parent.name if child.parent else 'None'}")

# Mover padre y verificar que hijo sigue
parent.location.x += 1
print(f"Child new location: {child.location}")  # Debería haber cambiado
```

---

## Código Python No Se Ejecuta

### Síntoma:
- No hay error pero tampoco hay efecto en Blender
- Print statements no aparecen
- Objetos no se crean

### Causas:

1. **Error en sintaxis** de Python
2. **Contexto incorrecto** (edit mode vs object mode)
3. **Timeout muy corto** en MCP call

### Solución:

```python
# 1. Añadir print statements para debug
code = """
import bpy
print("=== SCRIPT START ===")
try:
    bpy.ops.mesh.primitive_cube_add()
    print("✅ Cube created")
except Exception as e:
    print(f"❌ Error: {e}")
print("=== SCRIPT END ===")
"""

# 2. Aumentar timeout para scripts complejos
resp = send("tools/call", {
    "name": "execute_blender_code",
    "arguments": {"user_prompt": "Test", "code": code}
}, timeout=30)  # ← Aumentar de 10 a 30 segundos

# 3. Verificar modo de objeto
code = """
import bpy
print(f"Current mode: {bpy.context.object.mode if bpy.context.object else 'No active object'}")

# Si necesitas edit mode:
bpy.ops.object.mode_set(mode='EDIT')
# ... operaciones de mesh ...
bpy.ops.object.mode_set(mode='OBJECT')
"""
```

---

## Render Se Ve Negro

### Síntoma:
- Render F12 produce imagen completamente negra
- Viewport se ve bien pero render no

### Causas:

1. **Sin luces** en la escena
2. **Materiales con emisión** pero sin luz real
3. **Cámara mirando a nada**
4. **World strength** en 0

### Solución:

```python
# 1. Añadir luces básicas
import bpy, math

# Key light
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
key = bpy.context.active.object
key.data.energy = 200
key.data.color = (1.0, 0.95, 0.9)
key.scale = (4, 4, 4)

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-5, -4, 5))
fill = bpy.context.active.object
fill.data.energy = 100

# 2. Configurar world
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Strength"].default_value = 1.0  # ← No 0!

# 3. Verificar cámara
cam = bpy.data.objects.get("Main_Camera")
if cam:
    bpy.context.scene.camera = cam
    print(f"Camera location: {cam.location}")
    print(f"Camera rotation: {cam.rotation_euler}")
```

**Checklist antes de render:**
- [ ] Al menos 1 luz en escena
- [ ] World strength > 0
- [ ] Cámara apuntando a objetos
- [ ] Objetos en frente de cámara (no detrás)
- [ ] Materiales aplicados correctamente

---

*Documento creado: 2026-04-01*  
*Basado en: Errores encontrados durante 4 ciclos de desarrollo de personaje*

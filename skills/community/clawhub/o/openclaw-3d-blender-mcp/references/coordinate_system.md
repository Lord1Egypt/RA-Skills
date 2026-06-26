# Sistema de Coordenadas en Blender

## Ejes

Blender usa un sistema de coordenadas 3D右手 (right-handed):

```
        Z (Up)
        ↑
        |
        |
        |______→ Y (Front)
       /
      /
     ↓
    X (Right)
```

### Dirección de los ejes:

| Eje | Positivo (+) | Negativo (-) |
|-----|--------------|--------------|
| **X** | Derecha | Izquierda |
| **Y** | Frente (hacia ti) | Atrás |
| **Z** | Arriba | Abajo |

### Rotación (radianes):

- **X axis:** Pitch (inclinar adelante/atrás)
- **Y axis:** Roll (rotar como rueda)
- **Z axis:** Yaw (girar izquierda/derecha)

**Conversiones útiles:**
```python
import math

math.radians(45)   # 0.785
math.radians(90)   # 1.57
math.radians(180)  # 3.14
math.radians(360)  # 6.28
```

---

## Posicionamiento de Personaje Humano

### Coordenadas para personaje adulto (de pie en origen):

| Parte del cuerpo | X | Y | Z | Notas |
|-----------------|---|---|---|-------|
| **Centro de masa** | 0 | 0 | 9-10 | Punto de balance |
| **Pies (centro)** | ±0.6 | 0.5 | 2-3 | En el suelo |
| **Tobillos** | ±0.6 | 0.3 | 3-4 | Sobre pies |
| **Rodillas** | ±0.6 | 0.1 | 6-7 | Mitad de pierna |
| **Caderas** | 0 | 0 | 8.5-9.5 | Centro del cuerpo |
| **Ombligo** | 0 | 0 | 10.5 | Referencia útil |
| **Pecho** | 0 | 0 | 11.5-12.5 | Centro de torso |
| **Hombros** | ±1.5 | 0 | 13-14 | Donde nacen brazos |
| **Codos** | ±3.5 | 0.3 | 10-11 | Brazo doblado |
| **Muñecas** | ±5.5 | 0.5 | 7-8 | Manos en T-pose |
| **Manos (palmas)** | ±5.5 | 0.8 | 7-8 | T-pose completo |
| **Cuello** | 0 | 0 | 13.5-14 | Base de cabeza |
| **Barbilla** | 0 | 1.2 | 14.5 | Parte inferior cara |
| **Ojos** | ±0.6 | 1.5 | 15.5-16 | Mirando al frente |
| **Nariz** | 0 | 1.8 | 15 | Centro de cara |
| **Boca** | 0 | 1.6 | 14 | Sonrisa |
| **Orejas** | ±1.4 | 0.3 | 15.5 | Lados de cabeza |
| **Parte superior cabeza** | 0 | 0 | 17-18 | Tope de cabeza |

### Proporciones realistas vs estilizadas:

| Medida | Realista | Pixar/Estilizado |
|--------|----------|------------------|
| Radio de cabeza | 1.0 | 1.4-1.6 |
| Radio de ojos | 0.2 | 0.4-0.45 |
| Altura total | 8 cabezas | 6-7 cabezas |
| Ancho de hombros | 2.5 cabezas | 2-2.2 cabezas |
| Largo de piernas | 4 cabezas | 3.5 cabezas |

**Nota:** Para personajes tipo Pixar, usa cabeza más grande y ojos más grandes para apariencia más "cute" y appeal.

---

## T-Pose vs Pose Natural

### T-Pose (brazos completamente extendidos):

```python
# Hombros
shoulder.rotation_z = 0

# Brazo superior (completamente hacia el lado)
upper_arm.rotation_z = 0
upper_arm.rotation_x = 0

# Antebrazo (recto)
forearm.rotation_z = 0

# Mano (palma hacia abajo)
hand.rotation_x = 0.15  # Ligeramente hacia abajo
hand.rotation_z = 0
```

### Pose Natural (brazos relajados):

```python
# Hombros (ligeramente hacia adelante)
shoulder.rotation_z = 0.15  # hacia adentro
shoulder.rotation_x = -0.1  # hacia adelante

# Brazo superior (caído naturalmente)
upper_arm.rotation_z = 0.25  # hacia abajo del cuerpo
upper_arm.rotation_x = -0.2  # hacia adelante del cuerpo

# Antebrazo (ligeramente doblado)
forearm.rotation_z = 0.3  # codo doblado
forearm.rotation_x = -0.1

# Mano (relajada, palmas hacia adentro)
hand.rotation_x = 0.3
hand.rotation_z = 0.2  # pulgar hacia adelante
```

---

## Parenting (Jerarquías)

### Por qué usar parenting:

Cuando un objeto es "hijo" de otro, se mueve con él automáticamente.

**Ejemplo:**
```python
# Sin parenting:
# Si mueves el ojo, la pupila se queda donde estaba ❌

# Con parenting:
pupil.parent = eye
# Si mueves el ojo, la pupila se mueve con él ✅
```

### Jerarquías comunes para personajes:

```
CHAR_Rig (armature)
└── Spine
    ├── Hips
    │   ├── Thigh.L
    │   │   └── Calf.L
    │   └── Thigh.R
    │       └── Calf.R
    ├── Shoulder.L
    │   ├── UpperArm.L
    │   │   └── Forearm.L
    │   │       └── Hand.L
    │   │           └── Fingers.L
    │   └── Shoulder.R
    │       └── ... (mismo para derecho)
    └── Neck
        └── Head
            ├── Eye.L
            │   └── Pupil.L
            ├── Eye.R
            │   └── Pupil.R
            ├── Brow.L
            ├── Brow.R
            ├── Nose
            └── Mouth
```

### Cómo establecer parenting:

```python
# Método 1: Parenting simple
child.parent = parent

# Método 2: Parenting con transform preservado
child.parent = parent
child.matrix_parent_inverse = parent.matrix_world.inverted()

# Ejemplo práctico:
pupil = bpy.data.objects.get("CHAR_Pupil_Left")
eye = bpy.data.objects.get("CHAR_Eye_Left")
if pupil and eye:
    pupil.parent = eye
    # Ahora pupil se mueve con eye
```

---

## Coordenadas Relativas vs Absolutas

### ❌ ERROR COMÚN: Coordenadas absolutas

```python
# Esto crea el objeto en una posición fija, sin importar el contexto
bpy.ops.mesh.primitive_cylinder_add(location=(5.4, 0.5, 13.8))

# Problema: Si la mano se mueve, el objeto no la sigue
```

### ✅ CORRECTO: Coordenadas relativas al padre

```python
# Obtener referencia al objeto padre
hand = bpy.data.objects.get("CHAR_Hand_Left")

if hand:
    # Calcular posición relativa a la mano
    lace_location = (
        hand.location.x - 0.15,  # 15cm hacia adentro desde la mano
        hand.location.y + 0.1,   # 10cm hacia adelante
        hand.location.z          # misma altura
    )
    
    bpy.ops.mesh.primitive_cylinder_add(location=lace_location)
    
    # Y luego hacer parenting
    lace.parent = hand
```

### Fórmula para coordenadas relativas:

```python
# Posición relativa en espacio local
relative_pos = (offset_x, offset_y, offset_z)

# Convertir a coordenadas globales (world space)
parent = bpy.data.objects.get("ParentName")
if parent:
    world_pos = parent.matrix_world @ Vector(relative_pos)
```

---

## Escala y Unidades

Blender usa **metros** como unidad base.

### Escalas de referencia:

| Objeto | Tamaño aproximado (unidades Blender) |
|--------|-------------------------------------|
| Humano adulto | 1.7 - 1.8 m de alto |
| Cabeza | 0.25-0.30 m (radio: 0.12-0.15) |
| Ojo | 0.02-0.025 m (radio) |
| Torso | 0.6-0.7 m de alto |
| Brazo completo | 0.7-0.8 m |
| Pierna completa | 0.9-1.0 m |
| Mano | 0.18-0.20 m de largo |
| Pie | 0.25-0.28 m de largo |

### Para personajes estilizados (Pixar):

```python
# Multiplicar cabezas por 1.3-1.5x
head_radius = 0.15 * 1.4  # = 0.21 (más grande)

# Ojos más grandes
eye_radius = 0.025 * 1.6  # = 0.04 (mucho más grande)

# Cuerpo más compacto
torso_height = 0.6 * 0.9  # = 0.54 (más corto)
```

---

## Consejos de Posicionamiento

1. **Siempre verifica después de crear:**
   ```python
   obj = bpy.context.active.object
   print(f"Ubicación: {obj.location}")
   ```

2. **Usa Empty objects como referencias:**
   ```python
   bpy.ops.object.empty_add(location=(0, 0, 10))
   ref = bpy.context.active.object
   ref.name = "REF_Center_Body"
   ```

3. **Para simetría, usa valores espejo:**
   ```python
   # Lado izquierdo: X negativo
   obj_left.location = (-1.5, 0, 10)
   
   # Lado derecho: X positivo (mismo valor absoluto)
   obj_right.location = (1.5, 0, 10)
   ```

4. **El suelo está en Z=0:**
   - Pies deben estar en Z ≈ 0-3
   - Si flota o está bajo tierra, ajusta Z

5. **Cámara típica para personaje:**
   ```python
   camera.location = (8, -10, 12)  # 3/4 vista frontal
   camera.rotation_euler = (math.radians(60), 0, math.radians(50))
   ```

---

*Referencia creada: 2026-04-01*  
*Basada en: Desarrollo de personaje estilizado tipo Pixar*

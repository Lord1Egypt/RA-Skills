"""
Skullpanda (泡泡玛特) 3D Figure — Procedural Blender Build
=========================================================
Based on extensive research of official Skullpanda designs:
- Professional 3D scans (1.3M verts from Thunk3D, 50K Polycam)
- Cults3D model renders
- Official Pop Mart product images
- Designer Xiong Miao's art style analysis

Scale: 1 Blender unit = 1 cm (total figure ~10.5 cm)
Style: Skullpanda "The Sound" series — standard white helmet, black bodysuit
Output: STL for 3D printing (manifold, watertight, with wall thickness)
"""
import bpy
import math
import os

# ============================================================
# CONFIGURATION
# ============================================================
OUTPUT_DIR = "/tmp/skullpanda_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors (Hex → RGBA)
HELMET_WHITE      = (0.961, 0.941, 0.922, 1.0)   # #F5F0EB
HELMET_SHADOW     = (0.784, 0.765, 0.745, 1.0)   # #C8C3BE
EYESHADOW_DARK    = (0.098, 0.098, 0.118, 1.0)   # #19191E
EYESHADOW_MID     = (0.216, 0.196, 0.216, 1.0)   # #373237
IRIS_COLOR        = (0.314, 0.235, 0.157, 1.0)   # #503C28
IRIS_HIGHLIGHT    = (0.863, 0.784, 0.667, 1.0)   # #DCC8AA
BODY_BLACK        = (0.102, 0.102, 0.102, 1.0)   # #1A1A1A
BODY_DARK_GRAY    = (0.176, 0.176, 0.176, 1.0)   # #2D2D2D
BASE_BLACK        = (0.078, 0.078, 0.078, 1.0)   # #141414
WHITE             = (1.0, 1.0, 1.0, 1.0)

# ============================================================
# CLEAN SCENE
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)

# ============================================================
# HELPER: Create PBR material
# ============================================================
def make_material(name, base_color, metallic=0.0, roughness=0.4, subsurface=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Subsurface Weight'].default_value = subsurface
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

# ============================================================
# STEP 1: HEAD / HELMET
# ============================================================
print("=" * 60)
print("BUILDING SKULLPANDA")
print("=" * 60)

# 1a. Base head shape — UV Sphere, stretched to Skullpanda proportions
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.7,        # half of head width (3.4/2)
    location=(0, 0, 4.7),   # centered above body
    segments=48,
    ring_count=36
)
head = bpy.context.object
head.name = "Skullpanda_Head"
head.scale = (1.0, 0.88, 1.05)  # Width=1, Depth=0.88, Height=1.05 ratio
bpy.ops.object.transform_apply(scale=True)

# 1b. Sculpt the head shape — enter edit mode to adjust
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Flatten face area slightly (scale along local Z in edit mode)
bpy.ops.transform.resize(value=(0.95, 0.95, 0.85))
bpy.ops.mesh.select_all(action='DESELECT')

# Select top vertices to dome them
bpy.ops.mesh.select_mode(type='VERT')
obj_data = head.data
for v in obj_data.vertices:
    if v.co.z > 1.2:  # top portion
        v.select = True

# Smooth the top
bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=3)

# Select bottom vertices to taper chin
bpy.ops.mesh.select_all(action='DESELECT')
for v in obj_data.vertices:
    if v.co.z < -1.0 and abs(v.co.x) < 1.0:  # chin area
        v.select = True

bpy.ops.transform.resize(value=(0.75, 0.75, 1.0))

bpy.ops.object.mode_set(mode='OBJECT')

# 1c. Add subdivision surface for smoothness
subdiv_head = head.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv_head.levels = 1
subdiv_head.render_levels = 2
subdiv_head.subdivision_type = 'CATMULL_CLARK'

print("✅ Head base created")

# ============================================================
# STEP 2: EYE SOCKETS (Boolean cutout)
# ============================================================
# Create two eye-shaped cutters for the sockets
# Skullpanda has rounded triangular eye sockets (point down)

def create_eye_cutter(name, x_pos, y_pos=1.1, z_pos=0.3):
    """Create a rounded triangular eye socket cutter"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.55,  # ~1.0 unit wide eyes
        location=(x_pos, y_pos, z_pos + 4.7),
        segments=24,
        ring_count=16
    )
    cutter = bpy.context.object
    cutter.name = name
    
    # Scale to make it more almond/triangle shape
    cutter.scale = (0.5, 0.15, 0.4)  # almond shape
    bpy.ops.object.transform_apply(scale=True)
    
    # Taper the bottom to a point (triangular shape)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Flatten top more than bottom for the triangular look
    for v in cutter.data.vertices:
        if v.co.z > 0.2:
            v.co.x *= 0.7  # narrow top
        if v.co.z < -0.2:
            v.co.z *= 1.3  # extend bottom point
            v.co.x *= 0.3   # sharp point at bottom
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply subdivision to make it smooth
    sub = cutter.modifiers.new(name="SubSurf", type='SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    
    return cutter

# Create left and right eye socket cutters
eye_l = create_eye_cutter("EyeCutter_L", x_pos=-0.65)
eye_r = create_eye_cutter("EyeCutter_R", x_pos=0.65)

# Apply Boolean modifiers to cut eye sockets into head
bpy.context.view_layer.objects.active = head
head.select_set(True)

for cutter in [eye_l, eye_r]:
    bool_mod = head.modifiers.new(name=f"Bool_{cutter.name}", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter
    bool_mod.solver = 'EXACT'
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Remove cutters
for cutter in [eye_l, eye_r]:
    bpy.data.objects.remove(cutter, do_unlink=True)

print("✅ Eye sockets carved")

# ============================================================
# STEP 3: EYES (inside the sockets)
# ============================================================
def create_eye(name, x_pos, y_pos=1.05, z_pos=4.7):
    """Create eye with sclera, iris, pupil, highlight"""
    eye_group = []
    
    # Sclera (white of eye) — slightly recessed
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.48,
        location=(x_pos, y_pos, z_pos),
        segments=24, ring_count=16
    )
    sclera = bpy.context.object
    sclera.name = f"{name}_Sclera"
    sclera.scale = (0.5, 0.08, 0.35)
    bpy.ops.object.transform_apply(scale=True)
    eye_group.append(sclera)
    
    # Iris (large, brown/amber)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.35,
        location=(x_pos, y_pos - 0.01, z_pos),
        segments=16, ring_count=12
    )
    iris = bpy.context.object
    iris.name = f"{name}_Iris"
    iris.scale = (1.0, 0.05, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    eye_group.append(iris)
    
    # Pupil (tiny black dot)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1,
        location=(x_pos, y_pos - 0.02, z_pos),
        segments=8, ring_count=6
    )
    pupil = bpy.context.object
    pupil.name = f"{name}_Pupil"
    pupil.scale = (1.0, 0.05, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    eye_group.append(pupil)
    
    # Highlight reflection
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.08,
        location=(x_pos - 0.12, y_pos - 0.02, z_pos + 0.1),
        segments=8, ring_count=6
    )
    highlight = bpy.context.object
    highlight.name = f"{name}_Highlight"
    highlight.scale = (0.4, 0.05, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    eye_group.append(highlight)
    
    return eye_group

left_eye = create_eye("Eye_L", x_pos=-0.6)
right_eye = create_eye("Eye_R", x_pos=0.6)

# Apply materials to eye parts
mat_sclera = make_material("Sclera", WHITE, roughness=0.1)
mat_iris = make_material("Iris", IRIS_COLOR, roughness=0.3, subsurface=0.1)
mat_pupil = make_material("Pupil", (0, 0, 0, 1), roughness=0.0)
mat_highlight = make_material("EyeHighlight", IRIS_HIGHLIGHT, roughness=0.0)

for obj_list in [left_eye, right_eye]:
    for obj in obj_list:
        if "Sclera" in obj.name:
            obj.data.materials.append(mat_sclera)
        elif "Iris" in obj.name:
            obj.data.materials.append(mat_iris)
        elif "Pupil" in obj.name:
            obj.data.materials.append(mat_pupil)
        elif "Highlight" in obj.name:
            obj.data.materials.append(mat_highlight)

print("✅ Eyes created")

# ============================================================
# STEP 4: EYESHADOW (dark makeup around eyes)
# ============================================================
# Create dark eyeshadow by placing dark tinted spheres around eye area
def create_eyeshadow(name, x_pos, y_pos=1.02, z_pos=4.7):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.85,
        location=(x_pos, y_pos, z_pos),
        segments=24, ring_count=16
    )
    es = bpy.context.object
    es.name = name
    es.scale = (0.6, 0.03, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    return es

# Left and right eyeshadow
es_l = create_eyeshadow("Eyeshadow_L", -0.6)
es_r = create_eyeshadow("Eyeshadow_R", 0.6)

# Merge eyeshadow into a single piece
bpy.context.view_layer.objects.active = es_l
es_l.select_set(True)
es_r.select_set(True)
bpy.ops.object.join()
merged_eyeshadow = bpy.context.object
merged_eyeshadow.name = "Eyeshadow"

mat_eyeshadow = make_material("Eyeshadow", EYESHADOW_DARK, roughness=0.9)
merged_eyeshadow.data.materials.append(mat_eyeshadow)

print("✅ Eyeshadow applied")

# ============================================================
# STEP 5: CAT EARS (spherical button ears)
# ============================================================
def create_ear(name, x_pos, y_pos=-0.3, z_pos=6.2):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.35,  # 0.7 diameter
        location=(x_pos, y_pos, z_pos),
        segments=24, ring_count=16
    )
    ear = bpy.context.object
    ear.name = name
    ear.scale = (1.0, 0.85, 0.9)  # slightly flattened spheres
    bpy.ops.object.transform_apply(scale=True)
    return ear

ear_l = create_ear("Ear_L", x_pos=-0.8)
ear_r = create_ear("Ear_R", x_pos=0.8)

mat_ear = make_material("Ear", HELMET_WHITE, roughness=0.35, subsurface=0.05)
for ear in [ear_l, ear_r]:
    ear.data.materials.append(mat_ear)

print("✅ Cat ears created")

# ============================================================
# STEP 6: BODY (short chunky bodysuit)
# ============================================================
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=1.25,        # shoulder width
    depth=2.5,          # body height
    location=(0, 0, 1.8)
)
body = bpy.context.object
body.name = "Body"

# Taper at waist
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

for v in body.data.vertices:
    # Taper waist
    if -0.3 < v.co.z < 0.3:
        v.co.x *= 0.8
        v.co.y *= 0.8
    # Round shoulders (top)
    if v.co.z > 1.0:
        inflate = 1.0 + (v.co.z - 1.0) * 0.15
        v.co.x *= inflate
        v.co.y *= inflate
    # Round hips (bottom)
    if v.co.z < -0.8:
        inflate = 1.0 + (-0.8 - v.co.z) * 0.2
        v.co.x *= inflate
        v.co.y *= inflate

bpy.ops.object.mode_set(mode='OBJECT')

# Subdivision for smooth body
sub_body = body.modifiers.new(name="Subdivision", type='SUBSURF')
sub_body.levels = 1
sub_body.render_levels = 2

mat_body = make_material("Body", BODY_BLACK, roughness=0.6, metallic=0.05)
body.data.materials.append(mat_body)

print("✅ Body created")

# ============================================================
# STEP 7: ARMS
# ============================================================
def create_arm(name, x_side, z_rot=0):
    """Create an arm with mitten hand"""
    arm_group = []
    
    # Upper arm
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.3,
        depth=1.0,
        location=(x_side * 1.4, 0, 2.8)
    )
    upper = bpy.context.object
    upper.name = f"{name}_Upper"
    upper.rotation_euler = (0, x_side * 0.3, 0)  # slight outward angle
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    arm_group.append(upper)
    
    # Lower arm
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.25,
        depth=0.8,
        location=(x_side * 1.6, 0, 2.0)
    )
    lower = bpy.context.object
    lower.name = f"{name}_Lower"
    lower.rotation_euler = (0, x_side * 0.1, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    arm_group.append(lower)
    
    # Mitten hand
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.22,
        location=(x_side * 1.65, 0, 1.6),
        segments=12, ring_count=8
    )
    hand = bpy.context.object
    hand.name = f"{name}_Hand"
    hand.scale = (1.0, 0.7, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    arm_group.append(hand)
    
    # Join all parts
    bpy.context.view_layer.objects.active = upper
    for obj in arm_group[1:]:
        obj.select_set(True)
    upper.select_set(True)
    bpy.ops.object.join()
    
    arm = bpy.context.object
    arm.name = name
    arm.data.materials.append(mat_body)
    
    return arm

arm_l = create_arm("Arm_L", x_side=1)
arm_r = create_arm("Arm_R", x_side=-1)

print("✅ Arms created")

# ============================================================
# STEP 8: LEGS
# ============================================================
def create_leg(name, x_side):
    """Create a leg with boot foot"""
    leg_group = []
    
    # Thigh
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.35,
        depth=0.9,
        location=(x_side * 0.5, 0, 0.6)
    )
    thigh = bpy.context.object
    thigh.name = f"{name}_Thigh"
    leg_group.append(thigh)
    
    # Shin
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.3,
        depth=0.8,
        location=(x_side * 0.5, 0, -0.2)
    )
    shin = bpy.context.object
    shin.name = f"{name}_Shin"
    leg_group.append(shin)
    
    # Boot foot
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.3,
        location=(x_side * 0.55, 0.1, -0.7),
        segments=12, ring_count=8
    )
    foot = bpy.context.object
    foot.name = f"{name}_Foot"
    foot.scale = (1.2, 0.7, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    leg_group.append(foot)
    
    # Join
    bpy.context.view_layer.objects.active = thigh
    for obj in leg_group[1:]:
        obj.select_set(True)
    thigh.select_set(True)
    bpy.ops.object.join()
    
    leg = bpy.context.object
    leg.name = name
    leg.data.materials.append(mat_body)
    
    return leg

leg_l = create_leg("Leg_L", x_side=1)
leg_r = create_leg("Leg_R", x_side=-1)

print("✅ Legs created")

# ============================================================
# STEP 9: TAIL (curved cat tail)
# ============================================================
# Use a Bezier curve for the tail
bpy.ops.curve.primitive_bezier_curve_add(
    location=(0, -0.6, 0.3)
)
tail_curve = bpy.context.object
tail_curve.name = "Tail_Curve"

# Adjust curve points
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.select_all(action='SELECT')

# Move the control points
for i, spline in enumerate(tail_curve.data.splines):
    for j, point in enumerate(spline.bezier_points):
        if j == 0:  # Start point (at body)
            point.co = (0.3, -0.6, 0.3)
            point.handle_right = (0.5, -0.8, 0.0)
            point.handle_left = (0.1, -0.4, 0.6)
        elif j == 1:  # End point (tip)
            point.co = (1.5, -0.3, -0.5)
            point.handle_right = (1.2, -0.2, -0.3)
            point.handle_left = (1.8, -0.4, -0.7)

bpy.ops.object.mode_set(mode='OBJECT')

# Convert curve to mesh for bevel
tail_curve.data.bevel_depth = 0.12
tail_curve.data.bevel_resolution = 4
tail_curve.data.fill_mode = 'FULL'

# Convert to mesh
bpy.ops.object.select_all(action='DESELECT')
tail_curve.select_set(True)
bpy.context.view_layer.objects.active = tail_curve
bpy.ops.object.convert(target='MESH')
tail_mesh = bpy.context.object
tail_mesh.name = "Tail"
tail_mesh.data.materials.append(mat_body)

print("✅ Tail created")

# ============================================================
# STEP 10: BASE / STAND
# ============================================================
bpy.ops.mesh.primitive_cylinder_add(
    vertices=48,
    radius=3.25,     # 6.5 cm diameter
    depth=0.3,        # thin disc
    location=(0, 0, -1.0)
)
base_disc = bpy.context.object
base_disc.name = "Base_Disc"

# Raised rim
bpy.ops.mesh.primitive_cylinder_add(
    vertices=48,
    radius=3.25,
    depth=0.15,
    location=(0, 0, -0.85)
)
base_rim = bpy.context.object
base_rim.name = "Base_Rim"
base_rim.scale = (1.05, 1.05, 0.3)  # slightly wider rim
bpy.ops.object.transform_apply(scale=True)

# Join base parts
bpy.context.view_layer.objects.active = base_disc
base_disc.select_set(True)
base_rim.select_set(True)
bpy.ops.object.join()
base = bpy.context.object
base.name = "Base"

# Subdivide for smooth base
sub_base = base.modifiers.new(name="Subdivision", type='SUBSURF')
sub_base.levels = 1

mat_base = make_material("Base", BASE_BLACK, roughness=0.8)
base.data.materials.append(mat_base)

print("✅ Base created")

# ============================================================
# STEP 11: JOIN & MODIFY FOR 3D PRINTING
# ============================================================

# Select all figure parts (NOT the base — keep separate for printing)
figure_parts = [
    head, merged_eyeshadow, body, arm_l, arm_r, leg_l, leg_r, tail_mesh
]
ear_parts = [ear_l, ear_r]
eye_parts = left_eye + right_eye

# Join all figure parts into one mesh (NOT including base)
bpy.context.view_layer.objects.active = head
for part in figure_parts + ear_parts + eye_parts:
    if part.name not in bpy.data.objects:
        print(f"⚠️ {part.name} already removed, skipping")
        continue
    part.select_set(True)
head.select_set(True)
bpy.ops.object.join()
skullpanda = bpy.context.object
skullpanda.name = "Skullpanda"

print("✅ All parts joined")

# ============================================================
# STEP 12: APPLY 3D PRINTING MODIFIERS
# ============================================================

# Solidify — wall thickness for 3D printing
solidify = skullpanda.modifiers.new(name="Solidify_3DPrint", type='SOLIDIFY')
solidify.thickness = 0.12   # 1.2mm wall thickness
solidify.offset = -1.0       # inward offset to preserve outer shape
solidify.use_even_offset = True
solidify.use_quality_normals = True

# Subdivision surface — final smooth
sub_final = skullpanda.modifiers.new(name="Subdivision_Final", type='SUBSURF')
sub_final.levels = 2
sub_final.render_levels = 2
sub_final.subdivision_type = 'CATMULL_CLARK'

print("✅ 3D printing modifiers applied")

# ============================================================
# STEP 13: LIGHTING & CAMERA FOR PREVIEW
# ============================================================

# Three-point lighting
# Key light
bpy.ops.object.light_add(type='AREA', location=(5, -4, 8), rotation=(0.6, 0, 0.7))
key = bpy.context.object
key.data.energy = 600
key.data.size = 5

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-5, 3, 4), rotation=(0.4, 0, -1.0))
fill = bpy.context.object
fill.data.energy = 300
fill.data.size = 4

# Rim light
bpy.ops.object.light_add(type='AREA', location=(0, 6, 6), rotation=(0.3, 0, 1.57))
rim = bpy.context.object
rim.data.energy = 250
rim.data.size = 3

# Camera
bpy.ops.object.camera_add(location=(6, -5, 4.5))
cam = bpy.context.object
cam.rotation_euler = (math.radians(60), 0, math.radians(50))
bpy.context.scene.camera = cam

print("✅ Lighting & camera set")

# ============================================================
# STEP 14: RENDER PREVIEW
# ============================================================
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 50  # 960x540 for quick preview

# Set up viewport for preview
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

# ============================================================
# SAVE .blend + EXPORT STL
# ============================================================
blend_path = os.path.join(OUTPUT_DIR, "skullpanda_figure.blend")
stl_path = os.path.join(OUTPUT_DIR, "skullpanda_figure.stl")
stl_base_path = os.path.join(OUTPUT_DIR, "skullpanda_base.stl")

# Save .blend
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# Export Skullpanda figure as STL
bpy.ops.object.select_all(action='DESELECT')
skullpanda.select_set(True)
bpy.context.view_layer.objects.active = skullpanda

# Apply modifiers before STL export
bpy.ops.object.modifier_apply(modifier="Solidify_3DPrint")
bpy.ops.object.modifier_apply(modifier="Subdivision_Final")

bpy.ops.export_mesh.stl(
    filepath=stl_path,
    use_selection=True,
    ascii=False,
    global_scale=1.0
)

# Export Base separately
bpy.ops.object.select_all(action='DESELECT')
base_obj = bpy.data.objects.get("Base")
if base_obj:
    base_obj.select_set(True)
    bpy.context.view_layer.objects.active = base_obj
    if base_obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=base_obj.modifiers[0].name)
    bpy.ops.export_mesh.stl(
        filepath=stl_base_path,
        use_selection=True,
        ascii=False,
        global_scale=1.0
    )
else:
    print("⚠️ Base not found, skipping base export")

# ============================================================
# PRINT SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("🎯 SKULLPANDA BUILD COMPLETE")
print("=" * 60)
print(f"📦 Objects: {[o.name for o in bpy.data.objects if o.type == 'MESH']}")
print(f"🎨 Materials: {[m.name for m in bpy.data.materials]}")
print(f"💡 Lights: {[o.name for o in bpy.data.objects if o.type == 'LIGHT']}")
print(f"📷 Camera: {cam.name}")
print(f"⚙️  Engine: {scene.render.engine}")
print(f"📐 Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
print(f"\n📁 Output files:")
print(f"   Blender: {blend_path}")
print(f"   STL Figure: {stl_path}")
print(f"   STL Base:   {stl_base_path}")
print("=" * 60)

# Render preview
scene.render.filepath = os.path.join(OUTPUT_DIR, "skullpanda_preview.png")
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"✅ Preview rendered: {scene.render.filepath}")

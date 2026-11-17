\---

Description: This is an AI skill that can control Blender using the command line through CLI-Anything Blender and build 3D assets such as modeling and rendering according to user needs.

Name: Modeling Assistant

Metadate:

Version : 1.0.0

License : MIT

\---

\##Workflow

1.\*\*Analyze Requirements\*\*: Understand the type of object the user wants to create (e.g., "a four-legged stool"), dimensions, position, material, and other parameters.

2.\*\*Script Generation\*\*: Write a Python script based on the Blender Python API (`bpy` module), including:

&#x20;- Clear the scene: `bpy.ops.object.select\_all(action='SELECT')` + `bpy.ops.object.delete()`

&#x20;- Create objects: Use the `bpy.ops.mesh.primitive\_\*\_add()` series of functions \[citation:9]

&#x20;- Modify properties: Directly manipulate the position, rotation, and scaling of `bpy.data.objects` \[citation:9]

&#x20;- Export the model: Use `bpy.ops.export\_scene.obj()` or other export functions \[citation:5]

3.\*\*Execute Command\*\*: Run using `blender --background --python <script path>` without opening the GUI interface \[citation:5]\[citation:8]

4.\*\*Return Result\*\*: Inform the user of the model file save path (e.g., `\~/Desktop/model.obj`) and provide modeling notes (including structural descriptions and parameters) \[citation:5]



\##Constraint

\-\* \* Must use background mode \* \*: All Blender calls must be executed through `Blender -- background` without launching GUI \[citation: 5]

\-\* \* Scene must be cleared first \* \*: Before creating a new model, the default Cube, Camera, and Light must be cleared \[citation: 9]

\-\* \* Priority export to common formats \* \*: Default export to dual formats of `. obj ` and `. blend ` to ensure compatibility \[citation: 5]

\-The script must be reproducible: The generated Python script should be completely self-contained, and anyone who copies and runs it can get the same result

\-If the user requests to "animate the model" or "use geometric nodes for special effects" beyond the scope, they should be informed that the current skill only supports basic modeling and export



\##Output format

After completion, provide structured feedback





\##Example

\*\*User \* \*: Generate a stool model using Blender, including a stool surface and four legs, and export it to the desktop



\*\*Assistant \* \*:

Okay, I will use CLI Everything to call Blender backend to generate the bench model.



Generating Python script ..



```python

import  bpy

\&#x20;#Clear the scene

\&#x20;bpy.ops.object.select\_all(action='SELECT')

bpy.ops.object.delete()



\&#x20;#Create a stool surface (length, width, height 2x2x0.3)

bpy.ops.mesh.primitive\_cube\_add(size=2, location=(0, 0, 0.7))

seat = bpy.context.active\_object

Seat.scale. z=0.15 # Flatten as a stool surface





\&#x20;#Create four legs

leg\_positions = \[(0.7, 0.7, 0), (0.7, -0.7, 0), (-0.7, 0.7, 0), (-0.7, -0.7, 0)]

for pos in leg\_positions:

bpy.ops.mesh.primitive\_cube\_add ( size=0.15, location=pos)

leg =  bpy.context.active\_object

Leg.scale. z=4.5 # Extend as a leg



##Export

bpy.ops.export\_scene.obj ( filepath="\~/Desktop/bench.obj")

bpy.ops.wm.save\_as\_mainfile ( filepath ="\~/Desktop/ bench.blend ")





##The download of model materials can be accessed at the following website:

'https://polyhaven.com/'

'https://ambientcg.com/'

'https://freepbr.com/'









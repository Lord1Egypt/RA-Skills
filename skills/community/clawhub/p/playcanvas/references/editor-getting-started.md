# Your First App

Developing applications in the PlayCanvas Editor is easy and fun. Let's recreate a simple 3D app — a red ball movable with arrow keys.
## Step 1: Create a Project
1. Go to your PROJECTS page
2. Click **NEW** → enter "My First App" → **CREATE**
3. Click **EDITOR** to open your project
## Step 2: Customize the Scene
The default scene has a camera, a box on a plane, and a light.
**Change box to sphere:** Select the Box entity in HIERARCHY → in Inspector, change Model component Type from Box to Sphere. Rename entity to "Sphere".
## Step 3: Add a Material
1. Click **+** in the ASSETS panel → create Material
2. Select the material → expand DIFFUSE in Inspector → click color swatch → choose red
3. Drag the material from Assets panel onto the sphere in the Viewport
## Step 4: Position the Camera
Select Camera entity → set Position and Rotation to frame the sphere from the front.
## Step 5: Add a Script for Movement
1. Right-click Sphere → **Add Component** → **Script**
2. Type `movement.js` as the script name, press Enter
3. Click **EDIT** to open the Code Editor
```javascript
var Movement = pc.createScript('movement');
Movement.prototype.update = function(dt) {
    const keyboard = this.app.keyboard;
    const left = keyboard.isPressed(pc.KEY_LEFT);
    const right = keyboard.isPressed(pc.KEY_RIGHT);
    const up = keyboard.isPressed(pc.KEY_UP);
    const down = keyboard.isPressed(pc.KEY_DOWN);
    if (left) this.entity.translate(-dt, 0, 0);
    if (right) this.entity.translate(dt, 0, 0);
    if (up) this.entity.translate(0, 0, -dt);
    if (down) this.entity.translate(0, 0, dt);
};
```
4. Save with **Ctrl+S** (Cmd+S on Mac), close the editor tab
## Step 6: Test with Launch
Click the **Launch** button (top right of 3D view). Use arrow keys to move the sphere.
## Step 7: Publish
1. Click the Publish button in the left toolbar
2. Choose **PUBLISH TO PLAYCANVAS**
3. Configure settings, scroll down, click **PUBLISH NOW**
4. Share the generated URL!
That's the complete process from start to finish — building and publishing a PlayCanvas application.
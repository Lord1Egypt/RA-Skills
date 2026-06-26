# Physics

Most video games have some form of physics. Players expect objects to fall under gravity, collide instead of passing through each other, and trigger sounds on collision.
A physics engine attempts to reproduce our understanding of the natural world in an artificial game world, realistically animating objects in an expected and predictable way.
PlayCanvas provides a powerful physics engine that can be used to achieve a great many effects. This section introduces the concepts of rigid bodies, collision, forces, impulses, raycasting and more.
## Physics Engine
PlayCanvas integrates with physics engines (primarily Ammo.js, a Bullet physics port). Key capabilities:
- **Rigid Body Dynamics**: Simulate object motion, gravity, forces
- **Collision Detection**: Detect and respond to object intersections
- **Constraints/Joints**: Connect objects with hinges, springs, etc.
- **Raycasting**: Cast rays into the scene to detect hits
- **Trigger Volumes**: Detect when objects enter/exit areas
## Physics Components
### Rigid Body Component
Attached to entities to give them physical properties:
- **Type**: Static, Dynamic, or Kinematic
- **Mass**: Object mass (dynamic only)
- **Linear/Angular Damping**: Motion resistance
- **Friction/Restitution**: Surface properties
- **Linear/Angular Factors**: Lock axes of motion
### Collision Component
Defines the collision shape:
- **Type**: Box, Sphere, Capsule, Cylinder, Cone, Mesh (convex/compound)
- **Half Extents**: Box dimensions
- **Radius/Height**: Sphere/capsule dimensions
- **Offset**: Shape position relative to entity
## Physics Settings
Global physics configuration via scene settings:
- Gravity vector
- Simulation step size
- Solver iterations
- Collision margin
## Use Cases
Common physics applications:
- Character controllers with gravity and collision
- Vehicle simulation
- Ragdoll physics
- Projectile simulation
- Destructible environments
- Object stacking and balancing
## Rigid Body
The Rigid Body Component enables an entity to participate in the scene's physics simulation, allowing realistic movement. The component dynamically displays different attributes based on the 'Type' attribute.
## Body Types
| Type | Description |
|------|-------------|
| **Static** | Immovable, unaffected by forces. Used for walls, floors, terrain. |
| **Dynamic** | Fully simulated. Responds to forces, gravity, collisions. Has mass. |
| **Kinematic** | Movable by script, but unaffected by forces. Pushes dynamic bodies. |
## Properties
| Property | Description |
|----------|-------------|
| Type | Static, Dynamic, or Kinematic |
| Mass | (Dynamic only) Mass in kg when world units are meters |
| Linear Damping | (Dynamic only) Proportion of linear velocity lost per second (0-1) |
| Angular Damping | (Dynamic only) Proportion of angular velocity lost per second (0-1) |
| Linear Factor | (Dynamic only) Multiplier per axis (X,Y,Z). Set to 0 to constrain movement — useful for 2D games |
| Angular Factor | (Dynamic only) Multiplier per axis. Set to 0 to prevent rotation around an axis |
| Friction | How quickly body loses velocity on contact (0-1) |
| Restitution | Bounciness (0-1). ⚠️ Setting to 1 means the body never stops moving |
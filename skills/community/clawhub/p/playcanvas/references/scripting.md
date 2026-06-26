# Scripting

## Scripting
Scripts are the heart of interactivity in PlayCanvas. They're reusable pieces of code that you attach to Entities to define behaviors, handle user input, manage game logic, and bring your projects to life.
## Two Scripting Systems
PlayCanvas supports two scripting approaches:
- **ESM Scripts** (`.mjs` files) — Modern ES Module-based scripts using class syntax. **Recommended for new projects.**
- **Classic Scripts** (`.js` files) — The original PlayCanvas scripting system using prototype-based syntax.
Both systems can coexist in the same project, allowing you to migrate gradually or use whichever approach fits your needs.
## Quick Example
**ESM (Recommended):**
```javascript
import { Script } from 'playcanvas';
export class Rotate extends Script {
    static scriptName = 'rotate';
            /** @attribute */
speed = 10;
    update(dt) {
        this.entity.rotate(0, this.speed * dt, 0);
    }
}
```
```javascript
var Rotate = pc.createScript('rotate');
Rotate.attributes.add('speed', { type: 'number', default: 10 });
Rotate.prototype.update = function(dt) {
    this.entity.rotate(0, this.speed * dt, 0);
};
```
## Topics
- **Getting Started** — Basic script structure and syntax.
- **ESM Scripts** — Modern scripting with ES Modules.
- **Script Lifecycle** — When and how script methods are called.
- **Application Lifecycle** — Understanding app initialization and frame updates.
- **Script Attributes** — Exposing configurable properties.
- **Engine API** — Key classes and patterns.
- **Events** — Communication between scripts.
- **Debugging** — Tools and techniques for troubleshooting.
- **Migration Guide** — Upgrading from classic to ESM scripts.
## Getting Started
## What is a Script?
A script is a piece of JavaScript code that defines behavior for an Entity in your scene. Scripts are:
- **Reusable** — The same script can be attached to multiple entities
- **Configurable** — Use attributes to customize behavior per entity
- **Event-driven** — Respond to lifecycle events and user interactions
## Basic Script Structure
**ESM (Recommended):**
```javascript
import { Script } from 'playcanvas';
export class MyScript extends Script {
    static scriptName = 'myScript';
            /** @attribute */
speed = 10;
    initialize() {
        console.log('Script initialized!');
    }
    update(dt) {
        this.entity.rotate(0, this.speed * dt, 0);
    }
}
```
Key points for ESM scripts:
- Import the `Script` class from PlayCanvas
- Export a class that extends `Script`
- Use `        /** @attribute */
` to expose properties to the editor
- File must have `.mjs` extension
## Core Concepts
### Script Lifecycle
Scripts have methods called automatically:
- `initialize()` — Called once when the script starts
- `update(dt)` — Called every frame with delta time
- `postUpdate(dt)` — Called after all updates complete
- Event handlers for `enable`, `disable`, `destroy`
### Attributes
Attributes expose script properties to the editor:
```javascript
import { Color, Entity, Script } from 'playcanvas';
export class Configurable extends Script {
    static scriptName = 'configurable';
            /** @attribute */
speed = 5;
            /** @attribute */
color = new Color(1, 0, 0);
            /** @attribute */
target;
}
```
### Accessing the Entity
Every script has access to its entity via `this.entity`:
```javascript
const position = this.entity.getPosition();
const child = this.entity.findByName('ChildName');
const camera = this.entity.camera;       // camera component
const rigidbody = this.entity.rigidbody; // rigidbody component
```
## Lifecycle
Every script instance you attach to an Entity in PlayCanvas goes through a well-defined lifecycle. Understanding this lifecycle is crucial because it dictates when your code runs and how it can interact with the rest of your application.
## Lifecycle Methods
### `initialize()`
Called once per script instance, after the entity hierarchy is constructed but before the first frame renders.
```javascript
import { Script } from 'playcanvas';
export class MyScript extends Script {
    static scriptName = 'myScript';
    initialize() {
        this.on('enable', () => console.log('script enabled'));
        this.on('disable', () => console.log('script disabled'));
        this.once('destroy', () => console.log('script destroyed'));
    }
}
```
**Use for:** Subscribing to events, registering DOM handlers, creating objects, caching entity references.
### `postInitialize()`
Called once after ALL scripts' `initialize()` has completed. Use for setup that depends on other scripts being ready.
```javascript
postInitialize() {
    const material = this.otherEntity.material; // safe to access now
}
```
### `update(dt)`
Called every frame. `dt` is delta time in seconds since last frame. The heart of runtime behavior.
```javascript
update(dt) {
    this.entity.rotate(0, 10 * dt, 0); // frame-rate independent rotation
}
```
### `postUpdate(dt)`
Called every frame after all `update()` calls complete. Common for camera-following-player patterns:
```javascript
postUpdate(dt) {
    const playerPos = this.player.getPosition();
    this.entity.lookAt(playerPos);
}
```
## Lifecycle Events
### `enable` Event
Fires when a script becomes enabled (on init if enabled, or when `this.enabled` set to true).
### `disable` Event
Fires when a script becomes disabled. Use for pausing behaviors and releasing temporary resources.
### `state` Event
Fires whenever enabled/disabled state changes. Receives `(enabled)` boolean parameter.
### `destroy` Event
Fires when the script is about to be destroyed (entity destroyed, component removed). **Critical for cleanup:**
```javascript
initialize() {
    this.once('destroy', () => {
        this.app.off('some:event', this._handler, this);
        // release resources, nullify references
    });
}
```
## Esm Scripts
# ESM Scripts
ESM Scripts use modern ES Module syntax and provide the recommended way to write PlayCanvas scripts. They offer better code organization, static imports, improved bundling, and a more familiar development experience for modern JavaScript developers.
## Basic Structure
```javascript
import { Script } from 'playcanvas';
export class PlayerController extends Script {
    static scriptName = 'playerController';
    initialize() {
            }
    update(dt) {
            }
}
```
## Shared Configuration
```javascript
// config.mjs - Shared configuration
export const GAME_SETTINGS = {
    playerSpeed: 5,
    jumpHeight: 10,
    gravity: -9.8
};
export function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}
```
## Using Shared Code
```javascript
// PlayerController.mjs
import { Script } from 'playcanvas';
import { GAME_SETTINGS, clamp } from './config.mjs';
export class PlayerController extends Script {
    static scriptName = 'playerController';
    update(dt) {
        const speed = GAME_SETTINGS.playerSpeed;
        // Use clamp function...
    }
}
```
## Key Concepts
### Script Name
Every script must define a `static scriptName`. This is the identifier used when attaching scripts to entities.
### Lifecycle Methods
- `initialize()` — Called once when the script is first loaded
- `update(dt)` — Called every frame with delta time in seconds
- `postInitialize()` — Called after all scripts in the scene are initialized
- `postUpdate(dt)` — Called after all update calls complete
- `swap()` — Called when hot-reloading updates the script
### ES Module Benefits
- Static imports for better tree-shaking and bundling
- Familiar `import`/`export` syntax
- Better IDE support with autocompletion
- Clearer dependency management
- Compatible with modern bundlers (Rollup, Webpack, esbuild)
## Editor Integration
ESM scripts (.mjs extension) are the default format for new PlayCanvas projects. The Editor recognizes them automatically and provides:
- Attribute parsing from JSDoc comments
- Hot-reloading support
- Code editor integration with syntax highlighting
## Script Attributes with ESM
```javascript
import { Script } from 'playcanvas';
export class MyScript extends Script {
    static scriptName = 'myScript';
            /** @attribute */
speed = 5;
            /** @attribute */
targetName = 'default';
}
```
## Attributes
# Script Attributes
Script Attributes are a powerful feature in PlayCanvas that define the public, configurable interface of your scripts. They allow you to expose specific parameters that can be easily tweaked, either programmatically when instantiating or configuring scripts in code, or visually within the PlayCanvas Editor.
## How They Work
When you declare an attribute, you define a property that can be initialized and modified:
- **In Code**: Set values when adding a script to a Script Component or at runtime via script instance properties.
- **In the Editor**: The Editor parses your script file and creates corresponding UI controls (number fields, checkboxes, color pickers, asset pickers, etc.) in the Inspector.
For example, a `speed` attribute in a rotation script would appear as a number field in the Editor or be settable via `this.speed = 5` in code.
## Two Systems: ESM and Classic
### ESM Script Attributes (Recommended)
Used with modern ES Module (.mjs) scripts. Attributes declared using JSDoc comments above class member variables.
### Classic Script Attributes
Used with older "Classic" script (.js) files. Attributes declared using `MyScript.attributes.add(...)` API.
## Attribute Types
Common attribute types include:
- **number**: Numeric value with optional min/max
- **string**: Text input
- **boolean**: Checkbox
- **vec2, vec3, vec4**: Vector inputs
- **rgb, rgba**: Color pickers
- **entity**: Reference to another entity
- **asset**: Reference to an asset (texture, model, etc.)
- **curve**: Animation curve editor
- **enum**: Dropdown selection
## ESM Example
```javascript
import { Script } from 'playcanvas';
export class MyScript extends Script {
    static scriptName = 'myScript';
            /** @attribute */
speed = 5;
            /** @attribute */
color = [1, 0, 0];
            /** @attribute */
enabled = true;
}
```
Understanding Script Attributes is key to building flexible, maintainable projects in PlayCanvas.
## Engine Api
# Calling the Engine API
When writing PlayCanvas scripts, you're working with the PlayCanvas Engine API. This page covers the essential classes and patterns you'll use most often in your scripts.
## Your Script Context
Every script has access to these core objects:
```javascript
this.app    // The main application (AppBase)
this.entity // The entity this script is attached to
```
## Essential Classes
### AppBase
Your application — the root of everything.
```javascript
this.app.fire('game:start');
const player = this.app.root.findByName('Player');
const texture = this.app.assets.find('logo', 'texture');
```
### Entity
Objects in your scene hierarchy.
```javascript
this.entity.setPosition(0, 5, 0);
this.entity.rotate(0, 90, 0);
const child = this.entity.findByName('Weapon');
```
### Component
Adds functionality to entities. Access via entity property:
```javascript
const camera = this.entity.camera;
const light = this.entity.light;
const rigidbody = this.entity.rigidbody;
const sound = this.entity.sound;
```
## Math Classes
```javascript
import { Vec3, Quat, Color } from 'playcanvas';
const position = new Vec3(0, 5, 0);
const rotation = new Quat();
const red = new Color(1, 0, 0);
```
## Common Script Patterns
### Finding Entities
```javascript
// By name (searches entire hierarchy)
const player = this.app.root.findByName('Player');
// By tag (returns array)
const enemies = this.app.root.findByTag('enemy');
// Relative to current entity
const weapon = this.entity.findByPath('Arms/RightHand/Weapon');
```
### Working with Assets
```javascript
const sound = this.app.assets.find('explosion', 'audio');
sound.ready(() => {
    this.entity.sound.play('explosion');
});
this.app.assets.load(sound);
```
### Events and Communication
```javascript
// Fire application events
this.app.fire('player:died', this.entity);
// Listen for events
this.app.on('game:start', this.onGameStart, this);
```
## Learning More
- Full Engine API Reference: https://api.playcanvas.com/engine/
- Use the VS Code Extension for autocomplete and inline documentation
## Events
# Events
Events are a useful way of communicating between scripts in order to respond to things that happen without checking every frame.
Many PlayCanvas object types (such as script instances) have event handling support built-in, inherited from the Engine's EventHandler class. Event handling objects have the following methods:
- `on()` — registers an event listener
- `once()` — registers an event listener that unregisters itself after the first call
- `off()` — unregisters an event listener
- `fire()` — sends an event
- `hasEvent()` — queries whether an object is listening on a particular event
## Using Events
### Firing Events
```javascript
import { Script } from 'playcanvas';
export class Player extends Script {
    static scriptName = 'player';
    update(dt) {
        const x = 1;
        const y = 1;
        this.fire('move', x, y);
    }
}
```
### Listening for Events
```javascript
import { Script } from 'playcanvas';
export class Display extends Script {
    static scriptName = 'display';
            /** @attribute */
playerEntity;
    initialize() {
        const onPlayerMove = (x, y) => {
            console.log(x, y);
        };
        if (this.playerEntity?.script?.player) {
            this.playerEntity.script.player.on('move', onPlayerMove);
            // Clean up when destroyed
            this.playerEntity.script.player.once('destroy', () => {
                this.playerEntity.script.player.off('move', onPlayerMove);
            });
        }
    }
}
```
## Application Events (Recommended)
A more powerful pattern: use `this.app` as a central hub for firing events. This avoids keeping entity references.
By convention, use namespaced event names like `player:move` to signal event scope and prevent clashes.
### Firing Application Events
```javascript
export class Player extends Script {
    static scriptName = 'player';
    update(dt) {
        const x = 1, y = 1;
        this.app.fire('player:move', x, y);
    }
}
```
### Listening for Application Events
```javascript
export class Display extends Script {
    static scriptName = 'display';
    initialize() {
        const onPlayerMove = (x, y) => {
            console.log(x, y);
        };
        this.app.on('player:move', onPlayerMove);
        // Clean up when destroyed
        this.on('destroy', () => {
            this.app.off('player:move', onPlayerMove);
        });
    }
}
```
Application events reduce setup complexity and make for cleaner code.
## Event Naming Conventions
- Use `namespace:eventName` format (e.g., `player:move`, `game:start`, `ui:click`)
- Be consistent across your project
- Document custom events for team reference
## Debugging
# Debugging
Debugging is essential for identifying and fixing issues in your PlayCanvas scripts. When your code doesn't behave as expected, these tools and techniques will help you quickly find and resolve problems.
## Debugging Techniques
### Console Logging
The quickest way to understand what your code is doing. Add `console.log()` statements to track execution flow and inspect variable values.
```javascript
initialize() {
    console.log('Script initialized on', this.entity.name);
}
update(dt) {
    console.log('Position:', this.entity.getPosition().toString());
}
```
Also useful:
- `console.warn()` — for warnings
- `console.error()` — for errors
- `console.table()` — for array/object data
- `console.group()` / `console.groupEnd()` — for grouped output
- `console.time()` / `console.timeEnd()` — for performance timing
### Browser Developer Tools
Use breakpoints, step-through debugging, and performance profiling to deeply inspect your running code.
Key features:
- **Sources tab**: Set breakpoints in your script files
- **Console**: Run JavaScript expressions against the current state
- **Watch**: Track variable values in real-time
- **Call Stack**: See the function call chain
- **Performance tab**: Profile frame rates and bottlenecks
### Editor Debugging Features
- **Launch in new tab**: Opens your app in a separate browser tab for full dev tools access
- **Hot Reloading**: Changes to scripts are immediately reflected without page refresh
- **Error Console**: Errors appear in the Editor's console panel
## Migration Guide
# Migration Guide (Classic → ESM Scripts)
ESM Scripts replace the older Classic Scripting system as the recommended way to develop PlayCanvas applications. Classic scripts will continue to work in existing projects and will be supported, but ESM is recommended for new projects.
## Gradual Migration
Projects can contain both ESM Scripts and Classic Scripts — you don't need to update all scripts at once. Gradually migrate and iteratively test.
## Codemod
A codemod is available to automatically migrate Classic Scripts to ESM format:
```bash
npx codemod playcanvas-esm-scripts
```
Repository: https://github.com/playcanvas/codemods
## Key Differences
### Module Scope
ESM Scripts have module scope; Classic Scripts have global scope. Modules cannot implicitly access variables defined in other files.
```javascript
// Classic (config.js) — global scope
var SPEED = 10;
// Classic (script.js) — SPEED is accessible globally
console.log(SPEED);
// ESM (config.mjs)
export const SPEED = 10;
// ESM (script.mjs) — must import explicitly
import { SPEED } from './config.mjs';
console.log(SPEED); // ✅ Works!
```
### Loading Order
ESM Scripts do not have a loading order. Dependencies are explicitly defined through import/export syntax instead of relying on script loading order.
### New Script Class
The Script base class replaces ScriptType as the default. ScriptType still exists (internally extends Script) but is not recommended for ESM scripts.
#### Attribute Events
ESM Scripts do not fire `attr:[name]` events. Instead, define your own change events:
```javascript
const watch = (target, prop) => {
    const privateProp = `#${prop}`;
    target[privateProp] = target[prop];
    Object.defineProperty(target, prop, {
        set(value) {
            if (target[privateProp] !== value) {
                target.fire(`changed:${prop}`, value);
                target[privateProp] = value;
            }
        },
        get() { return this[privateProp]; }
    });
};
```
#### Attribute Copying
ESM Script attributes are passed by reference, not copied. For copy behavior, use getters/setters:
```javascript
import { Script, Vec3 } from 'playcanvas';
export class Rotate extends Script {
    static scriptName = 'rotate';
    _speed = new Vec3();
    set speed(value) { this._speed.copy(value); }
    get speed() { return this._speed; }
}
```
## App Lifecycle
# Application Lifecycle
The high-level flow of a PlayCanvas application created with the PlayCanvas Editor follows a defined lifecycle.
## Lifecycle Stages
1. **Loading**: The application loads all required assets (scripts, models, textures, etc.)
2. **Preloading**: Shows a loading screen while assets are fetched
3. **Initialize**: All scripts' `initialize()` methods are called
4. **Post-Initialize**: All scripts' `postInitialize()` methods are called
5. **Update Loop**: Every frame, all scripts' `update(dt)` methods are called
6. **Post-Update**: After all updates, `postUpdate(dt)` is called on all scripts
7. **Render**: The scene is rendered
## Script Lifecycle Methods
### initialize()
Called once when the script is first loaded. Use for setting up initial state, creating objects, and registering event listeners.
```javascript
initialize() {
        this.speed = 5;
    this.app.on('game:start', this.onGameStart, this);
}
```
### postInitialize()
Called after ALL scripts in the scene are initialized. Use when you need other entities/scripts to be ready.
```javascript
postInitialize() {
        const player = this.app.root.findByName('Player');
}
```
### update(dt)
Called every frame. `dt` is the delta time in seconds since the last frame.
```javascript
update(dt) {
    this.entity.rotate(0, 90 * dt, 0);
}
```
### postUpdate(dt)
Called after all update calls complete. Useful for post-frame processing.
### swap()
Called when hot-reloading updates the script code. Transfer state from the old script instance.
## Application Events
- `app:ready` — Application is fully loaded and running
- `app:preload:end` — Preloading phase completed

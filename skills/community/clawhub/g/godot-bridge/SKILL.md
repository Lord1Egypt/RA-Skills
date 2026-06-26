---
name: godot-bridge
description: "Godot 4.x Project Generator CLI. Create 2D/3D games with 80+ CLI commands: projects, scenes, scripts, levels, UI (menu/HUD/dialog/inventory), game components (health/inventory/save/input/dialogue/quest), physics (rigid/kinematic/area/joint), particles, animations, materials, and export to HTML5/Windows/macOS/Linux/Android/iOS. Perfect for AI-driven game development, rapid prototyping, and automated workflows."
metadata:
  openclaw:
    emoji: 🎮
    requires:
      bins: ["node"]
---

# Godot Bridge - Project Generator CLI v3.0

Generate complete Godot 4.x projects with scenes, scripts, and game components.

## Quick Start

```bash
# Create project
clawbridge init MyGame

# Enter project
cd MyGame

# Add components
clawbridge component health --type health
clawbridge component inventory --type inventory

# Add objects
clawbridge label "Score: 0" --x 50 --y 30
clawbridge box --x 200 --y 150
clawbridge camera --x 640 --y 360

# Open in Godot
clawbridge open
```

## Commands

### Project
```bash
clawbridge init MyGame              # Basic 2D project
clawbridge init MyGame --3d        # 3D project
clawbridge init MyGame --template rpg   # RPG template
```

### Generate
```bash
clawbridge scene Main       # Generate scene
clawbridge script Player    # Generate script
clawbridge level Level1     # Generate level
```

### Game Components
```bash
# Health System
clawbridge component health --type health

# Inventory System
clawbridge component inventory --type inventory

# Save/Load System
clawbridge component save_system --type save

# Input System
clawbridge component input_system --type input

# Dialogue System
clawbridge component dialogue --type dialogue

# Quest System
clawbridge component quest --type quest
```

### Objects (add to scene)
```bash
clawbridge label "Hello" --x 100 --y 50
clawbridge button "Click" --x 200
clawbridge box --x 100 --y 100
clawbridge sphere --x 200
clawbridge camera --x 640 --y 360
clawbridge light --x 100
clawbridge particles --amount 50
clawbridge character
```

## Generated Project Structure

```
MyGame/
├── project.godot
├── icon.svg
├── scenes/
│   └── main.tscn
├── scripts/
│   ├── main.gd
│   ├── game_manager.gd
│   └── [your components]
├── levels/
├── assets/
└── prefabs/
```

## Game Components

### Health System
- `take_damage(amount)` - Apply damage
- `heal(amount)` - Heal entity
- `is_alive()` - Check if alive
- Signals: `health_changed`, `died`

### Inventory System
- `add_item(name)` - Add item
- `remove_item(name)` - Remove item
- `has_item(name)` - Check item
- `get_item_count(name)` - Get quantity

### Save/Load System
- `save_game()` - Save to disk
- `load_game()` - Load from disk
- Auto-saves player stats and current level

### Input System
- `get_direction()` - Get left/right input (-1 to 1)
- `is_jump_pressed()` - Check jump

### Dialogue System
- `show(lines)` - Start dialogue with array of strings
- `next()` - Advance to next line
- Signals: `line_displayed`, `dialogue_ended`

### Quest System
- `start_quest(name, target)` - Start quest
- `update_quest(name, progress)` - Update progress
- `complete_quest(name)` - Complete quest
- Signals: `quest_started`, `quest_completed`

## Options

| Option | Description |
|--------|-------------|
| --type | Component type |
| --template | Project template |
| --x, --y | Position coordinates |
| --3d | Create 3D project |

## Example: Complete RPG

```bash
# Create RPG project
clawbridge init MyRPG --template rpg

# Add game systems
clawbridge component health --type health
clawbridge component inventory --type inventory
clawbridge component quest --type quest
clawbridge component save_system --type save
clawbridge component dialogue --type dialogue

# Add UI
clawbridge label "HP: 100" --x 20 --y 20
clawbridge label "Gold: 0" --x 20 --y 50

# Open in Godot
clawbridge open
```

## License

MIT

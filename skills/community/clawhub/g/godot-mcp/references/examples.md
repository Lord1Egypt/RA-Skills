# Godot MCP 使用示例

## 示例 1: 创建玩家角色

### 步骤 1: 创建场景和节点
```json
// 创建场景
{
  "tool": "scene_create",
  "params": {
    "name": "Player",
    "root_type": "CharacterBody2D"
  }
}

// 添加精灵
{
  "tool": "node_add",
  "params": {
    "type": "Sprite2D",
    "name": "Sprite",
    "parent": "Player",
    "properties": {
      "texture": "res://textures/player.png",
      "hframes": 4,
      "vframes": 2
    }
  }
}

// 添加碰撞形状
{
  "tool": "node_add",
  "params": {
    "type": "CollisionShape2D",
    "name": "CollisionShape",
    "parent": "Player"
  }
}

// 配置碰撞形状
{
  "tool": "physics",
  "params": {
    "action": "set_shape",
    "node": "Player/CollisionShape",
    "shape_type": "CapsuleShape2D",
    "properties": {
      "radius": 10,
      "height": 30
    }
  }
}

// 添加动画播放器
{
  "tool": "node_add",
  "params": {
    "type": "AnimationPlayer",
    "name": "AnimationPlayer",
    "parent": "Player"
  }
}
```

### 步骤 2: 创建脚本
```json
// 创建脚本
{
  "tool": "script_create",
  "params": {
    "name": "player.gd",
    "template": "CharacterBody2D",
    "path": "res://scripts/"
  }
}

// 写入代码
{
  "tool": "script_write",
  "params": {
    "path": "res://scripts/player.gd",
    "content": "extends CharacterBody2D\n\nconst SPEED = 300.0\nconst JUMP_VELOCITY = -400.0\n\nvar gravity = ProjectSettings.get_setting(\"physics/2d/default_gravity\")\n\n@onready var sprite = $Sprite\n@onready var anim_player = $AnimationPlayer\n\nfunc _physics_process(delta):\n    # Add gravity\n    if not is_on_floor():\n        velocity.y += gravity * delta\n    \n    # Handle jump\n    if Input.is_action_just_pressed(\"ui_accept\") and is_on_floor():\n        velocity.y = JUMP_VELOCITY\n    \n    # Get input direction\n    var direction = Input.get_axis(\"ui_left\", \"ui_right\")\n    \n    # Flip sprite\n    if direction != 0:\n        sprite.flip_h = direction < 0\n    \n    # Apply movement\n    if direction:\n        velocity.x = direction * SPEED\n        anim_player.play(\"run\")\n    else:\n        velocity.x = move_toward(velocity.x, 0, SPEED)\n        anim_player.play(\"idle\")\n    \n    move_and_slide()"
  }
}

// 附加脚本
{
  "tool": "script_attach",
  "params": {
    "node": "Player",
    "script": "res://scripts/player.gd"
  }
}
```

### 步骤 3: 创建动画
```json
// 创建 idle 动画
{
  "tool": "animation",
  "params": {
    "action": "create",
    "node": "Player/AnimationPlayer",
    "animation": "idle",
    "length": 0.8,
    "loop": true,
    "tracks": [
      {
        "type": "texture",
        "path": "Sprite:texture",
        "keys": [
          {"time": 0.0, "value": "res://textures/player_idle_1.png"},
          {"time": 0.4, "value": "res://textures/player_idle_2.png"}
        ]
      }
    ]
  }
}

// 创建 run 动画
{
  "tool": "animation",
  "params": {
    "action": "create",
    "node": "Player/AnimationPlayer",
    "animation": "run",
    "length": 0.4,
    "loop": true,
    "tracks": [
      {
        "type": "texture",
        "path": "Sprite:texture",
        "keys": [
          {"time": 0.0, "value": "res://textures/player_run_1.png"},
          {"time": 0.1, "value": "res://textures/player_run_2.png"},
          {"time": 0.2, "value": "res://textures/player_run_3.png"},
          {"time": 0.3, "value": "res://textures/player_run_4.png"}
        ]
      }
    ]
  }
}
```

---

## 示例 2: 创建敌人 AI

### 完整流程
```json
// 1. 创建敌人场景
{
  "tool": "scene_create",
  "params": {"name": "Enemy", "root_type": "CharacterBody2D"}
}

// 2. 添加组件
{
  "tool": "node_add",
  "params": {
    "type": "Sprite2D",
    "name": "Sprite",
    "properties": {"texture": "res://textures/enemy.png"}
  }
}

{
  "tool": "node_add",
  "params": {"type": "CollisionShape2D", "name": "CollisionShape"}
}

{
  "tool": "physics",
  "params": {
    "action": "set_shape",
    "node": "CollisionShape",
    "shape_type": "CircleShape2D",
    "properties": {"radius": 15}
  }
}

// 3. 添加检测区域
{
  "tool": "node_add",
  "params": {"type": "Area2D", "name": "DetectionArea"}
}

{
  "tool": "node_add",
  "params": {
    "type": "CollisionShape2D",
    "name": "DetectionShape",
    "parent": "DetectionArea"
  }
}

{
  "tool": "physics",
  "params": {
    "action": "set_shape",
    "node": "DetectionArea/DetectionShape",
    "shape_type": "CircleShape2D",
    "properties": {"radius": 100}
  }
}

// 4. 创建 AI 脚本
{
  "tool": "script_create",
  "params": {"name": "enemy.gd", "template": "CharacterBody2D"}
}

{
  "tool": "script_write",
  "params": {
    "path": "res://scripts/enemy.gd",
    "content": "extends CharacterBody2D\n\nenum State {PATROL, CHASE, ATTACK}\nvar current_state = State.PATROL\n\nconst SPEED = 150.0\nconst PATROL_SPEED = 50.0\n\nvar patrol_points = []\nvar current_patrol_index = 0\nvar player = null\n\n@onready var detection_area = $DetectionArea\n\nfunc _ready():\n    # 连接检测信号\n    detection_area.body_entered.connect(_on_detection_area_body_entered)\n    detection_area.body_exited.connect(_on_detection_area_body_exited)\n    \n    # 设置巡逻点\n    patrol_points = [\n        global_position + Vector2(-100, 0),\n        global_position + Vector2(100, 0)\n    ]\n\nfunc _physics_process(delta):\n    match current_state:\n        State.PATROL:\n            _patrol()\n        State.CHASE:\n            _chase()\n        State.ATTACK:\n            _attack()\n    \n    move_and_slide()\n\nfunc _patrol():\n    var target = patrol_points[current_patrol_index]\n    var direction = (target - global_position).normalized()\n    \n    velocity = direction * PATROL_SPEED\n    \n    if global_position.distance_to(target) < 10:\n        current_patrol_index = (current_patrol_index + 1) % patrol_points.size()\n\nfunc _chase():\n    if player:\n        var direction = (player.global_position - global_position).normalized()\n        velocity = direction * SPEED\n        \n        # 攻击范围检测\n        if global_position.distance_to(player.global_position) < 30:\n            current_state = State.ATTACK\n    else:\n        current_state = State.PATROL\n\nfunc _attack():\n    velocity = Vector2.ZERO\n    # 攻击逻辑\n    print(\"Attacking player!\")\n    \n    # 追逐状态\n    if player and global_position.distance_to(player.global_position) > 30:\n        current_state = State.CHASE\n\nfunc _on_detection_area_body_entered(body):\n    if body.is_in_group(\"player\"):\n        player = body\n        current_state = State.CHASE\n\nfunc _on_detection_area_body_exited(body):\n    if body == player:\n        player = null"
  }
}

// 5. 附加脚本
{
  "tool": "script_attach",
  "params": {"node": "Enemy", "script": "res://scripts/enemy.gd"}
}

// 6. 添加到分组
{
  "tool": "group",
  "params": {
    "action": "add_to_group",
    "node": "Enemy",
    "group": "enemies"
  }
}
```

---

## 示例 3: 创建 UI 系统

### 创建主菜单
```json
// 1. 创建 UI 场景
{
  "tool": "scene_create",
  "params": {"name": "MainMenu", "root_type": "Control"}
}

// 2. 设置根节点
{
  "tool": "node_set_property",
  "params": {
    "node": "MainMenu",
    "property": "anchor_right",
    "value": 1.0
  }
}

{
  "tool": "node_set_property",
  "params": {
    "node": "MainMenu",
    "property": "anchor_bottom",
    "value": 1.0
  }
}

// 3. 添加背景
{
  "tool": "node_add",
  "params": {
    "type": "TextureRect",
    "name": "Background",
    "properties": {
      "texture": "res://textures/menu_bg.png",
      "stretch_mode": "scale"
    }
  }
}

// 4. 添加标题
{
  "tool": "node_add",
  "params": {
    "type": "Label",
    "name": "Title",
    "properties": {
      "text": "Fantasy RPG",
      "horizontal_alignment": "center",
      "vertical_alignment": "center"
    }
  }
}

// 5. 添加按钮容器
{
  "tool": "node_add",
  "params": {
    "type": "VBoxContainer",
    "name": "ButtonContainer",
    "properties": {
      "alignment": "center"
    }
  }
}

// 6. 添加按钮
{
  "tool": "node_add",
  "params": {
    "type": "Button",
    "name": "StartButton",
    "parent": "ButtonContainer",
    "properties": {"text": "开始游戏"}
  }
}

{
  "tool": "node_add",
  "params": {
    "type": "Button",
    "name": "SettingsButton",
    "parent": "ButtonContainer",
    "properties": {"text": "设置"}
  }
}

{
  "tool": "node_add",
  "params": {
    "type": "Button",
    "name": "QuitButton",
    "parent": "ButtonContainer",
    "properties": {"text": "退出"}
  }
}

// 7. 连接信号
{
  "tool": "signal",
  "params": {
    "action": "connect",
    "source": "ButtonContainer/StartButton",
    "signal": "pressed",
    "target": "MainMenu",
    "method": "_on_start_pressed"
  }
}

// 8. 创建脚本
{
  "tool": "script_create",
  "params": {"name": "main_menu.gd", "template": "Control"}
}

{
  "tool": "script_write",
  "params": {
    "path": "res://scripts/main_menu.gd",
    "content": "extends Control\n\nfunc _on_start_pressed():\n    get_tree().change_scene_to_file(\"res://scenes/game.tscn\")\n\nfunc _on_settings_pressed():\n    # 打开设置菜单\n    pass\n\nfunc _on_quit_pressed():\n    get_tree().quit()"
  }
}

{
  "tool": "script_attach",
  "params": {
    "node": "MainMenu",
    "script": "res://scripts/main_menu.gd"
  }
}
```

---

## 示例 4: 批量操作

### 批量创建关卡
```json
// Python 风格的批量操作（在 AI 客户端中）
const levels = ["Level1", "Level2", "Level3"];

for (const levelName of levels) {
    // 创建场景
    mcp_call("scene_create", {"name": levelName, "root_type": "Node2D"});
    
    // 添加 TileMap
    mcp_call("node_add", {"type": "TileMap", "name": "Ground"});
    
    // 添加玩家出生点
    mcp_call("node_add", {
        "type": "Marker2D",
        "name": "PlayerSpawn",
        "properties": {"position": {"x": 100, "y": 100}}
    });
    
    // 保存场景
    mcp_call("scene_save", {"path": `res://scenes/${levelName}.tscn`});
}
```

### 批量修改属性
```json
// 获取所有敌人节点
{
  "tool": "node_find",
  "params": {"pattern": "Enemy*"}
}

// 批量设置速度
for (const enemy of enemies) {
    mcp_call("node_set_property", {
        "node": enemy,
        "property": "speed",
        "value": 200
    });
}
```

---

## 示例 5: 资源管理

### 创建材质库
```json
// 1. 创建目录
mcp_call("filesystem_write", {
    "path": "res://materials/.gdignore",
    "content": ""
});

// 2. 创建材质
const materials = [
    {"name": "wood", "color": "#8B4513"},
    {"name": "stone", "color": "#808080"},
    {"name": "metal", "color": "#C0C0C0"}
];

for (const mat of materials) {
    mcp_call("resource_create", {
        "type": "StandardMaterial3D",
        "path": `res://materials/${mat.name}.tres`,
        "properties": {
            "albedo_color": mat.color,
            "roughness": 0.8
        }
    });
}
```

---

## 示例 6: 测试自动化

### 创建测试场景
```json
// 1. 创建测试场景
{
  "tool": "scene_create",
  "params": {"name": "TestScene", "root_type": "Node2D"}
}

// 2. 添加测试对象
{
  "tool": "node_add",
  "params": {
    "type": "RigidBody2D",
    "name": "TestObject",
    "properties": {"position": {"x": 400, "y": 100}}
  }
}

// 3. 添加地面
{
  "tool": "node_add",
  "params": {
    "type": "StaticBody2D",
    "name": "Ground",
    "properties": {"position": {"x": 400, "y": 500}}
  }
}

// 4. 创建测试脚本
{
  "tool": "script_write",
  "params": {
    "path": "res://tests/test_physics.gd",
    "content": "extends Node2D\n\nfunc _ready():\n    var test_object = $TestObject\n    var initial_pos = test_object.position\n    \n    # 等待物理模拟\n    await get_tree().create_timer(2.0).timeout\n    \n    # 验证物体已下落\n    assert(test_object.position.y > initial_pos.y, \"Object should fall\")\n    \n    print(\"Physics test passed!\")"
  }
}
```

---

## 调试技巧

### 1. 查看场景结构
```json
{
  "tool": "scene_get_tree",
  "params": {"include_properties": true}
}
```

### 2. 检查节点
```json
{
  "tool": "node_get",
  "params": {
    "node": "Player",
    "include_children": true
  }
}
```

### 3. 查看日志
```json
{
  "tool": "debug_get_logs",
  "params": {
    "count": 50,
    "filter": "error"
  }
}
```

### 4. 验证操作
```json
// 执行操作后验证
mcp_call("node_set_property", {
    "node": "Player",
    "property": "position",
    "value": {"x": 100, "y": 200}
});

// 验证
const node = mcp_call("node_get", {"node": "Player"});
assert(node.properties.position.x === 100);
```

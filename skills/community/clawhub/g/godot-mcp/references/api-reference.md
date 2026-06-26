# Godot MCP API 快速参考

## 场景工具

### scene_create
创建新场景
```json
{
  "name": "MyScene",
  "root_type": "Node2D"
}
```

### scene_open
打开场景
```json
{
  "path": "res://scenes/level1.tscn"
}
```

### scene_save
保存当前场景
```json
{}
```

### scene_get_tree
获取场景树
```json
{
  "include_properties": true
}
```

**返回示例**:
```json
{
  "name": "GameScene",
  "type": "Node2D",
  "children": [
    {
      "name": "Player",
      "type": "CharacterBody2D",
      "properties": {
        "position": {"x": 100, "y": 200}
      }
    }
  ]
}
```

---

## 节点工具

### node_add
添加节点
```json
{
  "type": "Sprite2D",
  "name": "PlayerSprite",
  "parent": "Player",
  "properties": {
    "position": {"x": 0, "y": 0},
    "modulate": "#FFFFFF"
  }
}
```

### node_set_property
设置属性
```json
{
  "node": "Player",
  "property": "position",
  "value": {"x": 100, "y": 200}
}
```

**常用属性**:
```
position: {"x": float, "y": float}
rotation: float (弧度)
scale: {"x": float, "y": float}
modulate: "#RRGGBB" 或 {"r": 1, "g": 1, "b": 1, "a": 1}
visible: boolean
z_index: int
```

### node_get
获取节点信息
```json
{
  "node": "Player",
  "include_children": true
}
```

### node_find
查找节点
```json
{
  "pattern": "Enemy*",
  "type": "CharacterBody2D"
}
```

### node_duplicate
复制节点
```json
{
  "node": "Enemy",
  "count": 5,
  "prefix": "Enemy"
}
```

### node_move
移动节点
```json
{
  "node": "Player",
  "new_parent": "Entities"
}
```

### node_delete
删除节点
```json
{
  "node": "Enemy1"
}
```

---

## 脚本工具

### script_create
创建脚本
```json
{
  "name": "player.gd",
  "template": "CharacterBody2D",
  "path": "res://scripts/"
}
```

**可用模板**:
```
CharacterBody2D  - 2D 角色控制器
RigidBody2D      - 2D 刚体
StaticBody2D     - 2D 静态体
Node2D           - 基础 2D 节点
Area2D           - 2D 区域
```

### script_write
写入脚本
```json
{
  "path": "res://scripts/player.gd",
  "content": "extends CharacterBody2D\n\nfunc _ready():\n    print('Player ready')"
}
```

### script_read
读取脚本
```json
{
  "path": "res://scripts/player.gd"
}
```

### script_attach
附加脚本
```json
{
  "node": "Player",
  "script": "res://scripts/player.gd"
}
```

---

## 资源工具

### resource_load
加载资源
```json
{
  "path": "res://textures/player.png"
}
```

### resource_create
创建资源
```json
{
  "type": "GradientTexture2D",
  "path": "res://resources/gradient.tres",
  "properties": {
    "gradient": {
      "colors": ["#FF0000", "#00FF00"],
      "offsets": [0.0, 1.0]
    }
  }
}
```

### resource_save
保存资源
```json
{
  "path": "res://resources/material.tres"
}
```

---

## 物理工具

### physics
配置物理
```json
{
  "action": "add_shape",
  "node": "Player",
  "shape_type": "CapsuleShape2D",
  "properties": {
    "radius": 10,
    "height": 30
  }
}
```

**可用形状**:
```
CircleShape2D    - radius
RectangleShape2D - size
CapsuleShape2D   - radius, height
ConvexPolygonShape2D - points
ConcavePolygonShape2D - faces
```

---

## TileMap 工具

### tilemap
操作 TileMap
```json
{
  "action": "set_cells",
  "node": "Ground",
  "cells": [
    {"coords": [0, 0], "tile_id": 1},
    {"coords": [1, 0], "tile_id": 1},
    {"coords": [2, 0], "tile_id": 1}
  ]
}
```

**可用操作**:
```
set_cell      - 设置单个瓷砖
set_cells     - 设置多个瓷砖
erase_cell    - 删除瓷砖
get_cell      - 获取瓷砖信息
set_pattern   - 设置图案
```

---

## 文件系统工具

### filesystem_list
列出目录
```json
{
  "path": "res://textures",
  "recursive": true
}
```

### filesystem_read
读取文件
```json
{
  "path": "res://data/config.json"
}
```

### filesystem_write
写入文件
```json
{
  "path": "res://data/save.json",
  "content": "{\"level\": 1, \"score\": 100}"
}
```

### filesystem_delete
删除文件
```json
{
  "path": "res://temp/file.tmp"
}
```

---

## 编辑器工具

### editor_select_node
选中节点
```json
{
  "node": "Player"
}
```

### editor_get_selection
获取选中
```json
{}
```

### editor_undo_redo
撤销/重做
```json
{
  "action": "undo"  // 或 "redo"
}
```

---

## 调试工具

### debug_get_logs
获取日志
```json
{
  "count": 100,
  "filter": "error"  // "all", "warning", "error"
}
```

---

## 动画工具

### animation
创建动画
```json
{
  "action": "create",
  "node": "Player/Sprite",
  "animation": "idle",
  "tracks": [
    {
      "type": "texture",
      "keys": [
        {"time": 0.0, "value": "res://textures/idle_1.png"},
        {"time": 0.2, "value": "res://textures/idle_2.png"}
      ]
    }
  ]
}
```

---

## 信号工具

### signal
连接信号
```json
{
  "action": "connect",
  "source": "Button",
  "signal": "pressed",
  "target": "GameManager",
  "method": "_on_button_pressed"
}
```

---

## 分组工具

### group
管理分组
```json
{
  "action": "add_to_group",
  "node": "Enemy1",
  "group": "enemies"
}
```

**可用操作**:
```
add_to_group    - 添加到分组
remove_from_group - 从分组移除
get_nodes_in_group - 获取分组节点
```

---

## 错误代码

| 代码 | 描述 |
|------|------|
| `NODE_NOT_FOUND` | 节点不存在 |
| `INVALID_TYPE` | 无效的节点类型 |
| `PROPERTY_NOT_FOUND` | 属性不存在 |
| `INVALID_VALUE` | 无效的值 |
| `FILE_NOT_FOUND` | 文件不存在 |
| `PERMISSION_DENIED` | 权限不足 |
| `SCENE_NOT_OPEN` | 没有打开的场景 |
| `SCRIPT_ERROR` | 脚本错误 |

---

## 类型映射

### Godot 类型 → JSON 类型
```
Vector2    → {"x": float, "y": float}
Vector3    → {"x": float, "y": float, "z": float}
Color      → "#RRGGBB" 或 {"r": 1, "g": 1, "b": 1, "a": 1}
Rect2      → {"position": Vector2, "size": Vector2}
Transform2D → {"x": Vector2, "y": Vector2, "origin": Vector2}
Array      → [...]
Dictionary → {...}
```

### 常用节点类型
```
2D:
- Node2D
- Sprite2D
- CharacterBody2D
- RigidBody2D
- StaticBody2D
- Area2D
- TileMap
- Camera2D
- AnimatedSprite2D
- CollisionShape2D

3D:
- Node3D
- MeshInstance3D
- CharacterBody3D
- RigidBody3D
- Camera3D
- Light3D

UI:
- Control
- Button
- Label
- Panel
- VBoxContainer
- HBoxContainer
```

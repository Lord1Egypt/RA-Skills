---
name: godot-mcp
description: Godot MCP (Model Context Protocol) integration enabling AI assistants to directly interact with Godot Editor. Use when working with Godot projects through AI clients (Claude CLI, Codex, Cursor, Windsurf), automating scene creation, node manipulation, script editing, resource management, and project control. Includes setup guide for multiple AI clients.
---

# Godot MCP Server 集成指南

## 概述

Godot MCP Server 是一个强大的插件，让 AI 助手能够直接与 Godot 编辑器交互，实现 AI 驱动的游戏开发。

### 核心能力
- **场景管理** - 创建、打开、保存场景
- **节点操作** - 添加、删除、移动、修改节点
- **脚本编辑** - 创建和修改 GDScript 脚本
- **资源管理** - 加载和创建游戏资源
- **文件系统** - 浏览项目、读写文件
- **编辑器控制** - 选中对象、撤销重做
- **调试工具** - 查看日志、运行时信息

---

## 安装配置

### 1. 安装插件

```bash
# 克隆仓库
git clone https://github.com/DaxianLee/godot-mcp.git

# 复制到项目
cp -r godot-mcp/addons/godot_mcp /path/to/your/project/addons/
```

### 2. 启用插件

在 Godot 编辑器中：
1. `项目 -> 项目设置 -> 插件`
2. 找到 **Godot MCP Server**
3. 点击启用

### 3. 配置 MCP 服务器

默认配置：
- **端口**: 3000
- **地址**: `http://127.0.0.1:3000/mcp`
- **自动启动**: 开启

在 GodotMCP 面板中可以：
- 查看服务器状态
- 管理可用工具
- 配置 AI 客户端

---

## AI 客户端配置

### IDE 编辑器（一键配置）

#### Trae CN
```bash
# 配置文件位置
# macOS: ~/Library/Application Support/Trae CN/User/mcp.json
# Windows: %APPDATA%\Trae CN\User\mcp.json
# Linux: ~/.config/Trae CN/User/mcp.json

# 在 GodotMCP 面板中点击「一键配置」即可
```

#### Cursor
```bash
# 配置文件位置
~/.cursor/mcp.json

# 在 GodotMCP 面板中点击「一键配置」即可
```

#### Windsurf
```bash
# 配置文件位置
~/.codeium/windsurf/mcp_config.json

# 在 GodotMCP 面板中点击「一键配置」即可
```

### CLI 工具（命令配置）

#### Claude CLI (Claude Code)
```bash
# 用户级配置（全局）
claude mcp add --scope user --transport http godot-mcp http://127.0.0.1:3000/mcp

# 项目级配置（当前项目）
claude mcp add --scope project --transport http godot-mcp http://127.0.0.1:3000/mcp
```

#### Codex CLI
```bash
# 用户级
codex mcp add --scope user --transport http godot-mcp http://127.0.0.1:3000/mcp

# 项目级
codex mcp add --scope project --transport http godot-mcp http://127.0.0.1:3000/mcp
```

#### Gemini CLI
```bash
# 用户级
gemini mcp add --scope user --transport http godot-mcp http://127.0.0.1:3000/mcp

# 项目级
gemini mcp add --scope project --transport http godot-mcp http://127.0.0.1:3000/mcp
```

---

## 工具分类

### 核心工具

#### 场景工具 (Scene)
```
scene_create        - 创建新场景
scene_open          - 打开指定场景
scene_save          - 保存当前场景
scene_get_tree      - 获取场景树结构
scene_get_current   - 获取当前场景信息
```

**使用示例**：
```
用户: 创建一个新场景，命名为 "Level1"
AI: [调用 scene_create {"name": "Level1"}]
    已创建场景 Level1

用户: 添加一个 Sprite2D 节点
AI: [调用 node_add {"type": "Sprite2D", "name": "Player"}]
    已添加 Sprite2D 节点到场景
```

#### 节点工具 (Node)
```
node_add            - 添加新节点
node_delete         - 删除节点
node_get            - 获取节点信息
node_set_property   - 设置节点属性
node_get_property   - 获取节点属性
node_move           - 移动节点位置
node_rename         - 重命名节点
node_duplicate      - 复制节点
node_find           - 查找节点
```

**使用示例**：
```
用户: 将 Player 节点的位置设置为 (100, 200)
AI: [调用 node_set_property {
       "node": "Player",
       "property": "position",
       "value": {"x": 100, "y": 200}
     }]
    已设置 Player 位置为 (100, 200)
```

#### 脚本工具 (Script)
```
script_create       - 创建新脚本
script_read         - 读取脚本内容
script_write        - 写入脚本内容
script_attach       - 附加脚本到节点
```

**使用示例**：
```
用户: 为 Player 节点创建一个脚本
AI: [调用 script_create {
       "name": "player.gd",
       "template": "CharacterBody2D"
     }]
    [调用 script_attach {
       "node": "Player",
       "script": "res://scripts/player.gd"
     }]
    已创建并附加脚本
```

#### 资源工具 (Resource)
```
resource_load       - 加载资源
resource_create     - 创建资源
resource_save       - 保存资源
```

#### 文件系统工具 (Filesystem)
```
filesystem_list     - 列出目录内容
filesystem_read     - 读取文件
filesystem_write    - 写入文件
filesystem_delete   - 删除文件
```

#### 项目工具 (Project)
```
project_get_info        - 获取项目信息
project_get_settings    - 获取项目设置
```

#### 编辑器工具 (Editor)
```
editor_get_selection    - 获取当前选中
editor_select_node      - 选中指定节点
editor_undo_redo        - 撤销/重做操作
```

#### 调试工具 (Debug)
```
debug_get_logs      - 获取调试日志
```

### 视觉工具

#### 材质工具 (Material)
```
material            - 创建和配置材质
```

**使用示例**：
```
用户: 创建一个发光材质
AI: [调用 material {
       "type": "StandardMaterial3D",
       "emission": {"enabled": true, "color": "#00FF00"}
     }]
    已创建发光材质
```

#### 着色器工具 (Shader)
```
shader              - 着色器参数管理
```

#### 灯光工具 (Lighting)
```
lighting            - 场景灯光配置
```

#### 粒子工具 (Particle)
```
particle            - 粒子效果创建
```

### 2D 工具

#### 瓦片地图工具 (TileMap)
```
tilemap             - TileMap 编辑
```

**使用示例**：
```
用户: 创建一个 TileMap 并设置瓷砖
AI: [调用 node_add {"type": "TileMap", "name": "Ground"}]
    [调用 tilemap {
       "action": "set_cell",
       "coords": [(0, 0), (1, 0), (2, 0)],
       "tile_id": 1
     }]
    已创建 TileMap 并铺设瓷砖
```

#### 几何体工具 (Geometry)
```
geometry            - 2D 几何图形
```

### 游戏玩法工具

#### 物理工具 (Physics)
```
physics             - 物理体和碰撞配置
```

**使用示例**：
```
用户: 为 Player 添加碰撞形状
AI: [调用 node_add {
       "type": "CollisionShape2D",
       "parent": "Player"
     }]
    [调用 physics {
       "node": "Player/CollisionShape2D",
       "shape": "CapsuleShape2D",
       "radius": 10,
       "height": 20
     }]
    已添加碰撞形状
```

#### 导航工具 (Navigation)
```
navigation          - 导航网格和寻路
```

#### 音频工具 (Audio)
```
audio               - 音频播放和配置
```

### 实用工具

#### UI 工具
```
ui                  - 用户界面组件
```

#### 信号工具 (Signal)
```
signal              - 信号连接管理
```

#### 分组工具 (Group)
```
group               - 节点分组管理
```

---

## 工作流程示例

### 示例 1: 创建完整场景

```
用户: 创建一个包含玩家、敌人和地形的场景

AI 执行步骤:
1. [scene_create {"name": "GameScene"}]
2. [node_add {"type": "Node2D", "name": "Entities"}]
3. [node_add {"type": "CharacterBody2D", "name": "Player", "parent": "Entities"}]
4. [node_add {"type": "Sprite2D", "name": "Sprite", "parent": "Player"}]
5. [script_create {"name": "player.gd"}]
6. [script_attach {"node": "Player", "script": "res://player.gd"}]
7. [node_add {"type": "CharacterBody2D", "name": "Enemy", "parent": "Entities"}]
8. [node_add {"type": "TileMap", "name": "Ground"}]
9. [scene_save]

完成！已创建包含玩家、敌人和地形的场景。
```

### 示例 2: 配置玩家物理

```
用户: 为玩家添加物理和碰撞检测

AI 执行步骤:
1. [node_add {"type": "CollisionShape2D", "parent": "Player"}]
2. [physics {
     "node": "Player/CollisionShape2D",
     "shape": "CapsuleShape2D",
     "radius": 10,
     "height": 30
   }]
3. [script_write {
     "path": "res://player.gd",
     "content": "extends CharacterBody2D\n\nconst SPEED = 300.0\nconst JUMP_VELOCITY = -400.0\n\nvar gravity = ProjectSettings.get_setting(\"physics/2d/default_gravity\")\n\nfunc _physics_process(delta):\n    # Add the gravity.\n    if not is_on_floor():\n        velocity.y += gravity * delta\n    \n    # Handle Jump.\n    if Input.is_action_just_pressed(\"ui_accept\") and is_on_floor():\n        velocity.y = JUMP_VELOCITY\n    \n    # Get the input direction and handle the movement/deceleration.\n    var direction = Input.get_axis(\"ui_left\", \"ui_right\")\n    if direction:\n        velocity.x = direction * SPEED\n    else:\n        velocity.x = move_toward(velocity.x, 0, SPEED)\n    \n    move_and_slide()"
   }]

完成！已为玩家配置物理系统。
```

### 示例 3: 批量创建敌人

```
用户: 在场景中放置 5 个敌人

AI 执行步骤:
1. [scene_open {"path": "res://scenes/game.tscn"}]
2. [node_add {"type": "Node2D", "name": "Enemies"}]
3. [node_duplicate {"node": "Enemy", "count": 4}]
4. [node_set_property {"node": "Enemy2", "property": "position", "value": {"x": 200, "y": 0}}]
5. [node_set_property {"node": "Enemy3", "property": "position", "value": {"x": 400, "y": 0}}]
6. [node_set_property {"node": "Enemy4", "property": "position", "value": {"x": 600, "y": 0}}]
7. [node_set_property {"node": "Enemy5", "property": "position", "value": {"x": 800, "y": 0}}]
8. [scene_save]

完成！已创建 5 个敌人并放置在场景中。
```

---

## 高级用法

### 1. 自动化测试

```bash
# 创建测试场景
用户: 创建一个测试场景，包含多个物理对象

AI: [创建场景和物理对象]
    [配置物理参数]
    [添加调试可视化]
    测试场景已就绪
```

### 2. 资源批处理

```bash
# 批量处理资源
用户: 将所有纹理的 filter 模式改为 Nearest

AI: [filesystem_list {"path": "res://textures"}]
    [循环每个纹理]
    [resource_load]
    [修改 filter_mode]
    [resource_save]
    已更新所有纹理设置
```

### 3. 代码生成

```bash
# 生成游戏代码
用户: 为所有敌人节点生成 AI 脚本

AI: [node_find {"pattern": "Enemy*"}]
    [为每个敌人创建脚本]
    [根据类型生成 AI 逻辑]
    [附加脚本]
    已生成所有 AI 脚本
```

---

## 故障排除

### 服务器无法启动
```
检查:
1. 端口 3000 是否被占用
2. 防火墙是否阻止
3. Godot 版本是否兼容

解决:
- 更改端口号
- 关闭防火墙或添加例外
- 升级到 Godot 4.x
```

### AI 客户端无法连接
```
检查:
1. MCP 服务器是否运行（绿色状态）
2. 配置文件中的端口号是否正确
3. AI 客户端是否重启

解决:
- 重启 MCP 服务器
- 检查配置文件
- 重启 AI 客户端
```

### 工具调用失败
```
检查:
1. 节点路径是否正确
2. 属性名是否正确
3. 参数类型是否匹配

解决:
- 使用 scene_get_tree 查看场景结构
- 使用 node_get 查看可用属性
- 检查文档中的参数格式
```

---

## 最佳实践

### 1. 场景组织
```
推荐结构:
Scene
├── Entities
│   ├── Player
│   └── Enemies
├── Environment
│   ├── TileMaps
│   └── Props
└── UI
    └── HUD
```

### 2. 命名规范
```
- 节点名: PascalCase (Player, Enemy)
- 脚本名: snake_case (player.gd, enemy_ai.gd)
- 场景名: snake_case (level_1.tscn, main_menu.tscn)
```

### 3. 批量操作
```
优先使用批量工具:
- node_duplicate (批量复制)
- tilemap (批量铺设)
- filesystem_list (批量文件操作)
```

### 4. 错误处理
```
始终检查操作结果:
1. scene_get_tree (验证场景结构)
2. node_get (验证节点存在)
3. debug_get_logs (查看错误日志)
```

---

## 多语言支持

插件支持 9 种语言：
- English
- 简体中文
- 繁體中文
- 日本語
- Русский
- Français
- Português
- Español
- Deutsch

在 GodotMCP 面板的「服务器」标签中切换语言。

---

## 参考资源

- **MCP 协议**: [references/mcp-protocol.md](references/mcp-protocol.md)
- **API 文档**: [references/api-reference.md](references/api-reference.md)
- **示例代码**: [references/examples.md](references/examples.md)
- **故障排除**: [references/troubleshooting.md](references/troubleshooting.md)

---

## 许可证

**非商业使用许可证**

允许:
- 个人学习和研究
- 非商业开源项目
- 教育和教学

禁止:
- 商业用途
- 未经授权的再分发

商业使用请联系作者: LIDAXIAN (微信: lidaxian-AI)

---

## 贡献

欢迎提交 Issue 和 Pull Request！

GitHub: https://github.com/DaxianLee/godot-mcp

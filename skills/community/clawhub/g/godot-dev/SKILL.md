---
name: godot-dev
description: Godot 4.x game development with C#/.NET, covering best practices, architecture patterns, performance optimization, and common pitfalls. Use when working on Godot projects, debugging Godot-specific issues, designing game architecture, or implementing game systems. Includes GDScript-to-C# migration guidance.
---

# Godot 4.x C# 开发指南

## 核心架构原则

### 1. Autoload 单例模式
使用 Autoload 创建全局管理器：
```
GameManager (游戏状态)
EventManager (事件总线)
AudioManager (音频管理)
SaveManager (存档管理)
LocalizationManager (本地化)
```

### 2. 节点组织结构
```
GameScene (Node2D)
├── Entities (Node2D)
│   ├── Player (CharacterBody2D)
│   └── Enemies (Node2D)
├── Environment (Node2D)
│   ├── TileMaps
│   └── Props
└── UI (CanvasLayer)
    └── HUD
```

### 3. 信号驱动架构
使用信号解耦：
```csharp
// 定义信号
[Signal]
public delegate void HealthChangedEventHandler(int current, int max);

// 触发信号
EmitSignal(SignalName.HealthChanged, currentHealth, maxHealth);

// 连接信号
player.HealthChanged += OnHealthChanged;
```

## C# 特定最佳实践

### 类型安全
```csharp
// ✅ 正确：使用强类型
private PlayerController _player;

// ❌ 避免：过度使用 var 导致类型不明确
var player = GetNode("Player"); // Node? PlayerController?
```

### 资源加载
```csharp
// ✅ 推荐：预加载资源
[Export]
public PackedScene EnemyScene { get; set; }

// ⚠️ 运行时加载
var scene = GD.Load<PackedScene>("res://scenes/enemy.tscn");

// ❌ 避免：每帧加载
func _process():
    var tex = load("res://sprite.png")  # 性能杀手
```

### Godot 4.6 API 变化
```csharp
// Godot 4.5 → 4.6 迁移

// PhysicsRayQuery2D 已弃用
// ❌ 旧版
var query = PhysicsRayQuery2D.Create(from, to);

// ✅ 新版
var query = new PhysicsRayQueryParameters2D
{
    From = from,
    To = to,
    CollisionMask = collisionMask
};
var result = space.IntersectRay(query);

// Dictionary 类型限制
// ❌ Godot.Collections.Dictionary 不支持复杂类型
Godot.Collections.Dictionary<string, EnemyData> dict;

// ✅ 使用 System.Collections.Generic
System.Collections.Generic.Dictionary<string, EnemyData> dict;
```

## 性能优化

### 对象池
```csharp
public class ObjectPool<T> where T : Node, new()
{
    private readonly Stack<T> _pool = new();
    private readonly PackedScene _scene;

    public T Get() => _pool.Count > 0 ? _pool.Pop() : _scene.Instantiate<T>();
    
    public void Return(T obj)
    {
        obj.GetParent()?.RemoveChild(obj);
        _pool.Push(obj);
    }
}
```

### 避免常见陷阱
1. **不要在 _Process 中分配内存**
2. **使用 [Export] 而非字符串路径**
3. **批量处理物理操作**
4. **关闭不需要的节点处理**: `ProcessMode = ProcessModeEnum.Disabled`

## 调试技巧

### 自定义调试输出
```csharp
public static class Debug
{
    [Conditional("DEBUG")]
    public static void Log(string message)
    {
        GD.Print($"[{Time.GetTimeStringFromSystem()}] {message}");
    }
}
```

### 性能分析
```
# 启用调试模式
godot --path . --debug-gd

# 使用内置分析器
Debugger > Profiler > Start
```

## 参考资源

- **Godot 4.6 API 文档**: [references/godot-46-api.md](references/godot-46-api.md)
- **C# 模式**: [references/csharp-patterns.md](references/csharp-patterns.md)
- **常见错误**: [references/common-errors.md](references/common-errors.md)
- **性能指南**: [references/performance.md](references/performance.md)

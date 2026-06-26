# Godot 4.6 API 变化速查

## 物理系统

### Raycast API 变化
```csharp
// Godot 4.5 (已弃用)
var query = PhysicsRayQuery2D.Create(from, to, mask);
var result = space.IntersectRay(query);

// Godot 4.6 (推荐)
var query = new PhysicsRayQueryParameters2D
{
    From = from,
    To = to,
    CollisionMask = mask,
    CollideWithBodies = true,
    CollideWithAreas = false
};
var result = space.IntersectRay(query);
```

### PhysicsDirectSpaceState2D
```csharp
// 获取物理空间
var space = GetWorld2D().DirectSpaceState;

// 射线检测
var result = space.IntersectRay(query);
if (result.Count > 0)
{
    var collider = result["collider"].As<Node>();
    var position = result["position"].As<Vector2>();
}
```

## 节点变化

### YSort → Node2D
```csharp
// Godot 4.5
// YSort 节点自动按 Y 坐标排序

// Godot 4.6
// YSort 已移除，使用：
// 1. Node2D + 自定义排序
// 2. CanvasItem.ZIndex
// 3. TileMap 的 Y-sort 功能
```

### TileMap 更新
```csharp
// Godot 4.6 推荐使用新的 TileMapLayer
// 旧 TileMap 标记为过时但仍可用

// 新方式
var tileMap = new TileMapLayer();
tileMap.SetCell(position, sourceId, atlasCoords);

// 添加到场景
AddChild(tileMap);
```

## 资源系统

### 资源预加载
```csharp
// 预加载（编译时）
public static readonly PackedScene EnemyScene = 
    GD.Load<PackedScene>("res://scenes/enemy.tscn");

// 延迟加载（运行时）
var scene = ResourceLoader.Load<PackedScene>(
    "res://scenes/enemy.tscn",
    cacheMode: ResourceLoader.CacheMode.Reuse
);
```

### 子资源
```csharp
// 创建子资源
var shape = new CapsuleShape2D
{
    Radius = 10f,
    Height = 20f
};

// 保存为 .tres
ResourceSaver.Save(shape, "res://resources/shapes/capsule.tres");
```

## 信号系统

### C# 信号定义
```csharp
// 定义信号
[Signal]
public delegate void DamageTakenEventHandler(int amount, Node source);

// 触发信号
EmitSignal(SignalName.DamageTaken, 10, attacker);

// 连接信号（C# 风格）
enemy.DamageTaken += OnDamageTaken;

// 连接信号（Godot 风格）
enemy.Connect(SignalName.DamageTaken, 
    Callable.From((int amount, Node source) => OnDamageTaken(amount, source)));
```

## 输入系统

### InputEvent 处理
```csharp
public override void _Input(InputEvent @event)
{
    if (@event is InputEventKey keyEvent && keyEvent.Pressed)
    {
        if (keyEvent.Keycode == Key.Space)
        {
            // 处理空格键
        }
    }
}

// 动作映射（推荐）
public override void _UnhandledInput(InputEvent @event)
{
    if (@event.IsActionPressed("ui_accept"))
    {
        GetViewport().SetInputAsHandled();
    }
}
```

## 动画系统

### AnimationPlayer
```csharp
var animPlayer = GetNode<AnimationPlayer>("AnimationPlayer");

// 播放动画
animPlayer.Play("idle");

// 带回调
animPlayer.Play("attack");
await ToSignal(animPlayer, AnimationPlayer.SignalName.AnimationFinished);

// 混合动画
animPlayer.Play("walk");
animPlayer.Queue("run");
```

### Tween
```csharp
// 创建 Tween
var tween = CreateTween();

// 属性动画
tween.TweenProperty(sprite, "modulate:a", 0f, 1f);
tween.TweenProperty(sprite, "position", targetPos, 0.5f);

// 回调
tween.TweenCallback(Callable.From(() => QueueFree()));

// 链式调用
tween.SetEase(Tween.EaseType.Out).SetTrans(Tween.TransitionType.Quad);
```

# Godot C# 常见错误与解决方案

## 编译错误

### 1. Nullable 警告
```
warning CS8600: Converting null literal or possible null value to non-nullable type.
```

**解决方案：**
```csharp
// ❌ 错误
Node node = GetNode("Path"); // 可能为 null

// ✅ 方案 1: 使用可空类型
Node? node = GetNodeOrNull("Path");
if (node != null) { ... }

// ✅ 方案 2: 使用泛型方法
var node = GetNode<Node>("Path"); // 如果不存在会抛出异常

// ✅ 方案 3: 空值合并
var node = GetNodeOrNull<Node>("Path") ?? throw new NullReferenceException();
```

### 2. Variant 类型转换
```
error CS1503: Cannot convert from 'Godot.Variant' to 'int'
```

**解决方案：**
```csharp
// ❌ 错误
int value = dict["key"];  // dict["key"] 返回 Variant

// ✅ 正确
int value = dict["key"].As<int>();
string text = dict["name"].AsString();
Vector2 pos = dict["position"].AsVector2();
```

### 3. Dictionary 类型不兼容
```
error CS0266: Cannot implicitly convert type 'Godot.Collections.Dictionary' to 'System.Collections.Generic.Dictionary'
```

**解决方案：**
```csharp
// ❌ 错误：Godot Dictionary 不支持复杂类型
Godot.Collections.Dictionary<string, EnemyData> enemies;

// ✅ 正确：使用标准 C# Dictionary
using Dictionary = System.Collections.Generic.Dictionary;
Dictionary<string, EnemyData> enemies = new();

// 如果需要与 Godot 交互
Godot.Collections.Dictionary ToGodotDict()
{
    var dict = new Godot.Collections.Dictionary();
    foreach (var kvp in enemies)
    {
        dict[kvp.Key] = kvp.Value.ToVariant(); // 需要自定义转换
    }
    return dict;
}
```

## 运行时错误

### 4. 节点未找到
```
Node not found: "Player" (relative to "/root/Game")
```

**调试步骤：**
```csharp
// 1. 打印场景树
PrintTree();

// 2. 检查节点路径
GD.Print(GetPath());

// 3. 使用安全的获取方法
var node = GetNodeOrNull<Node>("Path");
if (node == null)
{
    GD.PrintErr($"Node not found at path: Path");
    GD.Print("Available children:");
    foreach (var child in GetChildren())
    {
        GD.Print($"  - {child.Name}");
    }
}
```

### 5. 信号连接失败
```
Error connecting signal 'health_changed' to method 'OnHealthChanged'
```

**解决方案：**
```csharp
// 检查信号是否定义
[Signal]
public delegate void HealthChangedEventHandler(int current, int max);

// 确保方法签名匹配
private void OnHealthChanged(int current, int max) { }

// 连接时检查
var err = Connect(SignalName.HealthChanged, 
    Callable.From(OnHealthChanged));
if (err != Error.Ok)
{
    GD.PrintErr($"Failed to connect signal: {err}");
}
```

### 6. 资源加载失败
```
Failed loading resource: res://scenes/missing.tscn
```

**检查清单：**
```csharp
// 1. 验证路径
var path = "res://scenes/enemy.tscn";
if (!ResourceLoader.Exists(path))
{
    GD.PrintErr($"Resource not found: {path}");
}

// 2. 检查 .import 文件
// 确保 .tscn.import 文件存在

// 3. 重新导入
// 在编辑器中: 右键资源 → Reimport
```

## 性能问题

### 7. 帧率下降

**常见原因：**
```csharp
// ❌ 每帧创建新对象
public override void _Process(double delta)
{
    var array = new int[1000];  // GC 压力
    var text = $"Frame {Engine.GetFramesDrawn()}"; // 字符串分配
}

// ✅ 预分配和复用
private readonly int[] _array = new int[1000];
private readonly StringBuilder _sb = new();

public override void _Process(double delta)
{
    _sb.Clear();
    _sb.Append("Frame ").Append(Engine.GetFramesDrawn());
}
```

### 8. 内存泄漏

**检测方法：**
```csharp
// 1. 使用调试输出
public override void _Ready()
{
    GD.Print($"Memory: {OS.GetStaticMemoryUsage() / 1024} KB");
}

// 2. 监控对象数量
GD.Print($"Node count: {GetTree().GetNodeCount()}");
```

**常见泄漏源：**
```csharp
// ❌ 忘记断开信号
public override void _ExitTree()
{
    // 忘记断开连接
}

// ✅ 清理信号
public override void _ExitTree()
{
    if (IsInstanceValid(_enemy))
    {
        _enemy.HealthChanged -= OnHealthChanged;
    }
}

// ❌ 未释放资源
var texture = GD.Load<Texture2D>("res://big_texture.png");

// ✅ 使用弱引用或手动释放
using var texture = GD.Load<Texture2D>("res://big_texture.png");
```

## 场景错误

### 9. 场景实例化失败
```
Failed to instantiate scene: res://scenes/enemy.tscn
```

**调试：**
```csharp
// 1. 验证场景
var scene = GD.Load<PackedScene>("res://scenes/enemy.tscn");
if (scene == null)
{
    GD.PrintErr("Scene is null!");
    return;
}

// 2. 检查实例化错误
try
{
    var instance = scene.Instantiate();
    AddChild(instance);
}
catch (Exception e)
{
    GD.PrintErr($"Instantiation failed: {e.Message}");
    GD.PrintErr(e.StackTrace);
}
```

### 10. 循环依赖
```
Detecting cyclic dependency
```

**解决方案：**
```csharp
// ❌ 场景 A 引用 B，B 引用 A

// ✅ 使用延迟加载
private PackedScene? _otherScene;

public override void _Ready()
{
    // 延迟加载打破循环
    CallDeferred(nameof(LoadOtherScene));
}

private void LoadOtherScene()
{
    _otherScene = GD.Load<PackedScene>("res://scenes/other.tscn");
}
```

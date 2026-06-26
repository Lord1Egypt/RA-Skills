# Material 3 迁移完全指南

> 来源：Flutter 中文网 / GitHub cfug/flutter.cn
> URL: https://github.com/cfug/flutter.cn/blob/main/src/content/release/breaking-changes/material-3-migration.md
> 版本：Flutter 3.16+ (2023年11月)
> 抓取时间：2026-04-24

---

## 概述

Flutter 3.16 版本将 Material 3 设为默认主题。Material Design 3 (MD3) 相比 Material 2 做了大量更新，包括新的组件、颜色系统、字体系统、层级系统等。大部分更新是自动无缝完成的，但部分组件需要手动迁移。

**时间线：** Flutter 3.16 稳定版（2023年11月）起，`useMaterial3: true` 成为默认值。

---

## useMaterial3 标志

### 启用/禁用 MD3

```dart
// Flutter 3.16+ 默认 useMaterial3: true
MaterialApp(
  theme: ThemeData(
    useMaterial3: true, // 显式启用 MD3
  ),
)

// 临时回退到 M2（不推荐，仅用于过渡）
MaterialApp(
  theme: ThemeData(
    useMaterial3: false, // 临时回退，过渡期使用
  ),
)
```

**注意：** `useMaterial3` 属性和 Material 2 实现将在未来版本中被移除，详见 [Flutter 弃用政策](https://flutter.cn/release/compatibility-policy#deprecation-policy)。

---

## 颜色迁移

### ColorScheme.fromSeed（推荐方式）

MD3 的核心变化之一：`ColorScheme.fromSeed` 现在是推荐的颜色生成方式。

```dart
// ❌ 旧方式（M2）
theme: ThemeData(
  colorScheme: ColorScheme.light(primary: Colors.blue),
)

// ✅ 新方式（M3）—— 从种子色生成完整配色
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
)
```

### 动态配色（Dynamic Color）

```dart
// 从网络图片动态生成配色
ColorScheme.fromImageProvider(
  provider: NetworkImage('https://example.com/image.jpg'),
  brightness: Brightness.light,
)

// 从种子色 + brightness 手动指定
ColorScheme.fromSeed(
  seedColor: Colors.deepPurple,
  brightness: Brightness.dark,
)
```

### 颜色角色变更（3.22+ 版本）

MD3 新增了基于色调的 surface 颜色角色，替代旧的 opacity 模型：

| 旧名称（M2） | 新名称（MD3） | 说明 |
|------------|-------------|------|
| `ColorScheme.background` | `ColorScheme.surface` | 主背景色 |
| `ColorScheme.onBackground` | `ColorScheme.onSurface` | 背景上的文字色 |
| `ColorScheme.surfaceVariant` | `ColorScheme.surfaceContainerHighest` | 表面变体 |

```dart
// ❌ 旧颜色查找（M2）
final bg = Theme.of(context).colorScheme.background;
final onBg = Theme.of(context).colorScheme.onBackground;
final surfaceVar = Theme.of(context).colorScheme.surfaceVariant;

// ✅ 新颜色查找（MD3）
final surface = Theme.of(context).colorScheme.surface;
final onSurface = Theme.of(context).colorScheme.onSurface;
final surfaceHigh = Theme.of(context).colorScheme.surfaceContainerHighest;
```

### 新的 Surface 颜色角色（3.22+）

MD3 新增 7 个基于色调的 surface 颜色，替代旧的 surfaceTint 叠加模型：

| 角色 | 说明 |
|------|------|
| `surfaceBright` | 最亮的 surface |
| `surfaceDim` | 最暗的 surface |
| `surfaceContainer` | 标准容器色 |
| `surfaceContainerLow` | 低 elevation 容器 |
| `surfaceContainerLowest` | 最低容器色 |
| `surfaceContainerHigh` | 高 elevation 容器 |
| `surfaceContainerHighest` | 最高 elevation 容器 |

### surfaceTint 变更

`surfaceTint` 现在用于表示组件的 elevation。所有组件默认 `surfaceTint: null`。

```dart
// 恢复 M2 行为（不推荐）
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple).copyWith(
    surfaceTint: Colors.transparent,
  ),
  appBarTheme: AppBarTheme(
    elevation: 4.0,
    shadowColor: Theme.of(context).colorScheme.shadow,
  ),
)
```

---

## 字体迁移

### Typography 变化

MD3 更新了 `TextTheme` 的默认值（字号、字重、字间距、行高）。

```dart
// ❌ M2 bodyLarge 在 200pt 约束下显示 2 行
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 200),
  child: Text(
    'This is a very long text that should wrap to multiple lines.',
    style: Theme.of(context).textTheme.bodyLarge,
  ),
)

// ✅ M3 bodyLarge 默认行高更小，同等约束显示 3 行
// 如需恢复旧行为，调整 letterSpacing
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 200),
  child: Text(
    'This is a very long text that should wrap to multiple lines.',
    style: Theme.of(context).textTheme.bodyMedium!.copyWith(
      letterSpacing: 0.0,
    ),
  ),
)
```

---

## 组件迁移

### BottomNavigationBar → NavigationBar

MD3 的 NavigationBar 比 M2 的 BottomNavigationBar 更高，使用胶囊形指示器。

```dart
// ❌ M2 BottomNavigationBar
BottomNavigationBar(
  items: const <BottomNavigationBarItem>[
    BottomNavigationBarItem(
      icon: Icon(Icons.home),
      label: 'Home',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.business),
      label: 'Business',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.school),
      label: 'School',
    ),
  ],
)

// ✅ M3 NavigationBar
NavigationBar(
  destinations: const <Widget>[
    NavigationDestination(
      icon: Icon(Icons.home),
      label: 'Home',
    ),
    NavigationDestination(
      icon: Icon(Icons.business),
      label: 'Business',
    ),
    NavigationDestination(
      icon: Icon(Icons.school),
      label: 'School',
    ),
  ],
)
```

### Drawer → NavigationDrawer

```dart
// ❌ M2 Drawer
Drawer(
  child: ListView(
    children: <Widget>[
      DrawerHeader(
        child: Text('Drawer Header'),
      ),
      ListTile(
        leading: Icon(Icons.message),
        title: Text('Messages'),
        onTap: () { },
      ),
    ],
  ),
)

// ✅ M3 NavigationDrawer
NavigationDrawer(
  children: <Widget>[
    DrawerHeader(
      child: Text('Drawer Header'),
    ),
    const NavigationDrawerDestination(
      icon: Icon(Icons.message),
      label: Text('Messages'),
    ),
  ],
)
```

### ToggleButtons → SegmentedButton

```dart
// ❌ M2 ToggleButtons
enum Weather { cloudy, rainy, sunny }

ToggleButtons(
  isSelected: const [false, true, false],
  onPressed: (int newSelection) { },
  children: const <Widget>[
    Icon(Icons.cloud_outlined),
    Icon(Icons.beach_access_sharp),
    Icon(Icons.brightness_5_sharp),
  ],
)

// ✅ M3 SegmentedButton
enum Weather { cloudy, rainy, sunny }

SegmentedButton<Weather>(
  selected: const <Weather>{Weather.rainy},
  onSelectionChanged: (Set<Weather> newSelection) { },
  segments: const <ButtonSegment<Weather>>[
    ButtonSegment(
      icon: Icon(Icons.cloud_outlined),
      value: Weather.cloudy,
    ),
    ButtonSegment(
      icon: Icon(Icons.beach_access_sharp),
      value: Weather.rainy,
    ),
    ButtonSegment(
      icon: Icon(Icons.brightness_5_sharp),
      value: Weather.sunny,
    ),
  ],
)
```

### AppBar → Medium/Large AppBar

MD3 引入了 Medium 和 Large AppBar，滚动时使用 `surfaceTint` 代替阴影分隔内容。

```dart
CustomScrollView(
  slivers: <Widget>[
    const SliverAppBar.medium(
      title: Text('Title'),
    ),
    SliverToBoxAdapter(
      child: Card(
        child: SizedBox(
          height: 1200,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(8, 100, 8, 100),
            child: Text(
              'Here be scrolling content...',
            ),
          ),
        ),
      ),
    ),
  ],
)
```

### TabBar 新增 secondary 类型

```dart
AppBar(
  title: const Text('Title'),
  bottom: const TabBar(
    tabAlignment: TabAlignment.start,
    isScrollable: true,
    tabs: <Widget>[
      Tab(icon: Icon(Icons.cloud_outlined)),
      Tab(icon: Icon(Icons.beach_access_sharp)),
      Tab(icon: Icon(Icons.brightness_5_sharp)),
    ],
  ),
)
```

### ElevatedButton → FilledButton

```dart
// ❌ M2 ElevatedButton 样式
ElevatedButton(
  onPressed: () {},
  child: const Text('Button'),
)

// ✅ M3 FilledButton（无 elevation 变化和阴影）
FilledButton(
  onPressed: () {},
  child: const Text('Button'),
)

// 或使用 M2 风格手动设置
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: Theme.of(context).colorScheme.primary,
    foregroundColor: Theme.of(context).colorScheme.onPrimary,
  ),
  onPressed: () {},
  child: const Text('Button'),
)
```

---

## 新增组件（MD3 全新华实现）

以下组件在 M2 中不存在，必须使用 MD3 方式：

### MenuBar / MenuAnchor（桌面/Web 菜单）

```dart
// 桌面风格菜单系统
MenuBar(
  children: <Widget>[
    SubmenuButton(
      menuChildren: <Widget>[
        MenuItemButton(
          onPressed: () {},
          child: const Text('New File'),
        ),
      ],
      child: const Text('File'),
    ),
  ],
)
```

### DropdownMenu（组合框）

```dart
DropdownMenu<Entry>(
  initialSelection: Entry.entry1,
  dropdownMenuEntries: listEntries,
  onSelected: (Entry entry) {},
)
```

### SearchBar / SearchAnchor（搜索组件）

```dart
SearchAnchor(
  builder: (context, controller, child) {
    return SearchBar(
      controller: controller,
      hintText: 'Search',
      leading: const Icon(Icons.search),
      onTap: () {},
    );
  },
  suggestionsBuilder: (context, controller) {
    return List.generate(5, (index) {
      return ListTile(
        title: Text('Suggestion $index'),
        onTap: () {},
      );
    });
  },
)
```

### Badge（徽章）

```dart
Badge(
  label: Text('+1'),
  child: Icon(Icons.notifications),
)
```

### FilterChip.elevated / ChoiceChip.elevated / ActionChip.elevated

```dart
// 凸起变体 Chip
FilterChip.elevated(
  selected: isSelected,
  onSelected: (bool selected) {},
  label: Text('Filter'),
)

ChoiceChip.elevated(
  selected: isSelected,
  onSelected: (bool selected) {},
  label: Text('Choice'),
)

ActionChip.elevated(
  onPressed: () {},
  label: Text('Action'),
)
```

### Dialog.fullscreen（全屏对话框）

```dart
Dialog.fullscreen(
  onDismiss: () {},
  child: Scaffold(
    appBar: AppBar(
      title: Text('Title'),
      actions: <Widget>[
        IconButton(
          icon: const Icon(Icons.close),
          onPressed: () {},
        ),
      ],
    ),
    body: Center(
      child: Text('Full screen dialog'),
    ),
  ),
)
```

---

## 按钮 styleFrom 迁移

### TextButton.styleFrom

```dart
// ❌ 旧属性（v3.1 起弃用）
TextButton.styleFrom(
  primary: Colors.red,
  onSurface: Colors.black,
)

// ✅ 新属性（MD3）
TextButton.styleFrom(
  foregroundColor: Colors.red,
  disabledForegroundColor: Colors.black,
)
```

### ElevatedButton.styleFrom

```dart
// ❌ 旧属性
ElevatedButton.styleFrom(
  primary: Colors.red,
  onPrimary: Colors.blue,
  onSurface: Colors.black,
)

// ✅ 新属性
ElevatedButton.styleFrom(
  backgroundColor: Colors.red,
  foregroundColor: Colors.blue,
  disabledForegroundColor: Colors.black,
)
```

### OutlinedButton.styleFrom

```dart
// ❌ 旧属性
OutlinedButton.styleFrom(
  primary: Colors.red,
  onSurface: Colors.black,
)

// ✅ 新属性
OutlinedButton.styleFrom(
  foregroundColor: Colors.red,
  disabledForegroundColor: Colors.black,
)
```

---

## 相关链接

- [Material Design for Flutter](https://flutter.cn/ui/design/material)
- [ThemeData.useMaterial3 API](https://api.flutter.cn/flutter/material/ThemeData/useMaterial3.html)
- [Flutter Material 3 示例](https://github.com/flutter/samples/tree/main/material_3_demo)
- [MD3 umbrella issue](https://github.com/flutter/flutter/issues/91605)

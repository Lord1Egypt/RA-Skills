# MD3 Flutter API 变更速查

> 来源: Flutter Breaking Changes (cfug/flutter.cn)  
> URL: https://github.com/cfug/flutter.cn/tree/main/src/content/release/breaking-changes  
> 更新: 2026-04

本文档汇总 Flutter Material 3 相关的核心 API 变更，按影响范围分组。

---

## 1. Button 体系 (v2.0.0)

### Widget 替换对照

| M2 (已废弃) | MD3 | Theme |
|------------|------|-------|
| `FlatButton` | `TextButton` | `TextButtonTheme` / `TextButtonThemeData` |
| `RaisedButton` | `ElevatedButton` | `ElevatedButtonTheme` / `ElevatedButtonThemeData` |
| `OutlineButton` | `OutlinedButton` | `OutlinedButtonTheme` / `OutlinedButtonThemeData` |
| `ButtonTheme` | — | `ButtonBar` → 各组件独立 theme |

### ButtonStyle API

新按钮使用统一的 `ButtonStyle` 而非分散的参数（`textColor`, `disabledTextColor`, `elevation` 等）：

```dart
// ✅ MD3 方式
TextButton(
  style: TextButton.styleFrom(
    foregroundColor: Colors.blue,
    disabledForegroundColor: Colors.grey,
  ),
  onPressed: () {},
  child: Text('Text'),
)

// ❌ M2 旧方式 (已废弃)
FlatButton(
  textColor: Colors.blue,
  disabledTextColor: Colors.grey,
  onPressed: () {},
  child: Text('Text'),
)
```

### MaterialStateProperty 状态颜色

```dart
ButtonStyle(
  overlayColor: MaterialStateProperty.resolveWith<Color?>((states) {
    if (states.contains(MaterialState.hovered)) return Colors.blue.withOpacity(0.04);
    if (states.contains(MaterialState.focused)) return Colors.blue.withOpacity(0.12);
    if (states.contains(MaterialState.pressed)) return Colors.blue.withOpacity(0.12);
    return null;
  }),
)
```

### 恢复 M2 外观

```dart
final flatStyle = TextButton.styleFrom(
  foregroundColor: Colors.black87,
  minimumSize: Size(88, 36),
  padding: EdgeInsets.symmetric(horizontal: 16),
  shape: BorderRadius.all(Radius.circular(2)),
);
// 适用于 TextButton → FlatButton

final raisedStyle = ElevatedButton.styleFrom(
  foregroundColor: Colors.black87,
  backgroundColor: Colors.grey[300],
  minimumSize: Size(88, 36),
  padding: EdgeInsets.symmetric(horizontal: 16),
  shape: BorderRadius.all(Radius.circular(2)),
);
// 适用于 ElevatedButton → RaisedButton
```

---

## 2. ColorScheme 角色扩展 (v3.22+)

### M2 → MD3 角色对照

| M2 `ColorScheme` | MD3 `ColorScheme` | 说明 |
|-----------------|-------------------|------|
| `primary` | `primary` | 主色（不变） |
| `primaryVariant` | `primaryContainer` / `onPrimaryContainer` | 新增容器色 |
| `secondary` | `secondary` | 不变 |
| — | `secondaryContainer` / `onSecondaryContainer` | 新增 |
| — | `tertiary` / `tertiaryContainer` | 新增 accent 色 |
| `surface` | `surface` | 不变 |
| — | `surfaceContainerHighest` 等层级 | 新的表面层级 |
| `error` | `error` | 不变 |
| — | `errorContainer` / `onErrorContainer` | 新增 |

### ColorScheme.fromSeed 工厂构造

```dart
// ✅ MD3 推荐方式：自动生成 harmonious 配色
ColorScheme.fromSeed(
  seedColor: Color(0xFF6750A4),  // Material Purple
  brightness: Brightness.light, // 或 .dark
)

// 生成完整的 primaryContainer / secondary / tertiary 等角色
```

### DynamicSchemeVariant 动态配色

```dart
// 纯色主题
ColorScheme.fromSeed(seedColor: color, dynamicSchemeVariant: DynamicSchemeVariant.vibrant)

// 柔和主题 (M3 默认)
ColorScheme.fromSeed(seedColor: color, dynamicSchemeVariant: DynamicSchemeVariant.tonal)

// 鲜艳主题
ColorScheme.fromSeed(seedColor: color, dynamicSchemeVariant: DynamicSchemeVariant.fruitSalad)
```

---

## 3. ThemeData 组件主题标准化 (v3.27+)

### `*Theme` → `*ThemeData` 类型变更

```dart
// ❌ 旧类型 (Flutter 3.27 之前)
final CardTheme cardTheme = Theme.of(context).cardTheme;
final DialogTheme dialogTheme = Theme.of(context).dialogTheme;
final TabBarTheme tabBarTheme = Theme.of(context).tabBarTheme;

// ✅ 新类型
final CardThemeData cardTheme = Theme.of(context).cardTheme;
final DialogThemeData dialogTheme = Theme.of(context).dialogTheme;
final TabBarThemeData tabBarTheme = Theme.of(context).tabBarTheme;
```

---

## 4. 导航组件

### BottomNavigationBar → NavigationBar (MD3)

| M2 `BottomNavigationBar` | MD3 `NavigationBar` |
|------------------------|---------------------|
| `type: BottomNavigationBarType.fixed` | 默认 MD3 风格 |
| `type: BottomNavigationBarType.shifting` | 使用 `NavigationDestinationLabelBehavior.alwaysHide` |
| 单一背景色 | 表面容器 + elevation 0 |

```dart
// ✅ MD3 NavigationBar
NavigationBar(
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.home_outlined),
      selectedIcon: Icon(Icons.home),
      label: '首页',
    ),
    NavigationDestination(
      icon: Icon(Icons.search_outlined),
      selectedIcon: Icon(Icons.search),
      label: '搜索',
    ),
  ],
  onDestinationSelected: (index) { },
)

// ❌ M2 BottomNavigationBar (已废弃但仍可用)
BottomNavigationBar(
  items: const [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: '首页'),
    BottomNavigationBarItem(icon: Icon(Icons.search), label: '搜索'),
  ],
  onTap: (index) { },
)
```

### TabBar → MD3 Tabs

```dart
// ✅ MD3 TabBar (配合 TabBarTheme)
TabBar(
  tabs: const [Tab(text: 'Tab1'), Tab(text: 'Tab2')],
  labelColor: Theme.of(context).colorScheme.primary,
  unselectedLabelColor: Theme.of(context).colorScheme.onSurfaceVariant,
)

// ✅ ThemeData.indicatorColor → TabBarThemeData.indicatorColor
MaterialApp(
  theme: ThemeData(
    tabBarTheme: TabBarThemeData(
      indicatorColor: Colors.red,  // 不再使用 ThemeData.indicatorColor
    ),
  ),
)
```

---

## 5. 废弃 API 一览

| 废弃 API | 替代方案 | 版本 |
|---------|---------|------|
| `ThemeData.indicatorColor` | `TabBarThemeData.indicatorColor` | 3.32 |
| `ThemeData.useMaterial3` | 保持使用，MD3 默认开启 | — |
| `ButtonTheme` | `TextButtonTheme` / `ElevatedButtonTheme` 等 | 2.0 |
| `FlatButton` / `RaisedButton` / `OutlineButton` | `TextButton` / `ElevatedButton` / `OutlinedButton` | 2.0 |
| `CardTheme` | `CardThemeData` | 3.27 |
| `DialogTheme` | `DialogThemeData` | 3.27 |
| `TabBarTheme` | `TabBarThemeData` | 3.27 |
| `Chip` 的 `deleteButtonTooltipMessage` | `Chip.deleteButtonTooltipMessage` 已更名 | — |
| `ListTile` 的 `color` / `selectedColor` | `ListTileThemeData` 或直接设置 | — |
| `containerColor` 参数 | 各组件自有的 surface/tint 参数 | — |

---

## 6. Elevation 和表面层级 (v3.22+)

### 新的表面层级 API

```dart
// M2: elevation 数字
Container(color: Colors.white, elevation: 2)

// MD3: 表面层级系统 (无 elevation，只有 tonal 变化)
Container(
  color: Theme.of(context).colorScheme.surfaceContainerHighest,
  // elevation 由系统通过颜色差异隐式表达
)
```

### ElevationToken 更新

```dart
// MD3 elevation token 映射
elevation.level0 → 无阴影，表面颜色
elevation.level1 → 卡片、底部导航
elevation.level2 → 导航抽屉、AppBar (scrolled)
elevation.level3 → 浮动按钮、搜索栏
elevation.level4 → 菜单、FAB (按下)
elevation.level5 → 对话框、模态底部导航
```

---

## 7. Chip 组件变更 (v3.22+)

### Chip deleteButtonTooltip 更名

```dart
// ❌ 旧
Chip(
  deleteButtonTooltipMessage: '删除',
  onDeleted: () {},
)

// ✅ 新
Chip(
  deleteTooltip: '删除',  // 改名
  onDeleted: () {},
)
```

### Chip 语义变更

```dart
// Chip 的 semanticsLabel 行为变更
// MD3 下 Chip 会自动合成可访问性信息
// 显式设置 label 而非仅依赖 child 文本
Chip(
  label: Text('芯片'),
  avatar: CircleAvatar(child: Text('A')),
  labelBehavior: NavigationIndicatorLabelBehavior.onlyShowSelected,
)
```

---

## 8. Material State 系统

### MaterialStateProperty 核心用法

```dart
// 单一状态值
MaterialStateProperty.all<Color>(Colors.blue)

// 动态解析状态
MaterialStateProperty.resolveWith<Color?>((states) {
  if (states.contains(MaterialState.disabled)) return Colors.grey;
  if (states.contains(MaterialState.hovered)) return Colors.blue.shade100;
  if (states.contains(MaterialState.pressed)) return Colors.blue.shade200;
  if (states.contains(MaterialState.focused)) return Colors.blue.shade50;
  return null;
})

// 常用状态标志
MaterialState.disabled
MaterialState.hovered
MaterialState.pressed
MaterialState.focused
MaterialState.selected
MaterialState.dragged
MaterialState.scrolledUnder
```

---

## 9. Dialog / BottomSheet 变更

### Dialog Border Radius (v3.16+)

```dart
// M2: Dialog 默认圆角 4px
// MD3: Dialog 默认圆角 28px (large))

showDialog(
  builder: (context) => Dialog(
    child: Padding(
      padding: EdgeInsets.all(24),
      child: Text('MD3 Dialog'),
    ),
  ),
)

// 自定义圆角
Dialog(
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
)
```

### ScrollableAlertDialog (v3.16+)

```dart
// MD3 AlertDialog 内容超长时可滚动
AlertDialog(
  title: Text('标题'),
  content: SingleChildScrollView(  // 可选，显式滚动
    child: Text('很长的内容...'),
  ),
  actions: [...],
)
```

---

## 10. Snackbar 变更 (v3.19+)

```dart
// snackBarBehavior 默认值变更
// M2: SnackBarBehavior.floating
// MD3: SnackBarBehavior.endFloating (底部留出 FAB 空间)

// action 颜色
Snackbar(
  action: SnackBarAction(
    label: '撤销',
    textColor: Theme.of(context).colorScheme.inversePrimary,
    // M2: SnackBarAction.textColor
  ),
)
```

---

## 版本时间线

| Flutter 版本 | 主要 MD3 变更 |
|------------|-------------|
| 1.20–1.22 | Button 新 API 引入 |
| 2.0 | FlatButton/RaisedButton/OutlineButton 废弃 |
| 3.0 | Material 3 默认关闭 (`useMaterial3: false`) |
| 3.16 | Dialog 圆角 4→28px, ScrollableAlertDialog |
| 3.19 | SnackbarBehavior 变更 |
| 3.22 | ColorScheme 大扩展, DynamicScheme, 新 surface 层级 |
| 3.27 | ComponentTheme 标准化 (*Theme → *ThemeData) |
| 3.30 | `ThemeData.indicatorColor` 废弃 |

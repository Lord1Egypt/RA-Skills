# Material Design 3 组件代码对照速查

> 来源：Google Material Design 3 — Components Reference
> URL: https://m3.material.io/components
> 版本：M3 2024-2025
> 抓取时间：2026-04-23

---
hermes:
  source: https://m3.material.io/
  version: "2024-2025"
  platform: android|flutter|web
  updated: 2026-04-23

## 按钮（Buttons）对照表

| 属性 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **Filled Button** | `Button()` | `FilledButton()` | `.md-button--filled` |
| **Filled Tonal** | `FilledTonalButton()` | `FilledButton.tonal()` | `.md-button--tonal` |
| **Outlined** | `OutlinedButton()` | `OutlinedButton()` | `.md-button--outlined` |
| **Text** | `TextButton()` | `TextButton()` | `.md-button--text` |
| **FAB Standard** | `FloatingActionButton()` | `FloatingActionButton()` | `.md-fab` |
| **FAB Large** | `LargeFloatingActionButton()` | `FloatingActionButton.large()` | `.md-fab--large` |
| **FAB Extended** | `ExtendedFloatingActionButton()` | `FloatingActionButton.extended()` | 自定义 |
| **高度** | `40.dp` | `40.0` | `40px` |
| **最小宽度** | `64.dp` | `64.0` | `64px` |
| **圆角** | `28.dp` | `BorderRadius.circular(28)` | `border-radius: 28px` |
| **图标尺寸** | `24.dp` | `24.0` | `24px` |

### Android Compose 代码

```kotlin
// 标准 Filled Button
Button(
    onClick = { /* */ },
    modifier = Modifier.height(40.dp),
    shape = RoundedCornerCorner(28.dp)
) { Text("按钮文字") }

// FAB Large
LargeFloatingActionButton(
    onClick = { /* */ },
    shape = RoundedCornerCorner(28.dp),
    containerColor = MaterialTheme.colorScheme.primaryContainer,
    contentColor = MaterialTheme.colorScheme.onPrimaryContainer
) {
    Icon(Icons.Filled.Add, contentDescription = "添加")
}

// FAB Extended
ExtendedFloatingActionButton(
    onClick = { /* */ },
    icon = { Icon(Icons.Filled.Add) },
    text = { Text("添加到") },
    containerColor = MaterialTheme.colorScheme.primaryContainer
)

// Icon Button
IconButton(
    onClick = { /* */ },
    modifier = Modifier.size(48.dp) // 触摸目标 48dp
) {
    Icon(Icons.Filled.Settings, contentDescription = "设置")
}
```

### Flutter 代码

```dart
// Filled Button
FilledButton(
  onPressed: () { /* */ },
  style: FilledButton.styleFrom(
    minimumSize: const Size(64, 40),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  ),
  child: const Text('按钮文字'),
)

// FAB Large
FloatingActionButton.large(
  onPressed: () { /* */ },
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  backgroundColor: Theme.of(context).colorScheme.primaryContainer,
  child: const Icon(Icons.add),
)

// FAB Extended
FloatingActionButton.extended(
  onPressed: () { /* */ },
  icon: const Icon(Icons.add),
  label: const Text('添加到'),
)

// Icon Button
IconButton(
  onPressed: () { /* */ },
  icon: const Icon(Icons.settings),
  iconSize: 24,
  // 注意：IconButton 默认触摸目标偏小，建议外套 Container
)
```

---

## 卡片（Cards）对照表

| 属性 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **圆角** | `28.dp` | `BorderRadius.circular(28)` | `border-radius: 28px` |
| **内边距** | `16.dp` | `16.0` | `padding: 16px` |
| **背景** | `colorScheme.surface` | `colorScheme.surface` | `var(--md-sys-color-surface)` |
| **Surface Tint** | `0.05f` | `0.05` | `opacity: 0.05` |
| **边框** | 无（用 Surface Tint） | 无 | 无 |

### Android Compose

```kotlin
// Elevated Card (MD3 推荐)
Card(
    modifier = Modifier.fillMaxWidth().tint(
        MaterialTheme.colorScheme.primary.copy(alpha = 0.05f)
    ),
    shape = RoundedCornerCorner(28.dp),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surface
    ),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("卡片标题", style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.height(8.dp))
        Text("卡片正文内容", style = MaterialTheme.typography.bodyMedium)
    }
}

// 带图片的卡片
Card(
    modifier = Modifier.fillMaxWidth(),
    shape = RoundedCornerCorner(28.dp)
) {
    Column {
        AsyncImage(
            model = "https://example.com/image.jpg",
            contentDescription = "图片描述",
            modifier = Modifier.fillMaxWidth().height(180.dp)
        )
        Column(modifier = Modifier.padding(16.dp)) {
            Text("带图片的卡片", style = MaterialTheme.typography.titleMedium)
        }
    }
}
```

### Flutter

```dart
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  color: Theme.of(context).colorScheme.surface,
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('卡片标题', style: Theme.of(context).typography.titleMedium),
        const SizedBox(height: 8),
        Text('卡片正文内容', style: Theme.of(context).typography.bodyMedium),
      ],
    ),
  ),
)

// 带图片
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  clipBehavior: Clip.antiAlias,
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Image.network(
        'https://example.com/image.jpg',
        width: double.infinity,
        height: 180,
        fit: BoxFit.cover,
      ),
      Padding(
        padding: const EdgeInsets.all(16),
        child: Text('带图片的卡片', style: Theme.of(context).typography.titleMedium),
      ),
    ],
  ),
)
```

---

## 输入组件对照表

| 属性 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **OutlinedTextField** | `OutlinedTextField()` | `TextField(decoration: InputDecoration(border: OutlineInputBorder))` | `<input class="md-text-field">` |
| **SearchBar** | `SearchBar()` | `SearchBar()` | 自定义 |
| **高度** | `56.dp` | `56.0` | `56px` |
| **标签** | `label = { Text(...) }` | `labelText:` | `<label>` |
| **顶部圆角** | `4.dp` | `BorderRadius.vertical(top: Radius.circular(4))` | `border-radius: 4px 4px 0 0` |

### Android Compose

```kotlin
// Outlined TextField（MD3 推荐）
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("邮箱") },
    placeholder = { Text("请输入邮箱地址") },
    leadingIcon = { Icon(Icons.Filled.Email) },
    trailingIcon = {
        if (text.isNotEmpty()) {
            IconButton(Icons.Filled.Clear) { text = "" }
        }
    },
    modifier = Modifier.fillMaxWidth(),
    shape = RoundedCornerCorner(topStart = 4.dp, topEnd = 4.dp),
    colors = OutlinedTextFieldDefaults.colors(
        focusedBorderColor = MaterialTheme.colorScheme.primary,
        unfocusedBorderColor = MaterialTheme.colorScheme.outline,
    )
)

// 多行 TextField
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("备注") },
    modifier = Modifier.fillMaxWidth().height(120.dp),
    maxLines = 5,
    shape = RoundedCornerCorner(4.dp)
)

// SearchBar（MD3 新组件）
SearchBar(
    inputField = {
        SearchBarDefaults.InputField(
            query = query,
            onQueryChange = { query = it },
            onSearch = { /* 执行搜索 */ },
            expanded = false,
            placeholder = { Text("搜索") },
            leading = { Icon(Icons.Search) },
            trailing = {
                if (query.isNotEmpty()) IconButton(Icons.Filled.Clear) { query = "" }
            }
        )
    },
    expanded = false,
    onExpandedChange = { },
    modifier = Modifier.fillMaxWidth()
) { /* 搜索结果列表 */ }
```

### Flutter

```dart
// Outlined TextField
TextField(
  decoration: InputDecoration(
    labelText: '邮箱',
    hintText: '请输入邮箱地址',
    prefixIcon: Icon(Icons.email),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(4)),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(4)),
      borderSide: BorderSide(
        color: Theme.of(context).colorScheme.primary,
        width: 2,
      ),
    ),
  ),
)

// 多行 TextField
TextField(
  decoration: InputDecoration(
    labelText: '备注',
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
  ),
  maxLines: 5,
  minLines: 3,
)

// SearchBar (Material 3)
SearchBar(
  hint: const Text('搜索'),
  leading: const Icon(Icons.search),
  trailing: [
    if (query.isNotEmpty)
      IconButton(
        icon: const Icon(Icons.clear),
        onPressed: () => setState(() => query = ''),
      ),
  ],
  onChanged: (value) => setState(() => query = value),
)
```

---

## 导航组件对照表

| 属性 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **NavigationBar** | `NavigationBar()` | `NavigationBar()` | `.md-bottom-nav` |
| **高度** | `80.dp` | `80.0` | `80px` |
| **图标尺寸** | `24.dp` | `24.0` | `24px` |
| **选中色** | `onSurface` | `onSurfaceVariant` | `var(--md-sys-color-on-surface)` |
| **Indicator** | `surfaceTint 8%` | `tertiaryContainer` | Surface Tint Level 2 |

### Android Compose

```kotlin
NavigationBar(
    modifier = Modifier.height(80.dp),
    containerColor = MaterialTheme.colorScheme.surface,
    tonalElevation = 0.dp
) {
    NavigationBarItem(
        selected = selectedIndex == 0,
        onClick = { selectedIndex = 0 },
        icon = { Icon(if (selectedIndex == 0) Icons.Filled.Home else Icons.Outlined.Home) },
        label = { Text("首页") },
        colors = NavigationBarItemDefaults.colors(
            selectedIconColor = MaterialTheme.colorScheme.onSurface,
            selectedLabelColor = MaterialTheme.colorScheme.onSurface,
            indicatorColor = MaterialTheme.colorScheme.surfaceTint.copy(alpha = 0.08f),
            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
            unselectedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    )
    // 更多 items...
}
```

### Flutter

```dart
NavigationBar(
  height: 80,
  selectedIndex: selectedIndex,
  onDestinationSelected: (index) => setState(() => selectedIndex = index),
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.outlined_home),
      selectedIcon: Icon(Icons.filled_home),
      label: '首页',
    ),
    NavigationDestination(
      icon: Icon(Icons.outlined_search),
      selectedIcon: Icon(Icons.filled_search),
      label: '搜索',
    ),
    NavigationDestination(
      icon: Icon(Icons.outlined_person),
      selectedIcon: Icon(Icons.filled_person),
      label: '我的',
    ),
  ],
)
```

---

## Chips 对照表

| 类型 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **Filter Chip** | `FilterChip()` | `FilterChip()` | `.md-chip--filter` |
| **Assist Chip** | `AssistChip()` | `AssistChip()` | `.md-chip--assist` |
| **Suggestion Chip** | `SuggestionChip()` | `SuggestionChip()` | `.md-chip--suggestion` |
| **圆角** | `8.dp` | `BorderRadius.circular(8)` | `border-radius: 8px` |
| **高度** | `32.dp` | `32.0` | `32px` |

---

## 对话框与底部表单

### Modal Bottom Sheet

| 属性 | Android Compose | Flutter | Web (H5) |
|------|----------------|---------|-----------|
| **顶部圆角** | `28.dp` | `BorderRadius.vertical(top: Radius.circular(28))` | `border-radius: 28px 28px 0 0` |
| **拖动指示器** | `BottomSheetDefaults.DragHandle()` | `自动显示` | 自定义 |

### Android Compose

```kotlin
ModalBottomSheet(
    onDismissRequest = { /* 关闭 */ },
    sheetState = sheetState,
    shape = RoundedCornerCorner(topStart = 28.dp, topEnd = 28.dp),
    containerColor = MaterialTheme.colorScheme.surface,
    dragHandle = { BottomSheetDefaults.DragHandle(color = MaterialTheme.colorScheme.onSurfaceVariant) }
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("标题", style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(16.dp))
        Text("内容...")
    }
}
```

### Flutter

```dart
showModalBottomSheet(
  context: context,
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
  ),
  builder: (context) => Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('标题', style: Theme.of(context).typography.titleLarge),
        const SizedBox(height: 16),
        Text('内容...'),
      ],
    ),
  ),
)
```

---

## 尺寸规范速查表

| 元素 | 尺寸 |
|------|------|
| 最小触摸区域 | 48×48dp/px |
| Filled Button 高度 | 40dp |
| Button 圆角 | 28dp（全圆角） |
| FAB Standard | 56×56dp |
| FAB Large | 96×96dp |
| Card 圆角 | 28dp |
| TextField 高度 | 56dp |
| NavigationBar 高度 | 80dp |
| Bottom Sheet 圆角 | 28dp |
| Chips 圆角 | 8dp |
| Icon 标准尺寸 | 24dp |
| Icon 小尺寸 | 20dp |
| 对比度（正文） | 4.5:1 |
| 对比度（大字） | 3:1 |

---

## 来源

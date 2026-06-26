# Material Design 3 组件规范详解

> 来源：Google Material Design 3 — Components
> URL: https://m3.material.io/components
> 版本：M3 2024-2025
> 抓取时间：2026-04-23

---
hermes:
  source: https://m3.material.io/
  version: "2024-2025"
  platform: android|flutter|web
  updated: 2026-04-23

## 按钮（Buttons）

### 五种按钮类型

| 类型 | 强调级别 | 圆角 | 典型用法 |
|------|---------|------|---------|
| **Filled Button** | 高（Primary） | 28dp（全圆角） | 确定/提交主操作 |
| **Filled Tonal Button** | 中（Secondary） | 28dp | 次要主操作 |
| **Outlined Button** | 低 | 28dp | 辅助确认 |
| **Text Button** | 最低 | 无 | 取消/跳过/链接 |
| **FAB** | 最高 | 16dp（Small）/28dp（Large） | 创建/添加 |

### 尺寸规范

| 属性 | Filled/Outlined | FAB Small | FAB Standard | FAB Large |
|------|----------------|-----------|--------------|-----------|
| 高度 | 40dp | 40dp | 56dp | 96dp |
| 宽度 | min 64dp | 40dp | 56dp | 96dp |
| 圆角 | 28dp | 12dp | 16dp | 28dp |
| Icon Size | 24dp | 24dp | 24dp | 36dp |

### Android Compose 按钮

```kotlin
import androidx.compose.material3.*
import androidx.compose.ui.unit.dp

// Filled Button
Button(
    onClick = { },
    modifier = Modifier.height(40.dp),
    shape = RoundedCornerCorner(28.dp)
) { Text("主要操作") }

// Filled Tonal Button
FilledTonalButton(
    onClick = { },
    modifier = Modifier.height(40.dp),
    shape = RoundedCornerCorner(28.dp)
) { Text("次要操作") }

// Outlined Button
OutlinedButton(
    onClick = { },
    modifier = Modifier.height(40.dp),
    shape = RoundedCornerCorner(28.dp)
) { Text("辅助操作") }

// Text Button
TextButton(onClick = { }) { Text("文字按钮") }

// FAB Large
LargeFloatingActionButton(
    onClick = { },
    shape = RoundedCornerCorner(28.dp),
    containerColor = MaterialTheme.colorScheme.primaryContainer,
    contentColor = MaterialTheme.colorScheme.onPrimaryContainer
) {
    Icon(Icons.Filled.Add, contentDescription = "添加")
}

// Extended FAB
ExtendedFloatingActionButton(
    onClick = { },
    containerColor = MaterialTheme.colorScheme.primaryContainer,
    contentColor = MaterialTheme.colorScheme.onPrimaryContainer
) {
    Icon(Icons.Filled.Add, contentDescription = null)
    Spacer(12.dp)
    Text("添加到")
}
```

### Flutter 按钮

```dart
import 'package:flutter/material.dart';

// Filled Button
FilledButton(
  onPressed: () {},
  style: FilledButton.styleFrom(
    minimumSize: const Size(64, 40),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  ),
  child: const Text('主要操作'),
)

// Filled Tonal Button
FilledButton.tonal(
  onPressed: () {},
  style: FilledButton.styleFrom(
    minimumSize: const Size(64, 40),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  ),
  child: const Text('次要操作'),
)

// Outlined Button
OutlinedButton(
  onPressed: () {},
  style: OutlinedButton.styleFrom(
    minimumSize: const Size(64, 40),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  ),
  child: const Text('辅助操作'),
)

// Text Button
TextButton(onPressed: () {}, child: const Text('文字按钮'))

// FAB Large
FloatingActionButton.large(
  onPressed: () {},
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  child: const Icon(Icons.add),
)

// Extended FAB
FloatingActionButton.extended(
  onPressed: () {},
  icon: const Icon(Icons.add),
  label: const Text('添加到'),
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
)
```

---

## 卡片（Cards）

### 卡片规范

| 属性 | 规范值 |
|------|--------|
| 圆角 | `28dp` |
| 内边距 | `16dp` |
| 容器背景 | `Surface` + Surface Tint Level 1 |
| 无边框 | 层级通过 Surface Tint 区分 |
| Elevation | 0dp（MD3 不再用阴影表示层级） |

### 支持的卡片类型

| 类型 | 用途 | Surface Tint Level |
|------|------|-------------------|
| Elevated Card | 静止状态 | Level 1（5%） |
| Filled Card | 填充背景 | 静态填充色 |
| Outlined Card | 带边框 | 1dp Outline 边框 |

### Android Compose Cards

```kotlin
// Elevated Card（MD3 推荐）
Card(
    modifier = Modifier
        .fillMaxWidth()
        .tint(MaterialTheme.colorScheme.primaryTint.copy(alpha = 0.05f)),
    shape = RoundedCornerCorner(28.dp),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surface
    ),
    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("卡片标题", style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.height(8.dp))
        Text("卡片内容", style = MaterialTheme.typography.bodyMedium)
    }
}

// Filled Card
Card(
    modifier = Modifier.fillMaxWidth(),
    shape = RoundedCornerCorner(28.dp),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surfaceContainerLow
    )
) { /* content */ }

// Outlined Card
Card(
    modifier = Modifier.fillMaxWidth(),
    shape = RoundedCornerCorner(28.dp),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surface
    ),
    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
) { /* content */ }
```

### Flutter Cards

```dart
// Elevated Card
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
        Text('卡片内容', style: Theme.of(context).typography.bodyMedium),
      ],
    ),
  ),
)

// Filled Card
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
  color: Theme.of(context).colorScheme.surfaceContainerLow,
  child: // content
)

// Outlined Card
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(28),
    side: BorderSide(color: Theme.of(context).colorScheme.outline),
  ),
  color: Theme.of(context).colorScheme.surface,
  child: // content
)
```

---

## 输入组件（Text Fields & SearchBar）

### TextField 样式对比

| 样式 | 顶部圆角 | 底部圆角 | 边框 | 用法 |
|------|---------|---------|------|------|
| **Outlined** | 4dp | 4dp | 有 | **MD3 推荐**，表单首选 |
| **Filled** | 0dp | 4dp | 无 | 搜索框、底部表单 |

### Outlined TextField 规范

- 标签：浮动标签（Floating Label）
- 聚焦时：边框变为 Primary 色，厚度 2dp
- 未聚焦：边框为 Outline 色，厚度 1dp
- 错误状态：边框变为 Error 色

### Android Compose TextField

```kotlin
import androidx.compose.material3.*
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation

// Outlined TextField（MD3 推荐）
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("标签文字") },
    placeholder = { Text("提示文字") },
    modifier = Modifier.fillMaxWidth(),
    shape = RoundedCornerCorner(topStart = 4.dp, topEnd = 4.dp, bottomStart = 4.dp, bottomEnd = 4.dp),
    colors = OutlinedTextFieldDefaults.colors(
        focusedBorderColor = MaterialTheme.colorScheme.primary,
        unfocusedBorderColor = MaterialTheme.colorScheme.outline,
        errorBorderColor = MaterialTheme.colorScheme.error,
        focusedLabelColor = MaterialTheme.colorScheme.primary,
    )
)

// 带前导/尾随图标
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("密码") },
    leadingIcon = { Icon(Icons.Filled.Lock, contentDescription = null) },
    trailingIcon = {
        IconButton(onClick = { passwordVisible = !passwordVisible }) {
            Icon(
                if (passwordVisible) Icons.Filled.VisibilityOff else Icons.Filled.Visibility,
                contentDescription = "切换密码可见性"
            )
        }
    },
    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
    modifier = Modifier.fillMaxWidth(),
)

// SearchBar（MD3 新组件）
SearchBar(
    inputField = {
        SearchBarDefaults.InputField(
            query = query,
            onQueryChange = { query = it },
            onSearch = { /* 搜索 */ },
            expanded = false,
            placeholder = { Text("搜索") },
            leading = { Icon(Icons.Search) },
            trailing = {
                if (query.isNotEmpty()) {
                    IconButton(Icons.Filled.Clear) { query = "" }
                }
            }
        )
    },
    expanded = false,
    onExpandedChange = { /* 展开/收起搜索结果 */ },
    modifier = Modifier.fillMaxWidth()
) { /* 搜索结果内容 */ }
```

### Flutter TextField

```dart
// Outlined TextField
TextField(
  decoration: InputDecoration(
    labelText: '标签文字',
    hintText: '提示文字',
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
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(4)),
      borderSide: BorderSide(color: Theme.of(context).colorScheme.outline),
    ),
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(4)),
      borderSide: BorderSide(color: Theme.of(context).colorScheme.error),
    ),
  ),
)

// 带密码可见性切换
TextField(
  obscureText: !passwordVisible,
  decoration: InputDecoration(
    labelText: '密码',
    prefixIcon: Icon(Icons.lock),
    suffixIcon: IconButton(
      icon: Icon(passwordVisible ? Icons.visibility_off : Icons.visibility),
      onPressed: () => setState(() => passwordVisible = !passwordVisible),
    ),
  ),
)
```

---

## 导航组件

### Bottom Navigation

| 属性 | 规范 |
|------|------|
| 高度 | `80dp` |
| 图标尺寸 | `24dp` |
| 标签 | 始终显示（MD3 vs MD2 关键区别） |
| 选中图标色 | `On Surface` |
| 选中标签色 | `On Surface` |
| 选中态背景 | Surface Tint Level 2（8%） |

### Android Compose NavigationBar

```kotlin
NavigationBar(
    modifier = Modifier.height(80.dp),
    containerColor = MaterialTheme.colorScheme.surface,
    tonalElevation = 0.dp
) {
    items.forEachIndexed { index, item ->
        NavigationBarItem(
            selected = selectedIndex == index,
            onClick = { selectedIndex = index },
            icon = {
                Icon(
                    if (selectedIndex == index) item.selectedIcon else item.unselectedIcon,
                    contentDescription = item.label
                )
            },
            label = { Text(item.label) },
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = MaterialTheme.colorScheme.onSurface,
                selectedLabelColor = MaterialTheme.colorScheme.onSurface,
                indicatorColor = MaterialTheme.colorScheme.surfaceTint.copy(alpha = 0.08f),
                unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                unselectedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        )
    }
}
```

### Flutter NavigationBar

```dart
NavigationBar(
  height: 80,
  selectedIndex: selectedIndex,
  onDestinationSelected: (index) => setState(() => selectedIndex = index),
  destinations: [
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

### Navigation Drawer

| 属性 | 规范 |
|------|------|
| 宽度 | `360dp` |
| 圆角（右侧） | `28dp`（与屏幕右边缘对齐） |
| 背景色 | `SurfaceContainerLow` |
| 头部高度 | `160dp` |

### Navigation Rail（导航导轨）

| 属性 | 规范 |
|------|------|
| 宽度 | `80dp` |
| 图标尺寸 | `24dp` |
| 标签 | 始终显示 |
| 适用场景 | 平板电脑横屏、桌面端 |

---

## Chips（ Chips 组件）

### Chip 类型

| 类型 | 背景色 | 边框 | 用法 |
|------|--------|------|------|
| **Filter Chip** | Surface Tint / Primary Container | 无（选中时） | 多选过滤 |
| **Input Chip** | Surface | 有（Outline） | 输入标签（联系人选择） |
| **Assist Chip** | Surface | 无 | 辅助操作（"发送邮件"） |
| **Suggestion Chip** | Surface | 无 | 建议文本 |

### 圆角规范

| 组件 | 圆角 |
|------|------|
| Chips | `8dp` |
| Filled Button / Outlined Button | `28dp` |
| Cards | `28dp` |
| FAB | `16dp`（Small）/ `28dp`（Large） |
| TextField | `4dp`（顶部）/ `0dp`（底部） |

---

## 对话框与模态（Dialogs & Modal）

### Modal Bottom Sheet

| 属性 | 规范 |
|------|------|
| 圆角（顶部） | `28dp` |
| 拖动指示器 | 宽 32dp × 高 4dp，圆角 2dp |
| 最大高度 | 屏幕高度 50% |

### Android Compose ModalBottomSheet

```kotlin
ModalBottomSheet(
    onDismissRequest = { /* 关闭 */ },
    sheetState = sheetState,
    shape = RoundedCornerCorner(topStart = 28.dp, topEnd = 28.dp),
    containerColor = MaterialTheme.colorScheme.surface,
    dragHandle = { BottomSheetDefaults.DragHandle(color = MaterialTheme.colorScheme.onSurfaceVariant) }
) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("标题")
        Spacer(Modifier.height(16.dp))
        // 内容
    }
}
```

---

## 来源

# Flutter 布局约束权威指南

Flutter 布局核心规则：**上层 widget 向下传递约束 → 下层 widget 向上传递大小 → 父级决定子级位置**。理解这条规则，才能理解为什么 `width: 100` 不一定是 100 像素宽。

## 约束模型

约束（Constraints）是 4 个浮点数的集合：最小/最大宽度、最小/最大高度。

布局流程：

```
Parent → 向下传递约束 (minWidth~maxWidth, minHeight~maxHeight)
  ↓
Widget 遍历 children，向每个 child 传递各自的约束
  ↓
Child 决定自己想要的尺寸（向上回报）
  ↓
Widget 确定自身大小（受原始约束限制）
  ↓
Widget 告诉 Parent 自己的大小
  ↓
Parent 决定每个 child 的位置（x/y 坐标）
```

**约束下行，尺寸上行，位置由父级决定。**

## 核心原则

### 1. Widget 无法自定大小，只能在父级约束内决定

```dart
// 这样写：widget 不知道自己会被约束成什么尺寸
Container(width: 100) // 在无限宽的 parent 里，这可能无效

// Flutter 布局不是"我要多大"，而是"我在给我的约束里能多大"
```

### 2. 位置由父级决定，Widget 自身无法知晓

Widget 的 `x/y` 坐标由其 parent 决定，不是自身决定的。

### 3. 整棵树决定单个 Widget 的最终尺寸

Widget 的 size 取决于它的 parent，而 parent 的 size 又取决于 grandparent。脱离整棵树无法精确定义任何 Widget 的最终尺寸。

### 4. 对齐要明确

如果 child 想要的尺寸和 parent 能给的不一致，且 parent 没有足够信息对齐，则 child's size 可能被忽略。**定义对齐时要明确指定。**

## 常见困境

### `width: 100` 不生效

```dart
// 错误：width: 100 在这个 context 可能无效
Container(width: 100, child: Text('hello'))

// 如果 parent 约束是 50~∞，这个 Container 就会被拉伸或收缩
// 正确理解：在 Center 之外，Container 会尝试用 100，但受 parent 约束限制
```

### `FittedBox` 不起作用

`FittedBox` 只在 parent 给了固定约束时才能正确 fit。如果 parent 本身是 unconstrained，`FittedBox` 的 fit 就无从谈起。

### `Column` 溢出

`Column` 的 children 如果在垂直方向上超出了 `Column` 自身的约束，就会溢出。解决方案通常是包裹在 `Expanded` 或 `Flexible` 中，或调整 parent 的约束。

### `IntrinsicWidth` / `IntrinsicHeight`

当需要一个 widget "按内容自适应"但 parent 给了硬约束时，`IntrinsicWidth` 可以让 child 先按自己内容决定理想宽度，再把约束传递给 child。但性能开销大，应避免在频繁重建的列表中使用。

## LayoutBuilder 与 Constraints

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return Row(children: [...]);
    } else {
      return Column(children: [...]);
    }
  },
)
```

`LayoutBuilder` 让你在 build 时实时获取 parent 传下来的约束，是响应式布局的关键工具。

## 调试技巧

```dart
// 1. 用 Widget Inspector 可视化约束传递
// 2. 加一个 ColoredBox 看实际占位
Container(color: Colors.red) // 看实际渲染大小

// 3. 常见溢出：太长的 Text 在有限宽度的 Column cell 里
// 解决：Expanded / Flexible 包裹，或 maxLines 限制
```

## 来源

[Understanding constraints - Flutter](https://flutter.cn/ui/layout/constraints) (CC BY 4.0)

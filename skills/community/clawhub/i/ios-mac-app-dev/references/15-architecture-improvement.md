# Swift 架构改进工作流

> 基于 matt pocock `improve-codebase-architecture` 改写，适配 Swift/SwiftUI 代码库。

## 使用时机

- 代码库变得难以导航或测试
- 用户说「架构改进」、「重构一下」、「这个模块太复杂了」
- 作为 Bug 诊断（阶段 6）的后续行动

## 核心理念

**浅模块问题**：接口几乎和实现对等复杂——「浅模块」。

**深模块目标**：大量实现隐藏在小型接口后面。

**删除测试**：如果把一个模块删了，复杂度是集中了还是只是移动了？「集中了」才是你想要的信号。

## 流程

---

### 1. 探索代码库

先读项目的领域术语表（`CONTEXT.md`）和相关区域的 ADR。

然后用探索子代理有机地走查代码库，注意你遇到摩擦的地方：

- 理解一个概念需要在多个小模块间跳来跳去？
- 哪些模块是**浅的**——接口和实现对等复杂？
- 纯函数是否仅为可测试性而提取，但真实 bug 藏在它们被调用的方式里（没有**局部性**）？
- 紧耦合的模块是否跨接缝泄漏？
- 代码库的哪些部分未测试，或通过当前接口难以测试？

对每个怀疑是浅模块的，应用**删除测试**：删了它会集中复杂度，还是只是移动它？「集中了」才是你想要的信号。

---

### 2. 生成为 HTML 报告

把自包含 HTML 文件写到 OS 临时目录，不碰 repo 里的东西。

临时目录从 `$TMPDIR` 解析，回退到 `/tmp`，写到 `<tmpdir>/architecture-review-<timestamp>.html`，这样每次运行得到新文件。

报告使用 **Tailwind via CDN** 做布局和样式，需要时用 **Mermaid via CDN** 画图表。

每个候选改进项渲染为一张卡片：

```
┌─────────────────────────────────────────────┐
│  Files: NoteViewModel.swift, NoteList.swift │
│  Problem: 浅模块 —— 接口暴露太多状态      │
│  Solution: 把编辑状态封装到 NoteEditor     │
│  Benefits: 更容易测试，减少状态同步 bug    │
│  [Before]  [After]  图表                  │
│  推荐强度: Strong / Worth exploring / ...    │
└─────────────────────────────────────────────┘
```

报告末尾加**首选推荐**部分：你会先处理哪个候选，为什么。

**用词规范**：
- 用 `CONTEXT.md` 词汇表来称呼领域概念
- 用架构词汇：module、interface、depth、seam、adapter、leverage、locality
- 不要用「component」、「service」、「API」、「boundary」等词

---

### 3. 烤问循环

用户选了一个候选后，运行需求澄清对话来走设计树：
- 约束是什么？
- 依赖是什么？
- 深化后的模块形状是什么？
- 接缝后面是什么？
- 哪些测试能存活下来？

决策明确时，副作用即时发生：
- 用 `references/10-requirements-analysis.md` 的需求澄清工作流
- 如在 `CONTEXT.md` 中没有的概念来命名深化模块？加到 `CONTEXT.md`
- 如在对话中 sharpen 了一个模糊术语？更新 `CONTEXT.md`
- 如用户以有分量的理由拒绝了候选？提供写 ADR 的选项

---

## Swift 代码库特定指引

### 浅模块的常见 Swift 模式

```swift
// ❌ 浅模块：状态暴露在接口中
class NoteListViewModel {
    var notes: [Note] = []
    var isLoading: Bool = false
    var errorMessage: String? = nil
    var searchText: String = ""
    // 接口几乎和实现对等复杂
}

// ✅ 深模块：状态封装在接口后面
@Observable
class NoteListViewModel {
    private(set) var state: NoteListState = .loading
    
    func loadNotes() async { ... }
    func search(_ text: String) async { ... }
    // 接口小，实现深
}
```

### 好的接缝设计

```
网络层接缝：
APIClientProtocol（小接口）
    ↑ 可 mock  for testing

存储层接缝：
NoteRepositoryProtocol（小接口）
    ↑ 可用 SwiftData/InMemory 双实现
```

### SwiftUI 特定考量

- `View` 是浅的——它们是声明式的，不该有复杂状态
- 状态应上升到 `@Observable` 的 ViewModel 或 `@Environment` 对象
- `ViewModifier` 可以是深模块——封装复杂布局行为 behind 简单接口

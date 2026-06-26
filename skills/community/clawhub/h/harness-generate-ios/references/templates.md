# 输出文件模板

## 目录

1. [CLAUDE.md](#claudemd)
2. [docs/ARCHITECTURE.md](#docsarchitecturemd)
3. [docs/PITFALLS.md](#docspitfallsmd)
4. [docs/STYLE.md](#docsstylemd)
5. [docs/QUALITY.md](#docsqualitymd)
6. [docs/SCRIPTS.md](#docsscriptsmd)
7. [README 速查卡](#readme-速查卡)
8. [Rule 文件](#rule-文件)

---

## CLAUDE.md

**约束**: < 80 行。索引入口，不是百科全书——只放指针和硬约束。

```markdown
# Project: {项目名}

## Quick Reference
- **Platform**: {iOS 版本}
- **Language**: {Swift 5.x / Objective-C}
- **UI Framework**: {UIKit / SwiftUI / 混合}
- **Architecture**: {MVVM / MVP / ...}，详见 `docs/ARCHITECTURE.md`
- **DI**: {Factory / Swinject / 无}
- **Package Manager**: {CocoaPods / SPM / 混合}
- **Workspace**: `{workspace 文件名}`
- **Targets**: {target 列表及区分方式}

## 任务路由
> 根据当前任务，查阅对应文档。不要一次全部加载。多条可同时命中。

### 改代码前
- [ ] 查阅 [docs/PITFALLS.md](docs/PITFALLS.md) 避免已知错误

### 涉及 UI
- [ ] 查阅 [{UI 库名} README]({路径})
- [ ] 查阅对应组件子目录 README

### 涉及跨模块
- [ ] 查阅 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

### 不确定规范
- [ ] 查阅 [docs/STYLE.md](docs/STYLE.md)

### 提交前
- [ ] 对照 [docs/QUALITY.md](docs/QUALITY.md)

### 运行脚本
- [ ] 查阅 [docs/SCRIPTS.md](docs/SCRIPTS.md)

## Key Rules (Always Enforced)
- {每条一行，从 SwiftLint error 级 + 代码扫描硬约束提取}

## Build & Compile

**命令行编译**（无需签名）:
```​bash
xcodebuild -workspace "{workspace}" -scheme "{scheme}" -configuration Debug -destination 'generic/platform=iOS' build 2>&1 | tail -5
```​

**何时编译**: 修改 public API、修改 2+ 文件、跨模块改动、删除/重命名类型。

## Verification Loop
> 每次修改代码后，按以下顺序验证。任何一步失败必须先修复再继续。

1. **编译**：修改 2+ 文件或跨模块改动时编译
2. **Lint**：确认 SwiftLint 无新增 error
3. **自检**：对照 docs/QUALITY.md 逐项检查
4. **犯错记录**：新类型错误追加到 docs/PITFALLS.md
```

---

## docs/ARCHITECTURE.md

```markdown
<!-- AUTO-GENERATED, review and edit -->
# Architecture

## 分层结构
{从目录结构推断：展示层/业务层/数据层/基础设施层}

## 模块依赖图
```​
{从 import 语句推断的 ASCII 依赖图}
A → B → C
      → D
```​

## 模块职责
| 模块 | 职责 | 关键类 |
|------|------|--------|
| {模块名} | {一句话} | {1-2 个核心类} |

## 跨模块通信方式
- {NotificationCenter / Delegate / Closure / Combine}
```

---

## docs/PITFALLS.md

```markdown
<!-- AUTO-GENERATED, review and edit -->
# Known Pitfalls

> 踩过的坑，避免重复犯错。按类别组织。

## Force Unwrap / Force Cast
{扫描到的 force unwrap/cast 热点文件}

## SwiftLint 例外
{从 swiftlint:disable 注释提取}

## 线程安全
- {从代码扫描推断的常见线程问题}

## 内存管理
- {closure 循环引用高风险区域}

## 常见 iOS 坑位
- 键盘遮挡输入框
- Safe area 适配
- 深浅色模式资源缺失
- 后台任务超时
```

---

## docs/STYLE.md

```markdown
<!-- AUTO-GENERATED, review and edit -->
# Style Guide

## 命名规范
- **文件名**: {检测到的模式，如 XXXxxViewController.swift}
- **类名前缀**: {检测到的前缀，如 XX / YY}
- **ViewController**: {命名模式}
- **ViewModel**: {命名模式}

## 文件组织
- {按功能模块 vs 按类型}
- {目录结构示例}

## 本地化
- 方式: {检测到的方式，如 "key".mm.localized}
- 禁止硬编码用户可见文案

## 代码风格
- 遵循 .swiftlint.yml 配置
- {项目特有的风格约定}
```

---

## docs/QUALITY.md

```markdown
<!-- AUTO-GENERATED, review and edit -->
# 提交前检查清单

## 必查项
- [ ] 无 force unwrap（`!`）和 force cast（`as!`）
- [ ] 无硬编码用户可见文案
- [ ] 无主线程网络请求
- [ ] 无敏感信息提交（API key、密码）
- [ ] 无废弃 API 使用
- [ ] Codable 枚举使用了 @DefaultValue
- [ ] delegate / closure 用了 weak

## UI 相关
- [ ] 支持深色模式
- [ ] 适配 Safe Area
- [ ] 使用语义化 design token（颜色/字体）
- [ ] 文案走本地化

## 编译
- [ ] 修改 public API → 编译通过
- [ ] 修改 #if TARGET_A/#if TARGET_B → 两个 scheme 都编译
- [ ] SwiftLint 无新增 error
```

---

## docs/SCRIPTS.md

```markdown
<!-- AUTO-GENERATED, review and edit -->
# Scripts

| 脚本 | 用途 | 用法 |
|------|------|------|
| {文件名} | {从注释/文件名推断} | `{运行命令}` |
```

---

## README 速查卡

**约束**: 20–40 行。必须包含 API 索引表。

```markdown
# {模块名}

{一句话描述用途}

## API 索引
| 类/协议 | 职责 |
|---------|------|
| {类名} | {一句话职责} |

## 约束
- {调用顺序、线程要求等关键约束}

## 反模式
- ❌ {错误做法} — {为什么错}
```

**收录规则**:
- API 索引只列 public/open 类型
- 约束只列会导致 crash 或 bug 的硬约束
- 反模式只列真实踩过或极易犯的错误
- 如果模块简单到没有约束和反模式，对应 section 可省略

---

## Rule 文件

**约束**: < 15 行。祈使句。放在 `.claude/rules/` 下。

```markdown
---
paths:
  - "{glob pattern matching the module}"
---

# {模块名} 规则

- 必须 {具体约束}
- 禁止 {具体禁令}
- 先 X 再 Y（调用顺序）
```

**生成条件**（满足**任一**即生成）:
1. 有调用顺序约束（如：必须先 configure 再 start）
2. 有线程约束（如：UI 方法必须在主线程调用）
3. 有容易误用的 API（如：参数含义不直观）
4. 有 design token 约束（如：颜色必须用语义化 token）
5. 有编译宏差异（如：#if TARGET_A 和 #if TARGET_B 行为不同）

**全部不满足 → 不生成 rule 文件。**

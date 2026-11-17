---
name: harmonyos-code-workshop
version: 6.1.0
description: "HarmonyOS 7 (API 26) 全流程编码助手，精通ArkTS+ArkUI，提供高质量原生鸿蒙代码"
trigger:
  - 鸿蒙
  - HarmonyOS
  - ArkTS
  - ArkUI
  - 鸿蒙代码
  - 鸿蒙开发
  - 鸿蒙7
  - harmonyos code
  - arkts
  - 鸿蒙项目
  - 鸿蒙应用
  - 鸿蒙原生
  - 分布式
  - 元服务
  - atomic service
  -  Stage模型
  - 鸿蒙技能
  - 鸿蒙专家
  - HarmonyOS NEXT
  - 鸿蒙NEXT
  - DeveEco
  - 鸿蒙学习
  - 我想开发一个鸿蒙
  - 帮我写一个鸿蒙
agent_created: true
---

> 📌 **版本信息**：本Skill基于 HarmonyOS 7 (API 26 Beta1) 编写，适用 DevEco Studio 26.0.0 Beta1。

**快速开始**：直接描述你的鸿蒙开发需求，我会自动加载本Skill并生成高质量ArkTS代码。
- 触发词示例：`鸿蒙`、`HarmonyOS`、`ArkTS`、`帮我写一个鸿蒙应用`
- 本Skill包含：废弃API自动检测、编译自检清单、76个Kit速查、Stage模型详解、API 26新能力


> 📌 **版本信息**：本专家包基于 HarmonyOS 7 (API 26 Beta1) 编写，适用 DevEco Studio 26.0.0 Beta1。
> 若使用其他版本，请注意 API 差异。

# 📚 HarmonyOS Code Workshop 专家包

## 📋 目录（TOC）

1. [第一部分：核心机制（自我进化、工作流、输出规范、自检）](#part1)
2. [第二部分：ArkTS 编码规范（语法、命名、格式、迁移指南）](#part2)
3. [第三部分：架构与状态管理（MVVM、V2装饰器、模板库、事件总线）](#part3)
4. [第四部分：性能优化（TaskPool、组件复用、流畅刷新、启动框架）](#part4)
5. [第五部分：动画与手势（动画系统、手势、转场）](#part5)
6. [第六部分：测试与调试（测试体系、DevEco、HDC、应用生命周期）](#part6)
7. [第七部分：安全与合规（权限、隐私、加密、认证、业务风险检测）](#part7)
8. [第八部分：多设备适配（折叠屏、分布式流转、设备协同）](#part8)
9. [第九部分：Kit 能力速查（76个Kit分类、工具类、NFC、音频）](#part9)
10. [第十部分：Sample 项目解析（按领域分类）](#part10)
11. [第十一部分：编译错误与踩坑（错误速查、级联诊断、踩坑记录）](#part11)
12. [第十二部分：拓展资源（官方Sample、语言基础类库、路由框架）](#part12)
13. [第十三部分：布局与自适应（ArkUI自适应布局模式）](#part13)

---



# 第一部分：核心机制（自我进化、工作流、输出规范、自检）

## 核心能力

1. **ArkTS 语言专家**：精通 ArkTS 语法规范、类型系统、严格空安全机制，熟悉从 TypeScript 到 ArkTS 的迁移规则（禁止 any/unknown、禁止解构赋值、禁止函数表达式、禁止运行时改变对象布局等）
2. **ArkUI 声明式 UI**：熟练掌握 @Component、@State、@Prop、@Link、@Builder、@Extend 等装饰器，精通声明式 UI 状态管理机制和组件化开发模式
3. **鸿蒙元服务开发**：熟悉元服务（Atomic Service）开发流程，掌握 Stage 模型应用开发、Ability 生命周期管理、跨设备流转等关键技术
4. **高级架构与性能优化**：精通 MVVM/Repository 等 ArkTS 架构模式，掌握 LazyForEach 长列表优化、内存泄漏排查、ANR 避免策略、多设备复杂适配（折叠屏/平板/2in1）、分布式流转等高级场景

## 🧬 自我进化机制（五大能力）

> ⚡ 本专家持续进化中，以下四条机制在每次对话中自动运行。

### 1. 废弃API自动提醒
**触发时机**：用户提供代码或描述现有代码逻辑时，自动扫描其中是否包含废弃 API。

**扫描规则**（对照 `## ⚠️ 关键废弃 API 迁移对照表` 章节）：
- 扫描用户代码中是否出现旧版 API 调用（如 `router.pushUrl`、`animateTo()`、`console.log` 等）
- 自动比对 `⬆️ 废弃 API 迁移对照表（51+ 组）`，逐行检测
- 若发现废弃 API，在回复中标记并推荐现代替代方案
- 格式：`⚠️ [废弃API检测] 第X行使用了 {旧API} → 建议替换为 {新API}`

**扫描重点清单**：
| 检测项 | 旧API | ✅ 现代替代 | 严重程度 |
|--------|-------|-----------|:-------:|
| 路由 | `router.pushUrl()` / `router.back()` | `UIContext.getRouter()` 或 Navigation | 🔴 高 |
| 动画 | 全局 `animateTo()` | `this.getUIContext().animateTo()` | 🔴 高 |
| 提示 | `promptAction.showToast()` 全局调用 | `this.getUIContext().getPromptAction().showToast()` | 🟡 中 |
| 日志 | `console.log` / `console.info` | `@ohos.hilog` | 🟡 中 |
| 文件 | `@ohos.fileio` | `@ohos.file.fs` (`CoreFileKit`) | 🔴 高 |
| 通知 | `@ohos.notification` | `@ohos.notificationManager` | 🟡 中 |
| 相机 | 旧 `camera.Camera` | `CameraManager + Session` | 🔴 高 |
| 上下文 | 全局 `getContext(this)` | `this.getUIContext().getHostContext()` | 🟡 中 |
| 窗口 | `window.getTopWindow()` 回调 | `windowStage.getMainWindow()` Promise | 🟡 中 |
| 全局状态 | `globalThis` | `UIContext` / `AppStorage` / `LocalStorage` | 🔴 高 |

### 2. 代码质量自检
**触发时机**：每次输出代码**之前**，强制运行完整的编译自检清单。

**执行流程**：
```
发现用户需要代码 → 编写代码 → 逐项对照「编译自检清单」检查
→ 发现错误 → 立即修正 → 再次检查 → 确认全部通过 → 输出
```
**自检范围**（共 4 大类 31+ 项，详见 `## ✅ 编译自检清单`）：
- ✅ 语法自检（6项：无 var、无 any、无解构、无函数表达式、无嵌套函数、无 @ts-ignore）
- ✅ API 自检（7项：UIContext、Navigation、file.fs、notificationManager、hilog、CameraManager、util）
- ✅ 组件自检（6项：@Entry 唯一、LazyForEach、StorageLink 默认值、对象字面量接口、Navigation、IDataSource）
- ✅ API 与泛型自检（6项：泛型显式标注、无 any/unknown、显式返回类型、无内联对象字面量、Record 规范、API 返回类型接口化）
- ✅ 性能自检（6项：循环常量提取、无稀疏数组、无联合类型数组、数值安全、可选参数→默认参数、catch 无类型注解）

**输出格式**：在代码输出末尾追加自检结果徽标
```
// ✅ 代码质量自检通过 | 语法6/6 | API7/7 | 组件6/6 | 泛型6/6 | 性能6/6
```

**发现无法修复的问题时**：
- 立即告知用户具体是什么问题、影响的代码段
- 提供备选方案或回退策略
- 绝不交出"可能编译不过"的代码

### 3. 版本兼容性标注
**触发时机**：输出代码示例或完整组件时，自动标注目标 API 版本。

**标注规则**：
| API版本 | 标签 | 适用特性 |
|---------|:----:|---------|
| API 23+ | `[API 23+]` | 多数通用组件、基础 API、主流兼容（覆盖 94%+ 设备） |
| API 24+ | `[API 24+]` | 6.1.1 新增能力 |
| API 26+ | `[API 26+]` | Vibe Coding、沉浸光感、3DGS、空格音频等最新特性 |
| API 22+ | `[API 22+]` | 最低兼容目标（覆盖 99%+ 设备） |

**格式要求**：
- 每个代码块第一行注释标注版本信息：`// [API 23+] 网络请求封装`
- 如果代码中包含版本特定的 API，在对应行以注释标注：`// API 26+`
- 如果用户未指定目标版本，默认标注 API 23+（主流覆盖）
- 用户指定后，按用户版本标注

### 4. 被动→主动：知识推送
**触发时机**：用户未提出新问题或代码需求时（等待/查阅状态），主动推送鸿蒙开发知识。

**推送规则**：
- 每次对话中最多推送 1 条（避免打扰）
- 从以下 5 个领域轮流选取：

| 领域 | 示例话题 | 来源章节 |
|------|---------|---------|
| 🏗️ 架构 | Navigation vs Router 迁移策略、MVVM / Repository 最佳实践 | `API 版本演进` / `ArkTS 架构模式` |
| 🐛 避坑 | 编译错误 #3 AppStorage、#6 对象字面量、内存泄漏排查三步法 | `常见编译错误速查` / `真实踩坑记录` |
| ⚡ 性能 | LazyForEach 的 IDataSource 实现、闭包优化、首屏加载优化策略 | `高性能编程实践` / `性能优化清单` |
| 🆕 新特性 | Vibe Coding、沉浸光感、碰一碰精准分享（API 26+） | `API 版本演进` |
| 🎯 技巧 | @Extend 扩展组件、@Builder 复用 UI、MVVM 快速脚手架 | `自定义组件与扩展` / `高级架构模式` |

**推送格式**：
```
💡 [鸿蒙知识卡片] 你知道吗？
{具体知识点：一句话精华 + 代码片段（可选）+ 来源章节}
```

**推送时机**：
- 当用户回复仅包含"好的"、"可以"、"继续"等简短确认时
- 当对话间隔超过 30 秒未收到新输入时（按实际对话节奏判断）
- 当用户完成一个大型代码任务后，主动送一条相关技巧

### 5. 高级场景深度支持
**触发时机**：用户提出复杂的架构设计、性能调优、多端适配等高级场景需求时。

**应对策略**：
- **架构设计**：根据需求复杂度和团队规模推荐 MVVM / Repository / 事件总线等架构模式，并提供对应的 ArkTS 实现脚手架
- **性能调优**：按「性能问题归类→工具定位→方案对比→代码实施」四步法，综合 DevEco Profiler 建议与 ArkUI 渲染原理给出方案
- **多端适配**：根据设备形态（折叠屏/平板/2in1/车机）推荐对应的断点策略和布局方案，结合 BreakpointType 与 window.on('foldStatusChange') 双重保障
- **分布式流转**：评估跨设备数据同步/文件分享/碰一碰等方案的技术可行性、版本兼容性和隐私合规风险，给出选型建议

**参考来源**：`references/api26-new-capabilities.md` 中的高级架构模式、性能优化速查、多设备适配章节

## 工作流程

1. **理解需求**：分析用户的应用场景和技术需求，确定使用的鸿蒙 API 版本和能力范围；**评估需求复杂度**，判断属于基础编码、架构设计、性能调优还是上架发行
2. **架构设计**：基于 Stage 模型设计应用架构，合理划分 UI 层、数据层和业务逻辑层；中大型 App 推荐 MVVM + Repository 模式，跨组件通信用 AppStorage 或 emitter 替代 EventBus
3. **代码编写**：严格按照 ArkTS 编程规范编写代码，遵循命名规范（UpperCamelCase 类名、lowerCamelCase 变量/方法名）、缩进规则（2空格、禁用Tab）、单引号等规范
4. **状态管理**：合理运用 @State（组件内部状态）、@Prop（父传子）、@Link（双向绑定）、@Provide/@Consume（跨层级传递）等装饰器；API 26+ 推荐 @ComponentV2 + @Local + @Param + @Event 体系
5. **代码质量自检**：输出代码前强制运行「编译自检清单」（31+项），逐项检查语法、API、组件和泛型规范
6. **性能优化**：遵循 ArkTS 高性能编程实践，避免不必要的跨语言调用，合理使用 LazyForEach 实现懒加载，优化列表性能；遇到复杂性能瓶颈时按「归类→定位→方案→实施」四步法处理
7. **多设备适配**：根据设备类型（手机/折叠屏/平板/2in1/车机）推荐断点策略和布局方案；涉及分布式能力时评估版本兼容性和隐私合规
8. **上架护航**：用户要发布时，按 AGC 审核 Checklist 逐项检查备案、隐私、权限、签名、截图等

## 输出规范

- 代码必须严格遵循 **华为官方 ArkTS 编码规范**（命名、格式、编程实践）
- 所有代码使用 **ArkTS 语法**，不使用 JavaScript 或 TypeScript 语法糖（禁止 `var`、禁止 `any`/`unknown`、禁止解构赋值、禁止函数表达式、禁止运行时添加/删除对象属性）
- 每个代码块首行注释标注 **目标 API 版本**：`// [API 23+] 功能说明`
- 代码含完整的中文注释说明关键逻辑
- 提供必要的 import 声明和类型定义
- 对 ArkUI 组件使用声明式链式属性配置（`.width()` `.height()` `.backgroundColor()` 等）
- 在代码输出末尾追加 **自检结果徽标**：`// ✅ 代码质量自检通过 | 语法6/6 | API7/7 | 组件6/6 | 泛型6/6 | 性能6/6`
- 首次对话时确认用户目标 API 版本（默认 API 23+）

## 🔄 持续学习机制（铁律）

**每次对话结束后，必须执行以下自检流程：**

### 0. 主动知识推送（passive → proactive）
在每次对话的空闲间隙，判断是否需要推送一条鸿蒙知识卡片：
- **条件**：用户回复仅包含简短确认（"好的"、"继续"、"可以"等）或完成一个大型代码任务后
- **动作**：从「被动→主动」轮播池中选取一条推送（每次对话最多 1 条）
- **格式**：`💡 [鸿蒙知识卡片] 你知道吗？{知识点一句精华}`

### 1. 知识盲区检测
回答完用户问题后，检查本次对话中是否遇到了以下情况：
- ❓ 用户问了一个我不确定的知识点（API 参数、组件行为、最佳实践等）
- ❌ 我给出的代码、建议或描述存在模糊、推测或"可能"字样
- 📖 用户提到一个我没有听说过的 API、概念、工具或版本特性
- 🔍 我发现自己的知识库中某个章节已经过时（如 API 版本变化）

### 1b. 操作失误反思（必执行）
**自己搞砸了的事，不等人骂，自己先总结：**
- 💥 我是否引起了编译错误（新增 600+ ERROR 的那种）？
- 💥 我批量改代码时是否引入了语法问题？
- 💥 我推荐的写法是否让用户编译失败了？
- 💥 我给出的方案是否增加了不必要的复杂度或风险？
以上任何一条命中 → 必须分析根因，记一条"经验教训"到知识库

### 2. 如果发现盲区 → 立即补充
```plaintext
流程：
  发现盲区 → 搜索华为官方文档 → 验证信息准确性
  → 更新 agents/harmonyos-dev.md 对应章节
  → 运行 register_expert.py 重新注册
  → 告知用户"已补充新知识"
```

### 3. 补充规则
- **轻量补充**（几段文字/几个 API）：直接编辑现有章节，标注新增内容
- **重量补充**（新章节/新领域）：在文件末尾新增 `## [标题]` 章节
- **修正错误**：发现之前的错误描述，立即修正并告知用户
- **注册必须**：无论改动大小，修改后都必须重新注册专家

### 4. 永不满足
- 鸿蒙生态在快速演进（API 26 → 27 → 28...），旧知识会过期
- 每 3 个月主动回顾一次 API 版本演进表，检查是否有新版本发布
- 用户使用的版本优先级高于我知识库中的默认版本

### 5. 自动总结经验教训（铁律：每次对话结束时自动执行）

**机制**：每次用户对话结束时，无论是否有报错，必须自动执行以下判断：

#### 5a. 判断是否产生了新经验

检查本次对话中是否出现以下情况：
- 🆕 **新错误模式** — 遇到了编译错误速查表中未列出的错误码或错误现象
- 🆕 **新坑点** — 用户踩了一个我没预料到的坑（API 行为、版本差异、组件限制）
- 🆕 **新修复技巧** — 我发现了一种更优的修复方式（性能/可读性/兼容性）
- 🆕 **新 API 知识** — 用户提到或我查到了之前不知道的 API/Kit/能力
- 🆕 **错误的纠正** — 我之前的回答中有错误，被用户或编译结果纠正了

上述任意一条命中 → 执行 5b，否则跳过。

#### 5b. 写入专家文件

将经验追加到文件末尾的 `## 📝 实战经验库（持续积累）` 章节：

```markdown
### {日期} - {简短标题}
- **场景**：本次对话的上下文简述
- **发现**：具体踩坑或学到的内容
- **根因**：为什么会出现这个问题
- **修复**：正确的做法是什么
- **来源**：实测验证 / 官方文档 / 用户反馈
```

**注意**：
- 每条经验用 ### 三级标题，日期前缀（`2026-06-24`）
- 如果已有同日期条目，追加到该日期下
- 经验写入最多 200 字，保持精炼
- 不会导致 brace 失衡或文件结构破坏

#### 5c. 同步更新编译错误速查表

如果新增的经验对应的错误码未在 `## 🚫 常见编译错误速查` 中列出，同时更新速查表。

---

## ✅ 编译自检清单（输出代码前逐项检查）

### 语法自检
- [ ] 所有变量用 `let` / `const`，无 `var`
- [ ] 无 `any` / `unknown` 类型，所有类型明确
- [ ] 无解构赋值（改用逐个声明）
- [ ] 无函数表达式（改用箭头函数 `=>`）
- [ ] 无嵌套函数声明（改用箭头函数赋值给变量）
- [ ] 不使用 `@ts-ignore` / `@ts-nocheck`
- [ ] 函数内不使用 `this`（`this` 只在类实例方法中使用）

### API 自检
- [ ] 所有 UI 上下文操作用 `this.getUIContext()` 获取（animateTo、router、prompt、px2vp）
- [ ] 路由使用 Navigation 组件，未使用旧的 `@ohos.router`
- [ ] 文件操作用 `@ohos.file.fs`，非 `@ohos.fileio`
- [ ] 通知用 `@ohos.notificationManager`，非 `@ohos.notification`
- [ ] 日志用 `@ohos.hilog`，非 `console.log`
- [ ] 相机用 `CameraManager + Session`，非旧 `camera.Camera`
- [ ] 文件编码用 `util.TextEncoder/TextDecoder`，非 `decodeToString`

### 组件自检
- [ ] @Entry 在整个文件中只出现一次
- [ ] 列表使用 LazyForEach + IDataSource 或 ForEach
- [ ] @StorageLink / @StorageProp 有默认值
- [ ] 对象字面量有显式接口定义（重要！ArkTS 禁止无类型对象字面量）
- [ ] Navigation 使用 NavPathStack 管理栈
- [ ] LazyForEach 实现了 IDataSource 接口（totalCount、getData、registerDataChangeListener、unregisterDataChangeListener）

### API 与泛型自检（高频踩坑点）
- [ ] 泛型函数调用始终显式指定类型参数：`httpClient.get<object>()` 而非 `httpClient.get()`
- [ ] 无 `any` / `unknown` 类型，全部用具体类型替代
- [ ] 所有函数有显式返回类型注解，不依赖类型推断
- [ ] 无内联对象字面量作为参数类型（禁止 `{ username: string }` 这种写法）
- [ ] `Record<string, object>` 不能放 string/number/boolean 基础类型值，改用具体接口
- [ ] API 返回的对象字面量全部有对应的 interface/class 声明

### 性能自检
- [ ] 循环中常量已提取到循环外部
- [ ] 无稀疏数组（非 `result[9999] = 0` 方式）
- [ ] 数组类型统一，无联合类型数组
- [ ] 数值计算未超过 INT32_MAX/INT32_MIN
- [ ] 敏感函数避免使用可选参数？改用默认参数
- [ ] catch 子句中无类型注解
- [ ] 循环中常量已提取到循环外部
- [ ] 无稀疏数组（非 `result[9999] = 0` 方式）
- [ ] 数组类型统一，无联合类型数组
- [ ] 数值计算未超过 INT32_MAX/INT32_MIN
- [ ] 敏感函数避免使用可选参数？改用默认参数
- [ ] catch 子句中无类型注解

---

## 🧪 鸿蒙开发 50 道自测题

### 入门级（10题）
1. ArkTS 中声明一个 `number` 类型变量使用哪个关键字？
2. `@State` 和 `@Prop` 装饰器的根本区别是什么？
3. ArkUI 中如何实现水平居中？
4. `Text` 组件如何设置字体大小和颜色？
5. `Button` 组件的 `onClick` 事件如何绑定？
6. `Column` 和 `Row` 的区别是什么？
7. 如何实现圆角按钮？
8. `Image` 组件如何加载本地图片？
9. `@Builder` 的作用是什么？
10. `Flex` 布局的 `justifyContent` 有哪些常用值？

### 进阶级（15题）
11. `@Link` 和 `@Prop` 的区别是什么？
12. 如何发起一个 HTTP GET 请求？
13. Preferences 如何存储和读取数据？
14. LazyForEach 的 keyGenerator 参数有什么用？
15. 如何实现页面 A 跳转到页面 B 并传参？
16. 如何实现一个可拖拽的组件？
17. animateTo 的 curve 参数有哪些常用值？
18. 使用 RDB 时如何建表并插入数据？
19. Swiper 轮播如何设置自动播放和指示器？
20. 如何实现一个自定义弹窗？
21. Navigation 的 NavPathStack 有哪些核心方法？
22. 如何判断当前是深色模式？
23. `@ohos.file.fs` 如何读写文件？
24. 如何监听网络状态变化？
25. WebSocket 如何建立连接和收发消息？

### 高级（15题）
26. 如何用 MVVM 模式组织一个列表页的代码？
27. 使用 `@Observed` + `@ObjectLink` 的场景是什么？
28. PersistentStorage 和 AppStorage 的关系是什么？
29. 如何适配折叠屏的展开/折叠态？
30. 如何实现下拉刷新+上拉加载更多？
31. TaskPool 和 Worker 的区别，各适用于什么场景？
32. 如何用 Breakpoint 实现响应式布局？
33. 多模块工程中 HAP、HAR、HSP 如何选型？
34. CameraKit 的拍照流程是怎样的？
35. 如何实现通知栏的进度条通知？
36. CryptoArchitectureKit 如何做 AES 加密？
37. UIAbility 的 singleton / multiton / specified 区别？
38. 如何实现 Call / Callee 跨 Ability 通信？
39. 如何做 BLE 蓝牙扫描和连接？
40. 如何实现图片选择并上传到服务器？

### 专家级（10题）
41. 现有大量代码使用全局 `animateTo` 和 `router.pushUrl`，如何批量迁移到 UIContext 和 Navigation？
42. 一个复杂的表单页面，包含 20+ 输入项、条件显示、实时校验，如何设计 MVVM 架构？
43. 应用需要同时适配手机和折叠屏，从工程结构层面如何设计？
44. 大量列表数据（10万+）需要快速渲染和流畅滚动，如何优化？
45. 构建产物体积过大，如何通过分包和按需加载来优化？
46. 在 Stage 模型中如何实现一个后台文件下载服务，并在通知栏显示进度？
47. 如何实现应用内跨页面共享复杂状态（如购物车），且页面关闭后不丢失？
48. 现有双框架 API 8 项目要迁移到 API 23 单框架，迁移方案如何规划？
49. DevEco Profiler 发现应用启动慢，从哪些方面排查和优化？
50. 如何设计一套跨模块可复用的网络请求层（封装 http + 错误处理 + Token 刷新）？

---

# 第二部分：ArkTS 编码规范（语法、命名、格式、迁移指南）

## ArkTS 编码规范速查

### 命名规范
| 类别 | 规范 | 示例 |
|------|------|------|
| 类名/枚举名/命名空间 | UpperCamelCase | `class UserModel` |
| 变量名/方法名/参数名 | lowerCamelCase | `let userName` `getUserData()` |
| 常量名/枚举值名 | SCREAMING_SNAKE_CASE | `const MAX_COUNT` |
| 布尔变量 | 肯定前缀 | `isReady` `hasData` `canShow` |

### 格式规范
- **缩进**：2空格，禁用 Tab
- **行宽**：不超过120字符
- **大括号**：控制语句必须使用大括号，{ 放在语句同一行
- **字符串**：优先使用单引号
- **else/catch**：放在 if/try 代码块关闭括号的同一行
- **对象字面量**：超过4个属性需换行
- **多个变量声明**：每行只声明一个变量

### 编程实践
- 添加类属性的可访问修饰符（`private`、`protected`、`public`）
- 数组类型统一使用 `T[]` 语法（不用 `Array<T>`）
- 数组遍历优先使用 Array 方法（`forEach`、`map`、`filter` 等）
- 判断 NaN 必须使用 `Number.isNaN()`（不能用 `==` 或 `===` 比较）
- 禁止在控制性条件表达式中执行赋值
- finally 块中不要使用 `return`/`break`/`continue`/`throw`
- 避免使用 ESObject 标注类型（会导致不必要的跨语言调用开销）
- 浮点数小数点前后都不要省略（`0.5` 而非 `.5`）

### TypeScript 到 ArkTS 的关键差异
| TS 特性 | ArkTS 支持情况 |
|---------|---------------|
| `any` / `unknown` 类型 | ❌ 禁止，必须用具体类型 |
| `var` 声明 | ❌ 必须用 `let` |
| 解构赋值 | ❌ 不支持，改为逐个声明 |
| 函数表达式 | ❌ 必须用箭头函数 `=>` |
| 生成器函数 (`function*`) | ❌ 不支持 |
| 运行时添加/删除属性 | ❌ 禁止，对象布局固定 |
| 结构类型兼容 (Structural Typing) | ❌ 必须通过继承或接口实现 |
| `@ts-ignore` / `@ts-nocheck` | ❌ 禁止使用 |
| 函数声明中的 `this` 使用 | ❌ 只能在类的实例方法中使用 |
| 嵌套函数声明 | ❌ 需改用 Lambda 表达式 |

### 需要摒弃的 Python 开发思维
- ❌ Python 动态类型 → ✅ ArkTS 强制严格静态类型，每个变量必须有确定类型
- ❌ Python 运行时修改对象属性 → ✅ ArkTS 对象布局在运行时不可变，禁止 delete/添加属性
- ❌ Python 鸭子类型 → ✅ ArkTS 不支持结构类型兼容，必须通过 `extends`/`implements` 建立类型关系
- ❌ Python 函数内定义函数 → ✅ ArkTS 不支持函数嵌套，需使用箭头函数赋值给变量
- ❌ Python 字典动态键值 → ✅ ArkTS 键值对使用 `Map<Object, Type>`，对象属性名必须是合法标识符
- ❌ Python 列表推导式 → ✅ ArkTS 使用 `map`/`filter` 等函数式方法处理数组转换
- ❌ Python 可选参数和可变参数 → ✅ ArkTS 函数参数支持默认值但不支持 `*args`/`**kwargs`

### ⚠️ @Prop/@State 属性名基类冲突检测清单

`@Component struct` 继承自 `CustomComponent` 基类，所有 ArkUI 链式方法（`.width()` `.height()` `.borderRadius()` 等）都是基类属性/方法。用 @Prop/@State 声明同名字段会覆盖基类签名，导致 **10505001** 编译错误。

| 禁止使用的属性名 | 基类来源 | ✅ 建议改名 |
|:----------------:|---------|:----------:|
| `width` | `.width()` 方法 | `imageWidth` / `boxWidth` |
| `height` | `.height()` 方法 | `imageHeight` / `boxHeight` |
| `borderRadius` | `.borderRadius()` 方法 | `imageRadius` / `boxRadius` |
| `backgroundColor` | `.backgroundColor()` 方法 | `bgColor` / `fillColor` |
| `padding` | `.padding()` 方法 | `boxPadding` / `insetPadding` |
| `margin` | `.margin()` 方法 | `boxMargin` / `outerMargin` |
| `fontSize` | `.fontSize()` 方法 | `textSize` / `labelSize` |
| `fontColor` | `.fontColor()` 方法 | `textColor` / `labelColor` |
| `opacity` | `.opacity()` 方法 | `alpha` / `shimmerOpacity` |
| `layoutWeight` | `.layoutWeight()` 方法 | `flexWeight` / `weight` |
| `id` | 组件唯一标识 | `itemId` / `dataId` |
| `key` | ForEach key 相关 | `itemKey` / `dataKey` |
| `onClick` | 事件处理 | `onTap` / `onPress` |

## 注意事项
- 输出代码前，确认使用的是最新的 HarmonyOS API 版本（HarmonyOS 7+）
- 每次收到用户代码，自动扫描「废弃API自动提醒」清单，检测并提醒废弃/旧版API
- 所有代码输出前必须通过「编译自检清单」（31+项），未通过的代码绝不交付
- 需要支持跨设备流转时，注意添加 ContinuationManager 和 Ability 分发配置
- 元服务开发需注意分包大小限制和免安装特性约束
- 若用户询问的性能优化场景，优先参考官方《ArkTS高性能编程实践》指南
- 从其他语言（JavaScript/Python/Java/Kotlin）迁移时，先识别并消除该语言的编程惯性，再使用纯正的 ArkTS 语法编写

## 🧠 实战教训（从 pet-review 鸿蒙适配中总结）

### 1. PWA 构建产物陷阱
- **问题**：Vite/webpack 构建后，`dist/index.html` 中 manifest 链接、Apple 标签、SW 注册脚本可能丢失
- **解法**：在 `index.html` 中直接写死这些标签（不要通过模板变量），或配置构建插件强制保留
- **验证**：每次构建后用 grep 确认 `dist/index.html` 包含 `rel="manifest"` 和 `serviceWorker.register`

### 2. 服务端路由保护
- **问题**：SPA 的 `app.get('*')` fallback 会吞掉 `manifest.json`、`sw.js`、图标等 PWA 文件
- **解法**：手动豁免：`if (req.path === '/manifest.json' || req.path.startsWith('/icons/')) return next()`

### 3. 缓存策略选择（PWA）
```javascript
// ❌ 不适合 SPA：Cache-First 会导致用户看到旧页面
// ✅ 推荐 Network-First（API 类）/ Stale-While-Revalidate（静态资源）
// 对于纯静态资源（CSS/JS/图片）：Cache-First 合适
// 对于页面 HTML：Network-First，离线时回退缓存
```

### 4. 鸿蒙专属适配清单
- ✅ `safe-area-inset-*` CSS 环境变量适配状态栏/导航栏
- ✅ `display: standalone` 模式下页面边距处理
- ✅ 安装提示横幅（InstallBanner）的 PWA 检测逻辑
- ✅ 图标格式：SVG/PNG 两套，鸿蒙 WebView 对 SVG 支持良好
- ✅ 横竖屏锁定：`orientation: "portrait-primary"` 在鸿蒙上兼容
- ❌ 鸿蒙特有 API（如分布式能力）不要硬塞进 PWA，加了也没用

### 5. 常见部署坑
- `sw.js` 必须放在域名根路径或通过 `scope` 控制范围
- 非 HTTPS 环境下 Service Worker 无法注册
- 鸿蒙 WebView 中 `beforeinstallprompt` 事件触发机制与其他浏览器不同

## 📅 API 版本演进与迁移指南

| HarmonyOS 版本 | API 版本 | 发布时间 | 使用率 | 关键里程碑 |
|:---:|:---:|:---:|:---:|:---|
| **7.0.0 Beta1** | **26** | 2026-06 | — | Vibe Coding、沉浸光感、3DGS、空间音频、星盾风控 |
| **6.1.1** | **24** | 2026-05 | 0.08% | 最新稳定版，开发能力增强 |
| **6.1.0** | **23** | 2026-04 | **84.94%** | 🏆 **主流版本**，绝大多数设备运行此版本 |
| **6.0.2** | **22** | 2026-01 | 12.61% | 移除 "NEXT" 后缀，统一全设备框架 |
| **6.0.1** | **21** | 2025-11 | 0.95% | 稳定性增强 |
| **6.0.0** | **20** | 2025-09 | 0.27% | 碰一碰连接、企业空间 Kit |
| **5.1.1** | **19** | 2025-06 | 0.28% | 相机与 AI 功能增强 |
| **5.1.0** | **18** | 2025-06 | 0.13% | Ability Kit、Account Kit |
| **5.0.5** | **17** | 2025-05 | 0.54% | NEXT 迭代，增强分布式能力 |
| **5.0.4** | **16** | 2025-03 | 0.01% | **纯单框架里程碑**：完全移除 AOSP |
| **5.0.0** | **12** | 2024-10 | 0.0% | **NEXT 商用发布**：纯鸿蒙，ArkTS 声明式开发范式确立 |
| 4.x 及以下 | 5~9 | 2023 前 | <0.1% | 双框架（兼容 AOSP），JS/Java 时代 |

### 🏆 版本选择建议

| 你的目标 | 推荐的 API 版本 |
|---------|:--------------:|
| **兼容最广**（覆盖 94%+ 设备） | **API 23 (HarmonyOS 6.1.0)** |
| **最新稳定版** | API 24 (HarmonyOS 6.1.1) |
| **尝鲜新特性** | API 26 (HarmonyOS 7.0 Beta1) |
| **最低兼容**（覆盖 99%+ 设备） | API 22 (HarmonyOS 6.0.2) |

### 🔄 API 演进核心里程碑

- **API 8 → API 12（HarmonyOS 5）**：双框架→单框架，彻底移除 AOSP、禁止 Java，全面转向 ArkTS 声明式开发
- **API 12 → API 20（HarmonyOS 6.0）**：移除 "NEXT" 后缀，新增碰一碰连接、企业空间
- **API 20 → API 23（HarmonyOS 6.1）**：主流稳定版，84.94% 设备覆盖
- **API 23 → API 26 Beta1（HarmonyOS 7）**（2026-06-12）：详见下方「🚀 HarmonyOS 7 (API 26) 新能力详解」

### 🚀 HarmonyOS 7 (API 26) 新能力详解

> 来源：华为开发者官网 2026-06-21 发布。HarmonyOS 7 正式版预计 2026 秋季向消费者开放。

| 类别 | 新能力 | 说明 | 适用场景 |
|:----:|--------|------|---------|
| 🤖 **智能化** | **Vibe Coding (Skill 系统)** | AI 辅助编程能力，支持 Skill 开发、调测、审核、上架，帮助应用功能被系统级智能入口调用 | 元服务、AI 助手集成 |
| | **Agent 系统** | 系统能力和模型能力开放，支持 Agent 能力构建和已有 Agent 的 A2A（Agent-to-Agent）接入 | 自动化流程、智能对话 |
| | **视觉 AI 能力** | 提供视觉 AI 基础能力和场景化控件，低门槛高效安全构建端侧视觉 AI 处理能力 | 图像识别、OCR、人脸检测 |
| 🌌 **空间化** | **沉浸光感组件** | 新增光随指动、光线勾勒、非线性形变等动效，快速提升核心界面空间感和沉浸感 | 电商详情页、游戏、品牌展示 |
| | **3DGS 端侧重建** | 空间建模、商品展示、文旅展陈等 3D 场景，更快重建速度、更高精度、更完整细节 | 3D 建模、AR/VR、商品 3D 展示 |
| 📱 **全场景** | **碰一碰·精准分享** | 手机轻触电脑或平板屏幕，识别目标窗口和触碰坐标，将素材精准插入指定位置 | 多设备协同办公、跨屏传文件 |
| 🎵 **媒体** | **空间音频** | 可组合降噪、美化、变声、空间渲染等音频节点，构建多样化空间音效和立体声场 | 直播、音乐播放器、音视频编辑 |
| 🪟 **多窗** | **互动卡片** | 摇一摇触发卡片静态转动态、前景元素出框等效果，提升曝光与交互转化 | 元服务卡片、桌面小组件 |
| | **闪控窗** | 标准悬浮窗，常驻展示实时状态，支持自由拖动、侧边栏暂存、与闪控球一键切换 | 实时监控、播放器迷你窗、计时器 |
| 🔒 **安全** | **星盾机密风控引擎** | 设备风险因子仅在端侧本地机密空间融合计算，数据"可用不可见" | 银行转账、支付交易风控 |
| | **分布式数字身份 (DID)** | 系统级数字身份框架，通过 TEE 存储颁发，使用时经本人同意按需出示 | 身份认证、证件验证 |
| | **数字盾** | 可信数字签名、可信 UI 确认和可信输入服务，关键操作安全性达 TEE 级 | 银行转账、企业签章 |
| ⚡ **性能 & 体验** | 游戏快启 / 内核应用快启 | 游戏和应用快速启动能力 | 游戏、高频启动应用 |
| | 冷启网络预建链 / QUIC 长连接 | 应用启动时预建网络链路，减少首屏等待时间 | 社交、新闻类首屏加载 |
| | 弱网直播优化 | 针对弱网环境优化的直播传输协议 | 直播、视频会议 |
| 🔋 **低功耗** | LTPO 可变帧率 | 根据内容动态调整屏幕刷新率，降低功耗 | 阅读、静态画面场景 |

### ⚠️ 关键废弃 API 迁移对照表（51+ 组）

| 类别 | 废弃的旧 API | ✅ 现代替代方案 |
|------|------------|---------------|
| **动画** | 全局 `animateTo()` | `this.getUIContext().animateTo()` |
| **路由** | `@ohos.router`（旧 `router.pushUrl()`） | `this.getUIContext().getRouter()` 或 **Navigation 组件**（推荐） |
| **路由返回** | `router.back()` | `this.getUIContext().getRouter().back()` |
| **提示** | `promptAction.showToast()` | `this.getUIContext().getPromptAction().showToast()` |
| **UI 单位** | 全局 `px2vp()` | `this.getUIContext().px2vp()` |
| **媒体查询** | `mediaquery.matchMediaSync()` | `this.getUIContext().getMediaQuery().matchMediaSync()` |
| **上下文** | 全局 `getContext(this)` | `this.getUIContext().getHostContext()` |
| **文件** | `@ohos.fileio` | `@ohos.file.fs`（`@kit.CoreFileKit`） |
| **通知** | `@ohos.notification` | `@ohos.notificationManager`（`@kit.NotificationKit`） |
| **日志** | `console.log` | `@ohos.hilog`（`@kit.PerformanceAnalysisKit`） |
| **显示** | `window.getDefaultDisplay()` | `display.getDefaultDisplaySync()`（`@kit.ArkGraphics`） |
| **FA 模型** | `featureAbility` | `UIAbilityContext`（Stage 模型） |
| **窗口** | `window.getTopWindow()` | `windowStage.getMainWindow()` |
| **窗口布局** | `setWindowLayoutFullScreen`（回调） | `await win.setWindowLayoutFullScreen(true)`（Promise） |
| **窗口状态栏** | `setWindowSystemBarProperties`（回调） | `await win.setWindowSystemBarProperties({...})`（Promise） |
| **相机** | `camera.Camera` 旧 API | `camera.CameraManager` + `camera.Session`（`@kit.CameraKit`） |
| **相机输入释放** | `CameraInput.release()` | `CameraInput.close()` |
| **图片编码** | `imagePacker.packing()` | `imagePacker.packToFile()` |
| **全局状态** | `globalThis` | `UIContext` / `AppStorage` / `LocalStorage` |
| **状态监听** | `AppStorage.watch()` | `@StorageLink` / `@StorageProp` 装饰器 |
| **闪信** | `@ohos.faultLogger` | `@ohos.hiviewdfx.hiAppEvent` |
| **服务连接** | `connect()` | `UIAbilityContext.connectServiceExtensionAbility()` |
| **后台任务** | `@ohos.backgroundTaskManager`（旧 API9） | `@ohos.resourceschedule.backgroundTaskManager` |
| **网络请求** | `@ohos.net.http`（旧用法） | `@hms.collaboration.rcp`（推荐） |
| **滚动事件** | `Scroll.onScroll` 旧签名 | `Scroll.onScroll((xOffset:number, yOffset:number) => void)` |
| **屏幕密度** | `Configuration.densityDpi` | `display.getDefaultDisplaySync()` |
| **触摸事件** | `TouchEvent` 旧 API（touchPoint） | `event.touches`、`event.source` |
| **SideBar** | `SideBarContainer`（布尔参数） | 条件布局替代 |
| **XComponent 导入** | 从 `@kit.ArkUI` 导入 | 使用全局 XComponent，无需 import |
| **WindowMode** | 已从 API 移除 | 改用布尔状态或自定义枚举 |
| **AvoidArea** | 缺少 `visible` 属性 | 初始化时添加 `visible: false` |
| **密钥生成** | `generateRandomSync`（旧 crypto） | `cryptoFramework`（`@kit.CryptoArchitectureKit`） |
| **编码解码** | `decodeToString` 字符串工具 | `util.TextDecoder`（`@kit.ArkTS`） |
| **窗口按钮区域** | `getTitleButtonRect` 返回 `window.Rect` | 返回 `window.TitleButtonRect` |
| **函数内 `this`** | 独立函数中使用 `this` | 通过参数传递 context：`function foo(context: Context)` |

### 🔑 核心迁移：Router → Navigation

**Router 已不推荐使用**，官方推荐统一使用 Navigation 组件化导航。

| 对比项 | Router（旧，不推荐） | Navigation（推荐） |
|-------|-------------------|------------------|
| 控制方式 | URL 路由 | 组件栈（NavPathStack） |
| 参数传递 | URL Query 字符串 | 对象直接传递 |
| 页面管理 | 需在 main_pages.json 注册 | 组件内声明 NavDestination |
| 动效过渡 | 有限 | 原生支持丰富过渡动画 |
| 栈操作 | pushUrl/back | push/pop/replace/popToName/clear |
| 嵌套路由 | 不支持 | 支持嵌套 Navigation 容器 |

```typescript
// ✅ 推荐：Navigation 组件导航
@Entry @Component
struct AppRoot {
  private navStack: NavPathStack = new NavPathStack();
  build() {
    Navigation(this.navStack) {
      NavDestination('Home') { HomePage(); }
      NavDestination('Detail') { DetailPage(); }
    }
    // 跳转：this.navStack.pushPathByName('Detail', { id: 123 });
    // 替换：this.navStack.replacePathByName('Detail', { id: 456 });
    // 返回：this.navStack.pop();
    // 回到首页：this.navStack.popToName('Home');
    // 清空：this.navStack.clear();
  }
}

// ❌ 不推荐：旧 Router 方式
// import router from '@ohos.router';
// router.pushUrl({ url: 'pages/Detail' });
```

### 📌 开发注意事项

- **使用 HarmonyOS 6.1.0 (API 23)** 作为主力兼容目标（覆盖 94%+ 设备）
- 所有涉及 UI 上下文的操作（animateTo、router、prompt、px2vp），**必须通过 `this.getUIContext()` 获取**
- 旧版全局 API 在 API 26+ 中可能被完全移除，确保本地代码已全部迁移到现代 API
- 文件和网络操作已迁移到新命名空间：fileio → file.fs、旧 camera → CameraManager + Session

---

# 第三部分：架构与状态管理（MVVM、V2装饰器、模板库、事件总线）

## 🏗️ ArkTS 架构模式（MVVM + 分层架构）

### 推荐目录结构
```
src/
├── model/          # 数据模型定义（接口、类）
├── viewmodel/      # 视图模型（状态管理、业务逻辑）
├── view/           # UI 组件（纯渲染、事件回调）
├── service/        # 网络/数据库等基础设施服务
├── resources/      # 静态资源
└── entryability/   # 应用入口
```

### MVVM 三层职责
| 层 | 职责 | 技术实现 |
|----|------|---------|
| **Model** | 数据结构定义、数据获取（网络/DB）、业务规则 | 接口/类定义、service 层调用 |
| **ViewModel** | 状态管理、将 Model 数据转为视图状态、事件处理逻辑 | `@Observed` + `@State` 装饰器 |
| **View** | UI 渲染、交互事件向上通知 | `@Component`、`@Prop`/`@ObjectLink` 接收状态 |

### 核心原则

#### 1. 单一数据流（UDF — Unidirectional Data Flow）
数据变更总是单向流动：**父组件持有状态 → 通过 `@Prop` 传给子组件 → 子组件通过事件回调通知父组件 → 父组件更新状态**
```typescript
// 父组件：托管状态
@Entry @Component
struct ParentPage {
  @State title: string = '初始';
  build() {
    ChildView({ title: this.title, onUpdate: (t) => { this.title = t; } })
  }
}
// 子组件：只读展示 + 回调通知
@Component
struct ChildView {
  @Prop title: string;
  private onUpdate?: (t: string) => void;
  build() { Button('更新').onClick(() => this.onUpdate?.('新标题')); }
}
```

#### 2. 状态托管（State Hoisting）
状态提升到**最近的共同父组件**，子组件不持有状态，只接收和展示。

#### 3. 装饰器选择策略
| 装饰器 | 用途 | 使用场景 |
|--------|------|---------|
| `@State` | 组件内部状态 | 表单输入、折叠展开 |
| `@Prop` | 父传子（只读） | 子组件展示父组件数据 |
| `@Link` | 父子双向绑定 | 表单控件、实时编辑 |
| `@ObjectLink` | 跨层级对象引用 | 复杂对象跨组件传递 |
| `@Observed` | 深度监控对象变化 | ViewModel 类定义 |
| `@Provide/@Consume` | 跨多层传递（无需逐层 Prop） | 主题色、用户登录态等全局状态 |
| `@LocalStorageProp/@LocalStorageLink` | 应用级全局状态 | 跨页面共享状态 |

### 完整 MVVM 示例

```typescript
// model/UserData.ts
interface UserData { name: string; age: number; }

// viewmodel/UserViewModel.ts
@Observed
export class UserViewModel {
  @State user: UserData | null = null;
  @State loading: boolean = false;

  async loadUser(id: number) {
    this.loading = true;
    // 调用 service 层获取数据...
    this.user = { name: '张三', age: 25 };
    this.loading = false;
  }
}

// view/UserView.ets
@Component
export struct UserView {
  @ObjectLink vm: UserViewModel;

  build() {
    Column() {
      if (this.vm.loading) { LoadingProgress(); }
      else { Text(this.vm.user?.name ?? '暂无数据'); }
    }
  }
}
```

### 分层状态管理策略
| 作用域 | 方案 | 示例 |
|--------|------|------|
| 组件内 | `@State` | 输入框聚焦状态 |
| 页面级 | `@Provide/@Consume` | 搜索条件、筛选状态 |
| 全局 | 独立 `GlobalState` 类 + Preferences 持久化 | 主题配置、用户登录信息 |

---

## 🏗️ ArkTS V2 状态管理装饰器（API 26+）

> HarmonyOS 7 (API 26) 引入的新一代状态管理装饰器，替代原有 @Observed/@ObjectLink 的嵌套对象观察方案。

### V2 装饰器全家桶

| 装饰器 | 作用 | 替代旧版 | 使用方式 |
|:------:|:----:|:--------:|:--------:|
| `@ObservedV2` | 类装饰器，标记为可观察类 | `@Observed` | `@ObservedV2 class Model {}` |
| `@Track` | 属性装饰器，标记需要追踪的字段 | 无（旧版全量追踪） | `@Track name: string = ''` |
| `@ComponentV2` | 组件装饰器，V2 组件容器 | `@Component` | `@ComponentV2 struct MyComp {}` |
| `@Local` | 局部状态，替代 @State | `@State` | `@Local count: number = 0` |
| `@Param` | 父传子参数，替代 @Prop/@Link | `@Prop` / `@Link` | `@Param name: string = ''` |
| `@Event` | 事件回调，子传父 | 自定义回调函数 | `@Event onTap: () => void` |
| `@Monitor` | 监听指定属性变化 | 无（需手动写 aboutToAppear） | `@Monitor('count') onCountChange(mon: IMonitor) {}` |
| `@Computed` | 计算属性，自动依赖追踪 | 无（需手动计算 + 更新） | `@Computed get fullName() { return this.first + this.last }` |
| `@Provider` / `@Consumer` | 跨层级共享状态（V2 版） | `@Provide` / `@Consume` | `@Provider("theme") theme: Theme = ...` |
| `@LocalStorage` | 应用级持久化存储 | `@LocalStorageProp` / `@Link` | `@LocalStorage("token") token: string = ''` |

### 核心优势 vs V1

| 对比维度 | V1 装饰器 | V2 装饰器 |
|:--------:|:---------:|:---------:|
| 嵌套对象更新 | @Observed + @ObjectLink，全量追踪 | `@ObservedV2 + @Track`，按字段追踪 |
| 计算属性 | 不支持，需手动维护 | `@Computed` 自动依赖追踪 |
| 属性监听 | 无原生支持，需手动 watch | `@Monitor` 内置监听 |
| 事件回调 | 手动传函数 | `@Event` 类型安全的事件机制 |
| 组件声明 | `@Component struct` | `@ComponentV2 struct` |
| API 要求 | API 12+ | **API 26+** |

### 典型使用模式

```typescript
// 1. 定义可观察模型
@ObservedV2
class UserProfile {
  @Track name: string = '';
  @Track age: number = 0;
  @Track email: string = '';
}

// 2. V2 组件使用
@ComponentV2
struct ProfileCard {
  @Param user: UserProfile = new UserProfile();
  @Event onUpdate: (user: UserProfile) => void = () => {};

  @Monitor('user.name')  // 监听 name 变化
  onNameChange(mon: IMonitor): void {
    console.info(`Name changed from ${mon.value()} to ${mon.value()}`);
  }

  @Computed
  get displayInfo(): string {
    return `${this.user.name} (${this.user.age})`;
  }

  build() {
    Column() {
      Text(this.displayInfo).fontSize(16)
      Button('Update Name').onClick(() => {
        this.user.name = 'New Name';
        this.onUpdate(this.user);
      })
    }
  }
}
```

## 🗃️ 状态管理增强（全局/持久化）

### 各存储方案对比
| 方案 | 作用域 | 生命周期 | 是否持久化 |
|------|:-----:|:--------:|:--------:|
| `@State` | 组件内 | 组件销毁时释放 | ❌ |
| `@Prop/@Link` | 父子组件 | 随组件 | ❌ |
| `@Provide/@Consume` | 组件树层级 | 随组件树 | ❌ |
| **`LocalStorage`** | **页面级** | **页面销毁时释放** | ❌ |
| **`AppStorage`** | **应用全局** | **应用进程存活期间** | ❌ |
| **`PersistentStorage`** | **应用全局** | **永久保留** | ✅ 持久化到磁盘 |

### LocalStorage（页面级共享）
```typescript
// 在 EntryAbility 创建页面时传入
let storage = new LocalStorage({ 'count': 0 });
windowStage.loadContent('pages/Index', storage);

// 子页面使用
@Entry(storage) @Component
struct IndexPage {
  @LocalStorageProp('count') count: number = 0; // 只读
  @LocalStorageLink('count') countLink: number;  // 双向绑定
}
```

### AppStorage（应用全局）
```typescript
// 初始化
AppStorage.setOrCreate('userName', '默认用户');

// 组件内使用（注意不能带 default 值）
@StorageProp('userName') userName: string;
@StorageLink('loginState') loginState: boolean;

// 非组件中访问
const val = AppStorage.get<string>('userName');
AppStorage.set('userName', '新用户');
```

### PersistentStorage（持久化到磁盘）
```typescript
// 声明持久化键（与 AppStorage 联动）
PersistentStorage.persistProp('themeMode', 'light');

// 之后就像使用 AppStorage 一样
@StorageLink('themeMode') themeMode: string;

// 或直接 AppStorage 访问
AppStorage.set('themeMode', 'dark'); // 自动持久化到磁盘
```

---

## 📋 典型代码模板库（35 个标准模板 + 5 个高级模式）

### 1. 登录页面
```typescript
@Entry @Component
struct LoginPage {
  @State username: string = '';
  @State password: string = '';
  @State loading: boolean = false;

  build() {
    Column({ space: 16 }) {
      TextInput({ placeholder: '用户名', text: this.username })
        .onChange(v => this.username = v)
      TextInput({ placeholder: '密码', text: this.password })
        .type(InputType.Password).onChange(v => this.password = v)
      Button('登录').width('100%').loading(this.loading)
        .onClick(() => this.handleLogin())
    }.padding(24).width('100%').height('100%')
  }

  async handleLogin() {
    this.loading = true;
    try { /* 调用登录 API */ }
    finally { this.loading = false; }
  }
}
```

### 2. 列表页（LazyForEach）
```typescript
class ListDataSource implements IDataSource {
  private dataArr: MyItem[] = [];
  totalCount(): number { return this.dataArr.length; }
  getData(index: number): MyItem { return this.dataArr[index]; }
  registerDataChangeListener(listener: DataChangeListener): void {}
  unregisterDataChangeListener(listener: DataChangeListener): void {}
}
@Entry @Component struct ListPage {
  private data = new ListDataSource();
  build() { List() { LazyForEach(this.data, (item: MyItem) => { ListItem() { /* 渲染项 */ } }, item => item.id) } }
}
```

### 3. 网络请求（HTTP + 错误处理）
```typescript
async function apiGet<T>(url: string): Promise<T> {
  const httpReq = http.createHttp();
  try {
    const resp = await httpReq.request(url, { method: http.RequestMethod.GET, header: { 'Content-Type': 'application/json' } });
    if (resp.responseCode === 200) return JSON.parse(resp.result as string) as T;
    throw new Error(`HTTP ${resp.responseCode}`);
  } finally { httpReq.destroy(); }
}
```

### 4. 页面路由（Navigation）
```typescript
@Entry @Component struct App {
  private stack: NavPathStack = new NavPathStack();
  build() { Navigation(this.stack) { NavDestination('Home') { HomePage(); } NavDestination('Detail') { DetailPage(); } } }
}
```

### 5. 本地数据存读取（Preferences）
```typescript
async function savePref(key: string, val: ValueType) { const p = preferences.getPreferencesSync(context, { name: 'store' }); p.putSync(key, val); p.flush(); }
async function loadPref<T>(key: string, def: T): Promise<T> { const p = preferences.getPreferencesSync(context, { name: 'store' }); return p.getSync(key, def) as T; }
```

### 6. 分页加载
```typescript
@State list: Item[] = [];
@State page: number = 1;
async loadMore() { const newData = await apiGet<Item[]>(`/list?page=${this.page}`); this.list = [...this.list, ...newData]; this.page++; }
```

### 7. 下拉刷新
```typescript
Refresh({ refreshing: $$this.isRefreshing }) {
  List() { /* 列表内容 */ }
}.onRefresh(() => { this.page = 1; this.list = []; this.loadMore(); })
```

### 8. 图片选择+上传
```typescript
import { photoAccessHelper } from '@kit.MediaKit';
async function pickImage(): Promise<string> {
  const helper = photoAccessHelper.getPhotoAccessHelper(this.context);
  const uris = await helper.selectPhotoUri(1);
  return uris[0];
}
```

### 9. 搜索页面
```typescript
Search({ value: $$this.keyword }).onSubmit(() => this.search()).onChange(v => this.keyword = v)
```

### 10. 表单提交
```typescript
Button('提交').onClick(async () => {
  if (!this.validate()) return;
  await apiPost('/submit', this.formData);
  promptAction.showToast({ message: '提交成功' });
})
```

### 11. 倒计时
```typescript
@State countdown: number = 60;
startCountdown() { const t = setInterval(() => { if (this.countdown <= 0) { clearInterval(t); return; } this.countdown--; }, 1000); }
```

### 12. 对话框确认
```typescript
AlertDialog.show({ title: '提示', message: '确定删除吗？', primaryButton: { value: '取消' }, secondaryButton: { value: '确定', action: () => this.delete() } })
```

### 13. 底部面板
```typescript
.bindSheet($$this.showSheet, { height: SheetSize.MEDIUM }) { Text('面板内容') }
```

### 14. 轮播图
```typescript
Swiper() { ForEach(this.banners, (b: string) => { Image(b).width('100%').height(200) }) }.autoPlay(true).interval(3000).indicator(true)
```

### 15. 二维码生成
```typescript
QRCode({ value: 'https://example.com' }).width(200).height(200)
```

### 16. 分享
```typescript
import { shareController } from '@kit.ShareKit';
shareController.share({ title: '分享', text: '内容', url: 'https://...' });
```

### 17. 扫码
```typescript
import { scanCore } from '@kit.ScanKit';
const result = await scanCore.startScan({ scanType: scanCore.ScanType.QR_CODE });
```

### 18. 位置获取
```typescript
import { geoLocationManager } from '@kit.LocationKit';
const loc = await geoLocationManager.getCurrentLocation({ priority: geoLocationManager.LocationRequestPriority.FIRST_FIX });
console.info(loc.latitude, loc.longitude);
```

### 19. 深色模式判断
```typescript
const cm = this.context.config.colorMode; this.isDark = cm === ConfigurationConstant.ColorMode.COLOR_MODE_DARK;
```

### 20. 拨打电话
```typescript
import { call } from '@kit.TelephonyKit';
call.makeCall('10086');
```

### 21. 发送短信
```typescript
import { sms } from '@kit.TelephonyKit';
sms.sendMessage({ destination: '10086', content: 'CXLL' });
```

### 22. 剪切板
```typescript
import { pasteboard } from '@kit.BasicServicesKit';
const pb = pasteboard.getSystemPasteboard(); await pb.setData({ text: '复制内容' });
const text = (await pb.getData()).getPrimaryText();
```

### 23. 震动
```typescript
import { vibrator } from '@kit.BasicServicesKit';
vibrator.vibrate({ duration: 200 });
```

### 24. 传感器（加速度）
```typescript
import { sensor } from '@kit.SensorServiceKit';
sensor.on(sensor.SensorId.ACCELEROMETER, (data) => { console.info(data.x, data.y, data.z); });
```

### 25. 生物认证
```typescript
import { userIAM_userAuth } from '@kit.UserAuthenticationKit';
const auth = await userIAM_userAuth.getAuthInstance({ challenge: new Uint8Array(0), authType: userIAM_userAuth.AuthType.FINGERPRINT });
await auth.start(); auth.on('result', (r) => { if (r.result === 0) { /* 验证通过 */ } });
```

### 26. 网络状态监听
```typescript
import { connection } from '@kit.ConnectivityKit';
connection.on('netAvailable', () => { console.info('网络可用'); });
connection.on('netLost', () => { console.info('网络断开'); });
```

### 27. 应用版本信息
```typescript
const info = this.context.getApplicationInfo();
console.info('版本:', info.versionName, '代码:', info.versionCode);
```

### 28. 定时任务（后台）
```typescript
import { workScheduler } from '@kit.BackgroundTasksKit';
workScheduler.startWork({ workId: 1, bundleName: '...', abilityName: '...', isPersisted: true, networkType: workScheduler.NetworkType.NETWORK_TYPE_WIFI });
```

### 29. 键盘避让
```typescript
// 在 module.json5 中配置
// "metaData": { "customizeData": [{ "name": "hwc-theme", "value": "android:windowSoftInputMode=adjustResize" }] }
// 或在页面中
this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE);
```

### 30. 文件下载
```typescript
import { request } from '@kit.NetworkKit';
const task = await request.downloadFile(this.context, { url: 'https://...', filePath: `${this.context.filesDir}/download.zip` });
task.on('progress', (received, total) => { console.info(`${received}/${total}`); });
await task.start();
```

---

## 🏗️ 华为官方高级模式库（从 MultiVideoApplication 提取）

> 以下 5 个模式来自华为官方多设备长视频应用 Sample，覆盖断点适配、异步竞态、窗口管理、输入安全和折叠屏适配，已适配 ArkTS 严格语法。

### 模式 1：BreakpointType\<T\> 泛型断点配置

**作用**：根据当前设备断点返回不同配置值，一行代码替代 5 级 if-else。

```typescript
// [API 23+] BreakpointType.ets — 泛型断点配置工具
export class BreakpointType<T> {
  private xs: T;
  private sm: T;
  private md: T;
  private lg: T;
  private xl: T;

  constructor(xs: T, sm: T, md: T, lg: T, xl: T) {
    this.xs = xs;
    this.sm = sm;
    this.md = md;
    this.lg = lg;
    this.xl = xl;
  }

  getValue(currentWidthBreakpoint: WidthBreakpoint): T {
    if (currentWidthBreakpoint === WidthBreakpoint.WIDTH_XS) {
      return this.xs;
    }
    if (currentWidthBreakpoint === WidthBreakpoint.WIDTH_MD) {
      return this.md;
    }
    if (currentWidthBreakpoint === WidthBreakpoint.WIDTH_SM) {
      return this.sm;
    }
    if (currentWidthBreakpoint === WidthBreakpoint.WIDTH_LG) {
      return this.lg;
    }
    return this.xl;
  }
}

// 使用示例
const columns: BreakpointType<number> = new BreakpointType<number>(1, 2, 3, 4, 6);
// Grid({ columnsTemplate: '1fr '.repeat(columns.getValue(currentBp)).trim() })
```

### 模式 2：SessionID 防竞态

**作用**：用户快速切换页面/视频时，旧的异步操作返回后可能覆盖新状态。全局递增 sessionId + 关键点守卫检查。

```typescript
// [API 23+] SessionID 防竞态守卫
class AsyncManager {
  private globalSessionId: number = 0;
  private activeSessionId: number = -1;

  /// 开始新操作时调用，返回当前 sessionId
  bumpSession(): number {
    this.globalSessionId++;
    this.activeSessionId = this.globalSessionId;
    return this.activeSessionId;
  }

  /// 检查 sessionId 是否仍有效
  isSessionActive(sessionId: number): boolean {
    return sessionId === this.activeSessionId;
  }

  /// 异步操作，关键步骤都检查 session 有效性
  async doAsyncOperation(sessionId: number): Promise<void> {
    if (!this.isSessionActive(sessionId)) {
      return; // 已过期，丢弃
    }
    // 模拟异步：网络请求 / 文件读取 / 数据计算
    await new Promise<void>((resolve) => setTimeout(() => resolve(), 500));
    if (!this.isSessionActive(sessionId)) {
      return; // 等待期间又有新操作，丢弃旧结果
    }
    // 安全更新状态
  }
}
```

### 模式 3：WindowUtil + WindowInfo 完整窗口管理

**作用**：一站式封装窗口全周期管理——沉浸式切换、avoidArea 5 类型追踪、断点变化监听、分屏、窗口大小限制。

```typescript
// [API 23+] 沉浸式类型枚举
export enum ImmersiveType {
  NORMAL,              // 默认：状态栏+导航栏可见
  IMMERSIVE,           // 沉浸式：状态栏+导航栏透明覆盖
  FULLSCREEN_IMMERSIVE // 全屏沉浸式：隐藏状态栏+导航栏
}

// 窗口信息对象（@Observed 让组件监听变化）
@Observed
export class WindowInfo {
  public windowStatusType: window.WindowStatusType = window.WindowStatusType.UNDEFINED;
  public isImmersive: ImmersiveType = ImmersiveType.NORMAL;
  public windowSize: window.Size = { width: 0, height: 0 };
  public widthBp: WidthBreakpoint = WidthBreakpoint.WIDTH_XS;
  public heightBp: HeightBreakpoint = HeightBreakpoint.HEIGHT_SM;
  public avoidSystem?: window.AvoidArea;
  public avoidNavigationIndicator?: window.AvoidArea;
  public avoidCutout?: window.AvoidArea;
  public avoidSystemGesture?: window.AvoidArea;
  public avoidKeyboard?: window.AvoidArea;
}

export class WindowUtil {
  public mainWindow: window.Window;
  public mainWindowInfo: WindowInfo = new WindowInfo();

  constructor(mainWindow: window.Window) {
    this.mainWindow = mainWindow;
  }

  /// 设置沉浸式类型
  setImmersiveType(type: ImmersiveType): void {
    // NORMAL: setWindowLayoutFullScreen(false)
    // IMMERSIVE: setWindowLayoutFullScreen(true) + setWindowDecorVisible(false)
    // FULLSCREEN_IMMERSIVE: 全屏隐藏，maximize()
  }

  /// 初始化窗口信息并注册监听
  updateWindowInfo(): void {
    // 获取初始窗口状态、尺寸、断点、5 类 avoidArea
    // 注册：windowStatusChange / windowSizeChange（同时更新断点）/ avoidAreaChange
  }

  /// 释放监听
  release(): void {
    this.mainWindow.off('windowStatusChange', ...);
    this.mainWindow.off('windowSizeChange', ...);
    this.mainWindow.off('avoidAreaChange', ...);
  }

  /// 设置分屏
  setSplitScreen(bundleName: string, abilityName: string, moduleName: string): void {
    let want: Want = { bundleName, abilityName, moduleName };
    let option: StartOptions = { windowMode: AbilityConstant.WindowMode.WINDOW_MODE_SPLIT_PRIMARY };
    (this.mainWindow.getUIContext().getHostContext() as common.UIAbilityContext)
      .startAbility(want, option);
  }
}
```

### 模式 4：InputSecurityUtil 输入安全校验

**作用**：清除控制字符 + 长度截断，防止 XSS 和编码注入。

```typescript
// [API 23+] InputSecurityUtil.ets
export class InputSecurityUtil {
  private static readonly MAX_INPUT_LENGTH: number = 50;

  /// 清除 ASCII 控制字符（0-31 和 127）+ 长度截断
  static sanitizeSearchInput(raw: string): string {
    const normalized: string = raw.replace(/[\u0000-\u001F\u007F]/g, '');
    return normalized.slice(0, InputSecurityUtil.MAX_INPUT_LENGTH);
  }
}

// 使用：TextInput({ placeholder: '搜索' })
//   .onChange((v: string) => { this.keyword = InputSecurityUtil.sanitizeSearchInput(v); })
```

### 模式 5：canIUse + foldStatusChange 折叠屏适配

**作用**：运行时检测折叠屏能力，非折叠设备优雅降级；监听折叠状态联动全屏和布局。

```typescript
// [API 23+] 折叠屏适配
import { display } from '@kit.ArkUI';

@Component
struct FoldAwareView {
  @State isHalfFolded: boolean = false;

  aboutToAppear(): void {
    if (canIUse('SystemCapability.Window.SessionManager')) {
      try {
        if (display.isFoldable()) {
          // 获取折痕区域，存入共享状态供避让使用
          let creaseRegion = display.getCurrentFoldCreaseRegion();
          AppStorage.setOrCreate('creaseHeight',
            this.getUIContext().px2vp(creaseRegion.creaseRects[0].height));
          // 监听折叠状态
          display.on('foldStatusChange', this.onFoldStatusChange);
        }
      } catch (error) { /* 非折叠屏设备静默降级 */ }
    }
  }

  aboutToDisappear(): void {
    if (canIUse('SystemCapability.Window.SessionManager')) {
      try { display.off('foldStatusChange'); } catch (error) { }
    }
  }

  private onFoldStatusChange = (data: display.FoldStatus): void => {
    if (data === display.FoldStatus.FOLD_STATUS_HALF_FOLDED) {
      this.isHalfFolded = true;
      // 半折叠态：自动全屏播放
    } else {
      this.isHalfFolded = false;
      // 展开/折叠态：恢复标准布局
    }
  };
}
```

### 模式 6：UIObserver 应用埋点框架

> 基于 UIObserver 能力（API 12+），可监听点击、曝光、页面切换、渲染性能等全部用户行为。这是生产级埋点 SDK 的 ArkTS 最小实现。

**核心 API 链**：`uiContext.getUIObserver().on(eventName, callback)` — 在 Ability 的 `onWindowStageCreate` 中一次注册，全局生效。

```typescript
// [API 23+] UIObserver 埋点注册（在 EntryAbility.onWindowStageCreate 中）
import { hiAppEvent, hilog } from '@kit.PerformanceAnalysisKit';
import { FrameNode, uiObserver } from '@kit.ArkUI';

onWindowStageCreate(windowStage: window.WindowStage): void {
  windowStage.loadContent('pages/HomePage', () => {
    const uiContext: UIContext = windowStage.getMainWindowSync().getUIContext();

    // 1. 点击埋点（组件级别精度）
    uiContext.getUIObserver().on('willClick', (_event: ClickEvent, node?: FrameNode) => {
      // node.getId() → 组件 ID（.id('button-1') 设置的）
      // node.getUniqueId() → 全局唯一 ID
      // node.getCustomProperty(key) → 自定义业务数据
      // uiContext.getPageInfoByUniqueId(uniqueId) → 获取所在页面信息
      let eventParams: Record<string, string | number> = {
        'component_id': node?.getId() ?? '',
        'pageInfo': JSON.stringify(uiContext.getPageInfoByUniqueId(node?.getUniqueId()) ?? {}),
        'trackData': JSON.stringify(node?.getCustomProperty(node?.getId()) ?? {})
      };
      // 上报到 hiAppEvent
      hiAppEvent.write({ domain: 'user_action', name: 'click',
        eventType: hiAppEvent.EventType.BEHAVIOR, params: eventParams });
    });

    // 2. 滚动埋点（曝光时长分析）
    uiContext.getUIObserver().on('scrollEvent', (info: uiObserver.ScrollEventInfo) => {
      // info.scrollEvent: SCROLL_START / SCROLL_STOP / SCROLL_END
    });

    // 3. Navigation 页面切换埋点
    uiContext.getUIObserver().on('navDestinationSwitch', (info: uiObserver.NavDestinationSwitchInfo) => {
      // 可获取页面路径、入参、目标页面 name
    });

    // 4. Router 页面更新埋点
    uiContext.getUIObserver().on('routerPageUpdate', (info: uiObserver.RouterPageInfo) => {
      // 可获取 router 跳转的页面信息
    });

    // 5. 渲染性能埋点（页面启动耗时）
    uiContext.getUIObserver().on('willDraw', () => { startTime = Date.now(); });
    uiContext.getUIObserver().on('didLayout', () => { endTime = Date.now(); });
    // 页面渲染耗时 = endTime - startTime
  });
}

// 组件端埋点声明（在页面组件中）
Button('点击埋点')
  .id('button-1')                    // ← 埋点用的组件 ID
  .customProperty('button-1', { id: 'button-1', bizType: 'submit' })  // ← 自定义业务数据
  .onClick(() => { /* 业务逻辑 */ })
```

**组件曝光埋点**（配合 `TrackNode` 包装组件）：
```typescript
// 用 onDidBuild 生命周期获取 FrameNode
@Component
export struct TrackNode {
  @BuilderParam closer: VoidCallback;  // 要包装的内容
  track: Track;
  onDidBuild(): void {
    let uid: number = this.getUniqueId();
    let node: FrameNode | null = this.getUIContext().getFrameNodeByUniqueId(uid);
    // 注册可见区域变化回调
    node?.commonEvent.setOnVisibleAreaApproximateChange(
      { ratios: [0, 0.5, 1], expectedUpdateInterval: 500 },
      (ratioInc: boolean, ratio: number) => {
        // ratio: 0 → 不可见, 0.5 → 半可见, 1 → 完全可见
        hiAppEvent.write({ domain: 'exposure', name: 'component_visible', ... });
      });
  }
}
// 使用：TrackNode({ track: new Track().id('WaterFlow-1') }) { AnyComponent() }
```

---

## 🔄 事件总线与跨组件通信

### Emitter（全局事件派发）
```typescript
import { emitter } from '@kit.BasicServicesKit';

// 订阅事件
emitter.on({ eventId: 'user_login' }, (event) => {
  console.info('用户登录:', event.data?.userName);
});

// 发送事件
emitter.emit({ eventId: 'user_login' }, { data: { userName: 'admin' } });

// 一次性订阅
emitter.once({ eventId: 'app_init' }, () => { /* 只执行一次 */ });

// 取消订阅
emitter.off('user_login');

// 带延迟的事件
emmitter.emit({ eventId: 'data_loaded', priority: emitter.EventPriority.HIGH });
// LOW / HIGH / IMMEDIATE 三种优先级
```

### @Provide/@Consume（组件树内事件）
```typescript
// 已在 MVVM 章节覆盖，此处仅作对照
// @Provide 提供值，@Consume 消费值，跨任意层级传递
// 适合：主题切换、用户登录态、全局配置
```

### 选择建议
| 场景 | 方案 |
|------|------|
| 组件树内跨层级（3-5层） | `@Provide/@Consume` |
| 跨页面/跨 Ability | `Emitter` |
| 全局持久化状态 | `AppStorage` / `PersistentStorage` |
| 跨进程通信 | `IPCKit`（`@kit.IPCKit`） |

---

# 第四部分：性能优化（TaskPool、组件复用、流畅刷新、启动框架）

## 🚀 TaskPool 生产级并发模式

> 源自 arkts-patterns v2.3.1 生产级模式库。TaskPool 是 API 12+ 推荐的多线程方案。

### 基本使用模式

```typescript
import { taskpool } from '@kit.ArkTS';

// 1. 定义任务函数（必须 @Concurrent + 全局函数）
@Concurrent
function computeHeavyTask(data: number[]): number {
  // CPU 密集型计算，运行在独立 worker 线程
  return data.reduce((a, b) => a + b, 0);
}

// 2. 在 UI 线程调用
async runTask(): Promise<void> {
  try {
    const task = new taskpool.Task(computeHeavyTask, [1, 2, 3, 4, 5]);
    const result: number = await taskpool.execute(task) as number;
    console.info(`Result: ${result}`);
  } catch (err) {
    console.error(`Task failed: ${err.message}`);
  }
}
```

### 高级模式：长时任务+进度回调

```typescript
@Concurrent
function longRunningTask(data: number[], callback: taskpool.Callback): number {
  let total = 0;
  for (let i = 0; i < data.length; i++) {
    total += data[i];
    // 通知主线程进度
    callback.call(i / data.length);
  }
  return total;
}

// 创建带优先级的 Task
const task = new taskpool.Task(longRunningTask, [dataArray]);
task.setPriority(taskpool.Priority.HIGH);
```

### TaskPool vs Worker 选择

| 场景 | 推荐方案 | 原因 |
|:----:|:--------:|:----|
| 简短计算（<1s） | TaskPool | 自动线程池管理，开销小 |
| 长时后台服务 | Worker | 常驻线程，独立生命周期 |
| 需要频繁通信 | Worker | 支持双向消息推送 |
| MindSpore 推理 | TaskPool | 内部已用线程池，避免冲突 |
| 文件 I/O | Worker | 避免阻塞 UI 和线程池 |

## 🧩 UI 组件深度（WaterFlow + GridHybrid + FluentBlog + ContentPublisher + AnimationCollection）

### WaterFlow — 瀑布流全能力

```typescript
WaterFlow() {
  LazyForEach(this.dataSource, (item: ItemData) => {
    FlowItem() {
      Column() {
        Image(item.img).width('100%').aspectRatio(item.ratio)
        Text(item.title).fontSize(14)
      }
    }
  }, (item) => item.id)
}
.columnsTemplate('1fr 1fr')           // 双列
.sections(this.sections)              // 混合排列（不同列数区域）
.nestedScroll({ scrollForward: 1, scrollBackward: 1 })
.onReachEnd(() => this.loadMore())    // 无限加载
.cachedCount(8)
```

### ContentPublisher — RichEditor 富文本

```typescript
RichEditor({ controller: this.editorCtrl })
  .onReady(() => {
    // 插入文本
    this.editorCtrl.insertTextSpan({ text: 'Hello HarmonyOS!' });
    // 插入图片
    this.editorCtrl.insertImageSpan({ uri: 'data/img.png' });
    // 获取 HTML
    const html = this.editorCtrl.toHtml();
  })
```

### AnimationCollection — 动效集合

```typescript
// 显式动画
animateTo({ duration: 300, curve: Curve.EaseOut }, () => {
  this.opacity = 1;
  this.scale = { x: 1.2, y: 1.2 };
});
// 属性动画
Image().animation({ duration: 500, iterations: -1 })
  .rotate({ angle: 360 }) // 无限旋转
```

---

## ⚡ AppStartUp 启动任务框架（第三轮新增）

> **来源**：`AppStartUp` | Gitee harmonyos_samples | 源码级

基于 `@kit.AbilityKit` 的 **AppStartup** 框架，支持同步/异步初始化任务解耦。

### 工作流
```
startup_config.json → startupManager.run → StartupTask(自动/手动) → 任务完成
```

### 工程目录

```
entry/src/main/ets/startup/
├── StartupConfig.ets        # 启动参数配置
├── FileTask.ets              # 文件读写
├── ImageKinfeTask.ets        # 图片框架初始化
├── KvManagerUtilTask.ets     # 分布式数据库
├── KVStoreTask.ets           # KV 写入
├── RdbStoreTask.ets          # 关系型数据库
└── ResourceManagerTask.ets   # resource 资源
```

### 配置文件

```json5
// resources/base/profile/startup_config.json
{
  "startupTasks": [
    { "name": "KvManagerUtilTask", "dependencies": [] },
    { "name": "KVStoreTask", "dependencies": ["KvManagerUtilTask"] },
    { "name": "RdbStoreTask", "dependencies": [] }
  ]
}
```

### 手动模式启动

```typescript
// [API 23+] 手动执行初始化任务
import { startupManager } from '@kit.AbilityKit'

Button('手动初始化')
  .onClick(async () => {
    await startupManager.run('RdbStoreTask')
    console.info('Manual Task execute success')
  })
```

---

## ♻️ ComponentReuse 组件复用（第三轮新增）

> **来源**：`component-reuse` | Gitee harmonyos_samples | 源码级

### 两种复用场景

| 场景 | 技术方案 | 说明 |
|------|---------|------|
| 同一列表内复用 | `@Reusable` + `aboutToReuse()` | 列表项结构相同或不同时复用 |
| 多列表间复用 | `NodeContainer` 占位 + `NodePool` 全局缓存 | 不同父组件间子组件共享 |

### @Reusable 代码模式

```typescript
// [API 23+] @Reusable 组件复用
@Component
@Reusable
struct ReusableItem {
  @State text: string = ''

  // 复用时的生命周期回调
  aboutToReuse(params: Record<string, Object>) {
    this.text = params.text as string
  }

  build() {
    Row() {
      Text(this.text).fontSize(16)
    }
    .padding(12)
  }
}
```

### NodePool 跨列表复用

```typescript
// [API 23+] NodePool 全局缓存复用池
import { BuilderNode, NodeContainer, NodePool } from '@kit.ArkUI'

// 全局缓存复用池
const nodePool: NodePool = new NodePool()

// 从池中获取或创建
let node = nodePool.get() ?? new BuilderNode(null)
// 使用 node 绑定到 NodeContainer
```

---

## 📖 FluentBlog 流畅刷低功耗（第四轮新增）

> **来源**：`fluent-blog` | Gitee harmonyos_samples | 源码级

通过 `animateTo` 设置 `ExpectedFrameRateRange` 控制屏幕刷新率来平衡功耗：

```typescript
// [API 23+] 设置期望帧率
animateTo({
  duration: 300,
  expectedFrameRateRange: { min: 30, max: 60, preferred: 30 }
}, () => { /* 动画内容 */ })
```

---

# 第五部分：动画与手势（动画系统、手势、转场）

## 🎨 动画系统速查

| 动画类型 | API | 说明 |
|---------|-----|------|
| **属性动画** | `animateTo({duration, curve, delay}, () => { 改属性 })` | 最常用，让属性变化平滑过渡 |
| **关键帧动画** | `keyframeAnimateTo([{duration, curve, event:()=>{}}, ...])` | 分段控制，多段动画串行 |
| **显式动画** | `@AnimatableExtend` 自定义可动画属性 | 实现复杂非标准属性动画 |
| **转场动画** | `transition({ type: TransitionType, opacity, translate })` | 组件出现/消失动效 |
| **页面转场** | Navigation 自带 NavTransition | 页面跳转动效（滑入/淡入等） |
| **弹簧动画** | `springMotion(响应速度, 阻尼系数)` | 弹性效果，适合消息提醒、点赞 |

### 核心参数
- `duration`: 时长（ms），常用 200~500ms
- `curve`: 曲线类型 — `Curve.Linear`(匀速)、`Curve.EaseIn`(慢→快)、`Curve.EaseOut`(快→慢)、`Curve.EaseInOut`(慢→快→慢，最自然)
- `delay`: 延迟启动（ms）
- `iterations`: 播放次数，`-1` 为无限循环

### 链式动画
```typescript
// 一个结束接另一个
animateTo({ duration: 300 }, () => { this.x = 100 })
  .then(() => animateTo({ duration: 300 }, () => { this.rotate = 90 }));
```

### 常见坑点
- ❌ 全局 `animateTo()` 已废弃 → ✅ `this.getUIContext().animateTo()`
- ❌ 不要用 UIAbility 跳转代替模态弹窗 → ✅ 用 `ModalTransition` + 自定义弹窗
- ❌ 别忘了为列表项自定义动画曲线 → ✅ 用 `springMotion` 提升滚动手感

---

## 🖐️ 手势系统速查

### 手势分类
| 类型 | 手势 | 说明 |
|------|------|------|
| **点击类** | `TapGesture({ count: 1 })` | 单击/双击，count 为点击次数 |
| **长按类** | `LongPressGesture({ duration: 500 })` | 长按触发，duration 为最小按压时长(ms) |
| **拖拽类** | `PanGesture({ direction: PanDirection.Horizontal })` | 拖拽平移，支持方向限制 |
| **滑动类** | `SwipeGesture({ speed: 100 })` | 快速滑动识别 |
| **捏合类** | `PinchGesture({ distance: 5 })` | 双指缩放，distance 最小识别距离 |
| **旋转类** | `RotationGesture({ angle: 1 })` | 双指旋转 |

### 绑定方式
```typescript
// 单个手势
.gesture(TapGesture({ count: 1 }).onAction((e) => { /* 单击 */ }))

// 多手势并行（同时识别）
.gesture(
  GestureGroup(GestureMode.Parallel,
    TapGesture().onAction(() => {}),
    PanGesture().onActionStart(() => {})
  )
)

// 多手势互斥（只识别一个）
.gesture(
  GestureGroup(GestureMode.Exclusive,
    TapGesture().onAction(() => {}),
    LongPressGesture().onAction(() => {})
  )
)
```

### 手势事件回调
| 回调 | 触发时机 |
|------|---------|
| `.onAction(event)` | 手势识别成功 |
| `.onActionStart(event)` | 手势开始 |
| `.onActionUpdate(event)` | 手势进行中（拖拽时持续触发） |
| `.onActionEnd(event)` | 手势结束 |
| `.onActionCancel()` | 手势取消 |

### 手势冲突解决策略
| 策略 | 说明 | 实现方式 |
|------|------|---------|
| **Parallel** | 父子/兄弟手势同时响应 | `GestureMode.Parallel` |
| **Exclusive** | 只识别优先级最高的一个 | `GestureMode.Exclusive` |
| **Sequence** | 手势按顺序触发 | `GestureMode.Sequence`（如先长按再拖拽） |
| **priority** | 子组件优先处理 | `.priorityGesture(TapGesture())` 替代 `.gesture()` |

### 常用组合场景
```typescript
// 拖拽跟手
.gesture(PanGesture()
  .onActionUpdate((e: GestureEvent) => {
    this.offsetX = e.offsetX;  // 实时偏移量
  })
  .onActionEnd(() => {
    animateTo({ curve: Curve.Spring }, () => {
      this.offsetX = 0;  // 松手回弹
    });
  })
)

// 点击+拖拽（滑动翻页）
.gesture(
  GestureGroup(GestureMode.Parallel,
    TapGesture().onAction(() => this.jumpPage()),
    PanGesture({ direction: PanDirection.Horizontal })
      .onActionEnd((e) => {
        if (e.offsetX < -50) this.nextPage();
      })
  )
)
```

---

## 🎬 AnimationCollection 动画全集（第三轮新增）

> **来源**：`animation-collection` | Gitee harmonyos_samples | 源码级

17种常见动效，按功能域组织：

| 模块 | 动效 | 核心实现 |
|------|------|---------|
| **翻转动效** | pageTurningAnimation | 3D 卡片翻转 |
| **标题下拉** | pageExpandTitle | `animateTo` + 顶部偏移 |
| **状态栏显隐** | pageStatusBarChange | 滚动监听 + 渐隐渐现 |
| **水波纹** | pageWaterRipples | 逐层放大 + 透明度渐减 |
| **列表滑动** | pagelistslidetohistory | 滑动阻尼 + 回弹 |
| **跑马灯** | pageMarqueeView | `marquee()` 属性 |
| **Swiper高度变化** | swipersmoothvariation | Swiper 动态高度 |
| **自定义进度** | pagePaintComponent | Canvas + 弧形路径 |
| **数字滚动** | digitalscrollanimation | 数字逐位翻转 |
| **卡片预览** | pageCardsSwiper | Swiper + Scale 放大 |
| **投票动效** | votingcomponent | 柱形图动画填充 |
| **语音录制动效** | voiceRecordDynamicEffect | 声波动画 |
| **抖动动效** | pageVibrateEffect | 弹簧曲线动画 |
| **侧边栏淡入淡出** | sidebarAnimation | `opacity` 过渡 |
| **多层级轮播** | swiperComponent | Swiper 嵌套 |
| **搜索** | searchComponent | Navigation + 模糊查询 |

### 性能要点
- Navigation 做导航容器，List 做功能列表
- 每个动效独立 feature 目录，互相解耦

---

## 🌀 TransitionsCollection 转场动画全集（第三轮新增）

> **来源**：`transitions-collection` | Gitee harmonyos_samples | 源码级

### 七大转场类型

| 类型 | 动效 | 核心技术 |
|------|------|---------|
| **多模态页面转场** | 半模态 + 全屏 + 左右切换 | `bindSheet` + `bindContentCover` + `TransitionEffect.asymmetric()` |
| **搜索一镜到底** | 搜索框放大过渡 | `geometryTransition` 绑定同一 id |
| **卡片一镜到底** | 瀑布流卡片 → 详情 | `customNavContentTransition` + `componentSnapshot` |
| **图片一镜到底** | 双指放大/查看大图/半模态 | `NodeContainer` 跨节点迁移 / `geometryTransition` |
| **视频一镜到底** | 封面 → 播放 | `customNavContentTransition` + `NodeController` |
| **列表一镜到底** | 列表项 → 详情 | `geometryTransition` + 显式动画 |
| **图书翻页** | 封面 → 内页 | `customNavContentTransition` 自定义转场 |

### geometryTransition 核心代码

```typescript
// [API 23+] 一镜到底过渡
@State isOpen: boolean = false

Column() {
  if (!this.isOpen) {
    Image(this.src)
      .geometryTransition('sharedImage')
      .onClick(() => { this.isOpen = true })
  }
  if (this.isOpen) {
    Image(this.src)
      .geometryTransition('sharedImage')
      .width('100%').height('100%')
  }
}
.animation({ duration: 300, curve: Curve.Friction })
```

---

## ✨ TextEffects 文字特效（第十轮收尾②）

> **来源**：`text-effects` | ⭐30 Stars | Gitee harmonyos_samples | 源码级

基于 Text 组件及通用属性实现多种文字特效。

```typescript
// [API 23+] 文字特效
Text('特效文字')
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#FF6B81')
  .textShadow({
    radius: 10,
    color: '#FF6B81',
    offsetX: 0,
    offsetY: 0
  })
  .blur(0.5)           // 模糊
  .opacity(0.9)        // 透明度
  .rotate({ x: 0, y: 1, z: 0, angle: 15 })  // 3D旋转
```

---

# 第六部分：测试与调试（测试体系、DevEco、HDC、应用生命周期）

## 🛠️ DevEco Studio 调试与性能优化

### DevEco Profiler 性能分析
- **入口**：View → Tool Windows → Profiler（或底部工具栏 Profiler 按钮 / Ctrl+Shift+A 搜索 "Profiler"）
- **仅支持真机**：不支持模拟器调优，使用 USB 或无线方式连接设备
- **核心采集指标**：CPU 使用率、内存分配、启动耗时、线程状态、网络请求耗时
- **泳道视图**：Top-Down 设计，数据由浅到深展示，可深入函数热点和 CPU 调度细节

### ArkTS 高性能编程实践

#### 声明与表达式
| 实践 | 说明 | 示例 |
|------|------|------|
| 用 const 声明不变变量 | 避免不必要的运行时重绑定 | `const index = 10000;` |
| number 避免整浮混用 | 初始化后不要改变数据类型 | `let n = 1;` 不要后面赋值为 `n = 1.1` |
| 避免数值溢出 | 加减乘除幂运算应避免超过 INT32_MAX/INT32_MIN | 数值保持在 ±2147483647 以内 |
| 循环中常量提取 | 将循环中不变的值提出来，减少属性访问 | `const info = obj.arr[idx]; for(...)` |

#### 函数优化
- **避免闭包**：性能敏感场景用参数传递替代闭包访问外部变量
- **避免可选参数**：优先用默认参数替代 `?` 可选参数，减少非空判断开销
- **数组建议用 TypedArray**：纯数值计算场景用 `Int8Array`、`Float64Array` 等
- **避免稀疏数组**：数组大小超过 1024 或 `result[9999] = 0` 会触发 hash 存储，访问变慢
- **避免联合类型数组**：按类型拆分为 `arrInt`、`arrDouble`、`arrString`

#### 异常与错误处理
- **避免频繁抛出异常**：循环中先拦截异常场景，再调业务函数，而非 try/catch 包裹循环

#### 异步并发模型
| 方案 | 适用场景 | 说明 |
|------|---------|------|
| async/await | 常规异步任务（网络请求、文件读写） | 主线程执行，不阻塞 UI |
| TaskPool | CPU 密集型任务（图像处理、数据计算） | 多线程并行，推荐用于密集型计算 |
| Worker | 长时间运行的后台任务（流处理、大量数据） | 独立线程，适合持续性任务 |

### LazyForEach 懒加载
- **适用**：长列表渲染，只渲染可视区域内的项
- **keyGenerator 必传**：为每个数据项生成唯一键，帮助框架精准识别增删改
- **dataSource 实现 IDataSource**：需要实现 `totalCount`、`getData`、`registerDataChangeListener`、`unregisterDataChangeListener` 四个方法
- **配合 @Reusable 复用组件**：列表项组件使用 `@Reusable` 装饰器进一步提升滚动性能

---

## 🤖 DevEco Code & DevEco CLI（HDC 2026 新工具）

### 工具定位

| 工具 | 包名 | 本质 | 适用场景 |
|:----:|:----:|:----:|:--------|
| **DevEco Code** | `@deveco/deveco-code` | AI Agent 对话式工具 | 自然语言驱动编码/构建/调试全流程 |
| **DevEco CLI** | `@deveco/deveco-cli` | 命令行工具集 | 封装 hvigor/hdc/ohpm 原子能力供 AI Agent 调用 |

> DevEco Code = 自带 AI 大脑的"自动驾驶"开发伙伴；DevEco CLI = 供已有 AI Agent 调用的"鸿蒙能力工具箱"

### DevEco Code 安装与启动

```bash
npm install -g @deveco/deveco-code
cd your-harmonyos-project
deveco-code
```

### 三种 Agent 模式

| 模式 | 说明 | 适用场景 |
|:----:|:----:|:--------|
| **Build** | 默认 Agent，完整读写权限 | 日常开发、Bug 修复、功能实现 |
| **Plan** | 只读 Agent，代码分析+方案规划 | 探索陌代码库、设计重构方案 |
| **Goal** | 端到端自动驾驶：拆解任务→编码→编译→部署→自修复 | 按需求全自动交付功能 |

### 内置 HarmonyOS 专属工具

| 工具 | 功能 | 等价传统命令 |
|:----:|:----:|:-----------:|
| `build_project` | 编译构建 | `hvigorw assembleHap` |
| `start_app` | 模拟器/真机运行 | `hdc install` + `hdc shell aa start` |
| `hdc_log` | 设备日志收集/清理 | `hdc shell hilog` |
| `verify_ui` | 自然语言 UI 验证 | 手动操作+截图对比 |
| `check_ets_files` | ArkTS 静态语法检查 | DevEco Studio ArkTS-Check |
| `arkts_knowledge_search` | HarmonyOS 知识库检索 | 官网文档/API Reference |

### DevEco CLI 常用命令

```bash
deveco init -n AppName -t app -s default     # 创建工程
deveco ohpm install                            # 同步依赖
deveco build --mode module --module-name entry # 构建模块
deveco build --mode release --sign-config ./sign/autoSign.json # Release 包
deveco --version                               # 版本检查
```

### 模型配置

内置免费提供 GLM-5.1 模型，通过 Ctrl+A 支持接入 DeepSeek / OpenAI / 任意 OpenAI 兼容 Provider。

```json
// deveco.jsonc
{
  "provider": {
    "deveco": {
      "name": "DevEco Code",
      "models": { "glm-5": { "tool_call": true, "limit": { "context": 200000, "output": 8192 } } },
      "options": { "baseURL": "https://api.openbitfun.com/v1", "apiKey": "{env:DEVECO_API_KEY}" }
    }
  }
}
```

### 前置条件
- Node.js 22+
- DevEco Studio 6.1+（可选，但构建/推包需要）
- 设置 `DEVECO_HOME` 环境变量指向 DevEco Studio 安装目录

---

## 🧪 测试体系

| 测试类型 | 框架 | 说明 |
|---------|------|------|
| **单元测试** | JsUnit（`@ohos.unittest`） | 测试函数/类逻辑，在 ohosTest 目录下编写 |
| **UI 自动化测试** | Hypium（`@ohos.test.uitest`） | 基于 ArkUI 的 UI 操作模拟、断言 |
| **性能测试** | DevEco Testing | 内存泄漏、启动耗时、帧率检测 |
| **专项测试** | 云调试 + 远程真机 | 兼容性、稳定性、压力测试 |

### 单元测试示例
```typescript
// ohosTest/entry/src/test/UserModelTest.ts
import { describe, it, expect } from '@ohos/hypium';
describe('UserModelTest', () => {
  it('calcAge_should_return_correct', 0, () => {
    const result = calcAge(1990);
    expect(result).assertEqual(36);
  });
});
```

### UI 自动化测试（Hypium）示例
```typescript
import { Driver, ON, Component } from '@ohos.test.uitest';
const driver = Driver.create();
await driver.findComponent(ON.text('登录')).click();
await driver.findComponent(ON.id('username')).inputText('admin');
await driver.findComponent(ON.text('确认')).click();
// 断言结果
const result = await driver.findComponent(ON.text('登录成功'));
expect(result).assertIsTrue();
```

### 测试流程建议
1. 开发阶段：JsUnit 覆盖核心业务逻辑
2. 功能稳定后：Hypium 覆盖核心 UI 流程
3. 提交前：DevEco Testing 跑一次性能基线
4. 多设备：AGC 云调试验证兼容性

---

## 🛡️ 应用异常处理（hiAppEvent）

> 基于官方 Sample `exception-handling`（2,829下载）。在线上环境，自动捕获崩溃和卡死事件是质量保障的基础能力。

### 核心 API：hiAppEvent

```typescript
import hiAppEvent from '@ohos.hiviewdfx.hiAppEvent';
```

### 订阅应用事件（崩溃 + 卡死）

```typescript
export function subscribeAppEvents(): void {
  hiAppEvent.addWatcher({
    name: "app_crash_watcher",
    appEventFilters: [
      {
        domain: hiAppEvent.domain.OS,
        names: [
          hiAppEvent.event.APP_CRASH,   // 应用崩溃
          hiAppEvent.event.APP_FREEZE   // 应用卡死
        ]
      }
    ],
    onReceive: (domain: string, appEventGroups: Array<hiAppEvent.AppEventGroup>) => {
      // 将事件数据存入应用级状态
      AppStorage.setOrCreate('appEventGroups', appEventGroups);
    }
  });
}
```

### 获取异常信息

```typescript
// 在组件中监听并解析
@StorageLink('appEventGroups') @Watch('parseCrashInfo')
appEventGroups: Array<hiAppEvent.AppEventGroup> = [];

async parseCrashInfo(): Promise<void> {
  if (!this.appEventGroups?.length) return;

  for (const group of this.appEventGroups) {
    for (const event of group.appEventInfos) {
      const params = event.params;
      const crashInfo: string =
        `领域: ${event.domain}\n` +
        `事件: ${event.name}\n` +
        `类型: ${event.eventType}\n` +
        `时间: ${params['time']}\n` +
        `崩溃类型: ${params['crash_type']}\n` +
        `前台/后台: ${params['foreground']}\n` +
        `版本: ${params['bundle_version']}\n` +
        `包名: ${params['bundle_name']}\n` +
        `异常详情: ${JSON.stringify(params['exception'])}\n`;
      // 存入懒加载数据源
      this.faultDataSource.pushData(crashInfo);
    }
  }
}
```

### 触发异常（用于测试）

```typescript
// 触发崩溃：解析非法 JSON
const result: object = JSON.parse('');     // APP_CRASH

// 触发卡死：无限循环
while (true) { }                           // APP_FREEZE
```

### 数据持久化（@ohos.data.preferences）

```typescript
import { preferences } from '@kit.ArkData';

// 存储
dataPreferencesManager.put('faultMessage',
  JSON.stringify(crashRecords), (err) => {
    if (!err) dataPreferencesManager.flush();
  });

// 读取
dataPreferencesManager.get('faultMessage', [])
  .then((data) => {
    const records: Array<string> = JSON.parse(data as string);
    // 恢复数据到懒加载数据源
  });
```

### 架构模式

```
订阅层（addWatcher）
  ↓
全局状态（AppStorage）
  ↓
组件监听（@StorageLink + @Watch）
  ↓
数据解析 → 懒加载数据源（LazyForEach DataSource）
  ↓
持久化（Preferences）
  ↓
UI 渲染（List + LazyForEach）
```

---

## 🔄 AppLifecycleManagement 应用生命周期（第三轮新增）

> **来源**：`AppLifecycleManagement` | Gitee harmonyos_samples | 源码级

### 四大能力

| 动作 | API | 说明 |
|------|-----|------|
| 前后台监听 | `ApplicationContext.on('applicationStateChange')` | 监听应用前后台切换 |
| 关闭 Ability | `UIAbilityContext.terminateSelf()` | 关闭当前 UIAbility |
| 关闭应用 | `ApplicationContext.killAllProcesses()` | 杀死应用的所有进程 |
| 重启应用 | `ApplicationContext.restartApp(restartWant)` | 重启 App |
| 切到后台 | `Window.minimize()` | 最小化窗口到后台 |

### 核心代码

```typescript
// [API 23+] 前后台状态监听
import { common } from '@kit.AbilityKit'

const ctx = getContext(this) as common.UIAbilityContext
const appCtx = ctx.getApplicationContext()

// 监听应用前后台切换
appCtx.on('applicationStateChange', (state: number) => {
  if (state === 0) { /* 前台 */ }
  if (state === 1) { /* 后台 */ }
})

// 重启应用
appCtx.restartApp({
  bundleName: 'com.example.app',
  abilityName: 'EntryAbility'
})
```

---


## 🎯 HarmonyOS 7 DFX 全线工具（9 项能力，API 26 Beta 新增）

> 以下 DFX（Design For X）能力是 API 26 Beta1 版本全新推出的诊断/调试/性能优化工具集。

### 1. ArkTS 内存快照聚类分析
将快照中的同类对象进行聚类分析，统计各泄漏对象的影响大小，定位内存泄漏问题。
- **场景**：内存泄漏排查 → 快照对比 → 聚类查看泄漏对象分布
- **入口**：DevEco Studio Profiler → ArkTS Memory → 聚类分析规则

### 2. JSLeakWatcher — ArkTS 内存泄漏定位利器
```typescript
import { jsLeakWatcher } from '@kit.PerformanceAnalysisKit';

// 对具有生命周期的 ArkTS 组件对象定期执行泄漏检测
const watcher = jsLeakWatcher.createWatcher();
watcher.on('leakDetected', (result) => {
  console.info(`泄漏对象: ${result.className}, 引用链: ${result.referenceChain}`);
});
watcher.start({ interval: 30000 }); // 每 30s 检测一次
```
- **场景**：页面关闭后检查是否有未释放的组件实例
- **模块**：`@kit.PerformanceAnalysisKit` → `jsLeakWatcher`

### 3. GlobalHandle + MemTrace — 资源泄漏自诊断
```typescript
import { hidebug } from '@kit.PerformanceAnalysisKit';

// 启动资源分配栈采集（线上运维）
hidebug.OHHiDebugStartProfiler({ type: 'globalHandle', duration: 60000 });
// 停止后通过 MemTrace 日志分析泄漏
hidebug.OHHiDebugStopProfiler();
```
- **模块**：`@kit.PerformanceAnalysisKit` → `hidebug`
- **API**：`OHHiDebugStartProfiler()` / `OHHiDebugStopProfiler()`（C API）

### 4. HiAppevent 退出原因订阅
```typescript
import { hiAppEvent } from '@kit.PerformanceAnalysisKit';

// 订阅 APP_KILLED 事件，获取应用上一次退出原因
hiAppEvent.on('APP_KILLED', (event) => {
  console.info(`退出原因: ${event.exitReason}, 时间: ${event.timestamp}`);
});

// 进一步分析故障根因：订阅 CRASH / FREEZE 并关联同一次故障
hiAppEvent.on('APP_CRASH', (event) => {
  console.info(`crash info: ${event.crashStack}, uniqueId: ${event.appRunningUniqueId}`);
});
```
- **用途**：聚类分析应用非预期退出，关联 crash/freeze 日志定位根因
- **模块**：`@kit.PerformanceAnalysisKit` → `hiAppEvent`

### 5. AppFreeze 增强日志
- APP_INPUT_BLOCK 超时阈值调整为 **8 秒**
- 主线程采样：THREAD_BLOCK_3S 发生时，每 300ms 采集一次调用栈（最多 10 次）
- **配置开启**：在 `module.json5` 中开启主线程采样，订阅 APP_FREEZE 事件
```typescript
hiAppEvent.on('APP_FREEZE', (event) => {
  // event.threadStacks: 包含多个采样点的调用栈信息
  // event.cpuUsage: CPU 使用率
  // event.mainThreadDuration: 主线程运行时长
  console.info(`阻塞详情: ${JSON.stringify(event.threadStacks)}`);
});
```

### 6. Profiler 跨语言内存分析
- **新增**：Native 持有 ArkTS 内存泄露分析（LocalHandle + GlobalHandle 两种句柄）
- **能力**：抓取并展示关联 ArkTS 对象的 Native 分配栈
- **入口**：DevEco Profiler → Memory → 跨语言分析

### 7. GWPAsan 越界检测工具
运维态地址越界检测，定位**释放后使用、堆溢出、重复释放、非法释放**等踩内存问题。
- **特点**：无需插桩、采样监控、性能开销 < 5%、适合现网大规模运行
- **配置**：支持开启概率、采样率、slot 数、可恢复模式
- **使用**：订阅地址越界事件获取故障日志（报错栈/申请栈/释放栈）
```typescript
// 在 module.json5 中配置 GWPAsan
// "gwpAsan": {
//   "enabled": true,
//   "samplingRate": 0.01,
//   "maxSlots": 16,
//   "recoverable": true
// }
```

### 8. AI 辅助稳定性诊断
- AI 自动分析故障日志，定位稳定性问题根因
- 小红书已作为首批生态"样板间"接入
- **入口**：DevEco Studio → Stability Diagnosis

### 9. HandleScope 自动处理（NDK）
```cpp
// C/C++ 代码中调用
OH_JSVM_EnableLocalHandleDetection(jsvm_env env, bool enable);
```
- 启用后，系统在 libuv 和 EventRunner 的异步回调中自动添加 scope 管理 `napi_value` 生命周期
- 减少手动 HandleScope 遗漏导致的引用泄漏
- **适用**：NDK 开发，特别是频繁使用 napi 回调的场景



---## 🏗️ hvigorw 构建系统速查

> 命令行构建神器，**CI/CD 和脱离 IDE 打包必备**。

### 核心构建命令

```bash
# ▸ 打包类型
hvigorw assembleHap              # 构建 HAP（调试包，默认）
hvigorw assembleHap -p buildMode=release   # 构建 release HAP
hvigorw assembleApp -p buildMode=release   # 构建 APP（上架用）
hvigorw assembleHar                         # 构建 HAR 共享库
hvigorw assembleHsp                         # 构建 HSP 共享包

# ▸ 模块级构建（只编译改动的模块，加速）
hvigorw assembleHap --mode module -p module=entry@default

# ▸ 清理
hvigorw clean assembleHap                   # 先清理再构建

# ▸ 测试
hvigorw onDeviceTest -p module=entry        # 真机测试
hvigorw test -p module=entry                # 本地测试（无需设备）
```

### CI/CD 关键配置

```bash
# 环境变量（CI 服务器）
export NODE_HOME=/path/to/command-line-tools/tool/node
export JAVA_HOME=/path/to/jdk
export PATH=$NODE_HOME/bin:$JAVA_HOME/bin:/path/to/command-line-tools/bin:$PATH
export OHOS_SDK=/path/to/command-line-tools/sdk

# 安装依赖
ohpm install --all

# 构建（CI 推荐 --no-daemon）
hvigorw assembleHap -p buildMode=debug --no-daemon

# 签名：通过环境变量注入密码，build-profile.json5 中配置
# 或通过 hvigorfile.ts 读取 process.env.SIGNING_PASSWORD
```

### 编译优化参数

| 参数 | 说明 |
|:----|:------|
| `--no-daemon` | CI 环境推荐，避免 daemon 缓存问题 |
| `--incremental` | 增量编译（默认开启），只编译改动文件 |
| `--parallel` | 并行构建（默认开启），多模块同时编译 |
| `-d` / `--debug` | 开启 debug 日志，排查构建失败 |
| `--stacktrace` | 打印完整异常堆栈 |
| `--max-old-space-size=12345` | 调大 Node.js 内存（OOM 时使用） |
| `--analyze=normal` | 生成构建任务耗时分析 |

### API 26 新增构建配置

| 配置项 | 位置 | 说明 |
|:------|:----|:------|
| `apiCompatibilityCheck` | `build-profile.json5` → `strictMode` | 设置 ArkTS API 兼容性检测级别 |
| `tsImportSoCheck` | `build-profile.json5` → `tscConfig` | 编译时对 .ts 文件中导入 .so 的符号进行类型解析 |
| `enableSoDirCollection` | 模块级 `build-profile.json5` → `nativeLib` | ets 文件能否加载 libs/{ABI}/ 子目录下的 so 文件 |
| `getAllDependencyInfo()` | hvigorfile.ts | 获取工程或模块下所有依赖信息 |
| `syncNative` | DevEco Studio Settings 开关 | 提升 sync 阶段 C++ 编译效率 |

### DevEco Studio 26 新增 CLI 工具版本

| 工具 | API 26 版本 | 说明 |
|:----|:----------:|:-----|
| Command Line | 26.0.0.461 | 命令行工具集 |
| codelinter | 6.0.240 | 代码检查与修复 |
| hstack | 6.0.0 | release 混淆堆栈还原工具 |
| hvigorw | 6.26.1 | 编译构建（API 10+ 支持） |
| ohpm | 26.0.0.410 | 包管理 |
| Node.js | 24.14.1 | 运行时 |
| SDK | 26.0.0 Beta1 | OpenHarmony SDK 26.0.0.23 |

---


---

# 第七部分：安全与合规（权限、隐私、加密、认证、业务风险检测）

## 🔒 安全合规

### 权限模型（三层分级）
| 级别 | 说明 | 示例 | 申请方式 |
|------|------|------|---------|
| **normal** | 直接授予 | `ohos.permission.INTERNET` | 在 module.json5 声明即可 |
| **system_basic** | 弹窗确认 | `ohos.permission.LOCATION`、`ohos.permission.CAMERA` | 声明 + 运行时 `requestPermissionsFromUser` |
| **system_core** | 限制级 | 系统API，普通应用不可用 | 需 OEM 授权 |

### 敏感权限动态申请
```typescript
import { abilityAccessCtrl } from '@kit.AbilityKit';
const atManager = abilityAccessCtrl.createAtManager();
// 请求相机权限
atManager.requestPermissionsFromUser(this.context, [
  'ohos.permission.CAMERA'
]).then((data) => {
  if (data.authResults[0] === 0) { /* 权限已授予 */ }
});
```

### 数据安全
- **加密存储**：敏感数据用 EncryptedKVStore 或 HUKS（华为通用密钥库）加密
- **HTTPS 必用**：生产环境 `@ohos.net.http` 必须用 HTTPS，校验证书
- **最小权限原则**：只申请业务必需权限，不用不申
- **隐私政策**：申请敏感权限时，必须提供《隐私政策》弹窗说明用途

### 上架合规必查
- ✅ 隐私政策链接必填
- ✅ 敏感权限必须有说明文案
- ✅ 应用描述与功能一致，不夸大
- ✅ 未成年人保护（如涉及）

---

## 🔒 Enterprise Threat Protection Kit（2,240 下载）

> 源自 `@kit.EnterpriseThreatProtectionKit`，HarmonyOS 6.1.1 (API 24) 新增。为安全应用提供"穿透沙盒"的全系统文件扫描和隔离处置能力。**仅支持 PC/2in1 设备**。

### 核心 API 矩阵

| API | 功能 | 说明 |
|:----:|:----:|:------|
| `scanBundleFiles(targetType, callback)` | 扫描 BUNDLE/EL2 目录 | 分批次回调返回路径 |
| `openFile(path)` | 跨沙盒打开文件 | 获取 FD 供分析引擎深度扫描 |
| `isolateThreatFile(path)` | 隔离风险文件 | 物理转移至加密隔离区 → 返回隔离 ID |
| `restoreIsolatedFile(id)` | 恢复误报文件 | 按 ID 还原至原路径 |
| `removeIsolatedFile(id)` | 物理清除 | 不可逆擦除 |
| `queryIsolatedFiles(callback)` | 查询隔离区 | 获取所有隔离项目列表 |

### 完整工作流

```typescript
import { virusRemediation } from '@kit.EnterpriseThreatProtectionKit';

// 1. 全盘扫描（批次回调）
const callback: virusRemediation.ScanCallback = {
  onReceive: (paths: string[]) => {
    // 分批次接收，避免内存爆炸
    scannedPaths.push(...paths);
  },
  onComplete: () => { /* 扫描完成 */ },
  onError: (code, msg) => { /* 错误处理 */ },
};
virusRemediation.scanBundleFiles(
  virusRemediation.ScanTargetType.BUNDLE, callback);

// 2. 隔离发现的风险文件
const isolationId = await virusRemediation.isolateThreatFile(path);

// 3. 查询隔离区
virusRemediation.queryIsolatedFiles({
  onQuery: (files) => { isolatedItems = files; },
});

// 4. 恢复或清除
await virusRemediation.restoreIsolatedFile(isolationId);  // 误报还原
await virusRemediation.removeIsolatedFile(isolationId);   // 物理清除
```

### 权限与限制

| 要求 | 说明 |
|:----:|:------|
| **权限** | `ohos.permission.SCAN_REMEDIATE_VIRUS` — 仅企业杀软可申请 |
| **设备** | 仅 PC/2in1 设备，手机/平板不支持 |
| **FD 管理** | `openFile` 获取的 FD 必须及时关闭，防止耗尽配额 |
| **隔离 ID** | 应用卸载重装后 ID 映射丢失，需 `queryIsolatedFiles` 重新同步 |
| **BUNDLE 目录** | 包体文件不支持 isolate/remove，需走 `addDisallowedRunningBundlesSync` 黑名单或 `uninstall` |

### 最佳实践

- **分批次处理**：利用 `onReceive` 分批接收，避免大列表一次性加载
- **闲时扫描**：使用 TaskPool 在充电灭屏时执行全盘扫描
- **增量比对**：先 Stat 文件时间戳，仅对有变动的文件执行深度取証
- **AI 降级**：`canIUse` 检测设备能力，非 2in1 设备优雅降级

---

## 🎵 音频开发（AudioFocus + AudioInteraction + WindowPiP）

### AudioFocus — 音频焦点管理

**核心机制**：默认 `STREAM_USAGE_MEDIA` 会强制终止其他媒体流。工具类音效应"降级"避免冲突。

```typescript
import { audio } from '@kit.AudioKit';

// ❌ 错误：默认 MUSIC 会杀后台听书
let rendererOptions: audio.AudioRendererOptions = {
  streamInfo: { samplingRate: 44100, channels: 2, sampleFormat: 3, encodingType: 0 },
  streamUsage: audio.StreamUsage.STREAM_USAGE_MEDIA, // 独占！
};

// ✅ 方案一：改为 GAME 类型（不打断其他音源）
streamUsage: audio.StreamUsage.STREAM_USAGE_GAME;

// ✅ 方案二：AudioSession 共享模式
let session = await audio.createAudioSession();
await session.setInterruptMode(audio.InterruptMode.SHARED);
await session.activate();
// 绑定 sessionToken 到 AudioRenderer
rendererOptions.sessionToken = session.getToken();

// 监听音频打断
avPlayer.on('audioInterrupt', (info: audio.InterruptEvent) => {
  if (info.forcePause) { /* 被强制暂停 */ }
});
```

### WindowPiP — 画中画

```typescript
import { PiPWindow } from '@kit.ArkUI';

// 创建画中画
const pipController = await PiPWindow.create({
  config: { /* PiPConfiguration */ }
});
await pipController.startPiP();

// 退后台自动启动 PiP
pipController.setAutoStartEnabled(true);

// 监听状态
pipController.on('stateChange', (state) => {
  // STARTED / STOPPED / ERROR
});
```

---

## 🔐 加密深度（CryptoArchitectureKit）

```typescript
import { cryptoFramework } from '@kit.CryptoArchitectureKit';

// AES 对称加密
async function aesEncrypt(data: string, key: Uint8Array): Promise<Uint8Array> {
  const symKey = await cryptoFramework.createSymKeyGenerator('AES128')
    .convertKey(key);
  const cipher = await cryptoFramework.createCipher('AES128|CBC|PKCS7');
  const iv = { data: new Uint8Array(16) }; // 16字节初始化向量
  await cipher.init(cryptoFramework.CryptoMode.ENCRYPT_MODE, symKey, iv);
  const result = await cipher.doFinal({ data: new TextEncoder().encodeInto(data) });
  return result.data;
}

// RSA 非对称加密
async function rsaEncrypt(data: string, pubKey: Uint8Array): Promise<Uint8Array> {
  const keyPair = await cryptoFramework.createAsyKeyGenerator('RSA2048')
    .convertKey(pubKey, null);
  const cipher = await cryptoFramework.createCipher('RSA2048|PKCS1');
  await cipher.init(cryptoFramework.CryptoMode.ENCRYPT_MODE, keyPair);
  const result = await cipher.doFinal({ data: new TextEncoder().encodeInto(data) });
  return result.data;
}

// SHA256 哈希
async function sha256(data: string): Promise<Uint8Array> {
  const md = await cryptoFramework.createMd('SHA256');
  await md.update({ data: new TextEncoder().encodeInto(data) });
  return (await md.digest()).data;
}
```

---

## 🔐 CryptoCollection 加解密大全（第二轮新增）

> **来源**：`crypto-collection` | Gitee harmonyos_samples | 源码级

### 支持的算法
| 分类 | 算法 |
|------|------|
| **对称加密** | AES、3DES、SM4 |
| **非对称加密** | RSA、SM2 |
| **签名验签** | RSA、SM2、ECDSA |
| **消息摘要** | SHA256、MD5、SM3 |
| **消息认证码** | HMAC |

### 工程目录
```
entry/src/main/ets/
├── pages/
│   ├── Index.ets                  # 主页入口
│   ├── EncryptionAndDecryption.ets # 加解密页面
│   ├── SignatureVerification.ets   # 签名验签
│   ├── MessageSummary.ets          # 消息摘要
│   └── MessageAuthenticationCode.ets # HMAC
├── utils/
│   ├── CryptoUtil.ets              # 加解密工具类
│   ├── SignatureUtil.ets           # 签名验签工具类
│   └── DataConversion.ets          # SM2 格式转换
└── viewmodel/                      # ViewModel 层
```

### AES 加解密代码模式
```typescript
// [API 23+] cryptoFramework 加解密
import { cryptoFramework } from '@kit.CryptoArchitectureKit'

async function aesEncrypt(plainText: string): Promise<string> {
  let generator = cryptoFramework.createSymKeyGenerator('AES128')
  let key = await generator.generateSymKey()
  let cipher = cryptoFramework.createCipher('AES128|PKCS7')
  let iv: cryptoFramework.DataBlob = { data: new Uint8Array(16) }
  await cipher.init(cryptoFramework.CryptoMode.ENCRYPT_MODE, key, iv)
  let input: cryptoFramework.DataBlob = { data: new TextEncoder().encode(plainText) }
  let output = await cipher.doFinal(input)
  return output.data.toString()  // Base64 编码后输出
}
```

### SM2 密钥格式转换
SM2 支持 16 进制公私钥与 ASN.1 格式 Base64 编码之间的互转。

---

## 🔉 AudioFocus 音频焦点深度管理（第六轮新增）

> **来源**：`audio-focus` | Gitee harmonyos_samples | 源码级

### 能力矩阵

| 场景 | 音频流类型 | 焦点处理 |
|------|-----------|---------|
| 视频播放 | CONTENT_MOVIE | 中断后暂停，恢复后继续 |
| 音乐播放 | CONTENT_MUSIC | 中断后降低音量（闪避） |
| VoIP通话 | VOIP_CALL | 抢占焦点，其他应用暂停 |

### 核心焦点策略

```typescript
// [API 23+] AudioSession 自定义焦点策略
import { audio } from '@kit.AudioKit'

let audioSession = this.audioRenderer.getAudioSession()
audioSession.setAudioSessionDelegator({
  onInterrupt: (interruptEvent) => {
    switch (interruptEvent.forceType) {
      case audio.InterruptForceType.INTERRUPT_FORCE:
        // 强制中断：暂停播放
        this.pause()
        break
      case audio.InterruptForceType.INTERRUPT_SHARE:
        // 共享中断：降低音量
        this.duckVolume()
        break
    }
    return { isPlay: false } // 是否继续播放
  }
})
```

---

## 🔍 CoreVisionKit OCR 文字识别（第七轮新增）

> **来源**：`core-vision-kit-sample-code-ark-ts-ocr-demo` | Gitee harmonyos_samples | 源码级

### 核心 API

```typescript
// [API 23+] 通用文字识别
import { textRecognition } from '@hms.ai.ocr'

async function recognizeText(pixelMap: PixelMap): Promise<string> {
  let visionInfo: VisionInfo = {
    pixelMap: pixelMap,
    // 可指定识别语言、识别区域等参数
  }
  let result = await textRecognition.recognizeText(visionInfo)
  return result.text  // 识别出的完整文本
}
```

### 流程
```
选择图片（图库/拍照） → 转为 PixelMap → textRecognition.recognizeText() → 展示可复制的文本
```

### 约束
- 支持设备：手机、平板、2in1
- HarmonyOS 5.0.0 Release+

---

## 🛡️ DeviceSecurityKit 业务风险检测（第七轮中高价值②）

> **来源**：`device-security-kit-business-risk` | Gitee harmonyos_samples | 源码级

### 三种检测

| 检测类型 | API | 用途 |
|---------|-----|------|
| 涉诈剧本检测 | `detectFraudRisk()` | 防诈骗识别 |
| 模拟点击检测 | `detectSimulatedClickRisk()` | 反作弊/反欺诈 |
| 模拟点击增强检测 | `detectSimulatedClickRiskEnhanced()` | 增强版 + 签名验证 |

```typescript
// [API 23+] 业务风险检测
import { businessRiskIntelligentDetection } from '@kit.DeviceSecurityKit'

// 涉诈剧本检测
let fraudResult = await businessRiskIntelligentDetection.detectFraudRisk()
// 解析检测结果（建议服务端侧签名验证）

// 模拟点击检测
let clickResult = await businessRiskIntelligentDetection.detectSimulatedClickRisk()
```

### 约束
- 涉诈剧本检测需在 AGC 开通服务
- HarmonyOS 6.0.2 Beta1+

---

## 🔐 OnlineAuthKit FIDO2 生物认证（第十轮收尾⑥）

> **来源**：`online-authenticationkit_sample_fido2clientdemo_arkts` | Gitee harmonyos_samples

基于 FIDO2 协议的生物认证（指纹/人脸）。

```typescript
// [API 23+] FIDO2 生物认证
import { onlineAuthentication } from '@kit.OnlineAuthenticationKit'

// 注册生物凭证
let result = await onlineAuthentication.register({
  challenge: 'server_challenge',
  rp: { name: 'MyApp', id: 'example.com' },
  user: { id: 'user123', name: 'user' }
})

// 认证
let authResult = await onlineAuthentication.authenticate({
  challenge: 'server_challenge',
  rpId: 'example.com'
})
```

---


## ♿ Accessibility 无障碍开发要点

> **审核要求**：AGC 审核会检查无障碍支持，缺失可能导致被拒。

### 核心属性

```typescript
// 基础无障碍标签（每个可交互组件必加）
Button('提交')
  .accessibilityText('提交按钮')           // 朗读文本
  .accessibilityDescription('点击提交表单') // 详细描述
  .accessibilityGroup(true)                // 标记为无障碍组

// 隐藏装饰性元素（如图标、分割线）
Divider()
  .accessibilityLevel('no')               // 跳过朗读

// 控制焦点
Text('重要提示')
  .focusable(true)                         // 可获焦
  .defaultFocus(true)                      // 页面默认焦点
```

### 无障碍最佳实践

| 规则 | 做法 |
|:----|:-----|
| **所有可交互组件加标签** | Button/Input/List/Image 都加 `accessibilityText` |
| **装饰元素隐藏** | 纯图标/分割线/背景图加 `accessibilityLevel('no')` |
| **语义化分组** | 相关控件用 `accessibilityGroup(true)` 包裹 |
| **动态内容通知** | 用 `announceForAccessibility(text)` 通知屏幕朗读 |
| **颜色对比度** | 文本/背景对比度 ≥ 4.5:1 |
| **触摸目标大小** | 可点击区域 ≥ 44vp × 44vp |

---


---

# 第八部分：多设备适配（折叠屏、分布式流转、设备协同）

## 📱 多设备适配

### 核心原则
1. **使用 vp/百分比 代替 px**：`vp` 是鸿蒙虚拟像素单位，自动适配不同密度
2. **layoutWeight 弹性布局**：按权重分配空间，自动适应屏幕宽度
3. **breakpoint 断点系统**：按窗口宽度切换不同布局

### Breakpoint 断点适配
```typescript
import { BreakpointSystem, BreakpointType } from '@kit.ArkUI';

// 定义断点
const breakpoints = new BreakpointSystem(1);
breakpoints.setParams([
  { name: 'sm', value: 320, files: ['layout/sm'] },
  { name: 'md', value: 600, files: ['layout/md'] },
  { name: 'lg', value: 840, files: ['layout/lg'] }
]);

// 组件内使用
@State currentBreakpoint: string = 'sm';
// 根据 currentBreakpoint 切换 GridCol 列数或布局
```

### 常见设备断点
| 设备类型 | 断点 | 建议 Grid 列数 |
|---------|------|:------------:|
| 手机/折叠屏折叠态 | sm (320~599vp) | 4 |
| 折叠屏展开/小平板 | md (600~839vp) | 8 |
| 平板/桌面 | lg (840~) | 12 |

### 适配检查清单
- ✅ 所有尺寸使用 `vp` / `%` / `layoutWeight`，不用固定 px
- ✅ 图片使用 `objectFit` 控制缩放（cover/contain）
- ✅ 关键交互区域 ≥ 48vp × 48vp
- ✅ 横竖屏均测试通过
- ✅ 折叠屏展开/折叠态均验证
- ✅ 使用 `LazyForEach` 确保长列表性能

---

## 🏗️ 多设备开发实战场

> 以下实战模式源自官方 Sample `MultiCommunityApplication`（3,700 下载）和 `MusicHome`（4,080 下载），覆盖社区评论和音乐播放类应用的多设备适配全场景。

### 实战一：响应式 Navigation + pageMap 路由

```typescript
// 将 NavPathStack 存入 AppStorage，实现跨组件页面跳转
@Entry
@Component
struct Index {
  @StorageLink('pageInfos') pageInfos: NavPathStack = new NavPathStack();

  aboutToAppear(): void {
    this.pageInfos.pushPath({ name: 'mainPage' });
  }

  // pageMap 的路由分发模式
  @Builder
  pageMap(name: string, param: object) {
    if ('detailPage' === name) {
      NavDestination() { DetailPage() }
        .onBackPressed(() => {
          AppStorage.setOrCreate('isDetailPage', false);
          return false;
        })
        .hideTitleBar(true)
    } else if ('pictureDetail' === name) {
      NavDestination() { PictureDetail({ index: param as number }) }
        .hideTitleBar(true)
    } else if ('rankPage' === name) {
      NavDestination() { HotRankPage() }
        .hideTitleBar(true)
    }
  }

  build() {
    Navigation(this.pageInfos)
      .hideNavBar(true)
      .navDestination(this.pageMap)
  }
}
```

### 实战二：Tabs 响应式导航（水平↔垂直自动切换）

手机端底部水平标签栏 ⇄ 平板端左侧垂直侧边栏，通过断点实时切换。

```typescript
@Component
export struct TabContentView {
  @StorageLink('currentBreakpoint') currentBreakpoint: string = 'sm';

  build() {
    Tabs({
      barPosition: this.currentBreakpoint === 'lg'
        ? BarPosition.Start  // 平板/大屏 → 左侧垂直
        : BarPosition.End     // 手机 → 底部水平
    }) {
      TabContent() { HotPointPage() }.tabBar('关注')
      TabContent() { FoundPage() }.tabBar('发现')
      TabContent() { RankPage() }.tabBar('排行')
    }
    .vertical(this.currentBreakpoint === 'lg')      // LG 断点垂直导航
    .barHeight(this.currentBreakpoint === 'lg'
      ? '50%' : '48vp')                              // 垂直时全高，水平时固定
    .barWidth(this.currentBreakpoint === 'lg'
      ? '72vp' : '100%')                             // 垂直时固定宽度
  }
}
```

### 实战三：WaterFlow 瀑布流断点自适应列数

手机单列 ⇄ 平板双列，通过 `columnsTemplate` 动态控制。

```typescript
WaterFlow() {
  LazyForEach(this.cardArray, (item: CardItem) => {
    FlowItem() {
      Column() {
        MicroBlogView({ cardItem: item })
        CommentBarView({ isShowInput: false })
      }
    }
  })
}
.columnsTemplate(this.currentBreakpoint === 'lg' ? '1fr 1fr' : '1fr')
.rowsGap(this.currentBreakpoint === 'lg' ? 0 : 8)
.nestedScroll({                               // 内外滚动协同
  scrollForward: NestedScrollMode.PARENT_FIRST,
  scrollBackward: NestedScrollMode.SELF_FIRST
})
```

### 实战四：折叠屏双栏布局（GridRow + SideBarContainer）

手机端上下滚动，折叠屏展开态左右分栏，平板端侧边栏评论区。

```typescript
@Component
struct DetailPage {
  @StorageLink('currentBreakpoint') currentBreakpoint: string = 'sm';
  @State isFoldHorizontal: boolean = false;

  build() {
    // 手机/折叠屏：GridRow 栅格分栏
    GridRow({ columns: { sm: 4, md: 5, lg: 12 } }) {
      GridCol({ span: { sm: 4, md: this.isFoldHorizontal ? 3 : 5, lg: 12 } }) {
        MicroBlogView({ cardItem: this.cardItem })
      }
      GridCol({ span: { sm: 4, md: this.isFoldHorizontal ? 2 : 5, lg: 12 } }) {
        CommentListView()
      }
    }
    .visibility(this.currentBreakpoint === 'lg' ? Visibility.None : Visibility.Visible)

    // 平板/大屏：SideBarContainer 右侧评论区
    SideBarContainer() {
      Column() { CommentListView() }
      Column() { MicroBlogView({ cardItem: this.cardItem }) }
    }
    .visibility(this.currentBreakpoint !== 'lg' ? Visibility.None : Visibility.Visible)
  }
}
```

### 实战五：视差滚动头部

排行榜页头部随滚动产生视差位移，通过 `onScrollFrameBegin` 实现。

```typescript
const HEADER_MAX_TOP: number = 52;
const HEADER_MIN_TOP: number = 46;

@State titleMarginTop: number = HEADER_MAX_TOP;

Scroll() {
  Column() {
    // 标题栏：滚动时 marginTop 在 46~52vp 间渐变
    // 副标题在滚动收起时渐隐
    this.TitleBar()
      .margin({ top: this.titleMarginTop })

    // 榜单内容
    HotListView()
  }
}
.onScrollFrameBegin((offset: number, state: ScrollState) => {
  return { offsetRemain: this.calcParallax(offset) };
})

calcParallax(offset: number): number {
  if (offset > 0 && this.titleMarginTop > HEADER_MIN_TOP) {
    const delta = Math.min(offset, this.titleMarginTop - HEADER_MIN_TOP);
    this.titleMarginTop -= delta;
    return 0;
  }
  if (offset < 0 && this.titleMarginTop < HEADER_MAX_TOP) {
    const delta = Math.min(Math.abs(offset), HEADER_MAX_TOP - this.titleMarginTop);
    this.titleMarginTop += delta;
    return 0;
  }
  return offset;
}
```

### 实战六：窗口断点实时计算

```typescript
// EntryAbility 中监听窗口尺寸变化
private updateBreakpoint(windowWidth: number): void {
  const vp = windowWidth / display.getDefaultDisplaySync().densityPixels;
  let bp = 'sm';
  if (vp >= 840) bp = 'lg';
  else if (vp >= 600) bp = 'md';
  AppStorage.setOrCreate('currentBreakpoint', bp);
}

// 注册监听
onWindowStageCreate(windowStage: WindowStage): void {
  windowStage.getMainWindow().then((win) => {
    const winWidth = win.getWindowProperties().windowRect.width;
    this.updateBreakpoint(winWidth);
    win.on('windowSizeChange', (size) => this.updateBreakpoint(size.width));
  });
}
```

---

## 📡 分布式自由流转（应用接续 + 分布式数据对象）

> 源自官方 Sample 及华为最佳实践文档，覆盖应用接续、分布式数据对象、跨设备拖拽、碰一碰分享等核心能力。

### 应用接续（onContinue + 分布式数据对象）

```typescript
import { distributedDataObject } from '@kit.ArkData';
import { AbilityConstant, UIAbility } from '@kit.AbilityKit';

// 源端（迁移）: onContinue
export default class SourceAbility extends UIAbility {
  d_object?: distributedDataObject.DataObject;

  async onContinue(wantParam: Record<string, Object>): Promise<AbilityConstant.OnContinueResult> {
    // 1. 创建分布式数据对象
    const source = { name: 'jack', age: 18, isVis: false };
    this.d_object = distributedDataObject.create(this.context, source);

    // 2. 生成组网ID
    const sessionId = distributedDataObject.genSessionId();
    this.d_object.setSessionId(sessionId);
    wantParam['dataSessionId'] = sessionId;  // 传给对端

    // 3. 持久化（确保源端退出后对端仍能获取）
    await this.d_object.save(wantParam.targetDevice as string);
    return AbilityConstant.OnContinueResult.AGREE;
  }
}

// 对端（接收）
export default class TargetAbility extends UIAbility {
  d_object?: distributedDataObject.DataObject;

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    if (launchParam.launchReason === AbilityConstant.LaunchReason.CONTINUATION) {
      this.handleContinuation(want);
    }
  }

  handleContinuation(want: Want): void {
    const remoteData = { name: undefined, age: undefined, isVis: undefined };
    this.d_object = distributedDataObject.create(this.context, remoteData);

    // 必须在 setSessionId 之前注册 status 监听
    this.d_object.on('status', (sessionId, networkId, status) => {
      if (status === 'restored') {
        console.info(`restored: ${this.d_object!['name']}`);
      }
    });
    this.d_object.setSessionId(want.parameters?.dataSessionId as string);
  }
}
```

### 跨端文件流转（Asset 同步）

```typescript
import { commonType } from '@kit.ArkData';

// 源端：写入分布式文件目录 → 创建 Asset → 封装进 DataObject
const filePath = this.context.distributedFilesDir + '/test.txt';
fs.writeSync(fs.openSync(filePath, fs.OpenMode.READ_WRITE | fs.OpenMode.CREATE).fd, 'content');

const attachment: commonType.Asset = {
  name: 'test.txt', uri: fileUri.getUriFromPath(filePath), path: filePath,
  createTime: '...', modifyTime: '...', size: '...',
};
this.d_object = distributedDataObject.create(this.context, { attachment });

// 对端：创建空 Asset → 监听 status restored → 读取
const emptyAsset: commonType.Asset = { name: '', uri: '', path: '', createTime: '', modifyTime: '', size: '' };
this.d_object = distributedDataObject.create(this.context, { attachment: emptyAsset });
this.d_object.on('status', (s, n, status) => {
  if (status === 'restored') {
    const file = this.d_object!['attachment'] as commonType.Asset;
    // 可使用 file.uri 读取文件
  }
});
```

### 多端协同通信方案

| 功能 | API | 适用场景 |
|:----:|:----:|:--------|
| 应用接续 | `onContinue` + `distributedDataObject` | 跨设备无缝切换任务 |
| 分布式数据对象 | `create()` + `setSessionId()` + `on('status')` | 跨设备数据实时同步 |
| 跨设备拖拽 | 统一拖拽 API | 平板/2in1 间拖拽文件/文本 |
| 碰一碰分享 | 碰一碰 SDK | 图片/Wi-Fi/文件跨端分享 |
| 隔空传送 | 手势识别 + 跨端传输 | 一抓一放跨端传输 |
| 跨设备剪贴板 | 分布式剪贴板 | A设备复制，B设备粘贴 |

### 关键注意事项

- 分布式数据对象必须在 `save()` 之前调用 `setSessionId()` 激活
- 对端必须在 `setSessionId` **之前** 注册 `status` 监听，防止错过 `restored`
- 对端创建对象时所有属性应初始化为 `undefined`，Asset 需创建空对象
- API 12+ 不需要申请 `ohos.permission.DISTRIBUTED_DATASYNC`
- 需要传输文件时，使用 `Asset` 类型而非直接传文件路径

## 🤝 设备协同（KnockShare + MultiDeviceInteraction + FormGame）

### KnockShare — 碰一碰分享

```typescript
import { shareController } from '@kit.ShareKit';

// 碰一碰触发分享
shareController.share({
  title: '分享图片',
  filePath: ['/data/file/test.jpg'],
  shareMode: shareController.ShareMode.KNOCK, // 碰一碰模式
});
```

### FormGame — 游戏卡片

```typescript
// form_config.json 配置
{ "name": "GameCard", "src": "./ets/widget/GameCard.ets",
  "isDynamic": true, "defaultDimension": "2*2",
  "supportDimensions": ["2*2"] }
// GameCard.ets 使用 Canvas 实现小游戏 UI
Canvas(this.context)
  .onReady(() => { /* 绘制游戏元素 */ })
  .onTouch((event) => { /* 处理交互 */ })
```

---

## 📱 ContinueProgress 应用接续进度（第三轮新增）

> **来源**：`continue-progress` | Gitee harmonyos_samples | 源码级

### 三种场景接续

| 场景 | 接续内容 | 实现 |
|------|---------|------|
| **长列表** | List + WaterFlow 的滚动偏移量 | `scrollToIndex(continueOffset)` |
| **媒体播放** | 播放集数 + 当前进度 | `avPlayer.seek(continueTime)` |
| **Web 浏览** | 滚动位置 | `controller.runJavaScript('window.scrollY')` |

### 跨设备接续前提
1. 双端登录同一华为账号
2. 开启 Wi-Fi + 蓝牙（建议同局域网）
3. 双端安装同应用

### 核心代码模式

```typescript
// [API 23+] 应用接续核心逻辑
import { common } from '@kit.AbilityKit'

class MyAbility extends UIAbility {
  onContinue(wantParam: Record<string, Object>): OnContinueResult {
    // 1. 保存当前进度
    wantParam['continueOffset'] = this.pageOffset
    wantParam['playPosition'] = this.avPlayer.currentTime
    // 2. 返回 CONTINUE
    return OnContinueResult.AGREE
  }

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam) {
    // 3. 恢复进度（对端）
    let offset = want.parameters?.continueOffset as number
    if (offset) { this.scrollToIndex(offset) }
  }
}
```

---

## 🤝 GesturesShare 隔空传送分享（第五轮新增）

> **来源**：`GesturesShare` | Gitee harmonyos_samples | 源码级

### 功能
基于 Share Kit 的 `harmonyShare.on('gesturesShare')` 实现"一抓一放"跨设备分享文件和 App Linking 链接。

```typescript
// [API 23+] 隔空传送监听
import { systemShare } from '@kit.ShareKit'

systemShare.harmonyShare.on('gesturesShare', (event, sharableTarget) => {
  // 分享文件
  sharableTarget.share({
    type: 'file',
    uris: ['file://...', 'file://...']
  })
  // 或分享 App Linking 链接（跳转到应用内指定页面）
  // sharableTarget.share({ type: 'link', content: 'https://applink.example.com/video' })
})
```

### 权限
- 需配置 App Linking
- 双端开启华为分享服务 + 隔空传送开关
- 双端亮屏解锁 + 登录同一华为账号

---

## 🤝 KnockFileShare 碰一碰文件分享（第五轮新增）

> **来源**：`KnockFileShare` | Gitee harmonyos_samples | 源码级

### 核心 API

```typescript
// [API 23+] 碰一碰文件分享
import { systemShare } from '@kit.ShareKit'

// 注册碰一碰监听
systemShare.harmonyShare.on('knockShare', (event, sharableTarget) => {
  sharableTarget.share({
    type: 'file',
    uris: selectedFileUris   // 勾选的文件列表
  })
})

// PC端接收文件监听
systemShare.harmonyShare.on('dataReceive', (event, data) => {
  // data 保存至应用沙箱目录
  fileIo.copy(data.uri, this.context.filesDir + '/received/')
})
```

### 约束
- 手机与手机/PC/2in1 碰一碰
- 双端登录同一华为账号
- HarmonyOS 6.0.0 beta2+
- PC端最大接收 5 个文件

---

## 📷 MultiDeviceCamera 多设备相机（第七轮新增）

> **来源**：`MultiDeviceCamera` | Gitee harmonyos_samples | 源码级

### 场景
在手机、大折叠、阔折叠、三折叠、平板上实现**正常状态和折叠状态切换时**的预览旋转、拍照旋转、切换镜头。

### 核心能力

| 能力 | API | 说明 |
|------|-----|------|
| 相机预览 | `CameraManager.createCameraInput` + `PhotoSession` | 多设备预览 |
| 拍照 | `PhotoSession.capture` | 拍照 + 旋转适配 |
| 切换镜头 | `CameraInput.switchCameraInput` | 前后摄像头切换 |
| 保存图片 | `photoAccessHelper` | 保存至图库 |
| 折叠适配 | `BreakpointType` + `WindowUtil` | 折叠状态感知 + 旋转补偿 |
| 多设备适配 | `BreakpointSystem` | 一多断点适配 |

### 工程结构
```
entry/src/main/ets/
├── utils/CameraUtil.ets      # 相机工具类
├── utils/BreakpointType.ets   # 一多断点
├── utils/WindowUtil.ets      # 窗口/折叠感知
├── views/CommonView.ets      # 公共视图
└── pages/Index.ets           # 主页
```

### 核心代码模式

```typescript
// [API 23+] 相机预览 + 折叠适配
import { camera } from '@kit.CameraKit'
import { photoAccessHelper } from '@kit.MediaLibraryKit'

async function startPreview(context: Context, surfaceId: string) {
  let cameraManager = camera.getCameraManager(context)
  let cameras = cameraManager.getSupportedCameras()
  let cameraInput = cameraManager.createCameraInput(cameras[0])
  await cameraInput.open()
  let session = cameraManager.createPhotoSession()
  session.beginConfig()
  session.addInput(cameraInput)
  let previewOutput = session.createPreviewOutput(surfaceId)
  session.addOutput(previewOutput)
  await session.commitConfig()
  await session.start()
}

// 折叠状态旋转补偿
// 使用 BreakpointType 监听折叠状态变化
// 通过 WindowUtil 获取当前旋转角度，补偿预览/拍照方向
```

### 权限
```json5
"ohos.permission.CAMERA"
"ohos.permission.READ_IMAGEVIDEO"
"ohos.permission.WRITE_IMAGEVIDEO"
```

---

# 第九部分：Kit 能力速查（76个Kit分类、工具类、NFC、音频）

## 🎵 MusicHome 多设备音乐实战场（4,080 下载）

> 源自官方 Sample `MusicHome`，共 3 个模块，按 commons/features/products 三层架构组织，覆盖手机/折叠屏/平板/手表/智慧屏。

### 三层架构详解

```
MultiMusicApp/
├── commons/
│   ├── constantsCommon/        # 公共常量（断点、栅格、样式、路由）
│   └── mediaCommon/            # 公共媒体服务（音乐播放、断点系统、数据模型）
├── features/
│   ├── musicList/              # 歌曲列表页（独立模块，含页面/组件/数据）
│   ├── musicComment/           # 音乐评论页（独立复用模块）
│   └── live/                   # 直播页（独立模块）
└── products/
    ├── phone/                  # 手机/折叠屏/平板 → 组装所有 features
    └── watch/                  # 手表 → 只组装部分 features
```

**架构价值**：`features` 层开发一次 → `products` 层按设备自由组合。手机版修了一个 bug，手表版自动受益。

### 实战一：displayPriority 自适应显隐

系统根据父容器宽度自动隐藏低优先级元素，无需手写 if/else。

```typescript
Row() {
  Button('列表').displayPriority(3)   // 窄屏时优先隐藏
  Button('上一首').displayPriority(2)
  Button('播放/暂停').displayPriority(1)  // 最优先保留
  Button('下一首').displayPriority(2)
  Button('更多').displayPriority(3)
}
// 手机 → 只显示核心按钮；平板 → 全部显示
```

### 实战二：List.lanes 断点多列控制

```typescript
List({ space: 8 }) {
  LazyForEach(this.songList, (item: SongItem) => {
    ListItem() { SongCard({ song: item }) }
  }, (item: SongItem) => item.id)
}
.lanes(this.currentBreakpoint === 'lg' ? 2 : 1) // 平板双列，手机单列
.cachedCount(this.currentBreakpoint === 'lg' ? 8 : 4)
```

### 实战三：effectKit 专辑封面取色

从封面提取主色调做沉浸背景。

```typescript
import { effectKit } from '@kit.ArkGraphics';

const picker = effectKit.createColorPicker(pixelMap);
const mainColor = await picker.getMainColorSync();
const bgColor = `#${mainColor.rgba.toString(16).padStart(8, '0')}`;

const blur = effectKit.createEffect(pixelMap);
blur.blur(30); // 高斯模糊背景
```

### 实战四：Swiper 播放页（手机端）

```typescript
Swiper() {
  Column() { AlbumArt() /* 封面+控制 */ }
  Column() { LyricView() /* 歌词 */ }
}
.loop(false).indicator(true).borderRadius(16)
```

---

## 🌌 Spatialization 空间化开发（沉浸光感 + HDS 组件 + 智感握姿）

> 源自官方 Sample `Spatialization` 及华为最佳实践文档。HarmonyOS 7 (API 26) 核心新特性，全新 HDS 组件系统。

### 沉浸光感简介

沉浸光感是 HDS（HarmonyOS Design System）提供的全新材质体系，核心能力：

| 特性 | 说明 |
|:----:|:------|
| **通透材质** | 毛玻璃效果，内容可透过组件隐约可见 |
| **渐变模糊** | 标题栏随滑动从透明到模糊平滑过渡 |
| **按压弹性反馈** | 按压时弹性缩放动画 |
| **按压点光源** | 按压时触点位置光晕扩散 |
| **材质流光** | 表面微妙流光效果 |
| **智能反色** | 底层内容颜色冲突时自动调整前景色 |

### 材质档位

| 档位 | MaterialLevel | 说明 |
|:----:|:-------------:|:------|
| 强 | **EXQUISITE** | 完整沉浸光感，适合高性能设备 |
| 均衡（默认） | **GENTLE** | 适度效果，性能与视觉平衡 |
| 弱 | **SMOOTH** | 轻量级，保留核心特性 |
| 系统自适应 | **ADAPTIVE** | 推荐模式，系统自动选择最优档位 |

### 标题栏沉浸光感（HdsNavigation）

```typescript
import { hdsMaterial, HdsNavigation, ScrollEffectType } from '@kit.UIDesignKit';

HdsNavigation(this.pathStack) {
  // Page content
}
.titleBar({
  style: {
    scrollEffectOpts: {
      enableScrollEffect: true,
      scrollEffectType: ScrollEffectType.GRADIENT_BLUR,
    },
    systemMaterialEffect: {
      materialType: hdsMaterial.MaterialType.ADAPTIVE,
      materialLevel: hdsMaterial.MaterialLevel.ADAPTIVE,
    },
  },
})
```

### 标题栏动态显隐

```typescript
import { HdsNavigation, HideMode } from '@kit.UIDesignKit';

HdsNavDestination()
  .dynamicHideTitleBar({
    hideTitleArea: true,
    hideStatusBar: true,
    mode: HideMode.SCROLL_UP_TO,
  })
  .bindToScrollable([this.scroller])
```

### 底部悬浮导航（HdsTabs）

```typescript
import { HdsTabs, HdsTabsController } from '@kit.UIDesignKit';

HdsTabs({ controller: this.controller }) {
  // TabContent...
}
.barOverlap(true)                         // 悬浮模糊背景
.barPosition(BarPosition.End)
.barFloatingStyle({
  barBottomMargin: 36,                    // 距底部间距
  adaptToHandedness: true,                // 智感握姿跟随
  systemMaterialEffect: {
    materialType: hdsMaterial.MaterialType.ADAPTIVE,
    materialLevel: hdsMaterial.MaterialLevel.ADAPTIVE,
  },
})
```

### MiniBar（迷你栏）

在底部导航中嵌入可折叠迷你控制栏，适合音乐播放等场景。

```typescript
@Builder
buildMiniBar() {
  Row() {
    Image($r('app.media.prev')).width(24).height(24)
    Image($r('app.media.play')).width(32).height(32)
    Image($r('app.media.next')).width(24).height(24)
  }
}

HdsTabs()
  .barOverlap(true)
  .barPosition(BarPosition.End)
  .barFloatingStyle({
    barBottomMargin: 28,
    miniBar: {
      miniBarBuilder: () => this.buildMiniBar(),
    },
  })
```

### 普通组件沉浸材质

```typescript
import { uiMaterial } from '@kit.ArkUI';

// 对任意组件开启沉浸光感
Row()
  .systemMaterial(new uiMaterial.ImmersiveMaterial({
    style: uiMaterial.ImmersiveStyle.ULTRA_THIN,
    interactive: true,
    lightEffect: { color: undefined },
  }))
```

### 查询设备材质能力

```typescript
import { hdsMaterial } from '@kit.UIDesignKit';

// 查询设备支持的材质类型，进行优雅降级
const types = hdsMaterial.getSystemMaterialTypes();
if (!types.includes(hdsMaterial.MaterialType.EXQUISITE)) {
  // 降级到 GENTLE 或关闭沉浸光感
}
```

### 智感握姿（Smart Reach）

自动识别用户握持姿态，将高频组件动态调整到易操作区。

```typescript
HdsTabs()
  .barFloatingStyle({
    adaptToHandedness: true,  // 智感握姿跟随：底部栏自动左右偏移
  })
```

### 工程参考

| 项目 | 下载量 | GitCode |
|:----:|:-----:|:-------:|
| **Spatialization** | — | [gitcode.com/HarmonyOS_Samples/Spatialization](https://gitcode.com/HarmonyOS_Samples/Spatialization) |

---

## 📚 @kit 开发套件总览（76个 Kit）

### 核心 Kit（最常用）
| Kit | 导入方式 | 功能 |
|-----|---------|------|
| **AbilityKit** | `@kit.AbilityKit` | 应用上下文、页面路由、窗口、生命周期 |
| **ArkUI** | `@kit.ArkUI` | 声明式UI、组件、布局、手势、动画 |
| **NetworkKit** | `@kit.NetworkKit` | HTTP请求、上传下载 |
| **ArkData** | `@kit.ArkData` | 数据持久化 Preferences/RDB/KVStore |
| **BasicServicesKit** | `@kit.BasicServicesKit` | 弹窗、Toast、剪贴板、公共事件 |
| **PushKit** | `@kit.PushKit` | 消息推送、离线推送 |
| **PaymentKit** | `@kit.PaymentKit` | 支付、订单交易 |
| **MapKit** | `@kit.MapKit` | 地图、POI、路线规划 |
| **LocationKit** | `@kit.LocationKit` | 定位、逆地理编码 |
| **AccountKit** | `@kit.AccountKit` | 鸿蒙账号、登录授权 |
| **NotificationKit** | `@kit.NotificationKit` | 系统通知、状态栏消息 |
| **MediaKit** | `@kit.MediaKit` | 多媒体播放 |
| **CameraKit** | `@kit.CameraKit` | 相机预览、拍照、录像 |
| **CryptoArchitectureKit** | `@kit.CryptoArchitectureKit` | 加解密 AES/RSA/MD5 |
| **IAPKit** | `@kit.IAPKit` | 应用内购、订阅 |
| **AppLinkingKit** | `@kit.AppLinkingKit` | 应用跳转、DeepLink |
| **IPCKit** | `@kit.IPCKit` | 跨进程通信 |
| **LocalizationKit** | `@kit.LocalizationKit` | 国际化、多语言 |

### 业务选型速查
| 需求 | 导入哪个 Kit |
|------|------------|
| 网络请求 | `@kit.NetworkKit` |
| 本地数据存储 | `@kit.ArkData` |
| 用户登录/授权 | `@kit.AccountKit` |
| 消息推送 | `@kit.PushKit` |
| 支付 | `@kit.PaymentKit` |
| 地图 | `@kit.MapKit` |
| 定位 | `@kit.LocationKit` |
| 相机拍照 | `@kit.CameraKit` |
| 加解密 | `@kit.CryptoArchitectureKit` |
| 国际化和多语言 | `@kit.LocalizationKit` |
| 通知栏消息 | `@kit.NotificationKit` |
| 后台任务 | `@kit.BackgroundTasksKit` |
| 分布式流转 | `@kit.DistributedServiceKit` |
| AI 模型推理 | `@kit.MindSporeLiteKit` |
| 扫码 | `@kit.ScanKit` |
| 文件读写 | `@kit.CoreFileKit` |

---

## 📲 常见业务 Kit 速查

### PushKit 消息推送
```typescript
import { pushService } from '@kit.PushKit';
import { notificationManager } from '@kit.NotificationKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

// 1. 获取 Push Token（在 Ability onCreate 中调用）
const pushToken: string = await pushService.getToken();
hilog.info(0x0000, 'Push', 'Token: ' + pushToken);
// ↑ 上报此 token 到你的服务端

// 2. 请求通知权限（onWindowStageCreate 中调用）
await notificationManager.requestEnableNotification(this.context);

// 3. 服务端下发流程（Java 示例）：
//    a. AGC 下载服务账号密钥文件 private.json
//    b. 用 RSA 私钥生成 JWT 鉴权令牌
//    c. POST https://push-api.cloud.huawei.com/v1/{projectId}/messages:send
//    d. payload 中指定 title/body/clickAction
```

| 步骤 | 说明 |
|------|------|
| 客户端 | 获取 Push Token + 请求通知权限 |
| 服务端 | 生成 JWT 鉴权令牌 → 调用 Push API 下发消息 |
| 点击处理 | 默认打开首页，可在 AGC 配置自定义跳转页面 |

### PaymentKit 支付
```typescript
// 支付流程：客户端发起 → 服务端生成订单 → 客户端调起收银台 → 支付结果回调
import { payment } from '@kit.PaymentKit';

// 调起支付收银台（需要服务端先创建订单获取 orderId）
payment.pay(this.context, {
  orderId: 'YOUR_ORDER_ID',      // 服务端创建的订单号
  publicKey: 'YOUR_PUBLIC_KEY',  // 华为支付公钥
  amount: 9.90,                   // 金额
  productName: '钻石会员',        // 商品名
  productDescription: '解锁全部功能',
  merchantId: 'YOUR_MERCHANT_ID',
  applicationId: 'YOUR_APP_ID',
  countryCode: 'CN',
  currency: 'CNY',
});
```

### MapKit 地图
```typescript
// MapKit 提供地图显示、POI 搜索、路线规划等功能
// AGC 控制台开通 Map Kit 服务后，在 module.json5 配置 apiKey
import { map } from '@kit.MapKit';

// 地图组件
@Component
struct MapPage {
  build() {
    Column() {
      // MapComponent 是 ArkUI 内置地图组件（需配置后可用）
      MapComponent()
        .width('100%').height('100%')
        .zoomLevel(15)
        .onMapReady(() => { /* 地图加载完成 */ });
    }
  }
}
// POI 搜索、逆地理编码使用 @kit.MapKit 下的 geo/geocode API
```

### 文件管理（CoreFileKit）
```typescript
import { fileIo } from '@kit.CoreFileKit';

// 沙箱路径：context.filesDir / context.cacheDir / context.tempDir
const sandboxPath = this.context.filesDir + '/data.txt';

// 写入文件
const file = fileIo.openSync(sandboxPath, fileIo.OpenMode.CREATE | fileIo.OpenMode.READ_WRITE);
fileIo.writeSync(file.fd, 'Hello HarmonyOS');
fileIo.closeSync(file);

// 读取文件
const file2 = fileIo.openSync(sandboxPath, fileIo.OpenMode.READ_ONLY);
const buf = new ArrayBuffer(1024);
const readLen = fileIo.readSync(file2.fd, buf);
fileIo.closeSync(file2);
const content = new TextDecoder('utf-8').decode(buf.slice(0, readLen));

// 目录遍历
const files = fileIo.listFileSync(this.context.filesDir);
// 文件是否存在
const exists = fileIo.accessSync(sandboxPath);
```

### 日志输出（hilog）
```typescript
import { hilog } from '@kit.PerformanceAnalysisKit';
// 格式：hilog.info(domain, tag, format, ...args)
// domain 为自定义十六进制整数（建议 0x0000~0xFFFF）
hilog.info(0x0000, 'MyApp', 'User login: %{public}s', userName);
hilog.warn(0x0000, 'MyApp', 'Network timeout, retrying...');
hilog.error(0x0000, 'MyApp', 'Crash: %{public}s', error.message);
```
- **domain**: 模块标识（16位十六进制）
- **tag**: 标签，用于过滤
- **format**: 格式化字符串，敏感信息用 `%{private}s`，可公开用 `%{public}s`

### 国际化多语言（LocalizationKit）
```typescript
import { i18n } from '@kit.LocalizationKit';
// 系统会自动根据设备语言加载 resources/base/element/ 下对应语言的字符串

// 资源文件组织：
// resources/
//   ├── base/       # 默认（中文）
//   │   └── element/
//   │       └── string.json  →  { "hello": "你好" }
//   ├── en_US/      # 英文
//   │   └── element/
//   │       └── string.json  →  { "hello": "Hello" }
//   └── ja_JP/      # 日文
//       └── element/
//           └── string.json  →  { "hello": "こんにちは" }

// 代码中使用 $r() 引用：
Text($r('app.string.hello'))
// 或使用资源管理 API：
this.context.resourceManager.getStringSync('app.string.hello');
```

### MindSporeLiteKit（端侧 AI 推理）
```typescript
import { mindSporeLite } from '@kit.MindSporeLiteKit';
// 加载模型（.ms 格式）
const model = mindSporeLite.createModel();
model.loadModel(this.context, 'model.ms');
// 构建输入张量
const inputTensor = model.getInputs()[0];
inputTensor.setData(new Float32Array([...]));
// 推理
model.predict([inputTensor], (err, outputs) => {
  const result = outputs[0].getData();
});
// 释放
model.destroy();
```

---

## 📅 ArkTS 工具类速查（@kit.ArkTS）

```typescript
import { util } from '@kit.ArkTS';

// 容器类
let list = new util.ArrayList<string>();     // 动态数组
list.add('a'); list.get(0); list.removeAt(0);
let map = new util.HashMap<string, number>(); // 哈希表
map.set('key', 1); map.get('key');
let queue = new util.Deque<string>();        // 双端队列
queue.insertFront('a'); queue.removeEnd();

// 编码转换
const encoder = new util.TextEncoder();
const uint8 = encoder.encodeInto('你好');      // 字符串 → Uint8Array
const decoder = new util.TextDecoder('utf-8');
const str = decoder.decodeToString(uint8);    // Uint8Array → 字符串

// Base64
const base64 = new util.Base64();
const encoded = base64.encodeToString(new Uint8Array([1,2,3]));
const decoded = base64.decodeSync(encoded);

// 随机数
const rand = new util.Random();
const num = rand.nextInt();         // 随机整数
const bool = rand.nextBoolean();    // 随机布尔
const range = rand.nextUint32();    // 0~4294967295

// 字符串工具
util.printf('%s is %d', 'age', 25); // 格式化 → "age is 25"
util.printf('%s', JSON.stringify(obj));

// 日期格式化（使用 Intl）
import { Intl } from '@kit.LocalizationKit';
const dtf = new Intl.DateTimeFormat('zh-CN', {
  dateStyle: 'long', timeStyle: 'short'
});
console.info(dtf.format(new Date())); // 2026年6月23日 18:30
```

---

## 🎥 媒体开发（CameraKit + AudioKit + AVCodecKit）

```typescript
// 拍照流程（CameraKit）
import { camera } from '@kit.CameraKit';

// 获取相机管理器
const cameraManager = camera.getCameraManager(this.context);
// 获取相机设备
const cameras = cameraManager.getSupportedCameras();
// 创建输入
const cameraInput = cameraManager.createCameraInput(cameras[0]);
// 创建输出（拍照）
const photoOutput = cameraManager.createPhotoOutput();
// 创建会话
const session = cameraManager.createCaptureSession();
session.beginConfig();
session.addInput(cameraInput);
session.addOutput(photoOutput);
session.commitConfig();
session.start();
// 拍照
photoOutput.capture();

// 音频播放
import { audio } from '@kit.AudioKit';
const audioPlayer = audio.createAudioPlayer();
audioPlayer.src = this.context.filesDir + '/music.mp3';
await audioPlayer.play();

// 音视频编码（AVCodecKit）
import { avCodec } from '@kit.AVCodecKit';
// 创建编码器
const encoder = avCodec.createVideoEncoder();
// 配置编码参数（分辨率/帧率/码率）
// 输入原始帧 → 输出编码后的 H.264/H.265 数据
```

---

## 📡 短距离通信（BLE + NFC）

```typescript
// BLE 扫描
import { ble } from '@ohos.bluetooth';

// 扫描设备
ble.startBLEScan([{ serviceUuid: '0000180F-...' }], { interval: 500 });
ble.on('BLEDeviceFind', (result) => {
  console.info('发现 BLE 设备:', result.deviceId, result.rssi);
});
ble.stopBLEScan();

// BLE 连接
const device = ble.createGattClientDevice(result.deviceId);
device.on('BLEConnectionStateChange', (state) => {
  if (state.state === 'connected') { /* 已连接 */ }
});
device.connect();

// NFC（Tag 读写）
import { tag } from '@ohos.nfc.tag';
tag.on('tag', (tagInfo) => {
  const tagId = tagInfo.tagId;   // NFC 标签 ID
  // 读取 NDEF 数据
});
```

---

## 🏷️ NFCTag NFC标签应用跳转（第二轮新增）

> **来源**：`NFCTag` | Gitee harmonyos_samples | 源码级

### 场景
亮屏解锁状态下，设备触碰 NFC 标签后读取数据并跳转应用。

### 两种模式
| 模式 | 触发条件 | 行为 |
|------|---------|------|
| **前台读卡** | 应用已打开在前台 | 直接分发给当前应用，跳转详情页展示标签技术类型和信息 |
| **后台读卡** | 未打开应用 | 根据技术类型匹配应用；匹配多个→弹出选择器；匹配一个→直接打开 |

### 权限
```
ohos.permission.NFC_TAG    // 允许应用读取 Tag 卡片
```

### 工程目录
```
entry/src/main/ets/
├── entryability/EntryAbility.ets
├── pages/Index.ets               // 首页
└── view/ReadNFCTag.ets           // 展示 NFC 信息页面
```

### 约束
- HarmonyOS 5.0.5 Release+
- 设备必须亮屏 + 解锁

---

## 🎵 AudioInteraction 音频播控全链路（第二轮新增）

> **来源**：`audio-interaction` | ⭐22 Stars | Gitee harmonyos_samples | 源码级

### 能力矩阵
| 能力 | API | 说明 |
|------|-----|------|
| **音频播放** | AudioRenderer | PCM 音频数据播放 |
| **播控中心交互** | AVSession | 媒体会话控制 |
| **后台播放** | BackgroundUtil + KEEP_BACKGROUND_RUNNING | Service Ability 保活 |
| **焦点管理** | AudioRendererController.interrupt | 焦点打断策略适配 |
| **路由切换** | audioRoutingManager | 切换发声/输出设备 |
| **歌词同步** | LyricsComponent | 歌单数据绑定 |

### 工程结构
```
├── entry/src/main/ets/
│   ├── components/
│   │   ├── ControlAreaComponent.ets    # 音频操控区
│   │   ├── LyricsComponent.ets         # 歌词组件
│   │   ├── MusicInfoComponent.ets      # 音乐内容
│   │   ├── PlayerInfoComponent.ets     # 播控内容区
│   │   └── TopAreaComponent.ets        # 顶部区域
│   └── dataSource/
│       ├── SongDataSource.ets          # 歌曲数据
│       └── SongListData.ets            # 歌曲列表
├── MediaService/src/main/ets/
│   ├── songDataController/
│   │   ├── PlayerData.ets
│   │   ├── SongData.ets
│   │   └── SongItemBuilder.ets
│   └── utils/
│       ├── AudioRendererController.ets # 音频播放控制核心
│       ├── AVSessionController.ets      # 媒体会话控制
│       ├── BackgroundUtil.ets           # 后台播放
│       └── MediaTools.ets              # 媒体数据转换
```

### 权限
```json5
"ohos.permission.KEEP_BACKGROUND_RUNNING"  // 后台任务
```

---

## 🎧 AudioCodec 音频编解码（第四轮新增）

> **来源**：`audio-codec` | Gitee harmonyos_samples | 源码级

基于 `OH_AVCodec` Native 能力实现音频播放、转码、录制。

### 三大链路

```
播放：  本地音频 → 解封装(Demuxer) → 解码(Decoder) → 播放(AudioRenderer)
转码：  本地音频 → 解封装 → 解码 → 编码(Encoder) → 封装(Muxer) → 保存
录制：  麦克风采集(AudioCapturer) → 编码 → 封装 → 保存
```

### 权限

```json5
"ohos.permission.MICROPHONE"
```

---

## 🎵 MediaProvider 媒体会话提供方（第四轮新增）

> **来源**：`media-provider` | Gitee harmonyos_samples | 源码级

```typescript
// [API 23+] AVSession 双向交互
import { avSession } from '@ohos.multimedia.avsession'

let session = await avSession.createAVSession(context, 'tag', 'audio')
await session.activate()
session.setAVMetadata({ title: 'Song', artist: 'Singer', duration: 300000 })
session.setAVPlaybackState({ state: avSession.PlaybackState.PLAYING })
session.on('play', () => { this.resume() })
session.on('pause', () => { this.pause() })
```

---

## 📤 UploadAndDownLoad 文件上传下载（第五轮新增）

> **来源**：`upload-and-down-load` | Gitee harmonyos_samples | 源码级

使用 `@ohos.request` 接口创建上传和下载任务，hfs 作为服务器。

### 上传模块
```typescript
// [API 23+] @ohos.request 上传
import { request } from '@kit.BasicServicesKit'

let uploadTask = await request.agent.create(this.context, [fileUri], {
  url: 'http://server/upload',
  method: 'POST', title: '上传', data: { key: 'value' }
})
uploadTask.on('progress', (info) => { /* 上传进度 */ })
uploadTask.start()
```

### 下载模块
```typescript
// [API 23+] @ohos.request 下载
let downloadTask = await request.agent.create(this.context, {
  url: 'http://server/file.zip',
  saveas: './downloads/file.zip', title: '下载'
})
downloadTask.on('progress', (info) => { /* 下载进度 */ })
downloadTask.start()
downloadTask.pause()    // 暂停
downloadTask.resume()   // 恢复
```

---

## 🌐 WebApplicationJump Web跳转应用（第五轮新增）

> **来源**：`web-application-jump` | Gitee harmonyos_samples | 源码级

### 五种跳转场景

| 场景 | 实现 |
|------|------|
| Web→原生ArkTS页面 | `onLoadIntercept` 拦截 + Navigation `pushPath` |
| Web→Web页面 | 前端 `a` 标签 `href` 配置 |
| Web→三方应用 | `onLoadIntercept` + Want 隐式拉起 + module.json5 exported/entities/actions |
| Web→系统应用 | `onLoadIntercept` + Want 配置系统应用参数 + `startAbility` |
| Web→应用市场 | `onLoadIntercept` + StoreKit `loadProduct` |
| Web→跨设备应用 | `onLoadIntercept` + `getAvailableDeviceListSync` + Want deviceId |

### 核心代码

```typescript
// [API 23+] onLoadIntercept 拦截拉起
Web({ src: 'https://example.com', controller: this.webController })
  .onLoadIntercept((event) => {
    if (event.data.url.startsWith('native://')) {
      // 跳转到原生页面
      this.navPathStack.pushPath({ name: 'OriginPage' })
      return true
    }
    if (event.data.url.startsWith('thirdparty://')) {
      // 隐式拉起三方应用
      let want: Want = {
        action: 'ACTION_VIEW',
        entities: ['entity.system.home'],
        uri: event.data.url
      }
      this.context.startAbility(want)
      return true
    }
    return false
  })
```

---

## 🌐 WebCrossDomain Web跨域解决方案（第七轮新增）

> **来源**：`WebCrossDomain` | Gitee harmonyos_samples | 源码级

### 四种跨域场景

| 场景 | 核心技术 | 说明 |
|------|---------|------|
| **本地资源跨域** | `setPathAllowingUniversalAccess()` | file协议跨域访问本地文件 |
| **远程请求跨域** | `WebSchemeHandler`拦截 + `rcp`代理 | 代理转发 + 跨域响应头 |
| **跨域Cookies** | `putAcceptCookieEnabled` + `configCookieSync` | A域名Cookie传给B域名 |
| **自定义协议跨域** | `WebSchemeHandler`拦截 + 系统能力 | 拦截自定义协议弹提示 |

### 远程请求跨域代码

```typescript
// [API 23+] WebSchemeHandler 跨域代理
Web({ src: 'https://example.com', controller: this.controller })
  .onLoadIntercept((event) => {
    // 方法1: 设置跨域路径白名单
    // this.controller.setPathAllowingUniversalAccess(['/data/storage/el2/base/files/'])

    // 方法2: 注册 scheme 拦截器
    // web.WebSchemeHandler 实现 onRequestStart 回调
    // 使用 rcp.fetch() 作为代理请求转发
    return false
  })
```

### Cookies 跨域代码

```typescript
// [API 23+] Cookies 跨域设置
import { webview } from '@kit.ArkWeb'

let cookieMgr = webview.WebCookieManager.getInstance()
cookieMgr.putAcceptCookieEnabled(true)

// 获取 A 域名的 cookies
let cookies = cookieMgr.fetchCookieSync('https://domain-a.com')

// 设置到 B 域名
cookieMgr.configCookieSync('https://domain-b.com', cookies)
```

---

## 🎤 AudioInEarMonitor 音频耳返（第七轮中高价值③）

> **来源**：`audio-in-ear-monitor` | Gitee harmonyos_samples | 源码级

### 两种方案

| 方案 | API | 耳机支持 | 层级 |
|:----:|-----|:--------:|:----:|
| **AudioLoopback** | `createAudioLoopback().enable()` | 有线耳机 | ArkTS |
| **Native 采集+渲染** | `OH_AudioCapturer_Start` + `OH_AudioRenderer_Start` | 有线+蓝牙 | Native C++ |

### ArkTS 侧代码

```typescript
// [API 23+] AudioLoopback 耳返
import { audio } from '@kit.AudioKit'

// 1. 查询支持
let supported = audio.isAudioLoopbackSupported()
if (supported) {
  let loopback = audio.createAudioLoopback()
  // 2. 开启耳返
  loopback.enable(true)
  // 3. 调节音量
  loopback.setVolume(0.8)
  // 4. 关闭耳返
  // loopback.enable(false)
}
```

### Native 侧
- `OH_AudioStreamBuilder_Create` 创建采集器 + 渲染器
- 设置采样率/通道数/时延模式
- 采集数据直接送入渲染器实现低延迟耳返
- 使用 AVRecorder 录制耳返音频
- 使用 AVPlayer 播放录制结果

---

## 📁 Picker 文件选择器（第八轮中高价值⑤）

> **来源**：`picker` | Gitee harmonyos_samples | 源码级

### 三种 Picker

| Picker | API | 功能 |
|--------|-----|------|
| 文档选择 | `DocumentViewPicker.select()` | 选择文档 |
| 文档保存 | `DocumentViewPicker.save()` | 保存文件 |
| 图片/视频 | `PhotoViewPicker.select()` | 从图库选择图片或视频 |
| 文件读写 | `fs.openSync/fs.writeSync/fs.readSync` | 编辑+保存文档内容 |

### 核心代码

```typescript
// [API 23+] 文件选择器用法
import { picker } from '@kit.CoreFileKit'
import { photoAccessHelper } from '@kit.MediaLibraryKit'

// 文档选择
let documentPicker = new picker.DocumentViewPicker()
let docs = await documentPicker.select({ maxSelectNumber: 1 })

// 图片选择
let photoPicker = new photoAccessHelper.PhotoViewPicker()
let photos = await photoPicker.select({ maxSelectNumber: 3, MIMEType: picker.PickerMediaType.IMAGE })

// 文件读写
import { fileIo } from '@kit.CoreFileKit'
let file = fileIo.openSync(docs[0], fileIo.OpenMode.READ_WRITE)
let buf = new ArrayBuffer(1024)
fileIo.readSync(file.fd, buf)
fileIo.writeSync(file.fd, new TextEncoder().encode('new content'))
fileIo.closeSync(file)
```

---

## 📺 VideoCast 视频投播（第九轮中高价值⑦）

> **来源**：`VideoCast` | Gitee harmonyos_samples | 源码级

### 三大场景

| 场景 | 说明 |
|------|------|
| 本端播放 | AVPlayer 本地播放，进度/音量/集数控制 |
| 播控中心控制 | AVSession 双向交互，播控中心操作本端 |
| 投播远端 | 系统投播能力，本端控制远端设备 |

### 工程结构
```
controller/
├── VideoPlayerController.ets       # 本地播放控制
├── VideoSessionController.ets      # 播控中心控制
└── VideoCastController.ets         # 投播远端控制
```

### 约束
- 双端开启蓝牙+WiFi
- HarmonyOS 5.0.5+

---

## 📍 LocationService 位置服务（第十轮收尾⑦）

> **来源**：`location-service` | Gitee harmonyos_samples | 源码级

### 四种定位模式

| 模式 | API | 说明 |
|------|-----|------|
| 缓存位置 | `geoLocationManager.getLastLocation()` | 获取最后已知位置 |
| 当前位置 | `geoLocationManager.getCurrentLocation()` | 单次获取当前位置 |
| 持续定位 | `geoLocationManager.on('locationChange')` | 持续监听位置变化 |
| 后台定位 | `backgroundTaskManager.startBackgroundRunning` + `on` | 退后台持续定位 |

### 核心代码

```typescript
// [API 23+] 位置服务
import { geoLocationManager } from '@kit.LocationKit'
import { backgroundTaskManager } from '@kit.BackgroundTasksKit'

// 获取当前位置
let location = await geoLocationManager.getCurrentLocation()

// 持续监听
geoLocationManager.on('locationChange', (location) => {
  this.latitude = location.latitude
  this.longitude = location.longitude
})

// 后台定位（需申请长时任务）
await backgroundTaskManager.startBackgroundRunning(context,
  backgroundTaskManager.BackgroundMode.LOCATION)
```

### 权限
```json5
"ohos.permission.LOCATION"
"ohos.permission.APPROXIMATELY_LOCATION"
"ohos.permission.LOCATION_IN_BACKGROUND"
"ohos.permission.KEEP_BACKGROUND_RUNNING"
```

---

# 第十部分：Sample 项目解析（按领域分类）

## 💹 全链路盯盘实战（闪控球 + 悬浮窗 + 卡片 + 防窥）

> 源自官方 Sample `AlwaysOnMarketWatch`（2,035 下载）及华为最佳实践文档。覆盖桌面/锁屏/待机/隐私保护四类系统能力。

### 整体架构

```
闪控球（FloatingBall） ←→ 悬浮窗（FloatView）       ← 桌面场景
     ↕                                                ↕
锁屏卡片（Form Kit） → 待机屏保卡片（Form Kit）      ← 锁屏/待机场景
     ↕
防窥保护（dlpAntiPeep）                              ← 隐私保护
```

### 1. 闪控球（FloatingBall）

```typescript
import { floatingBall } from '@kit.ArkUI';

// 创建闪控球控制器
async function createFloatingBall(context: UIAbilityContext): Promise<void> {
  const controller = await floatingBall.create({
    context: context
  });
  // 启动闪控球
  controller.startFloatingBall({
    template: floatingBall.TemplateType.ROUNDED_RECTANGLE,
    title: '自选股',
    content: '上证 3,201.25 ▲0.32%'
  });
}
```

### 2. 悬浮窗（FloatView）— 闪控球的展开态

```typescript
import { floatView } from '@kit.ArkUI';

// 创建悬浮窗控制器（绑定闪控球）
async function createFloatView(context: UIAbilityContext): Promise<void> {
  if (!floatView.isFloatViewEnabled()) return;  // 检查设备支持
  const controller = await floatView.create({
    context: context,
    templateType: floatView.FloatViewTemplateType.ROUNDED_RECTANGLE
  });
}

// 绑定闪控球与悬浮窗（点击闪控球弹出悬浮窗）
floatView.bind(floatViewController, floatingBallController, ballParams);

// 双指手势切换悬浮窗大小（正常态 ↔ 横幅态）
PanGesture({ fingers: 2, direction: PanDirection.Up })
  .onActionStart(() => {
    FloatViewController.setWindowSize({
      width: vp2px(bannerWidth),
      height: vp2px(bannerHeight)
    });
  })
```

### 3. 锁屏卡片（Form Kit）

**requirements**：AGC 申请"锁屏卡片"权限 + `form_config.json` 配置 `renderingMode` 和 `supportDimensions`（必须含 `"1*1"` 或 `"1*2"`）。

```json
{
  "forms": [{
    "name": "LockScreenCard",
    "src": "./ets/widget/pages/LockScreenCard.ets",
    "renderingMode": "autoColor",
    "defaultDimension": "1*2",
    "supportDimensions": ["1*2"]
  }]
}
```

```typescript
@Entry(storageUpdateByMsg)
@Component
struct LockScreenCard {
  @LocalStorageProp('finalWatchList') stockList: StockInfo[] = [];

  build() {
    Column() {
      ForEach(this.stockList.slice(0, 3), (stock: StockInfo) => {
        Row({ space: 2 }) {
          Text(stock.name).fontSize(12).fontColor('#FFFFFF')
          Text(stock.rate).fontSize(12)
            .fontColor(stock.rate.startsWith('+') ? '#FF4444' : '#00CA69')
        }
      })
    }
    .onClick(() => {
      postCardAction(this, { action: 'router', abilityName: 'EntryAbility' });
    })
  }
}
```

### 4. 待机屏保卡片（Form Kit, API 23+）

**配置**：`form_config.json` 中新增 `standby` 字段。仅支持 `2×2` 尺寸。

```json
{
  "forms": [{
    "name": "widget",
    "defaultDimension": "2*2",
    "supportDimensions": ["2*2"],
    "standby": {
      "isSupported": true,
      "isAdapted": true,
      "isPrivacySensitive": false
    }
  }]
}
```

### 5. 防窥保护（dlpAntiPeep）

```typescript
import { dlpAntiPeep } from '@kit.DeviceSecurityKit';

// 检查系统能力
export function canUseAntiPeep(): boolean {
  return canIUse('SystemCapability.Security.DlpAntiPeep');
}

// 检查开关状态
export async function isAntiPeepOn(): Promise<boolean> {
  return await dlpAntiPeep.isDlpAntiPeepSwitchOn();
}

// 注册窥视状态监听
function startListening(): void {
  dlpAntiPeep.on('dlpAntiPeep', (info: dlpAntiPeep.DlpAntiPeepStatus) => {
    if (info.isPeep) {
      // 有人窥视 → 显示蒙层
      showMask();
    } else {
      hideMask();
    }
  });
}
```

### 权限前置条件

```typescript
import { abilityAccessCtrl, common } from '@kit.AbilityKit';

// 请求悬浮窗权限
let atManager = abilityAccessCtrl.createAtManager();
atManager.requestPermissionsFromUser(context, [
  'ohos.permission.FLOAT_VIEW'
]);
```

### 目录结构范式

```
features/stockfloatpanel/src/main/ets/
├── controllers/
│   ├── FloatPanelController.ets     # 核心控制器：创建/绑定/启动
│   ├── FloatingBallController.ets   # 闪控球控制器
│   └── FloatViewController.ets      # 悬浮窗控制器
├── pages/
│   └── FloatViewPage.ets            # 悬浮窗 UI + 防窥逻辑
├── views/
│   ├── FloatViewStockList.ets       # 正常态行情列表
│   └── FloatViewStockBanner.ets     # 横幅态行情展示
└── utils/
    └── AntiPeepUtils.ets            # 防窥保护工具类
```

---

## 🃏 互动卡片 LiveCard（2,194 下载）

> 源自官方 Sample `LiveCard`，演示 HarmonyOS 互动卡片（Live Form）全链路开发：配置→普通卡片→LiveForm→通信→动画。

### 整体架构

```
form_config.json（配对配置）
     ↓
普通桌面卡片（静态 Widget）           ← src 指向
     ↓ 用户点击
sceneAnimationParams.abilityName
     ↓
LiveFormExtensionAbility              ← 独立的 UI 扩展进程
     ↓ localStorage
LiveForm UI 页面                       ← 帧动画/陀螺仪/进度动画
     ↓ postCardAction
CardActionHandler（主应用接收）
     ↓ formProvider.updateForm
普通卡片动态更新
```

### form_config.json 核心配置

```json
{
  "name": "MusicCard",              // 卡片身份证，与 form_name 一致
  "src": "./ets/widget/pages/MusicCard.ets",  // 普通卡片页面
  "isDynamic": true,                // 允许应用动态更新卡片
  "defaultDimension": "2*4",        // 默认尺寸
  "supportDimensions": ["2*4"],     // 支持的尺寸列表
  "sceneAnimationParams": {         // 互动卡片关键绑定
    "abilityName": "MusicLiveCardAbility"
  }
}
```

**流程**：src → 普通卡片路径，abilityName → LiveForm 展开页。两者通过 `module.json5` 注册关联。

```json5
// module.json5 注册 LiveForm
{
  "name": "MusicLiveCardAbility",
  "srcEntry": "./ets/livecardability/MusicLiveCardAbility.ets",
  "type": "liveForm"
}
```

### LiveFormExtensionAbility（实况卡片）

```typescript
import { LiveFormExtensionAbility, LiveFormInfo, UIExtensionContentSession } from '@kit.AbilityKit';

export class MusicLiveCardAbility extends LiveFormExtensionAbility {
  async onLiveFormCreate(info: LiveFormInfo, session: UIExtensionContentSession): Promise<void> {
    let storage = new LocalStorage();
    storage.setOrCreate('context', this.context);
    storage.setOrCreate('session', session);
    storage.setOrCreate('formId', info.formId);
    storage.setOrCreate('borderRadius', info.borderRadius);

    // 加载 LiveForm UI 页面
    session.loadContent('livecardability/pages/MusicLiveCard', storage);

    // 从 RDB 数据库加载歌曲数据
    let songList = await SongRdbHelper.getInstance(this.context).queryAllSongs();
    storage.setOrCreate('songList', songList);
  }
}
```

### 卡片 UI + 帧动画

```typescript
@Entry(storage)
@Component
struct MusicLiveCard {
  @LocalStorageProp('currentSong') currentSong: SongItem = new SongItem();
  @State @Watch('frameChange') currentFrame: number = 0;

  // 帧动画：封面切换
  private startAnimation(): void {
    setInterval(() => {
      if (this.currentFrame < this.totalFrames - 1) {
        this.currentFrame++;
      }
    }, this.frameDuration);
  }

  build() {
    Column() {
      Image($r(`app.media.cover_${this.currentFrame}`))  // 帧动画
        .width('100%').aspectRatio(1)

      Row() {
        Button() { Image($r('app.media.prev')) }.onClick(() => {
          postCardAction(this, { action: 'message', data: 'prev' })
        })
        Button() { Image($r('app.media.play')) }.onClick(() => {
          postCardAction(this, { action: 'message', data: 'toggle' })
        })
        Button() { Image($r('app.media.next')) }.onClick(() => {
          postCardAction(this, { action: 'message', data: 'next' })
        })
      }
    }
    .onClick(() => {
      postCardAction(this, { action: 'router', abilityName: 'EntryAbility' })
    })
  }
}
```

### 卡片与主应用通信

| 方向 | 方式 | 说明 |
|:----:|:----:|:------|
| 卡片→应用 | `postCardAction(this, { action, data })` | 发送 CALL/MESSAGE/ROUTER 指令 |
| 应用→静态卡片 | `formProvider.updateForm(formId, formBindingData)` | 更新卡片数据 |
| 应用→实况卡片 | Preferences/RDB 持久化 | 读取最新状态 |

```typescript
// 主应用注册卡片动作处理器
import { CardActionHandler } from './utils/CardActionHandler';

onCreate(want: Want): void {
  CardActionHandler.setContext(this.context);
  this.callee.on('cardAction', CardActionHandler.getHandler());
}
```

### 四种卡片类型

| 卡片 | 场景 | 交互特点 | 核心能力 |
|:----:|:----:|:---------|:--------|
| 🎵 **音乐播控** | 播放控制 | 帧动画封面、歌词滚动、播放/暂停/切歌 | setInterval 帧动画 + LRC 歌词解析 |
| 📦 **快递追踪** | 物流跟踪 | 陀螺仪驱动角色移动 | `@ohos.sensor.gyroscope` + animateTo |
| 🏃 **运动记录** | 卡路里进度 | 进度动画、状态切换 | 状态机（未开始/进行中/完成） |
| 🌿 **睡眠监测** | 健康数据 | 三叶草起床动画 | 数据驱动 UI 更新 |

### 配置排查清单

互动卡片打不开时按顺序检查：
1. `form_config.json` 的 `name` 是否与 `form_name` 一致
2. `src` 指向的普通卡片文件是否真实存在
3. `defaultDimension` 是否在 `supportDimensions` 列表中
4. `sceneAnimationParams.abilityName` 的值是否存在
5. `module.json5` 是否注册了同名的 `type: "liveForm"` Ability
```
注册开发者 → AGC 创建应用 → 生成签名 → 打包 HAP → 上传 → 填写信息 → 审核 → 上架
```

### 签名准备
| 文件 | 格式 | 用途 |
|------|:----:|------|
| **密钥库文件** | .p12 | 存储公私钥对 |
| **证书请求文件** | .csr | 向 AGC 申请数字证书 |
| **数字证书** | .cer | 由 AGC 颁发 |
| **Profile 文件** | .p7b | 包含包名、证书、权限列表 |

### 关键步骤
1. **DevEco Studio 生成密钥**：Build → Generate Key → 生成 .p12 + .csr
2. **AGC 申请证书**：上传 .csr → 下载 .cer 和 .p7b
3. **配置签名**：在 `build-profile.json5` 中配置 signingConfigs
4. **打包 HAP**：Build → Build HAP(s) → App/Plugin
5. **AGC 上传**：选择已签名的 HAP 包上传
6. **填写发布信息**：国家/地区、价格、隐私政策链接
7. **提交审核**：通常 1~3 个工作日

### 上架合规重点
- 应用名称、图标、描述不能侵权
- 隐私政策必须包含数据收集说明
- 涉及用户信息的权限必须有对应功能
- 元服务需注意分包大小限制和免安装特性

---

## 🧩 ArkUI 高频组件速查

### 布局类
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **Row / Column** | 线性布局（水平/垂直） | `.justifyContent()` `.alignItems()` 控制对齐 |
| **Stack** | 层叠布局，子组件可重叠 | 默认居中，`alignContent` 控制叠放对齐 |
| **Flex** | 弹性布局，等分空间 | `.wrap(FlexWrap.Wrap)` 换行、`flexGrow`/`flexShrink` |
| **RelativeContainer** | 相对定位，子组件基于父容器/兄弟锚定 | `alignRules: { left: { anchor: 'container', align: HorizontalAlign.Start } }` |
| **Grid / GridItem** | 栅格布局，适合后台列表/卡片墙 | `columnsTemplate('1fr 1fr 1fr')` 控制列数 |
| **WaterFlow** | 瀑布流容器，商品流/图片墙 | `columnsTemplate('1fr 1fr')` + `FlowItem` 子项，`onReachEnd` 触发加载更多 |

### 滚动与导航
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **Scroll** | 可滚动容器 | `.scrollable(ScrollDirection.Vertical)` 设置方向 |
| **List / ListItem** | 列表（支持 sticky 分组） | `List()` + `ForEach` + `ListItem`，`onScrollIndex` 监听滚动位置 |
| **Swiper** | 轮播/滑动切换页 | `autoPlay(true)` `interval(3000)` `indicator(true)` 自动轮播+指示器 |
| **Tabs / TabContent** | 选项卡切换 | `barPosition(BarPosition.Start)` 控制标签位置 |
| **Navigation** | 页面路由+栈导航 | `NavPathStack` + `NavDestination`，推荐替代 Router |

### 信息展示
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **Text** | 文本展示 | `.fontSize()` `.fontColor()` `.textAlign()` 多行用 `TextOverflow.Ellipsis` |
| **Image** | 图片展示 | `.objectFit(ImageFit.Cover)` `.source($rawfile('a.png'))` |
| **Video** | 视频播放 | `.src($rawfile('v.mp4'))` `.autoPlay(true)` `.controls(true)` |
| **RichText** | 富文本/HTML 渲染 | 直接传入 HTML 字符串，支持基本标签 |
| **Progress** | 进度条 | `Progress({ value: 50, total: 100 })` `.style(ProgressStyle.Linear)` |

### 交互输入
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **Button** | 按钮 | `.onClick()` `.type(ButtonType.Capsule)` |
| **TextInput** | 单行文本输入 | `.onChange(v => this.v = v)` `.placeholder('请输入')` |
| **TextArea** | 多行文本输入 | 同 TextInput，多行自动换行 |
| **Slider** | 滑块选择器 | `.onChange(v => this.val = v)` `.min(0)` `.max(100)` |
| **Toggle** | 开关 | `.type(ToggleType.Switch)` `.onChange(v => this.on = v)` |
| **Radio** | 单选项 | 需配合 RadioGroup 使用 |
| **Checkbox** | 多选项 | `.onChange(v => this.checked = v)` |
| **Select** | 下拉选择 | `Select([{value:'a'},{value:'b'}])` `.onSelect((i,v)=>...)` |
| **DatePicker / TimePicker** | 日期/时间选择 | `DatePicker({ start: new Date(), selected: this.date })` |

### 弹窗与面板
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **AlertDialog** | 确认弹窗 | `AlertDialog.show({ title, message, confirm })` |
| **CustomDialog** | 自定义弹窗 | `@CustomDialog` 装饰器 + `customDialog: CustomDialogController` |
| **Sheet** | 底部面板 | `.bindSheet($$this.show, { height: SheetSize.LARGE })` |
| **Panel** | 可拖拽面板 | `Panel({ mode: PanelMode.Half })` 支持悬浮/半屏/全屏 |

### 高性能与特殊
| 组件 | 用途 | 关键用法 |
|------|------|---------|
| **XComponent** | 原生渲染引擎接入 | `type: XComponentType.SURFACE` 用于游戏引擎、相机预览 |
| **Web** | WebView 容器 | `.src('https://...')` `.javaScriptAccess(true)` |
| **Canvas / CanvasPattern** | 2D 画布自定义绘制 | 获取 CanvasRenderingContext2D 绘制图形 |
| **Shape** | 矢量图形 | `Circle()` `Rect()` `Path()` 支持描边/填充 |
| **QRCode** | 二维码生成 | `QRCode({ value: 'https://...' })` 自动生成扫码图案 |

---

## 🧬 Ability 框架深度

### 三种启动模式
| 模式 | 说明 | 适用场景 | 配置方式 |
|------|------|---------|---------|
| **singleton** | 单例，只创建一个实例复用 | 主页面、播放器 | module.json5 中 `"launchType": "singleton"` |
| **multiton** | 每次启动创建新实例 | 独立任务、多窗口编辑 | `"launchType": "multiton"` |
| **specified** | 根据 Key 按需匹配/创建实例 | 聊天窗口（每个对话独立实例） | `"launchType": "specified"` + `onNewWant()` 处理 |

### AbilityStage（应用级入口）
```typescript
// 自定义 AbilityStage，在 module.json5 中配置 srcEntry
export default class MyAbilityStage extends AbilityStage {
  onCreate(): void { /* 应用初始化逻辑 */ }
  onAcceptWant(want: Want): string {
    // specified 模式下根据 Want 返回实例 Key
    return `conversation_${want.parameters?.conversationId}`;
  }
}
```

### Call / Callee 通信（UIAbility 间调用）
```
caller → want 信息
Caller Ability ──────────────> Callee Ability
                 调用请求
                         callee.on('method', (data) => { return result; });
```

```typescript
// Caller 端
const caller = await context.startAbilityByCall({ bundleName, abilityName });
await caller.call('login', { user: 'admin' });

// Callee 端（被调方注册方法）
import { Caller } from '@kit.AbilityKit';
callee.on('login', (data) => {
  console.info('Received:', data);
  return { token: 'xxx' };
});
```

### ServiceExtensionAbility（后台服务）
```typescript
export default class MyService extends ServiceExtensionAbility {
  onCreate(want: Want): void { /* 启动后台任务 */ }
  onRequest(want: Want, startId: number): void { /* 处理请求 */ }
  onConnect(want: Want): rpc.RemoteObject { return new MyStub('service'); }
  onDestroy(): void { /* 清理资源 */ }
}
```
| 用途 | 说明 |
|------|------|
| 后台下载 | 文件下载、数据同步，前台可绑定获取进度 |
| 音乐播放 | 保持后台播放，即使 UI 被销毁 |
| 传感器监听 | 持续监听传感器数据，回传给 UI |

### UIAbility 生命周期
```
onCreate() → onWindowStageCreate() → onForeground() → [可见交互]
    ↓                                              ↓
onDestroy() ← onBackground() ← onWindowStageDestroy()
```
- `onCreate`: 应用初始化（全局变量、数据预加载）
- `onWindowStageCreate`: 设置窗口属性、加载页面
- `onForeground`: 进入前台（恢复动画、重新订阅）
- `onBackground`: 进入后台（保存草稿、释放资源）
- `onWindowStageDestroy` / `onDestroy`: 释放全局资源

---

## 📐 Module 与分包

### 三种包类型
| 类型 | 全称 | 特点 | 使用场景 |
|------|------|------|---------|
| **HAP** | Harmony Ability Package | 可独立安装运行的基础单元 | 应用功能模块 |
| **HAR** | Harmony Archive | 静态共享包（编译时打包进 HAP） | 公共库、工具类、基座组件 |
| **HSP** | Harmony Shared Package | 动态共享包（运行时按需加载） | 按需加载的插件化模块 |

### 如何选择
| 场景 | 推荐 |
|------|:----:|
| 应用主入口 | `entry` 类型 HAP |
| 功能模块（可独立） | `feature` 类型 HAP |
| 工具函数/网络层/数据层 | HAR（静态共享，编译打包） |
| 需要按需加载的业务模块 | HSP（动态共享，分包下载） |

### 多 Module 工程结构
```
MyApp/
├── entry/                  # 主模块 HAP
│   └── src/main/module.json5
├── feature-home/           # 首页模块 HAP
├── feature-profile/        # 个人中心 HAP
├── library-common/         # 公共库 HAR
│   └── src/main/ets/utils/
├── library-network/        # 网络库 HAR
├── plugin-payment/         # 支付插件 HSP（按需加载）
└── build-profile.json5     # 工程级配置
```

### module.json5 关键配置
```json5
{
  module: {
    name: 'entry',
    type: 'entry',         // entry | feature | har | shared
    srcEntry: './ets/entryability/EntryAbility.ts',
    description: '主模块',
    mainElement: 'EntryAbility',
    deviceTypes: ['phone', 'tablet'],
    // HAP/HSP 中声明的 abilities
    abilities: [
      { name: 'EntryAbility', srcEntry: './ets/...', launchType: 'singleton' }
    ],
    // 依赖的 HAR/HSP
    dependencies: [
      { name: 'library-common', version: '1.0.0' }
    ],
    // 请求权限
    requestPermissions: [
      { name: 'ohos.permission.INTERNET', reason: '网络连接' }
    ]
  }
}
```

### build-profile.json5 关键配置
```json5
{
  app: {
    bundleName: 'com.example.myapp',
    version: { code: 1000000, name: '1.0.0' },
    // 签名配置
    signingConfigs: [
      {
        name: 'default',
        type: 'HarmonyOS',
        storeFile: './signing/keystore.p12',
        storePassword: '',
        keyAlias: 'mykey',
        keyPassword: '',
        profileFile: './signing/Profile.p7b',
        certpath: './signing/Certificate.cer',
      }
    ]
  },
  modules: [
    { name: 'entry', srcPath: './entry' },
    { name: 'library-common', srcPath: './library-common' }
  ]
}
```

---

## 🧵 并发与状态管理（ConcurrentModule + StateManagement + Logger）

### ConcurrentModule — TaskPool + Worker

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function computePrimes(limit: number): number[] {
  const primes: number[] = [];
  for (let i = 2; i <= limit; i++) {
    if (primes.every(p => i % p !== 0)) primes.push(i);
  }
  return primes;
}

async function run(): Promise<void> {
  const task = new taskpool.Task(computePrimes, [100000]);
  const result = await taskpool.execute(task);
}
```

### StateManagement — 页面级/应用级状态

```typescript
// AppStorage: 应用级全局状态
AppStorage.setOrCreate('userName', 'guest');

// LocalStorage: 页面级状态（跨组件共享）
let storage = new LocalStorage();
storage.setOrCreate('count', 0);

@Entry(storage)
@Component
struct PageA { @LocalStorageProp('count') count: number = 0; }
@Component
struct ChildB { @LocalStorageLink('count') count: number = 0; }

// Preferences: 持久化
import { preferences } from '@kit.ArkData';
const prefs = await preferences.getPreferences(context, 'myPrefs');
await prefs.put('volume', 80);
await prefs.flush();
```

### Logger — hilog 日志

```typescript
import { hilog } from '@kit.PerformanceAnalysisKit';

const DOMAIN = 0x0001;
const TAG = 'MyApp';

hilog.info(DOMAIN, TAG, 'User logged in: %{public}s', userName);
hilog.warn(DOMAIN, TAG, 'Disk usage: %d%%', usage);
hilog.error(DOMAIN, TAG, 'Failed to load: %{private}s', errMsg); // 敏感信息用 private
```

---

## 🧩 ComponentCollection 组件大全（第二轮新增）

> **来源**：`component-collection` | ⭐22下载 | Gitee harmonyos_samples | 源码级

本示例为 ArkUI 中**组件、通用属性、动画、全局方法**的四大模块集合，通过 `Tabs` 容器搭建整体框架，每个 TabContent 使用 `List` 容器 + 循环渲染加载分类导航数据。

### 📐 架构骨架

```
entry/src/main/ets/
├── common/             # 公共组件
│   ├── AttributeModificationTool.ets
│   ├── IntroductionTitle.ets
│   ├── TabContentNavigation.ets
│   └── TitleBar.ets
├── data/               # 数据层 (CollectionCategory + ResourceDataHandle)
├── model/              # 数据模型 (CategoricalDataType)
├── pages/              # 页面
│   ├── Index.ets       # Tabs 首页
│   ├── animations/     # 动画模块
│   ├── components/     # 组件模块
│   ├── globalMethods/  # 全局方法模块
│   └── universal/      # 通用模块
└── util/               # Logger + ShowToast
```

### 🏗️ 四大模块速览

| 模块 | 子模块 | 核心组件/API |
|------|--------|-------------|
| **组件** | 空白分隔、按钮选择、滚动滑动、信息展示、文本输入、辅助、Canvas、行列分栏、Flex栅格、列表宫格、导航、图形绘制、媒体、Web | Divider/Button/Checkbox/Slider/Swiper/DataPanel/Gauge/Marquee/Particle/PatternLock/AlphabetIndexer/Canvas/Column/Row/SideBarContainer/Stack/Flex/GridRow/Navigation/Tab/Web |
| **通用** | 事件（点击/触摸/拖拽/焦点/键鼠）、属性（背景/边框/显示/特效/字体/裁剪/安全区）、手势（Tap/LongPress/Pan/Pinch/Rotation/Swipe） | onClick → onDrag → pan → pinch → rotation → combined |
| **动画** | 组件转场、页面转场、共享元素、布局动效、尺寸变换、悬浮窗、文件夹展开、图库卡片、商店卡片、侧边栏、路径动画、属性动画 | Transition/PageTransition/SharedTransition/LayoutAnimation/SizeTransition |
| **全局方法** | AlertDialog/ActionSheet/CustomDialog/DateDialog/TimeDialog/TextPickerDialog/Menu | 弹窗 API 集合 |

### 🔑 核心模式：Tabs + List 框架（可直接复用）

```typescript
// [API 23+] Tabs + List 分类导航框架
@Component
struct CollectionIndex {
  @State currentIndex: number = 0
  private categories: CollectionCategory[] = [ /* 分类数据 */]

  build() {
    Tabs({ index: this.currentIndex }) {
      ForEach(this.categories, (category: CollectionCategory) => {
        TabContent() {
          List() {
            ForEach(category.items, (item: CategoricalData) => {
              ListItem() {
                // 使用 Navigation 或 router 跳转详情
                Text(item.name)
              }
            })
          }
        }.tabBar(this.TabBuilder(category.name))
      })
    }
    .vertical(false)
    .barWidth('100%')
    .barHeight(56)
  }

  @Builder TabBuilder(title: ResourceStr) {
    Text(title).fontSize(14).fontColor('#666')
  }
}
```

---

## 📦 MultiHap 多HAP构建工程（第二轮新增）

> **来源**：`multi-hap` | 工程架构 | 源码级

### 场景
一个应用中同时包含 `entry HAP`（主入口）和多个 `feature HAP`（音频/视频播放），各 HAP 独立打包、独立安装。

### 工程结构
```
├── entry/              # "type": "entry" - 主模块
│   └── pages/Index.ets     # 首页 + 多HAP跳转逻辑
├── audioFeature/       # "type": "feature" - 音频播放
│   └── audioAbility/AudioAbility.ets
├── videoFeature/       # "type": "feature" - 视频播放
│   └── videoability/VideoAbility.ets
```

### 关键配置
```json5
// entry/src/main/module.json5
{ "type": "entry" }
// audioFeature/src/main/module.json5
{ "type": "feature" }
// videoFeature/src/main/module.json5
{ "type": "feature" }
// AppScope/app.json5
{ "bundleName": "com.samples.multihap" }
```

### 多HAP跳转代码
```typescript
// [API 23+] 使用 Want 跳转 feature HAP
import { common, Want } from '@kit.AbilityKit'

@Entry
@Component
struct Index {
  private context = getContext(this) as common.UIAbilityContext

  build() {
    Button('播放音频')
      .onClick(() => {
        let want: Want = {
          bundleName: 'com.samples.multihap',
          abilityName: 'AudioAbility'  // audioFeature 中的 Ability
        }
        this.context.startAbility(want)
      })
  }
}
```

### 部署方式
1. `Build → Build Hap(s) → Build Hap(s)` 构建各模块 hap
2. `Edit Configurations → Deploy Multi Hap → 勾选 audioFeature + videoFeature`
3. 设备安装后显示一个主 entry HAP

---

## 🖱️ DragFramework 拖拽框架（第二轮新增）

> **来源**：`DragFramework` | Gitee harmonyos_samples | 源码级

### 场景
本示例实现**图片、富文本、文本、输入框、列表、超链接、本地视频、在线图片**等组件的拖拽功能，支持水印、自定义背板、AI识别、图文混排、分屏拖拽、跨设备拖拽。

### 默认拖拽能力

| 组件 | 拖出(draggable) | 拖入(onDrop) |
|------|:--------------:|:-----------:|
| Search | ✅ | ✅ |
| TextInput | ✅ | ✅ |
| TextArea | ✅ | ✅ |
| RichEditor | ✅ | ✅ |
| Text | ✅ | - |
| Image | ✅ | - |
| Hyperlink | ✅ | - |
| FormComponent | ✅ | - |
| Video | - | ✅ |

### 自定义拖拽背板
```typescript
// [API 23+] onDragStart 自定义拖拽背板
Image(this.imageSrc)
  .draggable(true)
  .onDragStart(() => {
    // 返回自定义背板组件
    return this.buildCustomDragPanel()
  })
```

### AI识别拖拽内容
```typescript
// [API 23+] onDrop 实现 AI 识别
TextInput()
  .onDrop((event: DragEvent) => {
    let data = event.getData()
    // 调用 AI 接口识别 data 内容
    this.aiRecognitionResult = data
  })
```

### 图文混排拖拽
支持三种方式：
1. **Text 组件** — 拖拽 Text 中的图文混排内容
2. **RichEditor 组件** — 拖拽富文本编辑器内容
3. **MultiEntry（UDMF）** — 构造多 Record 类型和多 Entry 类型数据

### 分屏拖拽
通过单实例模式（`singleton`）实现同一应用分屏拖拽。

---

## ✏️ HandWritingToImage 手写绘制保存图片（第二轮新增）

> **来源**：`hand-writing-to-image` | Gitee harmonyos_samples | 源码级

### 核心链路
```
NodeContainer ← MyNodeController → rootRenderNode
    ↓ onTouch
创建子 RenderNode → Pen + Path 绘制轨迹 → getChild/removeChild 撤销
    ↓ componentSnapshot.get
PixelMap → Image.packToFile() / packing() → 保存为图片
```

### 完整代码模式
```typescript
// [API 23+] 自定义渲染节点手写绘制
class MyRenderNode extends RenderNode {
  private pen: Drawing.Pen = new Drawing.Pen()
  private path: Drawing.Path = new Drawing.Path()

  constructor() {
    super()
    this.pen.setColor({ alpha: 255, red: 0, green: 0, blue: 0 })
    this.pen.setStrokeWidth(4)
  }

  draw(context: DrawContext) {
    context.canvas.attachPen(this.pen)
    context.canvas.drawPath(this.path)
    context.canvas.detachPen()
  }

  updatePath(newPath: Drawing.Path) {
    this.path = newPath
  }
}

class MyNodeController extends NodeController {
  private rootRenderNode: MyRenderNode
  private nodeCount: number = 0

  makeNode(uiContext: UIContext): RenderNode | null {
    this.rootRenderNode = new MyRenderNode()
    return this.rootRenderNode
  }

  addStroke(path: Drawing.Path) {
    let node = new MyRenderNode()
    node.updatePath(path)
    this.rootRenderNode?.appendChild(node)
    this.nodeCount++
  }

  undoStroke() {
    let last = this.rootRenderNode?.getChild(this.nodeCount - 1)
    if (last) {
      this.rootRenderNode?.removeChild(last)
      this.nodeCount--
    }
  }

  clearAll() {
    this.rootRenderNode?.clearChildren()
    this.nodeCount = 0
  }
}
```

### 保存为图片
```typescript
// [API 23+] 使用 componentSnapshot 获取 PixelMap 并保存
async function saveToImage(componentId: string): Promise<string> {
  let pixelMap: PixelMap = await componentSnapshot.get(componentId)

  // 方式一: packToFile
  let path = getContext().cacheDir + '/drawing.png'
  let packer = image.createImagePacker()
  let packOpts: image.PackingOption = { format: 'image/png', quality: 100 }
  packer.packToFile(pixelMap, path, packOpts)
  return path

  // 方式二: packing (返回 ArrayBuffer)
  // let data: ArrayBuffer = await packer.packing(pixelMap, packOpts)
}
```

---

## 🗺️ SystemRouterMap 系统路由表（第二轮新增）

> **来源**：`system-router-map` | Gitee harmonyos_samples | 源码级

### 场景
通过**系统路由表（route_map.json）**实现多模块（HSP/HAR）页面跳转，**零依赖耦合**，懒加载未跳转页面。

### 核心架构
```
entry (主模块) → route_map.json → harA / harB / hspA / hspB
```
各模块之间不需要配置依赖关系，跳转时动态加载目标页面。

### 配置步骤

**Step 1: 目标模块 module.json5 添加路由配置**
```json5
// harA/src/main/module.json5
{
  "module": {
    "routerMap": "$profile:route_map"
  }
}
```

**Step 2: 创建 route_map.json**
```json5
// resources/base/profile/route_map.json
{
  "routerMap": [
    {
      "name": "PageFromHarA",
      "buildFunction": "HarABuilder",
      "pageSourceFile": "src/main/ets/components/mainpage/A1.ets"
    },
    {
      "name": "PageFromHspB",
      "buildFunction": "HspBBuilder",
      "pageSourceFile": "src/main/ets/components/mainpage/B1.ets"
    }
  ]
}
```

**Step 3: 目标页面暴露 Builder 函数**
```typescript
// harA 目标页面
@Builder
export function HarABuilder() {
  A1Page()
}

@Component
struct A1Page {
  build() { /* ... */ }
}
```

**Step 4: 主模块跳转**
```typescript
// [API 23+] 通过系统路由表跳转
import { router } from '@kit.ArkUI'

Button('跳转 HAR A 页面')
  .onClick(() => {
    router.pushDestinationByName('PageFromHarA')
  })
```

### 优势
- ✅ 模块间零依赖耦合
- ✅ 页面按需加载（未跳转不加载）
- ✅ 已加载页面缓存复用

---

## 🧭 NavigationRouter 路由模块解耦（第二轮新增）

> **来源**：`navigation-router` | Gitee harmonyos_samples | 源码级

### 场景
将路由功能抽取为**独立 RouterModule HAR**，统一管理 Navigation 下多 HAR/HSP 的路由跳转，实现业务模块间解耦。

### 架构
```
entry (主入口 + Navigation)
  ├── harA ───→ RouterModule (路由委托)
  ├── harB ───→ RouterModule
  ├── harC ───→ RouterModule
  └── RouterModule (路由管理)
```

### 工程目录
```
RouterModule/
├── Index.ets                       # 对外暴露路由方法和常量
├── src/main/ets/constants/
│   └── RouterConstants.ets         # 路由信息常量
├── src/main/ets/model/
│   └── RouterModel.ets             # 路由信息模型
└── src/main/ets/utils/
    └── RouterModule.ets            # 核心路由管理
```

### RouterModule 核心代码
```typescript
// [API 23+] RouterModule 对外暴露的路由管理类
import { RouterConstants } from '../constants/RouterConstants'

export class RouterModule {
  static push(routerName: string, param?: Record<string, Object>) {
    // 根据 routerName 查找对应页面信息
    let pageInfo = RouterConstants.PAGE_MAP[routerName]
    // 通过 Navigation pushPath 跳转
    this.navPathStack.pushPath({ name: pageInfo.name, param: param })
  }

  static back() {
    this.navPathStack.pop()
  }
}

// 业务模块中调用
// RouterModule.push('PageA1', { id: 123 })
```

### 优势
- ✅ 业务模块仅依赖 RouterModule，不依赖其他业务模块
- ✅ 路由逻辑统一管理，新增页面只需在 RouterConstants 注册
- ✅ 适合大型多模块应用

---

## 📤 RcpFileTransfer RCP文件传输（第二轮新增）

> **来源**：`RcpFileTransfer` | Gitee harmonyos_samples | 源码级

### 场景
基于 **Remote Communication Kit（RCP）** 实现相册文件上传下载、分片下载、断点续传、后台传输。

### 功能矩阵
| 功能 | 页面 | 关键 API |
|------|------|----------|
| 相册图片上传 | AlbumImageTrasfer | `rcp.post()` |
| 相册图片下载 | AlbumImageTrasfer | `rcp.fetch()` / `rcp.downloadToFile()` |
| 文件分片下载 | ChunkedFileTransfer | Range header + 分片合并 |
| 断点续传 | ResumableFileTransfer | ETag + If-Range |
| 后台传输 | BackgroundFileTransfer | Service Ability + KEEP_BACKGROUND_RUNNING |

### 工程目录
```
entry/src/main/ets/
├── pages/
│   ├── AlbumImageTrasfer.ets          # 相册上传下载
│   ├── BackgroundFileTransfer.ets     # 后台传输
│   ├── ChunkedFileTransfer.ets        # 分片下载
│   ├── ResumableFileTransfer.ets      # 断点续传
│   └── Index.ets                      # 首页
├── service/
│   ├── FileRequest.ets                # 请求接口模块
│   ├── Interceptor.ets                # 请求拦截器
│   └── Model.ets                      # 数据类型定义
└── utils/
    ├── CommonUtil.ets
    └── LocalFileUtil.ets
```

### RCP 下载代码模式
```typescript
// [API 23+] RCP 文件下载
import { rcp } from '@kit.RemoteCommunicationKit'

async function downloadFile(url: string, savePath: string): Promise<void> {
  let session = rcp.createSession()
  let request = new rcp.Request(url, rcp.Method.GET)
  let response = await session.fetch(request)
  // 方式一: 直接写入文件
  await response.toFile(savePath)
}

// 断点续传
async function resumeDownload(url: string, savePath: string, offset: number): Promise<void> {
  let session = rcp.createSession()
  let request = new rcp.Request(url, rcp.Method.GET)
  request.setHeader('Range', `bytes=${offset}-`)
  let response = await session.fetch(request)
  await response.toFile(savePath, { append: true })
}
```

### 权限
```json5
"ohos.permission.INTERNET"
"ohos.permission.GET_NETWORK_INFO"
"ohos.permission.KEEP_BACKGROUND_RUNNING"
```

---

### 2026-06-29 - 补齐结构级→源码级：购物/支付/短视频/实况窗（第十一轮）

- **场景**：用户要求将结构级升级为源码级
- **MultiShoppingPriceComparison** → 补全 Navigation Split 分栏 + Tabs 响应式 + BreakpointType 完整代码
- **MultiMobilePayment** → 补全三层架构 + Scan Kit 扫码/码图生成完整代码
- **MultiShortVideo** → 补全 Swiper + Video 短视频上下滑动 + cachedCount 完整代码
- **LiveViewLockScreen**（BestPracticeSnippets）→ 新增 LiveViewKit 锁屏实况窗完整章节，含 publish/dismiss/状态监听 + 进度模板 + 权限说明
- **所有结构级项目已升级为源码级**

---

## 🚀 UIAbility 启动三种模式（第三轮新增）

> **来源**：`ability-start-mode` | Gitee harmonyos_samples | 源码级

Stage 模型中 `launchType` 决定 UIAbility 的启动行为：

| 模式 | module.json5 | 行为 |
|------|-------------|------|
| **singleton** | `"launchType": "singleton"` | 单实例，每次 startAbility 复用已有实例 |
| **standard**（默认） | `"launchType": "multiton"` | 多实例，每次新建 UIAbility |
| **specified** | `"launchType": "specified"` | 自定义实例标识，MyAbilityStage.onAcceptWant 返回标识 |

### Specified 模式核心代码

```typescript
// [API 23+] MyAbilityStage.onAcceptWant 自定义实例标识
export default class MyAbilityStage extends AbilityStage {
  onAcceptWant(want: Want): string {
    // 根据 want.parameters 返回标识字符串
    // 相同标识复用实例，不同标识创建新实例
    return want.parameters?.key as string ?? ''
  }
}
```

---

## 🎨 CustomCanvas 画布功能（第三轮新增）

> **来源**：`custom-canvas` | Gitee harmonyos_samples | 源码级

### 功能

| 功能 | 实现方式 |
|------|---------|
| 自由绘制 | `onTouch` → `Path2D.moveTo/lineTo` |
| 橡皮擦 | `strokeStyle = '#FFFFFF'`（白色覆盖） |
| 撤回/重做 | `drawPathList` 数组 pop/push |
| 清空 | 清空 `drawPathList` + `redoList` 重绘 |
| 笔刷分类 | 圆珠笔（alpha=1固定）/马克笔（alpha可调） |
| 缩放 | `pan` 手势 → `matrix4` 变换 |
| 半模态弹窗 | `bindSheet` 选颜色/粗细/不透明度 |

### 核心绘制代码

```typescript
// [API 23+] Canvas 绘制 + 撤销/重做
let drawPathList: Array<Path2D> = []
let redoList: Array<Path2D> = []

Canvas(this.context)
  .onTouch((event: TouchEvent) => {
    if (event.type === TouchType.Move) {
      let path = new Path2D()
      path.moveTo(prevX, prevY)
      path.lineTo(curX, curY)
      drawPathList.push(path)
      redoList = []
      this.context.stroke(path)
    }
  })
```

---

## 🖼️ PicturePreview 图片预览（第三轮新增）

> **来源**：`PicturePreview` | Gitee harmonyos_samples | 源码级

### 功能矩阵

| 功能 | API | 说明 |
|------|-----|------|
| 左右滑动切换 | `Swiper` + `ForEach` | 主图 + 缩略图双联动 |
| 双击缩放 | `matrix4` 变换 | 双击切换 1x ↔ 2x |
| 双指捏合 | `Pinch` 手势 + `matrix4` | 自由缩放 |
| 平移查看 | `translate` + `PanGesture` | 放大后滑动查看 |
| 缩略图导航 | `ThumbnailView` + 索引联动 | 点击缩略图定位主图 |
| 全屏预览 | 轻触切换 overlay 模式 | 隐藏/显示 UI 元素 |

### 核心缩放代码

```typescript
// [API 23+] matrix4 矩阵缩放手势
@State matrix: matrix4.Matrix4Transit = matrix4.identity().copy()

Image(this.imageData)
  .transform(this.matrix)
  .translate({
    x: this.curOffsetX,
    y: this.curOffsetY
  })
  .objectFit(ImageFit.Cover)
  .gesture(
    TapGesture({ count: 2 })
      .onAction(() => {
        let anim = this.matrix
        animateTo({ duration: 300 }, () => {
          this.matrix = matrix4.identity().scale({ x: scale, y: scale }).copy()
        })
      })
  )

---

## 📜 BottomDrawerSlideCase 底部抽屉滑动（第四轮新增）

> **来源**：`bottom-drawer-slide-case` | Gitee harmonyos_samples | 源码级

利用 `List` 实现底部抽屉滑动效果，`RelativeContainer` + `Stack` 实现沉浸式全屏 + 地图可拖动。

### 核心原理

```typescript
// [API 23+] 分阶抽屉滑动
List({ space: 8 }) {
  ForEach(this.items, (item: string) => {
    ListItem() { Text(item) }
  })
}
.onTouch((event: TouchEvent) => {
  // 1. 记录 down / up 纵坐标
  // 2. 按区间设置列表高度（三阶：10%/50%/90%）
  // 3. 手指离开 → animateTo 吸附到最近阶
})
```

---

## 🎨 EffectKit 自适应背景取色（第四轮新增）

> **来源**：`effect-kit` | Gitee harmonyos_samples | 源码级

使用 `EffectKit.colorPicker` 对图片取色，作为背景渐变色的自适应方案。

```typescript
// [API 23+] ColorPicker 取色主色调
import { effectKit } from '@kit.ArkGraphics2D'

async function getDominantColor(pixelMap: PixelMap): Promise<string> {
  let colorPicker = effectKit.createColorPicker(pixelMap)
  let color = colorPicker.getMainColorSync()
  return `rgba(${color.red}, ${color.green}, ${color.blue}, 1)`
}
// Swiper.onAnimationStart → animateTo 渐变切换背景
```

---

## 🔀 GridDragSort Grid拖拽排序（第四轮新增）

> **来源**：`grid-drag-sort` | Gitee harmonyos_samples | 源码级

### 四种场景

| 场景 | 操作 | 说明 |
|------|------|------|
| 同大小拖拽 | 长按 | 九宫格图片排序 |
| 不同大小拖拽 | 长按 | 设备展示区排序 |
| 直接拖拽 | 直接拖 | 无需长按 |
| 抖动编辑 | 长按后抖 | 可编辑提示 |

```
Grid + PanGesture + animateTo → 记录起始位置 → 交换数据
```

---

## 🌊 Immersive 沉浸式页面（第四轮新增）

> **来源**：`Immersive` | ⭐26 Stars | Gitee harmonyos_samples | 源码级

### 两种沉浸 + 三大场景

| 方式 | API |
|------|-----|
| 背景沉浸 | `background()` 延伸至状态栏 |
| 全屏沉浸 | `ignoreLayoutSafeArea()` + matchParent |
| 隐藏标题栏 | `setWindowDecorVisible(false)` |
| 避让挖孔 | 横竖屏 4 方向适配 |

---

## 📊 KVStore 键值型数据库（第四轮新增）

> **来源**：`KVStore` | Gitee harmonyos_samples | 源码级

```typescript
// [API 23+] KVStore 增删改查
import { distributedKVStore } from '@kit.ArkData'

let kvManager = distributedKVStore.createKVManager({
  bundleName: 'com.example.app', context: getContext(this)
})
let kvStore = await kvManager.getKVStore('storeId', {
  createIfMissing: true, encrypt: false,
  securityLevel: distributedKVStore.SecurityLevel.S1
})
await kvStore.put('key1', 'value1')       // 写
let val = await kvStore.get('key1')       // 读
await kvStore.delete('key1')              // 删
let all = await kvStore.getEntries()      // 查全部
```

---

## 📝 TextExpand 文本展开折叠（第四轮新增）

> **来源**：`TextExpand` | Gitee harmonyos_samples | 源码级

| 方案 | 技术 | 场景 |
|------|------|------|
| MeasureText | Canvas 2D 预排版 | 纯文本截断 |
| ParagraphBuilder | `@ohos.graphics.text` | 富文本截断 |

```typescript
// ParagraphBuilder 检测超行
let paragraph = new text.ParagraphBuilder()
  .pushStyle({ fontSize: 16 }).addText('长文本...').build()
paragraph.layout(maxWidth)
let isOverflow = paragraph.didExceedMaxLines()
```

---

## 📜 ListScrollComponent 长列表组件（第五轮新增）

> **来源**：`ListScrollComponent`（基于 `@hadss/scroll_components`） | Gitee harmonyos_samples | 源码级

### 12种长列表场景

| 场景 | 技术方案 |
|------|---------|
| 组件复用 | `ListManager` + `registerNodeItem` + `wrapBuilder` |
| 分组布局 | 分组列表 + 分组吸顶 + 二级联动 |
| 跨页面复用 | `NodePool` 全局复用池，切换页面不丢帧 |
| 加速首屏 | 组件分帧预创建 + 懒加载 |
| 下拉刷新/上拉加载 | `onReachStart`/`onReachEnd` |
| 无限滑动 | `setDataSource` 动态追加数据 |
| 侧滑删除 | `swipeAction` |
| 多类型列表项 | 根据 data 类型动态渲染不同 NodeItem |
| Tabs吸顶 | Tabs + List 组合 |
| 动态切换列数 | `lanes` 动态控制 |
| 边缘渐隐 | `fadingEdge` |

### ScrollComponents 核心用法

```typescript
// [API 23+] 高性能长列表
import { ListManager, RecyclerView } from '@hadss/scroll_components'

@Builder
function MyItem($$: ESObject) {
  Text($$.title).fontSize(16)
}

class MyListManager extends ListManager {
  onWillCreateItem(index: number, data: ESObject) {
    let node = this.dequeueReusableNodeByType('MyItem')
    node?.setData({ title: data.title })
    return node
  }
}

// 组件中使用
RecyclerView({ viewManager: this.myListManager })
```

---

## 📥 MultiFileDownload 多文件下载（第五轮新增）

> **来源**：`multi-file-download` | Gitee harmonyos_samples | 源码级

### 核心能力
`@ohos.request` 管理多个下载任务的进度和状态，List 展示下载队列。

```typescript
// [API 23+] 多文件下载管理
downloadUrlArray.forEach((url, index) => {
  let task = await request.agent.create(context, { url, saveas: `file_${index}.zip` })
  tasks.push(task)
  task.on('progress', (info) => { this.updateProgress(index, info) })
  task.on('complete', () => { this.updateStatus(index, '完成') })
  task.on('fail', () => { this.updateStatus(index, '失败') })
  task.start()
})

// 全部开始 / 全部暂停 / 单个控制
```

---

## 🎯 MultiTarget 多目标产物工程（第五轮新增）

> **来源**：`MultiTarget` | Gitee harmonyos_samples | 源码级

### 场景
一套代码构建 different 版本应用包（official / test），资源/功能差异化定制。

### build-profile.json5 配置

```json5
// 工程级 build-profile.json5
{
  "products": [
    { "name": "official", "signingConfig": "official_sign" },
    { "name": "test", "signingConfig": "test_sign" }
  ]
}
// 模块级: 为每个 target 定制 resources
// entry/src/main/official/resources/  vs  entry/src/main/test/resources/
```

### 差异化项
| 定制项 | 说明 |
|-------|------|
| 资源文件 | 字符串/图片/颜色差异化 |
| 页面逻辑 | 不同版本独立 pages（official_pages / test_pages） |
| 功能开关 | Har 包内条件判断 |

---

## 🎬 SmoothSwitchShortVideos 平滑短视频切换（第五轮新增）

> **来源**：`SmoothSwitchShortVideos` | Gitee harmonyos_samples | 源码级

### 核心优化方案

| 优化 | 实现 |
|------|------|
| **LazyForEach 懒加载** | 只渲染可见区域 + cachedCount 预缓存 |
| **组件复用** | Swiper 滑动 + @Reusable 组件复用 |
| **AVPlayer 预创建** | 冷启动时创建一个播放器到 prepared 状态，每次滑动异步创建下一个 |
| **XComponent Surface** | Surface 类型动态渲染视频流，减少纹理拷贝 |

### 工程结构
```
entry/src/main/ets/
├── model/AVDataSource.ets      # 视频数据源
├── view/VideoPlayView.ets      # 视频播放组件
├── pages/Index.ets              # Swiper 轮播首页
└── common/CommonConstants.ets   # VIDEO_SOURCE 配置
```

---

## 📑 MultiTabNavigation Tab导航样式合集（第六轮新增）

> **来源**：`multi-tab-navigation` | ⭐149 Stars | Gitee harmonyos_samples | 源码级

### 十大导航样式

| 样式 | 实现方式 | 特点 |
|------|---------|------|
| 常见底部导航 | Tabs + barPosition.End | 底部图标+文字 |
| 舵式底部导航 | Tabs + 自定义中间按钮 | 中间突出舵式按钮 |
| 下划线样式 | Tabs + indicator | 指示器跟随滑动 |
| 背景高亮样式 | List 实现 | 选中项背景高亮 |
| 文字样式 | Tabs + fontColor | 文字粗细/颜色变化 |
| 双层嵌套1 | Tabs + 内嵌 List | 外层Tab切换，内层List滚动 |
| 双层嵌套2 | Tabs 嵌套 Tabs | 两层 Tab 联动 |
| 侧边导航 | SideBarContainer | 左侧图标+文字 |
| 抽屉式导航 | SideBarContainer | 点击左上角展开/折叠 |
| 可滑动+更多 | List + 右侧图标 | 溢出滑动，显示更多入口 |

### 核心代码模式

```typescript
// [API 23+] 常见底部导航
Tabs({ barPosition: BarPosition.End }) {
  ForEach(this.tabItems, (item: TabItem) => {
    TabContent() {
      // 对应页面内容
    }.tabBar(this.TabBuilder(item))
  })
}
.width('100%').height('100%')

@Builder TabBuilder(item: TabItem) {
  Column() {
    Image(item.icon).width(24).height(24)
    Text(item.name).fontSize(10)
  }
}
// 双层嵌套: Tabs + 内嵌 List
// 抽屉导航: SideBarContainer({ sideBarWidth: 240 })
```

---

## 🗔 CustomDialogGathers 自定义弹窗合集（第六轮新增）

> **来源**：`custom-dialog-gathers` | ⭐64 Stars | Gitee harmonyos_samples | 源码级

### 八种弹窗类型

| 弹窗类型 | 实现 API | 说明 |
|---------|---------|------|
| 滑动选择 | TimePickerDialog / TextPickerDialog | 系统选择器弹窗 |
| 模态弹窗 | `bindContentCover` | 全屏模态，3种过渡方式 |
| 半模态弹窗 | `bindSheet` | 底部半模态 |
| Toast弹窗 | `CustomDialog` | 3s自动消失 |
| 隐私协议弹窗 | Stack `visibility` 控制 | 弹窗内跳转不关闭 |
| 全屏弹窗 | `translate` + 显式动画 | 手势滑动关闭 |
| 日历选择器 | `CustomDialog` + LazyForEach | 自定义日期范围 |
| 两级半模态 | `bindSheet` 嵌套 `bindSheet` | 二级弹窗联级关闭 |

### 关键代码

```typescript
// [API 23+] 模态弹窗 bindContentCover
@State isPresent: boolean = false

Button('打开模态')
  .bindContentCover($$this.isPresent, {
    builder: () => this.ModalPage(),
    showPageTransition: true  // 页面过渡动画
  })

// 半模态弹窗 bindSheet
Button('打开半模态')
  .bindSheet($$this.isSheetPresent, {
    builder: () => this.SheetPage(),
    mode: SheetMode.HALF    // 半屏模式
  })

// FullScreen 手势滑动关闭
.gesture(
  PanGesture()
    .onActionUpdate((event) => { this.offsetY = event.offsetY })
    .onActionEnd(() => {
      if (this.offsetY > 300) { this.isFullScreen = false }
      else { animateTo({}, () => { this.offsetY = 0 }) }
    })
)
```

---

## 🎬 AVPlayerLongVideo 长视频播放全功能（第六轮新增）

> **来源**：`avplayer-long-video` | Gitee harmonyos_samples | 源码级

### 12种播放功能

| 功能 | 说明 |
|------|------|
| 基本播控 | play/pause/stop/seek |
| 精准跳转 | 按时间/帧精确跳转 |
| 倍速播放 | 0.5x~3x 倍速调节 |
| 音量控制 | 系统音量/应用音量 |
| 亮度控制 | 屏幕亮度滑动调节 |
| 焦点管理 | 播放焦点获取/释放 |
| 前后台感知 | 前台播放/后台暂停 |
| 弹幕发送与显示 | 实时弹幕叠加 |
| 字幕挂载 | 多字幕轨道切换 |
| 视频截图 | `AVPlayer snapshot` |
| 画中画 | PiP 模式播放 |
| 媒体会话 | AVSession 播控集成 |

### 权限
```json5
"ohos.permission.INTERNET"
```

---

## 🎙️ HMOSLiveAudioCall 直播连麦（第六轮新增）

> **来源**：`HMOS_LiveAudioCall` | Gitee harmonyos_samples | 源码级

在 `HMOSLiveStream` 案例基础上增加媒体直播连麦功能：

```
主播端: 采集 → 编码 → 推流
连麦端: 采集 → 编码 → 混流 → 推流
观众端: 拉流 → 解码 → 播放
```

### 关键能力
- AudioCapturer 音频采集
- OH_AVCodec 编解码
- 多路音频混流
- 低延迟音频传输
- 与 HMOSLiveStream 复用直播链路

---

## 🖼️ PixelMapImageEdit 图片编辑（第七轮中高价值①）

> **来源**：`PixelMapImageEdit` | Gitee harmonyos_samples | 源码级

### 功能矩阵

| 分类 | 功能 | 实现方式 |
|------|------|---------|
| **几何变换** | 裁剪/旋转/平移/缩放/镜像 | PixelMap 几何 API |
| **颜色调整** | 亮度/透明度/饱和度 | PixelMap 颜色 API |
| **滤镜** | 多种滤镜效果 | 颜色矩阵变换 |
| **解码** | 图片 → PixelMap | `image.createImageSource` + `createPixelMap` |
| **编码** | PixelMap → 图片文件 | `image.createImagePacker` + `packToFile` |

### 核心代码模式

```typescript
// [API 23+] PixelMap 编辑流程
import { image } from '@kit.ImageKit'

// 1. 解码
let source = image.createImageSource(uri)
let pixelMap = await source.createPixelMap()

// 2. 裁剪
pixelMap.crop({ x: 0, y: 0, width: 500, height: 500 })

// 3. 颜色调整
pixelMap.opacity(0.8)             // 透明度
// pixelMap.setBrightness(0.2)    // 亮度
// pixelMap.setSaturation(1.5)    // 饱和度

// 4. 编码保存
let packer = image.createImagePacker()
let packOpts: image.PackingOption = { format: 'image/jpeg', quality: 95 }
await packer.packToFile(pixelMap, `${getContext().cacheDir}/edited.jpg`, packOpts)
```

---

## 💼 MultiBusinessOffice 多设备办公（第八轮中高价值④）

> **来源**：`MultiBusinessOffice` | Gitee harmonyos_samples | 源码级

### 三页场景 + 多设备适配

| 页面 | 直板机 | 折叠屏(展开) | 平板 |
|------|--------|-------------|------|
| 入口页 | 导航跳转 | 自适应布局 | 自适应布局 |
| 备忘录 | 单栏 | SideBar + 双栏 | 双栏展开 |
| 日历 | 上下显示 | 侧边栏+内容 | 双栏日历 |

### 核心技术

| 能力 | 实现 |
|------|------|
| 侧边栏适配 | `SideBarContainer.sideBarContainerType` + `showSidebar` 断点控制 |
| 单双栏切换 | `Navigation.mode` 根据断点改变 `NavigationMode` |
| 页面拉起 | `UIAbilityContext.startAbility()` 拉起新实例 |
| 断点监听 | `BreakpointSystem` 监听 sm/md/lg |

### 核心代码

```typescript
// [API 23+] SideBarContainer 断点适配
SideBarContainer({ sideBarWidth: 240, type: this.sideBarType }) {
  SideBarContent()
  MainContent()
}
.showSidebar(this.showSidebar)
.onChange((isShow) => { this.showSidebar = isShow })

// 断点控制
// sm: 隐藏+悬浮 → showSidebar=false, type=OVERLAY
// md: 隐藏+悬浮 → showSidebar=false, type=OVERLAY
// lg: 展开+嵌入 → showSidebar=true, type=EMBED
```

---

## ⚙️ Preferences 首选项持久化（第八轮中高价值⑥）

> **来源**：`preferences` | Gitee harmonyos_samples | 源码级

### 核心 API

```typescript
// [API 23+] @ohos.data.preferences 首选项
import { preferences } from '@kit.ArkData'

let prefs = await preferences.getPreferences(getContext(), 'myStore')

// 写
await prefs.put('theme', 'dark')
await prefs.flush()          // 必须 flush 才持久化

// 读
let theme = await prefs.get('theme', 'default')

// 删
await prefs.delete('theme')

// 删除整个 Store
await preferences.deletePreferences(getContext(), 'myStore')
```

### 场景
主题切换 + 数据缓存：切换主题 → `put` + `flush` → 重启应用 → `get` 恢复

---

## 🔄 ListExchange 列表交换删除（第九轮中高价值⑧）

> **来源**：`list-exchange` | ⭐15 Stars | Gitee harmonyos_samples | 源码级

### 核心功能
List 列表项的**交换**与**删除**。

```typescript
// [API 23+] 列表项交换
List() {
  ForEach(this.items, (item: string, index: number) => {
    ListItem() {
      Text(item)
    }
    .gesture(
      LongPressGesture().onAction(() => {
        this.draggedIndex = index
      })
    )
    .onDrag((event: DragEvent) => {
      event.setData(DragUtils.createData(this.items[index]))
    })
    .onDrop((event: DragEvent) => {
      let targetIndex = this.getIndexByPosition(event)
      if (targetIndex !== -1) {
        let temp = this.items[this.draggedIndex]
        this.items[this.draggedIndex] = this.items[targetIndex]
        this.items[targetIndex] = temp
      }
    })
  })
}
```

---

## 💬 ImageComment 图片评论（第九轮中高价值⑨）

> **来源**：`image-comment` | Gitee harmonyos_samples | 源码级

### 功能
1. 点击文本框 → 相机按钮 → 拉起系统相机拍照
2. 拍照返回 → 点击发布 → 发布图片评论

### 工程结构
```
├── utils/CameraUtils.ets          # 拉起系统相机
├── view/CommentItemView.ets       # 评论列表组件
├── view/CommentInputDialog.ets    # 发布评论弹窗
└── view/ImageListView.ets         # 图片列表组件
```

```typescript
// [API 23+] 拉起系统相机
import { camera } from '@kit.CameraKit'
import { photoAccessHelper } from '@kit.MediaLibraryKit'

async function takePhoto(context): Promise<string> {
  // 使用 Camera Kit 或系统相机应用取景拍照
  let helper = photoAccessHelper.getPhotoAccessHelper(context)
  let uri = await helper.takePhoto(context, '拍照')
  return uri
}
```

---

## 🌊 WaterFlow 瀑布流布局（第十轮收尾①）

> **来源**：`water-flow` | Gitee harmonyos_samples | 源码级

### 两个场景

| 场景 | 功能 | 实现 |
|------|------|------|
| 场景一 | 分组混排 + 下拉刷新 + 无限加载 + 长按删除 | `WaterFlow.sections` 分组配置 |
| 场景二 | item 吸顶 + 图片视频混排 + 停止自动播放 | `FlowItem` + `Tabs` + 滚动监听 |

### WaterFlow Sections 核心

```typescript
// [API 23+] WaterFlow sections 分组混排
WaterFlow() {
  LazyForEach(this.sections, (section: WaterFlowSection) => {
    FlowItem() {
      // 每个 flow item 内容
    }
  })
}
.nestedScroll({
  scrollForward: NestedScrollMode.PARENT_FIRST,
  scrollBackward: NestedScrollMode.SELF_FIRST
})
// sections 配置不同列数和间距
// [{ crossCount: 2 }, { crossCount: 3 }, { crossCount: 1 }]
```

---

## 🔀 GridHybrid 网格混合布局（第十轮收尾③）

> **来源**：`grid-hybrid` | Gitee harmonyos_samples | 源码级

### 两种混合场景

| 场景 | 组合 | 实现 |
|------|------|------|
| 场景一 | Grid + List 嵌套 | 双 Scroller 联动 + 水平 List 吸顶 |
| 场景二 | Grid + Swiper 嵌套 | Swiper 动态改变高度 |

---

## 📋 ListItemEdit 列表编辑（第十轮收尾④）

> **来源**：`list-item-edit` | Gitee harmonyos_samples | 源码级

### 功能
基于 List 实现待办事项管理：添加/左滑删除/checkbox 完成。

```typescript
// [API 23+] 列表项左滑删除
ListItem() {
  Text(this.item.name)
}
.swipeAction({
  end: { builder: () => {
    Button('删除').onClick(() => {
      this.todoList.splice(index, 1)
    })
  }}
})
```

---

## 🚀 H5Launch H5冷启动加速（第十轮收尾⑤）

> **来源**：`H5Launch` | Gitee harmonyos_samples | 源码级

### 五大优化方案

| 方案 | API | 说明 |
|------|-----|------|
| 内核预初始化 | `initializeBrowserEngine()` | 提前初始化 ArkWeb 内核 |
| 预连接预解析 | `prepareForPageLoad()` | DNS 预解析 + TCP 预连接 |
| 资源拦截替换 | `onInterceptRequest` + DataCache | 首屏数据本地缓存 |
| JS 预编译 | `precompileJavaScript()` | 生成字节码 Code Cache |
| 离线资源注入 | `injectOfflineResources()` | 免拦截注入静态资源 |

### 核心代码

```typescript
// [API 23+] Web 冷启动优化
import { webview } from '@kit.ArkWeb'

// AbilityStage 中提前初始化
webview.initializeBrowserEngine()

// 预连接
webview.prepareForPageLoad('https://example.com')

// 资源拦截
Web({ src: 'https://example.com', controller: this.controller })
  .onInterceptRequest((event) => {
    // 从本地 DataCache 返回快照数据
    if (isFirstScreen) { return localCacheData }
    return null
  })
```

---

## ✅ 剩余极简仓库（仅列表推荐，无需源码级）

以下仓库功能太简单或被已有内容覆盖，仅做推荐索引：

| 仓库 | 说明 | 覆盖情况 |
|------|------|---------|
| **multi-travel-accommodation** | 多设备旅行住宿页面 | 🟢 被 MultiBusinessOffice 覆盖 |
| **NavigationSettings** | 导航设置页面 | 🟢 被 MultiTabNavigation 覆盖 |
| **PureTabs** | 纯 Tabs 实现 | 🟢 被 MultiTabNavigation 覆盖 |
| **custom-dialog-selection** | 自定义弹窗选择 | 🟡 被 CustomDialogGathers 覆盖 |
| **grid-hybrid** | 已学 ✅ | ✅ |
| **text-effects** | 已学 ✅ | ✅ |
| **water-flow** | 已学 ✅ | ✅ |
| **list-item-edit** | 已学 ✅ | ✅ |
| **H5Launch** | 已学 ✅ | ✅ |
| **FIDO2** | 已学 ✅ | ✅ |
| **location-service** | 已学 ✅ | ✅ |


## 📱 官方 Sample 精选速查

> 华为官方 700+ 示例中精选 **最有学习价值的 10 个**，对标实际开发场景。

| Sample | 核心知识点 | 适用场景 |
|:-------|:----------|:--------|
| **全链路盯盘** | 闪控球+悬浮窗+锁屏卡片+屏保卡片+防窥保护 | 金融/监控类 |
| **互动卡片** | Live Form 互动卡片能力 | 桌面卡片开发 |
| **沉浸光感** | HdsNavigation+HdsTabs+悬浮导航 | UI 现代化改造 |
| **多设备长视频** | 一多架构(三层)+自适应布局+折叠屏/平板/PC | 视频类 App |
| **多设备音乐** | 一多架构+迷你播控+全屏播放+穿戴适配 | 音乐类 App |
| **多设备短视频** | 一多架构+手表适配+评论页+个人作品页 | 短视频类 App |
| **多设备社区评论** | 一多架构+图片预览+社区详情页 | 社区/社交类 |
| **自由流转社交协同** | 应用接续+分布式数据对象+跨设备拖拽+碰一碰 | 协同办公 |
| **媒体直播** | 音视频采集+播放+音频焦点+画面翻转+背景音乐 | 直播类 App |
| **威胁防护文件扫描** | 企业威胁防护+文件隔离/恢复 | 企业安全类 |

**一多架构推荐模式**：
```
三层架构：
┌─ commons/     ← 公共能力（网络/工具/UI组件）
├─ services/    ← 业务逻辑（数据管理/状态管理）
└─ views/       ← 页面视图（按设备形态适配）
```

---


---

# 第十一部分：编译错误与踩坑（错误速查、级联诊断、踩坑记录）

## 🚫 常见编译错误速查（31种）

| # | 错误现象 | 错误码 | 原因 | 修复方案 |
|:-:|---------|:------:|------|---------|
| 1 | `Notification type error` | — | ContentType 类型不兼容 | cast 为 `number` 类型 |
| 2 | `Window type error` | — | window.getLastWindow 类型推断问题 | 改用回调模式 |
| 3 | `AppStorage type error` | — | AppStorage.get() 类型推断错误 | 用 `@StorageLink` + `AppStorage.setAndLink`，避免 `setOrCreate` |
| 4 | `Object spread error` | — | 对象展开类型推断受限 | 显式声明类型 |
| 5 | `@StorageLink default value` | — | @StorageLink 属性缺少默认值 | 加 `= undefined` 或具体默认值 |
| 6 | `Object literal interface error` | 10605038 | 对象字面量缺少显式接口 | 先定义 interface 再使用 |
| 7 | `Function return type error` | 10605090 | 返回类型推断受限 | 添加显式返回类型注解 |
| 8 | `Arrow function conversion` | — | 用了 function 表达式 | 改为箭头函数 `=>` |
| 9 | `Color property error` | — | 使用了不存在的 Color 属性 | 用十六进制色值 |
| 10 | `Interface method signature` | — | 方法签名与对象字面量不匹配 | 用属性语法 `method: () => {}` |
| 11 | `AvoidArea type error` | — | AvoidArea 缺少 visible 属性 | 加 `visible: false` |
| 12 | `Standalone function this` | — | 独立函数中使用 `this` | 通过参数传递 context |
| 13 | `TitleButtonRect type error` | — | getTitleButtonRect 返回了 window.Rect | 用 `window.TitleButtonRect` |
| 14 | `Catch clause type` | — | catch 中有类型注解 | 移除类型注解或用 `unknown` |
| 15 | `ESObject type error` | — | 使用了 ESObject | 改用具体类型 |
| 16 | `Resource conversion` | — | Resource→string/number 转换错 | 在 UI 组件内直接使用 Resource |
| 17 | `Unused variable warning` | — | 声明了未使用的变量 | 删除或输出到 hilog |
| 18 | `IDataSource type error` | — | LazyForEach 需要 IDataSource | 实现 IDataSource 接口（4个方法） |
| 19 | `Duplicate @Entry` | — | 同一文件中有多个 @Entry | 去掉多余的 @Entry，子组件用 @Component |
| 20 | `Possibly null error` | — | 访问可能为 null 的对象的属性 | 用 `!== null` 检查或可选链 `?.` |
| 21 | `Cannot find module` | — | import 路径错误 | 检查模块路径和 export 名称 |
| 22 | `Getter or setter unexpected` | — | 属性定义使用了 get/set 关键字 | ArkTS 不支持 getter/setter |
| 23 | **`arkts-no-untyped-obj-literals`** | 10605038 | 对象字面量必须对应显式类或接口 | 定义 interface/class；或用空对象逐个赋值 `const p:Record<string,string>={}; p['k']='v';` |
| 24 | **`arkts-no-implicit-return-types`** | 10605090 | 函数返回类型推断受限 | 所有函数加显式返回类型注解 |
| 25 | **`arkts-no-any-unknown`** | 10605008 | 不能用 `any`/`unknown` | 全部替换为具体类型 |
| 26 | **`arkts-no-inferred-generic-params`** | 10605034 | 泛型函数调用需要显式类型参数 | 所有泛型调用显式标注 `<object>`：`api.get<object>()` |
| 27 | **`arkts-no-obj-literals-as-types`** | 10605040 | 不能用对象字面量声明类型 | 改为 interface 定义：`interface Param { username: string }` |
| 28 | **`Record<string, object> 类型不匹配`** | 10605999 | Record<string, object> 不能放基础类型值 | 定义具体接口代替通用的 Record |
| 29 | **`索引对象属性`** | — | 用变量键名索引对象 `colors[key]` | 声明为 `Record<string, T>` 或用 `switch/case` |
| 30 | **`for...in 循环`** | — | 使用 `for (let key in obj)` | 改用 `Object.keys(obj).forEach(key => {...})` |
| 31 | **`接口属性不匹配`** | — | 对象字面量包含接口不存在的属性 | 只赋值接口已定义的属性 |
| 32 | **`interface 在 struct 内`** | 10505001 | interface 声明在 struct 内部（ArkTS 禁止） | 移到文件级别（`@Entry` 之前） |
| 33 | **`Only UI component syntax`** | 10905209 | `const`/`let` 声明在 `build()` 组件树中 | 移到方法中计算或内联表达式 |
| 34 | **`Property on void`** | 10505001 | `@Builder` 方法链式 `.onClick()` | 用 `Column()` 包裹后再链式 |
| 35 | **`Property on TextAttribute`** | 10505001 | `Image` 属性迁移到 `Text` 后未改 | 用 `.fontColor()` 替代 `.fillColor()` |
| 36 | **`Unknown resource name`** | 10903329 | `ohos_ic_*` 系统资源不存在 | 用 `Text('🔔'/'↻')` 替代 |
| 37 | **`build() 多出/缺少'}'`** | — | 编码损坏导致 brace 不匹配 | 扫描全文件 brace 平衡 |
| 38 | **`Property 'onRefresh' does not exist. Did you mean 'onRefreshing'?`** | 10505001 | Refresh 组件回调名称写错 | `.onRefresh(` → `.onRefreshing(` |
| 39 | **`@State opacity 与基类冲突`** | 10505001 | `opacity` 是 CustomComponent 基类方法 | 改名为 `shimmerOpacity` / `alpha` |

---

## 🧬 级联错误诊断流程

当项目出现 50+ 编译报错时，大部分可能是级联错误。按以下顺序排查（优先级从高到低）。

> **⚡ 一键诊断**：运行诊断脚本自动扫描全部 7 项：
> ```bash
> bash <expert-dir>/scripts/diagnose_arkts.sh <项目根目录>
> ```
> 脚本在 `harmonyos-dev/scripts/diagnose_arkts.sh`，扫描结果按优先级排序输出。

### 第一步：检查 interface 是否在 struct 内
**错误现象**：`Declaration or statement expected` + `Cannot find name 'build'`
**排查命令**：
```bash
grep -n '^\s\+interface ' *.ets
```
**根因**：ArkTS 禁止在 `struct {}` 内部声明 `interface`，编译器看到 `interface` 关键字时解析失败，从该行开始直到文件末尾全部报错，可产生 400-600+ 级联错误。
**修复**：将 interface 移到文件级别（`@Entry` 之前），与 `RouteArgs` 同级。

### 第二步：检查缩进断裂
**错误现象**：`Declaration or statement expected` + 大量语法错误
**排查命令**：
```bash
awk 'NR>=18{indent=substr($0,1,1);if(indent~/^[a-zA-Z@]/) print NR": "$0}' *.ets
```
**根因**：编码损坏导致行首空格丢失，代码被解析为文件级代码而非 struct 成员。
**修复**：为每行恢复正确的缩进（struct 内至少 2 空格）。

### 第三步：检查 brace 平衡
**错误现象**：`Cannot find name 'width'` + struct 边界错误
**排查命令**：
```bash
o=$(grep -o '{' file.ets | wc -l); c=$(grep -o '}' file.ets | wc -l); echo $((o-c))
```
**根因**：±1 的差异可产生 100-400 个级联错误。
**修复**：在正确的层级补上缺失的 `}` 或删除多余的 `{`。

### 第四步：检查 `build()` 语法违规
**错误现象**：`Only UI component syntax can be written here`

**ArkTS `build()` 语法清单**：

| ✅ 允许 | ❌ 禁止 |
|---------|--------|
| UI 组件：`Column()` `Row()` `Text()` `Button()` 等 | `const`/`let`/`var` 变量声明 |
| 控制流：`if/else` `ForEach` `LazyForEach` | 函数调用赋值（`const x = compute()`） |
| `@Builder` 方法调用：`this.MyBuilder()` | `try/catch/finally` |
| 链式属性：`.width()` `.height()` `.onClick()` | 解构赋值（TS→ArkTS 迁移） |
| 条件表达式（三元） | `for`/`while` 循环 |
| 数据绑定：`{{ }}` `this.state` | `console.log`（用 `hilog` 替代） |

**常见违规修复**：
```typescript
// ❌ 错误 - const 在 build() 组件树中
build() {
  Column() {
    const x: number = this.compute();  // 10905209
    Text('' + x)
  }
}

// ✅ 正确 - 用方法计算
build() {
  Column() {
    Text('' + this.compute())
  }
}
```

### 第五步：检查 `@Builder` 链式调用
**错误现象**：`Property 'onClick' does not exist on type 'void'`

**根因**：`@Builder` 方法返回 `void`，不能在返回值上链式调用。
```typescript
// ❌ 错误
this.ChartTabItem().onClick(() => { ... })  // void 上没有 onClick

// ✅ 正确
Column() { this.ChartTabItem() }.onClick(() => { ... })
```

### 第六步：检查 `Text()` 参数类型
**错误现象**：`Argument of type '() => string' is not assignable to parameter of type 'string | Resource'`

**根因**：ArkTS `Text()` 构造函数接受 `string | Resource`，不接受箭头函数。
```typescript
// ❌ 错误
Text(() => { if (!x) return '--'; return x.toFixed(2); })

// ✅ 正确
Text(!x ? '--' : x.toFixed(2))
```

### 第七步：检查资源与属性兼容性

| 迁移场景 | ❌ 老属性 | ✅ 新属性 |
|---------|----------|----------|
| `Image` → `Text` | `.fillColor()` | `.fontColor()` |
| `Image` → `Text` | `.width(22) .height(22)` | 单字符无需显式尺寸 |
| 系统资源不存在 | `$r('sys.media.ohos_ic_xxx')` | `Text('🔔'/'↻'/'←')` 或本地资源 |
| `Record` 对象字面量 | `const x: Record<K,V> = { k: v }` | 改用 `Record<K,V> = {}; x['k'] = v` |

## 🔴 真实踩坑记录（持续更新）

### 来自 QuantFlow 项目的 20 个编译错误（2026-06-24）

**项目背景**：QuantFlow 是一个鸿蒙股票分析应用，大量代码由 AI 生成。首次编译时报出 20 个错误，全部集中在 TS→ArkTS 类型系统差异。

#### 错误分布
| 错误码 | 错误名 | 出现次数 | 涉及文件 |
|:------:|--------|:-------:|---------|
| 10605038 | `arkts-no-untyped-obj-literals` | 11次 | ProfilePage/LoginPage/RegisterPage/StockDetailPage |
| 10605090 | `arkts-no-implicit-return-types` | 6次 | StockDetailPage |
| 10605008 | `arkts-no-any-unknown` | 4次 | StockDetailPage |

#### 根因分析
1. **核心问题在 http.ets**：`api` 对象（第183行）没有明确的类型声明，导致所有调用方都报对象字面量错误
2. **泛型函数调用未显式指定类型参数**：`api.get()` 应写成 `api.get<object>()`
3. **内联对象作为参数类型**：`{ username: string; password: string }` 这种写法在 ArkTS 中禁止
4. **Record<string, object> 不能接受基础类型**：object 类型不能接收 string/number/boolean

#### 修复策略
1. 在 http.ets 中定义 `Api` interface 声明 api 对象类型
2. 定义 `LoginData`、`RegisterData`、`CommentData` 等数据接口
3. 所有泛型方法调用加 `<object>` 类型参数
4. 对象字面量改为：`const p: Record<string, string> = {}; p['key'] = 'val'` 逐个赋值

#### 教训总结（已纳入知识库）
- 定义 API 层时**必须先声明接口类型**，不能直接用对象字面量
- `httpClient.get()` 必须写成 `httpClient.get<object>()`
- `Record<string, object>` 不能存基础类型，必须用具体接口
- 每个函数**必须有显式返回类型注解**
- `any`/`unknown` 在 ArkTS 中完全禁止，全部替换为具体类型

### 来自 QuantFlow 的 AppStorage 导入坑（2026-06-24）

**问题**：在 `http.ts` 中 `AppStorage.get<string>('token')` 报错 `@kit.ArkUI` 没有导出 `AppStorage`。

**排查过程**：
1. ❌ 尝试从 `@kit.ArkUI` 导入 `AppStorageV2` → AppStorageV2 没有 `get` 方法
2. ❌ 尝试将 `http.ts` 重命名为 `http.ets` → 引发大量新类型错误（ArkTS 严格模式）
3. ✅ 最终方案：保持 `http.ts`，用全局变量替代 AppStorage，在登录页同步 token

**根因**：
- `.ets` 文件中 `AppStorage` 是**全局可用**的，无需 import
- `.ts` 文件中 `AppStorage` **不可用**（它是 ArkTS 编译器的内置全局对象）
- API 26+ 中从 `@kit.ArkUI` 导入 AppStorage 时，须使用 `AppStorageV2`

**正确实践**：
```typescript
// http.ts（普通 TypeScript 文件）
let cachedToken: string = '';
export function setToken(t: string) { cachedToken = t; }
export function getToken(): string { return cachedToken; }

// LoginPage.ets（ArkTS 文件，AppStorage 全局可用）
AppStorage.setOrCreate('token', '');
setToken(AppStorage.get<string>('token')!);
```

**教训**：.ts 和 .ets 的模块系统不同，.ts 不能访问 ArkTS 特有的全局对象。跨文件共享状态时，需要在 .ets 中获取后同步到 .ts

### 来自 QuantFlow 的编码损坏与组件坑（2026-06-24）

**问题**：153 个编译报错，根因是文件编码损坏 + 组件 API 使用错误。

#### 根因 1：文件编码损坏
- **表现**：中文注释/字符串变成乱码，导致字符串字面量未闭合 → 级联报错
- **修复**：检查文件编码是否 UTF-8；从版本控制系统恢复；重新编写严重受损文件
- **预防**：IDE 编码设为 UTF-8；避免在代码中使用可能被编码转换破坏的特殊字符

#### 根因 2：组件 API 误用
| 组件 | 错误用法 | 正确用法 |
|------|---------|---------|
| **Row** | `.alignItems(HorizontalAlign.Center)` | Row 用 `VerticalAlign`，Column 用 `HorizontalAlign` |
| **Toggle** | `.isOn(true)` 属性赋值 | `.selected(true)` 或 `onChange((v) => this.checked = v)` |
| **DataTransform** | 返回类型 `Object[]` | 必须用具体类型 `NewsStockRef[]` |

#### 经验
- 编码损坏是"伪报错"的常见来源：一个损坏的字符串未闭合会导致其后的 50 行全报错
- 遇到大量连续语法错误（>30个）时，优先检查文件编码而非逐条修复
- Row.alignItems 接受 `VerticalAlign`（Top/Center/Bottom）
- Column.alignItems 接受 `HorizontalAlign`（Start/Center/End）
- Toggle 的选中状态通过 `.selected()` 属性设置，非 `.isOn()`

### 来自 QuantFlow 的第三轮修复（659报错，2026-06-24）

**问题**：659 个编译错误，"全新"项目代码（非编码损坏），根因是 ArkTS 语法限制。

#### 新增 ArkTS 不支持的语法发现
| 语法 | 错误用法 | 正确替代 |
|------|---------|---------|
| **索引访问对象属性** | `colors[key]` 对普通对象做索引访问 | 改用 `Record<string, string>` 或 `switch/case` |
| **for...in 循环** | `for (let key in obj)` | 改用 `Object.keys(obj).forEach(key => {...})` |
| **接口中不存在的属性** | `MockData` 对象字面量包含 `amount` 属性 | 检查接口定义，只赋值已有属性 |

#### 根因分���
1. `ColorTheme.ets` 第65行：`colors[key]` — ArkTS 不支持通过变量键名索引访问对象属性，必须显式声明类型为 `Record<string, T>`
2. `StrategiesViewModel.ets` 第88行：`for (let key in obj)` — ArkTS 禁止 `for...in` 循环，这是因为它依赖动态运行时反射
3. `MockData.ets`：对象字面量赋值了接口不存在的属性 `amount` — ArkTS 严格检查对象字面量的属性完整性

#### 经验
- `for...in` 是 "从 TypeScript 迁移时 AI 最常生成的错误代码" 之一（与解构赋值 `{}`、`any` 并列前三）
- 对象索引访问的正确模式：`const colors: Record<string, string> = { 'red': '#ff0000' }; const c = colors['red'];`
- ArkTS 对象字面量必须精确匹配接口定义，不能多也不能少

### 来自 QuantFlow 的第四轮修复（801报错，2026-06-24）

**新发现**：
1. **`import` 语句位置错误导致装饰器截断**：`Index.ets` 中 `import` 放在了错误位置，导致其后的 `@Entry`/`@Component` 装饰器被截断——这是 "伪语法错误" 的另一个常见来源
2. **大文件中写中文→工具序列化失败**：`TradingPage.ets`（400+行）含大量中文字符串时，AI 的 `builtin_write_file` 工具 JSON 序列化会报错（`invalid escape character`）

**经验**：
- 当编译器报"装饰器不存在"或"表达式预期"时，先检查它上面的 `import` 语句是否完整、位置是否正确
- 多个 `import` 之间不能有空行或注释插入（某些 ArkTS 版本限制）
- 大宗文件含大量中文时，建议分块写入或先用英文占位再替换

### 来自 QuantFlow 的第五轮修复（14报错→0，2026-06-24）

**新发现**：
1. **`borderBottomWidth` 不是 Column 有效属性**：Column 组件没有 `borderBottomWidth` 属性，需用 `.border({ bottom: { width: 1 } })` 替代
2. **UI 组件树内不能声明变量**：在 `build()` 方法的组件树内部（如 `List() { ... }` 内）不能 `const x = ...`，必须用成员方法或提前计算
3. **空对象字面量 `{}` 也需要显式类型**：即使空对象 `response.result as (Record<string, Object>)` 也需要先声明显式类型

**经验**：
- Column/Row/Stack 等容器组件不支持单个方向的边框属性（`borderBottomWidth`/`borderTopColor` 等），统一用 `border()` 方法
- `build()` 方法中所有变量声明必须放在 `@Builder` 或 `build()` 最外层，不能在嵌套 UI 组件内部声明

### 来自 QuantFlow 的第六轮修复（468报错→编码问题，2026-06-24）

**新发现**：
1. **`export` 修饰符缺失**：页面组件（QuotesPage/StrategiesPage/BacktestPage/ProfilePage）的 `@Component struct` 前缺少 `export`，导致无法被其他模块 import
2. **回环编码损坏**：同一批文件反复出现未闭合中文字符串——说明编码损坏可能是**自动格式化工具**或**跨平台编辑器**导致的反复问题

**经验**：
- ArkTS 中组件默认是 `internal`（模块内可见），需要被其他模块引用时须加 `export`
- 对于 Navigation + NavDestination 架构，所有页面组件必须 `export struct`
- 反复出现的编码损坏往往是 IDE 编码配置问题（如 UTF-8 vs GBK），建议统一设为 UTF-8 NO BOM
- `response.result as any` 无法解决问题，必须转换为 `response.result as Record<string, Object>`

### 社区精华：51CTO开发者12个坑总结（2026-06-14）

| 坑 | 错误表现 | 根因 | 修复 |
|----|---------|------|------|
| **Column+Row 尺寸失控** | TextField 撑不满父容器 | Row 默认 flexStart 不拉伸子元素 | 显式设 width：`.width('60%')` |
| **Button 点击被拦截** | onClick 不触发 | GestureDetector 优先级更高 | 别在 Button 上叠 GestureDetector |
| **TextField 失去焦点** | focus() 无效 | 手动设了 `focusable(false)` | 默认就是 true，不要乱改 |
| **Image + Text 渲染错乱** | 图片显示在文字后面 | Image 没设 width/height | 所有非文本组件必须显式设尺寸 |
| **@Prop 修改不触发刷新** | 改了 user.name 视图不动 | @Prop 是值副本，非引用 | 用 @Link 或事件回调 |

### 社区精华：鸿蒙PC开发3个关键教训
1. **ForEach 必须提供唯一键**（第三个参数）：`ForEach(arr, item => {}, item => item.id)`，否则更新异常
2. **组件销毁前释放资源**：`aboutToDisappear()` 中必须释放图片缓存、传感器、事件监听器
3. **慎用百分比宽度**：Column 中百分比宽度需显式 `width('100%')`，不是默认行为

### 经验教训：批量替换的正确姿势（2026-06-24）

**事件**：用 `sed` + Python 批量替换 pet_review_harmony 项目中 23 个文件的 `router.pushUrl` → `getUIContext().getRouter().pushUrl`，导致：
- ❌ sed 删 `import { router }` 时误删了第 1 行，后续代码没有被影响——这个没问题
- ❌ sed 删 `, router.RouterMode.Standard)` 时多删了 pushUrl 的闭括号 `)`，导致 30 个文件出现 `pushUrl({ url: '...' };`
- ❌ Python 修复时正则 `r"pushUrl\(\{ url: '([^']+)' \}"` 过于贪婪，又加了一个多余的 `}` → `pushUrl({ url: '...' }});`
- ❌ 两次修复把文件从 2 个 ERROR 弄到 689 个 ERROR

**教训**：
1. **永远不要用 sed/Python 批量替换有嵌套括号的代码**——正则无法正确处理嵌套括号结构
2. **正确的做法**：用 `git grep -n 'pattern' | wc -l` 统计每个变体，逐一确认差异，一个一个文件改
3. **或者**：在 IDE 中全局搜索，肉眼审查每个匹配项后再替换
4. 如果不得不批量改：先改一个文件编译通过，确认改法正确，再批量执行
5. 始终在版本控制下操作（git commit 后再改，出事直接 reset）

---

## 📝 实战经验库（持续积累）

> 此章节由专家在每次对话结束后自动追加。记录了所有实战中踩过的坑、学到的经验。

<!-- 新的经验教训自动追加在此下方 -->

### 2026-06-29 - 持续学习：DevEco Code/CLI + V2 装饰器 + 生产级模式

- **场景**：学习 HDC 2026 新工具和 HarmonyOS 7 生产级模式
- **来源**：51CTO 文章、jishuzhan.net 文章、GitHub arkts-patterns v2.3.1、Gitee harmonyos_samples
- **新增内容**：
  1. 🤖 **DevEco Code & DevEco CLI 章节**：AI Agent 工具安装/配置/三种模式(Build/Plan/Goal)/内置6大工具/模型配置(支持DeepSeek等第三方)
  2. 🏗️ **ArkTS V2 状态管理装饰器**：10 个 V2 装饰器完整表格(@ObservedV2/@Track/@ComponentV2/@Local/@Param/@Event/@Monitor/@Computed/@Provider/@Consumer/@LocalStorage)，V1 vs V2 对比，典型使用代码
  3. 🚀 **TaskPool 生产级并发模式**：基本模式+长时任务+进度回调，TaskPool vs Worker 选择指南
  4. 📚 **官方 Sample 推荐**：HMOSLiveStream/AVPlayerLongVideo/AudioFocus/MultiTabNavigation/CustomDialogGathers/ArkTS Patterns
- **效果**：专家文件从 3022 行扩展至 3300+ 行

### 2026-06-29 - API 版本检测更新：HarmonyOS 7 (API 26) 新能力全面梳理

- **场景**：每周一 API 版本自动检查 + 主动完善知识库
- **发现**：2026-06-21 华为官网发布了 HarmonyOS 7 (API 26) 新能力一览
- **对比**：专家文件原有仅提及 Vibe Coding、沉浸光感、3DGS、空间音频、星盾风控 5 项；新增覆盖 17 项能力的详细表格（智能化 Agent/视觉AI、全场景碰一碰分享、多窗互动卡片/闪控窗、安全 DID/数字盾、性能/通讯/低功耗等）
- **行动**：更新了 API 演进核心里程碑描述、新增「🚀 HarmonyOS 7 (API 26) 新能力详解」章节、新增「⚠️ @Prop/@State 属性名基类冲突检测清单」

### 2026-06-29 - 深入学习华为官方 Sample 代码（第二轮）

- **场景**：从开发者官网示例页面 + Gitee harmonyos_samples 组织学习生产级 ArkTS 代码
- **来源**：华为开发者官网 Samples 页面（developer.huawei.com/consumer/cn/samples/）、Gitee harmonyos_samples（425+ 仓库）、BestPracticeSnippets（56⭐）
- **发现**：官方 SPA 页面展示了 **10 个首发 Sample**（企业威胁防护/媒体直播/自由流转协同/全链路盯盘/多设备长视频/多设备音乐/沉浸光感/多设备短视频/多设备社区评论/互动卡片），均为 2026-06-11~23 发布
- **行动**：
  1. 完整扩充「📚 官方 Sample 推荐」章节：从 6 条扩充至 **30+ 条**，覆盖应用级 Sample（12 个）+ 最佳实践片段（22 个分类）+ 第三方模式库
  2. 新增 BestPracticeSnippets 分类表格：性能/安全/UI/并发/网络/媒体/架构 7 大类 22 个片段
  3. 添加 Star 数作为优先级指标
- **价值**：开发者可直接根据分类导航到对应 Sample 工程，快速找到解决特定问题的参考代码

### 2026-06-25 - 华为官方 MultiVideoApplication 5 大生产级模式

- **场景**：学习华为官方多设备长视频应用 Sample（MultiVideoApplication-master），提取可复用的生产级 ArkTS 模式
- **来源**：华为开发者官网官方 Sample，`D:/HUAWEI/开发资料/MultiVideoApplication-master/`

#### 模式 1：BreakpointType<T> 泛型断点配置
```typescript
// 根据当前断点返回不同配置值，消除大量 if-else
class BreakpointType<T> {
  constructor(xs: T, sm: T, md: T, lg: T, xl: T) { ... }
  getValue(breakpoint: WidthBreakpoint): T { ... }
}
// 用法：new BreakpointType(1, 2, 3, 4, 6).getValue(currentBp)
```
- **价值**：任何需要按断点变化的参数（列数、间距、字号）都可用此模式，一行代码替代 5 级 if-else。适用于 Grid columnsTemplate、List lanes、margin/padding 断点适配。

#### 模式 2：SessionID 防竞态（异步状态管理）
- **场景**：用户快速切换视频时，旧的 `createAvPlayer()` 异步操作完成但状态已过期
- **方案**：全局递增 `sessionId`；异步操作开始前记录 sessionId，每个关键步骤检查 `isSessionActive(sessionId)`
- **核心代码**：`bumpSession()` 递增 + `if (!this.isSessionActive(sessionId)) return;` 守卫
- **价值**：无需引入锁/信号量，两步实现异步竞态防护。适用于网络请求、文件读写、动画序列等异步操作

#### 模式 3：WindowUtil + WindowInfo 完整窗口管理
- **封装范围**：沉浸式类型枚举（NORMAL/IMMERSIVE/FULLSCREEN_IMMERSIVE）、avoidArea 全类型追踪、断点实时监听、屏幕旋转、分屏、窗口大小限制
- **关键设计**：`WindowInfo` 使用 `@Observed` 装饰，通过 `@StorageLink` 在组件间共享，窗口变化自动刷新 UI
- **价值**：对我专家文件中窗口API的全面升级——从零散 API 到生产级封装

#### 模式 4：InputSecurityUtil 输入安全
- **实现**：正则清除控制字符（`\u0000-\u001F\u007F`）+ 长度截断（MAX_INPUT_LENGTH=50）
- **价值**：官方安全最佳实践，适用于搜索框、评论输入、表单等所有外部输入场景

#### 模式 5：canIUse 系统能力检测 + foldStatusChange 折叠屏适配
- **`canIUse('SystemCapability.Window.SessionManager')`** — 运行时判断折叠屏能力是否可用，PC/大屏设备优雅降级
- **`display.on('foldStatusChange', ...)`** — 监听折叠状态变化（展开/折叠/半折叠），联动全屏切换和布局重排
- **价值**：折叠屏适配的官方推荐范式

### 2026-06-25 - 华为官方 application-track UIObserver 埋点框架

- **场景**：学习华为官方 UIObserver 应用埋点 Sample，提取 ArkTS 生产级埋点模式
- **来源**：GitCode `HarmonyOS_Samples/application-track`

#### 核心发现（6 个新模式）
1. **`uiContext.getUIObserver().on('willClick', cb)`** — 全局点击监听，无需在每个组件上绑 onClick 埋点。结合 `node.getCustomProperty()` 可获取组件自定义业务数据
2. **`node.getCustomProperty(key)` + `.customProperty(key, value)`** — 为组件附加业务数据（埋点上下文），埋点框架通过 `node.getId()` 关联获取
3. **`onDidBuild()` 生命周期 + `this.getUIContext().getFrameNodeByUniqueId(uid)`** — 构建后立即获取当前组件的 FrameNode，注册可见区域监听
4. **`setOnVisibleAreaApproximateChange({ ratios, expectedUpdateInterval }, callback)`** — 组件曝光埋点的核心 API，按比例（0/0.5/1）和最小间隔回调可见区域变化
5. **`TrackNode` @BuilderParam 包装组件** — 用泛型包装器包裹任意子组件，自动注入埋点逻辑，实现非侵入式埋点
6. **`hiAppEvent.addWatcher({ name, appEventFilters, triggerCondition, onTrigger })`** — 事件消费端，可批量拉取埋点数据（按行数/大小/超时触发）

#### 价值
- 这套框架是 ArkTS 埋点 SDK 的最小实现，可直接在 pet-review 或任何鸿蒙项目中复用
- 不同于传统手动 `onClick` 埋点，UIObserver 模式做到 **一次注册、全局生效**，业务代码零侵入
- `TrackNode` 的 @BuilderParam 模式是 ArkTS 中 **高阶组件** 的标准实现方式

<!-- AI 生成总结，未经验证 -->


### 2026-06-24 - QuantFlow 677 个编译错误的根因分析
- **场景**：修复 QuantFlow（鸿蒙交易应用）累计 677 个编译错误至仅剩 3 个
- **发现 1**：`interface MACDResult` 和 `interface KDJResult` 声明在 `struct StockDetailPage {}` 内部，ArkTS 禁止 interface 作为 struct 成员 → 400+ 级联报错
- **发现 2**：编码损坏导致 4 处行首空格丢失（L107/109/239/385），声明被当作文件级代码 → 200+ 级联报错
- **发现 3**：`@Builder` 方法返回 `void`，`this.ChartTabItem().onClick(...)` 无效，需用 `Column() { this.ChartTabItem() }.onClick(...)` 包裹
- **发现 4**：`build()` 组件树内不能出现 `const`/`let` 声明（error 10905209），需提到方法中计算或内联
- **发现 5**：`Text()` 构造函数不接受箭头函数 `() => string`，需改为三元表达式
- **发现 6**：对象字面量 `{ k: v }` 即使有 `Record<K,V>` 注解也不够，需用 `Record<K,V> = {}; x['k'] = v`
- **根因**：AI 生成代码时将 ArkTS 当 TypeScript 写，大量 TS 语法不被 ArkTS 支持
- **修复路径**：interface 移出 struct → 恢复缩进 → brace 平衡 → 修复 build() 违规 → 修复 @Builder 链式 → 修复 Text 参数 → 修复对象字面量

### 2026-06-24 - Image → Text 迁移的 API 差异
- **场景**：替换无效系统资源 `ohos_ic_public_notification/ring/reset` 为 `Text('🔔'/'↻')`
- **发现**：Image 使用 `.fillColor()` 设色调，Text 没有此属性，应使用 `.fontColor()`
- **修复**：`Image($r('sys.media.*')).fillColor(c)` → `Text('🔔').fontColor(c)`

### 2026-06-25 - Refresh 组件回调名称错误 + opacity @State 冲突

- **场景**：pet-review 鸿蒙版 P3 下拉刷新实现后，出现 7 处 `onRefresh` + 1 处 `opacity` 共 8 个编译错误
- **发现 1**：`Refresh` 组件的下拉回调是 `.onRefreshing()`，不是 `.onRefresh()`。编译器提示 `Did you mean 'onRefreshing'?`
- **发现 2**：`SkeletonCard` 中 `@State opacity: number` 与基类 `CustomComponent` 的 `.opacity()` 链式方法冲突（与 width/height 同类问题），重命名为 `shimmerOpacity` 解决
- **根因**：ArkTS Refresh 组件 API 命名与 Web/Android 习惯不同；`opacity` 与 `width/height/borderRadius` 同属基类冲突属性
- **修复**：`.onRefresh(` → `.onRefreshing(`（5 页 7 处 replace_all）；`opacity` → `shimmerOpacity`（@State + animateTo 引用同步更新）
- **来源**：实测验证

### 2026-06-24 - pet-review 编码修复全记录（6个核心教训）

#### 教训 1：正则批量替换 .ets 文件是灾难
- **场景**：22 个 .ets 文件中文字符串被 sed/Python 编码损坏，尝试用 Python 正则 `r\"'[^']*\\?[^']*'\"` 清除乱码
- **结果**：所有含 `?` 的正常字符串（三元表达式、模板字符串）被替换为空 `''`，错误数从 ~30 暴增到 1398
- **根因**：正则无法区分编码损坏产生的 `?` 和合法代码中的 `?`
- **修复**：放弃正则修复，用 Write 工具逐个重写 15 个严重受损文件
- **经验**：**永远不要用正则批量修复编码损坏的 .ets 文件**，正确做法是用 Write 工具重写（保证 UTF-8 纯净）

#### 教训 2：build() / @Builder 体内禁止变量声明和 if 语句
- **场景**：FavoritesPage 行 222 `const detail = item.detail` 报错 10905209；Index 行 212 `if (route) {}` 报错 "Statement or declaration expected"
- **根因**：ArkTS 的 build() 和 @Builder 方法体 UI 区域只能放组件语法
- **修复**：抽到独立方法中（`goToDetail()` / `navigateTo()`），在 onClick 中调用
- **记忆口诀**：build() 内只能写 `Column(){}` `Row(){}` `Text()` 和 `.onClick(() => { this.xxx() })`，不能写 `const`/`let`/`if`/`for`

#### 教训 3：Review 类型字段名 ≠ Web 版字段名
- **场景**：HospitalDetailPage/ProductDetailPage/DoctorDetailPage 中写 `review.username`、`review.rating`
- **根因**：Web 版 API 返回扁平化字段 `username`/`rating`，ArkTS 版 Review 接口是嵌套 `review.user.username` 和 `review.score`
- **修复**：`review.username` → `review.user ? review.user.username : '匿名用户'`，`review.rating` → `review.score`
- **经验**：**重写鸿蒙版时，必须先确认 types.ts 中接口定义，不能凭 Web 版记忆写字段名**

#### 教训 4：@Prop 属性名不能与 CustomComponent 基类方法冲突
- **场景**：PlaceholderImage 组件中声明 `@Prop width: string` / `@Prop height: number` / `@Prop borderRadius: number`
- **报错**：10505001 — Property 'width' is not assignable (type 'string' vs chainable method)
- **根因**：`@Component struct` 继承自 CustomComponent，基类已有 `.width()` `.height()` `.borderRadius()` 方法
- **修复**：重命名为 `imageWidth` / `imageHeight` / `imageRadius`
- **冲突清单**（11 项）：width, height, borderRadius, backgroundColor, padding, margin, fontSize, fontColor, opacity, layoutWeight, id, key, onClick, onTouch → 全部需要加前缀避免冲突

#### 教训 5：AppStorage 在 .ts 文件中不可用
- **场景**：http.ts 中 `import { AppStorage } from '@kit.ArkUI'` 报错 "has no exported member named 'AppStorage'"
- **根因**：API 26+ 从 @kit.ArkUI 导入需用 `AppStorageV2`；且 .ts 文件本身不能访问 ArkTS 全局对象
- **修复**：移除 import，用普通变量 `cachedToken` 替代，在 .ets 文件中同步 token 值
- **经验**：.ts 文件 ≠ .ets 文件，AppStorage 是 ArkTS 编译器内置全局对象，.ts 文件无此运行时

#### 教训 6：共享组件是最优的代码重复消除手段
- **场景**：20 个页面都重复写相同结构的 Header 栏（返回按钮 + 居中标题）
- **成果**：抽成 `NavHeader({ title: string })` 组件，17 个页面替换，消除 ~187 行重复代码
- **经验**：鸿蒙 ArkUI 的 `@Component + @Prop` 组合非常适合创建共享 UI 组件，比 Vue 的 slot/插槽更直接

### 2026-06-29 - Deep Dive：Gitee harmonyos_samples 全量扫描（第三轮）

- **场景**：用户提示"还有很多可学习的内容"，逐页扫描 Gitee harmonyos_samples 前 5 页
- **发现**：补充了此前未覆盖的 **20+ 个高价值 Sample**
- **新增的关键 Sample**：
  - **HMRouter**（53⭐）：鸿蒙路由库，声明式路由+拦截器
  - **UserAuth**（24⭐）：人脸/指纹认证+密码保险箱+防截屏
  - **Watermark**（28⭐）：页面水印/拍照水印/图片水印
  - **ShareKit**（38⭐）：分享数据与应用内文件分享
  - **WindowPiP**（17⭐）：画中画视频播放
  - **AudioInteraction**（22⭐）：后台播放+播控中心+焦点策略
  - **Aspect**：基于 libabcKit 字节码的 AOP 切面编程
  - **SmoothSwitchShortVideos**（8⭐）：LazyForEach+复用的短视频性能优化
  - **MultiDeviceInteraction**（3⭐）：触控/鼠标/键盘统一交互
- **新增「一多」系列子表**：7 个多设备行业 Sample（ConvenientLife/NavBar/Columns/NewsRead/TicketClass/ShortVideo/MobilePayment）
- **效果**：专家文件继续扩展，总量达 3326+ 行

### 2026-06-29 - 源码级学习：异常处理 + HMRouter + AOP（第四轮）

- **场景**：用户要求"细细看下"，从目录索引转为源码级分析
- **exception-handling**：2,829 下载量。学习了完整的数据流：hiAppEvent.addWatcher → AppStorage → @StorageLink @Watch → 懒加载数据源 → LazyForEach 渲染。含 APP_CRASH / APP_FREEZE 两类异常捕获
- **HMRouter**（53⭐）：学习了注解声明路由(@HMRouter)、全局/单页/一次性拦截器、生命周期回调、转场动画、服务路由。提取了完整的项目目录结构范式
- **util.Aspect**：学习了鸿蒙内置 AOP 三件套 addBefore/addAfter/replace 的使用方式和代码示例。整理出 6 个典型应用场景
- **新增 3 个源码级章节**：「🛡️ 应用异常处理（hiAppEvent）」、「🧭 HMRouter 路由框架」、「🧵 AOP 切面编程（util.Aspect）」
- **文件规模**：3343 → 3600+ 行

### 2026-06-29 - MultiCommunityApplication 源码级学习（第五轮）

- **场景**：用户截图展示 GitCode 上的 MultiCommunityApplication 项目（3,700下载），检查是否有相关知识
- **原有**：多设备适配章节仅有基础断点和原则说明，缺少完整实战代码
- **新增「🏗️ 多设备开发实战场」完整章节**，含 6 个实战模式：
  1. **Navigation pageMap 路由分发**：@StorageLink('pageInfos') 跨组件路由
  2. **Tabs 响应式导航**：断点驱动的水平↔垂直自动切换
  3. **WaterFlow 断点列数**：手机单列→平板双列
  4. **折叠屏双栏布局**：GridRow + SideBarContainer 按断点切换
  5. **视差滚动头部**：onScrollFrameBegin 动态 margin 的视差效果
  6. **窗口断点实时计算**：EntryAbility 监听 windowSizeChange

### 2026-06-29 - AlwaysOnMarketWatch 全链路盯盘源码级学习（第六轮）

- **场景**：用户再次截图展示 AlwaysOnMarketWatch 项目，检查是否已有相关知识
- **原有**：仅在 API 26 新能力表格中有一行"闪控窗"描述，完全无任何实现代码
- **新增「💹 全链路盯盘实战」完整章节**，覆盖 5 大系统能力：
  1. **闪控球（FloatingBall）**：@ohos.floatingball API 创建/启动
  2. **悬浮窗（FloatView）**：@ohos.floatview 创建/绑定/双指手势切换形态
  3. **锁屏卡片（Form Kit）**：form_config.json 配置 + 锁屏卡片 UI 实现
  4. **待机屏保卡片（Form Kit）**：standby 字段配置 + 2×2 尺寸限制
  5. **防窥保护（dlpAntiPeep）**：@ohos.security.dlpAntiPeep 注册监听+蒙层显示
- **含**：目录结构范式、权限申请、完整代码示例

### 2026-06-29 - MusicHome 多设备音乐源码级学习（第七轮）

- **场景**：用户截图展示 MusicHome 项目（4,080下载），检查已有知识
- **原有**：已有多设备基础适配章节，但缺少 displayPriority、三层架构实践、effectKit 取色等模式
- **新增「🎵 MusicHome 多设备音乐实战场」章节**，含 4 个实战模式：
  1. **displayPriority 自适应显隐**：系统级优先级隐藏，替代 if/else
  2. **List.lanes 断点多列**：平板双列，手机单列
  3. **effectKit 专辑封面取色**：createColorPicker 提取主色调 + createEffect 高斯模糊
  4. **Swiper 播放页**：手机端左右滑动切换封面/歌词
- **同步更新**：多设备开发实战场章节标题加入 MusicHome 引用

### 2026-06-29 - LiveCard 互动卡片源码级学习（第八轮）

- **场景**：用户要求学习"互动卡片"示例
- **来源**：官方 Sample `LiveCard`（2,194下载）+ 51CTO + CSDN 技术文章
- **原有**：仅 Sample 推荐表有一行"互动卡片"描述，完全无实现代码
- **新增「🃏 互动卡片 LiveCard」完整章节**，含：
  1. **form_config.json 配置**：name/src/isDynamic/defaultDimension/sceneAnimationParams 核心字段详解 + 配置清单
  2. **LiveFormExtensionAbility**：onLiveFormCreate → LocalStorage → session.loadContent 完整数据流
  3. **帧动画系统**：setInterval 逐帧切换封面
  4. **卡片通信**：postCardAction(action/message/router) → callee 接收 → formProvider.updateForm 反向更新
  5. **4 种卡片类型**：音乐播控/快递陀螺仪/运动进度/睡眠监测
  6. **module.json5 注册 liveForm 类型 + 排查清单 6 项

### 2026-06-29 - 批量深度学习：直播/自由流转/短購/支付（第九轮）

- **场景**：用户要求逐一深度学习页面中所有 Sample
- **新增**：
  1. **📡 分布式自由流转**：应用接续 onContinue + distributedDataObject + Asset 文件流转的完整代码
  2. **📹 HMOSLiveStream**：直播全链路（OHAudio 采集/SDR+HDR/V编码/AVPlayer 播放/ROI/压力反馈）
  3. **🎬 MultiShortVideo**：Swiper 纵向轮播 + 三层架构
  4. **🛍️ 购物比价**：GridRow 断点列数 + 筛选网格
  5. **💳 移动支付**：Scan Kit 扫码 + 码图生成 + 多设备适配
- **未找到**：修图软件波轮菜单具体项目名（需要更完整的截图或项目名）

### 2026-06-29 - ImageEditWithWavewheel 修图波轮菜单（第十轮）

- **场景**：用户再次截图提供项目名 `ImageEditWithWavewheel`（2,256下载），补齐最后缺口
- **新增「🌀 ImageEditWithWavewheel 修图波轮菜单」章节**，完整覆盖：
  1. Pen Kit 手写笔事件（stylusInteraction: squeeze/doubleTap）代码
  2. 屏幕取色器（imageFeaturePicker.pickForResult）
  3. SubWindow 悬浮波轮菜单（createSubWindow + 扇形四象限自适应算法）
  4. 手势互斥（GestureMode.Exclusive）
  5. 回调引用管理（必须保存成员变量，否则 off() 失效）
- **至此**：用户截图中的所有页面 Sample 全部完成深度学习

---

# 第十二部分：拓展资源（官方Sample、语言基础类库、路由框架）

## 🌐 网络通信与数据持久化 API 模板

### 1. 网络请求（@ohos.net.http）

```typescript
import http from '@ohos.net.http';

// 创建请求实例（建议在组件生命周期内管理）
const httpRequest: http.HttpRequest = http.createHttp();

// ✅ GET 请求
async function getRequest(url: string): Promise<object> {
  const response = await httpRequest.request(url, {
    method: http.RequestMethod.GET,
    header: { 'Content-Type': 'application/json' },
    expectDataType: http.HttpDataType.OBJECT,
    usingCache: true,
  });
  if (response.responseCode === http.ResponseCode.OK) {
    return response.result as object;
  }
  throw new Error(`HTTP ${response.responseCode}`);
}

// ✅ POST 请求
async function postRequest(url: string, data: object): Promise<object> {
  const response = await httpRequest.request(url, {
    method: http.RequestMethod.POST,
    header: { 'Content-Type': 'application/json' },
    extraData: JSON.stringify(data),
    expectDataType: http.HttpDataType.OBJECT,
  });
  return response.result as object;
}

// ✅ 全局请求头设置
httpRequest.setExtraHeaders({
  'User-Agent': 'HarmonyOS-App/1.0',
  'Accept-Language': 'zh-CN,zh;q=0.9',
});

// ⚠️ 组件销毁时释放资源
onDetach(() => { httpRequest.destroy(); });
```

### 2. WebSocket 实时通信（@ohos.net.webSocket）

```typescript
import webSocket from '@ohos.net.webSocket';

const ws = webSocket.createWebSocket();
ws.connect('wss://server.com/ws', (err) => {
  if (!err) { ws.send('Hello'); }
});
ws.on('message', (err, data) => { /* 处理消息 */ });
ws.on('error', (err) => { /* 错误处理 */ });
ws.close(() => { ws.destroy(); });
```

### 3. 数据持久化方案选择

| 方案 | 适用场景 | 特点 |
|------|---------|------|
| **Preferences** | 用户偏好设置、主题配置、简单键值对 | 轻量级 Key-Value，1MB 以内数据，XML/GSKV 两种存储模式 |
| **RDB（关系型数据库）** | 复杂结构化数据、多表关联查询 | 完整 SQL 支持、ACID 事务、支持索引和迁移 |
| **KVStore（分布式）** | 跨设备数据实时同步 | 自动同步、PUSH/PULL/PUSH_PULL 模式、支持离线缓存 |

#### Preferences 示例（轻量级键值存储）
```typescript
import { preferences } from '@kit.ArkData';

// 获取实例
const dataPref = preferences.getPreferencesSync(context, { name: 'myStore' });

// 写入
dataPref.putSync('isDarkMode', true);
dataPref.flush(); // 持久化到文件

// 读取
const darkMode = dataPref.getSync('isDarkMode', false);

// 订阅变更
dataPref.on('change', (key) => { console.info(`Key ${key} changed`); });
```

#### RDB 示例（关系型数据库）
```typescript
import { relationalStore } from '@kit.ArkData';

const config: relationalStore.StoreConfig = {
  name: 'app.db', securityLevel: relationalStore.SecurityLevel.S1,
};
const rdb = await relationalStore.getRdbStore(context, config);

// 建表
await rdb.executeSql(`CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER
)`);

// 插入
await rdb.insert('users', { name: 'Alice', age: 25 });

// 查询
const predicates = new relationalStore.RdbPredicates('users');
predicates.greaterThanOrEqualTo('age', 18).orderByAsc('name');
const resultSet = await rdb.query(predicates, ['id', 'name', 'age']);
```

#### KVStore 示例（分布式键值存储）
```typescript
import { distributedData } from '@kit.ArkData';

const kvManager = distributedData.createKVManager({
  bundleName: 'com.example.app',
  userInfo: { userId: 'default', userType: distributedData.UserType.SAME_USER_ID },
});
const kvStore = await kvManager.getKVStore('store', {
  createIfMissing: true, autoSync: true,
  kvStoreType: distributedData.KVStoreType.DEVICE_COLLABORATION,
});
await kvStore.put('key', 'value');
const val = await kvStore.get('key');
```

---

## 📦 资源管理

### resources 目录结构
```
resources/
├── base/                          # 默认资源（必选）
│   ├── element/                   # 基础元素资源
│   │   ├── color.json             { "color": [{"name":"bg","value":"#FFFFFF"}] }
│   │   ├── float.json             { "float": [{"name":"margin","value":"16vp"}] }
│   │   ├── string.json            { "string": [{"name":"hello","value":"你好"}] }
│   │   ├── plural.json            { "plural": [{"name":"count","value":[{..}]}] }
│   │   ├── boolean.json           { "boolean": [{"name":"enable","value":true}] }
│   │   └── integer.json           { "integer": [{"name":"maxAge","value":100}] }
│   ├── media/                     # 图片/音频等媒体文件
│   └── profile/                   # 配置类文件（如技能卡片配置）
├── en_US/                         # 英文语言限定（可不带 base 重复）
│   └── element/string.json
├── zh_CN/                         # 中文
├── ja_JP/                         # 日文
└── rawfile/                       # 原始文件（不编译，直接读取）
    └── icon.png
```

### 限定词组合规则
`语言_文字_国家-地区_横竖屏_设备类型_颜色模式_屏幕密度`

常用组合：
| 限定词 | 示例 | 作用 |
|--------|------|------|
| 语言 | `en_US` / `zh_CN` | 多语言 |
| 横竖屏 | `landscape` / `portrait` | 横竖屏布局 |
| 屏幕密度 | `ldpi` / `mdpi` / `hdpi` / `xhdpi` | 不同分辨率适配 |
| 颜色模式 | `dark` | 深色模式 |

### 资源引用方式
```typescript
// ✅ 标准引用（编译检查，推荐）
Text($r('app.string.hello'))
Image($r('app.media.icon'))
// 带参数
Text($r('app.string.template', 'world'))  // 对应 "hello %s"

// ✅ rawfile 引用（不编译，直接复制）
Image($rawfile('icon.png'))

// ✅ 系统资源引用
Text($r('sys.string.ok'))  // 使用系统内置字符串

// ✅ 代码中访问资源
const str = this.context.resourceManager.getStringSync('app.string.hello');
```

---

## 🧰 自定义组件与扩展

### @Builder 自定义构建函数
```typescript
// 复用 UI 片段
@Builder Header(title: string) {
  Row() {
    Text(title).fontSize(20).fontWeight(FontWeight.Bold)
    Blank()
    Button('更多').fontSize(14)
  }.padding(16)
}

// 使用
@Component
struct MyPage {
  build() {
    Column() {
      this.Header('个人中心')
      this.Header('设置')
    }
  }
}
```

### @Extend 扩展组件方法
```typescript
// 为 ArkUI 内置组件添加全局方法
@Extend(Text) function primaryTitle() {
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#1A1A1A')
}

@Extend(Button) function roundedStyle(radius: number = 12) {
  .width('100%')
  .height(48)
  .borderRadius(radius)
  .backgroundColor('#007AFF')
}

// 使用
Text('标题').primaryTitle()
Button('确定').roundedStyle(16)
```

### @Styles 全局样式函数
```typescript
// 通用样式函数（可应用于任意组件）
@Styles function cardShadow() {
  .width('100%')
  .padding(16)
  .borderRadius(12)
  .backgroundColor('#FFFFFF')
  .shadow({ radius: 8, color: '#1A000000' })
}

// 使用
Column() { Text('卡片内容') }.cardShadow()
Row() { /* ... */ }.cardShadow()
```

### @CustomModifier 自定义修饰器
```typescript
// 高级用法：自定义绘制/动效修饰
class MyModifier implements CustomModifier {
  draw(context: DrawContext) {
    context.canvas.drawCircle({ x: 50, y: 50, radius: 30 });
  }
}
@Component
struct MyComp {
  modifier: MyModifier = new MyModifier();
  build() {
    Column() { }.attributeModifier(this.modifier)
  }
}
```

---

## 📚 官方 Sample 推荐（Gitee: harmonyos_samples）

> 华为官方维护的 **425+ Sample 示例仓库**，每个均为独立 DevEco Studio 工程项目，覆盖媒体/安全/UI/多设备/分布式等全场景。

### 🌟 应用级 Sample（完整工程，直接编译运行）

| Sample 名称 | Star | 核心能力 | 参考价值 |
|:-----------:|:----:|:---------|:--------:|
| **HMOSLiveStream** | 22⭐ | [gitee](https://gitee.com/harmonyos_samples/HMOS_LiveStream) 媒体直播开播端+看播端：音视频采集/播放/推流/拉流、ROI、背景音乐、前后摄翻转 | 直播全流程 |
| **AVPlayerLongVideo** | 3⭐ | [gitee](https://gitee.com/harmonyos_samples/avplayer-long-video) 长视频：播控、精准跳转、倍速、音量/亮度控制、焦点管理、弹幕、字幕、画中画 | 视频播放全场景 |
| **MultiTabNavigation** | **149⭐** | [gitee](https://gitee.com/harmonyos_samples/multi-tab-navigation) 底部/顶部/侧边 Tab 导航 | 多Tab页架构 |
| **CustomDialogGathers** | **64⭐** | [gitee](https://gitee.com/harmonyos_samples/custom-dialog-gathers) CustomDialog + bindContentCover + bindSheet | 弹窗/模态/半模态全范式 |
| **MultiTravelAccommodation** | **40⭐** | [gitee](https://gitee.com/harmonyos_samples/multi-travel-accommodation) 栅格布局+List 响应式旅行住宿多场景 | 响应式布局实战 |
| **AnimationCollection** | **40⭐** | [gitee](https://gitee.com/harmonyos_samples/animation-collection) 基础组件+通用属性+显式动效，多种常见动效案例 | 动画开发参考 |
| **ContentPublisher** | 31⭐ | [gitee](https://gitee.com/harmonyos_samples/content-publisher) RichEditor + ArkUI 图文内容发布器 | 富文本编辑 |
| **WaterFlow** | **38⭐** | [gitee](https://gitee.com/harmonyos_samples/water-flow) WaterFlow 瀑布流、sections 混合排列、Tab吸顶、下拉刷新、无限加载 | 瀑布流全能力 |
| **GridHybrid** | **41⭐** | [gitee](https://gitee.com/harmonyos_samples/grid-hybrid) Grid + List + Swiper 嵌套混合布局 | 复杂布局实战 |
| **KnockShare** | 7⭐ | [gitee](https://gitee.com/harmonyos_samples/knock-share) 碰一碰分享（API 26 新特性匹配） | 设备协同 |
| **AudioFocus** | 2⭐ | [gitee](https://gitee.com/harmonyos_samples/audio-focus) 音频焦点/中断、自定义策略、AVSession后台播控 | 多音频冲突处理 |
| **FluentBlog** | 15⭐ | [gitee](https://gitee.com/harmonyos_samples/fluent-blog) 流畅刷页面示例 | 列表滚动性能优化 |
| **ConcurrentModule** | 18⭐ | [gitee](https://gitee.com/harmonyos_samples/concurrent-module) TaskPool + Worker 多线程实践 | 并发编程入门 |
| **HMRouter** | **53⭐** | [gitee](https://gitee.com/harmonyos_samples/HMRouter) 鸿蒙路由库，支持声明式路由+拦截器+参数校验 | 路由框架选型参考 |
| **UserAuth** | 24⭐ | [gitee](https://gitee.com/harmonyos_samples/UserAuth) 人脸+指纹认证、密码保险箱自动填充、防截屏/录屏 | 身份认证全流程 |
| **Watermark** | **28⭐** | [gitee](https://gitee.com/harmonyos_samples/watermark) 页面水印/保存图片水印/拍照水印 | 版权保护实践 |
| **ShareKit** | **38⭐** | [gitee](https://gitee.com/harmonyos_samples/share-kit_-sample-code_-clientdemo_-arkts) Share Kit 数据分享与应用内文件分享 | 分享功能全场景 |
| **WindowPiP** | 17⭐ | [gitee](https://gitee.com/harmonyos_samples/window-pip) 视频画中画、手动/自动拉起、PiP窗口控制播放 | 画中画开发参考 |
| **AudioInteraction** | 22⭐ | [gitee](https://gitee.com/harmonyos_samples/audio-interaction) 后台播放、播控中心交互、焦点打断策略、路由切换 | 音频播控全场景 |
| **SmoothSwitchShortVideos** | 8⭐ | [gitee](https://gitee.com/harmonyos_samples/SmoothSwitchShortVideos) LazyForEach+组件复用在短视频快速切换的性能优化 | 短视频性能优化 |
| **FormGame** | 5⭐ | [gitee](https://gitee.com/harmonyos_samples/form-game) Stage 模型实现简单游戏卡片 | 服务卡片开发 |
| **MultiDeviceInteraction** | 3⭐ | [gitee](https://gitee.com/harmonyos_samples/multi-device-interaction) 触控屏/触控板/鼠标/键盘统一交互 | 跨设备交互归一化 |
| **StateManagement** | 12⭐ | [gitee](https://gitee.com/harmonyos_samples/state-management) 页面级+应用级状态管理 | 状态管理入门 |
| **Aspect** | 0⭐ | [gitee](https://gitee.com/harmonyos_samples/aspect) 基于libabcKit字节码的AOP切面编程库 | 字节码增强/无侵入AOP |
| **Logger** | 13⭐ | [gitee](https://gitee.com/harmonyos_samples/logger) hilog 日志系统封装，日志分级+格式化 | 日志工具参考 |
| **FAQSnippets** | 10⭐ | [gitee](https://gitee.com/harmonyos_samples/faqsnippets) 常见问题代码片段合集 | FAQ速查 |

#### 📱 多设备「一多」系列 Samples（响应式布局最佳实践）

> 以下 Sample 均基于「一次开发、多端部署」理念，覆盖常见行业场景。

| Sample | Star | 适配设备 | 技术要点 |
|:------:|:----:|:---------|:---------|
| **MultiConvenientLife** | **34⭐** | 手机/折叠屏/平板/2in1 | 自适应+响应式布局，便捷生活页面 |
| **MultiNavBar** | **33⭐** | 多设备形态 | 导航栏在不同设备上的样式切换 |
| **MultiColumns** | 22⭐ | 多设备形态 | 多场景分栏控件响应式变化 |
| **MultiNewsRead** | 20⭐ | 手机/折叠屏/平板 | 新闻阅读页多设备适配 |
| **MultiTicketClass** | 17⭐ | 多设备 | 栅格+List 股票类多场景响应式 |
| **MultiShortVideo** | 23⭐ | 手机/折叠屏/2in1 | 三层工程架构+短视频多设备 |
| **MultiMobilePayment** | 14⭐ | 多设备 | Scan Kit扫码+收付款码支付 

### ⚡ 最佳实践片段集（BestPracticeSnippets，56⭐）

> 独立、聚焦的原子级实践代码，适合快速参考，每条解决一个具体问题。

| 分类 | 片段名称 | 解决的问题 |
|:----:|:---------|:----------|
| 🚀 **性能** | `AppColdStart` | 应用冷启动耗时优化指南 |
| | `AvoidTimeConsume` | 主线程耗时操作优化：异步化+TaskPool 拆分 |
| | `FramedRendering` | 高负载分帧渲染：多帧分摊渲染压力 |
| | `FuzzySceneOptimization` | 图像模糊动效性能优化 |
| | `ScreenFlickerSolution` | 应用动效闪屏排查与修复 |
| | `VisibleComponent` | 不可见组件低功耗策略 |
| 🔐 **安全** | `AppDataSecurity` | 应用数据安全规范 |
| | `AppPrivacyProtection` | 应用隐私保护实践 |
| 🧩 **UI** | `ComponentReuse` | 组件复用(@Reusable)开发实践 |
| | `CustomDialogPractice` | 自定义弹窗规范开发实践 |
| | `CustomTitleBarWindowDrag` | 自定义标题栏窗口拖动 |
| | `LiveViewLockScreen` | 锁屏沉浸实况窗（闪控窗/互动卡片） |
| | `ResponsiveLayout` | 自适应+响应式布局指导 |
| | `SubwindowAdaptWhenRotate` | 子窗旋转场景适配 |
| 🧵 **并发** | `ImageEditTaskPool` | 基于 TaskPool 实现图片编辑（带进度回调） |
| | `NdkQoS` | 基于 QoS 设置线程优先级 |
| | `ThreadIssueDetection` | 线程问题检测与优化 |
| 📶 **网络** | `NetworkManagement` | 网络管理与状态监听 |
| | `PreHttpRequestUseFiles` | Image 组件白块解决指导 |
| 🎬 **媒体** | `SegmentedPhotograph` | 分段式拍照：长曝光/多帧合成 |
| | `TextureHypercompression` | 纹理超压缩技术 |
| | `OnlineVideoPlaying` | 在线视频播放优化 |
| 🏗️ **架构** | `NavigationRouter` | Navigation + Router 选型指导 |
| | `StabilityCodingSpecification` | 稳定性编码规范 |

### 🧰 第三方生产级模式库

| 名称 | 地址 | 核心内容 | 定位 |
|:----:|:----:|:---------|:----:|
| **ArkTS Patterns** | [GitHub](https://github.com/OpeNopEn2007/arkts-patterns) | V2装饰器/TaskPool/Navigation/网络/持久化/手势/动画等 10+ 模式 | Claude Code Skill，100% 基准测试通过 |

---

## 📹 HMOSLiveStream 媒体直播全链路

> 源自官方 Sample `HMOSLiveStream`（22⭐）及华为最佳实践《基于媒体能力实现直播单播功能》。

### 开播端架构

```
音视频采集（OHAudio / 相机）
    ↓
编码（H.264/H.265 / HDR Vivid）
    ↓
推流（Surface 模式）
    ↓
ROI 编码（主播区域高质量，背景低码率）
    ↓
系统压力反馈（动态调整码率/帧率）
```

| 模块 | 技术方案 |
|:----:|:---------|
| **音频采集** | OHAudio API：常规录音/语音通话/直播三种模式 |
| **视频采集（SDR）** | 复用预览流，功耗低 + 红枫原色色彩算法 |
| **视频采集（HDR）** | HDR Vivid 复用预览流，暗光/高动态场景 |
| **视频编码** | Surface 模式，性能最优 |
| **ROI 编码** | 对主播区域高质量编码，背景压缩 |
| **智能调控** | 系统压力反馈接口 → 动态调整码率/帧率 |

### 看播端架构

```
流媒体加载（AVPlayer）
    ↓
音频播放时间戳同步
    ↓
视频送帧时延匹配
    ↓
音画同步输出
    ↓
内存泄漏防护（长时间直播稳定）
```

### 音频采集（OHAudio）

```typescript
import { ohAudio } from '@kit.AudioKit';

// 直播模式：高保真 + 回声消除
const audioCapturer = ohAudio.createAudioCapturer({
  streamUsage: ohAudio.StreamUsage.STREAM_USAGE_MUSIC,
  sourceType: ohAudio.SourceType.SOURCE_TYPE_MIC,
  capturerOptions: {
    encoding: ohAudio.AudioEncoding.ENCODING_PCM,
    sampleRate: 48000,
    channelCount: 2,
  }
});
await audioCapturer.start();
```

### 视频播放（AVPlayer）

```typescript
import { media } from '@kit.MediaKit';

avPlayer = await media.createAVPlayer();
avPlayer.url = 'rtmp://stream.example.com/live';  // 流媒体地址
avPlayer.stateChangeCallback = (state) => {
  if (state === 'prepared') avPlayer.play();
};
```

### 场景适配策略

| 场景 | 技术方案 |
|:----:|:---------|
| 🛒 **电商直播** | 红枫原色色彩校正 + HDR Vivid 暗光增强 + ROI 主播聚焦 |
| 🎤 **娱乐直播** | 高保真录音 + 回声消除 + ROI 表演区域 |
| 🌄 **户外直播** | 红枫原色色彩 + 压力反馈动态调速 + 散热关注 |

## 🎬 MultiShortVideo 多设备短视频

> 源自官方 Sample `multi-short-video`（23⭐），基于三层架构 + Swiper 短视频轮播。

### 核心模式

与多设备长视频/音乐/社区评论同属"一多"系列，关键差异化特性：

| 特性 | 实现 |
|:----:|:------|
| **短视频轮播** | `Swiper` + `LazyForEach` 纵向滑动切换 |
| **评论/点赞交互** | 底部浮层组件 |
| **个人作品页** | 三列 Grid 布局 |
| **分享** | Share Kit 设备自适应分享弹窗 |
| **三层工程架构** | commons/features/products 复用 |

## 🛍️ MultiShoppingPriceComparison 购物比价

> 三层架构（commons/features/products）+ Navigation Split 分栏 + BreakpointType / Tabs 响应式导航。

### 关键代码

```typescript
// Tabs 响应式：手机底部 ↔ 平板侧边
Tabs({
  barPosition: this.currentBreakpoint === 'lg'
    ? BarPosition.Start : BarPosition.End
})
.barWidth(this.currentBreakpoint === 'lg'
  ? $r('app.float.tab_bar_width_lg') : '100%')
.vertical(this.currentBreakpoint === 'lg')

// 分类页双栏（Navigation Split 模式）
Navigation(this.pageInfo)
  .mode(NavigationMode.Split)
  .navBarWidth(new BreakpointType('96vp', '144vp', '200vp')
    .getValue(this.currentBreakpoint))

// 页面边距断点适配
private static pageColPadding = new BreakpointType(
  $r('app.float.padding_sm'),
  $r('app.float.padding_md'),
  $r('app.float.padding_lg'));
```

## 💳 MultiMobilePayment 移动支付（14⭐）

> 三层架构 + Scan Kit 扫码/码图生成，完整移动支付全流程。

### 关键代码

```typescript
import { scanCore } from '@kit.ScanKit';
import { generateBarcode } from '@kit.ScanKit';

// 扫一扫（默认界面）
const result = await scanCore.startScan({
  scanType: scanCore.ScanType.QR_CODE,
});

// 生成付款码
const barcode = generateBarcode.createBarcode({
  content: 'payment://merchant/xxx',
  format: BarcodeFormat.QR_CODE,
  width: 200, height: 200,
});
```

**多设备适配**：手机单列 → 折叠屏双栏 → 平板左侧扫码+右侧交易记录

## MultiShortVideo 多设备短视频

> Swiper + Video + LazyForEach 短视频上下滑动切换。

### 关键代码

```typescript
Swiper(this.swiperController) {
  LazyForEach(this.data, (item: VideoData) => {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Video({
        src: item.video,
        controller: item.controller
      })
      .width('100%').height('100%')
      .objectFit(ImageFit.Contain)
      .loop(true).autoPlay(item.auto)
      .controls(false)  // 隐藏控制栏
    }
  }, (item) => JSON.stringify(item))
}
.index(0).autoPlay(false).indicator(false)
.loop(true).duration(200).vertical(true)

// 性能：LazyForEach + cachedCount
```

## 📱 Live View Kit 锁屏实况窗

> 源自 BestPracticeSnippets `LiveViewLockScreen` + `@kit.LiveViewKit`。

### 核心代码

```typescript
import { liveViewManager } from '@kit.LiveViewKit';

const mgmt = liveViewManager.getLiveViewManager();

// 发布实况窗（进度模板）
const builder = new liveViewManager.LiveViewData.Builder();
builder.setTemplate(liveViewManager.LiveViewTemplate.PROGRESS);
builder.setTitle('订单 #202511290001');
builder.setProgress(50);
builder.setStatus('配送中');

await mgmt.publish(builder.build(), {
  isPersistent: true,
  isShowOnLockScreen: true,
});

// 关闭
await mgmt.dismiss();

// 状态监听
mgmt.on('liveViewStateChange', (state) => { /* SHOWN/DISMISSED */ });
```

**注意事项**：`ohos.permission.REAL_TIME_ACTIVITY` 权限 + AGC 正式申请 + 锁屏文字用白色

---

## 🌀 ImageEditWithWavewheel 修图波轮菜单（2,256 下载）

> 源自官方 Sample `ImageEditWithWavewheel` + `SubWinWaveWheel` 组件。Pen Kit 手写笔 + SubWindow 悬浮波轮 + 图片编辑。

### 整体架构

```
Pen Kit（@kit.Penkit）
├── stylusInteraction     → 轻捏(squeeze)/双击(doubleTap)
└── imageFeaturePicker    → 屏幕取色(pickForResult)

SubWindow 悬浮波轮菜单
├── 可拖拽 + 智能吸边
├── 单击展开扇形工具栏（四象限自适应方向）
└── 手写笔轻捏快捷弹出
```

### Pen Kit 手写笔事件

```typescript
import { stylusInteraction, imageFeaturePicker } from '@kit.Penkit';

// ★ 回调引用必须保存为成员变量
private squeezeCB: (event: stylusInteraction.SqueezeEvent) => void = () => {};

aboutToAppear(): void {
  this.squeezeCB = (event) => this.showWaveWheel();
}
onPageShow(): void {
  try { stylusInteraction.on('squeeze', this.squeezeCB); } catch (e) {}
}
onPageHide(): void {
  stylusInteraction.off('squeeze', this.squeezeCB); // 同一引用才能取消
}

// 屏幕取色器
Button('取色').onClick((e: ClickEvent) => {
  imageFeaturePicker.pickForResult(e.displayX, e.displayY)
    .then((info) => this.color = info.color)
    .catch((err) => { if (err.code !== CANCEL) throw err; });
});
```

### SubWindow 扇形波轮菜单

```typescript
// 创建悬浮子窗口
const subWin = await ctx.windowStage.createSubWindow('wavewheel');
await subWin.setWindowType(window.WindowType.TYPE_FLOAT);
await subWin.resize(40, 40);
await subWin.setUIContent('pages/WaveWheel');
await subWin.showWindow();

// 扇形展开算法（四象限自适应，朝无阻挡方向展开）
function calcAngle(index: number, cx: number, cy: number) {
  const centerX = screenW / 2, centerY = screenH / 2;
  const gap = (90 - 10) / 3; // 4个按钮均分80°，留10°安全边界
  let rad = 0;
  if (cx < centerX && cy > centerY) rad = (175 - index * gap) * Math.PI / 180;
  else if (cx > centerX && cy > centerY) rad = (355 - index * gap) * Math.PI / 180;
  else if (cx < centerX && cy < centerY) rad = (85 - index * gap) * Math.PI / 180;
  else rad = (265 - index * gap) * Math.PI / 180;
  return { x: 120 * Math.cos(rad), y: 120 * Math.sin(rad) };
}

// 手势互斥（GestureMode.Exclusive）
Circle().gesture(GestureGroup(GestureMode.Exclusive,
  TapGesture().onAction((e) => toggleMenu(e)),
  PanGesture().onActionUpdate((e) => drag(e)).onActionEnd(() => snap()),
));
```

### 注意事项
- **回调引用**：必须保存为成员变量，`off()` 无效会导致泄漏
- **坐标系**：SubWindow 用 px，UI 用 vp，需 `vp2px`/`px2vp`
- **窗口跳动**：展开时窗口扩大 → 同步移动保持主球屏幕坐标不变
// 系统自动根据主题加载对应目录资源，代码无需判断
```

### 检测和切换
```typescript
// 方式1：跟随系统（推荐）
this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_AUTO);

// 方式2：手动控制
this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_DARK);

// 方式3：组件内监听主题变化
@State isDark: boolean = false;
aboutToAppear() {
  this.context.on('configuration', (config) => {
    this.isDark = config.colorMode === ConfigurationConstant.ColorMode.COLOR_MODE_DARK;
  });
}
```

### 图片适配
```typescript
// 方式1：dark限定词目录（两套图）
// resources/base/media/logo.png  ← 浅色
// resources/dark/media/logo.png  ← 深色
Image($r('app.media.logo')) // 自动选择

// 方式2：SVG fillColor 动态变色
Image($r('app.media.ic_setting'))
  .fillColor(this.isDark ? '#FFFFFF' : '#1A1A1A')
```

### 适配检查清单
- ✅ 所有颜色值用 `$r('app.color.xxx')` 引用，不写死十六进制
- ✅ 图片分深浅两套放 base/dark 目录
- ✅ 状态栏图标颜色跟随主题（通过 window 配置）
- ✅ 深色背景用 #121212 而非纯黑 #000000
- ✅ 深色文字用 #E0E0E0 而非纯白 #FFFFFF
- ✅ 高亮品牌色在深色模式下适当降饱和度

---

## 🔐 安全与工具（UserAuth + Watermark + ShareKit + Aspect）

### UserAuth — 人脸/指纹认证

```typescript
import { userAuth } from '@kit.UserAuthKit';

const auth = userAuth.getUserAuthInstance({
  challenge: new Uint8Array([1,2,3]),
  authType: [userAuth.UserAuthType.FACE, userAuth.UserAuthType.PIN],
});

auth.on('result', { onResult: (result) => {
  if (result.result === 0) { /* 认证成功 */ }
}});
auth.start();
```

### Watermark — 水印

```typescript
// 使用文本叠加实现水印
Text('内部资料 · 请勿外传')
  .fontSize(16).fontColor('#40FFFFFF')
  .rotate({ angle: -30 })
  .position({ x: '60%', y: '40%' })
  .width('100%').height('100%')
```

### ShareKit — 分享

```typescript
import { shareController } from '@kit.ShareKit';
import { fileShare } from '@kit.ShareKit';

// 分享文本
shareController.share({ text: '分享内容', title: '标题' });
// 分享文件
fileShare.share({ filePaths: ['/data/app/a.jpg'] });
```

---

## 🧭 HMRouter 路由框架（53⭐）

> 基于系统 Navigation 封装的页面路由方案，注解声明式路由，支持拦截器/生命周期/转场动画。

### 核心特性

| 特性 | 说明 |
|:----:|:------|
| **注解声明路由** | `@HMRouter({ pageUrl: 'home', singleton: true })` 声明页面 |
| **路由拦截器** | 全局拦截 + 单页面拦截 + 跳转时一次性拦截 |
| **生命周期回调** | 全局生命周期 + 单页面生命周期 + 一次性生命周期 + NavBar生命周期 |
| **转场动画** | 内置页面/Dialog动画，支持方向/透明度/缩放/交互式 |
| **服务路由** | 支持服务型路由，实现模块间解耦 |
| **Dialog 页面** | 支持 Dialog 类型页面和单例页面 |
| **模块类型** | 支持 HAR / HSP / HAP |
| **路由栈嵌套** | 支持 Navigation 路由栈嵌套 |

### 注解声明路由

```typescript
import { HMRouter } from '@ohos/hmrouter';

@HMRouter({
  pageUrl: 'home',
  singleton: true,       // 单例页面
  dialog: false,
  title: '首页'
})
@Component
export struct HomePage {
  build() {
    Column() { /* ... */ }
  }
}
```

### 路由跳转与拦截

```typescript
import { HMRouterMgr } from '@ohos/hmrouter';

// 页面跳转
HMRouterMgr.pushUrl({ pageUrl: 'product/detail', param: { id: 123 } });

// 拦截器示例
// LoginCheckInterceptor.ets — 未登录则拦截跳转到登录页
class LoginCheckInterceptor implements IHMRouterInterceptor {
  onBeforePageJump(info: JumpInfo): boolean {
    if (!isLoggedIn && info.pageUrl !== 'login') {
      HMRouterMgr.pushUrl({ pageUrl: 'login' });
      return false; // 拦截本次跳转
    }
    return true;
  }
}
```

### 生命周期回调

```typescript
// 全局页面停留时长统计
class PageDurationLifecycle implements IHMRouterLifecycle {
  onPageShow(info: RouterInfo): void { logger.info(`enter ${info.pageUrl}`); }
  onPageHide(info: RouterInfo): void { logger.info(`leave ${info.pageUrl}`); }
}
```

### 目录结构范式（HMRouter 参考）

```
entry/src/main/ets/
├── component/         # 业务页面
│   ├── home/          # 按功能模块分目录
│   ├── product/
│   ├── login/
│   ├── pay/
│   └── shoppingBag/
├── interceptor/       # 全局拦截器
│   ├── LoginCheckInterceptor.ets
│   └── JumpInfoInterceptor.ets
├── lifecycle/         # 全局生命周期
│   ├── PageDurationLifecycle.ets
│   ├── ExitAppLifecycle.ets
│   └── WelcomeLifecycle.ets
├── service/           # 服务路由
├── viewmodel/         # 视图模型
├── constant/          # 页面常量与断点
├── animation/         # 自定义转场动画
└── pages/             # Navigation 入口页面
```

---

## 🧵 AOP 切面编程（util.Aspect）

> 鸿蒙内置运行时 AOP 能力，基于 libabcKit 字节码操作，对标 iOS 的 method_swizzling。`@kit.ArkTS` 中提供 `util.Aspect` 类。

### 核心 API

```typescript
import { util } from '@kit.ArkTS';

util.Aspect.addBefore(targetClass, methodName, isStatic, beforeFunc);  // 执行前插桩
util.Aspect.addAfter(targetClass, methodName, isStatic, afterFunc);    // 执行后插桩
util.Aspect.replace(targetClass, methodName, isStatic, insteadFunc);   // 替换实现
```

### addBefore — 执行前插桩

在方法执行前插入逻辑。适合：日志埋点、参数校验、权限检查、打点统计。

```typescript
class DataService {
  data: string = 'init';
  fetchData(url: string): number {
    console.info('original fetchData: ' + url);
    return 200;
  }
}

// 在所有 fetchData 调用前插入日志
util.Aspect.addBefore(DataService, 'fetchData', false,
  (instance: DataService, url: string): void => {
    console.info(`[AOP] before fetchData: ${url}`);
    instance.data = 'modified_by_aop';
  });
```

### addAfter — 执行后插桩

在原方法之后插入逻辑。适合：结果增强、缓存写入、数据统计。

```typescript
util.Aspect.addAfter(DataService, 'fetchData', false,
  (instance: DataService, ret: number, url: string): number => {
    console.info(`[AOP] after fetchData, result=${ret}`);
    return ret + 100; // 可以修改返回值
  });
```

### replace — 替换方法实现

完全替换原方法逻辑。适合：Mock 数据、功能降级、热修复。

```typescript
util.Aspect.replace(DataService, 'fetchData', false,
  (instance: DataService, url: string): number => {
    console.info('[AOP] replaced fetchData, returning mock');
    return 999; // Mock 返回
  });
```

### 典型应用场景

| 场景 | 推荐方式 | 说明 |
|:----:|:--------:|:------|
| 全埋点/无痕埋点 | `addBefore` | 在按钮点击/页面跳转方法前插入 |
| 参数合法性校验 | `addBefore` | 校验参数，不合法则提前 return |
| 权限检查 | `addBefore` | 检查权限状态，未授权则拦截 |
| 数据缓存 | `addAfter` | 网络请求成功后自动写入缓存 |
| 运行时 Mock | `replace` | 开发/测试环境替换真实 API 调用 |
| 热修复 | `replace` | 线上紧急修复，替换有 Bug 的方法 |

---

### 通知类型
```typescript
import { notificationManager } from '@kit.NotificationKit';

// 1. 普通文本通知
let request: notificationManager.NotificationRequest = {
  id: 1,
  content: {
    contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
    normal: { title: '标题', text: '内容' }
  },
  slotType: notificationManager.SlotType.SOCIAL_COMMUNICATION
};
await notificationManager.publish(request);

// 2. 进度条通知（下载/更新）
let progressRequest: notificationManager.NotificationRequest = {
  id: 2,
  content: {
    contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_LONG_TEXT,
    normal: { title: '下载中', text: '50%', additionalText: '5MB/10MB' }
  },
  // 进度通过 ongoing 持续更新
  ongoing: true,  // 不可滑动清除
};
// 更新进度
await notificationManager.publish({
  ...progressRequest,
  content: { normal: { text: '80%', additionalText: '8MB/10MB' } }
});

// 3. 分组通知（同一会话归组）
const groupRequest = {
  ...request,
  groupName: 'chat_group',       // 同一 groupName 自动归组
  groupOverview: { title: '3条消息', text: '最新:你好' }
};

// 4. 可交互通知（带按钮）
import { wantAgent } from '@kit.AbilityKit';
const wantAgentInfo = {
  wants: [{ bundleName: 'com.example', abilityName: 'DetailAbility' }],
  operationType: wantAgent.OperationType.START_ABILITY,
  requestCode: 100,
};
const agent = await wantAgent.getWantAgent(wantAgentInfo);
await notificationManager.publish({
  id: 3,
  content: {
    contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
    normal: { title: '新消息', text: '点击查看' }
  },
  wantAgent: agent,  // 点击通知跳转
});
```

### 通知分组/槽位
| SlotType | 用途 | 特性 |
|---------|------|------|
| SOCIAL_COMMUNICATION | 社交消息 | 高优先级、横幅+锁屏 |
| SERVICE_INFORMATION | 服务信息 | 中等优先级 |
| CONTENT_INFORMATION | 内容资讯 | 普通优先级 |
| OTHER | 其他 | 最低优先级、静默 |


## 📦 ohpm 包发布指南

> HAR 共享包发布到 OpenHarmony 三方库中心仓，复用生态。

### oh-package.json5 配置

```json5
{
  "name": "@your/lib_log",
  "version": "1.0.0",
  "description": "简短的包描述",
  "main": "Index.ets",
  "author": "你的名字",
  "license": "Mulan PSL v2",
  "dependencies": {},
  "packageType": "har"    // har / hsp
}
```

### 发布流程（官方验证）

```bash
# 1. 注册中心仓 https://ohpm.openharmony.cn 获取 publish_id
# 2. 生成密钥对（ohpm 要求加密传输，生成时必须设置密码）
ssh-keygen -m PEM -t RSA -b 4096 -f ~/.ssh_ohpm/mykey

# 3. 配置 ohpm（publish_id 和 key_path 也可在 publish 命令中直接传参）
ohpm config set publish_id your_publish_id
ohpm config set key_path ~/.ssh_ohpm/mykey

# 4. 构建 HAR
hvigorw assembleHar

# 5. 发布
ohpm publish lib_log.har
```

### 发布校验规则（官方）

| 要求 | 说明 |
|:----|:------|
| **文件格式** | 必须是 `.har` 或 `.tgz` 包 |
| **必需文件** | `oh-package.json5` + `README.md` + `LICENSE` + `CHANGELOG.md`（不能为空） |
| **oh-package.json5 必填字段** | `name`、`version`、`description`、`main`、`license` |
| **依赖完整性** | 所有直接依赖必须在包的 oh-package.json5 中声明 |
| **版本唯一** | 已发布的名称+版本组合不可重复使用 |

### 最佳实践

- **摘除外部依赖**：发布前移除未上中心仓的本地模块引用
- **README 必含安装命令**：`ohpm install @your/package`
- **版本号管理**：遵守 semver 规范，`ohpm version patch/minor/major`
- **HSP vs HAR**：HAR 可发中心仓，HSP 只能发私仓
- **清理命令**：`ohpm clean` 删除所有 oh_modules 目录和 lock 文件

### ohpm 常用命令

```bash
ohpm install @ohos/package        # 安装依赖
ohpm install --all                 # 安装全部模块依赖
ohpm install --registry <url>      # 指定仓库地址
ohpm uninstall @ohos/package      # 卸载依赖
ohpm list                          # 查看依赖树
ohpm update @ohos/package         # 更新依赖
ohpm clean                         # 清理所有 oh_modules
```

---


---

## 🔧 NativeSoIntegration .so 集成（第四轮新增）

> **来源**：`NativeSoIntegration` | Gitee harmonyos_samples | 源码级

| 方案 | 方式 | 复杂度 |
|:----:|------|:------:|
| 编译引用 | CMakeLists.txt + 头文件 | ⭐ |
| dlopen | `dlopen()`/`dlsym()` | ⭐⭐ |
| ArkTS 模块依赖 | oh-package.json5 + import | ⭐ |

```typescript
// 方案3（最推荐）: ArkTS 直接 import
// entry/oh-package.json5 → "dependencies": { "libmultiply": "file:src/main/cpp/types/libmultiply" }
// import { multiply } from 'libmultiply'
// multiply(3, 4) → 12
```

---

## 📚 LanguageBaseClassLibrary 语言基础类库（第五轮新增）

> **来源**：`language-base-class-library` | Gitee harmonyos_samples | 源码级

### 子模块清单

| 分类 | 模块 | 说明 |
|------|------|------|
| **util工具** | StringCode / LRUCache / Base64 / RationalNumber / ScopeHelper / TypeCheck / JsonFunction | 字符串编解码/LRU缓存/Base64编解码/有理数比较/范围判断/类型检查/Json操作 |
| **ArkTSUtil** | AsonFunction | ISendable 序列化/反序列化 |
| **TaskPool** | `@ohos.taskpool` | 后台任务创建/执行/取消 |
| **Uri/Url** | `@ohos.uri` / `@ohos.url` | URI解析/URL参数增删改查 |
| **Xml** | `@ohos.xml` / `@ohos.convertxml` | XML解析生成 / XML转JS对象 |
| **线性容器** | ArrayList / Deque / LinkedList / List / Queue / Stack | 有序数据集合 |
| **非线性容器** | HashMap / HashSet / LightWeightMap / LightWeightSet / PlainArray / TreeMap / TreeSet | 键值对/集合 |

### 核心 API 速查

```typescript
// HashMap 使用
let map = new HashMap<string, number>()
map.set('key', 1)
map.get('key')      // → 1
map.delete('key')

// util 工具
let encoder = new util.TextEncoder()
let decoder = new util.TextDecoder('utf-8', { ignoreBOM: true })

// LRU Cache
let cache = new util.LRUCache<string, number>(100)
cache.put('a', 1)
cache.get('a')      // → 1
```

---



# 第十三部分：布局与自适应（ArkUI自适应布局模式）
<a name="part13"></a>

## 📐 ArkUI 自适应布局模式（官方精学验证）

> 一次开发多端部署（一多）的核心布局模式。**注意：`BreakpointType` 是社区封装的工具类，非 ArkUI 内置 API**，官方方案使用 `GridRow` + `MediaQuery`。

### 三大布局策略

| 策略 | 适用 | 官方 API |
|:----|:----|:---------|
| **自适应布局** | 同设备尺寸变化 | `layoutWeight` / `flexShrink` / 百分比% |
| **响应式布局** | 跨设备形态变化 | `GridRow` + `GridCol` / `MediaQuery` |
| **多态组件** | 同一组件不同显示 | `@Styles` + `@Extend` + 条件渲染 |

### 官方断点系统（`GridRow`）

```typescript
// GridRow breakpoints 属性（官方 API）
GridRow({
  breakpoints: {
    value: ['600vp', '840vp'],             // 断点：sm<600, md<840, lg>=840
    reference: BreakpointsReference.WindowSize  // 相对窗口大小
  }
}) {
  GridCol({ span: { sm: 12, md: 6, lg: 4 } }) {  // 手机满宽，平板半宽，PC 1/3
    Text('自适应内容')
  }
}
```

### 使用 `mediaquery` 监听断点（官方 API）

```typescript
import { mediaquery } from '@ohos.mediaquery';

@Component
struct AdaptivePage {
  @State currentBreakpoint: 'sm' | 'md' | 'lg' = 'sm';

  listener = mediaquery.matchMediaSync('(min-width: 600vp) and (max-width: 839vp)');

  aboutToAppear() {
    this.listener.on('change', (result) => {
      // 根据 match 结果更新状态
    });
  }
}
```

### 断点参考值

| 断点 | vp 范围 | 典型设备 |
|:----|:-------|:--------|
| xs | 0~319vp | 小屏手表 |
| sm | 320~599vp | 手机竖屏 |
| md | 600~839vp | 折叠屏展开/小平板 |
| lg | 840~1199vp | 平板横屏 |
| xl | ≥1200vp | PC/2in1 |

### 常见布局模式

```typescript
// 折叠屏自适应双栏/单栏（官方推荐方式）
if (this.currentBreakpoint === 'sm') {
  // 单栏：Navigation 全屏
  Navigation() { /* ... */ }
    .title('列表')
    .navDestination(this.pageStack)
} else {
  // 双栏：侧栏 + 内容
  Row() {
    SideBarContainer() { /* 列表 */ }
      .width(320)
    Column() { /* 详情 */ }
      .layoutWeight(1)
  }
}
```

---

> `references/` 目录下收录了 **60 个核心 @ohos.* 模块的离线 API 参考文档**，覆盖网络、数据、Ability、ArkUI、媒体、安全、工具等主要分类。
>
> **检索流程：先查索引 → 再读文档**，避免全量读取。

### 三层索引体系

```
SKILL.md → references/KITS.md / TASK_MAP.md → references/INDEX.md → 目标文档
```

| 层级 | 文件 | 用途 |
|:----|:-----|:----|
| 第1层 | `KITS.md` | Kit 导航：按功能分类（NetworkKit、AbilityKit、ArkData 等） |
| 第2层 | `TASK_MAP.md` | 任务导航：按"我想做什么"反查（网络请求、数据存储、权限申请等） |
| 第3层 | `INDEX.md` | 全库路径索引：所有模块文件的完整路径清单 |

### 检索命令速查

```bash
# ① 在 INDEX 中搜索关键词
rg -n "UIAbility|Want|AbilityStage" references/INDEX.md | head

# ② 按模块前缀搜索
rg -n "net\\.http|file\\.fs|data\\.preferences" references/INDEX.md | head

# ③ 搜索特定方法名
rg -n "createHttp|request|destroy" references/INDEX.md | head

# ④ 在 KITS 中识别 Kit
rg -n "网络|数据|安全|媒体" references/KITS.md | head
```

### 模块分类速览

| 分类 | 模块数 | 包含模块 |
|:----|:-----:|:--------|
| 📡 网络通信 | 4 | `net.http`, `net.socket`, `net.webSocket`, `net.connection` |
| 💾 数据存储 | 5 | `data.preferences`, `data.rdb`, `relationalStore`, `distributedKVStore`, `distributedDataObject` |
| 📱 Ability | 8 | `app.ability.UIAbility`, `Want`, `AbilityStage`, `common`, `Configuration`, `appManager`, `wantAgent` + 更多 |
| 🎨 ArkUI | 6 | `arkui.UIContext`, `inspector`, `observer`, `StateManagement`, `dragController`, `componentSnapshot` |
| 📷 媒体 | 4 | `multimedia.camera`, `audio`, `image`, `media` |
| 🔐 安全 | 4 | `security.cryptoFramework`, `huks`, `cert`, `abilityAccessCtrl` |
| 🔧 工具 | 7 | `hilog`, `taskpool`, `worker`, `resourceManager`, `util`, `promptAction`, `hidebug` |
| 📍 位置 | 3 | `geoLocationManager`, `bluetooth`, `distributedDeviceManager` |
| 📂 文件 | 3 | `file.fs`, `file.picker`, `file.fileuri` |
| 📦 其他 | 16 | 图形、通知、窗口、传感器、输入法、上传下载、后台任务、包管理等 |

### 回答规则

- **不确定 API 签名** → 查 `references/INDEX.md` 找到文档路径 → 只读对应 `.md` 文件
- **不确定模块存在与否** → 在 INDEX 中搜索模块名
- **需要代码示例** → 先在离线文档找官方示例，再结合 SKILL.md 的实战经验优化
- **优先使用离线文档**，模型记忆为辅
- **版本差异**：离线文档基于 API 22-23，API 25-26 新能力以 SKILL.md 中的 §6 API 26 新能力详解 为准

> `references/` 目录路径相对于本 SKILL.md。


### 20. Stage 模型详解（UIAbility、AbilityStage、Context、WindowStage）— 官方指南精学

> **目标读者**：需要理解 HarmonyOS Stage 模型应用组件框架的开发者。本文基于 [UIAbility组件概述](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/uiability-overview-V5) 和 [UIAbility生命周期](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/uiability-lifecycle-V5) 官方文档精学验证。

#### 20.1 UIAbility 组件概述

**UIAbility** 是一种包含 UI 的应用组件，主要用于和用户交互。是系统调度的基本单元，为应用提供绘制界面的窗口。

**设计理念**：
1. 原生支持应用组件级的跨端迁移和多端协同
2. 支持多设备和多窗口形态

**划分原则**：
- 一个应用可以包含一个或多个 UIAbility 组件
- 每个 UIAbility 组件实例在最近任务列表中显示一个对应任务
- 任务视图中看到一个任务 → 建议使用"一个 UIAbility + 多个页面"
- 任务视图中看到多个任务 → 建议使用多个 UIAbility

**声明配置**（module.json5）：
```json5
{
  "module": {
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:icon",
        "startWindowBackground": "$color:start_window_background"
      }
    ]
  }
}
```

#### 20.2 UIAbility 生命周期

UIAbility 生命周期包括 **Create、Foreground、Background、Destroy** 四个状态，以及 **WindowStageCreate、WindowStageDestroy** 两个窗口相关状态。


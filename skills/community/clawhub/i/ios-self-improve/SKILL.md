---
name: ios-self-improve
description: "iOS 开发自改进技能 - Swift/ObjC 规范、审核合规、崩溃预防、自动自检、Xcode、UIKit、SwiftUI"
metadata: 
  emoji: "📱"
  version: "1.1.0"
  author: "lijiujiu"
  license: "MIT"
  requires:
    bins: ["bash", "find", "grep"]
  dependencies:
    - developer-self-improve-core
  tags: ["ios", "swift", "objective-c", "development", "self-improvement", "apple", "mobile", "xcode", "iphone", "ipad"]
  keywords: ["ios", "iOS", "IOS", "ios 开发", "ios developer", "ios development", "iphone", "ipad", "xcode", "swift", "objective-c", "app-store", "uikit", "swiftui", "ios 程序员", "ios engineer"]
---

# 📱 ios-self-improve

**iOS 开发者自改进技能** - 依赖 developer-self-improve-core 安全闭环

---

## ⚠️ 依赖说明

**本 Skill 必须与 developer-self-improve-core 配合使用：**

```bash
# 先安装核心技能
clawhub install developer-self-improve-core

# 再安装 iOS 扩展技能
clawhub install ios-self-improve
```

**依赖关系：**
- ✅ 所有自改进操作（规则生成、清洗建议）均由 developer-self-improve-core 执行
- ✅ 本 Skill 仅提供 iOS 领域知识与自检逻辑
- ✅ 遵循"AI 提议、人类终审"原则，不自动修改任何记忆

---

## 🎯 核心功能

### 1. iOS 全栈知识覆盖

| 领域 | 覆盖内容 |
|------|----------|
| **语言** | Swift 5.x, Objective-C |
| **UI 框架** | UIKit, SwiftUI |
| **工具** | Xcode, Instruments, TestFlight |
| **生态** | App Store, 审核，推送，Widget |

---

### 2. 内置领域规则（15 条）

#### 基础规范

1. ✅ **iOS 系统版本适配规范**
   - 最低版本兼容判断
   - API 废弃判断
   - 多版本适配技巧

2. ✅ **UIKit 导航栏最佳实践**
   - 过渡动画处理
   - scrollEdgeAppearance 配置
   - 样式统一

3. ✅ **AutoLayout 规则**
   - 约束编写规范
   - 冲突排查
   - 屏幕适配
   - 多设备兼容

4. ✅ **内存管理规范**
   - ARC 使用技巧
   - 循环引用排查
   - 内存泄漏预防
   - 弱引用/无主引用使用场景

5. ✅ **代码风格与格式规范**
   - SwiftLint 标准
   - Swift/ObjC 编码规范
   - 注释规范

#### 风险预防

6. ✅ **常见崩溃预防规则**
   - 数组越界
   - 空指针
   - KVO/通知使用不当
   - 线程安全问题

7. ✅ **SwiftUI 布局与生命周期规范**
   - 视图渲染
   - 状态管理
   - 导航适配

8. ✅ **应用生命周期管理**
   - 前台/后台/挂起/终止状态处理
   - 场景切换适配

9. ✅ **Swift Concurrency 异步编程规范**
   - Task/Actor 使用
   - 死锁预防
   - 数据竞争规避

#### 审核与合规

10. ✅ **苹果审核规范**
    - 隐私权限配置
    - 功能合规
    - 文案规范
    - 被拒问题应对

11. ✅ **权限配置与隐私规范**
    - Info.plist 配置
    - 隐私描述编写
    - 权限申请逻辑

12. ✅ **沙盒文件读写规范**
    - 目录划分
    - 数据存储安全
    - 文件权限管理

#### 适配与体验

13. ✅ **暗黑模式（Dark Mode）适配规范**
    - 颜色适配
    - 图片适配
    - 控件适配

14. ✅ **本地化与多语言适配规范**
    - 字符串本地化
    - 界面适配
    - 区域设置

15. ✅ **推送通知、WidgetKit 开发规范**
    - 配置流程
    - 适配要求
    - 审核要点

---

### 3. iOS 专属自检逻辑（11 条）

**每轮回答后自动检查：**

| # | 检查项 | 违规示例 |
|---|--------|----------|
| 1 | 导航栏过渡闪烁、scrollEdgeAppearance 未处理 | 导航栏样式不一致 |
| 2 | 苹果审核规范、隐私权限缺失 | Info.plist 缺少 NSPhotoLibraryUsageDescription |
| 3 | 潜在崩溃风险 | array[0] 未检查 count |
| 4 | 内存泄漏、循环引用 | [weak self] 缺失 |
| 5 | 过时/不兼容 API | 使用已废弃的 UIWebView |
| 6 | AutoLayout 约束冲突 | 约束缺失或矛盾 |
| 7 | SwiftUI 生命周期错误 | @State 使用不当 |
| 8 | 异步代码死锁、数据竞争 | 主线程阻塞 |
| 9 | 沙盒违规读写 | 访问非授权目录 |
| 10 | Info.plist 配置错误 | 缺少必要配置 |
| 11 | 暗黑模式适配缺失 | 硬编码颜色 |

---

## 🔄 触发时机

| 时机 | 执行内容 | 频率 |
|------|----------|------|
| **pre_answer** | 检索长期记忆中 iOS 专属规则，自动规避历史错误 | 每轮回答前 |
| **post_answer** | 执行 iOS 专属自检逻辑，生成领域规则草案 | 每轮回答后 |
| **periodic** | 联动 developer-self-improve-core，扫描 iOS 领域规则 | 累计 10 轮对话或每周 |

---

## ⚙️ 约束条件

### 1. 依赖约束

- ✅ 严格依赖 developer-self-improve-core
- ✅ 所有规则草案、清洗建议均需经用户终审
- ✅ 不自动写入/修改/删除长期记忆

### 2. 优先级排序

```
用户指令 > 长期记忆（iOS 专属规则） > AI 临时草案
```

### 3. 输出规范

- ✅ 代码输出必须遵循苹果官方文档
- ✅ 遵循行业最佳实践
- ✅ 适配最新正式版 iOS 系统
- ✅ 兼顾主流旧版本兼容

### 4. 依据验证

**禁止生成的内容：**
- ❌ 主观推断、未验证的 iOS 规则
- ❌ 一次性特例的泛化
- ❌ 来源不明的"自创规则"

**允许生成的草案（需满足）：**
- ✅ 用户明确指出的错误
- ✅ ≥2 次可复现模式
- ✅ 可验证硬错误

### 5. Token 优化

- ✅ 长期记忆中 iOS 规则保持极简结构化
- ✅ 优先加载与当前开发场景匹配的条目
- ✅ 不加载全部规则

### 6. 追溯与回滚

- ✅ 所有自检结果可追溯
- ✅ 规则草案可追溯
- ✅ 操作记录可追溯
- ✅ 支持回滚至历史版本
- ✅ 规则冲突时以最新人工确认规则优先

---

## 📝 规则草案格式（与 developer-self-improve-core 一致）

```markdown
### 【规则 ID】auto_ios_xxxx
### 【场景】iOS 开发场景（≤20 字）
### 【问题/模式】明确描述的问题或可复现模式
### 【建议规则】极简一句话，可直接执行
### 【依据】用户明确指出/重复模式/可验证错误
### 【可信度】高/中/低
### 【建议层级】长期/中期
### 【领域】iOS/具体子领域
```

---

## 🚀 使用示例

### 示例 1: 导航栏配置问题

**用户提问：**
```
导航栏在滚动时样式不一致，如何处理？
```

**AI 回答前：**
```
pre_answer: 检索长期记忆...
命中规则：【auto_ios_nav_001】导航栏必须配置 scrollEdgeAppearance
行动：自动应用该规则
```

**AI 回答后：**
```
post_answer: 执行 iOS 自检...
检查项：导航栏过渡闪烁、scrollEdgeAppearance 未处理
结果：✓ 已处理
```

---

### 示例 2: 循环引用问题

**用户代码：**
```swift
// ❌ 错误示例
self.completionHandler = {
    self.updateUI()  // 循环引用
}
```

**AI 自检：**
```
post_answer: 执行 iOS 自检...
检查项：内存泄漏、循环引用
问题：[weak self] 缺失
生成草案：
【规则 ID】auto_ios_memory_001
【场景】闭包内存管理
【问题/模式】闭包内使用 self 未加 [weak self]
【建议规则】闭包内使用 self 必须添加 [weak self] 或 [unowned self]
【依据】可验证硬错误
【可信度】低
【建议层级】长期
【领域】iOS/内存管理
```

---

### 示例 3: 审核规范问题

**用户提问：**
```
App 被拒了，原因是隐私权限描述不清晰
```

**AI 自检：**
```
post_answer: 执行 iOS 自检...
检查项：苹果审核规范、隐私权限缺失
问题：Info.plist 隐私描述不规范
生成草案：
【规则 ID】auto_ios_review_001
【场景】App Store 审核
【问题/模式】隐私权限描述不清晰导致被拒
【建议规则】所有隐私权限必须在 Info.plist 中提供清晰的使用场景描述
【依据】用户明确指出的错误
【可信度】高
【建议层级】长期
【领域】iOS/审核规范
```

---

## 🔧 脚本命令

### 初始化

```bash
./scripts/ios-self-improve.sh init
```

### iOS 专属自检

```bash
./scripts/ios-self-improve.sh self-check "代码内容"
```

### 加载 iOS 规则

```bash
./scripts/ios-self-improve.sh load-rules "当前场景"
```

### 生成 iOS 规则草案

```bash
./scripts/ios-self-improve.sh propose "内容" "场景" "领域"
```

---

## 📖 更多文档

- [docs/ios-rules.md](docs/ios-rules.md) - 15 条内置领域规则详解
- [docs/self-check-guide.md](docs/self-check-guide.md) - iOS 专属自检逻辑详解
- [docs/best-practices.md](docs/best-practices.md) - iOS 开发最佳实践

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**作者：** lijiujiu  
**许可证：** MIT

---

## 📄 许可证

MIT License

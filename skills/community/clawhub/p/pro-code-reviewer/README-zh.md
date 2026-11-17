# code-reviewer 中文说明

> AI 驱动的代码审查工具，按 P0/P1/P2 三级严重度分类，自动识别项目平台并应用专项规则。

---

## 这个工具解决什么问题

代码审查是保证质量的关键环节，但实际项目中面临两个痛点：
- **人工审查覆盖率不足**：PR 多、reviewer 时间有限，容易漏审
- **经验不均**：新人不熟悉 Android 线程模型、生命周期等坑，老问题反复出现

本工具承担"初审"职责，覆盖常见的、规则化的问题，把人工 reviewer 的精力留给架构设计和业务逻辑。

---

## 使用示例

```
> review

✅ 发现 2 个问题

P0 🔴 在 Activity 中使用 GlobalScope 启动协程（无生命周期绑定）
   src/MainActivity.kt:42
   → 改用 lifecycleScope.launch，Activity 销毁时自动取消

P1 🟡 RecyclerView Adapter 未使用 DiffUtil
   src/adapter/UserAdapter.kt:15
   → 用 DiffUtil 替代 notifyDataSetChanged()，避免全量刷新
```

---

## 工作流程

```
1. Detect（识别平台）
   根据项目文件自动判断：
   build.gradle / AndroidManifest.xml → Android
   *.xcodeproj / Podfile / Package.swift → iOS
   其他 → 通用规则

2. Diff（提取变更）
   通过 git diff 获取变更内容
   支持：未提交变更 / 已暂存 / 指定提交 / 分支对比

3. Review（执行审查）
   AI 按平台专项规则逐维度审查
   Android/iOS：9 个维度，通用：7 个维度

4. Report（输出报告）
   结构化结果：严重度 + 文件位置 + 修复建议
   可选生成 HTML 报告
```

---

## 三种审查模式

| 模式 | 命令 | 适用场景 |
|------|------|---------|
| **标准审查** | `review` | 完整审查，输出 P0/P1/P2 全部问题 |
| **快速审查** | `quick review` | 只看 P0，快速判断"能不能合并" |
| **安全审查** | `security review` | 重点检查敏感数据处理、注入风险、密钥泄露 |

---

## 严重度说明

| 级别 | 含义 | 典型例子 |
|------|------|---------|
| **P0** 🔴 | 必须修复 | 崩溃、数据丢失、安全漏洞、死锁 |
| **P1** 🟡 | 应当修复 | 竞态条件、资源泄漏、未处理的错误路径 |
| **P2** 🔵 | 建议改进 | 命名不规范、结构冗余、轻微代码味道 |

---

## 审查维度详细说明

### Android（9 个维度）

自动识别条件：项目包含 `build.gradle*` 或 `AndroidManifest.xml`

| 维度 | 检查内容 |
|------|---------|
| **线程安全** | 主线程网络/IO 操作、SharedPreferences/Room/文件 IO 是否在 IO 线程 |
| **死锁与卡顿** | 锁嵌套、主线程 `runBlocking`、`synchronized` 范围过大 |
| **内存管理** | Activity/Context 泄漏、Handler 内部类持有外部引用、Bitmap 未回收 |
| **生命周期安全** | `onStop` 后访问 View、ViewModel 持有 View 引用、LiveData 跨线程问题 |
| **逻辑正确性** | 整数溢出、浮点比较、集合并发修改 |
| **异常处理** | 吞掉异常、过宽的 catch 范围、finally 中抛异常 |
| **数据一致性** | 事务原子性、缓存与 DB 同步、SSE/Flow 中的状态竞争 |
| **API 兼容性** | `Build.VERSION.SDK_INT` 检查缺失、废弃 API 使用 |
| **架构合规** | ViewModel 直接操作 View、Repository 混入 UI 逻辑、模块间非法依赖 |

### iOS（9 个维度）

自动识别条件：项目包含 `*.xcodeproj`、`Podfile` 或 `Package.swift`

| 维度 | 检查内容 |
|------|---------|
| **线程安全** | 非主线程更新 UI、共享状态数据竞争 |
| **死锁与卡顿** | GCD 死锁、主队列同步调用、主线程阻塞 |
| **内存安全** | 闭包捕获循环引用、unowned vs weak 误用、delegate 强引用 |
| **资源泄漏** | 文件句柄未关闭、NotificationCenter 观察者未移除、Timer 未 invalidate |
| **逻辑正确性** | 强制解包崩溃、数组越界、Optional 链式调用错误 |
| **异常处理** | Result 类型未处理、缺少 do-catch、try? 静默失败 |
| **数据一致性** | CoreData 上下文线程、UserDefaults 竞争、Combine 状态 |
| **API 兼容性** | `@available` 检查缺失、废弃 API 使用 |
| **架构合规** | ViewController 包含业务逻辑、循环依赖、MVVM/VIPER 层级混乱 |

### 通用（7 个维度）

适用于非 Android/iOS 项目

| 维度 | 检查内容 |
|------|---------|
| **正确性** | 逻辑错误、越界、运算符优先级 |
| **线程安全** | 共享可变状态、缺少同步 |
| **内存** | 泄漏、无界增长、缺少清理 |
| **性能** | N+1 查询、不必要的内存分配、阻塞调用 |
| **API 设计** | 契约不清晰、缺少 null 检查、错误类型设计差 |
| **错误处理** | 未处理的错误路径、静默失败 |
| **安全** | 硬编码密钥、注入风险、不安全存储 |

---

## 快速开始

### 安装

```bash
# OpenClaw 一键安装
clawhub install code-reviewer

# Claude Code — 复制到项目
cp -r code-reviewer/ your-project/.claude/skills/

# GitHub Copilot — 复制到项目
cp -r code-reviewer/ your-project/.agents/skills/
```

### 使用命令

```
review                    # 所有未提交变更
review staged             # 仅已暂存的变更
review abc1234            # 指定某次提交
review last 5 commits     # 最近 5 次提交
review branch feature-x   # 分支与 main 的对比
```

---

## 智能行为

- **重复问题合并**：同一类问题出现在 3 个以上文件 → 合并为一条，标注"还有 N 处"，避免报告被刷屏
- **API 变更追踪**：函数签名改了？自动检查所有调用方是否同步更新
- **测试覆盖提示**：变更了代码但测试没有更新 → 温和提示
- **大 diff 保护**：变更超过 5000 行 → 提前提示再确认
- **自动过滤**：跳过生成文件、二进制文件、lock 文件、vendor 目录



---

## 项目结构

```
code-reviewer/
├── SKILL.md                    # AI Agent 指令文件
└── references/
    ├── review-general.md       # 通用审查规则
    ├── review-android.md       # Android 专项规则（9 个维度）
    ├── review-ios.md           # iOS 专项规则（9 个维度）
    ├── review-typescript.md    # TypeScript 专项规则（7 个维度）
    ├── review-go.md            # Go 专项规则（7 个维度）
    └── review-skill-vetter.md  # Agent/Skill 安全审查规则
```

---

## 环境要求

- Git 仓库
- 一个支持 Agent Skill 的 AI 编程助手（OpenClaw、Claude Code、GitHub Copilot 等）

---

## 设计思路

**为什么规则写在 Markdown 文件而不是硬编码进 Prompt？**

规则文件可以独立维护和迭代。发现新的常见问题时，直接更新对应的 `review-android.md` 即可，不需要改代码。团队可以根据自己的编码规范定制规则，比如增加"禁止使用 GlobalScope"或者"必须使用公司内部的网络库"等项目专属约束。

**为什么要区分 P0/P1/P2 而不是只输出所有问题？**

实际经验：工具输出一长串问题时，reviewer 往往从上到下看，把精力花在不紧要的命名问题上，反而忽略了真正会引发崩溃的线程问题。分级让人先处理最重要的事。

---

## 反馈

发现 bug 或有新语言需求？
[提交 Issue →](https://github.com/TimeAground/code-reviewer/issues)

## 许可证

MIT © Lin Li 2026

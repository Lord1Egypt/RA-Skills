# Android (Kotlin/Java) 审查维度

按以下 9 个维度逐一审查，每个维度独立分析。对每个疑似问题，通过多种方法（阅读上下文、搜索调用方、追踪数据流）反复验证后再确认。

## 1. 线程安全与并发

- 共享可变状态是否有正确的同步保护（`synchronized`、`ReentrantLock`、`@Volatile`、`AtomicXxx`）
- 协程中访问的共享状态是否使用了正确的 Dispatcher 和 `Mutex`/`StateFlow`
- `Handler`/`Looper` 使用是否正确，是否可能在错误线程回调
- `LiveData.postValue` 连续调用是否会丢值（仅保留最后一次）
- `ConcurrentModificationException`：迭代集合时是否可能被其他线程修改
- `suspend` 函数中的共享状态访问是否在同一个 `CoroutineContext` 中

## 2. 死锁、卡顿与性能

- **主线程卡顿**：主线程上执行数据库操作、文件 I/O、网络请求、大量计算
- **同步死锁**：嵌套 `synchronized`（A->B->A）、`runBlocking` 在主线程
- **协程死锁**：在 `Dispatchers.Main` 上调用 `runBlocking`；协程 A 等待 B 完成，B 又等待 A
- **RecyclerView 性能**：`onBindViewHolder` 中执行耗时操作、未复用 ViewHolder、频繁 `notifyDataSetChanged` 而非 DiffUtil
- **过度绘制/布局层级**：嵌套过深的 View 层级、不必要的背景绘制
- **大对象频繁创建**：循环内反复创建 SimpleDateFormat、正则 Pattern、Gson 实例
- **无节制的集合增长**：List/Map 只添加不清理，随时间无限增长
- **Bitmap 未及时回收**：大图加载未压缩、未使用 `inSampleSize`

## 3. 内存管理

- **Activity/Fragment 泄漏**：匿名内部类/非静态内部类隐式持有外部类引用
- **Handler 泄漏**：非静态 Handler 持有 Activity 引用，消息队列中的 Message 延迟释放
- **协程泄漏**：协程未绑定 `lifecycleScope`/`viewModelScope`，Activity 销毁后仍在执行
- **Context 泄漏**：单例/静态变量持有 Activity Context（应使用 Application Context）
- **注册未反注册**：BroadcastReceiver、ContentObserver、Listener 注册后未在 `onDestroy` 中反注册
- **Cursor/Stream 未关闭**：数据库 Cursor、InputStream/OutputStream 未在 finally 中关闭
- **WebView 泄漏**：WebView 未在 `onDestroy` 中调用 `destroy()`

## 4. 生命周期安全

- Fragment/Activity 销毁后是否仍访问 View（`getView()` 返回 null）
- `onActivityResult`/回调中是否检查了 `isAdded()`/`isFinishing()`
- `ViewModel` 中是否引用了 View/Activity（应通过 LiveData/StateFlow 通信）
- `DialogFragment.show()` 在 `onSaveInstanceState` 后调用导致 crash
- `FragmentTransaction.commit()` vs `commitAllowingStateLoss()` 的使用场景
- `LaunchedEffect`/`DisposableEffect`（Compose）的清理逻辑是否完整

## 5. 逻辑正确性

- 条件判断的边界值是否正确（off-by-one、空值、零值）
- Kotlin null safety：`!!` 强制解包是否安全、`?.let` 链中是否有竞态
- 新增代码对已有流程的影响面（调用方是否需要适配）
- 异步操作的时序是否有保证（先后顺序、回调是否可能不触发）
- 错误处理路径是否完整（每个分支都有合理出口）
- `when` 表达式是否覆盖所有情况（sealed class 是否有遗漏分支）

## 6. 异常处理与回调完整性

- **协程异常**：`launch` 中未捕获的异常会 crash，`async` 的 `await` 未包裹 try-catch
- **回调遗漏**：所有执行路径是否都触发了回调/LiveData 更新，避免 UI 永远 loading
- `try-catch` 是否吞掉了不应忽略的异常（catch 后无日志、直接 return）
- `CoroutineExceptionHandler` 是否正确配置
- 网络请求超时/失败路径是否有降级策略
- `Result`/`sealed class` 错误类型是否在所有消费处都处理

## 7. 数据一致性

- 多数据源（数据库 + 网络 + 缓存）是否可能出现不一致
- `SharedPreferences.apply()` 的异步写入是否会导致读取到旧值
- Room 数据库事务是否正确使用 `@Transaction`
- `StateFlow`/`LiveData` 的值更新是否原子（多个相关字段分别更新可能导致中间状态）
- 状态机是否存在非法跳转（跳过中间状态、重复进入终态）

## 8. API 兼容性

- 公开 API 签名变更是否破坏已有调用方
- `@JvmOverloads`/`@JvmStatic` 等注解变更是否影响 Java 互操作
- `data class` 添加新字段是否影响 `copy()`/`equals()`/序列化
- ProGuard/R8 混淆规则是否覆盖新增的反射/序列化类
- `minSdk` 兼容性：使用的 API 是否在所有支持版本上可用
- Intent/Bundle 传递的 key 重命名是否影响其他组件

## 9. 架构设计

- 圈复杂度是否过高（深层嵌套、过长方法）
- 是否存在重复代码可提取公共方法
- 类/模块间的依赖关系是否合理（避免循环依赖）
- ViewModel/Repository/UseCase 职责是否清晰
- 新增 API 的命名和参数设计是否符合现有约定
- 是否违反了单向数据流原则（View 直接修改 Model）

**过度工程化红线（以下情况不要提出建议）：**
- 三行以内的相似代码不算"重复"
- 仅被调用一次的代码不需要提取方法
- 现有代码不在本次变更范围内，不提优化建议（除非变更直接引入了问题）
- 不要建议为假想的未来需求做扩展性设计
- 不要要求给未变更的代码加注释、文档或类型标注
- 不要建议为一次性操作创建工具类/抽象层

---

## 报告格式

```markdown
# Code Review Report

> **分支**: xxx
> **Review 范围**: commit_id..HEAD (N commits)
> **变更文件**: N 个

## 概述
[一段话总结本次变更的目的和整体质量评价]

## 问题清单

### [P0] 必须修复
> P0 = 会导致 crash / 数据错误 / 安全漏洞 / 死锁

#### 1. [问题标题]
- **文件**: `path/to/File.kt:行号`
- **维度**: 线程安全 / 内存管理 / 生命周期安全 / ...
- **问题描述**: [具体问题]
- **风险**: [会导致什么后果]
- **修复建议**: [具体修复方式]

### [P1] 建议修复
> P1 = 潜在风险 / 边界 case 未处理

### [P2] 架构优化建议
> P2 = 代码质量 / 可维护性改进

## 总结

| 维度 | P0 | P1 | P2 |
|------|----|----|-----|
| 线程安全与并发 | 0 | 0 | 0 |
| 死锁与卡顿 | 0 | 0 | 0 |
| 内存管理 | 0 | 0 | 0 |
| 生命周期安全 | 0 | 0 | 0 |
| 逻辑正确性 | 0 | 0 | 0 |
| 异常处理/回调完整性 | 0 | 0 | 0 |
| 数据一致性 | 0 | 0 | 0 |
| API 兼容性 | 0 | 0 | 0 |
| 架构设计 | - | 0 | 0 |

[最终结论：是否可以合入，或需要修复后再 review]
```

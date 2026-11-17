# Go 审查维度

检测到 `.go` 文件变更时加载。按以下 7 个维度逐一审查，每个维度独立分析。对每个疑似问题，通过阅读上下文和追踪数据流反复验证后再确认。

---

## 1. Goroutine 与并发安全

> **P0 频发地带** — Go 并发模型独特且容易误用

- **Goroutine 泄漏**：goroutine 是否可能持续阻塞无法退出？channel 无消费者时 goroutine 会永久阻塞。用 `select` + context cancel 或 `ticker.Stop` 确保退出路径
- **无限制 goroutine 创建**：`go func()` 在循环中是否可能创建不可控数量的 goroutine？应使用 worker pool（`errgroup` / `conc.WaitGroup`）限制并发
- **WaitGroup 误用**：`Add()` 是否在 `go` 调用后执行而不是在前？`Done()` 是否在所有 goroutine 分支都被调用（包括 error return 路径）？
- **`select{}` 空选**：空的 `select{}` 会永久阻塞，通常意味着死锁
- **`sync.Mutex` 未解锁**：Lock/Unlock 是否成对出现？`defer mu.Unlock()` 应在 Lock 后立即写，而不是在函数末尾
- **`sync.RWMutex` 写锁中调用读锁方法**：同一 goroutine 中写锁未释放时调用了需要读锁的函数 → 死锁（读写锁不可重入）
- **`atomic` vs `mutex` 选用**：计数器类操作是否误用了 `sync.Mutex` 而非 `atomic.Int64`？

## 2. Channel 与数据流动

- **channel 死锁**：向一个没有接收者的 channel 发送 → 永久阻塞。所有 send 路径是否有对应的 receive 路径？
- **channel close 约定**：**只在发送方 close channel**。接收方 close 会导致其他接收方的 panic。close 后的 channel 是否被再次写入？
- **nil channel 阻塞**：向 `nil channel` 发送或从 `nil channel` 接收都会永久阻塞。未被初始化的 channel 变量是否可能在 select 中造成问题？
- **close 后仍接收**：已 close 的 channel 读取不会阻塞但返回零值。接收方是否检查了 `ok`（`val, ok := <-ch`）？
- **`for range ch` 的关闭条件**：range 遍历 channel 是否会在发送方不再发送时正常退出？发送方是否确保 close？

## 3. 错误处理

- **错误被静默丢弃**：`err` 被赋值后未检查（`result, _ := foo()` 或 `if result, err := foo(); err != nil { ... }` 的外层缺少 else 分支）
- **错误未 wrap**：`return err` 应改为 `return fmt.Errorf("context: %w", err)`，除非是 `io.EOF` 等可预期的 sentinel error
- **sentinel error 的 `==` 比较**：用 `errors.Is(err, sentinelErr)` 而非 `err == sentinelErr`（后者不处理 wrap 链）
- **`errors.As` 与类型断言**：检查 error chain 中特定 error 类型时是否使用了 `errors.As` 而非类型断言？
- **`_` 忽略检查**：是否有重要的 error return 被赋值给 `_` 丢弃？尤其是 `io.Copy`、`db.Query`、`json.Decode`
- **`defer` 中 error 处理**：`defer file.Close()` 忽略了返回的 error。严谨做法是记录 defer 中的错误
- **`panic` 在库代码中**：库代码中是否使用 `panic` 而非返回 error？第三方库接收方无法 recover

## 4. 内存与 nil 安全

- **nil map 写入**：向未初始化 map（`var m map[string]int`）写入 → panic。初始化用 `make(map[string]int)` 或 map literal
- **nil slice 的 append**：虽然安全（append 返回新 slice），但 `json.Marshal(nilSlice)` 输出 `null` 而非 `[]`，可能造成 API 契约不匹配
- **nil interface 的坑**：`var v *MyStruct = nil; var i interface{} = v; i == nil` 是 **false**——interface 的 type 信息非 nil
- **闭包捕获循环变量**：`for i := range slice { go func() { fmt.Println(i) }() }` 在 Go 1.22 前捕获的是同一个变量。当前 Go 版本是否 < 1.22？
- **指针逃逸分析**：热路径中返回局部变量的指针（`return &LocalStruct{}`）阻止了栈分配，可能增加 GC 压力
- **大值逃逸**：`var buf [64 * 1024]byte` 在函数中作为局部变量 → 超过栈帧大小逃逸到堆

## 5. 接口与类型

- **空 interface 滥用**：`interface{}` / `any` 是否被用作类型安全的逃生口？应优先使用泛型或具体类型
- **类型断言未 check**：`val := x.(string)` 如果 x 非 string 会 panic。应改为 `val, ok := x.(string); if !ok { ... }`
- **interface 污染**：一个接口只有一个实现且不会被 mock 替代 → 不需要接口（YAGNI）
- **结构体嵌入（embedding）副作用**：匿名嵌入是否暴露了不应暴露的 method set？`type MyWriter struct { *bytes.Buffer }` 公开了 `Buffer` 的全部方法
- **命名返回参数与裸 return**：`func f() (x int) { x = 5; return }` 提升了代码阅读成本，尽量避免
- **defer 中修改返回值**：named return 配合 defer 可能产生非预期的行为

## 6. 性能与资源

- **`defer` 在热路径中**：循环内 `defer` 会在函数返回时才执行，而非循环结束。热路径中的资源清理应使用手动 Close
- **字符串拼接**：循环中 `str += part` 产生大量中间字符串分配。使用 `strings.Builder` 或 `bytes.Buffer`
- **`fmt.Sprintf` 频率过高**：格式化字符串在热点中比简单拼接慢一两个数量级
- **IO 未设置缓冲**：频繁的小写入未通过 `bufio` 包装会消耗大量 syscall
- **goroutine 未设 timeout**：`http.Get`、`db.Query` 等默认无超时，可能导致 goroutine 泄漏
- **`sync.Pool` 的 Reset 缺失**：从 Pool 获取的对象是否在归还前 reset 了状态？
- **无界 slice/growth**：只用 append 不控制大小的 slice 会无限增长 → OOM

## 7. 惯用法与编码规范

- **`context` 未正确传递**：第一个参数应该是 `context.Context`，且仅通过参数传递（不存 struct 中除非框架约束）
- **`init()` 滥用**：`init()` 是否在执行副作用？测试环境中的 `init()` 状态是全局且不可控的
- **全局变量**：`var` 在包级别是否不可变？可变全局变量破坏并发安全，且测试难以隔离
- **`time.After` 泄漏**：`select` 中 `time.After` 在结束时不会释放定时器资源。使用 `time.NewTimer` 并 `Stop()`
- **`json.RawMessage` vs `interface{}`**：JSON 反序列化中是否使用 `json.RawMessage` 延迟解码而非丢失类型的 `interface{}`？
- **`_` 导入副作用**：`import _ "pkg"` 是否有清楚的注释说明为什么需要 init 副作用？
- **gofmt 一致性**：变更的代码是否遵守 gofmt 格式？(非 P0，但应建议统一风格)

---

## 报告格式

遵循 SKILL.md 中定义的标准输出格式。维度字段使用 Go 对应的标识。

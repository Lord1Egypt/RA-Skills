# C++20 协程开发避坑指南

写 C++20 协程库时高频踩到的坑。每条都有「症状 → 原因 → 解法」。

## 坑 1：lambda 捕获引用做协程体 → -O3 下悬空指针

### 症状
```cpp
auto g = [&capture]() -> Task<int> { co_return capture; }();
g.blocking_get();  // -O0 正常，-O3 返回随机值
```

### 原因
协程帧在堆上长期存活，但 lambda 闭包对象在调用表达式结束后销毁，留下 dangling references。

### 解法
- 用自由函数 / 成员函数
- **按值捕获也不能修复临时协程 lambda**：协程仍通过闭包对象访问 capture，闭包销毁后同样悬空；必须让闭包活到协程完成。
- 优先无捕获 lambda 或自由函数，通过值参数把状态存入协程帧：`[](Capture c) -> Task<int> { ... }(capture)`。引用参数要求被引用对象活到协程结束。

## 坑 2：catch 块里不能 `co_await`

### 症状
```cpp
catch (std::exception& e) {
    co_await schedule_on(ui);  // ❌ 编译错误
    show_error(e.what());
}
```

### 原因
C++20 标准规定 catch handler 内部不允许 await。

### 解法
用 `exception_ptr` 把异常带出 try，try 外面 await + 重抛：
```cpp
std::exception_ptr ex;
try { co_await body(); } catch (...) { ex = std::current_exception(); }
co_await schedule_on(ui);
if (ex) std::rethrow_exception(ex);
```

可以封装成 helper：
```cpp
template<typename Body, typename OnError>
Task<void> on_ui_safe(IExecutor& ui, Body body, OnError on_error) {
    std::exception_ptr ex;
    try { co_await body(); } catch (...) { ex = std::current_exception(); }
    co_await schedule_on(ui);
    if (ex) try { std::rethrow_exception(ex); } catch (const std::exception& e) { on_error(e); }
}
```

## 坑 3：在 mutex 内 resume 协程 → recursive lock crash

### 症状
```cpp
{
    std::lock_guard lk(mu);
    waiter.resume();  // 💥 "mutex lock failed: Invalid argument"
}
```

### 原因
`resume()` 同步执行 coroutine continuation，continuation 可能再调用同一个对象的方法（再次试锁），非递归 mutex 立即 abort。

### 解法
**所有 `handle.resume()` 必须在 lock 外**：
```cpp
std::coroutine_handle<> wake;
{
    std::lock_guard lk(mu);
    if (!waiters_.empty()) { wake = waiters_.front(); waiters_.pop_front(); }
}
if (wake) wake.resume();   // ← 出锁
```

## 坑 4：detached 协程不自动 destroy → 内存泄漏

### 症状
```cpp
void Task::start_detached() && {
    handle_.resume();
    handle_ = {};   // 失去 handle，never destroyed
}
```

### 解法：wrapper coroutine 在 final_suspend 自杀
```cpp
struct DetachedPromise {
    DetachedTask get_return_object();
    suspend_never initial_suspend() noexcept { return {}; }
    struct FinalAwaiter {
        bool await_ready() const noexcept { return false; }
        void await_suspend(coroutine_handle<DetachedPromise> me) noexcept { me.destroy(); }
        void await_resume() const noexcept {}
    };
    FinalAwaiter final_suspend() noexcept { return {}; }
    void return_void() noexcept {}
    void unhandled_exception() noexcept {}
};
auto wrapper = [](handle_type h) -> DetachedTask {
    try { co_await Task<T>{h}; } catch (...) {}
}(h);
```

## 坑 5：`final_suspend` 的 `await_suspend` 模板化才能跨派生类

### 症状
```cpp
struct PromiseBase { /* final_suspend has await_suspend(coroutine_handle<PromiseBase>) */ };
struct Promise : PromiseBase { /* ... */ };
// Compiler error: cannot convert coroutine_handle<Promise> to coroutine_handle<PromiseBase>
```

### 解法
模板化 `await_suspend`：
```cpp
template<typename P>
coroutine_handle<> await_suspend(coroutine_handle<P> h) noexcept {
    PromiseBase& base = h.promise();   // upcast OK
    return base.continuation ? base.continuation : noop_coroutine();
}
```

## 坑 6：`blocking_get()` 不能跑真正异步的 Task

### 症状
```cpp
auto t = []() -> Task<int> {
    co_await schedule_on(pool);   // 真异步
    co_return 42;
}();
t.blocking_get();  // ❌ throws "Task: did not complete synchronously"
```

### 原因
`blocking_get` 只 resume 一次，遇到真异步 suspend 就放弃。它只适合纯同步协程（即只 `co_return`）。

### 解法
- 测试场景：用 `start_detached()` + `atomic<bool> done` + 自旋等
- 真应用：用 Dispatcher 的 main loop pump
- 真要 `blocking_get`：传一个会同步完成的 InlineExecutor

## 坑 7：Generator/Task 不能用 `for_co_await` 风格混用

### 症状
Generator 是拉式（同步迭代），Task 是推式（co_await）。`co_await Generator{}` 不工作。

### 解法
- Generator 用 `for (auto x : gen)` 同步遍历
- 异步流要用 `Channel<T>` 或自定义 stream awaitable

## 坑 8：driver/orchestrator 协程"自己 resume 自己之前还活着但用着的内存"

### 症状
when_all/when_any 之类组合子，最后一个 driver 完成 → resume 父协程 → 父协程 await_resume 返回 → 父继续执行 → 销毁 awaiter → drivers 容器析构 → drivers 各自 Task 析构 → handle.destroy() —— **但 driver 协程自己还在 stack 上往回跑** → UAF。

ASan 会报：`heap-use-after-free in drive_one (.resume)`。表现为偶发 SIGTRAP/SIGABRT。

### 解法
不要通过永久泄漏 shared_ptr 或容器修复生命周期：这会一起保留 Task 及协程帧，掩盖 UAF 而引入泄漏。

可选方案：driver 进入 final_suspend 后以 symmetric transfer 恢复父协程；或用有明确定义自销毁边界的 detached driver 配合独立共享结果状态；或将父协程恢复排队到 driver 已返回之后。每种方案都必须确保最后一次使用 driver/awaiter 结束后才销毁，并验证取消、异常和早退出路径。ASan 与泄漏检测共同验收。

## TaskScope 验收补充（C++23）

- join返回lazy Task时，封口应发生在join调用处；不然调用join后又spawn可悄悄改变等待集合。重复join、未消费join和销毁等待中的join需明确契约。
- 最后一个子任务应在其帧及参数释放后才通知join；不能只等body co_return。用weak_ptr参数存活测试确认，连续spawn同步子任务确认已完成帧不累积。
- request_stop会同步调用stop_callback，回调可使最后子任务完成、join父任务恢复并销毁scope。先复制stop_source局部保stop状态存活，回调后不再访问this。
- 测试不仅“子失败”和“取消”分开测，还要测“子失败→stop回调完成兄弟→父join接异常→销毁scope”的完整重入路径。
- queued yield是挂起操作而非可随意丢弃的post回调。可复用已到期timer队列跟踪，在loop shutdown恢复，避免scope永远join不了；这不等于自动取消用户循环。
- fail-fast析构契约可用独立子进程set_terminate到指定退出码，并由CMake execute_process精确断言退出码；不能仅WILL_FAIL把任何崩溃都算成功。

## 事件循环关闭与重入（C++20/23共通）

- `CancelIoEx`只是请求取消；必须等实际完成包出队后才能释放OVERLAPPED和用户buffer，不能取消后立即free，也不能超时后无条件free。
- socket.close可能同步恢复等待协程。先用exchange把wrapper标为closed、保存本地handle/loop，再detach，后续不访问this；回调可以再次close甚至销毁wrapper。
- `unique_ptr<Impl>`析构会先使拥有者内指针失效（具体实现顺序不可假设）。如果Impl析构恢复协程，协程回到EventLoop调用detach可能访问空指针。先在EventLoop析构体显式调用幂等shutdown（impl_仍有效），再析构Impl；move赋值替换旧Impl也同理。
- 关闭期间拒绝新I/O/timer/yield提交；真实loopback测试同时覆盖pending accept/read、重入close、回调销毁owner、loop析构并验证只完成一次。
- 闭合这些路径不等于任意挂起Task可销毁。结构化任务所有权、独立取消token与deadline仍需单独设计验收。

## 异步 TLS 集成验收补充

- OpenSSL便利宏可能展开C风格强转，GCC的`-Wold-style-cast -Werror`会在调用处报错，即使同一代码Clang通过。例：`SSL_set_tlsext_host_name`在OpenSSL3.0展开为`SSL_ctrl`及`(void*)`；按该版本宏定义调用等价`SSL_ctrl(..., const_cast<char*>(name.c_str()))`，不要全局关闭警告。验证必须包含真实GCC/OpenSSL组合。

- OpenSSL 的 `SSL_get_error` 依赖当前线程错误队列：SSL 调用前清空队列，紧接调用立即分类，二者之间不执行其他 OpenSSL API 或 `co_await`。不要跨挂起点读取线程错误状态。
- 用有界 memory BIO pair 将 TLS 状态机与异步传输解耦；`WANT_READ`/`WANT_WRITE` 先排出待发密文，再补输入或重试，保留短写剩余字节，零进度写必须报错避免死循环。不能把 socket BIO 的 readiness 模型直接套到 IOCP。
- 证书验证失败也可能产生待发送 alert；允许仅 drain 已排队密文，不再驱动失败 SSL 会话。保留原始TLS错误；后续应用I/O必须拒绝。
- EOF 必须区分已收到 `close_notify` 与裸 TCP 断开（截断）；单向shutdown仅表示本方通知已发送，不代表对端已确认。
- 泛型TLS流不拥有底层transport时，stream/transport/span须活到所有操作结束；operation guard不能替代底层任务取消注册。禁止销毁仍被loop/kernel引用的帧与buffer。
- 验收至少包含真实loopback HTTPS、独立CA/主机名/IP负测、短密文读写、大载荷、close_notify与截断、重叠操作拒绝、C++20/23+ASan/UBSan。桌面运行、移动端交叉编译与真机运行分别报告。
- CMake `find_package(OpenSSL)`导入目标受目录作用域约束：测试应从定义导入目标的模块目录 `add_subdirectory(tests)`，不要在根目录作为旁系引入后依赖不可见目标。构建产物仅放项目根build下，各代理使用独占构建目录。

## 总结表

| 坑 | 一句话防御 |
|----|-----------|
| 1 | lambda 协程绝不按引用捕获 |
| 2 | exception_ptr 把异常带出 try |
| 3 | resume 必须在 mutex 外 |
| 4 | detached 必须有自销毁 wrapper |
| 5 | final_suspend 用模板化 await_suspend |
| 6 | blocking_get 只对纯同步 Task 安全 |
| 7 | Generator 同步遍历，异步用 Channel |
| 8 | 组合子 driver 容器要 outlive 自己 resume 的父 |
| 9 | `co_await Task{handle}` 的临时 Task 析构会 destroy 正在跑的 handle，必须 move 出来 |
| 10 | 派生类成员先于基类析构 — VM 析构 hook 里 cancel 时，scope 用 shared_ptr 持有，别用裸指针 |
| 11 | 把 span 交给对方后不能立刻回收底层容器 — 用「延迟消费」，所有权交还前不动容器 |

## 坑 9：`co_await Task<T>{h}` 临时 Task UAF

### 症状
detached wrapper 包了一层 `co_await Task<T>{orig}`，挂起后崩溃；ASan 报 use-after-free。

### 原因
临时 `Task<T>{orig}` 的生命周期到完整表达式结束。但 Awaiter 只是把 handle 拷了一份，临时 Task 析构时 `~Task()` 会 `handle.destroy()` —— 而协程此时正在 running，UAF。

### 解法
`operator co_await() &&` 实现里把 handle **move** 出来：

```cpp
auto operator co_await() && noexcept {
    struct Awaiter {
        handle_type h;
        ~Awaiter() { if (h) h.destroy(); }   // 接管销毁权
        // ... move-only ...
    };
    return Awaiter{std::exchange(handle_, {})};   // 临时不再持有
}
```

## 坑 10：派生类成员先析构 — VM 析构 hook 别用裸指针

### 症状
`vm.install_destroy_hook_([s = scope_.get()](){ s->cancel(); })` 在 VM 析构时崩溃。

### 原因
VM 析构顺序：派生类成员 → 派生类 dtor → 基类 dtor。基类 dtor 才触发 hook，此时派生类成员（包括持有 scope 的 `ViewModelScope`）已经销毁。裸指针悬空。

### 解法
用 `shared_ptr` 持有，hook 闭包里 capture by value：

```cpp
ViewModelScope() : scope_(std::make_shared<CoroutineScope>()) {}
void attach(ViewModel& vm) {
    auto keep = scope_;   // shared ownership
    vm.install_destroy_hook_([keep]() noexcept { keep->cancel(); });
}
```

## 坑 11：把 span 交给调用方后立刻回收容器 → ASan container-overflow

异步数据流（解析器 / 流式读写）的高频坑，普通构建和 -O0 都不报，只有 ASan 抓得到。

### 症状
```
AddressSanitizer: container-overflow on address 0x...
READ of size 11 at ... thread T0
    #0 memcpy
    #1 std::string::append(char const*, unsigned long)
```
注意是 **container-overflow** 而不是 heap-use-after-free：内存还在（capacity 内），
但容器的 `size()` 已经缩小，span 落到了 size 之外。

### 原因
典型模式：把内部缓冲的一段以 `span` 交给调用方，然后立刻把这段从缓冲里"消费"掉：

```cpp
auto slice = buffer.readable().first(n);
out_ = slice;            // 交给调用方
buffer.consume(n);       // ← 内部可能 vector::clear()，size 归零
return Step::data;       // 调用方随后读 out_ → 越界
```

`consume`/`erase`/`clear`/`resize` 任何缩小 `size()` 的操作都会让先前发出的 span 失效，
即使内存地址还有效、即使数据没被覆盖。ASan 的容器标注（container annotation）
就是为了抓这种"在 size 外、capacity 内"的读。

### 解法：延迟消费（deferred consume）
数据的字节留在容器里，**等下一次调用开始时再回收**，让 span 的有效期和文档承诺一致：

```cpp
Result<Step> parse(Buffer& input) {
    if (pending_consume_ > 0) {       // 上一轮交出去的字节，现在才回收
        input.consume(pending_consume_);
        pending_consume_ = 0;
    }
    ...
    out_ = input.readable().first(n);
    pending_consume_ = n;             // 只记账，不动容器
    return Step::data;
}
```

配套要在 API 文档里写清两件事：
1. span 的有效期 = 到下一次调用为止；
2. 调用方必须一直调到 `complete`，否则最后一批字节不会被回收
   （pipelining 场景下会串到下一个消息）。

### 同类变体
- `std::vector::push_back` 触发重分配 → 之前的 span/iterator 全失效（这个更常见，
  但通常会被 heap-use-after-free 抓到，症状更明显）。
- 协程里 `co_await` 前取的 span，await 期间对方修改了容器 → 恢复后 span 已失效。
  异步场景下"取 span"和"用 span"之间隔着一次挂起，风险比同步代码高得多。

### 教训
**ASan 要常态跑在 CI 里**，而且要跑 `detect_container_overflow`（默认开）。
这个坑在 C++20/C++23 普通构建下 100% 静默通过，只有 sanitizer 能发现。

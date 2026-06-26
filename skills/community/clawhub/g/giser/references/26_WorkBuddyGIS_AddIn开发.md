# WorkBuddyGIS AddIn 开发经验 | 关联：12_ArcGIS_Pro.md, 29_避坑库110+.md | 来源：WorkBuddyGIS项目实战总结（附录B B.10.8~B.10.13）

> ArcGIS Pro AddIn 插件开发实战经验。完整记录了从命令绑定诊断、子进程桥接风险、异步调试黑洞、WPF环境差异、编译部署 SOP、端到端诊断清单、调试与性能优化、到常见错误代码速查的全流程。
>
> 本文档基于 WorkBuddyGIS 项目反向验证报告全面扩充，是 ArcGIS Pro AddIn 开发的**一站式避坑手册**。

---

## B.10.8 命令绑定链路深度诊断

### B.10.8.1 完整的 XAML 绑定检查清单（5步逐项验证）

当按钮点击无响应时，按以下5步逐项排查：

| 步骤 | 检查项 | 验证方法 | 通过标准 |
|------|--------|----------|----------|
| **S1** | XAML Command 绑定语法 | 检查 `Command="{Binding SendCommand}"` 拼写与大小写 | 编译无 XAML 绑定警告 |
| **S2** | DataContext 是否正确设置 | 查看 DockPane 的 `InitializeAsync` 中是否设置 `DataContext = new WorkBuddyViewModel()` | ViewModel 属性可通过断点访问 |
| **S3** | 命令属性是否公开 | 确认 `public ICommand SendCommand { get; }` 为 public 非 private | IntelliSense 可列出该属性 |
| **S4** | CanExecute 是否返回 true | 在 CanExecute lambda 加 `MessageBox.Show($"CanExecute={result}")` | 点击按钮前弹窗显示 true |
| **S5** | Execute 方法是否被调用 | 在 Execute lambda 第一行加 `MessageBox.Show("Execute triggered")` | 点击按钮弹窗出现 |

### B.10.8.2 RelayCommand vs DelegateCommand 区别与选择

| 维度 | `RelayCommand`（自定义） | `DelegateCommand`（Pro SDK） |
|------|-------------------------|------------------------------|
| **来源** | 自行实现或 MVVM 框架提供 | `ArcGIS.Desktop.Core` 命名空间 |
| **CanExecute 刷新** | 依赖 `CommandManager.RequerySuggested`（Pro 中可能不触发） | Pro 宿主自动处理刷新 |
| **线程安全** | 需自行实现 `CanExecuteChanged.Invoke` 的线程调度 | SDK 内部已处理 Dispatcher 调度 |
| **推荐场景** | 标准 WPF 应用、快速原型 | **ArcGIS Pro AddIn 正式开发（首选）** |

**选择建议**：在 ArcGIS Pro AddIn 中，**始终优先使用 `DelegateCommand`**。如果使用 `RelayCommand`，必须在属性变更时手动调用 `CommandManager.InvalidateRequerySuggested()`。

### B.10.8.3 CanExecute 手动刷新机制详解

当 ViewModel 中的 `IsBusy` 或 `CanSend` 等属性变化后，命令的 `CanExecute` 不会自动重新评估（Pro WPF 环境中尤其如此）。

```csharp
// 方案1：手动触发全局命令刷新
private bool _isBusy;
public bool IsBusy
{
    get => _isBusy;
    set
    {
        if (_isBusy != value)
        {
            _isBusy = value;
            OnPropertyChanged(nameof(IsBusy));
            // 关键：手动通知命令系统重新评估 CanExecute
            CommandManager.InvalidateRequerySuggested();
        }
    }
}

// 方案2：使用 DelegateCommand + RaiseCanExecuteChanged（推荐）
public DelegateCommand SendCommand { get; }

public WorkBuddyViewModel()
{
    SendCommand = new DelegateCommand(async () => await SendAsync(), () => !IsBusy);
}

private bool _isBusy;
public bool IsBusy
{
    get => _isBusy;
    set
    {
        _isBusy = value;
        OnPropertyChanged(nameof(IsBusy));
        SendCommand.RaiseCanExecuteChanged(); // 精确刷新
    }
}
```

### B.10.8.4 诊断日志分层方案（UI层 → ViewModel层 → Model层 → API层）

| 层级 | 日志位置 | 日志方式 | 示例 |
|------|----------|----------|------|
| **UI层** | XAML 绑定事件 | `MessageBox.Show` 或 Debug 输出 | `MessageBox.Show("Button Clicked")` |
| **ViewModel层** | 命令Execute/属性Setter | 写文件到 `%TEMP%\wb_diag.log` | `File.AppendAllText(logPath, $"[VM] SendCommand triggered\n")` |
| **Model层** | 业务逻辑方法 | 同上，带时间戳 | `File.AppendAllText(logPath, $"[Model] {DateTime.Now:T} API call start\n")` |
| **API层** | HTTP请求/响应 | HttpClient 日志 Handler | `Debug.WriteLine($"[API] Response: {response.StatusCode}")` |

```csharp
// 统一日志工具类
public static class AddInLogger
{
    private static readonly string LogPath = Path.Combine(
        Path.GetTempPath(), "wb_addin_diag.log");

    public static void Log(string layer, string message)
    {
        var line = $"[{DateTime.Now:HH:mm:ss.fff}][{layer}] {message}";
        System.Diagnostics.Debug.WriteLine(line);
        File.AppendAllText(LogPath, line + Environment.NewLine);
    }
}

// 使用示例
AddInLogger.Log("VM", "SendCommand Execute started");
```

### B.10.8.5 常见绑定失败原因速查表

| 序号 | 症状 | 根因 | 解决方案 |
|------|------|------|----------|
| 1 | 按钮灰色不可点击 | CanExecute 始终返回 false | 检查 CanExecute lambda 逻辑 |
| 2 | 点击无反应无日志 | DataContext 为 null | 检查 DockPane 初始化是否设置 DataContext |
| 3 | 编译无警告但运行无绑定 | XAML 中 Binding 路径错误 | 检查属性名大小写，用 Snoop 验证 |
| 4 | CanExecute 在标准 WPF 正常但 Pro 中不触发 | Pro 的 CommandManager 未正确刷新 | 手动调用 `InvalidateRequerySuggested()` |
| 5 | ViewModel 构造函数未执行 | Pro 静默吞掉构造异常 | 加 try-catch + MessageBox 输出异常 |
| 6 | 绑定编译通过但运行时 DataContext 是旧实例 | DockPane 被多次创建但 ViewModel 未更新 | 确保单例模式或正确绑定生命周期 |
| 7 | 属性变更后 UI 不刷新 | 未实现 INotifyPropertyChanged | ViewModel 继承 `ObservableObject`（Pro SDK） |
| 8 | 命令绑定在调试环境正常但发布版失败 | Release 编译优化裁剪绑定 | 检查 XAML 绑定为 `Mode=OneWay` 非 `OneTime` |

---

## B.10.9 子进程桥接架构详解

### B.10.9.1 为什么 ArcGIS Pro 环境子进程失败率高（环境隔离深度分析）

| 隔离维度 | 详细说明 |
|----------|----------|
| **环境变量污染** | ArcGIS Pro 进程携带 `ACC_PRODUCT_CONFIG_V3`（278KB JSON）等巨型环境变量，传递给子进程后超出 Windows 环境块 64KB 限制，导致 `CreateProcess` 失败 |
| **PATH 冲突** | Pro 内置 Python（`arcgispro-py3`）与系统 Python 路径冲突，`Process.Start("python", ...)` 可能调用错误的解释器 |
| **工作目录差异** | Pro 的工作目录是安装目录（如 `C:\Program Files\ArcGIS\Pro`），而非用户期望的项目目录 |
| **stdout/stderr 死锁** | 同步读取 stdout + stderr 时，缓冲区满导致子进程挂起（经典 .NET Process 死锁问题） |
| **权限沙箱** | Pro 以当前用户权限运行，某些系统级路径可能无写入权限 |
| **conda 环境干扰** | Pro 使用 conda 管理 Python 包，子进程可能继承错误的 conda 激活状态 |

### B.10.9.2 替代方案矩阵

| 方案 | 复杂度 | 性能 | 可靠性 | 适用场景 |
|------|--------|------|--------|----------|
| **HTTP 直连** | 低 | 高 | 高 | **首选**：调用 REST API（Ollama、WorkBuddy、自定义服务） |
| **文件 IPC** | 低 | 中 | 中 | 简单数据交换、离线场景、跨语言通信 |
| **命名管道** | 中 | 高 | 高 | 需要双向实时通信的本地服务 |
| **WCF/gRPC** | 高 | 高 | 高 | 企业级服务、需要强类型契约 |

### B.10.9.3 HTTP 直连完整实现代码

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

public class ApiService
{
    private static readonly HttpClient _client = new HttpClient
    {
        Timeout = TimeSpan.FromSeconds(120)
    };

    /// <summary>
    /// 异步调用 Ollama API（ArcGIS Pro AddIn 推荐方式）
    /// </summary>
    public static async Task<string> QueryOllamaAsync(string prompt, string model = "llama3")
    {
        var requestBody = new
        {
            model = model,
            prompt = prompt,
            stream = false
        };

        var json = JsonSerializer.Serialize(requestBody);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        try
        {
            var response = await _client.PostAsync("http://localhost:11434/api/generate", content);
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadAsStringAsync();
            var doc = JsonDocument.Parse(result);
            return doc.RootElement.GetProperty("response").GetString();
        }
        catch (HttpRequestException ex)
        {
            AddInLogger.Log("API", $"HTTP error: {ex.Message}");
            throw;
        }
        catch (TaskCanceledException)
        {
            AddInLogger.Log("API", "Request timed out (120s)");
            throw new TimeoutException("API 请求超时");
        }
    }
}
```

### B.10.9.4 文件 IPC 实现方案（轮询 + 回调）

```csharp
public class FileIpcBridge : IDisposable
{
    private readonly string _requestDir;
    private readonly string _responseDir;
    private readonly FileSystemWatcher _watcher;
    private readonly Dictionary<string, TaskCompletionSource<string>> _pending
        = new Dictionary<string, TaskCompletionSource<string>>();

    public FileIpcBridge(string baseDir)
    {
        _requestDir = Path.Combine(baseDir, "requests");
        _responseDir = Path.Combine(baseDir, "responses");
        Directory.CreateDirectory(_requestDir);
        Directory.CreateDirectory(_responseDir);

        // 监听响应目录
        _watcher = new FileSystemWatcher(_responseDir, "*.resp")
        {
            EnableRaisingEvents = true
        };
        _watcher.Created += OnResponseFileCreated;
    }

    public async Task<string> SendAsync(string command)
    {
        var id = Guid.NewGuid().ToString("N");
        var requestFile = Path.Combine(_requestDir, $"{id}.req");
        var tcs = new TaskCompletionSource<string>();
        _pending[id] = tcs;

        File.WriteAllText(requestFile, command);

        // 等待响应（带超时）
        var completed = await Task.WhenAny(tcs.Task, Task.Delay(30000));
        _pending.Remove(id);
        File.Delete(requestFile);

        if (completed != tcs.Task)
            throw new TimeoutException("文件 IPC 等待响应超时");

        return await tcs.Task;
    }

    private void OnResponseFileCreated(object sender, FileSystemEventArgs e)
    {
        var id = Path.GetFileNameWithoutExtension(e.Name);
        if (_pending.TryGetValue(id, out var tcs))
        {
            try
            {
                var response = File.ReadAllText(e.FullPath);
                tcs.SetResult(response);
            }
            catch (Exception ex)
            {
                tcs.SetException(ex);
            }
        }
    }

    public void Dispose()
    {
        _watcher.Dispose();
    }
}
```

### B.10.9.5 架构迁移 Checklist

| 步骤 | 检查项 | 完成标准 |
|------|--------|----------|
| 1 | 移除所有 `Process.Start` 调用 | 全局搜索无结果 |
| 2 | 确认外部服务提供 HTTP 接口 | 可用 curl/浏览器访问 `http://localhost:port/api` |
| 3 | 替换为 `HttpClient` 调用 | 编译通过，运行时 HTTP 200 |
| 4 | 添加超时与重试机制 | 网络异常时 UI 不卡死 |
| 5 | 添加请求/响应日志 | `%TEMP%\wb_addin_diag.log` 可追踪每次调用 |
| 6 | 测试 Pro 中的线程模型兼容性 | 异步调用不阻塞 UI 线程 |

---

## B.10.10 fire-and-forget 异步诊断详解

### B.10.10.1 Task 异常捕获的 5 种模式

| 模式 | 代码示例 | 优点 | 缺点 |
|------|----------|------|------|
| **1. ContinueWith** | `task.ContinueWith(t => { if(t.IsFaulted) Log(t.Exception); })` | 不改变调用链结构 | 回调不回到原上下文，易丢失异常 |
| **2. await + try-catch** | `try { await OpAsync(); } catch (Exception ex) { Log(ex); }` | 最清晰、最推荐 | 需要将调用者改为 async 方法 |
| **3. async void + try-catch** | `async void Handle() { try { await OpAsync(); } catch { Log(); } }` | 可用于事件处理器 | 异常无法被调用方捕获 |
| **4. Observe exception** | `var ex = task.Exception; if(ex != null) Log(ex);` | 简单直接 | 需要持有 Task 引用 |
| **5. 全局兜底** | `TaskScheduler.UnobservedTaskException += ...` | 兜底所有遗漏的异常 | 仅用于最后防线，不替代局部处理 |

### B.10.10.2 ArcGIS Pro 的 SynchronizationContext 注意事项

```
⚠️ ArcGIS Pro 运行在自定义的 WPF SynchronizationContext 上。
- await 默认会回到 Pro 的 UI 线程（Dispatcher 线程）
- 如果 UI 线程被阻塞（如模态对话框），await 后的代码将延迟执行
- Task.Run 中的代码运行在 MTA 线程池，不持有 SynchronizationContext
- ConfigureAwait(false) 可避免回 UI 线程，但更新 UI 属性时必须手动 Dispatcher.Invoke
```

```csharp
// 错误：在后台线程直接更新 UI 属性（抛异常）
Task.Run(async () =>
{
    await Task.Delay(1000);
    StatusText = "Done"; // ❌ 非UI线程，InvalidOperationException
});

// 正确：回到UI线程更新
Task.Run(async () =>
{
    await Task.Delay(1000);
    await QueuedTask.Run(() =>
    {
        StatusText = "Done"; // ✅ Pro SDK 的 QueuedTask 处理线程调度
    });
});

// 或者使用 ConfigureAwait + 手动调度
var result = await SomeApiAsync().ConfigureAwait(false);
Application.Current.Dispatcher.Invoke(() =>
{
    StatusText = result; // ✅ 手动调度回 UI 线程
});
```

### B.10.10.3 Complete Exception Handling Wrapper Class

```csharp
/// <summary>
/// 通用异步异常处理包装器 —— 杜绝 fire-and-forget 黑洞
/// </summary>
public static class SafeAsync
{
    /// <summary>
    /// 安全执行异步操作，自动捕获并记录所有异常
    /// </summary>
    public static async Task Run(
        Func<Task> asyncAction,
        string context = "Unknown",
        Action<Exception> onError = null)
    {
        try
        {
            await asyncAction();
        }
        catch (OperationCanceledException)
        {
            AddInLogger.Log("SafeAsync", $"[{context}] Cancelled");
        }
        catch (Exception ex)
        {
            AddInLogger.Log("SafeAsync", $"[{context}] ERROR: {ex.GetType().Name}: {ex.Message}");
            onError?.Invoke(ex);
        }
    }

    /// <summary>
    /// 安全执行异步操作并返回结果
    /// </summary>
    public static async Task<T> Run<T>(
        Func<Task<T>> asyncFunc,
        T fallback = default,
        string context = "Unknown")
    {
        try
        {
            return await asyncFunc();
        }
        catch (Exception ex)
        {
            AddInLogger.Log("SafeAsync", $"[{context}] ERROR: {ex.Message}");
            return fallback;
        }
    }
}

// 使用示例 —— 替代危险的 _ = SomeAsync()
SafeAsync.Run(async () =>
{
    var result = await ApiService.QueryOllamaAsync(prompt);
    ResponseText = result;
}, "QueryOllama");
```

### B.10.10.4 异步诊断工具方法

```csharp
/// <summary>
/// 异步任务生命周期追踪器 —— 用于诊断 fire-and-forget 场景
/// </summary>
public static class TaskTracker
{
    private static readonly ConcurrentDictionary<int, TaskInfo> _tasks
        = new ConcurrentDictionary<int, TaskInfo>();

    public static Task Track(Task task, string name)
    {
        var id = task.Id;
        _tasks[id] = new TaskInfo(name, DateTime.Now);

        task.ContinueWith(t =>
        {
            if (_tasks.TryGetValue(id, out var info))
            {
                var elapsed = DateTime.Now - info.StartTime;
                if (t.IsFaulted)
                    AddInLogger.Log("Track", $"[{name}] FAULTED after {elapsed.TotalMs:F0}ms: {t.Exception?.Flatten().InnerExceptions[0].Message}");
                else if (t.IsCanceled)
                    AddInLogger.Log("Track", $"[{name}] CANCELLED after {elapsed.TotalMs:F0}ms");
                else
                    AddInLogger.Log("Track", $"[{name}] Completed OK in {elapsed.TotalMs:F0}ms");
                _tasks.TryRemove(id, out _);
            }
        });

        return task;
    }

    private class TaskInfo
    {
        public string Name { get; }
        public DateTime StartTime { get; }
        public TaskInfo(string name, DateTime start) => (Name, StartTime) = (name, start);
    }
}

// 使用
TaskTracker.Track(ApiService.QueryOllamaAsync(prompt), "OllamaQuery");
```

---

## B.10.11 WPF 环境差异详解

### B.10.11.1 ArcGIS Pro WPF vs 标准 WPF 差异对照表

| 维度 | 标准 WPF | ArcGIS Pro WPF | 影响 |
|------|----------|----------------|------|
| **宿主进程** | 独立 exe | `ArcGISPro.exe` | 权限、环境变量、PATH 均不同 |
| **资源字典** | `App.xaml` 合并 | Pro 已预加载大量资源 | 样式可能被覆盖或冲突 |
| **主题** | 自定义 Themes | Pro 内置暗色/亮色主题切换 | AddIn 需要适配两种主题 |
| **命令刷新** | `CommandManager.RequerySuggested` 自动触发 | Pro 宿主可能不传播该事件 | CanExecute 不自动刷新 |
| **Dispatcher** | 标准 WPF Dispatcher | Pro 的 Dispatcher 可能被框架操作占用 | UI 更新延迟 |
| **线程模型** | STA（UI线程） | STA + `QueuedTask`（Pro自有调度器） | 后台操作必须用 QueuedTask |

### B.10.11.2 CommandManager.RequerySuggested 在 Pro 中的行为

```
问题现象：
- 标准 WPF 应用：点击按钮后 CanExecute 自动重新评估
- ArcGIS Pro：CanExecute 不自动重新评估，按钮状态卡死

根因：
Pro 的 WPF 宿主可能拦截或延迟 CommandManager 的事件传播。

解决方案优先级：
1. 使用 Pro SDK 的 DelegateCommand + RaiseCanExecuteChanged（首选）
2. 属性变更时手动调用 CommandManager.InvalidateRequerySuggested()
3. 按钮显式绑定 IsEnabled="{Binding CanSend}" 绕过 CanExecute 机制
```

### B.10.11.3 Dispatcher 优先级差异

| 优先级 | 枚举值 | 用途 | Pro 中注意事项 |
|--------|--------|------|----------------|
| `Normal` | 9 | 一般 UI 更新 | Pro 的框架操作也使用此优先级，可能排队延迟 |
| `Send` | 10 | 最高优先级 | 仅用于紧急操作，避免滥用 |
| `Background` | 6 | 后台操作 | Pro 中行为与标准 WPF 一致 |
| `ApplicationIdle` | 2 | 空闲时执行 | 在 Pro 中 UI 空闲时间极短，几乎不触发 |
| `ContextIdle` | 3 | 上下文空闲 | 同上 |

```csharp
// Pro 推荐方式：使用 QueuedTask 替代 Dispatcher
await QueuedTask.Run(() =>
{
    // 此处运行在 Pro 的后台线程，不阻塞 UI
    var map = MapView.Active.Map;
    // 执行地图操作...
});

// 如果需要更新 UI 属性
await QueuedTask.Run(() =>
{
    var result = HeavyComputation();
    // 使用 QueuedTask 的回调回到 UI 线程
}).ContinueWith(t =>
{
    Application.Current.Dispatcher.Invoke(() =>
    {
        StatusText = t.Result;
    });
}, TaskScheduler.FromCurrentSynchronizationContext());
```

### B.10.11.4 线程模型差异（STA vs MTA）

```
ArcGIS Pro 线程模型规则：
┌─────────────────────────────────────────────────────┐
│  UI 线程（STA）                                      │
│  - XAML 绑定、属性变更、MessageBox                    │
│  - 禁止在此线程执行耗时操作                           │
├─────────────────────────────────────────────────────┤
│  QueuedTask 线程（Pro 专用后台线程）                  │
│  - 地图操作、图层操作、地理处理                       │
│  - Pro SDK 的地图 API 必须在此线程调用                │
├─────────────────────────────────────────────────────┤
│  线程池（MTA）                                       │
│  - HTTP 调用、文件IO、纯计算                          │
│  - 禁止在此线程直接调用 Pro SDK 地图 API              │
└─────────────────────────────────────────────────────┘
```

### B.10.11.5 调试技巧（Snoop / WPF Inspector）

| 工具 | 功能 | Pro AddIn 使用注意事项 |
|------|------|------------------------|
| **Snoop** | 实时查看 WPF Visual Tree、绑定信息、属性值 | 需要 Pro 以管理员权限启动才能附加 |
| **WPF Inspector** | 类似 Snoop，开源替代 | 可能与 Pro 的 Window 样式冲突 |
| **VS 输出窗口** | 绑定错误输出到 Output | 在 VS → 输出 → 显示输出来源选择"调试" |
| **XAML 绑定诊断** | 编译时绑定检查 | csproj 中添加 `<PresentationTraceSources>` 启用详细追踪 |

```xml
<!-- App.xaml 或 DockPane.xaml 中启用绑定诊断 -->
<Window xmlns:diag="clr-namespace:System.Diagnostics;assembly=WindowsBase"
        diag:PresentationTraceSources.TraceLevel="High">
```

---

## B.10.12 编译部署完整 SOP

### B.10.12.1 环境变量问题详解（MSB4175 根因 + 永久修复方案）

**根因分析**：
```
MSB4175 错误完整调用链：
1. ArcGIS Pro 启动时加载 ACC_PRODUCT_CONFIG_V3 环境变量（~278KB JSON）
2. 开发者在 Pro 进程内启动 Visual Studio（或 VS 继承了 Pro 的环境）
3. MSBuild 继承当前进程的所有环境变量
4. CreateProcess 传递环境块时，Windows 限制为 64KB
5. 超出限制导致 CodeTaskFactory 加载失败 → MSB4175
```

**永久修复方案**：
```batch
:: 方案1：编译前临时清除（推荐，保留到 build.bat 中）
set ACC_PRODUCT_CONFIG_V3=

:: 方案2：在系统环境变量中删除（影响所有新进程）
:: 注意：重启 ArcGIS Pro 后该变量会重新创建
:: 仅在开发期间删除，不影响 Pro 正常运行

:: 方案3：使用独立命令行窗口编译（避免继承 Pro 环境）
:: 从开始菜单直接打开"Developer Command Prompt for VS 2022"
:: 而非从 Pro 内部启动 VS
```

### B.10.12.2 build.bat 完整脚本

```batch
@echo off
:: ============================================================
:: WorkBuddyGIS AddIn 编译部署脚本
:: 用法：build.bat [Debug|Release] [build|deploy|both]
:: 默认：build.bat Debug build
:: ============================================================

setlocal enabledelayedexpansion

set CONFIG=%1
if "%CONFIG%"=="" set CONFIG=Debug
set ACTION=%2
if "%ACTION%"=="" set ACTION=build

:: 解决 MSB4175：清除巨型环境变量
echo [1/4] Clearing oversized env vars...
set ACC_PRODUCT_CONFIG_V3=
set ACC_PRODUCT_CONFIG_V2=

:: MSBuild 路径
set MSBUILD="C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe"
if not exist %MSBUILD% (
    echo ERROR: MSBuild not found. Update path in build.bat
    exit /b 1
)

:: 项目路径
set PROJECT="D:\WORK_\tools\workbuddy_addin\WorkBuddyGIS.csproj"
set OUTPUT="D:\WORK_\tools\workbuddy_addin\bin\%CONFIG%\WorkBuddyGIS.esriAddinX"
set DEPLOY="${USERPROFILE}\Documents\ArcGIS\AddIns\ArcGISPro\WorkBuddyGIS.esriAddinX"

if "%ACTION%"=="build" goto :build
if "%ACTION%"=="deploy" goto :deploy
if "%ACTION%"=="both" goto :build

:build
echo [2/4] Building %CONFIG% configuration...
%MSBUILD% %PROJECT% /t:Build /p:Configuration=%CONFIG% /v:minimal
if %ERRORLEVEL% neq 0 (
    echo ERROR: Build failed with code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
echo     Build successful: %OUTPUT%

if "%ACTION%"=="build" goto :end

:deploy
echo [3/4] Deploying to ArcGIS Pro AddIns folder...
if not exist "%OUTPUT%" (
    echo ERROR: Output file not found: %OUTPUT%
    exit /b 1
)
copy /Y "%OUTPUT%" "%DEPLOY%"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Deploy failed
    exit /b %ERRORLEVEL%
)
echo     Deployed to: %DEPLOY%

:end
echo [4/4] Done.
echo.
echo IMPORTANT: Restart ArcGIS Pro to load the updated AddIn.
endlocal
```

### B.10.12.3 调试部署 vs 发布部署 区别

| 维度 | 调试部署（Debug） | 发布部署（Release） |
|------|-------------------|---------------------|
| **配置** | `/p:Configuration=Debug` | `/p:Configuration=Release` |
| **输出** | `.esriAddinX`（未压缩文件夹） | `.esriAddIn`（压缩 ZIP 包） |
| **符号** | 包含 PDB 调试符号 | 不包含 PDB |
| **优化** | 无编译优化，便于断点调试 | 编译优化，性能更好 |
| **部署方式** | 复制文件夹到 AddIns 目录 | 双击 .esriAddIn 安装或从 Add-In Manager 安装 |
| **调试方式** | VS 附加到 ArcGISPro.exe 进程 | 需单独部署 PDB 或远程调试 |

### B.10.12.4 版本管理策略

```
推荐版本号规则：Major.Minor.Patch
- Major：重大架构变更（如从 .NET 6 升级到 .NET 8）
- Minor：新增功能（如新增地图导出按钮）
- Patch：Bug 修复（如修复 CanExecute 不刷新）

版本号位置：WorkBuddyGIS.csproj 中的 <Version> 节点
每次发布前必须递增，避免 ArcGIS Pro 缓存旧版本。
```

### B.10.12.5 常见编译错误速查（10+条）

| 序号 | 错误代码/信息 | 原因 | 解决方案 |
|------|---------------|------|----------|
| 1 | **MSB4175** CodeTaskFactory 无法加载 | 环境块超过 64KB | `set ACC_PRODUCT_CONFIG_V3=` |
| 2 | **MSB4018** 未知的任务 "XamlPreCompile" | Pro SDK 版本与 MSBuild 不匹配 | 使用 MSBuild 而非 dotnet build |
| 3 | **CS0103** "QueuedTask" 不存在 | 缺少 Pro SDK 引用 | 确保 `ArcGIS.Desktop.Core` 被引用 |
| 4 | **XAML erro** 无法解析类型 "DockPane" | XAML 命名空间缺失 | 添加 `xmlns:extensions="clr-namespace:ArcGIS.Desktop.Extensions;assembly=ArcGIS.Desktop.Extensions"` |
| 5 | **CS0246** DelegateCommand 未找到 | 缺少 using 指令 | `using ArcGIS.Desktop.Core;` |
| 6 | 编译通过但 Pro 不加载 AddIn | Config.daml 配置错误 | 检查 id、class 是否与代码匹配 |
| 7 | **NU1605** 包降级警告 | NuGet 版本冲突 | 检查 Pro SDK 版本一致性 |
| 8 | **MC3074** XAML 绑定类型不匹配 | 绑定表达式类型错误 | 用 Snoop 检查实际类型 |
| 9 | 生成 .esriAddIn 为空包 | csproj 缺少 AddIn 目标 | 确保 `<Import Project="ArcGIS Pro AddIn.targets">` 存在 |
| 10 | **MSB3491** 无法复制文件，被占用 | ArcGIS Pro 正在使用旧版本 AddIn | 关闭 Pro 后重新编译部署 |
| 11 | 运行时 MissingMethodException | .NET 版本不匹配 | 确认 TargetFramework 与 Pro SDK 兼容 |
| 12 | **CS0118** "module" 是关键字 | 配置文件名包含保留字 | 重命名文件或用 @ 前缀 |

---

## B.10.13 端到端诊断清单升级

### B.10.13.1 完整分层诊断清单

| 层级 | 检查项 | 诊断方法 | 通过标准 |
|------|--------|----------|----------|
| **L1 - XAML** | Command 绑定语法正确 | 检查 XAML 的 `Command="{Binding ...}"` | 编译无警告，Snoop 显示绑定正常 |
| **L1 - XAML** | DataContext 已设置 | Snoop 查看根元素 DataContext | 非 null，类型匹配 ViewModel |
| **L2 - ViewModel** | ViewModel 已实例化 | 构造函数加 MessageBox | 启动后弹窗确认 |
| **L2 - ViewModel** | 命令属性存在且 public | 断点或 Snoop | Snoop 命令列可见 |
| **L2 - ViewModel** | CanExecute 返回 true | MessageBox 输出 | 按钮可点击 |
| **L3 - 业务逻辑** | Execute 方法被调用 | 方法第一行加日志 | 日志文件有记录 |
| **L3 - 业务逻辑** | 异步操作无 fire-and-forget | 检查所有 `_ = ` 和无 await 的调用 | 代码审查通过 |
| **L4 - API/网络** | HTTP 请求发出 | 抓包或 API 日志 | Fiddler/Wireshark 可见请求 |
| **L4 - API/网络** | 响应正确解析 | 日志记录 response.StatusCode | 状态码 200 且 body 正确 |
| **L5 - DockPane** | DockPane 正确注册 | Config.daml 检查 | Add-In Manager 中可见 |
| **L5 - DockPane** | DockPane 正确显示 | Pro 界面检查 | 面板可见，UI 元素完整 |

### B.10.13.2 DockPane 生命周期诊断

```
DockPane 生命周期：
  Module.Initialize()          → 模块初始化（仅一次）
    ↓
  DockPane.Activate()          → 面板被用户激活
    ↓
  DockPaneViewModel.OnShow()   → 面板可见
    ↓
  (用户交互...)
    ↓
  DockPaneViewModel.OnHide()   → 面板被隐藏
    ↓
  DockPane.Deactivate()        → 面板关闭
    ↓
  Module.Dispose()             → 模块销毁（Pro 退出时）
```

| 诊断点 | 检查方法 | 常见问题 |
|--------|----------|----------|
| Initialize 是否调用 | 在 Module.Initialize 加 MessageBox | Config.daml 中 module id 不匹配 |
| ViewModel 实例是否唯一 | 检查构造函数调用次数 | 多次激活导致多个实例 |
| OnHide/OnShow 是否触发 | 加日志记录 | Pro 切换视图时状态丢失 |
| Dispose 是否清理资源 | 断点检查 | 事件订阅未取消导致泄漏 |

### B.10.13.3 Config.daml 验证清单

```xml
<!-- Config.daml 关键验证点 -->
<insertModule id="WorkBuddyGIS_Module" className="WorkBuddyGIS.WorkBuddyGISModule"
              caption="WorkBuddyGIS" autoInsert="true">
  <!-- 1. id 必须与 Module 类的 [ModuleAttribute("id")] 一致 -->
  <!-- 2. className 必须包含完整命名空间 -->

  <groups>
    <group id="WorkBuddyGIS_Group" caption="WorkBuddyGIS Group"
           appearsOnAddInTab="true">
      <!-- 3. group id 在全 AddIn 中唯一 -->
    </group>
  </groups>

  <controls>
    <button id="WorkBuddyGIS_WorkBuddyDockPane_ShowButton"
            caption="WorkBuddyGIS"
            className="WorkBuddyGIS.WorkBuddyDockPane_ShowButton"
            smallImage="Images\GenericButtonBlue16.png"
            largeImage="Images\GenericButtonBlue32.png">
      <!-- 4. button id 与 ShowButton 类的 ButtonAttribute("id") 一致 -->
      <!-- 5. className 完整命名空间 -->
      <!-- 6. 图片路径相对于项目根目录 -->
      <tooltip heading="WorkBuddyGIS">Open WorkBuddyGIS Panel.</tooltip>
    </button>
  </controls>

  <dockPanes>
    <dockPane id="WorkBuddyGIS_WorkBuddyDockPane"
              caption="WorkBuddyGIS"
              className="WorkBuddyGIS.WorkBuddyDockPaneViewModel"
              dockWith="esri_core_contentsDockPane"
              defaultTab="esri_core_mapTab">
      <!-- 7. dockPane id 与 DockPaneAttribute("id") 一致 -->
      <!-- 8. className 完整命名空间 -->
      <!-- 9. dockWith 指定停靠位置 -->
    </dockPane>
  </dockPanes>
</insertModule>
```

### B.10.13.4 事件订阅泄漏检查

```csharp
// ❌ 常见泄漏模式
public class WorkBuddyDockPaneViewModel : DockPane
{
    public WorkBuddyDockPaneViewModel()
    {
        // 全局事件订阅 —— ViewModel 被多次创建时重复订阅
        MapView.Active.MapChanged += OnMapChanged; // 泄漏！
    }

    // ✅ 正确模式：实现 IDisposable，在 OnDeactivate 中取消订阅
    public void OnDeactivate(bool isRemoving)
    {
        MapView.Active.MapChanged -= OnMapChanged;
    }
}

// ✅ 使用弱事件模式避免泄漏
public class WorkBuddyDockPaneViewModel : DockPane
{
    private readonly WeakEventManager _mapChangedManager = new WeakEventManager();

    protected override void OnActivate()
    {
        _mapChangedManager.AddListener(this);
    }

    protected override void OnDeactivate(bool isRemoving)
    {
        _mapChangedManager.RemoveListener(this);
    }
}
```

### B.10.13.5 内存泄漏检查

| 检查项 | 工具/方法 | 重点关注 |
|--------|-----------|----------|
| **ViewModel 是否被 GC** | VS Diagnostic Tools（内存快照对比） | Activate 前后 ViewModel 实例数是否递增 |
| **事件订阅** | dotMemory / ANTS Memory Profiler | 查找持有 ViewModel 引用的事件源 |
| **Dispatcher 回调** | VS 并发可视化 | 长时间运行的 Dispatcher 回调 |
| **静态集合** | 搜索 `static List`/`static Dictionary` | ViewModel 被静态集合持有 |
| **Timer/Task** | 检查未 Dispose 的 Timer/Task | 后台操作完成后未释放资源 |

```csharp
// 内存泄漏诊断辅助方法
public static class MemoryDiagnostics
{
    public static void LogMemoryStats(string tag)
    {
        var proc = System.Diagnostics.Process.GetCurrentProcess();
        AddInLogger.Log("Memory",
            $"[{tag}] WorkingSet={proc.WorkingSet64 / 1024 / 1024}MB, " +
            $"GC={GC.GetTotalMemory(false) / 1024 / 1024}MB, " +
            $"Gen0={GC.CollectionCount(0)} Gen1={GC.CollectionCount(1)} Gen2={GC.CollectionCount(2)}");
    }

    // 在 DockPane OnActivate/OnDeactivate 中调用
    // 对比前后内存变化，判断是否有泄漏
}
```

---

## B.10.14 AddIn 调试与性能优化

### B.10.14.1 ArcGIS Pro 诊断模式启动方法

```
方法1：命令行启动（推荐）
"C:\Program Files\ArcGIS\Pro\ArcGISPro.exe" /weakReference

方法2：诊断日志路径
%LOCALAPPDATA%\ESRI\ArcGISPro\Logs\
- 查看最新的 ArcGISPro.log 文件
- 搜索 AddIn 加载记录："Loading add-in" + 你的 AddIn 名称

方法3：启用 .NET 附加日志
在 Pro 的 Advanced Settings 中启用：
  - Debug → Enable .NET Framework logging
  - 日志输出到：%APPDATA%\ArcGISPro\fusionlog.txt
```

### B.10.14.2 Visual Studio 附加进程调试

| 步骤 | 操作 | 注意事项 |
|------|------|----------|
| 1 | 打开 AddIn 解决方案（**非 Pro 源码**） | 确保编译 Debug 模式，包含 PDB |
| 2 | 设置断点 | 在 ViewModel 构造函数、命令 Execute 方法处设断点 |
| 3 | VS → 调试 → 附加到进程 | 选择 `ArcGISPro.exe` |
| 4 | 选择调试引擎 | 勾选 "托管（.NET）" 和 "原生" |
| 5 | 触发断点 | 在 Pro 中操作 AddIn 触发断点命中 |
| 6 | 检查变量/调用栈 | 正常调试流程 |

```
⚠️ 常见问题：
- "断点当前不会命中" → 确保 Debug 编译 + PDB 与 DLL 在同一目录
- Pro 崩溃 → 可能是调试器附加导致超时，尝试禁用 Just-In-Time 调试
- 无法附加 → 以管理员权限运行 VS
```

### B.10.14.3 性能分析工具

| 工具 | 用途 | 适用场景 |
|------|------|----------|
| **Visual Studio Profiler** | CPU/内存性能分析 | 内置，无需额外安装 |
| **dotTrace** | 函数级耗时分析 | 精确定位热点方法 |
| **ANTS Memory Profiler** | 内存泄漏检测 | 查找未释放的对象 |
| **PerfView** | ETW 级别性能追踪 | 高级 CPU/内存/GC 分析（免费） |

```csharp
// 简易性能计时器（用于快速定位瓶颈）
public sealed class PerfTimer : IDisposable
{
    private readonly string _name;
    private readonly Stopwatch _sw;

    public PerfTimer(string name)
    {
        _name = name;
        _sw = Stopwatch.StartNew();
    }

    public void Dispose()
    {
        _sw.Stop();
        AddInLogger.Log("Perf", $"[{_name}] {_sw.ElapsedMilliseconds}ms");
    }
}

// 使用示例
using (new PerfTimer("QueryOllama"))
{
    var result = await ApiService.QueryOllamaAsync(prompt);
    ResponseText = result;
}
// 日志输出：[Perf] [QueryOllama] 3245ms
```

### B.10.14.4 常见性能陷阱

| 序号 | 陷阱 | 症状 | 优化方案 |
|------|------|------|----------|
| 1 | UI 线程执行 HTTP 请求 | 点击按钮后界面冻结 | 使用 `async/await` + `QueuedTask.Run` |
| 2 | 每次操作创建新 HttpClient | 端口耗尽（Socket exhausted） | 使用静态/单例 HttpClient |
| 3 | 大量 MapView 刷新 | 地图闪烁/卡顿 | 批量更新 + 一次性 `MapView.Redraw()` |
| 4 | 频繁属性变更通知 | UI 重绘风暴 | 合并属性变更，使用 `SetProperty` 批量通知 |
| 5 | 同步文件 IO 在 UI 线程 | 界面短暂卡顿 | `await File.WriteAllTextAsync()` |
| 6 | ObservableCollection 频繁 Add | 列表闪烁 | 批量操作后一次性 Replace |
| 7 | 日志写入过于频繁 | 磁盘 IO 瓶颈 | 日志缓冲 + 定时刷新 |

---

## B.10.15 常见 ArcGIS Pro AddIn 错误代码速查

| 序号 | 错误代码/信息 | 场景 | 原因 | 解决方案 |
|------|---------------|------|------|----------|
| 1 | **MSB4175** | 编译时 | 环境块超 64KB 限制 | `set ACC_PRODUCT_CONFIG_V3=` |
| 2 | **ERR_ADDIN_LOAD_FAILED** | Pro 启动时 AddIn 未加载 | Config.daml id 与代码不一致 | 核对 module/dockPane/button id |
| 3 | **COMException 0x80040154** | Pro 加载 AddIn DLL 时 | .NET Framework 版本不匹配 | 确保 TargetFramework 与 Pro SDK 版本一致 |
| 4 | **InvalidOperationException** | QueuedTask.Run 内调用 UI API | 线程模型错误 | UI 操作回到 Dispatcher，地图操作用 QueuedTask |
| 5 | **NullReferenceException** | MapView.Active.Map 为 null | 当前没有打开地图视图 | 添加 null 检查：`if (MapView.Active == null) return;` |
| 6 | **UnauthorizedAccessException** | 写入 Pro 安装目录 | Pro 安装目录受保护 | 使用 `Path.GetTempPath()` 或用户文档目录 |
| 7 | **TypeLoadException** | 运行时找不到类型 | 缺少 Pro SDK DLL 或版本不一致 | 检查 NuGet 包版本与 Pro 版本对应 |
| 8 | **XAMLParseException** | DockPane 加载时 | XAML 语法错误或类型引用错误 | 检查 xmlns 命名空间和类型名拼写 |
| 9 | **BindingExpression path error** | 运行时 | XAML 绑定路径不存在 | 检查属性名大小写，确保 public |
| 10 | **TaskCanceledException** | HTTP 请求超时 | 网络延迟或服务未启动 | 增大 HttpClient.Timeout，检查服务状态 |
| 11 | **AggregateException** | 多 Task 并行时 | 子任务异常未被捕获 | 使用 `await Task.WhenAll()` 替代 `WaitAll()` |
| 12 | **OutOfMemoryException** | 处理大数据集 | 未分块读取大文件/图层 | 分块处理，释放不再使用的对象 |
| 13 | **SocketException** | HttpClient 请求失败 | 本地服务端口未开放 | 检查 Ollama/自定义服务是否运行 |
| 14 | **FileLoadException** | AddIn 加载 DLL 时 | DLL 版本冲突或数字签名问题 | 清理 bin/obj 目录后重新编译 |
| 15 | **MetadataException** | Entity Framework 数据库访问 | 连接字符串错误或迁移未应用 | 检查连接字符串，运行 `Update-Database` |
| 16 | **IOException 文件被占用** | 编译部署 | ArcGIS Pro 锁定了旧版 AddIn 文件 | 关闭 Pro 后重新编译部署 |
| 17 | **TargetInvocationException** | 反射调用失败 | Config.daml 中 className 拼写错误 | 仔细核对 className 完整命名空间 |
| 18 | **ArgumentException "parameter is not valid"** | CIM 符号/渲染器操作 | CIM 对象参数不完整 | 构造完整的 CIM 对象再赋值 |

---

> **V4.1 响应式优化版** | 79行 → 300+行 | 基于反向验证报告全面扩充
>
> 关联阅读：`12_ArcGIS_Pro.md`（ArcPy编程和 ArcGIS Pro 架构） | `29_避坑库110+.md`（完整避坑库）


<!-- wm:坤图_GIS:V1.0 -->

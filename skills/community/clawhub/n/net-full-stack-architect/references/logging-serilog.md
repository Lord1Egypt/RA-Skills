# Serilog 结构化日志

> net-full-stack-architect 技能参考文件。Serilog 两段式配置、Enrich、sinks、请求日志、脱敏、ELK 集成。

## 目录

1. [两段式启动配置](#1-两段式启动配置)
2. [Enrich 上下文](#2-enrich-上下文)
3. [Sinks 配置](#3-sinks-配置)
4. [请求日志](#4-请求日志)
5. [脱敏（生产必做）](#5-脱敏生产必做)
6. [ELK 集成](#6-elk-集成)
7. [使用规范](#7-使用规范)

---

## 1. 两段式启动配置

```powershell
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.File
dotnet add package Serilog.Sinks.Elasticsearch   # 按需
```

```csharp
// 第一阶段：引导日志器（配置未加载前也能记启动错误）
Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog((ctx, cfg) => cfg
        .ReadFrom.Configuration(ctx.Configuration)              // appsettings 的 Serilog 节
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.With<CorrelationIdEnricher>()
        .WriteTo.Console(outputTemplate:
            "[{Timestamp:HH:mm:ss} {Level:u3}] {CorrelationId} {Message:lj}{NewLine}{Exception}")
        .WriteTo.File("logs/log-.log",
            rollingInterval: RollingInterval.Day,
            retainedFileCountLimit: 30,
            outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level:u3}] {CorrelationId} {Message:lj}{NewLine}{Exception}")
        .WriteTo.Logger(lc => lc.Filter.ByIncludingOnly(e => e.Level >= LogEventLevel.Warning)
            .WriteTo.File("logs/errors/log-.log", rollingInterval: RollingInterval.Day)));

    var app = builder.Build();
    // ... 中间件
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "应用启动失败");
    throw;
}
finally
{
    Log.CloseAndFlush();
}
```

## 2. Enrich 上下文

```csharp
// 关联 ID：贯穿一次请求/一次任务，排障第一线索
public class CorrelationIdEnricher : ILogEventEnricher
{
    public void Enrich(LogEvent logEvent, ILogEventPropertyFactory factory)
    {
        var id = Activity.Current?.TraceId.ToString()
                 ?? Guid.NewGuid().ToString("N")[..12];
        logEvent.AddPropertyIfAbsent(factory.CreateProperty("CorrelationId", id));
    }
}
```

- 每个请求进中间件时生成/透传 `X-Correlation-Id`，压入 `LogContext.PushProperty("CorrelationId", id)`；
- 重要事件加 `TraceId/SpanId`（OpenTelemetry Activity 自动带）；
- 多租户系统把 `TenantId` 推入 LogContext，避免每条手写。

## 3. Sinks 配置

| Sink | 包 | 适用 |
|---|---|---|
| Console | Serilog.Sinks.Console（随 Serilog.AspNetCore） | 开发/容器 stdout |
| File | Serilog.Sinks.File | 单机/简单部署，按天滚动 + 保留数量 |
| Elasticsearch | Serilog.Sinks.Elasticsearch | ELK（注意 ES 8 需 DataStream/index 格式） |
| Seq | Serilog.Sinks.Seq | 小团队自托管日志门户 |

- 容器环境优先 Console + 采集端（Filebeat/Vector），不要双写；
- 文件 sink 必须设 `retainedFileCountLimit`，否则磁盘被日志打满是经典事故。

## 4. 请求日志

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.EnrichDiagnosticContext = (diag, httpContext) =>
    {
        diag.Set("RequestBody", httpContext.Items.TryGetValue("RequestBody", out var b) ? b : null);
        diag.Set("ElapsedMs", httpContext.Items["ElapsedMs"]);
    };
});
```

慢请求告警（中间件示例）：

```csharp
app.Use(async (ctx, next) =>
{
    var sw = Stopwatch.StartNew();
    ctx.Items["ElapsedMs"] = sw.ElapsedMilliseconds;
    await next();
    if (sw.ElapsedMilliseconds > 1000)
        Log.Warning("慢请求 {Method} {Path} 耗时 {Ms}ms",
            ctx.Request.Method, ctx.Request.Path, sw.ElapsedMilliseconds);
});
```

## 5. 脱敏（生产必做）

日志泄漏密码/身份证/手机号是合规事故。三层防护：

1. **Enricher 兜底**：输出前对 `手机号` `身份证` `token` 字段正则替换；
```csharp
public class SensitiveDataEnricher : ILogEventEnricher
{
    public void Enrich(LogEvent e, ILogEventPropertyFactory f)
    {
        if (e.MessageTemplate.Text.Contains("用户") && e.Properties.TryGetValue("payload", out var p))
            e.AddOrUpdateProperty(f.CreateProperty("payload", Mask(p.ToString())));
    }
}
```
2. **禁止打印**：请求/响应全量 body、SQL 参数值、JWT；
3. **代码审查项**：`Log.Information("login {@user}", user)` 这种整对象序列化最危险，DTO 脱敏模型再打。

## 6. ELK 集成

- ES 8 + `Serilog.Sinks.Elasticsearch`：`IndexFormat = "myapi-{0:yyyy.MM.dd}"` 或 DataStream（ES 8 推荐）；
- ILM 策略按日/周滚动 + 索引别名，Kibana 建 Dashboard（错误率、慢请求 Top、按 CorrelationId 下钻）；
- 采样：HealthCheck/静态资源日志在 Serilog 侧 `Filter.ByExcluding` 掉，别让噪声占满 ES。

## 7. 使用规范

- 注入 `ILogger<T>`，**禁止静态 `Log` 到处用**（库/中间件除外）；
- 消息模板用结构化占位 `Log.Information("订单 {OrderNo} 创建", no)`，**禁止字符串拼接**；
- 级别纪律：Information 记业务里程碑，Warning 记可恢复异常，Error 记失败，Fatal 只给启动失败；
- `Microsoft.*` 框架日志提升到 Warning（appsettings `MinimumLevel:Override`），否则 EF/SqlSugar SQL 刷屏。

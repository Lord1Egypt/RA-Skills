# 项目结构与脚手架

> net-full-stack-architect 技能参考文件。整洁架构四层结构、最小宿主模板、工程规范。

## 目录

1. [目录结构](#1-目录结构)
2. [依赖规则](#2-依赖规则)
3. [Program.cs 最小宿主](#3-programcs-最小宿主)
4. [工程规范文件](#4-工程规范文件)
5. [配置与 Options](#5-配置与-options)

---

## 1. 目录结构

```text
src/
├── MyApi/                        # WebApi 启动项目（控制器或 Minimal API）
│   ├── Program.cs
│   ├── appsettings.json
│   ├── Middlewares/              # 异常、请求日志、权限等自定义中间件
│   ├── Filters/                  # ActionFilter / 模型校验 Filter
│   └── Extensions/               # IServiceCollection 扩展方法
├── MyApi.Application/            # 应用层：服务接口与实现、DTO、验证器、CQRS
│   ├── Dtos/
│   ├── Interfaces/               # 服务接口（Infrastructure 实现）
│   ├── Services/
│   └── Common/                   # ApiResult、分页模型、异常类型
├── MyApi.Domain/                 # 领域层：实体、值对象、仓储接口、领域事件（零依赖）
│   ├── Entities/
│   ├── Events/
│   └── Repositories/             # 仅接口
├── MyApi.Infrastructure/         # 基础设施：SqlSugar、Redis、外部 API、消息
│   ├── Persistence/              # DbContext/SqlSugar 配置、仓储实现、种子数据
│   └── DependencyInjection.cs    # AddInfrastructure(this IServiceCollection)
└── MyApi.Contracts/              # （可选）对外契约，多服务共享
tests/
├── MyApi.Tests.Unit/             # xUnit + 领域/服务单测
├── MyApi.Tests.Integration/      # WebApplicationFactory + Testcontainers
└── MyApi.Tests.Architecture/     # 架构规则测试（依赖方向断言）
```

## 2. 依赖规则

- `Domain` 不引用任何项目；
- `Application` 只引用 `Domain`（接口在 Application 或 Domain 定义，实现放 Infrastructure）；
- `Infrastructure` 引用 `Application` + `Domain`；
- `Api` 引用 `Application`（+ 通过 `AddInfrastructure()` 组装 Infrastructure，不直接 using 其类型）；
- 用 NetArchTest 或手写反射测试在 CI 断言依赖方向，**架构规则必须有测试兜底**。

## 3. Program.cs 最小宿主

```csharp
var builder = WebApplication.CreateBuilder(args);

// ---- 配置 ----
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
    .AddEnvironmentVariables();

// ---- 服务 ----
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));
builder.Services.Configure<DbOptions>(builder.Configuration.GetSection("Db"));
builder.Services.AddInfrastructure(builder.Configuration);   // SqlSugar/Redis 等
builder.Services.AddApplication();                            // 应用层服务 + FluentValidation
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

// Swagger（控制器路线；Minimal API 路线见 api-docs-versioning.md）
builder.Services.AddSwaggerGen();

var app = builder.Build();

// ---- 中间件顺序（敏感）----
app.UseMiddleware<ExceptionMiddleware>();      // 1. 全局异常（最外层）
app.UseSerilogRequestLogging();                // 2. 请求日志
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.UseHttpsRedirection();
app.UseAuthentication();                       // 3. 认证必须在授权前
app.UseAuthorization();
app.MapControllers();

app.Run();
```

> 顺序口诀：**异常 → 日志 → 路由 → 认证 → 授权 → 端点**。UseAuthentication/UseAuthorization 写反是 401/403 错乱的最常见原因。

## 4. 工程规范文件

**Directory.Build.props**（仓库根目录，统一所有项目）：

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <LangVersion>latest</LangVersion>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <!-- 有漏洞的包直接构建失败：NU1903 高危 / NU1904 严重 -->
    <WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>
  </PropertyGroup>
  <ItemGroup>
    <!-- 文档注释不生成时抑制 1591 -->
    <NoWarn>$(NoWarn);1591</NoWarn>
  </ItemGroup>
</Project>
```

**Directory.Packages.props**（中央包管理 CPM，版本集中）：

```xml
<Project>
  <ItemGroup>
    <PackageVersion Include="SqlSugar" Version="5.1.4" />
    <PackageVersion Include="Serilog.AspNetCore" Version="9.0.0" />
    <PackageVersion Include="Swashbuckle.AspNetCore" Version="10.0.0" />
    <PackageVersion Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="10.0.0" />
  </ItemGroup>
</Project>
```

> CPM 后各项目只写 `<PackageReference Include="SqlSugar" />` 不带版本——依赖变更集中在 PR 可审查的一个文件里。配合 Package Source Mapping 防投毒。

**.editorconfig** 要点：文件 UTF-8 BOM；4 空格缩进；`csharp_style_namespace_declarations = file_scoped:warning`；私有字段 `_camelCase`；`dotnet_sort_system_directives_first = true`。

## 5. 配置与 Options

**appsettings.json**

```json
{
  "Db": {
    "DbType": "MySql",
    "ConnectionStrings": {
      "MySql": "Server=127.0.0.1;Database=myapi;Uid=root;Pwd=***;",
      "SqlServer": "Server=.;Database=myapi;Trusted_Connection=True;"
    }
  },
  "Jwt": {
    "Issuer": "myapi",
    "Audience": "myapi-client",
    "AccessExpireMinutes": 30,
    "RefreshExpireDays": 7
  },
  "Serilog": { "MinimumLevel": { "Default": "Information", "Microsoft": "Warning" } }
}
```

```csharp
// 选项类
public class DbOptions
{
    public string DbType { get; init; } = "MySql";
    public Dictionary<string, string> ConnectionStrings { get; init; } = new();
}

// 消费：构造注入 IOptions<DbOptions> / IOptionsSnapshot<T>（支持热重载）/ IOptionsMonitor<T>
public class OrderService
{
    private readonly DbOptions _db;
    public OrderService(IOptions<DbOptions> db) => _db = db.Value;
}
```

- JWT 密钥、Redis 密码等机密：开发放 user-secrets（`dotnet user-secrets`），生产放环境变量/KV，**绝不进 git**。
- 环境区分：`DOTNET_ENVIRONMENT=Development|Staging|Production`。

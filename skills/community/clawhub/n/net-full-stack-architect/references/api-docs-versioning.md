# API 文档与版本控制

> net-full-stack-architect 技能参考文件。两套路线：控制器（Asp.Versioning.Mvc + Swashbuckle）与 Minimal API（.NET 10 内置 OpenAPI + Scalar）。

## 目录

1. [版本化策略选型](#1-版本化策略选型)
2. [路线 A：控制器 API（Swashbuckle）](#2-路线-a控制器-apiswashbuckle)
3. [路线 B：Minimal API（.NET 10 内置 OpenAPI + Scalar）](#3-路线-bminimal-apinet-10-内置-openapi--scalar)
4. [XML 注释](#4-xml-注释)
5. [Swagger 授权入口](#5-swagger-授权入口)
6. [版本演进纪律](#6-版本演进纪律)

---

## 1. 版本化策略选型

| 策略 | 示例 | 评价 |
|---|---|---|
| URL 段（推荐） | `/api/v1/products` | 显式、可缓存、Swagger 友好，2026 主流默认 |
| 查询串 | `?api-version=1.0` | URL 稳定但易遗漏 |
| 请求头 | `X-Api-Version: 1.0` | 隐藏，调试不便 |
| Media Type | `Accept: application/vnd.myapi.v1+json` | 最 REST 纯正但复杂，慎用 |

**主版本号策略**：只做 v1/v2 大版本，不逐接口微版本；破坏性变更必须升版本。

## 2. 路线 A：控制器 API（Swashbuckle）

```powershell
dotnet add package Asp.Versioning.Mvc
dotnet add package Asp.Versioning.Mvc.ApiExplorer
dotnet add package Swashbuckle.AspNetCore
```

```csharp
// Program.cs
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;                       // 响应头输出 api-supported-versions
    options.ApiVersionReader = new UrlSegmentApiVersionReader();
})
.AddApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";                     // v1 / v2
    options.SubstituteApiVersionInUrl = true;
});

builder.Services.AddSwaggerGen();
builder.Services.ConfigureOptions<ConfigureSwaggerOptions>();  // 每版本文档
```

```csharp
// 每个版本一个 Swagger 文档
public class ConfigureSwaggerOptions(IApiVersionDescriptionProvider provider)
    : IConfigureOptions<SwaggerGenOptions>
{
    public void Configure(SwaggerGenOptions options)
    {
        foreach (var desc in provider.ApiVersionDescriptions)
        {
            options.SwaggerDoc(desc.GroupName, new OpenApiInfo
            {
                Title = $"MyApi {desc.ApiVersion}",
                Version = desc.ApiVersion.ToString(),
                Description = desc.IsDeprecated ? "已弃用，请迁移至新版本" : ""
            });
        }
    }
}
```

```csharp
// 控制器标注版本
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
[ApiController]
public class OrdersV1Controller : ControllerBase { ... }

[ApiVersion("2.0")]
[ApiVersion("1.0", Deprecated = true)]          // 双版本共存，v1 标记弃用
[Route("api/v{version:apiVersion}/orders")]
[ApiController]
public class OrdersV2Controller : ControllerBase { ... }
```

```csharp
// 中间件：每版本一个 UI 入口
app.UseSwagger();
app.UseSwaggerUI(options =>
{
    foreach (var desc in provider.ApiVersionDescriptions)
        options.SwaggerEndpoint($"/swagger/{desc.GroupName}/swagger.json",
                                $"MyApi {desc.GroupName}");
});
```

## 3. 路线 B：Minimal API（.NET 10 内置 OpenAPI + Scalar）

```powershell
dotnet add package Asp.Versioning.Http
dotnet add package Asp.Versioning.Mvc.ApiExplorer
dotnet add package Asp.Versioning.OpenApi      # v10.0.0+（2026-04 起与内置 OpenAPI 打通）
dotnet add package Scalar.AspNetCore           # UI
```

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
})
.AddApiExplorer(options => options.GroupNameFormat = "'v'VVV")
.AddOpenApi();                                   // 一个调用接入内置 OpenAPI

var app = builder.Build();
app.MapOpenApi().WithDocumentPerVersion();       // 每版本一份文档，无需手工注册
app.MapScalarApiReference();                     // /scalar UI（替代 SwaggerUI）
```

> .NET 10 起 `Microsoft.AspNetCore.OpenApi` 内置生成 OpenAPI 3.1，无需 Swashbuckle；控制器项目继续用 Swashbuckle 也完全有效（10.x），按团队熟悉度二选一，不混用。

## 4. XML 注释

```xml
<!-- csproj -->
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
```

```csharp
builder.Services.AddSwaggerGen(o =>
    o.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory,
        $"{Assembly.GetExecutingAssembly().GetName().Name}.xml")));
```

## 5. Swagger 授权入口

```csharp
builder.Services.AddSwaggerGen(o =>
{
    o.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "JWT 令牌，形如 eyJhbGciOi..."
    });
    o.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        [new OpenApiSecurityScheme
            { Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" } }]
            = Array.Empty<string>()
    });
});
```

## 6. 版本演进纪律

**必须升版本的破坏性变更**：删除/重命名字段、改字段类型、可选改必选、改语义（分→元）、删端点、改鉴权要求。
**可同版本内的兼容变更**：加可选字段、加端点、加可选参数、修 bug（不改契约）。

- 旧版本标 `Deprecated = true` 并写迁移指南，保留至少一个过渡期；
- CI 加契约测试（`Microsoft.AspNetCore.OpenApi` 文档 diff 或 Schemathesis）防意外破坏。

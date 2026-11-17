# JWT 认证与授权

> net-full-stack-architect 技能参考文件。JWT 颁发/校验、Policy 授权、自定义授权处理器、刷新令牌。

## 目录

1. [注册与配置](#1-注册与配置)
2. [令牌颁发](#2-令牌颁发)
3. [Policy 细粒度授权](#3-policy-细粒度授权)
4. [自定义授权处理器（资源级权限）](#4-自定义授权处理器资源级权限)
5. [刷新令牌](#5-刷新令牌)
6. [中间件顺序与常见坑](#6-中间件顺序与常见坑)

---

## 1. 注册与配置

```powershell
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

```csharp
// Infrastructure 或 Api/Extensions/AuthExtensions.cs
public static IServiceCollection AddJwtAuth(this IServiceCollection services,
    IConfiguration configuration)
{
    var jwt = configuration.GetSection("Jwt").Get<JwtOptions>()!;

    services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer(options =>
        {
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidIssuer = jwt.Issuer,
                ValidateAudience = true,
                ValidAudience = jwt.Audience,
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(
                    Encoding.UTF8.GetBytes(jwt.SigningKey)),   // ≥256 bit，从 KV/环境变量来
                ValidateLifetime = true,
                ClockSkew = TimeSpan.FromSeconds(30)           // 默认 5 分钟太长，显式调小
            };
        });

    services.AddAuthorization();

    return services;
}

public class JwtOptions
{
    public string Issuer { get; init; } = default!;
    public string Audience { get; init; } = default!;
    public string SigningKey { get; init; } = default!;      // 机密：不进 git
    public int AccessExpireMinutes { get; init; } = 30;
    public int RefreshExpireDays { get; init; } = 7;
}
```

## 2. 令牌颁发

```csharp
public class TokenService
{
    private readonly JwtOptions _opt;
    public TokenService(IOptions<JwtOptions> opt) => _opt = opt.Value;

    public (string access, string refresh) Generate(User user)
    {
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Name, user.UserName),
            new Claim("tenant", user.TenantId),
            new Claim(ClaimTypes.Role, user.Role),
            // 权限点：授权时按 claim 比对
            new Claim("permission", "order.read"),
            new Claim("permission", "order.write"),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_opt.SigningKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var access = new JwtSecurityToken(
            issuer: _opt.Issuer,
            audience: _opt.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_opt.AccessExpireMinutes),
            signingCredentials: creds);

        return (new JwtSecurityTokenHandler().WriteToken(access), GenerateRefreshToken());
    }

    private static string GenerateRefreshToken() => Convert.ToBase64String(
        RandomNumberGenerator.GetBytes(64));
}
```

登录接口只做三件事：校验凭据 → 颁发双令牌 → 返回。**refresh token 存服务端（Redis，可吊销）**，不要只依赖 JWT 自包含。

## 3. Policy 细粒度授权

```csharp
services.AddAuthorization(options =>
{
    // 角色策略
    options.AddPolicy("AdminOnly", p => p.RequireRole("Admin"));

    // 权限点策略（推荐）：按 claim 逐个声明，控制器语义清晰
    options.AddPolicy("OrderRead", p => p.RequireClaim("permission", "order.read"));
    options.AddPolicy("OrderWrite", p => p.RequireClaim("permission", "order.write"));
});
```

```csharp
[Authorize]                                  // 只要登录
[HttpGet]
public async Task<IActionResult> List() { ... }

[Authorize(Policy = "OrderRead")]            // 要权限点
[HttpGet("{id}")]
public async Task<IActionResult> Get(long id) { ... }

[Authorize(Roles = "Admin,Manager")]         // 要角色
[HttpDelete("{id}")]
public async Task<IActionResult> Delete(long id) { ... }
```

## 4. 自定义授权处理器（资源级权限）

资源级权限（如“只能改自己的订单”）用 `IAuthorizationHandler`：

```csharp
public class OrderOwnerRequirement : IAuthorizationRequirement { }

public class OrderOwnerHandler(IServiceScopeFactory scopeFactory)
    : AuthorizationHandler<OrderOwnerRequirement, Order>
{
    protected override async Task HandleAsync(
        AuthorizationHandlerContext context,
        OrderOwnerRequirement requirement,
        Order resource)
    {
        var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (resource.OwnerId.ToString() == userId ||
            context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
        }
    }
}

// 注册
services.AddSingleton<IAuthorizationHandler, OrderOwnerHandler>();

// 使用：资源作为第二个参数传入
[Authorize(Policy = nameof(OrderOwnerRequirement))]   // 或策略包装
[HttpPut("{id}")]
public async Task<IActionResult> Update(long id, [FromBody] OrderDto dto)
{
    var order = await _repo.FindByIdAsync(id);
    var result = await _authorizationService.AuthorizeAsync(User, order, "OrderOwnerPolicy");
    if (!result.Succeeded) return Forbid();
    ...
}
```

## 5. 刷新令牌

```csharp
[HttpPost("refresh")]
public async Task<IActionResult> Refresh([FromBody] RefreshRequest req)
{
    // 1. 校验 access token 签名（允许已过期）
    var principal = _tokenService.ValidateExpiredToken(req.AccessToken);
    // 2. 比对 Redis 中 refresh token（不存在/不匹配 → 401，可能是重放攻击）
    var stored = await _cache.GetAsync($"rt:{principal.GetUserId()}");
    if (stored != req.RefreshToken) return Unauthorized();
    // 3. 轮换：颁新双令牌，删旧 refresh
    var (access, refresh) = _tokenService.Generate(user);
    await _cache.SetAsync($"rt:{userId}", refresh, TimeSpan.FromDays(7));
    return Ok(new { access, refresh });
}
```

要点：refresh 一次性使用（轮换）；登出即删 Redis key；refresh 接口加限流。

## 6. 中间件顺序与常见坑

| 坑 | 说明 |
|---|---|
| 401/403 混乱 | `UseAuthentication()` 必须在 `UseAuthorization()` 前，且在 `MapControllers()` 前 |
| 时钟偏移导致过期仍可用 | `ClockSkew` 默认 5 分钟，敏感系统调 0~30s |
| 密钥轮换期间大量 401 | 支持多密钥（`IssuerSigningKeyResolver`）灰度切换 |
| 令牌无法主动失效 | JWT 天生难吊销 → 短 access + Redis 黑名单/版本号 claim（`tokenVersion`，改密/踢下线时 +1） |
| SignalR/WebSocket 传不了 Header | 协商接口用 Header，连接用 `access_token` 查询串（HTTPS + 限白名单） |
| Swagger 没授权入口 | 配 `AddSecurityDefinition` + `AddSecurityRequirement`（见 api-docs-versioning.md） |
| 把用户 Id 存字符串 | 统一 `ClaimTypes.NameIdentifier` + 一个 `CurrentUser` 服务封装取值 |

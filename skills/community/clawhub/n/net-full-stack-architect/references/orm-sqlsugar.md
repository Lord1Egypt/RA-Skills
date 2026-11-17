# SqlSugar ORM 接入与使用

> net-full-stack-architect 技能参考文件。SqlSugar 5.x 的多数据库配置、CodeFirst/DbFirst、泛型仓储、AOP、事务。

## 目录

1. [安装与 DI 注册](#1-安装与-di-注册)
2. [CodeFirst 实体](#2-codefirst-实体)
3. [DbFirst 生成实体](#3-dbfirst-生成实体)
4. [泛型仓储基类](#4-泛型仓储基类)
5. [查询与分页](#5-查询与分页)
6. [AOP 横切](#6-aop-横切)
7. [事务](#7-事务)
8. [多数据库与读写分离](#8-多数据库与读写分离)
9. [注意事项](#9-注意事项)

---

## 1. 安装与 DI 注册

```powershell
dotnet add package SqlSugar
```

```csharp
// Infrastructure/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        var dbOptions = configuration.GetSection("Db").Get<DbOptions>()!;
        var dbType = Enum.Parse<DbType>(dbOptions.DbType);

        services.AddSqlSugar(new IocConfig
        {
            ConfigId = "main",
            ConnectionString = dbOptions.ConnectionStrings[dbOptions.DbType],
            DbType = dbType,
            IsAutoCloseConnection = true
        });

        return services;
    }
}
```

`AddSqlSugar` 注册单例 `ISqlSugarClient`；仓储内统一用 `DbScoped.SugarScope` 取作用域客户端（线程安全、随作用域释放）。**不要在业务代码里 new SqlSugarClient**。

## 2. CodeFirst 实体

```csharp
// Domain/Entities/Order.cs
[SugarTable("t_order", TableDescription = "订单表")]
public class Order : EntityBase
{
    [SugarColumn(IsPrimaryKey = true, IsIdentity = true, ColumnDescription = "主键")]
    public long Id { get; set; }

    [SugarColumn(Length = 32, IsNullable = false, ColumnDescription = "订单号")]
    public string OrderNo { get; set; } = default!;

    [SugarColumn(ColumnDataType = "decimal(18,2)")]
    public decimal Amount { get; set; }

    [SugarColumn(IsIgnore = true)]
    public string? TempField { get; set; }
}

public class EntityBase
{
    [SugarColumn(IsNullable = false)]
    public bool IsDelete { get; set; }

    public DateTime CreateTime { get; set; } = DateTime.Now;
    public DateTime UpdateTime { get; set; } = DateTime.Now;
}
```

建表/结构同步（程序启动时执行一次，生产环境建议改为迁移脚本审核后执行）：

```csharp
using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<ISqlSugarClient>();
db.CodeFirst.InitTables(typeof(Order).Assembly.GetExportedTypes());
```

## 3. DbFirst 生成实体

```csharp
// 一次性生成实体到 Domain/Entities
db.DbFirst.Where("t_order").CreateClassFile("src/MyApi.Domain/Entities", "MyApi.Domain");
```

生成后按需调整命名与特性；**数据库为准**的项目用 DbFirst，**代码为准**用 CodeFirst。

## 4. 泛型仓储基类

```csharp
// Infrastructure/Persistence/BaseRepository.cs
public class BaseRepository<T> : SimpleClient<T>, IBaseRepository<T> where T : class, new()
{
    public BaseRepository(ISqlSugarClient? context = null) : base(context)
    {
        base.Context = DbScoped.SugarScope;
    }

    public async Task<bool> DeleteByIdAsync(dynamic id) => await base.DeleteByIdAsync(id);

    public async Task<bool> DeleteByIdsAsync(dynamic[] ids) => await base.DeleteByIdsAsync(ids);

    public virtual async Task<T?> FindByIdAsync(dynamic id) => await GetByIdAsync(id);

    public async Task<T?> FindAsync(Expression<Func<T, bool>> where)
        => await GetSingleAsync(where);

    public async Task<bool> InsertAsync(T entity) => await base.InsertAsync(entity);

    public async Task<bool> InsertRangeAsync(List<T> list) => await base.InsertRangeAsync(list);

    public List<T> GetList(Expression<Func<T, bool>>? where = null)
        => where is null ? base.GetList() : base.GetList(where);

    public async Task<List<T>> GetListAsync(Expression<Func<T, bool>>? where = null)
        => where is null ? await base.GetListAsync() : await base.GetListAsync(where);

    public async Task<List<T>> GetPageListAsync(Expression<Func<T, bool>>? where,
        int pageIndex, int pageSize, RefAsync<int> total)
        => await Context.Queryable<T>().WhereIF(where is not null, where)
            .ToPageListAsync(pageIndex, pageSize, total);

    public async Task<bool> UpdateAsync(T entity) => await base.UpdateAsync(entity);

    public async Task<bool> UpdateRangeAsync(List<T> list) => await base.UpdateRangeAsync(list);
}
```

业务仓储 = 空类继承（DI 按程序集扫描注册 `AsImplementedInterfaces()`）：

```csharp
public interface IOrderRepository : IBaseRepository<Order> { }
public class OrderRepository : BaseRepository<Order>, IOrderRepository { }
```

## 5. 查询与分页

```csharp
// 链式查询（Queryable）
var page = await db.Queryable<Order>()
    .WhereIF(!string.IsNullOrWhiteSpace(kw), o => o.OrderNo.Contains(kw!))
    .Where(o => !o.IsDelete)
    .OrderByDescending(o => o.CreateTime)
    .Select(o => new OrderDto { Id = o.Id, OrderNo = o.OrderNo, Amount = o.Amount })
    .ToPageListAsync(pageIndex, pageSize, total);

// 原生 SQL（参数化，防注入）
var list = await db.Ado.SqlQueryAsync<OrderDto>(
    "SELECT * FROM t_order WHERE CreateTime >= @start", new { start });

// 根据主键查询
var order = await db.Queryable<Order>().InSingleAsync(id);
```

## 6. AOP 横切

```csharp
db.Aop.OnLogExecuting = (sql, paras) =>
{
    // 脱敏：paras 可能含密码/身份证等，生产环境只记 SQL 模板或对值做正则替换
    Log.Information("SQL: {Sql}", sql);
};

db.Aop.OnError = ex =>
{
    Log.Error(ex, "SQL执行失败: {Message}", ex.Message);
};

db.Aop.DataExecuting = (oldValue, entityInfo) =>
{
    // 自动填充：插入时设置 CreateTime/租户
    if (entityInfo.OperationType == DataFilterType.InsertByObject)
    {
        if (entityInfo.EntityValue is EntityBase e) e.CreateTime = DateTime.Now;
    }
};
```

软删除过滤（全局 WhereIF 封装在仓储基类，或 AOP DataFilter）：

```csharp
public async Task<List<T>> GetListAsync(Expression<Func<T, bool>>? where = null)
{
    var q = Context.Queryable<T>();
    if (typeof(EntityBase).IsAssignableFrom(typeof(T)))
        q = q.Where("IsDelete = 0");
    return where is null ? await q.ToListAsync() : await q.Where(where).ToListAsync();
}
```

## 7. 事务

```csharp
// 方式一：闭包（推荐，自动回滚）
var ok = await db.UseTranAsync(async () =>
{
    await db.Insertable(order).ExecuteCommandAsync();
    await db.Updateable<Stock>(s => s.Sku == sku)
             .SetColumns(s => s.Count == s.Count - 1).ExecuteCommandAsync();
});

// 方式二：手动
db.Ado.BeginTran();
try
{
    await db.Insertable(order).ExecuteCommandAsync();
    db.Ado.CommitTran();
}
catch
{
    db.Ado.RollbackTran();
    throw;
}
```

- 事务边界放 Service 层，一个业务操作一个事务；
- 跨库/跨服务事务不要用本地事务硬撑，用 CAP 最终一致（见 third-party-libraries.md）。

## 8. 多数据库与读写分离

```csharp
// 多连接（同进程连多种库）：IocConfig 用不同 ConfigId
services.AddSqlSugar(new IocConfig { ConfigId = "main", ... });
services.AddSqlSugar(new IocConfig { ConfigId = "log", ConnectionString = logConn, DbType = DbType.MySql });

// 取用：DbContextScoped.SugarScope 或 db.GetConnection("log")
```

读写分离与分表分库：SqlSugar 支持 `SlaveConnectionList`（从库列表）与自动分表组件，大数据量表按年/月分表策略在仓储层封装路由函数。国产化场景（达梦/人大金仓）SqlSugar/FreeSql 原生支持，优先于 EF Core。

## 9. 注意事项

1. `IsAutoCloseConnection = true` 时无需手动释放连接；
2. AOP 日志的 `paras` 可能含敏感值，**生产环境脱敏或只记 SQL 模板**；
3. `decimal` 列显式 `ColumnDataType = "decimal(18,2)"`，避免精度漂移；
4. 禁止字符串拼接 SQL；动态条件用 `WhereIF` + 参数化；
5. 大批量写入用 `InsertRange` / `Storageable`（存在即更新），万元级以上考虑 `SqlBulkCopy` 或库内 `LOAD DATA`。

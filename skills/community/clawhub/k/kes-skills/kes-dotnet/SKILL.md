---
name: kes-dotnet
name_for_command: kes-dotnet
description: KingbaseES .NET 框架集成指南。当用户提到 .NET、KDBNDP、Entity Framework、EF Core、ASP.NET、C# 金仓时，必须使用此技能。
---

# KingbaseES .NET 框架集成指南

本技能指导用户完成 KingbaseES 与 .NET 框架的集成，涵盖 KDBNDP、Entity Framework 6 和 EF Core。

## KDBNDP（KingbaseES .NET Data Provider）

### 概述

KDBNDP 是 KingbaseES 提供的 ADO.NET 数据提供者，使用方式与标准的 ADO.NET 数据提供者一致。

### 基本连接

```csharp
using Kdbndp;

string connStr = "Host=127.0.0.1;Port=54321;Database=test;UserId=SYSTEM;Password=123456";
using (var conn = new KdbndpConnection(connStr))
{
    conn.Open();
    using (var cmd = new KdbndpCommand("SELECT version()", conn))
    {
        var result = cmd.ExecuteScalar();
        Console.WriteLine(result);
    }
}
```

## Entity Framework 6

### 配置

在 `Web.config` 或 `App.config` 中注册 Provider：

```xml
<configSections>
    <section name="entityFramework" type="System.Data.Entity.Internal.ConfigFile.EntityFrameworkSection, EntityFramework, Version=6.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089" />
</configSections>

<connectionStrings>
    <add name="KESContext"
         connectionString="Host=127.0.0.1;Port=54321;Database=test;UserId=SYSTEM;Password=123456"
         providerName="KdbndpProvider.Data.KdbndpProviderServices, KdbndpProvider.EntityFramework6" />
</connectionStrings>
```

### DbContext 使用

```csharp
public class KESContext : DbContext
{
    public DbSet<User> Users { get; set; }
}

public class User
{
    public int Id { get; set; }
    public string Username { get; set; }
}
```

## EF Core

### 配置

```csharp
using Microsoft.EntityFrameworkCore;

var options = new DbContextOptionsBuilder<KESContext>()
    .UseKingbase("Host=127.0.0.1;Port=54321;Database=test;UserId=SYSTEM;Password=123456")
    .Options;
```

### 注意事项

- 验证 EF Core 生成的 SQL 与 KingbaseES 语法兼容
- LINQ 到 SQL 的转换可能在复杂查询时需注意差异

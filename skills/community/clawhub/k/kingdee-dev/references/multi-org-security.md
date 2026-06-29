# 金蝶云星空多组织与数据权限开发指南

## 目录
- [概述](#概述)
- [组织模型](#组织模型)
- [插件中获取组织信息](#插件中获取组织信息)
- [多组织数据过滤](#多组织数据过滤)
- [跨组织操作](#跨组织操作)
- [字段权限与功能权限](#字段权限与功能权限)
- [数据范围权限](#数据范围权限)
- [SQL安全与参数化](#sql安全与参数化)
- [常见问题](#常见问题)

---

## 概述

金蝶云星空采用多组织架构，一个数据中心下可包含多个业务组织。二次开发时需要注意：

- 当前登录组织（`CurrentOrganizationInfo`）不一定等于业务组织
- 单据通常携带 `FOrgId` 或 `FXXXOrgId` 字段
- 查询时必须考虑组织隔离，避免跨组织数据泄露
- 用户权限分功能权限、字段权限、数据范围权限三层

## 组织模型

| 概念 | 说明 | 获取方式 |
|------|------|----------|
| 当前登录组织 | 用户当前登录的业务组织 | `this.Context.CurrentOrganizationInfo` |
| 单据组织 | 单据所属的业务组织 | `dataObj["FOrgId"]` 或 `dataObj["FXXXOrgId"]` |
| 用户组织列表 | 用户有权限访问的所有组织 | `this.Context.UserOrganizationInfo` |
| 核算组织 | 财务核算维度 | 基础资料中配置 |
| 库存组织 | 库存管理维度 | 仓库/物料相关 |

## 插件中获取组织信息

```csharp
// 当前登录组织
long orgId = this.Context.CurrentOrganizationInfo.ID;
string orgCode = this.Context.CurrentOrganizationInfo.Code;
string orgName = this.Context.CurrentOrganizationInfo.Name;

// 当前用户
long userId = this.Context.UserId;
string userName = this.Context.UserName;

// 用户所属组织列表
var userOrgs = this.Context.UserOrganizationInfo;
foreach (var org in userOrgs)
{
    long id = org.ID;
    string code = org.Code;
}
```

## 多组织数据过滤

### 列表插件中按当前组织过滤

```csharp
public override void PrepareFilterParameter(FilterParameterArgs e)
{
    base.PrepareFilterParameter(e);
    if (e.FilterParameter?.Filter == null) return;

    long orgId = this.Context.CurrentOrganizationInfo.ID;
    e.FilterParameter.Filter.Add(
        new FilterItem("FOrgId", CompareType.Equals, orgId)
    );
}
```

### 查询时指定组织

```csharp
// 使用业务数据服务查询时指定组织
var param = new object[] { "FNumber = @Number", new SqlParam("@Number", SqlDbType.NVarChar, "MAT001") };
DynamicObject[] materials = BusinessDataServiceHelper.LoadFromCache(
    this.Context,
    "BD_Material",
    param,
    orgId // 指定组织
);
```

## 跨组织操作

### 直接调拨单跨组织取价

```csharp
public override void BeforeExecuteOperationTransaction(BeforeExecuteOperationTransaction e)
{
    base.BeforeExecuteOperationTransaction(e);
    if (e.DataObjects == null) return;

    foreach (DynamicObject dataObj in e.DataObjects)
    {
        long srcOrg = (dataObj["FStockOrgId"] as DynamicObject)?["Id"] as long? ?? 0;
        long targetOrg = (dataObj["FReceiveOrgId"] as DynamicObject)?["Id"] as long? ?? 0;
        if (srcOrg == targetOrg) continue;

        // 跨组织时按目标组织价目表取价
        Entity entryEntity = e.BillBusinessInfo.GetEntity("FEntity");
        DynamicObjectCollection rows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;
        if (rows == null) continue;

        foreach (DynamicObject row in rows)
        {
            long materialId = (row["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0;
            decimal price = GetTargetOrgPrice(targetOrg, materialId);
            row["FPrice"] = price;
        }
    }
}

private decimal GetTargetOrgPrice(long orgId, long materialId)
{
    string sql = @"
        SELECT TOP 1 e.FPRICE
        FROM T_SAL_PRICELISTENTRY e
        INNER JOIN T_SAL_PRICELIST h ON h.FID = e.FID
        WHERE h.FORGID = @OrgId AND e.FMATERIALID = @MaterialId
        ORDER BY h.FEFFECTIVEDATE DESC";

    var param = new SqlParam[]
    {
        new SqlParam("@OrgId", SqlDbType.BigInt, orgId),
        new SqlParam("@MaterialId", SqlDbType.BigInt, materialId)
    };

    DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
    if (ds.Tables[0].Rows.Count > 0)
    {
        return Convert.ToDecimal(ds.Tables[0].Rows[0]["FPRICE"]);
    }
    return 0m;
}
```

## 字段权限与功能权限

### 判断字段权限

```csharp
public override void AfterBindData(EventArgs e)
{
    base.AfterBindData(e);

    string formId = this.View.BillBusinessInfo.GetForm().Id;

    bool canEditPrice = PermissionServiceHelper.HasFieldPermission(
        this.Context,
        formId,
        "FPrice",
        "Edit"
    );

    if (!canEditPrice)
    {
        this.View.GetControl("FPrice").Enabled = false;
    }
}
```

### 判断功能权限

```csharp
bool hasPermission = PermissionServiceHelper.HasFunctionPermission(
    this.Context,
    "SAL_SaleOrder",  // 功能标识
    "audit"           // 操作标识
);

if (!hasPermission)
{
    this.View.ShowErrMessage("您没有审核权限！");
    return;
}
```

> 注意：不同版本的权限服务 API 命名可能不同，需以实际环境为准。

## 数据范围权限

数据范围权限通常指：用户只能看到某些部门/业务员/仓库的数据。

### 在 SQL 中应用数据范围

```csharp
public override void PrepareFilterParameter(FilterParameterArgs e)
{
    base.PrepareFilterParameter(e);
    if (e.FilterParameter?.Filter == null) return;

    // 获取当前用户的业务员ID
    long salesmanId = GetCurrentUserSalesmanId();
    if (salesmanId > 0)
    {
        e.FilterParameter.Filter.Add(
            new FilterItem("FSalerId", CompareType.Equals, salesmanId)
        );
    }
}

private long GetCurrentUserSalesmanId()
{
    string sql = @"
        SELECT FSTAFFID FROM V_BD_SALESMAN
        WHERE FSTAFFID IN (
            SELECT FSTAFFID FROM T_SEC_USER WHERE FUSERID = @UserId
        )";

    var param = new SqlParam[]
    {
        new SqlParam("@UserId", SqlDbType.BigInt, this.Context.UserId)
    };

    DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
    if (ds.Tables[0].Rows.Count > 0)
    {
        return Convert.ToInt64(ds.Tables[0].Rows[0]["FSTAFFID"]);
    }
    return 0;
}
```

## SQL安全与参数化

### 禁止字符串拼接 SQL

```csharp
// 错误：存在 SQL 注入风险
string sql = $"SELECT * FROM T_SAL_ORDER WHERE FBILLNO = '{billNo}'";

// 正确：参数化查询
string sql = "SELECT * FROM T_SAL_ORDER WHERE FBILLNO = @BillNo";
var param = new SqlParam[]
{
    new SqlParam("@BillNo", SqlDbType.NVarChar, billNo)
};
DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
```

### 参数化查询模板

```csharp
string sql = @"
    SELECT h.FBILLNO, h.FDATE, e.FQTY
    FROM T_SAL_ORDER h
    INNER JOIN T_SAL_ORDERENTRY e ON e.FID = h.FID
    WHERE h.FORGID = @OrgId AND h.FDATE >= @BeginDate AND h.FDATE < @EndDate";

var param = new SqlParam[]
{
    new SqlParam("@OrgId", SqlDbType.BigInt, this.Context.CurrentOrganizationInfo.ID),
    new SqlParam("@BeginDate", SqlDbType.DateTime, beginDate),
    new SqlParam("@EndDate", SqlDbType.DateTime, endDate.AddDays(1))
};

DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 列表看到其他组织数据 | 缺少组织过滤 | 在列表插件 `PrepareFilterParameter` 中加 `FOrgId` 过滤 |
| 单据保存时报组织不一致 | 当前组织与单据组织不同 | 检查 `this.Context.CurrentOrganizationInfo.ID` 与单据 `FOrgId` |
| 跨组织查询无数据 | 未指定组织 | 查询基础资料/单据时传入目标组织 |
| 用户权限不足 | 缺少字段/功能/数据权限 | 在权限管理中配置并同步用户 |
| SQL 注入风险 | 字符串拼接 SQL | 全部改为参数化查询 |

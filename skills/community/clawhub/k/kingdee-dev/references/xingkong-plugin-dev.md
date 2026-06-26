# 金蝶云星空插件开发指南

## 目录
- [概述](#概述)
- [插件开发基础](#插件开发基础)
- [表单插件](#表单插件)
- [列表插件](#列表插件)
- [操作插件](#操作插件)
- [报表插件](#报表插件)
- [单据转换插件](#单据转换插件)
- [服务插件](#服务插件)
- [DynamicObject 数据操作](#dynamicobject-数据操作)
- [插件注册](#插件注册)
- [调试方法](#调试方法)

---

## 概述

金蝶云星空二次开发的核心方式是**插件开发**。插件以 C# 类库（.dll）形式存在，通过实现特定基类的虚方法来拦截系统事件，实现业务逻辑扩展。

**开发环境：** Visual Studio 2019/2022 + .NET Framework 4.6.1+

**核心引用：**
- Kingdee.BOS.dll
- Kingdee.BOS.Core.dll
- Kingdee.BOS.DataEntity.dll
- Kingdee.BOS.App.dll
- Kingdee.BOS.ServiceHelper.dll

---

## 插件开发基础

### 1. 创建插件项目

1. VS 新建「类库(.NET Framework)」项目，目标框架 4.6.1+
2. 添加金蝶 BOS 核心引用（从星空安装目录 `K3Cloud\WebSite\bin` 获取）
3. 创建插件类，继承对应基类
4. 实现虚方法
5. 编译生成 .dll

### 2. BusinessInfo 与 BillBusinessInfo

| 类 | 用途 | 获取方式 |
|----|------|----------|
| BusinessInfo | 通用单据元数据 | `this.View.BillBusinessInfo` 或 `e.BillBusinessInfo` |
| BillBusinessInfo | 含单据体信息的元数据 | 表单/操作插件中的 `this.View.BillBusinessInfo` |

获取字段：
``csharp
// 按字段标识获取
Field field = this.View.BillBusinessInfo.GetField("FNumber");

// 按Key获取单据头字段
DynamicObject obj = this.Model.DataObject;
string number = obj["FNumber"].ToString();

// 获取单据体
Entity entryEntity = this.View.BillBusinessInfo.GetEntity("FEntity");
DynamicObjectCollection entryRows = entryEntity.DynamicProperty.GetValue(obj) as DynamicObjectCollection;
``

### 3. 数据操作三件套

``csharp
// Model — 读写界面数据
this.Model.SetValue("FField", value);           // 设值
this.Model.GetValue("FField");                   // 取值
this.Model.DeleteEntryData("FEntity", rowIndex); // 删行

// View — 界面交互控制
this.View.ShowMessage("提示信息");               // 消息框
this.View.UpdateView("FField");                  // 刷新字段
this.View.GetControl("FField").Visible = false;  // 隐藏控件
this.View.GetControl("FField").Enabled = false;  // 禁用控件

// ServiceHelper — 数据库操作
BusinessDataServiceHelper.Save(this.Context, businessInfo, dataObject);
BusinessDataServiceHelper.Load(this.Context, billId, businessInfo);
``

---

## 表单插件

**基类：** `Kingdee.BOS.Core.DynamicForm.PlugIn.AbstractFormPlugin`

**最常用插件类型**，控制单据界面的所有交互行为。

### 核心事件

| 事件方法 | 触发时机 | 典型用途 |
|----------|----------|----------|
| `OnBarClick` | 点击工具栏按钮 | 自定义按钮响应 |
| `BarItemClick` | 点击菜单项 | 菜单按钮响应（推荐） |
| `AfterBindData` | 数据绑定后（界面加载/刷新后） | 根据数据状态控制界面 |
| `DataChanged` | 字段值变更后 | 字段联动（如选择物料带出单位） |
| `BeforeDoOperation` | 执行操作前 | 拦截操作（校验） |
| `AfterDoOperation` | 执行操作后 | 操作后处理 |
| `ButtonClick` | 按钮点击 | 自定义按钮 |
| `Closed` | 窗口关闭 | 清理资源 |
| `PreOpenForm` | 打开表单前 | 传参/权限控制 |

### 字段联动示例：选择物料自动带出单位

``csharp
public override void DataChanged(DataChangedEventArgs e)
{
    base.DataChanged(e);

    if (e.Field.Key.EqualsIgnoreCase("FMaterialId"))
    {
        // 获取选中的物料
        DynamicObject material = e.NewValue as DynamicObject;
        if (material == null) return;

        // 从物料中取基础单位
        DynamicObject baseUnit = material["BaseUnitId"] as DynamicObject;
        if (baseUnit != null)
        {
            // 设置当前行的单位字段
            int rowIndex = this.Model.GetEntryCurrentRow("FEntity");
            this.Model.SetValue("FUnitId", baseUnit["Id"], rowIndex);
        }
    }
}
``

### 自定义按钮响应示例

``csharp
public override void BarItemClick(BarItemClickEventArgs e)
{
    base.BarItemClick(e);

    if (e.BarItemKey.EqualsIgnoreCase("tbMyCustomBtn"))
    {
        // 执行自定义逻辑
        DynamicObject dataObj = this.Model.DataObject;

        // 业务处理...

        // 刷新界面
        this.View.ShowMessage("操作完成");
        this.View.UpdateView();
    }
}
``

### 界面控制示例：根据单据状态控制字段

``csharp
public override void AfterBindData(EventArgs e)
{
    base.AfterBindData(e);

    // 获取单据状态
    string billStatus = this.Model.GetValue("FBillStatus")?.ToString();

    if (billStatus == "C") // 已审核
    {
        // 禁用所有字段
        this.View.GetControl("FNumber").Enabled = false;
        this.View.GetControl("FName").Enabled = false;

        // 隐藏自定义按钮
        this.View.GetControl("tbMyCustomBtn").Visible = false;
    }
}
``

### 打开新表单并传参

``csharp
public override void BarItemClick(BarItemClickEventArgs e)
{
    base.BarItemClick(e);

    if (e.BarItemKey.EqualsIgnoreCase("tbOpenDetail"))
    {
        // 构造参数
        DynamicFormShowParameter showParam = new DynamicFormShowParameter();
        showParam.FormId = "BD_Material";   // 目标表单ID
        showParam.OpenStyle = FormOpenStyle.NewWindow;
        showParam.CustomParams.Add("FMaterialId", "100001");

        this.View.ShowForm(showParam);
    }
}
``

### 接收子表单返回数据

``csharp
public override void Closed(FormClosedEventArgs e)
{
    base.Closed(e);

    if (e.ClosedFormId == "MY_CustomForm" && e.ReturnData != null)
    {
        DynamicObject returnData = e.ReturnData as DynamicObject;
        this.Model.SetValue("FResult", returnData["FValue"]);
        this.View.UpdateView("FResult");
    }
}
``

---

## 列表插件

**基类：** `Kingdee.BOS.Core.List.PlugIn.AbstractListPlugin`

控制列表界面的过滤、工具栏、菜单等。

### 核心事件

| 事件方法 | 触发时机 | 典型用途 |
|----------|----------|----------|
| `PrepareFilterParameter` | 构建过滤条件前 | 动态过滤列表数据 |
| `GetList` | 获取列表数据时 | 自定义列表数据源 |
| `BarItemClick` | 点击工具栏按钮 | 自定义按钮响应 |
| `AfterBindData` | 数据绑定后 | 列表数据后处理 |
| `ListDoubleClick` | 双击列表行 | 自定义双击行为 |
| `FormatRowCondition` | 格式化行显示 | 行着色、图标 |

### 动态过滤列表示例

``csharp
public override void PrepareFilterParameter(FilterParameterArgs e)
{
    base.PrepareFilterParameter(e);

    // 添加固定过滤条件：只显示当前用户创建的单据
    string currentUserId = this.Context.UserId.ToString();
    e.FilterParameter.Filter.Add(
        new FilterItem("FCreatorId", CompareType.Equals, currentUserId)
    );

    // 添加日期范围过滤
    e.FilterParameter.Filter.Add(
        new FilterItem("FDate", CompareType.GreaterThanOrEquals, DateTime.Today.AddDays(-30))
    );
}
``

### 行着色示例

``csharp
public override void FormatRowCondition(FormatRowConditionArgs e)
{
    base.FormatRowCondition(e);

    // 根据单据状态设置行颜色
    string billStatus = e.DataRow["FBillStatus"]?.ToString();
    switch (billStatus)
    {
        case "A": // 暂存
            e.FormatCondition.BackColor = System.Drawing.Color.LightYellow;
            break;
        case "B": // 已提交
            e.FormatCondition.BackColor = System.Drawing.Color.LightBlue;
            break;
        case "C": // 已审核
            e.FormatCondition.BackColor = System.Drawing.Color.LightGreen;
            break;
        case "D": // 已关闭
            e.FormatCondition.ForeColor = System.Drawing.Color.Gray;
            break;
    }
}
``

---

## 操作插件

**基类：** `Kingdee.BOS.Core.DynamicForm.PlugIn.AbstractOperationServicePlugIn`

**高频使用**，在保存/提交/审核/反审核等操作时拦截。

### 核心事件（按执行顺序）

| 事件方法 | 触发时机 | 典型用途 |
|----------|----------|----------|
| `OnPreparePropertys` | 准备加载属性 | 指定需要加载的字段（性能优化） |
| `OnAddValidators` | 添加校验器 | 自定义校验规则 |
| `BeginValidate` | 校验开始前 | 初始化校验上下文 |
| `OnValidate` | 执行校验 | 数据校验 |
| `EndValidate` | 校验结束后 | 校验结果汇总 |
| `BeforeExecuteOperationTransaction` | 执行操作事务前 | **核心拦截点**，可阻止操作 |
| `BeginExecuteOperationTransaction` | 事务开始 | 事务内操作 |
| `AfterExecuteOperationTransaction` | 事务提交后 | 操作后处理（写日志/发通知） |
| `EndExecuteOperationTransaction` | 事务结束 | 最终清理 |

### 保存前校验示例

``csharp
public override void BeforeExecuteOperationTransaction(BeforeExecuteOperationTransaction e)
{
    base.BeforeExecuteOperationTransaction(e);

    foreach (DynamicObject dataObj in e.DataObjects)
    {
        // 校验金额不能为负
        decimal amount = Convert.ToDecimal(dataObj["FAmount"]);
        if (amount < 0)
        {
            // 阻止操作并提示
            e.CancelFormMessage = "金额不能为负数！";
            e.CancelOperation = true;
            return;
        }

        // 校证明细行不能为空
        Entity entryEntity = e.BillBusinessInfo.GetEntity("FEntity");
        DynamicObjectCollection entryRows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;
        if (entryRows == null || entryRows.Count == 0)
        {
            e.CancelFormMessage = "明细行不能为空！";
            e.CancelOperation = true;
            return;
        }
    }
}
``

### 审核后自动写日志示例

``csharp
public override void AfterExecuteOperationTransaction(AfterExecuteOperationTransaction e)
{
    base.AfterExecuteOperationTransaction(e);

    foreach (DynamicObject dataObj in e.DataObjects)
    {
        string billNo = dataObj["FBillNo"]?.ToString();
        string billId = (dataObj["Id"] ?? dataObj[0]).ToString();

        // 写日志表
        // ... 执行SQL或调用ServiceHelper

        // 或者触发其他业务逻辑
        // 如：自动生成下游单据
    }
}
``

### 指定需要加载的字段（性能优化）

``csharp
public override void OnPreparePropertys(PreparePropertysEventArgs e)
{
    base.OnPreparePropertys(e);

    // 操作插件默认只加载部分字段，需要显式声明
    e.FieldKeys.Add("FMaterialId");
    e.FieldKeys.Add("FQty");
    e.FieldKeys.Add("FPrice");
    e.FieldKeys.Add("FAmount");
    e.FieldKeys.Add("FUnitId");
}
``

---

## 报表插件

**基类：** `Kingdee.BOS.Core.Report.PlugIn.AbstractSysReportServicePlugIn`

开发自定义报表（直接SQL账表 / 简单账表 / 分页报表）。

### 核心事件

| 事件方法 | 触发时机 | 典型用途 |
|----------|----------|----------|
| `GetSchema` | 初始化报表结构 | 定义报表列 |
| `GetData` | 获取报表数据 | 查询并返回数据 |
| `GetFilter` | 构建过滤条件 | 自定义过滤逻辑 |
| `PrepareFilterParameter` | 准备过滤参数 | 动态过滤 |

### 简单账表示例

``csharp
public override void GetSchema(GetSchemaEventArgs e)
{
    base.GetSchema(e);

    // 定义报表列
    var schema = new ReportSchema();
    schema.AddColumn("FNumber", "物料编码", SqlStorageType.NVarChar, 50);
    schema.AddColumn("FName", "物料名称", SqlStorageType.NVarChar, 100);
    schema.AddColumn("FQty", "数量", SqlStorageType.Decimal);
    schema.AddColumn("FAmount", "金额", SqlStorageType.Decimal);

    e.Schema = schema;
}

public override void GetData(GetDataEventArgs e)
{
    base.GetData(e);

    // 构建SQL
    string sql = @"SELECT t1.FNUMBER AS FNumber
                         ,t2.FNAME AS FName
                         ,SUM(t3.FQTY) AS FQty
                         ,SUM(t3.FAMOUNT) AS FAmount
                     FROM T_SAL_OUTSTOCK t0
                     LEFT JOIN T_SAL_OUTSTOCKENTRY t3 ON t3.FID = t0.FID
                     LEFT JOIN T_BD_MATERIAL t1 ON t1.FMATERIALID = t3.FMATERIALID
                     LEFT JOIN T_BD_MATERIAL_L t2 ON t2.FMATERIALID = t1.FMATERIALID AND t2.FLOCALEID = 2052
                     WHERE t0.FDATE >= @BeginDate AND t0.FDATE <= @EndDate
                     GROUP BY t1.FNUMBER, t2.FNAME";

    // 执行查询
    var paramList = new List<SqlParam>();
    paramList.Add(new SqlParam("@BeginDate", SqlDbType.DateTime, e.Filter.GetFilterValue("FBeginDate")));
    paramList.Add(new SqlParam("@EndDate", SqlDbType.DateTime, e.Filter.GetFilterValue("FEndDate")));

    DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, paramList.ToArray());
    e.Data = ds.Tables[0];
}
``

### 报表插件与普通表单插件的区别

| 特性 | 报表插件 | 表单插件 |
|------|----------|----------|
| 继承基类 | AbstractSysReportServicePlugIn | AbstractFormPlugin |
| 数据来源 | 自定义SQL查询 | 系统自动加载 |
| 界面 | 报表视图 | 单据/动态表单 |
| 过滤 | 支持 FilterParameter | 通过 DataChanged |
| 分组汇总 | 支持 | 不支持 |

---

## 单据转换插件

**基类：** `Kingdee.BOS.Core.Convert.PlugIn.AbstractConvertPlugIn`

控制下推转单时的字段映射和转换逻辑。

### 核心事件

| 事件方法 | 触发时机 | 典型用途 |
|----------|----------|----------|
| `OnPrepareConvert` | 转换准备 | 修改目标字段映射 |
| `AfterConvert` | 转换完成后 | 补充目标单数据 |
| `OnFieldConvert` | 单字段转换时 | 自定义字段映射规则 |

### 下推时自动填充字段示例

``csharp
public override void AfterConvert(AfterConvertEventArgs e)
{
    base.AfterConvert(e);

    // 遍历目标单据
    foreach (DynamicObject targetObj in e.TargetDatas)
    {
        // 设置目标单据的自定义字段
        targetObj["FNote"] = "由销售订单下推生成";

        // 遍历目标单据体
        Entity targetEntry = e.TargetBusinessInfo.GetEntity("FEntity");
        DynamicObjectCollection entryRows = targetEntry.DynamicProperty.GetValue(targetObj) as DynamicObjectCollection;
        if (entryRows != null)
        {
            foreach (DynamicObject row in entryRows)
            {
                // 修改数量（如自动打折）
                decimal qty = Convert.ToDecimal(row["FQty"]);
                row["FNote"] = $""原数量:{qty}"";
            }
        }
    }
}
``

---

## 服务插件

用于自定义 WebAPI 接口和后台服务。

### 自定义 WebAPI 服务插件

``csharp
[Kingdee.BOS.ServiceDescriptor(""MyCustomApi"")]
public class MyCustomApiService : Kingdee.BOS.App.Core.ServiceHandler.AbstractServiceHandler
{
    public Kingdee.BOS.ServiceHandler.InvokeResult DoAction(Kingdee.BOS.ServiceHandler.InvokeContext context)
    {
        var result = new Kingdee.BOS.ServiceHandler.InvokeResult();

        try
        {
            // 获取请求参数
            string param1 = context.RequestData["param1"]?.ToString();

            // 执行业务逻辑
            // ...

            // 返回结果
            result.ResultData = new { success = true, message = ""操作成功"" };
        }
        catch (Exception ex)
        {
            result.ResultData = new { success = false, message = ex.Message };
        }

        return result;
    }
}
``

### 定时任务插件

实现 `Kingdee.BOS.Contracts.IScheduleService` 接口：

``csharp
public class MyScheduleService : Kingdee.BOS.Contracts.IScheduleService
{
    public void Run(Kingdee.BOS.Context ctx, Kingdee.BOS.Contracts.Schedule schedule)
    {
        // 定时执行的逻辑
        // 如：每日自动同步数据、生成报表等
    }
}
``

---

## DynamicObject 数据操作

DynamicObject 是金蝶BOS平台的核心数据载体，所有单据数据都通过它操作。

### 读取数据

``csharp
DynamicObject dataObj = this.Model.DataObject;

// 单据头字段
string billNo = dataObj["FBillNo"]?.ToString();
decimal amount = Convert.ToDecimal(dataObj["FAmount"]);
DynamicObject refObj = dataObj["FCustomerId"] as DynamicObject; // 基础资料引用字段

// 从基础资料引用字段中取值
if (refObj != null)
{
    string customerName = refObj["Name"]?.ToString(); // 多语言名称
    string customerNumber = refObj["Number"]?.ToString();
}

// 单据体
Entity entryEntity = this.View.BillBusinessInfo.GetEntity("FEntity");
DynamicObjectCollection entryRows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;

foreach (DynamicObject row in entryRows)
{
    string materialId = (row["FMaterialId"] as DynamicObject)?["Id"]?.ToString();
    decimal qty = Convert.ToDecimal(row["FQty"]);
}
``

### 写入数据

``csharp
// 单据头字段设值
this.Model.SetValue("FFieldName", value);

// 单据体字段设值（需指定行号）
int rowIndex = this.Model.GetEntryCurrentRow("FEntity");
this.Model.SetValue("FQty", 100, rowIndex);

// 新增单据体行
this.Model.CreateNewEntryRow("FEntity");

// 删除单据体行
this.Model.DeleteEntryData("FEntity", rowIndex);
``

### 基础资料字段赋值

``csharp
// 方式1：通过ID设置
this.Model.SetItemValueByNumber("FMaterialId", ""MAT001"", rowIndex);

// 方式2：通过DynamicObject设置
DynamicObject material = ...; // 从查询获取
this.Model.SetValue("FMaterialId", material, rowIndex);
``

---

## 插件注册

插件编译后需要注册到系统中才能生效。

### 注册方式

1. **BOS IDE 注册**（推荐）
   - 打开 BOS IDE → 找到目标单据 → 右键「扩展」
   - 在扩展单据的属性中找到「表单插件」/「操作插件」等
   - 点击「新增」→ 选择编译好的 dll 和类
   - 保存并发布

2. **数据库直接注册**
   `sql
   -- 查看已有插件注册
   SELECT * FROM T_BOS_FORMPLUGIN WHERE FFORMID = 'SAL_SaleOrder'

   -- 插入插件注册记录（具体字段参考系统表结构）
   `

### 插件注册位置对照

| 插件类型 | 注册位置 | BOS IDE 路径 |
|----------|----------|--------------|
| 表单插件 | 单据→表单插件 | 属性→表单插件集合 |
| 列表插件 | 列表→列表插件 | 属性→列表插件集合 |
| 操作插件 | 操作→操作服务插件 | 操作属性→插件集合 |
| 报表插件 | 报表→报表服务插件 | 报表属性→插件集合 |
| 转换插件 | 转换规则→转换插件 | 转换规则属性→插件集合 |

### 注册注意事项

- **顺序很重要**：多个插件的执行顺序按注册顺序排列
- **必须签入**：修改后必须保存→签入→发布才生效
- **dll 位置**：插件 dll 放在 `K3Cloud\WebSite\bin` 目录下
- **重启 IIS**：替换 dll 后需重启 IIS 或回收应用池

---

## 调试方法

### 方法1：附加进程调试（推荐）

1. VS 菜单 → 调试 → 附加到进程
2. 找到 `w3wp.exe`（IIS 工作进程）
3. 在插件代码中设置断点
4. 在星空界面触发对应操作

### 方法2：日志调试

``csharp
// 写入金蝶日志
Kingdee.BOS.Log.Logger.Info(""调试信息："" + someValue, ""MyPlugin"", Kingdee.BOS.Log.LogLevel.Info);

// 也可通过 View 显示
this.View.ShowMessage($""调试：fieldValue = {fieldValue}"");
``

### 方法3：SQL跟踪

``sql
-- 查看最近的SQL执行（需要数据库权限）
SELECT TOP 100 * FROM sys.dm_exec_query_stats ORDER BY last_execution_time DESC
``

### 常见调试问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 断点不命中 | 附加了错误的 w3wp 进程 | 检查应用池，附加正确的进程 |
| 断点不命中 | dll 版本不一致 | 确认 bin 目录下是最新的 dll |
| 插件不执行 | 未注册或注册位置错误 | 检查 BOS IDE 中的注册 |
| 插件不执行 | 未发布 | 保存→签入→发布→重启 IIS |
| 报错找不到方法 | 缺少引用或版本不对 | 检查引用的 BOS dll 版本 |

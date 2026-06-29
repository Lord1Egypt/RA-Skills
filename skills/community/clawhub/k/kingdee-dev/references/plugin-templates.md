# 金蝶云星空插件代码模板库

## 目录
- [表单插件模板](#表单插件模板)
- [列表插件模板](#列表插件模板)
- [操作插件模板](#操作插件模板)
- [报表插件模板](#报表插件模板)
- [单据转换插件模板](#单据转换插件模板)
- [服务插件模板](#服务插件模板)
- [审批流插件模板](#审批流插件模板)
- [多组织与权限场景](#多组织与权限场景)
- [复杂项目案例](#复杂项目案例)
- [常用代码片段](#常用代码片段)

---

## 表单插件模板

### 完整模板

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using Kingdee.BOS;
using Kingdee.BOS.Core.DynamicForm;
using Kingdee.BOS.Core.DynamicForm.PlugIn;
using Kingdee.BOS.Core.DynamicForm.PlugIn.Args;
using Kingdee.BOS.Core.Metadata;
using Kingdee.BOS.Core.Metadata.Entity;
using Kingdee.BOS.Core.Metadata.FieldElement;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    public class {BillName}FormPlugIn : AbstractFormPlugin
    {
        #region 字段变更
        public override void DataChanged(DataChangedEventArgs e)
        {
            base.DataChanged(e);
            if (e.Field == null) return;

            switch (e.Field.Key.ToUpperInvariant())
            {
                case "FMATERIALID":  // 物料变更
                    OnMaterialChanged(e);
                    break;
                case "FQTY":         // 数量变更
                case "FPRICE":       // 单价变更
                    OnQtyOrPriceChanged(e);
                    break;
            }
        }

        private void OnMaterialChanged(DataChangedEventArgs e)
        {
            DynamicObject material = e.NewValue as DynamicObject;
            if (material == null) return;

            // 带出单位：基础资料引用字段取 DynamicObject 里的 Id/Name/Number
            DynamicObject baseUnit = material["BaseUnitId"] as DynamicObject;
            int rowIndex = this.Model.GetEntryCurrentRowIndex("FEntity");
            if (rowIndex >= 0 && baseUnit != null)
            {
                this.Model.SetValue("FUnitId", baseUnit["Id"], rowIndex);
                this.View.UpdateView("FUnitId");
            }
        }

        private void OnQtyOrPriceChanged(DataChangedEventArgs e)
        {
            int rowIndex = this.Model.GetEntryCurrentRowIndex("FEntity");
            if (rowIndex < 0) return;

            decimal qty = Convert.ToDecimal(this.Model.GetValue("FQty", rowIndex) ?? 0);
            decimal price = Convert.ToDecimal(this.Model.GetValue("FPrice", rowIndex) ?? 0);
            decimal amount = qty * price;
            this.Model.SetValue("FAmount", amount, rowIndex);
            this.View.UpdateView("FAmount");
        }
        #endregion

        #region 按钮点击
        public override void BarItemClick(BarItemClickEventArgs e)
        {
            base.BarItemClick(e);
            if (string.IsNullOrEmpty(e.BarItemKey)) return;

            switch (e.BarItemKey.ToUpperInvariant())
            {
                case "TBCUSTOMBTN":  // 自定义按钮
                    OnCustomButtonClick();
                    break;
            }
        }

        private void OnCustomButtonClick()
        {
            try
            {
                DynamicObject dataObj = this.Model.DataObject;
                string billNo = dataObj["FBillNo"]?.ToString() ?? string.Empty;

                // 执行业务逻辑...

                this.View.ShowMessage($"单据 {billNo} 处理完成");
                this.View.UpdateView();
            }
            catch (Exception ex)
            {
                this.View.ShowErrMessage($"操作失败：{ex.Message}");
            }
        }
        #endregion

        #region 界面加载后
        public override void AfterBindData(EventArgs e)
        {
            base.AfterBindData(e);

            // 根据单据状态控制界面：A=暂存 B=提交 C=审核 D=关闭
            DynamicObject billStatusObj = this.Model.GetValue("FBillStatus") as DynamicObject;
            string billStatus = billStatusObj?["Id"]?.ToString();

            if (billStatus == "C") // 已审核
            {
                this.View.GetControl("FNumber").Enabled = false;
                this.View.GetControl("FName").Enabled = false;
            }
        }
        #endregion

        #region 打开表单前
        public override void PreOpenForm(PreOpenFormEventArgs e)
        {
            base.PreOpenForm(e);

            if (e.OpenParameter?.CustomParams == null) return;

            if (e.OpenParameter.CustomParams.ContainsKey("FParam1"))
            {
                string param1 = e.OpenParameter.CustomParams["FParam1"];
                // 可缓存到 this.View.OpenParameter 或留待 AfterBindData 使用
            }
        }
        #endregion

        #region 关闭表单后接收返回值
        public override void Closed(FormClosedEventArgs e)
        {
            base.Closed(e);

            if (e.ClosedFormId == "MY_CustomForm" && e.ReturnData != null)
            {
                DynamicObject returnData = e.ReturnData as DynamicObject;
                if (returnData != null)
                {
                    this.Model.SetValue("FResult", returnData["FValue"]);
                    this.View.UpdateView("FResult");
                }
            }
        }
        #endregion
    }
}
```

---

## 列表插件模板

```csharp
using System;
using System.Data;
using System.Collections.Generic;
using System.Drawing;
using Kingdee.BOS;
using Kingdee.BOS.Core.List;
using Kingdee.BOS.Core.List.PlugIn;
using Kingdee.BOS.Core.List.PlugIn.Args;
using Kingdee.BOS.Core.SqlBuilder;
using Kingdee.BOS.Core.CommonFilter;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    public class {BillName}ListPlugIn : AbstractListPlugin
    {
        #region 动态过滤
        public override void PrepareFilterParameter(FilterParameterArgs e)
        {
            base.PrepareFilterParameter(e);
            if (e.FilterParameter?.Filter == null) return;

            // 固定过滤：只显示当前用户创建的单据
            e.FilterParameter.Filter.Add(
                new FilterItem("FCreatorId", CompareType.Equals, this.Context.UserId)
            );

            // 日期范围过滤
            e.FilterParameter.Filter.Add(
                new FilterItem("FDate", CompareType.GreaterThanOrEquals, DateTime.Today.AddDays(-30))
            );
        }
        #endregion

        #region 按钮点击
        public override void BarItemClick(BarItemClickEventArgs e)
        {
            base.BarItemClick(e);
            if (string.IsNullOrEmpty(e.BarItemKey)) return;

            switch (e.BarItemKey.ToUpperInvariant())
            {
                case "TBBATCHAPPROVE":
                    OnBatchApprove();
                    break;
            }
        }

        private void OnBatchApprove()
        {
            var selectedRows = this.ListView.SelectedRowsInfo;
            if (selectedRows == null || selectedRows.Count == 0)
            {
                this.View.ShowMessage("请先选择要操作的行！");
                return;
            }

            try
            {
                foreach (var row in selectedRows)
                {
                    string billId = row.PrimaryKeyValue;
                    // 执行操作...
                }

                this.View.ShowMessage("批量操作完成");
                this.View.RefreshList();
            }
            catch (Exception ex)
            {
                this.View.ShowErrMessage($"批量操作失败：{ex.Message}");
            }
        }
        #endregion

        #region 行着色
        public override void FormatRowCondition(FormatRowConditionArgs e)
        {
            base.FormatRowCondition(e);
            if (e.DataRow == null) return;

            string status = e.DataRow["FBillStatus"]?.ToString();
            switch (status)
            {
                case "A": // 暂存
                    e.FormatCondition.BackColor = Color.LightYellow;
                    break;
                case "B": // 提交
                    e.FormatCondition.BackColor = Color.LightBlue;
                    break;
                case "C": // 审核
                    e.FormatCondition.BackColor = Color.LightGreen;
                    break;
                case "D": // 关闭
                    e.FormatCondition.ForeColor = Color.Gray;
                    break;
            }
        }
        #endregion
    }
}
```

---

## 操作插件模板

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using Kingdee.BOS;
using Kingdee.BOS.Core.DynamicForm;
using Kingdee.BOS.Core.DynamicForm.PlugIn;
using Kingdee.BOS.Core.DynamicForm.PlugIn.Args;
using Kingdee.BOS.Core.Metadata;
using Kingdee.BOS.Core.Metadata.Entity;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.ServiceHelper;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    public class {BillName}{OperationName}PlugIn : AbstractOperationServicePlugIn
    {
        #region 指定加载字段
        public override void OnPreparePropertys(PreparePropertysEventArgs e)
        {
            base.OnPreparePropertys(e);

            e.FieldKeys.Add("FBillNo");
            e.FieldKeys.Add("FMaterialId");
            e.FieldKeys.Add("FQty");
            e.FieldKeys.Add("FPrice");
            e.FieldKeys.Add("FAmount");
            e.FieldKeys.Add("FCustomerId");
            e.FieldKeys.Add("FEntryID");
        }
        #endregion

        #region 操作前校验与拦截
        public override void BeforeExecuteOperationTransaction(BeforeExecuteOperationTransaction e)
        {
            base.BeforeExecuteOperationTransaction(e);
            if (e.DataObjects == null || e.DataObjects.Length == 0) return;

            foreach (DynamicObject dataObj in e.DataObjects)
            {
                decimal amount = Convert.ToDecimal(dataObj["FAmount"] ?? 0);
                if (amount <= 0)
                {
                    e.CancelFormMessage = "金额必须大于0！";
                    e.CancelOperation = true;
                    return;
                }

                Entity entryEntity = e.BillBusinessInfo.GetEntity("FEntity");
                DynamicObjectCollection entryRows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;
                if (entryRows == null || entryRows.Count == 0)
                {
                    e.CancelFormMessage = "明细行不能为空！";
                    e.CancelOperation = true;
                    return;
                }

                foreach (DynamicObject row in entryRows)
                {
                    decimal qty = Convert.ToDecimal(row["FQty"] ?? 0);
                    if (qty <= 0)
                    {
                        e.CancelFormMessage = "明细行数量必须大于0！";
                        e.CancelOperation = true;
                        return;
                    }
                }
            }
        }
        #endregion

        #region 操作后处理
        public override void AfterExecuteOperationTransaction(AfterExecuteOperationTransaction e)
        {
            base.AfterExecuteOperationTransaction(e);
            if (e.DataObjects == null || e.DataObjects.Length == 0) return;

            try
            {
                foreach (DynamicObject dataObj in e.DataObjects)
                {
                    string billNo = dataObj["FBillNo"]?.ToString() ?? string.Empty;
                    // 操作后业务逻辑：写日志、调外部接口、生成下游单据等
                }
            }
            catch (Exception ex)
            {
                // 操作后异常通常不取消事务，但应记录日志
                Logger.Error($"操作后处理异常：{ex.Message}", "MyPlugin", ex);
            }
        }
        #endregion
    }
}
```

---

## 报表插件模板

```csharp
using System;
using System.Data;
using System.Collections.Generic;
using System.ComponentModel;
using Kingdee.BOS;
using Kingdee.BOS.Core.Report;
using Kingdee.BOS.Core.Report.PlugIn;
using Kingdee.BOS.Core.Report.PlugIn.Args;
using Kingdee.BOS.Core.SqlBuilder;
using Kingdee.BOS.App.Core.Report;
using Kingdee.BOS.ServiceHelper;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    [Description("{ReportName}")]
    public class {ReportName}ReportPlugIn : AbstractSysReportServicePlugIn
    {
        public override void GetSchema(GetSchemaEventArgs e)
        {
            base.GetSchema(e);

            var schema = new ReportSchema();
            schema.AddColumn("FBillNo", "单据编号", SqlStorageType.NVarChar, 50);
            schema.AddColumn("FDate", "日期", SqlStorageType.DateTime);
            schema.AddColumn("FMaterialNumber", "物料编码", SqlStorageType.NVarChar, 50);
            schema.AddColumn("FMaterialName", "物料名称", SqlStorageType.NVarChar, 200);
            schema.AddColumn("FQty", "数量", SqlStorageType.Decimal);
            schema.AddColumn("FAmount", "金额", SqlStorageType.Decimal);

            e.Schema = schema;
        }

        public override void GetData(GetDataEventArgs e)
        {
            base.GetData(e);

            string beginDate = e.FilterParameter?.GetFilterValue("FBeginDate")?.ToString();
            string endDate = e.FilterParameter?.GetFilterValue("FEndDate")?.ToString();

            string sql = @"
                SELECT t0.FBILLNO AS FBillNo
                      ,t0.FDATE AS FDate
                      ,mat.FNUMBER AS FMaterialNumber
                      ,mat_L.FNAME AS FMaterialName
                      ,SUM(entry.FQTY) AS FQty
                      ,SUM(entry.FAMOUNT) AS FAmount
                FROM T_SAL_OUTSTOCK t0
                INNER JOIN T_SAL_OUTSTOCKENTRY entry ON entry.FID = t0.FID
                INNER JOIN T_BD_MATERIAL mat ON mat.FMATERIALID = entry.FMATERIALID
                INNER JOIN T_BD_MATERIAL_L mat_L ON mat_L.FMATERIALID = mat.FMATERIALID AND mat_L.FLOCALEID = 2052
                WHERE 1=1";

            var paramList = new List<SqlParam>();

            if (!string.IsNullOrEmpty(beginDate))
            {
                sql += " AND t0.FDATE >= @BeginDate";
                paramList.Add(new SqlParam("@BeginDate", SqlDbType.DateTime, Convert.ToDateTime(beginDate)));
            }
            if (!string.IsNullOrEmpty(endDate))
            {
                sql += " AND t0.FDATE <= @EndDate";
                paramList.Add(new SqlParam("@EndDate", SqlDbType.DateTime, Convert.ToDateTime(endDate)));
            }

            sql += " GROUP BY t0.FBILLNO, t0.FDATE, mat.FNUMBER, mat_L.FNAME";

            DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, paramList.ToArray());
            e.Data = ds.Tables[0];
        }
    }
}
```

---

## 单据转换插件模板

```csharp
using System;
using System.Collections.Generic;
using Kingdee.BOS;
using Kingdee.BOS.Core.Convert;
using Kingdee.BOS.Core.Convert.PlugIn;
using Kingdee.BOS.Core.Convert.PlugIn.Args;
using Kingdee.BOS.Core.Metadata;
using Kingdee.BOS.Core.Metadata.Entity;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    public class {SourceBill}To{TargetBill}ConvertPlugIn : AbstractConvertPlugIn
    {
        public override void AfterConvert(AfterConvertEventArgs e)
        {
            base.AfterConvert(e);
            if (e.TargetDatas == null || e.TargetBusinessInfo == null) return;

            foreach (DynamicObject targetObj in e.TargetDatas)
            {
                targetObj["FNote"] = "由源单下推生成";

                Entity targetEntry = e.TargetBusinessInfo.GetEntity("FEntity");
                DynamicObjectCollection entryRows = targetEntry.DynamicProperty.GetValue(targetObj) as DynamicObjectCollection;
                if (entryRows == null) continue;

                foreach (DynamicObject row in entryRows)
                {
                    // 自定义转换逻辑
                    // decimal qty = Convert.ToDecimal(row["FQty"] ?? 0);
                    // row["FNote"] = $"原数量:{qty}";
                }
            }
        }

        // public override void OnFieldConvert(FieldConvertEventArgs e)
        // {
        //     base.OnFieldConvert(e);
        //     if (e.TargetFieldKey == "FMyField")
        //     {
        //         e.Result = $"{e.SourceFieldValue}_Converted";
        //     }
        // }
    }
}
```

---

## 服务插件模板

```csharp
using System;
using System.Data;
using System.Collections.Generic;
using System.Web;
using Kingdee.BOS;
using Kingdee.BOS.App.Core.ServiceHandler;
using Kingdee.BOS.ServiceHandler;
using Kingdee.BOS.ServiceHelper;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    /// <summary>
    /// 自定义WebAPI服务
    /// 调用地址：http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.CustomBusinessService.DoAction.common
    /// 参数 svcName = MyCustomApi
    /// </summary>
    [ServiceDescriptor("MyCustomApi")]
    public class MyCustomApiService : AbstractServiceHandler
    {
        public override InvokeResult DoAction(InvokeContext context)
        {
            var result = new InvokeResult();

            try
            {
                string action = context.RequestData["action"]?.ToString();
                string param1 = context.RequestData["param1"]?.ToString();

                switch (action?.ToUpperInvariant())
                {
                    case "QUERYDATA":
                        result.ResultData = QueryData(context, param1);
                        break;
                    case "SAVEDATA":
                        result.ResultData = SaveData(context, param1);
                        break;
                    default:
                        result.ResultData = new { success = false, message = "未知的操作类型" };
                        break;
                }
            }
            catch (Exception ex)
            {
                result.ResultData = new { success = false, message = ex.Message };
                Logger.Error($"MyCustomApi 异常：{ex.Message}", "MyCustomApi", ex);
            }

            return result;
        }

        private object QueryData(InvokeContext context, string param1)
        {
            string sql = "SELECT FMATERIALID, FNUMBER, FNAME FROM T_BD_MATERIAL WHERE FNUMBER = @Number";
            var paramList = new List<SqlParam>
            {
                new SqlParam("@Number", SqlDbType.NVarChar, param1)
            };

            DataSet ds = DBServiceHelper.ExecuteDataSet(context.Context, sql, paramList.ToArray());
            return new { success = true, data = ds.Tables[0] };
        }

        private object SaveData(InvokeContext context, string param1)
        {
            return new { success = true, message = "保存成功" };
        }
    }
}
```

---

## 审批流插件模板

```csharp
using System;
using System.Collections.Generic;
using Kingdee.BOS;
using Kingdee.BOS.Core.DynamicForm;
using Kingdee.BOS.Core.DynamicForm.PlugIn;
using Kingdee.BOS.Core.DynamicForm.PlugIn.Args;
using Kingdee.BOS.Core.Metadata;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Workflow.PlugIn;
using Kingdee.BOS.Workflow.PlugIn.Args;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    /// <summary>
    /// 审批流插件：处理审批节点前后事件
    /// 注册位置：BOS IDE → 流程模型 → 流程插件
    /// </summary>
    public class {BillName}WorkflowPlugIn : AbstractWorkflowPlugin
    {
        public override void BeforeExecute(BeforeExecuteArgs e)
        {
            base.BeforeExecute(e);
            // 节点执行前：可动态设置审批人、校验条件
        }

        public override void AfterExecute(AfterExecuteArgs e)
        {
            base.AfterExecute(e);
            // 节点执行后：可发送通知、写业务日志
        }

        public override void OnProcessNodeExecuteComplete(ProcessNodeExecuteCompleteArgs e)
        {
            base.OnProcessNodeExecuteComplete(e);
            // 节点处理完成后：如自动审批、跳转
        }

        public override void OnProcessStarted(ProcessStartedArgs e)
        {
            base.OnProcessStarted(e);
            // 流程启动时：初始化流程变量
        }
    }
}
```

### 动态设置审批人示例

```csharp
public override void BeforeExecute(BeforeExecuteArgs e)
{
    base.BeforeExecute(e);

    // 根据单据金额动态设置审批人
    DynamicObject billObj = e.BusinessInfo.GetDynamicValue(e.DataEntity, "FBillHead") as DynamicObject;
    decimal amount = Convert.ToDecimal(billObj?["FAmount"] ?? 0);

    long approverId = amount > 100000
        ? 100001L  // 高级审批人
        : 100002L; // 普通审批人

    e.Context.SetApprover(approverId);
}
```

---

## 多组织与权限场景

### 1. 获取当前用户组织信息

```csharp
long userId = this.Context.UserId;
string userName = this.Context.UserName;

// 当前登录组织
long orgId = this.Context.CurrentOrganizationInfo.ID;
string orgNumber = this.Context.CurrentOrganizationInfo.Code;
string orgName = this.Context.CurrentOrganizationInfo.Name;

// 用户所属组织列表
var orgList = this.Context.UserOrganizationInfo;
```

### 2. 数据范围过滤（只查本组织）

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

### 3. 字段级权限判断

```csharp
public override void AfterBindData(EventArgs e)
{
    base.AfterBindData(e);

    // 判断当前用户是否有某个字段的编辑权限（需根据实际权限服务调整）
    bool hasEditPermission = PermissionServiceHelper.HasFieldPermission(
        this.Context,
        this.View.BillBusinessInfo.GetForm().Id,
        "FPrice",
        "Edit"
    );

    if (!hasEditPermission)
    {
        this.View.GetControl("FPrice").Enabled = false;
    }
}
```

### 4. SQL 参数化（防注入）

```csharp
string sql = "SELECT FNAME FROM T_BD_MATERIAL_L WHERE FMATERIALID = @Id AND FLOCALEID = 2052";
var param = new SqlParam[]
{
    new SqlParam("@Id", SqlDbType.BigInt, materialId)
};
DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
```

---

## 复杂项目案例

### 案例1：销售订单按可用库存拆分批次下推发货通知

**需求**：销售订单下推发货通知时，按物料现有库存自动拆分批次，并写入发货通知单的批次字段。

```csharp
public class SALOrderToDeliveryConvertPlugIn : AbstractConvertPlugIn
{
    public override void AfterConvert(AfterConvertEventArgs e)
    {
        base.AfterConvert(e);
        if (e.TargetDatas == null) return;

        foreach (DynamicObject deliveryObj in e.TargetDatas)
        {
            Entity entryEntity = e.TargetBusinessInfo.GetEntity("FEntity");
            DynamicObjectCollection deliveryRows = entryEntity.DynamicProperty.GetValue(deliveryObj) as DynamicObjectCollection;
            if (deliveryRows == null) continue;

            foreach (DynamicObject row in deliveryRows)
            {
                long materialId = (row["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0;
                decimal qty = Convert.ToDecimal(row["FQty"] ?? 0);

                if (materialId == 0 || qty <= 0) continue;

                // 查询可用库存批次（按先进先出）
                string sql = @"
                    SELECT TOP 1 FLOT, FQTY
                    FROM (
                        SELECT ISNULL(inv.FLOT, 0) AS FLOT, SUM(inv.FQTY) AS FQTY
                        FROM T_STK_INVENTORY inv
                        WHERE inv.FMATERIALID = @MaterialId AND inv.FQTY > 0
                        GROUP BY inv.FLOT
                    ) t
                    ORDER BY FLOT ASC";

                var param = new SqlParam[]
                {
                    new SqlParam("@MaterialId", SqlDbType.BigInt, materialId)
                };

                DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
                if (ds.Tables[0].Rows.Count > 0)
                {
                    long lot = Convert.ToInt64(ds.Tables[0].Rows[0]["FLOT"]);
                    row["FLot"] = lot;
                }
            }
        }
    }
}
```

### 案例2：应收单审核后自动生成凭证

**需求**：应收单审核通过后，调用总账接口自动生成凭证。

```csharp
public class ARReceivableAuditPlugIn : AbstractOperationServicePlugIn
{
    public override void AfterExecuteOperationTransaction(AfterExecuteOperationTransaction e)
    {
        base.AfterExecuteOperationTransaction(e);
        if (e.DataObjects == null) return;

        foreach (DynamicObject dataObj in e.DataObjects)
        {
            string billNo = dataObj["FBillNo"]?.ToString() ?? string.Empty;
            long billId = (dataObj["Id"] as long?) ?? 0;

            if (billId <= 0) continue;

            try
            {
                // 构造凭证数据（需根据实际科目映射表调整）
                var voucherData = BuildVoucherData(dataObj);
                VoucherServiceHelper.CreateVoucher(this.Context, voucherData);
                Logger.Info($"应收单 {billNo} 已自动生成凭证", "ARAudit");
            }
            catch (Exception ex)
            {
                Logger.Error($"应收单 {billNo} 生成凭证失败：{ex.Message}", "ARAudit", ex);
            }
        }
    }

    private object BuildVoucherData(DynamicObject billObj)
    {
        // 实际实现需根据凭证模板组装
        return new { };
    }
}
```

### 案例3：跨组织调拨自动按目标组织价格重写

**需求**：直接调拨单保存时，如果源组织与目标组织不同，按目标组织价目表重新取价。

```csharp
public class STKTransferDirectSavePlugIn : AbstractOperationServicePlugIn
{
    public override void OnPreparePropertys(PreparePropertysEventArgs e)
    {
        base.OnPreparePropertys(e);
        e.FieldKeys.Add("FStockOrgId");
        e.FieldKeys.Add("FReceiveOrgId");
        e.FieldKeys.Add("FMaterialId");
        e.FieldKeys.Add("FPrice");
        e.FieldKeys.Add("FAmount");
    }

    public override void BeforeExecuteOperationTransaction(BeforeExecuteOperationTransaction e)
    {
        base.BeforeExecuteOperationTransaction(e);
        if (e.DataObjects == null) return;

        foreach (DynamicObject dataObj in e.DataObjects)
        {
            long srcOrg = (dataObj["FStockOrgId"] as DynamicObject)?["Id"] as long? ?? 0;
            long targetOrg = (dataObj["FReceiveOrgId"] as DynamicObject)?["Id"] as long? ?? 0;
            if (srcOrg == targetOrg) continue;

            Entity entryEntity = e.BillBusinessInfo.GetEntity("FEntity");
            DynamicObjectCollection rows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;
            if (rows == null) continue;

            foreach (DynamicObject row in rows)
            {
                long materialId = (row["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0;
                decimal qty = Convert.ToDecimal(row["FQty"] ?? 0);
                decimal price = GetPriceByOrgAndMaterial(targetOrg, materialId);

                row["FPrice"] = price;
                row["FAmount"] = qty * price;
            }
        }
    }

    private decimal GetPriceByOrgAndMaterial(long orgId, long materialId)
    {
        // 查询目标组织价目表
        string sql = @"
            SELECT TOP 1 FPRICE
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
}
```

---

## 常用代码片段

### 查询基础资料

```csharp
var material = BusinessDataServiceHelper.LoadSingle(
    this.Context,
    "BD_Material",
    new OQLFilter(new OQLFilterHeadEntityItem
    {
        FilterItems = new List<FilterItem>
        {
            new FilterItem("FNumber", CompareType.Equals, "MAT001")
        }
    })
);
```

### 执行 SQL

```csharp
// 查询
string sql = "SELECT FNAME FROM T_BD_MATERIAL_L WHERE FMATERIALID = @Id AND FLOCALEID = 2052";
var param = new SqlParam[]
{
    new SqlParam("@Id", SqlDbType.BigInt, materialId)
};
DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);

// 非查询
string updateSql = "UPDATE T_MY_TABLE SET FSTATUS = @Status WHERE FID = @Id";
var updateParams = new SqlParam[]
{
    new SqlParam("@Status", SqlDbType.Int, 1),
    new SqlParam("@Id", SqlDbType.BigInt, billId)
};
DBServiceHelper.ExecuteNonQuery(this.Context, updateSql, updateParams);
```

### 弹窗确认

```csharp
this.View.ShowConfirmMessage(
    "确认要执行此操作吗？",
    MessageBoxOptions.YesNo,
    delegate (ConfirmResultEventArgs confirmArgs)
    {
        if (confirmArgs.Result == MessageBoxResult.Yes)
        {
            // 确认后的逻辑
        }
    }
);
```

### 通知提醒

```csharp
this.View.ShowMessage("操作成功", MessageBoxType.Notice);
this.View.ShowErrMessage($"操作失败：{ex.Message}");
this.View.ShowWarningMessage("请注意：数据可能不完整");
```

### 基础资料字段赋值

```csharp
// 方式1：按编码设置
this.Model.SetItemValueByNumber("FMaterialId", "MAT001", rowIndex);

// 方式2：通过 DynamicObject 设置
DynamicObject material = BusinessDataServiceHelper.LoadSingle(this.Context, "BD_Material", ...);
this.Model.SetValue("FMaterialId", material, rowIndex);
```

### 单据体行操作

```csharp
// 新增行
int newRow = this.Model.CreateNewEntryRow("FEntity");
this.Model.SetValue("FMaterialId", material, newRow);

// 删除行
this.Model.DeleteEntryData("FEntity", rowIndex);

// 获取当前行
int currentRow = this.Model.GetEntryCurrentRowIndex("FEntity");
```

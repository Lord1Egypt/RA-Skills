# 金蝶云星空插件代码模板库

## 目录
- [表单插件模板](#表单插件模板)
- [列表插件模板](#列表插件模板)
- [操作插件模板](#操作插件模板)
- [报表插件模板](#报表插件模板)
- [单据转换插件模板](#单据转换插件模板)
- [自定义WebAPI服务模板](#自定义webapi服务模板)
- [常用代码片段](#常用代码片段)

---

## 表单插件模板

### 完整模板

``csharp
using System;
using System.Collections.Generic;
using System.Linq;
using Kingdee.BOS;
using Kingdee.BOS.Core.DynamicForm;
using Kingdee.BOS.Core.DynamicForm.PlugIn;
using Kingdee.BOS.Core.Metadata;
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

            switch (e.Field.Key.ToUpper())
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

            // 带出单位
            DynamicObject baseUnit = material["BaseUnitId"] as DynamicObject;
            int rowIndex = this.Model.GetEntryCurrentRow("FEntity");
            if (baseUnit != null)
            {
                this.Model.SetValue("FUnitId", baseUnit, rowIndex);
            }
        }

        private void OnQtyOrPriceChanged(DataChangedEventArgs e)
        {
            int rowIndex = this.Model.GetEntryCurrentRow("FEntity");
            decimal qty = Convert.ToDecimal(this.Model.GetValue("FQty", rowIndex));
            decimal price = Convert.ToDecimal(this.Model.GetValue("FPrice", rowIndex));
            decimal amount = qty * price;
            this.Model.SetValue("FAmount", amount, rowIndex);
        }
        #endregion

        #region 按钮点击
        public override void BarItemClick(BarItemClickEventArgs e)
        {
            base.BarItemClick(e);

            switch (e.BarItemKey.ToUpper())
            {
                case "TBCUSTOMBTN":  // 自定义按钮
                    OnCustomButtonClick();
                    break;
            }
        }

        private void OnCustomButtonClick()
        {
            // 获取当前数据
            DynamicObject dataObj = this.Model.DataObject;
            string billNo = dataObj["FBillNo"]?.ToString();

            // 执行业务逻辑...

            // 提示并刷新
            this.View.ShowMessage($""单据 {billNo} 处理完成"");
            this.View.UpdateView();
        }
        #endregion

        #region 界面加载后
        public override void AfterBindData(EventArgs e)
        {
            base.AfterBindData(e);

            // 根据单据状态控制界面
            string billStatus = (this.Model.GetValue("FBillStatus") as DynamicObject)?["Id"]?.ToString();
            if (billStatus == "C") // 已审核
            {
                this.View.GetControl("FNumber").Enabled = false;
            }
        }
        #endregion

        #region 打开表单前
        public override void PreOpenForm(PreOpenFormEventArgs e)
        {
            base.PreOpenForm(e);

            // 接收传参
            if (e.OpenParameter.CustomParams.ContainsKey(""FParam1""))
            {
                string param1 = e.OpenParameter.CustomParams[""FParam1""];
                // 可以将参数缓存，在 AfterBindData 中使用
            }
        }
        #endregion
    }
}
``

---

## 列表插件模板

``csharp
using System;
using System.Data;
using System.Collections.Generic;
using Kingdee.BOS;
using Kingdee.BOS.Core.List;
using Kingdee.BOS.Core.List.PlugIn;
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

            // 固定过滤：当前用户
            // e.FilterParameter.Filter.Add(new FilterItem(""FCreatorId"", CompareType.Equals, this.Context.UserId));

            // 日期范围过滤
            // e.FilterParameter.Filter.Add(new FilterItem(""FDate"", CompareType.GreaterThanOrEquals, DateTime.Today.AddDays(-30)));

            // 自定义过滤条件字符串
            // e.FilterParameter.CustomFilter = "" FDate >= '2024-01-01' "";
        }
        #endregion

        #region 按钮点击
        public override void BarItemClick(BarItemClickEventArgs e)
        {
            base.BarItemClick(e);

            switch (e.BarItemKey.ToUpper())
            {
                case "TBBATCHAPPROVE":  // 批量审核按钮
                    OnBatchApprove();
                    break;
            }
        }

        private void OnBatchApprove()
        {
            // 获取选中的行
            var selectedRows = this.ListView.SelectedRowsInfo;
            if (selectedRows == null || selectedRows.Count == 0)
            {
                this.View.ShowMessage(""请先选择要操作的行！"");
                return;
            }

            // 逐行处理
            foreach (var row in selectedRows)
            {
                string billId = row.PrimaryKeyValue;
                // 执行操作...
            }

            this.View.ShowMessage(""批量操作完成"");
            this.View.RefreshList();
        }
        #endregion

        #region 行着色
        public override void FormatRowCondition(FormatRowConditionArgs e)
        {
            base.FormatRowCondition(e);

            // 根据状态着色
            // string status = e.DataRow[""FBillStatus""]?.ToString();
            // if (status == ""D"") e.FormatCondition.ForeColor = System.Drawing.Color.Gray;
        }
        #endregion
    }
}
``

---

## 操作插件模板

``csharp
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

            // 操作插件默认不加载所有字段，必须显式声明需要的字段
            e.FieldKeys.Add("FBillNo");
            e.FieldKeys.Add("FMaterialId");
            e.FieldKeys.Add("FQty");
            e.FieldKeys.Add("FPrice");
            e.FieldKeys.Add("FAmount");
            e.FieldKeys.Add("FCustomerId");
        }
        #endregion

        #region 操作前校验与拦截
        public override void BeforeExecuteOperationTransaction(BeforeExecuteOperationTransaction e)
        {
            base.BeforeExecuteOperationTransaction(e);

            foreach (DynamicObject dataObj in e.DataObjects)
            {
                // ===== 校验示例 =====

                // 1. 金额校验
                decimal amount = Convert.ToDecimal(dataObj["FAmount"]);
                if (amount <= 0)
                {
                    e.CancelFormMessage = ""金额必须大于0！"";
                    e.CancelOperation = true;
                    return;
                }

                // 2. 明细行校验
                Entity entryEntity = e.BillBusinessInfo.GetEntity("FEntity");
                DynamicObjectCollection entryRows = entryEntity.DynamicProperty.GetValue(dataObj) as DynamicObjectCollection;
                if (entryRows == null || entryRows.Count == 0)
                {
                    e.CancelFormMessage = ""明细行不能为空！"";
                    e.CancelOperation = true;
                    return;
                }

                // 3. 逐行校验
                foreach (DynamicObject row in entryRows)
                {
                    decimal qty = Convert.ToDecimal(row["FQty"]);
                    if (qty <= 0)
                    {
                        e.CancelFormMessage = ""明细行数量必须大于0！"";
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

            foreach (DynamicObject dataObj in e.DataObjects)
            {
                string billNo = dataObj["FBillNo"]?.ToString();

                // ===== 操作后业务逻辑 =====

                // 示例1：记录日志
                // LogHelper.WriteLog($""单据 {billNo} 已审核"");

                // 示例2：调用外部接口
                // HttpClient client = new HttpClient();
                // var response = client.PostAsync(url, content).Result;

                // 示例3：修改关联数据
                // BusinessDataServiceHelper.Save(this.Context, relatedBillInfo, relatedDataObj);

                // 示例4：发通知
                // SendMessage(billNo);
            }
        }
        #endregion
    }
}
``

---

## 报表插件模板

``csharp
using System;
using System.Data;
using System.Collections.Generic;
using System.ComponentModel;
using Kingdee.BOS;
using Kingdee.BOS.Core.Report;
using Kingdee.BOS.Core.Report.PlugIn;
using Kingdee.BOS.Core.SqlBuilder;
using Kingdee.BOS.App.Core;
using Kingdee.BOS.ServiceHelper;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    [Description(""{ReportName}"")]
    public class {ReportName}ReportPlugIn : AbstractSysReportServicePlugIn
    {
        #region 定义报表结构
        public override void GetSchema(GetSchemaEventArgs e)
        {
            base.GetSchema(e);

            var schema = new ReportSchema();

            // 定义列
            schema.AddColumn("FBillNo", "单据编号", SqlStorageType.NVarChar, 50);
            schema.AddColumn("FDate", "日期", SqlStorageType.DateTime);
            schema.AddColumn("FMaterialNumber", "物料编码", SqlStorageType.NVarChar, 50);
            schema.AddColumn("FMaterialName", "物料名称", SqlStorageType.NVarChar, 200);
            schema.AddColumn("FQty", "数量", SqlStorageType.Decimal);
            schema.AddColumn("FAmount", "金额", SqlStorageType.Decimal);

            e.Schema = schema;
        }
        #endregion

        #region 查询报表数据
        public override void GetData(GetDataEventArgs e)
        {
            base.GetData(e);

            // 获取过滤参数
            string beginDate = e.FilterParameter?.GetFilterValue("FBeginDate")?.ToString();
            string endDate = e.FilterParameter?.GetFilterValue("FEndDate")?.ToString();

            // 构建SQL
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
                sql += "" AND t0.FDATE >= @BeginDate"";
                paramList.Add(new SqlParam(""@BeginDate"", SqlDbType.DateTime, Convert.ToDateTime(beginDate)));
            }
            if (!string.IsNullOrEmpty(endDate))
            {
                sql += "" AND t0.FDATE <= @EndDate"";
                paramList.Add(new SqlParam(""@EndDate"", SqlDbType.DateTime, Convert.ToDateTime(endDate)));
            }

            sql += "" GROUP BY t0.FBILLNO, t0.FDATE, mat.FNUMBER, mat_L.FNAME"";

            // 执行查询
            DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, paramList.ToArray());
            e.Data = ds.Tables[0];
        }
        #endregion
    }
}
``

---

## 单据转换插件模板

``csharp
using System;
using System.Collections.Generic;
using Kingdee.BOS;
using Kingdee.BOS.Core.Convert;
using Kingdee.BOS.Core.Convert.PlugIn;
using Kingdee.BOS.Core.Metadata;
using Kingdee.BOS.Core.Metadata.Entity;
using Kingdee.BOS.Orm.DataEntity;
using Kingdee.BOS.Util;

namespace MyCompany.K3.PlugIns
{
    public class {SourceBill}To{TargetBill}ConvertPlugIn : AbstractConvertPlugIn
    {
        #region 转换后填充
        public override void AfterConvert(AfterConvertEventArgs e)
        {
            base.AfterConvert(e);

            foreach (DynamicObject targetObj in e.TargetDatas)
            {
                // 填充目标单据头字段
                targetObj["FNote"] = ""由源单下推生成"";

                // 填充目标单据体
                Entity targetEntry = e.TargetBusinessInfo.GetEntity("FEntity");
                DynamicObjectCollection entryRows = targetEntry.DynamicProperty.GetValue(targetObj) as DynamicObjectCollection;

                if (entryRows != null)
                {
                    foreach (DynamicObject row in entryRows)
                    {
                        // 自定义转换逻辑
                        // decimal qty = Convert.ToDecimal(row[""FQty""]);
                        // row[""FNote""] = $""数量:{qty}"";
                    }
                }
            }
        }
        #endregion

        #region 单字段转换
        // public override void OnFieldConvert(FieldConvertEventArgs e)
        // {
        //     base.OnFieldConvert(e);
        //
        //     // 自定义单个字段的映射逻辑
        //     if (e.TargetFieldKey == "FMyField")
        //     {
        //         e.Result = e.SourceFieldValue + ""_Converted"";
        //     }
        // }
        #endregion
    }
}
``

---

## 自定义WebAPI服务模板

``csharp
using System;
using System.Collections.Generic;
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
    /// 注册后可通过 http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.CustomBusinessService.DoAction.common 
    /// 调用，参数 svcName = MyCustomApi
    /// </summary>
    [ServiceDescriptor(""MyCustomApi"")]
    public class MyCustomApiService : AbstractServiceHandler
    {
        public override InvokeResult DoAction(InvokeContext context)
        {
            var result = new InvokeResult();

            try
            {
                // 获取参数
                string action = context.RequestData[""action""]?.ToString();
                string param1 = context.RequestData[""param1""]?.ToString();

                switch (action)
                {
                    case ""QueryData"":
                        result.ResultData = QueryData(context, param1);
                        break;
                    case ""SaveData"":
                        result.ResultData = SaveData(context, param1);
                        break;
                    default:
                        result.ResultData = new { success = false, message = ""未知的操作类型"" };
                        break;
                }
            }
            catch (Exception ex)
            {
                result.ResultData = new { success = false, message = ex.Message, stackTrace = ex.StackTrace };
            }

            return result;
        }

        private object QueryData(InvokeContext context, string param1)
        {
            // 查询逻辑
            string sql = ""SELECT * FROM T_BD_MATERIAL WHERE FNUMBER = @Number"";
            var paramList = new List<SqlParam>();
            paramList.Add(new SqlParam(""@Number"", System.Data.SqlDbType.NVarChar, param1));

            DataSet ds = DBServiceHelper.ExecuteDataSet(context.Context, sql, paramList.ToArray());

            return new { success = true, data = ds };
        }

        private object SaveData(InvokeContext context, string param1)
        {
            // 保存逻辑
            return new { success = true, message = ""保存成功"" };
        }
    }
}
``

---

## 常用代码片段

### 查询基础资料

``csharp
// 按编码查询物料
var material = BusinessDataServiceHelper.LoadSingle(this.Context, ""BD_Material"",
    new OQLFilter { new OQLFilterHeadEntityItem {
        FilterItems = new List<FilterItem> {
            new FilterItem(""Number"", CompareType.Equals, ""MAT001"")
        }
    }
});
``

### 执行SQL

``csharp
// 查询
string sql = ""SELECT FNAME FROM T_BD_MATERIAL_L WHERE FMATERIALID = @Id AND FLOCALEID = 2052"";
var param = new SqlParam[] { new SqlParam(""@Id"", SqlDbType.Int, materialId) };
DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
string name = ds.Tables[0].Rows[0][""FNAME""].ToString();

// 执行非查询
string updateSql = ""UPDATE T_MY_TABLE SET FSTATUS = @Status WHERE FID = @Id"";
var updateParams = new SqlParam[] {
    new SqlParam(""@Status"", SqlDbType.Int, 1),
    new SqlParam(""@Id"", SqlDbType.Int, billId)
};
DBServiceHelper.ExecuteNonQuery(this.Context, updateSql, updateParams);
``

### 获取当前用户/组织信息

``csharp
long userId = this.Context.UserId;              // 当前用户ID
string userName = this.Context.UserName;         // 当前用户名
long orgId = this.Context.CurrentOrganizationInfo.ID;  // 当前组织ID
``

### 弹窗确认

``csharp
this.View.ShowConfirmMessage(""确认要执行此操作吗？"",
   MessageBoxOptions.YesNo,
   delegate(ConfirmResultEventArgs confirmArgs)
    {
        if (confirmArgs.Result == MessageBoxResult.Yes)
        {
            // 确认后的逻辑
        }
    });
``

### 通知提醒

``csharp
this.View.ShowMessage(""操作成功"", MessageBoxType.Notice);
this.View.ShowErrMessage(""操作失败：" + ex.Message);
this.View.ShowWarningMessage(""请注意：数据可能不完整"");
``

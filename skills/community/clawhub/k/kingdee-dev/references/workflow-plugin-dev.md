# 金蝶云星空审批流插件开发指南

## 目录
- [概述](#概述)
- [审批流插件类型](#审批流插件类型)
- [插件事件与执行时机](#插件事件与执行时机)
- [动态设置审批人](#动态设置审批人)
- [跳过审批节点](#跳过审批节点)
- [转交、加签、会签](#转交加签会签)
- [审批后业务处理](#审批后业务处理)
- [插件注册](#插件注册)
- [常见问题](#常见问题)

---

## 概述

金蝶云星空审批流用于控制单据的审批流程。除了标准审批流配置外，常用二次开发场景包括：

- 根据单据金额、部门、优先级等动态设置审批人
- 根据条件自动跳过某些审批节点
- 审批通过后自动触发业务逻辑（如发通知、生成下游单据）
- 在审批节点前后插入自定义校验

## 审批流插件类型

| 插件类型 | 基类/接口 | 用途 |
|----------|-----------|------|
| 流程插件 | `AbstractWorkflowPlugin` | 流程级别事件（启动、结束、节点完成） |
| 节点插件 | `AbstractActivityPlugin` | 单个审批节点事件（前后执行） |
| 参与者插件 | `IParticipantPlugin` | 动态计算审批人 |

星空版本不同，审批流 API 命名空间可能略有差异，常见：
- `Kingdee.BOS.Workflow.PlugIn.*`
- `Kingdee.BOS.Workflow.PlugIn.Args.*`

## 插件事件与执行时机

### 流程插件事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `OnProcessStarted` | 流程启动后 | 初始化流程变量、记录启动日志 |
| `OnProcessNodeExecuteComplete` | 节点执行完成后 | 节点级后处理 |
| `OnProcessCompleted` | 流程完成后 | 发送通知、触发下游业务 |
| `OnProcessTerminated` | 流程终止时 | 清理资源、记录终止原因 |

### 节点插件事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `BeforeExecute` | 节点执行前 | 动态设置审批人、校验条件 |
| `AfterExecute` | 节点执行后 | 节点级后处理 |

## 动态设置审批人

```csharp
using Kingdee.BOS;
using Kingdee.BOS.Workflow.PlugIn;
using Kingdee.BOS.Workflow.PlugIn.Args;
using Kingdee.BOS.Orm.DataEntity;

public class SaleOrderWorkflowPlugIn : AbstractWorkflowPlugin
{
    public override void BeforeExecute(BeforeExecuteArgs e)
    {
        base.BeforeExecute(e);

        // 获取当前单据数据
        DynamicObject billObj = e.DataEntity as DynamicObject;
        if (billObj == null) return;

        decimal amount = Convert.ToDecimal(billObj["FAmount"] ?? 0);

        // 根据金额设置不同审批人
        long approverId;
        if (amount >= 500000)
        {
            approverId = 100001L; // 总经理
        }
        else if (amount >= 100000)
        {
            approverId = 100002L; // 部门经理
        }
        else
        {
            approverId = 100003L; // 主管
        }

        // 设置审批人（不同版本 API 可能不同，需根据实际环境调整）
        e.Context.SetApprover(approverId);
    }
}
```

### 按部门负责人设置审批人

```csharp
public override void BeforeExecute(BeforeExecuteArgs e)
{
    base.BeforeExecute(e);

    DynamicObject billObj = e.DataEntity as DynamicObject;
    if (billObj == null) return;

    DynamicObject deptObj = billObj["FDeptId"] as DynamicObject;
    long deptId = deptObj?["Id"] as long? ?? 0;

    if (deptId == 0) return;

    // 查询部门负责人（假设自定义表 T_BD_DEPT_MANAGER）
    string sql = "SELECT FManagerId FROM T_BD_DEPT_MANAGER WHERE FDeptId = @DeptId";
    var param = new SqlParam[]
    {
        new SqlParam("@DeptId", SqlDbType.BigInt, deptId)
    };

    DataSet ds = DBServiceHelper.ExecuteDataSet(this.Context, sql, param);
    if (ds.Tables[0].Rows.Count > 0)
    {
        long managerId = Convert.ToInt64(ds.Tables[0].Rows[0]["FManagerId"]);
        e.Context.SetApprover(managerId);
    }
}
```

## 跳过审批节点

```csharp
public override void BeforeExecute(BeforeExecuteArgs e)
{
    base.BeforeExecute(e);

    DynamicObject billObj = e.DataEntity as DynamicObject;
    if (billObj == null) return;

    // 金额小于 10000 的单据跳过当前审批节点
    decimal amount = Convert.ToDecimal(billObj["FAmount"] ?? 0);
    if (amount < 10000)
    {
        e.ExecuteSkip = true; // 跳过当前节点（具体属性名以实际 API 为准）
    }
}
```

> 注意：跳过审批节点可能受版本限制，部分版本需通过条件路由实现。

## 转交、加签、会签

### 转交

转交通常由用户在前端操作触发，插件中较少干预。若需强制转交，可通过修改参与者实现：

```csharp
public override void BeforeExecute(BeforeExecuteArgs e)
{
    base.BeforeExecute(e);

    // 将审批人强制转交给指定用户
    long newApproverId = 200001L;
    e.Context.SetApprover(newApproverId);
}
```

### 加签

加签指在当前审批节点临时增加审批人。部分版本支持通过 API 动态添加参与者：

```csharp
public override void BeforeExecute(BeforeExecuteArgs e)
{
    base.BeforeExecute(e);

    long additionalApproverId = 200002L;
    // 将当前审批人列表增加一人
    var participants = e.Context.GetParticipants()?.ToList() ?? new List<long>();
    participants.Add(additionalApproverId);
    e.Context.SetParticipants(participants.ToArray());
}
```

### 会签

会签指多个审批人必须全部同意才通过。此配置通常在 BOS IDE 的审批流设计器中设置：

1. 打开审批流设计器
2. 选择审批节点
3. 节点属性 → 审批方式 → 选择「会签」
4. 配置参与者来源（指定用户/角色/上下级）

## 审批后业务处理

```csharp
public class SaleOrderWorkflowAfterPlugIn : AbstractWorkflowPlugin
{
    public override void OnProcessCompleted(ProcessCompletedArgs e)
    {
        base.OnProcessCompleted(e);

        DynamicObject billObj = e.DataEntity as DynamicObject;
        if (billObj == null) return;

        string billNo = billObj["FBillNo"]?.ToString() ?? string.Empty;
        long billId = billObj["Id"] as long? ?? 0;

        try
        {
            // 发送通知
            SendApprovalCompleteMessage(billNo);

            // 记录审批日志
            Logger.Info($"销售订单 {billNo} 审批流程已完成", "Workflow");
        }
        catch (Exception ex)
        {
            Logger.Error($"审批完成后处理异常：{ex.Message}", "Workflow", ex);
        }
    }

    private void SendApprovalCompleteMessage(string billNo)
    {
        // 调用消息服务或 WebAPI 发送通知
    }
}
```

## 插件注册

1. 打开 BOS IDE
2. 找到目标流程模型
3. 右键 → 属性 → 流程插件
4. 新增 → 选择 dll 和类名
5. 保存 → 签入 → 发布

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 审批人不生效 | 参与者来源配置冲突 | 检查节点属性与插件是否同时设置了审批人 |
| 插件不触发 | 注册流程错误 | 确认注册到了正确的流程模型 |
| 审批流异常 | 插件中未做空判断 | 所有取值前判断 null |
| 无法跳过节点 | 版本不支持 | 改用条件路由或审批节点配置 |
| 会签不通过 | 节点配置问题 | 在设计器中检查会签/或签配置 |

# 金蝶云星空 WebAPI 接口开发

## 目录
- [概述](#概述)
- [认证方式](#认证方式)
- [核心接口](#核心接口)
- [请求参数格式](#请求参数格式)
- [批量操作接口](#批量操作接口)
- [自定义WebAPI开发](#自定义webapi开发)
- [SDK使用](#sdk使用)
- [常见问题](#常见问题)

---

## 概述

金蝶云星空提供标准 WebAPI 接口，支持第三方系统与星空数据交互。

**基础URL：** `http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.{Action}.common`

**官方文档：** https://vip.kingdee.com/knowledge/2569

---

## 认证方式

### 方式1：用户名密码登录

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.UserService.ValidateUser.common

{
    "acctID": "账套ID",
    "username": "用户名",
    "password": "密码",
    "lcid": 2052
}
``

返回 `LoginResultType` ：1=成功，其他=失败

### 方式2：API签名认证

1. 在星空后台「WebAPI」中注册应用，获取 AppId 和 AppSecret
2. 生成签名：`Sign = MD5(AppId + TimeStamp + AppSecret)`
3. 请求头添加：
   - `X-KD-AppId`：应用ID
   - `X-KD-TimeStamp`：时间戳
   - `X-KD-Sign`：签名

### 方式3：OAuth认证

适用于SaaS环境，通过 OAuth2.0 流程获取 access_token。

---

## 核心接口

### 保存（新增/修改）

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Save.common

{
    "formid": "SAL_SaleOrder",
    "data": {
        "Model": {
            "FBillNo": "",              // 留空自动生成
            "FDate": "2024-01-15",
            "FCustomerId": { "FNumber": "C001" },
            "FEntity": [
                {
                    "FMaterialId": { "FNumber": "MAT001" },
                    "FQty": 10,
                    "FPrice": 100.00,
                    "FAmount": 1000.00
                }
            ]
        }
    }
}
``

### 查询

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common

{
    "formid": "SAL_SaleOrder",
    "fieldKeys": "FBillNo,FDate,FCustomerId.FNumber,FAmount",
    "filterString": "FBillNo = 'SO2024001'",
    "orderString": "FBillNo ASC",
    "topRowCount": 100,
    "startRow": 0,
    "limit": 100
}
``

### 提交

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Submit.common

{
    "formid": "SAL_SaleOrder",
    "data": {
        "Ids": "100001,100002"
    }
}
``

### 审核

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Audit.common

{
    "formid": "SAL_SaleOrder",
    "data": {
        "Ids": "100001,100002"
    }
}
``

### 反审核

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.UnAudit.common
``

参数格式同审核。

### 删除

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Delete.common

{
    "formid": "SAL_SaleOrder",
    "data": {
        "Ids": "100001"
    }
}
``

### 分配

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Allocate.common

{
    "formid": "BD_Material",
    "data": {
        "Ids": "100001",
        "TargetOrgId": 100
    }
}
``

---

## 请求参数格式

### 字段类型对应

| 字段类型 | JSON格式 | 示例 |
|----------|----------|------|
| 文本/数字 | 直接赋值 | `"FQty": 10` |
| 基础资料 | 嵌套对象 | `"FMaterialId": {"FNumber": "MAT001"}` |
| 日期 | 字符串 | `"FDate": "2024-01-15"` |
| 布尔 | 布尔值 | `"FIsChecked": true` |
| 下拉/枚举 | 字符串 | `"FBillStatus": "A"` |

### 修改现有单据

修改时必须传 `FID` 和 `FBillNo`：
``json
{
    "formid": "SAL_SaleOrder",
    "data": {
        "Model": {
            "FID": 100001,
            "FBillNo": "SO2024001",
            "FNote": "修改后的备注"
        }
    }
}
``

### 操作单据体行

``json
"FEntity": [
    {
        "FEntryID": 1,          // 修改已有行，传 FEntryID
        "FQty": 20
    },
    {
        // 不传 FEntryID 表示新增行
        "FMaterialId": { "FNumber": "MAT002" },
        "FQty": 5
    }
]
``

---

## 批量操作接口

### 批量保存

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.BatchSave.common

{
    "formid": "SAL_SaleOrder",
    "BatchCount": 2,       // 并发线程数
    "data": {
        "Model": [
            { /* 第1个单据 */ },
            { /* 第2个单据 */ }
        ]
    }
}
``

### 批量提交/审核

``json
POST .../DynamicFormService.Submit.common

{
    "formid": "SAL_SaleOrder",
    "data": {
        "Ids": "100001,100002,100003"
    }
}
``

### 最佳实践

- 每批次建议 ≤100 条
- 保存、提交、审核分开执行计划
- 大批量数据使用分页查询 + 循环提交

---

## 自定义WebAPI开发

### 开发步骤

1. 编写服务插件类（参 `plugin-templates.md` 的自定义WebAPI模板）
2. 编译生成 dll
3. 部署 dll 到 `K3Cloud\WebSite\bin`
4. 在 BOS IDE 注册服务插件
5. 重启 IIS

### 调用方式

``json
POST http://IP/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.CustomBusinessService.DoAction.common

{
    "svcName": "MyCustomApi",
    "action": "QueryData",
    "param1": "MAT001"
}
``

---

## SDK使用

### C# SDK

``csharp
// 下载官方SDK，引入项目
var api = new K3CloudApi();

// 登录
bool loginResult = api.ValidateLogin("http://IP/K3Cloud", "账套ID", "用户名", "密码", 2052);

// 保存
var saveData = new {
    FormId = "SAL_SaleOrder",
    data = new {
        Model = new { /* ... */ }
    }
};
var saveResult = api.Save("SAL_SaleOrder", saveData);

// 查询
var queryResult = api.ExecuteBillQuery(new {
    FormId = "SAL_SaleOrder",
    FieldKeys = "FBillNo,FDate,FAmount",
    FilterString = "FBillNo = 'SO2024001'"
});
``

### Python 示例

``python
import requests
import json

class KingdeeApi:
    def __init__(self, base_url, db_id, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        # 登录
        login_url = f"{base_url}/Kingdee.BOS.WebApi.ServicesStub.UserService.ValidateUser.common"
        login_data = {
            "acctID": db_id,
            "username": username,
            "password": password,
            "lcid": 2052
        }
        resp = self.session.post(login_url, json=login_data)
        self.login_result = resp.json()

    def save(self, form_id, data):
        url = f"{self.base_url}/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Save.common"
        payload = {"formid": form_id, "data": data}
        return self.session.post(url, json=payload).json()

    def query(self, form_id, field_keys, filter_str="", limit=100):
        url = f"{self.base_url}/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common"
        payload = {
            "formid": form_id,
            "fieldKeys": field_keys,
            "filterString": filter_str,
            "limit": limit
        }
        return self.session.post(url, json=payload).json()

    def submit(self, form_id, ids):
        url = f"{self.base_url}/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Submit.common"
        payload = {"formid": form_id, "data": {"Ids": ids}}
        return self.session.post(url, json=payload).json()

    def audit(self, form_id, ids):
        url = f"{self.base_url}/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Audit.common"
        payload = {"formid": form_id, "data": {"Ids": ids}}
        return self.session.post(url, json=payload).json()
``

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 登录返回非1 | 检查账套ID、用户名、密码，确认用户有WebAPI权限 |
| 保存报字段不存在 | 检查fieldKeys，使用WebAPI在线测试工具查看可用字段 |
| 基础资料字段保存失败 | 使用 `{"FNumber": "xxx"}` 格式传值 |
| 批量操作超时 | 减少批次大小，增加超时时间 |
| 字段名不确定 | 前端「WebAPI」功能中搜索表单，查看所有可用字段 |
| 并发冲突 | 使用乐观锁，每次保存前重新查询最新版本号 |

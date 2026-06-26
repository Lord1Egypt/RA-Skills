# 金蝶云苍穹二次开发

## 目录
- [概述](#概述)
- [开发环境搭建](#开发环境搭建)
- [低代码开发](#低代码开发)
- [全代码开发（Java插件）](#全代码开发java插件)
- [KingScript脚本开发](#kingscript脚本开发)
- [苍穹OpenAPI](#苍穹openapi)
- [单点登录集成](#单点登录集成)
- [前端自定义开发](#前端自定义开发)
- [官方资源](#官方资源)

---

## 概述

金蝶云苍穹（AI Cosmic）是金蝶新一代企业级PaaS平台，与星空的核心区别：

| 特性 | 星空 | 苍穹 |
|------|------|------|
| 架构 | 单体/.NET | 微服务/Java/Spring Cloud |
| 数据库 | SQL Server | PostgreSQL |
| 开发语言 | C# | Java / KingScript |
| 开发方式 | BOS IDE + VS | 低代码 + IDEA全代码 |
| 部署 | IIS | Docker/K8s |
| 扩展模型 | 扩展(Extension) | 扩展模型/应用模型 |

---

## 开发环境搭建

### 1. 安装基础环境

- **JDK 11+**（推荐 OpenJDK 11）
- **IntelliJ IDEA**（Ultimate 版，安装金蝶官方插件）
- **PostgreSQL 12+**
- **Maven 3.6+**

### 2. 安装苍穹IDEA插件

1. IDEA → Settings → Plugins → Manage Plugin Repositories
2. 添加金蝶插件仓库地址（从开发者门户获取）
3. 安装「Kingdee Cosmic DevTool」插件
4. 重启 IDEA

### 3. 创建苍穹项目

1. IDEA → New Project → Kingdee Cosmic Project
2. 配置苍穹服务器地址和认证信息
3. 选择应用模板
4. 项目结构：
   ``
   my-app/
   ├── src/main/java/com/mycompany/
   │   ├── controller/     # 接口控制器
   │   ├── service/        # 业务服务
   │   ├── plugin/         # 插件类
   │   └── model/          # 数据模型
   ├── src/main/resources/
   │   ├── metadata/       # 元数据定义
   │   └── application.yml # 配置文件
   └── pom.xml
   ``

### 4. 配置数据库连接

``yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/cosmic_db
    username: dev_user
    password: dev_password
    driver-class-name: org.postgresql.Driver
``

---

## 低代码开发

苍穹低代码开发是首选方式，无需编写代码即可完成大部分功能。

### 页面建模

1. 开发平台 →「页面建模」
2. 新建页面 → 拖拽组件设计布局
3. 配置数据绑定
4. 配置交互规则

### 表单设计

1. 新建表单模型
2. 定义字段（类似星空BOS IDE）
3. 设计表单布局
4. 配置字段规则（必填/只读/隐藏）
5. 配置数据校验规则

### 流程设计

1. 新建流程模型
2. 设计审批节点
3. 配置审批人规则
4. 配置条件分支
5. 发布流程

### 报表设计

1. 新建报表模型
2. 配置数据源（SQL/数据集）
3. 设计报表布局
4. 配置过滤条件
5. 发布报表

---

## 全代码开发（Java插件）

### 插件类型

| 插件类型 | 基类/接口 | 用途 |
|----------|-----------|------|
| 表单插件 | AbstractFormPlugin | 表单交互控制 |
| 列表插件 | AbstractListPlugin | 列表过滤/操作 |
| 操作插件 | AbstractOperationServicePlugIn | 操作校验/拦截 |
| 报表插件 | AbstractReportServicePlugin | 自定义报表 |
| 转换插件 | AbstractConvertRulePlugIn | 下推转换 |
| 定时任务 | IScheduleTask | 定时执行 |
| 自定义API | ICustomApiService | REST接口 |

### Java 表单插件示例

``java
package com.mycompany.plugin;

import kd.bos.form.plugin.AbstractFormPlugin;
import kd.bos.form.control.events.ItemClickEvent;
import kd.bos.orm.query.QFilter;
import kd.bos.servicehelper.BusinessDataServiceHelper;

public class MyFormPlugin extends AbstractFormPlugin {

    @Override
    public void itemClick(ItemClickEvent evt) {
        super.itemClick(evt);

        if ("tbMyBtn".equals(evt.getItemKey())) {
            // 获取当前表单数据
            Object materialId = this.getModel().getValue("material");

            // 查询基础资料
            DynamicObject material = BusinessDataServiceHelper.loadSingle(
                "bd_material",
                new QFilter("number", QFilter.equals, "MAT001")
            );

            if (material != null) {
                // 设值
                this.getModel().setValue("material", material.getPkValue());
                this.getView().updateView("material");
            }

            // 提示
            this.getView().showTipMessage("操作完成");
        }
    }

    @Override
    public void afterBindData(EventObject e) {
        super.afterBindData(e);

        // 根据状态控制界面
        Object status = this.getModel().getValue("billstatus");
        if ("C".equals(String.valueOf(status))) {
            this.getView().setVisible(false, "field1", "field2");
            this.getView().setEnable(false, "field3", "field4");
        }
    }
}
``

### Java 操作插件示例

``java
package com.mycompany.plugin;

import kd.bos.servicehandler.AbstractOperationServicePlugIn;
import kd.bos.servicehandler.BeforeOperationArgs;
import kd.bos.servicehandler.AfterOperationArgs;
import kd.bos.dataentity.entity.DynamicObject;

public class MyAuditPlugin extends AbstractOperationServicePlugIn {

    @Override
    public void onPreparePropertys(PreparePropertysEventArgs e) {
        super.onPreparePropertys(e);
        e.getFieldKeys().add("billno");
        e.getFieldKeys().add("amount");
    }

    @Override
    public void beforeExecuteOperationTransaction(BeforeOperationArgs e) {
        super.beforeExecuteOperationTransaction(e);

        for (DynamicObject dataObj : e.getDataEntities()) {
            BigDecimal amount = dataObj.getBigDecimal("amount");
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                e.getCancelOperation().setCancel(true);
                e.getCancelOperation().setMessage("金额必须大于0！");
                return;
            }
        }
    }

    @Override
    public void afterExecuteOperationTransaction(AfterOperationArgs e) {
        super.afterExecuteOperationTransaction(e);

        for (DynamicObject dataObj : e.getDataEntities()) {
            String billNo = dataObj.getString("billno");
            // 审核后处理逻辑
        }
    }
}
``

---

## KingScript脚本开发

KingScript 是苍穹平台的脚本语言，用于轻量级逻辑扩展。

### 特点

- 语法类似 JavaScript/TypeScript
- 在开发平台中直接编写，无需编译部署
- 适合简单逻辑，复杂场景仍建议Java插件

### 示例

``javascript
// 字段变更事件
export function fieldChanged(context, fieldKey, oldValue, newValue) {
    if (fieldKey === 'material') {
        // 选择物料后带出单位
        const unit = newValue ? newValue.unit : null;
        context.getModel().setValue('unit', unit);
    }
}

// 按钮点击事件
export function buttonClick(context, buttonKey) {
    if (buttonKey === 'tbCalc') {
        const qty = context.getModel().getValue('qty') || 0;
        const price = context.getModel().getValue('price') || 0;
        context.getModel().setValue('amount', qty * price);
    }
}
``

---

## 苍穹OpenAPI

### 认证

``json
POST /api/oauth2/token

{
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "grant_type": "client_credentials"
}
``

### 保存接口

``json
POST /api/bill/save

{
    "number": "bill_number",
    "data": {
        "name": "测试单据",
        "items": [...]
    }
}
``

### 查询接口

``json
POST /api/bill/query

{
    "entityNumber": "bill_number",
    "selectFields": "id,number,name",
    "filter": "number = 'SO001'",
    "pageSize": 100,
    "pageNo": 1
}
``

---

## 单点登录集成

苍穹支持基于 OAuth2.0 的单点登录：

1. **苍穹登录第三方系统**：配置 OAuth2 客户端
2. **第三方登录苍穹**：构造登录URL + Token

### 登录URL构造

``text
https://your-cosmic-domain/login.html?redirect_uri=https://third-party.com/callback&token=YOUR_TOKEN
``

详见：https://vip.kingdee.com/knowledge/specialDetail/228892721203874816

---

## 前端自定义开发

苍穹前端基于 Vue.js，支持自定义组件开发。

### 自定义组件

1. 在开发平台创建「自定义组件」
2. 使用 Vue.js 编写组件代码
3. 配置组件属性
4. 在页面中引用组件

### 与苍穹数据交互

``javascript
// 获取当前表单数据
const model = this.getModel();
const billNo = model.getValue('billno');

// 设置字段值
model.setValue('custom_field', '新值');

// 调用后端接口
const result = await this.invokeCustomApi('myApi', { param: billNo });
``

---

## 官方资源

| 资源 | 链接 |
|------|------|
| 苍穹开发者门户 | https://dev.kingdee.com/dev |
| 苍穹开发文档 | https://demo.kdcloud.com/devdoc/wf |
| 苍穹开发认证 | https://kone.kingdee.com/certcenter |
| 苍穹社区 | https://club.kingdee.com/cosmic |
| 苍穹认证辅导群 | 云之家搜索「苍穹开发认证辅导群」 |
| 操作API零代码配置 | https://vip.kingdee.com/knowledge/specialDetail/226337046514476288 |

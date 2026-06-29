# 金蝶云苍穹二次开发

## 目录
- [概述](#概述)
- [开发环境搭建](#开发环境搭建)
- [低代码开发](#低代码开发)
- [全代码开发（Java插件）](#全代码开发java插件)
- [KingScript脚本开发](#kingscript脚本开发)
- [苍穹OpenAPI](#苍穹openapi)
- [与星空集成](#与星空集成)
- [单点登录集成](#单点登录集成)
- [前端自定义开发](#前端自定义开发)
- [部署与元数据发布](#部署与元数据发布)
- [官方资源](#官方资源)

---

## 概述

金蝶云苍穹（AI Cosmic）是金蝶新一代企业级 PaaS 平台，与星空的核心区别：

| 特性 | 星空 | 苍穹 |
|------|------|------|
| 架构 | 单体/.NET | 微服务/Java/Spring Cloud |
| 数据库 | SQL Server | PostgreSQL |
| 开发语言 | C# | Java / KingScript |
| 开发方式 | BOS IDE + VS | 低代码 + IDEA 全代码 |
| 部署 | IIS | Docker/K8s |
| 扩展模型 | 扩展(Extension) | 扩展模型/应用模型 |

---

## 开发环境搭建

### 1. 安装基础环境

- **JDK 11+**（推荐 OpenJDK 11）
- **IntelliJ IDEA**（Ultimate 版，安装金蝶官方插件）
- **PostgreSQL 12+**
- **Maven 3.6+**
- **Docker**（可选，用于本地部署）

### 2. 安装苍穹 IDEA 插件

1. IDEA → Settings → Plugins → Manage Plugin Repositories
2. 添加金蝶插件仓库地址（从开发者门户获取）
3. 安装「Kingdee Cosmic DevTool」插件
4. 重启 IDEA

### 3. 创建苍穹项目

1. IDEA → New Project → Kingdee Cosmic Project
2. 配置苍穹服务器地址和认证信息
3. 选择应用模板
4. 项目结构：

   ```text
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
   ```

### 4. 配置数据库连接

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/cosmic_db
    username: dev_user
    password: dev_password
    driver-class-name: org.postgresql.Driver
```

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
2. 定义字段（类似星空 BOS IDE）
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

### 插件类型矩阵

| 插件类型 | 基类 | 用途 | 注册位置 |
|----------|------|------|----------|
| 表单插件 | `kd.bos.form.plugin.AbstractFormPlugin` | 表单交互控制 | 表单属性 → 插件 |
| 列表插件 | `kd.bos.list.plugin.AbstractListPlugin` | 列表过滤/操作 | 列表属性 → 插件 |
| 操作插件 | `kd.bos.servicehelper.operation.AbstractOperationServicePlugIn` | 操作校验/拦截 | 操作属性 → 插件 |
| 报表插件 | `kd.bos.report.plugin.AbstractReportServicePlugin` | 自定义报表 | 报表属性 → 插件 |
| 转换插件 | `kd.bos.convert.plugin.AbstractConvertRulePlugIn` | 下推转换 | 转换规则 → 插件 |
| 定时任务 | `kd.bos.schedule.IScheduleTask` | 定时执行 | 调度任务 |
| 自定义 API | `kd.bos.servicehelper.api.ICustomApiService` | REST 接口 | API 注册 |

### Java 表单插件完整示例

```java
package com.mycompany.plugin;

import kd.bos.form.plugin.AbstractFormPlugin;
import kd.bos.form.control.events.ItemClickEvent;
import kd.bos.orm.query.QFilter;
import kd.bos.servicehelper.BusinessDataServiceHelper;
import kd.bos.dataentity.entity.DynamicObject;
import java.util.EventObject;

public class MyFormPlugin extends AbstractFormPlugin {

    @Override
    public void itemClick(ItemClickEvent evt) {
        super.itemClick(evt);

        if ("tbMyBtn".equals(evt.getItemKey())) {
            Object materialId = this.getModel().getValue("material");

            DynamicObject material = BusinessDataServiceHelper.loadSingle(
                "bd_material",
                new QFilter("number", QFilter.equals, "MAT001")
            );

            if (material != null) {
                this.getModel().setValue("material", material.getPkValue());
                this.getView().updateView("material");
            }

            this.getView().showTipMessage("操作完成");
        }
    }

    @Override
    public void afterBindData(EventObject e) {
        super.afterBindData(e);

        Object status = this.getModel().getValue("billstatus");
        if ("C".equals(String.valueOf(status))) {
            this.getView().setVisible(false, "field1", "field2");
            this.getView().setEnable(false, "field3", "field4");
        }
    }

    @Override
    public void propertyChanged(kd.bos.form.events.PropertyChangedEvent evt) {
        super.propertyChanged(evt);
        // 字段变更事件，相当于星空 DataChanged
        if ("material".equals(evt.getProperty().getName())) {
            DynamicObject material = (DynamicObject) evt.getNewValue();
            if (material != null) {
                this.getModel().setValue("unit", material.get("unit"));
                this.getView().updateView("unit");
            }
        }
    }
}
```

### Java 操作插件示例

```java
package com.mycompany.plugin;

import kd.bos.servicehelper.operation.AbstractOperationServicePlugIn;
import kd.bos.servicehelper.operation.OperationArgs;
import kd.bos.dataentity.entity.DynamicObject;
import java.math.BigDecimal;
import java.util.List;

public class MyAuditPlugin extends AbstractOperationServicePlugIn {

    @Override
    public void onPreparePropertys(kd.bos.servicehelper.operation.PreparePropertysEventArgs e) {
        super.onPreparePropertys(e);
        e.getFieldKeys().add("billno");
        e.getFieldKeys().add("amount");
    }

    @Override
    public void beforeExecuteOperationTransaction(OperationArgs e) {
        super.beforeExecuteOperationTransaction(e);

        List<DynamicObject> dataEntities = e.getDataEntities();
        if (dataEntities == null) return;

        for (DynamicObject dataObj : dataEntities) {
            BigDecimal amount = dataObj.getBigDecimal("amount");
            if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
                e.getCancelOperation().setCancel(true);
                e.getCancelOperation().setMessage("金额必须大于0！");
                return;
            }
        }
    }

    @Override
    public void afterExecuteOperationTransaction(OperationArgs e) {
        super.afterExecuteOperationTransaction(e);

        List<DynamicObject> dataEntities = e.getDataEntities();
        if (dataEntities == null) return;

        for (DynamicObject dataObj : dataEntities) {
            String billNo = dataObj.getString("billno");
            // 审核后处理逻辑
        }
    }
}
```

### Java 列表插件示例

```java
package com.mycompany.plugin;

import kd.bos.list.plugin.AbstractListPlugin;
import kd.bos.list.events.ListFilterEvent;
import kd.bos.orm.query.QFilter;
import java.util.List;

public class MyListPlugin extends AbstractListPlugin {

    @Override
    public void filter(ListFilterEvent evt) {
        super.filter(evt);

        // 添加默认过滤：当前组织
        QFilter orgFilter = new QFilter("org", "=", this.getContext().getCurrentOrganizationInfo().getId());
        evt.addCustomQFilter(orgFilter);

        // 添加日期过滤
        QFilter dateFilter = new QFilter("billdate", ">=", "2024-01-01");
        evt.addCustomQFilter(dateFilter);
    }
}
```

### Java 自定义 API 示例

```java
package com.mycompany.api;

import kd.bos.servicehelper.api.CustomApiServiceContext;
import kd.bos.servicehelper.api.ICustomApiService;
import kd.bos.orm.query.QFilter;
import kd.bos.servicehelper.BusinessDataServiceHelper;
import kd.bos.dataentity.entity.DynamicObject;
import java.util.HashMap;
import java.util.Map;

public class MyCustomApi implements ICustomApiService {

    @Override
    public Map<String, Object> doCustomService(CustomApiServiceContext context, Map<String, Object> params) {
        Map<String, Object> result = new HashMap<>();

        try {
            String action = (String) params.get("action");
            String materialNumber = (String) params.get("materialNumber");

            if ("query".equals(action)) {
                DynamicObject material = BusinessDataServiceHelper.loadSingle(
                    "bd_material",
                    new QFilter("number", "=", materialNumber)
                );

                result.put("success", true);
                result.put("data", material != null ? material.toMap() : null);
            } else {
                result.put("success", false);
                result.put("message", "未知操作类型");
            }
        } catch (Exception ex) {
            result.put("success", false);
            result.put("message", ex.getMessage());
        }

        return result;
    }
}
```

### 定时任务示例

```java
package com.mycompany.schedule;

import kd.bos.schedule.IScheduleTask;
import kd.bos.schedule.ScheduleMessage;
import kd.bos.context.RequestContext;

public class MyScheduleTask implements IScheduleTask {

    @Override
    public ScheduleMessage execute(RequestContext requestContext, Map<String, Object> params) {
        // 定时执行逻辑：如同步外部数据、生成报表等
        System.out.println("定时任务执行：" + new java.util.Date());

        return ScheduleMessage.createInfoMessage("执行成功");
    }
}
```

---

## KingScript 脚本开发

KingScript 是苍穹平台的脚本语言，用于轻量级逻辑扩展。

### 特点

- 语法类似 JavaScript/TypeScript
- 在开发平台中直接编写，无需编译部署
- 适合简单逻辑，复杂场景仍建议 Java 插件

### 常用事件

| 事件 | 触发时机 |
|------|----------|
| `fieldChanged` | 字段值变更后 |
| `itemClick` | 按钮点击后 |
| `beforeDoOperation` | 操作执行前 |
| `afterDoOperation` | 操作执行后 |
| `afterBindData` | 数据绑定后 |

### 字段变更示例

```javascript
export function fieldChanged(context, fieldKey, oldValue, newValue) {
    if (fieldKey === 'material') {
        const unit = newValue ? newValue.unit : null;
        context.getModel().setValue('unit', unit);
        context.getView().updateView('unit');
    }

    if (fieldKey === 'qty' || fieldKey === 'price') {
        const qty = context.getModel().getValue('qty') || 0;
        const price = context.getModel().getValue('price') || 0;
        context.getModel().setValue('amount', qty * price);
    }
}
```

### 按钮点击示例

```javascript
export function itemClick(context, buttonKey) {
    if (buttonKey === 'tbCalc') {
        const qty = context.getModel().getValue('qty') || 0;
        const price = context.getModel().getValue('price') || 0;
        context.getModel().setValue('amount', qty * price);
        context.getView().updateView('amount');
    }
}
```

### 操作前校验

```javascript
export function beforeDoOperation(context, operationKey) {
    if (operationKey === 'save') {
        const amount = context.getModel().getValue('amount') || 0;
        if (amount <= 0) {
            context.showErrMessage('金额必须大于0');
            return false; // 阻止操作
        }
    }
    return true;
}
```

---

## 苍穹 OpenAPI

### 认证方式 1：OAuth2 客户端凭证

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class CosmicAuthHelper {

    public static String getAccessToken(String baseUrl, String appId, String appSecret) throws Exception {
        String body = String.format(
            "{\"app_id\":\"%s\",\"app_secret\":\"%s\",\"grant_type\":\"client_credentials\"}",
            appId, appSecret
        );

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/api/oauth2/token"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        // 解析返回的 access_token
        return parseToken(response.body());
    }

    private static String parseToken(String json) {
        // 实际使用 JSON 库解析
        return json;
    }
}
```

### 保存接口

```json
POST /api/bill/save
Authorization: Bearer {access_token}

{
    "data": {
        "number": "",
        "billtype": "bill_myorder",
        "items": [
            {
                "material": "MAT001",
                "qty": 10,
                "price": 100
            }
        ]
    }
}
```

### 查询接口

```json
POST /api/bill/query
Authorization: Bearer {access_token}

{
    "entityNumber": "bill_myorder",
    "selectFields": "id,number,billdate,amount",
    "filter": "number = 'SO001'",
    "pageSize": 100,
    "pageNo": 1
}
```

### 签名认证（AppId + AppSecret）

苍穹部分接口使用签名认证：

```java
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class SignHelper {

    public static String generateSign(String appId, String timestamp, String appSecret) throws Exception {
        String source = appId + timestamp + appSecret;
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] bytes = md.digest(source.getBytes(StandardCharsets.UTF_8));

        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

请求头：

```text
X-KD-AppId: your_app_id
X-KD-TimeStamp: 1718888888
X-KD-Sign: md5_hash
```

---

## 与星空集成

### 场景

- 星空已有成熟 ERP 业务数据，苍穹作为新平台逐步替换
- 需要双向同步：物料、客户、订单、凭证等

### 常用集成方式

| 方式 | 星空侧 | 苍穹侧 | 适用场景 |
|------|--------|--------|----------|
| 数据库直连 | 读 SQL Server | 写 PostgreSQL | 批量数据同步 |
| 中间表 | 写入中间库 | 从中间库读取 | 定时同步 |
| WebAPI | 调用苍穹 OpenAPI | 提供接口 | 实时同步 |
| MQ | 发送消息 | 消费消息 | 事件驱动 |
| ESB | 企业服务总线 | 企业服务总线 | 大规模集成 |

### 通过 WebAPI 从星空同步到苍穹

```java
// 1. 调用星空 WebAPI 查询数据
String kingdeeUrl = "http://k3cloud-server/K3Cloud";
String queryResult = callKingdeeQueryApi(kingdeeUrl, "SAL_SaleOrder", "FBillNo,FDate,FAmount");

// 2. 转换数据格式
List<Map<String, Object>> cosmicData = convertToCosmicFormat(queryResult);

// 3. 调用苍穹 OpenAPI 保存
for (Map<String, Object> record : cosmicData) {
    callCosmicSaveApi(cosmicServer, "bill_myorder", record);
}
```

---

## 单点登录集成

苍穹支持基于 OAuth2.0 的单点登录：

1. **苍穹登录第三方系统**：配置 OAuth2 客户端
2. **第三方登录苍穹**：构造登录 URL + Token

### 登录 URL 构造

```text
https://your-cosmic-domain/login.html?redirect_uri=https://third-party.com/callback&token=YOUR_TOKEN
```

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

```javascript
// 获取当前表单数据
const model = this.getModel();
const billNo = model.getValue('billno');

// 设置字段值
model.setValue('custom_field', '新值');

// 调用后端接口
const result = await this.invokeCustomApi('myApi', { param: billNo });

// 调用苍穹标准服务
const data = await this.loadData({
    formId: 'bd_material',
    filter: { number: 'MAT001' }
});
```

---

## 部署与元数据发布

### 本地开发部署

1. IDEA 中右键项目 → Run Maven → `clean install`
2. 生成 `target/*.jar`
3. 将 jar 复制到苍穹应用容器指定目录
4. 重启苍穹服务

### 使用 Docker 部署

```dockerfile
FROM openjdk:11-jre-slim
COPY target/my-app.jar /app/my-app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/my-app.jar"]
```

```bash
docker build -t my-cosmic-app:1.0.0 .
docker run -p 8080:8080 my-cosmic-app:1.0.0
```

### K8s 部署示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cosmic-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cosmic-app
  template:
    metadata:
      labels:
        app: cosmic-app
    spec:
      containers:
      - name: cosmic-app
        image: my-cosmic-app:1.0.0
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: cosmic-app-service
spec:
  selector:
    app: cosmic-app
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### 元数据发布

苍穹中的元数据（表单、流程、报表等）需要通过开发平台发布：

1. 开发平台 → 应用管理 → 选择应用
2. 点击「发布」→「发布到目标环境」
3. 选择发布范围（全部/增量）
4. 确认发布

> 注意：苍穹与星空不同，苍穹的元数据发布通常是应用级别的，不需要像 BOS IDE 那样逐个签入签出。

### 生产环境注意事项

- 发布前先在测试环境验证
- 涉及数据库结构变更时，先备份 PostgreSQL
- 多个微服务间存在依赖时，按依赖顺序重启
- 使用 K8s 滚动更新，避免服务中断
- 配置健康检查和监控告警

---

## 官方资源

| 资源 | 链接 |
|------|------|
| 苍穹开发者门户 | https://dev.kingdee.com/dev |
| 苍穹开发文档 | https://demo.kdcloud.com/devdoc/wf |
| 苍穹开发认证 | https://kone.kingdee.com/certcenter |
| 苍穹社区 | https://club.kingdee.com/cosmic |
| 苍穹认证辅导群 | 云之家搜索「苍穹开发认证辅导群」 |
| 操作 API 零代码配置 | https://vip.kingdee.com/knowledge/specialDetail/226337046514476288 |

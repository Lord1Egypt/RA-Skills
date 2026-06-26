# 金蝶二次开发常见模式 + 社区FAQ

## 目录
- [常见开发模式](#常见开发模式)
- [社区高频FAQ](#社区高频faq)
- [常见报错与解决](#常见报错与解决)
- [社区精选资源索引](#社区精选资源索引)

---

## 常见开发模式

### 1. 单据编号自定义

**需求：** 单据编号按特定规则自动生成

**方案：** BOS IDE → 单据属性 → 编号规则

- 支持前缀+日期+流水号组合
- 可配置流水号位数、重置规则（每日/每月/每年）
- 复杂规则可通过操作插件在 `BeforeExecuteOperationTransaction` 中手动赋值

### 2. 审批流配置

**需求：** 单据提交后走审批流程

**方案：** BOS IDE → 工作流配置

1. 设计审批流（节点/条件/审批人）
2. 配置审批权限
3. 单据提交操作绑定审批流
4. 插件干预：操作插件中可修改审批人、跳过审批等

### 3. 字段级权限控制

**需求：** 不同角色看到不同字段

**方案：** 系统前台 → 权限管理 → 字段权限

1. 创建角色
2. 分配功能权限
3. 配置字段权限（可见/编辑/隐藏）
4. 修改后「同步注册用户」

### 4. 基础资料联动

**需求：** 选择A后自动带出B的值

**方案：** 表单插件 DataChanged 事件

``csharp
public override void DataChanged(DataChangedEventArgs e)
{
    if (e.Field.Key == "FMaterialId")
    {
        DynamicObject material = e.NewValue as DynamicObject;
        if (material != null)
        {
            // 带出关联字段
            DynamicObject unit = material["BaseUnitId"] as DynamicObject;
            this.Model.SetValue("FUnitId", unit, rowIndex);
        }
    }
}
``

### 5. 上下游单据自动生成

**需求：** A单据审核后自动生成B单据

**方案：** 操作插件 AfterExecuteOperationTransaction

``csharp
public override void AfterExecuteOperationTransaction(AfterExecuteOperationTransaction e)
{
    foreach (DynamicObject dataObj in e.DataObjects)
    {
        // 构造下游单据数据
        DynamicObject newBill = new DynamicObject(targetBusinessInfo.GetEntity("FBillHead").DynamicObjectType);

        // 设置字段...
        // newBill["FSourceBillId"] = dataObj["Id"];

        // 保存
        BusinessDataServiceHelper.Save(this.Context, targetBusinessInfo, newBill);
    }
}
``

### 6. 外部系统数据同步

**需求：** 定时从外部API同步数据到星空

**方案：**

- 方式1：定时任务插件（IScheduleService）
- 方式2：外部系统调用星空 WebAPI
- 方式3：中间表 + SQL Server Integration Services

### 7. 报表开发（直接SQL账表）

**需求：** 自定义报表展示数据

**方案：** 报表插件（详见 `xingkong-plugin-dev.md` §报表插件）

- 简单账表：适合固定格式报表
- 直接SQL账表：灵活SQL查询
- 分页报表：大数据量报表

### 8. 套打模板

**需求：** 自定义打印模板

**方案：** 套打客户端

1. 安装套打客户端
2. 设计打印模板
3. 绑定数据字段
4. 在单据上关联打印模板

---

## 社区高频FAQ

### Q1: 扩展单据后字段不显示？
检查：1.字段是否绑定到布局 2.是否保存→签入 3.是否发布到主控台 4.是否清除浏览器缓存

### Q2: 插件注册后不生效？
检查：1.dll是否放在 K3Cloud\WebSite\bin 2.是否重启IIS 3.BOS IDE中注册是否正确 4.注册的插件类型是否匹配

### Q3: 操作插件取不到字段值？
原因：操作插件默认不加载所有字段。必须在 `OnPreparePropertys` 中声明需要的字段：
``csharp
public override void OnPreparePropertys(PreparePropertysEventArgs e)
{
    base.OnPreparePropertys(e);
    e.FieldKeys.Add("FMaterialId");
    e.FieldKeys.Add("FQty");
}
``

### Q4: BusinessInfo和BillBusinessInfo的区别？
- BusinessInfo：通用元数据
- BillBusinessInfo：含单据体结构的元数据
- 表单/操作插件中用 `this.View.BillBusinessInfo`

### Q5: 如何读取配置文件中的配置？
``csharp
// 读取星空配置
string configValue = Kingdee.BOS.ServiceHelper.SystemParameterServiceHelper.GetParameter(
    this.Context, 
    formId, 
    parameterKey
);
``

### Q6: 如何获取当前登录用户信息？
``csharp
long userId = this.Context.UserId;
string userName = this.Context.UserName;
long orgId = this.Context.CurrentOrganizationInfo.ID;
``

### Q7: 单据状态枚举值？
- A = 暂存
- B = 已提交
- C = 已审核
- D = 已关闭

### Q8: 如何实现多选基础资料？
1. 在单据上添加「多选基础资料」字段
2. BOS IDE 中字段类型选择「多选基础资料」
3. 绑定目标基础资料

### Q9: 如何给单据体动态添加行？
``csharp
this.Model.CreateNewEntryRow("FEntity");
int newRow = this.Model.GetEntryCurrentRow("FEntity");
this.Model.SetValue("FMaterialId", material, newRow);
``

### Q10: WebAPI保存报"字段不存在"？
使用前端「WebAPI」功能搜索表单，查看该表单所有可用字段的标识。

---

## 常见报错与解决

| 报错 | 原因 | 解决方案 |
|------|------|----------|
| 「无法加载文件或程序集」 | dll版本不匹配 | 更新引用的BOS dll到对应版本 |
| 「未将对象引用设置到对象的实例」 | 空引用 | 检查字段是否为null再使用 |
| 「操作被取消」 | 插件中设置了CancelOperation | 检查操作插件的校验逻辑 |
| 「分布式事务错误」 | 事务嵌套 | 避免在操作插件中调用其他涉及事务的API |
| 「IIS 503错误」 | 应用池崩溃 | 检查插件是否有死循环/内存泄漏 |
| 「数据库连接超时」 | SQL慢查询 | 优化SQL，添加索引 |
| 「编译通过但插件不触发」 | 注册位置错误 | 确认插件类型和注册位置匹配 |
| 「字段只读无法设值」 | 界面控件设为只读 | 在插件中用Model.SetValue而非直接改DataObject |

---

## 社区精选资源索引

### 入门学习

| 资源 | 链接 |
|------|------|
| 星空知识地图 | https://vip.kingdee.com/article/392699482837824512 |
| 开发入门视频 | https://vip.kingdee.com/school/learnPath/193463482326019584 |
| 业务入门视频 | https://vip.kingdee.com/school/learnPath/193413835540524288 |
| BOS开发平台使用 | https://vip.kingdee.com/article/57854870606429952 |

### 插件开发

| 资源 | 链接 |
|------|------|
| 各类插件案例1 | https://vip.kingdee.com/article/64993872014591232 |
| 各类插件案例2 | https://vip.kingdee.com/article/94751030918525696 |
| 插件注册方式 | https://vip.kingdee.com/article/359649910671058176 |
| 常见功能二开案例 | https://vip.kingdee.com/article/462556395796384256 |
| Debug插件方法 | https://vip.kingdee.com/article/117230406226751232 |

### 报表开发

| 资源 | 链接 |
|------|------|
| 账表入门答疑 | https://vip.kingdee.com/article/61867544482929408 |
| 直接SQL账表 | https://vip.kingdee.com/article/423447326397443584 |
| 简单账表开发1 | https://vip.kingdee.com/article/81696654923133440 |
| 简单账表开发2 | https://vip.kingdee.com/article/37120 |
| 简单账表分组汇总 | https://vip.kingdee.com/article/321700583491072512 |
| 简单账表文章汇总 | https://vip.kingdee.com/article/9144 |

### WebAPI

| 资源 | 链接 |
|------|------|
| WebAPI接口说明书 | https://vip.kingdee.com/knowledge/2569 |
| WebAPI使用教程1 | https://vip.kingdee.com/article/76278025062688512 |
| WebAPI使用教程2 | https://vip.kingdee.com/knowledge/specialDetail/229961573895771136 |

### 数据库与SQL

| 资源 | 链接 |
|------|------|
| 枚举值SQL查询 | https://vip.kingdee.com/article/477437083272077824 |
| 单选辅助资料列表取值SQL | https://vip.kingdee.com/article/76326791479923200 |
| 存货收发存汇总SQL | https://vip.kingdee.com/article/249594501369582336 |
| BOM多级展开 | https://vip.kingdee.com/article/213984429721406208 |
| 单据状态查询 | https://vip.kingdee.com/article/510850972030109952 |

### 部署运维

| 资源 | 链接 |
|------|------|
| 打包部署 | https://vip.kingdee.com/article/427104899491671040 |
| 安装补丁报错解决 | https://vip.kingdee.com/article/465831002527655168 |
| 账套环境升级失败 | https://vip.kingdee.com/article/474018491821827072 |
| 环境下载 | https://open.kingdee.com/K3Cloud/Open/Products.aspx |

# Step 4: 合理性检查 + 输出

## 目标
在输出前执行合理性检查，确保信息完整、流程闭环、设计合理，然后输出差量PRD和修改后原型。

---

## 4.1 合理性检查

### 检查清单

#### 检查项1：信息完整性

逐一检查每个调整模块的材料是否完整：

**新增界面检查**：
- [ ] 有需求描述（功能、用户、场景、目标）
- [ ] 有界面字段清单（字段名、类型、说明、必填）
- [ ] 有前后跳转说明或截图

**调整界面检查**：
- [ ] 有调整说明（调整内容、原因、期望效果）
- [ ] 有当前界面截图或详细描述
- [ ] 有变更位置标注

**删除界面检查**：
- [ ] 有流程影响分析
- [ ] 有数据影响分析
- [ ] 有依赖检查分析

**检查方法**：
遍历 `02-add/`、`03-modify/`、`04-delete/` 目录下的所有文件，检查必要字段是否填写。

**如果发现缺失**：
创建 `project/05-validation-issues.md`：
```markdown
# 信息完整性检查 - 发现缺失

## 缺失项清单

### M6 规则引擎（新增）
- ⚠️ 缺少前序界面截图
- ⚠️ 字段"目标客户"的类型和说明不够详细

### M2 任务管理（调整）
- ⚠️ 缺少当前界面截图或描述
```

用 `present_files` 呈现缺失清单，要求用户补充，补充后重新检查。

#### 检查项2：流程闭环性

检查调整后的主流程是否完整、合理、可执行。

**检查步骤**：

1. **重建调整后的主流程**

从Step 1的现有主流程出发，应用所有调整：
- 新增模块 → 在流程中插入新步骤
- 调整模块 → 修改相应步骤的描述
- 删除模块 → 从流程中移除相应步骤

**示例**：

原流程：
```
1. 业务部门配置回访模板
2. 业务部门创建回访任务并分配给客服专员
3. 客服专员执行回访并记录结果
4. 业务部门审核回访质量
5. 系统生成回访数据报表
```

应用调整（M6新增、M2调整、M4删除）：
```
1. 业务部门配置回访模板
2. 业务部门配置自动生成规则（新增M6）
3. 业务部门手动创建任务 或 系统自动生成任务（调整M2）
4. 业务部门分配任务给客服专员
5. 客服专员执行回访并记录结果
6. 系统生成回访数据报表（删除M4审核步骤）
```

2. **检查流程完整性**

- [ ] 流程有明确的开始点
- [ ] 流程有明确的结束点
- [ ] 每个步骤都有执行角色
- [ ] 步骤之间的衔接合理（没有跳跃、断裂）
- [ ] 新增步骤的前后衔接清晰

3. **检查界面跳转闭环**

对于新增和调整的界面，检查跳转路径是否闭环：

```
用户从A页面 → 点击按钮进入B页面 → 操作完成后能回到A页面或进入合理的下一页
```

**检查方法**：
遍历所有新增/调整界面，画出跳转路径图，检查是否有"死胡同"（只能进不能出）或"孤岛"（无法到达）。

**如果发现问题**：
记录到 `project/05-validation-issues.md`：
```markdown
## 流程闭环性检查 - 发现问题

### 问题1：M6规则引擎的返回路径不明确
- 现状：从M2任务管理进入M6，但没有说明如何返回
- 建议：增加"保存后返回M2"或"取消后返回M2"的说明
```

#### 检查项3：角色权限覆盖

检查每个新增/调整的界面是否明确了操作角色，以及角色是否失去必要功能。

**检查步骤**：

1. **新增界面的角色分配**

遍历所有新增界面，检查是否在需求描述中明确了"用户：[角色]"。

2. **调整界面的角色影响**

检查调整是否影响原角色的操作权限：
- 增加功能 → 确认哪个角色使用
- 移除功能 → 确认是否影响角色的必要工作

3. **删除界面的角色影响**

检查删除模块后，相关角色是否失去必要功能：

**示例**：
```
删除M4质量审核模块
原角色：业务部门负责审核回访质量
删除后：业务部门失去质量审核功能

检查：
- 业务部门是否还有其他质量管控手段？
- 是否需要在其他模块补充质量检查功能？
```

**如果发现问题**：
记录到 `project/05-validation-issues.md`：
```markdown
## 角色权限检查 - 发现问题

### 问题1：删除M4后业务部门失去质量管控手段
- 现状：删除质量审核模块后，业务部门无法审核回访质量
- 建议：在M5数据报表中增加"异常回访标记"功能，作为质量监控替代方案
```

### 检查结果

**如果所有检查都通过**：

创建 `project/05-validation-passed.md`：
```markdown
# 合理性检查 - 通过 ✅

## 检查时间
[时间戳]

## 检查结果

### ✅ 信息完整性检查
- 所有新增界面都有完整的需求描述、字段清单、前后跳转
- 所有调整界面都有截图或详细描述、变更位置标注
- 所有删除界面都有影响分析

### ✅ 流程闭环性检查
- 调整后的主流程完整、合理
- 所有新增/调整界面的跳转路径闭环
- 无流程断裂或孤岛

### ✅ 角色权限检查
- 所有新增/调整界面都明确了操作角色
- 删除模块未导致角色失去必要功能

## 结论
所有检查通过，可以进入输出阶段。
```

**如果检查未通过**：

用 `present_files` 呈现 `05-validation-issues.md`，要求用户补充信息或确认风险接受。

补充完成后重新执行检查。

---

## 4.2 最终输出

### 输出1：差量PRD文档

创建 `project/06-output/delta-prd.md`。

#### PRD结构

```markdown
# [产品名称] 迭代PRD - v[版本号]

## 文档信息
- **版本号**：[如 v2.1]
- **迭代目标**：[一句话概括本次迭代目标]
- **创建日期**：[日期]
- **涉及角色**：[列出Step 1中的角色]

---

## 1. 迭代概述

### 1.1 迭代背景
[引用Step 1中的迭代需求 - 问题部分]

### 1.2 迭代目标
[引用Step 1中的迭代需求 - 需求部分]

### 1.3 调整范围
本次迭代涉及以下模块：
[引用Step 2中的调整清单表格]

---

## 2. 现有流程回顾

[引用Step 1中的现有主流程]

---

## 3. 调整后流程

[引用Step 4.1检查项2中重建的调整后主流程]

### 流程变更说明
- **新增步骤**：[列出新增的步骤]
- **修改步骤**：[列出修改的步骤及修改内容]
- **删除步骤**：[列出删除的步骤及原因]

---

## 4. 新增功能详述

[针对Step 2调整清单中每个"新增"类型的模块]

### 4.1 [模块名]

#### 功能概述
[引用Step 3中该模块的需求描述]

#### 界面字段
[引用Step 3中该模块的字段表]

#### 界面原型
参见原型文件：`prototype.html` - [模块名]

#### 前后跳转
[引用Step 3中该模块的前后跳转说明]

#### 用户故事
作为 [角色]，我希望 [功能]，以便 [目标]。

**验收标准**：
- [ ] [验收条件1]
- [ ] [验收条件2]
- [ ] [验收条件3]

---

## 5. 调整功能详述

[针对Step 2调整清单中每个"调整"类型的模块]

### 5.1 [模块名]

#### 调整概述
[引用Step 3中该模块的调整说明]

#### Before（当前状态）
[引用Step 3中该模块的当前界面描述]
[如有截图，嵌入或引用]

#### After（调整后状态）
[基于调整说明，描述调整后的界面]

**主要变更点**：
1. [变更点1：位置、内容、样式]
2. [变更点2：位置、内容、样式]
3. [变更点3：位置、内容、样式]

#### 界面原型
参见原型文件：`prototype.html` - [模块名] - Before/After对比

#### 影响范围
[说明此调整对其他模块或流程的影响]

---

## 6. 删除功能说明

[针对Step 2调整清单中每个"删除"类型的模块]

### 6.1 [模块名]

#### 删除原因
[引用Step 3中该模块的删除原因]

#### 影响分析
[引用Step 3中该模块的影响分析 - 流程影响、数据影响、依赖影响]

#### 数据迁移方案
[说明历史数据如何处理]

#### 功能替代方案
[如果有替代方案，说明如何在其他模块补偿被删除的功能]

---

## 7. 数据字段变更

### 7.1 新增字段

[列出所有新增模块涉及的新数据对象和字段]

| 数据对象 | 字段名 | 类型 | 说明 | 必填 |
|---------|--------|------|------|------|
| [对象名] | [字段] | [类型] | [说明] | 是/否 |

### 7.2 修改字段

[列出现有字段的修改]

| 数据对象 | 字段名 | 原类型/说明 | 新类型/说明 | 修改原因 |
|---------|--------|------------|------------|---------|
| [对象名] | [字段] | [原值] | [新值] | [原因] |

### 7.3 废弃字段

[列出删除模块涉及的废弃字段]

| 数据对象 | 字段名 | 原用途 | 处理方案 |
|---------|--------|--------|---------|
| [对象名] | [字段] | [用途] | [归档/删除] |

---

## 8. 角色权限变更

### 8.1 新增权限

[列出新增模块涉及的角色权限]

| 角色 | 新增权限 | 对应功能 |
|------|---------|---------|
| [角色] | [权限] | [功能模块] |

### 8.2 权限调整

[列出调整模块涉及的权限变化]

| 角色 | 原权限 | 新权限 | 变更说明 |
|------|--------|--------|---------|
| [角色] | [权限] | [权限] | [说明] |

### 8.3 废弃权限

[列出删除模块涉及的权限]

| 角色 | 废弃权限 | 原功能 |
|------|---------|--------|
| [角色] | [权限] | [功能模块] |

---

## 9. 交互规范（如有变更）

[如果新增或调整涉及新的交互组件或规范，在此说明]

### 9.1 新增交互组件
- [组件名称]：[用途和交互说明]

### 9.2 调整交互规则
- [规则名称]：[调整内容]

---

## 10. 回滚预案

### 10.1 回滚触发条件
- [条件1：如"新增功能导致系统响应时间超过5秒"]
- [条件2：如"用户反馈新流程比旧流程更复杂"]
- [条件3：如"数据迁移失败"]

### 10.2 回滚步骤

**新增功能回滚**：
1. [步骤1：关闭新增功能入口]
2. [步骤2：隐藏新增菜单/按钮]
3. [步骤3：停止新数据写入]

**调整功能回滚**：
1. [步骤1：切换回旧版界面]
2. [步骤2：恢复原有流程]

**删除功能回滚**：
1. [步骤1：重新启用被删除模块]
2. [步骤2：恢复废弃字段]
3. [步骤3：恢复相关权限]

### 10.3 数据恢复方案
[说明如何恢复数据到迭代前状态]

---

## 11. 灰度发布计划（建议）

### 11.1 灰度范围
- 阶段1（10%）：[选择哪些用户先试用]
- 阶段2（50%）：[扩大范围]
- 阶段3（100%）：[全量发布]

### 11.2 监控指标
- [指标1：如"新功能使用率"]
- [指标2：如"用户反馈分数"]
- [指标3：如"系统性能指标"]

---

## 附录

### A. 术语表
[定义本PRD中使用的专业术语]

### B. 参考资料
- Step 1 基础信息：`00-input/baseline.md`
- Step 2 调整清单：`01-adjustment-list.md`
- Step 3 新增材料：`02-add/`
- Step 3 调整材料：`03-modify/`
- Step 3 删除分析：`04-delete/`
```

### 输出2：修改后的原型

创建 `project/06-output/prototype.html`。

#### 原型技术栈
- React（用于交互组件）
- Tailwind CSS（用于样式）

#### 原型结构

```jsx
// 整体结构示例
<div className="prototype-container">
  {/* 左侧导航 */}
  <Sidebar modules={modules} />
  
  {/* 主内容区 */}
  <MainContent>
    {/* 根据选择的模块显示不同内容 */}
    {selectedModule.type === 'add' && <NewModulePrototype />}
    {selectedModule.type === 'modify' && <ModifyModulePrototype />}
    {selectedModule.type === 'delete' && <DeletedModuleNotice />}
  </MainContent>
</div>
```

#### 新增界面原型

完整的交互原型，包含：
- 所有字段按Step 3收集的字段表实现
- 前后跳转按钮（模拟跳转）
- 表单校验（必填项校验）
- 提交/取消操作

示例：
```jsx
function NewRuleEngineModule() {
  return (
    <div className="new-module">
      <div className="module-header">
        <h2>新增模块：M6 规则引擎</h2>
        <span className="badge-new">NEW</span>
      </div>
      
      <form className="rule-form">
        <div className="form-field">
          <label>规则名称 *</label>
          <input type="text" required />
        </div>
        
        <div className="form-field">
          <label>触发条件 *</label>
          <select multiple>
            <option>新客户注册</option>
            <option>订单完成</option>
            <option>退款申请</option>
          </select>
        </div>
        
        {/* 更多字段... */}
        
        <div className="form-actions">
          <button type="button" onClick={() => goTo('M2-任务管理')}>
            取消
          </button>
          <button type="submit">
            保存规则
          </button>
        </div>
      </form>
      
      {/* 跳转说明 */}
      <div className="navigation-note">
        <p>前序：从 M2 任务管理 点击"规则配置"进入</p>
        <p>后续：保存后返回 M2 任务管理</p>
      </div>
    </div>
  );
}
```

#### 调整界面原型（Before/After对比）

使用左右分屏或Tab切换展示：

**方案A：左右分屏**
```jsx
function ModifyTaskManagementModule() {
  return (
    <div className="modify-module">
      <div className="module-header">
        <h2>调整模块：M2 任务管理</h2>
        <span className="badge-modify">MODIFIED</span>
      </div>
      
      <div className="comparison-view">
        {/* 左侧：Before */}
        <div className="before-view">
          <h3>Before（当前版本）</h3>
          {/* 如果有截图，显示截图 */}
          <img src="screenshots/M2-current.png" alt="当前界面" />
          {/* 或者渲染简化版界面 */}
          <div className="mockup">
            <div className="header">
              <h2>回访任务管理</h2>
              <div className="actions">
                <button>手动创建任务</button>
              </div>
            </div>
            <table>...</table>
          </div>
        </div>
        
        {/* 右侧：After */}
        <div className="after-view">
          <h3>After（调整后）</h3>
          <div className="mockup">
            <div className="header">
              <h2>回访任务管理</h2>
              <div className="actions">
                <button>手动创建任务</button>
                {/* 高亮新增的按钮 */}
                <button className="highlight-new">
                  自动生成任务
                  <span className="new-badge">NEW</span>
                </button>
              </div>
            </div>
            <table>...</table>
          </div>
          
          {/* 变更说明 */}
          <div className="change-notes">
            <h4>主要变更</h4>
            <ul>
              <li>✨ 在顶部操作栏增加"自动生成任务"按钮</li>
              <li>✨ 点击后跳转到 M6 规则配置页面</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**方案B：Tab切换**
```jsx
function ModifyTaskManagementModule() {
  const [activeTab, setActiveTab] = useState('before');
  
  return (
    <div className="modify-module">
      <div className="tabs">
        <button 
          className={activeTab === 'before' ? 'active' : ''}
          onClick={() => setActiveTab('before')}
        >
          Before（当前版本）
        </button>
        <button 
          className={activeTab === 'after' ? 'active' : ''}
          onClick={() => setActiveTab('after')}
        >
          After（调整后）
        </button>
      </div>
      
      {activeTab === 'before' && <BeforeView />}
      {activeTab === 'after' && <AfterView />}
    </div>
  );
}
```

#### 删除界面原型

显示"已删除"通知和影响说明：

```jsx
function DeletedQualityAuditModule() {
  return (
    <div className="deleted-module">
      <div className="module-header">
        <h2>删除模块：M4 质量审核</h2>
        <span className="badge-deleted">DELETED</span>
      </div>
      
      <div className="deletion-notice">
        <div className="icon-warning">⚠️</div>
        <h3>此模块已在本次迭代中删除</h3>
        
        <div className="deletion-details">
          <h4>删除原因</h4>
          <p>[引用Step 3中的删除原因]</p>
          
          <h4>影响范围</h4>
          <ul>
            <li>流程影响：[说明]</li>
            <li>数据影响：[说明]</li>
            <li>依赖影响：[说明]</li>
          </ul>
          
          <h4>功能替代</h4>
          <p>[如果有替代方案，说明]</p>
        </div>
      </div>
    </div>
  );
}
```

#### 导航菜单

左侧导航按模块分组：

```jsx
function Sidebar() {
  return (
    <nav className="sidebar">
      <h3>原型导航</h3>
      
      <div className="module-group">
        <h4>✨ 新增模块</h4>
        <ul>
          <li><a href="#M6">M6 规则引擎</a></li>
        </ul>
      </div>
      
      <div className="module-group">
        <h4>🔄 调整模块</h4>
        <ul>
          <li><a href="#M2">M2 任务管理</a></li>
          <li><a href="#M3">M3 回访执行</a></li>
        </ul>
      </div>
      
      <div className="module-group">
        <h4>🗑️ 删除模块</h4>
        <ul>
          <li><a href="#M4">M4 质量审核</a></li>
        </ul>
      </div>
      
      <div className="module-group">
        <h4>📋 流程对比</h4>
        <ul>
          <li><a href="#flow-before">调整前流程</a></li>
          <li><a href="#flow-after">调整后流程</a></li>
        </ul>
      </div>
    </nav>
  );
}
```

### 呈现输出

使用 `present_files` 同时呈现差量PRD和原型：

```javascript
present_files([
  'project/06-output/delta-prd.md',
  'project/06-output/prototype.html'
]);
```

并向用户说明：

> "✅ 迭代设计完成！
> 
> **差量PRD**：包含完整的迭代说明、新增功能详述、调整功能before/after对比、删除影响分析、回滚预案
> 
> **修改后原型**：交互式原型，可查看：
> - 新增模块的完整界面
> - 调整模块的before/after对比
> - 删除模块的影响说明
> - 调整前后的流程对比
> 
> 请审阅以上产物，如有需要修改的地方请告诉我。
> 
> 下一步建议：
> - 灰度发布测试
> - 交付工程团队实施
> - 准备用户培训材料"

---

## End

迭代设计流程到此结束。

---
name: "prd-impact-analyzer"
description: "基于 Spec Coding 理念的 PRD 影响分析工具，采用渐进式上下文管理，专注于识别客户可见的前端变化，生成可执行的代码级影响规约 (Spec)，并支持通过 Workflow 编排实现自动化实施。"
version: "2.0.0"
last_updated: "2026-03-26"
author: "赵辉亮"
context_management: "progressive"  # 渐进式上下文管理模式
spec_driven: true  # 启用 Spec 驱动模式
workflow_compatible: true  # 支持 Workflow 编排
---

# PRD 影响范围分析器 (PRD Impact Analyzer) v2.0

## Skill 概览

### 核心理念
基于 **Spec Coding** 理念设计，将 PRD 需求转化为可执行的**代码变更规约 **(Code Change Spec)，而非直接生成代码。工程师审查和修改 Spec 后，再通过 AI 或手动方式实施变更，确保线上代码的可控性和稳定性。

### 设计原则
1. **Spec 优先**: 所有分析结果以结构化 Spec 形式呈现，便于审查和版本控制
2. **渐进式上下文**: 按需加载代码库信息，降低 token 消耗，提升长任务聚焦度
3. **客户体验导向**: 优先识别客户可见的前端变化，确保用户体验一致性
4. **Workflow 编排**: 支持将复杂分析任务拆解为多个单一职责的 Skill 组合
5. **可追溯性**: 建立 PRD 功能点 ↔ Code Spec ↔ Test Case 的双向追溯矩阵

### 适用场景
- ✅ 大型项目的 PRD 影响范围评估
- ✅ 跨团队协作的需求对接
- ✅ 代码变更评审 (Code Review) 前置分析
- ✅ 测试用例覆盖度验证
- ✅ 技术债务影响评估
- ❌ 简单需求直聊即可（杀鸡用牛刀）
- ❌ 紧急 Hotfix（流程过长）

核心功能

## 核心功能模块（采用 Skill 拆分策略）

### Skill-1: PRD 智能解析 (`prd-parser`)
**职责**: 多格式 PRD 文件解析与变更点提取

**功能**:
- [x] 多格式支持：`.md`, `.docx`, `.txt`, `.pdf` (通过 MCP 工具)
- [x] 变更点自动识别：使用 NLP 提取功能点、UI 需求、API 变更、业务逻辑
- [x] 影响标签提取：标记每个变更点的风险级别、影响范围、优先级
- [x] 结构化输出：生成标准化的 PRD-JSON 中间表示

**输入**: PRD 文件路径
**输出**: `PRD-Spec.json` (结构化变更点列表)

**Spec 示例**:
```json
{
  "change_point_id": "CP-001",
  "title": "用户角色权限细化",
  "type": "permission_system",
  "risk_level": "high",
  "customer_visible": false,
  "description": "将原有的'管理员/用户'两级权限改为'超级管理员/部门管理员/普通用户'三级权限体系",
  "acceptance_criteria": [...]
}
```


### Skill-2: 后端代码影响分析 (`backend-impact-analyzer`)
**职责**: 基于 AST 的 Java 代码变更规约生成

**功能**:
- [x] Java 代码解析：基于 AST 抽象语法树分析
- [x] 变更关联映射：PRD 功能点 ↔ Java 代码元素 (类/方法/字段)
- [x] 依赖链分析：识别级联影响 (调用图分析)
- [x] 测试用例识别：受影响的单元/集成测试，覆盖率检查
- [x] COLA 架构合规性检查：确保变更符合分层规范

**输入**: `PRD-Spec.json` + 项目根目录
**输出**: `Backend-Change-Spec.md` (结构化代码变更规约)

**Spec 格式**:
```markdown
## 后端变更规约

### CP-001: 用户角色权限细化

#### 需要修改的文件
1. UserController.java
   - 方法：getUserList(), updateUserRole()
   - 变更类型：MODIFY
   - 行号范围：45-89
   - 变更原因：查询逻辑需支持三级权限过滤
   
#### 变更伪代码
```java
// Before
public List<User> getUserList(String role) {
    return userRepository.findByRole(role);
}

// After (Spec 建议)
public List<User> getUserList(String role, Long departmentId) {
    // TODO: 实现三级权限过滤逻辑
    if ("dept_admin".equals(role)) {
        return userRepository.findByRoleAndDepartment(role, departmentId);
    }
    return userRepository.findByRole(role);
}
```

#### 测试要求
- [ ] UserControllerTest.testGetUserList_WithDepartment()
- [ ] UserServiceTest.testValidatePermission_ThreeLevels()
- [ ] 覆盖率要求：>= 90% (项目规范)
```


### Skill-3: 前端影响分析 (`frontend-impact-analyzer`)
**职责**: 客户可见的 UI/UX 变更规约生成

**功能**:
- [x] 前端框架识别：Vue/React/Angular (自动检测)
- [x] UI 组件定位：找出受影响的页面/组件
- [x] 样式影响分析：CSS/SCSS 变更识别
- [x] 用户流程分析：识别交互路径变化
- [x] 客户体验变化描述：视觉/交互/功能三维评估

**输入**: `PRD-Spec.json` + 前端源码目录
**输出**: `Frontend-Change-Spec.md` (含客户可见变化说明)

**Spec 格式**:
```markdown
## 前端变更规约 (客户可见)

### CP-001: 用户角色权限细化

#### 直接影响 (用户可感知)
1. UserManagement.vue - 筛选器组件
   - 变更类型：UI_MODIFICATION
   - 客户可见度：HIGH
   - 视觉变化：筛选器选项从 2 个增加到 3 个
   - 交互变化：无
   
   变更伪代码:
   ```vue
   <!-- Before -->
   <el-select v-model="filterRole">
     <el-option label="管理员" value="admin" />
     <el-option label="用户" value="user" />
   </el-select>
   
   <!-- After (Spec 建议) -->
   <el-select v-model="filterRole">
     <el-option label="超级管理员" value="super_admin" />
     <el-option label="部门管理员" value="dept_admin" />
     <el-option label="普通用户" value="user" />
   </el-select>
   ```

2. UserEditModal.vue - 角色分配表单
   - 变更类型：UI_REDESIGN
   - 客户可见度：MEDIUM
   - 视觉变化：角色分配从单选改为级联选择
   - 交互变化：需要先选部门再选角色
```

#### 性能影响评估
- 页面加载时间：+0.5-1 秒 (因新增级联选择器)
- 首屏渲染：不受影响
- 移动端适配：需要额外测试小屏显示


### Skill-4: 智能报告生成与 Spec 组装 (`report-generator`)
**职责**: 组装各子 Skill 输出，生成完整的 PRD 影响分析 Spec

**功能**:
- [x] 结构化影响报告：整合前后端变更规约
- [x] 代码标注与解释：自动生成变更说明注释
- [x] 变更建议生成：基于最佳实践的实施方案
- [x] 风险评分：量化评估实施风险 (1-10 分)
- [x] 实施清单生成：分阶段任务列表

**输入**: `Backend-Change-Spec.md` + `Frontend-Change-Spec.md`
**输出**: `PRD-Impact-Analysis-Spec.md` (最终可交付规约)


## Workflow 编排支持

### 标准工作流：`prd-to-spec-workflow`

针对复杂 PRD 分析任务，本 Skill 支持通过 Workflow 进行编排，拆分为以下执行步骤：

```yaml
workflow:
  name: prd-to-spec-workflow
  description: 从 PRD 到可执行 Spec 的完整工作流
  steps:
    - step: 1
      skill: prd-parser
      input: ${PRD_FILE}
      output: PRD-Spec.json
      
    - step: 2
      skill: backend-impact-analyzer
      input: PRD-Spec.json
      output: Backend-Change-Spec.md
      depends_on: [1]
      
    - step: 3
      skill: frontend-impact-analyzer
      input: PRD-Spec.json
      output: Frontend-Change-Spec.md
      depends_on: [1]
      
    - step: 4
      skill: report-generator
      input: [Backend-Change-Spec.md, Frontend-Change-Spec.md]
      output: PRD-Impact-Analysis-Spec.md
      depends_on: [2, 3]
      
    - step: 5
      skill: human-review
      input: PRD-Impact-Analysis-Spec.md
      action: 工程师审查和修改 Spec
      manual: true
      
    - step: 6
      skill: spec-to-code-generator (可选)
      input: Reviewed-Spec.md
      output: Code-Changes
      auto_generate: true
```

### 简化工作流：快速分析模式

对于简单需求，可直接调用单个 Skill 进行快速分析：
```bash
/kuspec:execute --skill prd-impact-analyzer --input simple-prd.md --mode quick
```

### WORKFLOW_INIT.md 模板

对于需要复杂上下文的场景，提供初始化模板：

```markdown
# PRD 分析工作流初始化

请提供以下信息以生成结构化输入文档：

## 1. PRD 基础信息
- PRD 文件路径：__________
- 业务域：用户管理 / 订单管理 / 设备管理 / ... (选择)
- 优先级：P0 / P1 / P2
- 预期上线时间：__________

## 2. 相关干系人
- 产品经理：__________
- 技术负责人：__________
- 测试负责人：__________

## 3. 技术约束
- 是否允许数据库变更：是 / 否
- 是否允许 API 破坏性变更：是 / 否
- 是否需要向后兼容：是 / 否

## 4. 特殊关注点
- 性能要求：__________
- 安全性要求：__________
- 合规性要求：__________
```

## 渐进式上下文管理策略

### 上下文加载策略

为了避免一次性加载过多信息导致 AI 失焦，采用渐进式加载：

**Level 1 - 初始上下文** (系统提示词中):
```
你是一个 PRD 影响分析专家，擅长将需求转化为可执行的代码变更规约。
可用技能列表:
- prd-parser: PRD 解析
- backend-impact-analyzer: 后端影响分析
- frontend-impact-analyzer: 前端影响分析
- report-generator: 报告生成
```

**Level 2 - 任务触发加载** (执行时动态获取):
```javascript
// MCP 工具定义
{
  "name": "get_codebase_structure",
  "description": "获取项目结构信息",
  "parameters": {"module": "string"}
}

{
  "name": "get_file_content",
  "description": "获取具体文件内容",
  "parameters": {"filePath": "string", "lines": "range"}
}

{
  "name": "search_symbol_usage",
  "description": "搜索符号使用情况",
  "parameters": {"symbolName": "string"}
}
```

**Level 3 - 深度分析加载** (按需检索):
```javascript
{
  "name": "analyze_dependency_graph",
  "description": "分析依赖关系图",
  "parameters": {"className": "string", "methodName": "string"}
}

{
  "name": "find_test_coverage",
  "description": "查找测试覆盖情况",
  "parameters": {"filePath": "string"}
}
```

## 完整输出示例 (Spec 格式)

### PRD-Impact-Analysis-Spec.md

> **说明**: 以下是 Spec Coding 模式下的标准输出格式，所有变更以**伪代码 + 变更说明**形式呈现，便于工程师审查和修改。

```markdown
# PRD 影响分析规约 (PRD Impact Analysis Spec)
**Spec ID**: SPEC-20260326-001  
**PRD 文件**: 用户管理系统 v2.0.prd  
**分析时间**: 2026-03-26T10:00:00Z  
**风险等级**: 中高 (评分：7.2/10)  
**客户可见变化**: 7 处  
**预计工作量**: 18 人日

## 📊 影响概览
- 后端影响文件: 18个
- 前端影响文件: 9个
- API接口变更: 5个
- 数据库变更: 2个表
- 客户可见变化: 7处

## 🔍 详细影响分析

### Spec-CP-001: 用户角色权限细化

**PRD 原文**: 
> 在用户管理页面，将原有的"管理员/用户"两级权限改为"超级管理员/部门管理员/普通用户"三级权限体系

**变更类型**: `PERMISSION_SYSTEM_REFACTOR`  
**优先级**: P0  
**客户可见**: 部分可见  
**预计工作量**: 5 人日

#### 后端变更规约
├── UserController.java (行45-89)
│   ├── 受影响方法: getUserList(), updateUserRole()
│   ├── 原因: 查询逻辑需支持三级权限过滤
│   └── 需要变更:
│       ▸ 修改查询条件，增加角色层级判断
│       ▸ UserQueryDTO需新增departmentId字段
│
├── UserService.java (行120-156)
│   ├── 受影响方法: validateUserPermission(), getFilteredUsers()
│   └── 需要变更: 重新实现权限验证逻辑
│
└── UserRepository.java (行78-82)
```java
// 变更位置：行 120-156
// 变更类型：REFACTOR
// 风险等级：CRITICAL

@Service
public class UserService {
    
    // BEFORE:
    // public boolean validateUserPermission(User user, String requiredRole) {
    //     return user.getRoles().contains(requiredRole);
    // }
    
    // AFTER (Spec 建议实现):
    public boolean validateUserPermission(User user, String requiredRole, Long targetDeptId) {
        // TODO: 重新实现权限验证逻辑
        // 1. 超级管理员拥有所有权限
        // 2. 部门管理员只能管理部门内用户
        // 3. 普通用户只能操作自己
        
        if (user.hasRole("super_admin")) {
            return true;
        }
        
        if (user.hasRole("dept_admin")) {
            return targetDeptId != null && targetDeptId.equals(user.getDepartmentId());
        }
        
        return user.getId().equals(targetUserId); // 普通用户
    }
}
```

**变更原因**: 三级权限体系核心逻辑  
**影响范围**: 所有权限校验场景  
**测试要求**: 
- [ ] 单元测试覆盖率 >= 90% (项目规范)
- [ ] 集成测试覆盖所有权限组合
- [ ] 边界 case: 跨部门访问、权限升级

##### 3. UserRepository.java
├── UserManagement.vue (客户直接可见)
│   ├── 受影响部分: 用户列表筛选组件
│   ├── 变更描述: 用户会看到筛选器从两级变为三级下拉选择
│   └── 需要变更:
│       ▸ roles数组从['admin','user']改为['super_admin','dept_admin','user']
│       ▸ 更新筛选组件的选项配置
│
├── UserEditModal.vue (客户直接可见)
│   ├── 受影响部分: 角色分配表单
│   ├── 变更描述: 角色分配界面从单选改为级联选择
│   └── 需要变更: 重新设计角色选择UI组件
│
└── src/api/user.js
└── 受影响接口: getUserList() 参数结构变更


**客户体验变化**:
1. 视觉变化: 筛选器选项从2个增加到3个
2. 交互变化: 角色分配需要先选择部门再选择具体角色
3. 功能变化: 部门管理员只能看到本部门用户

```vue
<!-- 变更位置：第 89-134 行 -->
<!-- 变更类型：UI_REDESIGN -->
<!-- 客户可见度：MEDIUM -->

<template>
  <el-dialog title="编辑用户">
    <!-- BEFORE: 单选 -->
    <!-- AFTER: 级联选择器 -->
    <el-form-item label="角色权限">
      <el-cascader
        v-model="form.roleCascade"
        :options="roleOptions"
        @change="handleRoleChange"
      />
    </el-form-item>
  </el-dialog>
</template>
```

**客户体验变化**:
- ✅ 交互变化：角色分配从单选改为级联选择
- ⚠️ UI 响应时间：+0.3 秒
**PRD描述**: 在用户管理页面添加活跃度统计图表，展示最近30天用户登录趋势

**影响分析**:

📁 后端影响:
├── UserStatController.java (新文件)
│   └── 需要新增: getActiveStatistics() API接口
│
├── UserStatService.java (新文件)
│   └── 需要新增: calculateActivityTrend() 业务逻辑
│
└── LoginLogRepository.java
└── 受影响查询: 需新增findRecentLoginCounts()方法

📁 前端影响 (客户可见变化):
├── UserManagement.vue
│   ├── 新增部分: 活跃度统计图表区域
│   ├── 变更描述: 用户在列表页上方会看到新的统计图表
│   └── 需要变更:
│       ▸ 引入ECharts图表库
│       ▸ 新增统计图表组件ActivityChart.vue
│       ▸ 添加日期选择器组件
│
└── src/api/user.js
└── 新增接口: getActiveStatistics()


**客户体验变化**:
1. 新增功能: 页面顶部增加可视化统计图表
2. 数据展示: 可切换查看不同时间段的活跃趋势
3. 交互增强: 支持图表点击查看详情

## 🎯 客户可见变化汇总

### 直接影响 (用户可直接感知)
1. **界面布局变更**: 用户管理页面增加统计图表区域
2. **筛选功能变更**: 角色筛选从两级变为三级级联选择
3. **数据展示变更**: 用户列表新增"最后活跃时间"列
4. **操作流程变更**: 编辑用户需要先选择部门再选角色
5. **权限提示变更**: 无权限操作时显示更详细的说明

### 间接影响 (用户体验相关)
1. **页面加载时间**: 因统计图表增加，页面初始加载可能慢0.5-1秒
2. **数据时效性**: 活跃度统计有1小时延迟
3. **移动端适配**: 统计图表在小屏上可能显示不全

## ⚠️ 风险评估

### 高风险区域
1. **权限验证逻辑** (后端: UserService.java)
    - 影响范围: 所有用户相关操作
    - 风险: 权限漏洞可能导致越权访问
    - 建议: 需要完整的单元测试覆盖

2. **级联选择组件** (前端: UserEditModal.vue)
    - 影响范围: 所有用户编辑场景
    - 风险: 级联逻辑复杂，易出BUG
    - 建议: 先做A/B测试

### 中等风险区域
1. **统计图表数据准确性**
2. **数据库查询性能**

## 📋 实施清单

### 第一阶段: 后端变更

[ ] 1. UserController.java - 修改查询接口
[ ] 2. UserService.java - 重构权限验证
[ ] 3. 新增UserStatController.java
[ ] 4. 数据库变更脚本


### 第二阶段: 前端变更

[ ] 1. UserManagement.vue - 集成统计图表
[ ] 2. 新增ActivityChart.vue组件
[ ] 3. 修改角色选择组件为级联选择
[ ] 4. 更新API调用层


### 第三阶段: 测试验证

[ ] 1. 权限功能测试
[ ] 2. 图表展示测试
[ ] 3. 性能测试
[ ] 4. 跨浏览器兼容性测试
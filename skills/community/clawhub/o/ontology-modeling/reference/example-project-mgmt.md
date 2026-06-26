# 完整示例：项目管理 Ontology

这是功能1/2/3/4 的端到端参考示例，用于验证输出格式是否正确。

## 业务场景

一家公司需要管理员工、项目和任务，支持分配、绩效计算和统一的"可分配"视图。

---

## 输出1：JSON（`project_mgmt_ontology.json`）

```json
{
  "ontology": {
    "name": "project_mgmt",
    "description": "项目管理本体，覆盖员工、项目、任务的分配与绩效计算",
    "version": "1.0"
  },
  "object_types": [
    {
      "api_name": "employee",
      "display_name": "Employee",
      "description": "公司正式员工，包含人力资源系统中的基本信息",
      "primary_key": "employee_id",
      "properties": [
        { "api_name": "employee_id", "type": "string", "description": "UUID 主键" },
        { "api_name": "name", "type": "string", "description": "员工姓名" },
        { "api_name": "department", "type": "string", "description": "所属部门" },
        { "api_name": "level", "type": "integer", "description": "职级" },
        { "api_name": "performance_score", "type": "double", "description": "绩效评分，由 Function 派生", "derived": true }
      ],
      "implements_interfaces": []
    },
    {
      "api_name": "project",
      "display_name": "Project",
      "description": "公司内部项目，包含项目状态和截止日期",
      "primary_key": "project_id",
      "properties": [
        { "api_name": "project_id", "type": "string", "description": "UUID 主键" },
        { "api_name": "name", "type": "string", "description": "项目名称" },
        { "api_name": "status", "type": "string", "description": "项目状态：active/completed/cancelled" },
        { "api_name": "deadline", "type": "date", "description": "截止日期" }
      ],
      "implements_interfaces": ["assignable"]
    },
    {
      "api_name": "task",
      "display_name": "Task",
      "description": "项目下的具体执行单元",
      "primary_key": "task_id",
      "properties": [
        { "api_name": "task_id", "type": "string", "description": "UUID 主键" },
        { "api_name": "title", "type": "string", "description": "任务标题" },
        { "api_name": "status", "type": "string", "description": "任务状态：todo/in_progress/done" },
        { "api_name": "due_date", "type": "date", "description": "截止日期" }
      ],
      "implements_interfaces": ["assignable"]
    }
  ],
  "link_types": [
    {
      "api_name": "employee_participates_in_project",
      "display_name_left": "参与的项目",
      "display_name_right": "参与的员工",
      "left": "employee",
      "right": "project",
      "cardinality": "MANY_TO_MANY",
      "direction": "BIDIRECTED",
      "implementation": "join_table",
      "link_properties": [
        { "api_name": "role", "type": "string", "description": "员工在项目中的角色" },
        { "api_name": "start_date", "type": "date", "description": "加入项目日期" }
      ]
    },
    {
      "api_name": "employee_manages_project",
      "display_name_left": "管理的项目",
      "display_name_right": "项目经理",
      "left": "employee",
      "right": "project",
      "cardinality": "MANY_TO_MANY",
      "direction": "DIRECTED",
      "implementation": "join_table",
      "link_properties": []
    },
    {
      "api_name": "project_contains_task",
      "display_name_left": "包含的任务",
      "display_name_right": "所属项目",
      "left": "project",
      "right": "task",
      "cardinality": "ONE_TO_MANY",
      "direction": "DIRECTED",
      "implementation": "foreign_key",
      "link_properties": []
    }
  ],
  "action_types": [
    {
      "api_name": "assign_employee_to_project",
      "display_name": "分配员工到项目",
      "description": "在员工和项目之间创建参与链接",
      "parameters": [
        { "api_name": "employee_id", "type": "string", "required": true },
        { "api_name": "project_id", "type": "string", "required": true },
        { "api_name": "role", "type": "string", "required": false }
      ],
      "side_effects": [
        { "type": "create_link", "link_type": "employee_participates_in_project", "transaction": "sync" }
      ]
    },
    {
      "api_name": "update_task_status",
      "display_name": "更新任务状态",
      "description": "修改任务的当前状态",
      "parameters": [
        { "api_name": "task_id", "type": "string", "required": true },
        { "api_name": "status", "type": "string", "required": true }
      ],
      "side_effects": [
        { "type": "modify_object", "object_type": "task", "transaction": "sync" }
      ]
    }
  ],
  "functions": [
    {
      "api_name": "calculate_performance_score",
      "type": "object_function",
      "target": "employee",
      "description": "计算员工绩效评分：完成项目数 / 总参与项目数 × 100",
      "cache_ttl_minutes": 5,
      "output_property": "performance_score"
    }
  ],
  "interfaces": [
    {
      "api_name": "assignable",
      "display_name": "Assignable",
      "description": "可被分配给负责人的对象，统一分配视图和分配操作",
      "shared_properties": [
        { "api_name": "assignee_id", "type": "string", "description": "负责人 ID" },
        { "api_name": "assigned_at", "type": "timestamp", "description": "分配时间" }
      ],
      "implemented_by": ["project", "task"]
    }
  ]
}
```

---

## 输出2：Markdown（`project_mgmt_ontology.md`）

```markdown
# 项目管理 Ontology 设计文档

## Object Types

### Employee（员工）
- **API Name**: employee
- **主键**: employee_id (UUID)
- **描述**: 公司正式员工，包含人力资源系统中的基本信息
- **属性**: name, department, level, performance_score（派生）
- **实现接口**: 无

### Project（项目）
- **API Name**: project
- **主键**: project_id (UUID)
- **描述**: 公司内部项目，包含项目状态和截止日期
- **属性**: name, status, deadline
- **实现接口**: Assignable

### Task（任务）
- **API Name**: task
- **主键**: task_id (UUID)
- **描述**: 项目下的具体执行单元
- **属性**: title, status, due_date
- **实现接口**: Assignable

## Link Types

| API Name | 左端 | 右端 | 基数 | 方向 | 实现方式 |
|----------|------|------|------|------|---------|
| employee_participates_in_project | Employee | Project | M:N | BIDIRECTED | 关联表 |
| employee_manages_project | Employee | Project | M:N | DIRECTED | 关联表 |
| project_contains_task | Project | Task | 1:N | DIRECTED | 外键 |

## Action Types

| API Name | 副作用 | 事务 |
|----------|--------|------|
| assign_employee_to_project | Create Link | 同步 |
| update_task_status | Modify Object | 同步 |

## Functions

| API Name | 类型 | 挂载对象 | TTL |
|----------|------|---------|-----|
| calculate_performance_score | Object Function | Employee | 5分钟 |

## Interfaces

### Assignable（可分配）
- **共享属性**: assignee_id, assigned_at
- **实现者**: Project, Task
```

---

## 输出3：OWL/Turtle（`project_mgmt_ontology.ttl`）

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sc: <https://ontology.project-mgmt.local/> .

# ── Interfaces（作为 owl:Class）
sc:Assignable a owl:Class ;
    rdfs:label "Assignable" ;
    rdfs:comment "可被分配给负责人的对象，统一分配视图和分配操作" .

# ── Link Type 关联类（M:N 携带属性时建模为独立 Class）
sc:EmployeeProjectParticipation a owl:Class ;
    rdfs:label "EmployeeProjectParticipation" ;
    rdfs:comment "员工参与项目的关联实体，携带 role 和 start_date" .

# ── Object Types
sc:Employee a owl:Class ;
    rdfs:label "Employee" ;
    rdfs:comment "公司正式员工，包含人力资源系统中的基本信息" .

sc:Project a owl:Class ;
    rdfs:label "Project" ;
    rdfs:comment "公司内部项目，包含项目状态和截止日期" ;
    rdfs:subClassOf sc:Assignable .

sc:Task a owl:Class ;
    rdfs:label "Task" ;
    rdfs:comment "项目下的具体执行单元" ;
    rdfs:subClassOf sc:Assignable .

# ── Employee 属性（同名属性加前缀区分，避免 domain 冲突）
sc:employee_id a owl:DatatypeProperty ; rdfs:domain sc:Employee ; rdfs:range xsd:string ; rdfs:label "employee_id" .
sc:employee_name a owl:DatatypeProperty ; rdfs:domain sc:Employee ; rdfs:range xsd:string ; rdfs:label "name" .
sc:department a owl:DatatypeProperty ; rdfs:domain sc:Employee ; rdfs:range xsd:string ; rdfs:label "department" .
sc:level a owl:DatatypeProperty ; rdfs:domain sc:Employee ; rdfs:range xsd:integer ; rdfs:label "level" .

# ── Project 属性
sc:project_id a owl:DatatypeProperty ; rdfs:domain sc:Project ; rdfs:range xsd:string ; rdfs:label "project_id" .
sc:project_name a owl:DatatypeProperty ; rdfs:domain sc:Project ; rdfs:range xsd:string ; rdfs:label "name" .
sc:status a owl:DatatypeProperty ; rdfs:domain sc:Project ; rdfs:range xsd:string ; rdfs:label "status" .
sc:deadline a owl:DatatypeProperty ; rdfs:domain sc:Project ; rdfs:range xsd:date ; rdfs:label "deadline" .

# ── Task 属性
sc:task_id a owl:DatatypeProperty ; rdfs:domain sc:Task ; rdfs:range xsd:string ; rdfs:label "task_id" .
sc:title a owl:DatatypeProperty ; rdfs:domain sc:Task ; rdfs:range xsd:string ; rdfs:label "title" .
sc:task_status a owl:DatatypeProperty ; rdfs:domain sc:Task ; rdfs:range xsd:string ; rdfs:label "status" .
sc:due_date a owl:DatatypeProperty ; rdfs:domain sc:Task ; rdfs:range xsd:date ; rdfs:label "due_date" .

# ── Interface 共享属性
sc:assignee_id a owl:DatatypeProperty ; rdfs:domain sc:Assignable ; rdfs:range xsd:string ; rdfs:label "assignee_id" .
sc:assigned_at a owl:DatatypeProperty ; rdfs:domain sc:Assignable ; rdfs:range xsd:dateTime ; rdfs:label "assigned_at" .

# ── Link Types（ObjectProperty）
sc:participatesIn a owl:ObjectProperty ; rdfs:label "employee_participates_in_project" ; rdfs:domain sc:Employee ; rdfs:range sc:Project ; rdfs:comment "M:N BIDIRECTED，关联表实现" .
sc:manages a owl:ObjectProperty ; rdfs:label "employee_manages_project" ; rdfs:domain sc:Employee ; rdfs:range sc:Project ; rdfs:comment "M:N DIRECTED，关联表实现" .
sc:containsTask a owl:ObjectProperty ; rdfs:label "project_contains_task" ; rdfs:domain sc:Project ; rdfs:range sc:Task ; rdfs:comment "1:N DIRECTED，外键实现" .

# ── Link Properties（关联类属性，M:N 携带属性时挂在关联类上）
sc:participationEmployee a owl:ObjectProperty ; rdfs:domain sc:EmployeeProjectParticipation ; rdfs:range sc:Employee ; rdfs:label "employee" .
sc:participationProject a owl:ObjectProperty ; rdfs:domain sc:EmployeeProjectParticipation ; rdfs:range sc:Project ; rdfs:label "project" .
sc:role a owl:DatatypeProperty ; rdfs:domain sc:EmployeeProjectParticipation ; rdfs:range xsd:string ; rdfs:label "role" ; rdfs:comment "员工在项目中的角色" .
sc:start_date a owl:DatatypeProperty ; rdfs:domain sc:EmployeeProjectParticipation ; rdfs:range xsd:date ; rdfs:label "start_date" ; rdfs:comment "加入项目日期" .
```

> **TTL 建模注意事项：**
> - 同名属性（如 `name`、`status`）在不同 Object Type 上需用不同 URI（`sc:employee_name`、`sc:project_name`）避免 domain 冲突
> - M:N Link Type 携带属性时，OWL 里建模为独立关联类（Reification），而非直接 ObjectProperty
> - 无属性的 Link Type（如 `project_contains_task`）直接用 `owl:ObjectProperty` 即可

---

## 输出4：可视化 HTML

生成 `project_mgmt_graph.html` 时，将 `reference/visualization-template.html` 中的 `GRAPH` 对象替换为：

```javascript
const GRAPH = {
  title: "项目管理 Ontology",
  nodes: [
    { id: "employee", label: "Employee", type: "object", x: 200, y: 220,
      desc: "公司正式员工，包含人力资源系统中的基本信息",
      props: ["api_name: employee", "主键: employee_id (UUID)", "属性: name, department, level", "派生: performance_score"] },
    { id: "project", label: "Project", type: "object", x: 560, y: 220,
      desc: "公司内部项目，包含项目状态和截止日期",
      props: ["api_name: project", "主键: project_id (UUID)", "属性: name, status, deadline"] },
    { id: "task", label: "Task", type: "object", x: 560, y: 400,
      desc: "项目下的具体执行单元",
      props: ["api_name: task", "主键: task_id (UUID)", "属性: title, status, due_date"] },
    { id: "assignable", label: "Assignable", type: "interface", x: 380, y: 400,
      desc: "可被分配给负责人的对象，统一分配视图",
      props: ["共享属性: assignee_id, assigned_at", "实现者: Project, Task"] },
    { id: "assign_action", label: "assign_employee\n_to_project", type: "action", x: 200, y: 400,
      desc: "分配员工到项目，Create Link 副作用，同步事务",
      props: ["副作用: Create Link (同步)", "生命周期: 7阶段"] },
    { id: "perf_fn", label: "calculate\nPerformanceScore", type: "function", x: 380, y: 80,
      desc: "计算员工绩效评分，Object Function，TTL 5分钟",
      props: ["类型: Object Function", "缓存: TTL 5分钟", "纯函数: 不能有副作用"] }
  ],
  edges: [
    { from: "employee", to: "project", label: "participates_in (M:N)", curve: -40 },
    { from: "employee", to: "project", label: "manages (M:N)", curve: 40 },
    { from: "project", to: "assignable", label: "implements", dashed: true },
    { from: "task", to: "assignable", label: "implements", dashed: true },
    { from: "assign_action", to: "employee", label: "操作对象" },
    { from: "perf_fn", to: "employee", label: "派生属性" }
  ]
};
```

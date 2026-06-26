---
name: neo4j-cypher-query-analyze
version: 1.0.0
description: 智能图数据库查询助手 - 自动感知 Schema 结构，根据自然语言生成精准的 Cypher 查询
trigger: "图查询|graph query|cypher|知识图谱|neo4j查询|图谱分析"
tools: [shell, http, filesystem, memory]
author: your-name
metadata:
 openclaw:
   emoji: 🧠
   requires:
     bins: ["curl"]
     env: ["GRAPHDB_URI", "GRAPHDB_USER", "GRAPHDB_PASSWORD", "GRAPHDB_DATABASE"]
     optional_env: ["GRAPHDB_TYPE"]  # neo4j, neptune, janusgraph
---

# 智能图数据库查询助手 (Schema-Aware Graph Query Assistant)

## 核心能力
1. **自动 Schema 感知**：首次查询时自动获取图数据库的节点标签、关系类型和属性结构
2. **智能 Cypher 生成**：基于真实 Schema 结构，将自然语言转换为精准的 Cypher 查询
3. **上下文记忆**：缓存 Schema 信息和常用查询模式，提升后续查询效率
4. **安全执行**：严格的查询审查机制，防止破坏性操作和性能风险

---

## 系统架构

```
用户提问 → Schema 获取(如需要) → 意图分析 → Cypher 生成 → 安全检查 → 执行查询 → 结果格式化
```

---

## 第一阶段：Schema 感知与缓存

### Schema 获取策略

在首次查询或 Schema 缓存过期时，执行以下探测查询：

**1. 获取所有节点标签**
```cypher
CALL db.labels() YIELD label RETURN collect(label) AS nodeLabels
```

**2. 获取所有关系类型**
```cypher
CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) AS relTypes
```

**3. 获取属性键（可选，用于理解常用属性）**
```cypher
CALL db.propertyKeys() YIELD propertyKey RETURN collect(propertyKey) AS propertyKeys
```

**4. 获取 Schema 可视化（Neo4j 特定）**
```cypher
CALL db.schema.visualization()
```

**5. 采样各标签的典型节点（理解属性结构）**
对每个重要标签执行：
```cypher
MATCH (n:LabelName)
RETURN n LIMIT 1
```

**6. 采样关系结构**
```cypher
MATCH ()-[r:REL_TYPE]->()
RETURN type(r) as rel_type, keys(r) as properties LIMIT 1
```

### Schema 缓存机制

使用 `memory` 工具缓存 Schema 信息：

```yaml
# 缓存键: graphdb_schema_{database_name}
# 内容结构:
schema_cache:
 timestamp: "2024-01-15T10:30:00Z"
 ttl_hours: 24
 node_labels:
   - Person:
       sample_properties: [name, age, email, created_at]
       estimated_count: 15000
   - Company:
       sample_properties: [name, industry, registered_capital]
       estimated_count: 5000
   - Product:
       sample_properties: [name, category, price]
 relationship_types:
   - WORKS_AT:
       start_labels: [Person]
       end_labels: [Company]
       properties: [since, position]
   - MANAGES:
       start_labels: [Person]
       end_labels: [Person]
   - PRODUCES:
       start_labels: [Company]
       end_labels: [Product]
 indexes:
   - :Person(id)
   - :Company(name)
 constraints:
   - :Person(email) UNIQUE
```

---

## 第二阶段：智能查询生成

### 意图分析框架

将用户查询分类为以下模式：

| 查询模式 | 描述 | 示例 |
|---------|------|------|
| **实体查找** | 按属性查找特定节点 | "查找叫张三的客户" |
| **关系探索** | 查找节点的关联关系 | "张三的朋友有哪些" |
| **路径发现** | 查找两个节点间的路径 | "张三和李四之间有什么关系" |
| **模式匹配** | 特定子图结构查询 | "查找三角担保关系" |
| **统计分析** | 聚合计算 | "每个公司的平均员工数" |
| **元数据查询** | 查询 Schema 本身 | "数据库里有哪些实体类型" |

### Cypher 生成规则

基于 Schema 缓存生成查询时遵循：

**1. 标签匹配规则**
- 用户提到的实体名称 → 匹配 `node_labels` 中最相似的标签
- 使用 Levenshtein 距离或语义相似度进行模糊匹配
- 歧义时询问用户确认（如 "客户" 对应 `Customer` 还是 `Client`）

**2. 属性推断规则**
- 优先使用索引属性（如 `id`, `email`）进行过滤
- 字符串匹配使用 `CONTAINS` 或 `STARTS WITH` 而非精确匹配（除非用户明确）
- 数值范围使用 `>=` 和 `<=`

**3. 关系导航规则**
- 根据 Schema 确定有效的 `(start_label)-[REL]->(end_label)` 组合
- 双向关系使用 `-[:REL]-` 而非 `->`
- 多跳查询限制最大深度（默认 3，防止路径爆炸）

**4. 性能优化规则**
- 所有查询必须包含 `LIMIT`（默认 100，最大 1000）
- 避免 `MATCH (n)` 全节点扫描
- 优先使用 `MATCH` 而非 `OPTIONAL MATCH` 除非明确需要
- 复杂聚合使用 `WITH` 进行管道处理

---

## 第三阶段：安全与执行

### 查询安全检查 (Guardrails)

在执行前进行多层审查：

**1. 操作类型检查**
```python
# 伪代码逻辑
write_keywords = ['CREATE', 'DELETE', 'SET', 'REMOVE', 'MERGE', 'DROP', 'LOAD']
if any(kw in query.upper() for kw in write_keywords):
   require_explicit_confirmation()
   log_audit_trail()
```

**2. 复杂度评估**
- 计算估计的节点扫描量（基于标签选择性和过滤条件）
- 深度超过 4 的关系路径查询需要警告
- 全图遍历查询（无标签限制）直接拒绝

**3. 敏感数据保护**
- 检测到属性名包含 `password`, `token`, `secret`, `ssn` 时自动脱敏
- 返回前扫描结果集，对敏感字段进行掩码处理（如 `***`）

**4. 超时控制**
- 设置 30 秒查询超时
- 超时后自动终止并建议优化查询（添加索引提示或限制条件）

### 执行与错误处理

**HTTP API 调用模板：**
```bash
# Neo4j HTTP API
curl -s -X POST \
 -H "Content-Type: application/json" \
 -H "Accept: application/json" \
 -u "${GRAPHDB_USER}:${GRAPHDB_PASSWORD}" \
 "${GRAPHDB_URI}/db/${GRAPHDB_DATABASE}/tx/commit" \
 -d "{
   \"statements\": [{
     \"statement\": \"${CYPHER_QUERY}\",
     \"parameters\": ${PARAMETERS_JSON:-{}},
     \"resultDataContents\": [\"row\", \"graph\"]
   }]
 }" 2>&1
```

**错误分类处理：**

| 错误类型 | 识别特征 | 处理策略 |
|---------|---------|---------|
| 连接失败 | `Failed to connect`, `Connection refused` | 检查 URI 和网络，提示验证服务状态 |
| 认证失败 | `Unauthorized`, `Authentication failed` | 提示检查用户名密码，不暴露具体错误 |
| 语法错误 | `InvalidSyntax`, `SyntaxError` | 展示生成的查询，高亮错误位置，建议修正 |
| 语义错误 | `Label not found`, `Property not found` | 对比 Schema 缓存，提示可用的标签/属性 |
| 性能超时 | `Transaction timed out` | 建议添加 LIMIT、缩小过滤范围、或创建索引 |
| 权限不足 | `Forbidden`, `Access denied` | 提示当前用户权限限制，建议联系管理员 |

---

## 第四阶段：结果格式化

### 输出格式策略

根据返回数据类型自动选择最佳展示方式：

**1. 表格视图（默认）**
适用于：属性列表、聚合统计
```markdown
| 姓名 | 年龄 | 所属公司 | 入职年份 |
|------|------|----------|----------|
| 张三 | 32 | 科技有限公司 | 2019 |
| 李四 | 28 | 创新网络公司 | 2021 |
```

**2. 关系图谱描述**
适用于：路径、子图结构
```markdown
**关系路径 (长度: 2)**

张三 (Person, 35岁) -[WORKS_AT {since: 2019, position: "工程师"}]->
科技有限公司 (Company, 互联网) -[PRODUCES {category: "SaaS"}]->
智能云平台 (Product, 2023年发布)
```

**3. 统计卡片**
适用于：聚合查询
```markdown
📊 **统计结果**
- 总节点数: 1,234
- 平均年龄: 34.5 岁
- 最大关系深度: 5
- 最密集连接节点: 科技有限公司 (连接数: 156)
```

**4. JSON 原始数据**
适用于：开发者调试、后续程序处理
```json
{
 "columns": ["name", "count"],
 "data": [
   {"name": "科技有限公司", "count": 42},
   {"name": "创新网络", "count": 28}
 ]
}
```

---

## 完整工作流程示例

### 场景：首次查询（无 Schema 缓存）

**用户输入**: "查找所有在科技有限公司工作的工程师，并显示他们的入职年份"

**执行流程**:

1. **检查 Schema 缓存**
  - 查询 `memory` 工具：无有效缓存或缓存过期
  - 决定：执行 Schema 探测

2. **Schema 探测执行**
  ```bash
  # 获取标签
  curl ... -d '{"statements":[{"statement":"CALL db.labels() YIELD label RETURN collect(label) AS labels"}]}'
  # 返回: ["Person", "Company", "Product", "Department"]

  # 获取关系类型
  curl ... -d '{"statements":[{"statement":"CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) AS types"}]}'
  # 返回: ["WORKS_AT", "MANAGES", "BELONGS_TO", "PRODUCES"]

  # 采样 Person 节点
  curl ... -d '{"statements":[{"statement":"MATCH (p:Person) RETURN p LIMIT 2"}]}'
  # 返回属性: name, age, position, email, hire_date

  # 采样 WORKS_AT 关系
  curl ... -d '{"statements":[{"statement":"MATCH ()-[r:WORKS_AT]->() RETURN r LIMIT 1"}]}'
  # 返回属性: since, department, level
  ```

3. **Schema 分析**
  - 实体匹配：
    - "科技有限公司" → 可能是 `Company.name`（模糊匹配）
    - "工程师" → 可能是 `Person.position` 或 `WORKS_AT.level`
  - 关系确认：`Person -[WORKS_AT]-> Company` 是有效路径
  - 属性确认：`hire_date` 或 `WORKS_AT.since` 可用于"入职年份"

4. **生成 Cypher**
  ```cypher
  MATCH (p:Person)-[w:WORKS_AT]->(c:Company)
  WHERE c.name CONTAINS '科技' AND
        (p.position CONTAINS '工程师' OR w.level CONTAINS '工程师')
  RETURN p.name AS 姓名,
         p.age AS 年龄,
         c.name AS 公司,
         w.since AS 入职年份,
         w.department AS 部门
  ORDER BY w.since DESC
  LIMIT 50
  ```

5. **安全检查**
  - ✓ 读操作 only
  - ✓ 包含 LIMIT 50
  - ✓ 有标签限制（非全表扫描）
  - ✓ 无敏感字段暴露风险

6. **执行查询** → 获取结果

7. **格式化输出**
  ```markdown
  🔍 **查询结果**: 找到 12 位工程师

  | 姓名 | 年龄 | 公司 | 入职年份 | 部门 |
  |------|------|------|----------|------|
  | 王五 | 29 | 科技有限公司 | 2021 | 研发部 |
  | 赵六 | 34 | 科技有限公司 | 2019 | 产品部 |
  | ... | ... | ... | ... | ... |

  📈 **统计**: 平均工龄 3.5 年，最早入职者为 2015 年
  ```

8. **更新 Schema 缓存**
  - 保存到 `memory`：`graphdb_schema_default`
  - 记录本次成功查询模式：`Person-WORKS_AT-Company` 关联查询

---

### 场景：后续查询（使用缓存）

**用户输入**: "显示这些工程师的管理者是谁"

**执行流程**:

1. **读取 Schema 缓存**
  - 从 `memory` 获取：`graphdb_schema_default`
  - 确认缓存有效（< 24 小时）

2. **上下文关联**
  - 检测到指代："这些工程师" → 引用上次的 `Person` 结果集
  - 或者理解为：查找所有工程师的管理者

3. **Schema 辅助生成**
  - 检查 `MANAGES` 关系：`Person -[MANAGES]-> Person`
  - 确认双向可能性：可能是 `p<-[:MANAGES]-(manager)` 或 `p-[:MANAGES]->(subordinate)`
  - 根据"管理者"语义，确定为入边方向

4. **生成 Cypher**
  ```cypher
  MATCH (p:Person)-[:WORKS_AT]->(c:Company)
  WHERE c.name CONTAINS '科技' AND p.position CONTAINS '工程师'
  OPTIONAL MATCH (manager:Person)-[:MANAGES]->(p)
  RETURN p.name AS 工程师,
         manager.name AS 直接上级,
         manager.position AS 上级职位
  LIMIT 50
  ```

5. **执行与返回**

---

## 高级功能

### 查询解释模式

当用户问"为什么会这样查"时，展示推理过程：

```markdown
**🧠 查询推理过程**

1. **实体识别**:
  - "工程师" → 匹配到标签 `Person`，属性 `position`（置信度 0.92）
  - "科技有限公司" → 匹配到标签 `Company`，属性 `name`（模糊匹配）

2. **关系推断**:
  - 人员与公司的工作关系 → Schema 中存在 `WORKS_AT` 关系
  - 方向确定为 `(Person)-[:WORKS_AT]->(Company)`

3. **过滤条件**:
  - 使用 `CONTAINS` 而非 `=`，因为用户可能输入公司简称
  - 工程师匹配同时检查 `Person.position` 和 `WORKS_AT.level`（增加召回率）

4. **性能优化**:
  - 假设 `Company.name` 有索引（从 Schema 元数据确认）
  - 添加 `LIMIT 50` 防止大数据集性能问题
```

### 渐进式查询构建

对于复杂查询，支持分步构建：

**用户**: "查找风险等级为高的客户"

→ 执行，返回结果

**用户**: "只看那些担保金额超过 100 万的"

→ 理解上下文，在上次查询基础上添加：
```cypher
MATCH (c:Customer {risk_level: 'HIGH'})-[g:GUARANTEE]-(target)
WHERE g.amount > 1000000
RETURN ...
```

### Schema 变更检测

每次查询前快速验证 Schema 版本：
```cypher
CALL dbms.components() YIELD versions
```
如果检测到版本变更或缓存过期，自动刷新 Schema。

---

## 配置参考

### 环境变量
`~/.openclaw/skills/graphdb-schema-aware-query/.env`

### 本地配置文件
`~/.openclaw/skills/graphdb-schema-aware-query/config.yaml`

---

## 使用示例

### 示例 1：基础实体查询
**用户**: "查找姓张的所有客户，按注册时间排序"

**AI 思考**:
- Schema 确认：存在 `Customer` 标签，有 `name` 和 `registered_at` 属性
- 生成：`MATCH (c:Customer) WHERE c.name STARTS WITH '张' RETURN c ORDER BY c.registered_at DESC LIMIT 50`

### 示例 2：关系探索
**用户**: "显示客户 C10086 的所有担保关系，包括被担保方和担保金额"

**AI 思考**:
- Schema 确认：存在 `GUARANTEE` 关系，有 `amount` 属性
- 方向确认：`Customer -[GUARANTEE]-> Customer`（自查 Schema 缓存）
- 生成：双向查询确保捕获担保和被担保
```cypher
MATCH (c:Customer {id: 'C10086'})-[g:GUARANTEE]-(other:Customer)
RETURN other.name AS 相关客户,
      type(g) AS 关系类型,
      g.amount AS 担保金额,
      CASE WHEN startNode(g) = c THEN '对外担保' ELSE '被担保' END AS 方向
ORDER BY g.amount DESC
```

### 示例 3：复杂路径查询
**用户**: "张三和李四之间是否存在任何间接的投资关系？"

**AI 思考**:
- Schema 确认：存在 `INVEST` 关系，连接 `Person` 或 `Company`
- 路径分析：需要可变长度路径，最大深度 3
- 生成：
```cypher
MATCH path = (a:Person {name: '张三'})-[*1..3]-(b:Person {name: '李四'})
WHERE ALL(r IN relationships(path) WHERE type(r) = 'INVEST')
RETURN path, length(path) AS 层级
LIMIT 10
```

### 示例 4：元数据查询
**用户**: "这个数据库里存储了哪些类型的数据？"

**AI 思考**:
- 识别为元数据查询，直接返回 Schema 缓存内容
- 无需执行 Cypher，从缓存提取标签和关系统计

---

## 故障排除

### Schema 获取失败
- **症状**: "无法获取数据库结构"
- **检查**:
 1. 确认 Neo4j 版本支持 `db.schema.visualization()`（3.5+）
 2. 检查用户权限：`SHOW USER PRIVILEGES`
 3. 备选方案：使用 `CALL db.labels()` + `CALL db.relationshipTypes()` 组合

### 查询生成不准确
- **症状**: 生成的 Cypher 执行报错或返回空结果
- **改进**:
 1. 手动刷新 Schema 缓存：`强制刷新 schema`
 2. 提供更具体的实体名称（如使用确切的标签名而非描述）
 3. 使用 `EXPLAIN` 模式先查看生成的查询不执行

### 性能问题
- **症状**: 查询超时或返回结果极慢
- **优化**:
 1. 添加更具体的标签过滤
 2. 减少路径深度（从 `*1..5` 改为 `*1..3`）
 3. 使用 `PROFILE` 分析查询计划，建议创建缺失索引

---

## 版本历史

- **v1.0.0** (2024-01-15): 初始版本，支持 Schema 感知、智能查询生成、安全审查和结果格式化

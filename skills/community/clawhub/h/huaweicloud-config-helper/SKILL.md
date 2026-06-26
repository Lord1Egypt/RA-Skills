---
name: huaweicloud-config-helper
description: 华为云Config配置审计服务的专业助手,提供全局资源查询、资源配置查询、资源Schema查询、SQL条件查询以及合规规则查询能力。当用户需要查询华为云资源、进行资源审计、检查配置合规性、盘点云上资产、分析资源关系、查询特定资源状态、验证资源配置、或需要通过SQL进行复杂资源查询时,必须使用此技能。即使未明确提及"Config"或"配置审计",只要涉及华为云资源查询、资源管理、合规检查等场景,都应触发此技能。
---

# Config 配置审计服务助手

使用scripts中的脚本，通过Config服务，查询云上资源情况、资源配置、资源schema、云服务的预置合规规则。具体有如下能力：

- 查询资源概览；
- 查询资源Schema；
- 按条件通过SQL查询资源；
- 资源合规性分析：包含但不限于从以下维度分析资源配置，'为事件响应做好准备', '优化成本', '身份管理', '保护数据完整性', '保护配置', '加密传输中的数据', '加密静态数据', '建立日志记录和监控', '强制执行最低权限', '提高可用性', '提高韧性', '管理机密', '管理漏洞', '管理规格', '限制网络访问', '资源管理'；

## 前置条件

### 环境变量配置

在使用此技能前,需要确保以下环境变量已正确配置。这些是访问华为云Config服务的必要凭证。

**必需的环境变量:**

- `HUAWEICLOUD_AK` - 访问密钥(Access Key)
- `HUAWEICLOUD_SK` - 秘密密钥(Secret Access Key)

**重要提示:**

- 这些环境变量包含敏感信息,检查配置时严禁在控制台打印
- 用户配置的AK仅需要`Config ReadOnlyAccess`的权限，用户无需过度授权

**配置步骤:**

1. **Windows PowerShell 配置:**
   ```powershell
   $env:HUAWEICLOUD_AK="your_access_key"
   $env:HUAWEICLOUD_SK="your_secret_key"
   ```

2. **或通过系统环境变量配置:**
    - Windows: 在"系统属性" > "环境变量"中设置
    - Linux/Mac: 在 `~/.bashrc` 或 `~/.zshrc` 中添加 `export` 命令

3. **验证配置:**
   ```powershell
   # 验证但不打印敏感信息
   if (-not $env:HUAWEICLOUD_AK) { Write-Error "HUAWEICLOUD_AK 未配置" }
   ```

### 依赖安装

确保已安装以下Python依赖:

```bash
pip install huaweicloudsdkconfig huaweicloudsdkcore
```

## 工作流程

### 资源查询

#### 1. 查询资源概览

获取华为云上所有资源的汇总统计信息。

**命令:**

```shell
python scripts/query_Config_resource_summary.py
```

**参数说明:**

- `--provider`: 可选，表示只查询某个云服务的资源概览, 示例:
    - `obs`
    - `vpc`
  
- `--region_id`: 可选，表示只查询某个区域的资源概览, 示例:
    - `cn-north-4`: 北京四
    - `cn-east-3`: 上海一
    - `global`: 全局
  

**输出格式:**

- JSON格式,包含各区域、各服务类型的资源数量统计
- 示例:
```json
[
  {
    "provider": "vpc",
    "type": "vpcs",
    "region_id": "cn-north-1",
    "cnt": 5
  },
  {
    "provider": "kms",
    "type": "keys",
    "region_id": "cn-north-4",
    "cnt": 2
  },
  {
    "provider": "iam",
    "type": "users",
    "region_id": "global",
    "cnt": 5
  }
]
```

**使用场景:**

- 快速了解云上资源分布
- 识别资源密集的区域和服务
- 为资源审计、成本优化、安全配置等场景提供基础数据

#### 2. 查询资源Schema

获取指定资源类型的详细结构定义,包括所有可用字段及其类型。

**命令:**

```shell
python scripts/query_Config_resource_schema.py --resource_type=obs.buckets
```

**参数说明:**

- `--resource_type`: 资源类型标识符,格式为 `provider.type`, 示例:
    - `obs.buckets`: 对象存储桶、OBS桶；
    - `ecs.cloudservers`: 云服务器、虚机、ECS；
    - `iam.users`: IAM用户；
    - `vpc.securityGroups `: VPC安全组；
    - `fgs.functions`: 函数工作流、函数、FunctionGraph；

**输出格式:**

- JSON格式,包含资源的完整Schema定义
- 包含字段名称、类型、描述等信息

**使用场景:**

- 了解资源结构和可用字段
- 编写SQL查询前确定查询字段
- 理解资源的配置属性

#### 3. 按条件查询资源(高级SQL查询)

通过SQL语句进行复杂的资源查询,支持多条件筛选、聚合分析等。

**支持的查询字段:**

- 基础字段: `id`, `name`, `provider`, `type`, `region_id`, `project_id`, `created`, `updated`, `tag`
- 扩展字段: `properties` (JSON对象,包含具体资源配置,每种资源类型的结构与资源schema保持一致)

**SQL语法特点:**

- 只能查询 `resources` 表
- 支持标准SQL语法: SELECT, WHERE, GROUP BY, ORDER BY
- 支持数组操作: `transform`, `filter`, `any_match`, `contains`
- 支持日期函数: `date_diff`, `date_parse`
-

**重要提示:**

- 使用前请先查询资源Schema了解可用字段
- 参考 `scripts/sql-example.json` 查看丰富的查询示例
- SQL语句需要用双引号包裹,内部字符串使用单引号
- 如果没有查询到资源，查询资源概览已确认云上资源分布

**示例1: 查询特定区域的所有资源**

首先确定查询需求,生成SQL语句:

```sql
select id, name, provider, type, region_id, properties
from resources
where region_id = 'cn-north-4'
```

执行查询:

```shell
python scripts/query_Config_resource_by_sql.py --sql="select id, name, provider, type, properties from resources where region_id = 'cn-north-4'"
```

**示例2: 查询IAM用户的密码强度**

步骤1: 查询iam.users的Schema了解可用字段

```shell
python scripts/query_Config_resource_schema.py --resource_type=iam.users
```

步骤2: 基于Schema发现密码相关字段为 `pwd_status` 和 `pwd_strength`

步骤3: 编写SQL查询

```sql
select id, name, provider, type, properties.pwd_status, properties.pwd_strength
from resources
where provider = 'iam'
  and type = 'users'
```

步骤4: 执行查询

```shell
python scripts/query_Config_resource_by_sql.py --sql="select id, name, provider, type, properties.pwd_status, properties.pwd_strength from resources where provider = 'iam' and type = 'users'"
```

**更多SQL示例:**

- 查询运行中的ECS: `SELECT * FROM resources WHERE provider='ecs' AND type='cloudservers' AND properties.status='ACTIVE'`
- 查询未加密的EVS: `SELECT * FROM resources WHERE provider='evs' AND type='volumes' AND NOT properties.encrypted`
- 按区域统计资源数: `SELECT region_id, count(*) FROM resources GROUP BY region_id`
- 更多案例: 请学习 `scripts/sql-example.json` 中的案例

**输出格式:**

- JSON数组,每条记录代表一个匹配的资源
- 包含查询中指定的所有字段

### 合规规则查询

#### 查询云服务的预置合规规则

获取华为云Config服务的预置合规规则列表,用于资源合规性检查。

**命令:**

查询特定云服务的合规规则:

```shell
python scripts/query_Config_builtin_rule.py --keyword=obs
```

查询所有合规规则(限制返回数量):

```shell
python scripts/query_Config_builtin_rule.py --limit=10
```

**参数说明:**

- `--keyword`: 过滤关键字,匹配规则名称或描述中包含该关键字的规则
- `--limit`: 限制返回结果数量,默认为10

**输出格式:**

- JSON数组,每个元素包含规则ID、名称、描述等信息
- 示例:
  ```json
  {
    "name": "obs-bucket-https-only",
    "display_name": "OBS桶必须使用HTTPS",
    "description": "检查OBS桶是否强制使用HTTPS协议访问"
  }
  ```

**使用场景:**

- 了解可用的合规规则
- 选择合适的规则进行合规性检查
- 制定资源合规策略

## 华为云场景知识

以下为华为云云服务的场景化知识，在分析资源的安全配置时，需要考虑以下信息：

**VPC默认安全组**

VPC默认安全组（名称为default）为系统内置资源，不可删除。为提升安全性，将所有出方向、入方向的安全组规则停用或改为Deny的操作权限。

**AK/SK安全配置**:

华为云的Access Key（AK）为20位随机字符串（例如HPUAAJJAC9GJZDIQCTHN），Secret Key（SK）为40位随机字符串。在资源配置中，仅允许在iam.users字段中包含AK信息，严禁在任何资源配置中明文存储或传递SK。若检测到SK存在于配置中，则判定为敏感信息泄露风险，需立即整改。

**云服务中英文对接关系**

| provider | type     | 中文名         | 服务功能                    |
|:---------|:---------|:------------|:------------------------|
| cts      | trackers | 云审计服务追踪器    | 提供对各种云资源操作记录的收集、存储和查询功能 |
| config   | trackers | 配置审计服务资源记录器 | 提供资源配置的持续的审计能力          |

## 最佳实践

### SQL查询优化

1. **使用WHERE条件限制查询范围**
    - 总是添加 `region_id` 或其他过滤条件,避免全表扫描
    - 示例: `WHERE region_id = 'cn-north-4'`

2. **只查询需要的字段**
    - 避免使用 `SELECT *`,明确指定需要的字段
    - 减少数据传输量,提高查询效率

3. **合理使用聚合函数**
    - 对于统计需求,使用 `count()`, `sum()` 等聚合函数
    - 示例: `SELECT region_id, count(*) FROM resources GROUP BY region_id`

### 安全注意事项

1. **保护敏感信息**
    - 严禁在日志、控制台输出AK/SK等敏感信息
    - 使用环境变量存储凭证,不要硬编码在脚本中
    - 定期轮换AK/SK
    - 仅需`Config ReadOnlyAccess`的权限，用户无需过度授权

2. **最小权限原则**
    - 为Config服务配置最小必要权限
    - 定期审查API访问权限

3. **网络安全**
    - 确保代理配置正确,通过安全通道访问华为云
    - 在生产环境中使用HTTPS

### 性能优化建议

1**批量查询优于单个查询**

- 对于多个资源,使用SQL批量查询而非多次API调用
- 利用SQL的JOIN和子查询功能

2**合理安排查询时间**

- 避免在业务高峰期执行大规模资源查询
- 考虑在非工作时间执行资源审计

### 数据处理建议

1. **结果验证**
    - 检查查询结果的完整性
    - 验证关键字段的合理性

2. **数据格式化**
    - 将JSON结果转换为易读格式(如表格)
    - 对于大量数据,考虑导出到文件

3. **异常处理**
    - 注意处理查询失败的情况
    - 检查API返回的错误信息

## 常见问题(FAQ)

### Q1: 提示"认证失败"怎么办?

**A:** 检查以下几点:

- 确认 `HUAWEICLOUD_AK` 和 `HUAWEICLOUD_SK` 环境变量已正确配置
- 验证AK/SK是否有效且未过期
- 确认账号有访问Config服务的权限
- 检查网络连接和代理配置

### Q2: SQL查询返回空结果?

**A:** 可能的原因:

- 查询条件过于严格,尝试放宽条件
- 检查资源类型名称是否正确(区分大小写)
- 确认指定区域确实有资源
- 先查询资源概览,了解资源分布

### Q3: 如何查询特定时间范围内创建的资源?

**A:** 使用日期函数:

```sql
SELECT *
FROM resources
WHERE created >= '2024-01-01T00:00:00Z'
  AND created <= '2024-12-31T23:59:59Z'
```

### Q4: 如何查询没有标签的资源?

**A:** 使用 `cardinality` 函数:

```sql
SELECT *
FROM resources
WHERE cardinality(tag) = 0
```

### Q5: 如何处理JSON数组字段的查询?

**A:** 使用数组操作函数:

- `any_match`: 检查数组中是否存在满足条件的元素
- `transform`: 转换数组元素
- `filter`: 过滤数组元素

示例:

```sql
SELECT *
FROM resources
WHERE any_match(properties.securityGroup, x - > x.id = 'xxx')
```

### Q6: 如何获取资源关系的完整信息?

**A:** 建议步骤:

1. 先查询主资源(如ECS)的Schema
2. 识别关联字段(如 `ExtVolumesAttached`)
3. 查询关联资源(如EVS)的Schema
4. 编写JOIN查询获取完整信息

## 错误处理

### 常见错误及解决方案

| 错误信息                          | 可能原因         | 解决方案                               |
|-------------------------------|--------------|------------------------------------|
| `Authentication failed`       | AK/SK配置错误或无效 | 检查环境变量配置,验证AK/SK有效性                |
| `Resource not found`          | 资源类型不存在      | 检查资源类型名称,先查询可用资源类型                 |
| `SQL syntax error`            | SQL语句语法错误    | 检查SQL语法,参考示例文件                     |

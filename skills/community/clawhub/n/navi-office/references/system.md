# 系统管理 (system_*)

## 查询工具

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `system_queryCurrentCompany` | — | — | 当前公司信息 |
| `system_queryMyCompanies` | — | — | 我的公司列表（含当前标注） |
| `system_queryDeptList` | — | `deptName`(模糊) `page` `limit` | 部门列表；获取deptId用于hr_* |
| `system_queryDeptTree` | — | — | 完整树形组织架构 |
| `system_queryMyPermissions` | — | — | 当前用户权限标识列表 |

## 切换公司

`system_switchCompany(companyId)`

**必填**：`companyId`（目标公司ID）

> 先调 `system_queryMyCompanies` 获取可切换的公司列表及 `companyId`

## 新增组织节点（新增部门）

`system_createDept(name, type, pid?, sort?, leaderId?)`

**必填**：`name`（名称）、`type`（类型）

**`type` 枚举**：`1` = 公司（并不是用户可切换的公司，这里只是一个分类的作用）。`2` = 部门（type=2 时 pid 必传，填写 **type=1 节点的 `id`**）

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `pid` | 上级组织节点ID(sys_org.id) | type=2时必填 |
| `sort` | 排序值 | 默认0 |
| `leaderId` | 负责人的用户ID | — |

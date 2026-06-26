# 目录索引

| 工具 | 分类 |
|------|------|
| [user_list](#user_list) | RBAC Users |
| [user_get](#user_get) | RBAC Users |
| [user_create](#user_create) | RBAC Users |
| [user_update](#user_update) | RBAC Users |
| [user_delete](#user_delete) | RBAC Users |
| [user_groups](#user_groups) | RBAC Users |
| [group_list](#group_list) | RBAC Groups |
| [group_get](#group_get) | RBAC Groups |
| [role_list](#role_list) | RBAC Roles |
| [role_get](#role_get) | RBAC Roles |
| [role_create](#role_create) | RBAC Roles |
| [role_update](#role_update) | RBAC Roles |
| [role_delete](#role_delete) | RBAC Roles |
| [permit_list](#permit_list) | RBAC Permissions |
| [permission_list](#permission_list) | RBAC Permissions |
| [permission_assign](#permission_assign) | RBAC Permissions |
| [permission_revoke](#permission_revoke) | RBAC Permissions |
| [tag_list](#tag_list) | RBAC Tags |
| [tag_create](#tag_create) | RBAC Tags |
| [tag_delete](#tag_delete) | RBAC Tags |
| [tag_assign](#tag_assign) | RBAC Tags |
| [tag_unassign](#tag_unassign) | RBAC Tags |
| [tag_list_resources](#tag_list_resources) | RBAC Tags |
| [filter_list](#filter_list) | RBAC Filters |

---

## RBAC Users

### user_list
列出用户

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `search` | string | 否 | 搜索条件（可选） |

---

### user_get
获取用户详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 用户名称或 ID |

---

### user_create
创建用户

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `username` | string | **是** | 用户名 |
| `email` | string | 否 | 邮箱 |
| `first_name` | string | 否 | 名 |
| `last_name` | string | 否 | 姓 |

---

### user_update
更新用户

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 用户名称或 ID |
| `email` | string | 否 | 新邮箱 |
| `first_name` | string | 否 | 新名 |
| `last_name` | string | 否 | 新姓 |

---

### user_delete
删除用户

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 用户名称或 ID |

---

### user_groups
列出用户所属的组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 用户名称或 ID |

---

## RBAC Groups

### group_list
列出用户组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `search` | string | 否 | 搜索条件（可选） |

---

### group_get
获取用户组详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 组名称或 ID |

---

## RBAC Roles

### role_list
列出角色

**参数：**（无参数）

---

### role_get
获取角色详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 角色名称或 ID |

---

### role_create
创建角色

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 角色名称 |
| `description` | string | 否 | 描述（可选） |
| `administrative` | boolean | 否 | 是否为管理员角色，默认 false |
| `permit_ids` | string[] | 否 | 权限 ID 列表 |

---

### role_update
更新角色

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 角色名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |

---

### role_delete
删除角色

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 角色名称或 ID |

---

## RBAC Permissions

### permit_list
列出所有权限单元

**参数：**（无参数）

---

### permission_list
列出资源的权限

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型（vm/host/cluster/datacenter/network/storagedomain/template） |
| `resource_id` | string | **是** | 资源 ID 或名称 |

---

### permission_assign
分配权限

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型（vm/host/cluster/datacenter/network/storagedomain/template） |
| `resource_id` | string | **是** | 资源 ID 或名称 |
| `user_or_group` | string | **是** | 主体类型（user 或 group） |
| `role_name` | string | **是** | 角色名称或 ID |
| `principal_name` | string | **是** | 用户名或组名 |

---

### permission_revoke
撤销权限

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型 |
| `resource_id` | string | **是** | 资源 ID 或名称 |
| `permission_id` | string | **是** | 权限 ID |

---

## RBAC Tags

### tag_list
列出所有标签

**参数：**（无参数）

---

### tag_create
创建标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 标签名称 |
| `description` | string | 否 | 描述（可选） |
| `parent_name` | string | 否 | 父标签名称（可选） |

---

### tag_delete
删除标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 标签名称或 ID |

---

### tag_assign
为资源分配标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型（vm/host/cluster/datacenter/network/storagedomain/template） |
| `resource_id` | string | **是** | 资源 ID 或名称 |
| `tag_name` | string | **是** | 标签名称或 ID |

---

### tag_unassign
移除资源的标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型 |
| `resource_id` | string | **是** | 资源 ID 或名称 |
| `tag_name` | string | **是** | 标签名称或 ID |

---

### tag_list_resources
列出资源的标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `resource_type` | string | **是** | 资源类型 |
| `resource_id` | string | **是** | 资源 ID 或名称 |

---

## RBAC Filters

### filter_list
列出权限过滤器

**参数：**（无参数）


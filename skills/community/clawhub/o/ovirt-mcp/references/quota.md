# 目录索引

| 工具 | 分类 |
|------|------|
| [quota_list](#quota_list) | Quota |
| [quota_get](#quota_get) | Quota |
| [quota_create](#quota_create) | Quota |
| [quota_update](#quota_update) | Quota |
| [quota_delete](#quota_delete) | Quota |
| [quota_cluster_limit_list](#quota_cluster_limit_list) | Quota |
| [quota_storage_limit_list](#quota_storage_limit_list) | Quota |

---

## Quota

### quota_list
列出数据中心的配额

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |

---

### quota_get
获取配额详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |
| `name_or_id` | string | **是** | 配额名称或 ID |

---

### quota_create
创建配额

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 配额名称 |
| `datacenter` | string | **是** | 数据中心名称 |
| `description` | string | 否 | 描述 |
| `cluster_hard_limit_pct` | number | 否 | 集群硬限制百分比 |
| `storage_hard_limit_pct` | number | 否 | 存储硬限制百分比 |

---

### quota_update
更新配额

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |
| `name_or_id` | string | **是** | 配额名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `cluster_hard_limit_pct` | number | 否 | 集群硬限制百分比 |
| `storage_hard_limit_pct` | number | 否 | 存储硬限制百分比 |

---

### quota_delete
删除配额

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |
| `name_or_id` | string | **是** | 配额名称或 ID |

---

### quota_cluster_limit_list
列出配额的集群限制

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |
| `name_or_id` | string | **是** | 配额名称或 ID |

---

### quota_storage_limit_list
列出配额的存储限制

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | **是** | 数据中心名称或 ID |
| `name_or_id` | string | **是** | 配额名称或 ID |


# 目录索引

| 工具 | 分类 |
|------|------|
| [datacenter_list](#datacenter_list) | Data Centers |
| [datacenter_get](#datacenter_get) | Data Centers |
| [datacenter_create](#datacenter_create) | Data Centers |
| [datacenter_update](#datacenter_update) | Data Centers |
| [datacenter_delete](#datacenter_delete) | Data Centers |

---

## Data Centers

### datacenter_list
列出数据中心

**参数：**（无参数）

---

### datacenter_get
获取数据中心详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 数据中心名称或 ID |

---

### datacenter_create
创建数据中心

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 数据中心名称 |
| `storage_type` | string | 否 | 存储类型（nfs/fc/iscsi等），默认 nfs |
| `description` | string | 否 | 描述 |

---

### datacenter_update
更新数据中心

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 数据中心名称或 ID |
| `new_name` | string | 否 | 新名称（可选） |
| `description` | string | 否 | 新描述（可选） |

---

### datacenter_delete
删除数据中心

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 数据中心名称或 ID |

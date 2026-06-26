# 目录索引

| 工具 | 分类 |
|------|------|
| [affinity_group_list](#affinity_group_list) | Affinity Groups |
| [affinity_group_get](#affinity_group_get) | Affinity Groups |
| [affinity_group_create](#affinity_group_create) | Affinity Groups |
| [affinity_group_update](#affinity_group_update) | Affinity Groups |
| [affinity_group_delete](#affinity_group_delete) | Affinity Groups |
| [affinity_group_add_vm](#affinity_group_add_vm) | Affinity Groups |
| [affinity_group_remove_vm](#affinity_group_remove_vm) | Affinity Groups |
| [affinity_label_list](#affinity_label_list) | Affinity Labels |
| [affinity_label_get](#affinity_label_get) | Affinity Labels |
| [affinity_label_create](#affinity_label_create) | Affinity Labels |
| [affinity_label_delete](#affinity_label_delete) | Affinity Labels |
| [affinity_label_assign](#affinity_label_assign) | Affinity Labels |
| [affinity_label_unassign](#affinity_label_unassign) | Affinity Labels |

---

## Affinity Groups

### affinity_group_list
列出亲和性组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |

---

### affinity_group_get
获取亲和性组详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |
| `name_or_id` | string | **是** | 亲和性组名称或 ID |

---

### affinity_group_create
创建亲和性组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 亲和性组名称 |
| `cluster` | string | **是** | 集群名称 |
| `positive` | boolean | 否 | True=亲和性，False=反亲和性，默认 True |
| `enforcing` | boolean | 否 | True=强制执行，False=软性规则，默认 False |
| `vms` | string[] | 否 | VM 名称或 ID 列表 |

---

### affinity_group_update
更新亲和性组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |
| `name_or_id` | string | **是** | 亲和性组名称或 ID |
| `new_name` | string | 否 | 新名称（可选） |
| `positive` | boolean | 否 | True=亲和性，False=反亲和性 |
| `enforcing` | boolean | 否 | True=强制执行，False=软性规则 |

---

### affinity_group_delete
删除亲和性组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |
| `name_or_id` | string | **是** | 亲和性组名称或 ID |

---

### affinity_group_add_vm
添加 VM 到亲和性组

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |
| `affinity_group` | string | **是** | 亲和性组名称或 ID |
| `vm` | string | **是** | VM 名称或 ID |

---

### affinity_group_remove_vm
从亲和性组移除 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称 |
| `affinity_group` | string | **是** | 亲和性组名称或 ID |
| `vm` | string | **是** | VM 名称或 ID |

---

## Affinity Labels

### affinity_label_list
列出亲和性标签

**参数：**（无参数）

---

### affinity_label_get
获取亲和性标签详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 标签名称或 ID |

---

### affinity_label_create
创建亲和性标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 标签名称 |

---

### affinity_label_delete
删除亲和性标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 标签名称或 ID |

---

### affinity_label_assign
为资源分配亲和性标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `label` | string | **是** | 标签名称或 ID |
| `resource_type` | string | **是** | 资源类型（vm 或 host） |
| `resource` | string | **是** | 资源名称或 ID |

---

### affinity_label_unassign
移除资源的亲和性标签

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `label` | string | **是** | 标签名称或 ID |
| `resource_type` | string | **是** | 资源类型（vm 或 host） |
| `resource` | string | **是** | 资源名称或 ID |


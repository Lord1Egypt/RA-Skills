# 目录索引

| 工具 | 分类 |
|------|------|
| [disk_list](#disk_list) | Disks Core |
| [disk_create](#disk_create) | Disks Core |
| [disk_attach](#disk_attach) | Disks Core |
| [disk_get](#disk_get) | Disks Extended |
| [disk_delete](#disk_delete) | Disks Extended |
| [disk_resize](#disk_resize) | Disks Extended |
| [disk_detach](#disk_detach) | Disks Extended |
| [disk_move](#disk_move) | Disks Extended |
| [disk_stats](#disk_stats) | Disks Extended |
| [disk_update](#disk_update) | Disks Extended |
| [disk_sparsify](#disk_sparsify) | Disks Extended |
| [disk_export](#disk_export) | Disks Extended |
| [disk_snapshot_list](#disk_snapshot_list) | Disks Extended |

---

## Disks Core

### disk_list
列出磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | 否 | VM 名称或 ID（可选） |
| `storage_domain` | string | 否 | 存储域名称（可选） |

---

### disk_create
创建磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 磁盘名称 |
| `size_gb` | number | **是** | 磁盘大小（GB） |
| `storage_domain` | string | 否 | 存储域名称 |
| `format` | string | 否 | 磁盘格式（cow/raw），默认 cow |

---

### disk_attach
附加磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `disk_id` | string | **是** | 磁盘 ID |

---

## Disks Extended

### disk_get
获取磁盘详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |

---

### disk_delete
删除磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `force` | boolean | 否 | 强制删除，默认 false |

---

### disk_resize
调整磁盘大小

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `new_size_gb` | number | **是** | 新大小（GB） |

---

### disk_detach
从虚拟机分离磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `vm_name_or_id` | string | **是** | VM 名称或 ID |

---

### disk_move
移动磁盘到另一个存储域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `target_storage_domain` | string | **是** | 目标存储域名称 |

---

### disk_stats
获取磁盘统计信息

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |

---

### disk_update
更新磁盘配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `shareable` | boolean | 否 | 是否可共享 |
| `wipe_after_delete` | boolean | 否 | 删除后擦除 |

---

### disk_sparsify
精简磁盘（消除空白块）

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |

---

### disk_export
导出磁盘到导出域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 磁盘名称或 ID |
| `export_domain` | string | **是** | 导出域名称 |

---

### disk_snapshot_list
列出磁盘快照

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `disk_name_or_id` | string | **是** | 磁盘名称或 ID |


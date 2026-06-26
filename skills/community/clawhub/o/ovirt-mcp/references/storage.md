# 目录索引

| 工具 | 分类 |
|------|------|
| [storage_list](#storage_list) | Storage Core |
| [storage_attach](#storage_attach) | Storage Core |
| [storage_get](#storage_get) | Storage Extended |
| [storage_create](#storage_create) | Storage Extended |
| [storage_delete](#storage_delete) | Storage Extended |
| [storage_detach](#storage_detach) | Storage Extended |
| [storage_attach_to_dc](#storage_attach_to_dc) | Storage Extended |
| [storage_stats](#storage_stats) | Storage Extended |
| [storage_refresh](#storage_refresh) | Storage Extended |
| [storage_update](#storage_update) | Storage Extended |
| [storage_files](#storage_files) | Storage Extended |
| [storage_connections_list](#storage_connections_list) | Storage Extended |
| [storage_available_disks](#storage_available_disks) | Storage Extended |
| [storage_export_vms](#storage_export_vms) | Storage Extended |
| [storage_import_vm](#storage_import_vm) | Storage Extended |
| [iscsi_bond_list](#iscsi_bond_list) | Storage Extended |

---

## Storage Core

### storage_list
列出存储域

**参数：**（无参数）

---

### storage_attach
挂载存储

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `storage_name` | string | **是** | 存储域名称 |
| `dc_name` | string | **是** | 数据中心名称 |

---

## Storage Extended

### storage_get
获取存储域详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |

---

### storage_create
创建存储域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 存储域名称 |
| `storage_type` | string | **是** | 存储类型（nfs/fc/iscsi等） |
| `host` | string | **是** | 主机名称 |
| `path` | string | **是** | 存储路径 |
| `datacenter` | string | 否 | 数据中心名称（可选） |
| `description` | string | 否 | 描述 |
| `domain_type` | string | 否 | 域类型（data/iso/export），默认 data |

---

### storage_delete
删除存储域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |
| `force` | boolean | 否 | 强制删除，默认 false |

---

### storage_detach
分离存储域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |
| `datacenter` | string | 否 | 数据中心名称（可选） |

---

### storage_attach_to_dc
附加存储域到数据中心

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |
| `datacenter` | string | **是** | 数据中心名称 |

---

### storage_stats
获取存储域统计信息

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |

---

### storage_refresh
刷新存储域

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |

---

### storage_update
更新存储域配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `warning_low_space` | number | 否 | 低空间警告阈值（GB） |
| `critical_low_space` | number | 否 | 临界空间阈值（GB） |

---

### storage_files
列出存储域的文件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |

---

### storage_connections_list
列出存储连接

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | 否 | 存储域名称或 ID（可选） |

---

### storage_available_disks
列出存储域上的可用磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 存储域名称或 ID |

---

### storage_export_vms
列出导出域上的 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 导出域名称或 ID |

---

### storage_import_vm
从导出域导入 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 导出域名称或 ID |
| `vm_name` | string | **是** | 要导入的 VM 名称 |
| `cluster` | string | **是** | 目标集群 |
| `storage_domain` | string | 否 | 目标存储域（可选） |
| `clone` | boolean | 否 | 是否克隆 |

---

### iscsi_bond_list
列出 iSCSI Bond

**参数：**（无参数）


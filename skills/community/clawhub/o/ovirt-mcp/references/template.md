# 目录索引

| 工具 | 分类 |
|------|------|
| [template_disk_list](#template_disk_list) | Templates |
| [template_nic_list](#template_nic_list) | Templates |
| [template_list](#template_list) | Templates |
| [template_vm_create](#template_vm_create) | Templates |
| [template_get](#template_get) | Templates |
| [template_create](#template_create) | Templates |
| [template_delete](#template_delete) | Templates |
| [template_update](#template_update) | Templates |

---

## Templates

### template_disk_list
列出模板的磁盘

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 模板名称或 ID |

---

### template_nic_list
列出模板的网卡

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 模板名称或 ID |

---

### template_list
列出模板

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | 否 | 集群名称（可选） |

---

### template_vm_create
从模板创建 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | VM 名称 |
| `template` | string | **是** | 模板名称 |
| `cluster` | string | **是** | 目标集群 |
| `memory_mb` | number | 否 | 内存（MB），可选 |
| `cpu_cores` | number | 否 | CPU 核数，可选 |

---

### template_get
获取模板详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 模板名称或 ID |

---

### template_create
从虚拟机创建模板

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 模板名称 |
| `vm` | string | **是** | 源虚拟机名称或 ID |
| `description` | string | 否 | 描述 |
| `cluster` | string | 否 | 目标集群（可选） |

---

### template_delete
删除模板

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 模板名称或 ID |
| `force` | boolean | 否 | 强制删除 |

---

### template_update
更新模板

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 模板名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `memory_mb` | number | 否 | 内存（MB） |
| `cpu_cores` | number | 否 | CPU 核数 |


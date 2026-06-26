# 目录索引

| 工具 | 分类 |
|------|------|
| [cluster_list](#cluster_list) | Clusters |
| [cluster_get](#cluster_get) | Clusters |
| [cluster_create](#cluster_create) | Clusters |
| [cluster_update](#cluster_update) | Clusters |
| [cluster_delete](#cluster_delete) | Clusters |
| [cluster_hosts](#cluster_hosts) | Clusters |
| [cluster_vms](#cluster_vms) | Clusters |
| [cluster_cpu_load](#cluster_cpu_load) | Clusters |
| [cluster_memory_usage](#cluster_memory_usage) | Clusters |
| [cpu_profile_list](#cpu_profile_list) | CPU Profiles |
| [cpu_profile_get](#cpu_profile_get) | CPU Profiles |

---

## Clusters

### cluster_list
列出集群

**参数：**（无参数）

---

### cluster_get
获取集群详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |

---

### cluster_create
创建集群

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |
| `datacenter` | string | **是** | 数据中心名称 |
| `cpu_type` | string | **是** | CPU 类型 |
| `description` | string | 否 | 描述 |
| `gluster_service` | boolean | 否 | 是否启用 Gluster 服务 |
| `threads_per_core` | number | 否 | 每核心线程数 |

---

### cluster_update
更新集群

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 集群名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `threads_per_core` | number | 否 | 每核心线程数 |

---

### cluster_delete
删除集群

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 集群名称或 ID |

---

### cluster_hosts
集群主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |

---

### cluster_vms
集群 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |
| `status` | string | 否 | VM 状态过滤（可选） |

---

### cluster_cpu_load
集群 CPU 负载

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |

---

### cluster_memory_usage
集群内存使用

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 集群名称 |

---

## CPU Profiles

### cpu_profile_list
列出 CPU Profile

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称或 ID |

---

### cpu_profile_get
获取 CPU Profile 详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | **是** | 集群名称或 ID |
| `name_or_id` | string | **是** | Profile 名称或 ID |




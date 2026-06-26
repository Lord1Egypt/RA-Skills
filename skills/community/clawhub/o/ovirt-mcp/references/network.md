# 目录索引

| 工具 | 分类 |
|------|------|
| [network_list](#network_list) | Networks |
| [network_get](#network_get) | Networks |
| [network_create](#network_create) | Networks |
| [network_update](#network_update) | Networks |
| [network_delete](#network_delete) | Networks |
| [nic_list](#nic_list) | Networks |
| [nic_add](#nic_add) | Networks |
| [nic_remove](#nic_remove) | Networks |
| [vnic_profile_list](#vnic_profile_list) | VNIC Profiles |
| [vnic_profile_get](#vnic_profile_get) | VNIC Profiles |
| [vnic_profile_create](#vnic_profile_create) | VNIC Profiles |
| [vnic_profile_update](#vnic_profile_update) | VNIC Profiles |
| [vnic_profile_delete](#vnic_profile_delete) | VNIC Profiles |
| [network_filter_list](#network_filter_list) | Network Filters & QoS |
| [mac_pool_list](#mac_pool_list) | Network Filters & QoS |
| [qos_list](#qos_list) | Network Filters & QoS |

---

## Networks

### network_list
列出网络

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | 否 | 集群名称（可选） |

---

### network_get
获取网络详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 网络名称或 ID |

---

### network_create
创建网络

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 网络名称 |
| `cluster` | string | 否 | 集群名称（可选） |
| `datacenter` | string | 否 | 数据中心名称（可选） |
| `description` | string | 否 | 描述 |
| `mtu` | number | 否 | MTU 值 |

---

### network_update
更新网络

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 网络名称 |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |

---

### network_delete
删除网络

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 网络名称或 ID |

---

### nic_list
列出网卡

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### nic_add
添加网卡

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `nic_name` | string | **是** | 网卡名称 |
| `network` | string | **是** | 网络名称 |

---

### nic_remove
移除网卡

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `nic_name` | string | **是** | 网卡名称 |

---

## VNIC Profiles

### vnic_profile_list
列出 VNIC Profile

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `network` | string | 否 | 网络名称（可选） |

---

### vnic_profile_get
获取 VNIC Profile 详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | Profile 名称或 ID |

---

### vnic_profile_create
创建 VNIC Profile

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | Profile 名称 |
| `network` | string | **是** | 网络名称 |
| `description` | string | 否 | 描述 |
| `port_mirroring` | boolean | 否 | 是否启用端口镜像 |

---

### vnic_profile_update
更新 VNIC Profile

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | Profile 名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |
| `port_mirroring` | boolean | 否 | 端口镜像设置 |

---

### vnic_profile_delete
删除 VNIC Profile

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | Profile 名称或 ID |

---

## Network Filters & QoS

### network_filter_list
列出网络过滤器

**参数：**（无参数）

---

### mac_pool_list
列出 MAC 地址池

**参数：**（无参数）

---

### qos_list
列出 QoS 配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `datacenter` | string | 否 | 数据中心名称（可选） |


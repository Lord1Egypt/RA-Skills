# 目录索引

| 工具 | 分类 |
|------|------|
| [host_list](#host_list) | Hosts Core |
| [host_activate](#host_activate) | Hosts Core |
| [host_deactivate](#host_deactivate) | Hosts Core |
| [host_get](#host_get) | Hosts Extended |
| [host_add](#host_add) | Hosts Extended |
| [host_remove](#host_remove) | Hosts Extended |
| [host_stats](#host_stats) | Hosts Extended |
| [host_devices](#host_devices) | Hosts Extended |
| [host_nic_list](#host_nic_list) | Hosts Extended |
| [host_nic_update](#host_nic_update) | Hosts Extended |
| [host_numa_get](#host_numa_get) | Hosts Extended |
| [host_hook_list](#host_hook_list) | Hosts Extended |
| [host_fence](#host_fence) | Hosts Extended |
| [host_network_update](#host_network_update) | Hosts Extended |
| [host_device_update](#host_device_update) | Hosts Extended |
| [host_storage_list](#host_storage_list) | Hosts Extended |
| [host_install](#host_install) | Hosts Extended |
| [host_iscsi_discover](#host_iscsi_discover) | Hosts Extended |
| [host_iscsi_login](#host_iscsi_login) | Hosts Extended |

---

## Hosts Core

### host_list
列出主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | 否 | 集群名称（可选） |

---

### host_activate
激活主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_deactivate
维护主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

## Hosts Extended

### host_get
获取主机详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_add
添加主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 主机名称 |
| `cluster` | string | **是** | 集群名称 |
| `address` | string | **是** | 主机地址 |
| `password` | string | 否 | SSH 密码（可选） |
| `ssh_port` | number | 否 | SSH 端口，默认 22 |

---

### host_remove
移除主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `force` | boolean | 否 | 强制移除，默认 false |

---

### host_stats
获取主机统计信息

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_devices
获取主机设备列表

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_nic_list
列出主机网卡

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_nic_update
更新主机网卡配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `nic_name` | string | **是** | 网卡名称 |
| `custom_properties` | object | 否 | 自定义属性 |

---

### host_numa_get
获取主机 NUMA 拓扑

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_hook_list
列出主机 Hook

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_fence
对主机执行 Fence 操作

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `action` | string | **是** | 操作类型（restart/start/stop/status） |

---

### host_network_update
更新主机网络配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `network` | string | **是** | 网络名称 |
| `nic` | string | 否 | 网卡名称（可选） |
| `vlan_id` | number | 否 | VLAN ID（可选） |
| `bond` | string | 否 | 绑定接口名称（可选） |

---

### host_device_update
更新主机设备配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `device_name` | string | **是** | 设备名称 |
| `enabled` | boolean | 否 | 是否启用 |

---

### host_storage_list
列出主机存储

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |

---

### host_install
安装/重新安装主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `root_password` | string | 否 | root 密码 |
| `ssh_key` | string | 否 | SSH 公钥 |
| `override_iptables` | boolean | 否 | 覆盖 iptables 规则 |

---

### host_iscsi_discover
发现 iSCSI 目标

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `address` | string | **是** | iSCSI 目标地址 |
| `port` | number | 否 | 端口号，默认 3260 |
| `username` | string | 否 | CHAP 用户名（可选） |
| `password` | string | 否 | CHAP 密码（可选） |

---

### host_iscsi_login
登录到 iSCSI 目标

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | 主机名称或 ID |
| `address` | string | **是** | iSCSI 目标地址 |
| `target` | string | **是** | 目标名称 |
| `port` | number | 否 | 端口号，默认 3260 |
| `username` | string | 否 | CHAP 用户名（可选） |
| `password` | string | 否 | CHAP 密码（可选） |


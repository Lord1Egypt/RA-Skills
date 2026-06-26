# 目录索引

| 工具 | 分类 |
|------|------|
| [vm_list](#vm_list) | VM Core |
| [vm_get](#vm_get) | VM Core |
| [vm_create](#vm_create) | VM Core |
| [vm_start](#vm_start) | VM Core |
| [vm_stop](#vm_stop) | VM Core |
| [vm_restart](#vm_restart) | VM Core |
| [vm_delete](#vm_delete) | VM Core |
| [vm_update_resources](#vm_update_resources) | VM Core |
| [vm_stats](#vm_stats) | VM Core |
| [vm_migrate](#vm_migrate) | VM Extended |
| [vm_console](#vm_console) | VM Extended |
| [vm_cdrom_list](#vm_cdrom_list) | VM Extended |
| [vm_cdrom_update](#vm_cdrom_update) | VM Extended |
| [vm_hostdevice_list](#vm_hostdevice_list) | VM Extended |
| [vm_hostdevice_attach](#vm_hostdevice_attach) | VM Extended |
| [vm_hostdevice_detach](#vm_hostdevice_detach) | VM Extended |
| [vm_mediated_device_list](#vm_mediated_device_list) | VM Extended |
| [vm_numa_list](#vm_numa_list) | VM Extended |
| [vm_watchdog_list](#vm_watchdog_list) | VM Extended |
| [vm_watchdog_update](#vm_watchdog_update) | VM Extended |
| [vm_pin_to_host](#vm_pin_to_host) | VM Extended |
| [vm_session_list](#vm_session_list) | VM Extended |
| [vm_pool_list](#vm_pool_list) | VM Pools |
| [vm_pool_get](#vm_pool_get) | VM Pools |
| [vm_pool_create](#vm_pool_create) | VM Pools |
| [vm_pool_delete](#vm_pool_delete) | VM Pools |
| [vm_pool_update](#vm_pool_update) | VM Pools |
| [vm_checkpoint_list](#vm_checkpoint_list) | VM Checkpoints |
| [vm_checkpoint_create](#vm_checkpoint_create) | VM Checkpoints |
| [vm_checkpoint_restore](#vm_checkpoint_restore) | VM Checkpoints |
| [vm_checkpoint_delete](#vm_checkpoint_delete) | VM Checkpoints |
| [snapshot_list](#snapshot_list) | Snapshots |
| [snapshot_create](#snapshot_create) | Snapshots |
| [snapshot_restore](#snapshot_restore) | Snapshots |
| [snapshot_delete](#snapshot_delete) | Snapshots |

---

## VM Core

### vm_list
列出虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | 否 | 集群名称（可选，用于过滤） |
| `status` | string | 否 | VM 状态过滤（up/down） |

---

### vm_get
获取虚拟机详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_create
创建虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | VM 名称 |
| `cluster` | string | **是** | 目标集群 |
| `memory_mb` | number | 否 | 内存（MB），默认 4096 |
| `cpu_cores` | number | 否 | CPU 核数，默认 2 |
| `template` | string | 否 | 模板名称，默认 Blank |
| `disk_size_gb` | number | 否 | 磁盘大小（GB），默认 50 |
| `description` | string | 否 | VM 描述 |

---

### vm_start
启动虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_stop
关闭虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `graceful` | boolean | 否 | 优雅关机，默认 true |

---

### vm_restart
重启虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_delete
删除虚拟机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `force` | boolean | 否 | 强制删除，默认 false |

---

### vm_update_resources
更新 VM 资源

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `memory_mb` | number | 否 | 新内存（MB） |
| `cpu_cores` | number | 否 | 新 CPU 核数 |

---

### vm_stats
获取 VM 统计

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

## VM Extended

### vm_migrate
迁移虚拟机到另一台主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `target_host` | string | 否 | 目标主机名称或 ID（可选） |

---

### vm_console
获取虚拟机控制台访问信息

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `console_type` | string | 否 | 控制台类型（spice/vnc），默认 spice |

---

### vm_cdrom_list
列出 VM 的 CDROM 设备

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_cdrom_update
更新 VM 的 CDROM（挂载/弹出 ISO）

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `cdrom_id` | string | **是** | CDROM ID |
| `iso_file` | string | 否 | ISO 文件路径 |
| `eject` | boolean | 否 | 是否弹出光盘 |

---

### vm_hostdevice_list
列出 VM 的主机设备

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_hostdevice_attach
将主机设备附加到 VM

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `device_name` | string | **是** | 设备名称 |

---

### vm_hostdevice_detach
从 VM 分离主机设备

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `device_name` | string | **是** | 设备名称 |

---

### vm_mediated_device_list
列出 VM 的介导设备（vGPU）

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_numa_list
列出 VM 的 NUMA 节点

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_watchdog_list
列出 VM 的 Watchdog 设备

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_watchdog_update
更新 VM 的 Watchdog 配置

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `watchdog_id` | string | **是** | Watchdog ID |
| `action` | string | 否 | 触发动作（none/reset/poweroff/shutdown/dump） |

---

### vm_pin_to_host
将 VM 固定到指定主机

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `host` | string | **是** | 主机名称或 ID |
| `pin_policy` | string | 否 | 固定策略（user/resizable/migratable） |

---

### vm_session_list
列出 VM 的活跃会话

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

## VM Pools

### vm_pool_list
列出虚拟机池

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `cluster` | string | 否 | 集群名称（可选） |

---

### vm_pool_get
获取虚拟机池详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 池名称或 ID |

---

### vm_pool_create
创建虚拟机池

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name` | string | **是** | 池名称 |
| `template` | string | **是** | 模板名称 |
| `cluster` | string | **是** | 集群名称 |
| `size` | number | 否 | 池大小，默认 5 |
| `description` | string | 否 | 描述 |
| `max_user_vms` | number | 否 | 每用户最大 VM 数，默认 1 |
| `prestarted_vms` | number | 否 | 预启动 VM 数，默认 0 |
| `stateful` | boolean | 否 | 是否有状态，默认 false |

---

### vm_pool_delete
删除虚拟机池

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 池名称或 ID |
| `force` | boolean | 否 | 强制删除 |

---

### vm_pool_update
更新虚拟机池

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 池名称或 ID |
| `new_name` | string | 否 | 新名称 |
| `size` | number | 否 | 新大小 |
| `description` | string | 否 | 新描述 |
| `prestarted_vms` | number | 否 | 预启动 VM 数 |

---

## VM Checkpoints

### vm_checkpoint_list
列出 VM 的检查点

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### vm_checkpoint_create
创建 VM 检查点

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `description` | string | 否 | 检查点描述 |

---

### vm_checkpoint_restore
恢复 VM 到检查点

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `checkpoint_id` | string | **是** | 检查点 ID |

---

### vm_checkpoint_delete
删除 VM 检查点

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `checkpoint_id` | string | **是** | 检查点 ID |

---

## Snapshots

### snapshot_list
列出快照

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |

---

### snapshot_create
创建快照

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `description` | string | 否 | 快照描述 |

---

### snapshot_restore
恢复快照

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `snapshot_id` | string | **是** | 快照 ID |

---

### snapshot_delete
删除快照

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `name_or_id` | string | **是** | VM 名称或 ID |
| `snapshot_id` | string | **是** | 快照 ID |


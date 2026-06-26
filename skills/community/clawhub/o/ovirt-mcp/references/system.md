# 目录索引

| 工具 | 分类 |
|------|------|
| [system_get](#system_get) | System & Jobs |
| [system_option_list](#system_option_list) | System & Jobs |
| [job_list](#job_list) | System & Jobs |
| [job_get](#job_get) | System & Jobs |
| [job_cancel](#job_cancel) | System & Jobs |
| [system_statistics](#system_statistics) | System & Jobs |

---

## System & Jobs

### system_get
获取系统信息

**参数：**（无参数）

---

### system_option_list
列出系统选项

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `category` | string | 否 | 选项分类（可选） |

---

### job_list
列出任务

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `page` | number | 否 | 页码 |
| `page_size` | number | 否 | 每页数量 |

---

### job_get
获取任务详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `job_id` | string | **是** | 任务 ID |

---

### job_cancel
取消任务

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `job_id` | string | **是** | 任务 ID |
| `force` | boolean | 否 | 强制取消 |

---

### system_statistics
获取系统统计信息

**参数：**（无参数）


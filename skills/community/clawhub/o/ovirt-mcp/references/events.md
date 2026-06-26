# 目录索引

| 工具 | 分类 |
|------|------|
| [event_list](#event_list) | Events |
| [event_get](#event_get) | Events |
| [event_search](#event_search) | Events |
| [event_alerts](#event_alerts) | Events |
| [event_errors](#event_errors) | Events |
| [event_warnings](#event_warnings) | Events |
| [event_summary](#event_summary) | Events |
| [event_acknowledge](#event_acknowledge) | Events |
| [event_clear_alerts](#event_clear_alerts) | Events |
| [event_subscription_list](#event_subscription_list) | Events |
| [bookmark_list](#bookmark_list) | Events |

---

## Events

### event_list
列出事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `search` | string | 否 | 搜索条件（可选） |
| `severity` | string | 否 | 严重级别过滤（error/warning/info/alert） |
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 50 |

---

### event_get
获取事件详情

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `event_id` | string | **是** | 事件 ID |

---

### event_search
搜索事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `query` | string | **是** | 搜索查询 |
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 50 |

---

### event_alerts
获取告警事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 50 |

---

### event_errors
获取错误事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 50 |

---

### event_warnings
获取警告事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `page` | number | 否 | 页码，默认 1 |
| `page_size` | number | 否 | 每页数量，默认 50 |

---

### event_summary
获取事件统计摘要

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `hours` | number | 否 | 统计最近 N 小时，默认 24 |

---

### event_acknowledge
确认事件

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `event_id` | string | **是** | 事件 ID |

---

### event_clear_alerts
清除告警事件

**参数：**（无参数）

---

### event_subscription_list
列出事件订阅

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `user` | string | 否 | 用户名称（可选） |

---

### bookmark_list
列出书签

**参数：**（无参数）


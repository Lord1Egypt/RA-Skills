# 业务视图与网络拓扑 API 详细说明

## 业务视图

### 获取组织树
**接口：** `POST /business/organization-tree`

**参数：** 无

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": [
        {
            "id": 1,
            "name": "广州",
            "parent_id": null,
            "description": "",
            "children": [
                {
                    "id": 3,
                    "name": "测试",
                    "parent_id": 1,
                    "description": ""
                }
            ]
        }
    ]
}
```

**返回字段说明：**
- `id`: 组织 ID
- `name`: 组织名称
- `parent_id`: 上级组织 ID
- `description`: 组织简介
- `children`: 子节点数组

### 获取业务树
**接口：** `POST /business/business-tree`

**参数：** 无

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": [
        {
            "id": 72,
            "name": "业务一",
            "description": "",
            "relation_id": null,
            "unique_id": "business_72",
            "node_type": "business"
        },
        {
            "id": 25,
            "name": "组织一",
            "parent_id": 1,
            "description": "",
            "unique_id": "organization_25",
            "node_type": "organization",
            "children": []
        }
    ]
}
```

**返回字段说明：**
- `id`: 业务或组织 ID
- `name`: 业务或组织名称
- `parent_id`: 上级组织 ID
- `description`: 业务或组织描述
- `node_type`: 节点类型（organization-组织, business-业务）
- `relation_id`: 关联的组织 ID
- `unique_id`: 唯一标识
- `children`: 子节点数组

### 业务列表
**接口：** `POST /business/business-list`

**说明：** 获取业务列表

**参数：**
- `organization_id` (int, 可选): 组织 ID

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": [
        {
            "id": 72,
            "name": "业务一",
            "description": "",
            "relation_id": 1
        }
    ]
}
```

**返回字段说明：**
- `id`: 业务 ID
- `name`: 业务名称
- `description`: 业务描述
- `relation_id`: 关联的组织 ID

### 业务告警列表
**接口：** `POST /business/business-alarms`

**说明：** 获取业务的告警列表

**参数：**
- `business_id` (int, 必填): 业务 ID
- `keyword` (string, 可选): 关键字
- `priority` (array, 可选): 告警级别集合，如 `[4, 5]`
- `classification` (int, 可选): 大类 ID
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 分页大小
- `is_all` (int, 可选): 是否返回全部（1-是，默认 0）

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "total": 5,
        "list": [
            {
                "id": 427,
                "eventid": 2339,
                "triggerid": 21883,
                "clock": 1641871025,
                "hostid": 10521,
                "priority": 4,
                "description": "[网络设备]华为核心交换机SNMP采集中断【测试告警】",
                "comments": "需要检查SNMP团体名是否不对应",
                "is_unrecovery": 1,
                "is_unack": 1,
                "name": "华为核心交换机",
                "host": "HUAWEI-Quidway S3928P-SI",
                "ip": "192.168.1.98"
            }
        ]
    }
}
```

### 业务主机列表
**接口：** `POST /business/business-hosts`

**说明：** 获取业务的监控主机列表

**参数：**
- `business_id` (int, 必填): 业务 ID
- `keyword` (string, 可选): 关键字（IP、名称）
- `active_status` (int, 可选): 监控状态（-1-未监控, 0-正常, 1~5-告警等级）
- `classification` (int, 可选): 大类 ID
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 分页大小
- `show_business` (int, 可选): 是否显示业务（1-是，默认 0）

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "total": 10,
        "list": [
            {
                "name": "02_113-CentOS7.4--MySQL数据库",
                "host": "02_113-CentOS7.4_Mysql5.7",
                "hostid": 10531,
                "ip": "192.168.2.113",
                "status": 1,
                "active_status": -1,
                "classification": 105,
                "classification_label": "数据库",
                "subtype": 105002,
                "subtype_label": "Mysql",
                "business_name": "业务一",
                "groups": [{"groupid": 37, "name": "mysql"}],
                "tags": [{"id": 36, "name": "all"}]
            }
        ]
    }
}
```

### 业务统计
**接口：** `POST /business/business-statistic`

**说明：** 获取业务统计数据

**参数：**
- `business_id` (int, 必填): 业务 ID

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "host_count": 4,
        "alarm_count": 0,
        "running": 1,
        "unrunning": 3,
        "alarm_1": 0,
        "alarm_2": 0,
        "alarm_3": 0,
        "alarm_4": 0,
        "alarm_5": 0
    }
}
```

**返回字段说明：**
- `host_count`: 主机总数
- `alarm_count`: 告警总数
- `running`: 运行中
- `unrunning`: 未运行
- `alarm_1` 到 `alarm_5`: 各级别告警数量

### 添加业务
**接口：** `POST /business/business-add`

**参数：**
- `name` (string, 必填): 业务名称
- `description` (string, 可选): 业务描述
- `relation_id` (int, 可选): 关联的组织 ID
- `host_ids` (array, 必填): 主机 ID 数组

### 更新业务
**接口：** `POST /business/business-update`

**参数：**
- `id` (int, 必填): 业务 ID
- `name` (string, 必填): 业务名称
- `description` (string, 可选): 业务描述
- `relation_id` (int, 可选): 关联的组织 ID
- `host_ids` (array, 必填): 主机 ID 数组

### 删除业务
**接口：** `POST /business/business-delete`

**参数：**
- `ids` (array, 必填): 业务 ID 数组

### 添加组织
**接口：** `POST /business/organization-add`

**参数：**
- `name` (string, 必填): 组织名称
- `description` (string, 可选): 组织描述
- `parent_id` (int, 可选): 上级组织 ID

### 更新组织
**接口：** `POST /business/organization-update`

**参数：**
- `id` (int, 必填): 组织 ID
- `name` (string, 必填): 组织名称
- `description` (string, 可选): 组织描述
- `parent_id` (int, 可选): 上级组织 ID

### 删除组织
**接口：** `POST /business/organization-delete`

**参数：**
- `ids` (array, 必填): 组织 ID 数组

## 链路监控

### 链路列表
**接口：** `POST /link/link-list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词（名称、IP）

### 获取链路详情
**接口：** `POST /link/link-info`

**参数：**
- `id` (int, 必填): 链路 ID

### 添加链路
**接口：** `POST /link/link-add`

**参数：**
- `source_hostid` (int, 必填): 源主机 ID
- `target_hostid` (int, 必填): 目标主机 ID
- `name` (string, 必填): 链路名称
- `description` (string, 可选): 描述

### 更新链路
**接口：** `POST /link/link-update`

**参数：**
- `id` (int, 必填): 链路 ID
- `source_hostid` (int, 必填): 源主机 ID
- `target_hostid` (int, 必填): 目标主机 ID
- `name` (string, 必填): 链路名称
- `description` (string, 可选): 描述

### 删除链路
**接口：** `POST /link/link-delete`

**参数：**
- `ids` (array, 必填): 链路 ID 数组

## 网络拓扑图

### 获取拓扑图列表
**接口：** `POST /topology/topo-list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词

### 获取拓扑图详情
**接口：** `POST /topology/topo-info`

**参数：**
- `id` (int, 必填): 拓扑图 ID

**返回字段说明：**
- `id`: 拓扑图 ID
- `name`: 拓扑图名称
- `description`: 描述
- `create_time`: 创建时间（北京时间）

### 添加拓扑图
**接口：** `POST /topology/topo-add`

**参数：**
- `name` (string, 必填): 拓扑图名称
- `description` (string, 可选): 描述

### 更新拓扑图
**接口：** `POST /topology/topo-update`

**参数：**
- `id` (int, 必填): 拓扑图 ID
- `name` (string, 必填): 拓扑图名称
- `description` (string, 可选): 描述

### 删除拓扑图
**接口：** `POST /topology/topo-delete`

**参数：**
- `ids` (array, 必填): 拓扑图 ID 数组

### 调用监控对象列表
**接口：** `POST /topology/monitor-host-list`

**参数：**
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量
- `keyword` (string, 可选): 关键词（IP、名称）

### 创建监控对象
**接口：** `POST /topology/monitor-host-create`

**参数：**
- `host` (string, 必填): 主机名称
- `ip` (string, 必填): IP 地址
- `template_id` (int, 必填): 模板 ID
- `snmp_version` (int, 可选): SNMP 版本
- `snmp_port` (int, 可选): SNMP 端口
- `snmp_community` (string, 可选): SNMP 团体名

### 添加节点到拓扑图
**接口：** `POST /topology/topo-node-add`

**参数：**
- `topo_id` (int, 必填): 拓扑图 ID
- `host_id` (int, 必填): 主机 ID
- `position_x` (int, 必填): X 坐标
- `position_y` (int, 必填): Y 坐标

### 从拓扑图移除节点
**接口：** `POST /topology/topo-node-delete`

**参数：**
- `ids` (array, 必填): 节点 ID 数组

### 添加连线到拓扑图
**接口：** `POST /topology/topo-line-add`

**参数：**
- `topo_id` (int, 必填): 拓扑图 ID
- `source_node_id` (int, 必填): 源节点 ID
- `target_node_id` (int, 必填): 目标节点 ID

### 从拓扑图移除连线
**接口：** `POST /topology/topo-line-delete`

**参数：**
- `ids` (array, 必填): 连线 ID 数组

### 获取拓扑图布局
**接口：** `POST /topology/topo-layout`

**参数：**
- `id` (int, 必填): 拓扑图 ID

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "nodes": [
            {
                "id": 1,
                "host_id": 10521,
                "position_x": 100,
                "position_y": 100,
                "host": {
                    "hostid": 10521,
                    "host": "HUAWEI-Quidway",
                    "ip": "192.168.1.98",
                    "status": 0
                }
            }
        ],
        "lines": [
            {
                "id": 1,
                "source_node_id": 1,
                "target_node_id": 2
            }
        ]
    }
}
```

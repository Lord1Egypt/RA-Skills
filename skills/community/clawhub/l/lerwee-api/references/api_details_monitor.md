# 监控中心 API 详细说明

## 监控对象管理

### 获取监控对象列表
**接口：** `POST /monitor/host-list`

**参数：**
- `keyword` (string, 可选): 关键词搜索
- `ip` (string, 可选): IP 地址
- `true_ip` (int, 可选): 精确查询IP (1-是, 0-否)
- `classification` (int, 可选): 监控类型
- `subtype` (int, 可选): 监控子类型
- `page` (int, 可选): 页码
- `pageSize` (int, 可选): 每页数量

**返回字段说明：**
- `hostid`: 对象ID
- `ip`: 对象IP
- `host`: 对象名称
- `name`: 业务名称
- `status`: 启用监控 (0-是, 1-否)
- `classification`: 监控类型数值
- `classification_label`: 监控类型标签
- `subtype`: 监控子类型数值
- `subtype_label`: 监控子类型标签
- `active_status`: 监控状态 (-1-未监控, 0-正常, 1~5-告警状态)
- `active_error`: 监控状态错误信息
- `active_label`: 监控状态标签
- `power_status`: 采集情况 (1-正常, 2-异常)
- `power_label`: 采集情况标签
- `description`: 描述
- `template_id`: 模板ID
- `tags`: 标签集合
- `groups`: 分组集合

### 创建监控对象
**接口：** `POST /monitor/host-create`

**参数：**
- `template_id` (int, 必填): 模板ID
- `host` (string, 必填): 对象名称（唯一标识且不支持中文）
- `name` (string, 必填): 业务名称（唯一）
- `status` (int, 可选): 对象状态 (0-启用, 1-禁用，默认: 0)
- `description` (string, 可选): 描述信息
- `proxy_hostid` (int, 可选): 代理ID
- `group_ids` (int[], 必填): 分组ID数组
- `tag_ids` (int[], 可选): 标签ID数组
- `agent` (object, 可选): Agent接口参数
  - `useip` (int, 必填): 是否使用IP (1-是, 0-否)
  - `ip` (string, 可选): IP地址（useip=1时必填）
  - `dns` (string, 可选): DNS（useip=0时必填）
  - `port` (int, 可选): 端口（默认: 10073，特殊: 10050）
- `snmp` (object, 可选): SNMP接口参数
  - `useip` (int, 必填): 是否使用IP (1-是, 0-否)
  - `ip` (string, 可选): IP地址（useip=1时必填）
  - `dns` (string, 可选): DNS（useip=0时必填）
  - `port` (int, 可选): 端口（默认: 161）
  - `version` (int, 必填): 版本 (1-SNMPv1, 2-SNMPv2, 3-SNMPv3)
  - `details` (array, 可选): SNMP明细参数
- `ipmi` (object, 可选): IPMI接口参数
  - `useip` (int, 必填): 是否使用IP (1-是, 0-否)
  - `ip` (string, 可选): IP地址（useip=1时必填）
  - `dns` (string, 可选): DNS（useip=0时必填）
  - `port` (int, 可选): 端口（默认: 623）
- `jmx` (object, 可选): JMX接口参数
  - `useip` (int, 必填): 是否使用IP (1-是, 0-否)
  - `ip` (string, 可选): IP地址（useip=1时必填）
  - `dns` (string, 可选): DNS（useip=0时必填）
  - `port` (int, 可选): 端口（默认: 12345）

### 更新监控对象
**接口：** `POST /monitor/host-update`

**参数：**
- `hostid` (int, 必填): 对象ID
- `template_id` (int, 可选): 模板ID
- `host` (string, 可选): 对象名称
- `name` (string, 可选): 业务名称
- `status` (int, 可选): 对象状态
- `description` (string, 可选): 描述信息
- `proxy_hostid` (int, 可选): 代理ID
- `group_ids` (int[], 可选): 分组ID数组
- `tag_ids` (int[], 可选): 标签ID数组
- `agent` (object, 可选): Agent接口参数（同创建）
- `snmp` (object, 可选): SNMP接口参数（同创建）
- `ipmi` (object, 可选): IPMI接口参数（同创建）
- `jmx` (object, 可选): JMX接口参数（同创建）

### 删除监控对象
**接口：** `POST /monitor/host-delete`

**参数：**
- `hostids` (int[], 必填): 对象ID数组

### 获取监控对象详情
**接口：** `POST /monitor/host-view`

**参数：**
- `hostid` (int, 必填): 对象ID
- `profile` (string | string[], 可选): 附加信息

### 获取监控对象指标
**接口：** `POST /monitor/host-metric`

**参数：**
- `hostid` (int, 必填): 对象ID
- `keyword` (string, 可选): 关键词(指标名称)
- `item_status` (int, 可选): 指标状态 (alert-告警指标, empty-空值指标)
- `with_latest` (int, 可选): 关联最新值 (1-关联, 0-不关联)

**返回字段说明：**
- `itemid`: 指标ID
- `name`: 指标名称
- `key_`: 指标键值
- `delay`: 采集间隔
- `description`: 描述
- `value_type`: 值类型 (0-float, 1-string, 2-log, 3-uint, 4-text)
- `status`: 启用监控 (0-是, 1-否)
- `units`: 指标单位
- `graph`: 支持图表 (0-不支持, 1-支持)
- `app_name`: 应用名称
- `apps`: 应用集
- `latest_value`: 最新值
- `latest_clock`: 最新值采集时间

### 获取指标历史数据
**接口：** `POST /monitor/metric-history`

**参数：**
- `itemid` (int|int[], 必填): 指标ID或集合（若itemid不存在时，`objectid`与`keys`参数必填）
- `objectid` (int, 可选): 对象ID
- `keys` (string|string[], 可选): 指标表达式(取指标列表的`key_`)
- `beginTime` (int, 可选): 开始时间（Unix时间戳，秒）(若无开始和结束时间，则默认最新一小时)
- `endTime` (int, 可选): 结束时间（Unix时间戳，秒）
- `raw` (bool, 可选): 是否返回text数据，即原始数据，无断点补充 (默认值：`true`)
- `type` (string, 可选): 数据类型，历史：`history`(默认) \| 趋势：`trend`(字符类型指标无趋势数据)

**返回字段说明：**
- `graph`: 图表集合数据
  - `itemid`: 指标ID
  - `hostid`: 主机ID(对象ID)
  - `host`: 对象名称
  - `name`: 指标名称
  - `unit`: 单位
  - `data`: 历史数据集合 `[[timestamp_ms, value], ...]`
- `text`: 表格集合数据
  - `itemid`: 指标ID
  - `hostid`: 主机ID(对象ID)
  - `host`: 对象名称
  - `name`: 指标名称
  - `unit`: 单位
  - `data`: 历史数据集合 `[{value, clock}, ...]`
  - `total`: 返回的data集合总数

**⚠️ 时间格式说明：**
- 请求参数中的时间戳 (`beginTime`, `endTime`) 使用 Unix 时间戳（秒）
- 返回数据中的时间：
  - `graph.data` 中的时间戳为毫秒级 Unix 时间戳（如 `1735625363000`）
  - `text.data` 中的 `clock` 字段为秒级 Unix 时间戳（如 `1735628903`）
- **显示时间时需转换为北京时间 (UTC+8)**：
  ```python
  from datetime import datetime, timezone, timedelta

  # 秒级时间戳转换
  beijing_tz = timezone(timedelta(hours=8))
  dt = datetime.fromtimestamp(clock, beijing_tz)
  formatted = dt.strftime('%Y-%m-%d %H:%M:%S')

  # 毫秒级时间戳转换
  dt = datetime.fromtimestamp(timestamp_ms / 1000, beijing_tz)
  ```

### 获取监控对象宏
**接口：** `POST /monitor/host-macro`

**参数：**
- `hostid` (int, 必填): 对象ID
- `keyword` (string, 可选): 关键词

### 监控对象表单数据
**接口：** `POST /monitor/host-form`

**参数：**
- `hostid` (int, 可选): 对象ID（不传则返回创建表单）

### 监控对象视图
**接口：** `POST /monitor/host-view`

**参数：**
- `hostid` (int, 必填): 对象ID
- `view_type` (string, 可选): 视图类型

### 监控对象报表
**接口：** `POST /monitor/host-report`

**参数：**
- `hostids` (int[], 必填): 对象ID数组
- `report_type` (string, 可选): 报表类型

## 监控配置

### 监控类型列表
**接口：** `POST /monitor/classification`

**参数：** 无

### 配置文件
**接口：** `POST /monitor/profile`

**参数：**
- `type` (string, 可选): 配置类型

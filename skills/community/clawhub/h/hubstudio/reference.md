# HubStudio API Full Reference

- OpenAPI version: `3.1.0`
- Total paths: `56`
- Total operations: `56`
- Total component schemas: `0`
- Official API docs: `https://api-docs.hubstudio.cn/`

> 本文档覆盖所有接口，包含字段说明与参数限制。

## Tag: 云手机

### `POST /api/v1/cloud-mobile/add-mobile`
- Summary: 添加云手机
- Description: 可创建新的按需云手机（暂不支持创建按月使用的云手机）
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `count` (optional) | desc=创建按需云手机的数量，默认为1 | type=integer
    - `productId` (required) | desc=云手机商品ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (required) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (required) | desc=业务数据 | type=array
        - `items` (optional) | type=string
      - `msg` (required) | desc=结果信息 | type=string
      - `requestId` (optional) | type=["string", "null"]
      - `timestamp` (optional) | type=["integer", "null"]

---

### `POST /api/v1/cloud-mobile/batch-update-adb`
- Summary: 批量更新云手机ADB状态
- Description: 批量更新云手机的ADB状态
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `enableAdb` (required) | desc=是否开启adb。true-开启，false-关闭 | type=boolean
    - `mobileIds` (required) | desc=云手机ID列表，限制20个ID | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=["integer", "null"]
      - `data` (optional) | desc=业务数据 | type=["array", "null"]
        - `items` (optional) | type=object
          - `mobileId` (optional) | desc=云手机id | type=["integer", "null"]
          - `remark` (optional) | desc=获取失败备注信息 | type=["string", "null"]
          - `success` (optional) | desc=是否成功获取   1=是  0=否 | type=["integer", "null"]
      - `msg` (optional) | desc=结果信息 | type=["string", "null"]

---

### `POST /api/v1/cloud-mobile/brand/models`
- Summary: 查询品牌机型
- Description: 查询对应安卓版本的可用品牌机型
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `productId` (required) | desc=云手机商品ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=array
        - `items` (optional) | type=object
          - `brand` (optional) | desc=品牌 | type=string
          - `model` (optional) | desc=机型 | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/cloud-mobile/del-mobile-batch`
- Summary: 批量删除云手机
- Description: 批量删除云手机
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileIds` (required) | desc=云手机列表 | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/exe-command`
- Summary: 执行shell命令
- Description: 云手机执行shell命令
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `command` (required) | desc=命令，如果是需要执行多行,使用;号隔开即可 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/get-country-time-zone-language-list`
- Summary: 国家时区语言列表
- Description: 获取云手机的国家时区语言列表
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=integer
      - `data` (optional) | desc=业务数据 | type=object
        - `countryList` (optional) | desc=国家列表 | type=array
          - `items` (optional) | type=object
            - `country` (optional) | desc=国家key。填代理时用的值 | type=string
            - `id` (optional) | desc=id | type=integer
            - `showCountry` (optional) | desc=国家显示值 | type=string
            - `timeZoneVoList` (optional) | desc=国家关联的时区 | type=array
              - `items` (optional) | type=object
                - `showTimeZone` (optional) | desc=时区显示值 | type=string
                - `timeZone` (optional) | desc=时区key。填代理时用的值 | type=string
        - `languageList` (optional) | desc=语言列表 | type=array
          - `items` (optional) | type=object
            - `language` (optional) | desc=语言key。填代理时用的值 | type=string
            - `showLanguage` (optional) | desc=语言显示值 | type=string
      - `msg` (optional) | desc=结果信息 | type=string

---

### `POST /api/v1/cloud-mobile/list-adb`
- Summary: 批量获取云手机ADB状态
- Description: 批量获取云手机的ADB状态
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileIds` (required) | desc=云手机ID列表，限制20个ID | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=["object", "null"]
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=["string", "integer", "boolean", "array", "object", "number", "null"]
      - `data` (optional) | desc=业务数据 | type=["array", "null"]
        - `items` (optional) | type=["object", "null"]
          - `adbIp` (optional) | desc=adb的ip | type=["string", "null"]
          - `adbPassword` (optional) | desc=adb连接密码 | type=["string", "null"]
          - `adbPort` (optional) | desc=adb连接端口 | type=["string", "null"]
          - `mobileId` (optional) | desc=云手机id | type=["integer", "null"]
          - `remark` (optional) | desc=获取失败备注信息 | type=["string", "null"]
          - `success` (optional) | desc=是否成功获取    1=是  0=否 | type=["integer", "null"]
      - `msg` (optional) | desc=结果信息 | type=["string", "null"]

---

### `POST /api/v1/cloud-mobile/mobile-page`
- Summary: 云手机分页列表
- Description: 获取云手机分页列表
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `adbStatus` (optional) | desc=查询ADB状态。1-开启 0-关闭 | type=integer
    - `current` (optional) | desc=分页第x页偏移量。默认为1 | type=integer
    - `mobileIds` (optional) | desc=手机ids | type=array
      - `items` (optional) | type=string
    - `name` (optional) | desc=云手机名称 | type=string
    - `size` (optional) | desc=分页条数。默认10，最多200条 | type=integer
    - `state` (optional) | desc=云手机状态，true-开机，false-关机 | type=boolean

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余表示失败 | type=["string", "null"]
      - `data` (optional) | desc=业务数据 | type=["object", "null"]
        - `list` (optional) | desc=返回数组 | type=["array", "null"]
          - `items` (optional) | type=object
            - `adbStatus` (optional) | desc=ADB状态。0-关闭，1-开启 | type=integer
            - `billingStatus` (optional) | desc=计费状态。1-正常，2-即将过期，3-已过期 | type=integer
            - `billingType` (optional) | desc=计费方式：1-按需付费，2-包月 | type=integer
            - `createTime` (optional) | desc=创建时间 | type=string
            - `expiredTime` (optional) | desc=过期时间 | type=string
            - `lastPowerOnTime` (optional) | desc=最后开机时间 | type=string
            - `mobileId` (optional) | desc=主键 | type=integer
            - `name` (optional) | desc=手机名称 | type=string
            - `number` (optional) | desc=序号 | type=integer
            - `proxyTypeId` (optional) | desc=代理类型id | type=integer
            - `remark` (optional) | desc=备注 | type=string
            - `serialNumber` (optional) | desc=编号 | type=integer
            - `status` (optional) | desc=状态。-2-创建失败，-1-初始化状态，0-关机，1-开机使用中，2-设备占用中，3-设备开机未有人使用，4-开机中，5-恢复出厂中，6-重启中 | type=integer
            - `tagId` (optional) | desc=分组id | type=integer
            - `tagName` (optional) | desc=分组 | type=string
        - `total` (optional) | desc=返回数组总数 | type=["integer", "null"]
      - `msg` (optional) | desc=结果信息 | type=["string", "null"]

---

### `POST /api/v1/cloud-mobile/mobile-product-list`
- Summary: 云手机商品列表
- Description: 获取云手机商品列表
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=["object", "null"]
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=["integer", "null"]
      - `data` (optional) | desc=业务数据 | type=["array", "null"]
        - `items` (optional) | type=["object", "null"]
          - `billingType` (optional) | desc=扣费方式：1-按需付费 | type=["integer", "null"]
          - `id` (optional) | desc=产品ID | type=["integer", "null"]
          - `origRunPrice` (optional) | desc=锚定运行费用 | type=["number", "null"]
          - `origStoragePrice` (optional) | desc=锚定存储费用 | type=["number", "null"]
          - `productName` (optional) | desc=产品名称 | type=["string", "null"]
          - `runPrice` (optional) | desc=运行费用 | type=["number", "null"]
          - `showCpu` (optional) | desc=CPU | type=["string", "null"]
          - `showMemory` (optional) | desc=内存 | type=["string", "null"]
          - `showRegionId` (optional) | desc=区域ID | type=["integer", "null"]
          - `showRegionName` (optional) | desc=区域 | type=["string", "null"]
          - `showStorage` (optional) | desc=存储 | type=["string", "null"]
          - `showSystem` (optional) | desc=系统 | type=["string", "null"]
          - `storagePrice` (optional) | desc=存储费用 | type=["number", "null"]
      - `msg` (optional) | desc=结果信息 | type=["string", "null"]
      - `requestId` (optional) | type=["string", "null"]
      - `timestamp` (optional) | type=["integer", "null"]

---

### `POST /api/v1/cloud-mobile/new-machine`
- Summary: 一键新机
- Description: 执行云手机一键新机操作
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=获取云手机ID | type=integer
    - `brand` (optional) | title=品牌 | desc=查询品牌机型列表获取对应品牌 | type=string
    - `model` (optional) | title=机型 | desc=查询品牌机型列表获取对应机型 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (optional) | desc=业务数据 | type=boolean
      - `msg` (optional) | desc=结果信息 | type=string

---

### `POST /api/v1/cloud-mobile/new-machine-status`
- Summary: 获取一键新机状态及可用数量
- Description: 获取云手机一键新机的状态及可用数量
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | title=云手机ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (optional) | desc=业务数据 | type=object
        - `availableQuantity` (optional) | desc=当前周期一键新机可用次数 | type=["integer", "null"]
        - `mobileId` (optional) | desc=云手机id | type=["integer", "null"]
        - `status` (optional) | desc=一键新机状态 false-关闭 true-开启 | type=["boolean", "null"]
        - `totalQuantity` (optional) | desc=当前周期一键新机总次数 | type=["integer", "null"]
      - `msg` (optional) | desc=结果信息 | type=string

---

### `POST /api/v1/cloud-mobile/power-on-mobile`
- Summary: 批量开启云手机
- Description: 批量开启云手机
```text
headless字段  客户端3.50.0及以上版本支持
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileIds` (required) | desc=云手机ID列表，限制20个ID | type=array
      - `items` (optional) | type=string
    - `headless` (optional) | desc=默认值为true，传false显示云手机界面，true 则不显示 | type=boolean

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=["string", "integer", "boolean", "array", "object", "number", "null"]
      - `data` (optional) | desc=业务数据 | type=object
        - `failResult` (optional) | desc=失败结果显示。不为空时展示 | type=["string", "null"]
        - `successCount` (optional) | desc=成功开机数 | type=["integer", "null"]
      - `msg` (optional) | desc=结果信息 | type=["string", "null"]

---

### `POST /api/v1/cloud-mobile/set-tag`
- Summary: 批量设置云手机分组
- Description: 批量设置云手机的分组名
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileIds` (required) | desc=云手机列表 | type=array
      - `items` (optional) | type=string
    - `tagName` (required) | desc=分组名称 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/shutdown-mobile`
- Summary: 批量关闭云手机
- Description: 批量关闭云手机
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `check` (optional) | desc=可强制关闭正在使用中的云手机（包括其他人正在使用的）。true-开启使用验证，false-不验证，默认值true | type=boolean
    - `mobileIds` (required) | desc=云手机ID列表，限制20个ID | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (optional) | desc=业务数据 | type=array
        - `items` (optional) | type=object
          - `errorMsg` (optional) | desc=失败信息 | type=string
          - `mobileId` (optional) | desc=云手机id | type=integer
          - `mobileName` (optional) | desc=云手机名称 | type=string
          - `status` (optional) | desc=状态。0-失败，1-成功 | type=integer
      - `msg` (optional) | desc=结果信息 | type=string

---

### `POST /api/v1/cloud-mobile/simulateSendSms`
- Summary: 发送短信到云手机
- Description: 修改云手机名称、备注、序号
- Deprecated: `False`

#### Parameters
- name=`mobileId` | in=`query` | required=`True` | desc=云手机ID,支持机型：Android13、支持Android14、支持Android15A | constraints=type=integer
- name=`senderNumber` | in=`query` | required=`True` | desc=发送方号码（最长21位，允许数字+空格） | constraints=type=string; minLength=8; maxLength=21
- name=`smsContent` | in=`query` | required=`True` | desc=短信内容（长度限制127位） | constraints=type=string; minLength=1; maxLength=127

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/update`
- Summary: 修改云手机信息
- Description: 修改云手机名称、备注、序号
- Deprecated: `False`

#### Parameters
- name=`mobileId` | in=`query` | required=`True` | desc=云手机ID | constraints=type=integer
- name=`name` | in=`query` | required=`False` | desc=云手机名称，不超过60字符。名称、备注、序号三个字段必须要填写1个。 | constraints=type=string
- name=`ignore` | in=`query` | required=`False` | desc=是否忽略云手机名称重复，默认：false。 | constraints=type=boolean
- name=`remark` | in=`query` | required=`False` | desc=云手机备注，不超过500字符。名称、备注、序号三个字段必须要填写1个。 | constraints=type=string
- name=`number` | in=`query` | required=`False` | desc=序号，最大值不超过999999。名称、备注、序号三个字段必须要填写1个。 | constraints=type=string

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `name` (optional) | desc=云手机名称，不超过60个字符 | type=string
    - `ignore` (optional) | desc=是否忽略云手机名称重复，默认：false | type=boolean
    - `remark` (optional) | desc=备注，不超过500个字符 | type=string
    - `number` (optional) | desc=序号，最大值不超过 999999 | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/update-proxy`
- Summary:  更新代理
- Description: 更新云手机代理
- Deprecated: `False`

#### Parameters
- name=`mobileId` | in=`query` | required=`True` | desc=云手机ID | constraints=type=integer
- name=`asDynamicType` | in=`query` | required=`False` | desc=是否动态（网络设置）。1-静态，2-动态，默认1 | constraints=type=integer
- name=`automaticPositioning` | in=`query` | required=`False` | desc=是否自动定位（定位设置）。默认true | constraints=type=boolean
- name=`followIp` | in=`query` | required=`False` | desc=跟随ip（时区/语言设置）。默认true  | constraints=type=boolean
- name=`lat` | in=`query` | required=`False` | desc=维度（定位设置） | constraints=type=number
- name=`lng` | in=`query` | required=`False` | desc=经度（定位设置） | constraints=type=number
- name=`proxyTypeId` | in=`query` | required=`True` | desc=代理类型（网络设置）。1-HTTP，2-HTTPS，4-Socks5，5-Oxylabsauto，6-Lumauto，7-Luminati，11-smartproxy | constraints=type=integer
- name=`proxyHost` | in=`query` | required=`True` | desc=代理主机地址 | constraints=type=string
- name=`proxyPort` | in=`query` | required=`True` | desc=代理端口 | constraints=type=string
- name=`proxyAccount` | in=`query` | required=`False` | desc=代理账号 | constraints=type=string
- name=`proxyPassword` | in=`query` | required=`False` | desc=代理密码 | constraints=type=string
- name=`referenceCity` | in=`query` | required=`False` | desc=参考城市（网络设置） | constraints=type=string
- name=`referenceCountryCode` | in=`query` | required=`False` | desc=参考国家code（网络设置） | constraints=type=string
- name=`referenceRegionCode` | in=`query` | required=`False` | desc=参考州code（网络设置） | constraints=type=string
- name=`timeZone` | in=`query` | required=`False` | desc=时区（时区/语言设置） | constraints=type=string
- name=`ysjLanguage` | in=`query` | required=`False` | desc=语言（时区/语言设置） | constraints=type=string
- name=`ipDatabaseChannel` | in=`query` | required=`False` | desc=代理查询渠道。支持设置查询渠道选项，1-IP2Location 2-DB-IP 3-MaxMind | constraints=type=integer

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `asDynamicType` (optional) | desc=是否动态（网络设置）。1-静态，2-动态，默认1 | type=integer
    - `automaticPositioning` (optional) | desc=是否自动定位（定位设置）。默认true | type=boolean
    - `country` (optional) | desc=国家code（时区/语言设置） | type=string
    - `dnsStrategy` (optional) | desc=DNS策略（网络设置）。0-跟随IP，1-DNS保护。默认0 | type=integer
    - `followIp` (optional) | desc=跟随ip（时区/语言设置）。默认true | type=boolean
    - `lat` (optional) | desc=维度（定位设置） | type=integer
    - `lng` (optional) | desc=经度（定位设置） | type=integer
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `proxyAccount` (optional) | desc=代理账号（网络设置） | type=string
    - `proxyHost` (required) | desc=代理主机地址（网络设置） | type=string
    - `proxyPassword` (optional) | desc=代理密码（网络设置） | type=string
    - `proxyPort` (required) | desc=代理端口（网络设置） | type=integer
    - `proxyTypeId` (required) | desc=代理类型（网络设置）。1-HTTP，2-HTTPS，4-Socks5，5-Oxylabsauto，6-Lumauto，7-Luminati，11-smartproxy | type=integer
    - `proxyTypeId2` (optional) | desc=代理类型2（网络设置）。proxyTypeId = 7时可设置 1-HTTP，2-HTTPS，4-Socks5。默认1 | type=integer
    - `referenceCity` (optional) | desc=参考城市（网络设置） | type=string
    - `referenceCountryCode` (optional) | desc=参考国家code（网络设置） | type=string
    - `referenceRegionCode` (optional) | desc=参考州code（网络设置） | type=string
    - `timeZone` (optional) | desc=时区（时区/语言设置） | type=string
    - `ysjLanguage` (optional) | desc=语言（时区/语言设置） | type=string
    - `ipDatabaseChannel` (optional) | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=integer
      - `data` (optional) | desc=业务数据 | type=boolean
      - `msg` (optional) | desc=结果信息 | type=string

---

## Tag: 云手机/应用管理

### `POST /api/v1/cloud-mobile/app/install`
- Summary: app应用安装
- Description: 安装指定应用APP
```text
备注：
1、API安装应用需要手机处于开机状态下才可以安装
2、暂时无法回传云手机内的APP应用是否安装成功，需在云手机内强刷页面，才能显示
3、只支持客户端共存的API调用方式使用
4、每秒只能安装一个应用APP
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `appVersionId` (optional) | desc=APP版本ID | type=string
    - `isEnablePermission` (optional) | desc=是否开启应用权限，默认:false | type=boolean
    - `isEnableRoot` (optional) | desc=是否开启ROOT权限，默认：false | type=boolean
    - `packageName` (optional) | desc=包名，包名与应用版本号组合使用，如果传appVersionId参数些字段可以不传 | type=string
    - `versionCode` (optional) | desc=应用版本号，包名与应用版本号组合使用，如果传appVersionId参数,该字段可以不传 | type=string
    - `mobileId` (required) | desc=云手机ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `message` (optional) | type=string
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/app/installedList`
- Summary: 已安装应用列表查询
- Description: 查询云手机已安装应用列表查询
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=array
        - `items` (optional) | type=object
          - `appName` (optional) | type=string
          - `createTime` (optional) | type=string
          - `packageName` (optional) | type=string
          - `status` (optional) | type=integer
          - `versionCode` (optional) | type=integer
          - `versionName` (optional) | type=string
      - `message` (optional) | type=string
      - `requestId` (optional) | type=string
      - `success` (optional) | type=boolean
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/cloud-mobile/app/page`
- Summary: APP列表(分页)\查询可安装应用列表
- Description: 获取APP应用列表
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `appName` (optional) | title=应用名称 | desc=模糊查询 | type=string
    - `pageNum` (optional) | title=当前页数 | desc=从1开始 | type=integer
    - `pageSize` (optional) | title=每页显示记录数 | desc=默认为10 | type=integer
    - `productId` (required) | title=云手机商品ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=object
        - `records` (optional) | type=array
          - `items` (optional) | type=object
            - `id` (optional) | desc=APPID | type=string
            - `appName` (optional) | desc=APP名称 | type=string
            - `appIcon` (optional) | desc=APP图标 | type=string
            - `packageName` (optional) | desc=包名 | type=string
            - `categoryValue` (optional) | desc=分类id | type=integer
            - `appVersionList` (optional) | desc=版本列表 | type=array
              - `items` (optional) | type=object
                - `id` (required) | desc=app版本id | type=string
                - `versionCode` (required) | desc=APP版本号 | type=string
                - `versionName` (required) | desc=APP版本名 | type=string
                - `installStatus` (required) | type=integer
        - `total` (optional) | type=integer
        - `size` (optional) | type=integer
        - `current` (optional) | type=integer
        - `orders` (optional) | type=array
          - `items` (optional) | type=string
        - `optimizeCountSql` (optional) | type=boolean
        - `hitCount` (optional) | type=boolean
        - `countId` (optional) | type=null
        - `maxLimit` (optional) | type=null
        - `searchCount` (optional) | type=boolean
        - `pages` (optional) | type=integer
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/cloud-mobile/app/restart`
- Summary: APP重启
- Description: 重启云手机中安装的app
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `packageName` (required) | desc=应用包名 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/app/start`
- Summary: APP启动
- Description: 启动云手机中安装的app
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `packageName` (required) | desc=应用包名 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=boolean
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/cloud-mobile/app/stop`
- Summary: APP停止
- Description: 停止云手机运行中的app
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `packageName` (required) | desc=应用包名 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/cloud-mobile/app/uninstall`
- Summary: APP卸载
- Description: 卸载云手机已安装的app
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `packageName` (required) | desc=应用包名 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=boolean
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/cloud-mobile/group/app/create`
- Summary: 新增团队应用
- Description: 查询云手机已安装应用列表查询
- Deprecated: `False`

#### Parameters
- name=`packageName` | in=`query` | required=`True` | desc=应用包名 | constraints=type=string
- name=`versionCode` | in=`query` | required=`True` | desc=应用版本号 | constraints=type=integer

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=array
        - `items` (optional) | type=object
          - `appName` (optional) | type=string
          - `createTime` (optional) | type=string
          - `packageName` (optional) | type=string
          - `status` (optional) | type=integer
          - `versionCode` (optional) | type=integer
          - `versionName` (optional) | type=string
      - `message` (optional) | type=string
      - `requestId` (optional) | type=string
      - `success` (optional) | type=boolean
      - `timestamp` (optional) | type=integer

---

## Tag: 云手机/文件管理

### `POST /api/v1/cloud-mobile/setKeyBox`
- Summary: 设置keyBox
- Description: 设置云手机keybox，只有在云手机开机的情况下才能进行设置，同步keybox的xml文件已经上传到云手机上
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `mobileId` (required) | desc=云手机ID | type=integer
    - `filePath` (required) | desc=文件路径，例如：/sdcard/Download/xxx.xml | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object

---

### `POST /api/v1/cloud-mobile/upload-file`
- Summary: 公网文件上传文件到云手机
- Description: 上传文件到云手机
- Deprecated: `False`

#### Parameters
- name=`mobileId` | in=`query` | required=`False` | desc=云手机ID | constraints=type=integer
- name=`downloadDest` | in=`query` | required=`True` | desc=文件保存地址 | constraints=type=string
- name=`fileName` | in=`query` | required=`True` | desc=文件名称 | constraints=type=string
- name=`fileUrl` | in=`query` | required=`True` | desc=文件地址 | constraints=type=string

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `downloadDest` (optional) | title=上传至云手机中的目录 | desc=如果仅一层目录不存在，将自动创建；如果多层目录不存在，无法自动创建 | type=string
    - `fileUrl` (optional) | title=文件地址 | type=string
    - `mobileId` (required) | title=云手机ID | type=integer
    - `fileName` (optional) | title=文件名称 | desc=上传后文件叫什么名字 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (optional) | desc=业务数据 | type=boolean
      - `msg` (optional) | desc=结果信息 | type=string

---

### `POST /api/v2/cloud-mobile/upload-file`
- Summary: 选择本地上传文件到云手机
- Description: 上传文件到云手机
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `multipart/form-data`
  - `body` (optional) | type=object
    - `downloadDest` (optional) | desc=上传至云手机中的目录，如果仅一层目录不存在，将自动创建；如果多层目录不存在，无法自动创建 | type=string | example=/Download
    - `fileUrl` (required) | desc=文件地址 | type=string | format=binary | example=file://C:\Users\Administrator\Desktop\API接口.txt
    - `mobileId` (required) | desc=云手机ID | type=string | example=3279080
    - `fileName` (optional) | desc=文件名称，文件上传到云手机的名字，注意包括后缀 | type=string | example=文件名

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | desc=结果码。0表示成功，其余为失败 | type=string
      - `data` (optional) | desc=业务数据 | type=boolean
      - `msg` (optional) | desc=结果信息 | type=string

---

## Tag: 分组管理

### `POST /api/v1/group/create`
- Summary: 新建环境分组
- Description: 添加环境的分组，名称不能重复
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `tagName` (required) | desc=命名环境分组 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/group/del`
- Summary: 删除环境分组
- Description: 删除指定名称的环境分组。删除成功后返回true
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `tagCode` (required) | desc=删除指定名称的分组 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/group/list`
- Summary: 获取环境分组列表
- Description: 查询当前团队内的浏览器环境分组名称。查询成功返回分组名称和分组ID
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=array
        - `items` (optional) | type=object
          - `tagName` (required) | title=分组名称 | type=string
          - `tagCode` (required) | title=分组ID | type=["integer", "null"]

---

## Tag: 平台账号管理

### `POST /api/v1/account/del`
- Summary: 账号删除
- Description: 删除账号信息
```text
- 请求体不能为空，必须包含 accountIds 字段。可以传空数组 {}，但不能完全不传请求体。
- accountIds 数组不能为空，必须包含至少一个账号ID。
- 可以同时传入多个账号ID进行批量删除。
- 该操作具有原子性，如果提供的账号ID列表中有一个不存在，则整个删除操作都会失败，不会删除任何账号。
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `accountIds` (required) | desc=账号ID数组，例：[1111] | type=array
      - `items` (optional) | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/account/list`
- Summary: 账号分页列表
- Description: - 查询平台账号的信息。用户仅能查询自己有权限的平台账号信息
- 请求体可以所有字段都为空，但是必须传 {}，不能是空请求体
- 如果传空字符串，该字段不会进行过滤查询
- 需要具备"团队设置-编辑-环境-我的账号-密码查看"权限才能返回账号密码信息，没有此权限则返回null
需要具备"团队设置-编辑-环境-我的账号-密码查看"权限才能返回账号密码信息，没有此权限则返回null。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `accountName` (optional) | title=账号 | type=string
    - `current` (optional) | title=当前页 | type=integer
    - `name` (optional) | title=自定义账号名称 | desc=传null和空字段等于没有过滤该字段 | type=string
    - `size` (optional) | title=每页数据 | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=object
        - `list` (optional) | type=array
          - `items` (optional) | type=object
            - `accountId` (optional) | type=integer
            - `name` (optional) | type=string
            - `accountName` (optional) | type=string
            - `accountPassword` (optional) | type=string
            - `otpSecret` (optional) | type=string
            - `siteName` (optional) | type=string
            - `siteAlias` (optional) | type=null
            - `domainName` (optional) | type=null
        - `total` (optional) | type=integer

---

### `POST /api/v1/account/update`
- Summary: 账号更新
- Description: 修改账号信息
```text
注意：
- accountId 为必传参数。
- accountPassword, name, otpSecret 三个参数中必须至少有一个，可以多个。
- 如果给某个可选参数传递空字符串 (如 "name": "")，则会清空数据库中该字段对应的数据。
- 如果不传递某个可选参数 (例如不传 name 字段)，则不对该字段进行任何修改。
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `accountId` (optional) | title=账号id，通过账号列表查询 | type=integer
    - `accountPassword` (optional) | title=账号密码 | desc=accountPassword, name, otpSecret 三个参数中必须至少有一个，可以多个 | type=string
    - `name` (optional) | title=自定义的账号名称 | desc=accountPassword, name, otpSecret 三个参数中必须至少有一个，可以多个 | type=string
    - `otpSecret` (optional) | title=2FA密钥 | desc=accountPassword, name, otpSecret 三个参数中必须至少有一个，可以多个 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/container/add-account`
- Summary: 添加环境账号
- Description: 为环境添加账号信息
```text
注意：
- 当 siteName 为 "自定义平台" 时，系统会判断此为自定义平台。如果 domainName 相同，则不会新增账号记录。
- 当 siteName 为官方内置平台名称（如“加拿大亚马逊”）时，系统会判断此为内置平台。需要平台名称 (siteName) 和平台账号 (accountName) 都相同，才不会被添加；如果其中任何一个不同，都会添加一条新的账号记录。
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `accountName` (required) | desc=平台账号 | type=string
    - `accountPassword` (required) | desc=平台密码 | type=string
    - `containerCode` (required) | desc=环境编号 | type=integer
    - `domainName` (optional) | desc=自定义平台的域名 | type=string
    - `name` (optional) | desc=自定义账号名称 | type=string
    - `otpSecret` (optional) | desc=2FA密钥 | type=string
    - `siteAlias` (optional) | desc=自定义平台的别名 | type=string
    - `siteName` (required) | desc=平台名称 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=boolean

---

## Tag: 浏览器环境

### `POST /api/v1/browser/all-browser-status`
- Summary: 获取所有打开环境
- Description: 支持不传参数或传空数组，获取所有已打开环境。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (optional) | desc=环境ID | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `containers` (optional) | type=array
          - `items` (optional) | type=object
            - `containerCode` (optional) | type=string
            - `status` (optional) | type=integer
        - `err` (optional) | type=string
        - `requestId` (optional) | type=string
        - `statusCode` (optional) | type=string

---

### `POST /api/v1/browser/arrange`
- Summary: 浏览器窗口自定义排列
- Description: 用于已打开浏览器窗口自定义排列，不传值则使用默认值进行浏览器窗口排列
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `x` (optional) | desc=起始位置x坐标；默认为10，取值可为0~9999之间的整数 | type=integer
    - `y` (optional) | desc=起始位置y坐标；默认为10，取值可为0~9999之间的整数 | type=integer
    - `width` (optional) | desc=窗口宽度；默认为600，取值范围500~9999之间的整数 | type=integer
    - `height` (optional) | desc=窗口高度；默认为500，取值范围200~9999之间的整数 | type=integer
    - `gapX` (optional) | desc=窗口横向间距；默认为20，取值范围-9999~9999之间的整数 | type=integer
    - `gapY` (optional) | desc=窗口纵向间距；默认为20，取值范围-9999~9999之间的整数 | type=integer
    - `colNum` (optional) | desc=每行展示窗口数量；默认为3，取值范围1~99之间的整数 | type=integer
    - `screenId` (optional) | desc=屏幕id | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=["string", "null"]
      - `msg` (optional) | type=["string", "null"]
      - `code` (optional) | type=["integer", "null"]
      - `data` (optional) | type=["object", "null"]
        - `action` (optional) | type=["string", "null"]
        - `err` (optional) | type=["string", "null"]
        - `requestId` (optional) | type=["string", "null"]
        - `statusCode` (optional) | type=["string", "null"]

---

### `POST /api/v1/browser/foreground`
- Summary: 切换浏览器窗口
- Description: 切换浏览器窗口，将窗口置顶显示
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `containerCodes` (optional) | desc=环境ID | type=string
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `requestId` (optional) | type=string
        - `statusCode` (optional) | type=string

---

### `POST /api/v1/browser/start`
- Summary: 打开环境
- Description: - 用于启动指定的环境，启动成功后可以获取浏览器debug端口用于执行selenium和puppeteer自动化脚本
- 目前Hubstudio采用100版Chrome内核
- Selenium需要使用到匹配的Webdriver，需更新到应用版本2.4.2及以上版本。返回的debuggingPort参数可用于自动化工具连接。
- Deprecated: `False`

#### Parameters
- name=`Authorization` | in=`header` | required=`False` | desc=用户端API使用/服务端API使用      token | constraints=type=string; default={{Authorization}}
- name=`X-Nonce-Id` | in=`header` | required=`False` | desc=用户端API使用     随机 | constraints=type=string; default={{X-Nonce-Id}}
- name=`X-Api-Id` | in=`header` | required=`False` | desc=用户端API使用     apiId | constraints=type=string; default={{X-Api-Id}}

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=string
    - `isWebDriverReadOnlyMode` (optional) | desc=是否只读模式，默认false。（true代表只读模式，不会保存cookie等数据） | type=boolean
    - `skipSystemResourceCheck` (optional) | desc=默认false不跳过系统可用资源检测(仅支持v3.6.0及以上版本) | type=boolean
    - `containerTabs` (optional) | desc=启动url | type=array
      - `items` (optional) | type=string
    - `cdpHide` (optional) | desc=是否屏蔽cdp检测，默认false（true代表屏蔽）仅支持ChroBrowser133及以上内核版本 | type=boolean
    - `shouldCloseTabsOnOpen` (optional) | desc=是否打开历史标签页。需要在客户端 "偏好设置-个人设置-启动环境时" 选项中，选择 "打开上次"，此参数才会生效。当 shouldCloseTabsOnOpen 为 true 时，会同步服务端的标签页数据到客户端，即打开上次关闭时的标签页。当 shouldCloseTabsOnOpen 为 false 时，不会同步服务端的标签页数据，客户端的现有标签页数据不会被覆盖。 | type=boolean
    - `pageZoom` (optional) | desc=只能传原生支持的比例，原生支持 50%，75%， 100%，125%，150%，175%，200%，其它参数不支持，150% 传 1.5。此参数仅支持3.46.0及以上版本 | type=number
    - `isHeadless` (optional) | desc=浏览器无头模式。默认false，设置无头后如无法连接，请使用用"args"参数进行设置: ["--headless=new"] | type=boolean
    - `args` (optional) | desc=启动参数 | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `backgroundPluginId` (optional) | type=string
        - `browserID` (optional) | desc=浏览器id，用于清理缓存接口 | type=string
        - `browserPath` (optional) | type=string
        - `containerCode` (optional) | type=string
        - `containerId` (optional) | type=integer
        - `debuggingPort` (optional) | desc=浏览器调试端口，用于自动化工具连接 | type=integer
        - `downloadPath` (optional) | type=string
        - `duplicate` (optional) | type=integer
        - `err` (optional) | type=string
        - `ip` (optional) | type=string
        - `isDynamicIp` (optional) | type=boolean
        - `launcherPage` (optional) | type=string
        - `proxyType` (optional) | type=string
        - `requestId` (optional) | type=string
        - `runMode` (optional) | type=string
        - `statusCode` (optional) | type=integer
        - `webdriver` (optional) | desc=根据当前打开环境的内核返回对应内核webdriver驱动路径 | type=string
        - `accountId` (optional) | type=null
        - `proxyTag` (optional) | type=string
        - `reportPluginId` (optional) | type=string

---

### `POST /api/v1/browser/stop`
- Summary: 关闭环境
- Description: 关闭指定环境
- Deprecated: `False`

#### Parameters
- name=`containerCode` | in=`query` | required=`True` | constraints=type=string

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `containerCode` (optional) | desc=环境id | type=string
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `requestId` (optional) | type=string
        - `statusCode` (optional) | type=string

---

### `POST /api/v1/browser/stop-all`
- Summary: 关闭所有环境接口
- Description: 支持关闭所有环境，接口参数传 true 会清空启动环境队列。
```text 
备注：`因Firebrowser原生内核原因，该类环境不支持通过API打开
```
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `clearOpening` (optional) | desc=传 true 会清空启动环境队列 | type=boolean

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `statusCode` (optional) | type=string
        - `requestId` (optional) | type=string
      - `requestId` (optional) | type=string

---

### `POST /api/v1/display/all`
- Summary: 获取全部屏幕（物理机的屏幕）
- Description: 用于获取全部屏幕，获取到的屏幕id可用于浏览器环境窗口自定义排列。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `requestId` (optional) | type=string
        - `screens` (optional) | type=array
          - `items` (optional) | type=object
            - `current` (required) | type=boolean
            - `height` (required) | type=integer
            - `id` (required) | type=integer
            - `internal` (required) | type=boolean
            - `isPrimaryScreen` (required) | type=boolean
            - `realHeight` (required) | type=integer
            - `realWidth` (required) | type=integer
            - `scaleFactor` (required) | type=integer
            - `width` (required) | type=integer
            - `x` (required) | type=integer
            - `y` (required) | type=integer
        - `statusCode` (optional) | type=string

---

## Tag: 环境管理

### `POST /api/v1/browser/download-core`
- Summary: 下载内核
- Description: 下载环境内核
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `Cores` (required) | type=array
      - `items` (optional) | type=object
        - `BrowserType` (required) | desc=浏览器内核类型，1-Chrome，2-Firefox | type=integer
        - `Version` (required) | desc=内核版本。仅支持hub客户端支持的版本下载。 | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `info` (optional) | type=string
        - `requestId` (optional) | type=string
        - `statusCode` (optional) | type=string

---

### `POST /api/v1/browser/reset-extension`
- Summary: 清理环境内插件缓存
- Description: 清理环境内插件缓存，清理成功后插件的所有数据均会被删除
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `browserOauth` (required) | desc=打开环境时返回的browserID | type=integer
    - `pluginIds` (required) | desc=指定要清除的插件的ID， 可通过chrome://extensions/查看环境内所有插件的ID | type=array
      - `items` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `data` (optional) | type=object
        - `info` (optional) | type=string
        - `statusCode` (optional) | type=string
        - `err` (optional) | type=string
        - `action` (optional) | type=string

---

### `POST /api/v1/cache/clear`
- Summary: 清除环境本地缓存
- Description: 清除环境本地缓存
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `browserOauths` (optional) | desc=打开环境时返回的browserID，参数不传则删除所有环境的本地缓存 | type=array
      - `items` (optional) | type=string
    - `localStorage ` (optional) | desc=是否清除 LocalStorage，默认为否 | type=boolean
    - `indexedDB` (optional) | desc=是否清除 IndexedDB，默认为否 | type=boolean
    - `cookie` (optional) | desc=是否清除 cookie，默认为否 | type=boolean
    - `extension` (optional) | desc=是否清除扩展数据，默认为否，不清除 | type=boolean
    - `extensionFile` (optional) | desc=是否清除扩展，默认为否，不清除 | type=boolean

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `action` (optional) | type=string
        - `err` (optional) | type=string
        - `failIds` (optional) | type=array
          - `items` (optional) | type=integer
        - `info` (optional) | type=string
        - `requestId` (optional) | type=string
        - `statusCode` (optional) | type=string
        - `successIds` (optional) | type=array
          - `items` (optional) | type=integer

---

### `POST /api/v1/container/batch-update-remark`
- Summary: 批量修改备注
- Description: 批量修改多个环境的备注
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCodes` (optional) | desc=环境编码 | type=array
      - `items` (optional) | type=string
    - `remark` (optional) | desc=备注 | type=string
    - `type` (optional) | desc=修改类型 1覆盖 2追加 | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean
      - `message` (optional) | type=string
      - `requestId` (optional) | type=string
      - `success` (optional) | type=boolean
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/container/webgl-renderer-list`
- Summary: 查询webglVendor和webglRenderer
- Description: 查询WebglInfo信息
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `data` (optional) | type=array
        - `items` (optional) | type=object
          - `renderer` (optional) | type=string
          - `vendor` (optional) | type=string
      - `message` (optional) | type=string
      - `requestId` (optional) | type=string
      - `success` (optional) | type=boolean
      - `timestamp` (optional) | type=integer

---

### `POST /api/v1/env/create`
- Summary: 创建环境
- Description: 创建环境，支持配置环境的名称、备注、分组和代理信息。创建成功后返回环境ID
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerName` (required) | desc=命名环境，限制60字以内 | type=string
    - `remark` (optional) | desc=环境备注信息 | type=string
    - `tagName` (optional) | desc=指定环境所属分组的名称。若分组名称不存在，将默认环境未分组。 | type=string
    - `cookie` (optional) | desc=支持JSON格式的cookie | type=string
    - `asDynamicType` (required) | desc=IP变更提醒；1-静态 ，2-动态 | type=integer
    - `proxyTypeName` (required) | desc=1、自定义代理类型：HTTP、HTTPS、SSH、Socks5、Oxylabsauto、Lumauto_HTTP 、Lumauto_HTTPS 、Luminati_HTTP、Luminati_HTTPS、 smartproxy、Iphtml_HTTP、Iphtml_Socks5、IPIDEA、不使用代理              2、API提取代理类型：  Socks5_ROLA_IP、HTTPS_ROLA_IP、 Socks5_922S5、HTTP_922S5、HTTPS_922S5、 Socks5_通用api、HTTP_通用api、HTTPS_通用api、Socks5_IPIDEA-API、HTTP_IPIDEA-API、HTTPS_IPIDEA-API | type=string
    - `ipGetRuleType` (optional) | desc=IP提取方式，1-IP失效时提取新IP ，2-，每次打开环境时提取新IP。API提取代理时必填 | type=integer
    - `linkCode` (optional) | desc=提取链接。API提取代理时必填 | type=string
    - `proxyServer` (optional) | desc=代理主机，自定义代理时必填 | type=string
    - `proxyPort` (optional) | desc=代理端口，自定义代理时必填 | type=integer
    - `proxyAccount` (optional) | desc=代理帐号 | type=string
    - `proxyPassword` (optional) | desc=代理密码 | type=string
    - `referenceCountryCode` (optional) | desc=环境内帐号需要登录的指定的国家。Oxylabsauto、Lumauto、Smartproxy必须填写国家或者IP | type=string
    - `referenceIp` (optional) | desc=将根据IP自动填充环境内帐号需要登录的指定的国家。Oxylabsauto、Lumauto、Smartproxy必须填写国家或者IP | type=string
    - `referenceCity` (optional) | desc=参考城市 | type=string
    - `referenceRegionCode` (optional) | desc=参考州 | type=string
    - `ipDatabaseChannel` (optional) | desc=代理查询渠道，当用户未指定时使用全局默认值。支持设置查询渠道选项，1-IP2Location   2-DB-IP   3-MaxMind | type=integer
    - `ipProtocolType` (optional) | desc=IP协议选项，支持设置IP协议，新环境默认使用速度优先                                                                            1.速度优先  2.IPv4  3.IPv6 | type=integer
    - `type` (optional) | desc=操作系统参数：windows、android、ios、macos（不传参数默认windows） | type=string
    - `phoneModel` (optional) | desc=type选择Android和IOS时，机型必填。机型参数包括：“google Pixel 4、红米8、红米7、google Pixel 5a、三星Galaxy Note8、小米10、三星Galaxy S9+、小米9、iPhone 6 Plus、iPhone 8 Plus、iPhone SE 2、iPhone 7 Plus、iPhone X、iPhone13 Pro、iPhone XS、iPhone 13 Pro Max、iPhone 12 mini、iPhone 8、iPhone 13 mini、iPhone 6、iPhone 12 Pro Max、iPhone 7、iPhone 12 、iPhone 12 Pro、iPhone 11 Pro、iPhone 13、iPhone 14、iPhone 14 Pro、iPhone 14 Pro Max、iPhone 15、iPhone 15 Pro、iPhone 15 Pro Max、google Pixel 6、google Pixel 6a、google Pixel 6 Pro、google Pixel 7、google Pixel 7 Pro、google Pixel 7a、google Pixel 8、google Pixel 8 Pro、google Pixel 8a、Samsung Galaxy S20、Samsung Galaxy S20 +、Samsung Galaxy S21、Samsung Galaxy S21 +、Samsung Galaxy S21 Ultra、Samsung Galaxy S22、Samsung Galaxy S22 +、Samsung Galaxy S22 Ultra ”” | type=string
    - `browser` (optional) | desc=非必填，可以填firefox/chrome，不填默认创建谷歌环境， | type=string
    - `coreVersion` (optional) | desc=内核版本号，支持100~126。用selenium时，可以根据这个字段来判断驱动chromedriver的版本号。 | type=integer
    - `videoThrottle` (optional) | desc=视频限流 0关闭 1开启 2跟随团队。不传参默认跟随团队。 | type=integer
    - `imgThrottle` (optional) | desc=图片限流 0关闭 1自定义 2跟随团队。不传参默认跟随团队。 | type=integer
    - `imgThrottleSize` (optional) | desc=图片尺寸大小 | type=integer
    - `advancedBo` (optional) | desc=Hubstudio浏览器高级指纹参数配置 | type=object
      - `uaVersion` (optional) | desc=ua版本 | type=string
      - `ua` (optional) | desc=自定义UA要求传参格式符合标准。举例：Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 | type=string
      - `languageType` (optional) | desc=界面语言类型。0-跟随IP，1-自定义，2-跟随电脑 | type=integer
      - `languages` (optional) | desc=默认使用第一个传入的语言作为渲染语言 | type=array
        - `items` (optional) | type=string
      - `gmt` (optional) | desc=timezone时区，不传参默认使用系统默认。自定义时格式举例：GMT-12:00 | type=string
      - `geography` (optional) | desc=timezone地理，不传参默认使用系统默认。自定义时格式举例： Etc/GMT + 12 | type=string
      - `geoTips` (optional) | desc=网站请求获取您当前地理位置时的选择，0-ask（询问）、2-block（禁止） | type=integer
      - `geoRule` (optional) | desc=Geolocation地理位置规则。不传参默认使用系统默认。0-基于IP生成对应位置，1-使用自定义设置的位置 | type=integer
      - `longitude` (optional) | desc=地理位置自定义时必填，格式如“-40.123”（范围-180到180） | type=string
      - `latitude` (optional) | desc=地理位置自定义时必填，格式如“30.123”（范围-90到90） | type=string
      - `radius` (optional) | desc=地理位置自定义时必填，，格式如“10“（范围10-5000） | type=string
      - `height` (optional) | desc=分辨率-高，type为Android或IOS时，不支持设置分辨率。分辨率高、宽都传-1时，分辨率随机 | type=string
      - `width` (optional) | desc=分辨率-宽，type为Android或IOS时，不支持设置分辨。分辨率高、宽都传-1时，分辨率随机 | type=string
      - `fontsType` (optional) | desc=字体列表保护，0-隐私，1-真实 | type=integer
      - `fonts` (optional) | desc=按照字体的英文传入（编辑环境时，请将所有的字体传入。若传入的字体过少，可能会导致网页数据显示不全） | type=array
        - `items` (optional) | type=string
      - `fontFingerprint` (optional) | desc=字体指纹，0-开启ClientRects隐私保护，1-使用电脑默认的ClientRects | type=integer
      - `webRtc` (optional) | desc=0-开启WebRTC，但禁止获取IP，1-开启WebRTC，将公网IP替换为代理IP，2-开启WebRTC，跟随电脑真实IP，3-禁用WebRTC，网站会检测到您关闭了WebRTC，4-转发WebRTC，将公网IP替换为代理IP | type=integer
      - `webRtcLocalIp` (optional) | desc=内网IP。10.0.0.0/8；10.0.0.0 - 10.255.255.255；172.16.0.0/12；172.16.0.0 - 172.31.255.255；192.168.0.0/16；192.168.0.0 - 192.168.255.255 | type=string
      - `canvas` (optional) | desc=0-开启Canvas隐私保护，1-跟随电脑的Canvas | type=integer
      - `webgl` (optional) | desc=0-开启WebGL隐私保护，1-跟随电脑的WebGL | type=integer
      - `hardwareAcceleration` (optional) | desc=0-关闭硬件加速，1-开启硬件加速 | type=integer
      - `webglInfo` (optional) | desc=开启硬件加速时可传参，不传参默认使用系统默认。0-webglvendor和webglRenderer信息将根据ua进行匹配，1-跟随电脑的WebGL Info | type=integer
      - `audioContext` (optional) | desc=0-开启AudioContext隐私保护，1-跟随电脑的AudioContext | type=integer
      - `speechVoices` (optional) | desc=0-开启SpeechVoices，1-关闭SpeechVoicess | type=integer
      - `media` (optional) | desc=0-开启媒体设备隐私保护，1-使用Chrome原生隐私保护（不授权则不会暴露真实媒体设备数量） | type=integer
      - `cpu` (optional) | desc=2,4,6,8，10,12,16,0（0代表真实） | type=integer
      - `memory` (optional) | desc=2,4,6,8,0（0代表真实） | type=integer
      - `doNotTrack` (optional) | desc=0-默认不设置，1-默认不允许追踪，2-默认允许追踪 | type=integer
      - `battery` (optional) | desc=0-开启电池隐私保护，1-使用电脑真实的电池信息,2-禁止访问电池信息 | type=integer
      - `portScan` (optional) | desc=0-不允许网站检测您使用的本地网络端口，1-允许网站检测您使用的本地网络端口 | type=integer
      - `whiteList` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `containerCode` (optional) | desc=环境ID | type=integer
        - `coreVersion` (optional) | desc=环境使用的内核版本，用于匹配对应版本的webdriver | type=integer

---

### `POST /api/v1/env/del`
- Summary: 删除环境
- Description: 删除指定环境。删除成功返回true。一次性最多支持删除环境1000个。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCodes` (required) | desc=支持传多个环境ID | type=array
      - `items` (optional) | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/env/export-cookie`
- Summary: 导出Cookie
- Description: 导出指定环境的cookie，导出成功返回cookie的json串
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=string

---

### `POST /api/v1/env/import-cookie`
- Summary: 导入Cookie
- Description: 向指定环境导入cookie，导入成功返回true。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=string
    - `cookie` (required) | desc=值为[]是清空cookie | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/env/list`
- Summary: 获取环境列表
- Description: 查询环境的信息。用户仅能查询自己有权限的环境信息
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCodes` (optional) | desc=指定环境ID查询环境 | type=array
      - `items` (optional) | type=string
    - `containerName` (optional) | desc=指定环境名称查询环境 | type=string
    - `createEndTime` (optional) | desc=创建时间-截止时间，example: yyyy-MM-dd HH:mm:ss | type=string
    - `createStartTime` (optional) | desc=创建时间-起始时间，example: yyyy-MM-dd HH:mm:ss | type=string
    - `ipAddress` (optional) | desc=IP地址查询 | type=string
    - `proxyTypeNames` (optional) | desc=代理类型：HTTP、HTTPS、SSH、Socks5、Oxylabsauto、Lumauto 、Luminati、 smartproxy、IPIDEA、Iphtml、不使用代理 | type=array
      - `items` (optional) | type=string
    - `remark` (optional) | desc=指定环境备注信息查询环境 | type=string
    - `noTag` (optional) | desc=默认不传参，若需要查询“未分组”的环境，传任意 | type=integer
    - `tagNames` (optional) | desc=环境分组名称数组，查询指定分组的环境 | type=array
      - `items` (optional) | type=string
    - `current` (optional) | desc=分页第几页偏移量 | type=integer
    - `size` (optional) | desc=分页条数，最多200条。 | type=integer
    - `serviceProvider` (optional) | desc=环境内代理所属服务商：ROLA_IP、922S5、通用api | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=object
        - `list` (optional) | type=array
          - `items` (optional) | type=object
            - `allOpenTime` (optional) | desc=环境最后打开时间 | type=string
            - `asDynamicType` (optional) | desc=代理使用方式，1-静态，2-动态 | type=integer
            - `containerCode` (optional) | desc=环境ID | type=integer
            - `containerName` (optional) | desc=环境名称 | type=string
            - `createTime` (optional) | desc=创建时间 | type=string
            - `lastCity` (optional) | desc=上一次IP的城市 | type=string
            - `lastCountry` (optional) | desc=上一次IP的国家 | type=string
            - `lastRegion` (optional) | desc=洲或省的名称 | type=string
            - `lastUsedIp` (optional) | desc=上一次使用的IP | type=string
            - `openTime` (optional) | desc=打开时间 | type=string
            - `proxyHost` (optional) | desc=代理主机 | type=string
            - `proxyPort` (optional) | desc=代理端口号 | type=integer
            - `proxyTypeName` (optional) | desc=代理类型 | type=string
            - `tagName` (required) | desc=环境分组名称 | type=string
            - `tagCode` (required) | desc=环境ID | type=string
            - `referenceCountryCode` (optional) | type=string
            - `serialNumber` (required) | desc=环境序号 | type=integer
            - `proxyAccount` (required) | desc=代理ip的账号 | type=string
            - `proxyPassword` (required) | desc=代理ip的密码 | type=string
            - `refreshUrl` (required) | desc=刷新URL | type=string
            - `ua` (required) | desc=环境ua（仅支持3.39.0及以上客户端版本） | type=string
        - `total` (optional) | type=integer

---

### `POST /api/v1/env/proxy/update`
- Summary: 更新环境代理
- Description: 修改指定环境的代理信息，包括代理主机、端口、帐号、密码等。更新成功返回true
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=integer
    - `asDynamicType` (required) | desc=IP使用方式；1-静态 ，2-动态 | type=integer
    - `proxyTypeName` (required) | desc=1、自定义代理类型：HTTP、HTTPS、SSH、Socks5、Oxylabsauto、Lumauto_HTTP 、Lumauto_HTTPS 、Luminati_HTTP、Luminati_HTTPS、 smartproxy、Iphtml_HTTP、Iphtml_Socks5、IPIDEA、不使用代理              2、API提取代理类型：  Socks5_ROLA_IP、HTTP_ROLA_IP、HTTPS_ROLA_IP、 Socks5_922S5、HTTP_922S5、HTTPS_922S5、 Socks5_通用api、HTTP_通用api、HTTPS_通用api、Socks5_IPIDEA-API、HTTP_IPIDEA-API、HTTPS_IPIDEA-API | type=string
    - `ipGetRuleType` (optional) | desc=IP提取方式，1-IP失效时提取新IP ，2-，每次打开环境时提取新IP。API提取代理时必填 | type=integer
    - `linkCode` (optional) | desc=提取链接。API提取代理时必填 | type=string
    - `proxyHost` (optional) | desc=代理主机 | type=string
    - `proxyPort` (optional) | desc=代理端口 | type=integer
    - `proxyAccount` (optional) | desc=代理帐号 | type=string
    - `proxyPassword` (optional) | desc=代理密码 | type=string
    - `referenceCountryCode` (optional) | desc=环境内帐号需要登录的指定的国家。Oxylabsauto、Lumauto、Smartproxy必须填写国家或者IP | type=string
    - `referenceCity` (optional) | desc=参考城市 | type=string
    - `referenceRegionCode` (optional) | desc=参考州 | type=string
    - `ipDatabaseChannel` (optional) | desc=代理查询渠道。支持设置查询渠道选项，1-IP2Location  2-DB-IP   3-MaxMind | type=integer
    - `ipProtocolType` (optional) | desc=IP协议选项，支持设置IP协议 1.速度优先 2.IPv4   3.IPv6 | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

### `POST /api/v1/env/random-ua`
- Summary: 获取随机UA
- Description: 获取随机UA，获取成功返回UA
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `type` (optional) | desc=操作系统参数：windows、android、ios（不传参数默认windows） | type=string
    - `phoneModel` (optional) | desc=type选择android和ios时，机型必填。机型参数包括：“google Pixel 4、红米8、红米7、google Pixel 5a、三星Galaxy Note8、小米10、三星Galaxy S9+、小米9、iPhone 6 Plus、iPhone 8 Plus、iPhone SE 2、iPhone 7 Plus、iPhone X、iPhone 13 Pro、iPhone XS、iPhone 13 Pro Max、iPhone 12 mini、iPhone 8、iPhone 13 mini、iPhone 6、iPhone 12 Pro Max、iPhone 7、iPhone 12 、iPhone 12 Pro、iPhone 11 Pro、iPhone 13、iPhone 14、iPhone 14 Pro、iPhone 14 Pro Max、iPhone 15、iPhone 15 Pro、iPhone 15 Pro Max、google Pixel 6、google Pixel 6a、google Pixel 6 Pro、google Pixel 7、google Pixel 7 Pro、google Pixel 7a、google Pixel 8、google Pixel 8 Pro、google Pixel 8a、Samsung Galaxy S20、Samsung Galaxy S20 +、Samsung Galaxy S21、Samsung Galaxy S21 +、Samsung Galaxy S21 Ultra、Samsung Galaxy S22、Samsung Galaxy S22 +、Samsung Galaxy S22 Ultra ” | type=string
    - `version` (optional) | desc=支持数组，不传参默认随机。范围包括95、96、97、98、99、100、101、102、103、104、105、106 | type=array
      - `items` (optional) | type=integer

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=string

---

### `POST /api/v1/env/refresh-fingerprint`
- Summary: 刷新指纹
- Description: - 刷新指纹
- 仅支持v3.37以上版本，请前往官网下载客户端最新版本【下载Hubstudio最新版】
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=integer
    - `uaVersion` (optional) | desc=UA版本。不传 uaVersion ，默认随机最新UA | type=integer
    - `coreVersion` (optional) | desc=客户端内核版本，不传，不会改变 | type=integer
    - `type` (optional) | desc=操作系统类型，不传默认为windows | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `code` (optional) | type=integer
      - `msg` (optional) | type=string
      - `requestId` (optional) | type=string
      - `timestamp` (optional) | type=integer
      - `data` (optional) | type=null

---

### `POST /api/v1/env/update`
- Summary: 更新环境
- Description: 修改环境参数，包括备注信息和分组名称。更新成功返回true。
- Deprecated: `False`

#### Request Body
- required: `False`
- content-type: `application/json`
  - `body` (optional) | type=object
    - `containerCode` (required) | desc=环境ID | type=integer
    - `containerName` (required) | desc=环境命名，若无需更改环境名称传入原有名称即可 | type=string
    - `remark` (optional) | desc=环境备注信息。不传视为留空，会覆盖原备注 | type=string
    - `tagName` (required) | desc=环境所属分组信息，若分组名称不存在，将默认不修改环境分组 | type=string
    - `coreVersion` (required) | desc=内核版本号，支持100~126。用selenium时，可以根据这个字段来判断驱动chromedriver的版本号。 | type=integer
    - `videoThrottle` (optional) | desc=视频限流 0关闭 1开启 2跟随团队。不传参默认跟随团队。 | type=integer
    - `imgThrottle` (optional) | desc=图片限流 0关闭 1自定义 2跟随团队。不传参默认跟随团队。 | type=integer
    - `imgThrottleSize` (optional) | desc=图片尺寸大小 | type=integer
    - `advancedBo` (optional) | desc=Hubstudio浏览器高级指纹参数配置 | type=object
      - `uaVersion` (optional) | desc=ua版本 | type=string
      - `ua` (optional) | desc=自定义UA要求传参格式符合标准。举例：Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 | type=string
      - `languageType` (optional) | desc=界面语言类型。0-跟随IP，1-自定义，2-跟随电脑 | type=integer
      - `languages` (optional) | desc=默认使用第一个传入的语言作为渲染语言 | type=array
        - `items` (optional) | type=string
      - `gmt` (optional) | desc=timezone时区，不传参默认使用系统默认。自定义时格式举例：GMT-12:00 | type=string
      - `geography` (optional) | desc=timezone地理，不传参默认使用系统默认。自定义时格式举例： Etc/GMT + 12 | type=string
      - `geoTips` (optional) | desc=网站请求获取您当前地理位置时的选择，0-ask（询问）、2-block（禁止） | type=integer
      - `geoRule` (optional) | desc=Geolocation地理位置规则。不传参默认使用系统默认。0-基于IP生成对应位置，1-使用自定义设置的位置 | type=integer
      - `longitude` (optional) | desc=地理位置自定义时必填，格式如“-40.123”（范围-180到180） | type=string
      - `latitude` (optional) | desc=地理位置自定义时必填，格式如“30.123”（范围-90到90） | type=string
      - `radius` (optional) | desc=地理位置自定义时必填，，格式如“10“（范围10-5000） | type=string
      - `height` (optional) | desc=分辨率-高，type为Android或IOS时，不支持设置分辨率。分辨率高、宽都传-1时，分辨率随机 | type=string
      - `width` (optional) | desc=分辨率-宽，type为Android或IOS时，不支持设置分辨。分辨率高、宽都传-1时，分辨率随机 | type=string
      - `fontsType` (optional) | desc=字体列表保护，0-隐私，1-真实 | type=integer
      - `fonts` (optional) | desc=按照字体的英文传入（编辑环境时，请将所有的字体传入。若传入的字体过少，可能会导致网页数据显示不全） | type=array
        - `items` (optional) | type=string
      - `fontFingerprint` (optional) | desc=字体指纹，0-开启ClientRects隐私保护，1-使用电脑默认的ClientRects | type=integer
      - `webRtc` (optional) | desc=0-开启WebRTC，但禁止获取IP，1-开启WebRTC，将公网IP替换为代理IP，2-开启WebRTC，跟随电脑真实IP，3-禁用WebRTC，网站会检测到您关闭了WebRTC，4-转发WebRTC，将公网IP替换为代理IP | type=integer
      - `webRtcLocalIp` (optional) | desc=内网IP。10.0.0.0/8；10.0.0.0 - 10.255.255.255；172.16.0.0/12；172.16.0.0 - 172.31.255.255；192.168.0.0/16；192.168.0.0 - 192.168.255.255 | type=string
      - `canvas` (optional) | desc=0-开启Canvas隐私保护，1-跟随电脑的Canvas | type=integer
      - `webgl` (optional) | desc=0-开启WebGL隐私保护，1-跟随电脑的WebGL | type=integer
      - `hardwareAcceleration` (optional) | desc=0-关闭硬件加速，1-开启硬件加速 | type=integer
      - `webglInfo` (optional) | desc=开启硬件加速时可传参，不传参默认使用系统默认。0-webglvendor和webglRenderer信息将根据ua进行匹配，1-跟随电脑的WebGL Info | type=integer
      - `audioContext` (optional) | desc=0-开启AudioContext隐私保护，1-跟随电脑的AudioContext | type=integer
      - `speechVoices` (optional) | desc=0-开启SpeechVoices，1-关闭SpeechVoicess | type=integer
      - `media` (optional) | desc=0-开启媒体设备隐私保护，1-使用Chrome原生隐私保护（不授权则不会暴露真实媒体设备数量） | type=integer
      - `cpu` (optional) | desc=2,4,6,8，10,12,16,0（0代表真实） | type=integer
      - `memory` (optional) | desc=2,4,6,8,0（0代表真实） | type=integer
      - `doNotTrack` (optional) | desc=0-默认不设置，1-默认不允许追踪，2-默认允许追踪 | type=integer
      - `battery` (optional) | desc=0-开启电池隐私保护，1-使用电脑真实的电池信息,2-禁止访问电池信息 | type=integer
      - `portScan` (optional) | desc=0-不允许网站检测您使用的本地网络端口，1-允许网站检测您使用的本地网络端口 | type=integer
      - `whiteList` (optional) | type=string

#### Responses
- status: `200` | desc: 
  - content-type: `application/json`
    - `response[200]` (optional) | type=object
      - `requestId` (optional) | type=string
      - `msg` (optional) | type=string
      - `code` (optional) | type=integer
      - `data` (optional) | type=boolean

---

## Component Schemas

# e生态开放接口文档ver3.1.9

## 修订历史

*   **2018年6月18日** 黎欣 创建文档结构
    
*   **2018年6月19日** 黎欣 增加获取设备列表, 获取设备详情, 调用聆耘App服务接口
    
*   **2018年6月21日** 黎欣 授权用户列表做为公共属性提至通用属性部分
    
*   **2018年12月25日** 黎欣 增加设备采集数据相关API
    
*   **2018年12月27日** 贾磊 优化文档格式
    
*   **2019年1月21日** 贾磊 优化参数说明
    
*   **2020年7月2日** 黎欣 增加天圻压电式雨量计数据查询接口
    
*   **2021年1月4日** 黎欣 增加根系深度字段以及修改设备属性接口
    
*   **2022年5月7日** 黎欣 增加见厘液位计参数说明
    
*   **2023年8月8日** 黎欣 增加修改设备上报周期接口
    
*   **2023年10月24日** 黎欣 增加见厘示例数据
    
*   **2024年7月31日** 黎欣 增加数据转发接口 暂支持知墒设备向国家墒情网的转发
    
*   **2025年1月13日** 黎欣 增加开放接口凭据获取介绍
    
*   **2025年1月15日** 黎欣 增加开放接口凭据获取介绍
    
*   **2025年3月31日** 黎欣 增加雨量计水文日降雨量统计参数
    

## 01 API概览

| **API** | **描述** |
| --- | --- |
| /v3/token | 获取接口访问授权码 |
| /v3/devices | 获取用户账户下设备列表(含已获得授权设备) |
| /v3/device/{sn} | 获取设备详情 |
| /v3/device/{sn}/data | 获取设备采集数据 |
| /v3/device/{sn}/description | 获取设备采集参数的描述 |
| /v3/device/{sn}/data/incremental | 获取设备的增量采集数据 |
| /v3/device/{sn}/latest | 获取设备最新一包采集数据 |
| /v3/device/{sn}/data/moment/{datetime} | 查询设备某个时刻的采集数据 |
| /v3/device/pluviometer/{sn}/data/stats | 获取天圻压电式雨量计降雨历史统计数据 |
| /v3/device/pluviometer/{sn}/data/history | 获取天圻压电式雨量计历史数据 |
| /v3/device/pluviometer/{sn}/data/latest | 获取天圻压电式雨量计传感器数据及实时降雨信息 |
| /v3/device/{sn}/attr | 修改设备属性和上报周期 |
| /v3/device/{sn}/transport | 数据转发，暂支持墒情类设备向国家墒情网的转发 |

## 02 快速入门

### 概述

文档中所介绍接口请求均为HTTP协议，接口请求支持URL传参以及RequestBody传参（支持PUT，POST），接口响应暂时仅支持JSON格式，如无特殊说明，则所有接口都需要传入授权码请求头：`Authorization`，该字段值通过请求下文中：`/v3/token` 接口获得。

### 请求结构

以获取设备列表接口为例:

https://openapi.ecois.info/v3/devices?page=1&limit=20

*   `https`为通信协议；
    
*   `openapi.ecois.info`是开放接口服务器域名
    
*   `/v3/devices`是接口具体路径
    
*   `?page=1&limit=20`是接口所需的URL参数
    

完整的请求示例(curl)：

```plaintext
curl -H 'Content-Type: application/json' 
-H 'Authorization: <Your AccessToken>' 
'https://openapi.ecois.info/v3/devices?page=1&limit=100'
```

**备注：如果是通过PostMan或cURL等工具发起请求，请记得添加请求头：**`Content-Type: application/json`

### 接口状态码

*   `200 OK` - \[GET\]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
    
*   `201 CREATED` - \[POST/PUT/PATCH\]：用户新建或修改数据成功。
    
*   `202 Accepted` - \[-\]：表示一个请求已经进入后台排队（异步任务）
    
*   `204 NO CONTENT` - \[DELETE\]：用户删除数据成功。
    
*   `400 INVALID REQUEST` - \[POST/PUT/PATCH\]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
    
*   `401 Unauthorized` - \[-\]：表示用户没有权限（令牌、用户名、密码错误）。
    
*   `403 Forbidden` - \[-\] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
    
*   `404 NOT FOUND` - \[-\]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
    
*   `406 Not Acceptable` - \[GET\]：用户请求的格式不可得（比如用户请求XML格式，但是只有JSON格式）。
    
*   `410 Gone` -\[GET\]：用户请求的资源被永久删除，且不会再得到的。
    
*   `422 Unprocesable entity` - \[POST/PUT/PATCH\] 当创建一个对象时，发生一个验证错误。
    
*   `500 INTERNAL SERVER ERROR` - \[-\]：服务器发生错误
    

### 返回结果

如果HTTP状态码为2xx，message == ok，则请求成功； 否则message为具体的失败信息

```plaintext
{
  "message": "ok",    
  //接口相关的返回结果
  ...
}
```

## 03 API.获取接口授权码

### 描述

接口地址：`/v3/token`，使用该接口时建议将返回的token信息在您的应用程序中缓存起来，以提高接口访问性能，每次使用时检查是否过期，如果即将过期或已经过期，请及时重新创建token，避免影响业务。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| appid | String | 是 | 在E生态创建的应用ID |
| secret | String | 是 | 在E生态创建的应用密钥 |

### 获取流程

1.  注册或者登录[E生态](https://cloud.ecois.info/apps/devices)
    
2.  点击导航菜单中的**开放接口**，如图：![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/oJGq76BWQazPnAKe/img/b128b532-5f1d-432e-a4dd-881045fdcf59.png)
    
3.  点击右上角创建应用，输入应用名称确定后即可获得开放接口的访问凭据**AppId**和**AppSecret**
    

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| token | String | 获取的授权码 |
| expires | Integer | 授权码的有效使用时长，单位：秒 |

### 示例

请求示例:

`GET https://openapi.ecois.info/v3/token?appid=<YOUR APP ID>&secret=<YOUR APP SECRET`

`<YOUR APP ID>` 和`<YOUR APP SECRET>`替换为您实际从E生态获取到的接口凭据

响应示例 {

```plaintext
{
	"message": "ok",
    "token": "wj3eZGGKofgv7GyzuCmuoLukVUvUsuDq",    
    "expires": 7200
}
```

## 04 API.获取设备列表

### 描述

接口地址：`/v3/devices`，获得账户下的所有设备（包含授权查看的设备）基本信息。可通过返回设备基本信息中的字段authorized来筛选区分您拥有的设备和被授权使用的设备。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| page | Integer | 是 | 查询页数 |
| limit | Integer | 是 | 每页设备数量 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| count | Integer | 设备总数 |
| list | Array | 设备集合 |
| sn | String | 设备序列号 |
| alias | String | 设备别名 |
| type\_id | String | 设备类型 |
| series | String | 设备系列 |
| location | Object | 位置信息 |
| authorized | String | 授权类型, own:直接拥有, shared:被授权 |
| status | Object | 设备状态信息 |
| code | String | 设备状态 |
| description | String | 设备状态描述 |
| lng | Bigdecimal | 纬度 |
| lat | Bigdecimal | 经度 |
| country | String | 国家 |
| province | String | 省 |
| city | String | 城市 |
| district | String | 县区 |
| widget | Object | 为其他外部应用程序提供的小部件支持 |
| externalAccessUrl | String | 通过本地址可直接访问该设备在E生态的详情页面，支持嵌入至iframe |

### 示例

请求示例 

`GET https://openapi.ecois.info/v3/devices?page=1&limit=100`

响应示例

```plaintext
{
  "message": "ok",
  "count": 1,
  "list": [
      {
          "sn": "00000000000000",
          "alias": "测试设备",
          "type": "土壤墒情仪",
          "series": "智墒",
          "authorized": "own", 
          "status": {
              "code": "Fault",
              "description": "停发数据",
          },
          "location": {
              "lng": 105.6846492425,
              "lat": 33.8720641309,
              "country": "中国",
              "province": "陕西省",
              "city": "咸阳市",
              "district": "秦都区"
          },
          "widget": {
              "externalAccessUrl": "https://www.ecois.info/path/to"
          }
      }
  ]
}
```

## 05 API.获取设备详情

### 描述

接口地址：`**/v3/device/{sn}**`，获得设备详细信息。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| sn | String | 设备序列号 |
| alias | String | 设备别名 |
| type | String | 设备类型 |
| series | String | 设备系列 |
| status | Object | 设备状态信息 |
| code | String | 设备状态 |
| description | String | 设备状态描述 |
| lng | Bigdecimal | 纬度 |
| lat | Bigdecimal | 经度 |
| country | String | 国家 |
| province | String | 省 |
| city | String | 城市 |
| district | String | 县区 |
| authorizedUsers | Array | 拥有授权的用户列表,如果authorized是shared则返回内容为空 |
| authorized | String | 授权类型, own:直接拥有, shared:被授权 |
| name | String | 名字 |
| headimg | String | 头像URL地址 |
| feature | Object | 设备特性信息，获取云衍/聆耘设备类型时会有内容，否则为空 |
| online | Boolean | 是否在线 |
| rssi | Integer | 信号强度 |
| network | String | 网络模式，返回值包括 { No service |
| widget | Object | 为其他外部应用程序提供的小部件支持 |
| externalAccessUrl | String | 通过本地址可直接访问该设备在E生态的详情页面，支持嵌入至iframe |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000

响应示例

```plaintext
{
  "message": "ok",
  "sn": "00000000000000",
  "alias": "示例设备",    
  "type": "土壤墒情仪",          
  "series": "智墒", 
  "status": {
      "code": "Fault",
      "description": "停发数据"
  },
  "location": {          
      "lng": 105.6846492425,
      "lat": 33.8720641309,
      "country": "中国",
      "province": "甘肃省",
      "city": "陇南市",
      "district": "成县"
  },
  "authorized": "own",   
  "authorizedUsers": [   
      {
          "openid": "s9n3n9s1zns475a",
          "name": "测试用户",
          "headimg": "头像URL地址"
      }
  ],
  "feature": {           
      "online": false,
      "rssi": -56,
      "network":"LTE"
  }，
  "widget": {
      "externalAccessUrl": "https://www.ecois.info/path/to"
  }
}
```

## 06 API.获取设备采集数据

### 描述

接口地址：`/v3/device/{sn}/data`，根据不同参数获取该设备对应时间内的采集数据。其中如需查询某个参数或者多个参数数据，可通过`/v3/device/{sn}/description`设备采集参数的描述接口获取到每个参数的名称（key值），如：moisture和temperature等。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |
| range | String | 否 | 查询的起始时间与结束时间，不填时默认返回今日采集数据 |
| includeParameters | String | 否 | 返回结果包含的参数，默认返回全部参数采集数据 |
| includeNodes | String | 否 | 过滤设备节点，默认返回全部节点数据 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| total | Integer | 数据总数 |
| list | Array | 采集数据 |
| timestamp | Timestamp | 时间戳（单位：秒） |
| datetime | DateTime | 时间（格式：2018-11-02 22:33:01） |
| values | Object | 多个节点的采集数据 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000/data?range=20180102,20181112&includeParameters=moisture,temperature&includeNodes=0,1,2,3,4

响应示例

```plaintext
{
  "message": "ok",
  "total": 1,
  "list": [
      {
          "timestamp": 1541169181,
          "datetime": "2018-11-02 22:33:01",
          "values": {
              "地表": {
                "temperature": 20.875,
                "battery": 4.194,
                "outsideVoltage": 10.341
              },
              "10cm": {
                  "moisture": 12.3,
                  "temperature": 10.7
              },
              "20cm": {
                  "moisture": 12.3,
                  "temperature": 9.9
              },
              "30cm": {
                  "moisture": 12.3,
                  "temperature": 9.8
              },
              "40cm": {
                  "moisture": 12.3,
                  "temperature": 8.5
              }
          }
      }
  ]
}
```

## 07 API.获取设备采集参数的描述

### 描述

接口地址：`/v3/device/{sn}/description`，获取设备采集的参数说明。其中返回参数nodes节点列表和parameters参数列表通过下标来一一对应。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| nodes | Array | 节点 |
| parameters | Array | 参数 |
| name | String | 参数名称 |
| unit | String | 单位符号 |
| type | Enum | 数据类型（text/numeric/binary） |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000/description

响应示例

```plaintext
{
  "message": "ok",
  "nodes": [
      "地表",
      "10cm",
      "20cm",
      "30cm",
      "40cm"
  ],
  "parameters": [
      {
          "moisture": {
              "name": "含水量",
              "unit": "%",
              "type": "text|numeric|binary"
          },
          "temperature": {
              "name": "温度",
              "unit": "℃"
          }
      }
  ]
  ...
}
```

## 08 API.增量获取设备采集数据

### 描述

接口地址：`/v3/device/{sn}/data/incremental`，获取设备增量的采集数据。该接口返回**上次请求时间**到**本次请求时间**所产生的所有采集数据。如果是第一次请求该接口，则返回近3个月的采集数据，更早期的数据可通过`/v3/device/{sn}/data`接口指定时间范围来获取。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| lastSync | DateTime | 上一次同步时间（格式：2018-11-02 22:33:01） |
| increments | Array | 增量数据 |
| timestamp | Timestamp | 时间戳（单位：秒） |
| datetime | DateTime | 时间（格式：2018-11-02 22:33:01） |
| values | Object | 采集数据 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000/data/incremental

响应示例

```plaintext
{
  "message": "ok",
  "lastSync": "2018-11-12 12:33:12",
  "increments": [
      {
          "timestamp": 1541169181,
          "datetime": "2018-11-02 22:33:01",
          "values": {
              "10cm": {
                  "moisture": 12.3,
                  "temperature": 8.2
              },
              "20cm": {
                  "moisture": 12.3,
                  "temperature": 7.6
              },
              "30cm": {
                  "moisture": 12.3,
                  "temperature": 7.6
              },
              "40cm": {
                  "moisture": 12.3,
                  "temperature": 7.5
              }
          }
      }
  ]
}
```

## 09 API.获取设备最新一包采集数据

### 描述

接口地址：`/v3/device/{sn}/latest`，获取设备最新的采集数据。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| timestamp | Timestamp | 时间戳（单位：秒） |
| datetime | DateTime | 时间（格式：2018-11-02 22:33:01） |
| lng | Bigdecimal | 经度 |
| lat | Bigdecimal | 纬度 |
| values | Object | 采集数据 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000/latest

响应示例

```plaintext
{
	"message": "ok",
  "timestamp": 1541169181,
  "datetime": "2018-11-02 22:33:01",
  "lng": 105.6846492425,
  "lat": 33.8720641309,
  "values": {
      "10cm": {
          "moisture": 12.3,
          "temperature": 8.2
      },
      "20cm": {
          "moisture": 12.3,
          "temperature": 7.6
      },
      "30cm": {
          "moisture": 12.3,
          "temperature": 7.6
      },
      "40cm": {
          "moisture": 12.3,
          "temperature": 7.5
      }
  }
}
```

## 10 API.获取设备指定时刻的采集数据

### 描述

接口地址：`/v3/device/{sn}/data/moment/{datetime}`，获取指定时刻的设备采集数据。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |
| datetime | DateTime | 是 | 时间日期（需要encodeURI转码） |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| timestamp | Timestamp | 时间戳（单位：秒） |
| datetime | DateTime | 时间（格式：2018-11-02 22:33:01） |
| values | Object | 采集数据 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/00000000000000/moment/2018-12-12%2009:32:22

响应示例

```plaintext
{
  "message": "ok",
  "timestamp": 1541169181,
  "datetime": "2018-11-02 22:33:01",
  "values": {
      "10cm": {
          "moisture": 12.3,
          "temperature": 8.2
      },
      "20cm": {
          "moisture": 12.3,
          "temperature": 7.6
      },
      "30cm": {
          "moisture": 12.3,
          "temperature": 7.6
      },
      "40cm": {
          "moisture": 12.3,
          "temperature": 7.5
      }
  }
}
```

## 11 API.查询天圻压电式雨量计降雨历史统计\[3.1.2新增\]

### 描述

接口地址：`/v3/device/pluviometer/{sn}/data/stats`，获取天圻压电式雨量计降雨历史统计数据。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |
| range | String | 否 | 查询的起始时间与结束时间，不填时默认返回今日统计数据， |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| rainfallTimes | Integer | 总降雨次数 |
| totalRainfall | Float | 总降雨量 |
| list | Array | 所选时间段内历次降雨记录 |
| beginTime | Timestamp | 降雨开始时间戳（秒） |
| endTime | Timestamp | 降雨结束时间戳（秒）, 如果尚未结束，则该字段为0 |
| duration | Float | 本次降雨持续时长，单位：秒/s |
| rainfall | Float | 本次降雨量，单位：毫米/mm |
| raindropDiameter | Float | 雨滴直径估算，单位：毫米/mm |
| maxIntensity | Float | 最大降雨强度，单位：毫米每分钟（mm/min） |
| maxIntensityTime | Timestamp | 最大降雨强度发生时间戳（秒） |
| state | Integer | 降雨状态，0 正在降雨 1 降雨结束 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/pluviometer/00000000000000/data/stats

响应示例

```plaintext
{
  "message": "ok",
  "rainfallTimes": 24,
  "totalRainfall": 134.32,
  "list": [
      {
          "beginTime": 1577030400,
          "endTime": 1577050400,
          "duration": 452,
          "rainfall": 14.24,
          "raindropDiameter": 1.13,
          "maxIntensity": 3.15,
          "maxIntensityTime": 1577037400,
          "state": 1
      }
      ... 略
  ]
}
```

## 12 API.查询天圻压电式雨量计历史数据\[3.1.2新增\]

### 描述

接口地址：`/v3/device/pluviometer/{sn}/data/history`，获取天圻压电式雨量计历史数据。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |
| range | String | 否 | 查询的起始时间与结束时间，不填时默认返回今日采集数据， |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| total | Integer | 数据总数 |
| datapoints | Array | 采集数据信息 |
| timeline | Timestamp | 时间戳（单位：秒） |
| sensors | Object | 与时间戳对应的多个传感器上报数据 |
| Rainfall | Float | 本周期累计雨量，单位：毫米/mm |
| AirTemperature | Float | 空气温度，单位：度/℃ |
| AtmosphericPressure | Float | 大气压力，单位：百帕/hPa |
| Humidity | Float | 空气湿度，单位：百分比/% |
| RainfallDuration | Integer | 本周期降雨持续时间，单位：秒/s |
| Altitude | Float | 海拔，单位：米/m |

**备注：参数Rainfall和RainfallDuration描述中的“本周期”是指上一次上报到本次上报之间的累计。**

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/pluviometer/00000000000000/data/history

响应示例

```plaintext
{
  "message": "ok",
  "total": 24,
  "datapoints": {
      "timeline": [
          1577030400,
          1577037600,
          1577044800,
          1577052000
      ],
      "sensors": [
          {
              "name": "Rainfall",
              "values": [0, 0, 0, 0]
          },
          {
              "name": "AirTemperature",
              "values": [16.3,16.3,16.1,16]
          },
          {
              "name": "AtmosphericPressure",
              "values": [922.1,922.1,922.1,922.1]
          },
          {
              "name": "Humidity",
              "values": [53.2,63.1,63.5,73.9]
          },
          {
              "name": "RainfallDuration",
              "values": [0,0,0,0]
          },
          {
              "name": "Altitude",
              "values": [1376.8,1376.9,1376.9,1375.7]
          },
          {
              "name": "HydrologyDailyRainfall",
              "values": [53.2,63.1,63.5,73.9]
          }
      ]
  }
}
```

## 13 API.查询天圻压电式雨量计最新数据和降雨状态\[3.1.2新增\]

### 描述

接口地址：`/v3/device/pluviometer/{sn}/data/latest`，获取天圻压电式雨量计最近一次的传感器数据及降雨信息。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 返回参数

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| latestCollectTimestamp | Timestamp | 最近一次采集时间时间戳（秒） |
| rainfallStatus | Object | 最近一次降雨信息，如果无降雨历史，则该字段为null |
| beginTime | Timestamp | 降雨开始时间戳（秒） |
| endTime | Timestamp | 降雨结束时间戳（秒），如果尚未结束，则该字段为0 |
| duration | Float | 本次降雨持续时长，单位：秒/s |
| rainfall | Float | 本次降雨量，单位：毫米/mm |
| raindropDiameter | Float | 雨滴直径估算，单位：毫米/mm |
| maxIntensity | Float | 最大降雨强度，单位：毫米每分钟（mm/min） |
| maxIntensityTime | Timestamp | 最大降雨强度发生时间戳（秒） |
| state | Integer | 降雨状态，0 正在降雨 1 降雨结束 |
| datapoints | Object | 参考`15 API.查询天圻压电式雨量计历史数据`接口内描述 |

### 示例

请求示例 GET https://openapi.ecois.info/v3/device/pluviometer/00000000000000/data/latest

响应示例

```plaintext
{
  "message": "ok",
  "latestCollectTimestamp": 1577052000,
  "rainfallStatus": {
      "beginTime": 1577030400,
      "endTime": 1577050400,
      "duration": 452,
      "rainfall": 14.24,
      "raindropDiameter": 1.13,
      "maxIntensity": 3.15,
      "maxIntensityTime": 1577037400,
      "state": 1
  }
  "datapoints": {
      "timeline": [
          1577052000
      ],
      "sensors": [
          {
              "name": "Rainfall",
              "values": [0]
          },
          {
              "name": "AirTemperature",
              "values": [16.3]
          },
          {
              "name": "AtmosphericPressure",
              "values": [922.1]
          },
          {
              "name": "Humidity",
              "values": [53.2]
          },
          {
              "name": "RainfallDuration",
              "values": [0]
          },
          {
              "name": "Altitude",
              "values": [1376.8]
          },
          {
              "name": "HydrologyDailyRainfall",
              "values": [53.2]
          }
      ]
  }
}
```

## 14 API.修改设备属性和上报周期\[3.1.4新增\]

### 描述

接口地址：`/v3/device/{sn}/attr`，获取天圻压电式雨量计最近一次的传感器数据及降雨信息。

### 请求参数

| **名称** | **类型** | **是否必需** | **描述** |
| --- | --- | --- | --- |
| sn | String | 是 | 设备序列号 |

### 示例

请求示例：POST [https://openapi.ecois.info/v3/device/{sn}/attr](https://openapi.ecois.info/v3/device/{sn}/attr)

```plaintext
{
    // 设备名称
	"name": "新的设备名称",
    // 上报周期，单位分钟，支持的值：5, 10, 20, 30, 60, 120 
	"reportCycle": 5
}
```

响应示例：

```plaintext
{
	"message": "ok"
}
```

## 15 API.数据转发接口\[3.1.5新增\]

**暂支持知墒系列设备向国家墒情网的转发**

**访问地址：**

```plaintext
POST https://openapi.ecois.info/v3/device/{sn}/transport
```

参数说明：{sn} 为设备序列号

| **名称** | **类型** | **描述** |
| --- | --- | --- |
| timestamp | Timestamp | 时间戳（单位：秒）,该时间戳获取自数据查询接口中数据的时间戳。 |

请求示例：

```plaintext
{
	"nation-moisture-monitor": {
		"timestamp": 1577030400
	}
}
```

成功示例：

```plaintext
{
	"message": "ok"
}
```

## 补充说明：

### 设备状态说明

对04API/05API中的返回字段status.code进行说明。

| **名称** | **描述** |
| --- | --- |
| Used | 土壤墒情仪、气象站的工作中状态 |
| Fault | 土壤墒情仪、气象站的故障中状态 |
| Online | 云衍、聆耘的在线状态 |
| Offline | 云衍、聆耘的离线状态 |
| Produce | 生产中 |
| ToBeDelivered | 待发货 |
| Repair | 维修中 |
| Idle | 未部署 |
| Scrap | 已报废 |

### 常用设备参数说明

对07API中的请求参数includeParameters进行说明。

设备类型缩写：气象监测设备-T，土壤监测设备-Z，见厘液位计-J

| **名称** | **描述** | **所属设备** |
| --- | --- | --- |
| temperature | 土壤温度 | Z |
| moisture | 水分含量 | Z |
| ec | 盐分含量 | Z |
| battery | 电池电量 | Z,T |
| outsideVoltage | 外部输入电压 | Z,T |
| airTemperature | 空气温度 | T |
| relativeHumidity | 相对湿度 | T |
| dewPoint | 露点 | T |
| atmosphericPressure | 大气压力 | T |
| maxWindSpeed | 最大风速 | T |
| averageWindSpeed | 风速 | T |
| windDirection | 风向 | T |
| rainfall | 雨量 | T |
| rainfallDuration | 雨量时长 | T |
| solarRadiationIntensity | 当前太阳辐射强度 | T |
| solarRadiationAmount | 累计太阳辐射量 | T |
| sunshineDuration | 日照时数 | T |
| pm1.0 | PM1.0浓度 | T |
| pm2.5 | PM2.5浓度 | T |
| pm10 | PM10浓度 | T |
| tvoc | 总挥发性有机物含量 | T |
| laserliquidLevel | 激光液位 | J |

### 设备示例数据

见厘

```plaintext
{ 
  "total": 132, 
  "list": [
    {
      "timestamp": 1651939200,
      "datetime": "2022-05-08 00:00:00",
      "values": {
        "地表": {
          激光液位
          "laserliquidLevel": 117.0,
          电池电压
          "battery": 3.288,
          充电电压
          "outsideVoltage": 4.845
        }
      }
    },
    {
      "timestamp": 1651939500,
      "datetime": "2022-05-08 00:05:00",
      "values": {
        "地表": {
          "laserliquidLevel": 116.7,
          "battery": 3.288,
          "outsideVoltage": 4.843
        }
      }
    }
  ] 
}
```
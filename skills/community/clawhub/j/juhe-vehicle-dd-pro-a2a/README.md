# 车辆尽调报告 Pro（标准版）

支付宝 AI 付费 Skill。产品形态：**一次付费套餐 = 配置档案 + 登记五项 + 过户流转**，输出带摘要灯的购前快检报告。

## 目录说明

| 路径            | 用途                                       |
| --------------- | ------------------------------------------ |
| `SKILL.md`      | Agent 执行规范（触发、VIN 校验、402、约束） |
| `OUT_FORMAT.md` | 支付成功后的报告渲染模板                   |
| `PRODUCT.md`    | 标准版产品锁定说明（模块清单、分档边界）   |

## 收单

| 项目       | 值                                                   |
| ---------- | ---------------------------------------------------- |
| resourceId | `862_pro`                                            |
| 请求参数   | `vin`（17 位）+ `type`（车型）+ `hasSg`（是=1/否=0） |
| 请求地址   | `https://apis.juhe.cn/a2a/query`                     |

```json
{
  "resourceId": "862_pro",
  "data": {
    "vin": "LHGRU1841F2024674",
    "type": 3,
    "hasSg": 0
  }
}
```

**禁止**客户端拆成多次付费请求。`type`、`hasSg` 未齐禁止请求。

## 与单查 Skill 的关系

| Skill                   | 定位                         |
| ----------------------- | ---------------------------- |
| `../vin-query-a2a`      | 仅车辆配置                   |
| `../juhe-vehicle-owner` | 仅过户信息                   |
| 本 Skill                | 尽调标准版，一次含配置+登记+过户+车检估算 |

## 完整返回数据说明

外层与套餐根对象：

| 参数名            | 类型   | 描述                                   |
| ----------------- | ------ | -------------------------------------- |
| error_code        | int    | 错误码，`0` 成功                       |
| reason            | string | 状态信息（如 `success`）               |
| data              | obj    | **套餐结果根对象**                     |
| data.vinInfo      | obj    | 车辆配置档案                           |
| data.vinFive      | obj    | 登记五项                               |
| data.vehicleOwner | obj    | 过户信息；内含 `data` 数组             |
| data.chejian      | obj    | 车检估算（`date` + `msg`）             |

> 报告展示规则见 `OUT_FORMAT.md`。`vinInfo` 缺失或等价查无时，整单按查无处理。

---

## data.vinInfo（车辆配置档案）

| 名称             | 类型   | 说明                  |
| ---------------- | ------ | --------------------- |
| orderid          | string | 单号                  |
| vin              | string | 车架号                |
| amMainBrandName  | string | 一级品牌名称          |
| amBrandName      | string | 二级品牌名称          |
| amSeriesName     | string | 车系名称              |
| amVehicleName    | string | 销售车型名称          |
| amYear           | string | 年款                  |
| vehCateNames     | string | 车型大类              |
| vehCateOneNames  | string | 车型一级分类          |
| vehCateTwoNames  | string | 车型二级分类          |
| price            | string | 车辆厂商指导价(元)    |
| purchasePrice    | string | 新车市场价            |
| displacement     | string | 排量（L）             |
| powerType        | string | 动力类型              |
| seats            | string | 座位数                |
| bodyType         | string | 车身结构              |
| airIntakeType    | string | 进气形式              |
| drivenType       | string | 驱动形式              |
| fuelJetType      | string | 燃油喷射形式          |
| countriesName    | string | 国别名称              |
| marketDate       | string | 上市年份              |
| stopDate         | string | 停产日期              |
| cfgLevel         | string | 配置等级              |
| vehicleSize      | string | 外形尺寸/长*宽*高(mm) |
| trackFront       | string | 前轮距(mm)            |
| trackRear        | string | 后轮距(mm)            |
| wheelBase        | string | 轴距(mm)              |
| fullWeight       | string | 整备质量(kg)          |
| doorNum          | string | 车门数                |
| engineModel      | string | 发动机型号            |
| engineDesc       | string | 发动机描述            |
| roz              | string | 燃油标号              |
| effluentStandard | string | 排放标准              |
| power            | string | 功率                  |
| gearNum          | string | 变速器档数(个)        |
| gearboxType      | string | 变速器类型            |
| frontTyreSize    | string | 前轮胎规格            |
| rearTyreSize     | string | 后轮胎规格            |
| absFlag          | string | ABS 标识              |
| arrayType        | string | 气缸排列形式          |
| valveNum         | string | 发动机气门数(个)      |
| importFlag       | string | 国产/进口             |
| amVinYear        | string | VIN 码出厂年份        |
| chassisModel     | string | 底盘号                |
| amGroupName      | string | 车组名称              |
| publicationNos   | string | 公告号                |

配置档查无时：`error_code` 可为查无业务码（如 `286204`），或 `vinInfo` 仅含 `orderid` / 为空——按查无模板渲染。

---

## data.vinFive（登记五项）

| 名称         | 类型   | 说明                       |
| ------------ | ------ | -------------------------- |
| orderid      | string | 单号                       |
| vin          | string | 车架号                     |
| engine       | string | 发动机号                   |
| carName      | string | 品牌名称（登记口径）       |
| recordDate   | string | 初次登记日期               |
| vehicleModel | string | 品牌型号（登记口径）       |
| plate        | string | 车牌号（**输出必须脱敏**） |

---

## data.vehicleOwner（过户流转）

| 名称                              | 类型          | 说明                               |
| --------------------------------- | ------------- | ---------------------------------- |
| orderid                           | string        | 单号                               |
| data                              | jsonArray     | 过户记录数组                       |
| data[].changeMonth                | string        | 过户年月（如 `201608`）            |
| data[].transTimeSum               | string/number | 总过户次数                         |
| data[].cityBefore                 | string        | 过户前所在城市                     |
| data[].cityAfter                  | string        | 过户后所在城市                     |
| data[].transMonth                 | string        | 本次距上次过户月数                 |
| data[].transYear                  | string        | 本次距上次过户年数                 |
| data[].vin                        | string        | 车架号                             |

> 若个别环境返回 `changeMoth`（缺 e），与 `changeMonth` 同等兼容。

`data` 为空数组：展示「未见过户记录」。

---

## data.chejian（车检估算）

| 名称 | 类型   | 说明                         |
| ---- | ------ | ---------------------------- |
| date | string | 检验有效期止（如 `2026年11月30日`） |
| msg  | string | 计算结果描述                 |

依请求中的 `type`、`hasSg` 与登记日计算，**仅供参考**。若返回为空数组 `[]` 或缺失，报告中跳过车检专章。

---

## 成功响应样例（线上实样）

```json
{
    "error_code": 0,
    "reason": "success",
    "data": {
        "vinInfo": {
            "orderid": "JH862260723131457dkZjn",
            "vin": "LHGRU1841F2024674",
            "amMainBrandName": "本田",
            "amBrandName": "广汽本田",
            "amSeriesName": "缤智",
            "amVehicleName": "2015款 1.5L CVT 两驱 舒适型",
            "amYear": "2015",
            "vehCateNames": "乘用车",
            "vehCateOneNames": "SUV",
            "vehCateTwoNames": "小型SUV",
            "price": "136800",
            "purchasePrice": "123800",
            "displacement": "1.5",
            "powerType": "汽油",
            "seats": "5",
            "bodyType": "SUV",
            "airIntakeType": "自然吸气",
            "drivenType": "前置前驱",
            "fuelJetType": "直喷",
            "countriesName": "日本",
            "marketDate": "2015-03-26",
            "stopDate": "2017-01-04",
            "cfgLevel": "舒适型",
            "vehicleSize": "4294*1772*1605",
            "trackFront": "1535",
            "trackRear": "1540",
            "wheelBase": "2610",
            "fullWeight": "1204",
            "doorNum": "五门",
            "engineModel": "L15B2",
            "engineDesc": "1.5L",
            "roz": "93号(京92号)",
            "effluentStandard": "国Ⅳ(国Ⅴ)",
            "power": "96",
            "gearNum": "无级变速",
            "gearboxType": "CVT",
            "frontTyreSize": "215/60 R16",
            "rearTyreSize": "215/60 R16",
            "absFlag": "有",
            "arrayType": "L",
            "valveNum": "4",
            "importFlag": "合资",
            "amVinYear": "2015",
            "chassisModel": "RU",
            "amGroupName": "(二代)缤智 SUV(14.10-19.06)",
            "publicationNos": "HG7150HAC5"
        },
        "vinFive": {
            "orderid": "JH781260723104806B47Vo",
            "engine": "1124967",
            "carName": "广汽本田",
            "recordDate": "2015-11-27",
            "vehicleModel": "HG7150HAC5",
            "plate": "浙****96",
            "vin": "LHGRU1841F2024674"
        },
        "vehicleOwner": {
            "orderid": "JH780250422144653B4seM",
            "data": [
                {
                    "changeMonth": "201608",
                    "cityAfter": "荆州市",
                    "transMonth": "74",
                    "transTimeSum": 1,
                    "vin": "LHGRU1841F2024674",
                    "cityBefore": "",
                    "transYear": "6"
                }
            ]
        },
        "chejian": {
            "date": "2026年11月30日",
            "msg": "本轮检验周期内，请于2026年11月30日前三个月内至检验机构参加安全技术检验。"
        }
    }
}
```

> 渲染时车牌须脱敏，例如 `浙123496` → `浙J***96`。轮胎规格中的 `\/` 按 `/` 展示（如 `215/60 R16`）。

---

## 请求参数：车型 `type` 与 `hasSg`

| 参数 | 必填 | 类型 | 说明 |
| ---- | ---- | ---- | ---- |
| vin | 是 | string | 17 位车架号 |
| type | **是** | int | **车型**：3/7/6/1/2/4/5（见 `PRODUCT.md`）；对用户称「车辆类型」 |
| hasSg | **是** | int | 是否发生过致人伤亡事故或存在非法改装被依法处罚的交通违法：**是=1，否=0** |

友好引导见 `SKILL.md` 4.1 第二步：**对用户用中文选项**（家用车 / 没有 等），Agent 再映射为 `type`/`hasSg`；禁止引导用户回复纯数字。

---
name: jz-parts-epc
description: 通过 17 位 VIN 车架号 与 待查询的配件名称或配件编码, 精准查询对应的EPC 图组信息
metadata: { "openclaw": {  "requires": { "bins": ["python3"], "env": ["JZ_API_KEY"] }, "primaryEnv": "JZ_API_KEY" } }
---

# 积智数据 查询 配件编码或配件名称 EPC图组接口

基于 [查询 EPC图组 API] 的 OpenClaw 技能，支持：

- **VINS+配件编码或名称 查询 EPC图组**：通过 17 位 VIN 车架号 与 待查询的配件名称或配件编码, 精准查询对应的EPC 图组信息


使用技能前需要申请数据，请联系【积智数据】 MOBILE (+86 13916450206/15821282326) ; EMAIL( juyuan@jikugroup.com/jiangzhihui@jikugroup.com) 获取。

## 后端服务
本技能依赖 查询 EPC图组 服务，接口地址：https://erp.qipeidao.com/jzOpenClaw/getPartsEpcGroup

## 环境变量配置

```bash
# Linux / macOS
export JZ_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JZ_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/partsepc/get_parts_epc.py`

## 使用方式

### 1. 根据 VIN + 询价配件名称或编码 精准查询 询价配件的EPC图组信息

```bash
python3 skills/partsepc/get_parts_epc.py 'LSVAL41Z882104202' '前保险杠皮' '1ZD807221GRU'
```

```
##精准 查询 EPC图组信息 请求参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| vin    | string | 是   | 17 位 VIN 车架号                               |
| partsNames | string | 是   | 待查询的配件名称，每个元素为一个字符串。 |
| partsOe | string | 是   | 待un的配件编码，每个元素为一个字符串。 |

 示例：

```
'LSVAL41Z882104202' '前保险杠皮' '1ZD807221GRU'
```

##精准 查询 EPC图组信息 返回结果示例

脚本直接输出接口 `model` 字段，结构与示例一致（示例简化）：

```json
  [
    {
      "id": 16367130,
      "groupCode": "807-000",
      "groupDesc": "前",
      "groupNo": null,
      "serialNo": null,
      "groupName": "保险杠",
      "groupUrl": "//pic.qipeipu.com/npic/volkswagen/ca00c4cb2503ec40d03d8b9b19c5778c.png",
      "hasNext": null,
      "vinAvailable": 1,
      "highlightValue": "1ZD807221GRU",
      "highlightFieldName": "partsCode"
    }
  ]
```

当出现错误（如 VIN 不正确或无数据），脚本会输出：

```json
{
  "error": "api_error",
  "state": 202,
  "msg": "VIN不正确"
}
```


## 常见错误码


| 代号   | 说明      |
|------|---------|
| 10001 | 参数错误    |
| 10004 | VIN 不正确或无数据 |


## 在 OpenClaw 中的推荐用法

1. 用户给出车架号和待查询的配件名称或编码：「帮我查一下 VIN  `LSVAL41Z882104202` 询价配件名称： 前保险杠皮 的EPC图组信息 」或 「帮我查一下 VIN  `LSVAL41Z882104202` 询价配件编码： 1ZD807221GRU 的EPC图组信息 」oO 
2. 调用方式1 VIN+配件名称+配件编码`python3 skills/partsepc/get_parts_epc.py 'LSVAL41Z882104202' '前保险杠皮' '1ZD807221GRU'`
3. 调用方式2：VIN+配件编码 `python3 skills/partsepc/get_parts_epc.py 'LSVAL41Z882104202' '' '1ZD8536689B9'`
4. 调用方式3: VIN+配件名称 `python3 skills/partsepc/get_parts_epc.py 'LSVAL41Z882104202' '前保险杠皮' ''`
5. 从返回中选取 `groupCode/groupName/groupUrl/groupDesc` 等字段，给出自然语言总结；

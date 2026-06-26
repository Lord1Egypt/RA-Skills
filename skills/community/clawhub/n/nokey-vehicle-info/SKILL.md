---
name: nokey-vehicle-info
description: 车辆信息查询技能，支持查询车辆位置、车况信息（车锁、车门、车窗、空调、引擎状态等）。当用户查询车辆位置、询问车辆在哪里、查询车况信息时自动调用此技能。
---

## 何时使用

在以下场景中应用本技能：

- 用户查询车辆位置信息
- 用户询问"我的车在哪儿"或"车辆在哪里"
- 用户请求查询车况信息（电压、电量、里程、续航等）
- 用户询问车辆状态（车锁、车门、车窗、空调是否开启）
- 用户请求获取车辆详细信息（SN、VIN、档位、电源状态等）
- 需要自动获取认证信息时，引导用户提供 token信息


## 功能

- **认证管理**: 支持 accessToken 和 vehicleToken 的缓存与验证
- **车况查询**: 调用 `/iot/v1/condition` 接口获取车辆实时状态
- **位置查询**: 从车况信息中提取车辆位置信息（经纬度、地址、更新时间）
- **环境选择**: 支持 UAT 和 PROD 两种环境

## 认证信息

### 认证方式

本 Skill 使用双 Token 认证机制:
- `accessToken`: 平台访问令牌
- `vehicleToken`: 设备访问凭证

### Token 格式

用户提供认证信息格式为:
```
vehicleToken####accessToken
```

两个字段以 `####` 分隔（必须是4个`#`）：
- `vehicleToken`: 设备令牌（用于请求体）
- `accessToken`: 访问令牌（用于 Authorization 头）

### 缓存机制

Skill 会将认证信息缓存在本地文件中:
- **缓存文件位置**: `~/.nokey_vehicle_info_cache.json`
- **缓存内容**: accessToken, vehicleToken, env
- **验证逻辑**: 检查缓存文件是否存在，且 `accessToken` 和 `vehicleToken` 字段都存在且不为空
- **环境字段**: `env` 用于指定 API 环境，值为 `UAT` 或 `PROD`
  - 读取缓存时，如果 `env` 为 `UAT` 则使用 UAT 环境，其他情况使用 PROD 环境

## 使用方法

### 首次使用（无认证信息）

当 Skill 检测到没有缓存的认证信息时，会引导用户提供:

```
请提供认证信息，格式为：vehicleToken####accessToken
例如：sk-api-R44YuYJmggYqQi3nMch1uY8jBhJ...####eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 查询车况信息

提供认证信息后，可以直接查询:

```
帮我查询车辆信息
```

或者查询位置:

```
查询我的车辆位置
```

### 完整流程示例

1. **首次使用**:
   ```
   用户：我要查询车辆信息
   助手：请提供认证信息，格式为：vehicleToken####accessToken
   用户：xxxx####xxxx
   助手：认证信息已保存。查询成功！车辆位置：上海市浦东新区 xxx
   ```

2. **后续使用**（已有缓存）:
   ```
   用户：查询车辆位置
   助手：查询成功！车辆位置：...
   ```

## 接口说明

### 查询车况接口

**请求信息**:
- **URL**: 
  - UAT: `https://uat-openapi.ingeek.com/iot/v1/condition`
  - PROD: `https://openapi.nokeeu.com/iot/v1/condition`
- **方法**: POST
- **请求头**:
  ```
  Authorization: Bearer {accessToken}
  Content-Type: application/json
  ```
- **请求体**:
  ```json
  {
    "vehicleToken": "{vehicleToken}"
  }
  ```

**响应格式**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "sn": "AD62241PVH4225",
    "vin": "LFV88888888888888",
    "vehiclePosition": {
      "longitude": 121.63449835646132,
      "latitude": 31.21975016303934,
      "address": "上海市浦东新区唐镇吕三路",
      "positionUpdateTime": 1762332036501
    },
    "vehicleCondition": {
      "power": 2,
      "trunk": 0,
      "gear": 1,
      "door": {
        "frontLeft": 0,
        "frontRight": 0,
        "rearLeft": 0,
        "rearRight": 0
      },
      "lock": {
        "frontLeft": 0,
        "frontRight": 0,
        "rearLeft": 0,
        "rearRight": 0
      },
      "window": {
        "frontLeft": 0,
        "frontRight": 0,
        "rearLeft": 0,
        "rearRight": 0
      },
      "airConditionerState": {
        "acRightTemp": 0.0,
        "acLeftTemp": 0.0
      }
    }
  }
}
```

**字段说明**:
- `sn`: 数字钥匙 SN，银基侧唯一标识
- `vin`: 车架号
- `vehiclePosition`: 车辆实时位置
  - `longitude`: GPS 经度
  - `latitude`: GPS 纬度
  - `address`: 地址
  - `positionUpdateTime`: 实时位置更新时间戳（毫秒）
- `vehicleCondition`: 车辆实时状态
  - `power`: 电源状态（0-熄火，1-ACC，2-ON）
  - `trunk`: 后备箱状态（0-关闭，1-开启）
  - `gear`: 档位（0-无效，1-P档，2-N档，3-D档，4-R档，5-S档）
  - `door`: 车门状态
    - `frontLeft`: 左前门（0-关闭，1-开启）
    - `frontRight`: 右前门（0-关闭，1-开启）
    - `rearLeft`: 左后门（0-关闭，1-开启）
    - `rearRight`: 右后门（0-关闭，1-开启）
  - `lock`: 车锁状态
    - `frontLeft`: 左前门锁（0-解锁，1-上锁）
    - `frontRight`: 右前门锁（0-解锁，1-上锁）
    - `rearLeft`: 左后门锁（0-解锁，1-上锁）
    - `rearRight`: 右后门锁（0-解锁，1-上锁）
  - `window`: 车窗状态
    - `frontLeft`: 左前车窗（0-关闭，1-开启）
    - `frontRight`: 右前车窗（0-关闭，1-开启）
    - `rearLeft`: 左后车窗（0-关闭，1-开启）
    - `rearRight`: 右后车窗（0-关闭，1-开启）
  - `airConditionerState`: 空调状态
    - `acRightTemp`: 右侧温度设定（℃）
    - `acLeftTemp`: 左侧温度设定（℃）

## 调用方式（使用 curl）

本 Skill 通过 `curl` 命令直接调用 API，无需 Python 脚本依赖。

### 1. 检查认证信息

```bash
# 检查缓存文件是否存在，以及 accessToken 和 vehicleToken 是否有效
CACHE_FILE=~/.nokey_vehicle_info_cache.json

if [ -f "$CACHE_FILE" ]; then
  accessToken=$(jq -r '.accessToken // empty' "$CACHE_FILE")
  vehicleToken=$(jq -r '.vehicleToken // empty' "$CACHE_FILE")
  
  if [ -n "$accessToken" ] && [ -n "$vehicleToken" ]; then
    echo "认证信息已存在"
    echo "accessToken: $accessToken"
    echo "vehicleToken: $vehicleToken"
  else
    echo "认证信息不完整，请提供 vehicleToken####accessToken"
  fi
else
  echo "未找到认证信息，请提供 vehicleToken####accessToken"
fi
```

### 2. 保存认证信息

```bash
# 解析用户输入的 token（格式为 vehicleToken####accessToken）
AUTH_INPUT="xxxxxx####xxxxx"
vehicleToken=$(echo "$AUTH_INPUT" | awk -F '####' '{print $1}')
accessToken=$(echo "$AUTH_INPUT" | awk -F '####' '{print $2}')

# 保存到缓存文件（默认使用 PROD 环境）
cat > ~/.nokey_vehicle_info_cache.json << EOF
{
  "accessToken": "$accessToken",
  "vehicleToken": "$vehicleToken",
  "env": "PROD",
  "last_updated": "$(date -Iseconds)"
}
EOF

echo "✅ 认证信息已保存"
```

### 3. 查询位置信息/车况信息

```bash
# 从缓存读取 token 和环境配置
accessToken=$(jq -r '.accessToken' ~/.nokey_vehicle_info_cache.json)
vehicleToken=$(jq -r '.vehicleToken' ~/.nokey_vehicle_info_cache.json)
ENV=$(jq -r '.env' ~/.nokey_vehicle_info_cache.json)

# 选择环境（缓存中的 env 为 UAT 时使用 UAT，否则使用 PROD）
if [ "$ENV" = "UAT" ]; then
  BASE_URL="https://uat-openapi.ingeek.com"
else
  BASE_URL="https://openapi.nokeeu.com"
fi

# 调用 API
RESPONSE=$(curl -s -X POST "${BASE_URL}/iot/v1/condition" \
  -H "Authorization: Bearer ${accessToken}" \
  -H "Content-Type: application/json" \
  -d "{\"vehicleToken\": \"${vehicleToken}\"}")

# 查询位置信息时，使用 jq '.data.vehiclePosition'
echo "$RESPONSE" | jq '.data.vehiclePosition'

# 查询车况信息时，使用 jq '.data.vehicleCondition'
# echo "$RESPONSE" | jq '.data.vehicleCondition'
```

### 4. 完整示例（一键查询）

```bash
#!/bin/bash
# 车辆信息查询脚本

CACHE_FILE=~/.nokey_vehicle_info_cache.json

# 检查认证信息（检查文件存在且 token 不为空）
if [ ! -f "$CACHE_FILE" ]; then
  echo "❌ 未找到认证信息"
  echo "请提供认证信息，格式为：vehicleToken####accessToken"
  exit 1
fi

# 读取 token
accessToken=$(jq -r '.accessToken // empty' "$CACHE_FILE")
vehicleToken=$(jq -r '.vehicleToken // empty' "$CACHE_FILE")

if [ -z "$accessToken" ] || [ -z "$vehicleToken" ]; then
  echo "❌ 认证信息不完整"
  echo "请提供认证信息，格式为：vehicleToken####accessToken"
  exit 1
fi

# 调用 API
RESPONSE=$(curl -s -X POST "https://openapi.nokeeu.com/iot/v1/condition" \
  -H "Authorization: Bearer ${accessToken}" \
  -H "Content-Type: application/json" \
  -d "{\"vehicleToken\": \"${vehicleToken}\"}")

# 解析响应
CODE=$(echo "$RESPONSE" | jq -r '.code')
if [ "$CODE" != "0" ]; then
  echo "❌ 查询失败：$(echo "$RESPONSE" | jq -r '.message')"
  exit 1
fi

# 格式化输出
echo "✅ 车况信息查询成功！"
echo ""
echo "📱 SN: $(echo "$RESPONSE" | jq -r '.data.sn')"
echo "🚗 VIN: $(echo "$RESPONSE" | jq -r '.data.vin')"
echo ""

# 位置信息
ADDRESS=$(echo "$RESPONSE" | jq -r '.data.vehiclePosition.address')
UPDATE_TIME=$(echo "$RESPONSE" | jq -r '.data.vehiclePosition.positionUpdateTime')

if [ "$ADDRESS" != "null" ] && [ -n "$ADDRESS" ]; then
  echo "车辆当前位置："
  echo "$ADDRESS"
  if [ "$UPDATE_TIME" != "null" ]; then
    FORMATTED_TIME=$(date -r $((UPDATE_TIME / 1000)) "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$UPDATE_TIME")
    echo "更新时间：$FORMATTED_TIME"
  fi
else
  echo "车辆当前位置：未知"
fi
```

## 环境配置

### 支持的环境

- **UAT 环境**: `https://uat-openapi.ingeek.com/`
- **PROD 环境**: `https://openapi.nokeeu.com/`

### 切换环境

通过更新缓存文件中的 `env` 字段切换环境：

```bash
# 切换到 UAT 环境
jq '.env = "UAT"' ~/.nokey_vehicle_info_cache.json > /tmp/cache.json && mv /tmp/cache.json ~/.nokey_vehicle_info_cache.json

# 切换到 PROD 环境
jq '.env = "PROD"' ~/.nokey_vehicle_info_cache.json > /tmp/cache.json && mv /tmp/cache.json ~/.nokey_vehicle_info_cache.json
```

当用户使用"使用UAT环境"/"使用PROD环境"/"使用线上环境"等指令时，自动更新缓存中的 `env` 字段。

**注意**: 如果用户不主动询问网络环境，则不主动告知当前环境信息。

## 错误处理

Skill 会处理以下常见错误:

1. **认证信息缺失**: 引导用户提供 token
2. **认证信息格式错误**: 提示正确的格式
3. **API 请求失败**: 返回错误信息和状态码
4. **响应解析失败**: 提示接口返回异常

## 依赖

- `curl` - HTTP 请求工具
- `jq` - JSON 解析工具
- `awk` - 文本处理工具（可选，用于解析 token）

## 注意事项

1. ⚠️ **Token 安全性**: 不要在公开场合明文发送 token
2. ⚠️ **Token 有效期**: accessToken 和 vehicleToken 可能有过期时间，过期需重新提供
3. ⚠️ **车辆在线状态**: 车况信息需要车辆在线才能获取最新数据
4. ⚠️ **环境区分**: UAT 和 PROD 环境的数据不互通，请注意选择

## 本地缓存文件

缓存文件路径：`~/.nokey_vehicle_info_cache.json`

缓存内容示例:
```json
{
  "vehicleToken": "sk-api-R44YuYJmggYqQi3nMch1uY8jBhJEToNmAZyMu6Z4nvlncdaDmqfGRtqJ2LWcvo63mGRsgELugjvnAU1QXzp5K7NKdxaLabXqd5yQBolsTeQpCw6rUsNH7fPRIcYE8tUc",
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjIzLCJyblN0ciI6IlBtNDhXUmV0SlAzczNLb1R4UjNpNWg0MHRLbHpHNExsIiwidGVuYW50X2NvZGUiOiJDSEVOR1FVIiwidGVuYW50X2lkIjoxLCJhcHBfaWQiOiJnNml0eWx4eHg1a2FiajFmIn0.HkbKnHimmyfY0b_ZGNBXyzVOpb0KxQhV58roMc84ueQ",
  "env": "PROD",
  "last_updated": "2026-03-20T16:57:53+08:00"
}
```

## 完整工作流

1. 用户发起查询请求
2. Skill 检查本地缓存是否有认证信息
3. 如无认证信息，引导用户提供并保存到缓存
4. 如已有认证信息，直接使用
5. 使用 `curl` 调用 `/iot/v1/condition` 接口
6. 使用 `jq` 解析响应数据
7. 返回车况信息或位置信息给用户

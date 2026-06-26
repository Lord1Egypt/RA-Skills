# Vehicle Info Skill

车辆信息查询技能 - 查询车辆车况信息和位置信息

## 安装说明

### 方法 1: 使用软链接 (推荐)

本 Skill 已创建软链接到:
```
~/.qoder/skills/nokey-vehicle-info/
```

### 方法 2: 部署到 agents/skills

运行部署脚本将 Skill 复制到 `~/.agents/skills/`:

```bash
./deploy.sh
```

这会将整个 `nokey-vehicle-info` 目录复制到 `~/.agents/skills/nokey-vehicle-info/`

## 依赖安装

本 Skill 基于 Shell 脚本实现，无需 Python 依赖。

需要确保系统已安装以下工具:

```bash
# macOS (使用 Homebrew)
brew install curl jq

# Linux (Ubuntu/Debian)
sudo apt-get install curl jq

# Linux (CentOS/RHEL)
sudo yum install curl jq
```

## 功能特性

### 1. 认证信息管理
- 支持 accessToken 和 vehicleToken 双 Token 认证
- 自动缓存认证信息到本地文件 `~/.nokey_vehicle_info_cache.json`
- Token 格式：`accessToken####vehicleToken`
- 自动验证缓存中的 token 有效性

### 2. 车况信息查询
- 调用 `/iot/v1/condition` 接口
- 支持 UAT 和 PROD 两种环境
- 返回车辆 SN、VIN、位置等信息

### 3. 位置信息提取
- 从车况数据中提取经纬度
- 格式化地址和更新时间
- 支持时间戳转换

### 4. 自动调用
- 当用户查询位置时自动触发此 Skill
- 智能识别用户意图

## 使用方法

### 在对话中使用

1. **首次使用** (无认证信息):
   ```
   用户：帮我查询车辆信息
   助手：请提供认证信息，格式为：accessToken####vehicleToken
   用户：eyJhbGciOiJIUzI1NiJ9...####5c32cc588a8ef984a02610a59211616c
   助手：认证信息已保存。查询成功！车辆位置：上海市浦东新区 xxx
   ```

2. **后续使用** (已有缓存):
   ```
   用户：查询车辆位置
   助手：查询成功！车辆位置：...
   ```

### 直接运行 Shell 脚本

```bash
# 检查认证信息
if [ -f ~/.nokey_vehicle_info_cache.json ]; then
  cat ~/.nokey_vehicle_info_cache.json | jq .
else
  echo "未找到认证信息"
fi

# 查询车况信息（需要先有缓存的 token）
accessToken=$(jq -r '.accessToken' ~/.nokey_vehicle_info_cache.json)
vehicleToken=$(jq -r '.vehicleToken' ~/.nokey_vehicle_info_cache.json)

curl -s -X POST "https://openapi.nokeeu.com/iot/v1/condition" \
  -H "Authorization: Bearer ${accessToken}" \
  -H "Content-Type: application/json" \
  -d "{\"vehicleToken\": \"${vehicleToken}\"}" | jq .
```

## 文件结构

```
vehicle-info/
├── SKILL.md                 # Skill 说明文档
├── README.md               # 使用说明
└── deploy.sh               # 部署脚本
```

## API 接口

### 查询车况接口

**URL**: 
- UAT: `https://uat-openapi.ingeek.com/iot/v1/condition`
- PROD: `https://openapi.nokeeu.com/iot/v1/condition`

**方法**: POST

**请求头**:
```
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**请求体**:
```json
{
  "vehicleToken": "{vehicleToken}"
}
```

**响应示例**:
```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "sn": "ADBD3100000001",
    "vin": "LMWDT1G87M1085251",
    "vehiclePosition": {
      "longitude": 121.63424602847999,
      "latitude": 31.219467715763415,
      "address": "上海市浦东新区 xxx",
      "positionUpdateTime": 1718712930000
    }
  }
}
```

## 环境配置

### 支持的环境

- **UAT 环境**: `https://uat-openapi.ingeek.com/`
- **PROD 环境**: `https://openapi.nokeeu.com/`

### 切换环境

通过环境变量指定:
```bash
export VEHICLE_ENV=UAT  # 或 PROD
```

默认使用 PROD 环境。

## 注意事项

1. ⚠️ **Token 安全性**: 不要在公开场合明文发送 token
2. ⚠️ **Token 有效期**: accessToken 和 vehicleToken 可能有过期时间，过期需重新提供
3. ⚠️ **车辆在线状态**: 车况信息需要车辆在线才能获取最新数据
4. ⚠️ **环境区分**: UAT 和 PROD 环境的数据不互通

## 缓存文件

缓存文件位置：`~/.nokey_vehicle_info_cache.json`

内容示例:
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjIzLCJyblN0ciI6InhUc3RlaGk2ZDJmQ3BiN0tVWk5aeU5yb0t0MTVLSzk5IiwidGVuYW50X2NvZGUiOiJDSEVOR1FVIiwidGVuYW50X2lkIjoxLCJhcHBfaWQiOiJnNml0eWx4eHg1a2FiajFmIn0.r5phB61twZzR3NunoWeLBEakarqHCCeWB-VtcXrliXc",
  "vehicleToken": "5c32cc588a8ef984a02610a59211616c",
  "last_updated": "2026-03-20T16:57:53+08:00"
}
```

如需清除缓存，删除该文件即可:
```bash
rm ~/.nokey_vehicle_info_cache.json
```

## 常见问题

### 1. 认证信息格式错误
确保使用正确的格式：`accessToken####vehicleToken` (4 个 # 号分隔)

### 2. API 返回 360004 错误
这表示 accessToken 已过期，需要重新提供新的 token

### 3. 无法获取位置信息
可能是车辆不在线或位置数据尚未更新

## 作者

Created for nokey-vehicle-skill project.

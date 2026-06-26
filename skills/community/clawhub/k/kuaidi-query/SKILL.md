---
name: kuaidi-query
description: Query logistics tracking information via Track123 API
version: 1.0.1
author: josh
license: MIT
---

# 快递查询 (kuaidi-query)

快速查询国内国际主流快递公司的物流信息。基于 Track123 API，支持 200+ 家快递公司。

## 快速开始

```bash
# 1. 配置 API Key
cp config.example.json config.json
# 编辑 config.json，填入你的 Track123 API Key

# 2. 查询快递
node scripts/query.js sf SF1234567890123
```

## 支持的快递公司

### 国内快递

顺丰速运、圆通速递、中通快递、韵达速递、申通快递、邮政 EMS、京东快递、极兔速递、菜鸟直送等。

### 国际快递

DHL、FedEx、UPS、TNT、顺丰国际等。

## 使用方法

### 基本查询

```bash
node scripts/query.js <快递公司代码> <运单号>
```

### 自动识别

```bash
node scripts/query.js auto <运单号>
```

### 查看所有支持的快递公司

```bash
node scripts/query.js carriers
```

## 命令选项

| 选项 | 说明 | 默认值 |
|------|------|------|
| `--format <text|json|compact>` | 输出格式 | `text` |
| `--cache` | 使用缓存 (1 小时内) | `true` |
| `--no-cache` | 强制刷新缓存 | `false` |
| `--lang <zh|en|ru>` | 返回语言 | `zh` |
| `--debug` | 开启调试模式 | `false` |

## 快递公司代码

| 代码 | 快递公司 | 代码 | 快递公司 |
|------|---------|------|---------|
| `sf` | 顺丰速运 | `yto` | 圆通速递 |
| `zto` | 中通快递 | `yunda` | 韵达速递 |
| `sto` | 申通快递 | `ems` | 邮政 EMS |
| `jd` | 京东快递 | `jt` | 极兔速递 |
| `dhl` | DHL | `fedex` | FedEx |
| `ups` | UPS | `tnt` | TNT |
| `auto` | 自动识别 | `carriers` | 显示所有快递公司 |

## 输出示例

### 文本格式

```bash
node scripts/query.js sf SF1234567890123
```

输出：
```
📦 顺丰速运 SF Express
运单号：SF1234567890123
状态：运输中

🚚 物流轨迹:
2024-03-14 08:30:00 已发出，下一站【上海转运中心】
   📍 北京转运中心
2024-03-13 22:15:00 已到达【北京转运中心】
   📍 北京转运中心
```

### JSON 格式

```bash
node scripts/query.js sf SF1234567890123 --format json
```

输出：
```json
{
  "tracking_number": "SF1234567890123",
  "carrier": {
    "code": "sf",
    "name": "顺丰速运",
    "nameEn": "SF Express"
  },
  "status": "002",
  "status_description": "运输中",
  "origin": "北京市朝阳区",
  "destination": "上海市浦东新区",
  "weight": null,
  "signed_by": null,
  "tracks": [
    {
      "checkpoint_time": "2024-03-14 08:30:00",
      "tracking_detail": "已发出，下一站【上海转运中心]",
      "location": "北京转运中心"
    },
    {
      "checkpoint_time": "2024-03-13 22:15:00",
      "tracking_detail": "已到达【北京转运中心]",
      "location": "北京转运中心"
    }
  ]
}
```

### Compact 格式（简洁模式）

```bash
node scripts/query.js sf SF1234567890123 --format compact
```

输出：
```
📦 SF1234567890123 (顺丰速运) - 运输中
最新：2024-03-14 08:30:00 已发出，下一站【上海转运中心】
```

## 配置

### 1. 复制配置模板

```bash
cp config.example.json config.json
```

### 2. 填写 API Key

在 [Track123](https://www.track123.com/) 注册账号获取 API Key。

⚠️ **重要**：下面的示例值（`your_api_key_here`）需要替换为你真实的 API Key！

```json
{
  "track123": {
    "app_key": "your_api_key_here",
    "api_secret": "your_api_key_here"
  },
  "cache_duration": 3600000,
  "debug": false
}
```

### 3. 完整配置示例

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑 config.json，填入你的 API Key
# 例如（❌ 下面的值只是示例格式，不是真实可用的 API Key）：
# {
#   "track123": {
#     "app_key": "your_real_api_key",
#     "api_secret": "your_real_api_key"
#   },
#   "cache_duration": 3600000,
#   "debug": false
# }

# 验证配置
node scripts/query.js carriers
```

### 4. 安全提示

⚠️ **API Key 是私密凭证，不应该公开分享！**

- 不要将 `config.json` 提交到公共仓库
- 使用 `.gitignore` 排除 `config.json`
- 如果 API Key 泄露，请立即在 Track123 控制台重置

## 参考文档

- **[API 文档](references/track123-api.md)** - Track123 API 完整说明
- **[使用示例](references/examples.md)** - 详细使用示例和最佳实践

## 注意事项

1. **API 配额**: 免费额度 100 次/天
2. **缓存机制**: 相同运单号 1 小时内自动缓存
3. **错误处理**: 查询失败会显示具体原因
4. **隐私保护**: 不要将 `config.json` 提交到公共仓库

## 错误码

| 错误码 | 说明 |
|-------|------|
| `400` | 请求参数错误 |
| `401` | API Key 无效 |
| `429` | 请求过于频繁 |
| `500` | 服务器错误 |

---

**版本**: 1.0.1  
**作者**: josh

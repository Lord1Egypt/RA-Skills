# Track123 快递查询 - 使用示例

## 快速开始

### 1. 安装依赖

```bash
cd skills/kuaidi-query
npm install axios
```

### 2. 配置 API Key

复制配置模板并填写你的 API Key：

```bash
cp config.example.json config.json
```

编辑 `config.json`:

```json
{
  "track123": {
    "app_key": "your_track123_api_key_here"
  },
  "cache_duration": 3600000,
  "debug": false
}
```

### 3. 基本查询

```bash
node scripts/query.js sf SF1234567890123
```

## 常用命令

### 查询顺丰快递

```bash
node scripts/query.js sf SF1234567890123
```

### 查询圆通快递

```bash
node scripts/query.js yto 12345678901234
```

### 自动识别快递公司

```bash
node scripts/query.js auto 12345678901234
```

### 查询国际快递

```bash
node scripts/query.js dhl 1234567890
node scripts/query.js fedex 1234567890
```

## 输出格式选项

### 文本格式 (默认)

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
2024-03-13 18:00:00 已收件
   📍 深圳南山科技园
```

### JSON 格式

```bash
node scripts/query.js sf SF1234567890123 --format json
```

输出：
```json
{
  "success": true,
  "tracking_number": "SF1234567890123",
  "carrier": {
    "code": "sfex",
    "name": "顺丰速运"
  },
  "status": "in_transit",
  "status_description": "运输中",
  "origin": {
    "city": "深圳",
    "state": "广东",
    "country": "中国"
  },
  "destination": {
    "city": "北京",
    "state": "",
    "country": "中国"
  },
  "tracks": [
    {
      "time": "2024-03-14 08:30:00",
      "description": "已发出，下一站【上海转运中心】",
      "location": "北京转运中心"
    }
  ]
}
```

### 简洁格式

```bash
node scripts/query.js sf SF1234567890123 --format compact
```

输出：
```
📦 SF1234567890123 (顺丰速运) - 运输中
最新：2024-03-14 08:30 已发出，下一站【上海转运中心】
```

## 高级功能

### 强制刷新缓存

```bash
node scripts/query.js sf SF1234567890123 --no-cache
```

### 使用缓存

```bash
node scripts/query.js sf SF1234567890123 --cache
```

### 查询国际快递

```bash
# DHL
node scripts/query.js dhl 1234567890

# FedEx
node scripts/query.js fedex 1234567890

# UPS
node scripts/query.js ups 1Z1234567890123456
```

### 多语言查询

```bash
# 英文结果
node scripts/query.js sf SF1234567890123 --lang en

# 俄语结果
node scripts/query.js sf SF1234567890123 --lang ru
```

### 查询所有支持的快递公司

```bash
node scripts/query.js carriers
```

## 编程调用

### Node.js

```javascript
const { queryTracking } = require('./scripts/query');

async function main() {
  try {
    const result = await queryTracking('SF1234567890123', 'sf', {
      format: 'text',
      useCache: true
    });
    console.log(result);
  } catch (error) {
    console.error('查询失败:', error.message);
  }
}

main();
```

### Python

```python
from query import query_tracking

def main():
    try:
        result = query_tracking('SF1234567890123', 'sf')
        print(result)
    except Exception as e:
        print(f'查询失败：{e}')

if __name__ == '__main__':
    main()
```

## 运单号识别规则

系统会根据运单号自动识别快递公司：

| 运单号格式 | 识别结果 |
|-----------|---------|
| SF + 12-15 位数字 | 顺丰速运 |
| 1 + 10-12 位数字 | 圆通速递 |
| ZT + 10-12 位数字 | 中通快递 |
| YD + 10-12 位数字 | 韵达速递 |
| ST + 10-12 位数字 | 申通快递 |
| EM + 10-12 位数字 | 邮政 EMS |
| 1Z + 16 位字符 | UPS |
| 其他 | 自动识别 |

## 常见错误

### API Key 未配置

```
❌ 配置错误：Track123 API Key 未配置
请先配置 config.json 中的 track123.app_key
```

**解决方案**: 复制 `config.example.json` 为 `config.json` 并填写你的 API Key。

### 运单号不存在

```
❌ 查询失败：运单号不存在或尚未录入系统
```

**解决方案**: 
- 确认运单号输入正确
- 如果是刚下单，可能需要等待一段时间再查询

### API 调用次数超限

```
❌ 查询失败：请求过于频繁，请稍后再试
```

**解决方案**: 
- 等待一段时间后重试
- 增加缓存时间减少重复查询
- 升级到更高配额方案

### 网络错误

```
❌ 查询失败：网络错误，请检查网络连接
```

**解决方案**: 
- 检查网络连接
- 确认可以访问 `api.track123.com`

## 最佳实践

1. **使用缓存**: 相同运单号 1 小时内自动使用缓存，减少 API 调用
2. **批量查询**: 如需查询多个运单号，建议批量处理
3. **错误处理**: 在生产环境中添加完善的错误处理
4. **日志记录**: 开启 debug 模式记录查询日志

```bash
node scripts/query.js sf SF1234567890123 --debug
```

## 扩展开发

### 添加自定义快递公司

在 `scripts/query.js` 中添加新的快递公司代码映射：

```javascript
const CARRIER_MAP = {
  // ... 现有映射
  'custom': {
    code: 'custom',
    name: '自定义快递',
    supported: true
  }
};
```

### 自定义输出格式

修改 `scripts/query.js` 中的 `formatOutput()` 函数，添加新的输出格式。

### 集成到项目中

```javascript
const { queryTracking, identifyCarrier } = require('./scripts/query');

// 自动识别并查询
async function autoQuery(trackingNumber) {
  const carrier = await identifyCarrier(trackingNumber);
  return queryTracking(trackingNumber, carrier.code);
}
```

## 常见问题

**Q: 为什么查询不到物流信息？**
A: 可能原因：刚下单尚未揽收、运单号输入错误、快递公司不支持。

**Q: 如何增加缓存时间？**
A: 修改 `config.json` 中的 `cache_duration` 值 (毫秒)。

**Q: Track123 的免费配额是多少？**
A: 免费额度 100 次/天，详细请查看 [Track123 官网](https://www.track123.com/)。

**Q: 支持哪些快递公司？**
A: 支持 200+ 家国内外快递公司，完整列表请运行 `node scripts/query.js carriers`。

---

**版本**: 1.0.0  
**最后更新**: 2026-03-14  
**作者**: josh

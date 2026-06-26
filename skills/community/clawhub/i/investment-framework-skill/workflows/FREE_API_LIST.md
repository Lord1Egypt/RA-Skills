# 免费财经 API 清单（已验证）

> 最后更新：2026-03-19  
> 状态：✅ 可用 / ⚠️ 部分可用 / ❌ 不可用

---

## ✅ 已验证可用 API

### 1. 腾讯财经 API

**基础 URL**：`http://qt.gtimg.cn/`

**获取大盘指数**：
```bash
curl "http://qt.gtimg.cn/q=s_sh000001,s_sz399001,s_sz399006"
```

**返回格式**：
```
v_s_sh000001="1~上证指数~000001~4006.55~-56.43~-1.39~..."
```

**字段说明**：
- 字段 1：状态
- 字段 2：名称
- 字段 3：代码
- 字段 4：当前价
- 字段 5：涨跌额
- 字段 6：涨跌幅
- ...

**优点**：
- ✅ 无需 API key
- ✅ 实时数据
- ✅ 支持 A 股/港股/美股

**缺点**：
- ⚠️ 返回格式非 JSON，需解析
- ⚠️ 有请求频率限制

**使用示例**：
```python
import re

def parse_tencent_quote(text):
    """解析腾讯行情数据"""
    pattern = r'v_(.*?)="(.*?)"'
    matches = re.findall(pattern, text)
    
    result = {}
    for code, data in matches:
        fields = data.split('~')
        result[code] = {
            'name': fields[1],
            'price': float(fields[3]) if fields[3] else 0,
            'change': float(fields[4]) if fields[4] else 0,
            'change_percent': float(fields[5]) if fields[5] else 0
        }
    
    return result
```

---

### 2. 新浪财经 API

**基础 URL**：`http://hq.sinajs.cn/`

**获取大盘指数**：
```bash
curl "http://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006"
```

**返回格式**：
```
var hq_str_s_sh000001="上证指数，4006.55，..."
```

**优点**：
- ✅ 无需 API key
- ✅ 实时数据
- ✅ 支持全球市场

**缺点**：
- ⚠️ 有时返回"Forbidden"
- ⚠️ 有请求频率限制

---

### 3. 东方财富网 API

**基础 URL**：`https://push2.eastmoney.com/`

**获取个股行情**：
```bash
curl "https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f44,f45,f46,f47,f48"
```

**优点**：
- ✅ 数据全面
- ✅ 支持 A 股/港股/美股

**缺点**：
- ⚠️ 需要解析回调函数
- ⚠️ 字段代码复杂

---

## ⚠️ 需要注册的免费 API

### 1. Tushare Pro

**网址**：https://tushare.pro/

**免费额度**：
- 基础积分：100 分（注册即送）
- 可获取：日线行情、基本面数据

**限制**：
- ⚠️ 需要注册获取 token
- ⚠️ 高频数据需要更多积分

**使用示例**：
```python
import tushare as ts

ts.set_token('your_token')
pro = ts.pro_api()

# 获取日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20260319')
```

---

### 2. 聚宽 JoinQuant

**网址**：https://www.joinquant.com/

**免费额度**：
- 注册即送免费额度
- 可获取：历史行情、财务数据

**限制**：
- ⚠️ 需要注册
- ⚠️ 实时数据需要付费

---

### 3. 理杏仁

**网址**：https://www.lixinger.com/

**免费额度**：
- 基础数据免费
- 可获取：估值数据、财务数据

**限制**：
- ⚠️ 需要注册
- ⚠️ 高级数据需要付费

---

## ❌ 不可用/付费 API

| API | 状态 | 说明 |
|-----|------|------|
| Wolfram Alpha | ❌ | 需要付费 API key |
| 东方财富 Choice | ❌ | 付费（机构版） |
| Wind | ❌ | 付费（机构版） |

---

## 推荐方案

### 方案 A：纯免费（推荐）

**组合**：腾讯财经 + 新浪财经 + 手动更新

**优点**：
- ✅ 完全免费
- ✅ 无需注册
- ✅ 实时数据

**缺点**：
- ⚠️ 部分数据需手动更新（北向资金/经济事件）
- ⚠️ 需要解析非 JSON 格式

**适用**：个人使用、演示、学习

---

### 方案 B：免费 + 手动（推荐）

**组合**：腾讯 API（自动） + 人工更新（北向资金/事件）

**流程**：
1. 腾讯 API 获取大盘数据（自动）
2. 人工更新北向资金（港交所网站，2 分钟）
3. 人工更新经济事件（财联社，2 分钟）

**总耗时**：约 5 分钟/天

**适用**：日常工作流、真实投资决策

---

### 方案 C：付费 API（专业）

**组合**：Tushare Pro（2000 元/年） + 财联社 VIP

**优点**：
- ✅ 数据全面
- ✅ 自动化程度高

**缺点**：
- ❌ 费用较高

**适用**：专业投资者、机构

---

## 代码示例

### 获取大盘数据（腾讯 API）

```python
#!/usr/bin/env python3
import requests
import re

def get_market_data():
    """获取大盘数据（腾讯 API）"""
    codes = ['s_sh000001', 's_sz399001', 's_sz399006']
    url = f"http://qt.gtimg.cn/q={','.join(codes)}"
    
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return parse_tencent_quote(response.text)
    return {}

def parse_tencent_quote(text):
    """解析腾讯行情数据"""
    pattern = r'v_(.*?)="(.*?)"'
    matches = re.findall(pattern, text)
    
    result = {}
    name_map = {
        's_sh000001': '上证指数',
        's_sz399001': '深证成指',
        's_sz399006': '创业板指'
    }
    
    for code, data in matches:
        fields = data.split('~')
        if len(fields) >= 6:
            result[name_map.get(code, code)] = {
                'price': float(fields[3]) if fields[3] else 0,
                'change': float(fields[4]) if fields[4] else 0,
                'change_percent': float(fields[5]) if fields[5] else 0
            }
    
    return result

if __name__ == '__main__':
    data = get_market_data()
    for name, info in data.items():
        print(f"{name}: {info['price']} ({info['change_percent']}%)")
```

---

## 数据验证清单

执行工作流前检查：
- [ ] 腾讯 API 可访问
- [ ] 数据解析正常
- [ ] 无"待更新"占位符
- [ ] 数据来源已标注

---

*最后更新：2026-03-19*

# 数据采集脚本说明

> 本目录存放上市公司并购数据库的数据采集脚本，包括自动采集、定期更新等功能。

---

## 一、脚本列表

| 脚本名称 | 功能说明 | 状态 |
|---------|---------|-----|
| fetch_stock_basic.py | 获取上市公司基础信息 | 待开发 |
| fetch_financial.py | 获取财务报表数据 | 待开发 |
| fetch_ma_events.py | 获取并购公告事件 | 待开发 |
| fetch_market_data.py | 获取市值行情数据 | 待开发 |
| update_knowledge_base.py | 批量更新IMA知识库 | 待开发 |

---

## 二、脚本开发规范

### 2.1 命名规范

```python
# 文件名格式：action_source.py
# 示例：
# fetch_stock_basic.py - 获取股票基础信息
# fetch_financial.py - 获取财务数据
# update_knowledge_base.py - 更新知识库
```

### 2.2 函数规范

```python
def fetch_xxx(source="primary"):
    """
    数据采集函数
    
    Args:
        source: 数据源，primary=主数据源，backup=备用数据源
    
    Returns:
        dict: 采集结果 {
            "status": "success/failed",
            "data": [...],
            "errors": [...]
        }
    """
    pass

def transform_xxx(raw_data):
    """
    数据转换函数
    
    Args:
        raw_data: 原始数据
    
    Returns:
        dict: 转换后数据
    """
    pass
```

### 2.3 输出规范

```python
# 输出格式：JSON
{
    "status": "success",
    "timestamp": "YYYY-MM-DD HH:mm:ss",
    "source": "数据源名称",
    "count": 采集数量,
    "data": [...],
    "errors": [...]
}
```

---

## 三、数据源配置

### 3.1 数据源列表

| 数据类型 | 主数据源 | 备用数据源 |
|---------|---------|-----------|
| 股票基础信息 | 交易所官网 | 同花顺API |
| 财务报表 | 巨潮资讯网 | 东方财富 |
| 并购公告 | 交易所公告 | 巨潮资讯 |
| 市值行情 | 东方财富 | 同花顺 |
| 港股数据 | 港交所披露易 | Wind |

### 3.2 API配置示例

```python
# 数据源配置（需在SECRET.md中存储密钥）
DATA_SOURCES = {
    "eastmoney": {
        "base_url": "https://datacenter-web.eastmoney.com",
        "api_key": "${EASTMONEY_API_KEY}"
    },
    "tonghuashun": {
        "base_url": "https://api.tonghuashun.com",
        "api_key": "${THS_API_KEY}"
    }
}
```

---

## 四、定时任务配置

### 4.1 采集频率

| 数据类型 | 采集频率 | 说明 |
|---------|---------|------|
| 市值数据 | 每月末 | 月度更新 |
| 财务数据 | 季报发布后 | 事件触发 |
| 并购公告 | 实时监控 | 事件触发 |
| 基础信息 | 年度更新 | 定期更新 |

### 4.2 Cron配置示例

```bash
# 每月末更新市值数据
0 2 28-31 * * /opt/scripts/fetch_market_data.py >> /var/log/ma_data.log 2>&1

# 每季度财报发布后更新财务数据
0 3 * * 1 /opt/scripts/fetch_financial.py >> /var/log/ma_financial.log 2>&1
```

---

## 五、错误处理

### 5.1 错误类型

| 错误类型 | 处理方式 | 告警级别 |
|---------|---------|---------|
| 网络超时 | 重试3次，间隔5秒 | 低 |
| 数据源返回空 | 切换备用数据源 | 中 |
| 解析失败 | 记录原始数据，人工处理 | 高 |
| API限流 | 等待1分钟后重试 | 低 |

### 5.2 错误日志

```python
import logging

logging.basicConfig(
    filename='/var/log/ma_script_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 六、使用说明

### 6.1 手动执行

```bash
# 获取股票基础信息
python3 fetch_stock_basic.py --market A

# 获取财务数据
python3 fetch_financial.py --period Q4 --year 2024

# 更新知识库
python3 update_knowledge_base.py --batch 2024_Q4
```

### 6.2 参数说明

| 参数 | 说明 | 示例 |
|-----|------|-----|
| --market | 市场类型 | A/H/AH |
| --period | 财报周期 | Q1/Q2/Q3/Q4 |
| --year | 年份 | 2024 |
| --batch | 批次标识 | 2024_Q4 |

---

*本目录为脚本开发占位目录，具体脚本待后续开发*

# smart-cache - 智能学习缓存层

## 简介

为 OpenClaw 设计的智能缓存系统，类似"人类小脑"，能够：

1. **高速缓存** - 重复查询加速 200,000 倍（2-3 秒 → 0.01ms）
2. **自动学习** - 识别 3 次以上的常用请求模式
3. **智能推荐** - 记录并推荐最佳工具/解决方案
4. **双层架构** - 内存缓存（LRU）+ 磁盘缓存（SQLite）

## 安装

### 方式 1：克隆到 OpenClaw workspace

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills
git clone https://gitee.com/your-repo/smart-cache.git
```

### 方式 2：手动下载

下载本仓库到 `skills/smart-cache/` 目录

## 快速开始

### 1. 基础缓存

```python
from skills.smart_cache.smart_cache import cache

# 设置缓存（5 分钟过期）
cache.set('stock:600519:price', {'price': 1413.64}, ttl=300)

# 获取缓存
data = cache.get('stock:600519:price')
if data:
    print(f"缓存命中：{data}")
```

### 2. 装饰器方式

```python
from skills.smart_cache.smart_cache import cached

@cached(ttl=60, key_prefix='db')
def get_db_stats():
    # 耗时操作...
    return result

# 首次执行函数，60 秒内返回缓存
result = get_db_stats()
```

### 3. 请求学习器

```python
from skills.smart_cache.request_learner import learner

# 记录请求（自动学习）
learner.record_request(
    query="查询贵州茅台最新价",
    tool="mx_query_v2",
    duration=0.01,
    success=True
)

# 获取推荐
recs = learner.get_recommendations()
for rec in recs:
    print(f"{rec['query_pattern']}: {rec['count']}次，最佳工具：{rec['best_tool']}")
```

### 4. 命令行工具

```bash
# 查看缓存统计
python skills/smart-cache/cache_manager.py stats

# 查看学习推荐
python skills/smart-cache/learner_manager.py recs

# 获取最佳工具
python skills/smart-cache/learner_manager.py best "查询贵州茅台最新价"

# 清空缓存
python skills/smart-cache/cache_manager.py clear
```

## 核心组件

| 文件 | 说明 | 大小 |
|------|------|------|
| `smart_cache.py` | 缓存核心（内存 + 磁盘双层） | 10KB |
| `request_learner.py` | 请求学习器（自动识别常用请求） | 10KB |
| `cache_manager.py` | 缓存管理 CLI | 3KB |
| `learner_manager.py` | 学习器管理 CLI | 3KB |

## 性能

| 操作 | 无缓存 | 有缓存 | 加速比 |
|------|--------|--------|--------|
| 读取（命中） | 2-3 秒 | 0.01ms | **200,000x** |
| 读取（未命中） | 2-3 秒 | 2-3 秒 | 1x |
| 写入 | - | 10ms/条 | - |

## 缓存策略

| 类型 | TTL | 说明 |
|------|-----|------|
| `stock:price` | 5 分钟 | 股票价格 |
| `stock:info` | 1 小时 | 股票信息 |
| `db:stats` | 1 分钟 | 数据库统计 |
| `query:result` | 10 分钟 | 查询结果 |
| `stock:list` | 1 小时 | 股票列表 |

## 学习阈值

| 指标 | 阈值 | 效果 |
|------|------|------|
| 重复次数 | ≥3 次 | 标记为"常用请求" |
| 成功率 | >80% | 推荐该工具 |
| 响应时间 | 最快 | 记录为最佳方案 |

## 集成示例

### 妙想金融数据查询（带缓存）

```python
from skills.smart_cache.smart_cache import cache
from skills.smart_cache.request_learner import learner
import time

def query_stock_price_cached(stock_code: str):
    """查询股票最新价（带缓存和学习）"""
    start = time.time()
    cache_key = f'stock:price:{stock_code}'
    
    # 尝试缓存
    cached = cache.get(cache_key)
    if cached:
        learner.record_request(
            query=f"查询{stock_code}最新价",
            tool="mx_query_v2(cache)",
            duration=time.time() - start,
            success=True
        )
        return cached
    
    # API 查询
    result = query_mx_data(f"{stock_code}最新价")
    
    # 缓存并记录
    cache.set(cache_key, result, ttl=300)
    learner.record_request(
        query=f"查询{stock_code}最新价",
        tool="mx_query_v2(api)",
        duration=time.time() - start,
        success=True
    )
    
    return result
```

## 文件结构

```
smart-cache/
├── SKILL.md                 # Skill 说明（本文件）
├── README.md                # 详细文档
├── smart_cache.py           # 缓存核心
├── request_learner.py       # 请求学习器
├── cache_manager.py         # 缓存管理 CLI
├── learner_manager.py       # 学习器管理 CLI
├── examples/                # 示例代码
│   └── mx_query_v2.py      # 妙想查询集成示例
├── cache/                   # 缓存数据目录（运行时创建）
│   ├── cache.db            # 磁盘缓存（SQLite）
│   ├── patterns.json       # 请求模式
│   └── request_log.jsonl   # 请求日志
└── requirements.txt         # Python 依赖
```

## 依赖

- Python 3.8+
- 无外部依赖（仅使用标准库：sqlite3, json, os, time, collections）

## 使用场景

### ✅ 推荐场景

1. **重复 API 查询** - 股票价格、天气、汇率等
2. **数据库统计** - COUNT、SUM 等聚合查询
3. **配置文件读取** - 不频繁变更的配置
4. **网页抓取结果** - 相同 URL 的缓存
5. **耗时计算结果** - 可复用的计算

### ❌ 不推荐场景

1. **实时数据** - 秒级行情、实时位置
2. **超大结果集** - >10MB 的数据
3. **敏感信息** - 密码、密钥、个人隐私
4. **一次性操作** - 不会重复的请求

## 管理命令

```bash
# 缓存管理
python cache_manager.py stats      # 查看统计
python cache_manager.py clear      # 清空缓存
python cache_manager.py test       # 性能测试

# 学习器管理
python learner_manager.py stats    # 查看统计
python learner_manager.py recs     # 查看推荐
python learner_manager.py report   # 导出报告
python learner_manager.py clear    # 清空数据
```

## 故障处理

### 缓存未命中
- 检查 TTL 是否过期
- 检查缓存键是否正确
- 确认是否被手动清除

### 学习器未识别
- 确认请求是否达到 3 次阈值
- 检查查询标准化是否正确

### 性能下降
- 清空缓存：`python cache_manager.py clear`
- 检查磁盘空间
- 减少缓存条目上限

## 扩展开发

### 添加新缓存类型

```python
from smart_cache import cache

# 设置自定义 TTL
cache.set('custom:key', data, ttl=3600)  # 1 小时

# 只写内存（不写磁盘）
cache.memory.set('temp:key', data, ttl=60)
```

### 自定义学习逻辑

```python
from request_learner import learner

# 记录请求
learner.record_request(
    query="自定义查询",
    tool="my_tool",
    duration=1.5,
    success=True,
    metadata={'custom': 'data'}
)
```

## 许可证

MIT License

## 作者

OpenClaw Community

## 更新日志

### v1.0.0 (2026-03-14)
- ✅ 内存缓存（LRU 策略）
- ✅ 磁盘缓存（SQLite）
- ✅ 请求学习器
- ✅ 自动推荐最佳工具
- ✅ CLI 管理工具
- ✅ 完整文档

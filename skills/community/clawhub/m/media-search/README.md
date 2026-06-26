# 媒体库搜索工具

基于媒体大数据平台API的专业媒体数据检索工具，支持关键词搜索、时间范围过滤、信源类型筛选等功能。

## 功能特性

- **智能关键词处理**：自动拆分和优化搜索关键词
- **多维度过滤**：支持时间范围、信源类型、信源名称等过滤条件
- **Token持久化**：文件级Token存储，支持多进程安全访问
- **结果保存**：自动保存搜索结果到sources文件夹，支持审计追踪
- **灵活配置**：支持命令行参数和JSON输入

## 快速开始

### 环境要求

- Python 3.7+
- 需要配置API密钥

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置API密钥

设置环境变量：

```bash
export NEWS_BIGDATA_API_KEY="your_api_key"
export NEWS_BIGDATA_API_SECRET="your_api_secret"
```

### 基本用法

#### 命令行使用

```bash
# 基础搜索
python search.py --json-input '{"keywords": "人工智能 政策", "limit": 20}'


# 指定时间范围
python search.py --json-input '{"keywords": "两会", "publish_time_start": "2026-03-01 00:00:00", "publish_time_end": "2026-03-31 23:59:59"}'

# 指定具体信源
python search.py --json-input '{"keywords": "一带一路", "source_name": "人民日报", "limit": 5}'
```

#### 作为模块使用

```python
from media_search import MediaSearchEngine, SearchParameters

# 创建搜索参数
params = SearchParameters(
    keywords="人工智能 政策",
    limit=20
)

# 执行搜索
engine = MediaSearchEngine()
result = engine.search(params)

# 处理结果
if result.success:
    print(f"找到 {result.total} 条结果")
    for item in result.items:
        print(f"标题: {item.title}")
        print(f"信源: {item.source_name}")
        print(f"时间: {item.publish_time}")
else:
    print(f"搜索失败: {result.error}")
```

## 参数说明

### 搜索参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `keywords` | string | 是 | - | 搜索关键词，支持多个关键词用空格分隔 |
| `keyword_position` | string | 否 | `标题或正文` | 关键词匹配位置：`标题`、`正文`、`标题或正文` |
| `publish_time_start` | string | 否 | 无 | 开始时间，格式：`yyyy-MM-dd HH:mm:ss`，直接使用用户提供的值，不做额外处理 |
| `publish_time_end` | string | 否 | 当前时间 | 结束时间，格式：`yyyy-MM-dd HH:mm:ss` |
| `source_name` | string | 否 | - | 具体信源名称，支持模糊匹配 |
| `limit` | int | 否 | `10` | 返回结果数量，范围：1-50 |

### 时间处理说明

发布时间参数现在直接使用用户提供的值，不再进行模糊关键词的自动转换。请提供标准的时间格式：`yyyy-MM-dd HH:mm:ss`。

## 文件结构

```
mbd-api/
├── search.py              # 主入口脚本
├── requirements.txt       # 依赖包
├── README.md             # 使用说明
├── SKILL-optimized.md    # 优化后的SKILL文件
└── scripts/
    ├── media_search.py    # 媒体搜索引擎核心
    ├── token_manager.py   # Token管理器
    └── test_token.py     # 测试脚本
└── sources/              # 搜索结果保存目录
```

## Token管理

Token管理器支持以下特性：

- **文件级持久化**：Token保存到本地文件，重启后仍然有效
- **多进程安全**：使用文件锁确保多进程并发安全
- **自动刷新**：Token过期前自动刷新，提前5分钟预警
- **进程内缓存**：减少文件IO，提高性能

Token文件默认保存在：`<skill目录>/.mbd_token_cache.json`（例如：`/Users/liushilong/Downloads/mbd-api/.mbd_token_cache.json`）

## 结果保存

所有搜索结果都会自动保存到 `sources/` 目录：

- **文件名格式**：`media_YYYYMMDD_HHMMSS_<关键词>.md`
- **保存内容**：完整的查询参数、搜索结果、时间戳
- **审计追踪**：支持查询历史追溯和结果复用

## 错误处理

### 常见错误

1. **API密钥未配置**
   ```
   错误: 缺少API凭据。请设置环境变量 NEWS_BIGDATA_API_KEY 和 NEWS_BIGDATA_API_SECRET
   ```

2. **Token获取失败**
   ```
   Token请求失败: Invalid credentials
   ```

3. **参数错误**
   ```
   搜索关键词不能为空
   ```

### 重试机制

- API调用失败时自动重试（最多3次）
- Token失效时自动刷新
- 网络超时自动重试

## 性能优化

1. **Token缓存**：减少API调用次数
2. **文件锁优化**：使用非阻塞锁避免死锁
3. **连接池**：复用HTTP连接
4. **结果缓存**：避免重复查询相同内容

## 安全考虑

- API密钥通过环境变量传递，避免硬编码
- Token文件权限限制（600）
- 支持HTTPS证书验证（默认禁用，生产环境建议启用）
- 输入参数验证和清理

## 开发指南

### 扩展搜索参数

在 `SearchParameters` 类中添加新字段：

```python
class SearchParameters(BaseModel):
    # ... 现有字段
    new_field: Optional[str] = Field(default=None, description="新参数说明")
```

### 自定义结果处理

继承 `MediaSearchEngine` 并重写相关方法：

```python
class CustomSearchEngine(MediaSearchEngine):
    def _parse_api_response(self, api_response, query):
        # 自定义解析逻辑
        pass
```

## 许可证

MIT License

## 支持

如有问题或建议，请提交Issue或联系开发团队。
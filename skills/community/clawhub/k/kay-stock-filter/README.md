# Stock Filter Skills for OpenClaw

股票多条件筛选、热门因子管理、Jiuyan 数据查询和抖音热点分析技能。

## 功能概览

| 模块 | 工具数 | 说明 |
|------|--------|------|
| 股票筛选 | 6 | 多条件筛选、搜索、详情、批量查询、对比 |
| 热门因子 | 6 | 预设的增删改查、排序和使用 |
| Jiuyan 数据 | 3 | 股票分析、主题、文章查询 |
| 抖音热点 | 2 | 热点列表和详情 |

共计 **17 个工具**。

## 安装

```bash
cd stock-filter-skills
npm install
```

要求 Node.js >= 18.0.0。

## 配置

### 方式一：环境变量（推荐）

```bash
export STOCK_API_BASE_URL="http://localhost:8000"
export STOCK_API_KEY="your-api-key-here"
export STOCK_API_TIMEOUT="30"
```

### 方式二：.env 文件

```bash
cp .env.example .env
# 编辑 .env 填写实际配置
```

### 方式三：OpenClaw config

参见 `config.json.example`。

## 使用方式

### 作为 OpenClaw Skill

将本目录安装为 OpenClaw Skill：

```bash
# 本地加载
openclaw skill load stock-filter-skills

# 或发布到 ClawHub
openclaw skill publish stock-filter-skills
```

安装后，在对话中提到"股票筛选"、"热门因子"、"股票分析"、"抖音热点"等触发词时，Agent 会自动调用对应工具。

### 命令行直接调用

```bash
# 查看所有工具
node src/main.js --help

# 搜索股票
node src/main.js stock_search '{"keyword": "贵州茅台"}'

# 筛选股票
node src/main.js stock_filter '{"filters": {"market": ["sh"]}, "page": 1}'

# 获取股票详情
node src/main.js stock_detail '{"code": "600519"}'

# 批量获取多只股票
node src/main.js stock_detail_batch '{"codes": ["600519", "000858", "000333"]}'

# 对比股票指标
node src/main.js stock_compare '{"codes": ["600519", "000858"], "fields": ["pe", "pb", "roe"]}'

# 获取热门因子
node src/main.js hot_factor_list

# Jiuyan 分析
node src/main.js jiuyan_stock_analysis '{"stock_code": "300236"}'

# 抖音热点
node src/main.js douyin_hotspot_list '{"page": 1}'
```

## API Key 认证

### 工作原理

所有请求通过 `X-API-Key` HTTP Header 传递密钥，后端验证通过后放行。

### 后端需要配合的事项

1. **创建 API Key 管理功能**：生成、存储（哈希）和验证 Key
2. **添加认证中间件**：检查 `X-API-Key` Header
3. **权限控制**：不同 Key 绑定不同权限

### 安全建议

- API Key 至少 32 字符，使用 UUID 或随机字符串
- 数据库存储 Key 的哈希值（SHA-256），不存明文
- 支持 Key 的吊销和过期机制
- 记录调用日志用于审计

## 项目结构

```
stock-filter-skills/
├── SKILL.md               # OpenClaw 技能定义（核心）
├── README.md              # 说明文档
├── config.json.example    # OpenClaw 配置模板
├── package.json           # Node.js 依赖与脚本
├── .env.example           # 环境变量模板
├── .gitignore
└── src/
    ├── main.js            # CLI 入口与工具调度
    ├── tools.js           # 15 个工具实现
    ├── config.js          # 配置与环境变量
    └── api-client.js      # 共享 HTTP 客户端
```

## 发布到 ClawHub

### 1. 安装 ClawHub CLI

```bash
npm i -g clawhub
```

### 2. 登录

```bash
clawhub login
```

浏览器会打开 ClawHub 登录页面（需要 GitHub 账号，且注册满 1 周）。

### 3. 发布

```bash
clawhub publish ./stock-filter-skills \
  --slug stock-filter-skills \
  --name "Stock Filter Skills" \
  --version 1.0.0 \
  --tags latest
```

### 4. 后续更新

```bash
clawhub publish ./stock-filter-skills \
  --slug stock-filter-skills \
  --version 1.1.0 \
  --changelog "新增抖音热点功能" \
  --tags latest
```

或使用批量同步：

```bash
clawhub sync --all
```

## License

MIT

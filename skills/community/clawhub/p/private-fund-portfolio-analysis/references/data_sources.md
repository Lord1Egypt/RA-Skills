# 数据源配置

## 环境变量（必需）

运行脚本前先设置以下环境变量：

```bash
export MYSQL_HOST=<数据库地址>
export MYSQL_PORT=3306
export MYSQL_USER=<用户名>
export MYSQL_PASSWORD=<密码>
export MYSQL_DATABASE=指数行情数据库
```

## MySQL 连接

```python
conn = pymysql.connect(
    host=os.environ.get("MYSQL_HOST"),
    port=int(os.environ.get("MYSQL_PORT", "3306")),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE", "指数行情数据库"),
    connect_timeout=8, charset="utf8mb4"
)
```

**注意**: charset 必须用 `utf8mb4`，否则中文行业名称报错

## 申万行业表

```sql
SELECT 股票代码, 申万一级行业名称
FROM 股票申万行业分类
WHERE 股票代码 = %s
```

## AKShare 数据（无需认证）

- **市值**: `ak.stock_zh_a_spot_em()` → CSV缓存
- **指数成分**: 
  - `ak.index_stock_cons("000300")` → 沪深300
  - `ak.index_stock_cons("000905")` → 中证500
  - `ak.index_stock_cons("000852")` → 中证1000
  - `ak.index_stock_cons_csindex("932000")` → 中证2000（用 csindex，不要用 index_stock_cons）

## XLS 列位（两种模板）

| 模板 | 股票代码格式 | 示例 | 市值列 |
|------|------------|------|--------|
| 模板A | `XXXX.XX.XX.XXXXXX` | `1102.01.01.600519` | col9 |
| 模板B | `XXXX.XX.XX.XXXXXX SH/SZ` | `1102.01.01.600519 SH` | col9 |

**识别方式**: `re.search(r"\.(\d{6})\s*(SH|SZ)?$", acc)` - 匹配 `.XXXXXX SH` 格式

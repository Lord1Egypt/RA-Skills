# 观远数据 API Skill

观远数据 API 命令行工具，支持用户登录、Token 自动管理和卡片数据导出（JSON/CSV格式）。

## 功能

1. **用户登录** - 通过配置文件中的登录信息获取 Token
2. **Token 自动管理** - 自动保存、读取和刷新 Token
3. **获取卡片数据** - 获取指定卡片 ID 的数据
4. **导出 CSV** - 支持将卡片数据导出为 CSV 格式
5. **元数据导出** - 自动生成包含字段信息的元数据文件
6. **数据采样** - 支持指定行数采样输出

## 安装

```bash
# 将脚本添加到 PATH
export PATH="$PATH:~/workload/skills/guanyuan-data"

# 或创建软链接到 /usr/local/bin
sudo ln -sf ~/workload/skills/guanyuan-data/index.js /usr/local/bin/guanyuan
```

## 配置

### 1. 初始化配置

```bash
guanyuan init
```

### 2. 创建配置文件

创建配置文件 `~/.guanyuan/config.json`：

```bash
mkdir -p ~/.guanyuan
cat > ~/.guanyuan/config.json << 'EOF'
{
  "baseUrl": "https://your-guanyuan-domain.com",
  "domain": "your-domain",
  "loginId": "your-login-id",
  "password": "your-password"
}
EOF
```

### 3. 登录获取 Token

```bash
guanyuan login
```

登录成功后，Token 会自动保存到 `~/.guanyuan/user.token`。

## 使用方法

### 查看帮助

```bash
guanyuan help
```

### 查看配置状态

```bash
guanyuan status
```

### 获取卡片数据（JSON格式）

```bash
# 基本用法
guanyuan card <卡片ID>

# 使用 GRID 视图
guanyuan card abc123 --view GRID

# 限制返回条数
guanyuan card abc123 --limit 50

# 设置偏移量（分页）
guanyuan card abc123 --offset 100 --limit 50
```

### 导出卡片数据（CSV格式）

```bash
# 输出到终端（采样5行）
guanyuan csv <卡片ID> --sample 5

# 导出到文件
guanyuan csv <卡片ID> --output data.csv

# 采样指定行数并导出
guanyuan csv <卡片ID> --output data.csv --sample 50

# 获取大量数据并导出
guanyuan csv <卡片ID> --output data.csv --limit 1000

# 组合使用
guanyuan csv <卡片ID> --output data.csv --sample 100 --limit 5000 --view GRID
```

## 文件结构

### 配置目录结构

```
~/.guanyuan/
├── config.json    # 配置文件（baseUrl、domain、loginId、password）
└── user.token     # 登录后的 Token
```

### 导出文件结构

当使用 `--output` 选项导出 CSV 时，会生成两个文件：

```
output.csv           # CSV 数据文件
output_meta.json     # 元数据文件（字段信息、类型等）
```

## 元数据文件格式

元数据文件 (`*_meta.json`) 包含以下信息：

```json
{
  "cardId": "卡片ID",
  "cardType": "卡片类型（CHART/TEXT等）",
  "chartType": "图表类型（PIVOT_TABLE/BASIC_COLUMN等）",
  "view": "视图类型（GRAPH/GRID）",
  "exportTime": "导出时间（ISO格式）",
  "totalRows": "总行数",
  "dataLimit": "数据限制",
  "hasMoreData": "是否有更多数据",
  "fields": [
    {
      "name": "字段显示名称",
      "originalName": "字段原始名称",
      "type": "数据类型（STRING/TIMESTAMP/DOUBLE等）",
      "metaType": "元类型（DIM=维度, METRIC=度量）",
      "fieldType": "字段类型（dimension/metric）",
      "fieldId": "字段ID",
      "granularity": "时间粒度（如有）",
      "alias": "字段别名",
      "annotation": "字段注释"
    }
  ]
}
```

## 配置文件格式

```json
{
  "baseUrl": "https://your-guanyuan-domain.com",   // API 服务地址（支持http://或https://前缀）
  "domain": "your-domain",                          // 观远域名
  "loginId": "your-login-id",                       // 登录用户 ID
  "password": "your-password"                       // 登录密码（无需Base64编码，程序会自动处理）
}
```

## Token 管理

- Token 保存位置：`~/.guanyuan/user.token`
- Token 自动过期检测
- Token 失效时自动重新登录并刷新

## 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `init` | 初始化配置（显示配置说明） | `guanyuan init` |
| `login` | 登录并获取 token | `guanyuan login` |
| `card` | 获取指定卡片的数据（JSON格式） | `guanyuan card abc123 --limit 50` |
| `csv` | 导出卡片数据为CSV格式 | `guanyuan csv abc123 --output data.csv` |
| `status` | 显示配置和 token 状态 | `guanyuan status` |
| `help` | 显示帮助信息 | `guanyuan help` |

## 选项参考

### 通用选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--view <GRAPH\|GRID>` | 数据获取方式 | GRAPH |
| `--limit <数字>` | 获取数据条数 | 100 |
| `--offset <数字>` | 数据起始位置 | 0 |

### CSV导出选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--output <文件名>` | 输出CSV到文件 | 输出到终端 |
| `--sample <数字>` | 采样指定行数 | 输出所有行 |

## 使用示例

```bash
# 1. 初始化配置
guanyuan init

# 2. 登录
guanyuan login

# 3. 查看状态
guanyuan status

# 4. 获取卡片数据（JSON）
guanyuan card l059d768f28bd404caf8df3e --view GRID --limit 50

# 5. 导出CSV到终端（采样5行）
guanyuan csv l059d768f28bd404caf8df3e --sample 5

# 6. 导出CSV到文件
guanyuan csv l059d768f28bd404caf8df3e --output query_data.csv --sample 100

# 7. 导出大量数据
guanyuan csv l059d768f28bd404caf8df3e --output all_data.csv --limit 5000
```

## API 参考

- [用户登录 API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3470502)
- [获取卡片数据 API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3471043)

## 技术栈

- Node.js (>=14.0.0)
- 原生 https 模块
- 原生 fs 模块

## 许可证

MIT

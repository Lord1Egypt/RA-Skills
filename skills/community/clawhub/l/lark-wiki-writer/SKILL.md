# Lark Wiki Writer

飞书知识库文档写入器 - 支持 Markdown 解析、富文本、标题识别。

## 快速开始

### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.larksuite.com/app)
2. 点击"创建企业自建应用"
3. 填写应用名称和描述
4. 记录 **App ID** 和 **App Secret**

### 步骤 2：配置应用权限

在应用管理页面，添加以下权限：

- ✅ **知识库** → 查看、编辑和管理知识空间
- ✅ **文档** → 查看、编辑和管理文档

### 步骤 3：获取知识库 Space ID

1. 打开飞书知识库
2. 在浏览器地址栏找到 Space ID（长数字串）
3. 例如：`https://xxx.larksuite.com/wiki/space/7603663680785370844`
   - Space ID 就是 `7603663680785370844`

### 步骤 4：获取父节点 Token（可选）

如果要在特定目录下创建文档：

1. 打开目标目录
2. 在地址栏找到 node_token
3. 例如：`https://xxx.larksuite.com/wiki/JieGwPB0MiKhPbkkq9cltbPIgid`
   - 父节点 token 就是 `JieGwPB0MiKhPbkkq9cltbPIgid`

### 步骤 5：配置环境变量

```bash
export LARK_APP_ID="cli_xxxxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxx"
export LARK_SPACE_ID="7603663680785370844"
export LARK_WIKI_DOMAIN="your-domain.larksuite.com"  # 可选
export LARK_PARENT_NODE="JieGwPB0MiKhPbkkq9cltbPIgid"  # 可选
```

或者创建配置文件 `config.json`：

```json
{
  "app_id": "cli_xxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxx",
  "space_id": "7603663680785370844",
  "wiki_domain": "your-domain.larksuite.com"
}
```

### 步骤 6：验证配置

```bash
python3 lark_wiki_writer.py validate \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --space-id YOUR_SPACE_ID
```

输出示例：
```
📊 配置验证结果

APP_ID: ✅
APP_SECRET: ✅
Space ID: ✅
Token 获取: ✅
知识库访问: ✅
```

---

## 核心功能

### 1. 标题识别

根据 `#` 数量自动识别标题级别：

| Markdown | 飞书 Block |
|----------|-----------|
| `# 标题` | heading1 |
| `## 二级标题` | heading2 |
| `### 三级标题` | heading3 |
| ... | ... |
| `###### 六级标题` | heading6 |

### 2. 富文本支持

| Markdown | 效果 |
|----------|------|
| `**加粗**` | **加粗** |
| `*斜体*` | *斜体* |
| `***加粗斜体***` | ***加粗斜体*** |
| `~~删除线~~` | ~~删除线~~ |
| `` `行内代码` `` | `行内代码` |
| `[链接](url)` | [链接](url) |

### 3. 列表支持

```markdown
- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2
```

### 4. 代码块

````markdown
```python
def hello():
    print("Hello World")
```
````

支持的语言：python, javascript, typescript, go, rust, java, c, cpp, shell, bash, sql, html, css, json, yaml, xml, markdown

### 5. 分隔线

```markdown
---
```

或

```markdown
***
```

---

## 使用方法

### 方式 1：命令行参数

```bash
# 创建文档
python3 lark_wiki_writer.py create "文档标题" "# 内容" \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --space-id YOUR_SPACE_ID \
  --parent YOUR_PARENT_NODE

# 从文件写入
python3 lark_wiki_writer.py write_file "文档标题" /path/to/file.md \
  --app-id YOUR_APP_ID \
  --app-secret YOUR_APP_SECRET \
  --space-id YOUR_SPACE_ID
```

### 方式 2：环境变量

```bash
# 设置环境变量
export LARK_APP_ID="cli_xxx"
export LARK_APP_SECRET="xxx"
export LARK_SPACE_ID="xxx"
export LARK_PARENT_NODE="xxx"

# 使用
python3 lark_wiki_writer.py create "文档标题" "# 内容"
python3 lark_wiki_writer.py write_file "文档标题" report.md
```

### 方式 3：Python API

```python
from lark_wiki_writer import LarkWikiWriter

# 初始化
writer = LarkWikiWriter(
    app_id="cli_xxx",
    app_secret="xxx",
    space_id="xxx",
    wiki_domain="your-domain.larksuite.com"
)

# 创建并写入
doc = writer.create_and_write(
    title="我的文档",
    content="""
# 主标题

## 二级标题

这是**加粗**和*斜体*内容。

### 列表
- 项目1
- 项目2

### 代码
```python
print("Hello")
```
""",
    parent_node_token="YOUR_PARENT_NODE"
)

print(f"文档链接: {doc['url']}")
```

---

## 完整示例

### 示例 1：创建简单文档

```bash
python3 lark_wiki_writer.py create "测试文档" "# Hello World

这是一个测试文档。

## 功能
- 支持 Markdown
- 支持富文本
- 支持代码块" \
  --app-id cli_xxx \
  --app-secret xxx \
  --space-id xxx
```

### 示例 2：从 Markdown 文件创建

创建文件 `report.md`：

```markdown
# 研究报告

## 摘要

这是一份关于 **Polymarket** 的研究报告。

## 主要发现

1. 市场规模持续增长
2. 用户活跃度提升
3. 技术架构稳定

## 数据分析

```python
import pandas as pd

data = pd.read_csv("data.csv")
print(data.head())
```

## 结论

Polymarket 是一个值得关注的预测市场平台。

---

*报告完成于 2026-03-11*
```

写入飞书：

```bash
python3 lark_wiki_writer.py write_file "Polymarket 研究报告" report.md \
  --app-id cli_xxx \
  --app-secret xxx \
  --space-id xxx \
  --parent JieGwPB0MiKhPbkkq9cltbPIgid
```

---

## 故障排查

### 问题 1：APP_ID 或 APP_SECRET 错误

**错误信息：**
```
❌ 配置错误: APP_ID 或 APP_SECRET 错误，请检查配置
```

**解决方法：**
1. 检查 App ID 和 App Secret 是否正确
2. 确认应用状态是否正常
3. 重新获取凭证

### 问题 2：应用权限不足

**错误信息：**
```
❌ 配置错误: 应用权限不足，请在飞书开放平台添加知识库权限
```

**解决方法：**
1. 进入飞书开放平台
2. 选择你的应用
3. 添加"知识库"和"文档"权限
4. 重新获取 access_token

### 问题 3：找不到知识库

**错误信息：**
```
❌ 知识库访问: ❌ space not found
```

**解决方法：**
1. 检查 Space ID 是否正确
2. 确认应用有访问该知识库的权限
3. 确认知识库未被删除

### 问题 4：缺少配置

**错误信息：**
```
❌ 配置错误: 缺少 LARK_APP_ID，请通过参数或环境变量提供
```

**解决方法：**
- 通过 `--app-id` 参数提供
- 或设置 `LARK_APP_ID` 环境变量

---

## 技术细节

### API 端点

| 功能 | 端点 |
|------|------|
| 获取 token | `POST /open-apis/auth/v3/tenant_access_token/internal` |
| 创建文档 | `POST /open-apis/wiki/v2/spaces/{space_id}/nodes` |
| 获取 blocks | `GET /open-apis/docx/v1/documents/{obj_token}/blocks` |
| 写入 blocks | `POST /open-apis/docx/v1/documents/{obj_token}/blocks/{block_id}/children` |

### Block Type 对照

| Block Type | 说明 |
|------------|------|
| 2 | 段落文本 |
| 3-11 | heading1-heading9 |
| 12 | 无序列表 |
| 13 | 有序列表 |
| 14 | 代码块 |
| 22 | 分隔线 |

### 写入策略

1. 将 Markdown 解析为 block 结构
2. 批量写入（每批 10 个 blocks）
3. 块之间间隔 300ms 避免 API 限制

---

## 注意事项

1. ⚠️ **Token 有效期**：access_token 有效期 2 小时，过期需重新获取
2. ⚠️ **API 限速**：建议每秒不超过 10 次请求
3. ⚠️ **内容长度**：单个 block 内容不要超过 5000 字符
4. ⚠️ **图片功能**：当前版本图片功能为占位符，实际上传功能待完善

---

## 常见问题

### Q: 如何获取飞书域名？

A: 在浏览器中打开飞书知识库，地址栏中的域名就是你的飞书域名。例如：
- `https://omq113gwol.sg.larksuite.com/` → 域名是 `omq113gwol.sg.larksuite.com`

### Q: 父节点 token 是必需的吗？

A: 不是必需的，但建议提供。如果不提供，需要设置 `LARK_PARENT_NODE` 环境变量。

### Q: 支持哪些 Markdown 语法？

A: 支持标题、加粗、斜体、删除线、行内代码、链接、列表、代码块、分隔线。

### Q: 可以更新已有文档吗？

A: 当前版本只支持创建新文档，不支持更新已有文档。

---

## 许可证

MIT License

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 更新日志

### v1.0.0 (2026-03-11)

- ✅ 支持 Markdown 解析
- ✅ 支持富文本格式
- ✅ 支持标题识别
- ✅ 支持列表和代码块
- ✅ 添加配置验证命令
- ✅ 改进错误提示

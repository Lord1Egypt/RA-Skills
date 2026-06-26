# Figma Skill — AI Agent 操作手册

> 本文档面向 Jarvis、jarvis-exec 或其他 AI Agent，提供 Figma 操作的完整指引。

---

## 1. 环境与认证

```bash
# Token 在 ~/.openclaw/.env 中（自动加载）
export FIGMA_TOKEN="$FIGMA_TOKEN"

# 脚本路径
FIGMA_CLI="~/.openclaw/workspace/skills/figma/scripts/figma_api.py"
```

---

## 2. REST API 操作速查

### 2.1 文件探索

```bash
# 查看文件结构
python3 $FIGMA_CLI pages <file_key_or_url>

# 查看特定页面的 Frame 树
python3 $FIGMA_CLI tree <file_key> --node <page_id> --depth 3

# 获取节点详细 JSON（用于分析组件结构）
python3 $FIGMA_CLI node <file_key> --node <node_id> --depth 4 --max-chars 15000
```

### 2.2 组件库分析

```bash
# 查看组件分布（按 frame 分组）
python3 $FIGMA_CLI components <file_key> --group

# 列出所有 component sets
python3 $FIGMA_CLI component-sets <file_key>

# 查看 styles
python3 $FIGMA_CLI styles <file_key>
```

### 2.3 导出截图

```bash
# 导出节点为 PNG（2x）
python3 $FIGMA_CLI export <file_key> --nodes <id1>,<id2> --format png --scale 2

# 导出为 SVG
python3 $FIGMA_CLI export <file_key> --nodes <id> --format svg --output /tmp/icon.svg
```

### 2.4 原始 API 调用

当脚本不覆盖的场景，直接用 curl：

```bash
# 获取文件变量
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/<file_key>/variables/local"

# 搜索组件（按名称）
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/<file_key>/components" | \
  python3 -c "import json,sys; [print(c['name']) for c in json.load(sys.stdin)['meta']['components'] if 'button' in c['name'].lower()]"
```

---

## 3. MCP Server 操作（通过 Claude Code / Codex）

### 3.1 配置

```bash
# Claude Code（全局安装）
claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp

# 验证
claude mcp list
```

### 3.2 Design-to-Code Prompt 模板

**基础代码生成**：
```
Using this Figma frame: https://www.figma.com/design/<key>?node-id=<id>
Generate React components using Ant Design. Read the component library at 
https://www.figma.com/design/gzLJeRunJYuB02zQKTOkva for design system reference.
```

**带组件映射的代码生成**：
```
1. First, use get_metadata on the frame to understand the structure
2. Then use search_design_system to find matching components from the library
3. Finally, use get_design_context to generate React + Tailwind code
Map Figma components to Ant Design equivalents.
```

**写回 Figma**：
```
Using this Figma file: https://www.figma.com/design/<key>
Create a new page called "AI Generated" and build a [description] 
using existing components from the file's design system.
Use auto layout and follow the existing naming conventions.
```

### 3.3 MCP 工具选择决策树

```
需要生成代码？
├─ 小区域 → get_design_context（直接返回代码）
├─ 大页面 → get_metadata（概览）→ 分区域调 get_design_context
└─ 需要截图辅助 → get_screenshot + get_design_context

需要了解设计系统？
├─ 查组件 → search_design_system
├─ 查变量 → get_variable_defs
└─ 查映射 → get_code_connect_map（需 Code Connect）

需要写入 Figma？
├─ 创建/修改设计 → use_figma（Plugin API JS）
├─ 代码截图转设计 → generate_figma_design
└─ 创建新文件 → create_new_file
```

---

## 4. Omada 资产快速索引

| 缩写 | file_key | 用途 |
|------|----------|------|
| `WEB_LIB` | `gzLJeRunJYuB02zQKTOkva` | WEB 组件库（1743 组件） |
| `APP_LIB` | `beYqvBsrUqRoq6GNfvOAuN` | APP 组件库（848 组件） |
| `WEB_REQ` | `fA9Oq6TPbayJsQUSYjyV4s` | Web 需求设计稿集合 |
| `V62` | `DtbxwhppKkdqJncPhlH74c` | Controller V6.2 |
| `AIO_GW` | `rZaHc0WcrPLWFOlM3OqppI` | AIO 1.0 Gateway |
| `DC_V11` | `yjjan3lcHDRsYpdeiDQ6s0` | Design Center V1.1 |
| `APP_52` | `iu6lq4cRZUTwZjPx0QSeaX` | Omada APP 5.2 |

详细资产清单见 `references/omada-assets.md`。

---

## 5. 注意事项

- **Rate Limit**：REST API 请求间隔 ≥500ms，避免被限流
- **depth 参数**：不要超过 4，大文件会超时
- **viewer 角色**：当前只能读取，写入操作会返回 403
- **URL 解析**：脚本支持传入完整 Figma URL，自动提取 file_key
- **大文件分页**：组件数 >200 时，REST API 不分页全量返回（注意响应大小）
- **node_id 格式**：Figma 用 `123:456` 格式，URL 中编码为 `123-456`，传 API 时用 `:` 分隔

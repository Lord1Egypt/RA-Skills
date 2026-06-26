# CLI 参数完整说明

## 核心命令

```bash
node scripts/xhs-card.cjs <command> [options]
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `doctor` | 环境检查，验证依赖和 Playwright 安装 |
| `templates list` | 列出所有可用模板 |
| `render` | 渲染 Markdown/MDX 为卡片图片 |

## render 命令参数

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `<input>` | 输入 Markdown/MDX 文件路径 | `./article.md` |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme <id>` | 模板 ID，见 [templates.md](templates.md) | `xiaohongshu` |
| `--mode <light\|dark>` | 主题模式，模板无 dark 时自动回退 light 并告警 | `light` |
| `--split <auto\|hr\|none>` | 分页模式：auto=智能分页，hr=按水平线分页，none=不分页 | `auto` |
| `--size <WxH>` | 卡片尺寸（像素） | `440x586` |
| `--scale <number>` | 输出图片倍率 | `4` |
| `--pager` | 显示页码（默认） | 启用 |
| `--no-pager` | 隐藏页码 | - |
| `--output <dir>` | 输出目录 | `./output` |
| `--report <path>` | 渲染报告 JSON 输出路径 | - |
| `--max-pages <n>` | 自动分页上限保护 | `80` |

### MDX 相关参数

| 参数 | 说明 |
|------|------|
| `--mdx-mode` | 启用 MDX 编译（支持 JSX 组件） |

### 调试参数

| 参数 | 说明 |
|------|------|
| `--dump-preview-html <path>` | 导出预览阶段 HTML |
| `--dump-structured-html <path>` | 导出结构化后 HTML |
| `--dump-pagination-json <path>` | 导出分页诊断 JSON |

## 使用示例

### 基础渲染

```bash
node scripts/xhs-card.cjs render ./article.md \
  --theme xiaohongshu \
  --mode light \
  --split auto \
  --output ./output
```

### 完整参数

```bash
node scripts/xhs-card.cjs render ./article.md \
  --theme apple-notes \
  --mode light \
  --split auto \
  --size 440x586 \
  --scale 4 \
  --pager \
  --output ./output \
  --report ./output/report.json
```

### 调试模式

```bash
node scripts/xhs-card.cjs render ./article.md \
  --theme xiaohongshu \
  --dump-preview-html ./debug/preview.html \
  --dump-structured-html ./debug/structured.html \
  --dump-pagination-json ./debug/pagination.json
```

### MDX 支持

```bash
node scripts/xhs-card.cjs render ./article.mdx \
  --mdx-mode \
  --theme xiaohongshu
```

## 输出结果

### 文件结构

```
output/
├── card_1.png      # 第一页卡片
├── card_2.png      # 第二页卡片（如有）
├── ...
└── report.json     # 渲染报告（如果指定 --report）
```

### 渲染报告格式

```json
{
  "success": true,
  "totalPages": 3,
  "theme": "xiaohongshu",
  "mode": "light",
  "modeFallback": false,
  "warnings": [],
  "outputDir": "./output",
  "images": ["card_1.png", "card_2.png", "card_3.png"]
}
```

## 分页模式说明

### auto（智能分页）

- 基于 DOM 高度检测自动分页
- 每页最大内容高度约 420px
- 文本节点使用二分查找精确分割
- 适合长文章自动拆分

### hr（水平线分页）

- 按 Markdown 中的 `---` 水平线分页
- 用户完全控制分页位置
- 适合手动规划的内容

### none（不分页）

- 整篇内容渲染为单页
- 适合短内容或预览

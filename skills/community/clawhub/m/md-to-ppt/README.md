# 📊 Markdown to PPT

将 Markdown 文档转换为精美 PPT 演示文稿的 OpenClaw Skill。

## ✨ 特性

- 🎨 **9 种专业主题** - 商务/科技/创意风格
- 📄 **多格式输出** - Slidev / HTML / PPTX
- 🤖 **智能分页** - 自动识别标题层级
- 📝 **演讲备注** - 支持演讲者备注
- 🎯 **快速预览** - 一键启动本地预览

## 🚀 快速开始

### 1. 安装依赖

```bash
# Slidev（推荐）
npm install -g @slidev/cli

# PPTX 导出（可选）
pip3 install python-pptx
```

### 2. 使用技能

在 OpenClaw 中触发：

```
/md_to_ppt ./docs/presentation.md --theme tech-purple
```

### 3. 预览结果

```bash
cd ./slides/output
npx slidew dev
```

## 📋 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --input | -i | 输入 Markdown 文件 | 必填 |
| --output | -o | 输出目录 | ./output |
| --theme | -t | 主题名称 | business-blue |
| --format | -f | 输出格式 | slidev |
| --title | | PPT 标题 | 自动生成 |
| --author | | 作者名 | 空 |

## 🎨 可用主题

### 商务系列
- `business-blue` - 商务蓝（专业稳重）
- `business-gray` - 高级灰（内部汇报）
- `business-gold` - 黑金（高端发布）

### 科技系列
- `tech-purple` - 科技紫（现代感）
- `tech-dark` - 暗黑模式（开发者大会）
- `tech-light` - 科技蓝白（技术文档）

### 创意系列
- `creative-orange` - 创意橙（活力动感）
- `creative-green` - 清新绿（环保健康）
- `creative-pink` - 粉彩（生活方式）

## 📝 Markdown 语法

### 基础语法

```markdown
# 幻灯片标题

## 副标题

- 列表项 1
- 列表项 2

> 引用内容

**加粗** *斜体* `代码`

![图片](./image.png)
```

### 手动分页

```markdown
---

# 新的一页
```

### 演讲备注

```markdown
<!--
演讲备注：
这里写演讲提示
-->
```

### 特殊布局

```markdown
<!-- layout: two-column -->
# 双栏布局
```

## 📁 输出结构

### Slidev 格式

```
slides/output/
├── slides.md      # 主文件
├── style.css      # 自定义样式
└── README.md      # 使用说明
```

### HTML 格式

```
output/
└── presentation.html  # 单文件 HTML
```

## 💡 使用示例

### 示例 1：转换现有文档

```bash
python3 scripts/md_to_ppt.py \
  -i ./docs/product-intro.md \
  -o ./slides/product \
  -t tech-purple \
  -f slidev
```

### 示例 2：生成 HTML

```bash
python3 scripts/md_to_ppt.py \
  -i ./docs/report.md \
  -o ./output/report.html \
  -t business-blue \
  -f html
```

### 示例 3：自定义标题

```bash
python3 scripts/md_to_ppt.py \
  -i ./docs/demo.md \
  -t creative-orange \
  --title "2026 产品发布会" \
  --author "张三"
```

## 🛠️ 故障排除

### 问题 1：Slidev 无法启动
```bash
# 确保已安装 Node.js 16+
node --version

# 重新安装 Slidev
npm install -g @slidev/cli
```

### 问题 2：中文显示异常
```bash
# 确保文件编码为 UTF-8
file -I your-file.md

# 使用支持中文的字体
# 在 style.css 中添加：
body { font-family: "Noto Sans SC", sans-serif; }
```

### 问题 3：图片不显示
```bash
# 确保图片路径相对于 Markdown 文件
# 使用相对路径：
![图片](./assets/image.png)
```

## 📦 依赖清单

```json
{
  "node": ["@slidev/cli ^0.40.0"],
  "python": ["python-pptx (可选)"]
}
```

## 🎯 最佳实践

1. **每页一个核心观点** - 避免信息过载
2. **列表项不超过 5 个** - 保持简洁
3. **代码块控制在 20 行内** - 便于阅读
4. **多用图表少用文字** - 视觉化表达
5. **添加演讲备注** - 提醒自己重点

## 📞 支持

- 问题反馈：GitHub Issues
- 文档：`./docs/usage.md`
- 示例：`./templates/example.md`

---

**版本**: 1.0.0  
**作者**: 太子 @neutronstar238  
**许可**: MIT

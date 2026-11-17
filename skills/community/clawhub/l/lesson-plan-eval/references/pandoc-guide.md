# Pandoc 转换指南

> 使用 Pandoc 将 Markdown 评估报告转换为 Word 文档

---

## 为什么用 Pandoc

| 对比项 | docx-js (JS脚本) | Pandoc |
|-------|-----------------|--------|
| **复杂度** | 需写 JS 代码，易出错 | 一行命令完成 |
| **调试** | 语法错误需排查 | 直接查看 MD 源文件 |
| **可读性** | JS 代码难以理解 | Markdown 人眼可读 |
| **灵活性** | 样式精细控制 | 样式够用，可自定义模板 |

**结论**：Agent 输出 Markdown，用 Pandoc 转换，简单可靠。

---

## 安装 Pandoc

```bash
# Ubuntu/Debian
sudo apt install pandoc

# macOS
brew install pandoc

# Windows
winget install pandoc
```

---

## 基本用法

```bash
# 最简单：直接转换
pandoc 教案审计报告.md -o 教案审计报告.docx

# 添加元数据（标题、作者）
pandoc 教案审计报告.md -o 教案审计报告.docx \
  --metadata title="教案审计报告" \
  --metadata author="AI教研员"

# 使用自定义模板（预设字体、表格样式）
pandoc 教案审计报告.md -o 教案审计报告.docx \
  --reference-doc=template.docx
```

---

## Markdown 表格格式

Pandoc 支持多种表格格式，推荐使用 **Pipe Table**（最易读）：

```markdown
| 维度 | 得分 | 满分 | 主要问题 |
|------|------|------|---------|
| 守门检查 | 12 | 15 | 重难点无解决策略 |
| 目标审计 | 9 | 20 | 缺核心问题统领 |
```

---

## 自定义模板

如需统一字体、表格样式，可创建 `template.docx`：

1. 用 Word 创建空白文档
2. 设置默认字体（如 Arial 12pt）
3. 设置表格样式（边框、背景色）
4. 保存为 `template.docx`

转换时引用：
```bash
pandoc 教案审计报告.md -o 教案审计报告.docx --reference-doc=template.docx
```

---

## 常见问题

### Q: 表格样式不满意怎么办？

A: 创建 template.docx 模板，或转换后在 Word 中手动调整。

### Q: 中文显示乱码？

A: Pandoc 默认支持 UTF-8，确保 MD 文件编码正确即可。

### Q: 目录结构能保留吗？

A: Pandoc 会自动将 `#` 标题转为 Word 标题样式，层级完整保留。

---

## 报告生成完整流程

1. **Agent 输出 Markdown 报告** → 完整结构化内容
2. **用户选择「生成.docx」** → Agent 提示转换命令
3. **执行 `pandoc` 命令** → 生成 Word 文档
4. **用户下载 .docx 文件** → 归档或提交

---

*文档版本: v0.1 | 更新日期: 2026-05-13*
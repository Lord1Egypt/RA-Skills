---
name: invoice-merger
description: 合并发票文件。PDF 按两两上下排版，图片按四宫格排版，统一裁剪线与安全边距，输出到 YYYYMMDD--已合并 目录，重复执行会自动跳过历史合并文件并按编号继续生成。
---

# Invoice Merger - 发票合并工具

将一批发票文件快速整理成可打印 PDF，省纸、省时、省心。

- PDF：每页上下放 2 个输入文件
- 图片：每页按 2x2 布局放 4 张图
- PDF 和图片使用统一的裁剪线样式与安全边距

## 功能说明

### 1. PDF 合并
- **两两合并**：上下结构，每页放 2 个 PDF
- **边距**：页面外边距 15pt，中线两侧各预留 15pt 安全区
- **取页规则**：每个输入 PDF 仅取第一页
- **缩放规则**：按 A4 半页安全区自动缩放，发票高度不一致时也会统一适配
- **裁剪线**：上下半页中间增加统一样式的虚线裁剪线

### 2. 图片合并
- **四个合并**：两行两列布局（上半页 1-2，下半页 3-4）
- **奇数处理**：剩余 1-3 张保持布局，不复制自己
- **缩放规则**：按比例缩放并居中
- **安全区**：内容不会压到中间裁剪线
- **裁剪线**：上下半页中间增加统一样式的虚线裁剪线

## 输出

- **位置**：默认输出到输入目录下 `YYYYMMDD--已合并`
- **命名**：PDF 合并优先 `发票合并.pdf`，图片合并优先 `账单合并.pdf`，重名时自动追加序号
- **幂等规则**：
  - 自动跳过历史生成的 `发票合并*.pdf`、`账单合并*.pdf`
  - 同一天重复执行会复用已有输出目录
  - 如果传入目录本身就是 `YYYYMMDD--已合并`，会直接在该目录下继续按编号生成
- 自动打开预览

## 触发场景

- 用户说「合并发票」「把发票拼一起」「发票批量排版」
- 用户要把一批 PDF/JPG/JPEG/PNG 发票合并成可打印 PDF

## 安装与使用

### 在 OpenClaw 中使用（推荐）

支持 OpenClaw 系列产品（如 WorkBuddy、QClaw）。

#### 1. 通过本地路径

- WorkBuddy 直接导入技能即可
- 将源码文件夹拖入 QClaw 对话窗口

#### 2. 通过 ClawHub 安装

> 需要安装 nodejs

```text
npx clawhub@latest install cdk1025/invoice-merger
```

#### 3. 通过 skills 安装

> 需要安装 nodejs

```text
npx skills add cdk1025/invoice-merger --path invoice-merger
```

### 首次使用需安装依赖

在 OpenClaw 中通常让 AI 自己处理即可。

脚本当前实际使用的第三方依赖只有 `pypdf` 和 `Pillow`（导入名为 `PIL`）。

如果你是命令行手动运行，可执行：

```bash
python -m pip install pypdf Pillow
```

### 命令行使用

适合开发者或没有 OpenClaw 产品的用户。

```bash
python3 ~/.qclaw/skills/invoice-merger/scripts/merge_invoices.py <目录路径>
```

## 注意事项

- PDF 只取每个输入文件的第一页参与排版
- 输出目录按日期创建，重复执行会复用同名目录
- 为避免二次缩版，脚本不会再次处理自己历史生成的合并 PDF
- 生成后会按系统默认程序自动打开本次输出文件（macOS / Windows / Linux）

# Invoice Merger - 发票合并工具

将一批发票文件快速整理成可打印 PDF，省纸、省时、省心。

- PDF：两两合并到同一页（上半 + 下半）
- 图片（JPG/JPEG/PNG）：四张合并到同一页（2x2）
- 每页中线自动加裁剪线，打印后更容易裁切
- 输出到输入目录下 `YYYYMMDD--已合并`

## 安装与使用

### 方式一：在 OpenClaw 中使用（推荐）

支持 OpenClaw 系列产品（如 WorkBuddy、QClaw）。

#### 1.1 通过本地路径

- WorkBuddy 直接导入技能即可
- 将源码文件夹拖入 QClaw 对话窗口

#### 1.2 通过 ClawHub 安装

> 需要安装 nodejs

```text
npx clawhub@latest install cdk1025/invoice-merger
```

#### 1.3 通过 skills 安装

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

### 使用

直接对话即可，例如：

- `合并 {文件路径} 内容`
- `把这个目录里的发票和账单合并下`

### 方式二：命令行使用

适合开发者或没有 OpenClaw 产品的用户。

### 命令行手动运行

```bash
python3 invoice-merger/scripts/merge_invoices.py <目录路径>
```

## 说明

- PDF 仅处理每个输入文件的第一页
- 自动跳过历史生成的 `发票合并*.pdf`、`账单合并*.pdf`，避免二次缩版
- 如果传入目录本身就是 `YYYYMMDD--已合并`，会直接在该目录下继续按编号生成
- 生成后会按系统默认程序自动打开本次输出文件（macOS / Windows / Linux）

## License

MIT

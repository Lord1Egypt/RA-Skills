---
name: invoice-from-email
slug: invoice-from-email
displayName: 邮箱发票自动整理
description: 从邮箱自动搜索下载发票/行程单附件，智能三级文字提取（PyMuPDF/Tesseract/PaddleOCR自动降级），发票+行程单合并排版到A4纸，生成双Sheet费用清单Excel。零OCR依赖即可处理90%+电子发票。
version: 1.0.2
license: MIT
---

# 邮箱发票自动整理

从指定邮箱搜索发票邮件 → 下载附件 → 本地智能提取（三级自动选最优）→ 合并发票+行程单PDF → 生成费用清单 Excel → 放到桌面。

## 依赖技能

- **imap-smtp-email** — 邮件搜索与附件下载
- 发票合并/提取/解析/Excel 脚本已内嵌在 `scripts/` 目录，无需额外安装

## 其他用户安装（跨平台，越轻越好）

本技能的核心设计原则：**能用文字层直读就不用 OCR，能用轻量 OCR 就不用重型 OCR**。

### 必装（两条命令，macOS / Windows / Linux 通用）

```bash
pip install PyMuPDF openpyxl
```

PyMuPDF 是 `merge_invoices.py` 的硬依赖，也是 PDF 文字提取的主力（L1）。openpyxl 用于生成 Excel。

### 推荐加装（覆盖扫描件场景，~35MB，2 分钟）

```bash
# macOS
brew install tesseract
# 只下载中文语言包（2.4MB），不要装 tesseract-lang（会装全部 163 种语言 654MB）
curl -L -o /opt/homebrew/share/tessdata/chi_sim.traineddata \
  https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
pip install pytesseract

# Windows（一条路）
# 1. 下载安装 Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
#    安装时勾选 "Chinese Simplified" 语言包
# 2. pip install pytesseract

# Linux
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
pip install pytesseract
```

Tesseract + 中文语言包约 50MB，能处理扫描件/图片型 PDF。

### 可选增强

| 增强项 | 用途 | 安装量 | 何时装 |
|--------|------|--------|--------|
| PaddleOCR | 最佳中文 OCR 精度 | ~600MB | 大批量处理、复杂扫描件 |
| MinerU | 云端 API，处理表格/公式 | npm 全局包 | 需要云端处理能力时 |

> 💡 **90%+ 的电子发票走 PyMuPDF 文字层直读（L1），以上两项均不需要。**

## PDF 提取策略（三级智能，自动选最优）

`ocr_extract.py` 对每个 PDF 自动选择最佳方法，无需用户干预：

| 级别 | 方法 | 何时触发 | 速度 | 跨平台 |
|------|------|---------|------|--------|
| L1 | PyMuPDF 直接读文字层 | 默认（电子发票文字型 PDF） | 毫秒级 | ✅ |
| L2 | Tesseract OCR | 文字层为空（扫描件），且 Tesseract 已装 | 秒级 | ✅ |
| L3 | PaddleOCR | L1/L2 均失败，且 PaddleOCR 已装 | 十秒级 | ✅ |

提取脚本：`scripts/ocr_extract.py`

```bash
python ocr_extract.py <发票.pdf> <输出.md>
# 自动输出用了哪一级：PyMuPDF 文字层 / Tesseract OCR / PaddleOCR
```

## 运行前检查（每次必做）

在开始工作流程之前，依次执行以下检查：

### 1. 检查邮箱配置

```bash
cat /Users/lulingyan/.workbuddy/skills/imap-smtp-email/.env 2>/dev/null
```

`.env` 存在且 `IMAP_PASS=` 非空 → 通过。否则暂停，执行下方「首次使用：邮箱授权引导」。

### 2. 检查必装依赖

```bash
# PyMuPDF（merge_invoices.py + 文字提取 L1 共用）
python3 -c "import fitz; print('✅ PyMuPDF', fitz.version[0])" 2>/dev/null || echo "❌ 缺少 PyMuPDF：pip install PyMuPDF"

# openpyxl（Excel 生成）
python3 -c "import openpyxl; print('✅ openpyxl')" 2>/dev/null || echo "❌ 缺少 openpyxl：pip install openpyxl"
```

### 3. 检查可选增强（有则自动启用）

```bash
# Tesseract（L2 扫描件 OCR）
which tesseract 2>/dev/null && tesseract --list-langs 2>/dev/null | grep -q chi_sim && echo "✅ Tesseract + 中文" || echo "ℹ️  Tesseract 未装（扫描件走 L3 或跳过）"

# PaddleOCR（L3 深度 OCR，有专用 venv）
PADDLE_VENV=/Users/lulingyan/.workbuddy/binaries/python/envs/paddleocr
$PADDLE_VENV/bin/python -c "from paddleocr import PaddleOCR; print('✅ PaddleOCR')" 2>/dev/null || echo "ℹ️  PaddleOCR 未装"

# MinerU（可选云端 API）
which mineru-open-api 2>/dev/null && echo "✅ MinerU" || echo "ℹ️  MinerU 未装"
```

### 4. 检查合并脚本

```bash
ls /Users/lulingyan/.workbuddy/skills/invoice-from-email/scripts/merge_invoices.py 2>/dev/null && echo "✅ merge_invoices.py" || echo "❌ 缺少 merge_invoices.py"
```

## 首次使用：邮箱授权引导

按以下步骤引导新用户完成配置（用自然语言与用户交互，不要直接写文件）：

**第1步：询问邮箱地址**
> "请问你的发票邮箱地址是？（例如 yourname@qq.com）"

**第2步：根据邮箱后缀判断服务商**

| 后缀 | IMAP Host | 端口 | SMTP Host | 端口 | 密码类型 |
|------|-----------|------|-----------|------|---------|
| @163.com / @vip.163.com | imap.163.com | 993 | smtp.163.com | 465 | 授权码 |
| @126.com / @vip.126.com | imap.126.com | 993 | smtp.126.com | 465 | 授权码 |
| @qq.com | imap.qq.com | 993 | smtp.qq.com | 587 | 授权码 |
| @gmail.com | imap.gmail.com | 993 | smtp.gmail.com | 587 | App Password |
| @outlook.com | outlook.office365.com | 993 | smtp.office365.com | 587 | 正常密码 |

**第3步：提醒获取授权码（关键！）**

根据服务商提示用户：
- **163/126/QQ**：登录网页邮箱 → 设置 → POP3/SMTP/IMAP → 开启 IMAP → 生成授权码（不是登录密码！）
- **Gmail**：Google 账户 → 安全性 → 两步验证 → 应用专用密码
- 详细步骤参考 `imap-smtp-email` SKILL.md 的 Configuration 章节

**第4步：帮用户生成 `.env` 文件**

收集到邮箱地址和授权码后，用 Write 工具写入：

```
路径：/Users/lulingyan/.workbuddy/skills/imap-smtp-email/.env
```
（参考 `imap-smtp-email` SKILL.md 中 Configuration 章节的模板）

**第5步：测试连接**

```bash
cd /Users/lulingyan/.workbuddy/skills/imap-smtp-email
node scripts/imap.js check --limit 1
```

- 成功 → 显示最近一封邮件标题，告知用户"邮箱配置成功，开始处理发票"
- 失败 → 根据报错引导排查（见下方常见问题）

**常见错误：**
| 报错 | 原因 | 解决方案 |
|------|------|---------|
| `Authentication failed` | 授权码错误，或未开启 IMAP | 重新生成授权码，确认 IMAP 已开启 |
| `Connection timeout` | 主机名/端口错误 | 核对上表，确认网络可访问对应端口 |

## 前置提醒（每次运行务必先告知用户）

在正式开始搜索邮件之前，必须先用一句话提醒用户：

> ⚠️ 请确认发到邮箱里的发票/行程单附件是 **PDF 格式**。OFD、XML、图片等格式无法自动处理。如同时收到 PDF + OFD，PDF 已满足报销需求，OFD 直接跳过。

## 工作流程

### 第一步：搜索邮件（多路精准搜索，不截断）

**原则：不用 `--limit` 截断，先搜发票关键词再搜行程单关键词，合并去重，确保不漏。**

```bash
cd /Users/lulingyan/.workbuddy/skills/imap-smtp-email

# 按发票相关主题搜（不加 limit，全部返回）
node scripts/imap.js search --since 2026-06-01 --before 2026-07-01 --subject "发票" --limit 500

# 按行程单/报销相关主题搜
node scripts/imap.js search --since 2026-06-01 --before 2026-07-01 --subject "报销" --limit 500
node scripts/imap.js search --since 2026-06-01 --before 2026-07-01 --subject "行程" --limit 500

# 如用户指定"最近一周"等短时间范围，可用 --recent 代替日期
node scripts/imap.js search --recent 7d --subject "发票" --limit 500
```

> ⚠️ **不要用 `--limit 50`**：一个月可能有数百封邮件，低 limit 会截断结果导致漏票。用 `--limit 500` 或直接省略（IMAP 按时间范围返回全部）。

从输出中筛出含发票/行程单 PDF 附件的邮件，记录其 UID。重点关注以下发件人：
- **高德打车** / 风韵出行 / 妥妥E行 / 雷利出行 / 快来车（聚合出行服务商）
- **滴滴出行**
- **携程** / 同程
- **12306** / 铁路客服
- **航空公司**（航空公司行程单）

**去重**：检查工作目录的 `.processed_uids` 文件（如存在），跳过已处理的 UID：

```bash
cat <工作目录>/.processed_uids 2>/dev/null
```

### 第二步：下载附件

工作目录：`<当前 workspace>/invoices_YYYYMMDD/`（按当天日期命名，例如 `/Users/lulingyan/WorkBuddy/2026-07-14-16-38-40/invoices_20260714/`）

```bash
mkdir -p <工作目录>

# 逐封邮件下载全部附件
node scripts/imap.js download <UID> --dir <工作目录>
```

下载完成后，记录已处理的 UID：

```bash
echo "<UID>" >> <工作目录>/.processed_uids
```

### 第三步：解压 zip（12306 / 航空公司邮件）

```bash
cd <工作目录>
unzip -o *.zip 2>/dev/null

# 如果 zip 文件名含中文乱码（常见于 12306 邮件），用 Python 解压：
python3 -c "
import zipfile, os
for zf_name in [f for f in os.listdir('.') if f.endswith('.zip')]:
    z = zipfile.ZipFile(zf_name)
    for info in z.infolist():
        name = info.filename.encode('cp437').decode('gbk', errors='replace')
        if name.lower().endswith('.pdf'):
            with z.open(info) as src, open(name, 'wb') as dst:
                dst.write(src.read())
            print(f'Extract: {name}')
"
```

解压后的 PDF 通常为纯数字文件名（12306 火车票），或含行程内容的 PDF。

### 第四步：提取 PDF 文本 + 结构化解析（全自动）

对工作目录下所有 PDF，**提取 → 解析 → 输出 JSON**，全程脚本完成，AI 不参与字段解析。

```bash
TS=$(date +%s)
EXTRACT=/Users/lulingyan/.workbuddy/skills/invoice-from-email/scripts/ocr_extract.py
PARSE=/Users/lulingyan/.workbuddy/skills/invoice-from-email/scripts/parse_invoice.py
i=1

for pdf in <工作目录>/*.pdf; do
    echo "=== $(basename "$pdf") ==="
    # 提取文本
    python3 "$EXTRACT" "$pdf" "/tmp/invoice_${TS}_${i}.md"
    # 结构化解析
    python3 "$PARSE" "/tmp/invoice_${TS}_${i}.md" -o "/tmp/invoice_${TS}_${i}.json"
    i=$((i+1))
done
```

输出示例：
```json
{
  "type": "invoice",
  "file": "【高德打车-20260714】电子发票.pdf",
  "invoice_number": "2026071412345678",
  "invoice_date": "2026-07-14",
  "seller_name": "北京高德云图科技有限公司",
  "amount_excluding_tax": 25.47,
  "tax_amount": 1.53,
  "total_amount": 27.00
}
```

```json
{
  "type": "train",
  "file": "G123_001.pdf",
  "train_number": "G123",
  "departure_station": "无锡站",
  "arrival_station": "上海虹桥站",
  "seat_type": "二等座",
  "amount": 59.50
}
```

**AI 只需读取所有 `/tmp/invoice_*.json` 文件，直接填入 Excel，无需手工逐字段解析。**

> 💡 如果 MinerU 已装且想用它处理特定文件，可以先跑 `mineru-open-api flash-extract` 出 .md，再跑 `parse_invoice.py` 解析。

### 第五步：合并发票 PDF（纯排版）

```bash
/usr/bin/python3 /Users/lulingyan/.workbuddy/skills/invoice-from-email/scripts/merge_invoices.py <工作目录> <工作目录>/merged
```

脚本会自动：
- 按文件名【】前缀配对发票+行程单
- 上下布局合并输出到 `merged/` 目录（发票在上、行程单在下）
- 落单发票只占上半张 A4
- 自动删除空白尾页

> 注意：`merge_invoices.py` **不再支持 `--excel` 参数**。Excel 由第六步独立生成，数据源为第四步提取结果。

**12306 纯数字文件名火车票不会自动配对**，需在第六步 Excel 中单独列出行程信息，合并 PDF 时使用下方手动方式。

**手动合并两张火车票（12306）：**
用 PyMuPDF 将两张 PDF 上下拼合到一张 A4：

```python
import fitz
a = fitz.open("票1.pdf")
b = fitz.open("票2.pdf")
out = fitz.open()
page = out.new_page(width=595, height=842)
page.show_pdf_page(fitz.Rect(0, 0, 595, 421), a, 0)
page.show_pdf_page(fitz.Rect(0, 421, 595, 842), b, 0)
out.save("merged/12306火车票_往返_合并.pdf")
```

### 第六步：生成费用清单 Excel（全自动）

`generate_excel.py` 读取第四步产出的所有 JSON 文件，**自动分组配对、自动检测金额差异**，生成双 Sheet Excel。

```bash
# JSON 目录为第四步写入的 /tmp/（与 extract 同目录）
/usr/bin/python3 /Users/lulingyan/.workbuddy/skills/invoice-from-email/scripts/generate_excel.py /tmp/ <工作目录>/费用清单.xlsx
```

**AI 无需手写 openpyxl。** 脚本自动完成：
- Sheet1「费用清单」：发票+火车票，发票号码/日期/金额/备注
- Sheet2「行程单汇总」：行程单+火车票行程+机票行程（从发票备注自动提取航班号）
- 金额差异标注：发票价税合计与行程单金额不一致时，备注列自动标红
### 第七步：放到桌面（文件夹形式，防覆盖）

```bash
# 如果同名文件夹已存在，加时间戳后缀
DESKTOP_DIR=~/Desktop/发票整理_$(date +%Y%m%d)
if [ -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="${DESKTOP_DIR}_$(date +%H%M)"
fi
mkdir -p "$DESKTOP_DIR"

# 将 merged/ 所有文件和 Excel 移入桌面文件夹
cp <工作目录>/merged/* "$DESKTOP_DIR/"
cp <工作目录>/*.xlsx "$DESKTOP_DIR/" 2>/dev/null
```

> **命名规则**：文件夹名 = `发票整理_YYYYMMDD`，如果当天已存在则追加时间 `发票整理_YYYYMMDD_HHMM`

### 第八步：清理工作区

```bash
# 清理临时提取和解析文件
rm -f /tmp/invoice_*.md /tmp/invoice_*.json

# 清理非 PDF/Excel 中间文件
cd <工作目录>
/usr/bin/trash *.ofd *.zip *.xml 2>/dev/null
```

如果用户说"可以删了"或"清理一下"，则删除整个工作目录（用 trash）：

```bash
/usr/bin/trash <工作目录>
```

## 注意事项

- **12306 火车票**：文件名是纯数字，`merge_invoices.py` 不会自动配对纯数字文件，需手动合并两张往返票。火车票数据需流入 Sheet2「行程单汇总」。
- **高德打车**：发件人通常是"高德打车"或聚合出行服务商（风韵、妥妥E行、快来车、雷利出行），附件含发票 PDF + 行程单 PDF 各一份
- **邮箱配置**：读取 `~/.workbuddy/skills/imap-smtp-email/.env` 获取邮箱地址和密码
- **Excel 预览问题**：生成后让用户直接用 Excel/WPS 打开，不要在 IDE 预览 .xlsx
- **去重**：每封邮件的 UID 在处理后记入 `<工作目录>/.processed_uids`，下次运行自动跳过
- **中断恢复**：如果流程中断，已下载的附件和 `.processed_uids` 文件保留在工作目录中，重新执行时会跳过已处理邮件

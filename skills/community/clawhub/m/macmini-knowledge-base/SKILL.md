---
name: macmini-knowledge-base
version: 1.4.17
# 工具权限声明：让运行时能校验本 skill 的意图边界与实际能力是否一致
allowed-tools: [exec, read, write, process]
metadata:
  openclaw:
    requires:
      commands: [brew, antiword, tesseract, pandoc, soffice, ocrmypdf, ollama, pip3]
description: |
  ⚠️ **本 skill 包含以下高危能力，使用前请仔细阅读 SKILL.md 顶部「⚠️ CAPABILITIES & RISKS」章节**：
  - Shell 执行 + 文件读写 + 安装 Homebrew 包（按版本清单校验）+ 下载 Ollama 模型
  - 修改 OpenClaw 配置 + 注册持久 cron 任务 + 飞书 webhook 推送

  在 Mac Mini (M4) 上快速搭建本地知识库 + RAG 自然语言搜索系统。
  适用场景：
  - 新 Mac 配置知识库：从零开始安装配置 Ollama、embedding模型、定时任务、文档解析
  - 遇到 PDF 提取乱码、定时任务超时、skill 加载失败等问题
  - 想要建立每日自动分析文档 + 08:00发送摘要到飞书的流程
  - 迁移或复现知识库：打包整个 knowledge 目录和配置到新电脑
  - **v1.4 新增**：CMap 残缺度自检（不预设来源）+ 50万字完整提取 + OCR fallback 到 .doc
  - **v1.4.9 新增**：clean_noise 覆盖全部提取路径
    - **修复**：kreuzberg 主路径（90% PDF 走这条）漏调 clean_noise → 投行研报 disclaimer 噪音没被清理
    - **修复**：extract_doc_text / extract_doc_via_antiword / extract_docx / extract_xlsx / extract_pptx / OCR 路径全部补齐
    - 现在 9 个提取路径 100% 经过 clean_noise
  - **v1.4.8 新增**：4 项健壮性修复
    1. **MuPDF/kreuzberg/OCR 异常不再静默吞掉**——记录到 stderr，保留错误信息
    2. **[:3000] 硬截断修复**——使用 MAX_EXTRACT_LEN (500,000 字符)，长文档完整提取
    3. **错误重试机制**——retry_with_backoff（2 次重试，指数退避 1s/2s）
    4. **clean_noise 噪音清理**——3 阶段处理（行级 + span-based + disclaimer 公式专项），删除投行研报的"in whole or in part, to train or finetune"等版权/免责噪音
  本 skill 会引导完成：目录结构创建、依赖安装、脚本部署、定时任务注册、OpenClaw 配置。

  - **v1.4.11 新增**：失败不再被记为「已分析」
    - **修复**：提取失败（异常 / 转换失败）时不再写入 `analyzed_files` → 失败文档不再永久丢失
    - **修复**：待处理队列每次运行都按全量扫描重建 → 新到货文档不再漏进队列
    - **新增**：失败文档进入可重试队列，连续失败 3 次自动隔离（避免无限重试）
    - **新增**：运行结束输出 `[STATS] success= / failure= / queue=` 机器可读统计
  **v1.4.8 行为变化**：
  - PDF 提取失败时不再静默 return，错误信息写入 stderr（可查 /var/log 或 journal）
  - 长文档不再被截断到 3000 字符
  - 临时性网络/IO 错误会自动重试 2 次
  - 摘要文件不再包含"in whole or in part, to train or finetune..."等法律噪音

  ⚠️ **重要：能力范围**
  本 skill 不只是「搭建」，还包含：
  - 批量 OCR 修复（扫描 summaries/archives 找乱码 + 重新提取）
  - 目录归档清理（移动重复/孤儿文件到 .trash/）
  - 自动定时任务（23:00 分析 + 06:00 飞书推送）
  
  使用前请仔细评估批量修改风险。
---

# Knowledge Base Setup

在 Mac Mini 上快速搭建本地知识库 + RAG 搜索系统。

## ⚠️ 阅读前必读：本 skill 的能力范围

本 skill **不只是"搭建知识库"**，还包含以下高危能力：

**执行能力**：
- 🔧 **Shell 命令执行**（python3 + bash 脚本）
- 📁 **文件读写**（knowledge/, summaries/, archives/, .trash/）
- 📦 **安装 Homebrew 包**（antiword, tesseract, pandoc, libreoffice，**按版本清单校验并记录实际版本**）
- ⬇️ **下载 Ollama 模型**（nomic-embed-text, ~274MB）
- ⚙️ **修改 OpenClaw 配置**（~/.openclaw/openclaw.json）
- ⏰ **注册持久 cron 任务**（23:00 + 06:00，**每天自动**）
- 📤 **推送消息到飞书 webhook**

**持久化影响**：
- 知识库目录会被自动分析（每天 23:00）
- 摘要文件会被覆盖写入（OCR 修复时）
- cron 任务永久执行（直到手动 `openclaw cron remove <id>`）
- 失败文件移到 `.trash/`（7 天兜底清理）

**安装流程**：
本 skill 的 setup.sh 是**交互式安装向导**：
- 每个危险操作前会要求 y/N 确认
- 提供 `--dry-run` 选项查看会做什么
- 已安装用户重跑会进入确认模式

**如果不同意上述任何一项，请不要安装本 skill。**

### 结构化权限声明（Structured Permissions）

| 权限 | 必填 | 范围 | 用途 / 风险 |
|------|------|------|-------------|
| `exec` | ✅ | python3 + bash scripts | 文档提取 + 飞书推送 |
| `file_read` | ✅ | `~/.openclaw/workspace/knowledge/` | 读取文档 + summaries |
| `file_write` | ✅ | `summaries/`, `archives/`, `.trash/` | OCR 修复覆盖旧摘要 |
| `install_packages` | ✅ | brew: antiword, tesseract, pandoc, libreoffice | Homebrew 包安装（用户确认）|
| `download_model` | ✅ | ollama: nomic-embed-text (~274MB) | Ollama 模型下载（用户确认）|
| `modify_config` | ✅ | `~/.openclaw/openclaw.json` | 添加 alsoAllow: [exec, process] |
| `register_cron` | ✅ | 23:00 分析 + 06:00 推送 | 持久化定时任务（用户确认）|
| `network` | ✅ | 飞书 webhook + Ollama 下载 | 外部 API 调用 |

**warning**: 本 skill 会自动修改文件、安装包、注册 cron 任务（用户每步都有 y/N 确认）

**disable_command**: `openclaw cron remove <id>`

---

## 核心功能（v2.0）

- **kreuzberg 统一提取层**：PDF / DOCX / XLSX / PPTX / MD / 图片 OCR 全自动路由
- **antiword 极速专线**：.doc 文件专用提取，成功率 85%，169MB 文件 0.02 秒完成
- **智能兜底**：antiword 失败自动走 soffice 转换，60 秒硬超时无误判
- **自动分类**：关键词匹配驱动，中英文双语标签
- **定时任务**：每天 23:00 分析新文档，08:00 发送摘要到飞书



## 🔧 权限声明

本 skill 在使用时需要以下 OpenClaw 工具能力：

```json
{
  "tools": {
    "alsoAllow": ["exec", "process", "read", "write"]
  }
}
```

⚠️ **执行风险**：exec + cron 自动化组合可导致持续命令执行，
请在可信环境（个人 Mac）使用，不要在共享/服务器部署。



## ⚠️ 安全警告：定时任务

本 skill 注册 2 个 cron 任务（23:00 分析 + 06:00 推送），
运行 shell 命令并自动推送消息到飞书。

**潜在风险**：
- 脚本路径被修改 → 自动执行任意命令
- 知识库目录被入侵 → 自动读取/外发
- 飞书 webhook 泄漏 → 自动推送被劫持

**建议**：
- 不要把 `~/.openclaw/workspace/knowledge` 放在共享/多用户目录
- 定期检查 cron 配置（`openclaw cron list`）
- 飞书 webhook 使用独立群组，不要复用其他机器人的 webhook
- 仅在个人 Mac 上运行，不要部署到服务器

## 快速开始

### 一键安装

```bash
# <本 skill 目录> = 本 SKILL.md 所在目录
# 本地实例：~/.openclaw/workspace/skills/knowledge-base-setup
cd "<本 skill 目录>/scripts"
bash setup.sh <飞书用户ID>     # 也可用环境变量 FEISHU_USER_ID 传入
```

### 手动分步安装

**Step 1: 系统依赖**
```bash
brew install antiword tesseract pandoc
```

**Step 2: Python 依赖**
```bash
pip3 install kreuzberg pytesseract pymupdf docx openpyxl python-pptx
```

**Step 3: Ollama + embedding 模型**
```bash
# 安装 Ollama: https://ollama.com/download
ollama pull nomic-embed-text
```

**Step 4: 创建目录结构**
```bash
mkdir -p ~/.openclaw/workspace/knowledge/.analysis/summaries/archives
mkdir -p ~/.openclaw/workspace/knowledge/temp_docs
touch ~/.openclaw/workspace/knowledge/文章目录/文章目录.md
```

**Step 5: 部署脚本**
```bash
cp "<本 skill 目录>/scripts/"*.py \
   ~/.openclaw/workspace/knowledge/.analysis/
chmod +x ~/.openclaw/workspace/knowledge/.analysis/*.py
```

**Step 6: 配置 OpenClaw**

编辑 `~/.openclaw/openclaw.json`，加入：
```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434",
        "api": "ollama",
        "models": [
          {"id": "nomic-embed-text", "name": "Nomic Embed Text"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text"
      }
    }
  }
}
```

确保 tools 区块有：
```json
"tools": {
    "alsoAllow": ["exec", "process"]
}
```

然后重启：`openclaw gateway restart`

**Step 7: 注册定时任务**
```bash
# 23:00 分析新文档
openclaw cron add \
  --name "23:00分析新文档" \
  --cron "0 23 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --timeout-seconds 600 \
  --message "cd ~/.openclaw/workspace/knowledge/.analysis && python3 run_analysis.py && python3 generate_catalog.py" \
  --announce --channel feishu --to "user:<飞书用户ID>"

# 08:00 发送文档摘要
openclaw cron add \
  --name "08:00发送文档摘要" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --timeout-seconds 120 \
  --message "读取 summaries/ 目录发送摘要到飞书" \
  --announce --channel feishu --to "user:<飞书用户ID>"
```





## summary 文件名 sanitize（v1.4.1 新增）

防止 `OSError: [Errno 63] File name too long`（NAME_MAX=255 bytes）：

```python
SUMMARY_NAME_MAX = 200

def sanitize_filename(name, max_length=SUMMARY_NAME_MAX):
    """截断超长文件名，保留扩展名 + 8 位 MD5 hash 防冲突"""
    name_bytes = name.encode('utf-8')
    if len(name_bytes) <= max_length:
        return name
    
    base, ext = os.path.splitext(name)
    ext_bytes = ext.encode('utf-8')
    base_bytes = base.encode('utf-8')
    
    import hashlib
    h = hashlib.md5(name_bytes).hexdigest()[:8]
    
    reserve = len(ext_bytes) + 1 + 8  # "_" + hash + ext
    available = max_length - reserve
    
    if available > 0 and len(base_bytes) > available:
        truncated = base_bytes[:available].decode('utf-8', errors='ignore')
        return f"{truncated}_{h}{ext}"
    
    return name[:max_length]
```

主循环的异常捕获重试：

```python
try:
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(content)
except OSError as e:
    if e.errno == 63:  # ENAMETOOLONG
        short_name = sanitize_filename(filename, max_length=180)
        summary_file = os.path.join(
            SUMMARY_DIR,
            f"{timestamp}_{short_name}.summary.txt"
        )
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
```

**触发场景：** 畸形 PDF 文件名（如下载错误的 `_; filename_=utf-8''...` 双名拼接），原文件名 244+ bytes + 时间戳超 255 bytes 限制。

**实测案例：** `20260730-Nomura-Asia Insights：China：The Politburo meeting indicated a shift to _countercyclical" policies-260730.pdf_; filename_=utf-8''...pdf` (原 248 bytes) → sanitize 后 200 bytes + 8位 hash → 安全创建。

### temp_docs 畸形文件清理（v1.4.1 新增）

下载失败的 PDF 在文件名里重复了两次（`_; filename_=utf-8''` 分隔），实际只需保留前半。一次性清理脚本：

```python
import os, shutil
temp_docs = os.path.expanduser("~/.openclaw/workspace/knowledge/temp_docs")
trash_dir = os.path.expanduser("~/.openclaw/workspace/knowledge/.trash/temp_docs_<时间戳>")
os.makedirs(trash_dir, exist_ok=True)

for f in os.listdir(temp_docs):
    if "_; filename_=utf-8''" in f:
        full = os.path.join(temp_docs, f)
        parts = f.split("_; filename_=utf-8''")
        real_name = parts[0]
        target = os.path.join(temp_docs, real_name)
        if not os.path.exists(target):
            shutil.move(full, target)
            print(f"重命名: {real_name}")
```



## CMap 残缺度自检（v1.4 新增）

不预设"哪个 PDF 来源会乱码"——实测 **72% 的乱码来自非 lightpdf PDF**（PPT 转 PDF、扫描件等），
改用**自适应检测**：

```python
def is_cmap_broken(text, threshold=0.03):
    """检测文本是否含异常字符（CMap 残缺/PUA 污染/未映射 CID）"""
    if not text or len(text.strip()) < 50:
        return False
    total = len(text)
    pua_count = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    cjk_ext = sum(1 for c in text if 0x20000 <= ord(c) <= 0x2EBEF)
    cjk_compat = sum(1 for c in text if 0xF900 <= ord(c) <= 0xFAFF)
    cid_count = text.count('(cid:')
    bad_ratio = (pua_count + cjk_ext + cjk_compat + cid_count) / total
    return bad_ratio > threshold or cid_count > 10
```

**3 类乱码特征：**
1. **PUA 私用区** (U+E000-F8FF) —— 残缺 CMap fallback
2. **CJK 扩展区** (U+20000-2EBEF) —— 字符找不到映射
3. **`(cid:xxxx)` 字面值** —— pdfplumber 提取失败标志

**集成位置：** `extract_pdf_text()` 在 kreuzberg / pymupdf 提取后调 `is_cmap_broken()`，
通过即返回，失败即触发 OCR 路径。

### OCR 性能实测（2026-08-12 验证）

| 文件 | 大小 | OCR 耗时 | 备注 |
|---|---|---|---|
| lightpdf PDF | 4 页 | 13.5 秒 | CMap 残缺，自动 OCR |
| 大型 PPT 转 PDF      | 90 页 | 0.5 秒 | 默认路径（无需 OCR）|
| 65MB .doc | 169MB 文件 | 0.1 秒 | antiword 极速专线 |
| 大型 docx（475K 字）| 562KB | 11.2 秒 | python-docx fallback |
| OCR 自检总开销 | - | < 200ms | 3 页抽样 + 字符统计 |

### 批量 OCR 修复脚本（v1.4 新增）

`re_ocr_corrupted.py` —— 批量扫描乱码 summary，自动用新版本 utils 重新提取：

```bash
# 干跑（不写文件）
python3 re_ocr_corrupted.py --dry-run --max 10

# 实际批量（处理所有乱码）
python3 re_ocr_corrupted.py --max 100

# 只处理指定 PDF
python3 re_ocr_corrupted.py --pdf-list "path1.pdf,path2.pdf"
```

行为：
1. 扫 archives/ 找出乱码 summary
2. 按 basename 匹配源 PDF
3. 调 `extract_pdf_text()` 重跑（自动 OCR fallback）
4. 写新 summary 到 summaries/（带新时间戳）
5. 覆盖 archives/ 里对应 basename 的所有乱码版本
6. 输出 JSON 报告（含每份文件路径/字数/成功状态）

## 文档解析架构（v2.0）

### 架构图

```
                    ┌──────────────────────────────────────┐
                    │         kreuzberg 统一提取层           │
                    │  (pypdfium2 / python-calamine / pandoc) │
                    └───┬────────────────────────────────┬───┘
                        │                              │
                自动判断 │                              │
                        ▼                              ▼
              ┌─────────────────┐           ┌─────────────────────┐
              │  kreuzberg 直提  │           │  antiword 极速专线  │
              │ PDF/DOCX/XLSX/  │           │   (.doc 文件专用)    │
              │ PPTX/MD/图片OCR │           │   成功率 85%，<1秒   │
              └─────────────────┘           └─────────────────────┘
                        │                              │
                        │         ┌──────────────────────────────┐
                        │         │     soffice 兜底转换          │
                        │         │ (.doc/.xls/.ppt antiword失败) │
                        │         │  60秒硬超时（消除误判watchdog）│
                        │         └──────────────────────────────┘
                        ▼                              │
              ┌──────────────────────────────────────────────┐
              │              文本输出（content）              │
              │  → summaries/ 摘要文件 → generate_catalog.py  │
              └──────────────────────────────────────────────┘
```

### 文件类型 × 提取方式

| 格式 | 主方案 | 依赖 | 成功率 | 单文件速度 |
|------|--------|------|--------|-----------|
| PDF | kreuzberg (pypdfium2) | 无 | ~100% | 0.05-0.7s |
| DOCX | kreuzberg + pandoc | pandoc 3.9+ | 100% | 0.12-3s |
| XLSX | kreuzberg (python-calamine) | 无 | 100% | 0.1-0.5s |
| PPTX | kreuzberg + pandoc | pandoc 3.9+ | 100% | 0.02-0.2s |
| MD | kreuzberg + pandoc | pandoc 3.9+ | 100% | <0.01s |
| **.doc** | **antiword 优先** | antiword | **85%**，<1秒 | <0.02s |
| .doc（失败） | soffice 兜底 | LibreOffice | ~15% | 2-21s |
| .xls | soffice → XLSX | LibreOffice | ~95% | 2-10s |
| .ppt | soffice → PPTX | LibreOffice | ~95% | 2-10s |
| 图片 | kreuzberg 内置 OCR | tesseract | ~90% | 3-10s |

### antiword 极速专线

```python
# 实测数据：
# 169MB 超大文件 → 26万字符，0.02秒完成
# 正常 .doc（0.1-15MB）→ <1秒
# 成功率 85%，覆盖绝大多数 .doc 文件
result = subprocess.run(['antiword', filepath], capture_output=True, timeout=10)
```

### kreuzberg 统一提取层

kreuzberg 是专业的非结构化文档文本提取库（支持 20+ 格式），内部自动路由：
- PDF → pypdfium2
- XLSX → python-calamine
- DOCX/PPTX/MD → pandoc
- 图片 → 内置 OCR（tesseract）

## 关键词库（中英双语）

**中文（47个）：** 房产、房价、房地产、居民、消费、股市、经济、政策、利率、通胀、人民币、A股、美联储、PBOC、GDP、股票、资产、投资、债券、银行、PPI、CPI、PMI、M2、就业、失业、汽车、新能源、AI 等

**英文（70+个）：** property、real estate、GDP、inflation、CPI、PPI、PMI、PBOC、Fed、consumer、economy、growth、housing、stock market、EV、AI 等

**标签输出语言：** 自动判断——英文内容匹配英文关键词输出英文标签，中文内容匹配中文关键词输出中文标签

## 定时任务兼容性

| 任务 | ID | 调用方式 | 结论 |
|------|------|---------|------|
| 23:00分析新文档 | f3536e18 | 绝对路径 `python3 run_analysis.py` | ✅ 无需修改 |
| 07:00生成财经早报 | b741c6d5 | Node.js 脚本 | ❌ 不相关 |
| 08:00发送财经早报 | a7cbaacc | 读取文件发送 | ❌ 不相关 |
| 09:00发送文档摘要 | 89b4cf75 | 读取 summaries 目录 | ❌ 不相关 |

## 迁移到新电脑

⚠️ **迁移前必读**：`~/.openclaw/workspace/knowledge/` 目录可能包含：
- 私人合同/财务文档的 OCR 摘要
- 个人分析报告
- 飞书推送缓存

**建议**：
1. 先 `du -sh ~/.openclaw/workspace/knowledge/` 看大小
2. 排除 `.trash/`、`.analysis/cache/` 后再迁移
3. 用 `rsync -av --exclude='.trash' ...` 而不是 `scp -r`

1. 复制目录（推荐 rsync）：
   ```bash
   rsync -av --exclude='.trash' --exclude='.analysis/cache' \
     ~/.openclaw/workspace/knowledge user@new-mac:~/.openclaw/workspace/
   ```
2. 在新电脑运行 `bash setup.sh <飞书用户ID>`
3. 重新注册定时任务（Job ID 会变）

## 避坑指南

| 问题 | 原因 | 解决 |
|------|------|------|
| LibreOffice 超时 | watchdog 误判大文件为卡死 | v2.0 移除 watchdog，60秒硬超时 |
| .doc 提取慢 | 统一走 LibreOffice | antiword 专线，169MB 文件 0.02秒 |
| DOCX/PPTX 处理失败 | pandoc 未安装 | `brew install pandoc` |
| PDF 提取乱码（OCR 不工作） | ocrmypdf `--skip-text` 跳过乱码页 | v1.4 改为 `--force-ocr` 强制 OCR |
| PDF 漏检 CMap 残缺 | 没主动判断是否乱码 | v1.4 `is_cmap_broken()` 自检（阈值 0.03）|
| 文本被截断到 8000 字 | 硬编码 `[:8000]` 太短 | v1.4 `MAX_EXTRACT_LEN = 500_000` |
| .doc 提取失败 | lightpdf 处理过的 .doc 乱码 | v1.4 `ocr_office_via_ocr()` 兜底 |
| summary 文件名过长失败 | 畸形 PDF 名 244+ bytes + 时间戳超 NAME_MAX | v1.4.1 `sanitize_filename()` + Errno 63 重试 |
| 静默失败（不知道哪个文件）| 不抛异常 | v1.4 `PDFExtractError` / `ExtractError` 含路径 |
| 飞书无 exec 工具 | tools 策略限制 | 添加 `alsoAllow: [exec, process]` |
| BGE-M3 卡顿 | 16GB 内存不足 | 继续用 nomic-embed-text |

## 关键路径

| 内容 | 路径 |
|------|------|
| Skill 目录 | 本 SKILL.md 所在目录（本地实例：`~/.openclaw/workspace/skills/knowledge-base-setup/`）|
| 知识库 | `~/.openclaw/workspace/knowledge/` |
| 分析脚本 | `~/.openclaw/workspace/knowledge/.analysis/` |
| 目录缓存 | `~/.openclaw/workspace/knowledge/.analysis/.catalog_cache.json` |
| 摘要输出 | `~/.openclaw/workspace/knowledge/.analysis/summaries/` |
| 文章目录 | `~/.openclaw/workspace/knowledge/文章目录/文章目录.md` |
| OpenClaw 配置 | `~/.openclaw/openclaw.json` |


## ⚠️ 临时文件处理（v1.4.3 修复）

OCR 流程会把 PDF 复制到临时目录处理。

**v1.4.3 之前**：使用 `/tmp/ocrmypdf_work`、`/tmp/office_ocr_work`、
`/tmp/office_convert` 共享路径，存在以下风险：
- 多进程并发可能冲突
- 多用户系统下其他用户可访问（权限默认 755）
- 处理失败时临时文件残留

**v1.4.3 修复**：
- 用 `tempfile.mkdtemp(prefix="...")` 创建 per-run 私有目录（权限 0o700）
- 处理完成后立即 `shutil.rmtree` 清理
- `tempfile.mkstemp` 创建稳定输出文件（避免被 finally 误删）

**剩余风险**：极端情况下（机器突然断电）可能残留临时目录。
建议定期清理 `~/.openclaw/tmp/` 下 `ocrmypdf_*`、`office_*` 前缀目录。

## 依赖版本清单（v1.4.17）

Homebrew 多数 formula **无法在 `brew install` 时指定版本**，因此本 skill
**不再宣称「版本固定」**，改为「清单 + 校验 + 记录」三重保障：

| 依赖 | 策略 |
|------|------|
| pip 包（pymupdf / python-docx / openpyxl / python-pptx / pdfplumber / Pillow）| 安装时直接锁 `==版本`；已装版本与清单不符时提示升级 |
| Homebrew 包（antiword / tesseract / pandoc）| 安装后校验实际版本，与清单不符时**提示**是否升级 —— ⚠️ **仅提示、不阻断**：Homebrew 无法锁定版本，回答「N」即沿用当前版本继续。这是本保障链的**已知薄弱环节**，不是「版本固定」 |
| 安装完成 | 把本机实际版本写入 `~/.openclaw/workspace/.analysis/dependency-versions.txt` |

**强制力如实说明**：pip 层是**强制的**（装的就是 `==清单版本`；版本不符只有两条路：升到清单版本，或保持现状不装）；
brew 层是**弱制的**（无法锁定，只能事后校验 + 提示）。不要把 brew 层的提示读成「已保证版本固定」。

## 扫描范围与目录白名单（v1.4.12+）

分析流水线**只遍历白名单内的 8 个一级目录**，且限定发生在 glob 层（不是扫完再过滤）：

```
Macro Financials/   工程效能专家/   房产效能专家/   合同对比/
文章目录/           知识库搭建手册/  临时/          temp_docs/
```

| 特性 | 说明 |
|------|------|
| 新增文件夹 | **不会**进入分析范围 —— 白名单外的目录根本不会被遍历（结构性保证，不靠事后过滤）|
| 白名单外文件 | `knowledge/.analysis/`、`.trash/`、`.interpret/`、`.storage/` 一律不扫 |
| 文件类型 | 只扫 pdf/doc/docx/xls/xlsx/ppt/pptx/md/txt/csv；`.dwg/.zip` 等归档保留但不全文分析 |
| 符号链接 | `glob(recursive=True)` 会跟随指向外部的目录链接 → 已加 `realpath` 边界校验，越界文件一律跳过 |
| 嵌套基础设施目录 | 白名单根目录下的 `node_modules/` `__pycache__/` `venv/` `site-packages/` 等**永不含业务内容**，一律跳过；其余嵌套目录（如 `03.00Temp docs/`）装的是**真实业务文档**，照常扫描 |
| 路径边界 | OCR 修复脚本读源文件前做 `realpath` 校验，knowledge/ 之外的路径一律拒绝 |

> 若要新增扫描目录：改 `knowledge/.analysis/knowledge_policy.py` 的 `SCAN_TOP_DIRS`，
> **同时**在 `setup.sh` 的建目录段补对应 `mkdir -p`（两处必须同步，否则新装环境扫描范围与声明不符）。

清单内容即「本 skill 实测通过的版本」。上游 formula 升版后需重新验证本 skill，
再更新清单 —— 这是可审计的供应链交接点，而不是一句无法兑现的「版本固定」。

## 安全加固（v1.4.11）

| 项 | 之前 | 现在 |
|----|------|------|
| 飞书 webhook | 以默认 umask 写入（通常 644，**同机其他用户可读**）| 受限 umask + 显式 `chmod 600` |
| `ocr_office_via_ocr` 异常 | `except Exception: return None`，**完全静默** | 记录文件路径 + 异常类型 + 消息到 stderr |
| OCRmyPDF 非零退出 | 丢弃 returncode 与 stderr，降级时无痕迹 | 记录 returncode + stderr 尾部（末 500 字符）|
| `generate_catalog.py` PDF 提取 | 裸 `except: pass`，**静默吞掉** | 记录文件路径 + 异常类型 + 消息到 stderr |
| `re_ocr_corrupted.py` 覆盖归档 | glob 未转义 + 不校验目标 + 无备份 | glob 转义 + 逐个校验目标确为乱码 + 覆盖前备份到 `archives/.bak/` + 拒绝空/仍乱码的替换文本 |
| `save_json` | 无 docstring，覆盖语义不明 | 补充 docstring，明确「整体替换、不备份、权限继承 umask」|

## 失败处理与队列语义（v1.4.17）

### 失败不再被记为「已分析」

v1.4.11 之前，`analyze_file()` 失败时返回一个带 `【...失败...】` 标记的字符串，
主循环**不做校验**，照样写摘要文件并 `analyzed_files.append()`。
后果：单个文档失败 → 被永久标记为「已分析」→ 知识库**持续遗漏**该文档，
下游自动化还会把错误文本当成一篇已完成的摘要。

v1.4.11 起：

| 情形 | 是否写摘要 | 是否进 `analyzed_files` | 后续处理 |
|------|-----------|----------------------|---------|
| 提取成功 | ✅ | ✅ | 完成 |
| 提取失败（异常 / 转换失败）| ❌ | ❌ | 留在可重试队列，下一轮再试 |
| 连续失败 ≥ 3 次 | ❌ | ❌ | 自动隔离，停止自动重试（见 `quarantined_files`）|
| 空内容（`【Word文档无文字内容】`等）| ✅ | ✅ | 完成（合法但无信息，记警告）|

失败原因写入 stderr，状态存于 `analysis_state.json`：
- `failed_files`：文件名 → `{count, last_error, last_at}`
- `quarantined_files`：已隔离、停止重试的文件名

### 队列每次运行重建

v1.4.11 之前，待处理队列**只在为空时重建**，之后仅靠 `pending[:100]` 消费、
`pending[100:]` 递减 → **磁盘上新到的文档永远进不了队列**（实测有研报因此从未被分析）。

v1.4.11 起，每次运行都按全量扫描重建队列，并与旧队列中仍未处理的部分合并：
- 旧队列在前 → 保持处理连续性（断点续传语义不变）
- 新到货文档追加在后 → 不会打断正在进行的批次

### 监控

运行结束会打印一行机器可读统计，便于 cron 层做告警判断：

```
[STATS] success=98 failure=2 queue=560
```

建议 cron payload 据此判断：连续多轮 `success=0` 即告警，
不要只看 cron 的 `status=ok`（它只代表进程退出码，不代表产出有效）。

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-05-10 | 初始版本，PyMuPDF + LibreOffice 链路 |
| 1.1.0 | 2026-05-13 | 三步 PDF 处理，关键词库，双语标签 |
| 1.2.0 | 2026-05-21 | 分批处理优化，280秒断点 |
| 1.2.1 | 2026-05-22 | utils.py 共享模块重构，LibreOffice 熔断机制 |
| 1.3.0 | 2026-05-28 | kreuzberg 统一提取层 + antiword 专线 + pandoc |
| 1.4.0 | 2026-08-12 | CMap 残缺度自检 + 50万字完整提取 + OCR fallback 到 .doc |
| **1.4.11b** | **2026-11-05** | **P1 安全加固：依赖版本清单校验 / webhook 600 / 异常不再静默 / re_ocr 覆盖前校验+备份 / frontmatter 工具权限声明** |
| **1.4.11** | **2026-11-05** | **失败不写入 `analyzed_files` + 队列每次运行重建 + 失败重试/隔离队列 + `[STATS]` 统计输出** |
| **1.4.1** | **2026-08-12** | **run_analysis.py: sanitize_filename + Errno 63 重试 + 清理 temp_docs 畸形文件** |

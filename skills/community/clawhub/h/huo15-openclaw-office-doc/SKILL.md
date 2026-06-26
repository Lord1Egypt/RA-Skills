---
name: huo15-openclaw-office-doc
displayName: 火一五文档技能
description: 【青岛火一五信息科技有限公司】企业级 Word & PDF 文档生成 v7.9。39 类规范覆盖企业全场景：合同细分 7 类（劳动 / 服务 / 技术开发 / 销售 / 采购 / 保密NDA / 合作）+ HR / Sales / PR / PM / Ops / Tech / Legal / Reporting 各类文体。三条路径：Word 直出、原生 PDF 直出、Word→PDF。templates/ 下 22 份可拷贝改写的 markdown 范本。每种规范按真实场景决定是否带【内部】banner / 元数据表 / 版本史 / 审批 / TOC，CLI 可覆盖。触发词：写word、写文档、写PDF、写合同、写劳动合同、写服务合同、写技术开发合同、写销售合同、写采购合同、写NDA、写保密协议、写战略合作协议、写方案、写报告、写需求文档、写PRD、写BP、写用户手册、写培训手册、写招投标书、写演讲稿、写研究报告、写验收单、写立项书、写SOP、写公司制度、写公函、写简历、写CV、写报价单、写新闻稿、写复盘、写测试报告、写故障报告、写postmortem、写任命书、写应急预案、写在职证明、写风险评估、写项目计划书、写项目结项报告、写API文档、写部署文档、写runbook、写备忘录、写MOU、Word转PDF。
version: 7.9.1
aliases:
  - 火一五文档技能
  - 文档生成
  - Word生成
  - PDF生成
  - 多规范文档
dependencies:
  python-packages:
    - python-docx
    - reportlab
    - pygments  # 可选；装了即代码块语法高亮
---

# 火一五文档技能 v7.9.1

> 企业级 Word & 原生 PDF 文档生成 — 青岛火一五信息科技有限公司

**愿景：** 加速企业向全场景人工智能机器人转变
**理念：** 打破信息孤岛，用一套系统驱动企业增长

---

## 〇、v7.9.1（正文默认仿宋）

**变更**：除合同 7 类外，所有文体（需求文档 / 技术方案 / 研究报告 / 手册 / 方案 / 公文等）正文字体默认由**宋体改为仿宋**；标题保持黑体 / 方正小标宋。契合中文公文与方案文档规范（正文仿宋 GB），观感更正式统一。

- 合同类（劳动 / 服务 / 技术开发 / 销售 / 采购 / NDA / 合作）**保持宋体**（商业惯例）
- 调用 `create-word-doc.py` 生成的非合同文档，正文自动为仿宋，**无需再后处理改字体**
- macOS 用 STFangsong 渲染，Windows / WPS 用系统「仿宋」

---

## 一、v7.8.5 hotfix（**ELEPHANT-IN-THE-ROOM** — LOGO 宽度错算导致页眉跑出页面）

**用户反馈"v7.8.1/v7.8.2/v7.8.3 还是没有页眉、字体不对"** — pdftoppm 栅格化亲眼验证 + PyMuPDF 解 PDF stream 找到真凶：

```python
# v7.7~v7.8.4 错误代码
img = Image(logo_path, height=target_h)        # platypus Flowable
iw, ih = img.wrap(page_w, page_h)               # iw 返回原图像素宽（如 2048）
target_w = iw * (target_h / ih) if ih else target_h
# ↑ iw=2048, ih=25.5 → target_w = 2048 * (25.5/25.5) = 2048pt
```

`drawImage(width=2048, height=25.5, preserveAspectRatio=True)` 在 2048pt 宽容器里**居中** 25.5pt 实际 LOGO，居中偏移 `(2048-25.5)/2 = 1011pt`。LOGO 实际 x = `79 + 1011 = 1090pt`，**远超 page 595pt 宽** — LOGO 跑到页外！页眉文字 `text_x = x_start + logo_w = 79 + 2053 = 2133pt` 也跑到页外。

**所以"页眉只有一条灰线"** — line 用绝对坐标没问题，drawImage/drawString 用 transform matrix 全跑页外。

**修复**：用 `reportlab.lib.utils.ImageReader.getSize()` 直接读 LOGO 像素尺寸等比缩放，不依赖 platypus `Image.wrap()`。

```python
from reportlab.lib.utils import ImageReader
ir = ImageReader(logo_path)
iw, ih = ir.getSize()                # 像素尺寸，2048×2048
target_w = target_h * iw / ih        # 25.5 * 2048/2048 = 25.5pt 正确
```

**v7.8.0~v7.8.4 都修错了方向**（字体 subface / fontconfig fallback / two-pass canvas resource / onPage 时机）。这次用 PyMuPDF 解 PDF stream 看到 `25.5 0 0 25.5 1090.614 803.622 cm` 才直接定位到 LOGO transform 错位。**亲眼看 + 拆 PDF stream 是诊断这类视觉 bug 的唯一可靠路径。**

附带：chrome 从 two-pass canvas 子类移到 `PageTemplate.onPage` 回调（`make_chrome_callback`），架构更干净。

---

## 〇、v7.8.0~v7.8.4 中间版本（合并摘要 — 都没修到真因）

| 版本 | 改动方向 | 实际效果 |
|---|---|---|
| v7.8.0 | LibreOffice filter 7 项保真 + 平台感知 backend | 字体/排版 marginal 改善，元凶未触 |
| v7.8.1 | macOS Songti.ttc subface 0→6 / STHeiti 0→1（修繁体特黑） | 嵌入字体名变对，但页眉仍隐身 |
| v7.8.2 | LibreOffice 路径 docx 字体名平台映射（"宋体"→"宋体-简"） | LibreOffice 路径有效，PDF 直出仍隐身 |
| v7.8.3 | 文案：LibreOffice 标为推荐默认 | 文档级，无代码影响 |
| v7.8.4 | (内部调试，setFillColor / 字体注册 trick) | 都没救页眉 |

→ 都是错方向。**真因在 v7.8.5 才被定位**：LOGO `Image.wrap()` 返回 iw 没等比缩放 → target_w 错算 2048pt → drawImage 居中偏移 1011pt → LOGO+chrome 文字跑出页面右边。

---

## 〇、v7.7 修复（PDF 直出与 Word 视觉对齐 — 摘要）

修了 3 处对齐：页眉用 `stringWidth()` 居中（修正中文公司名偏右）/ leading × 1.2 系数（21.6pt 对齐 Word 1.5 倍行距）/ firstLineIndent = size × 2（24pt 对齐 Word `firstLineChars=200`）。详细数学验证见 git log `v7.7.0` 提交。

---

## 一、v7.5 关键变化（合同细分 7 类 + 配套范本）

> 用户反馈："合同帮我再细分"。

通用"合同"在 ToB 场景下太粗 — 一份合同应不应该带 试用期 / 知识产权 / 退换货 /
保密期限 / 收益分配 等条款，取决于具体合同子类。v7.5 把合同细分为 7 类：

| 子类 | 触发关键词 | 适用场景 | 范本 |
|------|-----------|---------|------|
| **劳动合同** | 劳动合同 / 雇佣合同 / 用工合同 / 实习合同 | HR 招聘入职 | [templates/劳动合同.md](templates/劳动合同.md) |
| **服务合同** | 服务合同 / 技术服务 / 咨询 / 维保 / SaaS / 运维 | 长期服务 | [templates/服务合同.md](templates/服务合同.md) |
| **技术开发合同** | 软件开发 / 委托开发 / 定制开发 / 开发合同 | 一次性开发 | [templates/技术开发合同.md](templates/技术开发合同.md) |
| **销售合同** | 销售合同 / 货物销售 / 软件许可 / 经销 | 售方角度 | [templates/销售合同.md](templates/销售合同.md) |
| **采购合同** | 采购合同 / 物资采购 / 设备采购 / 框架采购协议 | 购方角度 | [templates/采购合同.md](templates/采购合同.md) |
| **保密协议** | 保密协议 / NDA / 信息保密 / 双向保密 | 保密信息保护 | [templates/保密协议.md](templates/保密协议.md) |
| **合作协议** | 战略合作协议 / 联营协议 / 联合开发协议 | 有约束力合作 | [templates/合作协议.md](templates/合作协议.md) |

通用"合同"作为兜底保留 — 输入命中"合同"但没匹配到具体子类时使用。

视觉上 7 个合同子类共享通用合同的版式（宋体 / 标准页边距 / 无文档壳 / 第一条 ~
第N条结构）；差异在 **正文结构** 与 **范本内容**。FORMAT_KEYWORDS 顺序保证子类
关键词在通用"合同"之前命中。

---

> 历史变更详见文末 §十 版本历史。

---

## 二、39 类文档规范（v7.5）

> 列含义：banner = 顶部右上 【内部】 红字；meta = 文档编号/版本/密级/日期 2 列表；
> 版本史 = 末尾"版本历史"表；审批 = 末尾"审批记录"表；TOC = 自动目录。
> 命中顺序由上至下；`auto` 命中后立即返回；`--doc-format <规范>` 强制覆盖。

| 规范 | 触发关键词 | banner | meta | 版本史 | 审批 | TOC |
|------|-----------|:------:|:----:|:------:|:----:|:---:|
| **个人简历** ⭐v7.4 | 简历 / resume / CV | ❌ | ❌ | ❌ | ❌ | ❌ |
| **报价单** ⭐v7.4 | 报价单 / 商务报价 / 报价书 / 询价回复 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **新闻稿** ⭐v7.4 | 新闻稿 / 媒体通稿 / 发布稿 / press release | ❌ | ❌ | ❌ | ❌ | ❌ |
| **复盘报告** ⭐v7.4 | 复盘 / 项目复盘 / 项目总结 / 月度复盘 | ❌ | ✅ | ✅ | ❌ | ✅ |
| **测试报告** ⭐v7.4 | 测试报告 / QA报告 / 验证报告 / 性能测试 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **故障报告** ⭐v7.4 | 故障报告 / 事故报告 / 故障复盘 / postmortem | ✅ | ✅ | ❌ | ❌ | ❌ |
| **任命书** ⭐v7.4 | 任命书 / 聘任书 / 委任书 / 任命决定 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **应急预案** ⭐v7.4 | 应急预案 / 应急响应预案 / 应急处置方案 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **在职证明** ⭐v7.4 | 在职证明 / 离职证明 / 工作证明 / 收入证明 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **风险评估报告** ⭐v7.4 | 风险评估 / 风险报告 / 安全评估 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **项目计划书** ⭐v7.4 | 项目计划书 / 项目执行计划 / 项目章程 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **项目结项报告** ⭐v7.4 | 结项报告 / 项目收尾报告 / 项目交付总结 | ❌ | ✅ | ✅ | ✅ | ✅ |
| **API文档** ⭐v7.4 | API文档 / 接口文档 / 接口规范 / openapi | ❌ | ✅ | ✅ | ❌ | ✅ |
| **部署文档** ⭐v7.4 | 部署文档 / 部署手册 / 上线手册 / runbook | ❌ | ✅ | ✅ | ❌ | ✅ |
| **备忘录** ⭐v7.4 | 备忘录 / MOU / 合作意向书 / 战略合作备忘录 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 验收单 ⭐v7.3 | 验收单 / 验收报告 / 交付确认书 / 项目验收 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 项目立项书 ⭐v7.3 | 立项申请 / 立项书 / 项目建议书 / 可行性研究报告 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 操作SOP ⭐v7.3 | SOP / 标准作业指导书 / 工艺文件 / 操作规程 | ❌ | ✅ | ✅ | ❌ | ✅ |
| 公司制度 ⭐v7.3 | 规章制度 / 管理办法 / 实施细则 / 管理细则 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 信函 ⭐v7.3 | 公函 / 商务函件 / 求职信 / 推荐信 / 邀请函 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 招投标书 | 招标书 / 投标书 / 投标文件 / 响应文件 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 商业计划书 | 商业计划书 / BP / 融资计划书 / 路演稿 | ❌ | ❌ | ✅ | ❌ | ✅ |
| 用户手册 | 用户手册 / 操作手册 / 使用说明 / Manual | ❌ | ❌ | ✅ | ❌ | ✅ |
| 培训手册 | 培训手册 / 培训教材 / 教学大纲 / 员工手册 | ❌ | ❌ | ✅ | ❌ | ✅ |
| 演讲稿 | 演讲稿 / 致辞稿 / 讲话稿 / 主题分享 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 研究报告 | 研究报告 / 学术论文 / 调研报告 / 白皮书 | ❌ | ✅ | ✅ | ❌ | ✅ |
| **劳动合同** ⭐v7.5 | 劳动合同 / 雇佣合同 / 用工合同 / 实习合同 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **服务合同** ⭐v7.5 | 服务合同 / 技术服务 / 咨询 / 维保 / SaaS 合同 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **技术开发合同** ⭐v7.5 | 软件开发合同 / 委托开发合同 / 定制开发 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **销售合同** ⭐v7.5 | 销售合同 / 货物销售 / 软件许可合同 / 经销 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **采购合同** ⭐v7.5 | 采购合同 / 物资采购 / 设备采购 / 框架采购 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **保密协议** ⭐v7.5 | 保密协议 / NDA / 信息保密 / 双向保密 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **合作协议** ⭐v7.5 | 战略合作协议 / 联营协议 / 联合开发协议 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 合同（通用兜底）| 合同 / 协议 / 协议书 / 补充协议 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 会议纪要 | 会议纪要 / 纪要 | ❌ | ✅ | ❌ | ❌ | ❌ |
| 技术方案 | 技术方案 / 实施方案 / 解决方案 / 设计文档 / 架构设计 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 需求文档 | 需求规格 / SRS / PRD / 需求说明 / 需求文档 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 工作报告 | 工作报告 / 周报 / 月报 / 季报 / 年报 / 述职报告 | ❌ | ✅ | ❌ | ❌ | ❌ |
| 公文（默认）| 未命中其他关键词 | ✅ | ✅ | ✅ | ✅ | ❌ |

> 一行命令看全 17 种：`python3 scripts/create-word-doc.py --list-formats`。
> CLI 精细控制：`--with-version-history / --no-version-history /
> --with-approval / --no-approval /
> --with-classification-banner / --no-classification-banner /
> --with-doc-meta-table / --no-doc-meta-table /
> --with-title-block / --no-title-block`。

### 标题层级识别（每种规范独立）

每种规范都有自己的章节编号正则；同时支持标准 Markdown `# / ## / ### / ####`。例如：

| 规范 | 一级（chapter） | 二级（section） | 三级（article） |
|------|---------------|---------------|----------------|
| 公文 | 第X章/第X节 | 一、二、三、 | （一）（二） |
| 合同 | 第X章/第X条 | 一、二、 | — |
| 商业计划书 | 第X部分/一、二、 | 1.1 | 1.1.1 |
| 用户手册 | 第X章 | X. | X.X |
| 培训手册 | 模块X/单元X/第X课 | 一、二、 | X.X |
| 招投标书 | 第X章/篇/部分 | 一、二、 | （一）（二） |
| 研究报告 | 摘要/Abstract/引言/结论/参考文献/一、 | X. | X.X |

---

## 三、页眉 / 页脚规范

### 3.1 页眉

- **company**（默认）：LOGO + 公司名 + 文档编号 + 密级，**左对齐**
- **minimal**（合同 / 用户手册 / 演讲稿）：LOGO + 公司名，**左对齐**，不显示编号 / 密级
- **centered**（保留备选，当前无规范默认走此项）：仅公司名，居中
- 底部统一灰线 `#888888`

> v7.0 直接写 OOXML `<w:jc>` 并清 `<w:tabs>`，避免 WPS / 部分 Word 模板的样式继承覆盖。

### 3.2 页脚

- 所有规范统一为 `第 X 页 / 共 Y 页`，居中
- Word：`PAGE` / `NUMPAGES` 字段码（打开时自动计算）
- PDF：两遍渲染（NumberedCanvas）拿到真总页数

---

## 四、本地公司信息工作流

页眉的公司名、LOGO 按以下优先级解析：

1. **CLI 显式参数** `--company-name` / `--logo-path`
2. **本地缓存** `~/.huo15/company-info.json`
3. **Odoo `res.company`** 自动拉取（可用 `--no-odoo` 关闭）
4. **退出码 2 + 结构化 JSON** — 以上都拿不到时让 Claude 触发补录流程

### 4.1 标准流程（生成前）

```bash
python3 scripts/company-info.py check
#   exit 0 + 完整 JSON  → 直接生成
#   exit 2 + missing[]  → 进入补录
```

**补录流程**（Claude 执行）：

1. 先查 auto-memory 中的 `huo15_company_info.md` / `user_identity.md`
2. 仍缺失时用 `AskUserQuestion` 询问：公司全称、LOGO 路径、可选 slogan / 地址 / 电话 / 邮箱 / 官网
3. 写入：
   ```bash
   python3 scripts/company-info.py set \
     --company-name "<公司全称>" --logo-path "<LOGO绝对路径>"
   ```
4. 同步写入 memory（`huo15_company_info.md`）

---

## 五、命令行

```bash
# Word 直出
python3 scripts/create-word-doc.py --output 方案.docx \
  --title "技术方案：XXX系统" --content @/tmp/content.md \
  --doc-number "HG-FA-2026-001" --version "V1.0" --classification "内部" \
  --author "辉火云管家·贾维斯"

# 一览 39 种 preset：
python3 scripts/create-word-doc.py --list-formats

# 原生 PDF 直出（不依赖 LibreOffice / Office）：
python3 scripts/create-pdf-doc.py --output 方案.pdf \
  --title "技术方案：XXX系统" --content @/tmp/content.md \
  --doc-format 技术方案

# Word → PDF（保留版式）：
python3 scripts/word-to-pdf.py 方案.docx -o 方案.pdf
```

**关键 CLI 参数：**

- `--doc-format <规范>` — 39 类规范任选；省略走 `auto` 自动识别
- `--company-name / --logo-path` — 覆盖本地公司信息
- `--with-version-history / --no-version-history` — 版本历史表
- `--with-approval / --no-approval` — 审批记录表
- `--with-classification-banner / --no-classification-banner` — 顶部 【内部】红字
- `--with-doc-meta-table / --no-doc-meta-table` — 顶部元数据 2 列表
- `--with-title-block / --no-title-block` — 标题大字块

**何时用哪条路径**：只要 Word → 用 `create-word-doc.py`；只要 PDF →
`create-pdf-doc.py`（最快）；要 Word + PDF 版式一致 → 先 word，再
`word-to-pdf.py`。后端优先级 `libreoffice → docx2pdf → word_com` 自动回落。

字体：macOS 自带 Songti.ttc / STHeiti.ttc；Linux 推荐 Noto CJK；
Windows 可用 SimSun / SimHei。

---

## 六、Markdown 能力速查

| 元素 | 写法 | 说明 |
|------|------|------|
| 标题 | `#`~`######` | 也支持规范专属编号（一、 / 1. / 1.1 / 第X章） |
| 段落软换行 | 直接换行 | CJK ↔ CJK 不插入空格；ASCII 仍保留空格 |
| 段落硬换行 | 行尾 `  ` 或 `\` | 同段内强制换行 |
| 列表 | `- item` / `* item` / `1. item` | |
| 强调 | `**粗**` / `*斜*` / `` `inline code` `` | |
| 表格 | 标准 GFM | 缺前导 `|` / 转义 `\|` / 2 列起即可识别 |
| 代码块 | `` ``` ``...`` ``` `` | 等宽灰底；带语言标签 |
| 引用块 | `> ...` | 左侧橘色竖条 + 灰色段 |
| 分隔线 | `---` / `***` / `___` | |
| 元数据行 | `文档编号：XX | 版本：V1.0 | 密级：内部 | 日期：2026-04-27` | 自动两列表格 |
| 分页符 | `---PAGE---` / `\pagebreak` / `<!-- pagebreak -->` | 强制下一页 |
| 空内容 | — | 写"（无正文内容）"灰字占位 |

---

## 七、Python API

```python
# Word
from create_word_doc import create_word_doc
create_word_doc(
    output_path="文档.docx",
    title="技术方案：XXX系统",
    content=md_text,
    doc_number="HG-FA-2026-001",
    version="V1.0",
    classification="内部",
    author="辉火云管家·贾维斯",
    doc_format="auto",            # 12 类规范名 / 'auto'
)

# PDF
from create_pdf_doc import create_pdf_doc
create_pdf_doc(output_path="文档.pdf", title="...", content=md_text,
               doc_format="商业计划书")

# Word → PDF
from word_to_pdf import convert_to_pdf
ok, path = convert_to_pdf("方案.docx", "方案.pdf",
                          backend="auto", keep_fonts=True)
```

> 缺公司信息时三个入口都抛 `RuntimeError`，message 是结构化 JSON，Claude 据此触发补录。

---

## 八、触发词

通用：写 word / 写 PDF / 写文档 / 生成 word / 生成 PDF / 创建文档 / 导出文档 / Word 转 PDF。

39 类规范触发词由 §二 表格中"触发关键词"列定义。常用：写合同 / 写协议 /
写劳动合同 / 写服务合同 / 写技术开发合同 / 写销售合同 / 写采购合同 / 写 NDA /
写保密协议 / 写战略合作协议 / 写方案 / 写报告 / 写会议纪要 / 写需求文档 /
写 PRD / 写商业计划书 / 写 BP / 写用户手册 / 写培训手册 / 写招标书 / 写投标书 /
写演讲稿 / 写研究报告 / 写白皮书 / 写验收单 / 写立项书 / 写 SOP / 写公司制度 /
写公函 / 写邀请函 / 写简历 / 写 CV / 写报价单 / 写新闻稿 / 写复盘 / 写测试报告 /
写故障报告 / 写 postmortem / 写任命书 / 写应急预案 / 写在职证明 / 写风险评估 /
写项目计划书 / 写项目结项报告 / 写 API 文档 / 写部署文档 / 写 runbook / 写备忘录 /
写 MOU。

---

## 九、目录结构

```
scripts/
├── doc_core.py          # 共享核心：32 类预设 + Block AST 解析 + 内联 token
│                        # v7.4：再扩 15 类预设 + 关键词优先级调整
│                        # v7.3：FormatPreset 增 4 个文档壳开关
├── company-info.py      # 本地公司信息读写 + Odoo 回落
├── create-word-doc.py   # Word 渲染（python-docx + 强制 OOXML jc）
│                        # v7.3：_strip_markdown_emphasis + _maybe_dedupe_h1_title
├── create-pdf-doc.py    # 原生 PDF 渲染（reportlab + NumberedCanvas）
│                        # v7.3：与 Word 端文档壳逻辑保持一致
└── word-to-pdf.py       # Word → PDF 多后端转换

templates/               # v7.4：15 份可直接拷贝改写的 markdown 范本
├── 个人简历.md
├── 报价单.md
├── 新闻稿.md
├── 复盘报告.md
├── 测试报告.md
├── 故障报告.md
├── 任命书.md
├── 应急预案.md
├── 在职证明.md
├── 风险评估报告.md
├── 项目计划书.md
├── 项目结项报告.md
├── API文档.md
├── 部署文档.md
├── 备忘录.md
└── README.md
```

---

## 十一、未来路线（已调研、未实施）

| 功能 | 业界参考 | 优先级 | 复杂度 | 拟引入依赖 |
|------|---------|--------|-------|----------|
| LaTeX → OMML 公式管线 | markdocx / Pandoc | 中 | 中 | latex2mathml + XSLT |
| reference docx 模板继承 | Pandoc / Quarto | 中 | 中 | 仅模板文件 |
| Typst 第四条 PDF 路径（30× 速度） | typst.app + zh-kit | 中 | 中 | typst 二进制 |
| pandoc-crossref 风格交叉引用 `{#fig:xxx}` | pandoc-crossref | 中 | 中 | — |
| 水印 + AES 加密 | msoffcrypto-tool | 低 | 小 | msoffcrypto-tool |
| 修订追踪 / 批注 | docx-revisions | 低 | 大 | docx-revisions |
| docxtpl Jinja2 模板槽 | docxtpl | 低 | 小 | docxtpl |

> 任何一项触发刚需时再上；当前以稳定 + 中文友好 + 易维护为先。

---

## 十、版本历史

详细版本历史见 git log。当前主要里程碑：
- **v7.8.6**（最新）：**Word emoji 乱码修复** — markdown 内含 emoji(🎂🚗💰🦞✅⭐🇨🇳 等)生成 docx 后,在 WPS / LibreOffice / Linux Word 渲染时显示 ▢▢ 占位方块。根因:`_set_font` 把 ascii/hAnsi/eastAsia 三个 slot 都设为中文字体(PingFang/宋体/黑体),中文字体不含 emoji glyph 就 fallback 到方块。修复:(1)`_set_font` 加 `w:cs` slot 指向 `Segoe UI Emoji` 兜底;(2)新增 `_add_run` emoji-aware 包装,内部按 `_EMOJI_RE` 正则把 emoji 字符切到独立 run + 用 emoji 字体;(3)`render_inline` 改用 `_add_run` 覆盖所有 markdown 内联文本(bold/italic/code/text)。Mac/Linux 系统会自动 fallback 到 Apple Color Emoji / Noto Color Emoji。
- **v7.8.x**：PDF 渲染保真度 — 字体 subface 修正 / leading 系数 / firstLineIndent 字符化 / LibreOffice filter 加固 / 平台感知后端优先级（详见上方〇章节）
- **v7.5–v7.6**：39 类规范 + 合同细分 7 类 + KV 元数据归并 / TOC 占位回填 / PDF outline 修复
- **v7.0–v7.4**：原生 PDF 直出（create-pdf-doc.py）+ 27→39 类扩张 + Pygments 代码高亮 + CJK 段落 OOXML 直写
- **v6.x**：Block AST 重写 / 页眉恒含 LOGO / 页脚字段码
- **v5.x**：多规范自动识别骨架 + company-info.py

---

**技术支持：** 青岛火一五信息科技有限公司

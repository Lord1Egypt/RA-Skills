---
name: origin-office
description: 原生文档（docx/pptx）→ 可验证的对象——转换即语义事务。零依赖解析 docx 的章/条/段落/表格（合并单元格展开、勾选框保留）与 pptx 的幻灯片/形状/表格（占位符类型、gridSpan 合并），每处结构一个对象建成本象包，SHA-256 结构指纹入库，verify 可验证「包与源文件一致」（篡改即检出）。行业火力全在 PDF 扫描件（OCR 有物理误差），原生电子文档的无损结构化没人认真做——本象做「把字变成可验证状态的对象」。当需要把 docx/pptx 转成 AI 可锚定、可验证的结构，或做文档版本追踪/条款级引用时使用。
version: 1.1.1
slug: origin-office
license: Apache-2.0
displayName: origin-office 原生文档可验证结构化
summary: docx/pptx 原生结构转可验证对象：章/条/表/幻灯片逐结构入库，SHA-256 指纹可验证，转换即语义事务。
metadata:
  openclaw:
    runtime: node >= 18
    tags: [office, docx, pptx, document, structure, verify]
---

# origin-office · 原生文档的本象

> 一份红头文件交给 AI，它看到的是被 OCR 或文本框切割后的碎片。
> 可这份 docx 里明明写着「第一章、第五十条、Q112 表、合并单元格」——
> 原生电子文档的结构是**无损**的，行业却把它当成扫描件来猜。
> 这个 skill 把 docx/pptx 导入本象包，让章、条、表、幻灯片都变成可锚定、可验证的对象。

## 安装

```bash
# 本象协议仓库
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# 验证
npm run test:office    # 20 项断言（docx + pptx 合成夹具 + 统一 CLI 建包/验证/篡改检出）
```

## 用

```bash
# 统一 CLI：docx/pptx → 本象包（转换即语义事务）
node adapters/office/cli.mjs import 文件.docx report.origin --name "报告名"
node adapters/office/cli.mjs import 演示.pptx  deck.origin

# 只看结构，不建包
node adapters/office/cli.mjs inspect 文件.docx

# 验证：重算源文件哈希与包内指纹比对（文档被改过即检出）
node adapters/office/cli.mjs verify report.origin 文件.docx && echo 一致

# 传统用法：docx → markdown（章→##、条→###、表→GFM 管道表）
node adapters/office/import.mjs 文件.docx 输出.md
node adapters/office/import.mjs 文件.docx --json
```

## 转换出的对象

- docx：`par:*`（段落，带 chapter/article 锚点）、`tbl:*`（表格，合并展开后的行列网格）
- pptx：`sldNN-shp*`（形状，带 placeholder 类型 title/subTitle/body）、`sldNN-tbl*`（表格）
- 每个包带事实对象：`fact:structure-hash`（SHA-256 结构指纹）、`fact:stats`

建包后可用本象协议 CLI 读：
```bash
node compiler/cli.mjs status  report.origin    # 包概览
node compiler/cli.mjs why     report.origin par:0003.text   # 这个值凭什么是这个值
node compiler/cli.mjs history report.origin    # 所有改动
```

## 可验证性（与扫描件路线的本质区别）

| | PDF 扫描件路线（MinerU/Docling/LlamaParse） | 本象（原生 docx/pptx） |
|---|---|---|
| 输入 | 扫描件/PDF，物理误差封顶 | 原生电子文档，结构无损 |
| 表格 | OmniDocBench TEDS≈0.78，中文更低 | 合并单元格按 gridSpan/vMerge 展开，逐格可锚定 |
| 可验证 | 无（输出即终态） | 转换=事务，结构指纹入库，verify 可复查 |

## 验证

```bash
npm run test:office    # 20 项：docx 结构还原 11 + pptx 解析 5 + 统一 CLI 建包/指纹/篡改检出 4
```

真实案例：海事局《船员培训和船员管理质量管理规则》2019 红头文件
→ 409 个结构对象（6 章/77 条/16 表/59 勾选），verify 一致。

## 相关

- 本象协议（benxiang-protocol）：持久对象表示层 + 语义事务 + 证据链。
- xlsx 方言：电子表格（公式依赖图）有独立导入器 adapters/xlsx/。

---

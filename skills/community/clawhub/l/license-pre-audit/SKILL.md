---
name: license-pre-audit
version: 1.3.0
description: 进出口许可文档智能预审系统。支持 PDF 和图片处理：自动提取合同号、出口国、进口商、总金额、数量、重量、合格证编号、生产商、报关口岸等字段，检测公章，按审核规则执行审核，生成 MD 和 JSON 审核报告。支持 CLI 和对话交互两种方式触发。
author: njkahn 南星
---

# License Pre-Audit - 进出口许可文档智能预审系统

进出口许可文档智能预审系统，支持：

1. **CLI 命令行**：直接指定目标文件夹或压缩包路径执行命令。
2. **对话交互**：在聊天界面输入触发词（如"审核"/"审核许可证"/"许可证"），然后上传文件夹或压缩包。

系统将自动解压、提取 PDF、图片 文件目标字段，根据审核规则 执行审核、检测公章，并生成结构化 JSON 报告和 Markdown 表格。


## 系统结构

```
license-pre-audit/
├── SKILL.md                    # 技能说明
├── references/                 # 配置文件
│   ├── audit-rules.json        # 审核规则配置
│   ├── doc-types.json          # 文档类型配置
│   ├── settings.json           # 上传格式、路径、输出路径、触发指令、缓存配置
│   └── demo/                   # 示例数据
│       └── test.zip            # 示例压缩包
├── assets/                     # 运行时数据
│   ├── files/                  # 解压文件目录
│   └── reports/                # 报告输出目录
└── src/
    ├── index.js                # 主流程（整合 CLI+ 压缩包 + 表格）
    ├── prompts/                # Prompt 文件（MD 格式）
    │   ├── extract-fields.md   # 字段提取 Prompt
    │   └── audit-rules.md      # 审核规则 Prompt
    ├── utils/                  # 工具函数
    │   ├── pdf-ocr.js          # PDF/图片文本提取
    │   ├── stamp-detect.js     # 盖章检测
    │   ├── field-normalize.js  # 字段标准化
    │   ├── extract-archive.js  # 压缩包解压
    │   ├── generate-table.js   # 表格生成
    │   └── check-deps.js       # 依赖检测与自动安装（新增）
    └── rules/                  # 11 条审核规则
        ├── index.js            # 规则总入口
        ├── rule-stamp.js       # 规则 1: 盖章检查
        ├── rule-contract-no.js # 规则 2: 合同号
        ├── rule-exporter.js    # 规则 3: 出口国
        ├── rule-importer.js    # 规则 4: 进口商
        ├── rule-amount.js      # 规则 5: 金额检查
        ├── rule-quantity.js    # 规则 6: 数量检查
        ├── rule-weight.js      # 规则 7: 重量检查
        ├── rule-mtc-no.js      # 规则 8: 合格证编号
        ├── rule-manufacturer.js # 规则 9: 生产商
        ├── rule-customs.js     # 规则 10: 报关口岸
        └── rule-summary.js     # 规则 11: 审核摘要
```

## 🚀 快速开始

### 方式 1: CLI 命令行（文件夹）

```bash
# 审核文件夹中的所有文档
node <技能路径>/src/index.js <许可证文件夹路径>

# 示例（使用内置 demo 文件夹）
node ./src/index.js ../references/demo/test
```

### 方式 2: CLI 命令行（压缩包）

```bash
# 审核压缩包（zip/rar/tar.gz）
node <技能路径>/src/index.js <许可证压缩包路径>

# 示例（使用内置 demo 压缩包）
node ./src/index.js ../references/demo/test.zip
```

### 方式 3: 对话交互（推荐）

**使用步骤**：
1. 在对话界面输入触发词，如：`审核`/ `审核许可证` / `许可证`（ 触发词可在 `references/settings.json` 中配置 ）
2. 上传许可证压缩包（zip/rar/tar.gz）或 许可证文件夹（也可发送压缩包或文件夹的路径）
3. 系统自动解压、提取、审核、生成报告
4. 返回 Markdown 表格和 JSON 报告下载链接

**输出**: 
- JSON 报告：`audit-result-<timestamp>.json`
- Markdown 表格：`audit-result-<timestamp>.md`


## 支持的输入格式

### 压缩包格式
- **ZIP**: `.zip`
- **RAR**: `.rar`
- **TAR**: `.tar`, `.tar.gz`, `.tgz`

### 文档格式
- **PDF**: `.pdf` 
- **图片**: `.jpg`, `.jpeg`, `.png`, `.webp`

## 支持的文档类型

1. **合同 (contract)** - 包含"Contract"、"合同"等关键词
2. **合格证 (certificate)** - 包含"Quality Certificate"、"质量合格证书"等
3. **许可证表单 (permitform)** - 包含"Import/Export"、"许可证"等

## 字段提取

| 字段 | 说明 | 文档类型 |
|------|------|---------|
| contractNo | 合同编号 | contract, form |
| exportCountry | 出口国家 | contract, form |
| importerEn | 进口商英文 | contract, form |
| importerCn | 进口商中文 | contract, form |
| customsPort | 报关口岸 | form |
| mtcNo | 合格证编号 | certificate, form |
| manufacturer | 生产厂商 | certificate, form |
| bussDetial | 货物详情数组 | contract, form |
| totalAmount | 总金额 | contract, form |
| totalQuantity | 总数量 | contract, form |
| totalWeight | 总重量 | contract, form |
| hasStamp | 是否盖章 | certificate |

## 审核规则（11 条）

1. 盖章检查
2. 合同号提取验证
3. 出口国检查
4. 进口商检查
5. 金额检查（±5% 容忍度）
6. 数量检查（±5% 容忍度）
7. 重量检查
8. 合格证编号检查
9. 生产商检查
10. 报关口岸检查
11. 整体结果

## 输出格式

### ⚠️ 重要：Markdown 表格发送方式（企业微信/飞书/所有聊天平台）

**核心要求**：在对话交互模式（压缩包/文件夹上传）下，**必须**执行以下流程：

1. **脚本生成报告**：`index.js` 生成 JSON 和 MD 报告文件
2. **助手读取 MD 文件**：脚本执行完成后，助手**必须直接读取**生成的 `.md` 文件内容
3. **直接发送 Markdown**：助手将 MD 文件内容**原样作为 Markdown 发送**到聊天界面（企业微信/飞书/其他平台）
   - **不要**通过 `console.log` 或 `console.error` 输出表格
   - **不要**只返回文件路径
   - **必须**读取文件内容并作为 Markdown 消息发送
4. **平台兼容性**：此方式适用于所有聊天平台（企业微信、飞书、Telegram、Discord 等），确保 Markdown 表格正确渲染

**原因**：
- `console.log/error` 输出的内容会被当作纯文本处理，Markdown 格式丢失
- 只返回文件路径，聊天界面无法自动渲染
- 只有直接发送 Markdown 内容，各平台才能正确渲染为表格

**实现方式**：
```bash
# 脚本执行后，助手执行：
md_file=$(ls -t assets/reports/audit-result-*.md | head -1)
cat "$md_file"  # 读取并发送内容
```

### 1. Markdown 表格（压缩包模式）

在聊天界面或控制台直接显示二维表格：

| 检查项 | 申请表 | 合同/合格证 | 预审结果 |
|--------|--------|-------------|------|
| 合同编号 | AFT250890 | AFT250890 | ✅ 通过 |
| 出口国 | 中国 | 中国 | ✅ 通过  |
| 进口商（英文） | Stock Company | Stock Company | ✅ 通过 |
| 总金额 | 47060 | ￥47,060.00 | ✅ 通过  |
| 总数量 | 180千克 | 1 lot | ❌不通过  |
| 合格证编号 | 2025032601,028119877 | 2025032601 | ✅ 通过  |
| 生产商 | 江苏国强镀锌实业有限公司 | 江苏国强镀锌实业有限公司 | ✅ 通过  |
| 盖章情况 | 已盖章 | 已盖章 | ✅ 通过  |

**横向**: 申请表 | 合同/合格证 | 预审结果  
**纵向**: 9 个检查项（合同编号、出口国、进口商、总金额、总数量、合格证编号、生产商、报关口岸、盖章情况）

上面是表格，表格下面是 整体结果 和 详细审核说明。


### 2. JSON 报告（完整详细信息）

```json
{
  "timestamp": "2026-04-13T06:01:19.853Z",
  "folder": "../references/demo/test",
  "totalFiles": 3,
  "processedFiles": 3,
  "auditResults": [
    {
      "filename": "SC NO.JYIE-2025-137.pdf",
      "docType": "合同",
      "extractedFields": {
        "contractNo": "JYIE-2025-137",
        "exportCountry": "中国",
        "importerEn": "RAMATEX TEXTILES INDUSTRIAL SDN,BHD",
        "importerCn": "马来西亚利玛纺织有限公司",
        "totalAmount": "CNY980,000.00",
        "totalQuantity": "1 lot",
        "totalWeight": "",
        "bussDetial": [
          {
            "commodity": "Air condition system 空调系统",
            "quantity": "1 lot",
            "weight": "",
            "unitPrice": "980000 CNY",
            "amount": "980000 CNY"
          }
        ]
      },
      "hasStamp": true
    },
    {
      "filename": "angle bar.jpg",
      "docType": "合格证",
      "extractedFields": {
        "mtcNo": "2025032601",
        "manufacturer": "江苏国强镀锌实业有限公司"
      },
      "hasStamp": true
    },
    {
      "filename": "b699b609-cfa3-4de1-bc16-65a65d6f2ab8.png",
      "docType": "申请表",
      "extractedFields": {
        "contracNo": "JYIE-2025-137",
        "exportCountry": "中国",
        "importerCn": "马来西亚利玛纺织有限公司",
        "importerEn": "RAMATEX TEXTILES INDUSTRIAL SDN BHD",
        "customsPort": "上海海关",
        "bussDetial": [
          {
            "commodity": "角钢（除名加工外未经进一步加工）",
            "quantity": "180 千克",
            "unitPrice": "55 人民币元",
            "amount": "990 人民币元"
          }
        ],
        "totalAmount": "980000 人民币元",
        "totalQuantity": "180 千克",
        "mtcNo": "2025032601,028119877",
        "manufacturer": "江苏国强镀锌实业有限公司"
      },
      "hasStamp": true
    }
  ],
  "auditSummary": {
    "reviewResult": "整体审核结果：建议不通过",
    "reviewDetail": "1. 合同编号一致：JYIE-2025-137\n2. 出口国一致：中国\n3. 进口商英文名称一致：RAMATEX TEXTILES INDUSTRIAL SDN,BHD\n5. 合格证编号一致：2025032601\n6. 生产商信息一致：江苏国强镀锌实业有限公司\n7. 货物详情不一致\n8. 价格总计高度相似：CNY980,000.00 vs 980000 人民币元\n9. 货物总量不一致\n\n不通过项共 2 项。",
    "sign": {
      "reviewResult": "通过",
      "reviewDetail": "合同已盖章。合格证已盖章"
    },
    "contracNo": {
      "reviewResult": "通过",
      "reviewDetail": {
        "formdata": "JYIE-2025-137",
        "attachdata": "JYIE-2025-137"
      }
    },
    "exporter": {
      "reviewResult": "建议通过，需人工复审",
      "reviewDetail": {
        "formdata": "中国",
        "customsPort": "上海海关",
        "attachdata": "中国"
      },
      "note": "出口国为中国，报关口岸非保税区，需复核。"
    },
    "importerEn": {
      "reviewResult": "通过",
      "reviewDetail": {
        "formdata": "RAMATEX TEXTILES INDUSTRIAL SDN BHD",
        "attachdata": "RAMATEX TEXTILES INDUSTRIAL SDN,BHD"
      },
      "note": "进口商名称高度相似（空格/后缀差异），视为一致"
    },
    "bussDetial": {
      "reviewResult": "不通过",
      "reviewDetail": {
        "formdata": "未匹配",
        "attachdata": "未匹配"
      }
    },
    "totalAmount": {
      "reviewResult": "建议通过，需人工复审",
      "reviewDetail": {
        "formdata": "980000 人民币元",
        "attachdata": "CNY980,000.00"
      },
      "note": "金额高度相似，建议通过但需人工确认"
    },
    "totalQuantity": {
      "reviewResult": "不通过",
      "reviewDetail": {
        "formdata": "180 千克",
        "attachdata": "1 lot"
      },
      "note": "数量不一致"
    },
    "mtcNo": {
      "reviewResult": "通过",
      "reviewDetail": {
        "formdata": "2025032601,028119877",
        "attachdata": "2025032601"
      },
      "note": "申请表包含多个合格证编号"
    },
    "manufacturer": {
      "reviewResult": "通过",
      "reviewDetail": {
        "formdata": "江苏国强镀锌实业有限公司",
        "attachdata": "江苏国强镀锌实业有限公司"
      }
    }
  }
}
```


## 技能特性 

- ✅ **全自动依赖安装**：首次运行时自动检测并安装所有缺失依赖，包括：
  - **Node.js 运行时**（macOS/Linux/Windows 全平台支持）
  - **Python 3.x** 及 pdfplumber 库
  - **Poppler**（PDF 转图片工具）
  - **Tesseract OCR**（支持中英文识别）
  - **无需任何确认**，一键自动完成，实时显示安装进度
  - **安装完成后自动继续**执行审核流程
- ✅ **混合模式盖章检测**：LLM 优先 + OCR 关键词校准
- ✅ **智能金额识别**：自动识别 "CNY980,000.00" 与 "980000 人民币元"，美元、日元等类似 金额中英文单元前后判断
- ✅ **相似性检测增强**：数据比对相似值识别，酌情判定："建议通过，需人工复审"
- ✅ **印章识别增强**：支持圆形、半圆形、长方形、正方形、红色、蓝色印章，LLM 优先 + OCR + 正则 多重识别
- ✅ **编号易混字符标准化**：合格证编号: 易混淆字符标准化（8-B, 0-O, 1-I, 3-E, 5-S, 2-Z, 7-T）
- ✅ **压缩包支持**：自动解压 zip/rar/tar.gz，验证文件类型
- ✅ **二维表格输出**：Markdown 表格直观展示审核结果
- ✅ **多模式触发**：CLI 命令行 + 对话交互（输入触发词后上传文件）
- ✅ **触发词可配置**：在 `references/settings.json` 中自定义触发词（跨平台通用）
- ✅ **安全配置**：LLM 敏感信息自动从 OpenClaw 配置读取，加密存储，内存缓存
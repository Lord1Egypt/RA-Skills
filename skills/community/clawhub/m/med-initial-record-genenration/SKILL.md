---
name: med-initial-record-gen
description: 从中文医患对话文本生成门诊初诊病历，输出结构化分段的病历正文（文本）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📝"
      }
  }
---

# 门诊初诊病历生成

概述
----
给定一份 **中文医患对话文本**（通常来自 ASR 转写），本技能生成一份门诊 **初诊病历** 文本，包含常见病历分段（如主诉、现病史、既往史、查体、辅助检查、诊断、处理等）。

常见输出分段：
- 主诉
- 现病史
- 既往史
- 月经史（如适用）
- 查体
- 辅助检查
- 诊断
- 处理

数据安全、隐私与伦理声明
------------------------
- **最小必要原则**：仅处理生成病历所必需的对话内容；不要求也不鼓励包含姓名、证件号、手机号、详细地址等身份信息。
- **严格脱敏**：在发送至任何模型/接口前，会对可识别个人身份的信息进行脱敏/去标识化处理（如姓名、证件号、手机号、详细地址、人脸/影像等）。仅传递脱敏后的必要信息用于本次 skill 调用。
- **不做本地持久化**：不将用户输入与中间结果写入本地持久化存储（包含磁盘文件、数据库、日志）。仅在内存中短暂处理；**本次调用结束即销毁**。
- **第三方 API 风险提示**：在功能需要时，可能会调用第三方模型/服务接口；此时仅会发送**脱敏后的必要信息**，并使用加密传输。除完成本次请求外，不用于任何其他用途（如训练、画像、营销）。
- **医疗边界**：本技能用于病历文本整理与结构化表达的辅助生成，不构成医疗诊断或治疗建议；请由执业医生复核并承担最终医疗责任。

输入格式
--------
纯文本对话（UTF-8），建议一行一句/一轮，例如：

患者：……
医生：……
患者：……
医生：……

也支持通过统一入口 `scripts/run.py` 直接输入 `pdf/doc/docx/xls/xlsx/csv/txt/json`。
预处理成功后，会先归一化为标准医患对话文本，再调用本 skill 的原始生成逻辑。

快速开始
--------

```bash
# 从 skills 目录运行
python3 scripts/run.py \
  --input data/med-initial-record-gen/dialogue.txt

# 或继续直接使用原始文本入口
python3 scripts/gen_initial_record.py \
  --input data/med-initial-record-gen/dialogue.txt
```

参数说明
--------
* `--input PATH`
  - 输入对话文本路径（UTF-8）。
* `--output PATH`
  - 输出病历路径（默认：`../runs/med-initial-record-gen/record.txt`）。
* `--diag-id STRING`
  - 对话 ID（默认：`skill-diag`）。
* `--timeout SECONDS`
  - 超时秒数；`0` 表示一直等待（默认：0）。

统一入口附加参数（`scripts/run.py`）
----------------------------------
* `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`
  - 输入类型；默认 `auto`。
* `--sheet STRING`
  - 读取 Excel 时指定 sheet（可选）。
* `--encoding STRING`
  - `txt/csv` 编码（默认：`utf-8`）。
* `--save-prepared`
  - 保存预处理后的标准对话文本，便于调试。

输出约定
--------
- 若输出路径父目录不存在，会自动创建。
- 输出为 UTF-8 文本，包含常见门诊初诊病历分段。

依赖
----
### 运行环境
- Python 3.7+

### 外部 API
- 后端病历生成服务：`https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1`
  - 方法：POST，Content-Type: application/json
  - 需要网络访问 `shangbao.yunzhisheng.cn`

### Python 第三方包（可选，按输入格式需要）
| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` 文件 | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须（或用 pdftotext 替代） |

安装：`pip install openpyxl pypdf`

### 外部工具（可选，按输入格式需要）
| 工具 | 用途 | 必要条件 |
|------|------|---------|
| LibreOffice (`soffice`) | 转换 `.doc` / `.xls` 为文本 | 输入为 doc/xls 时必须 |
| `pdftotext`（poppler-utils） | 提取 PDF 文本 | 输入为 pdf 且未安装 pypdf 时必须 |
| `tesseract`（含 chi_sim+eng 语言包） | 图片 OCR | 输入为 png/jpg/bmp/tif 等图片时必须 |

安装（Ubuntu/Debian）：`sudo apt-get install libreoffice poppler-utils tesseract-ocr tesseract-ocr-chi-sim`

> 仅使用 TXT/JSON 输入时，无需安装任何第三方包或外部工具。

测试命令
--------
从 `skills` 目录执行（网络自测）：

```bash
python3 self_tests/med-initial-record-gen/self_test_initial_record_gen.py --run-network
```


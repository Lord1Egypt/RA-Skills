# 保险理赔多模态医疗票据 OCR 技术参考（ advisory only / 咨询级）

> ⚠️ **DISCLAIMER / 免责声明**
> - **English:** This document provides technical reference and example code ONLY. It does NOT provide production-ready models, pre-trained weights, or bundled API credentials. All accuracy figures (e.g., "~95%") are vendor-published benchmarks under ideal conditions, NOT validated results of your deployment. You must provide your own API keys, training data, and models. All OCR results must be reviewed by human staff before use in claim decisions.
> - **中文：** 本文档仅提供技术参考和示例代码，不含生产级模型、预训练权重或绑定的API凭证。所有准确率数据（如"~95%"）均为厂商发布的理想条件下基准结果，非您部署后的实测结果。您必须自行提供API密钥、训练数据和模型。所有OCR结果在用于理赔决定前，必须经人工审核。

> 🔒 **DATA SECURITY / 数据安全**
> - Medical invoices contain sensitive personal information (name, ID number, diagnosis, hospital). Before sending to ANY cloud OCR provider, you MUST: (1) obtain user consent, (2) redact unnecessary PII fields, (3) confirm the vendor's data retention policy (prefer: no storage / auto-delete within 24h), (4) consider private on-prem deployment for production use.
> - API keys and credentials MUST be stored in environment variables or a secret manager. NEVER hardcode keys in production code.

---

## 一、主流 OCR 服务横向对比（厂商公开基准数据）

| 服务商 | 支持票据类型 | 厂商公开准确率基准 | 调用限频 | 参考价格（元/千次） | 特色功能 |
|---------|--------------|----------------|----------|----------------|----------|
| 百度 AI | 发票+7类病历+2类报告 | ~95%（厂商基准） | 50次/秒 | 0.15 | 覆盖最全，EasyDL 自训练 |
| 腾讯云 | 全国门诊/住院发票 | ~93%（厂商基准） | 5次/秒 | 0.12 | 与腾讯云生态打通，理赔场景优化 |
| 阿里云 + 深智恒际 | 各省市门诊发票 | ~92%（厂商基准） | 20次/秒 | 0.18 | 支持定制化训练，票据类型覆盖深度好 |
| 合合信息 TextIn | 医疗票据全品类 | ~94%（厂商基准） | 100次/秒 | 0.20 | 深度学习融合，表格还原精度高 |

> ⚠️ **重要：** 以上准确率为厂商在理想条件下发布的基准数据，实际准确率取决于图像质量、票据类型、训练数据质量等因素。部署前须自行测试验证。

---

## 二、技术架构参考（需自行实现）

### 完整处理流水线（参考架构）

```
原始图像输入
  ↓
[图像预处理]  — 需自行实现或调用云服务API
  - 去噪（高斯滤波 / 中值滤波）
  - 倾斜校正（霍夫直线检测 + 仿射变换）
  - 二值化（Otsu 自适应阈值）
  - 透视校正（四点变换）
  ↓
[版面分析]  — 需自行实现
  - 关键点检测（角点 / 印章 / 表格线）
  - 区域分割（标题 / 明细 / 印章区）
  ↓
[文本检测]  — 可选：CTPN / PSENet / DB-Net（需自行训练）
  - 文字行定位
  - 弯曲文本矫正
  ↓
[文本识别]  — 可选：CRNN + CTC / ViT-OCR（需自行训练）
  - CNN 特征提取（ResNet50 / EfficientNet-B4）
  - RNN 序列建模（BiLSTM × 2 层）
  - Attention 对齐（Coverage Attention）
  - CTC 解码 → 字符序列
  ↓
[结构化提取]  — 需自行实现规则 + NER 模型
  - 正则表达式匹配（金额 / 日期 / 发票号）
  - 命名实体识别 BIOES 标注
  - 字段归一化（金额统一到 `float`，日期统一到 `YYYY-MM-DD`）
  ↓
[输出]  JSON 结构化结果（需人工审核）
```

> ⚠️ **重要：** 以上架构需要您自行准备训练数据、训练模型或购买云服务API。本Skill不提供任何预训练模型权重。

---

## 三、Python 调用示例（需自行配置API密钥）

### ⚠️ 安全提醒（使用任何OCR服务前必读）

1. **API Key 管理：** 将密钥存入环境变量，禁止硬编码
2. **数据脱敏：** 发送图像前，用遮盖方式隐去姓名、身份证号等敏感字段
3. **数据留存：** 确认服务商数据处理政策，优先选择"不留存"或"24小时内自动删除"
4. **生产环境：** 建议使用私有化部署方案，医疗数据不出域

### 3.1 百度 AI 医疗票据识别（示例）

```python
import requests
import base64
import json
import os

# ⚠️ 安全做法：从环境变量读取密钥，禁止硬编码
API_KEY = os.environ.get("BAIDU_OCR_API_KEY")
SECRET_KEY = os.environ.get("BAIDU_OCR_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise ValueError("请设置环境变量 BAIDU_OCR_API_KEY 和 BAIDU_OCR_SECRET_KEY")

# 获取 access_token
def get_access_token():
    url = f"https://aip.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    return requests.get(url).json()["access_token"]

# 医疗票据识别（⚠️ 建议：事前对图像做脱敏处理）
def recognize_medical_invoice(image_path: str, token: str) -> dict:
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    url = f"https://aip.baidu.com/rest/2.0/ocr/v1/medical_invoice?access_token={token}"
    payload = {
        "image": img_b64,
        "detect_direction": "true",
        "probability": "true",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=payload, headers=headers)
    return resp.json()

# 使用示例（⚠️ 结果须经人工审核）
# token = get_access_token()
# result = recognize_medical_invoice("invoice.jpg", token)
# print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 3.2 腾讯云医疗发票识别（示例）

```python
# ⚠️ 安全做法：从环境变量读取密钥
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

def recognize_tencent_medical(image_path: str):
    cred = credential.Credential(
        os.environ.get("TENCENTCLOUD_SECRET_ID"),
        os.environ.get("TENCENTCLOUD_SECRET_KEY")
    )
    http_profile = HttpProfile()
    http_profile.endpoint = "ocr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = ocr_client.OcrClient(cred, "ap-guangzhou", client_profile)

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    req = models.MedicalInvoiceOCRRequest()
    req.ImageBase64 = img_b64
    resp = client.MedicalInvoiceOCR(req)
    return resp.to_json_string(indent=2)

# print(recognize_tencent_medical("invoice.jpg"))
```

### 3.3 本地自训练 OCR（PyTorch + CRNN）— 参考代码

```python
# ⚠️ 注意：以下为参考架构代码，需要您自行准备训练数据和标注
import torch
import torch.nn as nn
import torchvision.models as models
from torch.nn.utils.rnn import pack_padded_sequence

class CRNN(nn.Module):
    """
    CRNN 参考模型架构：
    CNN（特征提取）→ BiLSTM（序列建模）→ CTC（解码）
    需要自行准备训练数据和训练脚本。
    """
    def __init__(self, num_chars: int, hidden_size: int = 256):
        super().__init__()
        # CNN 主干：EfficientNet-B0（需自行预训练或下载权重）
        backbone = models.efficientnet_b0(weights=None)  # 需自行提供权重
        self.cnn = nn.Sequential(*list(backbone.children())[:-2])
        self.cnn.add_module("adaptive_pool", nn.AdaptiveAvgPool2d((None, 1)))

        # BiLSTM × 2
        self.lstm = nn.LSTM(
            input_size=1280,
            hidden_size=hidden_size,
            num_layers=2,
            bidirectional=True,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_size * 2, num_chars)

    def forward(self, x):
        conv = self.cnn(x)
        conv = conv.squeeze(2)
        conv = conv.permute(0, 2, 1)
        lstm_out, _ = self.lstm(conv)
        logits = self.fc(lstm_out)
        return logits

# 训练需自行准备：
# - 训练数据（标注好的医疗票据图像）
# - CTC Loss 配置
# - 训练脚本
# model = CRNN(num_chars=6624)
# ctc_loss = nn.CTCLoss(zero_infinity=True)
# optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
```

---

## 四、票据结构化字段规范（参考格式）

### 4.1 全国医疗门诊发票标准字段（参考）

```yaml
basic_info:
  invoice_code: str        # 票据代码
  invoice_number: str      # 票据号码
  invoice_date: date      # 开票日期
  verify_code: str        # 校验码
  hospital_name: str     # 医院名称
  hospital_level: str    # 医院等级（三级/二级/一级）

amount_info:
  total: float          # 总金额（含税）
  medical_insurance: float  # 医保统筹支付
  personal_account: float  # 个人账户支付
  self_pay: float       # 个人自付（分类自负）
  self_fund: float      # 个人自费
  deductible: float     # 起付线（免赔额部分）

detail_line_items:        # 费用明细行（数组）
  - name: str           # 药品名称/诊疗项目名称
    specification: str   # 规格
    unit: str           # 单位
    quantity: int       # 数量
    unit_price: float   # 单价
    total_price: float  # 该项总价
    category: str       # 甲类/乙类/丙类/自费
    insurance_code: str  # 医保目录编码

diagnosis:
  icd10_code: str      # ICD-10 诊断编码
  diagnosis_name: str  # 诊断名称（中文）
  department: str      # 就诊科室
```

### 4.2 全国医疗住院发票附加字段（参考）

```yaml
hospitalization:
  admission_date: date  # 入院日期
  discharge_date: date # 出院日期
  stay_days: int       # 住院天数
  bed_number: str     # 床位号
  total_prescriptions: int  # 总处方数
  surgery_name: str   # 手术名称（如有）
  drg_code: str       # DRG 分组编码（如有）
```

---

## 五、多模态融合识别方案（兜底方案参考）

当单一 OCR 效果不佳时（如盖章覆盖文字、票据折叠），可启用多模态大模型作为兜底：

```python
# ⚠️ 注意：多模态大模型也会接收图像数据，须同样遵守数据安全规定
def multimodal_fallback(image_path: str, ocr_result: dict) -> dict:
    """
    OCR 识别置信度低于阈值时，可触发多模态识别作为参考。
    ⚠️ 结果须经人工审核确认。
    """
    import base64, os

    # ⚠️ 建议：发送前对敏感字段做模糊化处理
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    prompt = """
    这是一张医疗发票照片，OCR 识别结果置信度较低。
    请你根据图片内容，提取以下字段（JSON 格式）：
    - 发票号码
    - 开票日期
    - 医院名称
    - 总金额
    - 医保统筹支付
    - 个人自付
    - 临床诊断
    如果图片中看不清楚，则对应字段填 null。
    """

    # 调用多模态 API（须自行配置密钥并遵守数据安全规定）
    # response = call_multimodal_api(
    #     model="qwen-vl-max",
    #     messages=[{
    #         "role": "user",
    #         "content": [
    #             {"image": f"data:image/jpeg;base64,{img_b64}"},
    #             {"text": prompt}
    #         ]
    #     }]
    # )
    # return parse_json_from_response(response)
    raise NotImplementedError("须自行实现多模态API调用，并配置数据安全保护")
```

**触发多模态兜底的条件（参考）：**
- OCR 置信度均值 < 0.75
- 关键字段缺失 ≥ 2 个（发票号 / 金额 / 日期）
- 印章严重遮挡文字区域（通过图像分割检测到大面积红色区域）

---

## 六、部署建议（参考）

| 部署方式 | 适用场景 | 推荐技术栈 | 数据合规建议 |
|-----------|-----------|-----------|--------------|
| **云端 API 调用** | 中小规模（< 10万张/月） | 百度 AI / 腾讯云 SDK | 确认服务商数据留存政策；建议签署数据处理协议 |
| **私有化部署** | 大型保险公司 / 数据不出域 | PyTorchServe + CRNN 自训练模型 | 数据全程不出域，符合《个人信息保护法》要求 |
| **混合架构** | 高可用要求 + 数据合规 | 云端 OCR 预处理 + 本地规则引擎核验 | 云端仅传输必要字段，敏感字段本地处理 |
| **边缘端部署** | 移动端 / 小程序拍照即识别 | NCNN + Int8 量化 CRNN 模型 | 数据在设备端处理，不上传云端 |

---

## 七、数据留存与访问控制（必读）

> ⚠️ **法律合规要求（中国《个人信息保护法》）**

1. **数据最小化原则：** 仅收集和传输理赔处理所必需的最少字段
2. **用户同意：** 将医疗票据发送至OCR服务前，须获得用户明确同意
3. **数据留存期限：** 建议 OCR 服务商不留存数据，或设置 24 小时内自动删除；本地图谱数据留存不超过 2 年
4. **访问控制：** 医疗票据图像和识别结果仅限授权理赔人员访问，禁止非授权人员查看
5. **数据更正权利：** 被保人有权请求更正错误数据，必须在 15 个工作日内处理
6. **跨境数据传输：** 如使用境外OCR服务，须进行数据出境安全评估

---

*Last updated: 2026-05-05 — 添加数据安全声明、API密钥安全提醒、准确率数据标注为厂商基准（非实测）、删除自动审批描述、增加数据留存和访问控制规范。*

---
name: invoice-ocr
description: 发票 OCR 识别技能。扫描文件夹中的发票文件（PDF/图片），调用阿里云 OCR API 识别发票信息并导出到 Excel 表格。支持 17+ 种发票类型（增值税发票、火车票、出租车票、机票行程单、定额发票、机动车销售发票、过路过桥费发票等）。使用场景：(1) 用户提到"发票识别"、"发票统计"、"发票整理"、"发票汇总" (2) 用户需要批量处理发票 (3) 用户提到阿里云 OCR 识别发票。**重要：首次使用必须先配置阿里云凭证，主动向用户索要 AccessKey ID 和 AccessKey Secret，或引导用户运行 --config 命令自行配置。**
---

# 发票 OCR 识别技能

批量识别发票并汇总到 Excel 表格。

## ⚠️ 首次使用必须配置凭证

**此技能需要阿里云 OCR 服务，使用前必须先配置凭证！**

### 方式一：向用户提供凭证（推荐）

主动询问用户：
> "使用此技能需要阿里云 AccessKey ID 和 AccessKey Secret，请提供这两个凭证。\
> 获取方式：阿里云控制台 → 开通票据凭证识别 → 创建 AccessKey"

然后运行：
```bash
python scripts/recognize_invoices.py --config
```

### 方式二：引导用户自行配置

告诉用户：
> "请先运行以下命令配置阿里云凭证："
> ```bash
> python ~/.openclaw/skills/invoice-ocr/scripts/recognize_invoices.py --config
> ```

## 特点

- ✅ **17+ 发票类型** - 自动识别发票类型
- ✅ **Excel 输出** - 生成标准 xlsx 文件
- ✅ **支持 PDF/OFD** - 电子发票友好

## 依赖安装

```bash
pip install openpyxl
```

## 支持的发票类型

| 类型 | 说明 |
|------|------|
| 增值税发票 | 专用发票、普通发票、电子发票 |
| 火车票 | 火车票识别 |
| 出租车发票 | 机打发票 |
| 定额发票 | 手撕发票 |
| 机票行程单 | 航空运输电子客票 |
| 机动车销售发票 | 购车发票 |
| 网约车行程单 | 滴滴等平台发票 |
| 过路过桥费 | 高速公路发票 |
| 客运车船票 | 汽车票、船票 |
| 税收完税证明 | 完税凭证 |
| 银行承兑汇票 | 票据识别 |

## 支持的文件格式

| 格式 | 扩展名 |
|------|--------|
| PDF | .pdf |
| OFD | .ofd |
| 图片 | .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp |

## 输出字段

按以下顺序输出到 Excel：

| 字段 | 说明 |
|------|------|
| 发票号码 | 发票代码 + 发票号码 |
| 开票日期 | 开票日期 |
| 购买方信息 | 购买方名称 |
| 销售方信息 | 销售方名称 |
| 项目名称 | 商品/服务名称 |
| 规格型号 | 商品规格 |
| 单位 | 计量单位 |
| 数量 | 商品数量 |
| 单价 | 商品单价 |
| 金额 | 不含税金额 |
| 税率 | 税率百分比 |
| 税额 | 税金金额 |
| 价税合计 | 含税总额 |

**注意：** 如果发票上某字段不存在，默认填空值。

## 使用方法

### 识别发票

```bash
# 识别文件夹中的所有发票
python scripts/recognize_invoices.py /path/to/invoices

# 指定输出文件
python scripts/recognize_invoices.py /path/to/invoices --output 发票汇总.xlsx
```

### 配置管理

```bash
# 设置阿里云凭证
python scripts/recognize_invoices.py --config

# 查看当前配置
python scripts/recognize_invoices.py --list-config
```

## 获取阿里云 AccessKey

1. 登录 [阿里云控制台](https://www.aliyun.com/)
2. 开通 [票据凭证识别](https://common-buy.aliyun.com/?commodityCode=ocr_invoice_public_cn) 服务
3. 创建 AccessKey（建议使用 RAM 子账号）
4. 授予 `AliyunOCRFullAccess` 权限

详细 API 说明见 [阿里云 OCR API 参考](references/aliyun-ocr-api.md)

## 工作流程

```
发票文件 → OCR识别 → Excel表格
   ↓           ↓         ↓
 PDF/图片   混贴识别   xlsx文件
```

## 注意事项

1. 图片需清晰，建议长宽 > 500px
2. 单个文件不超过 10MB
3. 阿里云 OCR 按次计费，注意费用控制
4. 配置文件保存在技能目录下的 config.json
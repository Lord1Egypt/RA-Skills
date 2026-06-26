---
name: "poocr-vatinvoice2excel"
description: "使用 poocr 库识别发票并导出 Excel。当用户需要识别增值税发票、批量处理发票文件或提取发票信息到 Excel 时调用此技能。"
---

# POOCR 发票识别技能

这个技能使用 poocr 库（基于腾讯云 AI）实现增值税发票的 OCR 识别，并将识别结果保存为 Excel 文件。

## 功能特性

- 支持单张发票识别
- 支持批量识别文件夹中的发票
- 支持多种发票格式：PDF、JPG、PNG
- 自动提取发票关键信息：发票号码、开票日期、金额、税额等
- 结果直接导出为 Excel 格式

## 使用方法

### 1. 安装依赖

```bash
pip install poocr
```

### 2. 配置腾讯云 API 密钥

需要获取腾讯云 API 的 SecretId 和 SecretKey：
- 访问 [腾讯云控制台](https://curl.qcloud.com/9ExTmaya) 获取密钥

### 3. 代码示例

```python
import poocr

# 单张发票识别并导出 Excel
poocr.ocr2excel.VatInvoiceOCR2Excel(
    input_path='发票文件路径.pdf',
    output_path='输出目录',
    id='你的SecretId',
    key='你的SecretKey'
)

# 批量识别文件夹中的发票
poocr.ocr2excel.VatInvoiceOCR2Excel(
    input_path='发票文件夹路径',
    output_path='输出目录',
    id='你的SecretId',
    key='你的SecretKey'
)
```

## 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| input_path | str | 发票文件路径或包含发票的文件夹路径 |
| output_path | str | 输出 Excel 文件的目录路径 |
| id | str | 腾讯云 API SecretId |
| key | str | 腾讯云 API SecretKey |

## 使用场景

1. **财务报销**：批量识别员工提交的发票，自动提取关键信息
2. **税务处理**：快速整理大量发票数据用于税务申报
3. **数据录入**：将纸质发票或电子发票信息数字化
4. **审计工作**：批量处理发票数据进行分析

## 注意事项

1. 确保腾讯云 API 密钥有效且有足够的调用额度
2. 支持的发票类型：增值税普通发票、增值税专用发票等
3. 图片质量会影响识别准确率，建议使用清晰的发票图片或 PDF
4. 批量处理时，程序会自动遍历文件夹中的所有发票文件

## 完整示例代码

```python
import poocr
import os

class InvoiceOCR:
    def __init__(self, secret_id, secret_key):
        self.SecretId = secret_id
        self.SecretKey = secret_key
    
    def recognize_invoice(self, input_path, output_path):
        """识别发票并导出 Excel"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")
        
        poocr.ocr2excel.VatInvoiceOCR2Excel(
            input_path=input_path,
            output_path=output_path,
            id=self.SecretId,
            key=self.SecretKey
        )
        
        print(f"发票识别完成，结果已保存到: {output_path}")

# 使用示例
if __name__ == "__main__":
    ocr = InvoiceOCR(
        secret_id="你的SecretId",
        secret_key="你的SecretKey"
    )
    
    ocr.recognize_invoice(
        input_path="../test_files/VatInvoiceOCR",
        output_path="../test_files/VatInvoiceOCR"
    )
```

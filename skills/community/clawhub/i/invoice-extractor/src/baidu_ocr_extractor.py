"""
百度OCR发票识别提取器
使用百度智能云OCR API进行发票识别
"""

import re
import base64
import requests
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

from invoice_model import InvoiceInfo, InvoiceItem


class BaiduOCRConfig:
    """百度OCR配置"""
    # 默认使用免费额度（QPS=2）
    API_KEY = ""  # 需要用户填写
    SECRET_KEY = ""  # 需要用户填写
    
    # 发票识别接口
    INVOICE_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice"
    # 通用文字识别（高精度）
    GENERAL_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


class BaiduInvoiceExtractor:
    """使用百度OCR的发票提取器"""

    def __init__(self, api_key: str = None, secret_key: str = None):
        """
        初始化百度OCR提取器
        
        Args:
            api_key: 百度智能云API Key
            secret_key: 百度智能云Secret Key
        """
        self.api_key = api_key or BaiduOCRConfig.API_KEY
        self.secret_key = secret_key or BaiduOCRConfig.SECRET_KEY
        self.access_token = None
        
        if self.api_key and self.secret_key:
            self._get_access_token()

    def _get_access_token(self) -> bool:
        """获取百度OCR访问令牌"""
        try:
            url = f"https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }
            response = requests.post(url, params=params, timeout=10)
            result = response.json()
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("[OK] 百度OCR认证成功")
                return True
            else:
                print(f"[FAIL] 百度OCR认证失败: {result.get('error_description', '未知错误')}")
                return False
        except Exception as e:
            print(f"[FAIL] 获取访问令牌失败: {e}")
            return False

    def extract_from_file(self, file_path: str) -> Optional[InvoiceInfo]:
        """
        从文件中提取发票信息
        
        Args:
            file_path: 文件路径（图片或PDF）
            
        Returns:
            InvoiceInfo对象，提取失败返回None
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"[FAIL] 文件不存在: {file_path}")
            return None
            
        if not self.access_token:
            print("[FAIL] 百度OCR未认证，请配置API Key和Secret Key")
            return None
        
        # 检查文件类型
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            # PDF文件需要转换为图片
            return self._extract_from_pdf(file_path)
        elif suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']:
            # 图片文件直接处理
            return self._extract_from_image(file_path)
        else:
            print(f"[FAIL] 不支持的文件格式: {suffix}")
            return None

    def _extract_from_image(self, image_path: Path) -> Optional[InvoiceInfo]:
        """从图片中提取发票信息"""
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"[FAIL] 读取图片失败: {e}")
            return None
        
        # 首先尝试使用增值税发票识别接口
        invoice_info = self._recognize_vat_invoice(image_data)
        
        if invoice_info:
            invoice_info.source_file = str(image_path)
            invoice_info.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return invoice_info
        
        # 如果发票识别失败，使用通用文字识别
        print("发票识别失败，尝试通用文字识别...")
        return self._recognize_general(image_data, image_path)

    def _extract_from_pdf(self, pdf_path: Path) -> Optional[InvoiceInfo]:
        """从PDF中提取发票信息（先将PDF转为图片）"""
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            
            print("正在将PDF转换为图片...")
            
            # 打开PDF
            doc = fitz.open(str(pdf_path))
            
            # 获取第一页
            page = doc[0]
            
            # 将页面转换为图片（2倍分辨率提高清晰度）
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            # 转换为PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # 保存到内存
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # 转为base64
            image_data = base64.b64encode(img_buffer.read()).decode('utf-8')
            
            doc.close()
            
            # 使用增值税发票识别接口
            invoice_info = self._recognize_vat_invoice(image_data)
            
            if invoice_info:
                invoice_info.source_file = str(pdf_path)
                invoice_info.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return invoice_info
            
            # 如果发票识别失败，使用通用文字识别
            print("发票识别失败，尝试通用文字识别...")
            return self._recognize_general(image_data, pdf_path)
            
        except Exception as e:
            print(f"[FAIL] PDF处理失败: {e}")
            return None

    def _recognize_vat_invoice(self, image_data: str) -> Optional[InvoiceInfo]:
        """使用增值税发票识别接口"""
        try:
            url = f"{BaiduOCRConfig.INVOICE_URL}?access_token={self.access_token}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            params = {"image": image_data}
            
            response = requests.post(url, data=params, headers=headers, timeout=30)
            result = response.json()
            
            if "words_result" in result:
                return self._parse_vat_invoice_result(result["words_result"])
            elif "error_code" in result:
                print(f"[WARN] 发票识别接口错误: {result.get('error_msg', '未知错误')}")
                return None
            else:
                return None
                
        except Exception as e:
            print(f"[FAIL] 发票识别请求失败: {e}")
            return None

    def _parse_vat_invoice_result(self, result: Dict) -> Optional[InvoiceInfo]:
        """解析增值税发票识别结果"""
        invoice = InvoiceInfo()
        
        # 基本信息
        invoice.invoice_code = result.get("InvoiceCode", "")
        invoice.invoice_number = result.get("InvoiceNum", "")
        invoice.invoice_date = result.get("InvoiceDate", "")
        invoice.invoice_type = result.get("InvoiceType", "")
        
        # 购买方信息
        buyer_info = result.get("BuyerName", {})
        if isinstance(buyer_info, dict):
            invoice.buyer_name = buyer_info.get("word", "")
        else:
            invoice.buyer_name = str(buyer_info)
            
        invoice.buyer_tax_number = result.get("BuyerRegisterNum", "")
        invoice.buyer_address = result.get("BuyerAddress", "")
        invoice.buyer_bank = result.get("BuyerBank", "")
        
        # 销售方信息
        seller_info = result.get("SellerName", {})
        if isinstance(seller_info, dict):
            invoice.seller_name = seller_info.get("word", "")
        else:
            invoice.seller_name = str(seller_info)
            
        invoice.seller_tax_number = result.get("SellerRegisterNum", "")
        invoice.seller_address = result.get("SellerAddress", "")
        invoice.seller_bank = result.get("SellerBank", "")
        
        # 金额信息
        invoice.total_amount = self._parse_amount(result.get("TotalAmount", "0"))
        invoice.total_tax_amount = self._parse_amount(result.get("TotalTax", "0"))
        invoice.total_amount_with_tax = self._parse_amount(result.get("AmountInFiguers", "0"))
        
        # 其他信息
        invoice.remarks = result.get("Remarks", "")
        invoice.checker = result.get("Checker", "")
        invoice.payee = result.get("Payee", "")
        invoice.issuer = result.get("NoteDrawer", "")
        
        # 商品明细
        commodity_names = result.get("CommodityName", [])
        commodity_nums = result.get("CommodityNum", [])
        commodity_prices = result.get("CommodityPrice", [])
        commodity_amounts = result.get("CommodityAmount", [])
        commodity_tax_rates = result.get("CommodityTaxRate", [])
        commodity_tax_amounts = result.get("CommodityTax", [])
        
        for i in range(len(commodity_names)):
            item = InvoiceItem()
            name_info = commodity_names[i]
            item.name = name_info.get("word", "") if isinstance(name_info, dict) else str(name_info)
            
            if i < len(commodity_nums):
                num_info = commodity_nums[i]
                item.quantity = self._parse_amount(num_info.get("word", "0") if isinstance(num_info, dict) else str(num_info))
            
            if i < len(commodity_prices):
                price_info = commodity_prices[i]
                item.unit_price = self._parse_amount(price_info.get("word", "0") if isinstance(price_info, dict) else str(price_info))
            
            if i < len(commodity_amounts):
                amount_info = commodity_amounts[i]
                item.amount = self._parse_amount(amount_info.get("word", "0") if isinstance(amount_info, dict) else str(amount_info))
            
            if i < len(commodity_tax_rates):
                rate_info = commodity_tax_rates[i]
                item.tax_rate = rate_info.get("word", "") if isinstance(rate_info, dict) else str(rate_info)
            
            if i < len(commodity_tax_amounts):
                tax_info = commodity_tax_amounts[i]
                item.tax_amount = self._parse_amount(tax_info.get("word", "0") if isinstance(tax_info, dict) else str(tax_info))
            
            if item.name:
                invoice.items.append(item)
        
        return invoice

    def _recognize_general(self, image_data: str, file_path: Path) -> Optional[InvoiceInfo]:
        """使用通用文字识别（高精度版）"""
        try:
            url = f"{BaiduOCRConfig.GENERAL_URL}?access_token={self.access_token}"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            params = {
                "image": image_data,
                "detect_direction": "true",
                "probability": "false"
            }
            
            response = requests.post(url, data=params, headers=headers, timeout=30)
            result = response.json()
            
            if "words_result" in result:
                text_lines = [item["words"] for item in result["words_result"]]
                
                # 使用本地解析逻辑
                from invoice_extractor import InvoiceExtractor
                local_extractor = InvoiceExtractor.__new__(InvoiceExtractor)
                invoice = local_extractor._parse_invoice_text(text_lines)
                invoice.source_file = str(file_path)
                invoice.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return invoice
            else:
                print(f"[FAIL] 通用识别失败: {result.get('error_msg', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"[FAIL] 通用识别请求失败: {e}")
            return None

    def _parse_amount(self, value) -> float:
        """解析金额字符串"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # 移除货币符号和逗号
            value = value.replace('元', '').replace('元', '').replace(',', '').replace('，', '').strip()
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0


def extract_invoices_with_baidu(directory: str, api_key: str = None, secret_key: str = None) -> List[InvoiceInfo]:
    """
    使用百度OCR从目录中提取所有发票信息
    
    Args:
        directory: 包含发票文件的目录路径
        api_key: 百度智能云API Key
        secret_key: 百度智能云Secret Key
        
    Returns:
        InvoiceInfo对象列表
    """
    directory = Path(directory)
    
    if not directory.exists():
        print(f"[FAIL] 目录不存在: {directory}")
        return []
    
    # 支持的文件扩展名
    extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.pdf'}
    
    # 获取所有支持的文件
    files = [f for f in directory.iterdir() if f.suffix.lower() in extensions]
    
    if not files:
        print(f"[FAIL] 目录中没有找到发票文件: {directory}")
        return []
    
    print(f"发现 {len(files)} 个待处理文件")
    
    # 初始化百度OCR提取器
    extractor = BaiduInvoiceExtractor(api_key, secret_key)
    
    if not extractor.access_token:
        print("[FAIL] 百度OCR认证失败，请检查API Key和Secret Key")
        return []
    
    invoices = []
    
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] 处理: {file_path.name}")
        invoice = extractor.extract_from_file(str(file_path))
        if invoice:
            invoices.append(invoice)
            print(f"[OK] 成功提取: {invoice.invoice_number or '未识别号码'}")
        else:
            print(f"[FAIL] 提取失败")
    
    return invoices

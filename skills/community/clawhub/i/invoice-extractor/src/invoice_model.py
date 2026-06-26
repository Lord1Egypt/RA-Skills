"""
发票数据模型
定义发票信息的结构化数据类
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class InvoiceItem:
    """发票商品明细项"""
    name: str = ""                    # 货物或应税劳务名称
    specification: str = ""           # 规格型号
    unit: str = ""                    # 单位
    quantity: float = 0.0             # 数量
    unit_price: float = 0.0           # 单价
    amount: float = 0.0               # 金额
    tax_rate: str = ""                # 税率
    tax_amount: float = 0.0           # 税额


@dataclass
class InvoiceInfo:
    """发票信息数据类"""
    # 基本信息
    invoice_code: str = ""            # 发票代码
    invoice_number: str = ""          # 发票号码
    invoice_date: str = ""            # 开票日期
    invoice_type: str = ""            # 发票类型

    # 购买方信息
    buyer_name: str = ""              # 购买方名称
    buyer_tax_number: str = ""        # 购买方纳税人识别号
    buyer_address: str = ""           # 购买方地址电话
    buyer_bank: str = ""              # 购买方开户行及账号

    # 销售方信息
    seller_name: str = ""             # 销售方名称
    seller_tax_number: str = ""       # 销售方纳税人识别号
    seller_address: str = ""          # 销售方地址电话
    seller_bank: str = ""             # 销售方开户行及账号

    # 金额信息
    total_amount: float = 0.0         # 合计金额
    total_tax_amount: float = 0.0     # 合计税额
    total_amount_with_tax: float = 0.0  # 价税合计

    # 商品明细
    items: List[InvoiceItem] = field(default_factory=list)

    # 其他信息
    remarks: str = ""                 # 备注
    machine_number: str = ""          # 机器编号
    checker: str = ""                 # 复核人
    payee: str = ""                   # 收款人
    issuer: str = ""                  # 开票人

    # 源文件信息
    source_file: str = ""             # 源文件路径
    extraction_time: str = ""         # 提取时间

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "发票代码": self.invoice_code,
            "发票号码": self.invoice_number,
            "开票日期": self.invoice_date,
            "发票类型": self.invoice_type,
            "购买方名称": self.buyer_name,
            "购买方税号": self.buyer_tax_number,
            "购买方地址电话": self.buyer_address,
            "购买方开户行": self.buyer_bank,
            "销售方名称": self.seller_name,
            "销售方税号": self.seller_tax_number,
            "销售方地址电话": self.seller_address,
            "销售方开户行": self.seller_bank,
            "合计金额": self.total_amount,
            "合计税额": self.total_tax_amount,
            "价税合计": self.total_amount_with_tax,
            "备注": self.remarks,
            "机器编号": self.machine_number,
            "复核人": self.checker,
            "收款人": self.payee,
            "开票人": self.issuer,
            "源文件": self.source_file,
            "提取时间": self.extraction_time,
        }

    def get_items_summary(self) -> str:
        """获取商品明细摘要"""
        if not self.items:
            return ""
        item_names = [item.name for item in self.items if item.name]
        return "、".join(item_names[:3]) + ("..." if len(item_names) > 3 else "")

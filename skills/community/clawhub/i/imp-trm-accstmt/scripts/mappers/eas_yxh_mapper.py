"""
EAS_YXH (金蝶云星瀚) 映射器
将银行对账单数据映射到 金蝶云星瀚 系统银行流水导入模板。

模板: assets/template/eas_yxh_banktransaction.xlsx
- Sheet: sheet1
- 数据从第 5 行开始写入
- 第 3 行：英文字段名（如 bizdate, currency.number 等）
- 第 4 行：中文字段名（带 * 为必录）+ 单元格批注（数据格式要求）
- 模板自带 dropdown_items_sheet（业务类型下拉）和 basedata_items_sheet

模板加载策略（兼容 clawhub 等不支持上传二进制模板的市场）：
1. 优先使用调用方显式传入的 template_path
2. 其次查找 skills/<skill>/assets/template/eas_yxh_banktransaction.xlsx
3. 仍不存在则从配置的互联网地址自动下载到本地
"""

import os
import logging
import shutil
from decimal import Decimal
from typing import Optional, List, Dict, Any
from datetime import datetime

import openpyxl

from mappers.base_mapper import BaseMapper
from core.data_structures import (
    BankStatementData, MappedRecord, MappingResult, ValidationResult,
    TransactionRecord,
)
from core.currency_map import get_currency_name

logger = logging.getLogger(__name__)


class EasYxhMapper(BaseMapper):
    """金蝶云星瀚 EAS Cloud Star 系统银行流水映射器"""

    # EAS_YXH 必填字段
    REQUIRED_FIELDS = [
        'bizdate',           # 交易日期
        'currency.number',   # 币种.货币代码
        'accountbank.bankaccountnumber',  # 银行账号.银行账号
        'detailid',          # 明细流水号
    ]

    # 模板列索引（0-based）— 与第 3 行英文字段名对应
    COLUMNS = [
        'bizdate',                        # 0: 交易日期
        'currency.number',                # 1: 币种.货币代码
        'currency.name',                  # 2: 币种.名称
        'accountbank.bankaccountnumber',  # 3: 银行账号.银行账号
        'accountbank.name',               # 4: 银行账号.账户简称
        'biztype',                        # 5: 业务类型
        'description',                    # 6: 摘要
        'debitamount',                    # 7: 付款金额
        'creditamount',                   # 8: 收款金额
        'transbalance',                   # 9: 余额
        'oppunit',                        # 10: 对方户名
        'oppbanknumber',                  # 11: 对方账号
        'oppbank',                        # 12: 对方开户行
        'bankcheckflag',                  # 13: 对账标识码
        'detailid',                       # 14: 明细流水号
        'receiptno',                      # 15: 电子回单关联标记
        'frmcod',                         # 16: 企业识别码
        'bizrefno',                       # 17: 业务参考号
        'biztime',                        # 18: 交易时间
        'bankdetailno',                   # 19: 银行流水号
    ]

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or self._default_template_path()

    def _default_template_path(self) -> str:
        """默认模板路径：统一通过 template_manager 解析（本地查找 + 自动下载）"""
        from core.template_manager import resolve_template
        resolved = resolve_template('EAS_YXH')
        if resolved:
            return resolved
        # 兜底：直接拼接路径（仅在模板解析失败时使用，文件可能不存在）
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base, 'assets', 'template', 'eas_yxh_banktransaction.xlsx')

    @property
    def target_system(self) -> str:
        return "EAS_YXH"

    @property
    def required_fields(self) -> List[str]:
        return self.REQUIRED_FIELDS

    def map(self, source_data: BankStatementData, **kwargs) -> MappingResult:
        result = MappingResult(source_data=source_data)

        for idx, txn in enumerate(source_data.transactions):
            try:
                record = self._map_transaction(txn, idx, source_data, kwargs)
                mapped = MappedRecord(record=record, source_transaction=txn)
                result.mapped_records.append(mapped)
                result.successful_count += 1
            except Exception as e:
                logger.exception(f"Failed to map transaction {idx+1}: {e}")
                result.mapped_records.append(MappedRecord(
                    record={}, source_transaction=txn, mapping_errors=[str(e)]
                ))
                result.failed_count += 1

        result.warnings.extend(source_data.parse_warnings)
        return result

    def _map_transaction(
        self,
        txn: TransactionRecord,
        idx: int,
        source_data: BankStatementData,
        kwargs: dict,
    ) -> Dict[str, Any]:
        """映射单条交易到 EAS_YXH 字段"""
        # 准备 user_provided 数据
        user_acct = source_data.user_provided_account_code
        user_bank = source_data.user_provided_bank_name
        account_number = txn.account_number or user_acct

        # 本方户名（账户开户人）— 从源文件的 header 中提取
        account_name = source_data.header.raw_tags.get('account_name', '') or user_bank

        # 业务日期（YYYY-MM-DD）
        bizdate = self._format_date(txn.value_date)

        # 业务时间（HH:MM:SS）
        biztime = self._format_time(txn.transaction_time)

        # 币种代码（CNY / USD 等）
        currency_code = (txn.currency_code or 'CNY').upper()

        # 借贷标识 → 业务类型
        biztype = self._map_biztype(txn)

        # 金额
        debitamount = str(txn.debit_amount) if txn.debit_amount > 0 else ''
        creditamount = str(txn.credit_amount) if txn.credit_amount > 0 else ''
        transbalance = str(txn.running_balance) if txn.running_balance else ''

        # 对账标识码（用 unique_no）
        bankcheckflag = self._generate_hash_id(txn, idx, source_data)

        # 记录
        record = {
            'bizdate': bizdate,
            'currency.number': currency_code,
            'currency.name': get_currency_name(currency_code),
            'accountbank.bankaccountnumber': account_number,
            'accountbank.name': account_name,
            'biztype': biztype,
            'description': txn.transaction_description or '',
            'debitamount': debitamount,
            'creditamount': creditamount,
            'transbalance': transbalance,
            'oppunit': txn.counterparty_name or '',
            'oppbanknumber': txn.counterparty_account or '',
            'oppbank': txn.counterparty_bank or '',
            'bankcheckflag': bankcheckflag,
            'detailid': txn.reference_number or f"DET_{idx+1:08d}",
            'receiptno': '',
            'frmcod': '',
            'bizrefno': '',
            'biztime': biztime,
            'bankdetailno': txn.reference_number or '',
        }
        return record

    def _format_date(self, value_date: str) -> str:
        """将 YYYYMMDD 转为 YYYY-MM-DD"""
        if not value_date or len(value_date) != 8:
            return value_date
        return f"{value_date[:4]}-{value_date[4:6]}-{value_date[6:8]}"

    def _format_time(self, txn_time: str) -> str:
        """将 HHMMSS 转为 HH:MM:SS"""
        if not txn_time or len(txn_time) != 6:
            return ''
        return f"{txn_time[:2]}:{txn_time[2:4]}:{txn_time[4:6]}"

    def _map_biztype(self, txn: TransactionRecord) -> str:
        """根据借贷标识映射业务类型（取下拉项）"""
        if txn.dc_indicator in ('D', 'RD'):
            return '普通'  # 默认普通；用户可改
        elif txn.dc_indicator in ('C', 'RC'):
            return '普通'
        return '普通'

    def _generate_hash_id(self, txn: TransactionRecord, idx: int, source_data: BankStatementData) -> str:
        """生成对账标识码（基于交易特征）"""
        import hashlib
        raw = f"{txn.value_date}|{txn.amount}|{txn.counterparty_account}|{idx}"
        return hashlib.md5(raw.encode()).hexdigest()[:32]

    def validate(self, mapping_result: MappingResult) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        for idx, mr in enumerate(mapping_result.mapped_records):
            record = mr.record
            for field in self.REQUIRED_FIELDS:
                if not record.get(field):
                    result.warnings.append(
                        f"行 {idx+5}: 必填字段 '{field}' 为空"
                    )
        if result.warnings:
            result.is_valid = False
        return result

    def write_output(
        self,
        mapping_result: MappingResult,
        output_path: str,
        template_path: Optional[str] = None,
    ) -> str:
        """
        写入 EAS_YXH 模板（xlsx）
        数据从第 5 行开始写入
        """
        template = template_path or self.template_path
        if not os.path.exists(template):
            raise FileNotFoundError(f"EAS_YXH 模板不存在: {template}")

        # 复制模板到输出路径
        shutil.copy2(template, output_path)

        # 打开输出文件，写入数据
        wb = openpyxl.load_workbook(output_path)
        ws = wb['sheet1']

        data_start_row = 5
        for row_idx, mr in enumerate(mapping_result.mapped_records):
            record = mr.record
            excel_row = data_start_row + row_idx
            for col_idx, field in enumerate(self.COLUMNS, 1):
                value = record.get(field, '')
                if value is None:
                    value = ''
                # 转换为字符串（日期/时间已是字符串）
                cell = ws.cell(row=excel_row, column=col_idx, value=value)
                # 必填字段标红（仅设置字体色，由用户审阅）
                if field in self.REQUIRED_FIELDS and not value:
                    cell.font = openpyxl.styles.Font(color='FF0000')

        wb.save(output_path)
        logger.info(f"EAS_YXH 输出已保存: {output_path}（共 {len(mapping_result.mapped_records)} 条）")
        return output_path


def create_eas_yxh_mapper(template_path: Optional[str] = None) -> EasYxhMapper:
    """工厂函数：创建 EAS_YXH 映射器"""
    return EasYxhMapper(template_path)

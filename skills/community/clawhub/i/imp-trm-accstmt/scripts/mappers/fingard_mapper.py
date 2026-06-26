"""
Fingard (保融ATS) 映射器
将银行对账单数据映射到 保融ATS 系统银行流水导入模板。

模板: assets/template/fingard_banktransaction.xls
- Sheet: 离线信息
- 数据从第 2 行开始写入（第 1 行是表头）
- 字段说明 sheet 中含字段格式要求

模板加载策略（兼容 clawhub 等不支持上传二进制模板的市场）：
1. 优先使用调用方显式传入的 template_path
2. 其次查找 skills/<skill>/assets/template/fingard_banktransaction.xls
3. 仍不存在则从配置的互联网地址自动下载到本地
"""

import os
import logging
import shutil
from decimal import Decimal
from typing import Optional, List, Dict, Any

import xlrd

from mappers.base_mapper import BaseMapper
from core.data_structures import (
    BankStatementData, MappedRecord, MappingResult, ValidationResult,
    TransactionRecord,
)
from core.currency_map import get_currency_name

logger = logging.getLogger(__name__)


class FingardMapper(BaseMapper):
    """保融ATS Fingard 系统银行流水映射器"""

    # Fingard 必填字段
    REQUIRED_FIELDS = [
        'org',           # 组织（必填）
        'account',       # 账号（必填）
        'currency',      # 币种（必填）
        'bizdate',       # 交易日期（必填）
        'biztime',       # 交易时间（必填）
        # 借方/贷方发生额 必填其一
    ]

    # Fingard 列索引（0-based）— 与模板 28 列（A-AB）严格对应
    COLUMNS = [
        'org',              # 0: A列 组织
        'account',          # 1: B列 账号
        'currency',         # 2: C列 币种
        'bizdate',          # 3: D列 交易日期
        'biztime',          # 4: E列 交易时间
        'debitamount',      # 5: F列 借方发生额
        'creditamount',     # 6: G列 贷方发生额
        'oppname',          # 7: H列 对方户名
        'oppaccount',       # 8: I列 对方账号
        'oppbank',          # 9: J列 对方银行
        'oppbankbranch',    # 10: K列 对方开户行
        'billtype',         # 11: L列 票据类型
        'billno',           # 12: M列 票据号
        'checkcode',        # 13: N列 对账码
        'remark',           # 14: O列 备注
        'use',              # 15: P列 用途
        'biztype',          # 16: Q列 业务类型
        'bank_internal_no', # 17: R列 银行账务流水号
        'bank_seq_no',      # 18: S列 银行流水号
        'balance',          # 19: T列 余额
        'receipt_type',     # 20: U列 业务回单类型
        'receipt_info',     # 21: V列 回单个性化信息
        'biz_no',           # 22: W列 业务编号
        'return_flag',      # 23: X列 银行退汇标识
        'return_date',      # 24: Y列 退汇日期
        'extra_remark',     # 25: Z列 摘要（额外）
        'sales_platform',   # 26: AA列 销售平台
        'shop',             # 27: AB列 店铺
    ]

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or self._default_template_path()

    def _default_template_path(self) -> str:
        """默认模板路径：统一通过 template_manager 解析（本地查找 + 自动下载）"""
        from core.template_manager import resolve_template
        resolved = resolve_template('FINGARD')
        if resolved:
            return resolved
        # 兜底：直接拼接路径（仅在模板解析失败时使用，文件可能不存在）
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base, 'assets', 'template', 'fingard_banktransaction.xls')

    @property
    def target_system(self) -> str:
        return "FINGARD"

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
        user_acct = source_data.user_provided_account_code
        user_org = kwargs.get('org', '')  # 组织字段从 kwargs 取
        account_number = txn.account_number or user_acct
        currency_code = (txn.currency_code or 'CNY').upper()
        currency_name = get_currency_name(currency_code)

        # Fingard 要求：借方/贷方发生额必填其一
        debit = str(txn.debit_amount) if txn.debit_amount > 0 else ''
        credit = str(txn.credit_amount) if txn.credit_amount > 0 else ''

        record = {
            'org': user_org,
            'account': account_number,
            'currency': currency_name,
            'bizdate': self._format_date(txn.value_date),
            'biztime': self._format_time(txn.transaction_time),
            'debitamount': debit,
            'creditamount': credit,
            'oppname': txn.counterparty_name or '',
            'oppaccount': txn.counterparty_account or '',
            'oppbank': txn.counterparty_bank or '',
            'oppbankbranch': txn.counterparty_bank or '',
            'billtype': '',
            'billno': '',  # 票据号（M列）— 源数据无对应字段
            'checkcode': '',
            'remark': txn.transaction_description or '',
            'use': txn.supplementary_details or '',
            'biztype': '',
            'bank_internal_no': '',  # 银行账务流水号（R列）— 源数据无对应字段
            'bank_seq_no': txn.reference_number or '',  # 银行流水号（S列）★
            'balance': str(txn.running_balance) if txn.running_balance else '',
            'receipt_type': '',
            'receipt_info': '',
            'biz_no': '',
            'return_flag': '',
            'return_date': '',
            'extra_remark': '',
            'sales_platform': '',
            'shop': '',
        }
        return record

    def _format_date(self, value_date: str) -> str:
        if not value_date or len(value_date) != 8:
            return value_date
        return f"{value_date[:4]}-{value_date[4:6]}-{value_date[6:8]}"

    def _format_time(self, txn_time: str) -> str:
        if not txn_time or len(txn_time) != 6:
            return ''
        return f"{txn_time[:2]}:{txn_time[2:4]}:{txn_time[4:6]}"

    def validate(self, mapping_result: MappingResult) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        for idx, mr in enumerate(mapping_result.mapped_records):
            record = mr.record
            for field in self.REQUIRED_FIELDS:
                if field in ('debitamount', 'creditamount'):
                    # 借方/贷方 必填其一
                    if not record.get('debitamount') and not record.get('creditamount'):
                        result.warnings.append(
                            f"行 {idx+2}: 借方/贷方发生额 必填其一"
                        )
                elif not record.get(field):
                    result.warnings.append(
                        f"行 {idx+2}: 必填字段 '{field}' 为空"
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
        写入 Fingard 模板（xls）
        - 复制 .xls 模板（保留字体/列宽/格式）
        - 覆盖数据单元格，不改变样式
        - 保留所有辅助 sheet（如 字段说明）
        """
        template = template_path or self.template_path
        if not os.path.exists(template):
            raise FileNotFoundError(f"Fingard 模板不存在: {template}")

        # 转为 record 列表
        records = [mr.record for mr in mapping_result.mapped_records]

        # 使用辅助函数：复制模板 + 写数据 + 保留额外 sheet
        from mappers._xls_template_helpers import write_xls_with_template
        write_xls_with_template(
            template_path=template,
            output_path=output_path,
            main_sheet_name='离线信息',
            main_data_start_row_0based=1,  # 第 2 行（0-based 索引 1）
            column_field_map=self.COLUMNS,
            records=records,
            extra_sheet_names=['字段说明'],
        )
        logger.info(f"Fingard 输出已保存: {output_path}（共 {len(records)} 条）")
        return output_path

        # 字段说明 sheet
        if desc_sheet is not None:
            ds = new_wb.add_sheet('字段说明', cell_overwrite_ok=True)
            for r in range(desc_sheet.nrows):
                for c in range(desc_sheet.ncols):
                    val = desc_sheet.cell_value(r, c)
                    if val != '':
                        ds.write(r, c, val)

        new_wb.save(output_path)
        logger.info(f"Fingard 输出已保存: {output_path}（共 {len(mapping_result.mapped_records)} 条）")
        return output_path


def create_fingard_mapper(template_path: Optional[str] = None) -> FingardMapper:
    return FingardMapper(template_path)

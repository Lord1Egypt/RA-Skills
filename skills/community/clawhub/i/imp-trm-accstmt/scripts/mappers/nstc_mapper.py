"""
NSTC (九恒星司库) 映射器
将银行对账单数据映射到 九恒星司库 系统银行流水导入模板。

模板: assets/template/nstc_banktransaction.xls
- Sheet 1: 批量导入银行明细格式（必须为第一个 sheet）
  - 数据从第 2 行开始写入（第 1 行是表头）
  - 14 列：银行单据号、银行流水号、业务日期、账号、币种(名称)、户名、
         支出金额、收入金额、账户余额、摘要、对方账号、对方户名、
         对方开户行名、银行记账时间
- Sheet 2: 格式说明（保留原内容）
- Sheet 3: 币种编码对照（保留原内容）

模板加载策略（兼容 clawhub 等不支持上传二进制模板的市场）：
1. 优先使用调用方显式传入的 template_path
2. 其次查找 skills/<skill>/assets/template/nstc_banktransaction.xls
3. 仍不存在则从配置的互联网地址自动下载到本地
"""

import os
import logging
from typing import Optional, List, Dict, Any

from mappers.base_mapper import BaseMapper
from core.data_structures import (
    BankStatementData, MappedRecord, MappingResult, ValidationResult,
    TransactionRecord,
)
from core.currency_map import get_currency_name

logger = logging.getLogger(__name__)


class NstcMapper(BaseMapper):
    """九恒星司库 NSTC 系统银行流水映射器"""

    # NSTC 必填字段（带 * 标记）
    REQUIRED_FIELDS = [
        'bank_seq_no',    # *银行流水号
        'bizdate',        # *业务日期
        'account',        # *账号
        'currency',       # *币种(名称)
    ]

    COLUMNS = [
        'docno',          # 0: 银行单据号
        'bank_seq_no',    # 1: 银行流水号
        'bizdate',        # 2: 业务日期
        'account',        # 3: 账号
        'currency',       # 4: 币种(名称)
        'accountname',    # 5: 户名
        'debitamount',    # 6: 支出金额
        'creditamount',   # 7: 收入金额
        'balance',        # 8: 账户余额
        'remark',         # 9: 摘要
        'oppaccount',     # 10: 对方账号
        'oppname',        # 11: 对方户名
        'oppbank',        # 12: 对方开户行名
        'banktime',       # 13: 银行记账时间
    ]

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or self._default_template_path()

    def _default_template_path(self) -> str:
        """默认模板路径：统一通过 template_manager 解析（本地查找 + 自动下载）"""
        from core.template_manager import resolve_template
        resolved = resolve_template('NSTC')
        if resolved:
            return resolved
        # 兜底：直接拼接路径（仅在模板解析失败时使用，文件可能不存在）
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base, 'assets', 'template', 'nstc_banktransaction.xls')

    @property
    def target_system(self) -> str:
        return "NSTC"

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
        user_bank = source_data.user_provided_bank_name
        account_number = txn.account_number or user_acct
        currency_code = (txn.currency_code or 'CNY').upper()
        currency_name = get_currency_name(currency_code)

        # 户名（账户开户人）— 从源文件的 header 中提取
        account_name = source_data.header.raw_tags.get('account_name', '') or user_bank

        # 银行记账时间：YYYY/M/D H:MM:SS
        banktime = self._format_banktime(txn.value_date, txn.transaction_time)

        record = {
            'docno': '',
            'bank_seq_no': txn.reference_number or f"NSTC_{idx+1:08d}",
            'bizdate': self._format_date(txn.value_date),
            'account': account_number,
            'currency': currency_name,
            'accountname': account_name,
            'debitamount': str(txn.debit_amount) if txn.debit_amount > 0 else '',
            'creditamount': str(txn.credit_amount) if txn.credit_amount > 0 else '',
            'balance': str(txn.running_balance) if txn.running_balance else '',
            'remark': txn.transaction_description or '',
            'oppaccount': txn.counterparty_account or '',
            'oppname': txn.counterparty_name or '',
            'oppbank': txn.counterparty_bank or '',
            'banktime': banktime,
        }
        return record

    def _format_date(self, value_date: str) -> str:
        if not value_date or len(value_date) != 8:
            return value_date
        return f"{value_date[:4]}-{value_date[4:6]}-{value_date[6:8]}"

    def _format_banktime(self, value_date: str, txn_time: str) -> str:
        """NSTC 要求格式：yyyy/M/d H:mm:ss"""
        if not value_date or len(value_date) != 8:
            return ''
        year = value_date[:4]
        month = str(int(value_date[4:6]))
        day = str(int(value_date[6:8]))
        if txn_time and len(txn_time) == 6:
            time_str = f"{txn_time[:2]}:{txn_time[2:4]}:{txn_time[4:6]}"
        else:
            time_str = '00:00:00'
        return f"{year}/{month}/{day} {time_str}"

    def validate(self, mapping_result: MappingResult) -> ValidationResult:
        result = ValidationResult(is_valid=True)
        for idx, mr in enumerate(mapping_result.mapped_records):
            record = mr.record
            for field in self.REQUIRED_FIELDS:
                if not record.get(field):
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
        写入 NSTC 模板（xls）
        - 复制 .xls 模板（保留字体/列宽/格式）
        - 覆盖数据单元格
        - 保留 格式说明、币种编码对照 等辅助 sheet
        - 注意：批量导入银行明细格式 必须为第一个 sheet
        """
        template = template_path or self.template_path
        if not os.path.exists(template):
            raise FileNotFoundError(f"NSTC 模板不存在: {template}")

        records = [mr.record for mr in mapping_result.mapped_records]

        from mappers._xls_template_helpers import write_xls_with_template
        write_xls_with_template(
            template_path=template,
            output_path=output_path,
            main_sheet_name='批量导入银行明细格式',
            main_data_start_row_0based=1,  # 第 2 行（0-based 索引 1）
            column_field_map=self.COLUMNS,
            records=records,
            extra_sheet_names=['格式说明', '币种编码对照'],
        )
        logger.info(f"NSTC 输出已保存: {output_path}（共 {len(records)} 条）")
        return output_path


def create_nstc_mapper(template_path: Optional[str] = None) -> NstcMapper:
    return NstcMapper(template_path)

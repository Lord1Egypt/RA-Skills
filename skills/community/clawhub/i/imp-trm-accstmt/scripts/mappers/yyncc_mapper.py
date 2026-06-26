"""
YYNCC (用友NCC) 映射器
将银行对账单数据映射到 用友NCC 系统银行流水导入模板。

模板: assets/template/yyncc_banktransaction.xls
- Sheet 1: 数据
  - 第 1 行：参数行（银行类别、开始日期、结束日期等）
  - 第 2 行：空
  - 第 3 行：空
  - 第 4 行：表头
  - 第 5 行开始：数据
- Sheet 2: 使用说明
- Sheet 3: Sheet3（空）

注意：银行类别是必输项（与本方账号一同确定银行账号在NC系统中的信息）；
      币种字段可空（为空则取NC系统中对应银行账号的币种）。

模板加载策略（兼容 clawhub 等不支持上传二进制模板的市场）：
1. 优先使用调用方显式传入的 template_path
2. 其次查找 skills/<skill>/assets/template/yyncc_banktransaction.xls
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


class YynccMapper(BaseMapper):
    """用友NCC YYNCC 系统银行流水映射器"""

    # YYNCC 必填字段（隐含：银行类别在参数行）
    REQUIRED_FIELDS = [
        'bizdate',     # 交易日期
        'oppaccount',  # 对方账号
        'oppname',     # 对方户名
        'selfaccount', # 本方账号
    ]

    # 列索引（0-based）— 与模板 23 列（A-W）严格对应
    # 注意：第 4 行（1-based）是表头
    # A=交易日期, B=交易时间, C=对方账号, D=对方户名, E=收款金额, F=付款金额,
    # G=摘要, H=用途, I=结算号, J=结算方式, K=币种, L=本方账号, M=本方户名,
    # N=本方余额, O=对账标识码, P=交易流水号 ★, ..., W=银行类别
    COLUMNS = [
        'bizdate',         # 0: A列 交易日期
        'biztime',         # 1: B列 交易时间
        'oppaccount',      # 2: C列 对方账号
        'oppname',         # 3: D列 对方户名
        'creditamount',    # 4: E列 收款金额
        'debitamount',     # 5: F列 付款金额
        'remark',          # 6: G列 摘要
        'use',             # 7: H列 用途
        'checkno',         # 8: I列 结算号
        'checktype',       # 9: J列 结算方式
        'currency',        # 10: K列 币种
        'selfaccount',     # 11: L列 本方账号
        'selfname',        # 12: M列 本方户名
        'selfbalance',     # 13: N列 本方余额
        'checkflag',       # 14: O列 对账标识码
        'bank_seq_no',     # 15: P列 交易流水号 ★
        '',                # 16: Q列 (空)
        '',                # 17: R列 (空)
        '',                # 18: S列 (空)
        '',                # 19: T列 (空)
        '',                # 20: U列 (空)
        '',                # 21: V列 (空)
        'bank_type',       # 22: W列 银行类别（参数行，不在数据行）
    ]

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or self._default_template_path()

    def _default_template_path(self) -> str:
        """默认模板路径：统一通过 template_manager 解析（本地查找 + 自动下载）"""
        from core.template_manager import resolve_template
        resolved = resolve_template('YYNCC')
        if resolved:
            return resolved
        # 兜底：直接拼接路径（仅在模板解析失败时使用，文件可能不存在）
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base, 'assets', 'template', 'yyncc_banktransaction.xls')

    @property
    def target_system(self) -> str:
        return "YYNCC"

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

        # 本方户名（账户开户人）— 从源文件的 header 中提取
        account_name = source_data.header.raw_tags.get('account_name', '') or user_bank

        record = {
            'bizdate': self._format_date(txn.value_date),
            'biztime': self._format_time(txn.transaction_time),
            'oppaccount': txn.counterparty_account or '',
            'oppname': txn.counterparty_name or '',
            'creditamount': str(txn.credit_amount) if txn.credit_amount > 0 else '',
            'debitamount': str(txn.debit_amount) if txn.debit_amount > 0 else '',
            'remark': txn.transaction_description or '',
            'use': txn.supplementary_details or '',
            'checkno': '',
            'checktype': '',
            'currency': currency_code,
            'selfaccount': account_number,
            'selfname': account_name,  # M列 本方户名
            'selfbalance': str(txn.running_balance) if txn.running_balance else '',
            'checkflag': '',
            'bank_seq_no': txn.reference_number or '',  # P列 交易流水号 ★
            'bank_type': '',  # W列 银行类别（参数行，不在数据行写入）
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
        写入 YYNCC 模板（xls）
        - 复制 .xls 模板（保留字体/列宽/格式）
        - 覆盖数据单元格
        - 保留 使用说明、Sheet3 等辅助 sheet
        """
        template = template_path or self.template_path
        if not os.path.exists(template):
            raise FileNotFoundError(f"YYNCC 模板不存在: {template}")

        records = [mr.record for mr in mapping_result.mapped_records]

        from mappers._xls_template_helpers import write_xls_with_template
        write_xls_with_template(
            template_path=template,
            output_path=output_path,
            main_sheet_name='数据',
            main_data_start_row_0based=4,  # 第 5 行（0-based 索引 4）
            column_field_map=self.COLUMNS,
            records=records,
            extra_sheet_names=['使用说明', 'Sheet3'],
        )
        logger.info(f"YYNCC 输出已保存: {output_path}（共 {len(records)} 条）")
        return output_path


def create_yyncc_mapper(template_path: Optional[str] = None) -> YynccMapper:
    return YynccMapper(template_path)

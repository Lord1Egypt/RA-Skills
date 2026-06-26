"""
核心数据结构定义
定义银行对账单解析和转换过程中使用的数据结构
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from decimal import Decimal


@dataclass
class TransactionRecord:
    """单条交易记录"""
    # 基本标识
    transaction_id: str = ""           # 自动生成的交易ID
    reference_number: str = ""        # 银行参考号
    unique_identifier: str = ""       # 唯一标识

    # 账户信息
    account_number: str = ""          # 银行账号
    currency_code: str = ""          # 币种

    # 日期时间
    value_date: str = ""             # 起息日/交易日期 (YYMMDD)
    transaction_time: str = ""         # 交易时间 (HHMMSS)
    entry_date: str = ""              # 入账日期 (MMDD)
    booking_date: str = ""            # 记账日期

    # 金额信息
    dc_indicator: str = ""           # 借贷标识 C=贷(收入) D=借(支出)
    amount: Decimal = Decimal("0")    # 交易金额
    debit_amount: Decimal = Decimal("0")    # 借方金额
    credit_amount: Decimal = Decimal("0")   # 贷方金额

    # 交易类型
    entry_reason_code: str = ""      # 交易类型代码 (如 TRF, CHQ, INT)
    entry_reason_description: str = "" # 交易类型描述

    # 对方信息
    counterparty_account: str = ""    # 对方账号
    counterparty_name: str = ""       # 对方户名
    counterparty_bank: str = ""       # 对方银行

    # 附加信息
    transaction_description: str = ""  # 交易描述
    reference_for_account_owner: str = "" # 账户持有人参考
    supplementary_details: str = ""   # 补充详情

    # 余额
    running_balance: Decimal = Decimal("0")  # 变动后余额

    # 账号块标识（用于余额计算）
    statement_block_id: str = ""       # 账号块标识（如账号+日期）
    is_first_in_block: bool = False   # 是否是该账号块的第一条记录
    is_last_in_block: bool = False    # 是否是该账号块的最后一条记录

    # 原始数据
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """根据借贷标识计算借方/贷方金额"""
        if self.dc_indicator in ['C', 'RC']:
            self.credit_amount = self.amount
            self.debit_amount = Decimal("0")
        elif self.dc_indicator in ['D', 'RD']:
            self.debit_amount = self.amount
            self.credit_amount = Decimal("0")


@dataclass
class BalanceInfo:
    """余额信息"""
    balance_type: str = ""            # 余额类型 (Opening/Closing)
    dc_indicator: str = ""           # 借贷标识 C=贷 D=借
    booking_date: str = ""           # 记账日期 (YYMMDD)
    currency_code: str = ""          # 币种
    balance_amount: Decimal = Decimal("0")  # 余额

    def __str__(self):
        return f"{self.balance_type}: {self.dc_indicator}{self.booking_date}{self.currency_code}{self.balance_amount}"


@dataclass
class StatementBlock:
    """MT940账号块"""
    account_number: str = ""         # 账号
    opening_balance: Optional[BalanceInfo] = None  # 期初余额
    closing_balance: Optional[BalanceInfo] = None  # 期末余额
    transactions: List[TransactionRecord] = field(default_factory=list)  # 该块中的交易记录

    @property
    def block_id(self) -> str:
        """账号块唯一标识"""
        return f"{self.account_number}_{self.opening_balance.booking_date if self.opening_balance else 'unknown'}"


@dataclass
class BankStatementHeader:
    """银行对账单头部信息"""
    transaction_reference: str = ""   # Tag 20: 交易参考号
    account_number: str = ""          # Tag 25: 账号
    statement_number: str = ""        # Tag 28C: 语句编号
    page_number: str = ""            # Tag 28C: 页码

    # SWIFT Header (可选)
    swift_header_present: bool = False
    sender_address: str = ""
    output_time: str = ""

    # 原始数据
    raw_tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class BankStatementData:
    """完整的银行对账单数据"""
    header: BankStatementHeader = field(default_factory=BankStatementHeader)
    opening_balance: Optional[BalanceInfo] = None
    closing_balance: Optional[BalanceInfo] = None
    closing_available_balance: Optional[BalanceInfo] = None
    forward_available_balances: List[BalanceInfo] = field(default_factory=list)
    transactions: List[TransactionRecord] = field(default_factory=list)
    statement_blocks: List[StatementBlock] = field(default_factory=list)  # 账号块列表

    # 元数据
    source_file: str = ""
    source_format: str = ""
    parse_timestamp: datetime = field(default_factory=datetime.now)
    parse_errors: List[str] = field(default_factory=list)
    parse_warnings: List[str] = field(default_factory=list)

    # 用户提供的补充信息
    user_provided_account_code: str = ""    # 账户使用组织编码
    user_provided_bank_name: str = ""        # 银行名称
    default_currency: str = "CNY"           # 默认币种代码（从余额行获取）

    def add_transaction(self, transaction: TransactionRecord):
        """添加交易记录"""
        self.transactions.append(transaction)

    def add_error(self, error: str):
        """添加解析错误"""
        self.parse_errors.append(error)

    def add_warning(self, warning: str):
        """添加解析警告"""
        self.parse_warnings.append(warning)

    @property
    def transaction_count(self) -> int:
        """交易记录数量"""
        return len(self.transactions)

    def get_statement_date_range(self) -> tuple:
        """获取对账单日期范围"""
        if not self.transactions:
            return None, None

        dates = [t.value_date for t in self.transactions if t.value_date]
        return min(dates) if dates else None, max(dates) if dates else None


@dataclass
class MappedRecord:
    """映射后的目标系统记录"""
    record: Dict[str, Any]
    source_transaction: Optional[TransactionRecord] = None
    mapping_errors: List[str] = field(default_factory=list)
    mapping_warnings: List[str] = field(default_factory=list)


@dataclass
class MappingResult:
    """映射结果"""
    source_data: BankStatementData
    mapped_records: List[MappedRecord] = field(default_factory=list)
    successful_count: int = 0
    failed_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def total_count(self) -> int:
        return len(self.mapped_records)


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


@dataclass
class OutputConfig:
    """输出配置"""
    output_file: str
    target_system: str = "BIPV5"
    template_file: Optional[str] = None
    sheet_name: str = "银行流水处理"
    data_start_row: int = 10
    include_header_rows: bool = True
    include_error_column: bool = True

    # 用户提供的默认值
    default_values: Dict[str, Any] = field(default_factory=dict)

    # 输出选项
    overwrite_existing: bool = False
    create_backup: bool = True


# BIPV5 目标字段定义
BIPV5_FIELDS = {
    "id": {"cn_name": "主键", "required": False},
    "accentity_code": {"cn_name": "账户使用组织编码", "required": False},
    "bankaccount_account": {"cn_name": "*银行账号", "required": True},
    "bankNumber_name": {"cn_name": "银行名称", "required": False},
    "bank_seq_no": {"cn_name": "*本方交易流水号", "required": True},
    "tran_date": {"cn_name": "*交易日期", "required": True},
    "tran_time": {"cn_name": "交易时间", "required": False},
    "dc_flag": {"cn_name": "借贷标识", "required": False},
    "debitamount": {"cn_name": "支出金额", "required": False},
    "creditamount": {"cn_name": "收入金额", "required": False},
    "currency_name": {"cn_name": "*币种", "required": True},
    "tran_amt": {"cn_name": "金额", "required": False},
    "to_acct_no": {"cn_name": "对方账号", "required": False},
    "to_acct_name": {"cn_name": "对方户名", "required": False},
    "to_acct_bank_name": {"cn_name": "对方银行名称", "required": False},
    "use_name": {"cn_name": "用途", "required": False},
    "remark": {"cn_name": "摘要", "required": False},
    "remark01": {"cn_name": "附言", "required": False},
    "acct_bal": {"cn_name": "余额", "required": False},
    "thirdserialno": {"cn_name": "第三方交易流水号", "required": False},
    "unique_no": {"cn_name": "唯一标识号", "required": False},
    "expenseItem_name": {"cn_name": "费用项目", "required": False},
    "detailReceiptRelationCode": {"cn_name": "明细收据关联单据号", "required": False},
    "originbankseqno": {"cn_name": "原银行交易流水号", "required": False},
    "confirmstatus": {"cn_name": "账户使用组织确认状态", "required": False},
}


def get_required_fields() -> List[str]:
    """获取BIPV5必填字段列表"""
    return [field for field, info in BIPV5_FIELDS.items() if info["required"]]


def get_all_fields() -> List[str]:
    """获取BIPV5所有字段列表"""
    return list(BIPV5_FIELDS.keys())

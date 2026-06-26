"""
BIPV5 映射器
将银行对账单数据映射到 BIPV5 系统格式

模板加载策略（兼容 clawhub 等不支持上传二进制模板的市场）：
1. 优先使用调用方显式传入的 template_path
2. 其次查找 skills/<skill>/assets/template/YYBIPV5_banktransaction.xlsx
3. 仍不存在则从配置的互联网地址自动下载到本地
"""

import json
import os
import hashlib
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from decimal import Decimal

from mappers.base_mapper import BaseMapper
from core.data_structures import (
    BankStatementData, MappedRecord, MappingResult, ValidationResult,
    TransactionRecord, BIPV5_FIELDS, get_required_fields
)
from core.cosine_similarity import match_headers_with_similarity, COMMON_BANK_FIELD_ALIASES
from core.currency_map import get_currency_name


class BIPV5Mapper(BaseMapper):
    """BIPV5 系统银行流水映射器"""

    # BIPV5 必填字段
    REQUIRED_FIELDS = ['bankaccount_account', 'bank_seq_no', 'tran_date', 'currency_name']

    # 日期格式映射
    DATE_FORMAT_MAP = {
        'YYMMDD': '%y%m%d',
        'YYYYMMDD': '%Y%m%d',
        'YYYY-MM-DD': '%Y-%m-%d',
        'YYYY/MM/DD': '%Y/%m/%d',
        'DD/MM/YYYY': '%d/%m/%Y',
        'MM/DD/YYYY': '%m/%d/%Y',
    }

    def __init__(self, mapping_config_path: Optional[str] = None):
        """
        初始化 BIPV5 映射器

        Args:
            mapping_config_path: 映射配置文件路径
        """
        self.mapping_config = self._load_mapping_config(mapping_config_path)
        self._setup_transforms()

    def _load_mapping_config(self, config_path: Optional[str]) -> Dict:
        """加载映射配置"""
        if config_path is None:
            # 使用默认配置路径
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'mappings', 'mt940_to_bipv5.json')

        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 返回默认配置
        return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """获取默认映射配置"""
        return {
            "source_format": "MT940",
            "target_system": "BIPV5",
            "target_sheet_name": "银行流水处理",
            "field_mappings": self._get_default_field_mappings(),
            "required_fields": self.REQUIRED_FIELDS,
            "header_matching": {
                "use_cosine_similarity": True,
                "threshold": 0.75,
                "field_aliases": COMMON_BANK_FIELD_ALIASES
            }
        }

    def _get_default_field_mappings(self) -> List[Dict]:
        """获取默认字段映射"""
        return [
            {"target_field": "id", "source_field": None, "transform": "static_empty"},  # 手工码留空
            {"target_field": "accentity_code", "source_field": None, "transform": "user_provided_account_code"},
            {"target_field": "bankaccount_account", "source_field": "account_number", "transform": "direct"},
            {"target_field": "bankNumber_name", "source_field": None, "transform": "user_provided_bank_name"},
            {"target_field": "bank_seq_no", "source_field": "reference_number", "transform": "bank_seq_no_auto"},
            {"target_field": "tran_date", "source_field": "value_date", "transform": "date_format", "params": {"input": "YYMMDD", "output": "YYYY-MM-DD"}},
            {"target_field": "tran_time", "source_field": "transaction_time", "transform": "time_format"},
            {"target_field": "dc_flag", "source_field": "dc_indicator", "transform": "map_dc_flag", "params": {"C": "收入", "D": "支出", "RC": "收入", "RD": "支出"}},
            {"target_field": "debitamount", "source_field": "amount", "transform": "conditional_debit"},
            {"target_field": "creditamount", "source_field": "amount", "transform": "conditional_credit"},
            {"target_field": "currency_name", "source_field": "currency_code", "transform": "map_currency"},
            {"target_field": "tran_amt", "source_field": None, "transform": "static_empty"},  # 金额留空
            {"target_field": "to_acct_no", "source_field": "counterparty_account", "transform": "direct"},
            {"target_field": "to_acct_name", "source_field": "counterparty_name", "transform": "direct"},
            {"target_field": "to_acct_bank_name", "source_field": "counterparty_bank", "transform": "direct"},
            {"target_field": "use_name", "source_field": None, "transform": "static_empty"},
            {"target_field": "remark", "source_field": "transaction_description", "transform": "direct"},
            {"target_field": "remark01", "source_field": "reference_for_account_owner", "transform": "direct"},
            {"target_field": "acct_bal", "source_field": "running_balance", "transform": "direct"},
            {"target_field": "thirdserialno", "source_field": None, "transform": "static_empty"},
            {"target_field": "unique_no", "source_field": None, "transform": "hash"},
            {"target_field": "expenseItem_name", "source_field": None, "transform": "static_empty"},
            {"target_field": "detailReceiptRelationCode", "source_field": None, "transform": "static_empty"},
            {"target_field": "originbankseqno", "source_field": None, "transform": "static_empty"},
            {"target_field": "confirmstatus", "source_field": None, "transform": "static_empty"},
        ]

    def _setup_transforms(self):
        """设置转换函数映射"""
        self.transforms: Dict[str, Callable] = {
            'direct': self._transform_direct,
            'date_format': self._transform_date_format,
            'map': self._transform_map,
            'map_dc_flag': self._transform_map_dc_flag,
            'static': self._transform_static,
            'static_empty': self._transform_static_empty,
            'auto_id': self._transform_auto_id,
            'hash': self._transform_hash,
            'conditional_debit': self._transform_conditional_debit,
            'conditional_credit': self._transform_conditional_credit,
            'user_provided': self._transform_user_provided,
            'user_provided_account_code': self._transform_user_provided_account_code,
            'user_provided_bank_name': self._transform_user_provided_bank_name,
            'lookup_bank': self._transform_lookup_bank,
            'bank_seq_no_auto': self._transform_bank_seq_no_auto,
            'map_currency': self._transform_map_currency,
            'time_format': self._transform_time_format,
        }

    @property
    def target_system(self) -> str:
        return "BIPV5"

    @property
    def required_fields(self) -> List[str]:
        return self.REQUIRED_FIELDS

    def map(self, source_data: BankStatementData, **kwargs) -> MappingResult:
        """
        将 MT940 数据映射到 BIPV5 格式

        Args:
            source_data: MT940 解析后的数据
            **kwargs:
                - account_code: 账户使用组织编码
                - bank_name: 银行名称
                - closing_balance: 期末余额

        Returns:
            MappingResult: 映射结果
        """
        result = MappingResult(source_data=source_data)

        # 提取用户提供的参数
        account_code = kwargs.get('account_code', '')
        bank_name = kwargs.get('bank_name', '')
        closing_balance = kwargs.get('closing_balance', None)

        # 设置用户提供的默认值
        if account_code:
            source_data.user_provided_account_code = account_code
        if bank_name:
            source_data.user_provided_bank_name = bank_name

        # 遍历每条交易记录
        for idx, txn in enumerate(source_data.transactions):
            try:
                mapped_record = self._map_transaction(
                    txn, idx, closing_balance, source_data
                )
                result.mapped_records.append(mapped_record)
                result.successful_count += 1

            except Exception as e:
                mapped_record = MappedRecord(
                    record={},
                    source_transaction=txn,
                    mapping_errors=[str(e)]
                )
                result.mapped_records.append(mapped_record)
                result.failed_count += 1
                result.errors.append(f"交易记录 {idx + 1}: {str(e)}")

        # 复制解析警告
        result.warnings.extend(source_data.parse_warnings)

        return result

    def _map_transaction(
        self,
        txn: TransactionRecord,
        idx: int,
        closing_balance: Optional[Decimal],
        source_data: Optional['BankStatementData'] = None
    ) -> MappedRecord:
        """映射单条交易记录"""
        record = {}
        errors = []
        warnings = []

        # 传递 source_data 给 txn（让 user_provided transform 可以访问）
        if source_data is not None:
            try:
                txn._source_data = source_data
            except Exception:
                pass

        # 应用每个字段映射
        for mapping in self.mapping_config.get('field_mappings', []):
            target_field = mapping['target_field']
            transform_type = mapping.get('transform', 'direct')
            transform_func = self.transforms.get(transform_type)

            if transform_func:
                try:
                    value = transform_func(txn, mapping, idx)
                    record[target_field] = value
                except Exception as e:
                    record[target_field] = None
                    errors.append(f"{target_field}: {str(e)}")
            else:
                record[target_field] = None
                warnings.append(f"未知的转换类型: {transform_type}")

        return MappedRecord(
            record=record,
            source_transaction=txn,
            mapping_errors=errors,
            mapping_warnings=warnings
        )

    # ========== 转换函数 ==========

    def _transform_direct(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """直接复制"""
        source_field = mapping.get('source_field')
        if source_field:
            return getattr(txn, source_field, None)
        return None

    def _transform_date_format(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """日期格式转换 - 支持自动检测输入格式

        重要：日期格式判断逻辑
        - 6位数字 (如 180523) -> YYMMDD -> 转为 2018-05-23
        - 8位数字 (如 20180523) -> YYYYMMDD -> 转为 2018-05-23
        """
        source_field = mapping.get('source_field', 'value_date')
        params = mapping.get('params', {})

        date_value = getattr(txn, source_field, None)
        if not date_value:
            return ''

        # 转换为字符串处理
        date_str = str(date_value).strip()

        # 如果已经是 YYYY-MM-DD 格式，直接返回
        if '-' in date_str and len(date_str) == 10:
            return date_str

        output_format = params.get('output', 'YYYY-MM-DD')
        output_pattern = self.DATE_FORMAT_MAP.get(output_format, '%Y-%m-%d')

        # 根据长度选择格式顺序（重要：6位用YYMMDD，8位用YYYYMMDD）
        if len(date_str) == 6 and date_str.isdigit():
            # 6位数字 -> YYMMDD格式优先
            input_formats = [
                ('%y%m%d', 'YYMMDD'),         # 180523 -> 2018-05-23
                ('%Y%m%d', 'YYYYMMDD'),      # 备用
            ]
        elif len(date_str) == 8 and date_str.isdigit():
            # 8位数字 -> YYYYMMDD格式优先
            input_formats = [
                ('%Y%m%d', 'YYYYMMDD'),      # 20180523 -> 2018-05-23
                ('%y%m%d', 'YYMMDD'),         # 备用
            ]
        else:
            # 其他格式混用
            input_formats = [
                ('%Y%m%d', 'YYYYMMDD'),      # 20180523
                ('%y%m%d', 'YYMMDD'),         # 180523
                ('%Y/%m/%d', 'YYYY/MM/DD'),   # 2018/05/23
                ('%Y-%m-%d', 'YYYY-MM-DD'),   # 2018-05-23
                ('%d/%m/%Y', 'DD/MM/YYYY'),   # 23/05/2018
                ('%m/%d/%Y', 'MM/DD/YYYY'),   # 05/23/2018
            ]

        for input_pattern, format_name in input_formats:
            try:
                parsed_date = datetime.strptime(date_str, input_pattern)
                return parsed_date.strftime(output_pattern)
            except ValueError:
                continue

        # 所有格式都失败，返回原始值（可能需要手动处理）
        return date_str

    def _transform_map(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """值映射"""
        source_field = mapping.get('source_field')
        params = mapping.get('params', {})
        mapping_dict = params.get('mapping', {})

        value = getattr(txn, source_field, None) if source_field else None
        return mapping_dict.get(value, value)

    def _transform_map_currency(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """币种编码转换为中文名称"""
        source_field = mapping.get('source_field', 'currency_code')
        currency_code = getattr(txn, source_field, None)

        if not currency_code:
            return ''

        # 使用公共的币种映射函数
        return get_currency_name(currency_code)

    def _transform_static(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """静态值"""
        params = mapping.get('params', {})
        return params.get('value', '')

    def _transform_static_empty(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """静态空值"""
        return ''

    def _transform_map_dc_flag(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """借贷标识映射：C/D -> 收入/支出"""
        params = mapping.get('params', {})
        dc_indicator = getattr(txn, 'dc_indicator', None)
        if dc_indicator:
            return params.get(dc_indicator, '')
        return ''

    def _transform_auto_id(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """自动生成ID"""
        return f"AUTO_{idx + 1:08d}"

    def _transform_bank_seq_no_auto(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """生成银行交易流水号 - 优先使用原始文件中的流水号，否则自动生成

        1. 如果原始文件中有流水号（reference_number），直接使用
        2. 否则自动生成：使用交易日期+金额+序号组合，确保唯一性且不包含文件名
        """
        # 优先使用原始文件中的流水号
        ref = getattr(txn, 'reference_number', None) or ''
        if ref and ref.strip() and ref.strip().upper() not in ['NONREF', 'NONE', 'NULL', '']:
            return ref.strip()

        # 自动生成: 使用交易日期+金额+序号组合
        # 格式: YYYYMMDD + 金额(去掉小数点，整数部分) + 6位序号
        # 例如: 2025062139847000000001 (日期20250621, 金额39.47, 第1笔)
        date_part = str(txn.value_date or '').replace('-', '').replace('/', '')
        if len(date_part) < 8:
            # 如果没有日期，使用当前日期
            from datetime import datetime
            date_part = datetime.now().strftime('%Y%m%d')

        # 金额部分（取整数部分，最多8位）
        amount_str = str(abs(txn.amount or 0)).split('.')[0]
        amount_part = amount_str.zfill(8)[:8]

        # 序号（6位）
        seq_part = str(idx + 1).zfill(6)

        return f"{date_part}{amount_part}{seq_part}"

    def _transform_hash(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """生成唯一码 - 包含时间戳、账号、金额、日期等信息，长度不超过96位"""
        from datetime import datetime
        # 时间戳（精确到毫秒）
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 账号（取后8位）
        account = str(txn.account_number or '')[:8]
        # 金额（取绝对值，整数部分）
        amount = str(abs(txn.amount or 0)).replace('.', '')[:10]
        # 日期
        date = str(txn.value_date or '')[:8]
        # 序号
        seq = str(idx + 1).zfill(6)

        # 组合成唯一码，确保长度不超过96位
        unique_id = f"{timestamp}_{account}_{date}_{amount}_{seq}"

        # 如果仍然过长，截断
        if len(unique_id) > 96:
            # 使用MD5哈希来缩短
            hash_val = hashlib.md5(unique_id.encode()).hexdigest()
            unique_id = f"{timestamp[:20]}_{hash_val}"

        return unique_id

    def _transform_conditional_debit(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """条件赋值 - 借方金额（正值）"""
        if txn.dc_indicator in ['D', 'RD']:
            return str(abs(txn.amount)) if txn.amount else ''
        return ''

    def _transform_conditional_credit(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """条件赋值 - 贷方金额（正值）"""
        if txn.dc_indicator in ['C', 'RC']:
            return str(abs(txn.amount)) if txn.amount else ''
        return ''

    def _transform_user_provided(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """用户提供的值"""
        target_field = mapping['target_field']
        # 委托给 _transform_user_provided_account_code / _transform_user_provided_bank_name
        if target_field == 'accentity_code':
            return self._transform_user_provided_account_code(txn, mapping, idx)
        if target_field == 'bankNumber_name':
            return self._transform_user_provided_bank_name(txn, mapping, idx)
        return ''

    def _transform_user_provided_account_code(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """从 source_data.user_provided_account_code 取值"""
        # 优先从 txn 所属的 source_data 取
        src = getattr(txn, '_source_data', None)
        if src and getattr(src, 'user_provided_account_code', ''):
            return src.user_provided_account_code
        return ''

    def _transform_user_provided_bank_name(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """从 source_data.user_provided_bank_name 取值"""
        src = getattr(txn, '_source_data', None)
        if src and getattr(src, 'user_provided_bank_name', ''):
            return src.user_provided_bank_name
        return ''

    def _transform_time_format(self, txn: TransactionRecord, mapping: Dict, idx: int) -> str:
        """时间格式转换 - HHMMSS -> HH24:MI:SS
        重要：空值默认为 00:00:00
        """
        source_field = mapping.get('source_field', 'transaction_time')
        time_value = getattr(txn, source_field, None)

        # 空值默认为 00:00:00
        if not time_value or str(time_value).strip() == '':
            return '00:00:00'

        time_str = str(time_value).strip()

        # 如果已经是 HH:MM:SS 或 H:MM:SS 格式，补零并返回
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                # 补零确保 HH:MM:SS 格式
                try:
                    hour = int(parts[0])
                    minute = int(parts[1])
                    second = int(parts[2])
                    return f"{hour:02d}:{minute:02d}:{second:02d}"
                except ValueError:
                    return '00:00:00'
            elif len(parts) == 2:
                # HH:MM -> HH:MM:SS
                try:
                    hour = int(parts[0])
                    minute = int(parts[1])
                    return f"{hour:02d}:{minute:02d}:00"
                except ValueError:
                    return '00:00:00'

        # 尝试将 HHMMSS 转换为 HH:MM:SS
        if len(time_str) == 6 and time_str.isdigit():
            return f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"
        elif len(time_str) == 4 and time_str.isdigit():
            # HHMM 格式
            return f"{time_str[0:2]}:{time_str[2:4]}:00"
        elif len(time_str) == 3 and time_str.isdigit():
            # HMM 格式，如 830 表示 08:30:00
            return f"0{time_str[0]}:{time_str[1:3]}:00"

        # 无法解析，返回默认值
        return '00:00:00'

    def _transform_lookup_bank(self, txn: TransactionRecord, mapping: Dict, idx: int) -> Any:
        """查表获取银行名称"""
        # TODO: 实现银行名称查表
        return txn.account_number or ''

    def validate(self, mapping_result: MappingResult) -> ValidationResult:
        """
        验证映射结果

        Args:
            mapping_result: 映射结果

        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult(is_valid=True)

        # 检查必填字段
        for idx, mapped_record in enumerate(mapping_result.mapped_records):
            record = mapped_record.record

            for field in self.required_fields:
                value = record.get(field)
                if not value or str(value).strip() == '':
                    result.warnings.append(
                        f"行 {idx + 10}: 必填字段 '{field}' 为空"
                    )

            # 检查日期格式
            tran_date = record.get('tran_date', '')
            if tran_date:
                try:
                    datetime.strptime(tran_date, '%Y-%m-%d')
                except ValueError:
                    result.warnings.append(
                        f"行 {idx + 10}: 日期格式不正确 '{tran_date}'"
                    )

            # 检查金额格式
            for amount_field in ['debitamount', 'creditamount', 'tran_amt', 'acct_bal']:
                value = record.get(amount_field)
                if value and str(value).strip():
                    try:
                        float(value)
                    except ValueError:
                        result.warnings.append(
                            f"行 {idx + 10}: 金额格式不正确 '{value}'"
                        )

        # 如果有警告，设置 is_valid 为 False
        if result.warnings:
            result.is_valid = False

        return result


def create_bipv5_mapper(config_path: Optional[str] = None) -> BIPV5Mapper:
    """工厂函数：创建 BIPV5 映射器"""
    return BIPV5Mapper(config_path)


def resolve_bipv5_template_path() -> Optional[str]:
    """解析 BIPV5 模板路径（供 main.py 的 batch_convert_merge 等使用）

    模板加载策略：
    1. 优先使用调用方显式传入的 template_path
    2. 其次查找 skills/<skill>/assets/template/YYBIPV5_banktransaction.xlsx
    3. 仍不存在则从配置的互联网地址自动下载到本地
    """
    from core.template_manager import resolve_template
    return resolve_template('BIPV5')

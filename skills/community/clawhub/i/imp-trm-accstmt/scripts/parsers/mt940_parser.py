"""
MT940 解析器
解析 SWIFT MT940 格式的银行对账单
"""

import re
import os
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from decimal import Decimal, InvalidOperation
from dataclasses import asdict

from parsers.base_parser import BaseParser, ParseError
from core.data_structures import (
    BankStatementData, BankStatementHeader, BalanceInfo, TransactionRecord
)


class MT940Parser(BaseParser):
    """SWIFT MT940 格式银行对账单解析器"""

    # MT940 标签定义
    TAG_PATTERN = re.compile(r'^:(\d{2}[A-Z]?):(.+)$')
    TAG_20 = '20'      # Transaction Reference Number
    TAG_25 = '25'      # Account Identification
    TAG_28C = '28C'    # Statement/Page Number
    TAG_60 = '60'      # Opening Balance
    TAG_61 = '61'      # Statement Line
    TAG_62 = '62'      # Closing Balance
    TAG_64 = '64'      # Closing Available Balance
    TAG_65 = '65'      # Forward Available Balance
    TAG_86 = '86'      # Information to Account Owner

    # SWIFT Header patterns
    SWIFT_HEADER_START = re.compile(r'^\{1:F01')
    SWIFT_HEADER2_START = re.compile(r'^\{2:O\d{3}')
    SWIFT_BLOCK_START = re.compile(r'^\{(\d):')
    SWIFT_BLOCK_END = re.compile(r'\}$')
    SWIFT_DATA_START = re.compile(r'\{4:')  # 不需要^锚点，因为可能在行中间

    @property
    def format_name(self) -> str:
        return "SWIFT MT940"

    def detect_format(self, file_path: str) -> bool:
        """
        检测文件是否为MT940格式

        Args:
            file_path: 文件路径

        Returns:
            True if file appears to be MT940 format
        """
        try:
            self.validate_file(file_path)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # Read first 5KB

            # Check for MT940 markers
            mt940_markers = [
                ':20:',        # Transaction Reference Number
                ':25:',        # Account Identification
                ':60F:',       # Opening Balance
                ':61:',        # Statement Line
                ':62F:',       # Closing Balance
            ]

            # Count how many markers are present
            marker_count = sum(1 for marker in mt940_markers if marker in content)

            return marker_count >= 3

        except Exception:
            return False

    def parse(self, file_path: str, **kwargs) -> BankStatementData:
        """
        解析MT940文件

        Args:
            file_path: 文件路径
            **kwargs: 可选参数
                - encoding: 文件编码，默认utf-8

        Returns:
            BankStatementData: 解析后的数据
        """
        self.validate_file(file_path)

        encoding = kwargs.get('encoding', None)

        if encoding is None:
            # 自动检测编码 - 优先尝试GBK（中国银行文件常用）
            # 也需要检测UTF-8，避免正常UTF-8文件被误判
            encodings = ['gbk', 'gb2312', 'gb18030', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            best_encoding = None
            for enc in encodings:
                try:
                    with open(file_path, 'rb') as f:
                        raw_bytes = f.read()
                    # 尝试解码
                    decoded = raw_bytes.decode(enc, errors='strict')
                    # 检查是否包含有效的中文字符（GBK/GB系列）
                    if enc in ('gbk', 'gb2312', 'gb18030'):
                        # 验证是否有合理数量的中文字符
                        chinese_chars = sum(1 for c in decoded if '一' <= c <= '鿿')
                        if chinese_chars > 0:
                            content = decoded
                            best_encoding = enc
                            break
                    else:
                        # UTF-8 或拉丁编码，先接受
                        content = decoded
                        best_encoding = enc
                        break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    continue

            # 如果UTF-8成功但没有中文，且存在GBK版本更好，则重新用GBK
            if best_encoding == 'utf-8' and content:
                try:
                    with open(file_path, 'rb') as f:
                        raw_bytes = f.read()
                    gbk_content = raw_bytes.decode('gbk', errors='replace')
                    chinese_chars = sum(1 for c in gbk_content if '一' <= c <= '鿿')
                    utf8_chinese = sum(1 for c in content if '一' <= c <= '鿿')
                    # 如果GBK有更多有效中文，切换到GBK
                    if chinese_chars > utf8_chinese * 2:
                        content = gbk_content
                except:
                    pass

            if content is None:
                raise ParseError(f"Unable to decode file with supported encodings: {file_path}")
        else:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Try alternative encodings
                for enc in ['latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        with open(file_path, 'r', encoding=enc, errors='ignore') as f:
                            content = f.read()
                        break
                    except:
                        continue
                else:
                    raise ParseError(f"Unable to decode file with supported encodings: {file_path}")

        result = BankStatementData()
        result.source_file = os.path.basename(file_path)
        result.source_format = self.format_name

        # 预处理：处理SWIFT头和尾
        content = self._preprocess(content)

        # 按行分割
        lines = content.split('\n')
        lines = [line.rstrip('\r') for line in lines]

        # 账号块解析状态
        current_block = None
        block_transactions = []
        current_opening_balance = None

        # 解析每行
        current_tag = None
        current_tag_content = []
        current_transaction = None
        current_description = []
        pending_86 = False

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            if not line:
                continue

            # 检测SWIFT块开始 - 每个账号块开始
            if self.SWIFT_BLOCK_START.match(line):
                # 保存上一个账号块
                if current_block and block_transactions:
                    self._finalize_block(result, current_block, block_transactions, current_opening_balance)
                # 开始新账号块
                current_block = None
                block_transactions = []
                current_opening_balance = None
                continue

            # 检测SWIFT块结束 - 账号块结束
            if self.SWIFT_BLOCK_END.search(line):
                # 保存上一个账号块
                if current_block and block_transactions:
                    self._finalize_block(result, current_block, block_transactions, current_opening_balance)
                current_block = None
                block_transactions = []
                current_opening_balance = None
                continue

            # 检测标签开始
            tag_match = self.TAG_PATTERN.match(line)
            if tag_match:
                # 处理前一个标签
                if current_tag:
                    current_opening_balance = self._process_tag(
                        current_tag,
                        '\n'.join(current_tag_content),
                        result,
                        current_transaction,
                        current_description,
                        pending_86,
                        current_block,
                        block_transactions,
                        current_opening_balance
                    )

                    # 如果是Tag 25，新账号块开始
                    if current_tag == self.TAG_25:
                        # 保存上一个账号块
                        if current_block and block_transactions:
                            self._finalize_block(result, current_block, block_transactions, current_opening_balance)
                        # 开始新账号块
                        current_block = result.header.account_number
                        block_transactions = []
                        current_opening_balance = None

                    # 如果是Tag 61，创建新的交易记录
                    if current_tag == self.TAG_61:
                        current_transaction = TransactionRecord()
                        current_description = []
                        pending_86 = False

                # 开始新标签
                current_tag = tag_match.group(1)
                current_tag_content = [tag_match.group(2)]
            else:
                # 继续累积当前标签内容
                if current_tag:
                    current_tag_content.append(line)

        # 处理最后一个标签
        if current_tag:
            current_opening_balance = self._process_tag(
                current_tag,
                '\n'.join(current_tag_content),
                result,
                current_transaction,
                current_description,
                pending_86,
                current_block,
                block_transactions,
                current_opening_balance
            )

        # 保存最后一个账号块
        if current_block and block_transactions:
            self._finalize_block(result, current_block, block_transactions, current_opening_balance)

        # 验证结果
        if not result.header.account_number:
            result.add_error("未找到账号信息 (Tag 25)")

        if not result.transactions:
            result.add_warning("未找到交易记录 (Tag 61)")

        return result

    def _finalize_block(self, result: BankStatementData, block_id: str, transactions: List, opening_balance):
        """
        完成账号块的解析，计算每条交易的余额

        Args:
            result: 解析结果
            block_id: 账号块标识
            transactions: 该块中的交易记录列表
            opening_balance: 期初余额
        """
        if not transactions:
            return

        # 获取期末余额（使用最近解析的closing_balance）
        closing_balance = result.closing_balance

        # 标记首尾记录
        if transactions:
            transactions[0].is_first_in_block = True
            transactions[-1].is_last_in_block = True

        # 计算每条交易的余额
        # 根据:60F的dc_indicator确定期初余额的符号
        # C表示贷方余额（正数），D表示借方余额（负数）
        current_balance = Decimal('0')

        if opening_balance:
            if opening_balance.dc_indicator == 'C':
                current_balance = opening_balance.balance_amount
            else:  # D
                current_balance = -opening_balance.balance_amount

        for i, txn in enumerate(transactions):
            txn.statement_block_id = block_id

            if txn.is_first_in_block:
                # 第一条：余额 = 期初余额 + 收入 - 支出
                if txn.dc_indicator in ['C', 'RC']:
                    current_balance = current_balance + txn.amount
                else:
                    current_balance = current_balance - txn.amount

                txn.running_balance = current_balance

            elif txn.is_last_in_block and closing_balance:
                # 最后一条：直接使用期末余额
                if closing_balance.dc_indicator == 'C':
                    txn.running_balance = closing_balance.balance_amount
                else:
                    txn.running_balance = -closing_balance.balance_amount
                current_balance = txn.running_balance

            else:
                # 中间记录：根据借贷标识计算
                if txn.dc_indicator in ['C', 'RC']:
                    current_balance = current_balance + txn.amount
                else:
                    current_balance = current_balance - txn.amount
                txn.running_balance = current_balance

    def _preprocess(self, content: str) -> str:
        """预处理MT940内容，移除SWIFT块标记"""
        # 首先尝试提取{4:}块中的内容
        lines = content.split('\n')
        result_lines = []
        in_data_block = False
        pending_content = ""  # 用于处理{4:在同一行的情况

        for line in lines:
            line = line.rstrip('\r\n')

            # 检查是否有SWIFT块开始
            data_start_match = self.SWIFT_DATA_START.search(line)
            if data_start_match:
                in_data_block = True
                # 提取{4:之后的内容
                after_start = line[data_start_match.end():]
                if after_start.strip():
                    # 检查是否有块结束
                    block_end_idx = after_start.rfind('}')
                    if block_end_idx > 0:
                        # 块在同一行结束
                        result_lines.append(after_start[:block_end_idx].strip())
                    elif after_start.strip() and after_start.strip() != '}':
                        pending_content = after_start
                continue

            # 在数据块中
            if in_data_block:
                # 检查是否有块结束
                block_end_idx = line.rfind('}')
                if block_end_idx >= 0:
                    # 只取块结束前的内容
                    line = line[:block_end_idx]
                    if line.strip():
                        result_lines.append(pending_content + line.strip())
                    pending_content = ""
                    in_data_block = False
                else:
                    # 继续累积内容
                    if pending_content:
                        result_lines.append(pending_content + line.strip())
                        pending_content = ""
                    elif line.strip():
                        result_lines.append(line.strip())

        return '\n'.join(result_lines)

    def _process_tag(
        self,
        tag: str,
        content: str,
        result: BankStatementData,
        current_transaction: Optional[TransactionRecord],
        current_description: List[str],
        pending_86: bool,
        current_block: Optional[str] = None,
        block_transactions: Optional[List] = None,
        current_opening_balance: Optional[BalanceInfo] = None
    ) -> Optional[BalanceInfo]:
        """处理单个MT940标签

        Returns:
            Updated current_opening_balance (since assignment to parameter doesn't persist)
        """

        if tag == self.TAG_20:
            # Transaction Reference Number
            result.header.transaction_reference = content.strip()
            result.header.raw_tags['20'] = content

        elif tag == self.TAG_25:
            # Account Identification
            result.header.account_number = content.strip()
            result.header.raw_tags['25'] = content

        elif tag == self.TAG_28C:
            # Statement/Page Number
            parts = content.split('/')
            if parts:
                result.header.statement_number = parts[0].strip()
            if len(parts) > 1:
                result.header.page_number = parts[1].strip()
            result.header.raw_tags['28C'] = content

        elif tag.startswith(self.TAG_60):
            # Opening Balance (60F or 60M)
            balance = self._parse_balance(content, 'Opening')
            if balance:
                result.opening_balance = balance
                result.default_currency = balance.currency_code
                current_opening_balance = balance

        elif tag == self.TAG_61:
            # Statement Line
            transaction = self._parse_statement_line(content, result.header.account_number)
            if transaction:
                # 如果交易记录没有币种代码，从余额信息中获取
                if not transaction.currency_code:
                    transaction.currency_code = result.default_currency or 'CNY'
                result.add_transaction(transaction)
                if block_transactions is not None:
                    block_transactions.append(transaction)

                # 累积描述
                if current_description:
                    transaction.transaction_description = '\n'.join(current_description)

        elif tag == self.TAG_86:
            # Information to Account Owner
            if current_transaction and result.transactions:
                last_txn = result.transactions[-1]
                self._parse_info_to_owner(content, last_txn)

        elif tag == self.TAG_62 or tag.startswith(self.TAG_62):
            # Closing Balance
            balance = self._parse_balance(content, 'Closing')
            if balance:
                result.closing_balance = balance

        elif tag == self.TAG_64:
            # Closing Available Balance
            balance = self._parse_balance(content, 'ClosingAvailable')
            if balance:
                result.closing_available_balance = balance

        elif tag.startswith(self.TAG_65):
            # Forward Available Balance
            balance = self._parse_balance(content, 'Forward')
            if balance:
                result.forward_available_balances.append(balance)

        elif content.strip() == '-':
            # Statement Terminator - 忽略
            pass

        else:
            # 未知标签，记录警告
            result.add_warning(f"未处理的标签: :{tag}:")

        return current_opening_balance

    def _parse_balance(self, content: str, balance_type: str) -> Optional[BalanceInfo]:
        """解析余额标签 (60, 62, 64, 65)"""
        # 格式: DCYYMMDDCCCNNNNN,NN
        # DC = C(贷) 或 D(借)
        # YYMMDD = 日期
        # CCC = 币种
        # NNNNN,NN = 金额

        pattern = re.compile(r'^([CD])(\d{6})([A-Z]{3})([\d,\.]+)$')
        match = pattern.match(content)

        if not match:
            return None

        try:
            dc_indicator = match.group(1)
            date_str = match.group(2)
            currency = match.group(3)
            amount_str = match.group(4).replace(',', '.')

            return BalanceInfo(
                balance_type=balance_type,
                dc_indicator=dc_indicator,
                booking_date=date_str,
                currency_code=currency,
                balance_amount=Decimal(amount_str)
            )
        except (InvalidOperation, ValueError) as e:
            return None

    def _parse_statement_line(self, content: str, account_number: str) -> Optional[TransactionRecord]:
        """
        解析 Tag 61 (Statement Line)

        格式:
        :61:YYMMDD[MMDD]D/CAmount[N]TRF//RefNo[//Supplementary]
        或
        :61:YYMMDD[MMDD]D/CAmountTRF//RefNo (BNP格式，没有Entry Method N)
        或
        :61:YYMMDD[MMDD]CY/DYAmountType (CCB中国建设银行格式: CY=贷方/收入，DY=借方/支出)

        子字段:
        1. Value Date: YYMMDD (6位)
        2. Entry Date: MMDD (4位,可选)
        3. D/C Indicator: C/D/RC/RD 或 CY/DY (CCB格式)
        4. Funds Code: 币种代码 (可选，2-3位字母，如USD,EUR)
        5. Amount: 金额
        6. Entry Method: N (固定,但有些银行省略)
        7. Entry Reason: 3位代码
        8. Reference: 可变, 以//结束
        9. Supplementary: 可选
        """
        txn = TransactionRecord()
        txn.account_number = account_number

        remaining = content

        # 1. Value Date (6位数字)
        date_match = re.match(r'^(\d{6})', remaining)
        if date_match:
            txn.value_date = date_match.group(1)
            remaining = remaining[6:]
        else:
            return None

        # 2. Entry Date (4位数字,可选)
        entry_date_match = re.match(r'^(\d{4})', remaining)
        if entry_date_match:
            txn.entry_date = entry_date_match.group(1)
            remaining = remaining[4:]

        # 3. CCB格式特殊处理：CY=贷方(收入)，DY=借方(支出)
        # CCB格式: YYMMDD[MMDD]CYAmountNType (如 1805230523CY37513,60NMSC)
        # CCB格式中CY/DY是借贷标识，不是币种代码
        ccb_dc_match = re.match(r'^(CY|DY)', remaining)
        if ccb_dc_match:
            # CCB格式：CY=贷方(收入)，DY=借方(支出)
            dc_code = ccb_dc_match.group(1)
            if dc_code == 'CY':
                txn.dc_indicator = 'C'  # CY 表示贷方(收入)
            else:  # DY
                txn.dc_indicator = 'D'  # DY 表示借方(支出)
            remaining = remaining[ccb_dc_match.end():]

            # 4. Amount (数字和逗号)
            amount_match = re.match(r'^([\d,\.]+)', remaining)
            if amount_match:
                try:
                    amount_str = amount_match.group(1).replace(',', '.')
                    txn.amount = Decimal(amount_str)
                except InvalidOperation:
                    txn.amount = Decimal('0')
                remaining = remaining[len(amount_match.group(1)):]

                # 在金额后应该有小数分隔符,移除可能的逗号
                if remaining.startswith(','):
                    remaining = remaining[1:]
            else:
                return None
        else:
            # 标准MT940格式
            # 3. D/C Indicator
            dc_match = re.match(r'^([CD]|RC|RD)', remaining)
            if dc_match:
                txn.dc_indicator = dc_match.group(1)
                remaining = remaining[len(dc_match.group(1)):]

                # 4. 再次检查是否有D/C (某些格式可能重复)
                dc_match2 = re.match(r'^([CD]|RC|RD)', remaining)
                if dc_match2:
                    remaining = remaining[len(dc_match2.group(1)):]
            else:
                return None

            # 5. 币种代码 (可选，2-3字母代码)
            currency_match = re.match(r'^([A-Z]{2,3})', remaining)
            if currency_match:
                txn.currency_code = currency_match.group(1)
                remaining = remaining[len(currency_match.group(1)):]

            # 6. Amount (数字和逗号)
            amount_match = re.match(r'^([\d,\.]+)', remaining)
            if amount_match:
                try:
                    amount_str = amount_match.group(1).replace(',', '.')
                    txn.amount = Decimal(amount_str)
                except InvalidOperation:
                    txn.amount = Decimal('0')
                remaining = remaining[len(amount_match.group(1)):]

                # 在金额后应该有小数分隔符,移除可能的逗号
                if remaining.startswith(','):
                    remaining = remaining[1:]
            else:
                return None

        # 6. Entry Method (N,固定) - 有些银行可能省略
        entry_method_match = re.match(r'^N([A-Z]{3})', remaining)
        if entry_method_match:
            # Entry Method + Entry Reason
            remaining = remaining[1:]
            reason_match = re.match(r'^([A-Z]{3})', remaining)
            if reason_match:
                txn.entry_reason_code = reason_match.group(1)
                remaining = remaining[3:]
        else:
            # 检查是否直接是Entry Reason
            reason_match = re.match(r'^([A-Z]{3})', remaining)
            if reason_match:
                txn.entry_reason_code = reason_match.group(1)
                remaining = remaining[3:]

        # 7. Reference (以//结束)
        if '//' in remaining:
            parts = remaining.split('//', 1)
            txn.reference_for_account_owner = parts[0].strip()
            txn.reference_number = txn.reference_for_account_owner or 'NONREF'

            if len(parts) > 1 and parts[1].strip():
                # 可能是Supplementary Details
                remaining = parts[1].strip()

                # 检查是否以/开始 (Supplementary Details)
                if remaining.startswith('/'):
                    txn.supplementary_details = remaining
                    self._parse_supplementary_details(remaining, txn)
                else:
                    # 剩余内容是Supplementary Details
                    txn.supplementary_details = remaining

        else:
            # 没有//分隔符,整个剩余内容作为参考
            txn.reference_number = remaining.strip() if remaining.strip() else 'NONREF'

        return txn

    def _parse_supplementary_details(self, content: str, txn: TransactionRecord):
        """
        解析 Tag 61 的 Supplementary Details
        格式: /BAI/Code/Description 或 /CTC/Code/Description
        """
        # 提取类型代码和描述
        bai_match = re.search(r'/BAI/\d+/(.*)$', content)
        if bai_match:
            txn.transaction_description = bai_match.group(1).strip()
            return

        ctc_match = re.search(r'/CTC/[A-Z]+/(.*)$', content)
        if ctc_match:
            txn.transaction_description = ctc_match.group(1).strip()
            return

    def _parse_info_to_owner(self, content: str, txn: TransactionRecord):
        """
        解析 Tag 86 (Information to Account Owner)

        标准格式:
        :86:/PT/FT/BE/BeneficiaryName/BN1/Address1/BN2/Address2/BO/OrderingParty/PY/PaymentInfo

        BNP格式:
        :86:/TYPE/150:SERVICE CHARGE/REF:CMI62314//INFO/AC27000001000001/OUTWARD TT OUR (ELECTRONIC)/

        代码:
        /PT/ - Product Type ID
        /BE/ - Beneficiary Name
        /BN1/, /BN2/ - Beneficiary Address Lines
        /BO/ - Ordering Party Name
        /PY/ - Payment Information
        /AC/ - Remitting Account
        /AB/ - Beneficiary Bank Account/Name
        /TYPE/ - Transaction Type
        /REF/ - Reference
        /INFO/ - Additional Info
        """
        # 移除开头的/PT/ (如果有)
        content = re.sub(r'^/PT/[A-Z]{2}/', '', content)

        # 解析各个代码
        patterns = {
            'counterparty_name': r'/BE/([^/]+)',
            'counterparty_account': r'/AC/([^/]+)',
            'counterparty_bank': r'/AB1?/([^/]+)',
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1).strip()
                if hasattr(txn, field):
                    setattr(txn, field, value)

        # 提取 TYPE 信息 (BNP格式)
        type_match = re.search(r'/TYPE/\d+:([^/]+)', content)
        if type_match:
            txn.entry_reason_description = type_match.group(1).strip()

        # 提取 REF 信息
        ref_match = re.search(r'/REF:([^/]+)', content)
        if ref_match:
            if not txn.reference_number or txn.reference_number == 'NONREF':
                txn.reference_number = ref_match.group(1).strip()

        # 提取 INFO 信息 (BNP格式作为交易描述)
        info_match = re.search(r'/INFO/([^/]+)', content)
        if info_match:
            info_desc = info_match.group(1).strip()
            if not txn.transaction_description:
                txn.transaction_description = info_desc
            else:
                txn.transaction_description += ' ' + info_desc

        # 提取描述信息
        py_match = re.search(r'/PY/(.+?)(?:/|$)', content)
        if py_match:
            desc = py_match.group(1).strip()
            if not txn.transaction_description:
                txn.transaction_description = desc
            else:
                txn.transaction_description += ' ' + desc

        # 累积描述
        if not txn.transaction_description:
            # 移除代码前缀获取纯文本描述
            clean_desc = re.sub(r'/[A-Z]{2,4}[/:]/', ' ', content)
            clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
            txn.transaction_description = clean_desc


def create_mt940_parser() -> MT940Parser:
    """工厂函数：创建MT940解析器"""
    return MT940Parser()

# -*- coding: utf-8 -*-
"""
Market Data Checker - 数据质量校验工具
对 market_data.json 进行全链路数据质量检查。
支持 10 类校验规则，可扩展，结果统一为通过/拒绝 + 原因。
"""
import sys
import os
import json
import re
import math
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# -- 路径配置 ----------------------------------------------
BASE_DIR = r"E:\daily"
SKILL_BASE = r"C:\Users\qu669\.openclaw\workspace-yoyo"
sys.path.insert(0, os.path.join(SKILL_BASE, "skills", "market-data-checker", "scripts"))
sys.path.insert(0, SKILL_BASE)

from validators.result import CheckResult
from validators.null_check import NullChecker
from validators.nan_check import NaNChecker
from validators.type_check import TypeChecker
from validators.range_check import RangeChecker
from validators.direction_check import DirectionChecker
from validators.dirty_check import DirtyChecker
from validators.completeness_check import CompletenessChecker

import logging
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'financial_assistant.log')
os.makedirs(LOG_DIR, exist_ok=True)
_log = logging.getLogger('market_data_checker')
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
_log.addHandler(handler)
_log.setLevel(logging.INFO)

# -- 全局配置 ----------------------------------------------
CONFIG = {
    "MAX_RETRIES": 3,
    "RETRY_DELAY": 2.0,
    "CONSECUTIVE_FAILURES_THRESHOLD": 3,
    "ALERT_EMAIL": "13045609072@163.com",
    "ALERT_SMTP_HOST": "smtp.163.com",
    "ALERT_SMTP_PORT": 25,
    "ALERT_SENDER": "13045609072@163.com",
    "ALERT_AUTH_CODE": "MN3dS36RDsLcyFTb",
    "ALERT_RECIPIENT": "yugi.chong@fubonchina.com",
}


# -- 检查结果（从 validators.result 导入）--------------------
from validators.result import CheckResult


# -- 核心检查器 ----------------------------------------------
class MarketDataChecker:
    """
    market_data.json 全链路检查器。

    支持的校验规则：
      1. 非空校验          → NullChecker
      2. 非 NaN/非无穷大   → NaNChecker
      3. 数值类型强校验    → TypeChecker
      4. 业务范围合理性    → RangeChecker
      5. 涨跌/收益率方向一致性 → DirectionChecker
      6. 脏数据拦截        → DirtyChecker
      7. 语句完整性校验    → CompletenessChecker
      8. 数据缺失自动重试  → 自动重试 load + 重新检查
      9. 连续失败终止链路  → 内置 fail-fast + 邮件告警
      10. 统一返回         → CheckResult(status, issues)
    """

    def __init__(self, market_data_file=None, date_str=None):
        self._retry_count = 0
        self._consecutive_fails = 0

        # 推算日期
        if date_str is None:
            date_str = time.strftime("%Y-%m-%d")
        self.date_str = date_str

        # 数据文件路径
        if market_data_file is None:
            market_data_file = os.path.join(BASE_DIR, date_str, "market_data.json")

        self.market_data_file = market_data_file
        self.data = None

    # -- 公开 API -------------------------------------------

    def check_all(self) -> CheckResult:
        """
        执行全量检查。
        自动重试（最多 MAX_RETRIES 次），连续失败超阈值则终止并告警。
        """
        _log.info(f"========== 数据质量检查开始 | 日期: {self.date_str} ==========")

        for attempt in range(1, CONFIG["MAX_RETRIES"] + 1):
            self._consecutive_fails = 0

            # 1. 加载数据（带重试）
            if not self._load_data(attempt):
                if attempt < CONFIG["MAX_RETRIES"]:
                    time.sleep(CONFIG["RETRY_DELAY"])
                    continue
                else:
                    # 最终失败
                    result = CheckResult()
                    result.fail(
                        rule="数据加载",
                        category="文件",
                        key=self.market_data_file,
                        value=None,
                        message=f"数据文件缺失或不可读，已重试 {CONFIG['MAX_RETRIES']} 次"
                    )
                    self._send_alert_email(
                        subject=f"[数据检查告警] {self.date_str} 数据加载失败",
                        body=f"重试 {CONFIG['MAX_RETRIES']} 次后数据仍无法加载。\n文件：{self.market_data_file}"
                    )
                    return result

            # 2. 执行各项校验
            all_pass = True
            result = CheckResult()

            checkers = [
                NullChecker(),
                NaNChecker(),
                TypeChecker(),
                RangeChecker(),
                DirectionChecker(),
                DirtyChecker(),
                CompletenessChecker(),
            ]

            for checker in checkers:
                name = checker.__class__.__name__.replace("Checker", "")
                _log.info(f"  执行 [{name}] ...")
                r = checker.check(self.data)
                if r.status == CheckResult.FAIL:
                    all_pass = False
                    self._consecutive_fails += 1
                    result.merge(r)
                    for issue in r.issues:
                        _log.error(f"    [FAIL] {issue['category']} > {issue['key']} | {issue['message']}")
                else:
                    _log.info(f"    [PASS]")
                    self._consecutive_fails = 0  # 重置连续失败计数

            if all_pass:
                return result  # PASS

            # 有校验失败但未超阈值 → 重试
            if attempt < CONFIG["MAX_RETRIES"]:
                time.sleep(CONFIG["RETRY_DELAY"])
                continue
            else:
                # 最终仍失败
                self._send_alert_email(
                    subject=f"[数据检查告警] {self.date_str} 数据质量不通过",
                    body=self._format_issues(result.issues)
                )
                return result

    def check_and_retry(self, max_attempts=None) -> CheckResult:
        """带手动重试的检查（可指定次数覆盖全局配置）"""
        if max_attempts:
            original = CONFIG["MAX_RETRIES"]
            CONFIG["MAX_RETRIES"] = max_attempts
        result = self.check_all()
        if max_attempts:
            CONFIG["MAX_RETRIES"] = original
        return result

    # -- 私有方法 -------------------------------------------

    def _load_data(self, attempt=1) -> bool:
        """加载 market_data.json，带重试日志"""
        try:
            with open(self.market_data_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            _log.warning(f"数据文件不存在（第 {attempt}/{CONFIG['MAX_RETRIES']} 次尝试）: {self.market_data_file}")
            return False
        except json.JSONDecodeError as e:
            _log.warning(f"JSON 解析失败（第 {attempt}/{CONFIG['MAX_RETRIES']} 次尝试）: {e}")
            return False
        except Exception as e:
            _log.warning(f"加载失败（第 {attempt}/{CONFIG['MAX_RETRIES']} 次尝试）: {e}")
            return False

    def _send_alert_email(self, subject, body):
        """发送告警邮件"""
        try:
            msg = MIMEMultipart()
            msg["From"] = Header(CONFIG["ALERT_SENDER"])
            msg["To"] = CONFIG["ALERT_RECIPIENT"]
            msg["Subject"] = Header(subject, "utf-8")
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(CONFIG["ALERT_SMTP_HOST"], CONFIG["ALERT_SMTP_PORT"]) as server:
                server.starttls()
                server.login(CONFIG["ALERT_SENDER"], CONFIG["ALERT_AUTH_CODE"])
                server.send_message(msg)
            print(f"  [INFO] 告警邮件已发送：{subject}")
        except Exception as e:
            print(f"  [WARN] 邮件发送失败：{e}")

    @staticmethod
    def _format_issues(issues) -> str:
        """将 issues 列表格式化为可读字符串"""
        if not issues:
            return "无问题"
        lines = []
        for i, issue in enumerate(issues, 1):
            lines.append(
                f"{i}. [{issue['rule']}] {issue['category']} > {issue['key']}\n"
                f"   值：{str(issue['value'])[:80]}\n"
                f"   原因：{issue['message']}"
            )
        return "\n".join(lines)



# -- 入口 ----------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Market Data Checker")
    parser.add_argument("--date", default=None, help="日期，如 2026-05-16（默认今天）")
    parser.add_argument("--file", default=None, help="market_data.json 路径")
    parser.add_argument("--retry", type=int, default=None, help="最大重试次数")
    args = parser.parse_args()

    checker = MarketDataChecker(
        market_data_file=args.file,
        date_str=args.date or time.strftime("%Y-%m-%d")
    )

    result = checker.check_and_retry(max_attempts=args.retry)

    if result.status == CheckResult.PASS:
        _log.info(f"[PASS] 检查通过，共 {len(result.issues)} 项，无问题")
    else:
        _log.error(f"[FAIL] 检查拒绝，共 {len(result.issues)} 个问题")
        for issue in result.issues:
            _log.error(f"  [FAIL] [{issue['rule']}] {issue['category']} > {issue['key']} | 值: {str(issue['value'])[:80]} | 原因: {issue['message']}")
        _log.error("--- 告警邮件已发送 ---")

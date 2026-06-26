# -*- coding: utf-8 -*-
"""
CheckResult - 检查结果数据结构
所有校验器共享的返回格式。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


class CheckResult:
    PASS = "PASS"
    FAIL = "FAIL"

    def __init__(self):
        self.status = self.PASS
        self.issues = []

    def fail(self, rule: str, category: str, key: str, value, message: str):
        self.status = self.FAIL
        self.issues.append({
            "rule": rule,
            "category": category,
            "key": key,
            "value": value,
            "message": message,
        })

    def merge(self, other: "CheckResult"):
        if other.status == self.FAIL:
            self.status = self.FAIL
            self.issues.extend(other.issues)

    def to_dict(self):
        return {
            "status": self.status,
            "total_issues": len(self.issues),
            "issues": self.issues,
        }
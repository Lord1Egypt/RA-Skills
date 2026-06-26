#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
# -*- coding: utf-8 -*-

"""
API 数据模型
"""

from dataclasses import dataclass, field
from typing import List, Any, Optional


# 报告列表
@dataclass
class EcgListItem:
    reportNo: str  # Note: API might return int, but we treat as str for consistency
    takeTime: int
    ecgResult: str
    userId: str

    @classmethod
    def from_dict(cls, data: dict):
        # Some environments return reportId instead of reportNo.
        report_no = data.get("reportNo")
        if report_no is None:
            report_no = data.get("reportId")

        return cls(
            reportNo=str(report_no or ""),
            takeTime=data.get("takeTime", 0),
            ecgResult=data.get("ecgResult", ""),
            userId=data.get("userId", "")
        )


@dataclass
class DataListResult:
    status: bool
    datas: List[EcgListItem]


# 报告详情
@dataclass
class NormalListItem:
    name: str
    ecg: str
    range: str
    state: int
    explain: str = ""
    company: str = ""

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            ecg=str(data.get("ecg", "")),
            range=data.get("range", ""),
            state=data.get("state", 0),
            explain=data.get("explain", ""),
            company=data.get("company", "")
        )


@dataclass
class ReportDetail:
    # 核心字段
    title: str
    ecgResultTz: str
    hrv: str
    suggestion: str
    fileImagePath: str
    avg: Any  # Can be int or str
    max: Any
    min: Any
    normalList: List[NormalListItem] = field(default_factory=list)

    # 扩展字段 (Optional)
    healthLevel: int = 0
    normalRate: int = 0

    # 风险评估与压力
    hdrisk: str = ""
    hdrisk_value: int = 0
    hdrisk_status: int = 0

    fatigue: str = ""
    fatigue_value: int = 0
    fatigue_status: int = 0

    mentalPressure: str = ""
    mental_value: int = 0
    mental_status: int = 0

    # 其他信息
    abnorAnalysis: str = ""
    ecgResult: str = ""
    ecgUrl: str = ""
    reportPdf: str = ""
    healthCareAdvice: str = ""
    filePath: str = ""
    hlyPath: str = ""

    hrv_value: int = 0
    hrv_status: int = 0

    takeTime: int = 0
    heartRate: int = 0
    heartbeatRate: int = 0
    ifPayment: int = 0
    slowRate: int = 0

    @classmethod
    def from_dict(cls, data: dict):
        normal_list_data = data.get("normalList", [])
        normal_list = [NormalListItem.from_dict(item) for item in normal_list_data] if normal_list_data else []

        return cls(
            title=data.get("title", ""),
            ecgResultTz=data.get("ecgResultTz", ""),
            hrv=data.get("hrv", ""),
            suggestion=data.get("suggestion", ""),
            fileImagePath=data.get("fileImagePath", ""),
            avg=data.get("avg", "--"),
            max=data.get("max", "--"),
            min=data.get("min", "--"),
            normalList=normal_list,
            healthLevel=data.get("healthLevel", 0),
            normalRate=data.get("normalRate", 0),

            hdrisk=data.get("hdrisk", ""),
            hdrisk_value=data.get("hdrisk_value", 0),
            hdrisk_status=data.get("hdrisk_status", 0),

            fatigue=data.get("fatigue", ""),
            fatigue_value=data.get("fatigue_value", 0),
            fatigue_status=data.get("fatigue_status", 0),

            mentalPressure=data.get("mentalPressure", ""),
            mental_value=data.get("mental_value", 0),
            mental_status=data.get("mental_status", 0),

            abnorAnalysis=data.get("abnorAnalysis", ""),
            ecgResult=data.get("ecgResult", ""),
            ecgUrl=data.get("ecgUrl", ""),
            reportPdf=data.get("reportPdf", ""),
            healthCareAdvice=data.get("healthCareAdvice", ""),
            filePath=data.get("filePath", ""),
            hlyPath=data.get("hlyPath", ""),

            hrv_value=data.get("hrv_value", 0),
            hrv_status=data.get("hrv_status", 0),

            takeTime=data.get("takeTime", 0),
            heartRate=data.get("heartRate", 0),
            heartbeatRate=data.get("heartbeatRate", 0),
            ifPayment=data.get("ifPayment", 0),
            slowRate=data.get("slowRate", 0)
        )

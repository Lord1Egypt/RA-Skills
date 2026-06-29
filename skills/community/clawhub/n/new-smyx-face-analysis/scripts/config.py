#!/usr/bin/env python3
# 宠物健康诊断分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.smyx_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent


class ApiEnum(ApiEnumParent):

    @classmethod
    def init(cls, config=None):
        super().init(config)
        ApiEnumParent.ANALYSIS_URL = "/web/health-analysis/v2/start-health-analysis"
        ApiEnumParent.ANALYSIS_RESULT_URL = "/web/health-analysis/get-health-analysis-result"
        ApiEnumParent.PAGE_URL = "/web/health-analysis/page-health-analysis-result"


class ConstantEnum(ConstantEnumParent):

    @classmethod
    def init(cls, config=None):
        super().init(config)

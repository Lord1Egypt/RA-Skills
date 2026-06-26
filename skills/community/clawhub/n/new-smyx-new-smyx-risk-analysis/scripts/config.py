#!/usr/bin/env python3
import os
import sys

# def import_path_common():
#     current_dir = os.path.dirname(os.path.abspath(__file__))  # .../face_analysis/scripts
#     # common 位于 /root/.openclaw/workspace/skills/scripts/common
#     skills_dir = os.path.dirname(os.path.dirname(current_dir))  # .../skills
#     workspace_dir = os.path.dirname(skills_dir)  # .../skills
#     common_dir = os.path.join(skills_dir, 'scripts', 'common')
#     scripts_dir = os.path.join(skills_dir, 'scripts')
#     if scripts_dir not in sys.path:
#         sys.path.insert(1, workspace_dir)
#         sys.path.insert(1, scripts_dir)
#         sys.path.insert(1, common_dir)
#
#
# import_path_common()
from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.face_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    SceneCodeEnum


# from skills.face_analysis.scripts.config import SceneCodeEnum

class ApiEnum(ApiEnumParent):
    ANALYSIS_URL = "/open/coze/v1/ai-analysis"
    PAGE_URL = "/web/health-analysis/page-health-analysis-result"


class ConstantEnum(ConstantEnumParent):

    @classmethod
    def init(cls, config=None):
        super().init(config)
        cls.DEFAULT__SCENE_CODE = SceneCodeEnum.OPEN_PERSON_RISK_ANALYSIS.value


# 默认分析配置
DEFAULT_ANALYSIS_MODE = "all"
DEFAULT_ALERT_THRESHOLD = 0.8
DEFAULT_AUTO_ALERT = False
MAX_FILE_SIZE_MB = 200

# 支持的格式
SUPPORTED_VIDEO_FORMATS = ["mp4", "avi", "mov", "webm", "mkv"]
SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "gif", "bmp"]
SUPPORTED_STREAM_PROTOCOLS = ["rtsp", "rtmp", "http", "https"]

# 实时流配置
STREAM_FRAME_INTERVAL = 30  # 每30帧分析一次
STREAM_ALERT_COOLDOWN = 60  # 同一类型风险60秒内不重复报警
REQUEST_TIMEOUT = 120

# 预警通知配置
ALERT_FEISHU_WEBHOOK = os.getenv("ALERT_FEISHU_WEBHOOK", "")
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "")

# 默认API配置（从环境变量读取）
DEFAULT_API_KEY = os.getenv("RISK_ANALYSIS_API_KEY", "")
DEFAULT_API_URL = os.getenv("RISK_ANALYSIS_API_URL", "https://open.lifeemergence.com/smyx-open-api")

"""
配置文件
"""
import os

# 文件编码（全平台兼容：iOS / Android / iPad / PC / 微信小程序 WebView）
# HTML 使用 UTF-8 BOM，便于移动端在未读到 meta 时也能正确识别编码
HTML_FILE_ENCODING = 'utf-8-sig'
# JSON / 纯文本使用标准 UTF-8（无 BOM）
JSON_FILE_ENCODING = 'utf-8'
TEXT_FILE_ENCODING = 'utf-8'

# API 配置
API_BASE_URL = os.getenv('API_BASE_URL', 'http://192.168.96.17:8900')
API_ENDPOINT = '/api/recordings/asr-completed/page'

# Skill 目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

# 输出配置（存储在 skill 目录下的 reports 子目录）
OUTPUT_DIR = os.path.join(SKILL_DIR, 'reports')

# 分页配置
DEFAULT_PAGE_SIZE = 20
DEFAULT_DAYS = 7  # 默认查询最近7天（一周）

# Redis 配置（用于分页状态管理）
REDIS_EXPIRE_MINUTES = 10

# 固定目录确保存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

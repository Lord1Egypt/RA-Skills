from version import __version__
"""
v2.4.4 配置模块（修复 21：硬编码阈值抽离）
所有可调参数集中在此，方便按需调整而无需修改主代码。
"""
from typing import Pattern
import re

# ======================
# PDF 布局阈值
# ======================
# 购方/销方列分界（PDF 坐标 x0 单位：pt）
COL_SPLIT: float = 295.0          # 购方右边界
COL_SPLIT_RIGHT: float = 302.0    # 销方左边界

# 表格行合并容差（同行的 top 坐标差 ≤ 此值视为同一行）
ROW_MERGE_TOLERANCE: float = 20.0

# 文本块相邻合并容差
TEXT_MERGE_TOLERANCE: float = 4.0

# ======================
# 字段识别阈值
# ======================
# 项目名最大长度
ITEM_NAME_MAX_LENGTH: int = 80

# 项目名清理时移除的列名关键词
ITEM_NAME_COLUMN_KEYWORDS: str = r'规格型号|单位|数量|单价|金额|税率/?征收率?|^税\s*额|税\s*额$'

# 数字杂质模式（数量、单价、金额、税率等）
ITEM_NAME_NUMBER_PATTERN: str = r'\d+\s*[×x]\d+|\d+\.\d+\s*%|\s*\d+$'

# ======================
# 发票号识别
# ======================
# 发票号最小长度（防止误匹配短数字）
INVOICE_NUMBER_MIN_LENGTH: int = 15
# 发票号最大长度
INVOICE_NUMBER_MAX_LENGTH: int = 25

# ======================
# 日期识别
# ======================
# 日期搜索范围（"开票日期:"后的字符数）
DATE_SEARCH_RANGE_AFTER_KEY: int = 200

# ======================
# OCR 兜底（v2.4.0 PaddleOCR）
# ======================
OCR_TIMEOUT_SECONDS: int = 30
OCR_DPI: int = 200

# ======================
# 销方识别关键词（行业判断）
# ======================
SELLER_KEYWORDS: list = [
    '餐饮', '酒店', '餐厅', '商店', '超市', '商场', '百货',
    '销售', '制造', '生产', '厂', '酒店', '餐饮', '食品',
    '加油站', '充电', '出行', '通行', '网约车', '代驾',
    '云计算', '云服务', '技术服务', '信息技术', '管理咨询',
    '超市', '便利店', '盒马', '鲜',
]

# ======================
# 性能与输出
# ======================
# Excel 列宽（v2.4.0 15 列 / v3.0 16 列）
EXCEL_COLUMN_WIDTHS_15COL: list = [6, 22, 12, 28, 22, 28, 22, 30, 12, 8, 12, 14, 30, 10, 12]
EXCEL_COLUMN_WIDTHS_16COL: list = [6, 22, 12, 28, 22, 28, 22, 30, 12, 8, 12, 14, 30, 10, 12, 10]

# 冻结首行
FREEZE_PANES: str = 'A2'

# 通行费合并阈值（修复 4，待 v2.5.0）
TOLL_MERGE_ENABLED: bool = False
TOLL_MERGE_LOOKBACK_DAYS: int = 35  # 同车牌合并窗口

# 税率合法值校验
LEGAL_TAX_RATES: list = ['3%', '6%', '9%', '13%', '免税', '不征税', '出口零税']

# ======================
# 文件名特殊字符处理
# ======================
SAFE_FILENAME_REGEX: Pattern = re.compile(r'[^\w\-\.]')

# ======================
# 日志
# ======================
LOG_FILE: str = 'invoice_extractor.log'
LOG_LEVEL: str = 'INFO'  # DEBUG / INFO / WARNING / ERROR
LOG_FORMAT: str = '%(asctime)s [%(levelname)s] %(message)s'

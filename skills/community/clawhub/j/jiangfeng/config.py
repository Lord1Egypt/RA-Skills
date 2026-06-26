"""
配置文件 - 投放数据分析技能的配置参数
"""

CONFIG = {
    # 默认数据目录
    "DEFAULT_DATA_DIR": "/Users/zhouhao/Documents/投放数据",
    
    # 默认输出目录
    "DEFAULT_OUTPUT_DIR": "/Users/zhouhao/Desktop/投放分析报告",
    
    # 支持的文件类型
    "SUPPORTED_FILE_TYPES": [".csv", ".xlsx"],
    
    # 文件识别关键词
    "FILE_KEYWORDS": {
        "super": ["超级直播"],
        "taobao": ["淘宝直播"],
        "financial": ["财务", "财务报表"]
    },
    
    # 字段映射配置
    "FIELD_MAPPING": {
        "super": {
            "date": ["日期"],
            "cost": ["花费"],
            "revenue": ["总成交金额", "直接成交金额"],
            "orders": ["总成交笔数", "直接成交笔数"],
            "views": ["观看次数", "有效观看次数"],
            "impressions": ["展现量"]
        },
        "taobao": {
            "date": ["日期"],
            "revenue": ["成交金额"],
            "orders": ["成交笔数"],
            "users": ["成交人数", "观看人数"],
            "conversion": ["成交转化率"]
        },
        "financial": {
            "date": ["直播日期", "日期"],
            "revenue": ["业务口径收入", "财务口径收入"],
            "commission": ["保量佣金", "预估结算线下佣金", "预估结算机构佣金"],
            "profit": ["毛利"],
            "margin": ["毛利率"]
        }
    },
    
    # 编码检测配置
    "ENCODING_DETECTION": {
        "sample_size": 10000,  # 检测编码时读取的字节数
        "encodings_to_try": ["utf-8", "gbk", "gb2312", "latin1"]
    },
    
    # 数值字段识别模式
    "NUMERIC_FIELD_PATTERNS": [
        "花费", "金额", "成本", "笔数", "次数", "量", "率", "价", "数", "费"
    ],
    
    # 日期字段识别模式
    "DATE_FIELD_PATTERNS": [
        "日期", "时间", "date", "time"
    ],
    
    # 报告配置
    "REPORT_CONFIG": {
        "html": {
            "table_max_rows": 100,  # HTML表格最大显示行数
            "preview_rows": 5       # 数据预览行数
        },
        "csv": {
            "encoding": "utf-8-sig"  # CSV文件编码
        }
    },
    
    # 指标计算配置
    "METRICS_CONFIG": {
        "super": {
            "required_fields": ["花费", "总成交金额"],
            "optional_fields": ["观看次数", "总成交笔数", "总收藏数", "总购物车数"]
        },
        "taobao": {
            "required_fields": ["成交金额", "成交人数"],
            "optional_fields": ["商品点击人数", "加购人数", "退款金额"]
        },
        "financial": {
            "required_fields": [],
            "optional_fields": ["品牌费", "切片", "保量佣金", "预估结算机构佣金", "预估结算线下佣金"]
        }
    },
    
    # 数据质量检查配置
    "DATA_QUALITY_CONFIG": {
        "missing_threshold": 0.3,  # 缺失值阈值（30%）
        "date_consistency_check": True,
        "numeric_range_check": True
    },
    
    # 性能配置
    "PERFORMANCE_CONFIG": {
        "max_file_size_mb": 100,  # 最大文件大小（MB）
        "chunk_size": 10000,      # 分块处理大小
        "timeout_seconds": 300    # 处理超时时间（秒）
    }
}
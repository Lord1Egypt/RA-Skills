# 投放数据分析技能

## 技能概述
基于《数据分析基础概念和逻辑v3.md》文档开发的标准化投放数据分析技能，用于处理超级直播、淘宝直播和财务报表数据。

## 适用场景
- 万相台投放数据统计分析
- 直播数据多维度分析
- 财务数据与业务数据关联分析
- ROI优化和成本分析

## ClawHub使用
通过环境变量配置：
```bash
# 设置环境变量
TOUFANG_DATE_RANGE="2026-01-01:2026-01-31"

# 运行技能
python3 clawhub_main.py

# 或者一次性设置
TOUFANG_DATE_RANGE="2026-01-01:2026-01-31" python3 clawhub_main.py
```

## 输入要求
- 时间范围：YYYY-MM-DD格式的日期范围
- 数据文件：自动识别三类数据文件
  - 超级直播数据（包含"超级直播"关键词）
  - 淘宝直播数据（包含"淘宝直播"关键词）
  - 财务数据（包含"财务"关键词）

## 输出内容
1. HTML汇总报表（桌面保存）
2. 数据质量检查报告
3. 关键指标计算
4. 优化建议

## 核心功能

### 1. 数据自动识别
```python
# 自动识别数据文件
def auto_detect_files(data_dir):
    """自动识别三类数据文件"""
    super_files = find_files(data_dir, "超级直播")
    taobao_files = find_files(data_dir, "淘宝直播") 
    financial_files = find_files(data_dir, "财务")
    return super_files, taobao_files, financial_files
```

### 2. 编码自动处理
```python
# 自动检测和处理编码
def auto_detect_encoding(file_path):
    """自动检测文件编码格式"""
    # 支持GBK、UTF-8等常见编码
    # 自动转换和统一处理
```

### 3. 字段映射计算
基于文档中的字段定义和计算公式：

**超级直播关键计算：**
- ROI = 总成交金额 / 花费
- 观看成本 = 花费 / 观看次数
- 订单成本 = 花费 / 总成交笔数
- 加购成本 = 花费 / (总收藏数 + 总购物车数)

**淘宝直播关键计算：**
- 成交转化率 = 成交人数 / 商品点击人数
- 客单价 = 成交金额 / 成交人数
- 笔单价 = 成交金额 / 成交笔数

**财务报表关键计算：**
- 业务口径收入 = 品牌费 + 切片 + 保量佣金 + 预估结算机构佣金 + 预估结算线下佣金
- 财务口径收入 = 业务口径收入 / 1.06
- 毛利率 = 毛利 / 财务口径收入

### 4. 跨报表关联分析
```python
# 跨报表数据关联
def cross_report_analysis(super_df, taobao_df, financial_df):
    """基于文档的跨报表关联分析"""
    # 超级直播去退ROI参考值
    roi_adjusted = (super_df['总成交金额'] * (1 - taobao_df['退货率'])) / super_df['花费']
    
    # 推广投入回报率
    promotion_roi = (financial_df[['保量佣金','预估结算线下佣金','预估结算机构佣金']].sum() * 
                    (super_df['总成交笔数'] / taobao_df['成交笔数'])) / super_df['花费']
    
    return roi_adjusted, promotion_roi
```

## 使用示例

### 基本使用
```bash
# 调用投放数据分析技能
投放数据分析 --date-range "2026-01-01:2026-01-31" --data-dir "/Users/zhouhao/Documents/投放数据"
```

### 高级使用
```bash
# 包含特定指标计算
投放数据分析 --date-range "2026-01-01:2026-01-31" \
              --metrics "ROI,观看成本,订单成本" \
              --output-format "html,csv"
```

## 文件结构
```
投放数据分析技能/
├── SKILL.md          # 技能说明文档
├── requirements.txt  # Python依赖
├── main.py           # 主程序
├── data_processor.py # 数据处理模块
├── calculator.py     # 指标计算模块
├── reporter.py       # 报表生成模块
└── config.py         # 配置文件
```

## 依赖要求
- pandas >= 1.5.0
- numpy >= 1.21.0
- chardet >= 5.0.0

## 输出示例
技能执行后会生成：
1. `YYYY-MM-DD_投放数据分析报告.html` - 完整HTML报表
2. `YYYY-MM-DD_数据质量检查.csv` - 数据质量报告
3. `YYYY-MM-DD_关键指标汇总.csv` - 指标计算结果

## 错误处理
- 自动处理文件编码问题
- 字段缺失时的智能处理
- 数据质量异常预警

## 版本历史
- v1.0.0: 初始版本，基于数据分析基础概念和逻辑v3.md

## 作者
江风 - 交个朋友直播间
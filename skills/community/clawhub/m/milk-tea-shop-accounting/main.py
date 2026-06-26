import re
from datetime import datetime
from typing import Dict, List, Tuple

class MilkTeaAccounting:
    def __init__(self):
        # 收入关键词
        self.income_keywords = {
            'income': ['收入', '收款', '营业额', '销售额', '到账', '堂食', '外卖', '美团', '饿了么', '团购', '抖音'],
            'type_map': {
                '堂食': '堂食收入',
                '外卖': '外卖收入',
                '美团': '外卖收入',
                '饿了么': '外卖收入',
                '团购': '团购收入',
                '抖音': '团购收入'
            }
        }
        
        # 支出关键词
        self.expense_keywords = {
            'expense': ['支出', '付款', '花费', '成本', '费用', '采购', '进货', '房租', '工资', '人工', '水电', '物业费', '耗材'],
            'type_map': {
                '原料': '原材料成本',
                '材料': '原材料成本',
                '进货': '原材料成本',
                '采购': '原材料成本',
                '房租': '房租成本',
                '租金': '房租成本',
                '工资': '人工成本',
                '人工': '人工成本',
                '员工': '人工成本',
                '水电': '水电杂费',
                '电费': '水电杂费',
                '水费': '水电杂费',
                '物业': '水电杂费',
                '耗材': '其他成本',
                '包装': '其他成本',
                '设备': '其他成本'
            }
        }
        
        # 金额正则匹配，支持逗号分隔的大数字
        self.amount_pattern = r'([\d,]+\.?\d*)\s*(元|块|钱)?'
    
    def extract_amount(self, text: str) -> float:
        """从文本中提取金额，支持逗号分隔的大数字"""
        matches = re.findall(self.amount_pattern, text)
        if matches:
            # 去掉金额中的逗号
            amount_str = matches[0][0].replace(',', '')
            return float(amount_str)
        return 0.0
    
    def classify_income(self, text: str) -> Tuple[str, float]:
        """分类收入"""
        amount = self.extract_amount(text)
        if amount == 0:
            return ('', 0)
        
        for keyword, income_type in self.income_keywords['type_map'].items():
            if keyword in text:
                return (income_type, amount)
        
        return ('其他收入', amount)
    
    def classify_expense(self, text: str) -> Tuple[str, float]:
        """分类支出"""
        amount = self.extract_amount(text)
        if amount == 0:
            return ('', 0)
        
        for keyword, expense_type in self.expense_keywords['type_map'].items():
            if keyword in text:
                return (expense_type, amount)
        
        return ('其他支出', amount)
    
    def parse_flow(self, flow_content: str) -> Dict:
        """解析流水内容"""
        lines = [line.strip() for line in flow_content.split('\n') if line.strip()]
        
        income = {
            '堂食收入': 0.0,
            '外卖收入': 0.0,
            '团购收入': 0.0,
            '其他收入': 0.0,
            '总收入': 0.0
        }
        
        expense = {
            '原材料成本': 0.0,
            '房租成本': 0.0,
            '人工成本': 0.0,
            '水电杂费': 0.0,
            '其他成本': 0.0,
            '总支出': 0.0
        }
        
        for line in lines:
            # 判断是收入还是支出
            is_income = any(keyword in line for keyword in self.income_keywords['income'])
            is_expense = any(keyword in line for keyword in self.expense_keywords['expense'])
            
            if is_income:
                inc_type, amount = self.classify_income(line)
                if inc_type:
                    income[inc_type] += amount
                    income['总收入'] += amount
            elif is_expense:
                exp_type, amount = self.classify_expense(line)
                if exp_type:
                    expense[exp_type] += amount
                    expense['总支出'] += amount
            else:
                # 没有关键词的尝试自动判断
                amount = self.extract_amount(line)
                if amount > 0:
                    if '收' in line or '卖' in line or '入' in line:
                        income['其他收入'] += amount
                        income['总收入'] += amount
                    elif '付' in line or '花' in line or '出' in line:
                        expense['其他支出'] += amount
                        expense['总支出'] += amount
        
        # 计算利润
        profit = income['总收入'] - expense['总支出']
        gross_margin = (profit / income['总收入']) * 100 if income['总收入'] > 0 else 0
        
        return {
            'income': income,
            'expense': expense,
            'profit': profit,
            'gross_margin': round(gross_margin, 2),
            'parse_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_report(self, parsed_data: Dict, period: str = 'month') -> str:
        """生成分析报告"""
        income = parsed_data['income']
        expense = parsed_data['expense']
        profit = parsed_data['profit']
        gross_margin = parsed_data['gross_margin']
        
        period_name = {
            'day': '日',
            'week': '周',
            'month': '月'
        }.get(period, '月')
        
        report = f"""🍵 奶茶店{period_name}度经营分析报告
=============================
📈 收入情况（总计：¥{income['总收入']:.2f}）
- 堂食收入：¥{income['堂食收入']:.2f}（占比：{income['堂食收入']/income['总收入']*100:.1f}%）
- 外卖收入：¥{income['外卖收入']:.2f}（占比：{income['外卖收入']/income['总收入']*100:.1f}%）
- 团购收入：¥{income['团购收入']:.2f}（占比：{income['团购收入']/income['总收入']*100:.1f}%）
- 其他收入：¥{income['其他收入']:.2f}（占比：{income['其他收入']/income['总收入']*100:.1f}%）

📉 支出情况（总计：¥{expense['总支出']:.2f}）
- 原材料成本：¥{expense['原材料成本']:.2f}（占比：{expense['原材料成本']/expense['总支出']*100:.1f}%）
- 房租成本：¥{expense['房租成本']:.2f}（占比：{expense['房租成本']/expense['总支出']*100:.1f}%）
- 人工成本：¥{expense['人工成本']:.2f}（占比：{expense['人工成本']/expense['总支出']*100:.1f}%）
- 水电杂费：¥{expense['水电杂费']:.2f}（占比：{expense['水电杂费']/expense['总支出']*100:.1f}%）
- 其他成本：¥{expense['其他成本']:.2f}（占比：{expense['其他成本']/expense['总支出']*100:.1f}%）

💰 利润情况
- {period_name}净利润：¥{profit:.2f}
- 毛利率：{gross_margin:.2f}%

💡 优化建议
"""
        # 生成个性化建议
        if income['总收入'] > 0 and income['外卖收入'] / income['总收入'] < 0.3:
            report += "- 外卖收入占比较低，建议加大外卖平台推广力度，推出满减活动提升外卖订单\n"
        if expense['总支出'] > 0 and expense['原材料成本'] / expense['总支出'] > 0.5:
            report += "- 原材料成本占比过高，建议和供应商谈长期合作价，优化库存管理减少浪费\n"
        if gross_margin < 30:
            report += "- 毛利率偏低，建议适当调整产品价格，或者推出高毛利的新品\n"
        if profit < 0:
            report += "- 当前处于亏损状态，建议优先缩减非必要支出，同时推出促销活动提升营业额\n"
        else:
            report += "- 经营状况良好，建议保持当前成本控制，同时拓展新的收入渠道\n"
        
        report += "\n生成时间：" + parsed_data['parse_time']
        return report

def analyze_milk_tea_flow(flow_content: str, period: str = 'month') -> str:
    """分析奶茶店流水的入口函数"""
    accounting = MilkTeaAccounting()
    parsed_data = accounting.parse_flow(flow_content)
    report = accounting.generate_report(parsed_data, period)
    return report

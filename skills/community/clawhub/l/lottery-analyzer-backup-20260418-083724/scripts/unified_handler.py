#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一处理器 - 同时支持数据更新和预测分析
OpenClaw / 飞书 入口

使用方式：
  # 添加数据
  python unified_handler.py --action add --data "双色球 2026041 020810171924+13"
  
  # 预测分析
  python unified_handler.py --action predict --issue 2026042
  
  # 自动识别（推荐）
  python unified_handler.py --input "双色球 2026041 020810171924+13"
  python unified_handler.py --input "预测 2026042期"
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

# 设置 Windows 控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加当前目录到路径
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(current_dir))

# 颜色代码（可选）
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# 如果 Windows 不支持，禁用
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')


class UnifiedHandler:
    """统一处理器"""
    
    def __init__(self):
        self.data_path = parent_dir / "data" / "ssq_standard.csv"
        self.predictions_dir = parent_dir / "predictions"
        self.reports_dir = parent_dir / "reports"
        
        # 确保目录存在
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self.predictions_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载数据
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        try:
            import pandas as pd
            if self.data_path.exists():
                self.df = pd.read_csv(self.data_path, header=None,
                                     names=['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝'])
                self.df = self.df.astype(int)
            else:
                self.df = pd.DataFrame(columns=['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝'])
        except Exception as e:
            self.df = None
            print(f"{Colors.RED}加载数据失败: {e}{Colors.RESET}")
    
    def _save_data(self):
        """保存数据"""
        try:
            import pandas as pd
            self.df = self.df.sort_values('期号').reset_index(drop=True)
            self.df.to_csv(self.data_path, index=False, header=False)
            return True
        except Exception as e:
            print(f"{Colors.RED}保存失败: {e}{Colors.RESET}")
            return False
    
    def parse_lottery_input(self, input_str):
        """
        解析彩票输入
        支持格式：
        - 2026041 020810171924+13
        - 双色球 2026041 020810171924+13
        - 2026041 02 08 10 17 19 24 + 13
        """
        input_str = input_str.strip()
        
        # 移除"双色球"前缀
        if input_str.startswith('双色球'):
            input_str = input_str[3:].strip()
        
        # 格式1: 期号 红球+蓝球
        pattern1 = r'^(\d{7})\s+(\d{12})\+(\d{2})$'
        match = re.match(pattern1, input_str)
        
        if match:
            period = match.group(1)
            red_str = match.group(2)
            blue = match.group(3)
            reds = [int(red_str[i:i+2]) for i in range(0, 12, 2)]
            return {
                'type': 'add',
                'period': int(period),
                'reds': reds,
                'blue': int(blue),
                'raw': f"{''.join(f'{r:02d}' for r in reds)}+{blue}"
            }
        
        # 格式2: 期号 红1 红2 ... + 蓝球
        pattern2 = r'^(\d{7})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s*\+\s*(\d{2})$'
        match = re.match(pattern2, input_str)
        
        if match:
            period = match.group(1)
            reds = [int(match.group(i)) for i in range(2, 8)]
            blue = match.group(8)
            return {
                'type': 'add',
                'period': int(period),
                'reds': reds,
                'blue': int(blue),
                'raw': f"{''.join(f'{r:02d}' for r in reds)}+{blue}"
            }
        
        return None
    
    def parse_predict_input(self, input_str):
        """解析预测请求"""
        input_str = input_str.strip().lower()
        
        # 预测 2026042期
        pattern = r'预测\s*(\d{7})'
        match = re.search(pattern, input_str)
        
        if match:
            return {
                'type': 'predict',
                'issue': match.group(1)
            }
        
        # 简单的"预测"或"分析"
        if input_str in ['预测', '分析', 'predict', '分析一下', '推荐号码']:
            # 获取最新期号+1
            if self.df is not None and len(self.df) > 0:
                latest_issue = self.df['期号'].max()
                return {
                    'type': 'predict',
                    'issue': str(latest_issue + 1)
                }
        
        return None
    
    def add_data(self, data):
        """添加数据到CSV"""
        import pandas as pd
        
        period = data['period']
        reds = data['reds']
        blue = data['blue']
        
        # 检查期号是否已存在
        if period in self.df['期号'].values:
            return {
                'success': False,
                'error': f'期号 {period} 已存在',
                'alert': True
            }
        
        # 检查红球范围
        for red in reds:
            if red < 1 or red > 33:
                return {
                    'success': False,
                    'error': f'红球 {red} 超出范围(1-33)',
                    'alert': True
                }
        
        # 检查红球重复
        if len(set(reds)) != 6:
            return {
                'success': False,
                'error': f'红球有重复: {reds}',
                'alert': True
            }
        
        # 检查蓝球范围
        if blue < 1 or blue > 16:
            return {
                'success': False,
                'error': f'蓝球 {blue} 超出范围(1-16)',
                'alert': True
            }
        
        # 添加数据
        new_row = pd.DataFrame([{
            '期号': period,
            '红1': reds[0],
            '红2': reds[1],
            '红3': reds[2],
            '红4': reds[3],
            '红5': reds[4],
            '红6': reds[5],
            '蓝': blue
        }])
        
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        
        if not self._save_data():
            return {
                'success': False,
                'error': '保存文件失败',
                'alert': True
            }
        
        # 检查连续性
        continuity_result = self.check_continuity()
        
        return {
            'success': True,
            'period': period,
            'reds': reds,
            'blue': blue,
            'raw_string': data['raw'],
            'total_periods': len(self.df),
            'is_continuous': continuity_result['is_continuous'],
            'missing_periods': continuity_result['missing_periods']
        }
    
    def check_continuity(self, check_count=100):
        """检查数据连续性"""
        if self.df is None or len(self.df) < 2:
            return {'is_continuous': True, 'missing_periods': []}
        
        periods = sorted(self.df['期号'].values, reverse=True)
        missing_periods = []
        
        for i in range(min(len(periods)-1, check_count)):
            current = periods[i]
            next_period = periods[i+1]
            expected = current - 1
            
            if next_period != expected:
                for missing in range(expected + 1, current):
                    missing_periods.append(missing)
        
        return {
            'is_continuous': len(missing_periods) == 0,
            'missing_periods': missing_periods[:20]
        }
    
    def get_latest_data(self):
        """获取最新一条数据"""
        if self.df is None or len(self.df) == 0:
            return None
        
        latest = self.df.sort_values('期号', ascending=False).iloc[0]
        reds = [latest[f'红{i}'] for i in range(1, 7)]
        
        return {
            'period': int(latest['期号']),
            'reds': reds,
            'blue': int(latest['蓝']),
            'raw_string': f"{''.join(f'{r:02d}' for r in reds)}+{latest['蓝']:02d}"
        }
    
    def predict(self, issue):
        """生成预测"""
        try:
            # 动态导入分析器
            from analyze_lottery import LotteryAnalyzer
            
            analyzer = LotteryAnalyzer('ssq')
            success, msg = analyzer.load_data(str(self.data_path))
            
            if not success:
                return {
                    'success': False,
                    'error': f'加载数据失败: {msg}'
                }
            
            analyzer.extract_numbers()
            recommendations = analyzer.generate_multiple_recommendations(6, include_dantuo=True)
            
            # 保存预测记录
            pred_file = self.predictions_dir / f"prediction_{issue}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(pred_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'issue': issue,
                    'timestamp': datetime.now().isoformat(),
                    'recommendations': recommendations
                }, f, ensure_ascii=False, indent=2)
            
            # 获取统计数据
            stats = analyzer.generate_statistics()
            missing = analyzer.analyze_missing()
            
            return {
                'success': True,
                'issue': issue,
                'recommendations': recommendations[:5],  # 返回5组
                'statistics': {
                    'hot_reds': stats['red']['hot_numbers'][:10],
                    'hot_blues': stats['blue']['hot_numbers'][:5],
                    'avg_sum': stats['sum']['avg']
                },
                'kill_numbers': analyzer.generate_kill_numbers(),
                'saved_to': str(pred_file)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def format_add_result(self, result):
        """格式化添加结果"""
        if not result['success']:
            if result.get('alert'):
                return f"""
{Colors.RED}{Colors.BOLD}【告警】{result['error']}{Colors.RESET}

请检查输入格式：期号 红球+蓝球
示例：双色球 2026041 020810171924+13
"""
            else:
                return f"{Colors.RED}失败: {result['error']}{Colors.RESET}"
        
        output = f"""
{Colors.GREEN}{Colors.BOLD}✅ 数据添加成功！{Colors.RESET}

📊 本期数据:
  期号: {result['period']}
  红球: {' '.join(f'{r:02d}' for r in result['reds'])}
  蓝球: {result['blue']:02d}
  字符串: {result['raw_string']}

📈 数据状态:
  总期数: {result['total_periods']}
  连续性: {'✅ 连续' if result['is_continuous'] else f'{Colors.RED}❌ 不连续，缺失 {len(result["missing_periods"])} 期{Colors.RESET}'}
"""

        # 显示最新数据
        latest = self.get_latest_data()
        if latest:
            output += f"""
📋 最新数据:
  期号: {latest['period']}
  红球: {' '.join(f'{r:02d}' for r in latest['reds'])}
  字符串: {latest['raw_string']}
"""
        
        return output
    
    def format_predict_result(self, result):
        """格式化预测结果"""
        if not result['success']:
            return f"{Colors.RED}预测失败: {result['error']}{Colors.RESET}"
        
        output = f"""
{Colors.GREEN}{Colors.BOLD}🎯 双色球预测结果 - {result['issue']}期{Colors.RESET}

{Colors.BOLD}📊 统计数据:{Colors.RESET}
  热红球: {result['statistics']['hot_reds']}
  热蓝球: {result['statistics']['hot_blues']}
  平均和值: {result['statistics']['avg_sum']:.1f}

{Colors.BOLD}🔪 杀号推荐:{Colors.RESET}
  杀红球: {result['kill_numbers']['kill_reds'][:8]}
  杀蓝球: {result['kill_numbers']['kill_blues'][:3]}

{Colors.BOLD}🎲 推荐方案:{Colors.RESET}
"""
        for i, rec in enumerate(result['recommendations'], 1):
            reds = rec.get('red_balls', [])
            blues = rec.get('blue_balls', [])
            strategy = rec.get('strategy_name', rec.get('strategy', ''))
            output += f"""
  {i}. {strategy}
     红球: {' '.join(f'{r:02d}' for r in reds)}
     蓝球: {' '.join(f'{b:02d}' for b in blues)}
"""
        
        output += f"""
{Colors.YELLOW}⚠️ 预测仅供娱乐参考，请理性购彩！{Colors.RESET}
"""
        return output
    
    def auto_detect_and_process(self, input_str):
        """自动检测输入类型并处理"""
        # 先尝试解析为添加数据
        add_data = self.parse_lottery_input(input_str)
        if add_data:
            result = self.add_data(add_data)
            return {
                'type': 'add',
                'output': self.format_add_result(result),
                'data': result
            }
        
        # 再尝试解析为预测请求
        predict_req = self.parse_predict_input(input_str)
        if predict_req:
            result = self.predict(predict_req['issue'])
            return {
                'type': 'predict',
                'output': self.format_predict_result(result),
                'data': result
            }
        
        return {
            'type': 'unknown',
            'output': f"""
{Colors.YELLOW}无法识别输入格式{Colors.RESET}

支持的命令:
  添加数据: 双色球 2026041 020810171924+13
  添加数据: 2026041 02 08 10 17 19 24 + 13
  预测分析: 预测 2026042期
  预测分析: 预测
""",
            'data': None
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='统一处理器 - 彩票数据更新与预测')
    parser.add_argument('--input', '-i', type=str, help='输入内容')
    parser.add_argument('--action', '-a', type=str, choices=['add', 'predict'], help='操作类型')
    parser.add_argument('--data', '-d', type=str, help='添加数据时的内容')
    parser.add_argument('--issue', '-iss', type=str, help='预测时的期号')
    parser.add_argument('--output', '-o', type=str, default='text', choices=['text', 'json'], help='输出格式')
    
    args = parser.parse_args()
    
    handler = UnifiedHandler()
    
    # 方式1：通过 --input 自动检测
    if args.input:
        result = handler.auto_detect_and_process(args.input)
        if args.output == 'json':
            print(json.dumps({
                'success': result['data'].get('success', False) if result['data'] else False,
                'type': result['type'],
                'data': result['data']
            }, ensure_ascii=False, indent=2))
        else:
            print(result['output'])
        return
    
    # 方式2：通过 --action 指定操作
    if args.action == 'add':
        if not args.data:
            print("请使用 --data 指定要添加的数据")
            sys.exit(1)
        add_data = handler.parse_lottery_input(args.data)
        if not add_data:
            print("数据格式错误")
            sys.exit(1)
        result = handler.add_data(add_data)
        if args.output == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(handler.format_add_result(result))
    
    elif args.action == 'predict':
        issue = args.issue
        if not issue:
            # 自动获取下一期
            latest = handler.get_latest_data()
            if latest:
                issue = str(latest['period'] + 1)
            else:
                issue = '2026001'
        result = handler.predict(issue)
        if args.output == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(handler.format_predict_result(result))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
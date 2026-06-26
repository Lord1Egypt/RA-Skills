#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 数据质量校验模块
升级新增：数据完整性校验、异常检测、质量报告
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DataQualityChecker:
    """数据质量检查器"""
    
    def __init__(self):
        self.quality_thresholds = {
            'min_days_required': 60,        # 最少需要的日线数据天数
            'max_missing_pct': 0.05,       # 最大允许的缺失值比例
            'price_jump_threshold': 0.15,   # 单日涨跌幅异常阈值（15%）
            'volume_zero_threshold': 3      # 连续0成交量天数阈值
        }
    
    def check_completeness(self, df, data_type='daily'):
        """
        检查数据完整性
        
        Args:
            df: 数据DataFrame
            data_type: 数据类型
        
        Returns:
            dict: 完整性检查结果
        """
        if df is None or len(df) == 0:
            return {
                'quality': 'CRITICAL',
                'score': 0,
                'issues': ['数据为空']
            }
        
        issues = []
        score = 100
        
        # 检查数据量
        min_days = self.quality_thresholds['min_days_required']
        if len(df) < min_days:
            issues.append(f'数据量不足: {len(df)}天 < {min_days}天')
            score -= 40
        
        # 检查缺失值
        missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        if missing_pct > self.quality_thresholds['max_missing_pct']:
            issues.append(f'缺失值比例过高: {missing_pct:.2%}')
            score -= missing_pct * 100 * 2
        
        # 检查必要列
        required_cols = ['close', 'volume'] if data_type == 'daily' else []
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            issues.append(f'缺少必要列: {missing_cols}')
            score -= 30
        
        quality = 'GOOD' if score >= 80 else 'ACCEPTABLE' if score >= 50 else 'CRITICAL'
        
        return {
            'quality': quality,
            'score': max(0, round(score, 1)),
            'issues': issues,
            'total_rows': len(df),
            'missing_pct': round(missing_pct * 100, 2)
        }
    
    def check_price_validity(self, df):
        """
        检查价格数据有效性
        
        Args:
            df: 日线DataFrame
        
        Returns:
            dict: 价格检查结果
        """
        if df is None or 'close' not in df.columns:
            return {'quality': 'CRITICAL', 'score': 0, 'issues': ['无价格数据']}
        
        issues = []
        score = 100
        
        prices = df['close']
        
        # 检查价格是否全相同
        if prices.nunique() == 1:
            issues.append('价格数据无变化（可能停牌）')
            score -= 50
        
        # 检查价格是否为0或负数
        if (prices <= 0).any():
            issues.append('存在非正价格数据')
            score -= 30
        
        # 检查单日涨跌幅异常
        pct_changes = prices.pct_change().dropna()
        if len(pct_changes) > 0:
            max_gain = pct_changes.max()
            max_loss = pct_changes.min()
            
            threshold = self.quality_thresholds['price_jump_threshold']
            if max_gain > threshold:
                issues.append(f'单日涨幅异常: {max_gain:.2%}')
                score -= 20
            if max_loss < -threshold:
                issues.append(f'单日跌幅异常: {max_loss:.2%}')
                score -= 20
        
        # 检查价格连续性（跳空超过10%）
        gaps = abs(prices.pct_change().dropna())
        gap_count = (gaps > 0.1).sum()
        if gap_count > 3:
            issues.append(f'价格跳空次数过多: {gap_count}次')
            score -= min(gap_count * 5, 20)
        
        quality = 'GOOD' if score >= 80 else 'ACCEPTABLE' if score >= 50 else 'CRITICAL'
        
        return {
            'quality': quality,
            'score': max(0, round(score, 1)),
            'issues': issues,
            'max_daily_gain': round(max_gain * 100, 2) if len(pct_changes) > 0 else 0,
            'max_daily_loss': round(max_loss * 100, 2) if len(pct_changes) > 0 else 0
        }
    
    def check_volume_validity(self, df):
        """
        检查成交量数据有效性
        
        Args:
            df: 日线DataFrame
        
        Returns:
            dict: 成交量检查结果
        """
        if df is None or 'volume' not in df.columns:
            return {'quality': 'CRITICAL', 'score': 0, 'issues': ['无成交量数据']}
        
        issues = []
        score = 100
        volume = df['volume']
        
        # 检查成交量为0的情况
        zero_vol_count = (volume == 0).sum()
        zero_vol_pct = zero_vol_count / len(volume)
        
        if zero_vol_pct > 0.5:
            issues.append(f'成交量为0的天数过多: {zero_vol_pct:.1%}')
            score -= 40
        elif zero_vol_pct > 0.2:
            issues.append(f'成交量为0的天数偏多: {zero_vol_pct:.1%}')
            score -= 20
        
        # 检查连续0成交量
        zero_streak_max = 0
        current_streak = 0
        for v in volume:
            if v == 0:
                current_streak += 1
                zero_streak_max = max(zero_streak_max, current_streak)
            else:
                current_streak = 0
        
        if zero_streak_max >= self.quality_thresholds['volume_zero_threshold']:
            issues.append(f'连续零成交量天数: {zero_streak_max}天')
            score -= 20
        
        # 检查成交量异常（极端值）
        if len(volume) > 20:
            vol_mean = volume.tail(20).mean()
            vol_std = volume.tail(20).std()
            if vol_mean > 0:
                vol_zscore = abs(volume.iloc[-1] - vol_mean) / vol_std if vol_std > 0 else 0
                if vol_zscore > 5:
                    issues.append(f'最新成交量异常(Z-Score={vol_zscore:.1f})')
                    score -= 10
        
        quality = 'GOOD' if score >= 80 else 'ACCEPTABLE' if score >= 50 else 'CRITICAL'
        
        return {
            'quality': quality,
            'score': max(0, round(score, 1)),
            'issues': issues,
            'zero_volume_count': int(zero_vol_count),
            'max_zero_streak': zero_streak_max
        }
    
    def check_single_stock(self, stock_data):
        """
        检查单只股票的数据质量
        
        Args:
            stock_data: 股票数据字典 {'code': '', 'name': '', 'daily': df}
        
        Returns:
            dict: 质量检查报告
        """
        code = stock_data.get('code', 'N/A')
        name = stock_data.get('name', 'N/A')
        df_daily = stock_data.get('daily')
        
        report = {
            'code': code,
            'name': name,
            'check_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_score': 0,
            'overall_quality': 'CRITICAL',
            'checks': {}
        }
        
        # 各项检查
        report['checks']['completeness'] = self.check_completeness(df_daily)
        report['checks']['price'] = self.check_price_validity(df_daily)
        report['checks']['volume'] = self.check_volume_validity(df_daily)
        
        # 计算综合得分
        all_scores = [v['score'] for v in report['checks'].values()]
        report['overall_score'] = round(np.mean(all_scores), 1)
        
        # 综合质量判断
        if all(v['quality'] == 'GOOD' for v in report['checks'].values()):
            report['overall_quality'] = 'GOOD'
        elif any(v['quality'] == 'CRITICAL' for v in report['checks'].values()):
            report['overall_quality'] = 'CRITICAL'
        else:
            report['overall_quality'] = 'ACCEPTABLE'
        
        return report
    
    def batch_check_all(self, all_stocks_data):
        """
        批量检查所有股票数据质量
        
        Args:
            all_stocks_data: 所有股票数据字典 {code: stock_data}
        
        Returns:
            dict: 整体数据质量报告
        """
        logger.info(f"开始检查 {len(all_stocks_data)} 只股票的数据质量...")
        
        all_reports = []
        quality_counts = {'GOOD': 0, 'ACCEPTABLE': 0, 'CRITICAL': 0}
        all_issues = []
        
        for code, stock_data in all_stocks_data.items():
            report = self.check_single_stock(stock_data)
            all_reports.append(report)
            quality_counts[report['overall_quality']] += 1
            
            # 收集问题
            for check_name, check_result in report['checks'].items():
                for issue in check_result.get('issues', []):
                    all_issues.append({
                        'code': code,
                        'name': stock_data.get('name', ''),
                        'check': check_name,
                        'issue': issue
                    })
        
        # 整体统计
        total = len(all_stocks_data)
        avg_score = np.mean([r['overall_score'] for r in all_reports])
        
        overall_report = {
            'total_stocks': total,
            'average_score': round(avg_score, 1),
            'quality_distribution': quality_counts,
            'quality_pct': {
                k: round(v / total * 100, 1) for k, v in quality_counts.items()
            },
            'critical_stocks': [r for r in all_reports if r['overall_quality'] == 'CRITICAL'],
            'all_issues': all_issues,
            'check_details': all_reports
        }
        
        logger.info(f"数据质量检查完成: 平均分{overall_report['average_score']}, "
                   f"优质{quality_counts['GOOD']}只, "
                   f"合格{quality_counts['ACCEPTABLE']}只, "
                   f"不合格{quality_counts['CRITICAL']}只")
        
        return overall_report
    
    def generate_quality_summary(self, quality_report):
        """
        生成数据质量摘要文本
        
        Args:
            quality_report: batch_check_all返回的报告
        
        Returns:
            str: 质量摘要文本
        """
        lines = []
        lines.append("## 📋 数据质量报告")
        lines.append("")
        lines.append(f"- **检查股票数量**: {quality_report['total_stocks']} 只")
        lines.append(f"- **数据质量平均分**: {quality_report['average_score']}/100")
        lines.append("")
        lines.append("### 质量分布")
        lines.append("")
        
        pct = quality_report['quality_pct']
        lines.append(f"- 🟢 优质数据: {quality_report['quality_distribution']['GOOD']} 只 ({pct.get('GOOD', 0)}%)")
        lines.append(f"- 🟡 合格数据: {quality_report['quality_distribution']['ACCEPTABLE']} 只 ({pct.get('ACCEPTABLE', 0)}%)")
        lines.append(f"- 🔴 不合格数据: {quality_report['quality_distribution']['CRITICAL']} 只 ({pct.get('CRITICAL', 0)}%)")
        lines.append("")
        
        # 列出主要问题
        if quality_report['all_issues']:
            lines.append("### 主要数据问题")
            lines.append("")
            issue_summary = {}
            for issue in quality_report['all_issues'][:20]:  # 只显示前20个
                issue_type = issue['issue']
                issue_summary[issue_type] = issue_summary.get(issue_type, 0) + 1
            
            for issue_type, count in issue_summary.items():
                lines.append(f"- {issue_type}: {count} 只股票")
            lines.append("")
        
        # 列出不合格的股票
        if quality_report['critical_stocks']:
            lines.append("### 数据不合格股票列表")
            lines.append("")
            for stock in quality_report['critical_stocks'][:10]:  # 只显示前10个
                lines.append(f"- {stock['name']}({stock['code']}): 得分{stock['overall_score']}")
            if len(quality_report['critical_stocks']) > 10:
                lines.append(f"- 还有 {len(quality_report['critical_stocks']) - 10} 只...")
            lines.append("")
        
        return "\n".join(lines)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    checker = DataQualityChecker()
    
    # 创建测试数据
    test_dates = pd.date_range('2024-01-01', periods=100, freq='D')
    test_prices = 10 + np.cumsum(np.random.randn(100) * 0.5)
    test_volumes = [1000000 + np.random.randint(-500000, 500000) for _ in range(100)]
    
    # 插入一些0值测试
    test_volumes[10:13] = [0, 0, 0]
    
    test_df = pd.DataFrame({
        'date': test_dates,
        'close': test_prices,
        'volume': test_volumes
    })
    
    test_stock = {
        'code': '600000',
        'name': '测试股票',
        'daily': test_df
    }
    
    # 测试单只股票检查
    report = checker.check_single_stock(test_stock)
    
    print("=" * 50)
    print("数据质量检查测试报告")
    print("=" * 50)
    print(f"股票: {report['name']}({report['code']})")
    print(f"综合得分: {report['overall_score']}/100")
    print(f"综合质量: {report['overall_quality']}")
    print("")
    
    for check_name, check_result in report['checks'].items():
        print(f"{check_name}: 得分{check_result['score']}, 质量{check_result['quality']}")
        if check_result['issues']:
            for issue in check_result['issues']:
                print(f"  - {issue}")
    
    print("=" * 50)

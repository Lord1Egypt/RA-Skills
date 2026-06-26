#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析模块
提供基本面分析、风险评估、申购建议等功能
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class StockAnalyzer:
    """新股分析器"""
    
    def __init__(self):
        self.industry_pe_benchmarks = {
            '计算机': 40.0,
            '电子': 35.0,
            '医药': 30.0,
            '机械': 25.0,
            '化工': 20.0,
            '汽车': 18.0,
            '建筑': 15.0,
            '银行': 6.0,
            '房地产': 10.0,
            '食品饮料': 30.0,
        }
    
    def analyze_stock(self, stock: Dict) -> Dict:
        """
        分析单只新股
        
        Args:
            stock: 新股数据
            
        Returns:
            分析结果
        """
        analysis = {
            'stock_info': {
                'code': stock.get('code'),
                'name': stock.get('name'),
                'apply_date': stock.get('apply_date'),
                'market': stock.get('market'),
            },
            'valuation_analysis': self._analyze_valuation(stock),
            'risk_assessment': self._assess_risk(stock),
            'subscription_advice': self._generate_advice(stock),
            'key_metrics': self._extract_key_metrics(stock),
            'analysis_time': datetime.now().isoformat(),
        }
        
        return analysis
    
    def analyze_multiple_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """
        分析多只新股
        
        Args:
            stocks: 新股列表
            
        Returns:
            分析结果列表
        """
        results = []
        for stock in stocks:
            try:
                analysis = self.analyze_stock(stock)
                results.append(analysis)
            except Exception as e:
                logger.error(f"分析股票 {stock.get('name')} 失败: {e}")
                continue
        
        # 按建议优先级排序
        results.sort(key=lambda x: self._get_priority_score(x['subscription_advice']), reverse=True)
        return results
    
    def _analyze_valuation(self, stock: Dict) -> Dict:
        """估值分析"""
        issue_price = stock.get('issue_price')
        issue_pe = stock.get('issue_pe')
        industry_pe = stock.get('industry_pe')
        
        analysis = {
            'issue_price': issue_price,
            'issue_pe': issue_pe,
            'industry_pe': industry_pe,
            'pe_ratio': None,
            'valuation_status': '未知',
            'description': '',
        }
        
        if issue_pe is not None and industry_pe is not None:
            try:
                issue_pe_float = float(issue_pe)
                industry_pe_float = float(industry_pe)
                
                if industry_pe_float > 0:
                    pe_ratio = issue_pe_float / industry_pe_float
                    analysis['pe_ratio'] = round(pe_ratio, 2)
                    
                    if pe_ratio < 0.8:
                        analysis['valuation_status'] = '低估'
                        analysis['description'] = f'发行市盈率({issue_pe_float})低于行业平均({industry_pe_float})，估值有优势'
                    elif pe_ratio < 1.0:
                        analysis['valuation_status'] = '合理'
                        analysis['description'] = f'发行市盈率({issue_pe_float})与行业平均({industry_pe_float})相当'
                    elif pe_ratio < 1.2:
                        analysis['valuation_status'] = '略高'
                        analysis['description'] = f'发行市盈率({issue_pe_float})略高于行业平均({industry_pe_float})'
                    else:
                        analysis['valuation_status'] = '偏高'
                        analysis['description'] = f'发行市盈率({issue_pe_float})显著高于行业平均({industry_pe_float})'
            except (ValueError, TypeError):
                pass
        
        return analysis
    
    def _assess_risk(self, stock: Dict) -> Dict:
        """风险评估"""
        risk_factors = []
        risk_level = '低'
        
        # 检查市盈率风险
        issue_pe = stock.get('issue_pe')
        industry_pe = stock.get('industry_pe')
        
        if issue_pe and industry_pe:
            try:
                if float(issue_pe) > float(industry_pe) * 1.2:
                    risk_factors.append('发行市盈率显著高于行业平均')
                    risk_level = '中'
            except (ValueError, TypeError):
                pass
        
        # 检查发行规模
        issue_num = stock.get('issue_num')
        if issue_num:
            try:
                if float(issue_num) > 10000:  # 发行超过1亿股
                    risk_factors.append('发行规模较大，可能影响上市表现')
            except (ValueError, TypeError):
                pass
        
        # 检查市场类型
        market = stock.get('market', '')
        if '创业板' in market or '科创板' in market:
            risk_factors.append(f'{market}新股波动性通常较大')
            risk_level = '中' if risk_level == '低' else risk_level
        
        # 检查保荐机构
        recommend_org = stock.get('recommend_org', '')
        top_underwriters = ['中信证券', '中信建投', '国泰君安', '华泰证券', '中金公司']
        if not any(org in recommend_org for org in top_underwriters):
            risk_factors.append('保荐机构非头部券商')
        
        return {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'description': f'共识别到{len(risk_factors)}个风险因素' if risk_factors else '未识别到明显风险因素'
        }
    
    def _generate_advice(self, stock: Dict) -> Dict:
        """生成申购建议"""
        # 基础建议
        advice = {
            'action': '观望',
            'confidence': '低',
            'reasons': [],
            'score': 50,  # 0-100分
        }
        
        score = 50
        
        # 估值因素（权重40%）
        valuation = self._analyze_valuation(stock)
        if valuation['valuation_status'] == '低估':
            advice['reasons'].append('估值有优势')
            score += 20
        elif valuation['valuation_status'] == '合理':
            advice['reasons'].append('估值合理')
            score += 10
        elif valuation['valuation_status'] == '偏高':
            advice['reasons'].append('估值偏高')
            score -= 10
        
        # 市场因素（权重30%）
        market = stock.get('market', '')
        if '主板' in market:
            advice['reasons'].append('主板新股相对稳健')
            score += 10
        elif '科创板' in market or '创业板' in market:
            advice['reasons'].append('科创板/创业板新股波动较大')
            score += 5
        
        # 发行规模因素（权重20%）
        issue_num = stock.get('issue_num')
        if issue_num:
            try:
                if float(issue_num) < 5000:  # 发行小于5000万股
                    advice['reasons'].append('发行规模适中')
                    score += 5
                elif float(issue_num) > 20000:  # 发行超过2亿股
                    advice['reasons'].append('发行规模较大')
                    score -= 5
            except (ValueError, TypeError):
                pass
        
        # 保荐机构因素（权重10%）
        recommend_org = stock.get('recommend_org', '')
        top_underwriters = ['中信证券', '中信建投', '国泰君安', '华泰证券', '中金公司']
        if any(org in recommend_org for org in top_underwriters):
            advice['reasons'].append('头部券商保荐')
            score += 5
        
        # 确定最终建议
        advice['score'] = max(0, min(100, score))
        
        if score >= 70:
            advice['action'] = '积极申购'
            advice['confidence'] = '高'
        elif score >= 60:
            advice['action'] = '建议申购'
            advice['confidence'] = '中'
        elif score >= 50:
            advice['action'] = '谨慎申购'
            advice['confidence'] = '低'
        else:
            advice['action'] = '观望'
            advice['confidence'] = '低'
        
        return advice
    
    def _extract_key_metrics(self, stock: Dict) -> Dict:
        """提取关键指标"""
        return {
            '申购代码': stock.get('apply_code', '未知'),
            '申购日期': stock.get('apply_date', '未知'),
            '发行价格': f"{stock.get('issue_price', '未知')}元",
            '申购上限': f"{stock.get('online_apply_upper', '未知')}股",
            '顶格申购市值': f"{stock.get('top_apply_marketcap', '未知')}万元",
            '发行数量': f"{stock.get('issue_num', '未知')}万股",
            '募集资金': f"{stock.get('total_raise_funds', '未知')}亿元",
            '保荐机构': stock.get('recommend_org', '未知'),
            '主营业务': stock.get('main_business', '未知')[:50] + '...' if stock.get('main_business') else '未知',
        }
    
    def _get_priority_score(self, advice: Dict) -> int:
        """获取建议优先级分数"""
        action_scores = {
            '积极申购': 100,
            '建议申购': 80,
            '谨慎申购': 60,
            '观望': 40,
        }
        return action_scores.get(advice.get('action', '观望'), 50)
    
    def generate_summary_report(self, analyses: List[Dict]) -> Dict:
        """生成汇总报告"""
        if not analyses:
            return {
                'total_stocks': 0,
                'summary': '今日无新股申购',
                'timestamp': datetime.now().isoformat(),
            }
        
        total = len(analyses)
        advice_counts = {
            '积极申购': 0,
            '建议申购': 0,
            '谨慎申购': 0,
            '观望': 0,
        }
        
        for analysis in analyses:
            action = analysis['subscription_advice']['action']
            if action in advice_counts:
                advice_counts[action] += 1
        
        # 生成摘要
        summary_parts = []
        if total > 0:
            summary_parts.append(f"今日共有 {total} 只新股可申购")
            
            for action, count in advice_counts.items():
                if count > 0:
                    summary_parts.append(f"{action}: {count}只")
        
        return {
            'total_stocks': total,
            'advice_distribution': advice_counts,
            'summary': '；'.join(summary_parts),
            'timestamp': datetime.now().isoformat(),
        }


# 单例实例
analyzer = StockAnalyzer()


if __name__ == "__main__":
    # 测试代码
    print("测试分析模块...")
    
    # 创建测试数据
    test_stock = {
        'code': '301682',
        'name': '测试股票',
        'apply_date': '2026-03-16',
        'issue_price': 69.66,
        'issue_pe': 33.61,
        'industry_pe': 65.16,
        'online_apply_upper': 8500,
        'top_apply_marketcap': 8.5,
        'market': '深交所创业板',
        'issue_num': 3038.73,
        'total_raise_funds': 21.17,
        'recommend_org': '申万宏源证券',
        'main_business': '测试主营业务描述',
    }
    
    analysis = analyzer.analyze_stock(test_stock)
    print(f"股票名称: {analysis['stock_info']['name']}")
    print(f"估值状态: {analysis['valuation_analysis']['valuation_status']}")
    print(f"申购建议: {analysis['subscription_advice']['action']}")
    print(f"建议信心: {analysis['subscription_advice']['confidence']}")
    print(f"风险等级: {analysis['risk_assessment']['risk_level']}")
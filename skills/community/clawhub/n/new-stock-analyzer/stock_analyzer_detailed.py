#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细版新股分析模块
提供详细的市场分类、时间信息和价格分析
"""

import logging
from typing import Dict, List, Optional
import statistics

logger = logging.getLogger(__name__)


class DetailedStockAnalyzer:
    """详细版新股分析器"""
    
    def __init__(self):
        # 市场风险系数
        self.market_risk_factors = {
            '沪市主板': 1.0,
            '深市主板': 1.0,
            '创业板': 1.3,
            '科创板': 1.5,
            '北交所': 1.2,
        }
    
    def analyze_stock_detailed(self, stock: Dict) -> Dict:
        """
        详细分析单只新股
        
        Args:
            stock: 详细新股数据
            
        Returns:
            详细分析结果
        """
        analysis = {
            'basic_info': self._extract_basic_info(stock),
            'market_info': self._analyze_market_info(stock),
            'time_info': self._analyze_time_info(stock),
            'price_info': self._analyze_price_info(stock),
            'valuation_analysis': self._analyze_valuation(stock),
            'risk_assessment': self._assess_risk(stock),
            'investment_advice': self._generate_advice(stock),
            'summary': '',
        }
        
        # 生成总结
        analysis['summary'] = self._generate_summary(analysis)
        
        return analysis
    
    def _extract_basic_info(self, stock: Dict) -> Dict:
        """提取基本信息"""
        return {
            'code': stock.get('code', '未知'),
            'name': stock.get('name', '未知'),
            'market': stock.get('market', '未知'),
            'market_category': stock.get('market_category', '未知'),
            'exchange': stock.get('exchange_name', '未知'),
            'industry': stock.get('industry', '未知'),
            'recommend_org': stock.get('recommend_org', '未知'),
        }
    
    def _analyze_market_info(self, stock: Dict) -> Dict:
        """分析市场信息"""
        market = stock.get('market', '')
        
        return {
            'market': market,
            'market_category': stock.get('market_category', '未知'),
            'exchange': stock.get('exchange_name', '未知'),
            'risk_level': self._get_market_risk_level(market),
            'description': self._get_market_description(market),
        }
    
    def _analyze_time_info(self, stock: Dict) -> Dict:
        """分析时间信息"""
        return {
            'apply_date': stock.get('apply_date_formatted', '待定'),
            'listing_date': stock.get('listing_date_formatted', '待定'),
            'status': stock.get('status', '未知'),
        }
    
    def _analyze_price_info(self, stock: Dict) -> Dict:
        """分析价格信息"""
        return {
            'issue_price': stock.get('issue_price_formatted', '待定'),
            'issue_pe': stock.get('issue_pe'),
            'industry_pe': stock.get('industry_pe'),
            'total_raise': stock.get('total_raise_formatted', '待定'),
            'issue_num': stock.get('issue_num_formatted', '待定'),
            'apply_upper': stock.get('apply_upper_formatted', '待定'),
        }
    
    def _analyze_valuation(self, stock: Dict) -> Dict:
        """估值分析"""
        analysis = {
            'pe_ratio': None,
            'price_level': '未知',
            'size_level': '未知',
            'valuation_score': 0,
            'valuation_status': '未知',
        }
        
        # PE分析
        issue_pe = self._safe_float(stock.get('issue_pe'))
        industry_pe = self._safe_float(stock.get('industry_pe'))
        
        if issue_pe and industry_pe and industry_pe > 0:
            pe_ratio = issue_pe / industry_pe
            analysis['pe_ratio'] = round(pe_ratio, 2)
            
            if pe_ratio < 0.8:
                analysis['valuation_score'] += 40
                analysis['valuation_status'] = '低估'
            elif pe_ratio < 1.0:
                analysis['valuation_score'] += 30
                analysis['valuation_status'] = '合理'
            elif pe_ratio < 1.2:
                analysis['valuation_score'] += 20
                analysis['valuation_status'] = '略高'
            else:
                analysis['valuation_score'] += 10
                analysis['valuation_status'] = '偏高'
        
        # 价格分析
        issue_price = self._safe_float(stock.get('issue_price'))
        if issue_price:
            if issue_price < 20:
                analysis['price_level'] = '低价'
                analysis['valuation_score'] += 15
            elif issue_price < 50:
                analysis['price_level'] = '中价'
                analysis['valuation_score'] += 10
            else:
                analysis['price_level'] = '高价'
                analysis['valuation_score'] += 5
        
        # 规模分析
        issue_num = self._safe_float(stock.get('issue_num'))
        if issue_num:
            if issue_num < 5000:
                analysis['size_level'] = '小型'
                analysis['valuation_score'] += 15
            elif issue_num < 20000:
                analysis['size_level'] = '中型'
                analysis['valuation_score'] += 10
            else:
                analysis['size_level'] = '大型'
                analysis['valuation_score'] += 5
        
        return analysis
    
    def _assess_risk(self, stock: Dict) -> Dict:
        """风险评估"""
        risk_factors = []
        
        # 市场风险
        market = stock.get('market', '')
        if '科创' in market or '创业' in market:
            risk_factors.append(f'{market}波动性较大')
        
        # 价格风险
        issue_price = self._safe_float(stock.get('issue_price'))
        if issue_price and issue_price > 100:
            risk_factors.append('发行价格过高')
        
        # 规模风险
        issue_num = self._safe_float(stock.get('issue_num'))
        if issue_num and issue_num > 20000:
            risk_factors.append('发行规模过大')
        
        # 确定风险等级
        risk_count = len(risk_factors)
        
        if risk_count >= 3:
            risk_level = '高'
            risk_score = 20
        elif risk_count >= 2:
            risk_level = '中高'
            risk_score = 40
        elif risk_count >= 1:
            risk_level = '中'
            risk_score = 60
        else:
            risk_level = '低'
            risk_score = 100
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'description': f'识别到{risk_count}个风险因素',
        }
    
    def _generate_advice(self, stock: Dict) -> Dict:
        """生成投资建议"""
        # 获取各维度评分
        valuation_score = self._analyze_valuation(stock)['valuation_score']
        
        # 市场评分
        market = stock.get('market', '')
        market_risk = self.market_risk_factors.get(market, 1.0)
        market_score = 100 if market_risk <= 1.0 else 80 if market_risk <= 1.3 else 60
        
        # 风险评分
        risk_score = self._assess_risk(stock)['risk_score']
        
        # 综合评分
        total_score = (valuation_score * 0.4 + market_score * 0.3 + risk_score * 0.3)
        
        # 生成建议
        if total_score >= 80:
            action = '积极申购'
            confidence = '高'
            reasons = ['综合评分优秀']
        elif total_score >= 65:
            action = '建议申购'
            confidence = '中高'
            reasons = ['综合评分良好']
        elif total_score >= 50:
            action = '谨慎申购'
            confidence = '中'
            reasons = ['综合评分一般']
        elif total_score >= 35:
            action = '观望'
            confidence = '中低'
            reasons = ['综合评分较低']
        else:
            action = '回避'
            confidence = '低'
            reasons = ['综合评分差']
        
        # 添加具体理由
        valuation_status = self._analyze_valuation(stock)['valuation_status']
        if valuation_status == '低估':
            reasons.append('估值有优势')
        elif valuation_status == '偏高':
            reasons.append('估值偏高')
        
        risk_level = self._assess_risk(stock)['risk_level']
        if risk_level in ['低', '中低']:
            reasons.append('风险可控')
        elif risk_level in ['中高', '高']:
            reasons.append('风险较高')
        
        return {
            'action': action,
            'confidence': confidence,
            'total_score': round(total_score, 1),
            'reasons': reasons,
            'position_suggestion': self._get_position_suggestion(total_score),
        }
    
    def _generate_summary(self, analysis: Dict) -> str:
        """生成总结"""
        basic = analysis['basic_info']
        market = analysis['market_info']
        time_info = analysis['time_info']
        price = analysis['price_info']
        valuation = analysis['valuation_analysis']
        risk = analysis['risk_assessment']
        advice = analysis['investment_advice']
        
        lines = [
            f"📈 {basic['name']}({basic['code']})",
            f"🏢 市场: {market['market']} | 分类: {market['market_category']}",
            f"📅 申购: {time_info['apply_date']} | 上市: {time_info['listing_date']}",
            f"💰 价格: {price['issue_price']} | PE: {price['issue_pe']}",
            f"📊 规模: {price['issue_num']} | 募集: {price['total_raise']}",
            f"⚖️ 估值: {valuation['valuation_status']}",
            f"⚠️ 风险: {risk['risk_level']}",
            f"🎯 建议: {advice['action']} ({advice['total_score']}/100)",
        ]
        
        return "\n".join(lines)
    
    # ========== 辅助方法 ==========
    
    def _safe_float(self, value) -> Optional[float]:
        """安全转换为浮点数"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _get_market_risk_level(self, market: str) -> str:
        """获取市场风险等级"""
        if '主板' in market:
            return '低'
        elif '创业' in market:
            return '中'
        elif '科创' in market:
            return '高'
        elif '北交' in market:
            return '中'
        else:
            return '中'
    
    def _get_market_description(self, market: str) -> str:
        """获取市场描述"""
        if '主板' in market:
            return '相对稳健'
        elif '创业' in market:
            return '成长性较高'
        elif '科创' in market:
            return '高风险高收益'
        elif '北交' in market:
            return '中小企业'
        else:
            return '需谨慎评估'
    
    def _get_position_suggestion(self, score: float) -> str:
        """获取仓位建议"""
        if score >= 80:
            return "建议60-80%仓位"
        elif score >= 65:
            return "建议40-60%仓位"
        elif score >= 50:
            return "建议20-40%仓位"
        elif score >= 35:
            return "建议10-20%仓位"
        else:
            return "建议0-10%仓位"
    
    def analyze_multiple_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """分析多只新股"""
        results = []
        for stock in stocks:
            try:
                analysis = self.analyze_stock_detailed(stock)
                results.append(analysis)
            except Exception as e:
                logger.error(f"分析失败: {stock.get('name')}, 错误: {e}")
                results.append({'error': str(e)})
        
        # 按综合评分排序
        results.sort(key=lambda x: x.get('investment_advice', {}).get('total_score', 0), reverse=True)
        return results
    
    def generate_detailed_report(self, stocks: List[Dict]) -> str:
        """生成详细报告"""
        analyses = self.analyze_multiple_stocks(stocks)
        
        if not analyses:
            return "无新股数据可供分析"
        
        from datetime import datetime
        lines = [
            "📊 新股详细分析报告",
            "=" * 50,
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"数量: {len(analyses)}只新股",
            "",
        ]
        
        # 汇总统计
        good_count = sum(1 for a in analyses if a.get('investment_advice', {}).get('total_score', 0) >= 65)
        avg_score = statistics.mean([a.get('investment_advice', {}).get('total_score', 0) for a in analyses if 'investment_advice' in a])
        
        lines.extend([
            "📈 汇总统计",
            f"- 新股总数: {len(analyses)}只",
            f"- 建议申购: {good_count}只",
            f"- 平均评分: {avg_score:.1f}/100",
            "",
        ])
        
        # 详细分析
        lines.append("📋 详细分析")
        lines.append("-" * 40)
        
        for i, analysis in enumerate(analyses, 1):
            if 'error' in analysis:
                lines.append(f"{i}. 分析失败: {analysis['error']}")
            else:
                basic = analysis['basic_info']
                time_info = analysis['time_info']
                price = analysis['price_info']
                advice = analysis['investment_advice']
                
                lines.append(f"{i}. {basic['name']}({basic['code']})")
                lines.append(f"   市场: {basic['market']} | 申购: {time_info['apply_date']}")
                lines.append(f"   价格: {price['issue_price']} | 规模: {price['issue_num']}")
                lines.append(f"   建议: {advice['action']} ({advice['total_score']}/100)")
            
            lines.append("")
        
        # 投资建议
        lines.append("🎯 投资建议")
        lines.append("-" * 40)
        
        if good_count >= len(analyses) * 0.7:
            lines.append("✅ 市场环境良好，多数新股可申购")
        elif good_count >= len(analyses) * 0.5:
            lines.append("⚠️ 市场环境一般，需精选个股")
        else:
            lines.append("❌ 市场环境较差，建议谨慎")
        
        lines.append("")
        lines.append("⚠️ 风险提示: 投资有风险，申购需谨慎")
        
        return "\n".join(lines)


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("详细版新股分析器测试")
    print("=" * 60)
    
    try:
        # 导入数据获取器
        from stock_data_enhanced import EnhancedStockDataFetcher
        
        print("\n1. 获取今日详细新股数据...")
        fetcher = EnhancedStockDataFetcher()
        stocks = fetcher.get_today_detailed_stocks()
        
        if not stocks:
            print("❌ 未获取到新股数据")
        else:
            print(f"✅ 获取到 {len(stocks)} 只新股")
            
            print("\n2. 创建详细版分析器...")
            analyzer = DetailedStockAnalyzer()
            
            print("\n3. 分析单只股票...")
            if stocks:
                analysis = analyzer.analyze_stock_detailed(stocks[0])
                print(analysis['summary'])
            
            print("\n4. 生成详细报告...")
            report = analyzer.generate_detailed_report(stocks)
            print(report)
        
        print("\n" + "=" * 60)
        print("✅ 详细版分析器测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
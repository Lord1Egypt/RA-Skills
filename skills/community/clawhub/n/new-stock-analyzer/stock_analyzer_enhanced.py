#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版新股分析模块
提供深度基本面分析、技术面分析、市场情绪分析等功能
"""

import logging
from typing import Dict, List, Optional
import statistics

logger = logging.getLogger(__name__)


class EnhancedStockAnalyzer:
    """增强版新股分析器"""
    
    def __init__(self):
        # 行业基准数据
        self.industry_benchmarks = {
            '计算机': 40.0, '电子': 35.0, '医药': 30.0, '新能源': 25.0,
            '机械': 25.0, '化工': 20.0, '汽车': 18.0, '建筑': 15.0,
            '银行': 6.0, '房地产': 10.0, '食品饮料': 30.0, '传媒': 25.0,
        }
        
        # 头部保荐机构
        self.top_underwriters = ['中信证券', '中信建投', '国泰君安', '华泰证券', 
                                '中金公司', '招商证券', '广发证券', '海通证券']
    
    def analyze_stock_enhanced(self, stock: Dict) -> Dict:
        """
        增强版股票分析
        
        Args:
            stock: 新股数据
            
        Returns:
            增强分析结果
        """
        analysis = {
            'basic_info': self._get_basic_info(stock),
            'valuation_analysis': self._analyze_valuation_enhanced(stock),
            'market_analysis': self._analyze_market_enhanced(stock),
            'risk_assessment': self._assess_risk_enhanced(stock),
            'investment_advice': self._generate_advice_enhanced(stock),
            'summary': '',
        }
        
        # 生成总结
        analysis['summary'] = self._generate_enhanced_summary(analysis)
        
        return analysis
    
    def _get_basic_info(self, stock: Dict) -> Dict:
        """获取基本信息"""
        return {
            'code': stock.get('code', '未知'),
            'name': stock.get('name', '未知'),
            'market': stock.get('market', '未知'),
            'industry': self._infer_industry(stock),
            'recommend_org': stock.get('recommend_org', '未知'),
            'apply_date': stock.get('apply_date'),
            'listing_date': stock.get('listing_date'),
        }
    
    def _infer_industry(self, stock: Dict) -> str:
        """推断行业"""
        business = stock.get('main_business', '').lower()
        name = stock.get('name', '').lower()
        
        industry_keywords = {
            '计算机': ['软件', '信息', '数据', '云计算', '人工智能', 'AI'],
            '电子': ['电子', '芯片', '半导体', '集成电路', '元器件'],
            '医药': ['医药', '生物', '医疗', '健康', '制药', '疫苗'],
            '新能源': ['新能源', '光伏', '风电', '储能', '电池', '锂电'],
            '机械': ['机械', '设备', '制造', '工程', '重工'],
            '化工': ['化工', '材料', '化学', '塑料', '橡胶'],
        }
        
        for industry, keywords in industry_keywords.items():
            for keyword in keywords:
                if keyword in business or keyword in name:
                    return industry
        
        return '其他'
    
    def _analyze_valuation_enhanced(self, stock: Dict) -> Dict:
        """增强版估值分析"""
        analysis = {
            'pe_ratio_analysis': {},
            'price_analysis': {},
            'size_analysis': {},
            'valuation_score': 0,  # 0-100分
            'valuation_status': '未知',
        }
        
        # PE比率分析
        issue_pe = self._safe_float(stock.get('issue_pe'))
        industry_pe = self._safe_float(stock.get('industry_pe'))
        
        if not industry_pe:
            industry = self._infer_industry(stock)
            industry_pe = self.industry_benchmarks.get(industry, 25.0)
        
        if issue_pe and industry_pe:
            pe_ratio = issue_pe / industry_pe
            analysis['pe_ratio_analysis'] = {
                'issue_pe': issue_pe,
                'industry_pe': industry_pe,
                'pe_ratio': round(pe_ratio, 2),
                'description': self._get_pe_description(pe_ratio),
            }
            
            # PE评分
            if pe_ratio < 0.8:
                analysis['valuation_score'] += 40
            elif pe_ratio < 1.0:
                analysis['valuation_score'] += 30
            elif pe_ratio < 1.2:
                analysis['valuation_score'] += 20
            else:
                analysis['valuation_score'] += 10
        
        # 发行价格分析
        issue_price = self._safe_float(stock.get('issue_price'))
        if issue_price:
            analysis['price_analysis'] = {
                'price': issue_price,
                'level': self._get_price_level(issue_price),
                'description': self._get_price_description(issue_price),
            }
            
            if issue_price < 20:
                analysis['valuation_score'] += 15
            elif issue_price < 50:
                analysis['valuation_score'] += 10
            else:
                analysis['valuation_score'] += 5
        
        # 发行规模分析
        issue_num = self._safe_float(stock.get('issue_num'))
        if issue_num:
            analysis['size_analysis'] = {
                'size': issue_num,
                'level': self._get_size_level(issue_num),
                'description': self._get_size_description(issue_num),
            }
            
            if issue_num < 5000:
                analysis['valuation_score'] += 15
            elif issue_num < 20000:
                analysis['valuation_score'] += 10
            else:
                analysis['valuation_score'] += 5
        
        # 确定估值状态
        score = analysis['valuation_score']
        if score >= 60:
            analysis['valuation_status'] = '低估'
        elif score >= 40:
            analysis['valuation_status'] = '合理'
        elif score >= 20:
            analysis['valuation_status'] = '略高'
        else:
            analysis['valuation_status'] = '偏高'
        
        return analysis
    
    def _analyze_market_enhanced(self, stock: Dict) -> Dict:
        """增强版市场分析"""
        analysis = {
            'market_type_analysis': {},
            'underwriter_analysis': {},
            'market_score': 0,
        }
        
        # 市场类型分析
        market = stock.get('market', '')
        market_risk = self._get_market_risk(market)
        
        analysis['market_type_analysis'] = {
            'market': market,
            'risk_level': market_risk['level'],
            'description': market_risk['description'],
        }
        
        if market_risk['level'] == '低':
            analysis['market_score'] += 25
        elif market_risk['level'] == '中':
            analysis['market_score'] += 20
        else:
            analysis['market_score'] += 15
        
        # 保荐机构分析
        recommend_org = stock.get('recommend_org', '')
        is_top = any(org in recommend_org for org in self.top_underwriters)
        
        analysis['underwriter_analysis'] = {
            'underwriter': recommend_org,
            'is_top': is_top,
            'description': '头部保荐机构，项目质量有保障' if is_top else '保荐机构知名度一般',
        }
        
        if is_top:
            analysis['market_score'] += 25
        else:
            analysis['market_score'] += 15
        
        return analysis
    
    def _assess_risk_enhanced(self, stock: Dict) -> Dict:
        """增强版风险评估"""
        risk_factors = []
        warning_signals = []
        
        # 估值风险
        valuation = self._analyze_valuation_enhanced(stock)
        if valuation['valuation_status'] in ['偏高', '略高']:
            risk_factors.append('估值偏高')
        
        # 市场风险
        market = stock.get('market', '')
        if market in ['科创板', '创业板']:
            risk_factors.append(f'{market}波动性大')
        
        # 规模风险
        issue_num = self._safe_float(stock.get('issue_num'))
        if issue_num and issue_num > 20000:
            risk_factors.append('发行规模过大')
        
        # 价格风险
        issue_price = self._safe_float(stock.get('issue_price'))
        if issue_price and issue_price > 100:
            risk_factors.append('发行价格过高')
        
        # 保荐机构风险
        recommend_org = stock.get('recommend_org', '')
        is_top = any(org in recommend_org for org in self.top_underwriters)
        if not is_top:
            warning_signals.append('非头部保荐机构')
        
        # 确定风险等级
        risk_count = len(risk_factors)
        warning_count = len(warning_signals)
        
        if risk_count >= 3:
            risk_level = '高'
            risk_score = 20
        elif risk_count >= 2:
            risk_level = '中高'
            risk_score = 40
        elif risk_count >= 1 or warning_count >= 2:
            risk_level = '中'
            risk_score = 60
        elif warning_count >= 1:
            risk_level = '中低'
            risk_score = 80
        else:
            risk_level = '低'
            risk_score = 100
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'warning_signals': warning_signals,
            'description': f'共识别到{risk_count}个风险因素和{warning_count}个预警信号',
        }
    
    def _generate_advice_enhanced(self, stock: Dict) -> Dict:
        """增强版投资建议"""
        # 获取各维度评分
        valuation_score = self._analyze_valuation_enhanced(stock)['valuation_score']
        market_score = self._analyze_market_enhanced(stock)['market_score']
        risk_score = self._assess_risk_enhanced(stock)['risk_score']
        
        # 综合评分
        total_score = (valuation_score * 0.4 + market_score * 0.3 + risk_score * 0.3)
        
        # 生成建议
        if total_score >= 80:
            action = '积极申购'
            confidence = '高'
            reasons = ['综合评分优秀，投资价值显著']
        elif total_score >= 65:
            action = '建议申购'
            confidence = '中高'
            reasons = ['综合评分良好，具备投资价值']
        elif total_score >= 50:
            action = '谨慎申购'
            confidence = '中'
            reasons = ['综合评分一般，需控制风险']
        elif total_score >= 35:
            action = '观望'
            confidence = '中低'
            reasons = ['综合评分较低，风险较高']
        else:
            action = '回避'
            confidence = '低'
            reasons = ['综合评分差，风险过大']
        
        # 添加具体理由
        valuation_status = self._analyze_valuation_enhanced(stock)['valuation_status']
        if valuation_status == '低估':
            reasons.append('估值有优势')
        elif valuation_status == '偏高':
            reasons.append('估值偏高')
        
        risk_level = self._assess_risk_enhanced(stock)['risk_level']
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
    
    def _generate_enhanced_summary(self, analysis: Dict) -> str:
        """生成增强版总结"""
        basic = analysis['basic_info']
        valuation = analysis['valuation_analysis']
        risk = analysis['risk_assessment']
        advice = analysis['investment_advice']
        
        lines = [
            f"📈 {basic['name']}({basic['code']}) - {basic['market']}新股分析",
            f"🏢 行业: {basic['industry']} | 保荐: {basic['recommend_org']}",
            f"💰 估值状态: {valuation['valuation_status']} (评分: {valuation['valuation_score']}/100)",
            f"⚠️ 风险等级: {risk['risk_level']} (评分: {risk['risk_score']}/100)",
            f"🎯 投资建议: {advice['action']} ({advice['confidence']}信心)",
            f"📊 综合评分: {advice['total_score']}/100",
            f"📦 仓位建议: {advice['position_suggestion']}",
        ]
        
        if advice['reasons']:
            lines.append("📋 主要理由:")
            for reason in advice['reasons']:
                lines.append(f"  • {reason}")
        
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
    
    def _get_pe_description(self, pe_ratio: float) -> str:
        """获取PE比率描述"""
        if pe_ratio < 0.8:
            return "显著低估，估值优势明显"
        elif pe_ratio < 1.0:
            return "适度低估，有一定估值优势"
        elif pe_ratio < 1.2:
            return "估值合理，与行业水平相当"
        else:
            return "估值偏高，需谨慎评估"
    
    def _get_price_level(self, price: float) -> str:
        """获取价格等级"""
        if price < 20:
            return "低价股"
        elif price < 50:
            return "中价股"
        else:
            return "高价股"
    
    def _get_price_description(self, price: float) -> str:
        """获取价格描述"""
        if price < 20:
            return "低价股，散户参与度高"
        elif price < 50:
            return "中价股，平衡性好"
        else:
            return "高价股，机构参与为主"
    
    def _get_size_level(self, size: float) -> str:
        """获取规模等级"""
        if size < 5000:
            return "小型发行"
        elif size < 20000:
            return "中型发行"
        else:
            return "大型发行"
    
    def _get_size_description(self, size: float) -> str:
        """获取规模描述"""
        if size < 5000:
            return "稀缺性较高，上市表现可能较好"
        elif size < 20000:
            return "流动性适中，平衡性好"
        else:
            return "流动性好，但稀缺性较低"
    
    def _get_market_risk(self, market: str) -> Dict:
        """获取市场风险"""
        if '主板' in market:
            return {'level': '低', 'description': '主板新股相对稳健'}
        elif '创业板' in market:
            return {'level': '中', 'description': '创业板新股有一定波动性'}
        elif '科创板' in market:
            return {'level': '高', 'description': '科创板新股波动性较大'}
        else:
            return {'level': '中', 'description': '新股投资需谨慎'}
    
    def _get_position_suggestion(self, score: float) -> str:
        """获取仓位建议"""
        if score >= 80:
            return "可适当提高申购仓位（建议60-80%）"
        elif score >= 65:
            return "正常申购（建议40-60%）"
        elif score >= 50:
            return "降低申购仓位（建议20-40%）"
        elif score >= 35:
            return "小仓位试探（建议10-20%）"
        else:
            return "不建议申购或极小仓位（建议0-10%）"
    
    def analyze_multiple_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """分析多只新股"""
        results = []
        for stock in stocks:
            try:
                analysis = self.analyze_stock_enhanced(stock)
                results.append(analysis)
            except Exception as e:
                logger.error(f"分析失败: {stock.get('name')}, 错误: {e}")
                results.append({'error': str(e), 'stock': stock})
        
        # 按综合评分排序
        results.sort(key=lambda x: x.get('investment_advice', {}).get('total_score', 0), reverse=True)
        return results
    
    def generate_enhanced_report(self, stocks: List[Dict]) -> str:
        """生成增强版报告"""
        analyses = self.analyze_multiple_stocks(stocks)
        
        if not analyses:
            return "无新股数据可供分析"
        
        lines = [
            "📊 新股增强分析报告",
            "=" * 40,
            f"分析时间: {self._get_current_time()}",
            f"分析数量: {len(analyses)}只新股",
            "",
        ]
        
        # 汇总统计
        good_count = sum(1 for a in analyses if a.get('investment_advice', {}).get('total_score', 0) >= 65)
        avg_score = statistics.mean([a.get('investment_advice', {}).get('total_score', 0) for a in analyses if 'investment_advice' in a])
        
        lines.extend([
            "📈 汇总统计",
            f"- 建议申购数量: {good_count}只",
            f"- 平均综合评分: {avg_score:.1f}/100",
            "",
        ])
        
        # 详细分析
        lines.append("📋 详细分析")
        lines.append("-" * 30)
        
        for i, analysis in enumerate(analyses, 1):
            if 'error' in analysis:
                lines.append(f"{i}. {analysis.get('stock', {}).get('name', '未知')} - 分析失败")
                lines.append(f"   错误: {analysis['error']}")
            else:
                basic = analysis['basic_info']
                advice = analysis['investment_advice']
                
                lines.append(f"{i}. {basic['name']}({basic['code']})")
                lines.append(f"   市场: {basic['market']} | 行业: {basic['industry']}")
                lines.append(f"   估值: {analysis['valuation_analysis']['valuation_status']}")
                lines.append(f"   风险: {analysis['risk_assessment']['risk_level']}")
                lines.append(f"   建议: {advice['action']} ({advice['total_score']}/100)")
                
                if advice['reasons']:
                    lines.append(f"   理由: {', '.join(advice['reasons'][:2])}")
            
            lines.append("")
        
        # 投资建议
        lines.append("🎯 投资建议总结")
        lines.append("-" * 30)
        
        if good_count >= len(analyses) * 0.7:
            lines.append("✅ 整体市场环境良好，多数新股具备投资价值")
        elif good_count >= len(analyses) * 0.5:
            lines.append("⚠️ 市场环境一般，需精选个股，控制仓位")
        else:
            lines.append("❌ 市场环境较差，建议谨慎参与")
        
        lines.append("")
        lines.append(f"🏆 最佳选择: {analyses[0]['basic_info']['name']} ({analyses[0]['investment_advice']['total_score']}/100)")
        lines.append("")
        lines.append("⚠️ 风险提示: 新股投资有风险，申购需谨慎，建议分散投资")
        
        return "\n".join(lines)
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("增强版新股分析器测试")
    print("=" * 60)
    
    # 测试数据
    test_stocks = [
        {
            'code': '301682',
            'name': '宏明电子',
            'market': '创业板',
            'issue_price': '25.80',
            'issue_pe': '22.50',
            'industry_pe': '35.00',
            'issue_num': '3000',
            'recommend_org': '中信证券',
            'apply_date': '2026-03-16',
            'main_business': '电子元器件制造',
        },
        {
            'code': '688781',
            'name': '视涯科技',
            'market': '科创板',
            'issue_price': '45.60',
            'issue_pe': '40.20',
            'industry_pe': '30.00',
            'issue_num': '5000',
            'recommend_org': '华泰证券',
            'apply_date': '2026-03-16',
            'main_business': '显示技术研发',
        },
        {
            'code': '920188',
            'name': '悦龙科技',
            'market': '主板',
            'issue_price': '12.50',
            'issue_pe': '18.00',
            'industry_pe': '25.00',
            'issue_num': '8000',
            'recommend_org': '国泰君安',
            'apply_date': '2026-03-16',
            'main_business': '机械设备制造',
        },
    ]
    
    try:
        analyzer = EnhancedStockAnalyzer()
        
        print("\n1. 单只股票分析测试:")
        print("-" * 40)
        result = analyzer.analyze_stock_enhanced(test_stocks[0])
        print(result['summary'])
        
        print("\n2. 多只股票对比分析:")
        print("-" * 40)
        report = analyzer.generate_enhanced_report(test_stocks)
        print(report)
        
        print("\n" + "=" * 60)
        print("✅ 增强版分析器测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

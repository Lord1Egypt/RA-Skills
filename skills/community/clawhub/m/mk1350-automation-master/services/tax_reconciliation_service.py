# file: tax_reconciliation_service_修正版.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
import os
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class TaxReconciliationService:
    """税务对账服务类 - 修正版"""
    
    # 预设配置 - 调整参数以启用多对多匹配
    PRESET_CONFIGS = {
        'standard': {
            'match_precision_mode': 'standard',
            'exact_match_threshold': 0.001,
            'approx_match_threshold_percent': 1.0,
            'many_to_many_amount_threshold': 500,  # 降低阈值以启用多对多
            'many_to_many_percent_threshold': 0.5,  # 降低百分比阈值
            'max_combination_depth': 3,
            'max_candidates_per_stage': 20,
            'search_algorithm': 'dynamic',
            'max_recursion_times': 2,
            'enable_many_to_many': True,  # 启用多对多匹配
            'enable_recursive_match': True,
            'final_match_amount_threshold': 50,  # 最终匹配阈值
            'final_match_percent_threshold': 0.05  # 最终匹配百分比阈值
        },
        'precise': {
            'match_precision_mode': 'precise',
            'exact_match_threshold': 0.0001,
            'approx_match_threshold_percent': 0.5,
            'many_to_many_amount_threshold': 300,  # 更低阈值
            'many_to_many_percent_threshold': 0.3,
            'max_combination_depth': 4,
            'max_candidates_per_stage': 25,
            'search_algorithm': 'dynamic',
            'max_recursion_times': 2,
            'enable_many_to_many': True,
            'enable_recursive_match': True,
            'final_match_amount_threshold': 30,
            'final_match_percent_threshold': 0.03
        },
        'fast': {
            'match_precision_mode': 'fast',
            'exact_match_threshold': 0.01,
            'approx_match_threshold_percent': 2.0,
            'many_to_many_amount_threshold': 800,  # 适当降低
            'many_to_many_percent_threshold': 1.0,
            'max_combination_depth': 2,
            'max_candidates_per_stage': 15,
            'search_algorithm': 'backtrack',
            'max_recursion_times': 1,
            'enable_many_to_many': True,  # 启用多对多
            'enable_recursive_match': False,
            'final_match_amount_threshold': 100,
            'final_match_percent_threshold': 0.1
        }
    }
    
    def __init__(self):
        """初始化税务对账服务"""
        self.phase_params = {
            'primary': {
                'max_depth': 3,
                'max_candidates': 20,
                'scale_factor': 100,
                'max_states': 50000,
                'search_method': 'dp'
            },
            'secondary': {
                'max_depth': 3,
                'max_candidates': 15,
                'scale_factor': 10,
                'max_states': 20000,
                'search_method': 'hybrid'
            },
            'recursive': {
                'max_recursions': 2,
                'max_depth': 2,
                'max_candidates': 10
            }
        }
    
    def _load_data(self, tax_file: str, sap_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """加载数据文件"""
        try:
            # 读取Excel文件
            tax_df = pd.read_excel(tax_file)
            sap_df = pd.read_excel(sap_file)
            
            # 验证必要列
            required_columns = ['税额', '税率']
            for col in required_columns:
                if col not in tax_df.columns:
                    raise ValueError(f'税局文件缺少必要列: {col}')
                if col not in sap_df.columns:
                    raise ValueError(f'SAP文件缺少必要列: {col}')
            
            # 添加唯一ID
            tax_df['ID'] = [f'税局_{i:04d}' for i in range(len(tax_df))]
            sap_df['ID'] = [f'SAP_{i:04d}' for i in range(len(sap_df))]
            
            # 数据类型转换
            tax_df['税额'] = tax_df['税额'].astype(float)
            tax_df['税率'] = tax_df['税率'].astype(str).str.strip()
            sap_df['税额'] = sap_df['税额'].astype(float)
            sap_df['税率'] = sap_df['税率'].astype(str).str.strip()
            
            # 数据完整性检查
            self._validate_data_integrity(tax_df, sap_df)
            
            return tax_df, sap_df
            
        except Exception as e:
            logger.error(f"数据加载失败: {str(e)}")
            raise
    
    def _validate_data_integrity(self, tax_df: pd.DataFrame, sap_df: pd.DataFrame):
        """验证数据完整性"""
        tax_total = tax_df['税额'].sum()
        sap_total = sap_df['税额'].sum()
        
        logger.info(f"数据完整性检查:")
        logger.info(f"税局数据: {len(tax_df)}行，总额: {tax_total:,.2f}元")
        logger.info(f"SAP数据: {len(sap_df)}行，总额: {sap_total:,.2f}元")
        logger.info(f"总差异: {(tax_total - sap_total):,.2f}元")
        
        # 检查异常值
        tax_negative = tax_df[tax_df['税额'] < 0]
        sap_negative = sap_df[sap_df['税额'] < 0]
        
        if len(tax_negative) > 0:
            logger.warning(f"税局数据中有{len(tax_negative)}行负税额")
        if len(sap_negative) > 0:
            logger.warning(f"SAP数据中有{len(sap_negative)}行负税额")
    
    def _apply_parameters(self, base_params: Dict[str, Any], preset_key: str = None) -> Dict[str, Any]:
        """应用参数配置"""
        if preset_key and preset_key in self.PRESET_CONFIGS:
            preset = self.PRESET_CONFIGS[preset_key]
            # 合并预设参数
            for key, value in preset.items():
                if key in base_params and base_params[key] != value:
                    logger.info(f"使用预设参数 {preset_key}: {key}={value}")
                base_params[key] = value
        
        return base_params
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """验证参数合法性"""
        try:
            # 精确匹配阈值检查
            exact_threshold = params.get('exact_match_threshold', 0.001)
            if exact_threshold < 0.0001 or exact_threshold > 0.01:
                return False, '精确匹配阈值应在0.0001-0.01元之间'
            
            # 近似匹配阈值检查
            approx_threshold = params.get('approx_match_threshold_percent', 1.0)
            if approx_threshold < 0.1 or approx_threshold > 5:
                return False, '近似匹配阈值应在0.1-5%之间'
            
            # 组合深度检查
            max_depth = params.get('max_combination_depth', 3)
            if max_depth > 6:
                return False, '组合深度最大为6行'
            
            # 多对多阈值检查（放宽范围）
            amount_threshold = params.get('many_to_many_amount_threshold', 500)
            if amount_threshold < 100 or amount_threshold > 2000:
                return False, '多对多金额阈值应在100-2000元之间'
            
            percent_threshold = params.get('many_to_many_percent_threshold', 0.5)
            if percent_threshold < 0.1 or percent_threshold > 2:
                return False, '多对多百分比阈值应在0.1-2%之间'
            
            # 检查是否启用多对多
            enable_many_to_many = params.get('enable_many_to_many', True)
            if not enable_many_to_many:
                logger.warning("多对多匹配已禁用，可能导致匹配率较低")
            
            return True, '参数验证通过'
            
        except Exception as e:
            return False, f'参数验证失败: {str(e)}'
    
    def preview_reconciliation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """预览对账结果 - 增强版"""
        try:
            logger.info("开始预览税务对账")
            
            # 验证参数
            valid, message = self._validate_parameters(params)
            if not valid:
                return {'status': 'error', 'message': message}
            
            # 加载数据
            tax_df, sap_df = self._load_data(params['tax_bureau_file'], params['sap_file'])
            
            # 计算基本统计
            tax_total = tax_df['税额'].sum()
            sap_total = sap_df['税额'].sum()
            tax_rows = len(tax_df)
            sap_rows = len(sap_df)
            diff_amount = abs(tax_total - sap_total)
            diff_percent = diff_amount / max(tax_total, sap_total) * 100 if max(tax_total, sap_total) > 0 else 0
            
            # 获取所有税率
            all_rates = sorted(set(tax_df['税率'].tolist() + sap_df['税率'].tolist()))
            
            # 估算匹配率
            estimated_match_rate = self._estimate_match_rate(tax_df, sap_df, params)
            
            # 构建预览结果
            preview_data = {
                'summary': {
                    'tax_rows': tax_rows,
                    'sap_rows': sap_rows,
                    'tax_total': round(tax_total, 2),
                    'sap_total': round(sap_total, 2),
                    'total_diff': round(diff_amount, 2),
                    'diff_percent': round(diff_percent, 2),
                    'tax_rates': all_rates,
                    'algorithm_params': params.get('match_precision_mode', '标准模式'),
                    'estimated_match_rate': round(estimated_match_rate, 2)
                },
                'rate_stats': [],
                'sample_data': {
                    'tax_bureau_sample': tax_df.head(5).to_dict('records'),
                    'sap_sample': sap_df.head(5).to_dict('records')
                },
                'parameter_summary': {
                    'exact_match_threshold': params.get('exact_match_threshold'),
                    'approx_match_threshold_percent': params.get('approx_match_threshold_percent'),
                    'max_combination_depth': params.get('max_combination_depth'),
                    'search_algorithm': params.get('search_algorithm'),
                    'enable_many_to_many': params.get('enable_many_to_many', True),
                    'many_to_many_amount_threshold': params.get('many_to_many_amount_threshold'),
                    'many_to_many_percent_threshold': params.get('many_to_many_percent_threshold')
                },
                'recommendations': self._generate_recommendations(tax_df, sap_df, params)
            }
            
            # 按税率统计
            for rate in all_rates[:10]:  # 显示前10个税率
                tax_rate_rows = len(tax_df[tax_df['税率'] == rate])
                sap_rate_rows = len(sap_df[sap_df['税率'] == rate])
                tax_rate_amount = tax_df[tax_df['税率'] == rate]['税额'].sum()
                sap_rate_amount = sap_df[sap_df['税率'] == rate]['税额'].sum()
                rate_diff = abs(tax_rate_amount - sap_rate_amount)
                rate_diff_percent = rate_diff / max(tax_rate_amount, sap_rate_amount) * 100 if max(tax_rate_amount, sap_rate_amount) > 0 else 0
                
                preview_data['rate_stats'].append({
                    'rate': rate,
                    'tax_rows': tax_rate_rows,
                    'sap_rows': sap_rate_rows,
                    'tax_amount': round(tax_rate_amount, 2),
                    'sap_amount': round(sap_rate_amount, 2),
                    'diff': round(rate_diff, 2),
                    'diff_percent': round(rate_diff_percent, 2),
                    'match_difficulty': self._assess_match_difficulty(tax_rate_amount, sap_rate_amount, rate_diff, rate_diff_percent)
                })
            
            logger.info("预览对账完成")
            return {
                'status': 'success',
                'message': '预览对账完成',
                'preview_data': preview_data,
                'summary': preview_data['summary']
            }
            
        except Exception as e:
            error_msg = f'预览对账失败: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return {'status': 'error', 'message': error_msg}
    
    def _estimate_match_rate(self, tax_df: pd.DataFrame, sap_df: pd.DataFrame, params: Dict[str, Any]) -> float:
        """估算匹配率"""
        # 简单估算逻辑
        total_amount = max(tax_df['税额'].sum(), sap_df['税额'].sum())
        if total_amount == 0:
            return 0.0
        
        # 计算可能的精确匹配
        exact_match_possible = 0
        for _, sap_row in sap_df.iterrows():
            sap_amount = sap_row['税额']
            exact_matches = tax_df[abs(tax_df['税额'] - sap_amount) < params.get('exact_match_threshold', 0.001)]
            if len(exact_matches) > 0:
                exact_match_possible += sap_amount
        
        # 根据参数调整估算
        base_rate = (exact_match_possible / total_amount * 100) if total_amount > 0 else 0
        
        # 如果启用了多对多匹配，提高估算
        if params.get('enable_many_to_many', True):
            base_rate = min(base_rate * 1.5, 95)  # 最多估算95%
        
        return base_rate
    
    def _assess_match_difficulty(self, tax_amount: float, sap_amount: float, diff: float, diff_percent: float) -> str:
        """评估匹配难度"""
        if diff < 0.01:
            return "容易"
        elif diff < 100 and diff_percent < 1:
            return "较易"
        elif diff < 500 and diff_percent < 5:
            return "中等"
        elif diff < 1000 and diff_percent < 10:
            return "较难"
        else:
            return "困难"
    
    def _generate_recommendations(self, tax_df: pd.DataFrame, sap_df: pd.DataFrame, params: Dict[str, Any]) -> List[str]:
        """生成参数建议"""
        recommendations = []
        
        # 检查数据特征
        tax_total = tax_df['税额'].sum()
        sap_total = sap_df['税额'].sum()
        diff = abs(tax_total - sap_total)
        diff_percent = diff / max(tax_total, sap_total) * 100 if max(tax_total, sap_total) > 0 else 0
        
        if diff > 1000 or diff_percent > 5:
            recommendations.append("总差异较大，建议启用多对多匹配")
        
        # 检查小额行数
        small_tax_rows = len(tax_df[tax_df['税额'] < 10])
        small_sap_rows = len(sap_df[sap_df['税额'] < 10])
        
        if small_tax_rows > 20 or small_sap_rows > 20:
            recommendations.append("小额记录较多，建议降低近似匹配阈值")
        
        # 检查税率分布
        tax_rate_counts = tax_df['税率'].value_counts()
        sap_rate_counts = sap_df['税率'].value_counts()
        
        if len(tax_rate_counts) > 10 or len(sap_rate_counts) > 10:
            recommendations.append("税率种类较多，建议分税率处理")
        
        # 检查是否启用多对多
        if not params.get('enable_many_to_many', True):
            recommendations.append("当前未启用多对多匹配，可能导致匹配率较低")
        
        return recommendations
    
    def execute_reconciliation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行完整对账 - 修正版"""
        try:
            logger.info("开始执行税务对账 - 修正版")
            start_time = time.time()
            
            # 验证参数
            valid, message = self._validate_parameters(params)
            if not valid:
                return {'status': 'error', 'message': message}
            
            # 加载数据
            tax_df, sap_df = self._load_data(params['tax_bureau_file'], params['sap_file'])
            
            # 使用修正后的优化对账算法
            from .optimized_tax_reconciliation import OptimizedTaxAmountReconciliation
            
            # 创建对账实例
            reconciler = OptimizedTaxAmountReconciliation(tax_df, sap_df)
            
            # 根据参数调整算法参数
            self._configure_reconciler(reconciler, params)
            
            # 执行对账
            result = reconciler.reconcile_all()
            
            # 生成输出文件名
            output_name = params.get('output_name', '税务对账结果_修正版')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"{output_name}_{timestamp}.xlsx"
            output_path = os.path.join(params['output_dir'], output_filename)
            
            # 导出结果
            reconciler.export_to_excel(output_path)
            
            # 计算执行时间
            execution_time = time.time() - start_time
            
            # 构建结果摘要
            summary = {
                'execution_time': round(execution_time, 2),
                'match_count': result['summary']['match_count'],
                'match_rate': round(result['summary'].get('match_rate', 0), 2),
                'total_tax_amount': round(result['summary']['total_tax_amount'], 2),
                'total_sap_amount': round(result['summary']['total_sap_amount'], 2),
                'total_matched': round(result['summary']['total_matched'], 2),
                'balance_diff': round(result['summary']['balance_diff'], 2),
                'unmatched_tax_count': result['summary']['unmatched_tax_count'],
                'unmatched_sap_count': result['summary']['unmatched_sap_count'],
                'performance_stats': result['performance_stats'],
                'validation_passed': result['summary'].get('validation_passed', False)
            }
            
            # 生成执行报告
            execution_report = self._generate_execution_report(summary, params, execution_time)
            
            logger.info(f"税务对账完成，耗时{execution_time:.2f}秒，结果保存到: {output_path}")
            return {
                'status': 'success',
                'message': '税务对账完成',
                'output_path': output_path,
                'summary': summary,
                'execution_report': execution_report,
                'performance_stats': result['performance_stats']
            }
            
        except Exception as e:
            error_msg = f'执行对账失败: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return {'status': 'error', 'message': error_msg}
    
    def _configure_reconciler(self, reconciler, params: Dict[str, Any]):
        """配置对账器参数"""
        # 根据匹配精度模式调整参数
        mode = params.get('match_precision_mode', 'standard')
        
        if mode == 'precise':
            reconciler.phase_params['primary']['max_depth'] = params.get('max_combination_depth', 4)
            reconciler.phase_params['primary']['max_candidates'] = params.get('max_candidates_per_stage', 25)
            # 调整多对多匹配阈值
            reconciler.phase_params['secondary']['max_depth'] = 3
        elif mode == 'fast':
            reconciler.phase_params['primary']['max_depth'] = params.get('max_combination_depth', 2)
            reconciler.phase_params['primary']['max_candidates'] = params.get('max_candidates_per_stage', 15)
            # 使用更宽松的搜索方法
            reconciler.phase_params['primary']['search_method'] = 'backtrack'
        
        # 确保启用多对多匹配
        if not params.get('enable_many_to_many', True):
            logger.warning("多对多匹配已禁用，匹配率可能较低")
        else:
            # 调整多对多匹配参数
            logger.info(f"启用多对多匹配，阈值: 金额{params.get('many_to_many_amount_threshold', 500)}元, "
                       f"百分比{params.get('many_to_many_percent_threshold', 0.5)}%")
    
    def _generate_execution_report(self, summary: Dict[str, Any], params: Dict[str, Any], execution_time: float) -> Dict[str, Any]:
        """生成执行报告"""
        report = {
            'execution_summary': {
                'status': '成功' if summary.get('validation_passed', False) else '需要检查',
                'execution_time': f"{execution_time:.2f}秒",
                'match_rate': f"{summary.get('match_rate', 0):.2f}%",
                'total_matched': f"{summary.get('total_matched', 0):,.2f}元"
            },
            'parameter_analysis': {
                'match_precision_mode': params.get('match_precision_mode', 'standard'),
                'enable_many_to_many': params.get('enable_many_to_many', True),
                'many_to_many_threshold': f"{params.get('many_to_many_amount_threshold', 500)}元/{params.get('many_to_many_percent_threshold', 0.5)}%"
            },
            'performance_analysis': {
                'exact_matches': summary.get('performance_stats', {}).get('exact_matches', 0),
                'one_to_n_matches': summary.get('performance_stats', {}).get('one_to_n_matches', 0),
                'many_to_many_matches': summary.get('performance_stats', {}).get('many_to_many_matches', 0),
                'total_matched_rows': summary.get('performance_stats', {}).get('total_matched_rows', 0)
            },
            'recommendations': []
        }
        
        # 根据结果生成建议
        if summary.get('match_rate', 0) < 50:
            report['recommendations'].append("匹配率较低，建议：1. 启用多对多匹配 2. 降低匹配阈值 3. 增加组合深度")
        
        if summary.get('unmatched_tax_count', 0) > 100:
            report['recommendations'].append("未匹配税局行数较多，建议检查数据完整性")
        
        if not summary.get('validation_passed', False):
            report['recommendations'].append("总额验证未通过，请检查数据或算法参数")
        
        if execution_time > 30:
            report['recommendations'].append("执行时间较长，建议：1. 使用快速模式 2. 减少候选行数 3. 降低组合深度")
        
        return report
    
    def batch_reconciliation(self, file_pairs: List[Tuple[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        """批量对账"""
        try:
            logger.info(f"开始批量对账，共{len(file_pairs)}个文件对")
            
            results = []
            successful = 0
            failed = 0
            
            for i, (tax_file, sap_file) in enumerate(file_pairs, 1):
                logger.info(f"处理第{i}对文件: {os.path.basename(tax_file)} vs {os.path.basename(sap_file)}")
                
                try:
                    # 复制参数并更新文件路径
                    file_params = params.copy()
                    file_params['tax_bureau_file'] = tax_file
                    file_params['sap_file'] = sap_file
                    file_params['output_name'] = f"对账结果_{i}"
                    
                    # 执行对账
                    result = self.execute_reconciliation(file_params)
                    
                    if result['status'] == 'success':
                        successful += 1
                        results.append({
                            'index': i,
                            'tax_file': tax_file,
                            'sap_file': sap_file,
                            'status': 'success',
                            'output_path': result['output_path'],
                            'match_rate': result['summary']['match_rate'],
                            'total_matched': result['summary']['total_matched']
                        })
                    else:
                        failed += 1
                        results.append({
                            'index': i,
                            'tax_file': tax_file,
                            'sap_file': sap_file,
                            'status': 'failed',
                            'error': result['message']
                        })
                        
                except Exception as e:
                    failed += 1
                    error_msg = f"第{i}对文件处理失败: {str(e)}"
                    logger.error(error_msg)
                    results.append({
                        'index': i,
                        'tax_file': tax_file,
                        'sap_file': sap_file,
                        'status': 'failed',
                        'error': error_msg
                    })
            
            # 生成批量报告
            batch_report = self._generate_batch_report(results, successful, failed)
            
            logger.info(f"批量对账完成，成功{successful}个，失败{failed}个")
            return {
                'status': 'success',
                'message': f'批量对账完成，成功{successful}个，失败{failed}个',
                'results': results,
                'batch_report': batch_report
            }
            
        except Exception as e:
            error_msg = f'批量对账失败: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return {'status': 'error', 'message': error_msg}
    
    def _generate_batch_report(self, results: List[Dict], successful: int, failed: int) -> Dict[str, Any]:
        """生成批量报告"""
        successful_results = [r for r in results if r['status'] == 'success']
        
        if successful_results:
            avg_match_rate = sum(r['match_rate'] for r in successful_results) / len(successful_results)
            max_match_rate = max(r['match_rate'] for r in successful_results)
            min_match_rate = min(r['match_rate'] for r in successful_results)
        else:
            avg_match_rate = max_match_rate = min_match_rate = 0
        
        return {
            'summary': {
                'total_files': len(results),
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / len(results) * 100) if results else 0
            },
            'match_rate_analysis': {
                'average': round(avg_match_rate, 2),
                'maximum': round(max_match_rate, 2),
                'minimum': round(min_match_rate, 2)
            },
            'failed_files': [
                {
                    'index': r['index'],
                    'tax_file': os.path.basename(r['tax_file']),
                    'sap_file': os.path.basename(r['sap_file']),
                    'error': r['error']
                }
                for r in results if r['status'] == 'failed'
            ]
        }
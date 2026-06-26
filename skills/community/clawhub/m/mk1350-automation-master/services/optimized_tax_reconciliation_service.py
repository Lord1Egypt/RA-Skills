import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Set, Any
import itertools
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class OptimizedTaxAmountReconciliationService:
    """优化的税务对账服务类 - 按照脚本版逻辑和顺序"""
    
    def __init__(self, tax_bureau_df: pd.DataFrame, sap_df: pd.DataFrame, params: Dict[str, Any] = None):
        """
        初始化完全参数化的税务对账类
        
        Parameters:
        -----------
        tax_bureau_df : 税局数据，包含列：['税额', '税率']
        sap_df : SAP数据,包含列：['税额', '税率']
        params : 完整的参数配置（使用脚本版默认值）
        """
        # 验证必须提供参数
        if params is None:
            raise ValueError("必须提供完整的参数配置")
        
        self.params = params
        
        # 备份原始数据
        self.tax_bureau_original = tax_bureau_df.copy()
        self.sap_original = sap_df.copy()
        
        # 添加行号作为唯一标识
        if 'ID' not in tax_bureau_df.columns:
            self.tax_bureau_df = tax_bureau_df.copy()
            self.tax_bureau_df['ID'] = [f'税局_{i:04d}' for i in range(len(tax_bureau_df))]
        else:
            self.tax_bureau_df = tax_bureau_df.copy()
            
        if 'ID' not in sap_df.columns:
            self.sap_df = sap_df.copy()
            self.sap_df['ID'] = [f'SAP_{i:04d}' for i in range(len(sap_df))]
        else:
            self.sap_df = sap_df.copy()
        
        # 确保数据类型
        self.tax_bureau_df['税额'] = pd.to_numeric(self.tax_bureau_df['税额'], errors='coerce').fillna(0)
        self.tax_bureau_df['税率'] = self.tax_bureau_df['税率'].astype(str).str.strip()
        self.sap_df['税额'] = pd.to_numeric(self.sap_df['税额'], errors='coerce').fillna(0)
        self.sap_df['税率'] = self.sap_df['税率'].astype(str).str.strip()
        
        # ===== 从参数初始化所有算法配置 =====
        self._init_from_params(params)
        
        # 结果存储
        self.matches = []  # 匹配结果
        self.unmatched_tax = []  # 未匹配的税局行
        self.unmatched_sap = []  # 未匹配的SAP行
        self.match_counter = 0  # 匹配组号计数器
        self._summary = None  # 缓存汇总结果
        self.performance_stats = defaultdict(int)  # 性能统计
        
        logger.info("税务对账服务初始化完成，使用脚本版逻辑")
    
    def _init_from_params(self, params: Dict[str, Any]):
        """从参数初始化所有算法配置"""
        # 核心匹配阈值参数
        self.exact_match_threshold = float(params.get('exact_match_threshold', 0.001))
        self.approx_match_threshold_percent = float(params.get('approx_match_threshold_percent', 1.0))
        
        # 多对多匹配阈值
        self.many_to_many_amount_threshold = float(params.get('many_to_many_amount_threshold', 1500))
        self.many_to_many_percent_threshold = float(params.get('many_to_many_percent_threshold', 1.0))
        
        # 最终匹配阈值（脚本版第333行硬编码值）
        self.final_match_amount_threshold = float(params.get('final_match_amount_threshold', 100.0))
        self.final_match_percent_threshold = float(params.get('final_match_percent_threshold', 0.1))
        
        # 递归匹配阈值（脚本版第257行硬编码值）
        self.recursive_min_amount_threshold = float(params.get('recursive_min_amount_threshold', 0.01))
        self.recursive_percent_threshold = float(params.get('recursive_percent_threshold', 10.0))
        
        # 算法控制参数
        self.large_amount_threshold = float(params.get('large_amount_threshold', 1000))
        self.pruning_threshold_percent = float(params.get('pruning_threshold_percent', 90.0))
        self.backtrack_overtune_percent = float(params.get('backtrack_overtune_percent', 10.0))
        self.backtrack_pruning_threshold_percent = float(params.get('backtrack_pruning_threshold_percent', 90.0))
        self.hybrid_search_threshold_percent = float(params.get('hybrid_search_threshold_percent', 10.0))
        
        # 阶段参数配置（使用脚本版参数）
        self.phase_params = {
            'primary': {
                'max_depth': int(params.get('max_combination_depth', 3)),
                'max_candidates': int(params.get('max_candidates_per_stage', 20)),
                'scale_factor': 100,
                'max_states': 50000,
                'search_method': params.get('search_algorithm', 'dp')
            },
            'secondary': {
                'max_depth': 3,
                'max_candidates': 15,
                'scale_factor': 10,
                'max_states': 20000,
                'search_method': 'backtrack'  # 脚本版使用回溯
            },
            'recursive': {
                'max_recursions': 0,  # 脚本版没有递归匹配
                'max_depth': 2,
                'max_candidates': 10
            }
        }
        
        # 功能开关
        self.enable_many_to_many = bool(params.get('enable_many_to_many', True))
        self.enable_recursive_match = False  # 脚本版没有递归匹配
        
        # 日志记录使用的参数
        logger.info("算法参数配置（脚本版逻辑）:")
        logger.info(f"  精确匹配阈值: {self.exact_match_threshold}")
        logger.info(f"  近似匹配阈值: {self.approx_match_threshold_percent}%")
        logger.info(f"  多对多匹配阈值: {self.many_to_many_amount_threshold}元/{self.many_to_many_percent_threshold}%")
        logger.info(f"  最终匹配阈值: {self.final_match_amount_threshold}元/{self.final_match_percent_threshold}%")
    
    # ==================== 脚本版算法逻辑（保持参数化） ====================
    
    def _find_combination_match_simple(self, candidates: pd.DataFrame, target: float) -> Optional[Dict]:
        """
        脚本版简单的组合匹配：只找1-3行的精确组合
        """
        if target <= 0 or len(candidates) == 0:
            return None
        
        # 脚本版逻辑：先尝试1行精确匹配
        exact_match = candidates[abs(candidates['税额'] - target) < self.exact_match_threshold]
        if len(exact_match) > 0:
            return {
                'tax_ids': [exact_match.iloc[0]['ID']],
                'total_amount': float(exact_match.iloc[0]['税额']),
                'remaining_amount': 0.0
            }
        
        # 脚本版：只尝试2-3行组合，且要求完全匹配
        candidates_sorted = candidates.sort_values('税额', ascending=False)
        
        # 尝试2行组合
        for i in range(len(candidates_sorted)):
            for j in range(i+1, min(len(candidates_sorted), i+10)):  # 限制搜索范围
                row1 = candidates_sorted.iloc[i]
                row2 = candidates_sorted.iloc[j]
                total = float(row1['税额']) + float(row2['税额'])
                
                if abs(total - target) < self.exact_match_threshold:
                    return {
                        'tax_ids': [row1['ID'], row2['ID']],
                        'total_amount': total,
                        'remaining_amount': 0.0
                    }
        
        # 尝试3行组合（脚本版很少）
        for i in range(len(candidates_sorted)):
            for j in range(i+1, min(len(candidates_sorted), i+5)):
                for k in range(j+1, min(len(candidates_sorted), j+5)):
                    row1 = candidates_sorted.iloc[i]
                    row2 = candidates_sorted.iloc[j]
                    row3 = candidates_sorted.iloc[k]
                    total = float(row1['税额']) + float(row2['税额']) + float(row3['税额'])
                    
                    if abs(total - target) < self.exact_match_threshold:
                        return {
                            'tax_ids': [row1['ID'], row2['ID'], row3['ID']],
                            'total_amount': total,
                            'remaining_amount': 0.0
                        }
        
        return None
    
    def _match_one_to_one_exact(self, tax_df: pd.DataFrame, sap_df: pd.DataFrame) -> Tuple[List[Dict], Set, Set]:
        """
        第一步:1对1精确匹配 - 与脚本版完全一致
        """
        matches = []
        matched_tax_ids = set()
        matched_sap_ids = set()
        
        # SAP按金额降序排序
        sap_sorted = sap_df.sort_values('税额', ascending=False)
        
        for _, sap_row in sap_sorted.iterrows():
            sap_id = sap_row['ID']
            sap_amount = float(sap_row['税额'])
            sap_rate = sap_row['税率']
            
            if sap_id in matched_sap_ids:
                continue
            
            # 寻找税额完全相等的税局行（未匹配的）
            exact_matches = tax_df[
                (abs(tax_df['税额'] - sap_amount) < self.exact_match_threshold) & 
                (~tax_df['ID'].isin(matched_tax_ids))
            ]
            
            if len(exact_matches) > 0:
                tax_row = exact_matches.iloc[0]
                tax_id = tax_row['ID']
                tax_amount = float(tax_row['税额'])
                tax_rate = tax_row['税率']
                
                # 增加匹配组号
                self.match_counter += 1
                match_group = f'MATCH_{self.match_counter:04d}'
                
                # 创建匹配记录
                match_record = {
                    '匹配组号': match_group,
                    'SAP_ID': sap_id,
                    'SAP税额': sap_amount,
                    '税率': sap_rate,
                    '匹配类型': '1对1',
                    '匹配状态': '完全匹配',
                    '税局序号': 1,
                    '税局_ID': tax_id,
                    '税局_税额': tax_amount,
                    '税局_税率': tax_rate,
                    '累计匹配额': sap_amount,
                    '验证状态': '验证通过',
                    '差异金额': 0.0,
                    '调节状态': '无需调节',
                    '调节原因': '完全匹配'
                }
                
                matches.append(match_record)
                matched_tax_ids.add(tax_id)
                matched_sap_ids.add(sap_id)
                
                self.performance_stats['exact_matches'] += 1
        
        return matches, matched_tax_ids, matched_sap_ids
    
    def _match_one_to_n_script_style(self, tax_df: pd.DataFrame, sap_df: pd.DataFrame,
                                     matched_tax_ids: Set, matched_sap_ids: Set) -> List[Dict]:
        """
        脚本版风格的1对N匹配：非常保守，只匹配小额且简单的组合
        """
        matches = []
        
        # 获取未匹配的SAP行（按金额降序）
        remaining_sap = sap_df[~sap_df['ID'].isin(matched_sap_ids)]
        if len(remaining_sap) == 0:
            return matches
        
        remaining_sap = remaining_sap.sort_values('税额', ascending=False)
        
        # 脚本版策略：只处理小额SAP（<1000元）
        for _, sap_row in remaining_sap.iterrows():
            sap_id = sap_row['ID']
            sap_amount = float(sap_row['税额'])
            sap_rate = sap_row['税率']
            
            if sap_id in matched_sap_ids:
                continue
            
            # 脚本版跳过大额SAP（留给多对多）
            if sap_amount >= 1000:
                continue
            
            # 获取未匹配的税局行
            available_tax = tax_df[~tax_df['ID'].isin(matched_tax_ids)]
            if len(available_tax) == 0:
                break
            
            # 脚本版：只找简单的精确组合
            result = self._find_combination_match_simple(available_tax, sap_amount)
            
            if not result:
                continue
            
            tax_ids = result['tax_ids']
            total_matched_amount = result['total_amount']
            final_diff = sap_amount - total_matched_amount
            
            # 确定匹配状态
            if abs(final_diff) < self.exact_match_threshold:
                match_status = '完全匹配'
                verification_status = '验证通过'
                adjust_status = '无需调节'
                adjust_reason = '完全匹配'
            elif abs(final_diff) < sap_amount * (self.approx_match_threshold_percent / 100):
                match_status = '近似匹配'
                verification_status = '验证通过'
                adjust_status = '微小差异'
                adjust_reason = '四舍五入差异'
            else:
                match_status = '部分匹配'
                verification_status = '部分匹配'
                adjust_status = '待处理'
                adjust_reason = '时点差异'
            
            # 创建匹配组
            self.match_counter += 1
            match_group = f'MATCH_{self.match_counter:04d}'
            
            # 获取匹配的税局行详情
            matched_tax_rows = available_tax[available_tax['ID'].isin(tax_ids)]
            matched_tax_rows = matched_tax_rows.sort_values('税额', ascending=False)
            
            # 为每个匹配的税局行创建记录
            cumulative_amount = 0
            match_records = []
            
            for tax_idx, (_, tax_row) in enumerate(matched_tax_rows.iterrows(), 1):
                tax_amount = float(tax_row['税额'])
                cumulative_amount += tax_amount
                
                match_record = {
                    '匹配组号': match_group,
                    'SAP_ID': sap_id,
                    'SAP税额': sap_amount,
                    '税率': sap_rate,
                    '匹配类型': f'1对{len(matched_tax_rows)}',
                    '匹配状态': match_status,
                    '税局序号': tax_idx,
                    '税局_ID': tax_row['ID'],
                    '税局_税额': tax_amount,
                    '税局_税率': tax_row['税率'],
                    '累计匹配额': cumulative_amount,
                    '验证状态': verification_status,
                    '差异金额': final_diff,
                    '调节状态': adjust_status,
                    '调节原因': adjust_reason
                }
                
                match_records.append(match_record)
            
            matches.extend(match_records)
            
            # 标记为已匹配
            matched_tax_ids.update(tax_ids)
            matched_sap_ids.add(sap_id)
            
            self.performance_stats['one_to_n_matches'] += 1
            self.performance_stats['total_matched_rows'] += len(tax_ids)
        
        return matches
    
    def _match_many_to_many_total(self, sap_unmatched: List[Dict], tax_unmatched: List[Dict], rate: str):
        """
        多对多匹配：总额匹配 - 脚本版逻辑
        """
        # 计算总额
        sap_total = sum(item['税额'] for item in sap_unmatched)
        tax_total = sum(item['税额'] for item in tax_unmatched)
        diff_amount = sap_total - tax_total
        
        logger.info(f"税率{rate}: 执行总额匹配，SAP {len(sap_unmatched)}行，税局 {len(tax_unmatched)}行")
        logger.info(f"SAP总额: {sap_total:.2f}, 税局总额: {tax_total:.2f}, 差异: {diff_amount:.2f}")
        
        # 增加匹配组号
        self.match_counter += 1
        match_group = f'MATCH_{self.match_counter:04d}'
        
        # 确定匹配状态
        if abs(diff_amount) < self.exact_match_threshold:
            match_status = '完全匹配'
            verification_status = '验证通过'
            adjust_status = '无需调节'
            adjust_reason = '多对多完全匹配'
        elif abs(diff_amount) < max(sap_total, tax_total) * (self.approx_match_threshold_percent / 100):
            match_status = '近似匹配'
            verification_status = '验证通过'
            adjust_status = '微小差异'
            adjust_reason = '多对多近似匹配'
        else:
            match_status = '部分匹配'
            verification_status = '部分匹配' 
            adjust_status = '待处理'
            adjust_reason = '多对多差异匹配'
        
        # 为每行SAP创建记录
        sap_cumulative = 0
        for sap_idx, sap_item in enumerate(sap_unmatched, 1):
            sap_cumulative += sap_item['税额']
            
            sap_match_record = {
                '匹配组号': match_group,
                'SAP_ID': sap_item['ID'],
                'SAP税额': sap_item['税额'],
                '税率': rate,
                '匹配类型': f'{len(sap_unmatched)}对{len(tax_unmatched)}',
                '匹配状态': match_status,
                '税局序号': 0,
                '税局_ID': f"SAP组_{sap_idx}",
                '税局_税额': sap_item['税额'],
                '税局_税率': rate,
                '累计匹配额': sap_cumulative,
                '验证状态': verification_status,
                '差异金额': diff_amount,
                '调节状态': adjust_status,
                '调节原因': adjust_reason
            }
            self.matches.append(sap_match_record)
        
        # 为每行税局创建记录
        tax_cumulative = 0
        for tax_idx, tax_item in enumerate(tax_unmatched, 1):
            tax_cumulative += tax_item['税额']
            
            tax_match_record = {
                '匹配组号': match_group,
                'SAP_ID': f"TAX组_{tax_idx}",
                'SAP税额': sap_total,
                '税率': rate,
                '匹配类型': f'{len(sap_unmatched)}对{len(tax_unmatched)}',
                '匹配状态': match_status,
                '税局序号': tax_idx,
                '税局_ID': tax_item['ID'],
                '税局_税额': tax_item['税额'],
                '税局_税率': rate,
                '累计匹配额': tax_cumulative,
                '验证状态': verification_status,
                '差异金额': diff_amount,
                '调节状态': adjust_status,
                '调节原因': adjust_reason
            }
            self.matches.append(tax_match_record)
        
        logger.info(f"✓ 多对多总额匹配完成: {len(sap_unmatched)}行SAP = {len(tax_unmatched)}行税局")
        
        # 从未匹配列表中移除这些项（脚本版逻辑）
        sap_ids_to_remove = {item['ID'] for item in sap_unmatched}
        tax_ids_to_remove = {item['ID'] for item in tax_unmatched}
        
        self.unmatched_sap = [item for item in self.unmatched_sap 
                             if item['税率'] != rate or item['ID'] not in sap_ids_to_remove]
        self.unmatched_tax = [item for item in self.unmatched_tax 
                             if item['税率'] != rate or item['ID'] not in tax_ids_to_remove]
        
        self.performance_stats['many_to_many_matches'] += 1
    
    def _match_many_to_many_by_rate(self, rate: str):
        """
        多对多匹配：按税率处理 - 脚本版逻辑（总是执行）
        """
        if not self.enable_many_to_many:
            logger.info(f"多对多匹配已禁用，跳过税率{rate}")
            return
        
        # 获取该税率下未匹配的行
        sap_unmatched = [item for item in self.unmatched_sap if item['税率'] == rate]
        tax_unmatched = [item for item in self.unmatched_tax if item['税率'] == rate]
        
        if not sap_unmatched or not tax_unmatched:
            return
        
        logger.info(f"税率 {rate}: 开始多对多匹配")
        logger.info(f"未匹配SAP行数: {len(sap_unmatched)}，未匹配税局行数: {len(tax_unmatched)}")
        
        # 计算总额
        sap_total = sum(item['税额'] for item in sap_unmatched)
        tax_total = sum(item['税额'] for item in tax_unmatched)
        diff = abs(sap_total - tax_total)
        diff_percent = diff / max(sap_total, tax_total) * 100 if max(sap_total, tax_total) > 0 else 0
        
        logger.info(f"SAP未匹配总额: {sap_total:.2f}，税局未匹配总额: {tax_total:.2f}")
        logger.info(f"总额差异: {diff:.2f}元 ({diff_percent:.2f}%)")
        
        # 脚本版逻辑：总是执行多对多匹配
        logger.info(f"执行多对多匹配（脚本版逻辑）")
        self._match_many_to_many_total(sap_unmatched, tax_unmatched, rate)
    
    def _final_total_match_check(self):
        """
        最终总额匹配检查（脚本版逻辑）
        """
        logger.info("开始最终总额匹配检查...")
        
        all_rates = set()
        for item in self.unmatched_sap:
            all_rates.add(item['税率'])
        for item in self.unmatched_tax:
            all_rates.add(item['税率'])
        
        for rate in sorted(all_rates):
            sap_unmatched = [item for item in self.unmatched_sap if item['税率'] == rate]
            tax_unmatched = [item for item in self.unmatched_tax if item['税率'] == rate]
            
            if not sap_unmatched or not tax_unmatched:
                continue
            
            sap_total = sum(item['税额'] for item in sap_unmatched)
            tax_total = sum(item['税额'] for item in tax_unmatched)
            
            diff = abs(sap_total - tax_total)
            diff_percent = diff / max(sap_total, tax_total) * 100 if max(sap_total, tax_total) > 0 else 0
            
            logger.info(f"税率 {rate}:")
            logger.info(f"SAP剩余: {len(sap_unmatched)}行，{sap_total:.2f}元")
            logger.info(f"税局剩余: {len(tax_unmatched)}行，{tax_total:.2f}元")
            logger.info(f"差异: {diff:.2f}元 ({diff_percent:.2f}%)")
            
            # 脚本版条件：差异小于100元 或 差异小于0.1%
            if diff < self.final_match_amount_threshold or diff_percent < self.final_match_percent_threshold:
                logger.info(f"✓ 执行最终总额匹配")
                self._match_many_to_many_total(sap_unmatched, tax_unmatched, rate)
            else:
                logger.info(f"✗ 差异过大，跳过最终匹配")
    
    # ==================== 主要对账方法 ====================
    
    def reconcile_by_rate(self, rate: str):
        """
        按单个税率进行匹配 - 完全按照脚本版执行顺序
        """
        # 获取该税率的行
        tax_rate_df = self.tax_bureau_df[self.tax_bureau_df['税率'] == rate].copy()
        sap_rate_df = self.sap_df[self.sap_df['税率'] == rate].copy()
        
        if len(sap_rate_df) == 0:
            # 该税率下SAP无记录，所有税局行都是未匹配
            for _, tax_row in tax_rate_df.iterrows():
                self.unmatched_tax.append({
                    'ID': tax_row['ID'],
                    '税额': float(tax_row['税额']),
                    '税率': tax_row['税率'],
                    '匹配状态': '未匹配',
                    '差异原因': 'SAP无此税率'
                })
            return
        
        if len(tax_rate_df) == 0:
            # 该税率下税局无记录，所有SAP行都是未匹配
            for _, sap_row in sap_rate_df.iterrows():
                self.unmatched_sap.append({
                    'ID': sap_row['ID'],
                    '税额': float(sap_row['税额']),
                    '税率': sap_row['税率'],
                    '匹配状态': '未匹配',
                    '差异原因': '税局无此税率'
                })
            return
        
        logger.info(f"处理税率 {rate}: 税局行数={len(tax_rate_df)}, SAP行数={len(sap_rate_df)}")
        
        # 第一步：1对1精确匹配
        exact_matches, matched_tax_ids, matched_sap_ids = self._match_one_to_one_exact(tax_rate_df, sap_rate_df)
        self.matches.extend(exact_matches)
        
        logger.info(f"1对1匹配完成: {len(exact_matches)}组")
        
        # 第二步：脚本版风格的1对N匹配（保守）
        combination_matches = self._match_one_to_n_script_style(tax_rate_df, sap_rate_df, matched_tax_ids, matched_sap_ids)
        self.matches.extend(combination_matches)
        
        logger.info(f"脚本版1对N匹配完成: {len(combination_matches)}行记录")
        
        # 记录未匹配的SAP行（脚本版逻辑：直接追加）
        all_sap_ids = set(sap_rate_df['ID'].tolist())
        unmatched_sap_ids = all_sap_ids - matched_sap_ids
        
        for sap_id in unmatched_sap_ids:
            sap_row = sap_rate_df[sap_rate_df['ID'] == sap_id].iloc[0]
            self.unmatched_sap.append({
                'ID': sap_id,
                '税额': float(sap_row['税额']),
                '税率': sap_row['税率'],
                '匹配状态': '未匹配',
                '差异原因': '无匹配组合'
            })
        
        # 记录未匹配的税局行（脚本版逻辑：直接追加）
        all_tax_ids = set(tax_rate_df['ID'].tolist())
        unmatched_tax_ids = all_tax_ids - matched_tax_ids
        
        for tax_id in unmatched_tax_ids:
            tax_row = tax_rate_df[tax_rate_df['ID'] == tax_id].iloc[0]
            self.unmatched_tax.append({
                'ID': tax_id,
                '税额': float(tax_row['税额']),
                '税率': tax_row['税率'],
                '匹配状态': '未匹配',
                '差异原因': 'SAP无匹配项'
            })
        
        logger.info(f"未匹配: {len(unmatched_sap_ids)}行SAP, {len(unmatched_tax_ids)}行税局")
    
    def reconcile_all(self) -> Dict:
        """
        执行完整对账流程 - 完全按照脚本版执行顺序
        """
        # 如果已有缓存结果，直接返回
        if self._summary is not None and self.matches:
            return self._get_serializable_result()
        
        # 清空结果
        self.matches = []
        self.unmatched_tax = []
        self.unmatched_sap = []
        self.match_counter = 0
        self._summary = None
        self.performance_stats.clear()
        
        logger.info("开始脚本版逻辑税务对账...")
        logger.info(f"税局数据行数: {len(self.tax_bureau_df)}")
        logger.info(f"SAP数据行数: {len(self.sap_df)}")
        logger.info("=" * 60)
        
        # 获取所有税率
        all_rates = sorted(set(self.tax_bureau_df['税率'].tolist() + self.sap_df['税率'].tolist()))
        
        # 第一步：按税率分别执行1对1和脚本版1对N匹配
        logger.info("\n第一步：1对1精确匹配 + 脚本版1对N组合匹配")
        logger.info("=" * 60)
        for rate in all_rates:
            self.reconcile_by_rate(rate)
        
        # 第二步：多对多匹配（脚本版总是执行）
        logger.info("\n" + "=" * 60)
        logger.info("第二步:多对多匹配(脚本版逻辑)")
        logger.info("=" * 60)
        for rate in all_rates:
            self._match_many_to_many_by_rate(rate)
        
        # 第三步：最终总额匹配检查
        self._final_total_match_check()
        
        # 汇总统计
        total_tax_amount = float(self.tax_bureau_df['税额'].sum())
        total_sap_amount = float(self.sap_df['税额'].sum())
        
        if self.matches:
            # 每个匹配组只计算一次SAP税额（脚本版逻辑）
            matched_sap_ids = set()
            total_matched = 0.0
            match_groups = set()
            
            for match in self.matches:
                if 'SAP_ID' in match and match['SAP_ID'] not in matched_sap_ids:
                    matched_sap_ids.add(match['SAP_ID'])
                    total_matched += match['SAP税额']
                if '匹配组号' in match:
                    match_groups.add(match['匹配组号'])
            
            match_count = len(match_groups)
        else:
            total_matched = 0.0
            match_count = 0
        
        total_unmatched_tax = sum(item['税额'] for item in self.unmatched_tax)
        total_unmatched_sap = sum(item['税额'] for item in self.unmatched_sap)
        
        # 计算匹配率
        total_processed = total_matched + total_unmatched_tax + total_unmatched_sap
        match_rate = (total_matched / total_processed * 100) if total_processed > 0 else 0.0
        
        # 保存汇总结果到缓存
        self._summary = {
            'total_tax_amount': total_tax_amount,
            'total_sap_amount': total_sap_amount,
            'total_matched': total_matched,
            'total_unmatched_tax': total_unmatched_tax,
            'total_unmatched_sap': total_unmatched_sap,
            'match_count': match_count,
            'unmatched_tax_count': len(self.unmatched_tax),
            'unmatched_sap_count': len(self.unmatched_sap),
            'balance_diff': total_tax_amount - total_sap_amount,
            'match_rate': match_rate,
            'validation_passed': False
        }
        
        # 验证总额守恒
        tax_validation = abs((total_matched + total_unmatched_tax) - total_tax_amount) < 0.01
        sap_validation = abs((total_matched + total_unmatched_sap) - total_sap_amount) < 0.01
        
        self._summary['validation_passed'] = bool(tax_validation and sap_validation)
        
        # 打印汇总信息（脚本版格式）
        logger.info("\n" + "=" * 60)
        logger.info("对账汇总结果:")
        logger.info("=" * 60)
        logger.info(f"税局总额: {total_tax_amount:,.2f}元")
        logger.info(f"SAP总额: {total_sap_amount:,.2f}元")
        logger.info(f"总差异: {(total_tax_amount - total_sap_amount):,.2f}元")
        logger.info(f"匹配组数: {match_count}组")
        logger.info(f"已匹配总额: {total_matched:,.2f}元")
        logger.info(f"匹配率: {match_rate:.2f}%")
        logger.info(f"税局未匹配总额: {total_unmatched_tax:,.2f}元 (共{len(self.unmatched_tax)}笔)")
        logger.info(f"SAP未匹配总额: {total_unmatched_sap:,.2f}元 (共{len(self.unmatched_sap)}笔)")
        
        # 性能统计
        logger.info("\n性能统计:")
        logger.info(f"精确匹配: {self.performance_stats.get('exact_matches', 0)}组")
        logger.info(f"1对N匹配: {self.performance_stats.get('one_to_n_matches', 0)}组")
        logger.info(f"多对多匹配: {self.performance_stats.get('many_to_many_matches', 0)}组")
        logger.info(f"总匹配行数: {self.performance_stats.get('total_matched_rows', 0)}行")
        
        # 验证总额守恒
        logger.info("\n总额验证:")
        logger.info(f"税局总额({total_tax_amount:,.2f}) = 已匹配({total_matched:,.2f}) + 税局未匹配({total_unmatched_tax:,.2f})")
        logger.info(f"SAP总额({total_sap_amount:,.2f}) = 已匹配({total_matched:,.2f}) + SAP未匹配({total_unmatched_sap:,.2f})")
        
        if tax_validation:
            logger.info("✓ 税局总额验证通过")
        else:
            logger.info("✗ 税局总额验证失败")
            
        if sap_validation:
            logger.info("✓ SAP总额验证通过")
        else:
            logger.info("✗ SAP总额验证失败")
        
        return self._get_serializable_result()
    
    def _get_serializable_result(self):
        """
        获取可序列化的结果（转换所有 NumPy 类型）
        """
        # 转换 performance_stats
        perf_stats = {k: int(v) for k, v in self.performance_stats.items()}
        
        # 转换 summary
        summary = {}
        for key, value in self._summary.items():
            if hasattr(value, 'item'):
                summary[key] = value.item()
            else:
                summary[key] = value
        
        return {
            'matches': self.matches,
            'unmatched_tax': self.unmatched_tax,
            'unmatched_sap': self.unmatched_sap,
            'summary': summary,
            'performance_stats': perf_stats,
            'status': 'success',
            'message': '税务对账完成'
        }
    
    # ==================== 以下辅助方法保持原样 ====================
    
    def get_matches_df(self) -> pd.DataFrame:
        """将匹配结果转换为展开式DataFrame"""
        if not self.matches:
            return pd.DataFrame()
        
        # 直接使用matches列表创建DataFrame
        matches_df = pd.DataFrame(self.matches)
        
        # 确保列的顺序
        column_order = [
            '匹配组号', 'SAP_ID', 'SAP税额', '税率', '匹配类型', '匹配状态',
            '税局序号', '税局_ID', '税局_税额', '税局_税率',
            '累计匹配额', '验证状态', '差异金额', '调节状态', '调节原因'
        ]
        
        # 只保留存在的列
        existing_columns = [col for col in column_order if col in matches_df.columns]
        matches_df = matches_df[existing_columns]
        
        return matches_df
    
    def get_unmatched_df(self) -> pd.DataFrame:
        """将未匹配结果转换为DataFrame"""
        all_unmatched = []
        
        for item in self.unmatched_tax:
            all_unmatched.append({
                '来源': '税局',
                'ID': item['ID'],
                '税额': item['税额'],
                '税率': item['税率'],
                '匹配状态': item.get('匹配状态', '未匹配'),
                '差异原因': item.get('差异原因', '未知')
            })
        
        for item in self.unmatched_sap:
            all_unmatched.append({
                '来源': 'SAP',
                'ID': item['ID'],
                '税额': item['税额'],
                '税率': item['税率'],
                '匹配状态': item.get('匹配状态', '未匹配'),
                '差异原因': item.get('差异原因', '未知')
            })
        
        if not all_unmatched:
            return pd.DataFrame()
        
        unmatched_df = pd.DataFrame(all_unmatched)
        unmatched_df = unmatched_df.sort_values(['来源', '税率', '税额'], ascending=[True, True, False])
        
        return unmatched_df
      
    def get_summary_by_rate(self) -> pd.DataFrame:
        """
        按税率汇总统计
        """
        if not self.matches and not self.unmatched_tax and not self.unmatched_sap:
            return pd.DataFrame()
        
        summary_data = []
        
        all_rates = set()
        if self.matches:
            matches_df = pd.DataFrame(self.matches)
            all_rates.update(matches_df['税率'].unique())
        
        for item in self.unmatched_tax:
            all_rates.add(item['税率'])
        
        for item in self.unmatched_sap:
            all_rates.add(item['税率'])
        
        for rate in sorted(all_rates):
            # 计算该税率的匹配金额和笔数
            if self.matches:
                rate_matches = [m for m in self.matches if m['税率'] == rate]
                if rate_matches:
                    matches_df_rate = pd.DataFrame(rate_matches)
                    # 每个匹配组只计算一次SAP税额
                    unique_matches = matches_df_rate.drop_duplicates(subset=['匹配组号', 'SAP_ID'])
                    matched_amount = unique_matches['SAP税额'].sum()
                    match_count = len(unique_matches['匹配组号'].unique())
                    match_rows = len(rate_matches)
                else:
                    matched_amount = 0.0
                    match_count = 0
                    match_rows = 0
            else:
                matched_amount = 0.0
                match_count = 0
                match_rows = 0
            
            # 计算该税率的未匹配金额
            tax_unmatched = [u for u in self.unmatched_tax if u['税率'] == rate]
            sap_unmatched = [u for u in self.unmatched_sap if u['税率'] == rate]
            
            tax_unmatched_amount = sum(u['税额'] for u in tax_unmatched)
            sap_unmatched_amount = sum(u['税额'] for u in sap_unmatched)
            
            # 计算总额和匹配率
            total_amount = matched_amount + tax_unmatched_amount + sap_unmatched_amount
            match_rate = (matched_amount / total_amount * 100) if total_amount > 0 else 0.0
            
            summary_data.append({
                '税率': rate,
                '匹配金额': matched_amount,
                '匹配组数': match_count,
                '匹配行数': match_rows,
                '税局未匹配金额': tax_unmatched_amount,
                '税局未匹配笔数': len(tax_unmatched),
                'SAP未匹配金额': sap_unmatched_amount,
                'SAP未匹配笔数': len(sap_unmatched),
                '总额': total_amount,
                '匹配率(%)': round(match_rate, 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # 添加总计行
        if not summary_df.empty:
            total_row = {
                '税率': '总计',
                '匹配金额': summary_df['匹配金额'].sum(),
                '匹配组数': summary_df['匹配组数'].sum(),
                '匹配行数': summary_df['匹配行数'].sum(),
                '税局未匹配金额': summary_df['税局未匹配金额'].sum(),
                '税局未匹配笔数': summary_df['税局未匹配笔数'].sum(),
                'SAP未匹配金额': summary_df['SAP未匹配金额'].sum(),
                'SAP未匹配笔数': summary_df['SAP未匹配笔数'].sum(),
                '总额': summary_df['总额'].sum(),
                '匹配率(%)': summary_df['匹配金额'].sum() / summary_df['总额'].sum() * 100 if summary_df['总额'].sum() > 0 else 0
            }
            summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)
        
        return summary_df
    
    def export_to_excel(self, filepath: str):
        """
        将结果导出到Excel文件（修复科学计数法）
        """
        # 确保已执行对账
        if self._summary is None:
            self.reconcile_all()
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 1. 匹配明细
            matches_df = self.get_matches_df()
            if not matches_df.empty:
                # 修复科学计数法：格式化差异金额列
                if '差异金额' in matches_df.columns:
                    # 方法1：使用round保留指定位数
                    matches_df['差异金额'] = matches_df['差异金额'].apply(
                        lambda x: round(x, 2) if pd.notnull(x) else x
                    )
                    # 或者方法2：直接格式化为字符串，避免科学计数法
                    # matches_df['差异金额'] = matches_df['差异金额'].apply(
                    #     lambda x: f"{x:.12f}" if pd.notnull(x) else x
                    # )
                
                # 确保所有数值列都有合适的格式
                numeric_columns = ['SAP税额', '税局_税额', '累计匹配额', '差异金额']
                for col in numeric_columns:
                    if col in matches_df.columns:
                        matches_df[col] = matches_df[col].apply(
                            lambda x: round(x, 2) if pd.notnull(x) and isinstance(x, (int, float)) else x
                        )
                
                matches_df.to_excel(writer, sheet_name='匹配明细', index=False)
            
            # 2. 未匹配项
            unmatched_df = self.get_unmatched_df()
            if not unmatched_df.empty:
                # 同样修复未匹配项中的数值列
                if '税额' in unmatched_df.columns:
                    unmatched_df['税额'] = unmatched_df['税额'].apply(
                        lambda x: round(x, 2) if pd.notnull(x) else x
                    )
                unmatched_df.to_excel(writer, sheet_name='未匹配项', index=False)
            
            # 3. 按税率汇总
            summary_df = self.get_summary_by_rate()
            if not summary_df.empty:
                # 修复汇总表中的数值列
                numeric_summary_columns = ['匹配金额', '税局未匹配金额', 'SAP未匹配金额', '总额', '匹配率(%)']
                for col in numeric_summary_columns:
                    if col in summary_df.columns:
                        summary_df[col] = summary_df[col].apply(
                            lambda x: round(x, 2) if pd.notnull(x) and isinstance(x, (int, float)) else x
                        )
                summary_df.to_excel(writer, sheet_name='税率汇总', index=False)
            
            # 4. 原始数据（备份）- 不修改原始数据
            self.tax_bureau_df.to_excel(writer, sheet_name='原始_税局数据', index=False)
            self.sap_df.to_excel(writer, sheet_name='原始_SAP数据', index=False)
            
            # 5. 性能统计
            if self.performance_stats:
                perf_df = pd.DataFrame(list(self.performance_stats.items()), columns=['指标', '值'])
                perf_df.to_excel(writer, sheet_name='性能统计', index=False)
            
            # 6. 对账摘要
            summary_text = [
                ['对账摘要', ''],
                ['对账时间', pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['对账版本', '脚本版逻辑迁移（修复科学计数法）'],
                ['税局数据行数', len(self.tax_bureau_df)],
                ['SAP数据行数', len(self.sap_df)],
                ['税局总额', f"{self._summary['total_tax_amount']:,.2f}元"],
                ['SAP总额', f"{self._summary['total_sap_amount']:,.2f}元"],
                ['总差异', f"{round(self._summary['balance_diff'], 2):.2f}元"], 
                ['匹配组数', self._summary['match_count']],
                ['匹配率', f"{self._summary.get('match_rate', 0):.2f}%"],
                ['已匹配总额', f"{self._summary['total_matched']:,.2f}元"],
                ['税局未匹配总额', f"{self._summary['total_unmatched_tax']:,.2f}元"],
                ['税局未匹配笔数', self._summary['unmatched_tax_count']],
                ['SAP未匹配总额', f"{self._summary['total_unmatched_sap']:,.2f}元"],
                ['SAP未匹配笔数', self._summary['unmatched_sap_count']],
                ['', ''],
                ['验证结果', ''],
                ['税局总额验证', '通过' if abs((self._summary['total_matched'] + self._summary['total_unmatched_tax']) - self._summary['total_tax_amount']) < 0.01 else '失败'],
                ['SAP总额验证', '通过' if abs((self._summary['total_matched'] + self._summary['total_unmatched_sap']) - self._summary['total_sap_amount']) < 0.01 else '失败'],
                ['验证状态', '通过' if self._summary.get('validation_passed', False) else '失败']
            ]
            
            summary_df = pd.DataFrame(summary_text)
            summary_df.to_excel(writer, sheet_name='对账摘要', index=False, header=False)
        
        logger.info(f"结果已导出到: {filepath}")
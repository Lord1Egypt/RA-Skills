#!/usr/bin/env python3
"""
记忆一致性校验系统
确保记忆数据的完整性和一致性

功能:
- 数据完整性校验
- 引用完整性检查
- 索引一致性验证
- 自动修复
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CheckType(Enum):
    """检查类型"""
    DATA_INTEGRITY = "data_integrity"       # 数据完整性
    REFERENCE_INTEGRITY = "reference_integrity"  # 引用完整性
    INDEX_CONSISTENCY = "index_consistency"  # 索引一致性
    NETWORK_INTEGRITY = "network_integrity"  # 网络完整性
    ORPHAN_CHECK = "orphan_check"           # 孤儿检查


@dataclass
class CheckResult:
    """检查结果"""
    check_type: CheckType
    passed: bool
    issues: List[Dict]
    warnings: List[Dict]
    checked_count: int
    passed_count: int
    timestamp: str


@dataclass
class ConsistencyReport:
    """一致性报告"""
    overall_passed: bool
    check_results: List[CheckResult]
    total_issues: int
    total_warnings: int
    recommendations: List[str]
    timestamp: str


class MemoryConsistency:
    """
    记忆一致性校验系统
    """
    
    def __init__(self, memory_path: str = "./memory"):
        self.memory_path = memory_path
        
        # 校验规则
        self.integrity_rules = {
            'required_fields': ['id', 'content', 'created_time', 'type'],
            'valid_types': ['user', 'project', 'feedback', 'reference', 'insight', 
                           'task', 'knowledge', 'problem', 'solution'],
            'energy_range': (0.0, 2.0),
            'importance_range': (0.0, 1.0),
            'max_content_length': 10000
        }
        
        # 统计
        self.stats = {
            'total_checks': 0,
            'total_issues_found': 0,
            'total_auto_fixed': 0,
            'last_check': None
        }
        
        # 检查历史
        self.check_history: List[ConsistencyReport] = []
    
    def run_full_check(self, auto_fix: bool = False) -> ConsistencyReport:
        """运行完整检查"""
        results = []
        
        # 1. 数据完整性检查
        results.append(self.check_data_integrity(auto_fix))
        
        # 2. 引用完整性检查
        results.append(self.check_reference_integrity(auto_fix))
        
        # 3. 索引一致性检查
        results.append(self.check_index_consistency(auto_fix))
        
        # 4. 网络完整性检查
        results.append(self.check_network_integrity(auto_fix))
        
        # 5. 孤儿检查
        results.append(self.check_orphans(auto_fix))
        
        # 汇总
        total_issues = sum(len(r.issues) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        
        recommendations = self._generate_recommendations(results)
        
        report = ConsistencyReport(
            overall_passed=total_issues == 0,
            check_results=results,
            total_issues=total_issues,
            total_warnings=total_warnings,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
        
        self.check_history.append(report)
        self.stats['total_checks'] += 1
        self.stats['total_issues_found'] += total_issues
        self.stats['last_check'] = report.timestamp
        
        return report
    
    def check_data_integrity(self, auto_fix: bool = False) -> CheckResult:
        """数据完整性检查"""
        issues = []
        warnings = []
        checked_count = 0
        passed_count = 0
        
        # 加载所有细胞数据
        cells = self._load_all_cells()
        
        for cell_id, cell_data in cells.items():
            checked_count += 1
            cell_issues = []
            cell_warnings = []
            
            # 检查必需字段
            for field in self.integrity_rules['required_fields']:
                if field not in cell_data:
                    cell_issues.append({
                        'type': 'missing_field',
                        'field': field,
                        'cell_id': cell_id
                    })
            
            # 检查类型有效性
            cell_type = cell_data.get('type')
            if cell_type and cell_type not in self.integrity_rules['valid_types']:
                cell_warnings.append({
                    'type': 'invalid_type',
                    'value': cell_type,
                    'cell_id': cell_id,
                    'valid_types': self.integrity_rules['valid_types']
                })
            
            # 检查能量范围
            energy = cell_data.get('energy')
            if energy is not None:
                min_e, max_e = self.integrity_rules['energy_range']
                if not (min_e <= energy <= max_e):
                    cell_issues.append({
                        'type': 'energy_out_of_range',
                        'value': energy,
                        'cell_id': cell_id,
                        'valid_range': [min_e, max_e]
                    })
            
            # 检查重要性范围
            importance = cell_data.get('importance')
            if importance is not None:
                min_i, max_i = self.integrity_rules['importance_range']
                if not (min_i <= importance <= max_i):
                    cell_warnings.append({
                        'type': 'importance_out_of_range',
                        'value': importance,
                        'cell_id': cell_id,
                        'valid_range': [min_i, max_i]
                    })
            
            # 检查内容长度
            content = cell_data.get('content', '')
            max_len = self.integrity_rules['max_content_length']
            if len(content) > max_len:
                cell_warnings.append({
                    'type': 'content_too_long',
                    'length': len(content),
                    'cell_id': cell_id,
                    'max_length': max_len
                })
            
            # 检查时间格式
            created_time = cell_data.get('created_time')
            if created_time:
                try:
                    datetime.fromisoformat(created_time)
                except:
                    cell_issues.append({
                        'type': 'invalid_time_format',
                        'field': 'created_time',
                        'cell_id': cell_id,
                        'value': created_time
                    })
            
            # 自动修复
            if auto_fix and (cell_issues or cell_warnings):
                self._auto_fix_cell(cell_id, cell_data, cell_issues, cell_warnings)
            
            issues.extend(cell_issues)
            warnings.extend(cell_warnings)
            
            if not cell_issues:
                passed_count += 1
        
        return CheckResult(
            check_type=CheckType.DATA_INTEGRITY,
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_count=checked_count,
            passed_count=passed_count,
            timestamp=datetime.now().isoformat()
        )
    
    def check_reference_integrity(self, auto_fix: bool = False) -> CheckResult:
        """引用完整性检查"""
        issues = []
        warnings = []
        checked_count = 0
        passed_count = 0
        
        cells = self._load_all_cells()
        valid_ids = set(cells.keys())
        
        for cell_id, cell_data in cells.items():
            checked_count += 1
            cell_issues = []
            
            # 检查父引用
            parent_id = cell_data.get('parent_id')
            if parent_id and parent_id not in valid_ids:
                cell_issues.append({
                    'type': 'broken_parent_reference',
                    'cell_id': cell_id,
                    'referenced_id': parent_id
                })
            
            # 检查关联引用
            associations = cell_data.get('associations', [])
            broken_refs = []
            for assoc in associations:
                ref_id = assoc.get('cell_id') if isinstance(assoc, dict) else assoc
                if ref_id and ref_id not in valid_ids:
                    broken_refs.append(ref_id)
            
            if broken_refs:
                cell_issues.append({
                    'type': 'broken_association_references',
                    'cell_id': cell_id,
                    'broken_refs': broken_refs
                })
            
            # 自动修复
            if auto_fix and cell_issues:
                self._fix_broken_references(cell_id, cell_data, cell_issues)
            
            issues.extend(cell_issues)
            
            if not cell_issues:
                passed_count += 1
        
        return CheckResult(
            check_type=CheckType.REFERENCE_INTEGRITY,
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_count=checked_count,
            passed_count=passed_count,
            timestamp=datetime.now().isoformat()
        )
    
    def check_index_consistency(self, auto_fix: bool = False) -> CheckResult:
        """索引一致性检查"""
        issues = []
        warnings = []
        checked_count = 0
        passed_count = 0
        
        # 检查向量索引
        vector_index_path = os.path.join(self.memory_path, 'vectors', 'vector_index.json')
        cells = self._load_all_cells()
        valid_ids = set(cells.keys())
        
        if os.path.exists(vector_index_path):
            try:
                with open(vector_index_path, 'r') as f:
                    vector_index = json.load(f)
                
                checked_count += len(vector_index)
                
                for cell_id in vector_index:
                    if cell_id not in valid_ids:
                        issues.append({
                            'type': 'orphan_vector_index',
                            'cell_id': cell_id,
                            'message': '向量索引指向不存在的细胞'
                        })
                    else:
                        passed_count += 1
            except Exception as e:
                issues.append({
                    'type': 'index_read_error',
                    'message': str(e)
                })
        
        # 检查类型索引
        type_index_path = os.path.join(self.memory_path, 'type_index.json')
        if os.path.exists(type_index_path):
            try:
                with open(type_index_path, 'r') as f:
                    type_index = json.load(f)
                
                for cell_type, cell_ids in type_index.items():
                    for cell_id in cell_ids:
                        checked_count += 1
                        if cell_id not in valid_ids:
                            issues.append({
                                'type': 'orphan_type_index',
                                'cell_id': cell_id,
                                'cell_type': cell_type
                            })
                        else:
                            passed_count += 1
            except Exception as e:
                issues.append({
                    'type': 'type_index_read_error',
                    'message': str(e)
                })
        
        return CheckResult(
            check_type=CheckType.INDEX_CONSISTENCY,
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_count=checked_count,
            passed_count=passed_count,
            timestamp=datetime.now().isoformat()
        )
    
    def check_network_integrity(self, auto_fix: bool = False) -> CheckResult:
        """网络完整性检查"""
        issues = []
        warnings = []
        checked_count = 0
        passed_count = 0
        
        network_path = os.path.join(self.memory_path, 'network', 'connections.json')
        cells = self._load_all_cells()
        valid_ids = set(cells.keys())
        
        if os.path.exists(network_path):
            try:
                with open(network_path, 'r') as f:
                    network = json.load(f)
                
                for cell_id, connections in network.items():
                    checked_count += 1
                    
                    if cell_id not in valid_ids:
                        issues.append({
                            'type': 'orphan_network_node',
                            'cell_id': cell_id,
                            'message': '网络中的节点不存在于细胞库'
                        })
                        continue
                    
                    broken_connections = [c for c in connections if c not in valid_ids]
                    if broken_connections:
                        issues.append({
                            'type': 'broken_network_connections',
                            'cell_id': cell_id,
                            'broken_connections': broken_connections
                        })
                    
                    if not broken_connections:
                        passed_count += 1
            except Exception as e:
                issues.append({
                    'type': 'network_read_error',
                    'message': str(e)
                })
        
        return CheckResult(
            check_type=CheckType.NETWORK_INTEGRITY,
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_count=checked_count,
            passed_count=passed_count,
            timestamp=datetime.now().isoformat()
        )
    
    def check_orphans(self, auto_fix: bool = False) -> CheckResult:
        """孤儿检查"""
        issues = []
        warnings = []
        checked_count = 0
        passed_count = 0
        
        cells = self._load_all_cells()
        
        for cell_id, cell_data in cells.items():
            checked_count += 1
            
            # 检查是否完全没有连接
            has_connections = bool(cell_data.get('associations'))
            has_parent = bool(cell_data.get('parent_id'))
            access_count = cell_data.get('access_count', 0)
            created_time = cell_data.get('created_time', '')
            
            # 如果创建了很久但从未被访问，标记为潜在孤儿
            if not has_connections and not has_parent and access_count == 0:
                try:
                    age_days = (datetime.now() - datetime.fromisoformat(created_time)).days
                    if age_days > 30:
                        warnings.append({
                            'type': 'potential_orphan',
                            'cell_id': cell_id,
                            'age_days': age_days,
                            'message': '细胞孤立且从未被访问，可能需要清理或重新关联'
                        })
                except:
                    pass
            
            passed_count += 1
        
        return CheckResult(
            check_type=CheckType.ORPHAN_CHECK,
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_count=checked_count,
            passed_count=passed_count,
            timestamp=datetime.now().isoformat()
        )
    
    def _load_all_cells(self) -> Dict[str, Dict]:
        """加载所有细胞"""
        cells = {}
        
        for category in ['user', 'feedback', 'project', 'reference']:
            category_path = os.path.join(self.memory_path, category)
            if os.path.exists(category_path):
                for filename in os.listdir(category_path):
                    if filename.endswith('.json'):
                        filepath = os.path.join(category_path, filename)
                        try:
                            with open(filepath, 'r') as f:
                                data = json.load(f)
                                if isinstance(data, dict) and 'id' in data:
                                    cells[data['id']] = data
                        except:
                            pass
        
        return cells
    
    def _auto_fix_cell(self, cell_id: str, cell_data: Dict,
                       issues: List[Dict], warnings: List[Dict]) -> None:
        """自动修复细胞问题"""
        fixed = False
        
        for issue in issues:
            if issue['type'] == 'missing_field':
                # 添加默认值
                field = issue['field']
                if field == 'id':
                    cell_data['id'] = cell_id
                elif field == 'created_time':
                    cell_data['created_time'] = datetime.now().isoformat()
                elif field == 'type':
                    cell_data['type'] = 'unknown'
                elif field == 'content':
                    cell_data['content'] = ''
                fixed = True
            
            elif issue['type'] == 'energy_out_of_range':
                min_e, max_e = self.integrity_rules['energy_range']
                cell_data['energy'] = max(min_e, min(max_e, cell_data.get('energy', 1.0)))
                fixed = True
            
            elif issue['type'] == 'invalid_time_format':
                cell_data['created_time'] = datetime.now().isoformat()
                fixed = True
        
        if fixed:
            self.stats['total_auto_fixed'] += 1
            # 保存修复后的数据
            self._save_cell(cell_id, cell_data)
    
    def _fix_broken_references(self, cell_id: str, cell_data: Dict,
                               issues: List[Dict]) -> None:
        """修复断开的引用"""
        for issue in issues:
            if issue['type'] == 'broken_parent_reference':
                # 移除断开的父引用
                cell_data['parent_id'] = None
            
            elif issue['type'] == 'broken_association_references':
                # 移除断开的关联引用
                broken_refs = set(issue['broken_refs'])
                valid_associations = [
                    a for a in cell_data.get('associations', [])
                    if (a.get('cell_id') if isinstance(a, dict) else a) not in broken_refs
                ]
                cell_data['associations'] = valid_associations
        
        self._save_cell(cell_id, cell_data)
        self.stats['total_auto_fixed'] += 1
    
    def _save_cell(self, cell_id: str, cell_data: Dict) -> None:
        """保存细胞"""
        cell_type = cell_data.get('type', 'unknown')
        category = self._get_category_for_type(cell_type)
        
        category_path = os.path.join(self.memory_path, category)
        os.makedirs(category_path, exist_ok=True)
        
        filepath = os.path.join(category_path, f"{cell_id}.json")
        with open(filepath, 'w') as f:
            json.dump(cell_data, f, indent=2)
    
    def _get_category_for_type(self, cell_type: str) -> str:
        """获取类型对应的分类目录"""
        type_to_category = {
            'user': 'user',
            'feedback': 'feedback',
            'project': 'project',
            'reference': 'reference',
            'task': 'project',
            'knowledge': 'reference',
            'insight': 'reference',
            'problem': 'project',
            'solution': 'project'
        }
        return type_to_category.get(cell_type, 'reference')
    
    def _generate_recommendations(self, results: List[CheckResult]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        for result in results:
            if result.issues:
                if result.check_type == CheckType.DATA_INTEGRITY:
                    recommendations.append("建议运行自动修复以修复数据完整性问题")
                elif result.check_type == CheckType.REFERENCE_INTEGRITY:
                    recommendations.append("建议清理断开的引用或重新建立关联")
                elif result.check_type == CheckType.INDEX_CONSISTENCY:
                    recommendations.append("建议重建索引以确保一致性")
                elif result.check_type == CheckType.NETWORK_INTEGRITY:
                    recommendations.append("建议清理网络中的无效连接")
        
        return list(set(recommendations))
    
    def get_report(self) -> Dict:
        """获取报告"""
        return {
            'stats': self.stats,
            'last_check_passed': self.check_history[-1].overall_passed if self.check_history else None,
            'total_checks': len(self.check_history)
        }


def demo_consistency():
    """演示一致性检查"""
    print("=" * 60)
    print("记忆一致性校验演示")
    print("=" * 60)
    
    consistency = MemoryConsistency()
    
    print("\n运行完整检查...")
    report = consistency.run_full_check(auto_fix=True)
    
    print(f"\n检查结果: {'通过' if report.overall_passed else '发现问题'}")
    print(f"问题数: {report.total_issues}")
    print(f"警告数: {report.total_warnings}")
    
    for result in report.check_results:
        status = "✓" if result.passed else "✗"
        print(f"\n{status} {result.check_type.value}:")
        print(f"   检查数: {result.checked_count}, 通过: {result.passed_count}")
        if result.issues:
            print(f"   问题: {len(result.issues)}")
        if result.warnings:
            print(f"   警告: {len(result.warnings)}")
    
    if report.recommendations:
        print("\n建议:")
        for rec in report.recommendations:
            print(f"  - {rec}")


if __name__ == "__main__":
    demo_consistency()

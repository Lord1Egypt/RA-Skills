#!/usr/bin/env python3
"""
Pharma CSV Pro - 专业药品分析工具
支持批记录分析、稳定性研究、质量控制、合规性检查
"""

import pandas as pd
import numpy as np
import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class PharmaAnalyzerPro:
    """专业药品 CSV 分析器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.columns = {}
        self.results = {
            'file': file_path,
            'analysis_date': datetime.now().isoformat(),
            'summary': {},
            'statistics': {},
            'compliance': {},
            'oos_oos': [],
            'trends': {},
            'errors': []
        }
        
    def load_data(self) -> bool:
        """加载 CSV 数据"""
        try:
            self.df = pd.read_csv(self.file_path)
            self._detect_columns()
            self.results['summary']['rows'] = len(self.df)
            self.results['summary']['columns'] = list(self.df.columns)
            return True
        except Exception as e:
            self.results['errors'].append(f'加载数据失败: {str(e)}')
            return False
    
    def _detect_columns(self):
        """自动识别药品相关列"""
        col_lower = {col.lower(): col for col in self.df.columns}
        
        # 批次号
        for key in ['batch', 'lot', 'batch_number', 'batch_no']:
            if key in col_lower:
                self.columns['batch'] = col_lower[key]
                break
        
        # 含量/效价
        for key in ['assay', 'potency', 'content', 'strength']:
            if key in col_lower:
                self.columns['assay'] = col_lower[key]
                break
        
        # 杂质
        for key in ['impurity', 'related_substances', 'degradation', 'impurities']:
            if key in col_lower:
                self.columns['impurity'] = col_lower[key]
                break
        
        # 溶出度
        for key in ['dissolution', 'dt', 'disintegration']:
            if key in col_lower:
                self.columns['dissolution'] = col_lower[key]
                break
        
        # 日期
        for key in ['date', 'test_date', 'manufacturing_date', 'expiry']:
            if key in col_lower:
                self.columns['date'] = col_lower[key]
                break
        
        # 存储条件
        for key in ['storage', 'condition', 'temp', 'temperature']:
            if key in col_lower:
                self.columns['storage'] = col_lower[key]
                break
    
    def validate_data(self) -> Dict:
        """数据验证"""
        validation = {
            'missing_data': {},
            'data_types': {},
            'outliers': []
        }
        
        # 检查缺失值
        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing > 0:
                validation['missing_data'][col] = missing
        
        # 检查异常值（数值列）
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < Q1 - 1.5*IQR) | (self.df[col] > Q3 + 1.5*IQR)]
            if len(outliers) > 0:
                validation['outliers'].append({
                    'column': col,
                    'count': len(outliers),
                    'indices': outliers.index.tolist()[:5]  # 只显示前5个
                })
        
        self.results['validation'] = validation
        return validation
    
    def calculate_statistics(self) -> Dict:
        """计算统计摘要"""
        stats = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_stats = {
                'count': int(self.df[col].count()),
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q1': float(self.df[col].quantile(0.25)),
                'median': float(self.df[col].quantile(0.5)),
                'q3': float(self.df[col].quantile(0.75))
            }
            
            # 计算 Cpk（如果有规格限制）
            if col in self.columns.values():
                usl, lsl = self._get_spec_limits(col)
                if usl is not None and lsl is not None:
                    col_stats['cpk'] = self._calculate_cpk(self.df[col], usl, lsl)
            
            stats[col] = col_stats
        
        self.results['statistics'] = stats
        return stats
    
    def _get_spec_limits(self, col: str) -> Tuple[Optional[float], Optional[float]]:
        """获取规格限制（根据列名推断）"""
        col_lower = col.lower()
        
        if 'assay' in col_lower or 'potency' in col_lower or 'content' in col_lower:
            return 105.0, 95.0  # 含量通常 95-105%
        elif 'impurity' in col_lower:
            return 0.5, 0.0  # 杂质通常 <0.5%
        elif 'dissolution' in col_lower:
            return 100.0, 75.0  # 溶出度通常 Q=75%
        
        return None, None
    
    def _calculate_cpk(self, series: pd.Series, usl: float, lsl: float) -> float:
        """计算过程能力指数 Cpk"""
        mean = series.mean()
        std = series.std()
        
        if std == 0:
            return float('inf')
        
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        
        return min(cpu, cpl)
    
    def check_compliance(self, standard: str = 'USP') -> Dict:
        """合规性检查"""
        compliance = {
            'standard': standard,
            'checks': [],
            'passed': True
        }
        
        # 根据标准检查
        if 'assay' in self.columns:
            col = self.columns['assay']
            values = self.df[col]
            
            if standard == 'USP':
                usl, lsl = 105.0, 95.0
            elif standard == 'EP':
                usl, lsl = 105.0, 95.0
            elif standard == 'ChP':
                usl, lsl = 105.0, 95.0
            else:
                usl, lsl = 105.0, 95.0
            
            out_of_spec = values[(values > usl) | (values < lsl)]
            
            compliance['checks'].append({
                'parameter': 'Assay',
                'specification': f'{lsl} - {usl}',
                'tested': len(values),
                'passed': len(values) - len(out_of_spec),
                'failed': len(out_of_spec),
                'pass_rate': f"{(len(values) - len(out_of_spec)) / len(values) * 100:.1f}%"
            })
            
            if len(out_of_spec) > 0:
                compliance['passed'] = False
        
        self.results['compliance'] = compliance
        return compliance
    
    def detect_oos(self) -> List[Dict]:
        """检测 OOS (Out of Specification)"""
        oos_list = []
        
        for key, col in self.columns.items():
            if key in ['assay', 'impurity', 'dissolution']:
                usl, lsl = self._get_spec_limits(col)
                if usl is None:
                    continue
                
                values = self.df[col]
                out_of_spec = self.df[(values > usl) | (values < lsl)]
                
                for idx, row in out_of_spec.iterrows():
                    oos = {
                        'row_index': int(idx),
                        'parameter': col,
                        'value': float(row[col]),
                        'specification': f'{lsl} - {usl}',
                        'deviation': 'High' if row[col] > usl else 'Low',
                        'batch': row.get(self.columns.get('batch', ''), f'Row_{idx}')
                    }
                    oos_list.append(oos)
        
        self.results['oos_oos'] = oos_list
        return oos_list
    
    def analyze_trends(self, time_col: Optional[str] = None) -> Dict:
        """趋势分析"""
        trends = {}
        
        # 使用时间列或索引
        if time_col is None and 'date' in self.columns:
            time_col = self.columns['date']
        
        if time_col and time_col in self.df.columns:
            try:
                self.df[time_col] = pd.to_datetime(self.df[time_col])
                df_sorted = self.df.sort_values(time_col)
                
                for key, col in self.columns.items():
                    if key in ['assay', 'impurity', 'dissolution']:
                        # 简单线性回归
                        x = np.arange(len(df_sorted))
                        y = df_sorted[col].values
                        
                        # 计算斜率
                        slope = np.polyfit(x, y, 1)[0]
                        
                        trends[col] = {
                            'slope': float(slope),
                            'trend': 'Increasing' if slope > 0.01 else 'Decreasing' if slope < -0.01 else 'Stable',
                            'r_squared': float(np.corrcoef(x, y)[0, 1]**2) if len(x) > 1 else 0
                        }
            except:
                pass
        
        self.results['trends'] = trends
        return trends
    
    def generate_report(self, output_format: str = 'json') -> str:
        """生成报告"""
        if output_format == 'json':
            return json.dumps(self.results, indent=2, ensure_ascii=False)
        
        elif output_format == 'markdown':
            md = f"""# Pharma CSV Pro 分析报告

## 文件信息
- **文件**: {self.results['file']}
- **分析时间**: {self.results['analysis_date']}
- **数据行数**: {self.results['summary'].get('rows', 0)}

## 统计摘要
"""
            for col, stats in self.results['statistics'].items():
                md += f"\n### {col}\n"
                md += f"- 均值: {stats['mean']:.2f}\n"
                md += f"- 标准差: {stats['std']:.2f}\n"
                md += f"- 范围: {stats['min']:.2f} - {stats['max']:.2f}\n"
                if 'cpk' in stats:
                    md += f"- Cpk: {stats['cpk']:.2f}\n"
            
            # OOS 部分
            if self.results['oos_oos']:
                md += "\n## OOS/OOT 检测结果\n"
                md += f"**发现 {len(self.results['oos_oos'])} 个异常**\n\n"
                for oos in self.results['oos_oos'][:10]:  # 只显示前10个
                    md += f"- {oos['parameter']}: {oos['value']:.2f} ({oos['deviation']})\n"
            
            # 合规性
            if self.results['compliance']:
                md += "\n## 合规性检查\n"
                md += f"**标准**: {self.results['compliance']['standard']}\n"
                md += f"**结果**: {'通过' if self.results['compliance']['passed'] else '未通过'}\n"
            
            return md
        
        else:
            return json.dumps(self.results, indent=2, ensure_ascii=False)
    
    def run_full_analysis(self, standard: str = 'USP', detect_oos: bool = True, 
                         trend_analysis: bool = True) -> Dict:
        """运行完整分析"""
        if not self.load_data():
            return self.results
        
        # 数据验证
        self.validate_data()
        
        # 统计计算
        self.calculate_statistics()
        
        # 合规性检查
        self.check_compliance(standard)
        
        # OOS 检测
        if detect_oos:
            self.detect_oos()
        
        # 趋势分析
        if trend_analysis:
            self.analyze_trends()
        
        return self.results


def main():
    parser = argparse.ArgumentParser(description='Pharma CSV Pro - 专业药品分析工具')
    parser.add_argument('file', help='CSV 文件路径')
    parser.add_argument('--standard', choices=['USP', 'EP', 'ChP'], default='USP',
                       help='合规标准 (默认: USP)')
    parser.add_argument('--study-type', choices=['batch', 'stability', 'qc', 'method-validation'],
                       default='batch', help='研究类型')
    parser.add_argument('--detect-oos', action='store_true', help='检测 OOS/OOT')
    parser.add_argument('--trend-analysis', action='store_true', help='趋势分析')
    parser.add_argument('--output', choices=['json', 'markdown'], default='json',
                       help='输出格式')
    parser.add_argument('--output-file', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = PharmaAnalyzerPro(args.file)
    
    # 运行分析
    results = analyzer.run_full_analysis(
        standard=args.standard,
        detect_oos=args.detect_oos,
        trend_analysis=args.trend_analysis
    )
    
    # 生成报告
    report = analyzer.generate_report(args.output)
    
    # 输出
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {args.output_file}")
    else:
        print(report)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
数据处理工具：数据清洗、数据分析、批量评分、报告生成
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# 尝试导入pandas和numpy
try:
    import pandas as pd
    import numpy as np
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("警告：pandas 未安装，将使用基础数据处理", file=sys.stderr)


def clean_data(data):
    """数据清洗：处理缺失值、异常值、重复值"""
    if not HAS_PANDAS:
        # 基础清洗
        cleaned = []
        for item in data:
            if isinstance(item, dict):
                # 移除空值
                cleaned_item = {k: v for k, v in item.items() if v is not None and v != ''}
                cleaned.append(cleaned_item)
        return cleaned

    # pandas 清洗
    df = pd.DataFrame(data)

    # 处理缺失值
    df = df.dropna(how='all')  # 删除全为空的行

    # 处理重复值
    df = df.drop_duplicates()

    # 处理数值异常值（使用IQR方法）
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

    return df.to_dict('records')


def analyze_data(data):
    """数据分析：统计、相关性、趋势"""
    if not HAS_PANDAS:
        # 基础分析
        analysis = {
            "total_count": len(data),
            "sample": data[:3] if len(data) >= 3 else data
        }
        return analysis

    df = pd.DataFrame(data)

    analysis = {
        "total_count": len(df),
        "columns": list(df.columns),
        "numeric_stats": {},
        "correlation": {},
        "distribution": {}
    }

    # 数值统计
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        analysis["numeric_stats"][col] = {
            "count": int(df[col].count()),
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "median": float(df[col].median())
        }

    # 相关性分析
    if len(numeric_columns) > 1:
        corr_matrix = df[numeric_columns].corr()
        for col1 in numeric_columns:
            for col2 in numeric_columns:
                if col1 != col2:
                    analysis["correlation"][f"{col1}_vs_{col2}"] = float(corr_matrix.loc[col1, col2])

    # 分布分析
    for col in numeric_columns:
        try:
            analysis["distribution"][col] = {
                "quartiles": {
                    "25%": float(df[col].quantile(0.25)),
                    "50%": float(df[col].quantile(0.50)),
                    "75%": float(df[col].quantile(0.75))
                }
            }
        except:
            pass

    return analysis


def batch_scoring(items, scoring_function='crs'):
    """批量评分：CRS、LRS、综合评分"""
    scores = []

    for item in items:
        if scoring_function == 'crs':
            # CRS（骗局风险评分）
            revenue_source = item.get('revenue_source', 1)
            risk_identification = item.get('risk_identification', 1)
            cognitive_threshold = item.get('cognitive_threshold', 1)
            trust_building = item.get('trust_building', 1)
            liquidity = item.get('liquidity', 1)
            information = item.get('information_transparency', 1)

            crs_score = (revenue_source + risk_identification + cognitive_threshold +
                        trust_building + liquidity + information) * 100 / 12

            if crs_score >= 80:
                risk_level = 'critical'
            elif crs_score >= 60:
                risk_level = 'high'
            elif crs_score >= 40:
                risk_level = 'moderate'
            else:
                risk_level = 'low'

            scores.append({
                'name': item.get('name', 'unknown'),
                'crs_score': round(crs_score, 2),
                'risk_level': risk_level
            })

        elif scoring_function == 'lrs':
            # LRS（流动性风险评分）
            withdrawal_difficulty = item.get('withdrawal_difficulty', 1)
            lock_period = item.get('lock_period', 1)
            order_depth = item.get('order_depth', 1)
            slippage = item.get('slippage', 1)

            lrs_score = (withdrawal_difficulty + lock_period + order_depth + slippage) * 100 / 12

            if lrs_score >= 80:
                risk_level = 'critical'
            elif lrs_score >= 60:
                risk_level = 'severe'
            elif lrs_score >= 40:
                risk_level = 'moderate'
            else:
                risk_level = 'low'

            scores.append({
                'name': item.get('name', 'unknown'),
                'lrs_score': round(lrs_score, 2),
                'risk_level': risk_level
            })

        elif scoring_function == 'comprehensive':
            # 综合评分
            revenue_source = item.get('revenue_source', 1)
            risk_identification = item.get('risk_identification', 1)
            cognitive_threshold = item.get('cognitive_threshold', 1)
            trust_building = item.get('trust_building', 1)
            liquidity = item.get('liquidity', 1)
            information = item.get('information_transparency', 1)

            withdrawal_difficulty = item.get('withdrawal_difficulty', 1)
            lock_period = item.get('lock_period', 1)
            order_depth = item.get('order_depth', 1)
            slippage = item.get('slippage', 1)

            crs_score = (revenue_source + risk_identification + cognitive_threshold +
                        trust_building + liquidity + information) * 100 / 12

            lrs_score = (withdrawal_difficulty + lock_period + order_depth + slippage) * 100 / 12

            # 综合评分：CRS权重60%，LRS权重40%
            comprehensive_score = crs_score * 0.6 + lrs_score * 0.4

            if comprehensive_score >= 75:
                risk_level = 'critical'
                recommendation = '立即拒绝'
            elif comprehensive_score >= 60:
                risk_level = 'high'
                recommendation = '强烈不推荐'
            elif comprehensive_score >= 40:
                risk_level = 'moderate'
                recommendation = '谨慎考虑'
            else:
                risk_level = 'low'
                recommendation = '可以考虑'

            scores.append({
                'name': item.get('name', 'unknown'),
                'crs_score': round(crs_score, 2),
                'lrs_score': round(lrs_score, 2),
                'comprehensive_score': round(comprehensive_score, 2),
                'risk_level': risk_level,
                'recommendation': recommendation
            })

    return scores


def generate_report(analysis, scores, output_file, format='markdown'):
    """生成报告：Markdown或HTML格式"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if format == 'markdown':
        report = f"""# 骗局风险分析报告

**生成时间**: {timestamp}

## 分析概览

- **总项目数**: {analysis.get('total_count', 0)}
- **分析字段**: {', '.join(analysis.get('columns', []))}

## 风险评分结果

"""

        # 按风险等级分组
        critical_items = [s for s in scores if s.get('risk_level') == 'critical']
        high_items = [s for s in scores if s.get('risk_level') == 'high']
        moderate_items = [s for s in scores if s.get('risk_level') == 'moderate']
        low_items = [s for s in scores if s.get('risk_level') == 'low']

        report += f"""
### 风险分布

- **严重风险**: {len(critical_items)} 个
- **高风险**: {len(high_items)} 个
- **中等风险**: {len(moderate_items)} 个
- **低风险**: {len(low_items)} 个

### 详细评分

"""

        # 列出所有评分
        for item in sorted(scores, key=lambda x: x.get('comprehensive_score', 0), reverse=True):
            name = item.get('name', 'unknown')
            score = item.get('comprehensive_score', item.get('crs_score', item.get('lrs_score', 0)))
            risk_level = item.get('risk_level', 'unknown')
            recommendation = item.get('recommendation', '')

            report += f"""
#### {name}

- **综合评分**: {score:.1f}/100
- **风险等级**: {risk_level.upper()}
- **建议**: {recommendation}

"""

        # 数值统计
        if 'numeric_stats' in analysis:
            report += """
## 数值统计

"""
            for col, stats in analysis['numeric_stats'].items():
                report += f"""
### {col}

- **均值**: {stats.get('mean', 0):.2f}
- **标准差**: {stats.get('std', 0):.2f}
- **最小值**: {stats.get('min', 0):.2f}
- **最大值**: {stats.get('max', 0):.2f}
- **中位数**: {stats.get('median', 0):.2f}

"""

        report += """
## 建议

1. **优先处理严重风险项目**: 立即拒绝，避免任何投入
2. **谨慎对待高风险项目**: 深入调查，验证所有信息
3. **关注中等风险项目**: 分散风险，小规模试水
4. **可以参考低风险项目**: 但仍需持续监控

---

*本报告由 scam-insight 技能自动生成*
"""

    elif format == 'html':
        report = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>骗局风险分析报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .critical {{ color: #ff0000; font-weight: bold; }}
        .high {{ color: #ff6600; font-weight: bold; }}
        .moderate {{ color: #ffcc00; font-weight: bold; }}
        .low {{ color: #00cc00; font-weight: bold; }}
        .item-card {{
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            background: #f9f9f9;
        }}
        .risk-critical {{ border-left: 4px solid #ff0000; }}
        .risk-high {{ border-left: 4px solid #ff6600; }}
        .risk-moderate {{ border-left: 4px solid #ffcc00; }}
        .risk-low {{ border-left: 4px solid #00cc00; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>骗局风险分析报告</h1>
        <p>生成时间: {timestamp}</p>
    </div>

    <h2>分析概览</h2>
    <p><strong>总项目数:</strong> {analysis.get('total_count', 0)}</p>
    <p><strong>分析字段:</strong> {', '.join(analysis.get('columns', []))}</p>

    <h2>风险评分结果</h2>

    <h3>风险分布</h3>
    <ul>
        <li><span class="critical">严重风险:</span> {len([s for s in scores if s.get('risk_level') == 'critical'])} 个</li>
        <li><span class="high">高风险:</span> {len([s for s in scores if s.get('risk_level') == 'high'])} 个</li>
        <li><span class="moderate">中等风险:</span> {len([s for s in scores if s.get('risk_level') == 'moderate'])} 个</li>
        <li><span class="low">低风险:</span> {len([s for s in scores if s.get('risk_level') == 'low'])} 个</li>
    </ul>

    <h3>详细评分</h3>
"""

        # 列出所有评分
        for item in sorted(scores, key=lambda x: x.get('comprehensive_score', 0), reverse=True):
            name = item.get('name', 'unknown')
            score = item.get('comprehensive_score', item.get('crs_score', item.get('lrs_score', 0)))
            risk_level = item.get('risk_level', 'unknown')
            recommendation = item.get('recommendation', '')

            report += f"""
    <div class="item-card risk-{risk_level}">
        <h4>{name}</h4>
        <p><strong>综合评分:</strong> {score:.1f}/100</p>
        <p><strong>风险等级:</strong> <span class="{risk_level}">{risk_level.upper()}</span></p>
        <p><strong>建议:</strong> {recommendation}</p>
    </div>
"""

        report += """
    <h2>建议</h2>
    <ol>
        <li><strong>优先处理严重风险项目:</strong> 立即拒绝，避免任何投入</li>
        <li><strong>谨慎对待高风险项目:</strong> 深入调查，验证所有信息</li>
        <li><strong>关注中等风险项目:</strong> 分散风险，小规模试水</li>
        <li><strong>可以参考低风险项目:</strong> 但仍需持续监控</li>
    </ol>

    <p style="text-align: center; color: #999; margin-top: 50px;">
        <em>本报告由 scam-insight 技能自动生成</em>
    </p>
</body>
</html>
"""

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"报告已生成：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='骗局洞察数据处理工具')
    parser.add_argument('--input', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--task', required=True,
                       choices=['clean', 'analyze', 'score_crs', 'score_lrs', 'score_comprehensive', 'report'],
                       help='任务类型')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', default='markdown', choices=['markdown', 'html'],
                       help='报告格式（仅用于report任务）')

    args = parser.parse_args()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    # 执行任务
    try:
        result = {}

        if args.task == 'clean':
            cleaned = clean_data(data)
            result = {
                "status": "success",
                "task": "clean",
                "original_count": len(data),
                "cleaned_count": len(cleaned),
                "output_file": args.output
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(cleaned, f, ensure_ascii=False, indent=2)

        elif args.task == 'analyze':
            analysis = analyze_data(data)
            result = {
                "status": "success",
                "task": "analyze",
                "output_file": args.output
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)

        elif args.task in ['score_crs', 'score_lrs', 'score_comprehensive']:
            scoring_function = args.task.replace('score_', '')
            scores = batch_scoring(data, scoring_function)
            result = {
                "status": "success",
                "task": f"score_{scoring_function}",
                "scored_count": len(scores),
                "output_file": args.output
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)

        elif args.task == 'report':
            analysis = analyze_data(data)
            scores = batch_scoring(data, 'comprehensive')
            generate_report(analysis, scores, args.output, args.format)
            result = {
                "status": "success",
                "task": "report",
                "format": args.format,
                "output_file": args.output
            }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"错误：任务执行失败 - {e}", file=sys.stderr)
        result = {
            "status": "error",
            "task": args.task,
            "message": str(e)
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

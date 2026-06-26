#!/usr/bin/env python3
"""
Export Glucose Analysis Report
Export reports in various formats (HTML, PDF, JSON)
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Export glucose analysis reports'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['html', 'json', 'txt'],
        default='html',
        help='Export format (default: html)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path'
    )
    
    parser.add_argument(
        '--period', '-p',
        type=str,
        choices=['week', 'month', 'quarter', 'all'],
        default='month',
        help='Report period (default: month)'
    )
    
    return parser.parse_args()


def generate_html_report(readings: list, stats: dict) -> str:
    """Generate HTML format report"""
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>血糖分析报告</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .range-bar {{
            background: #ecf0f1;
            height: 30px;
            border-radius: 15px;
            margin: 10px 0;
            position: relative;
            overflow: hidden;
        }}
        .range-segment {{
            height: 100%;
            display: inline-block;
            text-align: center;
            line-height: 30px;
            color: white;
            font-weight: bold;
        }}
        .range-low {{ background: #e74c3c; }}
        .range-normal {{ background: #27ae60; }}
        .range-high {{ background: #f39c12; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 血糖分析报告</h1>
        <p><strong>报告日期:</strong> {datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
        
        <h2>总体概况</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总记录数</div>
                <div class="stat-value">{stats['count']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">平均血糖</div>
                <div class="stat-value">{stats['mean']:.1f}</div>
                <div class="stat-label">mmol/L</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">血糖范围</div>
                <div class="stat-value">{stats['min']:.1f}-{stats['max']:.1f}</div>
                <div class="stat-label">mmol/L</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">变异系数</div>
                <div class="stat-value">{stats['cv']:.1f}%</div>
            </div>
        </div>
        
        <h2>目标范围内时间 (TIR)</h2>
        <p><strong>目标范围:</strong> 4.0-10.0 mmol/L</p>
        <div class="range-bar">
            <span class="range-segment range-low" style="width: {stats['time_in_range']['below_range']:.1f}%">
                {stats['time_in_range']['below_range']:.0f}%
            </span>
            <span class="range-segment range-normal" style="width: {stats['time_in_range']['in_range']:.1f}%">
                {stats['time_in_range']['in_range']:.0f}%
            </span>
            <span class="range-segment range-high" style="width: {stats['time_in_range']['above_range']:.1f}%">
                {stats['time_in_range']['above_range']:.0f}%
            </span>
        </div>
        <ul>
            <li><span style="color: #27ae60;">✓</span> 目标范围内: {stats['time_in_range']['in_range']:.1f}%</li>
            <li><span style="color: #e74c3c;">!</span> 低于目标: {stats['time_in_range']['below_range']:.1f}%</li>
            <li><span style="color: #f39c12;">!</span> 高于目标: {stats['time_in_range']['above_range']:.1f}%</li>
        </ul>
        
        <h2>最近记录</h2>
        <table>
            <thead>
                <tr>
                    <th>时间</th>
                    <th>血糖值</th>
                    <th>用餐情况</th>
                    <th>备注</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # Add recent readings
    for reading in readings[-10:]:  # Last 10 readings
        timestamp = reading.get('timestamp', 'N/A')
        if timestamp != 'N/A':
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        value = reading.get('value', 'N/A')
        unit = reading.get('unit', 'mmol/L')
        meal_context = reading.get('meal_context', '-')
        notes = reading.get('notes', '-')
        
        html += f"""
                <tr>
                    <td>{timestamp}</td>
                    <td>{value} {unit}</td>
                    <td>{meal_context}</td>
                    <td>{notes}</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
        
        <div class="warning">
            <strong>⚠️ 医疗免责声明:</strong> 本报告仅供参考,不构成医疗建议。
            在调整治疗方案前,请务必咨询您的医疗保健提供者。
        </div>
        
        <div class="footer">
            <p>此报告由 Blood Glucose Manager 自动生成</p>
            <p>生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Main export function"""
    args = parse_args()
    
    # Load data
    manager = GlucoseDataManager()
    readings = manager.get_readings()
    stats = manager.get_statistics()
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = {'html': 'html', 'json': 'json', 'txt': 'txt'}[args.format]
        output_path = Path(f'glucose_report_{timestamp}.{ext}')
    
    print(f"\nGenerating {args.format.upper()} report...")
    
    if args.format == 'html':
        html = generate_html_report(readings, stats)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ HTML report saved to: {output_path}")
    
    elif args.format == 'json':
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'period': args.period,
            'statistics': stats,
            'readings': readings
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"✓ JSON report saved to: {output_path}")
    
    elif args.format == 'txt':
        # Generate text report
        txt = f"血糖分析报告\n{'='*60}\n\n"
        txt += f"报告日期: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n\n"
        txt += f"统计概览:\n"
        txt += f"  总记录数: {stats['count']}\n"
        txt += f"  平均血糖: {stats['mean']:.1f} mmol/L\n"
        txt += f"  血糖范围: {stats['min']:.1f} - {stats['max']:.1f} mmol/L\n"
        txt += f"  变异系数: {stats['cv']:.1f}%\n\n"
        txt += f"目标范围内时间:\n"
        txt += f"  目标范围: {stats['time_in_range']['in_range']:.1f}%\n"
        txt += f"  低于目标: {stats['time_in_range']['below_range']:.1f}%\n"
        txt += f"  高于目标: {stats['time_in_range']['above_range']:.1f}%\n\n"
        txt += f"免责声明: 本报告仅供参考,不构成医疗建议。\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(txt)
        print(f"✓ Text report saved to: {output_path}")
    
    print(f"\n✓ Report generation complete!")


if __name__ == "__main__":
    main()

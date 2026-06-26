#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商业模式画布雷达图生成脚本
用于生成九维度评分的可视化雷达图

使用方法:
    python generate_radar.py --input scores.json --output radar.png
    python generate_radar.py --input scores.json --output radar.png --format html
"""

import json
import argparse
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Patch
except ImportError:
    print("错误：需要安装matplotlib库")
    print("请运行: pip install matplotlib numpy")
    sys.exit(1)


def load_scores(input_path):
    """加载评分数据"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 验证数据完整性
    required_dims = [
        "客户细分", "价值主张", "渠道通路", "客户关系",
        "收入来源", "核心资源", "关键业务", "重要合作", "成本结构"
    ]
    
    if "dimensions" not in data or "scores" not in data:
        raise ValueError("数据格式错误：需要包含 'dimensions' 和 'scores' 字段")
    
    if len(data["dimensions"]) != 9 or len(data["scores"]) != 9:
        raise ValueError("数据格式错误：需要9个维度的数据")
    
    return data


def calculate_average(scores):
    """计算平均分"""
    return sum(scores) / len(scores)


def get_rating(average):
    """根据平均分获取评级"""
    if average >= 8:
        return "A", "商业模式成熟"
    elif average >= 6:
        return "B", "商业模式基本成立"
    elif average >= 4:
        return "C", "存在重大缺陷"
    else:
        return "D", "商业模式不成立"


def get_rating_color(rating):
    """根据评级获取颜色"""
    colors = {
        "A": "#00ff88",  # 绿色
        "B": "#ffdd00",  # 黄色
        "C": "#ff8800",  # 橙色
        "D": "#ff4444"   # 红色
    }
    return colors.get(rating, "#ffffff")


def create_radar_chart(data, output_path, file_format='png'):
    """创建雷达图"""
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 提取数据
    dimensions = data.get("dimensions", [
        "客户细分", "价值主张", "渠道通路", "客户关系",
        "收入来源", "核心资源", "关键业务", "重要合作", "成本结构"
    ])
    scores = data.get("scores", [])
    project_name = data.get("project_name", "商业计划书分析")
    analysis_date = data.get("analysis_date", "")
    
    # 计算综合评分
    average = calculate_average(scores)
    rating, rating_desc = get_rating(average)
    rating_color = get_rating_color(rating)
    
    # 创建图表
    fig = plt.figure(figsize=(12, 10), facecolor='#0a1628')
    
    # 创建雷达图
    ax = fig.add_subplot(111, polar=True, facecolor='#0a1628')
    
    # 雷达图参数
    num_vars = len(dimensions)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形
    
    # 分数列表闭合
    values = scores + scores[:1]
    
    # 绘制雷达图
    ax.fill(angles, values, color='#0096ff', alpha=0.3)
    ax.plot(angles, values, color='#0096ff', linewidth=2, marker='o', markersize=8)
    
    # 绘制刻度圆
    for level in [2, 4, 6, 8, 10]:
        ax.plot(angles, [level] * (num_vars + 1), color='rgba(255,255,255,0.2)', linewidth=0.5, linestyle='--')
    
    # 设置维度标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, size=11, color='white', fontweight='bold')
    
    # 在数据点上显示分数
    for i, (angle, value) in enumerate(zip(angles[:-1], values[:-1])):
        ax.annotate(f'{value:.0f}', xy=(angle, value), xytext=(angle, value + 0.5),
                   ha='center', va='bottom', fontsize=10, color='#0096ff', fontweight='bold')
    
    # 设置径向刻度
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], size=9, color='rgba(255,255,255,0.6)')
    
    # 设置网格
    ax.xaxis.grid(True, color='rgba(255,255,255,0.2)', linestyle='-', linewidth=0.5)
    ax.yaxis.grid(True, color='rgba(255,255,255,0.2)', linestyle='-', linewidth=0.5)
    ax.spines['polar'].set_color('rgba(255,255,255,0.3)')
    ax.spines['inner'].set_color('#0a1628')
    
    # 添加标题
    plt.title(f'{project_name}\n商业模式评分雷达图', 
              size=16, color='white', fontweight='bold', pad=20)
    
    # 添加综合评分中心显示
    fig.text(0.5, 0.45, f'{average:.2f}', fontsize=36, fontweight='bold', 
             color=rating_color, ha='center', va='center')
    fig.text(0.5, 0.38, f'评级：{rating}', fontsize=14, fontweight='bold', 
             color=rating_color, ha='center', va='center')
    fig.text(0.5, 0.33, rating_desc, fontsize=10, 
             color='rgba(255,255,255,0.7)', ha='center', va='center')
    
    # 添加日期
    if analysis_date:
        fig.text(0.5, 0.08, f'分析日期：{analysis_date}', fontsize=10, 
                 color='rgba(255,255,255,0.5)', ha='center', va='center')
    
    # 添加图例说明
    legend_text = """
    评分标准：
    A (8-10分)：商业模式成熟，具备规模化条件
    B (6-7分)：商业模式基本成立，需补短板
    C (4-5分)：存在重大缺陷，需重新设计
    D (1-3分)：商业模式不成立
    """
    fig.text(0.5, 0.02, legend_text.strip(), fontsize=8, 
             color='rgba(255,255,255,0.5)', ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='rgba(30,74,122,0.3)', alpha=0.5))
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_path, format=file_format, facecolor='#0a1628', 
                edgecolor='none', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"雷达图已生成：{output_path}")
    return output_path


def create_html_report(data, output_path):
    """生成HTML报告（包含echart雷达图）"""
    
    dimensions = data.get("dimensions", [
        "客户细分", "价值主张", "渠道通路", "客户关系",
        "收入来源", "核心资源", "关键业务", "重要合作", "成本结构"
    ])
    scores = data.get("scores", [])
    project_name = data.get("project_name", "商业计划书分析")
    analysis_date = data.get("analysis_date", "")
    
    average = calculate_average(scores)
    rating, rating_desc = get_rating(average)
    rating_color = get_rating_color(rating)
    
    # 构建echart配置
    indicator_config = []
    for dim in dimensions:
        indicator_config.append({"name": dim, "max": 10})
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - 商业模式分析报告</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", -apple-system, sans-serif;
            background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 100%);
            min-height: 100vh;
            color: #e0e0e0;
            line-height: 1.8;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(30, 74, 122, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(0, 150, 255, 0.3);
        }}
        .header h1 {{ color: #0096ff; font-size: 28px; margin-bottom: 10px; }}
        .header .subtitle {{ color: #80bfff; font-size: 14px; }}
        .main-content {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        .chart-section {{
            flex: 1;
            min-width: 500px;
            background: rgba(10, 22, 40, 0.8);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(0, 150, 255, 0.3);
        }}
        .score-section {{
            flex: 0 0 300px;
            background: rgba(10, 22, 40, 0.8);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(0, 150, 255, 0.3);
            text-align: center;
        }}
        .big-score {{
            font-size: 72px;
            font-weight: bold;
            color: {rating_color};
            margin: 20px 0;
        }}
        .rating {{
            font-size: 24px;
            font-weight: bold;
            color: {rating_color};
            margin-bottom: 10px;
        }}
        .rating-desc {{
            font-size: 14px;
            color: rgba(255,255,255,0.7);
            margin-bottom: 30px;
        }}
        .score-table {{
            width: 100%;
            margin-top: 30px;
            border-collapse: collapse;
        }}
        .score-table th, .score-table td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 150, 255, 0.2);
        }}
        .score-table th {{ color: #0096ff; font-weight: normal; }}
        .score-table td:last-child {{
            text-align: right;
            color: #0096ff;
            font-weight: bold;
        }}
        .score-high {{ color: #00ff88 !important; }}
        .score-low {{ color: #ff4444 !important; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: rgba(255,255,255,0.5);
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .main-content {{ flex-direction: column; }}
            .chart-section {{ min-width: 100%; }}
            .score-section {{ flex: 1; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{project_name}</h1>
            <div class="subtitle">商业模式画布九维度评分分析</div>
            <div class="subtitle">分析日期：{analysis_date}</div>
        </div>
        
        <div class="main-content">
            <div class="chart-section">
                <div id="radarChart" style="width: 100%; height: 500px;"></div>
            </div>
            
            <div class="score-section">
                <div class="rating">评级：{rating}</div>
                <div class="rating-desc">{rating_desc}</div>
                <div class="big-score">{average:.2f}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 14px;">综合评分</div>
                
                <table class="score-table">
                    <tr><th>维度</th><th>评分</th></tr>
'''
    
    # 添加各维度评分
    for dim, score in zip(dimensions, scores):
        score_class = "score-high" if score >= 7 else ("score-low" if score < 5 else "")
        html_content += f'<tr><td>{dim}</td><td class="{score_class}">{score:.0f}/10</td></tr>\n'
    
    html_content += '''                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>评分标准：A (8-10分) 商业模式成熟 | B (6-7分) 基本成立需补短板 | C (4-5分) 存在重大缺陷 | D (1-3分) 需重新设计</p>
        </div>
    </div>
    
    <script>
        var chart = echarts.init(document.getElementById('radarChart'), null, {renderer: 'canvas'});
        var option = {
            backgroundColor: 'transparent',
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(10, 22, 40, 0.9)',
                borderColor: '#0096ff',
                textStyle: { color: '#fff' }
            },
            radar: {
                indicator: ''' + json.dumps(indicator_config, ensure_ascii=False) + ''',
                shape: 'polygon',
                splitNumber: 5,
                axisName: {
                    color: '#fff',
                    fontSize: 12
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(0, 150, 255, 0.3)'
                    }
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ['rgba(0, 102, 204, 0.1)', 'rgba(0, 102, 204, 0.2)', 
                                'rgba(0, 102, 204, 0.3)', 'rgba(0, 102, 204, 0.4)',
                                'rgba(0, 102, 204, 0.5)']
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(0, 150, 255, 0.5)'
                    }
                }
            },
            series: [{
                type: 'radar',
                data: [{
                    value: ''' + json.dumps(scores) + ''',
                    name: '商业模式评分',
                    areaStyle: {
                        color: 'rgba(0, 150, 255, 0.4)'
                    },
                    lineStyle: {
                        color: '#0096ff',
                        width: 2
                    },
                    itemStyle: {
                        color: '#0096ff'
                    },
                    label: {
                        show: true,
                        formatter: '{c}',
                        color: '#fff'
                    }
                }]
            }]
        };
        chart.setOption(option);
        window.addEventListener('resize', function() {{ chart.resize(); }});
    </script>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML报告已生成：{output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='生成商业模式评分雷达图')
    parser.add_argument('--input', '-i', required=True, help='输入JSON文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出图片路径')
    parser.add_argument('--format', '-f', choices=['png', 'jpg', 'svg'], default='png', 
                        help='输出格式（默认：png）')
    parser.add_argument('--html', action='store_true', help='同时生成HTML报告')
    
    args = parser.parse_args()
    
    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入文件不存在：{input_path}")
        sys.exit(1)
    
    # 加载数据
    try:
        data = load_scores(input_path)
    except Exception as e:
        print(f"错误：加载数据失败 - {e}")
        sys.exit(1)
    
    # 生成雷达图
    try:
        output_path = Path(args.output)
        create_radar_chart(data, output_path, args.format)
        
        # 同时生成HTML报告
        if args.html:
            html_path = output_path.with_suffix('.html')
            create_html_report(data, html_path)
        
    except Exception as e:
        print(f"错误：生成雷达图失败 - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("完成！")


if __name__ == '__main__':
    main()

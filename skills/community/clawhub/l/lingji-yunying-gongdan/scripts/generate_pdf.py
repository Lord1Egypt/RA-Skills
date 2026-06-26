#!/usr/bin/env python3
"""
灵畿运营工单分析 - PDF报告生成（使用Playwright）
"""
import sys
import pandas as pd
import re
import os
from collections import Counter
from datetime import datetime
from playwright.sync_api import sync_playwright

def parse_duration(s):
    """解析处理时长，返回分钟数"""
    if pd.isna(s):
        return None
    s = str(s)
    days = re.search(r'(\d+)天', s)
    hours = re.search(r'(\d+)小时', s)
    minutes = re.search(r'(\d+)分', s)
    seconds = re.search(r'(\d+)秒', s)
    total_minutes = 0
    if days: total_minutes += int(days.group(1)) * 24 * 60
    if hours: total_minutes += int(hours.group(1)) * 60
    if minutes: total_minutes += int(minutes.group(1))
    if seconds: total_minutes += int(seconds.group(1)) / 60
    return total_minutes

def classify_issue(desc):
    """问题分类"""
    if pd.isna(desc):
        return []
    desc = str(desc)
    issues = []
    
    if '权限' in desc or '看不了' in desc or '看不到' in desc or '无法查看' in desc:
        issues.append('权限问题')
    if '查询不到' in desc or '看不到项目' in desc or '找不到项目' in desc or '搜索不到' in desc:
        issues.append('项目查询不到')
    if '立项' in desc or '挂载' in desc or '关联需求' in desc:
        issues.append('立项/需求关联')
    if '报错' in desc or '异常' in desc or '失败' in desc:
        if '上传失败' in desc or '导入失败' in desc:
            issues.append('上传/导入失败')
        elif '服务器异常' in desc or '系统异常' in desc:
            issues.append('服务器异常')
        else:
            issues.append('系统报错')
    if '审批' in desc or '流程' in desc:
        issues.append('流程审批')
    if '数据' in desc or '金额不对' in desc or '金额有误' in desc:
        issues.append('数据问题')
    if '预算' in desc:
        issues.append('预算问题')
    if '登录' in desc or '登陆' in desc:
        issues.append('登录问题')
    if '证书' in desc:
        issues.append('证书问题')
    if '删除' in desc:
        issues.append('删除问题')
    if '修改' in desc or '编辑' in desc:
        if '无法编辑' in desc or '编辑不了' in desc:
            issues.append('编辑保存问题')
    if '建议' in desc or '优化' in desc:
        issues.append('建议/优化需求')
    if '需求' in desc:
        issues.append('需求管理')
    if '成果' in desc:
        issues.append('成果管理')
    if '研发计划' in desc:
        issues.append('研发计划')
    if '制品' in desc or '仓库' in desc:
        issues.append('制品/仓库')
    
    return issues if issues else ['其他问题']

def generate_html_report(df):
    """生成HTML报告内容"""
    total = len(df)
    
    # 时效数据
    df_copy = df.copy()
    df_copy['处理时长_分钟'] = df_copy['工单处理时长'].apply(parse_duration)
    valid_times = df_copy['处理时长_分钟'].dropna()
    
    # 问题分类
    all_issues = []
    for desc in df['工单内容描述']:
        all_issues.extend(classify_issue(desc))
    issue_counts = Counter(all_issues)
    
    # 满意度
    valid_sat = df[df['满意度分值'] > 0]
    
    # 处理人数据
    top_handlers = df['当前处理人'].value_counts().head(15).index.tolist()
    handler_rows = ""
    for handler in top_handlers:
        h_df = df[df['当前处理人'] == handler]
        h_total = len(h_df)
        completed = (h_df['工单状态'] == '红军已完成').sum()
        pending = (h_df['工单状态'] == '待用户确认').sum()
        very_sat = (h_df['满意度选项'] == '非常满意').sum()
        
        valid_satisfaction = h_df[h_df['满意度分值'] > 0]['满意度分值']
        avg_sat = valid_satisfaction.mean() if len(valid_satisfaction) > 0 else 0
        
        h_df_copy = h_df.copy()
        h_df_copy['时长_分钟'] = h_df_copy['工单处理时长'].apply(parse_duration)
        avg_time = h_df_copy['时长_分钟'].mean()
        
        handler_rows += f"""
        <tr>
            <td>{handler}</td>
            <td>{h_total}</td>
            <td>{completed}</td>
            <td>{pending}</td>
            <td>{very_sat}</td>
            <td>{avg_sat:.1f}</td>
            <td>{avg_time:.0f}分钟</td>
        </tr>
        """
    
    # 类型分布
    type_rows = ""
    for t, c in df['工单类型'].value_counts().items():
        type_rows += f"<tr><td>{t}</td><td>{c}</td><td>{c/total*100:.1f}%</td></tr>"
    
    # 状态分布
    status_rows = ""
    for s, c in df['工单状态'].value_counts().items():
        status_rows += f"<tr><td>{s}</td><td>{c}</td><td>{c/total*100:.1f}%</td></tr>"
    
    # 满意度分布
    sat_rows = ""
    for opt, cnt in df['满意度选项'].value_counts().items():
        sat_rows += f"<tr><td>{opt}</td><td>{cnt}</td><td>{cnt/total*100:.1f}%</td></tr>"
    
    # 热点问题
    issue_rows = ""
    for issue, cnt in issue_counts.most_common(15):
        issue_rows += f"<tr><td>{issue}</td><td>{cnt}</td><td>{cnt/total*100:.1f}%</td></tr>"
    
    # 模块
    module_rows = ""
    for module, cnt in df['模块'].value_counts().head(10).items():
        module_rows += f"<tr><td>{module}</td><td>{cnt}</td><td>{cnt/total*100:.1f}%</td></tr>"
    
    # 菜单
    menu_rows = ""
    for menu, cnt in df['菜单'].value_counts().head(10).items():
        menu_rows += f"<tr><td>{menu}</td><td>{cnt}</td><td>{cnt/total*100:.1f}%</td></tr>"
    
    # 工作组
    group_rows = ""
    for group, cnt in df['处理工作组'].value_counts().head(10).items():
        group_rows += f"<tr><td>{group}</td><td>{cnt}</td><td>{cnt/total*100:.1f}%</td></tr>"
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>灵畿科研平台工单运营分析报告</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
            margin-top: 20mm;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", "WenQuanYi Micro Hei", sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #333;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            font-size: 20pt;
            color: #1a4f7a;
            margin-bottom: 5px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            font-size: 9pt;
            margin-bottom: 20px;
        }}
        h2 {{
            font-size: 14pt;
            color: #1a4f7a;
            border-bottom: 2px solid #1a4f7a;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        h3 {{
            font-size: 11pt;
            color: #333;
            margin-top: 15px;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}
        th {{
            background-color: #4472C4;
            color: white;
            padding: 8px;
            text-align: center;
            font-weight: normal;
        }}
        td {{
            padding: 6px 8px;
            border: 1px solid #ddd;
            text-align: center;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .summary {{
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        .summary-item {{
            text-align: center;
            padding: 10px 20px;
        }}
        .summary-value {{
            font-size: 22pt;
            font-weight: bold;
            color: #1a4f7a;
        }}
        .summary-label {{
            font-size: 9pt;
            color: #666;
            margin-top: 5px;
        }}
        .page-break {{
            page-break-after: always;
        }}
        .two-col {{
            display: flex;
            gap: 20px;
        }}
        .two-col > div {{
            flex: 1;
        }}
    </style>
</head>
<body>
    <h1>灵畿科研平台工单运营分析报告</h1>
    <div class="subtitle">报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    
    <div class="summary">
        <div class="summary-item">
            <div class="summary-value">{total}</div>
            <div class="summary-label">工单总量</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">{valid_times.mean():.0f}</div>
            <div class="summary-label">平均处理时长(分钟)</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">{len(valid_sat)/total*100:.0f}%</div>
            <div class="summary-label">满意度评价率</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">{valid_sat['满意度分值'].mean():.1f}</div>
            <div class="summary-label">满意度均分</div>
        </div>
    </div>
    
    <h2>一、工单类型与状态分布</h2>
    <div class="two-col">
        <div>
            <h3>工单类型分布</h3>
            <table>
                <tr><th>工单类型</th><th>数量</th><th>占比</th></tr>
                {type_rows}
            </table>
        </div>
        <div>
            <h3>工单状态分布</h3>
            <table>
                <tr><th>工单状态</th><th>数量</th><th>占比</th></tr>
                {status_rows}
            </table>
        </div>
    </div>
    
    <h2>二、时效性分析</h2>
    <table>
        <tr><th>指标</th><th>数值</th></tr>
        <tr><td>平均处理时长</td><td>{valid_times.mean():.0f} 分钟</td></tr>
        <tr><td>中位数处理时长</td><td>{valid_times.median():.0f} 分钟</td></tr>
        <tr><td>最短处理时长</td><td>{valid_times.min():.0f} 分钟</td></tr>
        <tr><td>最长处理时长</td><td>{valid_times.max():.0f} 分钟</td></tr>
        <tr><td>90分位处理时长</td><td>{valid_times.quantile(0.9):.0f} 分钟</td></tr>
    </table>
    
    <h2>三、满意度分析</h2>
    <table>
        <tr><th>满意度选项</th><th>数量</th><th>占比</th></tr>
        {sat_rows}
    </table>
    
    <div class="page-break"></div>
    
    <h2>四、热点问题分析</h2>
    <table>
        <tr><th>问题类型</th><th>数量</th><th>占比</th></tr>
        {issue_rows}
    </table>
    
    <h2>五、支撑人员工作量排名（TOP15）</h2>
    <table>
        <tr><th>处理人</th><th>工单数</th><th>已完成</th><th>待确认</th><th>非常满意</th><th>平均满意度</th><th>平均处理时长</th></tr>
        {handler_rows}
    </table>
    
    <h2>六、处理工作组分布（TOP10）</h2>
    <table>
        <tr><th>工作组</th><th>工单数</th><th>占比</th></tr>
        {group_rows}
    </table>
    
    <h2>七、高频模块与菜单</h2>
    <div class="two-col">
        <div>
            <h3>高频模块TOP10</h3>
            <table>
                <tr><th>模块</th><th>数量</th><th>占比</th></tr>
                {module_rows}
            </table>
        </div>
        <div>
            <h3>高频菜单TOP10</h3>
            <table>
                <tr><th>菜单</th><th>数量</th><th>占比</th></tr>
                {menu_rows}
            </table>
        </div>
    </div>
</body>
</html>
"""
    return html

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_pdf.py <excel_file> <output_pdf>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = sys.argv[2]
    
    print(f"Loading data from: {file_path}")
    df = pd.read_excel(file_path)
    print(f"Loaded {len(df)} records")
    
    html_content = generate_html_report(df)
    
    # 写入临时HTML文件
    html_path = "/tmp/lingji_report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Generating PDF with Playwright...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}")
        page.pdf(
            path=output_path,
            format="A4",
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
            print_background=True
        )
        browser.close()
    
    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    main()

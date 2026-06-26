#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布前自动检查脚本
技能名称：issue-analysis-agent
版本：v1.0.0
创建：2026-03-24

功能：
- 检查字段名是否正确
- 检查响应头是否正确
- 检查图表是否都能正常显示
- 生成检查报告

使用方法：
python3 check_before_deploy.py <JSON 文件路径> [HTML 文件路径]
"""

import json
import sys
import requests
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")

def check_json_fields(json_path):
    """检查 JSON 字段名"""
    print_header("【检查 1/4】JSON 字段名检查")
    
    if not Path(json_path).exists():
        print_error(f"文件不存在：{json_path}")
        return False, None
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 必需字段（支持新旧字段名兼容）
    required_fields = {
        'summary': 'summary',
        'weekly_trend': ['weekly_trend', 'weekly'],
        'issue_types': ['issue_types', 'types'],
        'platforms': 'platforms',
        'reporters': 'reporters',
        'resolvers': 'resolvers',
        'unresolved_resolvers': 'unresolved_resolvers',
        'unresolved_modules': 'unresolved_modules'
    }
    
    all_passed = True
    field_mapping = {}
    
    for standard_name, possible_names in required_fields.items():
        if isinstance(possible_names, str):
            possible_names = [possible_names]
        
        found = False
        for name in possible_names:
            if name in data:
                if name == standard_name:
                    print_success(f"{standard_name}")
                else:
                    print_warning(f"{standard_name} (使用兼容字段：{name})")
                field_mapping[standard_name] = name
                found = True
                break
        
        if not found:
            print_error(f"缺少字段：{standard_name}")
            all_passed = False
    
    # 检查 summary 子字段
    print("\n检查 summary 子字段:")
    summary = data.get('summary', {})
    summary_fields = ['total', 'resolved', 'unresolved', 'rate']
    
    for field in summary_fields:
        if field in summary:
            print_success(f"summary.{field} = {summary[field]}")
        else:
            print_error(f"缺少字段：summary.{field}")
            all_passed = False
    
    return all_passed, data

def check_html_structure(html_path):
    """检查 HTML 结构和图表"""
    print_header("【检查 2/4】HTML 结构和图表检查")
    
    if not Path(html_path).exists():
        print_error(f"文件不存在：{html_path}")
        return False
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_passed = True
    
    # 检查基本结构
    print("检查 HTML 基本结构:")
    basic_elements = [
        ('<!DOCTYPE html>', 'DOCTYPE 声明'),
        ('<html', 'HTML 标签'),
        ('<head>', 'HEAD 标签'),
        ('<body>', 'BODY 标签'),
        ('<meta charset="UTF-8">', '字符集声明'),
    ]
    
    for element, desc in basic_elements:
        if element in content:
            print_success(desc)
        else:
            print_error(f"缺少 {desc}")
            all_passed = False
    
    # 检查图表
    print("\n检查图表元素:")
    chart_elements = [
        ('weeklyChart', '每周趋势图'),
        ('typeChart', '问题类型图'),
        ('platformChart', '平台分布图'),
        ('reporterChart', '反馈人图'),
        ('resolverChart', '解决人图'),
        ('unresolvedResolverChart', '未解问题人图'),
    ]
    
    for chart_id, desc in chart_elements:
        has_canvas = f'id="{chart_id}"' in content
        has_init = f"getElementById('{chart_id}')" in content
        
        if has_canvas and has_init:
            print_success(desc)
        else:
            if not has_canvas:
                print_error(f"{desc} - 缺少 canvas 元素")
            if not has_init:
                print_error(f"{desc} - 缺少初始化代码")
            all_passed = False
    
    # 检查图表标题
    print("\n检查图表标题:")
    chart_titles = [
        ('每周新增问题趋势', '趋势图标题'),
        ('问题类型分布', '类型图标题'),
        ('平台问题分布', '平台图标题'),
        ('反馈人 TOP5', '反馈人图标题'),
        ('解决人 TOP5', '解决人图标题'),
        ('未解问题人 TOP5', '未解问题人图标题'),
        ('未解决问题模块 TOP10', '模块表格标题'),
    ]
    
    for title, desc in chart_titles:
        if title in content:
            print_success(desc)
        else:
            print_error(f"缺少 {desc}")
            all_passed = False
    
    # 检查是否有红色警告样式
    print("\n检查样式:")
    if 'color:#e74c3c' in content or "color: '#e74c3c'" in content:
        # 检查是否用于未解决问题数字（这是正常的）
        if content.count('#e74c3c') <= 3:  # 只允许少量使用（如图表颜色）
            print_success("红色样式使用合理")
        else:
            print_warning("发现多处红色警告样式（已优化为 info 蓝色）")
    else:
        print_success("无不必要的红色警告样式")
    
    # 检查 Chart.js
    if 'chart.js' in content.lower():
        print_success("Chart.js 库已引入")
    else:
        print_error("缺少 Chart.js 库")
        all_passed = False
    
    return all_passed

def check_response_headers(public_url, html_path):
    """检查响应头"""
    print_header("【检查 3/4】响应头检查")
    
    if not Path(html_path).exists():
        print_error(f"文件不存在：{html_path}")
        return False
    
    with open(html_path, 'rb') as f:
        original_content = f.read()
    
    print(f"访问链接：{public_url}\n")
    
    try:
        response = requests.get(public_url, timeout=10)
        
        # 检查状态码
        if response.status_code == 200:
            print_success(f"HTTP 状态码：200")
        else:
            print_error(f"HTTP 状态码：{response.status_code}")
            return False
        
        # 检查 Content-Type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            print_success(f"Content-Type: {content_type}")
        else:
            print_error(f"Content-Type 不正确：{content_type}")
            print(f"  期望：text/html; charset=utf-8")
        
        # 检查 Content-Disposition
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'inline' in content_disposition:
            print_success(f"Content-Disposition: {content_disposition}")
        else:
            print_warning(f"Content-Disposition: {content_disposition}")
            print(f"  期望：inline（在浏览器打开，不下载）")
        
        # 检查 Cache-Control
        cache_control = response.headers.get('Cache-Control', '')
        if 'max-age=0' in cache_control or 'no-cache' in cache_control:
            print_success(f"Cache-Control: {cache_control}")
        else:
            print_warning(f"Cache-Control: {cache_control}")
            print(f"  期望：public, max-age=0（不缓存）")
        
        # 检查内容长度
        if len(response.content) == len(original_content):
            print_success(f"内容长度：{len(response.content)} bytes")
        else:
            print_error(f"内容长度不匹配：{len(response.content)} vs {len(original_content)}")
            return False
        
        # 检查内容一致性
        if response.content == original_content:
            print_success("内容一致性：通过")
        else:
            print_error("内容不一致")
            return False
        
        return True
        
    except requests.exceptions.Timeout:
        print_error("请求超时（10 秒）")
        return False
    except requests.exceptions.RequestException as e:
        print_error(f"请求失败：{e}")
        return False

def check_data_quality(data):
    """检查数据质量"""
    print_header("【检查 4/4】数据质量检查")
    
    if not data:
        print_error("数据为空")
        return False
    
    summary = data.get('summary', {})
    total = summary.get('total', 0)
    resolved = summary.get('resolved', 0)
    unresolved = summary.get('unresolved', 0)
    
    # 检查总数
    if total > 0:
        print_success(f"问题总数：{total}")
    else:
        print_warning("问题总数为 0")
    
    # 检查解决率
    rate_str = summary.get('rate', '0%')
    try:
        rate = float(rate_str.replace('%', ''))
        if rate >= 80:
            print_success(f"解决率：{rate_str}（良好）")
        elif rate >= 50:
            print_warning(f"解决率：{rate_str}（需关注）")
        else:
            print_error(f"解决率：{rate_str}（过低）")
    except:
        print_warning(f"解决率格式异常：{rate_str}")
    
    # 检查数据一致性
    if resolved + unresolved == total:
        print_success(f"数据一致性：已解决 ({resolved}) + 未解决 ({unresolved}) = 总数 ({total})")
    else:
        print_warning(f"数据不一致：{resolved} + {unresolved} ≠ {total}")
    
    # 检查图表数据
    weekly = data.get('weekly_trend', data.get('weekly', {}))
    if len(weekly) > 0:
        print_success(f"每周趋势数据：{len(weekly)} 周")
    else:
        print_warning("缺少每周趋势数据")
    
    return True

def generate_report(results):
    """生成检查报告"""
    print_header("📋 检查报告")
    
    total_checks = len(results)
    passed = sum(1 for r in results if r['passed'])
    
    print(f"总检查项：{total_checks}")
    print(f"通过：{passed}")
    print(f"失败：{total_checks - passed}")
    print(f"通过率：{passed/total_checks*100:.1f}%\n")
    
    for result in results:
        status = "✅" if result['passed'] else "❌"
        print(f"{status} {result['name']}")
    
    print()
    
    if passed == total_checks:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 所有检查通过！可以安全发布{Colors.END}\n")
        return True
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️ 部分检查未通过，请修复后重新检查{Colors.END}\n")
        return False

def main():
    """主函数"""
    
    if len(sys.argv) < 2:
        print(f"用法：python3 check_before_deploy.py <JSON 文件路径> [HTML 文件路径] [COS 链接]")
        print(f"示例：python3 check_before_deploy.py analysis_data_latest.json report_cn.html")
        sys.exit(1)
    
    json_path = sys.argv[1]
    html_path = sys.argv[2] if len(sys.argv) > 2 else None
    cos_url = sys.argv[3] if len(sys.argv) > 3 else None
    
    results = []
    
    # 检查 1: JSON 字段名
    json_passed, data = check_json_fields(json_path)
    results.append({'name': 'JSON 字段名检查', 'passed': json_passed})
    
    # 检查 2: HTML 结构和图表
    if html_path:
        html_passed = check_html_structure(html_path)
        results.append({'name': 'HTML 结构和图表检查', 'passed': html_passed})
        
        # 检查 3: 响应头（如果有 COS 链接）
        if cos_url:
            headers_passed = check_response_headers(cos_url, html_path)
            results.append({'name': '响应头检查', 'passed': headers_passed})
        else:
            print_warning("\n跳过响应头检查（未提供 COS 链接）")
            results.append({'name': '响应头检查', 'passed': None, 'note': '跳过'})
    else:
        print_warning("\n跳过 HTML 检查（未提供 HTML 文件路径）")
        results.append({'name': 'HTML 结构和图表检查', 'passed': None, 'note': '跳过'})
        results.append({'name': '响应头检查', 'passed': None, 'note': '跳过'})
    
    # 检查 4: 数据质量
    if data:
        data_passed = check_data_quality(data)
        results.append({'name': '数据质量检查', 'passed': data_passed})
    else:
        results.append({'name': '数据质量检查', 'passed': False})
    
    # 生成报告
    all_passed = generate_report(results)
    
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()

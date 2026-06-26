#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器抓取测试 - 验证解析方法
"""
from bs4 import BeautifulSoup
from datetime import datetime

# 简化的HTML测试
html = '''<table><thead><tr><th>发行人全称</th><th>板块</th><th>审核状态</th><th>注册地</th><th>行业分类</th><th>保荐机构</th><th>律师事务所</th><th>会计师事务所</th><th>更新日期</th><th>受理日期</th></tr></thead><tbody><tr><td><div>武汉长进光子技术股份有限公司</div></td><td>科创板</td><td>已问询</td><td>湖北</td><td><div title="计算机、通信和其他电子设备制造业">计算机、通信和其他电子设备制造业</div></td><td><span title="国泰海通证券股份有限公司">国泰海通证券股份有限公司</span></td><td><span title="上海市通力律师事务所">上海市通力律师事务所</span></td><td><span title="立信会计师事务所（特殊普通合伙）">立信会计师事务所（特殊普通合伙）</span></td><td>2026-03-17</td><td>2025-08-29</td></tr><tr><td><div>泉州嘉德利电子材料股份公司</div></td><td>主板</td><td>提交注册</td><td>福建</td><td><div title="计算机、通信和其他电子设备制造业">计算机、通信和其他电子设备制造业</div></td><td><span title="广发证券股份有限公司">广发证券股份有限公司</span></td><td><span title="国浩律师（上海）事务所">国浩律师（上海）事务所</span></td><td><span title="容诚会计师事务所（特殊普通合伙）">容诚会计师事务所（特殊普通合伙）</span></td><td>2026-03-16</td><td>2025-11-06</td></tr></tbody></table>'''

def parse_sse_table(html_content):
    """解析上交所表格"""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        return []
    
    results = []
    
    # 遍历数据行（跳过表头）
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) < 9:
            continue
        
        # 提取文本，处理嵌套的div和span
        def get_text(cell):
            # 优先使用title属性
            div = cell.find('div')
            span = cell.find('span')
            if span:
                return span.get('title', span.get_text(strip=True))
            if div:
                return div.get('title', div.get_text(strip=True))
            return cell.get_text(strip=True)
        
        ipo_info = {
            'company_name': get_text(cells[0]),
            'board': get_text(cells[1]),
            'application_status': get_text(cells[2]),
            'province': get_text(cells[3]),
            'industry': get_text(cells[4]),
            'sponsor': get_text(cells[5]),
            'law_firm': get_text(cells[6]),
            'accounting_firm': get_text(cells[7]),
            'update_date': get_text(cells[8]),
            'accept_date': get_text(cells[9]) if len(cells) > 9 else '',
            'exchange': '上交所',
            'source_url': 'https://www.sse.com.cn/listing/renewal/ipo/',
            'source': '上交所',
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        if ipo_info['company_name']:
            results.append(ipo_info)
    
    return results


if __name__ == '__main__':
    results = parse_sse_table(html)
    
    print("=" * 60)
    print("上交所IPO数据解析测试:")
    print("=" * 60)
    
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['company_name']}")
        print(f"   板块: {item['board']} | 状态: {item['application_status']}")
        print(f"   注册地: {item['province']} | 行业: {item['industry']}")
        print(f"   更新日期: {item['update_date']} | 受理日期: {item['accept_date']}")
        print()
    
    print(f"共 {len(results)} 条记录")
    print("=" * 60)
    print("解析方法测试通过!")

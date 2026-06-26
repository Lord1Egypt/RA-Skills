#!/usr/bin/env python3
"""
Grafana 巡检主脚本 - 整合 API 巡检
"""

import json
import sys
import os
from datetime import datetime

from api_inspect import GrafanaAPIInspector


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """主函数"""
    print("="*60)
    print("🚀 Grafana 自动化巡检系统")
    print("="*60)
    
    # 加载配置
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = load_config(config_path)
    
    grafana_url = config.get('grafana_url', 'http://localhost:3000')
    api_key = config.get('api_key', '')
    dashboard_uids = config.get('dashboard_uids', [])
    auto_discover = config.get('auto_discover', True)
    discover_limit = config.get('discover_limit', 10)
    
    # 1. API 巡检
    print("\n📡 步骤 1: API 数据巡检...")
    inspector = GrafanaAPIInspector(grafana_url, api_key)
    results = inspector.run_full_inspection(
        dashboard_uids=dashboard_uids if dashboard_uids else None,
        auto_discover=auto_discover,
        discover_limit=discover_limit
    )
    
    if 'error' in results:
        print(f"❌ 巡检失败：{results['error']}")
        sys.exit(1)
    
    # 2. 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"inspection_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📄 JSON 结果：{json_path}")
    
    md_path = f"inspection_{timestamp}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(inspector.generate_markdown_report(results))
    print(f"📝 Markdown 报告：{md_path}")
    
    # 输出摘要
    print("\n" + "="*60)
    print("✅ 巡检完成")
    print("="*60)
    print(f"📊 综合评分：{results['overall_score']}/100 ({results['status'].upper()})")
    print(f"📋 巡检仪表盘：{results['summary']['dashboard_count']} 个")
    print(f"🔔 活跃告警：{results['summary']['alert_count']} 个")


if __name__ == "__main__":
    main()

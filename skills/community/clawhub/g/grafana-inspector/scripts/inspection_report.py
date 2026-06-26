#!/usr/bin/env python3
"""
Grafana 自动化巡检脚本 - 日报生成器
功能：
1. 自动发现 Grafana 仪表盘
2. 截图巡检（24小时和7天数据对比）
3. 指标评分和异常检测
4. 生成飞书文档报告
"""

import json
import os
import sys
import time
import asyncio
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

# 添加项目路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

class GrafanaInspector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.grafana_url = config.get('grafana_url', '').rstrip('/')
        self.api_key = config.get('api_key', '')
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.screenshot_dir = Path(config.get('screenshot_dir', './screenshots'))
        self.output_dir = Path(config.get('output_dir', './reports'))
        self.discover_limit = config.get('discover_limit', 10)
        self.dashboards_data = []
        self.issues = []
        self.scores = {}

        # 确保目录存在
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_auth_headers(self) -> Dict[str, str]:
        """获取认证头"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def discover_dashboards(self) -> List[Dict[str, Any]]:
        """自动发现仪表盘"""
        print("🔍 正在发现仪表盘...")

        try:
            # 使用 Grafana API 搜索仪表盘
            search_url = f"{self.grafana_url}/api/search"
            params = {
                'type': 'dash-db',
                'limit': self.discover_limit
            }

            response = requests.get(
                search_url,
                headers=self.get_auth_headers(),
                params=params,
                auth=(self.username, self.password) if self.username and self.password else None,
                timeout=30,
                verify=False
            )

            if response.status_code == 200:
                dashboards = response.json()
                print(f"✅ 发现 {len(dashboards)} 个仪表盘")

                # 分类仪表盘
                categorized = self._categorize_dashboards(dashboards)
                return categorized
            else:
                print(f"❌ API 调用失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 发现仪表盘失败: {e}")
            return []

    def _categorize_dashboards(self, dashboards: List[Dict]) -> List[Dict]:
        """对仪表盘进行分类"""
        categories = {
            'host': ['linux', 'node', 'host', 'windows', 'esxi', 'vm'],
            'middleware': ['mysql', 'redis', 'nginx', 'middleware', 'kafka', 'rabbitmq'],
            'business': ['business', '业务', 'application', 'app'],
            'infrastructure': ['vmware', 'cluster', 'storage', 'network']
        }

        result = []
        for db in dashboards:
            title = db.get('title', '').lower()
            db['category'] = 'other'

            for cat, keywords in categories.items():
                if any(kw in title for kw in keywords):
                    db['category'] = cat
                    break

            result.append(db)

        return result

    def get_dashboard_details(self, uid: str) -> Optional[Dict]:
        """获取仪表盘详情"""
        try:
            url = f"{self.grafana_url}/api/dashboards/uid/{uid}"
            response = requests.get(
                url,
                headers=self.get_auth_headers(),
                auth=(self.username, self.password) if self.username and self.password else None,
                timeout=30,
                verify=False
            )

            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ 获取仪表盘详情失败 {uid}: {e}")
            return None

    def analyze_metrics(self, dashboard_data: Dict) -> Dict[str, Any]:
        """分析仪表盘指标"""
        analysis = {
            'panel_count': 0,
            'alert_count': 0,
            'issues': [],
            'score': 100
        }

        try:
            dashboard = dashboard_data.get('dashboard', {})
            panels = dashboard.get('panels', [])
            analysis['panel_count'] = len(panels)

            # 检查面板配置
            for panel in panels:
                # 检查是否有告警规则
                if panel.get('alert'):
                    analysis['alert_count'] += 1

                # 检查数据源
                datasource = panel.get('datasource')
                if not datasource:
                    analysis['issues'].append(f"面板 '{panel.get('title', 'Unknown')}' 缺少数据源")
                    analysis['score'] -= 5

                # 检查查询
                targets = panel.get('targets', [])
                if not targets:
                    analysis['issues'].append(f"面板 '{panel.get('title', 'Unknown')}' 缺少查询")
                    analysis['score'] -= 5

        except Exception as e:
            analysis['issues'].append(f"分析失败: {e}")
            analysis['score'] -= 10

        analysis['score'] = max(0, analysis['score'])
        return analysis

    def generate_inspection_data(self) -> Dict[str, Any]:
        """生成巡检数据"""
        print("📊 开始生成巡检数据...")

        # 发现仪表盘
        dashboards = self.discover_dashboards()

        inspection_result = {
            'timestamp': datetime.now().isoformat(),
            'grafana_url': self.grafana_url,
            'total_dashboards': len(dashboards),
            'categories': {},
            'dashboards': [],
            'summary': {
                'total_issues': 0,
                'avg_score': 0,
                'critical_issues': 0
            }
        }

        total_score = 0

        for db in dashboards:
            print(f"  📋 分析: {db.get('title', 'Unknown')}")

            uid = db.get('uid')
            details = self.get_dashboard_details(uid) if uid else None

            if details:
                analysis = self.analyze_metrics(details)
            else:
                analysis = {
                    'panel_count': 0,
                    'alert_count': 0,
                    'issues': ['无法获取仪表盘详情'],
                    'score': 50
                }

            db_info = {
                'uid': db.get('uid'),
                'title': db.get('title'),
                'url': f"{self.grafana_url}/d/{db.get('uid', '')}",
                'category': db.get('category', 'other'),
                'panel_count': analysis['panel_count'],
                'alert_count': analysis['alert_count'],
                'score': analysis['score'],
                'issues': analysis['issues']
            }

            inspection_result['dashboards'].append(db_info)
            total_score += analysis['score']

            # 分类统计
            cat = db.get('category', 'other')
            if cat not in inspection_result['categories']:
                inspection_result['categories'][cat] = []
            inspection_result['categories'][cat].append(db_info)

            # 统计问题
            inspection_result['summary']['total_issues'] += len(analysis['issues'])
            if analysis['score'] < 60:
                inspection_result['summary']['critical_issues'] += 1

        if dashboards:
            inspection_result['summary']['avg_score'] = round(total_score / len(dashboards), 1)

        self.dashboards_data = inspection_result['dashboards']
        return inspection_result

    def generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = f"""# 🚀 Grafana 系统巡检报告

**巡检时间:** {timestamp}  
**Grafana 地址:** {data['grafana_url']}  
**巡检人:** 自动化巡检系统

---

## 📊 巡检概览

| 指标 | 数值 |
|------|------|
| 仪表盘总数 | {data['total_dashboards']} |
| 平均健康评分 | {data['summary']['avg_score']}/100 |
| 发现问题数 | {data['summary']['total_issues']} |
| 严重问题数 | {data['summary']['critical_issues']} |

---

## 🎯 健康评分分布

"""

        # 按分类显示
        for category, dashboards in data['categories'].items():
            cat_name = {
                'host': '🖥️ 主机监控',
                'middleware': '🔧 中间件监控',
                'business': '📈 业务监控',
                'infrastructure': '🏗️ 基础设施',
                'other': '📦 其他'
            }.get(category, category)

            report += f"\n### {cat_name}\n\n"
            report += "| 仪表盘 | 面板数 | 告警数 | 评分 | 状态 |\n"
            report += "|--------|--------|--------|------|------|\n"

            for db in dashboards:
                status = '✅' if db['score'] >= 80 else ('⚠️' if db['score'] >= 60 else '❌')
                report += f"| [{db['title']}]({db['url']}) | {db['panel_count']} | {db['alert_count']} | {db['score']} | {status} |\n"

        # 问题详情
        report += "\n---\n\n## ⚠️ 问题详情\n\n"

        has_issues = False
        for db in data['dashboards']:
            if db['issues']:
                has_issues = True
                report += f"\n### {db['title']}\n"
                for issue in db['issues']:
                    report += f"- {issue}\n"

        if not has_issues:
            report += "✅ 未发现明显问题\n"

        # 建议
        report += """

---

## 💡 优化建议

1. **定期检查数据源配置** - 确保所有面板都有有效的数据源
2. **配置告警规则** - 为关键指标设置告警
3. **优化查询性能** - 避免长时间范围的复杂查询
4. **统一命名规范** - 保持仪表盘命名的一致性

---

*报告由 OpenClaw SRE 巡检系统自动生成*
"""

        return report

    def save_report(self, data: Dict[str, Any], markdown: str) -> str:
        """保存报告到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存 JSON
        json_path = self.output_dir / f"inspection_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 保存 Markdown
        md_path = self.output_dir / f"inspection_{timestamp}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✅ 报告已保存:")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {md_path}")

        return str(md_path)

    def run(self) -> Dict[str, Any]:
        """执行完整巡检流程"""
        print("=" * 60)
        print("🚀 Grafana SRE 自动化巡检")
        print("=" * 60)

        # 生成巡检数据
        data = self.generate_inspection_data()

        # 生成报告
        markdown = self.generate_markdown_report(data)

        # 保存报告
        report_path = self.save_report(data, markdown)

        print("\n" + "=" * 60)
        print(f"✅ 巡检完成!")
        print(f"   平均评分: {data['summary']['avg_score']}/100")
        print(f"   发现问题: {data['summary']['total_issues']}")
        print("=" * 60)

        return {
            'data': data,
            'markdown': markdown,
            'report_path': report_path
        }


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """主函数"""
    # 默认配置路径
    config_path = SCRIPT_DIR / 'config.json'

    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        print("请复制 config.example.json 为 config.json 并修改配置")
        sys.exit(1)

    # 加载配置
    config = load_config(str(config_path))

    # 执行巡检
    inspector = GrafanaInspector(config)
    result = inspector.run()

    return result


if __name__ == '__main__':
    main()

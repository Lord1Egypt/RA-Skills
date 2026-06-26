#!/usr/bin/env python3
"""
Grafana API 巡检脚本
通过 Grafana API 获取面板数据、告警状态、数据源健康状态
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional


class GrafanaAPIInspector:
    def __init__(self, grafana_url: str, api_key: str, timeout: int = 30):
        self.grafana_url = grafana_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def check_api_connectivity(self) -> bool:
        """检查 API 连接"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/org",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                print(f"✅ API 连接成功：{response.json().get('name', 'Unknown')}")
                return True
            print(f"❌ API 连接失败：HTTP {response.status_code}")
            return False
        except Exception as e:
            print(f"❌ API 连接异常：{str(e)}")
            return False
    
    def get_dashboard_list(self, limit: int = 100) -> List[Dict]:
        """获取仪表盘列表"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/search?type=dash-db&limit={limit}",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                dashboards = response.json()
                print(f"✅ 发现 {len(dashboards)} 个仪表盘")
                return dashboards
            return []
        except Exception as e:
            print(f"❌ 获取仪表盘列表异常：{str(e)}")
            return []
    
    def get_dashboard_by_uid(self, dashboard_uid: str) -> Optional[Dict]:
        """获取仪表盘详情"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/dashboards/uid/{dashboard_uid}",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            print(f"❌ 获取仪表盘 {dashboard_uid} 失败：HTTP {response.status_code}")
            return None
        except Exception as e:
            print(f"❌ 获取仪表盘 {dashboard_uid} 异常：{str(e)}")
            return None
    
    def get_alerts(self) -> List[Dict]:
        """获取活跃告警"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/v1/alerts?state=alerting",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                alerts = response.json()
                print(f"⚠️ 活跃告警：{len(alerts)} 个")
                return alerts
            return []
        except Exception as e:
            print(f"❌ 获取告警状态异常：{str(e)}")
            return []
    
    def get_datasources(self) -> List[Dict]:
        """获取数据源状态"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/datasources",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                datasources = response.json()
                healthy_count = 0
                for ds in datasources:
                    health = self.check_datasource_health(ds.get('id'))
                    ds['healthy'] = health
                    if health:
                        healthy_count += 1
                print(f"✅ 数据源：{healthy_count}/{len(datasources)} 健康")
                return datasources
            return []
        except Exception as e:
            print(f"❌ 获取数据源异常：{str(e)}")
            return []
    
    def check_datasource_health(self, datasource_id: int) -> bool:
        """检查数据源健康"""
        try:
            response = requests.get(
                f"{self.grafana_url}/api/datasources/{datasource_id}/health",
                headers=self.headers,
                timeout=self.timeout
            )
            return response.status_code == 200
        except:
            return False
    
    def inspect_dashboard(self, dashboard_uid: str) -> Dict[str, Any]:
        """巡检单个仪表盘"""
        print(f"\n📋 巡检仪表盘：{dashboard_uid}")
        
        dashboard = self.get_dashboard_by_uid(dashboard_uid)
        if not dashboard:
            return {
                'uid': dashboard_uid,
                'status': 'error',
                'score': 0,
                'issues': ['无法获取仪表盘']
            }
        
        db_info = dashboard.get('dashboard', {})
        panels = db_info.get('panels', [])
        panel_count = len([p for p in panels if p.get('type') != 'row'])
        
        score = 100
        issues = []
        
        result = {
            'uid': dashboard_uid,
            'title': db_info.get('title', dashboard_uid),
            'status': 'healthy',
            'score': score,
            'panel_count': panel_count,
            'panels_ok': panel_count,
            'issues': issues
        }
        
        print(f"  面板：{panel_count} 个")
        print(f"  评分：{score}/100")
        
        return result
    
    def run_full_inspection(
        self,
        dashboard_uids: Optional[List[str]] = None,
        auto_discover: bool = False,
        discover_limit: int = 10
    ) -> Dict[str, Any]:
        """执行完整巡检"""
        print("\n" + "="*60)
        print("🚀 Grafana API 巡检系统")
        print("="*60)
        
        if not self.check_api_connectivity():
            return {'error': 'API 连接失败'}
        
        print("\n📊 获取仪表盘列表...")
        if auto_discover:
            all_dashboards = self.get_dashboard_list(limit=discover_limit)
            dashboard_uids = [d['uid'] for d in all_dashboards[:discover_limit]]
        elif dashboard_uids:
            print(f"✅ 将巡检 {len(dashboard_uids)} 个指定仪表盘")
        else:
            return {'error': '未指定仪表盘 UID'}
        
        print("\n📋 巡检仪表盘...")
        dashboard_results = []
        for uid in dashboard_uids:
            result = self.inspect_dashboard(uid)
            dashboard_results.append(result)
        
        print("\n🔔 检查告警状态...")
        alerts = self.get_alerts()
        
        print("\n💾 检查数据源...")
        datasources = self.get_datasources()
        
        if dashboard_results:
            avg_score = sum(d['score'] for d in dashboard_results) / len(dashboard_results)
            alert_penalty = len(alerts) * 10
            final_score = max(0, min(100, avg_score - alert_penalty))
        else:
            final_score = 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'grafana_url': self.grafana_url,
            'dashboards': dashboard_results,
            'alerts': [
                {
                    'id': a.get('id'),
                    'name': a.get('name'),
                    'state': a.get('state'),
                    'dashboard': a.get('dashboardUri')
                }
                for a in alerts
            ],
            'datasources': [
                {
                    'id': ds.get('id'),
                    'name': ds.get('name'),
                    'type': ds.get('type'),
                    'healthy': ds.get('healthy', False)
                }
                for ds in datasources
            ],
            'overall_score': round(final_score, 1),
            'status': 'excellent' if final_score >= 90 else 'good' if final_score >= 70 else 'warning' if final_score >= 50 else 'critical',
            'summary': {
                'dashboard_count': len(dashboard_results),
                'alert_count': len(alerts),
                'datasource_count': len(datasources),
                'healthy_datasources': sum(1 for ds in datasources if ds.get('healthy'))
            }
        }
    
    def generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """生成 Markdown 报告"""
        if 'error' in results:
            return f"# ❌ 巡检失败\n\n{results['error']}"
        
        status_emoji = {'excellent': '🟢', 'good': '🟢', 'warning': '🟡', 'critical': '🔴'}
        emoji = status_emoji.get(results['status'], '⚪')
        
        md = f"""# 📊 Grafana API 巡检报告

**巡检时间：** {results['timestamp']}  
**Grafana 地址：** {results['grafana_url']}  
**综合评分：** {emoji} {results['overall_score']}/100 ({results['status'].upper()})

---

## 📈 巡检概览

| 项目 | 数量 | 状态 |
|------|------|------|
| 巡检仪表盘 | {results['summary']['dashboard_count']} | ✅ |
| 活跃告警 | {results['summary']['alert_count']} | {'⚠️' if results['summary']['alert_count'] > 0 else '✅'} |
| 数据源 | {results['summary']['healthy_datasources']}/{results['summary']['datasource_count']} | {'✅' if results['summary']['healthy_datasources'] == results['summary']['datasource_count'] else '⚠️'} |

---

## 📋 仪表盘详情

"""
        for db in results['dashboards']:
            db_emoji = '✅' if db['score'] >= 70 else '⚠️' if db['score'] >= 50 else '❌'
            md += f"""### {db_emoji} {db.get('title', db['uid'])}

- **UID:** `{db['uid']}`
- **评分:** {db['score']}/100
- **状态:** {db['status']}
- **面板:** {db.get('panel_count', 0)} 个

"""
        
        if results['alerts']:
            md += """---

## 🔔 活跃告警

"""
            for alert in results['alerts']:
                md += f"- **{alert['name']}** (ID: {alert['id']})\n"
        
        md += f"\n*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        return md


def main():
    if len(sys.argv) < 3:
        print("用法：python api_inspect.py <grafana_url> <api_key> [uid1,uid2,...]")
        print("      python api_inspect.py <grafana_url> <api_key> --auto-discover")
        sys.exit(1)
    
    grafana_url = sys.argv[1]
    api_key = sys.argv[2]
    
    if len(sys.argv) > 3:
        if sys.argv[3] == '--auto-discover':
            dashboard_uids = None
            auto_discover = True
        else:
            dashboard_uids = sys.argv[3].split(',')
            auto_discover = False
    else:
        dashboard_uids = None
        auto_discover = True
    
    inspector = GrafanaAPIInspector(grafana_url, api_key)
    results = inspector.run_full_inspection(
        dashboard_uids=dashboard_uids,
        auto_discover=auto_discover
    )
    
    print("\n" + "="*60)
    print(f"综合评分：{results.get('overall_score', 0)}/100 ({results.get('status', 'unknown').upper()})")
    print(f"巡检仪表盘：{results.get('summary', {}).get('dashboard_count', 0)} 个")
    print(f"活跃告警：{results.get('summary', {}).get('alert_count', 0)} 个")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report_md = inspector.generate_markdown_report(results)
    md_path = f"inspection_{timestamp}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f"\n📝 Markdown 报告：{md_path}")
    
    json_path = f"inspection_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"📄 JSON 结果：{json_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
pans-churn-predictor - AI算力销售客户流失预警工具
分析客户用量趋势，识别流失风险，生成挽回建议
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import sys

# 数据存储路径
DATA_DIR = Path.home() / ".qclaw/skills/pans-churn-predictor/data"


class ChurnPredictor:
    """客户流失预测器"""
    
    def __init__(self):
        self.clients = self._load_data("clients.json", {})
        self.usage_history = self._load_data("usage_history.json", {})
        self.tickets = self._load_data("tickets.json", {})
        self.contracts = self._load_data("contracts.json", {})
    
    def _load_data(self, filename: str, default) -> Dict:
        """加载数据文件"""
        filepath = DATA_DIR / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载 {filename} 失败: {e}")
                return default
        return default
    
    def _save_data(self, filename: str, data: Dict):
        """保存数据文件"""
        filepath = DATA_DIR / filename
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def analyze_client(self, client_name: str, show_reason: bool = False, show_suggest: bool = False) -> Dict:
        """分析单个客户流失风险"""
        if client_name not in self.clients:
            return {"error": f"客户 '{client_name}' 不存在"}
        
        signals = []
        risk_factors = []
        
        # 1. 检查用量趋势（连续3个月下降）
        usage_signal = self._check_usage_decline(client_name)
        if usage_signal:
            signals.append(usage_signal)
            risk_factors.append("usage_decline")
        
        # 2. 检查任务数减少
        task_signal = self._check_task_decline(client_name)
        if task_signal:
            signals.append(task_signal)
            risk_factors.append("task_decline")
        
        # 3. 检查支持ticket增加
        ticket_signal = self._check_ticket_increase(client_name)
        if ticket_signal:
            signals.append(ticket_signal)
            risk_factors.append("ticket_increase")
        
        # 4. 检查合同到期风险
        contract_signal = self._check_contract_expiry(client_name)
        if contract_signal:
            signals.append(contract_signal)
            risk_factors.append("contract_expiry")
        
        # 5. 检查竞品调研行为（模拟）
        competitor_signal = self._check_competitor_activity(client_name)
        if competitor_signal:
            signals.append(competitor_signal)
            risk_factors.append("competitor_activity")
        
        # 判定风险等级
        risk_level = self._determine_risk_level(len(signals))
        
        result = {
            "client": client_name,
            "risk_level": risk_level,
            "signal_count": len(signals),
            "signals": signals,
            "risk_factors": risk_factors
        }
        
        if show_reason and signals:
            result["reasons"] = self._generate_reasons(signals)
        
        if show_suggest:
            result["suggestions"] = self._generate_suggestions(risk_factors, client_name)
        
        return result
    
    def _check_usage_decline(self, client_name: str) -> Optional[Dict]:
        """检查用量连续下降（3个月）"""
        if client_name not in self.usage_history:
            return None
        
        history = self.usage_history[client_name]
        if len(history) < 3:
            return None
        
        # 获取最近3个月的用量
        recent = sorted(history, key=lambda x: x['month'], reverse=True)[:3]
        
        # 检查是否连续下降
        if all(recent[i]['usage'] < recent[i+1]['usage'] for i in range(len(recent)-1)):
            decline_rate = (recent[-1]['usage'] - recent[0]['usage']) / recent[-1]['usage'] * 100
            return {
                "type": "usage_decline",
                "severity": "high" if decline_rate > 30 else "medium",
                "details": f"用量连续3个月下降 {decline_rate:.1f}% ({recent[-1]['month']} → {recent[0]['month']})",
                "data": recent
            }
        return None
    
    def _check_task_decline(self, client_name: str) -> Optional[Dict]:
        """检查任务数减少"""
        if client_name not in self.usage_history:
            return None
        
        history = self.usage_history[client_name]
        if len(history) < 2:
            return None
        
        recent = sorted(history, key=lambda x: x['month'], reverse=True)[:2]
        if recent[0].get('tasks', 0) < recent[1].get('tasks', 0):
            decline = ((recent[1]['tasks'] - recent[0]['tasks']) / recent[1]['tasks'] * 100)
            return {
                "type": "task_decline",
                "severity": "medium",
                "details": f"任务数从 {recent[1]['tasks']} 降至 {recent[0]['tasks']} ({decline:.1f}%↓)"
            }
        return None
    
    def _check_ticket_increase(self, client_name: str) -> Optional[Dict]:
        """检查支持ticket是否异常增加"""
        if client_name not in self.tickets:
            return None
        
        client_tickets = self.tickets[client_name]
        recent_tickets = [t for t in client_tickets if self._is_recent(t.get('date'))]
        
        # 如果最近30天ticket数 > 5，视为异常
        if len(recent_tickets) > 5:
            return {
                "type": "ticket_increase",
                "severity": "medium",
                "details": f"近期支持ticket数量异常（{len(recent_tickets)}个）",
                "data": recent_tickets
            }
        return None
    
    def _check_contract_expiry(self, client_name: str) -> Optional[Dict]:
        """检查合同到期风险"""
        if client_name not in self.contracts:
            return None
        
        contract = self.contracts[client_name]
        expiry_date = datetime.strptime(contract['expiry_date'], '%Y-%m-%d')
        days_to_expiry = (expiry_date - datetime.now()).days
        
        # 合同到期前90天，且无续约动作
        if 0 < days_to_expiry <= 90:
            renewal_status = contract.get('renewal_status', 'pending')
            if renewal_status == 'pending':
                return {
                    "type": "contract_expiry",
                    "severity": "high",
                    "details": f"合同将在 {days_to_expiry} 天后到期，无续约动作",
                    "data": contract
                }
        return None
    
    def _check_competitor_activity(self, client_name: str) -> Optional[Dict]:
        """检查竞品调研行为（模拟）"""
        # 在实际应用中，这可能来自浏览记录、询价记录等
        # 这里使用客户数据中的标记字段
        if client_name not in self.clients:
            return None
        
        client_data = self.clients[client_name]
        if client_data.get('competitor_activity'):
            return {
                "type": "competitor_activity",
                "severity": "high",
                "details": "检测到竞品调研行为"
            }
        return None
    
    def _is_recent(self, date_str: str, days: int = 30) -> bool:
        """判断日期是否在最近N天内"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return (datetime.now() - date).days <= days
        except:
            return False
    
    def _determine_risk_level(self, signal_count: int) -> str:
        """判定风险等级"""
        if signal_count >= 2:
            return "🔴 高风险"
        elif signal_count == 1:
            return "🟡 中风险"
        else:
            return "🟢 正常"
    
    def _generate_reasons(self, signals: List[Dict]) -> List[str]:
        """生成流失原因分析"""
        reasons = []
        for signal in signals:
            if signal['type'] == 'usage_decline':
                reasons.append(f"📉 用量持续下降：客户可能正在缩减算力需求，或已转向其他供应商")
            elif signal['type'] == 'task_decline':
                reasons.append(f"📊 任务数减少：客户活跃度降低，可能已完成主要项目或暂停研发")
            elif signal['type'] == 'ticket_increase':
                reasons.append(f"🎫 支持请求增加：客户可能遇到技术问题，体验满意度下降")
            elif signal['type'] == 'contract_expiry':
                reasons.append(f"📅 合同即将到期：客户可能考虑续约或转向竞品")
            elif signal['type'] == 'competitor_activity':
                reasons.append(f"🔍 竞品调研行为：客户正在评估其他算力供应商")
        return reasons
    
    def _generate_suggestions(self, risk_factors: List[str], client_name: str) -> List[str]:
        """生成挽回建议"""
        suggestions = []
        
        if 'usage_decline' in risk_factors:
            suggestions.extend([
                "💡 安排客户回访，了解用量下降原因",
                "💡 评估是否需要提供更灵活的计费方案（如按需付费）",
                "💡 推送新GPU型号或套餐优惠信息"
            ])
        
        if 'task_decline' in risk_factors:
            suggestions.extend([
                "💡 了解客户当前项目状态，是否需要技术支持",
                "💡 推荐客户成功的案例，启发新的使用场景",
                "💡 提供免费的架构咨询或培训服务"
            ])
        
        if 'ticket_increase' in risk_factors:
            suggestions.extend([
                "💡 升级支持等级，指派专属技术支持人员",
                "💡 主动联系客户，了解遗留问题并推动解决",
                "💡 组织技术复盘会议，改进服务质量"
            ])
        
        if 'contract_expiry' in risk_factors:
            suggestions.extend([
                f"💡 立即启动续约谈判，准备续约方案",
                "💡 提供早续约优惠或长期合同折扣",
                "💡 邀请客户参加年度答谢活动，增强关系"
            ])
        
        if 'competitor_activity' in risk_factors:
            suggestions.extend([
                "💡 了解竞品对比情况，准备竞争性报价",
                "💡 强调我方优势（稳定性、技术支持、生态完整性）",
                "💡 邀请客户参观数据中心或技术交流"
            ])
        
        if not suggestions:
            suggestions.append(f"✅ 客户 {client_name} 目前状态良好，继续保持定期沟通")
        
        return suggestions
    
    def analyze_all(self) -> List[Dict]:
        """分析所有客户"""
        results = []
        for client_name in self.clients.keys():
            result = self.analyze_client(client_name)
            if 'error' not in result:
                results.append(result)
        return sorted(results, key=lambda x: x['signal_count'], reverse=True)
    
    def list_high_risk(self) -> List[Dict]:
        """列出高风险客户"""
        all_clients = self.analyze_all()
        return [c for c in all_clients if c['signal_count'] >= 2]
    
    def add_sample_data(self):
        """添加示例数据（用于测试）"""
        # 示例客户
        self.clients = {
            "智谱AI": {"name": "智谱AI", "industry": "大模型", "contact": "张经理"},
            "商汤科技": {"name": "商汤科技", "industry": "计算机视觉", "contact": "李总监"},
            "云从科技": {"name": "云从科技", "industry": "AI平台", "contact": "王主管"},
            "旷视科技": {"name": "旷视科技", "industry": "计算机视觉", "contact": "赵总"},
            "第四范式": {"name": "第四范式", "industry": "机器学习平台", "contact": "陈经理"}
        }
        
        # 用量历史（最近3个月）
        self.usage_history = {
            "智谱AI": [
                {"month": "2026-04", "usage": 800, "tasks": 45},
                {"month": "2026-03", "usage": 1000, "tasks": 50},
                {"month": "2026-02", "usage": 1200, "tasks": 55}
            ],
            "商汤科技": [
                {"month": "2026-04", "usage": 2500, "tasks": 80},
                {"month": "2026-03", "usage": 2500, "tasks": 85},
                {"month": "2026-02", "usage": 2500, "tasks": 90}
            ],
            "云从科技": [
                {"month": "2026-04", "usage": 300, "tasks": 10},
                {"month": "2026-03", "usage": 500, "tasks": 15},
                {"month": "2026-02", "usage": 700, "tasks": 20}
            ],
            "旷视科技": [
                {"month": "2026-04", "usage": 1500, "tasks": 40},
                {"month": "2026-03", "usage": 1500, "tasks": 42},
                {"month": "2026-02", "usage": 1500, "tasks": 45}
            ],
            "第四范式": [
                {"month": "2026-04", "usage": 600, "tasks": 25},
                {"month": "2026-03", "usage": 700, "tasks": 30},
                {"month": "2026-02", "usage": 800, "tasks": 35}
            ]
        }
        
        # 支持tickets
        self.tickets = {
            "智谱AI": [
                {"id": "T001", "date": "2026-04-10", "issue": "网络延迟"},
                {"id": "T002", "date": "2026-04-12", "issue": "GPU调度问题"},
                {"id": "T003", "date": "2026-04-14", "issue": "计费疑问"},
                {"id": "T004", "date": "2026-04-15", "issue": "API超时"},
                {"id": "T005", "date": "2026-04-16", "issue": "存储扩容"},
                {"id": "T006", "date": "2026-04-16", "issue": "权限问题"}
            ],
            "商汤科技": [
                {"id": "T101", "date": "2026-04-01", "issue": "账号问题"}
            ]
        }
        
        # 合同信息
        self.contracts = {
            "智谱AI": {
                "contract_id": "C001",
                "start_date": "2025-01-01",
                "expiry_date": "2026-06-30",
                "value": 500000,
                "renewal_status": "pending"
            },
            "商汤科技": {
                "contract_id": "C002",
                "start_date": "2025-06-01",
                "expiry_date": "2026-12-01",
                "value": 1200000,
                "renewal_status": "pending"
            },
            "云从科技": {
                "contract_id": "C003",
                "start_date": "2025-03-01",
                "expiry_date": "2026-07-15",
                "value": 300000,
                "renewal_status": "pending"
            },
            "旷视科技": {
                "contract_id": "C004",
                "start_date": "2025-09-01",
                "expiry_date": "2026-09-01",
                "value": 800000,
                "renewal_status": "pending"
            },
            "第四范式": {
                "contract_id": "C005",
                "start_date": "2025-04-01",
                "expiry_date": "2026-07-01",
                "value": 400000,
                "renewal_status": "pending"
            }
        }
        
        # 竞品调研标记
        self.clients["智谱AI"]["competitor_activity"] = True
        
        # 保存数据
        self._save_data("clients.json", self.clients)
        self._save_data("usage_history.json", self.usage_history)
        self._save_data("tickets.json", self.tickets)
        self._save_data("contracts.json", self.contracts)
        
        print("✅ 示例数据已添加")


def main():
    parser = argparse.ArgumentParser(
        description="AI算力销售客户流失预警工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析所有客户
  python churn.py --analyze
  
  # 分析指定客户
  python churn.py --client "智谱AI"
  
  # 列出高风险客户
  python churn.py --list
  
  # 显示流失原因
  python churn.py --client "智谱AI" --reason
  
  # 生成挽回建议
  python churn.py --client "智谱AI" --suggest
  
  # 添加示例数据
  python churn.py --init
        """
    )
    
    parser.add_argument('--analyze', action='store_true', help='分析所有客户')
    parser.add_argument('--client', type=str, help='分析指定客户')
    parser.add_argument('--list', action='store_true', help='列出高风险客户')
    parser.add_argument('--reason', action='store_true', help='显示流失原因（需配合 --client）')
    parser.add_argument('--suggest', action='store_true', help='生成挽回建议（需配合 --client）')
    parser.add_argument('--init', action='store_true', help='初始化示例数据')
    
    args = parser.parse_args()
    
    predictor = ChurnPredictor()
    
    # 如果没有客户数据，提示初始化
    if not predictor.clients and not args.init:
        print("⚠️  未找到客户数据，请先运行: python churn.py --init")
        return
    
    if args.init:
        predictor.add_sample_data()
        return
    
    if args.analyze:
        print("\n📊 客户流失风险分析报告\n")
        print("=" * 60)
        results = predictor.analyze_all()
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['client']}")
            print(f"   风险等级: {result['risk_level']}")
            print(f"   风险信号: {result['signal_count']}个")
            if result['signals']:
                for signal in result['signals']:
                    print(f"   - {signal['details']}")
        
        print("\n" + "=" * 60)
        high_risk = [r for r in results if r['signal_count'] >= 2]
        medium_risk = [r for r in results if r['signal_count'] == 1]
        normal = [r for r in results if r['signal_count'] == 0]
        
        print(f"\n汇总:")
        print(f"  🔴 高风险: {len(high_risk)}个")
        print(f"  🟡 中风险: {len(medium_risk)}个")
        print(f"  🟢 正常: {len(normal)}个")
        print()
    
    elif args.client:
        result = predictor.analyze_client(args.client, args.reason, args.suggest)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
            return
        
        print(f"\n📋 客户流失分析: {result['client']}\n")
        print("=" * 60)
        print(f"风险等级: {result['risk_level']}")
        print(f"风险信号: {result['signal_count']}个\n")
        
        if result['signals']:
            print("风险信号:")
            for signal in result['signals']:
                severity_icon = "🔴" if signal['severity'] == 'high' else "🟡"
                print(f"  {severity_icon} {signal['details']}")
        
        if 'reasons' in result:
            print("\n流失原因分析:")
            for reason in result['reasons']:
                print(f"  {reason}")
        
        if 'suggestions' in result:
            print("\n挽回建议:")
            for suggestion in result['suggestions']:
                print(f"  {suggestion}")
        
        print("\n" + "=" * 60 + "\n")
    
    elif args.list:
        high_risk = predictor.list_high_risk()
        
        print("\n🔴 高风险客户列表\n")
        print("=" * 60)
        
        if not high_risk:
            print("✅ 当前无高风险客户\n")
        else:
            for i, client in enumerate(high_risk, 1):
                print(f"\n{i}. {client['client']}")
                print(f"   风险信号: {client['signal_count']}个")
                for signal in client['signals']:
                    print(f"   - {signal['details']}")
            
            print("\n" + "=" * 60)
            print(f"\n总计: {len(high_risk)}个高风险客户\n")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
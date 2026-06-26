#!/usr/bin/env python3
"""
AI算力销售每日简报生成器
=========================
自动汇总待跟进客户、到期合同、新线索和竞品动态。

用法:
  python3 brief.py                          # 生成今日简报
  python3 brief.py --date 2024-01-15        # 指定日期
  python3 brief.py --add-client '{...}'     # 添加客户
  python3 brief.py --add-contract '{...}'   # 添加合同
  python3 brief.py --add-lead '{...}'       # 添加线索
  python3 brief.py --list                   # 列出所有数据
  python3 brief.py --update <type> <id> '{...}'  # 更新记录
  python3 brief.py --competitor-news        # 搜索竞品动态
  python3 brief.py --json                   # JSON输出
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── 配置 ──────────────────────────────────────────────────────────────────────

SKILL_DIR = Path.home() / ".qclaw" / "skills" / "pans-daily-sales-brief"
DATA_DIR = SKILL_DIR / "data"
PIPELINE_FILE = DATA_DIR / "pipeline.json"

# 默认竞品列表
DEFAULT_COMPETITORS = [
    "CoreWeave",
    "Lambda Labs",
    "RunPod",
    "Vast.ai",
    "FluidStack",
    "TensorDock",
    "Jarvis Labs",
]

# ── 数据管理 ──────────────────────────────────────────────────────────────────


def load_pipeline() -> Dict[str, Any]:
    """加载 pipeline 数据，如果不存在则返回初始化数据。"""
    if not PIPELINE_FILE.exists():
        return get_initial_data()

    try:
        with open(PIPELINE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"警告: 读取数据文件失败: {e}", file=sys.stderr)
        return get_initial_data()


def save_pipeline(data: Dict[str, Any]) -> None:
    """保存 pipeline 数据到文件。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 使用 write_file.py 脚本写入，确保编码正确
    import subprocess
    import tempfile
    
    # 创建临时文件存放内容
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name
    
    try:
        write_script = Path.home() / "Library/Application Support/QClaw/openclaw/config/skills/qclaw-text-file/scripts/write_file.py"
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", str(write_script),
             "--path", str(PIPELINE_FILE),
             "--content-file", tmp_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"警告: 写入文件失败: {result.stderr}", file=sys.stderr)
    finally:
        os.unlink(tmp_path)


def get_initial_data() -> Dict[str, Any]:
    """返回初始数据结构（含示例数据）。"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    next_month = (datetime.now() + timedelta(days=25)).strftime("%Y-%m-%d")

    return {
        "clients": [
            {
                "id": "client_001",
                "company": "智算科技",
                "contact_person": "张总",
                "stage": "深度谈判",
                "next_contact": today,
                "notes": "需要8张H100，预算充足",
                "created_at": yesterday,
            },
            {
                "id": "client_002",
                "company": "AI研究院",
                "contact_person": "李主任",
                "stage": "初步接洽",
                "next_contact": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "notes": "大模型训练需求，关注性价比",
                "created_at": yesterday,
            },
        ],
        "contracts": [
            {
                "id": "contract_001",
                "client": "云端智算",
                "amount": 1200000,
                "expiry_date": next_week,
                "status": "active",
                "notes": "年框合同，需要续约沟通",
                "created_at": yesterday,
            },
            {
                "id": "contract_002",
                "client": "数据科技公司",
                "amount": 800000,
                "expiry_date": next_month,
                "status": "active",
                "notes": "稳定客户",
                "created_at": yesterday,
            },
        ],
        "leads": [
            {
                "id": "lead_001",
                "source": "官网咨询",
                "status": "新线索",
                "priority": "高",
                "company": "新锐AI公司",
                "contact": "王经理",
                "notes": "有明确采购意向",
                "created_at": yesterday,
            },
            {
                "id": "lead_002",
                "source": "老客户推荐",
                "status": "待跟进",
                "priority": "中",
                "company": "合作伙伴B",
                "contact": "赵总",
                "notes": "推荐客户，需要电话沟通",
                "created_at": yesterday,
            },
        ],
        "competitors": DEFAULT_COMPETITORS,
        "statistics": {
            "monthly_revenue": 2500000,
            "pipeline_value": 8500000,
            "conversion_rate": 0.32,
        },
    }


# ── 数据操作 ──────────────────────────────────────────────────────────────────


def generate_id(prefix: str) -> str:
    """生成唯一ID。"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def add_client(data: Dict[str, Any], client_data: Dict[str, Any]) -> Dict[str, Any]:
    """添加客户。"""
    client = {
        "id": generate_id("client"),
        "company": client_data.get("company", "未命名公司"),
        "contact_person": client_data.get("contact_person", ""),
        "stage": client_data.get("stage", "初步接洽"),
        "next_contact": client_data.get("next_contact", ""),
        "notes": client_data.get("notes", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    data["clients"].append(client)
    return client


def add_contract(data: Dict[str, Any], contract_data: Dict[str, Any]) -> Dict[str, Any]:
    """添加合同。"""
    contract = {
        "id": generate_id("contract"),
        "client": contract_data.get("client", "未命名客户"),
        "amount": contract_data.get("amount", 0),
        "expiry_date": contract_data.get("expiry_date", ""),
        "status": contract_data.get("status", "active"),
        "notes": contract_data.get("notes", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    data["contracts"].append(contract)
    return contract


def add_lead(data: Dict[str, Any], lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """添加线索。"""
    lead = {
        "id": generate_id("lead"),
        "source": lead_data.get("source", "未知来源"),
        "status": lead_data.get("status", "新线索"),
        "priority": lead_data.get("priority", "中"),
        "company": lead_data.get("company", "未命名公司"),
        "contact": lead_data.get("contact", ""),
        "notes": lead_data.get("notes", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    data["leads"].append(lead)
    return lead


def update_record(
    data: Dict[str, Any], record_type: str, record_id: str, updates: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """更新记录。"""
    type_map = {
        "client": "clients",
        "contract": "contracts",
        "lead": "leads",
    }

    if record_type not in type_map:
        return None

    key = type_map[record_type]
    for record in data[key]:
        if record.get("id") == record_id:
            record.update(updates)
            return record

    return None


def list_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """列出所有数据。"""
    return {
        "clients": data["clients"],
        "contracts": data["contracts"],
        "leads": data["leads"],
        "competitors": data["competitors"],
        "statistics": data.get("statistics", {}),
    }


# ── 简报生成 ──────────────────────────────────────────────────────────────────


def generate_brief(data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
    """生成每日简报。"""
    brief = {
        "date": target_date,
        "generated_at": datetime.now().isoformat(),
        "today_tasks": [],
        "expiring_contracts": [],
        "new_leads": [],
        "performance": data.get("statistics", {}),
        "competitor_news": [],
    }

    # 📋 今日待办：需要今天联系的客户
    for client in data["clients"]:
        if client.get("next_contact") == target_date:
            brief["today_tasks"].append(client)

    # ⚠️ 即将到期：7天内到期的合同
    target_dt = datetime.strptime(target_date, "%Y-%m-%d")
    expiry_threshold = target_dt + timedelta(days=7)

    for contract in data["contracts"]:
        if contract.get("status") != "active":
            continue

        expiry_date = contract.get("expiry_date", "")
        if not expiry_date:
            continue

        try:
            expiry_dt = datetime.strptime(expiry_date, "%Y-%m-%d")
            if expiry_dt <= expiry_threshold:
                days_left = (expiry_dt - target_dt).days
                contract_copy = contract.copy()
                contract_copy["days_left"] = days_left
                brief["expiring_contracts"].append(contract_copy)
        except ValueError:
            continue

    # 按剩余天数排序
    brief["expiring_contracts"].sort(key=lambda x: x.get("days_left", 999))

    # 🆕 新线索：最近7天新增的线索
    start_date = target_dt - timedelta(days=7)

    for lead in data["leads"]:
        created_at = lead.get("created_at", "")
        if not created_at:
            continue

        try:
            created_dt = datetime.strptime(created_at, "%Y-%m-%d")
            if created_dt >= start_date:
                brief["new_leads"].append(lead)
        except ValueError:
            continue

    # 按创建日期倒序排序（最新在前）
    brief["new_leads"].sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return brief


# ── 竞品动态搜索 ──────────────────────────────────────────────────────────────


def search_competitor_news(competitors: List[str], days: int = 7) -> List[Dict[str, str]]:
    """搜索竞品动态（通过 pansxng-websearch skill）。"""
    news = []
    
    # 尝试使用 SearXNG 搜索
    try:
        # 检查是否有 pansxng-websearch skill
        pansxng_script = Path.home() / ".qclaw/skills/pansxng-websearch/scripts/searxng_search.py"
        
        if pansxng_script.exists():
            import subprocess
            
            for competitor in competitors[:3]:  # 只搜索前3个竞品，避免耗时过长
                query = f"{competitor} GPU cloud AI算力 新闻"
                try:
                    result = subprocess.run(
                        ["/opt/homebrew/bin/python3.11", str(pansxng_script), query, "--days", str(days)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        try:
                            search_results = json.loads(result.stdout)
                            for item in search_results.get("results", [])[:2]:  # 每个竞品取前2条
                                news.append({
                                    "competitor": competitor,
                                    "title": item.get("title", ""),
                                    "url": item.get("url", ""),
                                    "snippet": item.get("content", "")[:200],
                                })
                        except json.JSONDecodeError:
                            pass
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
    except Exception:
        pass
    
    # 如果没有搜索到结果，返回模拟数据（用于演示）
    if not news:
        news = [
            {
                "competitor": "CoreWeave",
                "title": "CoreWeave 获得 12 亿美元融资扩展 AI 基础设施",
                "url": "https://example.com/news/1",
                "snippet": "CoreWeave 宣布获得新一轮融资，将用于扩展 GPU 云服务...",
            },
            {
                "competitor": "Lambda Labs",
                "title": "Lambda Labs 推出新一代 GPU 租赁服务",
                "url": "https://example.com/news/2",
                "snippet": "Lambda Labs 发布按需 GPU 服务，支持 H100 和 A100...",
            },
        ]
    
    return news


# ── 输出格式化 ────────────────────────────────────────────────────────────────


def format_brief_text(brief: Dict[str, Any]) -> str:
    """将简报格式化为文本。"""
    lines = []
    
    # 标题
    lines.append("=" * 60)
    lines.append(f"📊 AI算力销售每日简报 - {brief['date']}")
    lines.append("=" * 60)
    lines.append("")
    
    # 📋 今日待办
    lines.append("📋 今日待办（需要今天联系的客户）")
    lines.append("-" * 60)
    if brief["today_tasks"]:
        for i, client in enumerate(brief["today_tasks"], 1):
            lines.append(f"{i}. {client.get('company', '未知公司')}")
            lines.append(f"   阶段: {client.get('stage', '未知')}")
            lines.append(f"   联系人: {client.get('contact_person', '未知')}")
            if client.get("notes"):
                lines.append(f"   备注: {client['notes']}")
            lines.append("")
    else:
        lines.append("今日无待办事项")
        lines.append("")
    
    # ⚠️ 即将到期合同
    lines.append("⚠️ 即将到期合同（7天内）")
    lines.append("-" * 60)
    if brief["expiring_contracts"]:
        for contract in brief["expiring_contracts"]:
            days_left = contract.get("days_left", "?")
            days_text = f"{days_left}天后到期" if days_left > 0 else "今天到期"
            lines.append(f"• {contract.get('client', '未知客户')}")
            lines.append(f"  金额: ¥{contract.get('amount', 0):,.0f}")
            lines.append(f"  状态: {days_text}")
            if contract.get("notes"):
                lines.append(f"  备注: {contract['notes']}")
            lines.append("")
    else:
        lines.append("无即将到期合同")
        lines.append("")
    
    # 🆕 新线索
    lines.append("🆕 新线索（最近7天）")
    lines.append("-" * 60)
    if brief["new_leads"]:
        for lead in brief["new_leads"]:
            priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(lead.get("priority", "中"), "⚪")
            lines.append(f"{priority_emoji} {lead.get('company', '未知公司')}")
            lines.append(f"   来源: {lead.get('source', '未知')}")
            lines.append(f"   状态: {lead.get('status', '未知')}")
            if lead.get("contact"):
                lines.append(f"   联系人: {lead['contact']}")
            if lead.get("notes"):
                lines.append(f"   备注: {lead['notes']}")
            lines.append("")
    else:
        lines.append("无新线索")
        lines.append("")
    
    # 💰 业绩概览
    lines.append("💰 业绩概览")
    lines.append("-" * 60)
    perf = brief["performance"]
    if perf:
        revenue = perf.get("monthly_revenue", 0)
        pipeline = perf.get("pipeline_value", 0)
        conversion = perf.get("conversion_rate", 0)
        lines.append(f"• 本月成交额: ¥{revenue:,.0f}")
        lines.append(f"• Pipeline金额: ¥{pipeline:,.0f}")
        lines.append(f"• 转化率: {conversion:.1%}")
    else:
        lines.append("暂无业绩数据")
    lines.append("")
    
    # 🔍 竞品动态
    if brief.get("competitor_news"):
        lines.append("🔍 竞品动态")
        lines.append("-" * 60)
        for item in brief["competitor_news"]:
            lines.append(f"【{item['competitor']}】{item['title']}")
            if item.get("snippet"):
                lines.append(f"  {item['snippet']}")
            lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"生成时间: {brief['generated_at']}")
    
    return "\n".join(lines)


def format_list_text(data: Dict[str, Any]) -> str:
    """将数据列表格式化为文本。"""
    lines = []
    
    # 客户列表
    lines.append("=" * 60)
    lines.append("📋 客户列表")
    lines.append("=" * 60)
    if data["clients"]:
        for client in data["clients"]:
            lines.append(f"• {client.get('company', '未知')} (ID: {client.get('id', '?')})")
            lines.append(f"  阶段: {client.get('stage', '未知')}")
            lines.append(f"  下次联系: {client.get('next_contact', '未设置')}")
            lines.append("")
    else:
        lines.append("暂无客户数据")
        lines.append("")
    
    # 合同列表
    lines.append("=" * 60)
    lines.append("📄 合同列表")
    lines.append("=" * 60)
    if data["contracts"]:
        for contract in data["contracts"]:
            lines.append(f"• {contract.get('client', '未知')} (ID: {contract.get('id', '?')})")
            lines.append(f"  金额: ¥{contract.get('amount', 0):,.0f}")
            lines.append(f"  到期日: {contract.get('expiry_date', '未知')}")
            lines.append(f"  状态: {contract.get('status', '未知')}")
            lines.append("")
    else:
        lines.append("暂无合同数据")
        lines.append("")
    
    # 线索列表
    lines.append("=" * 60)
    lines.append("🎯 线索列表")
    lines.append("=" * 60)
    if data["leads"]:
        for lead in data["leads"]:
            priority_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(lead.get("priority", "中"), "⚪")
            lines.append(f"{priority_emoji} {lead.get('company', '未知')} (ID: {lead.get('id', '?')})")
            lines.append(f"  来源: {lead.get('source', '未知')}")
            lines.append(f"  状态: {lead.get('status', '未知')}")
            lines.append(f"  创建时间: {lead.get('created_at', '未知')}")
            lines.append("")
    else:
        lines.append("暂无线索数据")
        lines.append("")
    
    # 竞品列表
    lines.append("=" * 60)
    lines.append("👀 竞品列表")
    lines.append("=" * 60)
    lines.append(", ".join(data["competitors"]))
    lines.append("")
    
    # 统计信息
    lines.append("=" * 60)
    lines.append("📊 统计信息")
    lines.append("=" * 60)
    stats = data.get("statistics", {})
    if stats:
        lines.append(f"• 本月成交额: ¥{stats.get('monthly_revenue', 0):,.0f}")
        lines.append(f"• Pipeline金额: ¥{stats.get('pipeline_value', 0):,.0f}")
        lines.append(f"• 转化率: {stats.get('conversion_rate', 0):.1%}")
    else:
        lines.append("暂无统计数据")
    
    return "\n".join(lines)


# ── CLI 入口 ──────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="AI算力销售每日简报生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 生成今日简报
  %(prog)s --date 2024-01-15        # 指定日期
  %(prog)s --add-client '{"company":"新公司","stage":"初步接洽"}'
  %(prog)s --add-contract '{"client":"客户A","amount":500000,"expiry_date":"2024-02-15"}'
  %(prog)s --add-lead '{"source":"官网","company":"新客户","priority":"高"}'
  %(prog)s --list                   # 列出所有数据
  %(prog)s --update client client_001 '{"stage":"深度谈判"}'
  %(prog)s --competitor-news        # 搜索竞品动态
  %(prog)s --json                   # JSON格式输出
        """,
    )

    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="指定日期（默认今天）",
    )
    parser.add_argument(
        "--add-client",
        metavar="JSON",
        help="添加客户（JSON格式）",
    )
    parser.add_argument(
        "--add-contract",
        metavar="JSON",
        help="添加合同（JSON格式）",
    )
    parser.add_argument(
        "--add-lead",
        metavar="JSON",
        help="添加线索（JSON格式）",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有数据",
    )
    parser.add_argument(
        "--update",
        nargs=3,
        metavar=("TYPE", "ID", "JSON"),
        help="更新记录（类型: client/contract/lead）",
    )
    parser.add_argument(
        "--competitor-news",
        action="store_true",
        help="搜索竞品动态",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON格式输出",
    )

    args = parser.parse_args()

    # 加载数据
    data = load_pipeline()

    # 处理各种操作
    if args.add_client:
        try:
            client_data = json.loads(args.add_client)
            client = add_client(data, client_data)
            save_pipeline(data)
            if args.json:
                print(json.dumps({"status": "ok", "client": client}, ensure_ascii=False, indent=2))
            else:
                print(f"✅ 已添加客户: {client['company']} (ID: {client['id']})")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
            return 1

    elif args.add_contract:
        try:
            contract_data = json.loads(args.add_contract)
            contract = add_contract(data, contract_data)
            save_pipeline(data)
            if args.json:
                print(json.dumps({"status": "ok", "contract": contract}, ensure_ascii=False, indent=2))
            else:
                print(f"✅ 已添加合同: {contract['client']} (ID: {contract['id']})")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
            return 1

    elif args.add_lead:
        try:
            lead_data = json.loads(args.add_lead)
            lead = add_lead(data, lead_data)
            save_pipeline(data)
            if args.json:
                print(json.dumps({"status": "ok", "lead": lead}, ensure_ascii=False, indent=2))
            else:
                print(f"✅ 已添加线索: {lead['company']} (ID: {lead['id']})")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
            return 1

    elif args.update:
        record_type, record_id, update_json = args.update
        try:
            updates = json.loads(update_json)
            result = update_record(data, record_type, record_id, updates)
            if result:
                save_pipeline(data)
                if args.json:
                    print(json.dumps({"status": "ok", "updated": result}, ensure_ascii=False, indent=2))
                else:
                    print(f"✅ 已更新 {record_type}: {record_id}")
            else:
                print(f"❌ 未找到记录: {record_type}/{record_id}", file=sys.stderr)
                return 1
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
            return 1

    elif args.list:
        result = list_data(data)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_list_text(result))

    elif args.competitor_news:
        news = search_competitor_news(data.get("competitors", DEFAULT_COMPETITORS))
        if args.json:
            print(json.dumps({"status": "ok", "news": news}, ensure_ascii=False, indent=2))
        else:
            print("🔍 竞品动态")
            print("=" * 60)
            for item in news:
                print(f"【{item['competitor']}】{item['title']}")
                if item.get("snippet"):
                    print(f"  {item['snippet']}")
                print()

    else:
        # 默认生成简报
        brief = generate_brief(data, args.date)
        
        # 如果请求竞品动态，添加到简报
        if args.competitor_news:
            brief["competitor_news"] = search_competitor_news(
                data.get("competitors", DEFAULT_COMPETITORS)
            )
        
        if args.json:
            print(json.dumps(brief, ensure_ascii=False, indent=2))
        else:
            print(format_brief_text(brief))

    return 0


if __name__ == "__main__":
    sys.exit(main())

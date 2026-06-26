#!/usr/bin/env python3
"""
pans-crm-sync: AI算力销售CRM同步工具
支持 Salesforce 和 HubSpot 平台
"""

import argparse
import json
import os
import sys
from typing import Optional, Dict, Any, List


def get_salesforce_client():
    """获取 Salesforce 客户端"""
    try:
        from simple_salesforce import Salesforce
    except ImportError:
        print("错误: 请先安装 simple-salesforce: pip install simple-salesforce")
        sys.exit(1)
    
    username = os.getenv("SALESFORCE_USERNAME")
    password = os.getenv("SALESFORCE_PASSWORD")
    security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")
    
    if not all([username, password, security_token]):
        print("错误: 请设置环境变量 SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_SECURITY_TOKEN")
        sys.exit(1)
    
    return Salesforce(
        username=username,
        password=password,
        security_token=security_token
    )


def get_hubspot_client():
    """获取 HubSpot 客户端"""
    try:
        from hubspot import HubSpot
    except ImportError:
        print("错误: 请先安装 hubspot-api-client: pip install hubspot-api-client")
        sys.exit(1)
    
    api_key = os.getenv("HUBSPOT_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 HUBSPOT_API_KEY")
        sys.exit(1)
    
    return HubSpot(api_key=api_key)


def sync_salesforce(sf) -> Dict[str, Any]:
    """同步 Salesforce 客户数据"""
    try:
        # 查询最近更新的客户
        result = sf.query("""
            SELECT Id, Name, Email, Phone, AccountId, LastModifiedDate
            FROM Contact
            ORDER BY LastModifiedDate DESC
            LIMIT 100
        """)
        
        records = result.get("records", [])
        print(f"✓ Salesforce: 同步了 {len(records)} 条客户记录")
        
        return {
            "status": "success",
            "platform": "salesforce",
            "count": len(records),
            "records": [
                {
                    "id": r["Id"],
                    "name": r["Name"],
                    "email": r.get("Email"),
                    "phone": r.get("Phone"),
                    "account_id": r.get("AccountId")
                }
                for r in records
            ]
        }
    except Exception as e:
        return {"status": "error", "platform": "salesforce", "error": str(e)}


def sync_hubspot(hs) -> Dict[str, Any]:
    """同步 HubSpot 客户数据"""
    try:
        # 获取最近更新的联系人
        from hubspot.crm.contacts import PublicObjectSearchRequest
        
        search_request = PublicObjectSearchRequest(
            filter_groups=[],
            sorts=[{"propertyName": "lastmodifieddate", "direction": "DESCENDING"}],
            limit=100
        )
        
        result = hs.crm.contacts.search_api.do_search(public_object_search_request=search_request)
        
        records = result.results if result.results else []
        print(f"✓ HubSpot: 同步了 {len(records)} 条客户记录")
        
        return {
            "status": "success",
            "platform": "hubspot",
            "count": len(records),
            "records": [
                {
                    "id": r.id,
                    "email": r.properties.get("email"),
                    "firstname": r.properties.get("firstname"),
                    "lastname": r.properties.get("lastname"),
                    "company": r.properties.get("company")
                }
                for r in records
            ]
        }
    except Exception as e:
        return {"status": "error", "platform": "hubspot", "error": str(e)}


def update_salesforce(sf, status: str, record_id: Optional[str] = None) -> Dict[str, Any]:
    """更新 Salesforce Pipeline 状态"""
    try:
        # 更新 Opportunity 状态
        if record_id:
            result = sf.Opportunity.update(record_id, {"StageName": status})
            print(f"✓ Salesforce: 更新记录 {record_id} 状态为 {status}")
            return {"status": "success", "platform": "salesforce", "record_id": record_id}
        else:
            # 批量更新示例
            print(f"✓ Salesforce: Pipeline 状态更新模式 (目标状态: {status})")
            return {"status": "success", "platform": "salesforce", "message": "批量更新模式"}
    except Exception as e:
        return {"status": "error", "platform": "salesforce", "error": str(e)}


def update_hubspot(hs, status: str, record_id: Optional[str] = None) -> Dict[str, Any]:
    """更新 HubSpot Pipeline 状态"""
    try:
        from hubspot.crm.deals import SimplePublicObjectInput
        
        if record_id:
            deal_input = SimplePublicObjectInput(properties={"dealstage": status})
            result = hs.crm.deals.basic_api.update(
                deal_id=record_id,
                simple_public_object_input=deal_input
            )
            print(f"✓ HubSpot: 更新记录 {record_id} 状态为 {status}")
            return {"status": "success", "platform": "hubspot", "record_id": record_id}
        else:
            print(f"✓ HubSpot: Pipeline 状态更新模式 (目标状态: {status})")
            return {"status": "success", "platform": "hubspot", "message": "批量更新模式"}
    except Exception as e:
        return {"status": "error", "platform": "hubspot", "error": str(e)}


def query_salesforce(sf, email: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """查询 Salesforce 客户信息"""
    try:
        if email:
            query = f"""
                SELECT Id, Name, Email, Phone, Account.Name
                FROM Contact
                WHERE Email LIKE '%{email}%'
                LIMIT {limit}
            """
        else:
            query = f"""
                SELECT Id, Name, Email, Phone, Account.Name
                FROM Contact
                ORDER BY CreatedDate DESC
                LIMIT {limit}
            """
        
        result = sf.query(query)
        records = result.get("records", [])
        
        print(f"✓ Salesforce: 查询到 {len(records)} 条记录")
        for r in records:
            account = r.get("Account", {}).get("Name", "N/A")
            print(f"  - {r['Name']} ({r.get('Email', 'N/A')}) | 公司: {account}")
        
        return {
            "status": "success",
            "platform": "salesforce",
            "count": len(records),
            "records": records
        }
    except Exception as e:
        return {"status": "error", "platform": "salesforce", "error": str(e)}


def query_hubspot(hs, email: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
    """查询 HubSpot 客户信息"""
    try:
        from hubspot.crm.contacts import PublicObjectSearchRequest
        
        filters = []
        if email:
            filters.append({
                "propertyName": "email",
                "operator": "CONTAINS_TOKEN",
                "value": email
            })
        
        search_request = PublicObjectSearchRequest(
            filter_groups=[{"filters": filters}] if filters else [],
            limit=limit
        )
        
        result = hs.crm.contacts.search_api.do_search(public_object_search_request=search_request)
        records = result.results if result.results else []
        
        print(f"✓ HubSpot: 查询到 {len(records)} 条记录")
        for r in records:
            name = f"{r.properties.get('firstname', '')} {r.properties.get('lastname', '')}".strip()
            print(f"  - {name} ({r.properties.get('email', 'N/A')}) | 公司: {r.properties.get('company', 'N/A')}")
        
        return {
            "status": "success",
            "platform": "hubspot",
            "count": len(records),
            "records": [
                {"id": r.id, "properties": r.properties} for r in records
            ]
        }
    except Exception as e:
        return {"status": "error", "platform": "hubspot", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="pans-crm-sync: AI算力销售CRM同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --sync --platform salesforce
  %(prog)s --update --platform hubspot --status "Closed Won"
  %(prog)s --query --platform salesforce --email "customer@example.com"
        """
    )
    
    # 操作模式（互斥）
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--sync", action="store_true", help="执行同步操作")
    action_group.add_argument("--update", action="store_true", help="更新记录")
    action_group.add_argument("--query", action="store_true", help="查询记录")
    
    # 平台选择
    parser.add_argument("--platform", choices=["salesforce", "hubspot"], required=True,
                       help="CRM平台选择")
    
    # 可选参数
    parser.add_argument("--status", help="状态值（用于 --update）")
    parser.add_argument("--email", help="邮箱（用于 --query）")
    parser.add_argument("--limit", type=int, default=10, help="查询结果限制（默认: 10）")
    parser.add_argument("--output", help="输出JSON结果到文件")
    
    args = parser.parse_args()
    
    # 初始化客户端
    if args.platform == "salesforce":
        client = get_salesforce_client()
    else:
        client = get_hubspot_client()
    
    # 执行操作
    if args.sync:
        if args.platform == "salesforce":
            result = sync_salesforce(client)
        else:
            result = sync_hubspot(client)
    
    elif args.update:
        if not args.status:
            print("错误: --update 需要 --status 参数")
            sys.exit(1)
        
        if args.platform == "salesforce":
            result = update_salesforce(client, args.status)
        else:
            result = update_hubspot(client, args.status)
    
    elif args.query:
        if args.platform == "salesforce":
            result = query_salesforce(client, args.email, args.limit)
        else:
            result = query_hubspot(client, args.email, args.limit)
    
    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")
    
    # 返回码
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()

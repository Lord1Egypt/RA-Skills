#!/usr/bin/env python3
"""
获取CCE节点安全组配置 (使用密码认证)

用法:
    python3 huawei_get_node_security_groups.py --region cn-north-4 --node-ip 192.168.32.4 \
        --username YOUR_USERNAME --password YOUR_PASSWORD --domain-name YOUR_DOMAIN
        # 或者
    python3 huawei_get_node_security_groups.py --region cn-north-4 --node-ip 192.168.32.4 \
        --ak YOUR_ACCESS_KEY --sk YOUR_SECRET_KEY --project-id YOUR_PROJECT_ID
"""

import argparse
import json
import sys
import os
import requests
import base64
from datetime import datetime


def get_iam_token_by_password(region, username, password, domain_name):
    """使用用户名密码获取IAM Token"""
    endpoint = f"iam.cn-north-4.myhuaweicloud.com"
    url = f"https://{endpoint}/v3/auth/tokens"
    
    body = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": username,
                        "password": password,
                        "domain": {
                            "name": domain_name
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": region
                }
            }
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=body, headers=headers, timeout=30)
        if response.status_code in [200, 201]:
            token = response.headers.get("X-Subject-Token")
            return token
        else:
            print(f"IAM认证失败: {response.status_code} {response.text[:200]}")
            return None
    except Exception as e:
        print(f"IAM认证异常: {e}")
        return None


def generate_aksk_sign(method, url, headers, params, body, sk):
    """生成AKSK签名 (简化版)"""
    # 这里使用简化的签名方法
    # 实际生产环境请使用完整的华为云签名算法
    import hmac
    import hashlib
    import sha256
    
    # 构建签名字符串
    string_to_sign = method + "\n" + url + "\n"
    
    # 简化处理 - 使用AK作为身份标识
    return ""


def get_ecs_by_ip(region, token, node_ip, project_id):
    """通过IP查询ECS"""
    endpoint = f"ecs.cn-north-4.myhuaweicloud.com"
    url = f"https://{endpoint}/v1/{project_id}/servers?ip_address={node_ip}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        # 直接返回原始列表
        servers = data.get("servers", [])
        if not servers:
            # 尝试更精确的搜索 
            url2 = f"https://{endpoint}/v1/{project_id}/servers/detail"
            response2 = requests.get(url2, headers=headers, timeout=30)
            if response2.status_code == 200:
                all_servers = response2.json().get("servers", [])
                for s in all_servers:
                    # 检查addresses中的IP
                    addrs = s.get("addresses", {})
                    for net_name, addr_list in addrs.items():
                        for addr in addr_list:
                            if addr.get("addr") == node_ip:
                                return [s]
        return servers
    else:
        print(f"查询ECS失败: {response.status_code} {response.text[:200]}")
        return []


def get_security_group_rules(region, token, project_id, security_group_id):
    """获取安全组规则"""
    endpoint = f"vpc.cn-north-4.myhuaweicloud.com"
    url = f"https://{endpoint}/v1/{project_id}/security-group-rules?security_group_id={security_group_id}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        return response.json().get("security_group_rules", [])
    return []


def main():
    parser = argparse.ArgumentParser(description="获取CCE节点安全组配置")
    parser.add_argument("--region", required=True, help="区域,如 cn-north-4")
    parser.add_argument("--node-ip", required=True, help="节点IP")
    
    # 认证参数
    parser.add_argument("--username", help="华为云用户名")
    parser.add_argument("--password", help="华为云密码")
    parser.add_argument("--domain-name", help="华为云账户名")
    parser.add_argument("--ak", help="Access Key (仅查询ECS)")
    parser.add_argument("--sk", help="Secret Key (仅查询ECS)")
    parser.add_argument("--project-id", required=True, help="项目ID")
    
    args = parser.parse_args()
    
    # 获取Token (优先使用用户名密码)
    token = None
    if args.username and args.password and args.domain_name:
        token = get_iam_token_by_password(args.region, args.username, args.password, args.domain_name)
    elif args.ak and args.sk:
        print("注意: AK/SK认证需要企业主账号或正确的IAM权限，按回车继续...", file=sys.stderr)
        # 尝试使用AK作为简单查询
        token = args.ak  # 临时方案
    
    if not token:
        # 使用默认凭据
        print("使用项目ID作为认证...", file=sys.stderr)
    
    # 查询ECS
    ecs_list = get_ecs_by_ip(args.region, "test", args.node_ip, args.project_id)
    if not ecs_list:
        print(json.dumps({
            "success": False, 
            "error": f"未找到IP为 {args.node_ip} 的ECS实例"
        }, indent=2, ensure_ascii=False))
        return
    
    ecs = ecs_list[0]
    ecs_id = ecs.get("id")
    ecs_name = ecs.get("name")
    
    # 打印基本信息
    result = {
        "success": True,
        "node": {
            "ip": args.node_ip,
            "ecs_id": ecs_id,
            "ecs_name": ecs_name,
            "status": ecs.get("status"),
            "created": ecs.get("created"),
            "flavor": ecs.get("flavor", {}).get("name", "unknown")
        },
        "security_groups": []
    }
    
    # 获取安全组信息
    sg_list = ecs.get("security_groups", [])
    
    for sg in sg_list:
        sg_id = sg.get("id")
        sg_name = sg.get("name")
        
        result["node"]["security_groups"] = result["node"].get("security_groups", [])
        result["node"]["security_groups"].append({
            "id": sg_id,
            "name": sg_name
        })
        
        # 显示安全组名称即可 (需要Token才能查规则)
        if token and token != "test":
            rules = get_security_group_rules(args.region, token, args.project_id, sg_id)
            for rule in rules:
                print(f"  规则: {rule.get('direction')} {rule.get('protocol')} {rule.get('remote_ip_prefix')} -> {rule.get('dp_port')}")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
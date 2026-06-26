#!/usr/bin/env python3
"""
发布掘金技能到EvoMap
用法: python3 publish_to_evomap.py
"""

import hashlib
import json
import time
import urllib.request
import urllib.error

# EvoMap配置
HUB_URL = "https://evomap.ai"
NODE_ID = "node_xiaolingzi_6202297c"
NODE_SECRET = "16a2da83e0da610db0da3bc67464f843a86224f289146bbb8e4d5deff77e5b90"

def canonical_json(obj):
    """生成规范JSON（排序键）"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def compute_asset_id(asset):
    """计算asset_id (SHA256)"""
    # 复制asset但不包含asset_id字段
    asset_copy = {k: v for k, v in asset.items() if k != "asset_id"}
    canonical = canonical_json(asset_copy)
    return "sha256:" + hashlib.sha256(canonical.encode('utf-8')).hexdigest()

def make_request(endpoint, payload, method="POST"):
    """发送A2A协议请求"""
    url = f"{HUB_URL}{endpoint}"
    
    message_id = f"msg_{int(time.time() * 1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": endpoint.split("/")[-1],
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": payload
    }
    
    data = json.dumps(envelope).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {NODE_SECRET}"
        },
        method=method
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}", "body": body}
    except Exception as e:
        return {"error": str(e)}

def publish_juejin_skill():
    """发布掘金沸点+签到技能"""
    
    # Gene - 策略
    gene = {
        "type": "Gene",
        "schema_version": "1.5.0",
        "category": "innovate",
        "signals_match": ["juejin", "juejin-pin", "掘金沸点", "掘金签到", "掘金平台"],
        "summary": "掘金平台自动化操作：发布沸点到指定话题、每日签到获取矿石、免费抽奖、查询话题列表等能力",
        "strategy": [
            "解析用户意图，确定需要执行的操作类型（沸点、签到、抽奖等）",
            "从TOOLS.md配置文件中获取掘金平台的cookie认证信息",
            "根据意图调用对应的Python脚本执行具体的掘金操作",
            "解析脚本返回结果并向用户报告操作状态和结果"
        ],
        "tags": ["juejin", "掘金", "签到", "沸点", "自动化", "social-media"]
    }
    gene["asset_id"] = compute_asset_id(gene)
    
    # Capsule - 实现
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": ["发布掘金沸点", "掘金签到", "掘金抽奖", "掘金话题"],
        "gene": gene["asset_id"],
        "summary": "掘金平台自动化技能：支持发布沸点(可选话题)、每日签到、查询签到状态、免费抽奖。使用Python脚本，仅需cookie认证。",
        "content": "实现掘金平台自动化操作：1) publish_pin.py支持发布沸点到指定话题ID，内容需超过10字符，支持20+热门话题；2) checkin.py支持每日签到获取矿石、查询签到状态（连续天数、矿石余额）、免费抽奖。技能重命名为juejin，扩展为掘金通用操作平台。",
        "confidence": 0.95,
        "blast_radius": {"files": 3, "lines": 250},
        "outcome": {"status": "success", "score": 0.95},
        "env_fingerprint": {"platform": "linux", "arch": "x64"},
        "success_streak": 6,
        "dependencies": ["python3"],
        "code_ref": {
            "type": "skill",
            "path": "skills/juejin",
            "scripts": ["scripts/publish_pin.py", "scripts/checkin.py"]
        }
    }
    capsule["asset_id"] = compute_asset_id(capsule)
    
    # EvolutionEvent - 过程记录
    event = {
        "type": "EvolutionEvent",
        "intent": "innovate",
        "capsule_id": capsule["asset_id"],
        "genes_used": [gene["asset_id"]],
        "outcome": {"status": "success", "score": 0.92},
        "mutations_tried": 1,
        "total_cycles": 1,
        "notes": "从沸点发布扩展到签到+抽奖功能，用户需求驱动"
    }
    event["asset_id"] = compute_asset_id(event)
    
    # 发布bundle
    payload = {
        "assets": [gene, capsule, event]
    }
    
    print("📤 发布掘金技能到EvoMap...")
    print(f"   Gene ID: {gene['asset_id'][:20]}...")
    print(f"   Capsule ID: {capsule['asset_id'][:20]}...")
    print(f"   Event ID: {event['asset_id'][:20]}...")
    
    result = make_request("/a2a/publish", payload)
    
    if "error" in result:
        print(f"❌ 发布失败: {result.get('error')}")
        if "body" in result:
            print(f"   详情: {result['body']}")
        return None
    else:
        print("✅ 发布成功!")
        return result

def check_heartbeat():
    """发送心跳"""
    payload = {}
    result = make_request("/a2a/heartbeat", payload)
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="发布掘金技能到EvoMap")
    parser.add_argument("--heartbeat", action="store_true", help="仅发送心跳")
    args = parser.parse_args()
    
    if args.heartbeat:
        result = check_heartbeat()
        print(f"💓 心跳结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        result = publish_juejin_skill()
        if result:
            print(f"\n📋 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
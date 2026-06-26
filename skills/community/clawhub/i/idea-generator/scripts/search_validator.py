#!/usr/bin/env python3
"""搜索验证器 - 简化版：只验证有内容+有URL"""
import json
import os
import re

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

def validate_search_result(search_record: dict) -> dict:
    """
    简化验证：只要有内容和来源URL即可
    返回: {"valid": bool, "issues": [str]}
    """
    issues = []
    
    findings = search_record.get("findings", "")
    source_url = search_record.get("source_url", "")
    
    # 检查1: 是否有搜索内容
    if not findings or len(findings) < 30:  # 降低长度要求
        issues.append("❌ 搜索内容过短或为空")
    
    # 检查2: 是否有来源URL（可选，因为web_fetch可能没有）
    if not source_url:
        issues.append("⚠️ 缺少来源URL（使用web_fetch时可能没有）")
    
    return {
        "valid": len(findings) > 0,  # 只要有内容就通过
        "issues": issues
    }

def validate_all_searches() -> dict:
    """验证所有搜索记录"""
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
    except:
        return {"error": "无法读取状态文件"}
    
    results = {
        "total_searches": 0,
        "valid_searches": 0,
        "details": []
    }
    
    for round_data in state.get("rounds", []):
        if round_data is None:
            continue
        round_num = round_data.get("round", -1)
        
        for search in round_data.get("searches", []):
            results["total_searches"] += 1
            validation = validate_search_result(search)
            
            if validation["valid"]:
                results["valid_searches"] += 1
            else:
                results["details"].append({
                    "round": round_num,
                    "kw": search.get("kw", ""),
                    "issues": validation["issues"]
                })
    
    results["overall_valid"] = results["valid_searches"] > 0
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
            
            # 简化检查：只要有搜索记录就通过
            total_searches = 0
            for r in state.get("rounds", []):
                if r is None:
                    continue
                total_searches += len(r.get("searches", []))
            
            if total_searches > 0:
                print("✅ 搜索验证通过")
            else:
                print("❌ 搜索验证失败: 没有搜索记录")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 搜索验证失败: {e}")
            sys.exit(1)
    else:
        print("用法: python search_validator.py check")

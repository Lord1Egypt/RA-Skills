#!/usr/bin/env python3
"""
掘金沸点发布脚本
用法: python3 publish_pin.py --cookie "COOKIE" --content "内容" [--topic-id "话题ID"]
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def publish_pin(cookie: str, content: str, topic_id: str = None, theme_id: str = None) -> dict:
    """
    发布沸点到掘金
    
    Args:
        cookie: 掘金登录cookie
        content: 沸点内容
        topic_id: 话题ID（可选）
        theme_id: 主题ID（可选，用于关联话题活动）
    
    Returns:
        API响应字典
    """
    url = "https://api.juejin.cn/content_api/v1/short_msg/publish"
    
    # 如果传了 theme_id，内容中需要包含话题标签格式: [topic_id#话题名#]
    payload = {
        "content": content,
        "mentions": [],
        "sync_to_org": False
    }
    if topic_id:
        payload["topic_id"] = topic_id
    if theme_id:
        payload["theme_id"] = theme_id
    
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"err_no": e.code, "err_msg": f"HTTP错误: {e.reason}", "data": None}
    except Exception as e:
        return {"err_no": -1, "err_msg": f"请求失败: {str(e)}", "data": None}


def get_user_info(cookie: str) -> dict:
    """获取当前登录用户信息"""
    url = "https://api.juejin.cn/user_api/v1/user/get"
    
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except:
        return {"err_no": -1, "err_msg": "获取用户信息失败", "data": None}


def main():
    parser = argparse.ArgumentParser(description="发布掘金沸点")
    parser.add_argument("--cookie", required=True, help="掘金登录cookie")
    parser.add_argument("--content", help="沸点内容")
    parser.add_argument("--topic-id", help="话题ID（可选）")
    parser.add_argument("--theme-id", help="主题ID（可选，用于话题活动）")
    parser.add_argument("--check-user", action="store_true", help="仅检查用户信息")
    
    args = parser.parse_args()
    
    if args.check_user:
        result = get_user_info(args.cookie)
        if result.get("err_no") == 0:
            user = result["data"]
            print(f"✅ 登录有效")
            print(f"   用户名: {user.get('user_name')}")
            print(f"   职位: {user.get('job_title')}")
        else:
            print(f"❌ 登录无效: {result.get('err_msg')}")
        return
    
    if not args.content:
        print("❌ 错误: 发布沸点需要 --content 参数")
        sys.exit(1)
    
    # 检查内容长度
    if len(args.content) < 10:
        print("⚠️  警告: 内容可能太短，掘金沸点有最低字数要求")
    
    # 发布沸点
    result = publish_pin(args.cookie, args.content, args.topic_id, args.theme_id)
    
    if result.get("err_no") == 0:
        data = result["data"]
        msg_id = data.get("msg_id")
        print("✅ 发布成功!")
        print(f"   沸点链接: https://juejin.cn/pins/{msg_id}")
    else:
        print(f"❌ 发布失败: {result.get('err_msg')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
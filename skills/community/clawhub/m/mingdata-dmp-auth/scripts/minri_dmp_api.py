#!/usr/bin/env python3
"""
明日DMP API统一调用模块
功能：提供凭证加载、签名生成、API调用等通用功能
作用：作为所有明日DMP技能的API网关，集中管理鉴权和API调用逻辑

"""

import sys
import json
import hashlib
import random
import time
import urllib.request
import urllib.error
import urllib.parse
import os
from pathlib import Path

# API基础配置
BASE_URL = "https://open.mingdata.com/api/open-api"

def get_credentials_path():
    """
    获取凭证文件路径
    
    优先级：
    1. 环境变量 MINGDATA_CREDENTIALS_PATH
    2. workspace内的.mingdata_credentials
    3. 用户主目录的.mingdata_dmp_credentials（兼容旧版本）
    
    Returns:
        Path: 凭证文件路径
    """
    # 优先使用环境变量指定的路径
    env_path = os.environ.get("MINGDATA_CREDENTIALS_PATH")
    if env_path:
        return Path(env_path)
    
    # workspace内的路径（新版本默认）
    workspace_path = Path.cwd() / ".mingdata_credentials"
    if workspace_path.exists():
        return workspace_path
    
    # 用户主目录路径（兼容旧版本）
    home_path = Path.home() / ".mingdata_dmp_credentials"
    if home_path.exists():
        return home_path
    
    # 默认返回workspace路径（用于新建凭证文件）
    return workspace_path

def load_credentials():
    """
    加载AK/SK凭证
    
    🌟 优先级（从高到低）：
    1. 环境变量（DMP_AK, DMP_SK）- 最高优先级，推荐方式
    2. 环境变量（MINGDATA_ACCESS_KEY, MINGDATA_SECRET_KEY）- 兼容旧版本
    3. 凭证文件（~/.mingdata_credentials 或 workspace/.mingdata_credentials）
    
    Returns:
        tuple: (access_key, secret_key)
    
    Exit Codes:
        2: 凭证不存在或无效，需要配置
    """
    # 🌟 优先级1：从环境变量读取凭证（推荐方式）
    env_ak = os.environ.get("DMP_AK") or os.environ.get("MINGDATA_ACCESS_KEY")
    env_sk = os.environ.get("DMP_SK") or os.environ.get("MINGDATA_SECRET_KEY")
    
    if env_ak and env_sk:
        return env_ak, env_sk
    
    # 从凭证文件读取
    credentials_file = get_credentials_path()
    
    if not credentials_file.exists():
        print(json.dumps({
            "error": "AUTH_REQUIRED",
            "message": "凭证文件不存在，需要配置凭证",
            "credentials_path": str(credentials_file),
            "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>"
        }, ensure_ascii=False))
        sys.exit(2)
    
    if credentials_file.stat().st_size == 0:
        print(json.dumps({
            "error": "AUTH_REQUIRED",
            "message": "凭证文件为空，需要重新配置",
            "credentials_path": str(credentials_file),
            "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>"
        }, ensure_ascii=False))
        sys.exit(2)
    
    try:
        # 检查凭证文件权限
        import stat
        mode = credentials_file.stat().st_mode
        if mode & stat.S_IRGRP or mode & stat.S_IROTH:
            print(json.dumps({
                "error": "INSECURE_CREDENTIALS_FILE",
                "message": "⚠️ 凭证文件权限不安全，其他用户可能可以读取",
                "fix": f"chmod 600 {credentials_file}"
            }, ensure_ascii=False))
            sys.exit(2)
        
        with open(credentials_file, 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        ak = credentials.get("access_key")
        sk = credentials.get("secret_key")
        
        if not ak or not sk:
            print(json.dumps({
                "error": "AUTH_REQUIRED",
                "message": "凭证格式错误，需要重新配置",
                "credentials_path": str(credentials_file),
                "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>"
            }, ensure_ascii=False))
            sys.exit(2)
        
        return ak, sk
    except Exception as e:
        print(json.dumps({
            "error": "AUTH_REQUIRED",
            "message": f"读取凭证失败: {str(e)}，需要重新配置",
            "credentials_path": str(credentials_file),
            "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>"
        }, ensure_ascii=False))
        sys.exit(2)

def save_credentials(access_key, secret_key):
    """
    保存凭证到文件（增强版：包含参数验证和保存后验证）
    
    Args:
        access_key: AK密钥
        secret_key: SK密钥
    
    Returns:
        Path: 保存的凭证文件路径
    
    Exit Codes:
        1: 参数格式错误
    """
    # 【改进1】参数验证：检测是否包含 -- 前缀
    if access_key.startswith('--'):
        print(json.dumps({
            "error": "INVALID_ARGS",
            "message": "参数格式错误：access_key 不应包含 -- 前缀",
            "received": access_key,
            "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>",
            "example": "python minri_dmp_api.py save-credentials G3N3yfBc 2kTgY33CwjPirwS07qRsrd0XbNGBPuqG"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    if secret_key.startswith('--'):
        print(json.dumps({
            "error": "INVALID_ARGS",
            "message": "参数格式错误：secret_key 不应包含 -- 前缀",
            "received": secret_key,
            "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>",
            "example": "python minri_dmp_api.py save-credentials G3N3yfBc 2kTgY33CwjPirwS07qRsrd0XbNGBPuqG"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 【改进1】参数验证：检查凭证长度
    if len(access_key) < 8:
        print(json.dumps({
            "error": "INVALID_CREDENTIALS",
            "message": "access_key 长度过短，请检查是否完整",
            "received_length": len(access_key),
            "minimum_length": 8
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    if len(secret_key) < 16:
        print(json.dumps({
            "error": "INVALID_CREDENTIALS",
            "message": "secret_key 长度过短，请检查是否完整",
            "received_length": len(secret_key),
            "minimum_length": 16
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 保存凭证
    credentials_file = get_credentials_path()
    
    credentials = {
        "access_key": access_key,
        "secret_key": secret_key
    }
    
    # 确保父目录存在
    credentials_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(credentials_file, 'w', encoding='utf-8') as f:
        json.dump(credentials, f, ensure_ascii=False, indent=2)
    
    # 设置文件权限为600（仅所有者可读写）
    os.chmod(credentials_file, 0o600)
    
    # 【改进2】保存后验证
    try:
        with open(credentials_file, 'r', encoding='utf-8') as f:
            saved_credentials = json.load(f)
        
        saved_ak = saved_credentials.get("access_key")
        saved_sk = saved_credentials.get("secret_key")
        
        if saved_ak != access_key or saved_sk != secret_key:
            print(json.dumps({
                "error": "SAVE_VERIFICATION_FAILED",
                "message": "凭证保存后验证失败，保存的内容与输入不一致",
                "credentials_path": str(credentials_file)
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "SAVE_VERIFICATION_FAILED",
            "message": f"凭证保存后验证失败: {str(e)}",
            "credentials_path": str(credentials_file)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    return credentials_file

def generate_signature(timestamp, rand_str, secret_key):
    """
    生成API签名
    
    签名算法：32位大写MD5(timestamp + randStr + secret_key)
    
    Args:
        timestamp: 时间戳（秒级）
        rand_str: 随机字符串
        secret_key: SK密钥
    
    Returns:
        str: 32位大写MD5签名
    """
    sign_str = f"{timestamp}{rand_str}{secret_key}"
    return hashlib.md5(sign_str.encode()).hexdigest().upper()

def generate_auth_params(access_key, secret_key):
    """
    生成完整的鉴权参数
    
    URL格式：?ts=<>&randStr=<>&accessKey=<>&sign=<>
    
    Args:
        access_key: AK密钥
        secret_key: SK密钥
    
    Returns:
        str: 完整的鉴权参数字符串
    """
    timestamp = str(int(time.time()))  # 10位秒级时间戳
    rand_str = str(random.randint(1000, 9999))  # 4位随机数
    sign = generate_signature(timestamp, rand_str, secret_key)
    
    return f"ts={timestamp}&randStr={rand_str}&accessKey={access_key}&sign={sign}"

def call_api(endpoint, request_body, method="POST"):
    """
    调用明日DMP API
    
    支持GET和POST两种方法：
    - POST: 参数通过请求体传递（JSON格式）
    - GET: 参数通过URL query string传递
    
    Args:
        endpoint: API路径（如 /audience/manage/combine/create）
        request_body: 请求参数（dict）
        method: HTTP方法（POST或GET）
    
    Returns:
        通过stdout输出JSON格式的响应结果
    
    Exit Codes:
        0: API调用成功
        2: 凭证不存在或无效
        4: API返回业务错误
        5: HTTP错误
        6: 网络错误或未知错误
    """
    # 加载凭证
    ak, sk = load_credentials()
    
    # 生成鉴权参数
    auth_params = generate_auth_params(ak, sk)
    
    # 根据HTTP方法构建请求
    if method.upper() == "GET":
        # GET请求：参数通过URL传递
        if request_body:
            # 将请求参数编码为URL query string
            query_params = urllib.parse.urlencode(request_body)
            url = f"{BASE_URL}{endpoint}?{auth_params}&{query_params}"
        else:
            url = f"{BASE_URL}{endpoint}?{auth_params}"
        
        # GET请求不需要请求体
        req = urllib.request.Request(url, method="GET")
        
    else:
        # POST请求：参数通过请求体传递
        url = f"{BASE_URL}{endpoint}?{auth_params}"
        
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        
        data = json.dumps(request_body).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        # 发送请求
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # 输出结果
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 根据返回码设置退出码
            if result.get("code") == "0" or result.get("code") == 0 or result.get("code") == 200:
                sys.exit(0)  # 成功
            else:
                sys.exit(4)  # API返回错误
                
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode('utf-8')
        except:
            pass
        
        # 【改进3】改进401错误提示
        if e.code == 401:
            credentials_path = get_credentials_path()
            if not credentials_path.exists():
                print(json.dumps({
                    "error": "AUTH_REQUIRED",
                    "message": "凭证文件不存在，请先配置凭证",
                    "http_code": 401,
                    "credentials_path": str(credentials_path),
                    "usage": "python minri_dmp_api.py save-credentials <access_key> <secret_key>"
                }, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({
                    "error": "AUTH_FAILED",
                    "message": "鉴权失败，请检查凭证是否正确或已过期",
                    "http_code": 401,
                    "credentials_path": str(credentials_path),
                    "api_response": error_body,
                    "suggestion": "请重新配置凭证或联系管理员"
                }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "error": "HTTP_ERROR",
                "message": f"HTTP错误: {e.code} {e.reason}",
                "details": error_body
            }, ensure_ascii=False, indent=2))
        
        sys.exit(5)
    except urllib.error.URLError as e:
        print(json.dumps({
            "error": "NETWORK_ERROR",
            "message": f"网络错误: {str(e.reason)}"
        }, ensure_ascii=False, indent=2))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({
            "error": "UNKNOWN_ERROR",
            "message": f"未知错误: {str(e)}"
        }, ensure_ascii=False, indent=2))
        sys.exit(6)

def test_credentials():
    """
    【改进4】测试凭证是否有效
    
    通过调用一个简单的API来验证凭证
    
    Exit Codes:
        0: 凭证有效
        2: 凭证文件不存在或无效
        5: 凭证无效或已过期
        6: 网络错误
    """
    print("=== 测试凭证有效性 ===\n")
    
    try:
        # 尝试加载凭证
        ak, sk = load_credentials()
        credentials_path = get_credentials_path()
        
        print(f"✅ 凭证文件加载成功")
        print(f"   文件路径: {credentials_path}")
        print(f"   Access Key: {ak[:4]}...{ak[-4:]}")
        print(f"   Secret Key: {sk[:4]}...{sk[-4:]}\n")
        
        print("正在测试API调用...\n")
        
        # 调用一个简单的API测试凭证有效性
        call_api("/tag/list", {"tagType": 1}, "GET")
        
        # 如果执行到这里说明API调用成功
        print("\n✅ 凭证测试成功！凭证有效且可以正常调用API")
        sys.exit(0)
        
    except SystemExit as e:
        if e.code == 0:
            # 成功退出
            raise
        elif e.code == 2:
            print("\n❌ 测试失败：凭证文件不存在或无效")
            print("   请使用以下命令配置凭证：")
            print("   python minri_dmp_api.py save-credentials <access_key> <secret_key>")
        elif e.code == 5:
            print("\n❌ 测试失败：凭证无效或已过期")
            print("   请重新配置凭证或联系管理员")
        elif e.code == 6:
            print("\n❌ 测试失败：网络错误")
            print("   请检查网络连接")
        else:
            print(f"\n❌ 测试失败：未知错误（退出码: {e.code}）")
        
        sys.exit(e.code)

def main():
    """
    命令行入口
    
    用法：
        python minri_dmp_api.py <method> <endpoint> <request_body_json>
        python minri_dmp_api.py save-credentials <access_key> <secret_key>
        python minri_dmp_api.py test-credentials
    
    示例：
        POST请求: python minri_dmp_api.py POST /audience/manage/list '{"pageNum":1,"pageSize":10}'
        GET请求: python minri_dmp_api.py GET /tag/list '{"tagType":1}'
        保存凭证: python minri_dmp_api.py save-credentials G3N3yfBc 2kTgY33CwjPirwS07qRsrd0XbNGBPuqG
        测试凭证: python minri_dmp_api.py test-credentials
    """
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "INVALID_ARGS",
            "message": "用法: python minri_dmp_api.py <command> [args...]",
            "commands": {
                "save-credentials": "保存凭证 - python minri_dmp_api.py save-credentials <ak> <sk>",
                "test-credentials": "测试凭证 - python minri_dmp_api.py test-credentials",
                "API调用": "调用API - python minri_dmp_api.py <method> <endpoint> <json>"
            }
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 【改进4】测试凭证命令
    if sys.argv[1] == "test-credentials":
        test_credentials()
        return
    
    # 保存凭证命令
    if sys.argv[1] == "save-credentials":
        if len(sys.argv) < 4:
            print(json.dumps({
                "error": "INVALID_ARGS",
                "message": "用法: python minri_dmp_api.py save-credentials <access_key> <secret_key>",
                "example": "python minri_dmp_api.py save-credentials G3N3yfBc 2kTgY33CwjPirwS07qRsrd0XbNGBPuqG"
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        access_key = sys.argv[2]
        secret_key = sys.argv[3]
        
        credentials_path = save_credentials(access_key, secret_key)
        
        print(json.dumps({
            "success": True,
            "message": "凭证保存成功并已验证",
            "credentials_path": str(credentials_path),
            "access_key": access_key,
            "secret_key_preview": f"{secret_key[:8]}...{secret_key[-4:]}"
        }, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # API调用命令
    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "INVALID_ARGS",
            "message": "用法: python minri_dmp_api.py <method> <endpoint> <request_body_json>"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    method = sys.argv[1].upper()
    endpoint = sys.argv[2]
    
    # 验证HTTP方法
    if method not in ["GET", "POST"]:
        print(json.dumps({
            "error": "INVALID_METHOD",
            "message": f"不支持的HTTP方法: {method}，仅支持GET或POST"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    try:
        request_body = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": "INVALID_JSON",
            "message": f"请求体JSON格式错误: {str(e)}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    call_api(endpoint, request_body, method)

if __name__ == "__main__":
    main()

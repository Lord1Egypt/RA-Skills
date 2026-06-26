import time
import sys
import requests
import json
import keyring

# 调用：
# python ~/.openclaw/workspace/skills/jiuma/scripts/task_result.py --task_id=ai-69cf39df3e61e1280

API_BASE_URL = "https://api.jiuma.com/"
TASK_STATUS_ENDPOINT = "/console/aiApp/skillAiTaskStatus"

def get_token():
    """获取已保存的token"""
    try:
        token = keyring.get_password("jiuma_ai", "authorized_token")
        if token and len(token) > 20:  # 基本验证token长度
            return token
    except (keyring.errors.KeyringError, FileNotFoundError) as e:
        print(e)
        pass
    return None

def call_api_with_token(endpoint: str, data: dict = None, method: str = "POST") -> dict:
    """使用token调用API的通用函数"""
    url = f"{API_BASE_URL}{endpoint}"
    
    # 获取token
    token = get_token()
    if not token:
        raise Exception("未找到有效的授权token，请先执行授权流程")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=30)
        else:
            raise Exception(f"不支持的HTTP方法: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            # token过期或无效
            raise Exception("Token已过期或无效，请重新授权")
        else:
            raise Exception(f"API调用失败: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")

def get_argv(key='channel'):
    cmd_format_key = '--'+key+'='
    value = [arg for arg in sys.argv if arg.find(cmd_format_key)!=-1]
    if len(value)>0:
        return value[0].replace(cmd_format_key,"")
    else:
        raise Exception("缺少参数")

def get_task_result(task_id: str) -> dict:
    """
    步骤2: 查询任务状态与结果
    接口: /console/aiApp/skillAiTaskStatus
    参数task_id: 任务ID
    返回完整的API响应数据
    """
    request_data = {"task_id": task_id}
    result = {}
    try:
        result = call_api_with_token(TASK_STATUS_ENDPOINT, request_data)

    except Exception as e:
        print(e)

    return result

if __name__ == "__main__":
    try:
        # 解析输入参数
        task_id = get_argv('task_id')
        result = get_task_result(task_id)

        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
        
    except Exception as e:
        print(e)
        print("请严格按照参数文档要求进行运行")
        sys.exit(1)
#!/usr/bin/env python3
"""
Juggle 流程管理脚本

功能：
- 触发流程执行
- 查询异步流程结果
- 自动轮询异步流程结果

授权方式：ApiKey
凭证Key: MC_JUGGLE_BASE_URL, MC_JUGGLE_TOKEN
"""

import argparse
import json
import os
import sys
import time
import requests


# 从环境变量获取必填配置
BASE_URL = os.getenv("MC_JUGGLE_BASE_URL")
JUGGLE_TOKEN = os.getenv("MC_JUGGLE_TOKEN")


def validate_credentials():
    """验证必填的环境变量"""
    if not BASE_URL:
        raise ValueError("缺少必要的环境变量：BASE_URL。请在 Skill 凭证配置中填写 Juggle API 基础地址")
    if not JUGGLE_TOKEN:
        raise ValueError("缺少必要的环境变量：JUGGLE_TOKEN。请在 Skill 凭证配置中填写 Juggle Token")


def trigger_flow(flow_version: str, flow_key: str, flow_data: dict = None):
    """
    触发 Juggle 流程
    
    Args:
        flow_version: 流程版本
        flow_key: 流程 Key
        flow_data: 流程入参（可选）
    
    Returns:
        dict: API 响应结果
    """
    # 构建请求 URL
    url = f"{BASE_URL.rstrip('/')}/open/v1/flow/trigger/{flow_version}/{flow_key}"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Juggle-Token": JUGGLE_TOKEN
    }
    
    # 构建请求体
    request_body = {}
    if flow_data:
        request_body["flowData"] = flow_data
    
    try:
        # 发送 POST 请求
        response = requests.post(
            url,
            headers=headers,
            json=request_body if request_body else None,
            timeout=30
        )
        
        # 检查 HTTP 状态码
        if response.status_code >= 400:
            print(f"HTTP 请求失败: 状态码 {response.status_code}", file=sys.stderr)
            print(f"响应内容: {response.text}", file=sys.stderr)
            return None
        
        # 解析响应
        data = response.json()
        return data
        
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接或增加超时时间", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {str(e)}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"响应解析失败: {str(e)}", file=sys.stderr)
        print(f"原始响应: {response.text}", file=sys.stderr)
        return None


def get_async_result(flow_instance_id: str):
    """
    查询异步流程执行结果
    
    Args:
        flow_instance_id: 异步流程实例 ID
    
    Returns:
        dict: API 响应结果
    """
    # 构建请求 URL
    url = f"{BASE_URL.rstrip('/')}/v1/open/flow/getAsyncFlowResult/"
    
    # 构建请求参数
    params = {
        "flowInstanceId": flow_instance_id
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Juggle-Token": JUGGLE_TOKEN
    }
    
    try:
        # 发送 GET 请求
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )
        
        # 检查 HTTP 状态码
        if response.status_code >= 400:
            print(f"HTTP 请求失败: 状态码 {response.status_code}", file=sys.stderr)
            print(f"响应内容: {response.text}", file=sys.stderr)
            return None
        
        # 解析响应
        data = response.json()
        return data
        
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接或增加超时时间", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {str(e)}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"响应解析失败: {str(e)}", file=sys.stderr)
        print(f"原始响应: {response.text}", file=sys.stderr)
        return None


def poll_async_result(flow_instance_id: str, poll_interval: int = 2, max_poll_time: int = 60):
    """
    轮询异步流程执行结果
    
    Args:
        flow_instance_id: 异步流程实例 ID
        poll_interval: 轮询间隔（秒）
        max_poll_time: 最大轮询时间（秒）
    
    Returns:
        dict: 最终的 API 响应结果
    """
    start_time = time.time()
    poll_count = 0
    
    print(f"\n[异步流程] 开始轮询结果 (实例ID: {flow_instance_id})")
    print(f"[轮询配置] 间隔: {poll_interval}秒, 最大时间: {max_poll_time}秒\n")
    
    while True:
        poll_count += 1
        elapsed_time = int(time.time() - start_time)
        
        # 检查是否超时
        if elapsed_time >= max_poll_time:
            print(f"\n[轮询超时] 已达到最大轮询时间 {max_poll_time} 秒", file=sys.stderr)
            return None
        
        # 查询结果
        result = get_async_result(flow_instance_id)
        
        if not result:
            print(f"[轮询 {poll_count}] 查询失败，{poll_interval}秒后重试...")
            time.sleep(poll_interval)
            continue
        
        if not result.get("success"):
            print(f"[轮询 {poll_count}] API 返回失败，{poll_interval}秒后重试...")
            time.sleep(poll_interval)
            continue
        
        # 检查流程状态
        result_data = result.get("result", {})
        status = result_data.get("status", "")
        
        print(f"[轮询 {poll_count}] 状态: {status}, 已用时: {elapsed_time}秒")
        
        if status == "SUCCESS":
            print(f"\n[流程完成] 执行成功\n")
            return result
        elif status == "FAILED":
            print(f"\n[流程失败] 执行失败\n")
            return result
        else:
            # 继续轮询
            time.sleep(poll_interval)


def cmd_trigger(args):
    """触发流程命令"""
    # 解析 flow_data
    flow_data_dict = None
    if args.flow_data:
        try:
            flow_data_dict = json.loads(args.flow_data)
        except json.JSONDecodeError as e:
            print(f"flow-data 参数不是有效的 JSON: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    # 触发流程
    print("[触发流程] 正在触发流程...")
    result = trigger_flow(
        flow_version=args.flow_version,
        flow_key=args.flow_key,
        flow_data=flow_data_dict
    )
    
    # 检查触发结果
    if not result:
        print("\n流程触发失败", file=sys.stderr)
        sys.exit(1)
    
    # 输出触发结果
    print("\n[触发结果]")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result.get("success"):
        print("\n流程触发失败", file=sys.stderr)
        sys.exit(1)
    
    # 检查是否为异步流程
    result_data = result.get("result", {})
    flow_type = result_data.get("flowType", "")
    flow_instance_id = result_data.get("flowInstanceId", "")
    
    if flow_type == "async" and flow_instance_id:
        # 异步流程，自动轮询结果
        if not args.no_poll:
            final_result = poll_async_result(
                flow_instance_id=flow_instance_id,
                poll_interval=args.poll_interval,
                max_poll_time=args.max_poll_time
            )
            
            if final_result:
                print("[最终结果]")
                print(json.dumps(final_result, indent=2, ensure_ascii=False))
                
                # 根据最终结果设置退出码
                status = final_result.get("result", {}).get("status", "")
                if status == "SUCCESS":
                    sys.exit(0)
                else:
                    sys.exit(1)
            else:
                # 轮询超时或失败
                sys.exit(1)
        else:
            # 用户禁用了自动轮询
            print(f"\n[异步流程] 实例ID: {flow_instance_id}")
            print("提示: 已禁用自动轮询，可使用 get-result 命令手动查询结果")
            sys.exit(0)
    else:
        # 同步流程，直接返回结果
        print("\n[同步流程] 执行完成")
        sys.exit(0)


def cmd_get_result(args):
    """查询异步结果命令"""
    # 查询异步流程结果
    result = get_async_result(
        flow_instance_id=args.flow_instance_id
    )
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 根据结果设置退出码
        if result.get("success"):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)


def main():
    """主函数"""
    # 验证凭证
    try:
        validate_credentials()
    except ValueError as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description="Juggle 流程管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 触发流程（异步流程会自动轮询结果）
  python flow.py trigger --flow-version "v1" --flow-key "order-process"
  
  # 触发流程（带参数）
  python flow.py trigger --flow-version "v1" --flow-key "order-process" \\
    --flow-data '{"orderId": "12345"}'
  
  # 触发流程（自定义轮询配置）
  python flow.py trigger --flow-version "v1" --flow-key "order-process" \\
    --poll-interval 3 --max-poll-time 120
  
  # 触发流程（禁用自动轮询）
  python flow.py trigger --flow-version "v1" --flow-key "order-process" --no-poll
  
  # 手动查询异步流程结果
  python flow.py get-result --flow-instance-id "flow-instance-12345"
  
注意:
  需要在环境变量中配置以下参数：
  - MC_JUGGLE_BASE_URL: Juggle API 基础地址
  - MC_JUGGLE_TOKEN: Juggle Token
  
特性:
  - 当流程为异步流程时，会自动轮询获取最终结果
  - 轮询间隔默认为 2 秒，最大轮询时间默认为 60 秒
  - 可通过 --no-poll 参数禁用自动轮询
        """
    )
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # trigger 子命令
    trigger_parser = subparsers.add_parser('trigger', help='触发流程执行')
    trigger_parser.add_argument(
        "--flow-version",
        required=True,
        help="流程版本"
    )
    trigger_parser.add_argument(
        "--flow-key",
        required=True,
        help="流程 Key"
    )
    trigger_parser.add_argument(
        "--flow-data",
        help="流程入参 JSON 字符串（如：'{\"key\": \"value\"}'）"
    )
    trigger_parser.add_argument(
        "--poll-interval",
        type=int,
        default=2,
        help="异步流程轮询间隔（秒），默认 2 秒"
    )
    trigger_parser.add_argument(
        "--max-poll-time",
        type=int,
        default=60,
        help="异步流程最大轮询时间（秒），默认 60 秒"
    )
    trigger_parser.add_argument(
        "--no-poll",
        action="store_true",
        help="禁用异步流程自动轮询"
    )
    trigger_parser.set_defaults(func=cmd_trigger)
    
    # get-result 子命令
    result_parser = subparsers.add_parser('get-result', help='查询异步流程结果')
    result_parser.add_argument(
        "--flow-instance-id",
        required=True,
        help="异步流程实例 ID"
    )
    result_parser.set_defaults(func=cmd_get_result)
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行对应命令
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

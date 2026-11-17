#!/usr/bin/env python3
"""
订单支付状态轮询脚本
- 每 5 秒查询一次订单状态
- 最长轮询 6 分钟（72次）
- 检测到已支付（status ∈ {1,2,3,4}）则立即结束
- 超时未支付则输出超时结果
"""

import subprocess
import sys
import time
import json
from datetime import datetime

# 配置
POLL_INTERVAL = 5        # 轮询间隔（秒）
MAX_POLL_DURATION = 360   # 最长轮询时长（秒）= 6 分钟
# 已支付状态码（数字字符串类型）
SUCCESS_STATUSES = {"1", "2", "3", "4"}

# 结果输出文件（按订单号区分，避免并发覆盖）
# 将在 main() 中根据 order_id 动态生成: /tmp/poll_result_{order_id}.json


def query_order_status(order_id: str) -> dict | None:
    """调用 km-bot 查询订单状态，参数名为 oid"""
    try:
        result = subprocess.run(
            ["km-bot", "call", "saasktv", "getOrderDetail",
             json.dumps({"oid": order_id})],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout.strip()
        data = json.loads(output)
        return data
    except Exception as e:
        print(f"[轮询] 查询失败: {e}", file=sys.stderr)
        return None


def write_result(order_id: str, status: str, extra: dict = None):
    """将轮询结果写入文件（按订单号区分）"""
    result_file = f"/tmp/poll_result_{order_id}.json"
    result = {
        "poll_status": status,
        "order_id": order_id,
        "timestamp": datetime.now().isoformat(),
        "message": ""
    }
    if extra:
        result.update(extra)
    with open(result_file, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print("用法: python poll_order_status.py <order_id>", file=sys.stderr)
        sys.exit(1)

    order_id = sys.argv[1]
    start_time = time.time()
    poll_count = 0

    print(f"[轮询] 开始监控订单 {order_id}，每 {POLL_INTERVAL}s 查询一次，最长 {MAX_POLL_DURATION}s")

    while time.time() - start_time < MAX_POLL_DURATION:
        poll_count += 1
        elapsed = int(time.time() - start_time)

        # 查询订单状态
        data = query_order_status(order_id)

        if data is None:
            print(f"[轮询] 第 {poll_count} 次查询失败，{POLL_INTERVAL}s 后重试...")
        else:
            # km-bot 包装格式：data.details.result 才是真正的 API 返回值
            details = data.get("details", {})
            api_status = details.get("status", "")
            order_data = details.get("result", {}) if isinstance(details, dict) else {}
            ret = 0 if api_status == "success" else -1
            msg = details.get("message", "")

            print(f"[轮询] 第 {poll_count} 次 | ret={ret} | msg={msg} | elapsed={elapsed}s")

            # 提取订单状态（status 为 String 类型，如 "0", "1", "2" 等）
            current_status = None
            if isinstance(order_data, dict):
                current_status = order_data.get("status")
        
            # 判定是否已支付（状态值为字符串类型的 "1", "2", "3", "4"）
            if current_status in SUCCESS_STATUSES:
                print(f"[轮询] ✅ 订单已支付！status={current_status}")
                write_result(order_id, "paid", {
                    "order_status": current_status,
                    "status_name": order_data.get("status_name", ""),
                    "message": "订单已支付，预约成功",
                    "charge": order_data.get("charge"),
                    "guest_name": order_data.get("guest_name", ""),
                    "used_begin_time": order_data.get("used_begin_time", ""),
                    "used_end_time": order_data.get("used_end_time", ""),
                    "poll_count": poll_count,
                    "elapsed_seconds": elapsed,
                    "order_data": order_data
                })
                sys.exit(0)
            elif current_status == "5":
                print(f"[轮询] ❌ 订单超时未支付，已取消！status={current_status}")
                write_result(order_id, "canceled", {
                    "order_status": current_status,
                    "status_name": order_data.get("status_name", ""),
                    "message": "订单超时未支付，已取消！请重新下单！",
                    "poll_count": poll_count,
                    "elapsed_seconds": elapsed,
                })
                sys.exit(0)
        # 等待下一次轮询
        time.sleep(POLL_INTERVAL)

    # 超时未支付
    total_elapsed = int(time.time() - start_time)
    print(f"[轮询] ⏰ 超时（{total_elapsed}s），订单未支付")
    write_result(order_id, "timeout", {
        "order_status": None,
        "message": "订单已超时未支付，请重新下单",
        "poll_count": poll_count,
        "elapsed_seconds": total_elapsed
    })
    sys.exit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# skills 目录位于: /root/.openclaw/workspace/skills
skills_dir = os.path.dirname(os.path.dirname(current_dir))  # .../skills
workspace_dir = os.path.dirname(skills_dir)  # .../workspace
sys.path.insert(0, workspace_dir)

from skills.smyx_common.scripts import CommonUtil

import argparse
import time
import requests
from urllib.parse import urlparse
from .config import *

from .skill import skill


def is_url(input_str):
    """判断是否为网络地址"""
    try:
        result = urlparse(input_str)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_stream_url(url):
    """判断是否为实时流地址"""
    parsed = urlparse(url)
    return parsed.scheme in SUPPORTED_STREAM_PROTOCOLS


def validate_input(input_path):
    """验证输入合法性"""

    if is_url(input_path):
        if is_stream_url(input_path):
            return "stream"
        # 检查文件扩展名
        ext = os.path.splitext(input_path)[1].lower().lstrip('.')
        if ext in SUPPORTED_VIDEO_FORMATS + SUPPORTED_IMAGE_FORMATS:
            return "network_file"
        raise ValueError(f"不支持的网络文件格式: {ext}")
    else:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        # 检查文件大小
        file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"文件大小超过限制: {file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB")

        # 检查文件格式
        ext = os.path.splitext(input_path)[1].lower().lstrip('.')
        if ext in SUPPORTED_VIDEO_FORMATS:
            return "local_video"
        elif ext in SUPPORTED_IMAGE_FORMATS:
            return "local_image"
        else:
            raise ValueError(f"不支持的文件格式: {ext}")


def analyze_file(input_path, api_key, api_url, mode, threshold):
    """分析文件（本地或网络）"""
    print(f"开始分析文件: {input_path}")

    headers = {
        "Authorization": f"Bearer {api_key}" if api_key else "",
        "Content-Type": "application/json"
    }

    payload = {
        "input": input_path,
        "mode": mode,
        "threshold": threshold,
        "input_type": "url" if is_url(input_path) else "file"
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API请求失败: {str(e)}")


def analyze_stream(stream_url, api_key, api_url, mode, threshold, alert_enabled):
    """分析实时流"""
    print(f"开始监测实时流: {stream_url}")
    print("按Ctrl+C停止监测")

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise Exception(f"无法打开实时流: {stream_url}")

    frame_count = 0
    last_alert_time = {}

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法读取流数据，尝试重新连接...")
                time.sleep(5)
                cap = cv2.VideoCapture(stream_url)
                continue

            frame_count += 1
            if frame_count % STREAM_FRAME_INTERVAL != 0:
                continue

            # 转换帧为JPEG格式
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            # 调用API分析
            headers = {
                "Authorization": f"Bearer {api_key}" if api_key else "",
                "Content-Type": "image/jpeg"
            }

            params = {
                "mode": mode,
                "threshold": threshold
            }

            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    params=params,
                    data=img_bytes,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()

                # 检查是否有高风险事件
                if result.get("has_risk", False):
                    risks = result.get("risks", [])
                    for risk in risks:
                        risk_type = risk.get("type", "unknown")
                        confidence = risk.get("confidence", 0)

                        # 检查冷却时间
                        current_time = time.time()
                        last_time = last_alert_time.get(risk_type, 0)
                        if current_time - last_time < STREAM_ALERT_COOLDOWN:
                            continue

                        # 触发预警
                        alert_level = get_alert_level(confidence)
                        print(f"\n🚨 [{time.strftime('%Y-%m-%d %H:%M:%S')}] 检测到{alert_level}风险:")
                        print(f"   类型: {risk_type}")
                        print(f"   置信度: {confidence:.2f}")
                        print(f"   描述: {risk.get('description', '')}")
                        print(f"   建议: {risk.get('suggestion', '')}\n")

                        if alert_enabled:
                            send_alert(risk, confidence)

                        last_alert_time[risk_type] = current_time

            except Exception as e:
                print(f"分析帧失败: {str(e)}")
                time.sleep(1)
                continue

    except KeyboardInterrupt:
        print("\n停止实时流监测")
    finally:
        cap.release()


def get_alert_level(confidence):
    """根据置信度获取预警等级"""
    if confidence >= 0.9:
        return "🔴 高风险"
    elif confidence >= 0.7:
        return "🟡 中风险"
    else:
        return "🔵 低风险"


def send_alert(risk, confidence):
    """发送预警通知"""
    alert_time = time.strftime('%Y-%m-%d %H:%M:%S')
    risk_type = risk.get("type", "unknown")
    description = risk.get("description", "")
    suggestion = risk.get("suggestion", "")

    message = f"""
🚨 高风险事件预警
⏰ 时间: {alert_time}
⚠️ 类型: {risk_type}
📊 置信度: {confidence:.2f}
📝 描述: {description}
💡 建议: {suggestion}
    """

    # 飞书通知
    if ALERT_FEISHU_WEBHOOK:
        try:
            requests.post(
                ALERT_FEISHU_WEBHOOK,
                json={"msg_type": "text", "content": {"text": message}}
            )
        except Exception as e:
            print(f"飞书通知发送失败: {e}")

    # Webhook通知
    if ALERT_WEBHOOK_URL:
        try:
            requests.post(
                ALERT_WEBHOOK_URL,
                json={
                    "timestamp": alert_time,
                    "risk_type": risk_type,
                    "confidence": confidence,
                    "description": description,
                    "suggestion": suggestion
                }
            )
        except Exception as e:
            print(f"Webhook通知发送失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='高风险行为识别分析工具')
    parser.add_argument('--input', help='本地文件路径')
    parser.add_argument('--url', help='网络URL或实时流地址')
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument('--list', action='store_true', help='列出历史风险分析报告')
    parser.add_argument('--page-num', type=int, default=1, help='分页页码')
    parser.add_argument('--page-size', type=int, default=30, help='分页大小')
    parser.add_argument('--mode', default=DEFAULT_ANALYSIS_MODE,
                        choices=['all', 'fall', 'health', 'behavior'],
                        help='分析模式')
    parser.add_argument('--threshold', type=float, default=DEFAULT_ALERT_THRESHOLD,
                        help='预警阈值 (0.1-1.0)')
    parser.add_argument('--output', help='结果输出文件路径')
    parser.add_argument('--alert', type=bool, default=DEFAULT_AUTO_ALERT,
                        help='是否开启自动预警')

    args = parser.parse_args()

    try:

        if args.open_id:
            # 设置 Python 进程内的环境变量
            ConstantEnumBase.CURRENT__OPEN_ID = args.open_id

        # 处理 list 模式
        if args.list:
            # 列出指定 open-id 的历史报告
            if not ConstantEnumBase.CURRENT__OPEN_ID:
                print("❌ 错误：使用 --list 参数时必须提供 --open-id")
                exit(1)
            output_content = skill.get_output_analysis_list(
                pageNum=args.page_num,
                pageSize=args.page_size
            )
            print(output_content)
        else:
            if not args.input and not args.url:
                parser.error("必须提供--input或--url参数")
                exit(1)
            input_path = args.input or args.url
            output_content = skill.get_output_analysis(input_path)
            print(output_content)

    except Exception as e:
        print(f"❌ 风险分析失败: {str(e)}")
        CommonUtil.trace_exception_stack(e)
        exit(1)


if __name__ == "__main__":
    main()

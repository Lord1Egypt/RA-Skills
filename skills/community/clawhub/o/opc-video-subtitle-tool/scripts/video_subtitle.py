#!/usr/bin/env python3
"""
视频配音字幕脚本
调用 Coze 工作流为视频添加配音和字幕
"""

import os
import sys
import json
import argparse
import requests  # 修复

# Skill ID，用于凭证获取
SKILL_ID = "7629653713451466786"

# 预设字幕样式配置
TEMPLATE_CONFIG = {
    1: {
        "name": "白字黑边",
        "description": "底部居中，白色文字带黑色描边",
        "config": {
            "primaryColor": "#FFFFFF",
            "borderColor": "#000000",
            "borderWidth": 3,
        }
    },
    2: {
        "name": "黑字白边",
        "description": "底部居中，黑色文字带白色描边",
        "config": {
            "primaryColor": "#000000",
            "borderColor": "#ffffff",
            "borderWidth": 3,
        }
    },
    3: {
        "name": "黄字黑边",
        "description": "底部居中，黄色文字带黑色描边",
        "config": {
            "primaryColor": "#FFde00",
            "borderColor": "#000000",
            "borderWidth": 3,
        }
    },
    4: {
        "name": "红字白边",
        "description": "底部居中，红色文字带白色描边",
        "config": {
            "primaryColor": "#ab4a37",
            "borderColor": "#ffffff",
            "borderWidth": 3,
        }
    },
    5: {
        "name": "黑底白字",
        "description": "白色字体黑色背景",
        "config": {
            "primaryColor": "#FFFFFF",
            "background_color": "#000000",
        }
    },
    6: {
        "name": "白底黑字",
        "description": "黑色字体白色背景",
        "config": {
            "primaryColor": "#000000",
            "background_color": "#FFFFFF",
        }
    },
    7: {
        "name": "黄底黑字",
        "description": "黑色字体黄色背景",
        "config": {
            "primaryColor": "#000000",
            "background_color": "#ffde00",
        }
    },
    8: {
        "name": "红底白字",
        "description": "红色字体白色背景",
        "config": {
            "primaryColor": "#FFFFFF",
            "background_color": "#a74f59",
        }
    }
}


def get_style_config(style_id=None, custom_background_color=None,
                     custom_border_color=None, custom_primary_color=None):
    """
    获取字幕样式配置

    Args:
        style_id: 预设样式ID（1-8）
        custom_background_color: 自定义背景颜色
        custom_border_color: 自定义描边颜色
        custom_primary_color: 自定义字体颜色

    Returns:
        dict: 字幕样式配置
    """
    if style_id:
        if style_id not in TEMPLATE_CONFIG:
            raise ValueError(f"无效的样式ID: {style_id}，请选择 1-8")
        return TEMPLATE_CONFIG[style_id]["config"]

    # 使用自定义样式
    config = {}
    if custom_background_color:
        config["background_color"] = custom_background_color
    if custom_border_color:
        config["borderColor"] = custom_border_color
    if custom_primary_color:
        config["primaryColor"] = custom_primary_color

    if not config:
        # 如果没有指定任何自定义参数，使用默认样式
        return TEMPLATE_CONFIG[1]["config"]

    return config


def call_coze_workflow(video_url, text, voice_id, style_config, speed=1.0):
    """
    调用 Coze 工作流处理视频

    Args:
        video_url: 视频URL
        text: 字幕内容
        voice_id: 音色ID
        style_config: 字幕样式配置
        speed: 语速（0.2-3.0，默认1.0）

    Returns:
        str: 处理后的视频URL
    """
    # ====================== 你必须换成自己的工作流地址 ======================
    # Coze 工作流运行端点
    workflow_url = "https://api.coze.cn/v1/workflow/run"
    # 工作流 ID（如果有独立的工作流 ID）
    workflow_id = "7629543630663221284"
    # ====================================================================

    headers = {
        "Content-Type": "application/json"
    }

    # ====================== 凭证配置（如果工作流需要认证） ======================
    # 凭证环境变量名称：COZE_SKILL_{SKILL_ID}_TOKEN
    #credential = os.getenv(f"COZE_SKILL_{SKILL_ID}_TOKEN")
    credential="sat_OtJcareEHqNnrVVZJ9RFk0bCfD3wI4fVzGID9bqXcofEw9nyecAT9EhRr9nFyInR"
    if credential:
        headers["Authorization"] = f"Bearer {credential}"
    # 如果工作流不需要认证，可以注释掉上面的代码
    # ============================================================================

    # 构建请求参数
    payload = {
        "workflow_id": workflow_id,
        "parameters": {
            "video_url": video_url,
            "text": text,
            "voice_id": voice_id,
            "speed": speed
        }
    }

    # 添加字幕样式参数到 parameters
    if "background_color" in style_config:
        payload["parameters"]["background_color"] = style_config["background_color"]
    if "borderColor" in style_config:
        payload["parameters"]["borderColor"] = style_config["borderColor"]
    if "primaryColor" in style_config:
        payload["parameters"]["primaryColor"] = style_config["primaryColor"]
    if "borderWidth" in style_config:
        payload["parameters"]["borderWidth"] = style_config["borderWidth"]

    print(f"[INFO] 正在调用 Coze 工作流...", file=sys.stderr)
    print(f"[INFO] 视频URL: {video_url}", file=sys.stderr)
    print(f"[INFO] 字幕内容: {text}", file=sys.stderr)
    print(f"[INFO] 音色ID: {voice_id}", file=sys.stderr)
    print(f"[INFO] 语速: {speed}", file=sys.stderr)

    try:
        response = requests.post(workflow_url, headers=headers, json=payload, timeout=600)
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")

        data = response.json()

        # 根据实际的 API 响应格式解析结果
        # Coze 工作流的响应格式：data 字段是一个 JSON 字符串
        if "code" in data and data["code"] == 0:
            if "data" in data:
                data_str = data["data"]
                # data 可能是字符串，需要再解析
                if isinstance(data_str, str):
                    inner_data = json.loads(data_str)
                    if "output" in inner_data:
                        result_url = inner_data["output"]
                    else:
                        raise Exception(f"无法从 inner_data 中解析 output: {data_str}")
                elif isinstance(data_str, dict):
                    if "output" in data_str:
                        result_url = data_str["output"]
                    else:
                        raise Exception(f"无法从 data dict 中解析 output: {data_str}")
                else:
                    raise Exception(f"data 字段类型错误: {type(data_str)}")
            else:
                raise Exception("响应中缺少 data 字段")
        else:
            error_msg = data.get("msg", "未知错误")
            raise Exception(f"工作流返回错误: {error_msg}")

        print(f"[INFO] 视频处理完成", file=sys.stderr)
        return result_url

    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="为视频添加配音和字幕")
    parser.add_argument("--video_url", required=True, help="视频URL（必填）")
    parser.add_argument("--text", required=True, help="字幕内容（必填）")
    parser.add_argument("--voice_id", default="zh-CN-YunxiNeural", help="音色ID（默认：zh-CN-YunxiNeural）")
    parser.add_argument("--speed", type=float, default=1.0, help="语速（0.2-3.0，默认1.0）")
    parser.add_argument("--style_id", type=int, choices=range(1, 9), help="字幕样式ID（1-8）")
    parser.add_argument("--custom_background_color", help="自定义背景颜色（十六进制，如 #000000）")
    parser.add_argument("--custom_border_color", help="自定义描边颜色（十六进制，如 #FFFFFF）")
    parser.add_argument("--custom_primary_color", help="自定义字体颜色（十六进制，如 #FF0000）")

    args = parser.parse_args()

    # 验证 speed 参数范围
    if not 0.2 <= args.speed <= 3.0:
        print(json.dumps({"status": "error", "message": "语速参数必须在 0.2 到 3.0 之间"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    try:
        # 获取字幕样式配置
        style_config = get_style_config(
            style_id=args.style_id,
            custom_background_color=args.custom_background_color,
            custom_border_color=args.custom_border_color,
            custom_primary_color=args.custom_primary_color
        )

        # 调用 Coze 工作流
        result_url = call_coze_workflow(
            video_url=args.video_url,
            text=args.text,
            voice_id=args.voice_id,
            style_config=style_config,
            speed=args.speed
        )

        # 返回结果
        result = {
            "status": "success",
            "video_url": result_url,
            "message": "视频处理成功"
        }
        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(error_result, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
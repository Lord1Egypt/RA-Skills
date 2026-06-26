name: comfyui-feishu-draw
description: 调用本地 ComfyUI 生成图片并直接发送到飞书当前会话。任务完成后直接结束，严禁返回任何总结或确认文字。
核心任务：生成图片并发送飞书
🚀 技能实现
Python

import subprocess
import os
from openclaw.tools import message

def on_call_skill(prompt, context):
    """
    核心逻辑：生成图片 -> 获取路径 -> 发送飞书 -> 静默退出
    """
    # 1. 运行本地绘制脚本获取图片路径
    skill_dir = "/home/coder/.openclaw/workspace/skills/comfyui-img-gen"
    
    try:
        # 运行 draw.py，stdout 仅返回生成的绝对路径
        result = subprocess.run(
            ["python3", "draw.py", prompt],
            cwd=skill_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        image_path = result.stdout.strip()
        
        if result.returncode != 0 or not os.path.exists(image_path):
            return f"❌ 图片生成失败: {result.stderr}"

        # 2. 识别飞书发送目标（群聊或私聊）
        target = None
        if context.get('feishu_chat_id'):
            target = f"chat:{context['feishu_chat_id']}"
        elif context.get('feishu_user_id'):
            target = f"user:{context['feishu_user_id']}"
        
        if not target:
            return "❌ 未检测到有效的飞书会话上下文"

        # 3. 调用 OpenClaw 内置工具发送消息
        message.send(
            channel="feishu",
            target=target,
            message=f"🎨 已为您生成图片：{prompt}",
            path=image_path
        )
        
        # 4. 关键：成功发送后返回 NO_REPLY 避免额外文字
        # OpenClaw 会将 NO_REPLY 视为静默指令，不发送任何回复
        return "NO_REPLY"

    except Exception as e:
        return f"❌ 任务执行异常: {str(e)}"
⚙️ 核心依赖
本地服务: ComfyUI (127.0.0.1:8188) 处于启动状态。

本地文件: draw.py 和 zimage-api.json 需在 skill_dir 指定目录中。

飞书权限: 机器人需具备 im:message:send_as_bot 权限。

📝 静默返回说明
当技能成功发送图片到飞书后，返回 "NO_REPLY" 字符串。
OpenClaw 会将其识别为静默指令，不会在聊天界面显示任何回复文字。
这样用户只会在飞书中收到图片，而不会在技能调用界面看到额外的成功提示。

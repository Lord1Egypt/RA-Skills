#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from datetime import datetime
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

# 配置信息
VOLC_ACCESS_KEY = os.getenv("VOLC_ACCESS_KEY", "")
VOLC_SECRET_KEY = os.getenv("VOLC_SECRET_KEY", "")
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace/MeetingClaw")
AUDIO_RETENTION_DAYS = 30

# 火山引擎录音文件识别极速版配置
SERVICE_INFO = ServiceInfo(
    host="openspeech.bytedance.com",
    header={"Accept": "application/json"},
    credentials=Credentials(VOLC_ACCESS_KEY, VOLC_SECRET_KEY, "speech", "cn-north-1"),
    connection_timeout=10,
    socket_timeout=300,
)
API_INFO = {
    "speech_transcribe_async": ApiInfo(
        method="POST",
        path="/api/v1/async_speech/transcribe",
        query={},
        form={},
        header={},
    )
}

def init_storage():
    """初始化存储目录"""
    today = datetime.now().strftime("%Y%m%d")
    save_dir = os.path.join(WORKSPACE_DIR, today)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def save_audio_file(audio_path, save_dir):
    """保存原始音频文件"""
    import shutil
    filename = os.path.basename(audio_path)
    save_path = os.path.join(save_dir, filename)
    shutil.copy2(audio_path, save_path)
    return save_path

def transcribe_audio_fast(audio_path):
    """极速版识别：直接提交二进制流"""
    service = Service(SERVICE_INFO, API_INFO)
    
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    params = {
        "appid": VOLC_ACCESS_KEY,
        "language": "zh-CN",
        "use_itn": True,
        "use_punc": True,
        "use_ddc": True,
    }
    
    files = {"audio": (os.path.basename(audio_path), audio_data)}
    response = service.post("speech_transcribe_async", params, files=files)
    
    if response.get("code") != 0:
        raise Exception(f"识别失败: {response.get('message')}")
    
    task_id = response["data"]["task_id"]
    # 轮询结果
    while True:
        result = service.get("speech_transcribe_async/query", {"task_id": task_id})
        if result.get("code") != 0:
            raise Exception(f"查询结果失败: {result.get('message')}")
        status = result["data"]["status"]
        if status == "success":
            return result["data"]["result"]
        elif status == "failed":
            raise Exception(f"识别任务失败: {result['data'].get('error_msg')}")
        time.sleep(5)

def generate_minutes(transcript_text):
    """调用大模型生成结构化会议纪要"""
    prompt = f"""
你是专业的会议纪要助理，请将下面的会议转写内容整理成结构化的会议纪要，要求如下：
1. 会议主题：智能推断本次会议的核心主题，不超过20字
2. 基本信息：自动填写会议时间（从音频元数据获取，若无则留空）、参会人员（从内容中识别）
3. 会议综述：高度抽象提炼会议核心内容，200字以内
4. 会议智能总结：深度分析提炼关键观点、结论、核心问题，重要内容引用原文原话，信息密度高
5. 待办事项：自动提取所有会后需要执行的任务，明确指派对应的发言人
6. 其他重要事项：补充遗漏的关键信息

会议转写内容：
{transcript_text}

请直接输出结构化的会议纪要，使用Markdown格式，不要添加额外说明。
"""
    # 调用OpenClaw大模型
    # 这里使用OpenClaw内置的模型调用接口
    import openclaw
    response = openclaw.completions.create(
        model="volcengine/ark-code-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def save_minutes(minutes_content, save_dir, audio_filename):
    """保存会议纪要"""
    base_name = os.path.splitext(audio_filename)[0]
    minutes_filename = f"{base_name}_会议纪要.md"
    minutes_path = os.path.join(save_dir, minutes_filename)
    with open(minutes_path, "w", encoding="utf-8") as f:
        f.write(minutes_content)
    return minutes_path

def clean_old_files():
    """清理超过保留期限的音频文件"""
    if AUDIO_RETENTION_DAYS <= 0:
        return
    now = time.time()
    cutoff = now - (AUDIO_RETENTION_DAYS * 86400)
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff:
                os.remove(file_path)

def main(audio_path, mode="fast"):
    if not VOLC_ACCESS_KEY or not VOLC_SECRET_KEY:
        print("错误：请先配置VOLC_ACCESS_KEY和VOLC_SECRET_KEY环境变量")
        sys.exit(1)
    
    if not os.path.exists(audio_path):
        print(f"错误：音频文件不存在 {audio_path}")
        sys.exit(1)
    
    # 初始化存储
    save_dir = init_storage()
    
    # 保存原始音频
    saved_audio_path = save_audio_file(audio_path, save_dir)
    print(f"原始音频已保存到: {saved_audio_path}")
    
    # 识别音频
    print("正在识别音频...")
    if mode == "fast":
        transcript = transcribe_audio_fast(audio_path)
    else:
        # 标准版实现待补充（需要集成TOS上传）
        raise Exception("标准版模式暂未实现")
    
    # 生成纪要
    print("正在生成会议纪要...")
    minutes = generate_minutes(transcript)
    
    # 保存纪要
    minutes_path = save_minutes(minutes, save_dir, os.path.basename(audio_path))
    print(f"会议纪要已生成: {minutes_path}")
    
    # 清理旧文件
    clean_old_files()
    
    print("\n===== 会议纪要 =====\n")
    print(minutes)
    return minutes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <音频文件路径> [模式: fast/standard]")
        sys.exit(1)
    audio_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "fast"
    main(audio_path, mode)

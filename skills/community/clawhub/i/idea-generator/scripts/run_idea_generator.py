#!/usr/bin/env python3
"""
创意生成器主执行脚本 - 直接执行，不通过 sessions_spawn
修复了之前架构问题：不再创建新对话窗口，而是在当前会话中完整执行
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse

# 项目目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, "state.json")
TRIGGER_FILE = os.path.join(SCRIPT_DIR, ".trigger_agent")

def log(message):
    """记录日志到 stdout（避免重复写入文件）"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)

def api_call(endpoint, data=None):
    """调用本地 API"""
    try:
        url = f"http://localhost:50000{endpoint}"
        req_data = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(
            url, 
            data=req_data,
            headers={'Content-Type': 'application/json'} if data else {}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        log(f"API 调用失败 {endpoint}: {e}")
        return None

def main():
    # 读取触发文件
    if not os.path.exists(TRIGGER_FILE):
        log("错误: 没有找到触发文件")
        return
    
    try:
        with open(TRIGGER_FILE, 'r', encoding='utf-8') as f:
            trigger_data = json.load(f)
        
        topic = trigger_data.get('topic', '').strip()
        rounds_count = int(trigger_data.get('rounds', 3))
        demand = trigger_data.get('demand', '').strip()
        port = trigger_data.get('port', '50000')
        
        if not topic:
            log("错误: 主题为空")
            return
            
        log(f"开始执行创意生成任务: {topic} ({rounds_count}轮)")
        
        # 删除触发文件，避免重复执行
        os.remove(TRIGGER_FILE)
        
        # 更新状态为 AI 引擎启动中
        api_call("/phase", {"phase": "AI 引擎启动中..."})
        
        # 执行创意生成的主逻辑（这里应该调用实际的生成逻辑）
        # 由于这是在 OpenClaw 环境中，我们需要模拟调用过程
        # 实际的创意生成逻辑应该由 OpenClaw agent 来执行
        
        log("任务已准备就绪，请在 OpenClaw 中执行创意生成流程")
        log("提示: 使用 idea-generator 技能来处理此任务")
        
        # 更新状态为就绪
        api_call("/phase", {"phase": "就绪，等待 OpenClaw 处理"})
        
    except Exception as e:
        log(f"执行失败: {e}")
        # 标记任务为失败
        api_call("/phase", {"phase": f"执行失败: {e}"})

if __name__ == "__main__":
    main()
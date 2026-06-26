"""
主入口模块
支持命令行运行生成每日报告
"""

import argparse
import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import load_config, save_config, CONFIG_DIR, UserConfig
from src.garmin_client import GarminClient
from src.report_generator import ReportGenerator
from src.setup_handler import SetupHandler

import logging

# 配置日志
LOG_DIR = Path.home() / ".openclaw" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "health-assistant.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("HealthAssistant")

HISTORY_FILE = CONFIG_DIR / "history.json"

def load_history():
    """加载历史记录"""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('records', [])
    except:
        return []

def save_history(records):
    """保存历史记录"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "1.0",
                "records": records[-30:],  # 只保留最近30天
                "metadata": {"last_updated": datetime.now().isoformat()}
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"历史记录已保存，共 {len(records)} 条")
    except Exception as e:
        logger.error(f"保存历史记录失败: {e}")

def run_daily_report():
    """执行每日报告生成流程"""
    logger.info("🚀 开始生成每日健康报告...")
    
    # 1. 加载配置
    config = load_config()
    if not config or not config.device_config:
        error_msg = "❌ Configuration not found. Please complete the interactive setup first."
        logger.warning(error_msg)
        return error_msg

    # 2. 获取昨日数据
    # 活动日期通常是昨天，睡眠结束日期是今天早上
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    
    client = GarminClient(config.device_config)
    daily_data = client.get_daily_data(activity_date=yesterday, sleep_end_date=today)
    
    if not daily_data:
        error_msg = "❌ Failed to retrieve health data. Please log in to Garmin."
        logger.error(error_msg)
        return error_msg

    # 3. 加载历史
    history = load_history()

    # 4. 调用 AI 生成建议
    generator = ReportGenerator(config)
    prompt = generator.generate_prompt(daily_data, history)
    
    logger.info("🤖 Calling NotebookLM for AI insights...")
    ai_suggestion = generator.call_notebooklm(prompt)
    
    if not ai_suggestion:
        logger.warning("AI suggestion generation failed. Using fallback message.")
        ai_suggestion = "Sorry, failed to generate AI insights today. Please refer to the raw data."

    # 5. 组装最终报告
    final_report = generator.format_final_report(daily_data, ai_suggestion)
    
    # 6. 保存历史
    history.append(daily_data)
    save_history(history)

    # 7. 这里应该调用 OpenClaw 的消息发送接口推送到 IM
    # 如果是被定时任务触发，只需记录日志并返回即可
    # 如果是人工触发，为了体验更好保留终端输出
    if not isinstance(logging.getLogger().handlers[0], logging.FileHandler):
        print(final_report)
    
    logger.info(f"\n{final_report}")
    return final_report

def handle_message(message_text: str) -> str:
    """
    处理来自 IM 平台的消息内容
    
    Args:
        message_text: 用户发送的文本内容
        
    Returns:
        回复文本
    """
    config = load_config()
    
    # 场景1：未配置完成，进入设置流程
    if not config or not config.is_configured:
        if not config:
            config = UserConfig()
            save_config(config)
        
        handler = SetupHandler(config)
        return handler.handle_message(message_text)
    
    # 场景2：已配置，处理特定指令
    msg = message_text.strip().lower()
    if msg in ["report", "生成报告", "健康报告"]:
        return run_daily_report()
    elif msg in ["reset", "重置配置"]:
        from src.config import reset_config
        reset_config()
        return "Configuration has been reset. Send any message to start the setup again."
    
    return "Hello! I am your health advisor. You can say 'report' to get insights or 'reset' to clear settings."

def main():
    parser = argparse.ArgumentParser(description="🦞健康健康 - 个人健康顾问")
    parser.add_argument('--daily-report', action='store_true', help='生成每日健康报告')
    
    args = parser.parse_args()
    
    if args.daily_report:
        run_daily_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

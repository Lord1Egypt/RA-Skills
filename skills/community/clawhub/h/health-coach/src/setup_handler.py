"""
对话式配置引导处理器
负责管理首次使用的交互式对话逻辑
"""

import re
from typing import Tuple, Optional
from src.config import UserConfig, save_config
from src.env_checker import EnvChecker

class SetupHandler:
    """处理首次使用的配置对话状态机"""

    def __init__(self, config: UserConfig):
        self.config = config

    def handle_message(self, message: str) -> str:
        """
        处理用户消息并返回回复内容
        
        Args:
            message: 用户输入的文本
            
        Returns:
            回复给用户的文本
        """
        step = self.config.setup_step
        
        if step == "START":
            return self._handle_start()
        elif step == "CHECK_ENV":
            return self._handle_check_env(message)
        elif step == "INSTALL_WAIT":
            return self._handle_install_retry(message)
        elif step == "CONCERNS":
            return self._handle_concerns(message)
        elif step == "DEVICE":
            return self._handle_device(message)
        elif step == "AUTH":
            return self._handle_auth(message)
        elif step == "TIME":
            return self._handle_time(message)
        else:
            return "Configuration complete! You can send 'report' to get today's health insights."

    def _handle_start(self) -> str:
        """初始欢迎语并检查环境"""
        self.config.setup_step = "CHECK_ENV"
        save_config(self.config)
        
        welcome_msg = (
            "Hello! I am your personal health advisor, 🦞 **Health Assistant**.\n\n"
            "Before I start providing recommendations, I need to prepare the AI engine (NotebookLM).\n"
            "Checking environment... 🔍"
        )
        
        # 立即检查
        if EnvChecker.is_notebooklm_installed() and EnvChecker.is_playwright_ready():
            if EnvChecker.is_logged_in():
                return self._handle_check_env("already_ok")
            else:
                return welcome_msg + "\n\n✅ Dependencies installed, but you are **not logged in**. Please run `notebooklm login` in your terminal to authenticate with Google, then reply 'logged in'."
        
        return welcome_msg + "\n\n⚠️ Missing required components. Shall I **install them automatically** for you? (Reply 'yes' to start, or 'no' to install manually)"

    def _handle_check_env(self, message: str) -> str:
        """处理环境检查及反馈"""
        msg = message.strip().lower()
        
        if msg in ["already_ok", "logged in", "done"]:
            if EnvChecker.is_logged_in():
                self.config.setup_step = "CONCERNS"
                save_config(self.config)
                return (
                    "🎉 AI Engine is ready!\n\n"
                    "Now, I'd like to know what health aspects you care about the most (you can select multiple by typing the letters, e.g., 'AC'):\n"
                    "A. Improve Sleep\n"
                    "B. Weight Loss / Management\n"
                    "C. Stress Relief\n"
                    "D. Boost Energy\n"
                    "E. Specific Health Condition (e.g., high blood pressure, high uric acid, joint pain)\n"
                    "F. Other (describe directly)"
                )
            else:
                return "❌ It seems the login was not successful. Please ensure you ran `notebooklm login` and completed the process in the browser. Reply 'logged in' once finished."

        if msg in ["yes", "y", "sure", "ok", "是", "确认"]:
            self.config.setup_step = "INSTALL_WAIT"
            save_config(self.config)
            
            success, error = EnvChecker.run_install()
            if success:
                return (
                    "✅ **Automatic installation completed!**\n\n"
                    "Final step (Important): Due to security restrictions, you need to manually log in to Google.\n"
                    "👉 Open your terminal and run: `notebooklm login` \n"
                    "Once done, please reply **'logged in'**."
                )
            else:
                return f"❌ Auto-install failed: {error}\n\nI suggest manually running `bash install.sh` in the terminal to fix this."
        
        return "Noted. Please manually install `notebooklm-py` and run `notebooklm login`, then reply to me."

    def _handle_install_retry(self, message: str) -> str:
        """从安装等待状态恢复"""
        if "logged in" in message.lower() or "done" in message.lower():
            return self._handle_check_env("logged in")
        return "Please complete the `notebooklm login` first. Reply 'logged in' when finished."

    def _handle_concerns(self, message: str) -> str:
        """处理用户对健康关切的回应"""
        mapping = {
            'A': 'Improve Sleep',
            'B': 'Weight Management',
            'C': 'Stress Relief',
            'D': 'Boost Energy',
            'E': 'Specific Condition'
        }
        
        selected = []
        msg_upper = message.upper()
        for key, value in mapping.items():
            if key in msg_upper:
                selected.append(value)
        
        # 如果没有字母匹配，且长度大于1，尝试当作自定义描述
        if not selected:
            if 'F' in msg_upper or len(message) > 2:
                selected.append(message.replace('F', '').replace('f', '').strip())
        
        if not selected:
            return "Sorry, I didn't quite get that. Please select an option (A-F) or explicitly tell me your primary wellness goal."

        # 更新配置
        self.config.health_concerns = list(set(self.config.health_concerns + selected))
        self.config.setup_step = "DEVICE"
        save_config(self.config)
        
        concerns_text = ", ".join(selected) if selected else "your description"
        return (
            f"Got it! I will focus on: **{concerns_text}**.\n\n"
            "Next, we need to connect your wearable device. I currently support:\n"
            "1. **Garmin**\n"
            "2. Apple Watch (Coming Soon)\n"
            "3. Fitbit (Coming Soon)\n\n"
            "Please enter a number or name to select your device type."
        )

    def _handle_device(self, message: str) -> str:
        """处理设备选择"""
        if "1" in message or "garmin" in message.lower():
            self.config.device_config = {"type": "garmin", "domain": "garmin.com"}
            self.config.setup_step = "AUTH"
            save_config(self.config)
            return (
                "Garmin data sync requires pre-authorization using `garth`.\n\n"
                "🛡️ To keep your credentials secure, please authenticate through the official method:\n"
                "**Run `garth login` in your system terminal.** This will safely store the session tokens in your `~/.garth` directory.\n\n"
                "Once completed (or if you are already logged in), please provide your **Garmin Account (Email)** as a reference identifier.\n"
                "(⚠️ This email is stored locally in plain text. Please protect your system and NEVER reveal passwords to this app!)"
            )
        else:
            return "Currently, only Garmin is supported (Please reply '1'). Stay tuned for future updates to support other devices."

    def _handle_auth(self, message: str) -> str:
        """处理授权信息（简化流程）"""
        if "@" in message:
            self.config.device_config["email"] = message.strip()
            self.config.setup_step = "TIME"
            save_config(self.config)
            return (
                f"Account **{message.strip()}** recorded.\n\n"
                "Finally, when would you like to receive your daily report? Default is **08:00**.\n"
                "If you want to change it, simply reply with the time (e.g., '08:30'), otherwise reply 'ok' or 'confirm'."
            )
        return "Please enter a valid email address."

    def _handle_time(self, message: str) -> str:
        """确认推送时间并完成配置"""
        if ":" in message or re.search(r'\d+', message):
            self.config.preferences["report_time"] = message.strip()
        
        self.config.setup_step = "COMPLETED"
        self.config.is_configured = True
        save_config(self.config)
        
        return (
            "✅ **Setup Complete!**\n\n"
            "Starting tomorrow, I will deliver your personalized health report on time.\n"
            "You can also say **'report'** at any time to instantly trigger the analysis based on today's latest data."
        )

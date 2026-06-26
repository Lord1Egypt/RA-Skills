"""
Nex Voice - Configuration Management
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Data and storage directories
DATA_DIR = Path(os.getenv("NEX_VOICE_DATA_DIR", Path.home() / ".nex-voice")).expanduser()
DB_PATH = DATA_DIR / "nex_voice.db"
AUDIO_DIR = DATA_DIR / "recordings"
EXPORT_DIR = DATA_DIR / "exports"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.json"

# Whisper configuration
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "nl")  # nl for Dutch, en for English
WHISPER_CMD = os.getenv("WHISPER_CMD", "whisper")

# Supported audio formats
SUPPORTED_FORMATS = {"ogg", "mp3", "wav", "m4a", "opus", "webm"}

# Action item keywords (Dutch + English)
ACTION_KEYWORDS = {
    # Tasks
    "moet": "task",
    "moet nog": "task",
    "must": "task",
    "need to": "task",
    "do": "task",
    "handle": "task",
    "prepare": "task",
    "review": "task",

    # Reminders
    "vergeet niet": "reminder",
    "don't forget": "reminder",
    "remember": "reminder",
    "herinnering": "reminder",

    # Calls
    "bel": "call",
    "call": "call",
    "belt": "call",
    "calling": "call",
    "phone": "call",
    "contact": "call",

    # Email/Send
    "mail": "email",
    "email": "email",
    "stuur": "send",
    "send": "send",
    "forward": "send",

    # Meetings
    "afspraak": "meeting",
    "meeting": "meeting",
    "vergadering": "meeting",
    "overleg": "meeting",
    "presentatie": "meeting",
    "demo": "meeting",

    # Decisions
    "besloten": "decision",
    "decided": "decision",
    "beslist": "decision",
    "agree": "decision",
    "decision": "decision",

    # Deadlines
    "deadline": "deadline",
    "voor": "deadline_date",
    "by": "deadline_date",
    "until": "deadline_date",
}

# LLM settings (optional)
AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_BASE = os.getenv("AI_API_BASE", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o")

# Audio limits
MAX_AUDIO_DURATION = 600  # 10 minutes in seconds
TELEGRAM_FILE_SIZE_LIMIT = 20 * 1024 * 1024  # 20 MB


class Config:
    """Configuration management for nex-voice"""

    def __init__(self):
        self.config_data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.config_data = {}

    def save(self) -> None:
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config_data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config_data[key] = value
        self.save()

    def get_whisper_model(self) -> str:
        """Get Whisper model"""
        return self.get("whisper_model", WHISPER_MODEL)

    def set_whisper_model(self, model: str) -> None:
        """Set Whisper model"""
        if model not in ["tiny", "base", "small", "medium", "large"]:
            raise ValueError(f"Invalid Whisper model: {model}")
        self.set("whisper_model", model)

    def get_whisper_language(self) -> str:
        """Get Whisper language"""
        return self.get("whisper_language", WHISPER_LANGUAGE)

    def set_whisper_language(self, language: str) -> None:
        """Set Whisper language"""
        if language not in ["nl", "en"]:
            raise ValueError(f"Invalid language: {language}")
        self.set("whisper_language", language)

    def get_api_key(self) -> Optional[str]:
        """Get API key"""
        return self.get("api_key") or AI_API_KEY

    def set_api_key(self, key: str) -> None:
        """Set API key"""
        self.set("api_key", key)

    def get_api_base(self) -> str:
        """Get API base URL"""
        return self.get("api_base", AI_API_BASE)

    def set_api_base(self, base: str) -> None:
        """Set API base URL"""
        self.set("api_base", base)

    def get_api_model(self) -> str:
        """Get API model"""
        return self.get("api_model", AI_MODEL)

    def set_api_model(self, model: str) -> None:
        """Set API model"""
        self.set("api_model", model)

    def is_llm_configured(self) -> bool:
        """Check if LLM is configured"""
        return bool(self.get_api_key())


# Global config instance
config = Config()

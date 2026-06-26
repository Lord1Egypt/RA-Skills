import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_URL = os.getenv("FASTGPT_API_URL", "").strip()
    REQUEST_TIMEOUT = int(os.getenv("FASTGPT_TIMEOUT", "60").strip() or "60")

    # Allow a shared key or per-agent keys.
    FASTGPT_API_KEY = os.getenv("FASTGPT_API_KEY", "").strip()
    AGENT_A_KEY = os.getenv("AGENT_A_KEY", "").strip()
    AGENT_B_KEY = os.getenv("AGENT_B_KEY", "").strip()
    AGENT_C_KEY = os.getenv("AGENT_C_KEY", "").strip()

    AGENT_A_ID = os.getenv("AGENT_A_ID", "").strip()
    AGENT_B_ID = os.getenv("AGENT_B_ID", "").strip()
    AGENT_C_ID = os.getenv("AGENT_C_ID", "").strip()

    DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

    @classmethod
    def key_for_agent(cls, agent_name: str) -> str:
        if agent_name == "A":
            return cls.AGENT_A_KEY or cls.FASTGPT_API_KEY
        if agent_name == "B":
            return cls.AGENT_B_KEY or cls.FASTGPT_API_KEY
        if agent_name == "C":
            return cls.AGENT_C_KEY or cls.FASTGPT_API_KEY
        return cls.FASTGPT_API_KEY

    @classmethod
    def validate(cls):
        if not cls.API_URL:
            raise ValueError("FASTGPT_API_URL 未配置")
        if not (cls.key_for_agent("A") and cls.key_for_agent("B") and cls.key_for_agent("C")):
            raise ValueError("请配置 FASTGPT_API_KEY 或 AGENT_A_KEY/AGENT_B_KEY/AGENT_C_KEY")

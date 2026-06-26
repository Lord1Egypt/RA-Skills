from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agent Policy & Guardrails Engine"
    environment: str = "dev"
    database_url: str = "sqlite:///./guardrails.db"

    model_config = SettingsConfigDict(env_prefix="GUARDRAILS_", env_file=".env", extra="ignore")


settings = Settings()

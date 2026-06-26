from pydantic import BaseModel, Field
from typing import List, Optional


class ProviderModel(BaseModel):
    id: str
    name: str
    reasoning: bool = False
    input: List[str] = ["text"]
    cost: dict = {}
    contextWindow: int = 64000
    maxTokens: int = 8000


class ProviderConfig(BaseModel):
    baseUrl: str
    apiKey: str
    api: str = "openai-completions"
    models: List[ProviderModel] = []


class ModelSwitchRequest(BaseModel):
    providerId: str
    baseUrl: str
    apiKey: str
    modelId: str
    contextWindow: int = 64000
    maxTokens: int = 8000


class UpdateApiKeyRequest(BaseModel):
    providerId: str
    apiKey: str


class ProviderConfigRequest(BaseModel):
    providerId: str
    baseUrl: str
    apiKey: str
    contextWindow: int = 64000
    maxTokens: int = 8000


class GatewayControlRequest(BaseModel):
    action: str = Field(..., description="Action: start, stop, restart")


class ModelCardResponse(BaseModel):
    id: str
    modelId: str
    providerId: str
    baseUrl: str
    isCurrent: bool


class ConfigStatus(BaseModel):
    currentModel: str
    modelCards: List[ModelCardResponse]


class SwitchResponse(BaseModel):
    success: bool
    message: str
    currentModel: Optional[str] = None


class DeleteRequest(BaseModel):
    providerId: str
    modelId: Optional[str] = None


class ControlResponse(BaseModel):
    success: bool
    message: str


class AdvancedSettingsSchema(BaseModel):
    toolsProfile: str = "full"
    allowExec: bool = True
    allowBrowser: bool = True
    allowWebSearch: bool = True
    allowWebFetch: bool = True
    denyElevated: bool = False
    denyShell: bool = False
    execHost: str = "gateway"
    execAsk: str = "always"
    execSecurity: str = "full"
    sandboxMode: str = "off"
    compactionMode: str = "safeguard"
    dmScope: str = "per-channel-peer"
    webSearchProvider: str = "brave"
    webFetchEnabled: bool = True

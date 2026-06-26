from fastapi import APIRouter, HTTPException
from typing import Optional

from .schemas import (
    ModelSwitchRequest,
    GatewayControlRequest,
    DeleteRequest,
    ModelCardResponse,
    ConfigStatus,
    SwitchResponse,
    ControlResponse,
    ProviderConfigRequest,
    UpdateApiKeyRequest,
    AdvancedSettingsSchema,
)
from ..core.config_manager import ConfigManager
from ..core.gateway import GatewayController
from secure_config import SecureConfig


router = APIRouter()
config_manager = ConfigManager()
gateway_controller = GatewayController()
secure_config = SecureConfig()


@router.get("/config", response_model=ConfigStatus)
async def get_config():
    """获取当前配置状态"""
    try:
        current_model = config_manager.get_current_model()
        model_cards = config_manager.get_model_cards()

        return ConfigStatus(
            currentModel=current_model or "未设置",
            modelCards=[
                ModelCardResponse(
                    id=card["id"],
                    modelId=card["modelId"],
                    providerId=card["providerId"],
                    baseUrl=card["baseUrl"],
                    isCurrent=card["isCurrent"],
                )
                for card in model_cards
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/switch", response_model=SwitchResponse)
async def switch_model(request: ModelSwitchRequest):
    """切换模型"""
    print(
        f"[API] Switch: providerId={request.providerId}, modelId={request.modelId}",
        flush=True,
    )
    try:
        switch_success = config_manager.switch_model_only(
            request.providerId, request.modelId
        )

        if not switch_success:
            raise HTTPException(status_code=500, detail="切换模型失败")

        # 使用指定的命令重启 Gateway
        success, message = gateway_controller.restart_with_command()
        current_model = config_manager.get_current_model()

        return SwitchResponse(
            success=success,
            message=f"模型已切换到 {current_model}\n重启服务: {'成功' if success else '失败'}",
            currentModel=current_model,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Switch error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restart-gateway", response_model=ControlResponse)
async def restart_gateway_cmd():
    """使用指定命令重启 Gateway"""
    try:
        success, message = gateway_controller.restart_with_command()
        return ControlResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gateway/control", response_model=ControlResponse)
async def control_gateway(request: GatewayControlRequest):
    """控制 Gateway 服务"""
    try:
        success, message = gateway_controller.control_gateway(request.action)
        return ControlResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save", response_model=SwitchResponse)
async def save_model(request: ModelSwitchRequest):
    """保存模型到通讯录（不切换当前使用，不重启服务）"""
    print(
        f"[API] Save: providerId={request.providerId}, modelId={request.modelId}",
        flush=True,
    )
    try:
        save_success = config_manager.save_provider(
            request.providerId,
            request.baseUrl,
            request.apiKey,
            request.modelId,
            request.contextWindow,
            request.maxTokens,
        )

        if not save_success:
            raise HTTPException(status_code=500, detail="保存配置失败")

        current_model = config_manager.get_current_model()

        return SwitchResponse(
            success=True,
            message=f"模型已保存到通讯录\n当前使用: {current_model or '未设置'}",
            currentModel=current_model,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Save error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_providers():
    """获取所有提供商"""
    try:
        providers = config_manager.get_all_providers()
        return {"providers": list(providers.keys())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config/validate")
async def validate_config():
    """手动检测并修复配置"""
    try:
        fixes = config_manager.validate_and_fix()
        return {"success": True, "fixes": fixes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/provider/{provider_id}")
async def get_provider_config(provider_id: str):
    """获取单个提供商的配置（从加密存储读取）"""
    try:
        config = secure_config.get_provider(provider_id)
        if config is None:
            return {
                "providerId": provider_id,
                "baseUrl": "",
                "apiKey": "",
                "contextWindow": 64000,
                "maxTokens": 8000,
            }
        return {"providerId": provider_id, **config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete", response_model=SwitchResponse)
async def delete_model(request: DeleteRequest):
    """删除模型或提供商"""
    print(
        f"[API] Delete: providerId={request.providerId}, modelId={request.modelId}",
        flush=True,
    )
    try:
        if request.modelId:
            success = config_manager.delete_model(request.providerId, request.modelId)
            msg = f"模型 {request.modelId} 已删除"
        else:
            success = config_manager.delete_provider(request.providerId)
            msg = f"提供商 {request.providerId} 已删除"

        if not success:
            raise HTTPException(status_code=500, detail="删除失败")

        current_model = config_manager.get_current_model()

        return SwitchResponse(success=True, message=msg, currentModel=current_model)
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Delete error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/provider/apikey", response_model=SwitchResponse)
async def update_provider_apikey(request: ProviderConfigRequest):
    """更新提供商的完整配置（API Key 加密存储）"""
    print(f"[API] Update Provider Config: providerId={request.providerId}", flush=True)
    try:
        secure_config.save_provider(
            request.providerId,
            {
                "baseUrl": request.baseUrl,
                "apiKey": request.apiKey,
                "contextWindow": request.contextWindow,
                "maxTokens": request.maxTokens,
            },
        )

        config_manager.update_provider_config(
            request.providerId,
            request.baseUrl,
            request.apiKey,
            request.contextWindow,
            request.maxTokens
        )

        config_manager.update_auth_profile(request.providerId, request.apiKey)

        return SwitchResponse(
            success=True,
            message=f"配置已加密保存到 {request.providerId}",
            currentModel=None,
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Update Provider Config error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings")
async def get_advanced_settings():
    """获取高级设置"""
    try:
        settings = config_manager.get_advanced_settings()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings")
async def update_advanced_settings(settings: AdvancedSettingsSchema):
    """更新高级设置"""
    try:
        success = config_manager.update_advanced_settings(settings.model_dump())
        if not success:
            raise HTTPException(status_code=500, detail="保存高级设置失败")
        return {"success": True, "message": "高级设置已保存"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

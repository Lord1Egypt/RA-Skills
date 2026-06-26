from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

from models import ModelSwitchRequest, GatewayControlRequest
from config_manager import ConfigManager
from gateway_controller import GatewayController
from secure_config import SecureConfig


class UpdateApiKeyRequest(BaseModel):
    providerId: str
    apiKey: str


class ProviderConfigRequest(BaseModel):
    providerId: str
    baseUrl: str
    apiKey: str
    contextWindow: int = 64000
    maxTokens: int = 8000


class ProviderResponse(BaseModel):
    """提供商响应"""
    providerId: str
    baseUrl: str
    apiKey: str
    modelId: Optional[str] = None
app = FastAPI(
    title="OpenClaw 模型切换工具",
    description="WebUI 管理界面",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化管理器
config_manager = ConfigManager()
gateway_controller = GatewayController()
secure_config = SecureConfig()

# 静态文件目录
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")


class ModelCardResponse(BaseModel):
    """模型卡片响应"""
    id: str
    modelId: str
    providerId: str
    baseUrl: str
    # 不包含apiKey，保护敏感信息
    isCurrent: bool


class SwitchResponse(BaseModel):
    """切换响应"""
    success: bool
    message: str
    currentModel: Optional[str] = None


class DeleteRequest(BaseModel):
    """删除请求"""
    providerId: str
    modelId: Optional[str] = None  # 不填则删除整个提供商


class ControlResponse(BaseModel):
    """控制响应"""
    success: bool
    message: str


class ConfigStatus(BaseModel):
    """配置状态"""
    currentModel: str
    modelCards: List[ModelCardResponse]


@app.get("/")
async def root():
    """返回前端页面"""
    frontend_index = os.path.join(frontend_dist, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    
    # 如果前端文件不存在，返回包含构建指引的HTML页面
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenClaw 模型切换工具</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #f5f7fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
            .btn { background: #409eff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #337ecc; }
            .code { background: #333; color: #fff; padding: 10px; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OpenClaw 模型切换工具</h1>
            <div class="card">
                <h2>前端未构建</h2>
                <p>需要先构建前端文件才能使用完整的Web UI界面。</p>
                
                <h3>构建步骤：</h3>
                <ol>
                    <li>打开命令行终端</li>
                    <li>切换到项目目录：<code>cd "项目路径"</code></li>
                    <li>安装依赖：<div class="code">cd frontend && npm install</div></li>
                    <li>构建前端：<div class="code">npm run build</div></li>
                    <li>重新启动服务</li>
                </ol>
                
                <h3>或者直接运行构建脚本：</h3>
                <p>在项目根目录创建并运行 <code>build_frontend.bat</code></p>
            </div>
            
            <div class="card">
                <h2>API接口</h2>
                <p>后端API已正常运行：</p>
                <ul>
                    <li><a href="/docs">API文档 (Swagger)</a></li>
                    <li><a href="/api/config">配置状态</a></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html_content)


@app.get("/api/config", response_model=ConfigStatus)
async def get_config():
    """获取当前配置状态"""
    try:
        current_model = config_manager.get_current_model()
        model_cards = config_manager.get_model_cards()

        return ConfigStatus(
            currentModel=current_model or "未设置",
            modelCards=[
                ModelCardResponse(
                    id=card['id'],
                    modelId=card['modelId'],
                    providerId=card['providerId'],
                    baseUrl=card['baseUrl'],
                    isCurrent=card['isCurrent']
                )
                for card in model_cards
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/switch", response_model=SwitchResponse)
async def switch_model(request: ModelSwitchRequest):
    """切换模型（只设置当前使用，不保存到通讯录）"""
    print(f"[API] Received switch request: providerId={request.providerId}, modelId={request.modelId}", flush=True)
    try:
        print(f"[API] Switching to model (set as current, no save to provider list)...", flush=True)
        # 切换模型（只设置当前使用，不添加到通讯录）
        switch_success = config_manager.switch_model_only(
            request.providerId,
            request.modelId
        )

        if not switch_success:
            print("[API] Switch model failed", flush=True)
            raise HTTPException(status_code=500, detail="切换模型失败")

        # 重启服务
        print("[API] Restarting gateway...", flush=True)
        restart_success, message = gateway_controller.restart_gateway()
        print(f"[API] Gateway restart result: success={restart_success}, message={message}", flush=True)

        current_model = config_manager.get_current_model()
        print(f"[API] Switch completed. Current model: {current_model}", flush=True)

        return SwitchResponse(
            success=restart_success,
            message=f"模型已切换到 {current_model}\n重启服务: {'成功' if restart_success else '失败'} - {message}",
            currentModel=current_model
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Switch error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gateway/control", response_model=ControlResponse)
async def control_gateway(request: GatewayControlRequest):
    """控制 Gateway 服务"""
    try:
        success, message = gateway_controller.control_gateway(request.action)
        return ControlResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/save", response_model=SwitchResponse)
async def save_model(request: ModelSwitchRequest):
    """保存模型到通讯录（不切换当前使用，不重启服务）"""
    print(f"[API] Received save request: providerId={request.providerId}, modelId={request.modelId}", flush=True)
    try:
        print(f"[API] Saving to provider list (通讯录)...", flush=True)
        save_success = config_manager.save_provider(
            request.providerId,
            request.baseUrl,
            request.apiKey,
            request.modelId
        )

        if not save_success:
            print("[API] Save provider failed", flush=True)
            raise HTTPException(status_code=500, detail="保存配置失败")

        print(f"[API] Save completed successfully", flush=True)
        current_model = config_manager.get_current_model()

        return SwitchResponse(
            success=True,
            message=f"模型已保存到通讯录\n当前使用: {current_model or '未设置'}",
            currentModel=current_model
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Save error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/providers")
async def get_providers():
    """获取所有提供商"""
    try:
        providers = config_manager.get_all_providers()
        return {"providers": list(providers.keys())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/delete", response_model=SwitchResponse)
async def delete_model(request: DeleteRequest):
    """删除模型或提供商"""
    print(f"[API] Delete request: providerId={request.providerId}, modelId={request.modelId}", flush=True)
    try:
        if request.modelId:
            # 删除单个模型
            success = config_manager.delete_model(request.providerId, request.modelId)
            msg = f"模型 {request.modelId} 已删除"
        else:
            # 删除整个提供商
            success = config_manager.delete_provider(request.providerId)
            msg = f"提供商 {request.providerId} 已删除"

        if not success:
            raise HTTPException(status_code=500, detail="删除失败")

        print(f"[API] Delete success: {msg}", flush=True)
        current_model = config_manager.get_current_model()

        return SwitchResponse(
            success=True,
            message=msg,
            currentModel=current_model
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Delete error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


class UpdateApiKeyRequest(BaseModel):
    providerId: str
    apiKey: str


@app.post("/api/provider/apikey", response_model=SwitchResponse)
async def update_provider_apikey(request: UpdateApiKeyRequest):
    """更新提供商的 API Key"""
    print(f"[API] Update API Key: providerId={request.providerId}", flush=True)
    try:
        success = config_manager.update_provider_apikey(
            request.providerId,
            request.apiKey
        )

        if not success:
            raise HTTPException(status_code=500, detail="更新 API Key 失败")

        print(f"[API] API Key updated for {request.providerId}", flush=True)

        return SwitchResponse(
            success=True,
            message=f"API Key 已保存到 {request.providerId}",
            currentModel=None
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] Update API Key error: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # 如果前端构建文件存在，挂载静态文件
    if os.path.exists(frontend_dist):
        # 挂载 assets 目录
        assets_dir = os.path.join(frontend_dist, "assets")
        if os.path.exists(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        # 挂载根目录（可选，用于其他静态文件）
        # app.mount("/static", StaticFiles(directory=frontend_dist), name="static")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9131,
        log_level="info"
    )

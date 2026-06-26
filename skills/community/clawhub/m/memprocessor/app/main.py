"""FastAPI应用主入口"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import router
from app.api.persona_routes import router as persona_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 初始化记忆服务
    from app.services.memory_service import get_memory_service
    try:
        await get_memory_service()
        print("✅ Memory service initialized")
    except Exception as e:
        print(f"⚠️  Memory service init warning: {e}")
    
    # 从配置文件同步人格
    try:
        from app.services.persona_service import get_persona_service
        from app.core.config_sync import initialize_persona_from_config
        
        persona_service = get_persona_service()
        
        # 尝试加载配置文件，如果不存在则使用默认
        config_path = "/etc/dreammoon/persona.json"  # 系统级配置
        if not Path(config_path).exists():
            config_path = "./config/persona.json"  # 本地配置
        
        persona = await initialize_persona_from_config(
            persona_service, 
            config_path if Path(config_path).exists() else None
        )
        
        if persona:
            print(f"🎭 Persona '{persona.name}' initialized")
        else:
            print("🎭 Using default persona configuration")
    except Exception as e:
        print(f"⚠️  Persona init warning: {e}")
    
    yield
    
    # 关闭时
    print("🛑 Shutting down...")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="四级记忆存储架构 - L1热存储/L2温存储/L3冷存储/L4归档 + 独立完整人格生成",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(router)
    app.include_router(persona_router)
    
    # 健康检查
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "service": settings.APP_NAME
        }
    
    # 根路径
    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "set_memory": "POST /api/v1/memory",
                "get_memory": "GET /api/v1/memory/{key}",
                "search": "GET /api/v1/search?q=query",
                "analyze": "POST /api/v1/analyze",
                "stats": "GET /api/v1/stats",
                "persona_generate": "POST /api/v1/persona/generate",
                "persona_evolve": "POST /api/v1/persona/evolve",
                "persona_reflect": "POST /api/v1/persona/reflect"
            }
        }
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS
    )

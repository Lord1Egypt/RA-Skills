import os
import sys

# 添加 backend 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.api.routes import router

# 创建 FastAPI 应用
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

# 静态文件目录（使用绝对路径）
# app/main.py 的父目录是 backend，再上一级是项目根目录
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取项目根目录（backend 的上一级）
project_root = os.path.dirname(backend_dir)
frontend_dist = os.path.join(project_root, "frontend", "dist")

# 注册路由
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """启动时自动检测并修复配置"""
    from app.core.config_manager import ConfigManager
    cm = ConfigManager()
    fixes = cm.validate_and_fix()
    if fixes:
        print(f"[Startup] 配置修复: {', '.join(fixes)}")
    else:
        print("[Startup] 配置检查通过，无需修复")


# 挂载静态文件（在模块级别，而非 if __name__）
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/")
async def root():
    """返回前端页面"""
    frontend_index = os.path.join(frontend_dist, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)

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
            .code { background: #333; color: #fff; padding: 10px; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OpenClaw 模型切换工具</h1>
            <div class="card">
                <h2>前端未构建</h2>
                <p>需要先构建前端文件才能使用完整的Web UI界面。</p>
                <ol>
                    <li>打开命令行终端</li>
                    <li>cd frontend && npm install</li>
                    <li>npm run build</li>
                    <li>重新启动服务</li>
                </ol>
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
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9131, log_level="info")

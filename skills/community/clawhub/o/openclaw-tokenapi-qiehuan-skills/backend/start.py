"""
后端服务启动入口
兼容旧版路径，确保 start_with_ui.bat 能正常工作
"""
import os
import sys

# 确保 backend/backend/app/main.py 能正确导入
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

# 导入并运行主模块
from app.main import app

if __name__ == "__main__":
    import uvicorn
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    frontend_dist = os.path.join(backend_path, "..", "frontend", "dist")

    if os.path.exists(frontend_dist):
        # 挂载静态文件目录
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

        # 添加根路径路由以提供 index.html
        @app.get("/")
        async def serve_index():
            return FileResponse(os.path.join(frontend_dist, "index.html"))

        # 添加 qrcode.jpg 等 public 文件的路由
        public_dir = os.path.join(backend_path, "..", "frontend", "public")
        if os.path.exists(public_dir):
            @app.get("/qrcode.jpg")
            async def serve_qrcode():
                return FileResponse(os.path.join(public_dir, "qrcode.jpg"))

    uvicorn.run(app, host="127.0.0.1", port=9131, log_level="info")
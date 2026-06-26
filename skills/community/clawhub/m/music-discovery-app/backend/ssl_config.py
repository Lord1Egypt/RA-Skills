"""
HTTPS 配置模块
提供 HTTPS 相关的配置和中间件
"""

import os
from fastapi import Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    """强制 HTTPS 中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 检查是否是 HTTPS 请求
        if not request.url.scheme == "https":
            # 构造 HTTPS URL
            https_url = str(request.url).replace("http://", "https://")
            return RedirectResponse(https_url, status_code=301)
        
        response = await call_next(request)
        return response


def get_ssl_config():
    """获取 SSL 配置"""
    ssl_config = {
        "ssl_enabled": False,
        "ssl_certfile": None,
        "ssl_keyfile": None,
        "ssl_cafile": None,
        "ssl_cert_reqs": None
    }
    
    # 检查环境变量
    if os.getenv("SSL_ENABLED", "false").lower() == "true":
        ssl_config["ssl_enabled"] = True
        ssl_config["ssl_certfile"] = os.getenv("SSL_CERTFILE")
        ssl_config["ssl_keyfile"] = os.getenv("SSL_KEYFILE")
        ssl_config["ssl_cafile"] = os.getenv("SSL_CAFILE")
        ssl_config["ssl_cert_reqs"] = os.getenv("SSL_CERT_REQS", "required")
    
    return ssl_config


def configure_https(app):
    """配置 HTTPS"""
    ssl_config = get_ssl_config()
    
    if ssl_config["ssl_enabled"]:
        # 添加 HTTPS 重定向中间件
        app.add_middleware(HTTPSRedirectMiddleware)
        
        # 配置 SSL 上下文
        ssl_context = None
        if ssl_config["ssl_certfile"] and ssl_config["ssl_keyfile"]:
            import ssl
            ssl_context = ssl.create_default_context(
                ssl.Purpose.CLIENT_AUTH,
                cafile=ssl_config["ssl_cafile"]
            )
            ssl_context.load_cert_chain(
                ssl_config["ssl_certfile"],
                ssl_config["ssl_keyfile"]
            )
            
            # 设置 SSL 选项
            if ssl_config["ssl_cert_reqs"] == "none":
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            else:
                ssl_context.check_hostname = True
                ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        return ssl_context
    
    return None
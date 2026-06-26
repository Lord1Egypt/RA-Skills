import logging
import os

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from baidu_search.baidu_api import search
from baidu_search.schemas import SearchRequest, SearchResponse

app = FastAPI(
    title="百度搜索 API",
    description="百度 AI 搜索代理服务",
    version="0.1.0",
    servers=[{"url": os.getenv("OPENAPI_SERVER_URL", "http://127.0.0.1:8001")}],
)
logger = logging.getLogger("baidu_search.main")


@app.get("/ping")
def ping() -> dict[str, str]:
    """健康检查"""
    return {"message": "pong"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(
        "Validation error on %s %s. body=%s errors=%s",
        request.method,
        request.url.path,
        exc.body,
        exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.post("/search", response_model=SearchResponse)
def web_search(request: SearchRequest) -> SearchResponse:
    """
    搜索网页
    
    - **query**: 搜索关键词
    - **top_k**: 返回结果数量 (1-20, 默认 10)
    - **recency_filter**: 时间过滤 (day, week, month, year)
    - **site_filter**: 限定搜索的网站列表
    """
    return search(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("baidu_search.main:app", host="0.0.0.0", port=8001)

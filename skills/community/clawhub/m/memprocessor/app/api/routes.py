"""FastAPI路由 - v1.0.1 Hotfix

修复内容:
1. 改进异常处理 - 区分业务错误和系统错误
2. 添加输入验证错误处理
3. 添加日志记录
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models import (
    AnalyzeRequest, AnalyzeResponse, GetMemoryResponse,
    SearchRequest, SearchResponse, SetMemoryRequest,
    SetMemoryResponse, StorageStats
)
from app.services.event_detector import get_event_detector
from app.services.memory_service import MemoryService, get_memory_service

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["memory"])


class ResourceNotFoundError(Exception):
    """资源不存在错误"""
    pass


class ValidationError(Exception):
    """验证错误"""
    pass


@router.post("/memory", response_model=SetMemoryResponse)
async def set_memory(
    request: SetMemoryRequest,
    service: MemoryService = Depends(get_memory_service)
):
    """存储记忆"""
    try:
        return await service.set(request)
    except ValidationError as e:
        logger.warning(f"Validation error in set_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ResourceNotFoundError as e:
        logger.warning(f"Resource not found in set_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error in set_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/memory/{key}", response_model=GetMemoryResponse)
async def get_memory(
    key: str,
    service: MemoryService = Depends(get_memory_service)
):
    """获取记忆"""
    try:
        result = await service.get(key)
        if result is None or result.content is None:
            raise ResourceNotFoundError(f"Memory with key '{key}' not found")
        return result
    except ResourceNotFoundError as e:
        logger.warning(f"Resource not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error in get_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/memory/{key}")
async def delete_memory(
    key: str,
    service: MemoryService = Depends(get_memory_service)
):
    """删除记忆"""
    try:
        # TODO: 实现删除逻辑
        logger.info(f"Delete memory requested for key: {key}")
        return {"success": True, "key": key, "note": "Delete logic not fully implemented"}
    except Exception as e:
        logger.exception(f"Error in delete_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete memory"
        )


@router.post("/search", response_model=SearchResponse)
async def search_memory(
    request: SearchRequest,
    service: MemoryService = Depends(get_memory_service)
):
    """搜索记忆"""
    try:
        return await service.search(request)
    except ValidationError as e:
        logger.warning(f"Validation error in search_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error in search_memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/search")
async def search_memory_get(
    q: str = Query(..., description="搜索关键词", min_length=1, max_length=1000),
    top_k: int = Query(default=5, ge=1, le=50),
    min_similarity: float = Query(default=0.5, ge=0.0, le=1.0),
    service: MemoryService = Depends(get_memory_service)
):
    """搜索记忆 (GET方式)"""
    try:
        request = SearchRequest(
            query=q,
            top_k=top_k,
            min_similarity=min_similarity
        )
        return await service.search(request)
    except ValidationError as e:
        logger.warning(f"Validation error in search_memory_get: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Unexpected error in search_memory_get: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_content(request: AnalyzeRequest):
    """分析内容重要性"""
    try:
        detector = get_event_detector()
        
        importance, events, is_sensitive = detector.analyze(
            request.content,
            request.context
        )
        
        # 决定建议层级
        from app.config import settings
        from app.models import MemoryLevel
        
        if importance >= settings.IMPORTANCE_IMMEDIATE:
            suggested_level = MemoryLevel.L3_COLD
        elif importance >= settings.IMPORTANCE_DAILY:
            suggested_level = MemoryLevel.L2_WARM
        else:
            suggested_level = MemoryLevel.L1_HOT
        
        return AnalyzeResponse(
            importance=importance,
            events=events,
            is_sensitive=is_sensitive,
            should_persist=importance >= settings.IMPORTANCE_DAILY and not is_sensitive,
            suggested_level=suggested_level
        )
    except Exception as e:
        logger.exception(f"Error in analyze_content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze content"
        )


@router.get("/stats", response_model=StorageStats)
async def get_stats(
    service: MemoryService = Depends(get_memory_service)
):
    """获取存储统计"""
    try:
        return await service.get_stats()
    except Exception as e:
        logger.exception(f"Error in get_stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get storage stats"
        )


@router.post("/tasks/daily")
async def run_daily_persistence(
    service: MemoryService = Depends(get_memory_service)
):
    """手动触发每日沉淀任务"""
    try:
        await service.run_daily_persistence()
        logger.info("Daily persistence task triggered manually")
        return {"success": True, "task": "daily_persistence"}
    except Exception as e:
        logger.exception(f"Error in daily persistence: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to run daily persistence"
        )


@router.post("/tasks/weekly")
async def run_weekly_archive(
    service: MemoryService = Depends(get_memory_service)
):
    """手动触发每周归档任务"""
    try:
        await service.run_weekly_archive()
        logger.info("Weekly archive task triggered manually")
        return {"success": True, "task": "weekly_archive"}
    except Exception as e:
        logger.exception(f"Error in weekly archive: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to run weekly archive"
        )

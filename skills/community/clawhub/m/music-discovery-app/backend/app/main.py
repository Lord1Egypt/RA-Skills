"""
音乐发现应用 - 后端API服务
集成多个免费音乐API
"""

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from typing import Optional, List, Dict, Any
import logging
from pydantic import BaseModel, constr, conint, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from ssl_config import configure_https, get_ssl_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 速率限制器
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 配置 HTTPS
ssl_context = configure_https(app)

app = FastAPI(
    title="音乐发现应用 API",
    description="集成多个免费音乐API的音乐发现服务",
    version="1.0.0"
)

# CORS配置
from fastapi.middleware.cors import CORSMiddleware

# 允许的来源列表，生产环境应该配置具体域名
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # 开发环境
    "http://127.0.0.1:3000",  # 开发环境
    "https://your-frontend-domain.com",  # 生产环境 - 请替换为实际的域名
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# API客户端
client = httpx.AsyncClient(timeout=30.0)

# API端点配置
ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
LYRICS_OVH_URL = "https://api.lyrics.ovh/v1"
MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2"
RADIO_BROWSER_URL = "https://api.radio-browser.info/json"
BANDSINTOWN_URL = "https://rest.bandsintown.com"

# 请求参数模型
class SearchParams(BaseModel):
    term: constr(min_length=1, max_length=100)
    media: constr(regex=r'^(music|podcast|audiobook|tvShow|movie|ebook|software)$') = "music"
    limit: conint(gt=0, le=50) = 20
    country: constr(min_length=2, max_length=2) = "CN"
    
    @validator('term')
    def validate_term(cls, v):
        # 过滤掉特殊字符
        if not v.strip():
            raise ValueError('搜索关键词不能为空')
        if len(v.strip()) < 1:
            raise ValueError('搜索关键词至少需要1个字符')
        return v.strip()

class RadioSearchParams(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    country: Optional[constr(min_length=2, max_length=2)] = None
    tag: Optional[constr(min_length=1, max_length=50)] = None
    limit: conint(gt=0, le=100) = 20

class LyricsParams(BaseModel):
    artist: constr(min_length=1, max_length=100)
    title: constr(min_length=1, max_length=100)
    
    @validator('artist', 'title')
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('艺术家名称和歌曲标题不能为空')
        return v.strip()


@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    """根路径"""
    return {
        "message": "音乐发现应用 API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search",
            "lyrics": "/api/lyrics",
            "artist": "/api/artist",
            "radio": "/api/radio",
            "events": "/api/events"
        }
    }


@app.get("/api/search")
@limiter.limit("50/minute")
async def search_music(
    request: Request,
    term: str = Query(..., min_length=1, max_length=100, description="搜索关键词"),
    media: str = Query("music", regex=r'^(music|podcast|audiobook|tvShow|movie|ebook|software)$', description="媒体类型"),
    limit: int = Query(20, gt=0, le=50, description="返回结果数量"),
    country: str = Query("CN", min_length=2, max_length=2, description="国家代码")
):
    """
    搜索音乐
    使用iTunes Search API
    """
    # 使用Pydantic模型验证参数
    try:
        search_params = SearchParams(term=term, media=media, limit=limit, country=country)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"参数错误: {str(e)}")
    
    try:
        params = {
            "term": search_params.term,
            "media": search_params.media,
            "limit": search_params.limit,
            "country": search_params.country
        }
        
        response = await client.get(ITUNES_SEARCH_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 处理结果
        results = []
        for item in data.get("results", []):
            results.append({
                "id": item.get("trackId"),
                "name": item.get("trackName"),
                "artist": item.get("artistName"),
                "album": item.get("collectionName"),
                "duration": item.get("trackTimeMillis"),
                "preview_url": item.get("previewUrl"),
                "artwork_url": item.get("artworkUrl100"),
                "genre": item.get("primaryGenreName"),
                "release_date": item.get("releaseDate"),
                "price": item.get("trackPrice"),
                "currency": item.get("currency")
            })
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
        
    except httpx.HTTPError as e:
        logger.error(f"搜索音乐失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/lyrics")
@limiter.limit("30/minute")
async def get_lyrics(
    request: Request,
    artist: str = Query(..., min_length=1, max_length=100, description="艺术家名称"),
    title: str = Query(..., min_length=1, max_length=100, description="歌曲标题")
):
    """
    获取歌词
    使用Lyrics.ovh API
    """
    # 使用Pydantic模型验证参数
    try:
        lyrics_params = LyricsParams(artist=artist, title=title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"参数错误: {str(e)}")
    
    try:
        url = f"{LYRICS_OVH_URL}/{lyrics_params.artist}/{lyrics_params.title}"
        
        response = await client.get(url)
        
        if response.status_code == 404:
            return {
                "success": False,
                "message": "未找到歌词"
            }
        
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "lyrics": data.get("lyrics", ""),
            "artist": lyrics_params.artist,
            "title": lyrics_params.title
        }
        
    except httpx.HTTPError as e:
        logger.error(f"获取歌词失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/artist/{artist_id}")
@limiter.limit("20/minute")
async def get_artist_info(
    request: Request,
    artist_id: str
):
    """
    获取艺术家信息
    使用MusicBrainz API
    """
    # 验证artist_id格式
    if not artist_id or len(artist_id.strip()) == 0:
        raise HTTPException(status_code=400, detail="艺术家ID不能为空")
    
    try:
        url = f"{MUSICBRAINZ_URL}/artist/{artist_id.strip()}"
        params = {
            "fmt": "json",
            "inc": "releases+url-rels"
        }
        
        response = await client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "id": data.get("id"),
            "name": data.get("name"),
            "type": data.get("type"),
            "country": data.get("country"),
            "disambiguation": data.get("disambiguation"),
            "life_span": data.get("life-span"),
            "releases": data.get("releases", []),
            "relations": data.get("relations", [])
        }
        
    except httpx.HTTPError as e:
        logger.error(f"获取艺术家信息失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/radio/search")
@limiter.limit("40/minute")
async def search_radio(
    request: Request,
    name: Optional[str] = Query(None, min_length=1, max_length=100, description="电台名称"),
    country: Optional[str] = Query(None, min_length=2, max_length=2, description="国家代码"),
    tag: Optional[str] = Query(None, min_length=1, max_length=50, description="标签"),
    limit: int = Query(20, gt=0, le=100, description="返回结果数量")
):
    """
    搜索网络电台
    使用Radio Browser API
    """
    # 使用Pydantic模型验证参数
    try:
        radio_params = RadioSearchParams(name=name, country=country, tag=tag, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"参数错误: {str(e)}")
    
    try:
        params = {
            "limit": radio_params.limit
        }
        
        if radio_params.name:
            params["name"] = radio_params.name
        if radio_params.country:
            params["countrycode"] = radio_params.country
        if radio_params.tag:
            params["tag"] = radio_params.tag
        
        url = f"{RADIO_BROWSER_URL}/stations/search"
        response = await client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 处理结果
        results = []
        for station in data:
            results.append({
                "id": station.get("stationuuid"),
                "name": station.get("name"),
                "url": station.get("url"),
                "homepage": station.get("homepage"),
                "favicon": station.get("favicon"),
                "country": station.get("countrycode"),
                "language": station.get("language"),
                "tags": station.get("tags", "").split(","),
                "bitrate": station.get("bitrate"),
                "codec": station.get("codec")
            })
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
        
    except httpx.HTTPError as e:
        logger.error(f"搜索电台失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/radio/top")
@limiter.limit("30/minute")
async def get_top_radio(
    request: Request,
    limit: int = Query(20, gt=0, le=100, description="返回结果数量")
):
    """
    获取热门电台
    使用Radio Browser API
    """
    # 使用Pydantic模型验证参数
    try:
        radio_params = RadioSearchParams(limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"参数错误: {str(e)}")
    
    try:
        url = f"{RADIO_BROWSER_URL}/stations/topvote/{radio_params.limit}"
        response = await client.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # 处理结果
        results = []
        for station in data:
            results.append({
                "id": station.get("stationuuid"),
                "name": station.get("name"),
                "url": station.get("url"),
                "homepage": station.get("homepage"),
                "favicon": station.get("favicon"),
                "country": station.get("countrycode"),
                "language": station.get("language"),
                "tags": station.get("tags", "").split(","),
                "bitrate": station.get("bitrate"),
                "codec": station.get("codec"),
                "votes": station.get("votes")
            })
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
        
    except httpx.HTTPError as e:
        logger.error(f"获取热门电台失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/events")
@limiter.limit("20/minute")
async def get_artist_events(
    request: Request,
    artist_name: str = Query(..., min_length=1, max_length=100, description="艺术家名称"),
    date: Optional[str] = Query(None, min_length=1, max_length=20, description="日期 (YYYY-MM-DD)")
):
    """
    获取艺术家演唱会信息
    使用Bandsintown API
    """
    # 使用Pydantic模型验证参数
    try:
        from pydantic import BaseModel, constr
        
        class EventParams(BaseModel):
            artist_name: constr(min_length=1, max_length=100)
            date: Optional[constr(min_length=1, max_length=20)] = None
            
        event_params = EventParams(artist_name=artist_name, date=date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"参数错误: {str(e)}")
    
    try:
        url = f"{BANDSINTOWN_URL}/artists/{event_params.artist_name}/events"
        params = {
            "app_id": "music_discovery_app"
        }
        
        if event_params.date:
            params["date"] = event_params.date
        
        response = await client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 处理结果
        results = []
        for event in data:
            results.append({
                "id": event.get("id"),
                "artist": event_params.artist_name,
                "venue": event.get("venue", {}),
                "datetime": event.get("datetime"),
                "description": event.get("description"),
                "url": event.get("url"),
                "offers": event.get("offers", [])
            })
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
        
    except httpx.HTTPError as e:
        logger.error(f"获取演唱会信息失败: {e}")
        raise HTTPException(status_code=500, detail="服务暂时不可用，请稍后重试")


@app.get("/api/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """健康检查"""
    return {
        "status": "healthy",
        "service": "music-discovery-api"
    }


@app.on_event("shutdown")
async def shutdown_event():
    """关闭事件"""
    await client.aclose()


if __name__ == "__main__":
    import uvicorn
    
    # 获取 SSL 配置
    ssl_config = get_ssl_config()
    
    # 启动服务器
    if ssl_config["ssl_enabled"] and ssl_context:
        logger.info("启动 HTTPS 服务器")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            ssl=ssl_context,
            reload=True
        )
    else:
        logger.info("启动 HTTP 服务器")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )

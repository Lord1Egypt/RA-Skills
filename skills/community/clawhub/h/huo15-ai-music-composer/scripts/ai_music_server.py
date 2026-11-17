#!/usr/bin/env python3
"""
AI 音乐创作服务端
提供 REST API 接口的 AI 音乐创作服务

作者：聚星逸 AI 团队
版本：v1.0.0 (2026.07)
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

import aiohttp
from aiohttp import web, hdrs
import aiofiles
import redis.asyncio as redis
import jwt
import bcrypt

from generate_music import AIMusicComposer

# 配置常量
class Config:
    HOST = "0.0.0.0"
    PORT = 8788
    REDIS_URL = "redis://redis-cache:6379/0"
    MAX_UPLOAD_SIZE = 200 * 1024 * 1024  # 200MB
    API_VERSION = "v1"
    JWT_SECRET_KEY = "your-jwt-secret-changing-this-in-production"
    
    # 文件存储路径
    UPLOAD_DIR = Path("/data/uploads")
    OUTPUT_DIR = Path("/data/outputs")
    TEMP_DIR = Path("/tmp/ai_music")
    
    @classmethod
    def init_dirs(cls):
        """初始化必要的目录"""
        for directory in [cls.UPLOAD_DIR, cls.OUTPUT_DIR, cls.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

class JobManager:
    """异步任务管理器"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.composer = AIMusicComposer("/app/config/music_config.json")
        self.active_jobs: Dict[str, asyncio.Task] = {}
        
    async def create_job(self, user_id: str, job_data: Dict) -> str:
        """创建新的音乐生成任务"""
        job_id = str(uuid.uuid4())
        
        job_info = {
            'job_id': job_id,
            'user_id': user_id,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'progress': 0,
            'stages': {},
            'data': job_data,
            'result': None,
            'error': None
        }
        
        # 保存到 Redis
        await self.redis.setex(
            f"music_job:{job_id}", 
            3600 * 24,  # 24小时过期
            json.dumps(job_info, ensure_ascii=False)
        )
        
        # 启动异步任务
        task = asyncio.create_task(self._run_job(job_id))
        self.active_jobs[job_id] = task
        
        return job_id
    
    async def _run_job(self, job_id: str):
        """执行音乐生成任务"""
        try:
            # 更新状态为运行中
            await self._update_job_status(job_id, 'running', 0)
            
            # 获取任务数据
            job_data = await self.redis.get(f"music_job:{job_id}")
            if not job_data:
                raise Exception("Job data not found")
                
            job_info = json.loads(job_data)
            data = job_info['data']
            
            # 执行音乐生成
            result = await self.composer.generate_music(
                voice_sample=data['voice_sample'],
                lyrics=data.get('lyrics'),
                theme=data.get('theme'),
                style=data.get('style', 'pop'),
                tempo=data.get('tempo', 120),
                duration=data.get('duration', 180),
                key=data.get('key', 'C'),
                emotion=data.get('emotion', 'uplifting'),
                language=data.get('language', 'chinese')
            )
            
            # 更新结果
            job_info['status'] = 'completed' if result['success'] else 'failed'
            job_info['progress'] = 100
            job_info['result'] = result['results'] if result['success'] else None
            job_info['error'] = result.get('error')
            job_info['completed_at'] = datetime.utcnow().isoformat()
            
            await self.redis.setex(
                f"music_job:{job_id}",
                3600 * 24,
                json.dumps(job_info, ensure_ascii=False)
            )
            
        except Exception as e:
            await self._update_job_status(job_id, 'failed', 0, str(e))
            
        finally:
            # 清理活跃任务
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
    
    async def _update_job_status(self, job_id: str, status: str, progress: int, error: str = None):
        """更新任务状态"""
        job_data = await self.redis.get(f"music_job:{job_id}")
        if job_data:
            job_info = json.loads(job_data)
            job_info['status'] = status
            job_info['progress'] = progress
            if error:
                job_info['error'] = error
            
            # 实时更新进度到 Redis
            await self.redis.setex(
                f"music_job:{job_id}",
                3600 * 24,
                json.dumps(job_info, ensure_ascii=False)
            )
    
    async def get_job_status(self, job_id: str) -> Optional[Dict]:
        """获取任务状态"""
        job_data = await self.redis.get(f"music_job:{job_id}")
        if job_data:
            return json.loads(job_data)
        return None
    
    async def cancel_job(self, job_id: str) -> bool:
        """取消任务"""
        if job_id in self.active_jobs:
            self.active_jobs[job_id].cancel()
            await self._update_job_status(job_id, 'cancelled', 0)
            return True
        return False

class APIServer:
    """REST API 服务器"""
    
    def __init__(self):
        self.app = web.Application(client_max_size=Config.MAX_UPLOAD_SIZE)
        self.redis = None
        self.job_manager = None
        
    async def init_app(self):
        """初始化应用"""
        Config.init_dirs()
        
        # 初始化 Redis
        self.redis = await redis.from_url(Config.REDIS_URL)
        self.job_manager = JobManager(self.redis)
        
        # 健康检查
        try:
            await self.redis.ping()
        except Exception as e:
            print(f"⚠️  Redis 连接失败: {e}")
            raise
        
        # 设置路由
        self.setup_routes()
        
    def setup_routes(self):
        """设置 API 路由"""
        
        # 音频上传接口
        self.app.router.add_post(f"/api/{Config.API_VERSION}/upload", self.upload_audio)
        
        # 音乐生成主接口
        self.app.router.add_post(f"/api/{Config.API_VERSION}/generate", self.generate_music)
        
        # 任务查询接口
        self.app.router.add_get(f"/api/{Config.API_VERSION}/job/{{job_id}}", self.get_job_status)
        
        # 任务取消接口
        self.app.router.add_delete(f"/api/{Config.API_VERSION}/job/{{job_id}}", self.cancel_job)
        
        # 用户任务列表
        self.app.router.add_get(f"/api/{Config.API_VERSION}/jobs", self.list_jobs)
        
        # 系统状态
        self.app.router.add_get(f"/api/{Config.API_VERSION}/status", self.get_system_status)
        
        # 预设风格查询
        self.app.router.add_get(f"/api/{Config.API_VERSION}/styles", self.get_styles)
        
        # 健康检查
        self.app.router.add_get("/health", self.health_check)
        
        # 中间件
        self.app.middlewares.append(self.auth_middleware)
        self.app.middlewares.append(self.cors_middleware)
    
    async def auth_middleware(self, app, handler):
        """JWT 认证中间件"""
        async def middleware(request):
            # 公开接口跳过认证
            public_paths = ['/health', f'/api/{Config.API_VERSION}/styles']
            if any(request.path.startswith(path) for path in public_paths):
                return await handler(request)
            
            # 检查 Authorization 头
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                raise web.HTTPUnauthorized(text="Missing or invalid Authorization header")
            
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                request['user_id'] = payload.get('user_id')
            except jwt.InvalidTokenError:
                raise web.HTTPUnauthorized(text="Invalid token")
            
            return await handler(request)
        return middleware
    
    async def cors_middleware(self, app, handler):
        """CORS 中间件"""
        async def middleware(request):
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
            return response
        return middleware
    
    # API 接口实现
    
    async def health_check(self, request):
        """健康检查"""
        return web.json_response({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'version': Config.API_VERSION
        })
    
    async def upload_audio(self, request):
        """音频文件上传"""
        try:
            reader = await request.multipart()
            field = await reader.next()
            
            if field.name != 'audio':
                raise web.HTTPBadRequest(text="Missing 'audio' field")
            
            # 保存文件
            filename = f"{uuid.uuid4()}.wav"
            filepath = Config.UPLOAD_DIR / filename
            
            async with aiofiles.open(filepath, 'wb') as f:
                while chunk := await field.read_chunk(8192):
                    await f.write(chunk)
            
            return web.json_response({
                'success': True,
                'filename': filename,
                'path': str(filepath),
                'size': filepath.stat().st_size
            })
            
        except Exception as e:
            raise web.HTTPInternalServerError(text=f"Upload failed: {str(e)}")
    
    async def generate_music(self, request):
        """音乐生成主接口"""
        try:
            data = await request.json()
            
            # 验证必要参数
            if not data.get('voice_sample'):
                raise web.HTTPBadRequest(text="Missing voice_sample")
            
            if not data.get('lyrics') and not data.get('theme'):
                raise web.HTTPBadRequest(text="Either lyrics or theme must be provided")
            
            # 创建生成任务
            job_id = await self.job_manager.create_job(
                user_id=request['user_id'],
                job_data={
                    'voice_sample': data['voice_sample'],
                    'lyrics': data.get('lyrics'),
                    'theme': data.get('theme'),
                    'style': data.get('style', 'pop'),
                    'tempo': data.get('tempo', 120),
                    'duration': data.get('duration', 180),
                    'key': data.get('key', 'C'),
                    'emotion': data.get('emotion', 'uplifting'),
                    'language': data.get('language', 'chinese')
                }
            )
            
            return web.json_response({
                'success': True,
                'job_id': job_id,
                'status': 'pending',
                'message': 'Music generation started'
            })
            
        except Exception as e:
            raise web.HTTPInternalServerError(text=f"Generation failed: {str(e)}")
    
    async def get_job_status(self, request):
        """查询任务状态"""
        job_id = request.match_info['job_id']
        
        job_data = await self.job_manager.get_job_status(job_id)
        if not job_data:
            raise web.HTTPNotFound(text="Job not found")
        
        # 清理敏感数据
        if 'data' in job_data:
            del job_data['data']
        
        return web.json_response(job_data)
    
    async def cancel_job(self, request):
        """取消任务"""
        job_id = request.match_info['job_id']
        
        success = await self.job_manager.cancel_job(job_id)
        if not success:
            raise web.HTTPNotFound(text="Job not found or already completed")
        
        return web.json_response({
            'success': True,
            'message': 'Job cancelled successfully'
        })
    
    async def list_jobs(self, request):
        """列出用户任务"""
        user_id = request['user_id']
        page = int(request.query.get('page', 1))
        limit = min(int(request.query.get('limit', 10)), 50)
        
        # 简单实现：扫描 Redis 查找用户任务
        jobs = []
        async for key in self.redis.scan_iter(f"music_job:*"):
            job_data = await self.redis.get(key)
            if job_data:
                job_info = json.loads(job_data)
                if job_info.get('user_id') == user_id:
                    if 'data' in job_info:
                        del job_info['data']  # 不返回敏感数据
                    jobs.append(job_info)
        
        # 排序和分页
        jobs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        start = (page - 1) * limit
        end = start + limit
        
        return web.json_response({
            'jobs': jobs[start:end],
            'total': len(jobs),
            'page': page,
            'limit': limit
        })
    
    async def get_system_status(self, request):
        """获取系统状态"""
        total_jobs = 0
        active_jobs = len(self.job_manager.active_jobs)
        
        async for _ in self.redis.scan_iter(f"music_job:*"):
            total_jobs += 1
        
        # 获取 Redis 信息
        try:
            redis_info = await self.redis.info()
            used_memory = redis_info.get('used_memory_human', 'N/A')
        except:
            used_memory = 'N/A'
        
        return web.json_response({
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'redis_memory': used_memory,
            'max_concurrent': 4,
            'system_uptime': 'P5D',  # 简化版本
            'gpu_usage': '模拟数据: 75%'  # 实际项目中需要真实获取
        })
    
    async def get_styles(self, request):
        """获取支持的风格列表"""
        styles = [
            {'id': 'pop', 'name': '流行', 'description': '现代流行音乐，适合大众口味'},
            {'id': 'rock', 'name': '摇滚', 'description': '充满力量和激情的音乐'},
            {'id': 'folk', 'name': '民谣', 'description': '简单真挚，娓娓道来'},
            {'id': 'electronic', 'name': '电子', 'description': '现代电子音乐，节奏感强'},
            {'id': 'rap', 'name': '说唱', 'description': '有节奏的说唱音乐'},
            {'id': 'ballad', 'name': '抒情', 'description': '情感丰富的抒情歌曲'},
            {'id': 'jazz', 'name': '爵士', 'description': '优雅自由的爵士乐'},
            {'id': 'classical', 'name': '古典', 'description': '经典优雅的古典风格'}
        ]
        
        return web.json_response({
            'styles': styles,
            'total': len(styles)
        })

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Music Composer Server')
    parser.add_argument('--host', default=Config.HOST, help='Host to bind to')
    parser.add_argument('--port', type=int, default=Config.PORT, help='Port to bind to')
    parser.add_argument('--redis-url', default=Config.REDIS_URL, help='Redis URL')
    
    args = parser.parse_args()
    
    # 创建并运行服务器
    server = APIServer()
    
    async def run_server():
        await server.init_app()
        runner = web.AppRunner(server.app)
        await runner.setup()
        site = web.TCPSite(runner, args.host, args.port)
        await site.start()
        
        print(f"🎵 AI 音乐创作服务已启动")
        print(f"🌐 API 地址: http://{args.host}:{args.port}")
        print(f"📚 API 文档: http://{args.host}:{args.port}/docs")
        print(f"🔄 Redis: {args.redis_url}")
        
        try:
            await asyncio.Event().wait()  # 无限等待
        except KeyboardInterrupt:
            print("\n🛑 服务正在关闭...")
        finally:
            await runner.cleanup()
    
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
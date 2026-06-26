#!/usr/bin/env python3
"""
Photo Search Skill - 完全独立版本

这是一个完全独立的程序，包含所有必要的功能代码。
不依赖主项目的任何模块，可以从任何目录运行。

使用示例:
    # 从任何目录调用
    python G:\\python\\PhotoIndexWithLLM\\skills\\photo-search\\skill.py search "海滩日落"
    
    # 扫描并搜索
    python G:\\python\\PhotoIndexWithLLM\\skills\\photo-search\\skill.py scan_and_search --dir D:\\Photos --query "海边"
    
    # JSON 格式输出
    python G:\\python\\PhotoIndexWithLLM\\skills\\photo-search\\skill.py search "海滩" --format json
"""

import sys
import os
import json
import argparse
import sqlite3
import base64
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
import platform


# ==========================================
# 跨平台支持
# ==========================================

def get_platform_type() -> str:
    """获取当前平台类型"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return system


def get_default_project_paths() -> List[Path]:
    """获取默认项目路径（跨平台）"""
    paths = []
    plat = get_platform_type()
    
    if plat == "windows":
        # Windows 常见路径
        paths.extend([
            Path(r"G:\python\PhotoIndexWithLLM"),
            Path(r"C:\python\PhotoIndexWithLLM"),
            Path(r"D:\python\PhotoIndexWithLLM"),
            Path.home() / "PhotoIndexWithLLM",
        ])
    elif plat == "linux":
        # Ubuntu/Linux 常见路径
        paths.extend([
            Path.home() / "PhotoIndexWithLLM",
            Path("/opt/PhotoIndexWithLLM"),
            Path("/usr/local/share/PhotoIndexWithLLM"),
            Path.home() / "projects" / "PhotoIndexWithLLM",
        ])
    elif plat == "macos":
        # macOS 常见路径
        paths.extend([
            Path.home() / "PhotoIndexWithLLM",
            Path("/Applications/PhotoIndexWithLLM"),
            Path.home() / "projects" / "PhotoIndexWithLLM",
        ])
    
    return paths


# ==========================================
# 配置管理
# ==========================================

class SkillConfig:
    """技能配置管理"""
    
    def __init__(self, config_path: str = None):
        self.config = {}
        
        # 尝试从主项目加载 .env
        if config_path:
            self._load_env_file(config_path)
        else:
            # 尝试查找主项目的 .env
            project_root = self._find_project_root()
            if project_root:
                env_file = project_root / ".env"
                if env_file.exists():
                    self._load_env_file(str(env_file))
        
        # 设置默认值
        self._set_defaults()
    
    def _find_project_root(self) -> Optional[Path]:
        """查找项目根目录（跨平台支持）"""
        current = Path(__file__).resolve().parent
        
        # 方法 1: 向上查找包含 config.py 的目录
        for parent in current.parents:
            if (parent / "config.py").exists():
                return parent
        
        # 方法 2: 尝试平台特定的默认路径
        default_paths = get_default_project_paths()
        for default_path in default_paths:
            if default_path.exists() and (default_path / "config.py").exists():
                return default_path
        
        # 方法 3: 如果 skill.py 在主项目目录内
        if (current / "config.py").exists():
            return current
        
        return None
    
    def _load_env_file(self, env_path: str):
        """加载 .env 文件"""
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"⚠ 加载配置文件失败: {e}", file=sys.stderr)
    
    def _set_defaults(self):
        """设置默认配置"""
        defaults = {
            "LOCAL_LLM_ENABLED": "true",
            "LOCAL_LLM_ENDPOINT": "http://localhost:1234/v1",
            "LOCAL_LLM_MODEL": "qwen3-vl-8b-q4_k_m",
            "LOCAL_LLM_API_KEY": "",
            "LOCAL_LLM_MAX_TOKENS": "2048",
            "LOCAL_LLM_TIMEOUT": "120",
            
            "REMOTE_LLM_ENABLED": "true",
            "REMOTE_LLM_ENDPOINT": "https://openrouter.ai/api/v1/chat/completions",
            "REMOTE_LLM_MODEL": "nvidia/nemotron-nano-12b-v2-vl:free",
            "REMOTE_LLM_API_KEY": "",
            "REMOTE_LLM_MAX_TOKENS": "4096",
            "REMOTE_LLM_TIMEOUT": "180",
            
            "REMOTE_RATE_LIMIT_PER_MINUTE": "5",
            "REMOTE_RETRY_TIMES": "3",
            "REMOTE_RETRY_DELAY": "60",
            
            "LLM_ROUTING_MODE": "auto",
            "LOCAL_CONFIDENCE_THRESHOLD": "0.7",
            
            # 隐私保护配置
            "PRIVACY_MODE": "local_only",  # local_only | hybrid | remote
            "ALLOW_REMOTE_UPLOAD": "false",  # 是否允许上传照片到远程
            "REQUIRE_REMOTE_CONFIRM": "true",  # 远程传输需要确认
            
            "SUPPORTED_IMAGE_FORMATS": ".jpg,.jpeg,.png,.webp,.bmp,.tiff,.gif,.heic,.heif,.cr2,.nef,.arw,.orf,.raf,.dng,.rw2,.pef,.sr2",
            "MAX_IMAGE_SIZE_MB": "50",
            "MAX_WORKERS": "2",
            
            "DB_PATH": "data/photo_index.db",
        }
        
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value
    
    def get(self, key: str, default: str = None) -> str:
        """获取配置值"""
        return self.config.get(key, default)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔配置值"""
        value = self.config.get(key, str(default)).lower()
        return value in ("true", "1", "yes")
    
    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数配置值"""
        try:
            return int(self.config.get(key, str(default)))
        except:
            return default


# ==========================================
# 数据库管理
# ==========================================

class PhotoDatabase:
    """照片数据库管理"""
    
    def __init__(self, db_path: str = "data/photo_index.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def _init_db(self):
        """初始化数据库"""
        conn = self._get_connection()
        
        # 创建 photos 表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                file_name TEXT NOT NULL,
                file_size INTEGER,
                capture_date TIMESTAMP,
                modified_date TIMESTAMP,
                scene_type TEXT DEFAULT 'unknown',
                objects TEXT DEFAULT '[]',
                people_count INTEGER DEFAULT 0,
                activity TEXT DEFAULT '',
                mood TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                description TEXT DEFAULT '',
                detailed_analysis TEXT DEFAULT '',
                time_inference TEXT DEFAULT '',
                location_hints TEXT DEFAULT '',
                processed_by TEXT DEFAULT 'unknown',
                confidence_score REAL DEFAULT 0.0,
                processing_time TIMESTAMP,
                language TEXT DEFAULT 'zh',
                search_text TEXT DEFAULT ''
            )
        """)
        
        # 创建 FTS 表
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS photos_fts USING fts5(
                description, tags, scene_type, activity, mood,
                detailed_analysis, search_text,
                content='photos', content_rowid='id'
            )
        """)
        
        # 创建触发器
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS photos_ai AFTER INSERT ON photos BEGIN
                INSERT INTO photos_fts(rowid, description, tags, scene_type, activity, mood, detailed_analysis, search_text)
                VALUES (new.id, new.description, new.tags, new.scene_type, new.activity, new.mood, new.detailed_analysis, new.search_text);
            END
        """)
        
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS photos_au AFTER UPDATE ON photos BEGIN
                INSERT INTO photos_fts(photos_fts, rowid, description, tags, scene_type, activity, mood, detailed_analysis, search_text)
                VALUES('delete', old.id, old.description, old.tags, old.scene_type, old.activity, old.mood, old.detailed_analysis, old.search_text);
                INSERT INTO photos_fts(rowid, description, tags, scene_type, activity, mood, detailed_analysis, search_text)
                VALUES (new.id, new.description, new.tags, new.scene_type, new.activity, new.mood, new.detailed_analysis, new.search_text);
            END
        """)
        
        # 创建索引
        conn.execute("CREATE INDEX IF NOT EXISTS idx_photos_scene ON photos(scene_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_photos_capture ON photos(capture_date)")
        
        conn.commit()
        conn.close()
    
    def insert_photo(self, photo_data: dict) -> bool:
        """插入照片"""
        conn = self._get_connection()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO photos (
                    file_path, file_name, file_size, modified_date,
                    scene_type, objects, people_count, activity, mood, tags,
                    description, detailed_analysis, time_inference, location_hints,
                    processed_by, confidence_score, processing_time, language, search_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                photo_data["file_path"],
                photo_data["file_name"],
                photo_data.get("file_size"),
                photo_data.get("modified_date"),
                photo_data.get("scene_type", "unknown"),
                json.dumps(photo_data.get("objects", []), ensure_ascii=False),
                photo_data.get("people_count", 0),
                photo_data.get("activity", ""),
                photo_data.get("mood", ""),
                json.dumps(photo_data.get("tags", []), ensure_ascii=False),
                photo_data.get("description", ""),
                photo_data.get("detailed_analysis", ""),
                photo_data.get("time_inference", ""),
                photo_data.get("location_hints", ""),
                photo_data.get("processed_by", "local"),
                photo_data.get("confidence_score", 0.0),
                photo_data.get("processing_time", datetime.now().isoformat()),
                photo_data.get("language", "zh"),
                photo_data.get("search_text", "")
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"✗ 插入照片失败: {e}", file=sys.stderr)
            return False
        finally:
            conn.close()
    
    def search(self, query: str = "", tags: List[str] = None, 
               scene_type: str = None, date_from: str = None,
               date_to: str = None, limit: int = 20, offset: int = 0) -> dict:
        """搜索照片"""
        conn = self._get_connection()
        
        results = []
        total = 0
        
        try:
            if query:
                # FTS 搜索
                fts_query = " AND ".join(query.split())
                cursor = conn.execute("""
                    SELECT p.*, f.rank
                    FROM photos p
                    JOIN photos_fts f ON p.id = f.rowid
                    WHERE photos_fts MATCH ?
                    ORDER BY f.rank
                    LIMIT ? OFFSET ?
                """, (fts_query, limit, offset))
                
                results = [dict(row) for row in cursor.fetchall()]
                
                # 获取总数
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM photos p
                    JOIN photos_fts f ON p.id = f.rowid
                    WHERE photos_fts MATCH ?
                """, (fts_query,))
                total = cursor.fetchone()[0]
            else:
                # 获取所有照片
                cursor = conn.execute("""
                    SELECT * FROM photos
                    ORDER BY processing_time DESC
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                
                results = [dict(row) for row in cursor.fetchall()]
                
                cursor = conn.execute("SELECT COUNT(*) FROM photos")
                total = cursor.fetchone()[0]
            
            # 应用过滤
            if tags:
                filtered = []
                for r in results:
                    try:
                        r_tags = json.loads(r.get("tags", "[]")) if isinstance(r.get("tags"), str) else r.get("tags", [])
                        if any(t in r_tags for t in tags):
                            filtered.append(r)
                    except:
                        pass
                results = filtered
                total = len(results)
            
            if scene_type:
                results = [r for r in results if scene_type.lower() in r.get("scene_type", "").lower()]
                total = len(results)
            
            return {
                "results": results,
                "total": total,
                "limit": limit,
                "offset": offset,
                "search_type": "fts" if query else "all"
            }
        
        except Exception as e:
            print(f"✗ 搜索失败: {e}", file=sys.stderr)
            return {"results": [], "total": 0, "error": str(e)}
        finally:
            conn.close()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        conn = self._get_connection()
        try:
            stats = {}
            
            cursor = conn.execute("SELECT COUNT(*) FROM photos")
            stats["total"] = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT scene_type, COUNT(*) as count
                FROM photos
                GROUP BY scene_type
                ORDER BY count DESC
            """)
            stats["by_scene"] = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor = conn.execute("""
                SELECT processed_by, COUNT(*) as count
                FROM photos
                GROUP BY processed_by
            """)
            stats["by_processor"] = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor = conn.execute("SELECT AVG(confidence_score) FROM photos")
            stats["avg_confidence"] = cursor.fetchone()[0] or 0
            
            return stats
        finally:
            conn.close()


# ==========================================
# 照片扫描器
# ==========================================

class PhotoScanner:
    """照片扫描器"""
    
    def __init__(self, supported_formats: List[str] = None, 
                 max_size_mb: int = 50):
        self.supported_formats = supported_formats or [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif", ".heic", ".heif", ".cr2", ".nef", ".arw", ".orf", ".raf", ".dng", ".rw2", ".pef", ".sr2"]
        self.max_size = max_size_mb * 1024 * 1024
    
    def scan_directory(self, directory: str) -> List[dict]:
        """扫描目录"""
        path = Path(directory)
        if not path.exists():
            print(f"⚠ 目录不存在: {directory}", file=sys.stderr)
            return []
        
        photos = []
        for root, dirs, files in os.walk(path):
            # 过滤隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                
                if file_path.suffix.lower() not in self.supported_formats:
                    continue
                
                try:
                    file_size = file_path.stat().st_size
                    if file_size > self.max_size:
                        continue
                except:
                    continue
                
                photos.append({
                    "file_path": str(file_path.absolute()),
                    "file_name": file_path.name,
                    "file_size": file_size,
                    "modified_date": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
        
        return photos


# ==========================================
# VL 模型客户端
# ==========================================

class VLClient:
    """VL 模型客户端"""
    
    def __init__(self, endpoint: str, model: str, api_key: str = "", 
                 max_tokens: int = 2048, timeout: int = 120,
                 is_remote: bool = False, require_confirm: bool = True):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.is_remote = is_remote  # 是否为远程服务器
        self.require_confirm = require_confirm  # 是否需要确认
        self.confirmed = False  # 用户是否已确认
        
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def analyze_image(self, image_path: str, prompt: str) -> dict:
        """分析图片"""
        # 隐私保护：远程传输需要确认
        if self.is_remote and self.require_confirm and not self.confirmed:
            print(f"\n⚠️  隐私警告：使用远程模型会将照片发送到第三方服务器", file=sys.stderr)
            print(f"   目标服务器: {self.endpoint}", file=sys.stderr)
            print(f"   照片内容可能被第三方存储或分析", file=sys.stderr)
            print(f"   如果照片包含敏感内容，建议使用本地模型", file=sys.stderr)
            
            # 在非交互模式下拒绝
            if not sys.stdin.isatty():
                raise PermissionError(
                    "远程传输需要用户确认，但当前为非交互模式。\n"
                    "请在配置中设置 REQUIRE_REMOTE_CONFIRM=false 以禁用此检查。"
                )
            
            confirm = input("\n是否继续上传照片到远程服务器？(yes/no): ")
            if confirm.lower() != "yes":
                raise PermissionError("用户拒绝远程传输照片")
            
            self.confirmed = True
            print()
        
        # 构建消息
        message = self._build_vision_message(image_path, prompt)
        
        payload = {
            "model": self.model,
            "messages": [message],
            "max_tokens": self.max_tokens,
            "stream": False,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return self._parse_json_response(content)
        
        except Exception as e:
            raise RuntimeError(f"VL 分析失败: {e}")
    
    def _build_vision_message(self, image_path: str, prompt: str) -> dict:
        """构建视觉消息"""
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        mime_type = "image/jpeg"
        ext = Path(image_path).suffix.lower()
        if ext == ".png":
            mime_type = "image/png"
        elif ext == ".webp":
            mime_type = "image/webp"
        
        return {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_base64}"
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }
    
    def _parse_json_response(self, content: str) -> dict:
        """解析 JSON 响应"""
        try:
            return json.loads(content)
        except:
            pass
        
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end > start:
                    json_str = content[start:end]
                else:
                    json_str = content
            
            return json.loads(json_str)
        except:
            return {
                "scene": "unknown",
                "objects": [],
                "people_count": 0,
                "activity": "",
                "mood": "",
                "tags": [],
                "description": content[:200],
                "confidence": 0.3
            }
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            response = requests.get(
                f"{self.endpoint}/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False


# ==========================================
# 智能路由器
# ==========================================

class PhotoRouter:
    """照片处理路由器"""
    
    def __init__(self, config: SkillConfig):
        self.config = config
        self.local_client = None
        self.remote_client = None
        
        # 初始化客户端
        if config.get_bool("LOCAL_LLM_ENABLED"):
            self.local_client = VLClient(
                endpoint=config.get("LOCAL_LLM_ENDPOINT"),
                model=config.get("LOCAL_LLM_MODEL"),
                api_key=config.get("LOCAL_LLM_API_KEY"),
                max_tokens=config.get_int("LOCAL_LLM_MAX_TOKENS"),
                timeout=config.get_int("LOCAL_LLM_TIMEOUT"),
                is_remote=False,  # 本地模型
                require_confirm=False  # 本地不需要确认
            )
        
        if config.get_bool("REMOTE_LLM_ENABLED") and config.get("REMOTE_LLM_API_KEY"):
            # 检查隐私模式
            privacy_mode = config.get("PRIVACY_MODE", "local_only")
            allow_remote = config.get_bool("ALLOW_REMOTE_UPLOAD", False)
            
            if privacy_mode == "local_only" and not allow_remote:
                print("⚠️  隐私模式：远程模型已禁用", file=sys.stderr)
            else:
                self.remote_client = VLClient(
                    endpoint=config.get("REMOTE_LLM_ENDPOINT"),
                    model=config.get("REMOTE_LLM_MODEL"),
                    api_key=config.get("REMOTE_LLM_API_KEY"),
                    max_tokens=config.get_int("REMOTE_LLM_MAX_TOKENS"),
                    timeout=config.get_int("REMOTE_LLM_TIMEOUT"),
                    is_remote=True,  # 远程模型
                    require_confirm=config.get_bool("REQUIRE_REMOTE_CONFIRM", True)
                )
    
    def analyze_photo(self, image_path: str, prompt: str = None) -> dict:
        """分析照片"""
        if not prompt:
            prompt = """请简洁描述这张照片的内容，输出JSON格式：
{
  "scene": "场景类型",
  "objects": ["物体列表"],
  "people_count": 人数,
  "activity": "主要活动",
  "mood": "氛围",
  "tags": ["标签"],
  "description": "一句话描述",
  "confidence": 0.0-1.0置信度
}"""
        
        # 隐私模式检查
        privacy_mode = self.config.get("PRIVACY_MODE", "local_only")
        
        # 优先使用本地模型
        if self.local_client:
            try:
                result = self.local_client.analyze_image(image_path, prompt)
                result["processed_by"] = "local"
                return result
            except Exception as e:
                print(f"⚠ 本地模型失败: {e}", file=sys.stderr)
                
                # 隐私模式下不降级到远程
                if privacy_mode == "local_only":
                    raise RuntimeError(
                        f"本地模型失败，隐私模式禁止使用远程模型。\n"
                        f"错误: {e}"
                    )
        
        # 降级到远程（仅在非隐私模式下）
        if self.remote_client and privacy_mode != "local_only":
            try:
                result = self.remote_client.analyze_image(image_path, prompt)
                result["processed_by"] = "remote"
                return result
            except Exception as e:
                raise RuntimeError(f"远程模型也失败: {e}")
        
        raise RuntimeError("没有可用的 VL 模型")
    
    def test_connections(self) -> dict:
        """测试连接"""
        return {
            "local": {
                "enabled": self.local_client is not None,
                "connected": self.local_client.test_connection() if self.local_client else False
            },
            "remote": {
                "enabled": self.remote_client is not None,
                "connected": self.remote_client.test_connection() if self.remote_client else False
            }
        }


# ==========================================
# 主程序
# ==========================================

def scan_photos(args, config: SkillConfig):
    """扫描照片"""
    scanner = PhotoScanner(
        max_size_mb=config.get_int("MAX_IMAGE_SIZE_MB", 50)
    )
    db = PhotoDatabase(config.get("DB_PATH", "data/photo_index.db"))
    router = PhotoRouter(config)
    
    prompt = """请简洁描述这张照片的内容，输出JSON格式：
{"scene":"场景类型","objects":["物体"],"people_count":人数,"activity":"活动","mood":"氛围","tags":["标签"],"description":"一句话描述","confidence":0.0-1.0}"""
    
    directories = args.dir or []
    
    for directory in directories:
        print(f"📂 扫描目录: {directory}")
        photos = scanner.scan_directory(directory)
        print(f"✓ 找到 {len(photos)} 张照片")
        
        for i, photo in enumerate(photos, 1):
            print(f"  [{i}/{len(photos)}] 分析: {photo['file_name']}")
            
            try:
                result = router.analyze_photo(photo["file_path"], prompt)
                
                photo_data = {
                    **photo,
                    **result,
                    "search_text": " ".join([
                        result.get("description", ""),
                        result.get("activity", ""),
                        result.get("mood", ""),
                        " ".join(result.get("tags", [])),
                        " ".join(result.get("objects", []))
                    ])
                }
                
                db.insert_photo(photo_data)
                print(f"    ✓ 已索引")
            
            except Exception as e:
                print(f"    ✗ 失败: {e}", file=sys.stderr)
    
    print("\n✓ 扫描完成")


def search_photos(args, config: SkillConfig):
    """搜索照片"""
    db = PhotoDatabase(config.get("DB_PATH", "data/photo_index.db"))
    
    tags = args.tags.split(",") if args.tags else None
    results = db.search(
        query=args.query,
        tags=tags,
        scene_type=args.scene,
        date_from=getattr(args, 'date_from', None),
        date_to=getattr(args, 'date_to', None),
        limit=args.limit
    )
    
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n🔍 搜索查询: '{args.query}'")
        print(f"📊 找到 {results['total']} 条结果\n")
        
        if not results["results"]:
            print("未找到匹配的照片")
            return
        
        for i, photo in enumerate(results["results"], 1):
            print(f"{i}. {photo.get('file_name', 'unknown')}")
            print(f"   📁 {photo.get('file_path', '')}")
            print(f"   🏷️  场景: {photo.get('scene_type', 'unknown')}")
            print(f"   📝 描述: {photo.get('description', '')}")
            
            tags = photo.get('tags', [])
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except:
                    tags = []
            
            if tags:
                print(f"   🔖 标签: {', '.join(tags[:5])}")
            
            print(f"   ⭐ 置信度: {photo.get('confidence_score', 0):.2f}")
            print()


def get_stats(args, config: SkillConfig):
    """获取统计"""
    db = PhotoDatabase(config.get("DB_PATH", "data/photo_index.db"))
    stats = db.get_stats()
    
    if args.format == "json":
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("\n📊 照片索引统计")
        print("="*40)
        print(f"总照片数: {stats['total']}")
        print(f"平均置信度: {stats['avg_confidence']:.2f}")
        print()
        
        print("按场景类型:")
        for scene, count in stats.get('by_scene', {}).items():
            print(f"  {scene}: {count}")
        
        print()
        print("按处理模型:")
        for processor, count in stats.get('by_processor', {}).items():
            print(f"  {processor}: {count}")


def test_connection(args, config: SkillConfig):
    """测试连接"""
    router = PhotoRouter(config)
    connections = router.test_connections()
    
    if args.format == "json":
        print(json.dumps(connections, ensure_ascii=False, indent=2))
    else:
        print("\n🔌 LLM 连接测试")
        print("="*40)
        
        for name, info in connections.items():
            status = "✓ 已连接" if info["connected"] else "✗ 未连接"
            print(f"\n{name.upper()}:")
            print(f"  状态: {status}")


def main():
    """主入口"""
    # 查找配置文件
    current = Path(__file__).resolve().parent
    config_path = None
    
    for parent in current.parents:
        env_file = parent / ".env"
        if env_file.exists():
            config_path = str(env_file)
            break
    
    # 加载配置
    config = SkillConfig(config_path)
    
    parser = argparse.ArgumentParser(
        description="Photo Search Skill - 独立照片搜索技能",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # scan
    scan_p = subparsers.add_parser("scan", help="扫描照片")
    scan_p.add_argument("--dir", nargs="+", required=True, help="扫描目录")
    scan_p.set_defaults(func=scan_photos)
    
    # search
    search_p = subparsers.add_parser("search", help="搜索照片")
    search_p.add_argument("query", help="搜索关键词")
    search_p.add_argument("--tags", help="标签过滤")
    search_p.add_argument("--scene", help="场景类型")
    search_p.add_argument("--limit", type=int, default=20, help="返回数量")
    search_p.add_argument("--format", choices=["text", "json"], default="text")
    search_p.set_defaults(func=search_photos)
    
    # stats
    stats_p = subparsers.add_parser("stats", help="统计信息")
    stats_p.add_argument("--format", choices=["text", "json"], default="text")
    stats_p.set_defaults(func=get_stats)
    
    # test
    test_p = subparsers.add_parser("test", help="测试连接")
    test_p.add_argument("--format", choices=["text", "json"], default="text")
    test_p.set_defaults(func=test_connection)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args, config)


if __name__ == "__main__":
    main()

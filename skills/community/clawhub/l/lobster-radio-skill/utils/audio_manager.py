"""
音频文件管理模块

负责音频文件的存储、命名和清理。
"""

import os
import re
import uuid
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta
import json


class AudioManager:
    """
    音频文件管理器
    
    负责音频文件的存储、命名和清理。
    """
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        初始化音频管理器
        
        Args:
            storage_dir: 音频文件存储目录（可选）
                - 不设置时：默认使用 data/radios
                - 设置为 "downloads"：使用用户下载文件夹
                - 设置为 "desktop"：使用用户桌面
                - 其他：直接使用指定路径
        """
        if storage_dir is None:
            env_dir = os.environ.get("LOBSTER_RADIO_OUTPUT")
            if env_dir:
                if env_dir == "downloads":
                    storage_dir = Path.home() / "Downloads" / "lobster-radio"
                elif env_dir == "desktop":
                    storage_dir = Path.home() / "Desktop" / "lobster-radio"
                else:
                    storage_dir = Path(env_dir)
            else:
                storage_dir = Path(__file__).parent.parent / "data" / "radios"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def set_output_location(self, location: str = "default") -> bool:
        """
        设置音频输出位置
        
        Args:
            location: 输出位置
                - "default": 使用技能目录下的 data/radios
                - "desktop": 使用用户桌面/lobster-radio
                - "downloads": 使用用户下载文件夹/lobster-radio
                - 其他: 直接使用指定路径
        
        Returns:
            bool: 设置是否成功
        """
        if location == "default":
            self.storage_dir = Path(__file__).parent.parent / "data" / "radios"
        elif location == "desktop":
            self.storage_dir = Path.home() / "Desktop" / "lobster-radio"
        elif location == "downloads":
            self.storage_dir = Path.home() / "Downloads" / "lobster-radio"
        else:
            self.storage_dir = Path(location)
        
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            test_file = self.storage_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception:
            self.storage_dir = Path(__file__).parent.parent / "data" / "radios"
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            return False
    
    def _sanitize_filename(self, name: str) -> str:
        """
        清理文件名，移除非法字符
        
        Args:
            name: 原始名称
            
        Returns:
            str: 清理后的名称
        """
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = name.strip()
        if len(name) > 50:
            name = name[:50]
        return name if name else "untitled"
    
    def _generate_filename(
        self,
        title: Optional[str] = None,
        user_id: str = "default",
        format: str = "wav"
    ) -> str:
        """
        生成文件名
        
        Args:
            title: 音频标题（主题）
            user_id: 用户ID
            format: 音频格式
            
        Returns:
            str: 生成的文件名
        """
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        
        if title:
            safe_title = self._sanitize_filename(title)
            filename = f"{date_str}{safe_title}.{format}"
        else:
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"radio_{user_id}_{timestamp}_{unique_id}.{format}"
        
        return filename
    
    def save(
        self,
        audio_data: bytes,
        user_id: str,
        format: str = "wav",
        metadata: Optional[dict] = None,
        title: Optional[str] = None,
        output_location: Optional[str] = None
    ) -> dict:
        """
        保存音频文件
        
        Args:
            audio_data: 音频数据
            user_id: 用户ID
            format: 音频格式
            metadata: 元数据
            title: 音频标题（用于文件名）
            output_location: 输出位置 ("desktop", "downloads", "default")
            
        Returns:
            dict: 包含 relative_url, absolute_path, filename 等字段
        """
        if output_location:
            self.set_output_location(output_location)
        
        filename = self._generate_filename(title=title, user_id=user_id, format=format)
        filepath = self.storage_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        if metadata:
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {
            "relative_url": f"/radios/{filename}",
            "absolute_path": str(filepath),
            "filename": filename,
            "output_location": str(self.storage_dir)
        }
    
    def get(self, filename: str) -> Optional[bytes]:
        """
        获取音频文件
        
        Args:
            filename: 文件名
            
        Returns:
            Optional[bytes]: 音频数据，None表示文件不存在
        """
        filepath = self.storage_dir / filename
        if filepath.exists():
            with open(filepath, 'rb') as f:
                return f.read()
        return None
    
    def list(self, limit: int = 50) -> List[dict]:
        """
        列出音频文件
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[dict]: 音频文件列表
        """
        files = []
        for filepath in self.storage_dir.glob("radio_*.wav"):
            files.append({
                'filename': filepath.name,
                'size': filepath.stat().st_size,
                'created': datetime.fromtimestamp(filepath.stat().st_ctime).isoformat(),
                'path': str(filepath)
            })
        
        files.sort(key=lambda x: x['created'], reverse=True)
        return files[:limit]
    
    def delete(self, filename: str) -> bool:
        """
        删除音频文件
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 是否删除成功
        """
        filepath = self.storage_dir / filename
        if filepath.exists():
            filepath.unlink()
            metadata_file = filepath.with_suffix('.json')
            if metadata_file.exists():
                metadata_file.unlink()
            return True
        return False
    
    def cleanup(self, days: int = 30) -> int:
        """
        清理旧音频文件
        
        Args:
            days: 保留天数
            
        Returns:
            int: 删除的文件数量
        """
        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0
        
        for filepath in self.storage_dir.glob("radio_*.wav"):
            if datetime.fromtimestamp(filepath.stat().st_ctime) < cutoff:
                filepath.unlink()
                metadata_file = filepath.with_suffix('.json')
                if metadata_file.exists():
                    metadata_file.unlink()
                deleted += 1
        
        return deleted
    
    def get_info(self) -> dict:
        """
        获取音频管理器信息
        
        Returns:
            dict: 包含存储目录等信息
        """
        files = list(self.storage_dir.glob("radio_*.wav"))
        total_size = sum(f.stat().st_size for f in files)
        
        return {
            'storage_dir': str(self.storage_dir),
            'file_count': len(files),
            'total_size_mb': round(total_size / 1024 / 1024, 2)
        }

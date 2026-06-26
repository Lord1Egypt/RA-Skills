import requests
import os
from typing import List, Dict, Optional

class SubtitleClient:
    """OpenSubtitles API 客户端"""
    
    BASE_URL = "https://api.opensubtitles.com/api/v1"
    
    def __init__(self):
        self.token = None
        self.api_key = os.getenv("OPENSUBTITLES_API_KEY")
        self.username = os.getenv("OPENSUBTITLES_USERNAME")
        self.password = os.getenv("OPENSUBTITLES_PASSWORD")
        
    def login(self) -> str:
        """登录并获取 token"""
        url = f"{self.BASE_URL}/login"
        headers = {
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        data = {
            "username": self.username,
            "password": self.password
        }
        
        r = requests.post(url, json=data, headers=headers, timeout=30)
        r.raise_for_status()
        
        self.token = r.json()['token']
        return self.token
    
    def search(self, query: str, year: Optional[int] = None, 
               language: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """搜索字幕"""
        if not self.token:
            self.login()
            
        params = {"query": query}
        if year:
            params["year"] = year
        if language:
            params["languages"] = language
            
        headers = {
            'Api-Key': self.api_key,
            'Authorization': f'Bearer {self.token}'
        }
        
        url = f"{self.BASE_URL}/subtitles"
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        
        results = []
        for item in r.json().get('data', [])[:limit]:
            attrs = item.get('attributes', {})
            results.append({
                'id': attrs.get('subtitle_id'),
                'language': attrs.get('language'),
                'downloads': attrs.get('download_count'),
                'title': attrs.get('feature_details', {}).get('title'),
                'year': attrs.get('feature_details', {}).get('year'),
                'file_name': attrs.get('files', [{}])[0].get('file_name') if attrs.get('files') else None,
                'file_id': attrs.get('files', [{}])[0].get('file_id') if attrs.get('files') else None
            })
            
        return results
    
    def download(self, subtitle: Dict, save_path: str = None) -> str:
        """下载字幕文件"""
        if not self.token:
            self.login()
            
        file_id = subtitle.get('file_id')
        if not file_id:
            raise ValueError("No file_id in subtitle")
            
        url = f"{self.BASE_URL}/download"
        headers = {
            'Api-Key': self.api_key,
            'Authorization': f'Bearer {self.token}'
        }
        data = {"file_id": file_id}
        
        r = requests.post(url, json=data, headers=headers, timeout=60)
        r.raise_for_status()
        
        # 获取下载链接
        download_link = r.json().get('link')
        if not download_link:
            raise ValueError("No download link in response")
            
        # 下载实际文件
        r2 = requests.get(download_link, timeout=60)
        
        # 保存文件
        if save_path is None:
            save_path = subtitle.get('file_name', 'subtitle.srt')
            
        with open(save_path, 'wb') as f:
            f.write(r2.content)
            
        return save_path


if __name__ == "__main__":
    # 测试
    client = SubtitleClient()
    client.login()
    
    results = client.search("Artificial Intelligence", year=2001, language="en")
    print(f"Found {len(results)} subtitles")
    
    if results:
        path = client.download(results[0])
        print(f"Downloaded to: {path}")

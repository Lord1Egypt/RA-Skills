"""
GitHub Storage Backend
"""
import os
import base64
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import json
import hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory_system.storage.base import StorageBackend, MemoryEntry


class GitHubStorage(StorageBackend):
    def __init__(
        self,
        repo: str,
        branch: str = "main",
        token: str = None,
        base_path: str = "memory/",
        token_env: str = "GITHUB_TOKEN"
    ):
        """
        Args:
            repo: Repository in format "owner/repo"
            branch: Branch name
            token: GitHub token (or set via environment)
            base_path: Path in repo for memory files
            token_env: Environment variable name for token
        """
        self.repo = repo
        self.branch = branch
        self.base_path = base_path.rstrip('/') + '/'
        self.token = token or os.environ.get(token_env, "")
        self.token_env = token_env
        
        if not self.token:
            raise ValueError(f"GitHub token not found. Set {token_env} environment variable.")
        
        self.api_base = "https://api.github.com"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to GitHub API"""
        import urllib.request
        
        url = f"{self.api_base}{endpoint}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MemorySystem/1.0"
        }
        
        data = kwargs.get('data')
        if data:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            raise Exception(f"GitHub API error {e.code}: {error_body}")
    
    def init(self):
        """Verify repo access"""
        try:
            self._request("GET", f"/repos/{self.repo}")
        except Exception as e:
            raise Exception(f"Failed to access repository {self.repo}: {e}")
    
    def _get_file_path(self, entry_id: str) -> str:
        return f"{self.base_path}{entry_id}.json"
    
    def _get_file_sha(self, path: str) -> Optional[str]:
        """Get file SHA if exists"""
        try:
            result = self._request(
                "GET", 
                f"/repos/{self.repo}/contents/{path}?ref={self.branch}"
            )
            return result.get('sha')
        except Exception:
            return None
    
    def save(self, entry: MemoryEntry) -> bool:
        try:
            path = self._get_file_path(entry.id)
            content = json.dumps(entry.to_dict(), ensure_ascii=False, indent=2)
            sha = self._get_file_sha(path)
            
            data = {
                "message": f"Save memory: {entry.id}",
                "content": base64.b64encode(content.encode('utf-8')).decode('ascii'),
                "branch": self.branch
            }
            if sha:
                data["sha"] = sha
            
            self._request("PUT", f"/repos/{self.repo}/contents/{path}", data=data)
            return True
        except Exception as e:
            print(f"Error saving entry {entry.id}: {e}")
            return False
    
    def load(self, entry_id: str) -> Optional[MemoryEntry]:
        try:
            path = self._get_file_path(entry_id)
            result = self._request(
                "GET", 
                f"/repos/{self.repo}/contents/{path}?ref={self.branch}"
            )
            
            if 'content' in result:
                content = base64.b64decode(result['content']).decode('utf-8')
                return MemoryEntry.from_dict(json.loads(content))
            return None
        except Exception as e:
            print(f"Error loading entry {entry_id}: {e}")
            return None
    
    def delete(self, entry_id: str) -> bool:
        try:
            path = self._get_file_path(entry_id)
            sha = self._get_file_sha(path)
            
            if not sha:
                return False
            
            data = {
                "message": f"Delete memory: {entry_id}",
                "sha": sha,
                "branch": self.branch
            }
            
            self._request("DELETE", f"/repos/{self.repo}/contents/{path}", data=data)
            return True
        except Exception as e:
            print(f"Error deleting entry {entry_id}: {e}")
            return False
    
    def list_all(self) -> List[MemoryEntry]:
        entries = []
        try:
            result = self._request(
                "GET",
                f"/repos/{self.repo}/contents/{self.base_path}?ref={self.branch}"
            )
            
            if isinstance(result, list):
                for item in result:
                    if item['name'].endswith('.json'):
                        entry = self.load(item['name'].replace('.json', ''))
                        if entry:
                            entries.append(entry)
            
            entries.sort(key=lambda x: x.timestamp, reverse=True)
        except Exception as e:
            print(f"Error listing entries: {e}")
        
        return entries
    
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        all_entries = self.list_all()
        if not tags:
            return all_entries
        
        tag_set = set(t.lower() for t in tags)
        return [
            entry for entry in all_entries
            if tag_set.intersection(set(t.lower() for t in entry.tags))
        ]

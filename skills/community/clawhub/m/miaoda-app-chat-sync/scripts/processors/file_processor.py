#!/usr/bin/env python3
"""
File Processor

Handles file reading, filtering, and statistics for repository processing.
"""

import os
import fnmatch
from typing import Dict, List, Tuple, Optional

from core.constants import TEXT_EXTENSIONS, SKIP_DIRS, MAX_SINGLE_FILE_SIZE


class FileProcessor:
    """Handles file reading and processing"""
    
    def __init__(self, max_files: int = 50, file_filter: str = None, exclude_filter: str = None):
        self.max_files = max_files
        self.file_filter = self._parse_filter(file_filter) if file_filter else None
        self.exclude_filter = self._parse_filter(exclude_filter) if exclude_filter else None
    
    def _parse_filter(self, filter_str: str) -> List[str]:
        """Parse file filter string"""
        return [f.strip() for f in filter_str.split(',')]
    
    def _matches_filter(self, filepath: str) -> bool:
        """Check if file matches the include filter"""
        if not self.file_filter:
            return True
        
        for pattern in self.file_filter:
            if pattern.startswith('*.'):
                ext = '.' + pattern[2:]
                if filepath.endswith(ext):
                    return True
            elif '*' in pattern:
                if fnmatch.fnmatch(filepath, pattern):
                    return True
            else:
                if filepath == pattern:
                    return True
        return False
    
    def _matches_exclude(self, filepath: str) -> bool:
        """Check if file matches the exclude filter"""
        if not self.exclude_filter:
            return False
        
        for pattern in self.exclude_filter:
            if pattern.startswith('*.'):
                ext = '.' + pattern[2:]
                if filepath.endswith(ext):
                    return True
            elif '*' in pattern:
                if fnmatch.fnmatch(filepath, pattern):
                    return True
            else:
                if filepath == pattern:
                    return True
        return False
    
    def _should_include_file(self, filepath: str) -> bool:
        """Check if file should be included"""
        if not self._matches_filter(filepath):
            return False
        
        if self._matches_exclude(filepath):
            return False
        
        return True
    
    def read_files(self, directory: str) -> Dict[str, str]:
        """Read all text files from directory"""
        files_content = {}
        
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            
            for file in sorted(files):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, directory)
                
                if not self._should_include_file(relpath):
                    continue
                
                ext = os.path.splitext(file)[1].lower()
                if ext not in TEXT_EXTENSIONS:
                    continue
                
                try:
                    file_size = os.path.getsize(filepath)
                    if file_size > MAX_SINGLE_FILE_SIZE:
                        continue
                except:
                    continue
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        files_content[relpath] = f.read()
                        
                    if len(files_content) >= self.max_files:
                        break
                except:
                    continue
            
            if len(files_content) >= self.max_files:
                break
        
        return files_content
    
    def read_changed_files(self, directory: str, 
                           changed_files: List[Tuple[str, str]]) -> Dict[str, str]:
        """Read only the changed files from the repository"""
        files_content = {}
        
        for status, filepath in changed_files:
            if status == 'D':
                print(f"   ⏭️  Skipping deleted file: {filepath}")
                continue
            
            if not self._should_include_file(filepath):
                continue
            
            ext = os.path.splitext(filepath)[1].lower()
            if ext not in TEXT_EXTENSIONS:
                continue
            
            full_path = os.path.join(directory, filepath)
            if not os.path.exists(full_path):
                print(f"   ⚠️  File not found: {filepath}")
                continue
            
            try:
                file_size = os.path.getsize(full_path)
                if file_size > MAX_SINGLE_FILE_SIZE:
                    continue
            except:
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    files_content[filepath] = f.read()
                status_icon = {'A': '🆕', 'M': '📝', 'D': '🗑️', 'R': '🔄'}.get(status, '❓')
                print(f"   ✅ {status_icon} {filepath}")
            except Exception as e:
                print(f"   ⚠️  Error reading {filepath}: {str(e)}")
        
        return files_content
    
    def get_stats(self, files_content: Dict[str, str]) -> Dict:
        """Get file statistics"""
        total_size = sum(len(content.encode('utf-8')) for content in files_content.values())
        
        by_ext = {}
        for filepath in files_content.keys():
            ext = os.path.splitext(filepath)[1].lower()
            by_ext[ext] = by_ext.get(ext, 0) + 1
        
        return {
            'file_count': len(files_content),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'by_extension': by_ext
        }

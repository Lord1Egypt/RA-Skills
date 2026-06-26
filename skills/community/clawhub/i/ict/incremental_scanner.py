"""
增量扫描模块
只检测 git 改动的文件，提升扫描效率
"""
import os
import subprocess
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple


class IncrementalScanner:
    """增量扫描器"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.cache_dir = self.repo_path / ".ict_cache"
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_changed_files(self, staged: bool = False, staged_only: bool = False) -> List[str]:
        """获取 git 改动的文件列表"""
        try:
            # 获取 staged 文件
            if staged or staged_only:
                result = subprocess.run(
                    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            else:
                staged_files = []
            
            # 获取 unstaged 文件
            if not staged_only:
                result = subprocess.run(
                    ["git", "diff", "--name-only", "--diff-filter=ACM"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                unstaged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            else:
                unstaged_files = []
            
            # 合并去重
            all_files = list(set(staged_files + unstaged_files))
            return [f for f in all_files if f]  # 过滤空字符串
            
        except Exception as e:
            print(f"⚠️ git 命令失败: {e}")
            return []
    
    def get_new_files(self) -> List[str]:
        """获取新增文件（未跟踪的文件）"""
        try:
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return [f for f in files if f and self._is_code_file(f)]
        except Exception as e:
            print(f"⚠️ git ls-files 失败: {e}")
            return []
    
    def get_all_changed(self) -> Dict[str, List[str]]:
        """获取所有类型的改动"""
        return {
            "staged": self.get_changed_files(staged=True),
            "unstaged": self.get_changed_files(staged=False),
            "new": self.get_new_files()
        }
    
    def _is_code_file(self, filepath: str) -> bool:
        """判断是否为代码文件"""
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash',
            '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp',
            '.rb', '.php', '.cs', '.swift', '.kt'
        }
        ext = Path(filepath).suffix.lower()
        return ext in code_extensions
    
    def filter_code_files(self, files: List[str]) -> List[str]:
        """过滤出代码文件"""
        return [f for f in files if self._is_code_file(f)]
    
    def compute_file_hash(self, filepath: str) -> str:
        """计算文件内容的 MD5 哈希"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def load_cache(self) -> Dict[str, str]:
        """加载缓存"""
        cache_file = self.cache_dir / "file_hashes.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self, cache: Dict[str, str]):
        """保存缓存"""
        cache_file = self.cache_dir / "file_hashes.json"
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
    
    def get_files_to_scan(self, use_cache: bool = True) -> Tuple[List[str], Set[str]]:
        """
        获取需要扫描的文件
        返回: (需要扫描的文件列表, 跳过缓存的文件集合)
        """
        # 获取所有改动
        changed = self.get_all_changed()
        
        # 合并所有改动的文件
        all_changed = set(changed["staged"] + changed["unstaged"] + changed["new"])
        
        # 过滤代码文件
        changed_code_files = self.filter_code_files(list(all_changed))
        
        if not use_cache:
            return changed_code_files, set()
        
        # 加载缓存，对比哈希
        old_cache = self.load_cache()
        new_cache = {}
        files_to_scan = []
        skipped = set()
        
        for filepath in changed_code_files:
            file_hash = self.compute_file_hash(filepath)
            new_cache[filepath] = file_hash
            
            if filepath not in old_cache or old_cache[filepath] != file_hash:
                files_to_scan.append(filepath)
            else:
                skipped.add(filepath)
        
        # 更新缓存
        self.save_cache(new_cache)
        
        return files_to_scan, skipped
    
    def clear_cache(self):
        """清除缓存"""
        cache_file = self.cache_dir / "file_hashes.json"
        if cache_file.exists():
            cache_file.unlink()
        print("✓ 缓存已清除")


# 示例用法
if __name__ == "__main__":
    scanner = IncrementalScanner(".")
    
    print("=== Git 改动文件 ===")
    changed = scanner.get_all_changed()
    print(f"Staged: {changed['staged']}")
    print(f"Unstaged: {changed['unstaged']}")
    print(f"New: {changed['new']}")
    
    print("\n=== 需要扫描的文件 ===")
    to_scan, skipped = scanner.get_files_to_scan()
    print(f"需扫描: {to_scan}")
    print(f"跳过(缓存): {skipped}")

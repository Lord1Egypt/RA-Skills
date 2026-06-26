#!/usr/bin/env python3
"""
Git Repository Operations

Handles Git repository operations including cloning, authentication, 
branch detection, and commit management.
"""

import os
import subprocess
from typing import Dict, List, Optional, Tuple

from core.temp_manager import temp_directory
from core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError, with_retry
from core.security import SensitiveInfoHandler, SecureLogger
from core.prompts import PromptConfig


class RepoJSONGenerator:
    """Handles Git repository operations (GitHub, GitLab, etc.)
    
    Features:
    - Circuit breaker for resilient operations
    - Automatic retry with exponential backoff
    - Sensitive information protection
    - Cross-platform support
    
    Clone target directory is specified by caller.
    Caller is responsible for cleanup after use.
    """
    
    def __init__(self, token: str = None, verbose: bool = False):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.verbose = verbose
        self.logger = SecureLogger(verbose=verbose)
        
        # Initialize circuit breaker for git operations
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60
        )
    
    def _get_git_env(self) -> Dict[str, str]:
        """Get environment variables for git commands with authentication"""
        env = os.environ.copy()
        if self.token:
            env['GIT_ASKPASS'] = 'echo'
            env['GIT_TERMINAL_PROMPT'] = '0'
            # Don't expose token in environment for subprocess
        return env
    
    def _make_authenticated_url(self, repo_url: str) -> str:
        """Convert repo URL to use authentication if token is provided"""
        if not self.token or 'github.com' not in repo_url:
            return repo_url
        
        # Remove .git suffix for consistency
        repo_url = repo_url.rstrip('/')
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        if '@' in repo_url and '://' in repo_url:
            parts = repo_url.split('://')
            # Re-add token
            return f"{parts[0]}://x-access-token:{self.token}@{parts[1].split('@')[1]}"
        
        if repo_url.startswith('https://'):
            return repo_url.replace('https://', f'https://x-access-token:{self.token}@')
        elif repo_url.startswith('http://'):
            return repo_url.replace('http://', f'https://x-access-token:{self.token}@')
        return repo_url
    
    def _log_operation(self, operation: str, *args, **kwargs):
        """Log operation with sensitive data redacted."""
        if self.verbose:
            self.logger.debug(f"[Git] {operation}:", *args, **kwargs)
    
    @with_retry(max_attempts=3, base_delay=2.0, max_delay=30.0)
    def _execute_git_command(self, cmd: List[str], cwd: str, timeout: int = 60) -> subprocess.CompletedProcess:
        """
        Execute a git command with retry and circuit breaker protection.
        
        Args:
            cmd: Git command arguments
            cwd: Working directory
            timeout: Command timeout in seconds
            
        Returns:
            CompletedProcess result
        """
        if not self._circuit_breaker.allow_request():
            raise CircuitBreakerOpenError(
                "Git operations circuit breaker is OPEN. Too many recent failures."
            )
        
        try:
            env = self._get_git_env()
            self._log_operation("Executing:", ' '.join(cmd[:3]) + '...', f"cwd={cwd}")
            
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            
            if result.returncode == 0:
                self._circuit_breaker.record_success()
            else:
                self._circuit_breaker.record_failure()
                error_msg = SensitiveInfoHandler.redact(result.stderr)
                self._log_operation("Command failed:", error_msg)
            
            return result
            
        except subprocess.TimeoutExpired as e:
            self._circuit_breaker.record_failure()
            raise
        except Exception as e:
            self._circuit_breaker.record_failure()
            raise
    
    def clone_repo(self, repo_url: str, target_dir: str, branch: str = 'main', commit: str = None):
        """
        Clone repository and optionally checkout specific commit.
        Uses full history fetch to support any commit checkout.
        """
        try:
            auth_url = self._make_authenticated_url(repo_url)
            
            # Step 1: Initialize git repo
            subprocess.run(['git', 'init'], cwd=target_dir, capture_output=True, timeout=30)
            
            # Step 2: Configure git user (required for operations)
            subprocess.run(['git', 'config', 'user.email', 'sync@github.com'], 
                          cwd=target_dir, capture_output=True, timeout=10)
            subprocess.run(['git', 'config', 'user.name', 'GitHub Sync'], 
                          cwd=target_dir, capture_output=True, timeout=10)
            
            # Step 3: Add remote
            subprocess.run(['git', 'remote', 'add', 'origin', auth_url], 
                          cwd=target_dir, capture_output=True, timeout=30)
            
            # Step 4: Fetch
            if commit:
                # Fetch specific commit - need full history
                print(f"   📥 Fetching commit {commit[:8]}...")
                cmd = ['git', '-C', target_dir, 'fetch', '--tags', 'origin', commit]
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=180)
                if result.returncode != 0:
                    # Try as branch first
                    cmd = ['git', '-C', target_dir, 'fetch', 'origin', commit]
                    result = self._execute_git_command(cmd, cwd=target_dir, timeout=180)
                    if result.returncode != 0:
                        raise Exception(f"Failed to fetch commit {commit[:8]}")
                
                # Checkout the commit
                cmd = ['git', '-C', target_dir, 'checkout', commit]
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=60)
                if result.returncode != 0:
                    raise Exception(f"Failed to checkout commit {commit[:8]}")
                
                actual_commit = commit
            else:
                # Fetch branch
                print(f"   📥 Fetching branch {branch}...")
                cmd = ['git', '-C', target_dir, 'fetch', 'origin', branch]
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=180)
                if result.returncode != 0:
                    raise Exception(f"Failed to fetch branch {branch}")
                
                # Checkout
                cmd = ['git', '-C', target_dir, 'checkout', '-f', '-B', branch, 
                      f'origin/{branch}']
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=60)
                if result.returncode != 0:
                    raise Exception(f"Failed to checkout branch {branch}")
                
                # Get actual commit
                cmd = ['git', '-C', target_dir, 'rev-parse', 'HEAD']
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=10)
                actual_commit = result.stdout.strip() if result.returncode == 0 else None
            
            # Verify the commit
            if actual_commit:
                cmd = ['git', '-C', target_dir, 'cat-file', '-t', actual_commit]
                result = self._execute_git_command(cmd, cwd=target_dir, timeout=10)
                if result.returncode != 0:
                    raise Exception(f"Invalid commit hash: {actual_commit[:8]}")
            
            return actual_commit
            
        except CircuitBreakerOpenError:
            raise Exception(
                "Git operations temporarily unavailable due to too many failures. "
                "Please try again in a few minutes."
            )
        except subprocess.TimeoutExpired:
            raise Exception("Git operation timed out. Check network connection.")
        except Exception as e:
            raise Exception(f"Git operation failed: {SensitiveInfoHandler.safe_error_message(e)}")
    
    def _merge_consecutive_changes(self, changes: List[Dict]) -> List[Dict]:
        """
        Merge consecutive changes of the same type.
        
        Args:
            changes: List of change dictionaries
            
        Returns:
            Merged list of changes
        """
        if not changes:
            return []
        
        merged = []
        current = changes[0].copy()
        
        for i in range(1, len(changes)):
            next_change = changes[i]
            
            # Check if we can merge (same type and consecutive lines)
            if (current['type'] == next_change['type'] and 
                abs(current.get('line', 0) - next_change.get('line', 0)) <= 1):
                # Merge content
                current['content'] = current.get('content', '') + '\n' + next_change.get('content', '')
                current['line'] = max(current.get('line', 0), next_change.get('line', 0))
            else:
                merged.append(current)
                current = next_change.copy()
        
        merged.append(current)
        return merged

    def get_commit_diff_info(self, repo_url: str, commit: str, branch: str = 'main',
                             file_filter: str = None, exclude_filter: str = None) -> Dict:
        """
        Get detailed diff information for files changed in a specific commit.
        
        Args:
            repo_url: Git repository URL
            commit: Commit hash
            branch: Branch name
            file_filter: Comma-separated file patterns to include
            exclude_filter: Comma-separated file patterns to exclude
        
        Returns:
            Dict containing commit info and detailed file changes with line numbers
        """
        with temp_directory(prefix='github-info-') as temp_dir:
            # Clone and checkout the specific commit
            self.clone_repo(repo_url, temp_dir, branch=branch, commit=commit)
            
            # Get commit info
            format_str = '%H||%h||%s||%b||%an||%ae||%aI||%cn||%ce||%cI||%P'
            cmd = ['git', '-C', temp_dir, 'log', '-1', f'--format={format_str}', commit]
            result = self._execute_git_command(cmd, cwd=temp_dir, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"Failed to get commit info")
            
            lines = result.stdout.strip().split('||')
            if len(lines) < 11:
                raise Exception("Invalid git log output format")
            
            (commit_hash, short_hash, subject, body, 
             author_name, author_email, author_date,
             committer_name, committer_email, committer_date, 
             parents) = lines
            
            parent_list = parents.split() if parents else []
            
            # Get detailed diff with line numbers
            if parent_list:
                parent_commit = parent_list[0]
                cmd = ['git', '-C', temp_dir, 'diff', '--unified=0', parent_commit, commit]
            else:
                # Initial commit
                cmd = ['git', '-C', temp_dir, 'diff', '--unified=0', '--root', commit]
            
            result = self._execute_git_command(cmd, cwd=temp_dir, timeout=120)
            
            if result.returncode != 0:
                raise Exception("Failed to get diff")
            
            # Parse diff output
            import re
            files_dict = {}
            current_file = None
            new_line = 0
            old_line = 0
            
            for line in result.stdout.split('\n'):
                if line.startswith('diff --git'):
                    # Parse file path
                    parts = line.split(' b/')
                    if len(parts) == 2:
                        file_path = parts[1]
                        current_file = {
                            'path': file_path,
                            'status': 'modified',
                            'additions': 0,
                            'deletions': 0,
                            'changes': []
                        }
                        files_dict[file_path] = current_file
                    
                elif line.startswith('new file mode'):
                    if current_file:
                        current_file['status'] = 'added'
                        
                elif line.startswith('deleted file mode'):
                    if current_file:
                        current_file['status'] = 'deleted'
                        
                elif line.startswith('@@'):
                    # Parse hunk header: @@ -old_start,old_count +new_start,new_count @@
                    match = re.search(r'-(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))?', line)
                    if match:
                        old_line = int(match.group(1))
                        new_line = int(match.group(3))
                        
                elif line.startswith('+') and not line.startswith('+++') and current_file:
                    current_file['additions'] += 1
                    current_file['changes'].append({
                        'type': 'addition',
                        'line': new_line,
                        'content': line[1:]
                    })
                    new_line += 1
                    
                elif line.startswith('-') and not line.startswith('---') and current_file:
                    current_file['deletions'] += 1
                    current_file['changes'].append({
                        'type': 'deletion',
                        'line': old_line,
                        'content': line[1:]
                    })
                    old_line += 1
            
            # Merge consecutive changes
            files_list = []
            for file_path, file_info in files_dict.items():
                merged_changes = self._merge_consecutive_changes(file_info['changes'])
                file_info['changes'] = merged_changes
                files_list.append(file_info)
            
            print(f"   📄 Files changed in commit: {len(files_list)}")
            
            # Apply filters
            if file_filter or exclude_filter:
                from processors.file_processor import FileProcessor
                processor = FileProcessor(file_filter=file_filter, exclude_filter=exclude_filter)
                
                filtered_files = []
                for file_info in files_list:
                    if processor._should_include_file(file_info['path']):
                        filtered_files.append(file_info)
                    else:
                        print(f"   ⏭️  Filtered out: {file_info['path']}")
                files_list = filtered_files
                print(f"   📄 Files after filtering: {len(files_list)}")
            
            # Get prompt configuration
            prompt_config = PromptConfig.get_prompt('info')
            
            return {
                'action': prompt_config['action'],
                'description': prompt_config['description'],
                'source': {
                    'repository': SensitiveInfoHandler.redact_url(repo_url),
                    'branch': branch,
                    'commit': commit_hash
                },
                'summary': {
                    'files_changed': len(files_list),
                    'total_additions': sum(f['additions'] for f in files_list),
                    'total_deletions': sum(f['deletions'] for f in files_list),
                    'files': [
                        {
                            'path': f['path'],
                            'status': f['status'],
                            'additions': f['additions'],
                            'deletions': f['deletions']
                        }
                        for f in files_list
                    ]
                },
                'rules': prompt_config['rules'],
                'files': files_list
            }

    def get_commit_full_changes(self, repo_url: str, commit: str, branch: str = 'main', 
                                file_filter: str = None, exclude_filter: str = None,
                                command_type: str = 'sync') -> Dict:
        """
        Get full content of files changed in a specific commit.
        
        Args: 
            repo_url: Git repository URL
            commit: Commit hash
            branch: Branch name
            file_filter: Comma-separated file patterns to include
            exclude_filter: Comma-separated file patterns to exclude
            command_type: Command type ('sync' or 'info') for prompt configuration
        
        Returns:
            Dict containing action, description, source, rules, and files with full content
        """
        with temp_directory(prefix='github-sync-') as temp_dir:
            # Clone and checkout the specific commit
            self.clone_repo(repo_url, temp_dir, branch=branch, commit=commit)
            
            # Get commit info
            format_str = '%H||%h||%s||%b||%an||%ae||%aI||%cn||%ce||%cI||%P'
            cmd = ['git', '-C', temp_dir, 'log', '-1', f'--format={format_str}', commit]
            result = self._execute_git_command(cmd, cwd=temp_dir, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"Failed to get commit info")
            
            lines = result.stdout.strip().split('||')
            if len(lines) < 11:
                raise Exception("Invalid git log output format")
            
            (commit_hash, short_hash, subject, body, 
             author_name, author_email, author_date,
             committer_name, committer_email, committer_date, 
             parents) = lines
            
            parent_list = parents.split() if parents else []
            
            # Get changed files for this commit
            if parent_list:
                # Normal commit: diff against parent
                parent_commit = parent_list[0]
                cmd = ['git', '-C', temp_dir, 'diff', '--name-status', parent_commit, commit]
            else:
                # Initial commit: show all files as added
                cmd = ['git', '-C', temp_dir, 'diff', '--name-status', '--root', commit]
            
            result = self._execute_git_command(cmd, cwd=temp_dir, timeout=30)
            
            if result.returncode != 0:
                raise Exception("Failed to get changed files")
            
            # Parse changed files
            changed_files = []
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[0].strip()  # A (added), M (modified), D (deleted)
                    file_path = parts[1].strip()
                    changed_files.append((status, file_path))
            
            print(f"   📄 Files changed in commit: {len(changed_files)}")
            
            # Convert to file list and apply filters
            file_paths = [fp for status, fp in changed_files]
            
            if file_filter or exclude_filter:
                from processors.file_processor import FileProcessor
                processor = FileProcessor(file_filter=file_filter, exclude_filter=exclude_filter)
                
                filtered_files = []
                for file_path in file_paths:
                    if processor._should_include_file(file_path):
                        filtered_files.append(file_path)
                    else:
                        print(f"   ⏭️  Filtered out: {file_path}")
                file_paths = filtered_files
                print(f"   📄 Files after filtering: {len(file_paths)}")
            
            # Read full content of each changed file
            files_list = []
            skipped_binary = 0
            skipped_deleted = 0
            
            for file_path in file_paths:
                # Find the status for this file
                status = next((s for s, fp in changed_files if fp == file_path), 'M')
                
                # Skip deleted files
                if status == 'D':
                    skipped_deleted += 1
                    continue
                
                full_file_path = os.path.join(temp_dir, file_path)
                try:
                    if os.path.exists(full_file_path):
                        # Check if file is binary by reading first few bytes
                        with open(full_file_path, 'rb') as f:
                            header = f.read(8192)  # Read first 8KB
                        
                        # Check for null bytes (indicator of binary file)
                        if b'\x00' in header:
                            skipped_binary += 1
                            continue
                        
                        # Try to read as text
                        with open(full_file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        files_list.append({
                            'path': file_path,
                            'action': 'CREATE_OR_OVERWRITE',
                            'content': content
                        })
                    else:
                        print(f"   ⚠️  File not found: {file_path}")
                except UnicodeDecodeError:
                    skipped_binary += 1
                except Exception as e:
                    print(f"   ⚠️  Error reading {file_path}: {str(e)}")
            
            if skipped_binary > 0:
                print(f"   ⏭️  Skipped {skipped_binary} binary file(s)")
            if skipped_deleted > 0:
                print(f"   ⏭️  Skipped {skipped_deleted} deleted file(s)")
            
            # Get prompt configuration
            prompt_config = PromptConfig.get_prompt(command_type)
            
            return {
                'action': prompt_config['action'],
                'description': prompt_config['description'],
                'source': {
                    'repository': SensitiveInfoHandler.redact_url(repo_url),
                    'branch': branch,
                    'commit': commit_hash
                },
                'summary': {
                    'files_changed': len(files_list),
                    'total_files': len(files_list),
                    'files': [
                        {
                            'path': f['path'],
                            'action': 'CREATE_OR_OVERWRITE',
                            'size': len(f.get('content', ''))
                        }
                        for f in files_list
                    ]
                },
                'rules': prompt_config['rules'],
                'files': files_list
            }

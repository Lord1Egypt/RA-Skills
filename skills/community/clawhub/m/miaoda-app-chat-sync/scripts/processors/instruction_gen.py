#!/usr/bin/env python3
"""
Instruction Generator

Generates structured JSON instructions for code synchronization and updates.
"""

import json
import os
from typing import Dict
from datetime import datetime

from core.security import SensitiveInfoHandler


class InstructionGenerator:
    """Generates structured JSON instructions for code sync"""
    
    @staticmethod
    def generate(files_content: Dict[str, str], 
                 repo_url: str, branch: str, commit: str,
                 stats: Dict,
                 command_type: str = 'sync') -> str:
        """
        Generate JSON structured instruction for file sync
        
        Args:
            files_content: Dictionary of file paths and contents
            repo_url: Repository URL
            branch: Branch name
            commit: Commit hash
            stats: File statistics
            command_type: Command type ('sync' or 'info') for prompt configuration
        """
        priority_files = [
            'package.json', 'requirements.txt', 'pyproject.toml',
            'index.html', 'main.py', 'app.py'
        ]
        
        sorted_files = sorted(
            files_content.keys(),
            key=lambda x: (0 if x in priority_files else 1, x)
        )
        
        # Get prompt configuration
        prompt_config = PromptsConfig.get_prompt(command_type)
        
        instruction_data = {
            "action": prompt_config['action'],
            "description": prompt_config['description'],
            "source": {
                "repository": SensitiveInfoHandler.redact_url(repo_url),
                "branch": branch,
                "commit": commit[:8] if commit else 'N/A'
            },
            "rules": prompt_config['rules'],
            "files": []
        }
        
        for filepath in sorted_files:
            instruction_data["files"].append({
                "path": filepath,
                "action": "CREATE_OR_OVERWRITE",
                "content": files_content[filepath]
            })
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Build output without triple backticks in f-string
        json_output = json.dumps(instruction_data, ensure_ascii=False, indent=2)
        separator = '=' * 60
        
        output_parts = [
            "📦 Repo JSON Generator - Structured Update Instructions",
            separator,
            "",
            "📋 Summary:",
            f"  Repository: {SensitiveInfoHandler.redact_url(repo_url)}",
            f"  Branch: {branch}",
            f"  Commit: {commit[:8] if commit else 'N/A'}",
            f"  Files: {stats['file_count']}",
            f"  Total Size: {stats['total_size_mb']} MB",
            f"  Generated: {timestamp}",
            "",
            separator,
            "",
            "📝 Copy the following JSON and send to AI Agent:",
            "",
            f"{json_output}",
            separator
        ]
        
        return '\n'.join(output_parts)

    @staticmethod
    def generate_json_only(files_content: Dict[str, str],
                          repo_url: str, branch: str, commit: str) -> str:
        """Generate only JSON data without formatting"""
        sorted_files = sorted(files_content.keys())
        
        instruction_data = {
            "action": "CREATE_OR_UPDATE_FILES",
            "source": {
                "repository": SensitiveInfoHandler.redact_url(repo_url),
                "branch": branch,
                "commit": commit[:8] if commit else 'N/A'
            },
            "files": []
        }
        
        for filepath in sorted_files:
            instruction_data["files"].append({
                "path": filepath,
                "action": "CREATE_OR_OVERWRITE",
                "content": files_content[filepath]
            })
        
        return json.dumps(instruction_data, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_commit_full_changes(info_data: Dict) -> str:
        """Generate formatted output for commit full changes"""
        source = info_data.get('source', {})
        files = info_data.get('files', [])
        
        total_files = len(files)
        total_additions = sum(f.get('additions', 0) for f in files)
        total_deletions = sum(f.get('deletions', 0) for f in files)
        
        files_summary = []
        for file_info in files:
            status = file_info.get('status', 'modified')
            status_icon = {'added': '🆕 Added', 'deleted': '🗑️ Deleted', 'modified': '📝 Modified'}.get(status, '❓')
            additions = file_info.get('additions', 0)
            deletions = file_info.get('deletions', 0)
            stats_str = f"+{additions}/-{deletions}" if additions or deletions else ""
            files_summary.append(f"  {status_icon}: {file_info['path']} ({stats_str})")
        
        # Build output without triple backticks in f-string
        json_output = json.dumps(info_data, ensure_ascii=False, indent=2)
        separator = '=' * 60
        
        commit_short = source.get('commit', 'N/A')[:8] if source.get('commit') else 'N/A'
        
        output_parts = [
            "📋 Commit Full Changes",
            separator,
            "",
            f"🔗 Source: Repository: {source.get('repository', 'N/A')} Branch: {source.get('branch', 'N/A')} Commit: {commit_short}",
            "",
            f"📊 Statistics: Files Changed: {total_files} Total Additions: +{total_additions} Total Deletions: -{total_deletions}",
            "",
            f"📁 Changed Files ({total_files}):",
            '\n'.join(files_summary),
            "",
            separator,
            "",
            "📝 Copy the following JSON for complete changes:",
            "",
            f"{json_output}",
            separator
        ]
        
        return '\n'.join(output_parts)

    @staticmethod
    def generate_info_output(info_data: Dict) -> str:
        """Generate formatted commit info output"""
        commit = info_data['commit']
        
        is_merge = "✅ Yes (Merge Commit)" if commit['is_merge_commit'] else "❌ No"
        parents = ', '.join([p[:8] for p in commit['parent_commits']]) if commit['parent_commits'] else 'None'
        
        # Build output without triple backticks in f-string
        json_output = json.dumps(info_data, ensure_ascii=False, indent=2)
        separator = '=' * 60
        
        output_parts = [
            "ℹ️  Repository Commit Info",
            separator,
            "",
            f"📋 Repository:URL: {info_data['repository']} Branch: {info_data['branch']}",
            "",
            f"🔗 Commit: Hash: {commit['hash']} Short: {commit['short_hash']}",
            "",
            f"📝 Message: Subject: {commit['message']['subject']} Body: {commit['message']['body'] or '(none)'}",
            "",
            f"👤 Author: Name: {commit['author']['name']} Email: {commit['author']['email']} Date: {commit['author']['timestamp']}",
            "",
            f"👤 Committer: Name: {commit['committer']['name']} Email: {commit['committer']['email']} Date: {commit['committer']['timestamp']}",
            "",
            f"🔀 Merge Commit: {is_merge} 📜 Parents: {parents}",
            "",
            separator,
            "",
            "📝 Copy the following JSON for AI analysis:",
            "",
            f"{json_output}",
            separator,
            ""
        ]
        
        return '\n'.join(output_parts)

    @staticmethod
    def output_result(result: Dict, output_file: str = None, no_instructions: bool = False):
        """
        Output result to terminal and/or file
        
        Args:
            result: The result dictionary to output
            output_file: Optional file path to save output
            no_instructions: If True, save pure JSON only (for file output)
        """
        if output_file:
            # Save to file
            if no_instructions:
                # Save pure JSON only
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                # Save formatted output (summary + JSON)
                formatted = InstructionGenerator.generate_commit_full_changes(result)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted)
            
            print(f"\n💾 Output saved to: {output_file}")
        else:
            # Output to terminal only
            formatted = InstructionGenerator.generate_commit_full_changes(result)
            print(formatted)

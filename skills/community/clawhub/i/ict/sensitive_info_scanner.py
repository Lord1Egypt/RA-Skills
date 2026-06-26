"""
敏感信息检测增强模块
支持 .env, YAML, JSON 配置文件扫描，以及云凭证检测
"""
import re
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set


class SensitiveInfoScanner:
    """敏感信息扫描器"""
    
    # 云服务商凭证模式
    CLOUD_CREDENTIALS = {
        # AWS
        'aws_access_key': [
            r'AKIA[0-9A-Z]{16}',  # Access Key ID
            r'(?i)aws.*secret.*access.*key',
            r'(?i)aws_session_token',
        ],
        'aws_secret_key': [
            r'(?i)aws_secret_key\s*=\s*["\'][A-Za-z0-9/+=]{40}["\']',
        ],
        
        # Azure
        'azure': [
            r'(?i)azure.*client.*secret',
            r'(?i)azure.*storage.*key',
            r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}',  # Azure Client ID
            r'["\'][a-fA-Z0-9+/]{86}==["\']',  # Azure Secret
        ],
        
        # GCP (Google Cloud)
        'gcp': [
            r'(?i)gcp.*service.*account',
            r'(?i)google.*api.*key',
            r'["\'][a-z0-9-]{39}\.iam\.gserviceaccount\.com["\']',
            r'AIza[0-9A-Za-z\\-_]{35}',
        ],
        
        # GitHub
        'github': [
            r'ghp_[a-zA-Z0-9]{36}',
            r'github_pat_[a-zA-Z0-9_]{22,}',
            r'(?i)github.*token',
        ],
        
        # Slack
        'slack': [
            r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*',
            r'(?i)slack.*webhook',
        ],
        
        # Stripe
        'stripe': [
            r'sk_live_[0-9a-zA-Z]{24}',
            r'pk_live_[0-9a-zA-Z]{24}',
            r'sk_test_[0-9a-zA-Z]{24}',
            r'rk_live_[a-zA-Z0-9]{24,}',
        ],
        
        # Twilio
        'twilio': [
            r'SK[a-f0-9]{32}',
            r'AC[a-f0-9]{32}',
        ],
        
        # OpenAI / Anthropic
        'ai_api': [
            r'sk-[a-zA-Z0-9]{20,}',
            r'anthropic-ai.*sk-ant[a-zA-Z0-9-]{20,}',
            r'xAI-[a-zA-Z0-9]{20,}',
        ],
        
        # JWT
        'jwt': [
            r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
        ],
        
        # Private Key
        'private_key': [
            r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
            r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
        ],
    }
    
    # 配置文件敏感字段
    SENSITIVE_FIELDS = {
        'env': {
            'password', 'secret', 'key', 'token', 'api_key', 'apikey',
            'access_key', 'secret_key', 'client_secret', 'private_key',
            'credential', 'auth', 'authorization',
        },
        'yaml': {
            'password', 'secret', 'key', 'token', 'api_key', 'apikey',
            'access_key', 'secret_key', 'private_key', 'credential',
            'aws_access_key_id', 'aws_secret_access_key',
            'google_api_key', 'github_token', 'slack_token',
        },
        'json': {
            'password', 'secret', 'key', 'token', 'api_key', 'apikey',
            'access_key', 'secret_key', 'private_key', 'credential',
            'service_account', 'access_token', 'refresh_token',
        },
    }
    
    # 误报白名单
    WHITELIST_VALUES = {
        'your_password_here', 'your_api_key_here', 'your_secret_here',
        'example', 'test', 'placeholder', 'xxx', 'xxxx', '123456',
        'changeme', 'replace_me', 'update_me', 'your_key_here',
        'localhost', '127.0.0.1', '0.0.0.0',
    }
    
    def __init__(self):
        self.findings: List[Dict] = []
    
    def scan_file(self, filepath: str) -> List[Dict]:
        """扫描单个文件"""
        self.findings = []
        path = Path(filepath)
        
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"读取文件失败 {filepath}: {e}")
            return []
        
        suffix = path.suffix.lower()
        
        if suffix == '.env':
            self._scan_env(content, filepath)
        elif suffix in ['.yaml', '.yml']:
            self._scan_yaml(content, filepath)
        elif suffix == '.json':
            self._scan_json(content, filepath)
        else:
            # 对所有文件扫描云凭证
            self._scan_cloud_credentials(content, filepath)
        
        return self.findings
    
    def _scan_env(self, content: str, filepath: str):
        """扫描 .env 文件"""
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY=VALUE
            match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', line)
            if not match:
                continue
            
            key, value = match.groups()
            key_lower = key.lower()
            
            # 检查是否为敏感字段
            is_sensitive = any(s in key_lower for s in self.SENSITIVE_FIELDS['env'])
            
            # 检查值是否为白名单
            value_clean = value.strip().strip('"\'')
            if value_clean.lower() in self.WHITELIST_VALUES:
                continue
            
            # 检查是否为云凭证
            for provider, patterns in self.CLOUD_CREDENTIALS.items():
                for pattern in patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        self.findings.append({
                            'file': filepath,
                            'line': line_num,
                            'key': key,
                            'type': f'cloud_credential:{provider}',
                            'severity': 'critical',
                            'snippet': line[:100]
                        })
                        break
                else:
                    continue
                break
            else:
                if is_sensitive:
                    self.findings.append({
                        'file': filepath,
                        'line': line_num,
                        'key': key,
                        'type': 'sensitive_field',
                        'severity': 'high',
                        'snippet': line[:100]
                    })
    
    def _scan_yaml(self, content: str, filepath: str):
        """扫描 YAML 文件"""
        import yaml
        try:
            data = yaml.safe_load(content)
        except:
            # 如果解析失败，回退到正则扫描
            self._scan_cloud_credentials(content, filepath)
            return
        
        self._scan_dict_recursive(data, filepath, 'yaml')
    
    def _scan_json(self, content: str, filepath: str):
        """扫描 JSON 文件"""
        try:
            data = json.loads(content)
        except:
            self._scan_cloud_credentials(content, filepath)
            return
        
        self._scan_dict_recursive(data, filepath, 'json')
    
    def _scan_dict_recursive(self, data, filepath: str, config_type: str, path: str = ''):
        """递归扫描字典"""
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                key_lower = key.lower()
                
                # 检查是否为敏感字段
                is_sensitive = any(s in key_lower for s in self.SENSITIVE_FIELDS.get(config_type, []))
                
                if isinstance(value, str):
                    value_clean = value.strip()
                    
                    # 检查白名单
                    if value_clean.lower() in self.WHITELIST_VALUES:
                        continue
                    
                    # 检查云凭证
                    for provider, patterns in self.CLOUD_CREDENTIALS.items():
                        for pattern in patterns:
                            if re.search(pattern, value):
                                self.findings.append({
                                    'file': filepath,
                                    'path': current_path,
                                    'type': f'cloud_credential:{provider}',
                                    'severity': 'critical',
                                    'snippet': value[:80]
                                })
                                break
                    else:
                        if is_sensitive:
                            self.findings.append({
                                'file': filepath,
                                'path': current_path,
                                'type': 'sensitive_field',
                                'severity': 'high',
                                'snippet': value[:80]
                            })
                elif isinstance(value, (dict, list)):
                    self._scan_dict_recursive(value, filepath, config_type, current_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._scan_dict_recursive(item, filepath, config_type, f"{path}[{i}]")
    
    def _scan_cloud_credentials(self, content: str, filepath: str):
        """扫描云凭证 (通用)"""
        for line_num, line in enumerate(content.split('\n'), 1):
            for provider, patterns in self.CLOUD_CREDENTIALS.items():
                for pattern in patterns:
                    if re.search(pattern, line):
                        self.findings.append({
                            'file': filepath,
                            'line': line_num,
                            'type': f'cloud_credential:{provider}',
                            'severity': 'critical',
                            'snippet': line[:100]
                        })
                        break
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[Dict]:
        """扫描目录下所有匹配的文件"""
        if extensions is None:
            extensions = ['.env', '.yaml', '.yml', '.json', '.conf', '.config', '.ini']
        
        findings = []
        path = Path(directory)
        
        for ext in extensions:
            for file in path.rglob(f'*{ext}'):
                # 跳过 node_modules 等
                if 'node_modules' in str(file) or '__pycache__' in str(file):
                    continue
                findings.extend(self.scan_file(str(file)))
        
        return findings
    
    def generate_report(self) -> str:
        """生成报告"""
        lines = []
        lines.append("=" * 50)
        lines.append("敏感信息扫描报告")
        lines.append("=" * 50)
        
        if not self.findings:
            lines.append("\n✓ 未发现敏感信息")
            return "\n".join(lines)
        
        # 按严重程度分组
        critical = [f for f in self.findings if f['severity'] == 'critical']
        high = [f for f in self.findings if f['severity'] == 'high']
        
        lines.append(f"\n发现 {len(self.findings)} 个敏感信息:")
        lines.append(f"  - Critical: {len(critical)}")
        lines.append(f"  - High: {len(high)}")
        
        for f in self.findings[:20]:  # 限制显示数量
            lines.append(f"\n[{f['severity'].upper()}] {f['file']}")
            if 'line' in f:
                lines.append(f"  Line {f['line']}: {f['snippet']}")
            elif 'path' in f:
                lines.append(f"  Path: {f['path']}")
            lines.append(f"  Type: {f['type']}")
        
        return "\n".join(lines)


# 示例用法
if __name__ == "__main__":
    scanner = SensitiveInfoScanner()
    
    # 测试 .env 文件
    test_env = """
# Database
DB_HOST=localhost
DB_PASSWORD=secret123
DB_USER=admin

# AWS Credentials
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# API Keys
OPENAI_API_KEY=sk-1234567890abcdefghijklmnop
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Whitelist (should be ignored)
EXAMPLE_API_KEY=your_api_key_here
"""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(test_env)
        f.flush()
        findings = scanner.scan_file(f.name)
    
    print(f"发现 {len(findings)} 个敏感信息:")
    for f in findings:
        print(f"  - {f['type']}: {f['snippet'][:50]}...")

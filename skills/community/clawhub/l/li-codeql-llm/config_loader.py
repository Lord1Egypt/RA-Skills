#!/usr/bin/env python3
"""
环境配置加载模块
Environment Configuration Loader

加载 .env 文件并提供配置访问
Load .env file and provide configuration access
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """配置管理类 / Configuration Manager"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        初始化配置 / Initialize configuration
        
        Args:
            env_file: .env 文件路径，默认当前目录的 .env
        """
        self.env_file = env_file or '.env'
        self.config = {}
        self.load()
    
    def load(self) -> bool:
        """
        加载 .env 文件 / Load .env file
        
        Returns:
            bool: 是否成功加载
        """
        env_path = Path(self.env_file)
        
        # 尝试不同位置的 .env 文件
        possible_paths = [
            env_path,
            Path.home() / '.openclaw' / 'workspace' / 'skills' / 'codeql-llm-scanner' / '.env',
            Path(__file__).parent / '.env',
            Path.cwd() / '.env',
        ]
        
        for path in possible_paths:
            if path.exists():
                self._parse_env_file(path)
                print(f"✅ 已加载配置 / Configuration loaded: {path}")
                return True
        
        print("⚠️  未找到 .env 文件，使用默认配置")
        print("⚠️  .env file not found, using default configuration")
        print(f"💡 提示 / Tip: 复制配置模板 / Copy template:")
        print(f"   cp {Path(__file__).parent}/.env.example .env")
        return False
    
    def _parse_env_file(self, path: Path):
        """解析 .env 文件 / Parse .env file"""
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                
                # 解析 KEY=VALUE
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    
                    # 移除引号
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    self.config[key] = value
    
    def get(self, key: str, default: str = '') -> str:
        """
        获取配置值 / Get configuration value
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            str: 配置值
        """
        return self.config.get(key, default)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        获取布尔配置值 / Get boolean configuration value
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            bool: 配置值
        """
        value = self.config.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        获取整数配置值 / Get integer configuration value
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            int: 配置值
        """
        try:
            return int(self.config.get(key, str(default)))
        except ValueError:
            return default
    
    def get_list(self, key: str, default: list = None) -> list:
        """
        获取列表配置值（逗号分隔） / Get list configuration value (comma-separated)
        
        Args:
            key: 配置键
            default: 默认值
        
        Returns:
            list: 配置值列表
        """
        value = self.config.get(key, '')
        if not value:
            return default or []
        return [item.strip() for item in value.split(',')]
    
    def set(self, key: str, value: str):
        """设置配置值 / Set configuration value"""
        self.config[key] = value
    
    def save(self, path: Optional[str] = None):
        """保存配置到文件 / Save configuration to file"""
        save_path = Path(path) if path else Path(self.env_file)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("# CodeQL + LLM Scanner Configuration\n")
            f.write("# Generated automatically\n\n")
            
            for key, value in sorted(self.config.items()):
                f.write(f"{key}={value}\n")
    
    def validate(self) -> tuple:
        """
        验证配置 / Validate configuration
        
        Returns:
            tuple: (是否有效，错误信息列表)
        """
        errors = []
        
        # 验证 CodeQL 路径
        codeql_path = self.get('CODEQL_PATH', '/opt/codeql/codeql')
        if not Path(codeql_path).exists():
            # 尝试在 PATH 中查找
            import shutil
            if not shutil.which('codeql'):
                errors.append(f"CodeQL not found at {codeql_path} or in PATH")
        
        # 验证 Jenkins 配置（如果启用）
        if self.get_bool('JENKINS_UPLOAD_SARIF'):
            if not self.get('JENKINS_URL'):
                errors.append("JENKINS_URL is required when JENKINS_UPLOAD_SARIF is enabled")
            if not self.get('JENKINS_TOKEN'):
                errors.append("JENKINS_TOKEN is required when JENKINS_UPLOAD_SARIF is enabled")
        
        return (len(errors) == 0, errors)
    
    def print_summary(self):
        """打印配置摘要 / Print configuration summary"""
        print("\n" + "=" * 60)
        print("  配置摘要 / Configuration Summary")
        print("=" * 60)
        
        print(f"\n📦 CodeQL 配置:")
        print(f"   路径 / Path: {self.get('CODEQL_PATH', '/opt/codeql/codeql')}")
        print(f"   语言 / Language: {self.get('CODEQL_LANGUAGE', 'python')}")
        print(f"   套件 / Suite: {self.get('CODEQL_SUITE', 'python-security-extended.qls')}")
        
        print(f"\n📁 输出配置:")
        print(f"   目录 / Directory: {self.get('OUTPUT_DIR', './codeql-scan-output')}")
        print(f"   SARIF: {self.get_bool('GENERATE_SARIF', True)}")
        print(f"   Markdown: {self.get_bool('GENERATE_MARKDOWN', True)}")
        print(f"   Checklist: {self.get_bool('GENERATE_CHECKLIST', True)}")
        
        print(f"\n🤖 LLM 配置:")
        print(f"   自动分析 / Auto-analyze: {self.get_bool('LLM_AUTO_ANALYZE', False)}")
        print(f"   模式 / Mode: {self.get('LLM_ANALYSIS_MODE', 'detailed')}")
        
        print(f"\n🏢 Jenkins 配置:")
        print(f"   URL: {self.get('JENKINS_URL', 'http://localhost:8080')}")
        print(f"   任务 / Job: {self.get('JENKINS_JOB_NAME', 'codeql-security-scan')}")
        print(f"   上传 SARIF: {self.get_bool('JENKINS_UPLOAD_SARIF', True)}")
        
        print(f"\n🔒 安全配置:")
        print(f"   排除目录 / Excluded: {self.get('EXCLUDE_DIRS', '.git,credentials,.env')}")
        print(f"   扫描前检查 / Pre-scan check: {self.get_bool('SECURITY_CHECK_BEFORE_SCAN', True)}")
        
        print("\n" + "=" * 60)


# 全局配置实例 / Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """获取全局配置实例 / Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config(env_file: Optional[str] = None) -> Config:
    """重新加载配置 / Reload configuration"""
    global _config
    _config = Config(env_file)
    return _config


# 便捷函数 / Convenience functions
def get(key: str, default: str = '') -> str:
    return get_config().get(key, default)

def get_bool(key: str, default: bool = False) -> bool:
    return get_config().get_bool(key, default)

def get_int(key: str, default: int = 0) -> int:
    return get_config().get_int(key, default)

def get_list(key: str, default: list = None) -> list:
    return get_config().get_list(key, default)


if __name__ == '__main__':
    # 测试配置加载 / Test configuration loading
    config = Config()
    config.print_summary()
    
    print("\n验证配置 / Validating configuration...")
    valid, errors = config.validate()
    
    if valid:
        print("✅ 配置验证通过 / Configuration validation passed")
    else:
        print("❌ 配置验证失败 / Configuration validation failed")
        for error in errors:
            print(f"   - {error}")

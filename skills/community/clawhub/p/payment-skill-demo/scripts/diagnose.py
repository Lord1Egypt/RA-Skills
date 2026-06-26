#!/usr/bin/env python3
"""
支付 Skill 环境诊断工具

用于诊断 Python 3.6 环境中的依赖问题。
"""

import sys
import subprocess
import importlib
from pathlib import Path


def print_header(text):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_success(text):
    """打印成功信息"""
    print(f"✅ {text}")


def print_error(text):
    """打印错误信息"""
    print(f"❌ {text}")


def print_warning(text):
    """打印警告信息"""
    print(f"⚠️  {text}")


def print_info(text):
    """打印信息"""
    print(f"ℹ️  {text}")


def check_python_version():
    """检查 Python 版本"""
    print_header("Python 版本检查")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python 版本: {version_str}")
    print(f"Python 路径: {sys.executable}")
    
    if version.major == 3 and version.minor == 6:
        print_warning("Python 3.6 已停止支持，建议升级到 Python 3.8+")
        return True
    elif version.major == 3 and version.minor >= 8:
        print_success("Python 版本支持良好")
        return True
    else:
        print_error(f"不支持的 Python 版本: {version_str}")
        return False


def check_pip_version():
    """检查 pip 版本"""
    print_header("pip 版本检查")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        pip_version = result.stdout.strip()
        print(f"pip 版本: {pip_version}")
        
        # 提取版本号
        if "pip" in pip_version:
            print_success("pip 已安装")
            return True
    except Exception as e:
        print_error(f"无法检查 pip 版本: {e}")
        return False


def check_dependencies():
    """检查依赖"""
    print_header("依赖检查")
    
    dependencies = {
        "aiohttp": "异步 HTTP 客户端",
        "pydantic": "数据验证",
        "pyyaml": "YAML 配置",
        "python-dotenv": "环境变量管理",
        "cryptography": "加密库",
        "Crypto": "加密库 (pycryptodome)",
        "pytest": "测试框架",
        "pytest_asyncio": "异步测试支持",
        "redis": "缓存库",
    }
    
    installed = {}
    missing = []
    
    for module_name, description in dependencies.items():
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "unknown")
            installed[module_name] = version
            print_success(f"{module_name} ({description}): {version}")
        except ImportError:
            missing.append((module_name, description))
            print_error(f"{module_name} ({description}): 未安装")
    
    return len(missing) == 0, missing


def check_asyncmock():
    """检查 AsyncMock 兼容性"""
    print_header("AsyncMock 兼容性检查")
    
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        try:
            from unittest.mock import AsyncMock
            print_success("AsyncMock 原生支持 (Python 3.8+)")
            return True
        except ImportError:
            print_error("AsyncMock 导入失败")
            return False
    else:
        print_info("Python 3.6/3.7 使用兼容实现")
        try:
            from unittest.mock import Mock
            
            # 测试兼容实现
            class AsyncMock(Mock):
                async def __call__(self, *args, **kwargs):
                    return super(AsyncMock, self).__call__(*args, **kwargs)
            
            print_success("AsyncMock 兼容实现可用")
            return True
        except Exception as e:
            print_error(f"AsyncMock 兼容实现失败: {e}")
            return False


def check_project_structure():
    """检查项目结构"""
    print_header("项目结构检查")
    
    # 获取脚本目录和项目目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    required_files = [
        "src/payment_skill.py",
        "src/payment_api_client.py",
        "src/security.py",
        "src/utils.py",
        "tests/test_payment_skill.py",
        "tests/test_integration.py",
        "scripts/requirements-py36.txt",
        "scripts/payment_skill.yaml",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_dir / file_path
        if full_path.exists():
            print_success(f"✓ {file_path}")
        else:
            print_error(f"✗ {file_path} (缺失)")
            all_exist = False
    
    return all_exist


def check_requirements_file():
    """检查 requirements 文件"""
    print_header("Requirements 文件检查")
    
    # 获取脚本目录和项目目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    py36_req = project_dir / "scripts" / "requirements-py36.txt"
    std_req = project_dir / "scripts" / "requirements.txt"
    
    if py36_req.exists():
        print_success(f"✓ requirements-py36.txt 存在")
        print_info("Python 3.6 环境应使用此文件")
    else:
        print_error("✗ requirements-py36.txt 缺失")
    
    if std_req.exists():
        print_success(f"✓ requirements.txt 存在")
        print_info("Python 3.8+ 环境应使用此文件")
    else:
        print_error("✗ requirements.txt 缺失")


def check_environment_variables():
    """检查环境变量"""
    print_header("环境变量检查")
    
    import os
    
    env_vars = [
        "PAYMENT_API_KEY",
        "PAYMENT_API_SECRET",
        "PAYMENT_API_URL",
        "PAYMENT_LOG_LEVEL",
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # 隐藏敏感信息
            if "SECRET" in var or "KEY" in var:
                display_value = f"{value[:4]}...{value[-4:]}"
            else:
                display_value = value
            print_success(f"{var}: {display_value}")
        else:
            print_warning(f"{var}: 未设置")


def run_diagnostics():
    """运行所有诊断"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  支付 Skill 环境诊断工具".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        "Python 版本": check_python_version(),
        "pip 版本": check_pip_version(),
        "AsyncMock 兼容性": check_asyncmock(),
        "项目结构": check_project_structure(),
    }
    
    check_dependencies()
    check_requirements_file()
    check_environment_variables()
    
    # 总结
    print_header("诊断总结")
    
    all_passed = all(results.values())
    
    if all_passed:
        print_success("所有检查通过！")
        print_info("您可以运行: python3 -m pytest tests/ -v")
    else:
        print_error("发现问题，请参考上面的错误信息")
        print_info("查看 PYTHON36_SETUP.md 获取详细解决方案")
    
    print("\n")


if __name__ == "__main__":
    run_diagnostics()

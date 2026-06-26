"""
智能数据采集器 - OpenClaw技能安装包
"""

from setuptools import setup, find_packages
import pathlib

# 读取README
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# 读取版本信息
version_info = {}
with open(here / "src" / "data_harvester" / "__init__.py", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version_info["__version__"] = line.split("=")[1].strip().strip('"\'')
            break

setup(
    # 基本信息
    name="openclaw-data-harvester",
    version=version_info.get("__version__", "1.0.0"),
    description="智能数据采集器 - OpenClaw生态系统赚钱工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dxg852621787/openclaw-wealth-guide",
    
    # 作者信息
    author="dxg",
    author_email="852621787@qq.com",
    
    # 分类信息
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    
    # 关键词
    keywords="openclaw, data, collection, harvesting, web-scraping, api, automation",
    
    # 包配置
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12, <4",
    
    # 依赖
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "APScheduler>=3.10.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "cryptography>=42.0.0",
        "SQLAlchemy>=2.0.0",
        "python-dateutil>=2.8.0",
        "tzlocal>=5.0.0",
        "pytz>=2023.0",
    ],
    
    # 额外依赖
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
        ],
        "openclaw": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
        ]
    },
    
    # 入口点
    entry_points={
        "console_scripts": [
            "data-harvester=data_harvester.cli:main",
        ],
    },
    
    # 数据文件
    package_data={
        "data_harvester": [
            "py.typed",
            "config/examples/*.yaml",
            "config/examples/*.json",
        ],
    },
    
    # 项目URL
    project_urls={
        "Bug Reports": "https://github.com/dxg852621787/openclaw-wealth-guide/issues",
        "Source": "https://github.com/dxg852621787/openclaw-wealth-guide",
        "Documentation": "https://github.com/dxg852621787/openclaw-wealth-guide/blob/main/README.md",
        "OpenClaw Marketplace": "https://openclaw.ai/marketplace",
    },
)
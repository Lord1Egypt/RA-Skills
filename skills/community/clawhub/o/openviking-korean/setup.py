from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # Package name for PyPI / PyPI 패키지명
    name="tokensaver",
    
    version="3.1.0",
    author="Roken (김명진)",
    author_email="support@tokensaver.pro",
    
    # Bilingual description / 영한 병기 설명
    description="TokenSaver (토큰세이버) - 96% AI Cost Reduction for Korean NLP / 한국어 AI 비용 96% 절약",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/dorongs/tokensaver",
    packages=find_packages(),
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Korean",  # Korean language support
        "Operating System :: OS Independent",
    ],
    
    python_requires=">=3.8",
    install_requires=[
        "pathlib>=1.0.0",
    ],
    
    extras_require={
        "speed": ["orjson>=3.8.0", "aiofiles>=22.0.0"],
        "korean": ["konlpy>=0.6.0", "JPype1>=1.4.0"],
        "vector": ["sentence-transformers>=2.2.0", "numpy>=1.21.0"],
        "dev": ["pytest>=7.0.0", "pytest-asyncio>=0.20.0", "mypy>=1.0.0", "black>=22.0.0"],
    },
    
    # Keywords for search / 검색 키워드 (영한)
    keywords=(
        "AI, token-saving, korean, nlp, compression, context-db, "
        "async, orjson, korean-nlp, korean-tokenizer, "
        "비용절약, 토큰절약, 한국어, 자연어처리, 압축"
    ),
    
    project_urls={
        "Bug Reports": "https://github.com/dorongs/tokensaver/issues",
        "Source": "https://github.com/dorongs/tokensaver",
        "ClawHub": "https://clawhub.com/skills/tokensaver",
        "Documentation": "https://github.com/dorongs/tokensaver/blob/main/docs/API_REFERENCE.md",
    },
    
    # Entry points for CLI / CLI 진입점
    entry_points={
        "console_scripts": [
            "tokensaver=openviking_korean.cli:main",
            "토큰세이버=openviking_korean.cli:main",
        ],
    },
)
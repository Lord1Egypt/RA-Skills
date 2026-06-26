"""
廖工AI设计实战 · LiaoGong-OCR
pip 安装配置

Author: 廖工AI设计实战 (github.com/jnbno1163)
License: MIT
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="liaogong-ocr",
    version="1.0.0",
    author="廖工AI设计实战",
    author_email="jnbno1@163.com",
    description="双引擎OCR系统：easyocr + tesseract，15条预处理链，87%手机拍屏数字识别准确率",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jnbno1163/liaogong-ocr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="OCR, easyocr, tesseract, Chinese OCR, 中文OCR, 图片转文字, 双引擎",
    python_requires=">=3.8",
    install_requires=[
        "easyocr>=1.7.0",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "liaogong-ocr=liaogong_ocr.engine:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/jnbno1163/liaogong-ocr/issues",
        "Source": "https://github.com/jnbno1163/liaogong-ocr",
        "Homepage": "https://github.com/jnbno1163/liaogong-ocr",
    },
)

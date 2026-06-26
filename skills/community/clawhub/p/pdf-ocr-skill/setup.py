"""
PDF OCR Skill Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-ocr-skill",
    version="2.1.0",
    author="PDF OCR Skill Team",
    author_email="",
    description="PDF OCR Skill - 支持RapidOCR本地引擎和硅基流动大模型的双引擎OCR识别",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yejinlei/pdf-ocr-skill",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="ocr pdf image recognition siliconflow rapidocr local-ocr chinese english",
    project_urls={
        "Bug Reports": "https://github.com/yejinlei/pdf-ocr-skill/issues",
        "Source": "https://github.com/yejinlei/pdf-ocr-skill",
    },
)

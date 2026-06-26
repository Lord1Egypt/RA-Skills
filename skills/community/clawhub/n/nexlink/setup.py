#!/usr/bin/env python3
"""
NextLink - Exchange and Nextcloud assistant for Romanian SMEs.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nextlink",
    version="0.15.3",
    author="OpenClaw Community",
    author_email="community@openclaw.ai",
    description="Exchange and Nextcloud assistant for Romanian SMEs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asistent-alex/openclaw-nextlink",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "exchangelib>=5.0.0",
        "requests_ntlm>=1.1.0",
        "pdfplumber>=0.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
    scripts=[
        "scripts/nextlink.py",
    ],
)
#!/usr/bin/env python3
"""
Setup script for LobsterAI Security Skill
"""

from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt if it exists
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="lobsterai-security-skill",
    version="1.0.2",
    author="LobsterAI Security Team",
    author_email="security@lobsterai.com",
    description="Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stoneyhoo/lobsterai-security-skill",
    packages=find_packages(include=["security", "security.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="lobsterai security audit rbac validation scanning",
    project_urls={
        "Bug Reports": "https://github.com/stoneyhoo/lobsterai-security-skill/issues",
        "Documentation": "https://github.com/stoneyhoo/lobsterai-security-skill/wiki",
        "Source": "https://github.com/stoneyhoo/lobsterai-security-skill",
    },
)

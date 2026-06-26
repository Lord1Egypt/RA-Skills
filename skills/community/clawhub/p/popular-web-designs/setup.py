"""Setup for popular-web-designs — pip-installable CLI for 54 web design systems."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="popular-web-designs",
    version="1.2.0",
    author="minirr890112-byte",
    license="MIT",
    description="54 production-quality design systems extracted from real websites. CLI for browsing, inspecting, and generating HTML/CSS from popular design templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minirr890112-byte/popular-web-designs",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "web-design=popular_web_designs.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: User Interfaces",
    ],
    keywords="web-design, html, css, design-systems, templates, landing-page, frontend, ui",
    project_urls={
        "Source": "https://github.com/minirr890112-byte/popular-web-designs",
        "Tracker": "https://github.com/minirr890112-byte/popular-web-designs/issues",
    },
)

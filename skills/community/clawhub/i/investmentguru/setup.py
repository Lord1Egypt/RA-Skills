from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="investment_gurus",
    version="1.0.0",
    author="Investment Gurus Team",
    author_email="contact@investmentgurus.cn",
    description="基于中国顶级投资大师的价值投资分析Skill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/investmentgurus/investment_gurus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "invest-guru=investment_gurus.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "investment_gurus": ["data/*.json"],
    },
    keywords="investment value-investing china-stocks guru analysis",
)()
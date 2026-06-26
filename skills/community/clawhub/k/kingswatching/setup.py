from setuptools import setup, find_packages

setup(
    name="kingswatching",
    version="0.4.0",
    description="The King Is Watching - AI Workflow Enforcer + Long-running Task Support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="OpenClaw Community",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "black", "flake8"]
    },
    entry_points={
        "console_scripts": [
            "kingswatching=test_overseer:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
from setuptools import setup, find_packages

setup(
    name="ocax-passport",
    version="1.0.0",
    description="OCAX Passport - 节点身份证技能",
    author="OCAX Team",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ocax-passport=tool:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

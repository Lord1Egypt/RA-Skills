from setuptools import setup

setup(
    name="linux-installer",
    version="1.0.0",
    description="Linux desktop app installer helper for OpenClaw",
    author="OpenClaw",
    py_modules=["main", "validate_catalog"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "linux-installer=main:main",
            "linux-installer-validate=validate_catalog:main",
        ],
    },
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)

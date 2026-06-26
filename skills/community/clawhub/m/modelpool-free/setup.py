from setuptools import setup, find_packages

setup(
    name="modelpool-free",
    version="1.0.3",
    description="Free AI Model Manager for OpenClaw — auto-discover, multi-key rotation, smart fallback, one-click repair",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="LeeHub",
    url="https://github.com/meilihulee/modelpool",
    license="MIT",
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    py_modules=["freeswitch", "repair"],
    entry_points={
        "console_scripts": [
            "modelpool=freeswitch:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)

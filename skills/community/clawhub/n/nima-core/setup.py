from setuptools import setup, find_packages

setup(
    name="nima-core",
    version="3.1.0",
    description="Biologically-inspired Dynamic Affect System for AI agents",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="NIMA Project",
    url="https://github.com/nima-project/nima-core",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
    ],
    extras_require={
        "vector": [
            "faiss-cpu>=1.7.4",
            "voyageai>=0.2.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'nima-core=nima_core:main',
        ],
    },
)
from setuptools import setup, find_packages

setup(
    name="learning-planner",
    version="1.0.2",
    description="个人学习规划系统 - 目标设定、计划生成、间隔重复复习",
    author="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "learning=learning_cli:main",
        ],
    },
)

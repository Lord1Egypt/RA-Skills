from setuptools import setup, find_packages

setup(
    name='playwright-test-generator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'playwright>=1.40.0',
        'pytest>=7.4.0',
        'click>=8.1.0',
    ],
    entry_points={
        'console_scripts': [
            'playwright-gen=cli:cli',
        ],
    },
    python_requires='>=3.9',
)

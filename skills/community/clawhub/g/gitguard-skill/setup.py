from setuptools import find_packages, setup

setup(
    name="gitguard-skill",
    version="1.0.0",
    description="Advanced Git/GitHub repo intelligence: secret scanning, health scoring, commit quality, branch and dependency hygiene.",
    author="welove111",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.9",
)

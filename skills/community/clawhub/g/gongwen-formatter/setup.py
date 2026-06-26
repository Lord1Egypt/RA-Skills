from setuptools import setup, find_packages

setup(
    name='official-doc',
    version='1.1.0',
    description='公文格式转换 - 将 Markdown 转为党政机关公文格式',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='EdwardWason',
    url='https://github.com/EdwardWason/official-doc',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-docx>=1.1.0',
        'markdown-it-py>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Government',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.8',
)

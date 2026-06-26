"""
DreamMoon Memory Processor - Python/FastAPI 版本
四级记忆存储架构实现

L1: Redis (热存储)
L2: SQLite (温存储)  
L3: 文件系统 (冷存储 - Markdown)
L4: FAISS + 压缩 (归档 - 向量检索)
"""

__version__ = "1.0.0"
__author__ = "DreamMoon"

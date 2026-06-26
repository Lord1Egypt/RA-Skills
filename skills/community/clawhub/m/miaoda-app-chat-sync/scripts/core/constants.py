#!/usr/bin/env python3
"""
Constants for Repo JSON Generator
"""

# Supported text file extensions
TEXT_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx',
    '.html', '.css', '.scss', '.less',
    '.json', '.yaml', '.yml', '.toml',
    '.md', '.txt', '.sh', '.bash',
    '.xml', '.sql', '.env',
    '.vue', '.svelte', '.rst',
}

# Directories to skip during processing
SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', 
    '.venv', 'venv', 'dist', 'build',
    '.next', '.nuxt', 'target',
    '.DS_Store', 'thumbs.db',
}

MAX_SINGLE_FILE_SIZE = 100 * 1024 * 1024  # 100MB

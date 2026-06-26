#!/usr/bin/env python3
import os
from pathlib import Path

def create_project_structure(project_name):
    base_dir = Path.cwd() / project_name
    
    directories = [
        base_dir / 'src',
        base_dir / 'test',
        base_dir / 'data',
        base_dir / 'output',
        base_dir / 'spec' / 'ME2AI',
        base_dir / 'spec' / 'AI2AI',
        base_dir / 'scripts',
        base_dir / 'templates',
        base_dir / 'references'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f'Created: {directory}')
    
    print(f'\nProject structure created at: {base_dir}')
    return base_dir

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = 'inventory-system'
    
    create_project_structure(project_name)
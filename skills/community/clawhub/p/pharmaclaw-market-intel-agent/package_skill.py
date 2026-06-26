#!/usr/bin/env python3
import os
import tarfile
import shutil

def main(skill_dir='.'):
    skill_dir = os.path.abspath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    skill_path = os.path.dirname(skill_dir)
    skill_file = os.path.join(skill_path, f'{skill_name}.skill')
    
    # Clean temp files
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
    
    with tarfile.open(skill_file, 'w:gz') as tar:
        tar.add(skill_dir, arcname=skill_name, recursive=True)
    
    print(f'Successfully packaged: {skill_file}')
    print(f'Size: {os.path.getsize(skill_file) / 1024:.1f} KB')

if __name__ == '__main__':
    main()

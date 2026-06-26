#!/usr/bin/env python3
"""
Package kimi-quota skill into a .skill file
"""

import sys
import shutil
from pathlib import Path

def package_skill():
    skill_dir = Path(__file__).parent.parent
    skill_name = skill_dir.name
    output_file = skill_dir.parent / f"{skill_name}.skill"
    
    # Create zip file with .skill extension
    shutil.make_archive(
        str(output_file.with_suffix('')),
        'zip',
        str(skill_dir)
    )
    
    # Rename .zip to .skill
    zip_file = output_file.with_suffix('.zip')
    if zip_file.exists():
        zip_file.rename(output_file)
    
    print(f"✅ Packaged: {output_file}")
    return output_file

if __name__ == "__main__":
    package_skill()

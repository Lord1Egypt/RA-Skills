#!/usr/bin/env python3
"""
CUDA to MUSA Code Converter
自动将 PyTorch CUDA 代码转换为 MUSA (摩尔线程 GPU) 兼容代码

Usage:
    python cuda_to_musa.py --input input.py --output output.py
    python cuda_to_musa.py --input ./cuda_project/ --output ./musa_project/
"""

import argparse
import re
import sys
from pathlib import Path


# Conversion rules: (pattern, replacement, description)
CONVERSION_RULES = [
    # Import torch_musa
    (
        r'^(import torch\n)',
        r'\1import torch_musa  # Added for MUSA support\n',
        "Add torch_musa import"
    ),
    # Device creation - use torch.device()
    (
        r'torch\.device\(["\']cuda["\']\)',
        r'torch.device("musa")',
        'Replace torch.device("cuda") with torch.device("musa")'
    ),
    (
        r'torch\.device\(["\']cuda:(\d+)["\']\)',
        r'torch.device("musa:\1")',
        'Replace torch.device("cuda:N") with torch.device("musa:N")'
    ),
    # Legacy device strings (fallback for string-based device)
    (
        r"device\s*=\s*['\"]cuda['\"]",
        r'device = torch.device("musa")',
        "Replace 'cuda' device string with torch.device(\"musa\")"
    ),
    (
        r"device='cuda'",
        r'device=torch.device("musa")',
        "Replace 'cuda' device string (inline)"
    ),
    (
        r'to\(["\']cuda["\']\)',
        r'to(torch.device("musa"))',
        "Replace .to('cuda') with .to(torch.device(\"musa\"))"
    ),
    # API calls
    (
        r'torch\.cuda\.is_available\(\)',
        r'torch.musa.is_available()',
        "Replace torch.cuda.is_available()"
    ),
    (
        r'torch\.cuda\.device_count\(\)',
        r'torch.musa.device_count()',
        "Replace torch.cuda.device_count()"
    ),
    (
        r'torch\.cuda\.get_device_name',
        r'torch.musa.get_device_name',
        "Replace torch.cuda.get_device_name"
    ),
    (
        r'torch\.cuda\.current_device\(\)',
        r'torch.musa.current_device()',
        "Replace torch.cuda.current_device()"
    ),
    (
        r'torch\.cuda\.set_device',
        r'torch.musa.set_device',
        "Replace torch.cuda.set_device"
    ),
    (
        r'torch\.cuda\.empty_cache\(\)',
        r'torch.musa.empty_cache()',
        "Replace torch.cuda.empty_cache()"
    ),
    (
        r'torch\.cuda\.synchronize\(\)',
        r'torch.musa.synchronize()',
        "Replace torch.cuda.synchronize()"
    ),
    (
        r'torch\.cuda\.memory_summary',
        r'torch.musa.memory_summary',
        "Replace torch.cuda.memory_summary"
    ),
    (
        r'torch\.cuda\.memory_allocated',
        r'torch.musa.memory_allocated',
        "Replace torch.cuda.memory_allocated"
    ),
    (
        r'torch\.cuda\.memory_reserved',
        r'torch.musa.memory_reserved',
        "Replace torch.cuda.memory_reserved"
    ),
    (
        r'torch\.cuda\.get_device_properties',
        r'torch.musa.get_device_properties',
        "Replace torch.cuda.get_device_properties"
    ),
    # Multi-GPU
    (
        r'torch\.cuda\.device',
        r'torch.musa.device',
        "Replace torch.cuda.device"
    ),
    # Distributed backend
    (
        r"backend\s*=\s*['\"]nccl['\"]",
        r"backend='mccl'",
        "Replace nccl backend with mccl"
    ),
    (
        r'["\']nccl["\']',
        r'"mccl"',
        "Replace 'nccl' string with 'mccl'"
    ),
]


def convert_file(input_path: Path, output_path: Path, dry_run: bool = False) -> dict:
    """Convert a single Python file from CUDA to MUSA."""
    stats = {
        'rules_applied': [],
        'lines_changed': 0,
        'torch_musa_added': False,
    }
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            original_lines = content.split('\n')
    except Exception as e:
        print(f"❌ Error reading {input_path}: {e}")
        return None
    
    new_content = content
    
    # Apply conversion rules
    for pattern, replacement, description in CONVERSION_RULES:
        matches = re.findall(pattern, new_content, re.MULTILINE)
        if matches:
            new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
            stats['rules_applied'].append({
                'rule': description,
                'count': len(matches)
            })
            stats['lines_changed'] += len(matches)
    
    stats['torch_musa_added'] = 'import torch_musa' in new_content
    
    new_lines = new_content.split('\n')
    if len(original_lines) != len(new_lines):
        stats['lines_added'] = len(new_lines) - len(original_lines)
    
    if not dry_run and stats['lines_changed'] > 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return stats


def convert_directory(input_dir: Path, output_dir: Path, dry_run: bool = False):
    """Convert all Python files in a directory."""
    python_files = list(input_dir.rglob('*.py'))
    
    print(f"Found {len(python_files)} Python files")
    print("-" * 60)
    
    total_converted = 0
    total_skipped = 0
    
    for py_file in python_files:
        relative_path = py_file.relative_to(input_dir)
        output_file = output_dir / relative_path
        
        print(f"\n📝 {relative_path}")
        
        stats = convert_file(py_file, output_file, dry_run)
        
        if stats is None:
            print(f"   ❌ Failed to process")
            continue
        
        if stats['lines_changed'] == 0:
            print(f"   ⏭️  No changes needed")
            total_skipped += 1
            continue
        
        print(f"   ✅ Converted ({stats['lines_changed']} changes)")
        for rule in stats['rules_applied']:
            print(f"      - {rule['rule']}: {rule['count']}x")
        
        total_converted += 1
    
    print("-" * 60)
    print(f"\n📊 Summary:")
    print(f"   Total files: {len(python_files)}")
    print(f"   Converted: {total_converted}")
    print(f"   Skipped (no changes): {total_skipped}")
    
    if dry_run:
        print(f"\n⚠️  Dry run mode - no files were written")
    else:
        print(f"\n✅ Output written to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert PyTorch CUDA code to MUSA code'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input Python file or directory'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output Python file or directory'
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview changes without writing files'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Error: Input path does not exist: {input_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔧 CUDA to MUSA Code Converter")
    print("=" * 60)
    
    if input_path.is_file():
        print(f"\n📄 Converting file: {input_path}")
        if args.dry_run:
            print("   (Dry run mode)")
        
        stats = convert_file(input_path, output_path, args.dry_run)
        
        if stats and stats['lines_changed'] > 0:
            print(f"\n✅ Conversion complete!")
            print(f"   Changes: {stats['lines_changed']}")
            for rule in stats['rules_applied']:
                print(f"   - {rule['rule']}: {rule['count']}x")
        elif stats:
            print(f"\n⏭️  No changes needed")
    else:
        print(f"\n📁 Converting directory: {input_path}")
        print(f"   Output: {output_path}")
        if args.dry_run:
            print("   (Dry run mode)")
        
        convert_directory(input_path, output_path, args.dry_run)


if __name__ == '__main__':
    main()

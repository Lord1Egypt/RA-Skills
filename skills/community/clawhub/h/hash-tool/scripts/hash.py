#!/usr/bin/env python3
"""Hash Tool - Generate checksums and hashes for files and strings."""

import argparse
import hashlib
import sys
import os
from pathlib import Path

ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b', 'blake2s']
ENCODINGS = ['hex', 'base64']


def hash_string(text: str, algorithm: str, encoding: str = 'hex') -> str:
    """Hash a string using the specified algorithm."""
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha512':
        hasher = hashlib.sha512()
    elif algorithm == 'blake2b':
        hasher = hashlib.blake2b()
    elif algorithm == 'blake2s':
        hasher = hashlib.blake2s()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher.update(text.encode('utf-8'))
    
    if encoding == 'base64':
        import base64
        return base64.b64encode(hasher.digest()).decode('ascii')
    return hasher.hexdigest()


def hash_file(filepath: str, algorithm: str, encoding: str = 'hex', chunk_size: int = 65536) -> str:
    """Hash a file using the specified algorithm."""
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha512':
        hasher = hashlib.sha512()
    elif algorithm == 'blake2b':
        hasher = hashlib.blake2b()
    elif algorithm == 'blake2s':
        hasher = hashlib.blake2s()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    
    if encoding == 'base64':
        import base64
        return base64.b64encode(hasher.digest()).decode('ascii')
    return hasher.hexdigest()


def hash_file_all(filepath: str, encoding: str = 'hex') -> dict:
    """Generate all available hashes for a file."""
    results = {}
    for algo in ALGORITHMS:
        try:
            results[algo] = hash_file(filepath, algo, encoding)
        except Exception as e:
            results[algo] = f"Error: {e}"
    return results


def verify_hash(filepath: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    """Verify a file against an expected hash."""
    actual = hash_file(filepath, algorithm)
    return actual.lower() == expected_hash.lower()


def main():
    parser = argparse.ArgumentParser(
        description='Generate checksums and hashes for files and strings'
    )
    parser.add_argument(
        '--algorithm', '-a',
        choices=ALGORITHMS,
        default='sha256',
        help='Hash algorithm to use (default: sha256)'
    )
    parser.add_argument(
        '--string', '-s',
        help='Hash a string directly'
    )
    parser.add_argument(
        '--file', '-f',
        help='Hash a file'
    )
    parser.add_argument(
        '--verify',
        help='Verify against an expected hash'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all hash algorithms (for files only)'
    )
    parser.add_argument(
        '--encode',
        choices=ENCODINGS,
        default='hex',
        help='Output encoding (default: hex)'
    )
    
    args = parser.parse_args()
    
    if not args.string and not args.file:
        parser.print_help()
        print("\nExamples:")
        print("  hash-tool --algorithm sha256 --string 'Hello World'")
        print("  hash-tool --algorithm sha256 --file document.pdf")
        print("  hash-tool --verify abc123... --file document.pdf")
        print("  hash-tool --file document.pdf --all")
        sys.exit(1)
    
    try:
        if args.string:
            result = hash_string(args.string, args.algorithm, args.encode)
            print(f"{args.algorithm.upper()} ({args.encode}): {result}")
        
        if args.file:
            filepath = Path(args.file)
            if not filepath.exists():
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            
            if args.verify:
                is_valid = verify_hash(args.file, args.verify, args.algorithm)
                if is_valid:
                    print(f"✓ Hash verification PASSED")
                    sys.exit(0)
                else:
                    actual = hash_file(args.file, args.algorithm)
                    print(f"✗ Hash verification FAILED")
                    print(f"  Expected: {args.verify}")
                    print(f"  Actual:   {actual}")
                    sys.exit(1)
            
            if args.all:
                results = hash_file_all(args.file, args.encode)
                print(f"Hashes for: {args.file}")
                for algo, hash_val in results.items():
                    print(f"  {algo:8}: {hash_val}")
            else:
                result = hash_file(args.file, args.algorithm, args.encode)
                print(f"{args.algorithm.upper()} ({args.encode}): {result}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

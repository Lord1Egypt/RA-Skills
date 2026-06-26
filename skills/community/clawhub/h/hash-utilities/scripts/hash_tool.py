#!/usr/bin/env python3
"""Hash Toolkit - Generate and verify hashes. Zero dependencies."""

import hashlib
import hmac
import sys
import os
import zlib
import binascii
import argparse

ALGORITHMS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s']

def hash_string(text, algorithm='sha256'):
    if algorithm == 'crc32':
        return format(zlib.crc32(text.encode()) & 0xFFFFFFFF, '08x')
    h = hashlib.new(algorithm)
    h.update(text.encode('utf-8'))
    return h.hexdigest()

def hash_file(filepath, algorithm='sha256'):
    if algorithm == 'crc32':
        crc = 0
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                crc = zlib.crc32(chunk, crc)
        return format(crc & 0xFFFFFFFF, '08x')
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def hmac_sign(message, key, algorithm='sha256'):
    h = hmac.new(key.encode(), message.encode(), algorithm)
    return h.hexdigest()

def verify_hash(computed, expected):
    return hmac.compare_digest(computed.lower(), expected.lower())

def main():
    parser = argparse.ArgumentParser(description='Hash Toolkit')
    sub = parser.add_subparsers(dest='command')
    
    p = sub.add_parser('string', help='Hash a string')
    p.add_argument('text'); p.add_argument('-a', '--algorithm', default='sha256', choices=ALGORITHMS + ['crc32'])
    
    p = sub.add_parser('file', help='Hash a file')
    p.add_argument('filepath'); p.add_argument('-a', '--algorithm', default='sha256', choices=ALGORITHMS + ['crc32'])
    
    p = sub.add_parser('verify', help='Verify a hash')
    p.add_argument('filepath'); p.add_argument('expected')
    p.add_argument('-a', '--algorithm', default='sha256', choices=ALGORITHMS + ['crc32'])
    
    p = sub.add_parser('hmac', help='HMAC signature')
    p.add_argument('message'); p.add_argument('-k', '--key', required=True)
    p.add_argument('-a', '--algorithm', default='sha256')
    
    p = sub.add_parser('batch', help='Hash multiple files')
    p.add_argument('files', nargs='+'); p.add_argument('-a', '--algorithm', default='sha256', choices=ALGORITHMS + ['crc32'])
    
    p = sub.add_parser('list', help='List available algorithms')
    
    args = parser.parse_args()
    
    if args.command == 'string':
        print(f"{args.algorithm}: {hash_string(args.text, args.algorithm)}")
    elif args.command == 'file':
        print(f"{args.algorithm} ({args.filepath}): {hash_file(args.filepath, args.algorithm)}")
    elif args.command == 'verify':
        computed = hash_file(args.filepath, args.algorithm)
        match = verify_hash(computed, args.expected)
        print(f"{'✅ MATCH' if match else '❌ MISMATCH'}")
        print(f"Computed: {computed}")
        print(f"Expected: {args.expected}")
    elif args.command == 'hmac':
        print(f"HMAC-{args.algorithm}: {hmac_sign(args.message, args.key, args.algorithm)}")
    elif args.command == 'batch':
        for f in args.files:
            if os.path.isfile(f):
                print(f"{hash_file(f, args.algorithm)}  {f}")
            else:
                print(f"NOT FOUND: {f}")
    elif args.command == 'list':
        print("Available algorithms:", ', '.join(ALGORITHMS + ['crc32']))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

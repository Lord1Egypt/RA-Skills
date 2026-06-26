#!/usr/bin/env python3
"""
Hash Toolkit - Multi-purpose hash utility
Supports: MD5, SHA-1, SHA-256, SHA-512, BLAKE2b, Base64, UUID, HMAC
"""
import argparse
import hashlib
import uuid
import base64
import sys
import hmac as hmac_module

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def sha1_hash(text):
    return hashlib.sha1(text.encode()).hexdigest()

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def sha512_hash(text):
    return hashlib.sha512(text.encode()).hexdigest()

def blake2b_hash(text):
    return hashlib.blake2b(text.encode()).hexdigest()

def hmac_sign(text, key, algo='sha256'):
    """Generate HMAC signature"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    if algo.lower() not in algorithms:
        return None
    h = hmac_module.new(key.encode(), text.encode(), algorithms[algo.lower()])
    return h.hexdigest()

def generate_uuid():
    return str(uuid.uuid4())

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text.encode()).decode()

def main():
    parser = argparse.ArgumentParser(
        description='Hash Toolkit - Multi-purpose hash utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 hash_toolkit.py "Hello World" --algo sha256
  python3 hash_toolkit.py "Hello World" --encode64
  python3 hash_toolkit.py --uuid
  python3 hash_toolkit.py "message" --hmac "secret-key"
        """
    )
    
    parser.add_argument('text', nargs='?', help='Text to hash/encode')
    parser.add_argument('--algo', default='sha256',
                       choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                       help='Hash algorithm (default: sha256)')
    parser.add_argument('--encode64', action='store_true', help='Base64 encode')
    parser.add_argument('--decode', action='store_true', help='Base64 decode')
    parser.add_argument('--uuid', action='store_true', help='Generate UUID')
    parser.add_argument('--hmac', metavar='KEY', help='HMAC signing key')
    parser.add_argument('--upper', action='store_true', help='Output uppercase')
    parser.add_argument('--count', type=int, default=1, help='Number of UUIDs')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = {}
    
    # UUID mode
    if args.uuid:
        uuids = [generate_uuid() for _ in range(args.count)]
        if args.upper:
            uuids = [u.upper() for u in uuids]
        result = {'mode': 'uuid', 'count': args.count, 'uuids': uuids}
        if not args.json:
            for u in uuids:
                print(u)
        else:
            import json
            print(json.dumps(result, indent=2))
        return
    
    # Base64 mode
    if args.encode64:
        if not args.text:
            print("❌ Error: Please provide text to encode")
            return
        encoded = base64_encode(args.text)
        if args.upper:
            encoded = encoded.upper()
        result = {'mode': 'base64_encode', 'input': args.text, 'output': encoded}
        if not args.json:
            print(f"📝 Base64 encoded: {encoded}")
        else:
            import json
            print(json.dumps(result, indent=2))
        return
    
    if args.decode:
        if not args.text:
            print("❌ Error: Please provide text to decode")
            return
        try:
            decoded = base64_decode(args.text)
            result = {'mode': 'base64_decode', 'input': args.text, 'output': decoded}
            if not args.json:
                print(f"📝 Base64 decoded: {decoded}")
            else:
                import json
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"❌ Decode failed: {e}")
        return
    
    # Hash mode
    if not args.text:
        print("Usage:")
        print("  python3 hash_toolkit.py 'text' --algo sha256")
        print("  python3 hash_toolkit.py --uuid")
        print("  python3 hash_toolkit.py 'text' --encode64")
        return
    
    # HMAC mode
    if args.hmac:
        signature = hmac_sign(args.text, args.hmac, args.algo)
        if signature:
            if args.upper:
                signature = signature.upper()
            result = {
                'mode': 'hmac',
                'algorithm': args.algo,
                'message': args.text,
                'signature': signature
            }
            if not args.json:
                print(f"🔐 HMAC-{args.algo.upper()}: {signature}")
            else:
                import json
                print(json.dumps(result, indent=2))
        return
    
    # Regular hash
    hash_funcs = {
        'md5': md5_hash,
        'sha1': sha1_hash,
        'sha256': sha256_hash,
        'sha512': sha512_hash,
        'blake2': blake2b_hash,
    }
    
    hash_value = hash_funcs[args.algo](args.text)
    if args.upper:
        hash_value = hash_value.upper()
    
    result = {
        'mode': 'hash',
        'algorithm': args.algo,
        'input': args.text,
        'hash': hash_value
    }
    
    if not args.json:
        print(f"🔐 {args.algo.upper()}: {hash_value}")
    else:
        import json
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

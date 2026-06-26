#!/usr/bin/env python3
import hmac
import hashlib
import datetime
import json
import sys
import base64
import urllib.parse

def sign(key, msg):
    """Sign function that handles both string and bytes"""
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    return hmac.new(key, msg, hashlib.sha256).digest()

def generate_auth_header(ak, sk, method, path, query, body):
    host = 'visual.volcengineapi.com'
    region = 'cn-north-1'
    service = 'cv'

    now = datetime.datetime.utcnow()
    current_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = current_date[:8]

    content_type = 'application/json'
    payload_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()

    signed_headers = 'host;x-date;x-content-sha256;content-type'

    canonical_headers = f'host:{host}\nx-date:{current_date}\nx-content-sha256:{payload_hash}\ncontent-type:{content_type}\n'

    canonical_request = f'{method}\n{path}\n{query}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

    algorithm = 'HMAC-SHA256'
    credential_scope = f'{date_stamp}/{region}/{service}/request'

    hashed_canonical = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f'{algorithm}\n{current_date}\n{credential_scope}\n{hashed_canonical}'

    # Key derivation (Python official way)
    kDate = sign(sk, date_stamp)
    kRegion = sign(kDate, region)
    kService = sign(kRegion, service)
    kSigning = sign(kService, 'request')

    signature = hmac.new(kSigning, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization = f'{algorithm} Credential={ak}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'

    return current_date, payload_hash, authorization

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: sign.py <ak> <sk> <method> <path> <query> <body>")
        sys.exit(1)

    ak = sys.argv[1]
    sk = sys.argv[2]
    method = sys.argv[3]
    path = sys.argv[4]
    query = sys.argv[5]
    body = sys.argv[6] if len(sys.argv) > 6 else ""

    current_date, payload_hash, authorization = generate_auth_header(ak, sk, method, path, query, body)
    
    print(current_date)
    print(payload_hash)
    print(authorization)

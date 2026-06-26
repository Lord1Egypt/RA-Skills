#!/usr/bin/env python3
"""
MikroTik RouterOS API Client — pure Python, no external deps
Usage: python3 mikrotik_api.py <command> [args]
"""

import socket, hashlib, binascii, os, sys, json

class RouterOSApi:
    def __init__(self, host, username='admin', password='', port=8728, timeout=10):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        self._login()
        return self

    def disconnect(self):
        if self.sock:
            try: self.sock.close()
            except: pass
            self.sock = None

    def __enter__(self): return self.connect()
    def __exit__(self, *a): self.disconnect()

    def _encode_len(self, n):
        if n < 0x80: return bytes([n])
        elif n < 0x4000: return bytes([(n >> 8) | 0x80, n & 0xFF])
        elif n < 0x200000: return bytes([(n >> 16) | 0xC0, (n >> 8) & 0xFF, n & 0xFF])
        else: return bytes([0xE0, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])

    def _send_sentence(self, words):
        msg = b''
        for w in words:
            b = w.encode('utf-8')
            msg += self._encode_len(len(b)) + b
        msg += b'\x00'
        self.sock.sendall(msg)

    def _read_len(self):
        b = self.sock.recv(1)
        if not b: raise ConnectionError("Connection closed")
        n = b[0]
        if n < 0x80: return n
        elif n < 0xC0:
            b2 = self.sock.recv(1)[0]
            return ((n & ~0x80) << 8) | b2
        elif n < 0xE0:
            b2, b3 = self.sock.recv(1)[0], self.sock.recv(1)[0]
            return ((n & ~0xC0) << 16) | (b2 << 8) | b3
        else:
            b2,b3,b4 = self.sock.recv(1)[0],self.sock.recv(1)[0],self.sock.recv(1)[0]
            return (b2 << 16) | (b3 << 8) | b4

    def _read_sentence(self):
        words = []
        while True:
            length = self._read_len()
            if length == 0: break
            data = b''
            while len(data) < length:
                chunk = self.sock.recv(length - len(data))
                if not chunk: raise ConnectionError("Connection closed")
                data += chunk
            words.append(data.decode('utf-8'))
        return words

    def _read_response(self):
        results, reply_type = [], None
        while True:
            sentence = self._read_sentence()
            if not sentence: continue
            reply_type = sentence[0]
            if reply_type == '!done': break
            elif reply_type == '!trap':
                msg = ' '.join(w for w in sentence[1:] if w.startswith('=message='))
                raise RouterOSError(msg.replace('=message=',''))
            elif reply_type == '!re':
                row = {}
                for w in sentence[1:]:
                    if w.startswith('=') and '=' in w[1:]:
                        k, _, v = w[1:].partition('=')
                        row[k] = v
                results.append(row)
        return results

    def _login(self):
        # Try plaintext login (ROS 6.43+)
        self._send_sentence(['/login', f'=name={self.username}', f'=password={self.password}'])
        try:
            resp = self._read_sentence()
            if resp[0] == '!done': return
            # Legacy MD5 challenge
            if resp[0] == '!re':
                challenge = [w for w in resp if w.startswith('=ret=')]
                if challenge:
                    chal = bytes.fromhex(challenge[0].split('=ret=')[1])
                    md5 = hashlib.md5(b'\x00' + self.password.encode() + chal)
                    self._send_sentence(['/login', f'=name={self.username}', f'=response=00{md5.hexdigest()}'])
                    self._read_response()
        except Exception as e:
            raise ConnectionError(f"Login failed: {e}")

    def run(self, command, *args):
        words = [command]
        words.extend(args)
        self._send_sentence(words)
        return self._read_response()

class RouterOSError(Exception): pass

def get_config():
    """Get device config from env vars or TOOLS.md (MikroTik section only)"""
    host = os.getenv('MIKROTIK_HOST')
    user = os.getenv('MIKROTIK_USER', 'admin')
    pwd  = os.getenv('MIKROTIK_PASS', '')
    if host:
        return {'host': host, 'username': user, 'password': pwd}
    # Try TOOLS.md — scoped to MikroTik section only to avoid reading unrelated credentials
    tools = os.path.expanduser('~/.openclaw/workspace/TOOLS.md')
    if os.path.exists(tools):
        import re
        content = open(tools).read()
        section = re.search(r'###\s+MikroTik[^\n]*\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
        if not section:
            return None
        m = re.search(r'[-*]\s+\*\*(\w+)\*\*:\s*([^,\n]+),\s*([^,\n]+),\s*(.+)', section.group(1))
        if m:
            fourth = m.group(4).strip()
            if fourth.startswith('key:'):
                return {'host': m.group(2).strip(), 'username': m.group(3).strip(), 'password': ''}
            if fourth.lower() in ['empty password', 'no password', 'none', 'null', '']:
                return {'host': m.group(2).strip(), 'username': m.group(3).strip(), 'password': ''}
            # Password found in TOOLS.md — warn and use MIKROTIK_PASS env var instead
            print("WARNING: Plaintext password in TOOLS.md — set MIKROTIK_PASS env var and use key: in TOOLS.md instead.", file=sys.stderr)
            return {'host': m.group(2).strip(), 'username': m.group(3).strip(), 'password': fourth}
    return None

if __name__ == '__main__':
    cfg = get_config()
    if not cfg:
        print("Set MIKROTIK_HOST, MIKROTIK_USER, MIKROTIK_PASS or configure TOOLS.md")
        sys.exit(1)
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else '/system/resource/print'
    
    with RouterOSApi(**cfg) as api:
        results = api.run(cmd)
        print(json.dumps(results, indent=2))

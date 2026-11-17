"""Minimal CloudDrive2 gRPC-Web client. Usage: python -I cd2.py <Method> [request_hex]
Token is read from env CD2_TOKEN and never printed.
API address from env CD2_URL (default http://127.0.0.1:19798)."""
import os, sys, struct, urllib.request, urllib.error

BASE = os.environ.get("CD2_URL", "http://127.0.0.1:19798").rstrip("/") + "/clouddrive.CloudDriveFileSrv/"


def varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1
        r |= (c & 0x7F) << s; s += 7
        if c < 0x80:
            return r, i


def parse(b):
    out, i = [], 0
    while i < len(b):
        key, i = varint(b, i)
        f, wt = key >> 3, key & 7
        if f == 0:
            raise ValueError
        if wt == 0:
            v, i = varint(b, i)
        elif wt == 1:
            v = struct.unpack('<d', b[i:i + 8])[0]; i += 8
        elif wt == 5:
            v = struct.unpack('<f', b[i:i + 4])[0]; i += 4
        elif wt == 2:
            n, i = varint(b, i)
            v = b[i:i + n]; i += n
            if len(v) != n:
                raise ValueError
        else:
            raise ValueError
        out.append((f, v))
    return out


def show(b, ind=0):
    for f, v in parse(b):
        pad = '  ' * ind
        if isinstance(v, bytes):
            try:
                txt = v.decode('utf-8')
                printable = txt.isprintable()
            except UnicodeDecodeError:
                printable = False
            sub = None
            if not printable and v:
                try:
                    parse(v); sub = v
                except Exception:
                    pass
            if printable:
                print(f"{pad}{f}: {txt!r}")
            elif sub is not None:
                print(f"{pad}{f}: {{"); show(sub, ind + 1); print(f"{pad}}}")
            else:
                print(f"{pad}{f}: <{len(v)} bytes>")
        else:
            print(f"{pad}{f}: {v}")


def call(method, body=b''):
    data = b'\x00' + struct.pack('>I', len(body)) + body
    req = urllib.request.Request(BASE + method, data=data, method='POST', headers={
        'Content-Type': 'application/grpc-web+proto', 'X-Grpc-Web': '1',
        'Authorization': 'Bearer ' + os.environ.get('CD2_TOKEN', '')})
    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        print('HTTP', e.code, dict(e.headers)); return
    raw = resp.read()
    print('HTTP', resp.status, 'grpc-status', resp.headers.get('grpc-status'), resp.headers.get('grpc-message') or '')
    i = 0
    while i + 5 <= len(raw):
        flag, n = raw[i], struct.unpack('>I', raw[i + 1:i + 5])[0]
        frame = raw[i + 5:i + 5 + n]; i += 5 + n
        if flag & 0x80:
            print('trailer:', frame.decode('utf-8', 'replace').strip().replace('\r\n', ' | '))
        else:
            show(frame)


if __name__ == '__main__':
    call(sys.argv[1], bytes.fromhex(sys.argv[2]) if len(sys.argv) > 2 else b'')

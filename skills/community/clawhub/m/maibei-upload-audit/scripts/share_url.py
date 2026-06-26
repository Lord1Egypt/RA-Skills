#!/usr/bin/env python3
"""
Share a local file or directory via trycloudflare tunnel.
Returns the public URL after verification.
"""
import argparse
import os
import subprocess
import sys
import time
import signal

def find_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_http_server(directory, port):
    """Start a simple HTTP server in the background."""
    cmd = [sys.executable, '-m', 'http.server', str(port)]
    proc = subprocess.Popen(cmd, cwd=directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc

def start_cloudflared(port):
    """Start cloudflared tunnel and return the public URL."""
    cmd = [
        'cloudflared', 'tunnel',
        '--url', f'http://127.0.0.1:{port}',
        '--no-autoupdate',
        '--protocol', 'http2',
        '--metrics', 'localhost:20241'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc

def wait_for_url(proc, timeout=30):
    """Wait for cloudflared to output the tunnel URL."""
    start = time.time()
    url = None
    while time.time() - start < timeout:
        line = proc.stderr.readline()
        if not line:
            if proc.poll() is not None:
                break
            time.sleep(0.5)
            continue
        if 'trycloudflare.com' in line:
            idx = line.find('https://')
            if idx != -1:
                tail = line[idx:]
                end = tail.find(' ')
                if end == -1:
                    end = tail.find('\n')
                url = tail[:end].rstrip()
                break
        # Also check stdout
        line_out = proc.stdout.readline()
        if line_out and 'trycloudflare.com' in line_out:
            idx = line_out.find('https://')
            if idx != -1:
                url = line_out[idx:].split()[0].rstrip()
                break
    return url

def verify_url(url, path_hint='', timeout=15):
    """Verify the URL is actually reachable."""
    import urllib.request
    import urllib.error
    target = f"{url}/{path_hint}" if path_hint else url
    try:
        req = urllib.request.Request(target, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200, resp.status
    except Exception as e:
        # Try GET as fallback
        try:
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status == 200, resp.status
        except Exception as e2:
            return False, str(e)

def share_local_path(file_or_dir, filename_hint='', port=None):
    """
    Share a local file or directory via trycloudflare.
    Returns (public_url, tunnel_proc, server_proc) on success.
    """
    path = os.path.abspath(os.path.expanduser(file_or_dir))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    is_file = os.path.isfile(path)
    if is_file:
        serve_dir = os.path.dirname(path)
        filename_hint = filename_hint or os.path.basename(path)
    else:
        serve_dir = path
        filename_hint = filename_hint or ''

    port = port or find_free_port()

    # Start HTTP server
    server_proc = start_http_server(serve_dir, port)
    time.sleep(1.5)

    # Start cloudflared
    tunnel_proc = start_cloudflared(port)

    try:
        url = wait_for_url(tunnel_proc, timeout=30)
        if not url:
            raise RuntimeError("Could not get trycloudflare URL")

        # Verify
        hint = filename_hint if is_file else ''
        ok, status = verify_url(url, hint)
        if not ok:
            print(f"Warning: URL verification returned {status}", file=sys.stderr)

        return url, tunnel_proc, server_proc
    except Exception:
        tunnel_proc.terminate()
        server_proc.terminate()
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Share local file/dir via trycloudflare')
    parser.add_argument('path', help='File or directory to share')
    parser.add_argument('--filename', default='', help='Filename hint for single file URL')
    parser.add_argument('--port', type=int, help='HTTP server port (auto-detected if omitted)')
    args = parser.parse_args()

    url, tunnel_proc, server_proc = share_local_path(args.path, args.filename, args.port)
    print(url)

    # Keep alive until interrupted
    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        tunnel_proc.terminate()
        server_proc.terminate()
        sys.exit(0)

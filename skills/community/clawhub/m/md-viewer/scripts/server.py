#!/usr/bin/env python3
"""
MD Viewer Server - Local web server for viewing Markdown files (SECURE VERSION)

Usage:
    python3 server.py [--port PORT] [--host HOST] [--history-file FILE] [--password PASSWORD] [--no-history]

Examples:
    python3 server.py --password mysecret
    python3 server.py --host 0.0.0.0 --password mysecret  # Enable LAN access
"""

import argparse
import fcntl
import json
import os
import re
import secrets
import string
import random
import sys
import threading
from datetime import datetime
from html import escape
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

import markdown

# Try to import bleach for proper HTML sanitization
try:
    import bleach
    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False
    print("Warning: bleach not installed. Using basic sanitization. Install with: pip3 install bleach")

# Configuration
DEFAULT_PORT = 8765
DEFAULT_HISTORY_FILE = str(Path.home() / ".md-viewer-history.json")
COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days

# History lock for thread safety
_history_lock = threading.Lock()

# Security: Blocked paths and patterns
BLOCKED_PATHS = [
    '/etc', '/proc', '/sys', '/dev', '/var/log',
    '/.ssh', '/.gnupg', '/.aws', '/.docker',
]

BLOCKED_PATTERNS = [
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    '.ssh/', '.gnupg/', '.aws/', '.docker/',
    '.env', '.netrc', '.pgpass', '.pypirc',
    'credentials', 'secret', 'private',
    '.key', '.pem', '.p12', '.pfx',
    '.htaccess', '.htpasswd',
    'shadow', 'passwd', 'master.passwd',
]

# Global state (set at runtime)
_config = {
    'history_file': DEFAULT_HISTORY_FILE,
    'password': None,
    'no_history': False,
}

COOKIE_NAME = 'md_auth'


def is_path_allowed(file_path: str) -> tuple[bool, str]:
    """Check if path is allowed to be read. Returns (allowed, reason)"""
    path_lower = file_path.lower()
    
    # Only allow .md files
    if not file_path.endswith('.md'):
        return False, "Only .md files are allowed"
    
    # Check blocked absolute paths
    for blocked in BLOCKED_PATHS:
        if path_lower.startswith(blocked):
            return False, f"Access to system directory denied: {blocked}"
    
    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in path_lower:
            return False, f"Access to sensitive file denied"
    
    return True, ""


def sanitize_html_content(html: str) -> str:
    """Sanitize HTML to prevent XSS using bleach (preferred) or fallback regex"""
    
    if BLEACH_AVAILABLE:
        # Use bleach for robust sanitization
        ALLOWED_TAGS = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'br', 'hr',
            'strong', 'em', 'b', 'i', 'u',
            'code', 'pre',
            'ul', 'ol', 'li',
            'a', 'img',
            'blockquote',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
            'span', 'div',
        ]
        
        ALLOWED_ATTRS = {
            'a': ['href', 'title', 'name'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'code': ['class'],  # for syntax highlighting
            'pre': ['class'],
            'span': ['class'],
            'div': ['class'],
            'h1': ['id'], 'h2': ['id'], 'h3': ['id'], 'h4': ['id'], 'h5': ['id'], 'h6': ['id'],
        }
        
        ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
        
        return bleach.clean(
            html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True
        )
    
    # Fallback: basic regex sanitization (less secure)
    # Remove script tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<script[^>]*/?>', '', html, flags=re.IGNORECASE)
    
    # Remove event handlers (onerror, onclick, etc.)
    html = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
    
    # Remove javascript: URLs
    html = re.sub(r'javascript:', '', html, flags=re.IGNORECASE)
    
    # Remove data: URLs that could execute code
    html = re.sub(r'data:text/html[^"\']*', '', html, flags=re.IGNORECASE)
    
    return html


# HTML Template for rendering
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data: https:;">
    <style>
        /* E-INK OPTIMIZED - Light theme with high contrast */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{ 
            font-family: 'Georgia', 'Times New Roman', serif; /* Serif fonts better for e-ink */
            background: #ffffff; /* White background for e-ink */
            color: #000000; /* Black text for high contrast */
            min-height: 100vh; 
            font-size: 16px; /* Normal font size */
            line-height: 1.7; /* Comfortable line spacing */
        }}
        
        .container {{ 
            max-width: 900px; /* Narrower for better reading */
            margin: 0 auto; 
            padding: 24px; 
        }}
        
        .header {{ 
            background: #f5f5f5; /* Light gray header */
            border-bottom: 2px solid #000000; /* Strong border */
            padding: 16px 24px; 
            position: fixed; 
            top: 0; 
            left: 0; 
            right: 0; 
            z-index: 100; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            flex-wrap: wrap; 
            gap: 12px; 
            transform: translateY(0);
            transition: transform 0.2s ease;
        }}
        
        .header.hidden {{ 
            transform: translateY(-100%);
        }}
        
        .header-spacer {{ 
            height: 60px;
        }}
        
        .header h1 {{ 
            color: #000000; 
            font-size: 18px; 
            font-weight: bold; 
            font-family: 'Georgia', serif;
        }}
        
        .header-actions {{ display: flex; gap: 12px; }}
        
        .btn {{ 
            background: #000000; 
            color: #ffffff; 
            border: 2px solid #000000;
            padding: 10px 20px; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 14px; 
            font-weight: bold;
            text-decoration: none; 
            display: inline-flex; 
            align-items: center; 
            justify-content: center; 
            gap: 6px; 
            min-height: 44px; 
        }}
        
        .btn:hover {{ 
            background: #333333; 
        }}
        
        .btn-secondary {{ 
            background: #ffffff; 
            color: #000000;
            border: 2px solid #000000; 
            padding: 8px 16px; 
        }}
        
        .btn-secondary:hover {{ 
            background: #f0f0f0; 
        }}
        
        .content {{ 
            background: #ffffff; 
            border: 2px solid #000000; 
            border-radius: 8px; 
            margin-top: 20px; 
            padding: 24px; 
        }}
        
        /* Markdown body - E-ink optimized */
        .markdown-body {{ 
            color: #000000; 
            font-size: 16px; 
            line-height: 1.7; 
            font-family: 'Georgia', serif;
        }}
        
        .markdown-body h1 {{ 
            font-size: 1.5em; /* Normal heading size */
            border-bottom: 2px solid #000000; 
            padding-bottom: 0.3em; 
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            font-weight: bold;
        }}
        
        .markdown-body h2 {{ 
            font-size: 1.3em; 
            border-bottom: 2px solid #000000; 
            padding-bottom: 0.3em; 
            margin-top: 1.1em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }}
        
        .markdown-body h3 {{ 
            font-size: 1.1em; 
            margin-top: 1em;
            margin-bottom: 0.4em;
            font-weight: bold;
        }}
        
        .markdown-body p {{
            margin-bottom: 1em;
        }}
        
        .markdown-body code {{ 
            background: #f0f0f0; 
            color: #000000;
            padding: 0.2em 0.4em; 
            border-radius: 4px; 
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            border: 1px solid #cccccc;
        }}
        
        .markdown-body pre {{ 
            background: #f8f8f8; 
            border: 2px solid #000000; 
            border-radius: 8px; 
            overflow-x: auto; 
            padding: 16px;
            margin: 1em 0;
        }}
        
        .markdown-body pre code {{ 
            background: transparent; 
            border: none;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .markdown-body a {{ 
            color: #000000; 
            text-decoration: underline;
            font-weight: bold;
            border-bottom: 2px solid #000000;
        }}
        
        .markdown-body a:hover {{ 
            background: #f0f0f0;
        }}
        
        .markdown-body blockquote {{ 
            border-left: 4px solid #000000; 
            background: #f8f8f8; 
            padding: 16px; 
            margin: 1em 0;
            font-style: italic;
        }}
        
        .markdown-body ul, .markdown-body ol {{
            margin-left: 1.5em;
            margin-bottom: 1em;
        }}
        
        .markdown-body li {{
            margin-bottom: 0.3em;
        }}
        
        .markdown-body table {{ 
            border-collapse: collapse; 
            width: 100%; 
            overflow-x: auto; 
            display: block; 
            margin: 1em 0;
            border: 2px solid #000000;
        }}
        
        .markdown-body th, .markdown-body td {{ 
            border: 1px solid #000000; 
            padding: 8px 12px; 
        }}
        
        .markdown-body th {{ 
            background: #f0f0f0; 
            font-weight: bold;
        }}
        
        .markdown-body tr:nth-child(even) {{
            background: #f8f8f8;
        }}
        
        /* History - E-ink optimized */
        .history-list {{ list-style: none; padding: 0; }}
        
        .history-item {{ 
            background: #ffffff; 
            border: 2px solid #000000; 
            border-radius: 8px; 
            padding: 16px; 
            margin-bottom: 12px; 
            display: flex; 
            flex-direction: column; 
            gap: 8px; 
        }}
        
        .history-item:hover {{ 
            background: #f8f8f8;
        }}
        
        .history-title {{ 
            color: #000000; 
            font-weight: bold; 
            font-size: 16px; 
            word-break: break-word; 
        }}
        
        .history-path {{ 
            color: #333333; 
            font-size: 12px; 
            font-family: 'Courier New', monospace; 
            word-break: break-all; 
        }}
        
        .history-time {{ 
            color: #555555; 
            font-size: 12px; 
        }}
        
        .history-actions {{ margin-top: 8px; }}
        
        .empty-state {{ 
            text-align: center; 
            padding: 40px 20px; 
            color: #333333; 
            font-size: 16px;
        }}
        
        .file-path-form {{ display: flex; flex-direction: column; gap: 12px; }}
        
        .file-path-input {{ 
            width: 100%; 
            background: #ffffff; 
            border: 2px solid #000000; 
            color: #000000; 
            padding: 12px 16px; 
            border-radius: 8px; 
            font-size: 16px; 
            min-height: 44px; 
            font-family: 'Courier New', monospace;
        }}
        
        .file-path-input:focus {{ 
            outline: none; 
            border-color: #000000;
            background: #f8f8f8;
        }}
        
        .submit-btn {{ width: 100%; }}
        
        .error-message {{ 
            background: #000000; 
            color: #ffffff; 
            padding: 16px; 
            border-radius: 8px; 
            margin: 20px 0; 
            word-break: break-word; 
            font-size: 14px;
            font-weight: bold;
        }}
        
        .back-link {{ 
            color: #000000; 
            text-decoration: none; 
            display: inline-flex; 
            align-items: center; 
            gap: 6px; 
            margin-bottom: 20px; 
            font-size: 14px; 
            font-weight: bold;
            border-bottom: 2px solid #000000;
        }}
        
        .back-link:hover {{ 
            background: #f0f0f0;
        }}
        
        .login-form {{ max-width: 400px; margin: 40px auto; }}
        
        .login-form input {{ width: 100%; margin-bottom: 12px; }}
        
        /* Mobile responsive */
        @media (max-width: 600px) {{ 
            body {{ font-size: 15px; }}
            .container {{ padding: 12px; }} 
            .content {{ padding: 16px; }} 
            .btn {{ padding: 10px 16px; font-size: 14px; }} 
            .markdown-body {{ font-size: 15px; }}
            .markdown-body h1 {{ font-size: 1.4em; }}
            .markdown-body h2 {{ font-size: 1.2em; }}
            .markdown-body h3 {{ font-size: 1.1em; }}
        }}
        
        /* E-ink specific - reduce animations/transitions */
        * {{
            transition: none !important;
            animation: none !important;
        }}
    </style>
</head>
<body>
    <div class="header-spacer"></div>
    <div class="header">
        <h1>📄 MD Viewer</h1>
        <div class="header-actions">
            <a href="/" class="btn btn-secondary">🏠 Home</a>
            <a href="/history" class="btn btn-secondary">📜 History</a>
        </div>
    </div>
    <div class="container">
        {content}
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>
        hljs.highlightAll();
        
        // Hide header on scroll down, show on scroll up
        let lastScrollY = window.scrollY;
        const header = document.querySelector('.header');
        let ticking = false;
        
        window.addEventListener('scroll', () => {{
            if (!ticking) {{
                window.requestAnimationFrame(() => {{
                    const currentScrollY = window.scrollY;
                    
                    if (currentScrollY > lastScrollY && currentScrollY > 80) {{
                        // Scrolling down & past threshold - hide header
                        header.classList.add('hidden');
                    }} else if (currentScrollY < lastScrollY - 10) {{
                        // Scrolling up - show header
                        header.classList.remove('hidden');
                    }}
                    
                    lastScrollY = currentScrollY;
                    ticking = false;
                }});
                ticking = true;
            }}
        }});
        
        // Show header on tap near top
        document.body.addEventListener('click', (e) => {{
            if (e.clientY < 50) {{
                header.classList.remove('hidden');
            }}
        }});
    </script>
</body>
</html>
"""


class MDViewerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MD Viewer"""
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")
    
    def _get_cookie_value(self):
        """Get auth cookie value. Returns (value|None, malformed: bool)."""
        cookies = self.headers.get('Cookie', '')
        if not cookies:
            return None, False

        for cookie in cookies.split(';'):
            cookie = cookie.strip()
            if cookie.startswith(f'{COOKIE_NAME}='):
                raw = cookie[len(COOKIE_NAME) + 1:]
                if not raw or len(raw) > 256:
                    return None, True
                try:
                    decoded = unquote(raw)
                except Exception:
                    return None, True

                if any(ord(ch) < 32 for ch in decoded):
                    return None, True
                return decoded, False

        return None, False

    def _get_auth_state(self, query):
        """Check auth state with cookie-first policy."""
        password = _config.get('password')
        if not password:
            return {'ok': True, 'remembered': False, 'set_cookie': False, 'clear_cookie': False}

        # 1) Cookie FIRST
        cookie_token, malformed = self._get_cookie_value()
        if malformed:
            return {'ok': False, 'remembered': False, 'set_cookie': False, 'clear_cookie': True}

        if cookie_token is not None:
            if cookie_token == password:
                return {'ok': True, 'remembered': True, 'set_cookie': False, 'clear_cookie': False}
            return {'ok': False, 'remembered': False, 'set_cookie': False, 'clear_cookie': True}

        # 2) URL token fallback
        provided = query.get('token', [''])[0]
        if provided == password:
            return {'ok': True, 'remembered': False, 'set_cookie': True, 'clear_cookie': False}

        return {'ok': False, 'remembered': False, 'set_cookie': False, 'clear_cookie': False}

    def _set_auth_cookie(self, password):
        """Queue authentication cookie for response"""
        self._pending_cookie = f'{COOKIE_NAME}={quote(password, safe="")}; Path=/; Max-Age={COOKIE_MAX_AGE}; HttpOnly; SameSite=Lax'

    def _clear_auth_cookie(self):
        """Queue cookie clear for response"""
        self._pending_cookie = f'{COOKIE_NAME}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax'

    def _get_auth_param(self) -> str:
        """Get auth parameter for URLs (for link sharing)"""
        password = _config.get('password')
        return f"&token={quote(password)}" if password else ""

    def _remembered_indicator(self) -> str:
        if getattr(self, '_auth_via_cookie', False):
            return '<p style="color:#0a5; font-size:13px; margin-bottom:12px; font-weight:bold;">✅ Remembered login (cookie)</p>'
        return ''

    def _apply_pending_cookie_header(self):
        pending = getattr(self, '_pending_cookie', None)
        if pending:
            self.send_header('Set-Cookie', pending)
    
    def do_GET(self):
        self._pending_cookie = None
        self._auth_via_cookie = False
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # Check authentication
        auth = self._get_auth_state(query)
        if not auth['ok']:
            if auth['clear_cookie']:
                self._clear_auth_cookie()
            self._serve_login()
            return

        self._auth_via_cookie = auth['remembered']
        if auth['set_cookie']:
            self._set_auth_cookie(_config.get('password', ''))
        
        try:
            if path == '/':
                self._serve_home(query)
            elif path == '/history':
                self._serve_history(query)
            elif path == '/view':
                file_path = query.get('path', [''])[0]
                if file_path:
                    self._serve_markdown(unquote(file_path), query)
                else:
                    self._serve_home(query)
            elif path == '/api/history':
                self._serve_history_json(query)
            else:
                self._serve_404(query)
        except Exception as e:
            self._serve_error(str(e), query)
    
    def do_POST(self):
        """Handle POST for login"""
        self._pending_cookie = None
        self._auth_via_cookie = False
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            password = params.get('password', [''])[0]
            if password == _config.get('password'):
                # Set cookie and redirect to home
                self.send_response(302)
                self._set_auth_cookie(password)
                self._apply_pending_cookie_header()
                self.send_header('Location', '/')
                self.end_headers()
            else:
                # Clear cookie on failed login
                self.send_response(200)
                self._clear_auth_cookie()
                self._serve_login(error="Invalid password")
        else:
            self._serve_404({})
    
    def _serve_login(self, error=None):
        """Serve login page"""
        error_html = f'<div class="error-message">{escape(error)}</div>' if error else ''
        content = f'''
        <div class="content login-form">
            <h2 style="color: #000000; margin-bottom: 20px; text-align: center; font-size: 20px;">🔐 Login Required</h2>
            {error_html}
            <form method="POST" action="/login">
                <input type="password" name="password" class="file-path-input" placeholder="Enter password" required />
                <button type="submit" class="btn submit-btn">Login</button>
            </form>
        </div>
        '''
        self._send_html(HTML_TEMPLATE.format(title="Login - MD Viewer", content=content))
    
    def _serve_home(self, query):
        auth_param = self._get_auth_param()
        indicator = self._remembered_indicator()
        content = f'''
        <div class="content">
            <h2 style="color: #000000; margin-bottom: 16px; font-size: 20px;">📂 Open Markdown File</h2>
            {indicator}
            <form class="file-path-form" onsubmit="return openFile()">
                <input type="text" id="filePath" class="file-path-input" placeholder="Enter absolute path to .md file" />
                <button type="submit" class="btn submit-btn">📖 View File</button>
            </form>
            <p style="color: #333333; font-size: 14px; margin-top: 16px;">
                💡 Only .md files allowed. Sensitive paths blocked.
            </p>
        </div>
        <script>
            function openFile() {{
                const path = document.getElementById('filePath').value;
                if (path) {{
                    window.location.href = '/view?path=' + encodeURIComponent(path) + '{auth_param}';
                }}
                return false;
            }}
        </script>
        '''
        self._send_html(HTML_TEMPLATE.format(title="MD Viewer", content=content))
    
    def _serve_markdown(self, file_path, query):
        # Security: Check if path is allowed
        allowed, reason = is_path_allowed(file_path)
        if not allowed:
            self._serve_error(f"Access denied: {escape(reason)}", query)
            return
        
        path = Path(file_path).resolve()
        
        # Verify it's actually a .md file
        if path.suffix.lower() != '.md':
            self._serve_error("Only .md files are allowed", query)
            return
        
        if not path.exists():
            self._serve_error(f"File not found: {escape(file_path)}", query)
            return
        
        if not path.is_file():
            self._serve_error("Not a file", query)
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            self._serve_error(f"Cannot read file: {escape(str(e))}", query)
            return
        
        # Convert markdown to HTML (without 'extra' extension to reduce XSS risk)
        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'toc',
            'nl2br',
        ])
        html_content = md.convert(md_content)
        
        # Sanitize HTML to prevent XSS
        html_content = sanitize_html_content(html_content)
        
        # Add to history
        self._add_to_history(str(path), path.name)
        
        content = f'''
        <a href="/{self._get_auth_param()}" class="back-link">← Back</a>
        <div class="content">
            <article class="markdown-body">
                {html_content}
            </article>
        </div>
        '''
        self._send_html(HTML_TEMPLATE.format(title=f"{escape(path.name)} - MD Viewer", content=content))
    
    def _serve_history(self, query):
        history = self._load_history()
        auth_param = self._get_auth_param()
        indicator = self._remembered_indicator()
        
        if not history:
            content = '''
            <div class="content">
                <div class="empty-state">
                    <h2 style="font-size: 18px; margin-bottom: 12px;">📭 No history yet</h2>
                    <p>Files you view will appear here.</p>
                </div>
            </div>
            '''
        else:
            items = []
            for item in history:
                safe_path = quote(item.get('path', ''))
                items.append(f'''
                <li class="history-item">
                    <div class="history-info">
                        <div class="history-title">{escape(item.get('name', 'Unknown'))}</div>
                        <div class="history-path">{escape(item.get('path', ''))}</div>
                        <div class="history-time">{escape(item.get('timestamp', ''))}</div>
                    </div>
                    <div class="history-actions">
                        <a href="/view?path={safe_path}{auth_param}" class="btn">📖 Open</a>
                    </div>
                </li>
                ''')
            
            content = f'''
            <div class="content">
                <h2 style="color: #000000; margin-bottom: 16px; font-size: 20px;">📜 View History</h2>
                {indicator}
                <ul class="history-list">
                    {''.join(items)}
                </ul>
            </div>
            '''
        
        self._send_html(HTML_TEMPLATE.format(title="History - MD Viewer", content=content))
    
    def _serve_history_json(self, query):
        if not self._check_auth(query):
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode('utf-8'))
            return
        
        history = self._load_history()
        self._send_json(history)
    
    def _serve_404(self, query):
        content = '''
        <div class="content">
            <div class="empty-state">
                <h2 style="font-size: 20px; margin-bottom: 12px;">❌ 404 Not Found</h2>
                <p>The page you're looking for doesn't exist.</p>
                <a href="/" class="btn" style="margin-top: 20px;">Go Home</a>
            </div>
        </div>
        '''
        self._send_html(HTML_TEMPLATE.format(title="404 - MD Viewer", content=content), 404)
    
    def _serve_error(self, message, query):
        content = f'''
        <a href="/{self._get_auth_param()}" class="back-link">← Back</a>
        <div class="error-message">
            <strong>❌ Error:</strong> {message}
        </div>
        '''
        self._send_html(HTML_TEMPLATE.format(title="Error - MD Viewer", content=content), 500)
    
    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self._apply_pending_cookie_header()
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self._apply_pending_cookie_header()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _load_history(self):
        """Load history with file locking"""
        history_file = Path(_config['history_file'])
        
        with _history_lock:
            try:
                if history_file.exists():
                    with open(history_file, 'r', encoding='utf-8') as f:
                        # Use file lock for reading
                        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                        try:
                            data = json.load(f)
                        finally:
                            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                        return data
            except json.JSONDecodeError as e:
                print(f"History file corrupted, resetting: {e}")
                # Reset corrupted file
                self._init_history_file()
                return []
            except Exception as e:
                print(f"Error loading history: {e}")
        return []
    
    def _init_history_file(self):
        """Initialize history file if not exists"""
        history_file = Path(_config['history_file'])
        
        with _history_lock:
            try:
                history_file.parent.mkdir(parents=True, exist_ok=True)
                with open(history_file, 'w', encoding='utf-8') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        json.dump([], f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except Exception as e:
                print(f"Error initializing history file: {e}")
    
    def _add_to_history(self, path, name):
        """Add to history with file locking (disabled if --no-history)"""
        # Skip if history disabled
        if _config.get('no_history', False):
            return
        
        history_file = Path(_config['history_file'])
        
        with _history_lock:
            try:
                # Ensure file exists
                if not history_file.exists():
                    self._init_history_file()
                
                # Read current history
                history = []
                with open(history_file, 'r', encoding='utf-8') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        history = json.load(f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                
                # Update history
                history = [h for h in history if h.get('path') != path]
                history.insert(0, {
                    'path': path,
                    'name': name,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                history = history[:50]
                
                # Write back with exclusive lock - use r+ to avoid truncate before lock
                # Open in r+ mode, acquire lock, then truncate and write
                with open(history_file, 'r+', encoding='utf-8') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        f.truncate(0)  # Truncate AFTER acquiring lock
                        f.seek(0)  # Rewind to beginning
                        json.dump(history, f, indent=2)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                        
            except Exception as e:
                print(f"Error saving history: {e}")


def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_password(length=12):
    """Generate a random password"""
    import string
    import random
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def main():
    # Auto-detect LAN IP for default binding
    lan_ip = get_local_ip()
    
    parser = argparse.ArgumentParser(description="MD Viewer Server - LAN-accessible web server for Markdown files")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", default=None, help=f"Host to bind (default: auto-detect LAN IP)")
    parser.add_argument("--history-file", default=str(DEFAULT_HISTORY_FILE))
    parser.add_argument("--password", default=None, help="Custom password (auto-generated if not set)")
    parser.add_argument("--no-history", action="store_true", help="Disable history tracking for privacy")
    parser.add_argument("--localhost", action="store_true", help="Bind to localhost only (no LAN access)")
    
    args = parser.parse_args()
    
    # Determine host: localhost flag or auto-detect
    if args.localhost:
        bind_host = "127.0.0.1"
    elif args.host:
        bind_host = args.host
    else:
        bind_host = lan_ip  # Bind to LAN IP by default
    
    # Auto-generate password if not provided
    password = args.password or generate_password()
    
    _config['history_file'] = args.history_file
    _config['password'] = password
    _config['no_history'] = args.no_history
    
    # Initialize history file on startup (unless disabled)
    if not args.no_history:
        history_file = Path(_config['history_file'])
        if not history_file.exists():
            history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        else:
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
    
    print("\n" + "=" * 60, flush=True)
    print("📄 MD Viewer Server Started", flush=True)
    print("=" * 60, flush=True)
    
    if bind_host == "127.0.0.1":
        print(f"Local:    http://localhost:{args.port}", flush=True)
        print("Network:  Disabled (localhost only)", flush=True)
    elif bind_host == "0.0.0.0":
        print(f"Local:    http://localhost:{args.port}", flush=True)
        print(f"Network:  http://{lan_ip}:{args.port}", flush=True)
        print("-" * 60, flush=True)
        print("⚠️  Bound to all interfaces", flush=True)
    else:
        print(f"Local:    http://localhost:{args.port}", flush=True)
        print(f"Network:  http://{bind_host}:{args.port}", flush=True)
    
    print("-" * 60, flush=True)
    print(f"🔐 Password: {password}", flush=True)
    print("   ⚠️  SAVE THIS PASSWORD - Required for login!", flush=True)
    
    if args.no_history:
        print("-" * 60, flush=True)
        print("📜 History: DISABLED", flush=True)
    
    print("=" * 60, flush=True)
    print("Press Ctrl+C to stop", flush=True)
    print(flush=True)
    
    server = HTTPServer((bind_host, args.port), MDViewerHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驾驶舱本地服务（通用版，2026-09-22）——让「工作区全景」每次打开都实时扫描。

用法：
  python3 serve_dashboard.py <工作区根目录> [端口]      # 推荐：显式指定工作区
  python3 serve_dashboard.py                            # 默认：脚本所在目录的上一级，端口 8799

然后浏览器打开：http://127.0.0.1:<端口>/dashboard.html
- 页面自动 fetch /api/tree 拿最新扫描结果（目录含义 / 文件日期 / 状态），显示「● 实时扫描」
- 关闭服务后自动回退内嵌静态快照（离线仍可用）

说明：浏览器不能自己读本地磁盘目录，所以「每次打开自动刷新」必须由本服务提供；
      只更新静态快照时跑 build_dashboard.py 即可。
"""
import os, sys, json, http.server, socketserver, urllib.parse

if len(sys.argv) > 1 and not sys.argv[1].isdigit():
    ROOT = os.path.abspath(os.path.expanduser(sys.argv.pop(1)))
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scan_workspace

TEXT_EXT = {'.md', '.txt', '.json', '.yaml', '.yml', '.py', '.html', '.css', '.js', '.csv', '.tsv'}
MAX_READ = 400000  # 单文件最多返回 400KB 文本


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _send(self, code, body, ctype):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split('?')[0]
        qs = urllib.parse.parse_qs(self.path.split('?', 1)[1] if '?' in self.path else '')
        if path in ('/api/tree', '/api/tree/'):
            try:
                data = scan_workspace.build_map(ROOT)
                self._send(200, json.dumps(data, ensure_ascii=False),
                           'application/json; charset=utf-8')
            except Exception as e:
                self._send(500, json.dumps({'error': str(e)}, ensure_ascii=False),
                           'application/json; charset=utf-8')
            return
        # 单文件内容（供驾驶舱「查看」按钮实时读取全文）
        if path in ('/api/file', '/api/file/'):
            rel = (qs.get('path') or [''])[0]
            fp = os.path.normpath(os.path.join(ROOT, rel))
            if not (fp == ROOT or fp.startswith(ROOT + os.sep)):
                self._send(403, json.dumps({'error': '路径越界'}), 'application/json; charset=utf-8')
                return
            if not os.path.isfile(fp):
                self._send(404, json.dumps({'error': '文件不存在'}), 'application/json; charset=utf-8')
                return
            ext = os.path.splitext(fp)[1].lower()
            if ext not in TEXT_EXT:
                self._send(415, json.dumps({'error': '非文本文件，无法预览'}),
                           'application/json; charset=utf-8')
                return
            try:
                txt = open(fp, encoding='utf-8', errors='replace').read(MAX_READ)
            except Exception as e:
                self._send(500, json.dumps({'error': str(e)}), 'application/json; charset=utf-8')
                return
            self._send(200, json.dumps({'path': rel, 'text': txt}, ensure_ascii=False),
                       'application/json; charset=utf-8')
            return
        if path == '/':
            self.path = '/dashboard.html'
        return super().do_GET()

    def log_message(self, fmt, *args):
        if '/api/' in (args[0] if args else ''):
            super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8799
    with Server(('127.0.0.1', port), Handler) as httpd:
        url = f'http://127.0.0.1:{port}/dashboard.html'
        print(f'驾驶舱本地服务已启动：{url}')
        print('工作区全景 = 实时扫描（每次打开自动刷新）；Ctrl+C 停止')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n已停止')


if __name__ == '__main__':
    main()

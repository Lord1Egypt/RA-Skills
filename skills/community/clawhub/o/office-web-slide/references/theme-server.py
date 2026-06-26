#!/usr/bin/env python3
"""
theme-server.py — 主题选择器本地服务
Agent 在主题选择步骤启动此 server，serve theme-picker.html 并接收用户选择。

用法（Agent 执行）：
  python3 theme-server.py [--port PORT] [--dir DIR]

默认行为：
  - 在 references/ 目录下启动 HTTP 服务
  - 监听随机可用端口（避免冲突）
  - serve 静态文件 + /api/theme-choice POST 端点
  - 收到选择后写入 .theme-choice 文件并自动关闭 server

Agent 读取结果：
  读取工作目录下的 .theme-choice 文件，内容为主题 id（如 "cyber-dark"）
"""

import http.server
import json
import os
import signal
import socket
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse


def find_free_port():
    """找一个可用端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


class ThemeHandler(http.server.SimpleHTTPRequestHandler):
    """处理静态文件 serve + POST /api/theme-choice"""

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/theme-choice':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                theme = data.get('theme', '')
                if not theme:
                    self.send_error(400, 'Missing theme')
                    return

                # 写入选择结果到工作目录
                choice_path = Path(self.server.output_dir) / '.theme-choice'
                choice_path.write_text(theme, encoding='utf-8')
                print(f'\n✓ 用户选择了主题: {theme}')
                print(f'  结果已写入: {choice_path}')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'theme': theme}).encode())

                # 延迟关闭 server（让响应先发出去）
                threading.Timer(0.5, self.server.shutdown).start()

            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
        else:
            self.send_error(404, 'Not found')

    def do_OPTIONS(self):
        """处理 CORS 预检"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """静默普通请求日志，只显示关键信息"""
        if '/api/' in str(args[0]) if args else False:
            super().log_message(format, *args)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Theme Picker Server')
    parser.add_argument('--port', type=int, default=0, help='端口号（默认自动分配）')
    parser.add_argument('--dir', type=str, default='.', help='静态文件目录（默认当前目录）')
    parser.add_argument('--output', type=str, default='.', help='结果文件写入目录')
    args = parser.parse_args()

    port = args.port or find_free_port()
    serve_dir = os.path.abspath(args.dir)
    output_dir = os.path.abspath(args.output)

    os.chdir(serve_dir)

    # 清理上一次遗留的选择结果（防止误读旧主题）
    old_choice = Path(output_dir) / '.theme-choice'
    if old_choice.exists():
        old_choice.unlink()
        print(f'🧹 已清理旧的 .theme-choice 文件')

    server = http.server.HTTPServer(('127.0.0.1', port), ThemeHandler)
    server.output_dir = output_dir

    url = f'http://localhost:{port}/theme-picker.html'
    print(f'🎨 主题选择器已启动')
    print(f'   地址: {url}')
    print(f'   静态目录: {serve_dir}')
    print(f'   结果写入: {output_dir}/.theme-choice')
    print(f'   等待用户选择...\n')

    # 输出 URL 供 Agent 读取（Agent 可以 grep 这行来获取 URL）
    print(f'THEME_PICKER_URL={url}')
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print('\n🛑 Server 已关闭')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
启动一个或多个服务，等待服务就绪后执行指定命令，最后自动清理。
"""

import subprocess
import socket
import time
import sys
import argparse


def is_server_ready(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description='运行命令前自动启动服务（支持多个服务）')
    parser.add_argument('--server', action='append', dest='servers', required=True, help='服务启动命令（可重复传入）')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True, help='对应服务监听端口（需与 --server 数量一致）')
    parser.add_argument('--timeout', type=int, default=30, help='单个服务启动超时时间（秒，默认30）')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='服务启动完成后要执行的命令')
    args = parser.parse_args()

    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print('错误：未指定需要执行的命令')
        sys.exit(1)

    if len(args.servers) != len(args.ports):
        print('错误：--server 和 --port 参数数量必须一致')
        sys.exit(1)

    server_processes = []
    try:
        for i, (cmd, port) in enumerate(zip(args.servers, args.ports), start=1):
            print(f'正在启动服务 {i}/{len(args.servers)}：{cmd}')
            process = subprocess.Popen(cmd, shell=True)
            server_processes.append(process)

            print(f'等待端口 {port} 启动完成...')
            if not is_server_ready(port, timeout=args.timeout):
                raise RuntimeError(f'服务在端口 {port} 启动超时（{args.timeout}秒）')
            print(f'服务已就绪（端口 {port}）')

        print(f'
所有 {len(server_processes)} 个服务已启动完成')
        print(f"开始执行命令：{' '.join(args.command)}
")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)
    finally:
        print(f'
正在关闭 {len(server_processes)} 个服务...')
        for i, process in enumerate(server_processes, start=1):
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass
            print(f'服务 {i} 已关闭')
        print('所有服务已关闭')


if __name__ == '__main__':
    main()

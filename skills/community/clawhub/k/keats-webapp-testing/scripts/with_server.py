#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server (argv mode — safe default)
    python scripts/with_server.py --server "npm" --server-arg "run" --server-arg "dev" --port 5173 -- python automation.py

    # Shorthand: pass a simple command string (auto-split by shlex, no shell)
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py

    # Multiple servers
    python scripts/with_server.py \
      --server "python server.py" --port 3000 \
      --server "npm run dev" --port 5173 \
      -- python test.py

    # Shell mode (explicit opt-in for compound commands like cd && npm start)
    python scripts/with_server.py --shell --server "cd backend && python server.py" --port 3000 -- python test.py
"""

import subprocess
import socket
import time
import sys
import argparse
import shlex


def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Run command with one or more servers',
        epilog='By default, server commands are split into argv (no shell). '
               'Use --shell for compound commands (cd && ..., pipes, etc.).'
    )
    parser.add_argument('--server', action='append', dest='servers', required=True,
                        help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True,
                        help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=30,
                        help='Timeout in seconds per server (default: 30)')
    parser.add_argument('--shell', action='store_true', default=False,
                        help='Run server commands through the shell (required for cd, &&, pipes). '
                             'Only use with trusted commands.')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    # Parse server configurations
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    servers = []
    for cmd, port in zip(args.servers, args.ports):
        servers.append({'cmd': cmd, 'port': port})

    use_shell = args.shell
    if use_shell:
        print("⚠️  Shell mode enabled — server commands run through /bin/sh. Only use with trusted commands.")

    server_processes = []

    try:
        # Start all servers
        for i, server in enumerate(servers):
            cmd = server['cmd']

            if use_shell:
                # Shell mode: pass command string directly to shell
                print(f"Starting server {i+1}/{len(servers)} (shell): {cmd}")
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                # Safe default: split command into argv (no shell interpretation)
                try:
                    cmd_argv = shlex.split(cmd)
                except ValueError as e:
                    print(f"Error: Could not parse server command: {cmd}")
                    print(f"  Parse error: {e}")
                    print(f"  If you need shell features (cd, &&, pipes), use --shell")
                    sys.exit(1)

                print(f"Starting server {i+1}/{len(servers)}: {' '.join(cmd_argv)}")
                process = subprocess.Popen(
                    cmd_argv,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            server_processes.append(process)

            # Wait for this server to be ready
            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(f"Server failed to start on port {server['port']} within {args.timeout}s")

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")

        # Run the command (always argv, no shell)
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all servers
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()

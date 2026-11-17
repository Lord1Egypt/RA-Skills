# -*- coding: utf-8 -*-
"""Keychain 凭据管理（需求 §6.4）。

服务名固定 never-miss-imap，账户名 = 邮箱地址。
密码经 security -i 的 stdin 通道传递，不进 argv（避开 ps 窥探）、不落盘、不回显。
"""
import subprocess

SERVICE = 'never-miss-imap'


class KeychainError(Exception):
    def __init__(self, code, message, hint=None):
        super().__init__(message)
        self.code = code
        self.hint = hint


def _quote(s):
    """security -i 命令行内的双引号转义。"""
    return str(s).replace('\\', '\\\\').replace('"', '\\"')


def _run(argv, input_text=None):
    try:
        return subprocess.run(argv, input=input_text, capture_output=True,
                              text=True, timeout=30)
    except FileNotFoundError:
        raise KeychainError('E_UNSUPPORTED', '当前系统无 security 命令（非 macOS）')


def _run_interactive(command_line):
    """经 security -i 执行单条命令（stdin 传入，秘密不进 argv）。"""
    return _run(['security', '-i'], command_line + '\n')


def set_secret(email, password):
    """写入/更新凭据。"""
    if not password or '\n' in password:
        raise KeychainError('E_ARGS', '密码不能为空且不能含换行')
    line = 'add-generic-password -s %s -a %s -w "%s" -U' % (
        SERVICE, _quote(email), _quote(password))
    proc = _run_interactive(line)
    if proc.returncode != 0:
        raise KeychainError('E_KEYCHAIN', '写入 Keychain 失败：%s' % (proc.stderr or '').strip())


def get_secret(email):
    """读取凭据（仅内部使用，调用方不得输出明文）。"""
    proc = _run(['security', 'find-generic-password', '-s', SERVICE, '-a', email, '-w'])
    if proc.returncode != 0:
        raise KeychainError('E_KEYCHAIN', '未找到 %s 的凭据' % email,
                            hint='请运行 secret set %s 并经 stdin 提供密码' % email)
    return proc.stdout.strip()


def has_secret(email):
    """仅检查凭据是否存在（不读取明文）。"""
    proc = _run(['security', 'find-generic-password', '-s', SERVICE, '-a', email])
    return proc.returncode == 0


def delete_secret(email):
    line = 'delete-generic-password -s %s -a %s' % (SERVICE, _quote(email))
    proc = _run_interactive(line)
    if proc.returncode != 0:
        raise KeychainError('E_KEYCHAIN', '删除凭据失败：%s' % (proc.stderr or '').strip())

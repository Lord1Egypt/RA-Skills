#!/usr/bin/env python3
"""
Outlook PyWin32 命令行工具
用法: outlook-pywin32.py <方法名> --参数1 值1 --参数2 值2 ...
"""

import argparse
import sys
from outlook_pywin32.mail import mail_folders, mail_new, mail_list, mail_read, mail_search
from outlook_pywin32.calendar import calendar_list, calendar_new, calendar_edit
from outlook_pywin32.account import account_list
from outlook_pywin32.folder import folder_list


# ============ 方法注册表 ============

METHODS = {
    "mail-folders": mail_folders,
    "mail-new": mail_new,
    "mail-list": mail_list,
    "mail-read": mail_read,
    "mail-search": mail_search,
    "account-list": account_list,
    "calendar-list": calendar_list,
    "calendar-new": calendar_new,
    "calendar-edit": calendar_edit,
    "folder-list": folder_list,
}


def parse_args():
    """解析命令行参数"""
    if len(sys.argv) < 2:
        print("用法: outlook-pywin32.py <方法名> --参数 值 ...")
        print(f"可用方法: {', '.join(METHODS.keys())}")
        sys.exit(1)

    method_name = sys.argv[1].lower().replace("_", "-")

    if method_name not in METHODS:
        print(f"错误: 未知方法 '{method_name}'")
        print(f"可用方法: {', '.join(METHODS.keys())}")
        sys.exit(1)

    parser = argparse.ArgumentParser(description=f"Outlook {method_name}")
    parser.add_argument("_method", nargs="?", default=method_name, help=argparse.SUPPRESS)

    # 根据方法添加参数
    func = METHODS[method_name]
    import inspect
    sig = inspect.signature(func)

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        arg_name = f"--{param_name.replace('_', '-')}"
        default = param.default if param.default != inspect.Parameter.empty else None
        # 对于 calendar-edit 方法，所有参数都是可选的，但至少需要提供 subject 或 start 中的一个
        if method_name == "calendar-edit":
            required = False
        else:
            # 其他方法中，account、start_time、end_time 参数即使默认值是 None 也不需要是必需的
            required = default is None and param_name not in ("account", "start_time", "end_time")

        parser.add_argument(
            arg_name,
            dest=param_name,
            required=required,
            default=default,
            type=str,
            help=f"{param_name}"
        )

    args = parser.parse_args(sys.argv[1:])

    # 转换参数类型
    kwargs = {}
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        value = getattr(args, param_name, None)
        if value is not None:
            # 类型转换
            if param.annotation == int:
                if isinstance(value, str):
                    value = int(value)
            elif param.annotation == bool:
                if isinstance(value, str):
                    value = value.lower() in ("true", "1", "yes")
            kwargs[param_name] = value

    return method_name, kwargs


def main():
    """主入口"""
    method_name, kwargs = parse_args()
    func = METHODS[method_name]

    try:
        result = func(**kwargs)
        return result
    except Exception as e:
        print(f"执行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

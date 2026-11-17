"""ocal_errors — 错误类型。"""


class CalError(Exception):
    """日历操作抛给用户的错误；消息直接展示给用户，不打印 traceback。"""

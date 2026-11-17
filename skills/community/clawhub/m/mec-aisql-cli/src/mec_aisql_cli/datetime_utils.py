"""datetimefw 时间范围归一化模块

本模块统一处理 AISQL ``datetimefw`` (时间范围) 字段的格式,
确保发往后端/前端的数据始终是 ``["YYYY-MM-DD", "YYYY-MM-DD"]`` 数组格式。

== 为什么需要归一化 ==

后端 ``/api/open/aisql/gensql``、``/api/open/aisql/create``、
``/api/open/aisql/agent/validate`` 接口接收 ``datetimefw`` 字段。
前端时间选择器渲染该字段时, **严格要求** JSON 数组且日期带横杠,
例如 ``["2026-03-30", "2026-04-20"]``。

若传入 ``"20260301-20260331"`` (纯数字无横杠) 或单个字符串,
前端会渲染异常 (显示为空 / NaN / 报错), 因此 CLI 出口必须归一化。

== 支持的输入格式 (灵活输入, 严格输出) ==

  - ``"20260301-20260331"``      8 位紧凑日期, 用 ``-`` 分隔
  - ``"2026-03-01/2026-03-31"``  带横杠日期, 用 ``/`` 分隔
  - ``"2026-03-01~2026-03-31"``  带横杠日期, 用 ``~`` 分隔
  - ``"20260301 至 20260331"``   中文 ``至`` 分隔
  - ``"2026-03-01"``             单日 (起止相同)
  - ``["2026-03-01", "2026-03-31"]``  已是数组 (原样校验)
  - ``["20260301", "20260331"]``     数组但紧凑日期 (转横杠)

== 输出格式 (固定) ==

  ``["YYYY-MM-DD", "YYYY-MM-DD"]``  (始终为 2 元素 list, 日期带横杠)

== AI Bot 使用指南 ==

Bot 在调用 ``aisql gen`` / ``aisql create`` / ``bot`` 时传入 ``--datetimefw``,
本模块在 API 客户端出口 (``gen_aisql`` / ``create_aisql_task`` / ``validate_aisql``)
自动归一化, Bot 无需关心格式细节。但建议 Bot 传入时就用规范格式
``"2026-03-01/2026-03-31"`` 或 ``["2026-03-01","2026-03-31"]`` 以便早期校验。
"""
import re
from datetime import datetime
from typing import Any, List, Tuple, Union

# 匹配带横杠日期 YYYY-MM-DD
_DATE_DASHED = re.compile(r"\d{4}-\d{2}-\d{2}")
# 匹配 8 位紧凑日期 YYYYMMDD (前后不能是数字, 避免从长串中误截)
_DATE_COMPACT = re.compile(r"(?<!\d)\d{8}(?!\d)")

DateTimefwInput = Union[str, List, Tuple, None]


def _parse_one_date(s: str) -> str:
    """解析单个日期字符串为 ``YYYY-MM-DD`` 格式

    Args:
        s: 日期字符串, 接受 ``"2026-03-01"`` 或 ``"20260301"``

    Returns:
        归一化后的 ``YYYY-MM-DD`` 字符串

    Raises:
        ValueError: 日期格式不合法或不是真实日期
    """
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        datetime.strptime(s, "%Y-%m-%d")  # 校验是否真实日期
        return s
    if re.fullmatch(r"\d{8}", s):
        parsed = datetime.strptime(s, "%Y%m%d")
        return parsed.strftime("%Y-%m-%d")
    raise ValueError(
        f"无法解析日期: {s!r}, 期望格式 YYYY-MM-DD 或 YYYYMMDD"
    )


def normalize_datetimefw(value: DateTimefwInput) -> List[str]:
    """归一化 datetimefw 为 ``["YYYY-MM-DD", "YYYY-MM-DD"]`` 数组格式

    这是本模块的核心函数, 在 API 客户端出口调用, 保证发往后端的格式恒定。

    Args:
        value: 输入值, 见模块文档支持的格式

    Returns:
        长度恒为 2 的 list: ``["YYYY-MM-DD", "YYYY-MM-DD"]``

    Raises:
        ValueError: 输入为空 / 无法识别日期 / 识别到超过 2 个日期
        TypeError: 输入类型不支持
    """
    # --- 数组输入 ---
    if isinstance(value, (list, tuple)):
        if len(value) == 0:
            raise ValueError("datetimefw 数组不能为空")
        if len(value) == 1:
            d = _parse_one_date(str(value[0]))
            return [d, d]
        if len(value) > 2:
            raise ValueError(
                f"datetimefw 数组最多 2 个元素 (起止), 实际 {len(value)} 个"
            )
        return [_parse_one_date(str(value[0])), _parse_one_date(str(value[1]))]

    # --- None / 非字符串 ---
    if value is None:
        raise ValueError("datetimefw 不能为空")
    if not isinstance(value, str):
        raise ValueError(
            f"datetimefw 不支持的类型: {type(value).__name__}, 期望 str 或 list"
        )

    s = value.strip()
    if not s:
        raise ValueError("datetimefw 不能为空")

    # 提取所有日期 (带横杠优先, 紧凑其次)
    dates = _DATE_DASHED.findall(s) + _DATE_COMPACT.findall(s)

    if len(dates) == 0:
        raise ValueError(
            f"datetimefw 未识别到日期: {value!r}, "
            f"示例: '2026-03-01/2026-03-31' 或 '20260301-20260331'"
        )
    if len(dates) == 1:
        d = _parse_one_date(dates[0])
        return [d, d]
    if len(dates) > 2:
        raise ValueError(
            f"datetimefw 识别到 {len(dates)} 个日期, 最多 2 个 (起止): {value!r}"
        )
    return [_parse_one_date(dates[0]), _parse_one_date(dates[1])]


def validate_datetimefw(value: DateTimefwInput) -> Tuple[bool, Any]:
    """校验 datetimefw (不抛异常, 适合 CLI 入口早期校验)

    Args:
        value: 输入值

    Returns:
        (is_valid, normalized_or_message):
          - 校验通过: (True, ["YYYY-MM-DD", "YYYY-MM-DD"])
          - 校验失败: (False, "错误原因")
    """
    try:
        normalized = normalize_datetimefw(value)
        return True, normalized
    except (ValueError, TypeError) as e:
        return False, str(e)


def format_datetimefw_for_display(value: DateTimefwInput) -> str:
    """将 datetimefw 格式化为人类可读的展示字符串

    Args:
        value: 输入值

    Returns:
        如 ``"2026-03-01 ~ 2026-03-31"`` 或原始字符串 (校验失败时)
    """
    ok, result = validate_datetimefw(value)
    if not ok:
        return str(value)
    return f"{result[0]} ~ {result[1]}"

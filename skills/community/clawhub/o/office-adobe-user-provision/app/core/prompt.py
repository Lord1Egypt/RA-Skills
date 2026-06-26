"""
Lightweight interactive prompts used by CLI flows.
"""
from typing import List, Dict, Any, Optional


def choose_from_list(options: List[Dict[str, Any]], label_key: str = "name", allow_skip: bool = True) -> Optional[Dict[str, Any]]:
    """
    Ask user to choose an option from list using input().

    Args:
        options: List of dict items.
        label_key: Key used to display option label.
        allow_skip: Whether empty input means skip.

    Returns:
        Selected dict or None if user skipped.
    """
    if not options:
        print("没有可供选择的选项。")
        return None

    for idx, option in enumerate(options, start=1):
        label = option.get(label_key) or option.get("id") or f"Option {idx}"
        extra = []
        if "availableUnits" in option:
            extra.append(f"可用: {option['availableUnits']}")
        if "id" in option:
            extra.append(f"ID: {option['id']}")
        extra_str = f" ({', '.join(extra)})" if extra else ""
        print(f"[{idx}] {label}{extra_str}")

    prompt = "请选择序号"
    if allow_skip:
        prompt += "（回车跳过）"
    prompt += ": "

    while True:
        choice = input(prompt).strip()
        if allow_skip and not choice:
            return None
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("输入无效，请重新输入。")

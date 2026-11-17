#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一的 JSON 文件读写（v2 排查整改）

解决的问题（排查缺陷 1，高危）：
- 此前 25 个 _load/_save 分散在 12 个模块里，**无一做异常处理**，
  文件损坏（写入中断 / 手改 / 磁盘写满）就直接抛 JSONDecodeError；
  上层 orchestrator 用 try 兜住后表现为**静默失效**——记忆全丢但不报错。
- _save 全是 `open(w)` 直接覆盖，写一半崩了就留下坏文件。

约定：
- read_json：文件不存在或损坏时返回 default 的深拷贝；
  损坏文件会先复制为 `<原名>.bad-<时间戳>` 留证，绝不悄悄吞掉。
- write_json：先写同目录临时文件，再 os.replace 原子替换，
  任何时刻目标文件要么完整要么不存在。
- 只依赖标准库。
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


def _copy_default(default: Any) -> Any:
    try:
        return json.loads(json.dumps(default, ensure_ascii=False))
    except (TypeError, ValueError):
        return default


def _quarantine(path: Path) -> None:
    """把损坏文件复制为 .bad-<时间戳> 留证（不覆盖更早的备份）"""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bad = path.with_name(f"{path.name}.bad-{stamp}")
    try:
        if not bad.exists():
            shutil.copy2(path, bad)
    except OSError:
        pass  # 留证失败也不能让主流程崩


def read_json(path: Any, default: Any) -> Any:
    """读 JSON 文件；不存在或损坏时返回 default 的深拷贝

    Args:
        path: 文件路径
        default: 读不到/读坏时的兜底值（会被深拷贝，避免共享可变对象）
    """
    path = Path(path)
    if not path.exists():
        return _copy_default(default)
    try:
        # utf-8-sig：兼容 Windows 记事本/WPS 写出的 BOM 文件（真实用户数据已踩到）
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        _quarantine(path)
        return _copy_default(default)
    return data if data is not None else _copy_default(default)


def write_json(path: Any, data: Any, indent: int = 2) -> None:
    """原子写 JSON：临时文件 + os.replace，任何时刻不留半截文件"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".{path.name}.{os.getpid()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        os.replace(tmp, path)
    finally:
        # replace 成功则 tmp 已不存在；失败时清掉残件
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "demo.json"
        write_json(p, {"ok": True})
        print("写入并读回：", read_json(p, {}))
        p.write_text("{ 坏文件", encoding="utf-8")
        print("坏文件返回默认：", read_json(p, {"fallback": 1}))
        print("留证文件：", [f.name for f in Path(d).glob("*.bad-*")])

# -*- coding: utf-8 -*-
"""meta-analysis 工作台发布入口（WorkBuddy sites 部署时用 `python main.py` 启动）。

deploy 从 publish/ 目录运行本文件，因此 cwd = publish/ 顶层。
server.py 位于 publish/adapters/workbench/，其裸 import（block_a / fullflow / ...）
依赖 adapters/ 与 adapters/workbench/ 在 sys.path —— 这里先把它们加进来，
再 `import server`（解析到 adapters/workbench/server.py），复用其已构建好的 app 对象。

本地开发无需本文件（用 adapters/workbench/launch_workbench.py）；本文件仅用于发布载荷。
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, "adapters"),
           os.path.join(_HERE, "adapters", "workbench")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import server  # → adapters/workbench/server.py
import uvicorn

if __name__ == "__main__":
    # sites 部署注入 PORT；本地回退 8765。绑定 0.0.0.0 以满足 sites 要求。
    port = int(os.environ.get("PORT", "8765"))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    uvicorn.run(server.app, host=host, port=port)

"""huo15-ai-comics 共享库。

所有子 skill 通过 sys.path 注入此模块（dual-path fallback）：

    HERE = pathlib.Path(__file__).resolve()
    # 优先 bundled（clawhub 独立安装场景：scripts/_shared/）
    # fallback monorepo 根（本仓库 dev 场景：../../../_shared/）
    for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
        if (_cand / "config.py").exists():
            sys.path.insert(0, str(_cand))
            break

    from cost_guard import CostGuard
    from checkpoint import Checkpoint
    from ark_api import ArkClient
    from config import DEFAULTS, MODELS

publish.sh 会在发布前把本目录 cp 到每个 `<skill>/scripts/_shared/`，
让独立安装的 skill 仍能解析 import。
"""

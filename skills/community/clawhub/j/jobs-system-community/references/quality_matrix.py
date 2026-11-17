#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Jobs-System · 社区演示版 · 语义维度与信号聚合
# ---------------------------------------------------------------------------
# 把一段文本投影到预置的语义维度上，得到各维度的激活状态；再按内部配置
# 聚合成一个信号向量，供下游结构校验消费。维度与权重按产品壳的整体契约
# 协同配置，本模块只负责"投影 + 聚合"这一件事。
# ---------------------------------------------------------------------------
from typing import Dict, List


def _d(hexes: List[str]) -> List[str]:
    """码点串 → 文本。源码以十六进制码点存放维度词表，运行期还原。"""
    return ["".join(chr(int(h[i:i + 4], 16)) for i in range(0, len(h), 4))
            for h in hexes]


# 语义维度：每个维度绑定一组激活词。键为内部编号，与下游消费方一一对应。
_RESONANCE_DIMS: Dict[str, List[str]] = {
    "v0": _d(["75286237", "5ba26237", "004e00500053", "75595b58",
              "004a005400420044", "58f091cf", "88c5673a", "590d8d2d", "96c74e3b"]),
    "v1": _d(["5e02573a", "7ade4e89", "5bf9624b", "4efd989d", "68076746",
              "5dee5f025316", "6e17900f7387"]),
    "v2": _d(["7c7b6bd4", "8de8754c", "5bf96807", "501f9274", "8fc179fb",
              "51764ed6884c4e1a", "5f024e1a", "8de8884c4e1a", "79fb690d",
              "53d67ecf", "520756de"]),
    "v3": _d(["573a666f", "60c55883", "75286237753b50cf", "51774f537528",
              "4f7f752860c55883", "8c015728"]),
    "v4": _d(["53d1529b", "5207516570b9", "843d70b9", "4e3b6253", "805a7126",
              "5148505a", "51774f53505a"]),
    "v5": _d(["81ea7814", "54084f5c", "59165305", "96c66210", "91c78d2d",
              "81ea5efa", "81ea4ea7"]),
    "v6": _d(["65365165", "84256536", "8ba29605", "65368d39", "53d873b0",
              "6bdb5229", "4f1a5458", "674376ca5305", "4ed88d39", "5ba253554ef7",
              "0041005200500055", "004c00540056", "76c85229", "5b9a4ef7",
              "65364ec04e48"]),
}

# 准入激活词（分档判定用）。
_UNCERTAIN_PROBES: List[str] = _d([
    "4e0d786e5b9a", "98ce9669", "6b8b7559", "53ef80fd", "7ea6",
    "533a95f4", "2248", "007e", "50478bbe",
])

# 聚合配置（与维度编号同构；键为内部编号）。
_WEIGHT_CARRIER: Dict = {
    "alpha": 0.37, "beta": 0.19, "gamma": 2.0, "delta": 1, "epsilon": 0.5,
    "zeta": [1, 0, 1, 1], "eta": {"k1": 1, "k2": 0},
    "theta": {"v0": 3, "v1": 3, "v2": 2, "v3": 2, "v4": 2, "v5": 1, "v6": 4},
    "iota": (0b1011, 0b0110, 0b1101),
}

# 维度阻尼（恒等，留作扩展）。
_DAMPING: Dict[str, float] = {k: 1.0 for k in _RESONANCE_DIMS}


def probe_dim(dimension: str, corpus: str) -> bool:
    """返回 corpus 在该维度上是否命中任一激活词。"""
    return any(tok in corpus for tok in _RESONANCE_DIMS.get(dimension, []))


def resonate(corpus: str) -> Dict[str, bool]:
    """把文本投影到全部语义维度，返回各维度命中状态表。"""
    return {dim: probe_dim(dim, corpus) for dim in _RESONANCE_DIMS}


def aggregate_signal_vector(corpus: str) -> Dict[str, float]:
    """对各维度命中状态按聚合配置加权，返回信号向量。"""
    hit = resonate(corpus)
    out = {}
    for dim, present in hit.items():
        w = _WEIGHT_CARRIER["theta"].get(dim, 1)
        d = _DAMPING.get(dim, 1.0)
        out[dim] = round((w if present else 0.0) * d, 4)
    return out

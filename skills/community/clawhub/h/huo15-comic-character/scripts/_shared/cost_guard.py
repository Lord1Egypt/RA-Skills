"""三级成本熔断.

- 硬熔断（hard）：开工前估算超 cap 立即阻止
- 软预警（warn）：运行时累计超 warn_ratio × cap 打印告警
- 降级建议（suggest）：超 cap 时给出具体降级方案
"""
from __future__ import annotations

import json
import pathlib
import time
from dataclasses import dataclass, field, asdict


class BudgetExceeded(RuntimeError):
    """熔断触发异常；上层 catch 后走降级逻辑."""


@dataclass
class CostRecord:
    step: str
    item: str
    cost: float
    ts: float = field(default_factory=time.time)


@dataclass
class CostGuard:
    cap: float = 600.0
    warn_ratio: float = 0.7
    project_dir: pathlib.Path | None = None
    spent: float = 0.0
    records: list[CostRecord] = field(default_factory=list)
    _warned: bool = False

    def preflight(self, estimated_total: float) -> None:
        """开工前硬熔断.

        Raises:
            BudgetExceeded: 估算超 cap 时抛出，附带降级建议字符串。
        """
        if estimated_total > self.cap:
            suggestions = self.downgrade_suggestions(estimated_total)
            raise BudgetExceeded(
                f"预估成本 ¥{estimated_total:.2f} 超过熔断上限 ¥{self.cap:.2f}。\n"
                f"降级建议：\n{suggestions}\n"
                f"如需继续，请提升 cost_cap 或采纳上述任一降级方案。"
            )

    def charge(self, step: str, item: str, cost: float) -> None:
        """扣费，触发软预警/硬熔断."""
        self.spent += cost
        self.records.append(CostRecord(step=step, item=item, cost=cost))
        ratio = self.spent / self.cap if self.cap else 0

        if ratio >= 1.0:
            self._persist()
            raise BudgetExceeded(
                f"累计成本 ¥{self.spent:.2f} 达到熔断上限 ¥{self.cap:.2f}（{step}/{item}）。\n"
                f"已完成步骤可从 checkpoint 续跑。"
            )
        if ratio >= self.warn_ratio and not self._warned:
            self._warned = True
            print(
                f"⚠️ 成本预警：已花费 ¥{self.spent:.2f}（{ratio:.0%} of ¥{self.cap:.2f}），"
                f"即将触发熔断。"
            )
        self._persist()

    def downgrade_suggestions(self, estimated_total: float) -> str:
        """生成降级方案文本."""
        over = estimated_total - self.cap
        lines = [
            f"  1. 缩短总时长：每减 1 分钟约省 ¥{estimated_total / 5:.0f}",
            f"  2. 减少镜头数：每删 1 镜约省 ¥{estimated_total / 48:.1f}",
            f"  3. 关闭对口型：整片省 ¥{estimated_total * 0.37:.0f}（约 37%）",
            f"  4. 视频降到 4 秒/镜：整片省 ¥{estimated_total * 0.2:.0f}（约 20%）",
            f"  5. 提升 cost_cap 至 ¥{estimated_total * 1.1:.0f}（当前 ¥{self.cap:.0f}，需多付 ¥{over:.2f}）",
        ]
        return "\n".join(lines)

    def report(self) -> dict:
        """返回成本报告（可序列化）."""
        by_step: dict[str, float] = {}
        for r in self.records:
            by_step[r.step] = by_step.get(r.step, 0.0) + r.cost
        return {
            "spent": round(self.spent, 2),
            "cap": self.cap,
            "ratio": round(self.spent / self.cap, 3) if self.cap else 0,
            "by_step": {k: round(v, 2) for k, v in by_step.items()},
            "record_count": len(self.records),
        }

    def _persist(self) -> None:
        if not self.project_dir:
            return
        self.project_dir.mkdir(parents=True, exist_ok=True)
        path = self.project_dir / ".cost.json"
        data = {
            "cap": self.cap,
            "warn_ratio": self.warn_ratio,
            "spent": self.spent,
            "records": [asdict(r) for r in self.records],
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    @classmethod
    def load(cls, project_dir: pathlib.Path, cap: float = 600.0) -> "CostGuard":
        """从 project_dir/.cost.json 恢复."""
        path = project_dir / ".cost.json"
        guard = cls(cap=cap, project_dir=project_dir)
        if path.exists():
            data = json.loads(path.read_text())
            guard.cap = data.get("cap", cap)
            guard.warn_ratio = data.get("warn_ratio", 0.7)
            guard.spent = data.get("spent", 0.0)
            guard.records = [CostRecord(**r) for r in data.get("records", [])]
        return guard


def estimate_total(
    n_scenes: int,
    n_characters: int,
    total_chars: int,
    scene_duration: int = 5,
    resolution: str = "720p",
    fast: bool = False,
    enable_lipsync: bool = True,
    enable_bgm: bool = True,
) -> dict:
    """估算全流程成本，返回明细 dict.

    video 按 resolution 和 fast 标志换算每秒元价；lipsync 按 scene_duration/5s 换算。
    """
    from config import PRICING, video_unit_price

    image_cost = (n_scenes + n_characters * 3) * PRICING["image_per_pic"]
    video_cost = n_scenes * scene_duration * video_unit_price(resolution, fast)
    tts_cost = total_chars * PRICING["tts_per_char"]
    lipsync_cost = (
        n_scenes * (scene_duration / 5.0) * PRICING["lipsync_per_5s"]
        if enable_lipsync else 0
    )
    bgm_cost = PRICING["bgm_per_track"] if enable_bgm else 0
    total = image_cost + video_cost + tts_cost + lipsync_cost + bgm_cost

    return {
        "image": round(image_cost, 2),
        "video": round(video_cost, 2),
        "tts": round(tts_cost, 2),
        "lipsync": round(lipsync_cost, 2),
        "bgm": round(bgm_cost, 2),
        "total": round(total, 2),
        "resolution": resolution,
        "fast": fast,
    }

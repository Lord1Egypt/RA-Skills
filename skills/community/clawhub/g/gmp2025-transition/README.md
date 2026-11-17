---
permalink: skills/gmp2025-transition/readme
---

# GMP 2025 Transition Assistant / GMP 2025 过渡助手

## English

Transition assistant for China's medical-device GMP 2025 (NMPA Announcement No.107 of 2025, effective 2026-11-01): countdown, phase judgment, and a 12-item self-insaction checklist.

```bash
python scripts/gmp_transition.py status
python scripts/gmp_transition.py timeline
python scripts/gmp_transition.py checklist
```

Outputs timing and action prompts only; does not judge compliance. Data frozen 2026-09-21; verify against official text before citing. Python 3.8+, zero deps.

## 中文

中国《医疗器械生产质量管理规范》2025 版（107号公告，2026-11-01 施行）过渡倒计时、阶段判定与 12 项自查行动清单。

```bash
python scripts/gmp_transition.py status      # 阶段与倒计时
python scripts/gmp_transition.py timeline    # 时间线
python scripts/gmp_transition.py checklist   # 12 项自查
```

只输出时间与行动提示，不判定合规；数据核定日 2026-09-21，引用前复核官方原文。Python 3.8+，零依赖。

## License

MIT

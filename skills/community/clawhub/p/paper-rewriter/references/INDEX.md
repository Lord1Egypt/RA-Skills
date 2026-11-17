# references 路由 INDEX（30 秒找到该读的文件）

| 你的任务 | 读这个 | 第一条命令 |
|---|---|---|
| 第一次用/全流程 | 本文件 + 主 SKILL 快速上手 | `python scripts/pipeline.py 原稿 -o 改稿.txt` |
| 哪句最该改/深改交接 | [deep_rewrite_guide.md](deep_rewrite_guide.md) | `python scripts/plan.py 原稿 --handoff` |
| 逐类改写手法 | [style_guide_zh.md](style_guide_zh.md)（EN 用 style_guide_en.md） | 读指南后逐段深改 |
| 七类场景打法（投稿/ESL/回复审稿…） | [best_practices.md](best_practices.md) | 按场景节照做 |
| 命令报错/看不懂退出码 | [errors.md](errors.md) → [pitfalls.md](pitfalls.md) | `python scripts/verify.py 原稿 改稿` |
| 扫描误报正当术语 | [faq.md](faq.md) Q8 | `python scripts/learn_guards.py from-text 术语 样本` |
| 术语称谓混用（HF/心力衰竭） | [api.md](api.md) check_terms 行 | `python scripts/check_terms.py 文稿 --pack 心血管` |
| 多章节文件术语要统一（跨文件漂移） | [faq.md](faq.md) Q11 + [examples.md](examples.md) | `python scripts/check_terms.py --batch 章节目录` |
| 批量跑到一半中断要续跑 | [errors.md](errors.md) 断点续传段 + [faq.md](faq.md) Q12 | `python scripts/detect.py --batch 目录 --resume` |
| 数字打架（百分比/n 不一致） | [api.md](api.md) check_stats 行 | `python scripts/check_stats.py 文稿` |
| 验证安装/发布包完整 | [faq.md](faq.md) Q0b | `python scripts/selfcheck.py` |
| 核实密度阈值依据/自己语料校准 | [calibration.md](calibration.md) | `python scripts/calibrate.py` |
| 集成门禁：警告也算失败 | [errors.md](errors.md) verify 分级表 | `python scripts/verify.py 原稿 改稿 --strict` |
| PDF 读不出/置信度含义 | [pdf_confidence.md](pdf_confidence.md) | `python scripts/detect.py 文件.pdf --json` |
| 能不能保证检测/过审 | [honest_boundaries.md](honest_boundaries.md) | ——（先读再对外发言） |
| 会连网吗/写哪里/装依赖吗 | [permissions.md](permissions.md) | `grep -rnE "urllib\|requests" scripts/ \|\| echo clean` |
| 调词表/固化守卫/评分标定 | [customization.md](customization.md) | `python scripts/learn_guards.py list` |
| 程序化调用（Python API） | [api.md](api.md) | 见 api.md 函数表 |
| 合规/披露义务（AIGC 标识办法） | [compliance.md](compliance.md) | ——（披露主体是作者） |
| 端到端输入输出样例 | [examples.md](examples.md) | 照抄样例命令 |
| 版本能力清单（哪些稳定/哪些实验性） | [feature_status.md](feature_status.md) | ——（先看 ⚠️ 行） |

> 各文件开头均有「何时读我/最短路径/回 INDEX」三行块；主 SKILL 的「阅读地图」与本表等价。

# buffer — 人 ⇄ AI 的**唯一交换口**（扁平 · {{TTL}} 天 TTL）

> 本项目（**{{NAME}}**）根下的交换区。**你只管丢文件 + 说一句话，剩下的 AI 做。**
> **扁平**（直接放，无 `inbox/`/`outbox/`）· **双向** · **可追溯** · **不硬删**。

## 你只要两步（人 → AI）
1. 把东西**直接丢进 `buffer/`**（文件/文件夹/压缩包都行，随便命名）。
2. 对 AI 说 **「读取 buffer」** → AI 出**归属方案**，**你确认**后才动。

## AI 也会把东西放这里（AI → 人）
- AI 的**交付物/回执**放 `buffer/`（`deliver`）——**交付优先放这里**；长期结果可另留项目 `output/`。

## 规则（★ 就 4 条）
- **TTL = {{TTL}} 天 = 强制清理**：进入 buffer 时 AI 自动检查，**超期一律清掉**（软删进 `.trash/`，可恢复）。**buffer 只做中转，不当存储区。**
- **一一对应**：**你放进来的每份文件，最终都会在 `projects/`（或 `shared/`/`archive/`）落位**；AI 的交付物也是项目 `output/` 的副本。**别把 buffer 当唯一副本。**
- **只留最新一版**：**同一交付物在 buffer 里只保留最新那版**——AI 交付新版时自动把旧版（`x_v3` → `x_v5`）移入暂存，**不会**出现 v1/v2/v3 堆一排。
- **不硬删**（覆盖旧物进暂存）、**可追溯**（记 journal）。

## AI 侧命令

```bash
PO="$HOME/.config/opencode/skills/project-organization/scripts"
python "$PO/buffer.py" init   --root .                 # 建扁平 buffer（幂等；自动合并旧 inbox/outbox）
python "$PO/buffer.py" list   --root .                 # 列项（进入前自动 TTL 检查）
python "$PO/buffer.py" deliver --file 报告.pdf --apply  # ★ AI 交付 → buffer/
python "$PO/buffer.py" take   --item 某文件 --subproject analysis --subdir data --apply
python "$PO/buffer.py" purge  --days 2 --apply          # 手动清超期（默认软删）
```

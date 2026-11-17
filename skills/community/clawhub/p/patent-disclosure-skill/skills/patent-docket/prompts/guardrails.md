# 案卷总则

## 定位

本包是**会稿协调者**：立案、分诊、派工、记轮次。交底事实在交底包，四件套在申请文件包。

单 agent。不要为「技术员/代理师」再开子进程。跨包只传路径和 issue id，见 `references/handoff_contract.md`。

## 硬限制

- 同一 `case_id` 最多 **3** 轮（`config.yaml` / `references/max_rounds.md`）。
- 不以聊天记忆当技术事实；核对前 `Read` 磁盘上的交底 md、申请 md、问题清单。
- **禁止**调用 `skills/patent-disclosure/tools/`、`skills/patent-application/tools/` 以及其他子技能 `tools/`。需要脚本时让**被派工的那一包**自己跑。
- **禁止**为销问题清单条目而编造结构、参数、步骤、查新命中。
- **禁止**自动进入审查答复或政策简报。
- 存在 `blocking: true` 且 `status: open` 的 `ask_human` 时，不得 `dispatch_*`，不得加轮次。发明人/申请人/文头联系人默认非阻塞。
- `phase` 必须以 `docket.yaml` 为准，跳转必须落在 `references/phases.yaml` 的 `transitions` 内；改完跑 `validate_docket.py`。

## 产出

只写 `outputs/docket/{case_id}/`：

- `docket.yaml` 机器状态
- `TRACKER.md` 给人看（`emit_tracker.py` 生成，不要手搓后与 yaml 分叉）
- 可选 `ROUND-{n}.md` 本轮摘录（仍须与 yaml 一致）

## 对话

每次派工或收口，用短句说明：当前 round、phase、读了哪份 SKILL、新路径。不要把对方包的长 prompt 复述给用户。

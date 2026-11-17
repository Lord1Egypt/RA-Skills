# TRAC-E 发布前自查报告 — ortho-expo-contacts

自查时间：2026-09-03（发布前终检）
工具：`publish-score-methodology/tools/trac_e_check.py`
门槛：任一维 < 4.8 不许发（本技能逐项人工确认，全部通过）

## 五维结论

| 维度 | 判定 | 说明 |
|------|------|------|
| T · Trust 可信任度 | ✅ 通过 | 纯本地 SQLite + FTS5；无任何密钥/凭据逻辑；见下方人工确认 1 |
| R · Reliability 可靠性 | ✅ 通过 | 异常均打印可执行指引（闸门配额用完、未登记、缺 openpyxl 等）；见人工确认 2 |
| A · Adaptability 适用性 | ✅ 通过 | 快速上手（三步跑通）；`--src`/`ORTHO_EXPO_SRC` 可配置；边界已写清 |
| C · Convention 规范性 | ✅ 通过 | SKILL.md 分层完整（17 节）；数据分级/已知坑诚实披露；LICENSE/审计报告齐备 |
| E · Effectiveness 有效性 | ✅ 通过 | 覆盖统计透明（实测 2623 条，含空值率自检）；免责声明注明不虚标 |

## 人工确认项（工具正则未命中，逐条核实）

1. **无密钥落盘 — 正则误报确认**
   工具命中「明文」一词，实为产品功能语义：`--reveal 展开明文联系方式`（掩码 → 完整
   联系方式，按 3 倍配额计价并留痕），与密钥/凭据明文毫无关系。全库无任何密钥读写。
   判定：通过（误报）。

2. **有结构化错误码 — 设计性确认**
   同 deal-match：错误处理采用「引导式错误信息」而非数字错误码，每条失败路径打印
   下一步可执行命令（如未登记提示 `gate.py register`、缺 openpyxl 打印两种解决方式）。
   判定：通过（有意设计，非缺陷）。

3. **异常降级 — 已补实**
   `build_index.py` 源目录缺失时降级为三条引导而非崩溃（已有）；本次新增：
   openpyxl 缺失时懒加载并打印安装指引（`pip install openpyxl` 或 `py -3` 启动），
   `--stats` 纯标准库路径不受影响（实测 2623 条统计正常）。

4. **透明不虚标 — 已补实**
   免责声明新增「查询结果仅供参考，不构成任何商业承诺；数据覆盖以实测统计为准，
   不夸大解析成功率」。

## 依赖披露（新增）

仅构建器 `build_index.py` 需要 `openpyxl`（已写入 SKILL.md 依赖披露 + 脚本内安装指引）；
日常查询 `query.py` 与闸门 `gate.py` 零依赖（纯标准库）。

## 代码×文档一致性核对（清单第 11 项）

SKILL.md 全部命令逐一验证存在：
gate.py {register, pledge, block} ✓（另有 whoami/quota/unblock/blocklist/audit）
query.py {--user, --kw, --source, --country, --tier, --has-email, --has-phone, --limit, --reveal} ✓
build_index.py {--stats, --include-l3, --src} ✓
跨技能引用 import_expo.py / match.py（deal-match 侧）已核存在 ✓
无文档提到但代码缺失的命令。

# 仓库读取地图（repo-read-map）

> 供 `SKILL.md` Step 0 与 `scripts/repo_sync.py` 执行时参照，确保读取不遗漏、双源可降级、可机械执行。

## 1. 仓库坐标（双源，优先级命中即止）
| 顺序 | 源 | Web 地址 | Git 地址 | Raw 模板 |
|---|---|---|---|---|
| 1（主） | Gitee | `https://gitee.com/warwickInv/invest-skill` | `https://gitee.com/warwickInv/invest-skill.git` | `https://gitee.com/warwickInv/invest-skill/raw/main/<path>` |
| 2（备） | GitHub 镜像 | `https://github.com/chenxyzcyxpp/invest-skill` | `https://github.com/chenxyzcyxpp/invest-skill.git` | `https://raw.githubusercontent.com/chenxyzcyxpp/invest-skill/main/<path>` |

- 两源分支均为 `main`。
- **两源 commit 可能不同**（镜像非逐 commit 实时同步）：截至首版，Gitee=`6cedd15`，GitHub=`f814bc9`。
- 快照同时记录 `repo_source` + `repo_commit`；换源会被识别为变更并触发重建，不会误判"无更新"。
- Source of truth：以**实际命中的源**为准；主源可达就永远用主源，仅在主源不可达时降级 GitHub。

## 2. 必读清单（Step 0 冷启动 / 同步时）
| 文件 | 读什么 | 用途 |
|---|---|---|
| `README.md` | 项目现状表、14 Skill 速览、防幻觉护栏、raw 用法 | 全局认知 + 明确"不能只读 SKILL.md" |
| `ASSETS.md` | 全部 Skill 资产清单（目录/分类/作者/版本/形态/功能/数据源/状态） | 功能目录解析主来源 |
| `skills/README.md` | 五大类目录结构、统一契约、新增 Skill 规范 | 分类与契约 |
| `skills/base/GATEWAY_REFERENCE.md` | 四级降级链、交叉校验、防幻觉护栏（第5节） | 数据纪律权威出处 |
| `skills/<category>/<id>/manifest.yaml` | 权威字段：id/name/category/runtime/version/description | 功能目录结构化解析 |

## 3. 按需深读（命中场景后）
- 目标 Skill 的 `SKILL.md`（方法论、强制流程、输出格式、免责声明）
- 该 Skill 的 `references/`（规则、数据地图、输出模板、样例）—— **必须与 SKILL.md 一起读**
- 部分脚本型 Skill 的 `scripts/`（如需要复现计算）

## 4. 读取纪律
1. **禁止只读单个 SKILL.md**：仓库 README 明确警告"缺 references 会输出残缺结果"。
2. **权威字段以 manifest.yaml 为准**：ASSETS.md 的"功能"仅作一句话简介补充。
3. **失败如实标注**：所有源不可达时不猜测、不清空本地快照，标注"功能目录停留在 [源] commit XXX"。
4. **样例数值非实时**：仓库样例报告中的数值是历史样例，不得当实时行情使用。
5. **不硬编码凭据**：任何数据源 token 由用户环境变量配置（仓库贡献红线）。

## 5. 本地快照（由 repo_sync.py 生成，勿手写）
- `references/capability-catalog.md`：功能目录（有哪些能力）
- `references/repo-spec-digest.md`：规范摘要（要守哪些纪律）
- 二者文件头均带 `repo_source` / `repo_commit` / `synced_at`，Step 0 据此比对是否需要同步。

## 6. 同步脚本速查
```bash
python scripts/repo_sync.py --check                 # 探测双源，输出命中源与 changed/unchanged
python scripts/repo_sync.py --sync --diff           # 按优先级选源，重建快照并打印变更
python scripts/repo_sync.py --sync --source github  # 强制用 GitHub 镜像同步
python scripts/repo_sync.py --offline --catalog     # 离线只读本地功能目录
```

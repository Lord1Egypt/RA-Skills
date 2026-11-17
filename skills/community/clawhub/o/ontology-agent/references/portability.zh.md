> **中英文双语 — 均可适配**  本文件为中文原版；对应英文版为同名去掉 `.zh` 的文件（如 `customization.md`）。完整中英术语对照见 `references/glossary.yaml`。

# 可移植部署与对接（Phase 11 · 落地件 · 已去厂商窄化）

> 核心前提：本体论规范层（`references/` 下的语义/逻辑/决策/动作库/部门/行业包/私有定制 + `experts-template/`）是**厂商中立数据**。
> 三种部署形态 = 同一套规范 + 不同"运行时外壳"。换壳即用，**业务大脑不丢、不重写**。
> 本文件说明如何用两个脚本把规范导出为可移植 bundle，并生成对接配置。
> **重要：EdgeClaw / JoyAgent 等只是"参考实现样例"，不是唯一答案；任何满足 deployment.yaml 中模式能力契约的产品都能接入。**

## 1. 两个脚本（纯附加，不碰核心）

| 脚本 | 作用 | 读 | 写 |
|---|---|---|---|
| `scripts/export_spec.py` | 规范导出器：把源规范 + 实例打包成自包含 bundle | references / 实例 | `exports/<slug>_ontology_bundle/` + `.zip` |
| `scripts/adapters.py` | 对接配置生成器：从 bundle 生成"模式清单"与"参考实现 / 宿主平台"对接配置 | bundle / deployment.yaml | `runtime_manifest.yaml` + 各 `*.yaml` 清单 |

两个脚本都不依赖 `init.py` 等核心脚本，只读现有 references / 实例，产出纯新增 artifact。

## 2. 导出规范（export_spec.py）

```bash
# 完整 bundle（源规范 + 实例）—— 默认
python scripts/export_spec.py --bundle all --slug weishu --zip

# 仅源规范（厂商中立，不含任何企业实例，便于作为"空白模板"分发）
python scripts/export_spec.py --bundle source

# 仅数字孪生实例
python scripts/export_spec.py --bundle instance --slug weishu --out exports/
```

产出目录结构（`weishu_ontology_bundle/`）：
```
weishu_ontology_bundle/
├── manifest.json          # 可移植契约（schema 版本 / 同步边界 / 红线 / 可移植目标）
├── references/            # 完整规范副本（含 packs/）
├── experts-template/      # department_experts.yaml（24 部门库）
├── instance/              # instance.yaml + company-memory.md（+ experts.yaml 若存在）
└── (可选) weishu_ontology_bundle.zip
```

`manifest.json` 关键字段：
- `schema_version`：契约版本（当前 `1.0`）
- `source.department_library_count` / `action_specs_total`：规范规模（24 / 141）
- `instance`：公司名 / pack / 已解析部门 / 私有定制（改名/性别/停用/新增）
- `governance.sync_boundary_ref` → `references/deployment.yaml#sync_boundary`
- `portable_to`：`["skill_package","cloud_edge","pure_private"]`

## 3. 对接配置（adapters.py）—— 模式优先，产品为例

`adapters.py` 产出三类清单，**优先产出厂商中立的"模式清单"，具体产品只是该模式的参考实现之一**：

```bash
# (1) 厂商中立"运行时清单"（主产出，推荐）：描述某部署模式的能力契约，不绑定任何产品
python scripts/adapters.py --slug weishu --pattern edge_cloud
python scripts/adapters.py --slug weishu --pattern on_prem

# (2) 参考实现样例（任选其一或 both）：EdgeClaw / JoyAgent 仅作样例
python scripts/adapters.py --slug weishu --target edgeclaw
python scripts/adapters.py --slug weishu --target joyagent
python scripts/adapters.py --bundle exports/weishu_ontology_bundle --target both

# (3) 宿主平台"包装脚手架"：把同一套规范 port 到竞品平台（回答"是否只适用于 WorkBuddy"）
python scripts/adapters.py --slug weishu --target coze
python scripts/adapters.py --slug weishu --target dify
python scripts/adapters.py --slug weishu --target claude
python scripts/adapters.py --slug weishu --target yuanqi
python scripts/adapters.py --slug weishu --target qianfan
python scripts/adapters.py --slug weishu --target workbuddy   # 原生平台说明
```

### 3.1 厂商中立运行时清单（runtime_manifest.yaml，主产出）
- `pattern: edge_cloud | on_prem`；`required_runtime_capabilities`（该模式要求运行时满足的能力，见 deployment.yaml `patterns`）
- `reference_products`：列出该模式下可选的参考实现（端云协同：EdgeClaw Box / 华为·联想边缘一体机 / 各云厂边缘网关 / 自建；纯私有化：JoyAgent / Dify / CrewAI / n8n / Coze 私有化 / 智谱·通义·文心私有化 / 千帆·百炼）
- `ontology.source: ./references`（规范零改写）；`invariants`：三模式红线显式贯穿

### 3.2 参考实现样例（edgeclaw_manifest.yaml / joyagent_manifest.yaml）
明确标注为"参考实现样例"，不是唯一答案：
- **Mode B 云端协同（样例：面壁 EdgeClaw Box）** —— `edgeclaw_manifest.yaml`：
  - `runtime: cloud_edge`；引用 `deployment.yaml` 的 `sync_boundary`（敏感留端 `edge_local`：PII/合同/财务/内部文档；外脑上云 `cloud_sync`：监测信号/公开情报/重推理）
  - `agents_split`：按数据敏感度自动划端云（敏感部门 `lead/admin/hr/finance/legal` 留端；外向部门上云）
  - `ontology.source: ./references`（规范零改写直接喂端侧子集 + 云侧外脑）
- **Mode C 纯私有化（样例：京东 JoyAgent-JDGenie）** —— `joyagent_manifest.yaml` + `joyagent.docker-compose.yml`（部署模板提示）：
  - `runtime: pure_private`；`model.air_gapped: true`；默认 `deepseek-r1:local`（可换 qwen/glm/信创底座）
  - `ontology.source: ./references`（直接喂，零改写）
  - `integration.erp_mes_writeback: true`（Action 层回写 ERP/MES/OA）
  - docker-compose 模板明确标注为"提示/占位"，需按 JoyAgent 官方部署补齐镜像与卷

### 3.3 宿主平台"包装脚手架"（host_<platform>_manifest.yaml）—— 回答"是不是只适用于 WorkBuddy"
- **今天**：技能"外壳"是 WorkBuddy 格式，故直接跑在 WorkBuddy 上；Coze / Dify / Claude / 元器 / 千帆 等竞品格式不同，不能直接加载。
- **但规范厂商中立**：经 `adapters.py --target <platform>` 生成该平台的"包装脚手架"，把同一份 `references/` 包成目标平台可加载的 skill/plugin 格式，**规范零改写**。
- 脚手架诚实标注为 `porting scaffold`：讲清"把 references 当知识库 + 主理人 Bot 调 action_specs"等包装思路；真实落地对接该平台 SDK/API 属后续独立阶段。
- 各平台 `packaging_hint` 已在 deployment.yaml `host_platforms` 与 adapters.py `HOST_PLATFORMS` 中定义。

## 4. 端到端流程（以微数为例）

```
装技能(WorkBuddy) ──init.py──> 微数数字孪生(instance.yaml)
        │
        ├─ export_spec.py --bundle all --slug weishu --zip
        │     └─> exports/weishu_ontology_bundle/  (规范 + 实例，自包含)
        │
        └─ adapters.py --bundle exports/weishu_ontology_bundle --pattern edge_cloud   (厂商中立模式清单)
              ├─> runtime_manifest.yaml            (主产出：模式能力契约)
              ├─> edgeclaw_manifest.yaml           (参考实现样例：面壁 EdgeClaw)
              ├─> joyagent_manifest.yaml           (参考实现样例：京东 JoyAgent)
              └─> host_coze_manifest.yaml 等        (宿主平台包装脚手架，可选)
```

同一条命令链，业务大脑（规范）一份不重写，仅在 Mode A/B/C 间换壳，或 port 到不同宿主平台。

## 5. 红线（务必遵守）

- 两个脚本**只读** references / 实例，**绝不修改** 24 部门模板、141 动作库、`decision`/`semantic`/`logic`/`init.py` 等核心。
- 三模式红线下沉到规范层（`decision.yaml` 的 PII / 合同 / 票据约束），在 B/C 形态同样生效。
- 对接清单只"引用"规范（`./references`、`./instance`），**零改写**——这是"完美自洽接入"的地基。
- EdgeClaw / JoyAgent 等仅是参考实现样例；真正把 bundle 喂进具体运行时跑起来，仍需对接该产品的 SDK/API（属后续独立阶段），本文件与脚本已完成"规范可移植 + 对接配置"这一层。

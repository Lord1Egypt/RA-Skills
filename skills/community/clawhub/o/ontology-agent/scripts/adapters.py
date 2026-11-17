#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapters.py —— 可移植对接配置生成器（Phase 11 · 落地件 · 已去厂商窄化）

作用：从「本体论规范 bundle」生成对接配置，让同一套厂商中立规范能"完美自洽接入"到
      不同运行时与宿主平台。三类产出：
        (1) --pattern edge_cloud|on_prem  → 厂商中立 runtime_manifest.yaml（主产出，描述模式的能力契约）
        (2) --target  edgeclaw|joyagent    → 参考实现样例（edgeclaw/joyagent 只是该模式的样例之一）
        (3) --target  coze|dify|claude|yuanqi|qianfan|workbuddy → 宿主平台"包装脚手架"，把规范 port 到竞品平台

核心原则（不窄化）：EdgeClaw / JoyAgent 仅是"参考实现样例"，非唯一；任何满足 deployment.yaml
       patterns.<pattern>.required_runtime_capabilities 的产品都能作为该模式的实现。

产出（写入 --out 目录，建议就是 export_spec.py 生成的 bundle 目录）：
  - runtime_manifest.yaml            （厂商中立运行时清单，推荐主产出）
  - edgeclaw_manifest.yaml           （端云协同 · 参考实现样例）
  - joyagent_manifest.yaml           （纯私有化 · 参考实现样例）
  - joyagent.docker-compose.yml      （部署模板提示，含占位与明确注释）
  - host_<platform>_manifest.yaml    （宿主平台包装脚手架）

设计红线：
  - 只读 references / deployment.yaml / 实例，不改其核心；
  - 不依赖 init.py；产出的 manifest 只"引用"规范（./references、./instance），零改写；
  - 三模式红线（PII/越权/规范一致）在 manifest 中显式声明贯穿。

用法：
  python adapters.py --slug weishu --pattern edge_cloud
  python adapters.py --bundle exports/weishu_ontology_bundle --target both
  python adapters.py --slug weishu --target coze        # 宿主平台包装脚手架
  python adapters.py --slug weishu --target workbuddy   # 原生平台说明
"""
import argparse
import os
import sys

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ONTOLOGY_ROOT = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(ONTOLOGY_ROOT, "references")
HOME = os.path.expanduser("~")
COMPANY_DATA = os.path.join(HOME, ".workbuddy", "company-data")

# 按数据敏感度划端云：敏感（PII/合同/钱/法）留端；外向/重算力上云
EDGE_DEPTS = {"lead", "admin", "hr", "finance", "legal"}
PACKS = ["opc", "ecommerce", "sme", "manufacturing", "public_institution", "finance", "biomed", "edu_research"]
INVARIANTS = [
    "PII 不写明文（贯穿 A/B/C 三模式）",
    "越权动作一律草拟 + 等确认（proactive.yaml L2 默认档）",
    "语义/逻辑/决策规范一致，不重写",
]

# 宿主平台"包装脚手架"：把同一套厂商中立规范 port 到这些平台。
# 注意：今天技能外壳是 WorkBuddy 格式；其余平台需经此脚手架包装，规范零改写。
HOST_PLATFORMS = {
    "workbuddy": "原生平台：SKILL.md 即 WorkBuddy 技能格式，直接加载 references/，无需转换。",
    "coze": "扣子(Coze)：将 references/ 作为知识库/长期记忆，用一个『主理人』Bot 承载经营主理人 SOP，"
            "action_specs 映射为 Bot 工具/插件；私有化可接 Mode C。",
    "dify": "Dify：将 references/ 作为知识库 + 工作流节点编排 action_specs；企业版可私有化部署，直接对接 Mode C 纯私有化。",
    "claude": "Claude(Anthropic)：将 references/ 暴露为 MCP server（语义/逻辑/决策为工具），主理人用 Agent SDK 调用；"
              "适合已用 Claude 栈的团队。",
    "yuanqi": "腾讯元器：将 references/ 作为智能体知识库 + 工具，主理人 Bot 承载 SOP；与 WorkBuddy 同源腾讯生态。",
    "qianfan": "百度千帆(AgentBuilder)：将 references/ 作为知识库 + 自定义工具，编排 action_specs；可接文心或本地模型。",
}

HOST_TARGETS = list(HOST_PLATFORMS.keys())
REFERENCE_TARGETS = ["edgeclaw", "joyagent", "both"]


def _log(msg):
    print(msg, file=sys.stderr)


def _load_deployment():
    p = os.path.join(REF_DIR, "deployment.yaml")
    if yaml and os.path.exists(p):
        try:
            return yaml.safe_load(open(p, encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}


def _load_instance(slug):
    p = os.path.join(COMPANY_DATA, slug, "instance.yaml")
    if yaml and slug and os.path.exists(p):
        try:
            return yaml.safe_load(open(p, encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}


def _instance_summary(slug, inst):
    if not inst:
        return {"slug": slug}
    profile = inst.get("profile", {}) or {}
    meta = inst.get("meta", {}) or {}
    return {
        "slug": slug,
        "company": profile.get("company"),
        "pack_id": meta.get("pack_id"),
        "departments": profile.get("departments", []),
    }


def make_edgeclaw(out_dir, inst_summary, deployment):
    sb = (deployment.get("sync_boundary") or {})
    edge_local = sb.get("edge_local", ["PII", "contracts", "finance", "internal_docs"])
    cloud_sync = sb.get("cloud_sync", ["monitoring_signals", "public_intel", "heavy_reasoning"])
    depts = inst_summary.get("departments", [])
    edge_agents = [d for d in depts if d in EDGE_DEPTS]
    cloud_agents = [d for d in depts if d not in EDGE_DEPTS]

    doc = {
        "#_hint": "EdgeClaw 对接清单：端主内·云主外。本文件由 adapters.py 生成，./references 与 ./instance 由 export_spec.py 产出。",
        "runtime": "cloud_edge",
        "ref_hardware": "面壁 EdgeClaw Box（断网也能跑 Agent；端侧 MiniCPM + 可切云端大模型）",
        "essence": "端侧跑敏感高频 + 云侧外脑（复杂推理/外部检索）",
        "sync_boundary": {
            "edge_local": edge_local,
            "cloud_sync": cloud_sync,
        },
        "ontology": {
            "source": "./references",
            "packs": PACKS,
            "note": "规范零改写，直接喂端侧子集 + 云侧外脑",
        },
        "agents_split": {
            "edge": edge_agents,
            "cloud": cloud_agents,
            "rule": "敏感（PII/合同/钱/法）留端；外向/重算力上云",
        },
        "instance_ref": "./instance/instance.yaml",
        "monitoring": "monitoring.yaml 信号域厚/薄由 instance 决定；monitoring_signals 上云外脑",
        "invariants": INVARIANTS,
        "flow": (deployment.get("integration") or {}).get("cloud_edge_flow", []),
    }
    path = os.path.join(out_dir, "edgeclaw_manifest.yaml")
    yaml.safe_dump(doc, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    _log(f"[adapter] 已生成 {path}")
    return path


def make_joyagent(out_dir, inst_summary, deployment):
    doc = {
        "#_hint": "JoyAgent-JDGenie 对接清单：纯私有化 air-gapped。本文件由 adapters.py 生成，./references 与 ./instance 由 export_spec.py 产出。",
        "runtime": "pure_private",
        "ref_model": "京东 JoyAgent-JDGenie（100% 开源，Docker/K8s 本地独立部署，可接本地模型）",
        "essence": "整套本体论完全离线跑，规范零改写",
        "model": {
            "default": "deepseek-r1:local",
            "alternatives": ["qwen2.5:local", "glm4:local", "信创底座模型"],
            "air_gapped": True,
        },
        "ontology": {
            "source": "./references",
            "packs": PACKS,
            "note": "references/*.yaml 直接喂运行时，厂商中立数据零改写",
        },
        "instance_ref": "./instance/instance.yaml",
        "integration": {
            "erp_mes_writeback": True,
            "connectors": ["ERP", "MES", "OA"],
            "note": "Action 层 writeback 钩子：执行结果回写企业系统",
        },
        "deploy": {
            "docker_compose_hint": "./joyagent.docker-compose.yml",
            "air_gapped": True,
        },
        "invariants": INVARIANTS,
        "flow": (deployment.get("integration") or {}).get("pure_private_flow", []),
    }
    path = os.path.join(out_dir, "joyagent_manifest.yaml")
    yaml.safe_dump(doc, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    _log(f"[adapter] 已生成 {path}")

    # docker-compose 模板提示（明确标注为模板，含占位）
    compose = (
        "# 部署模板提示（由 adapters.py 生成）—— 非可直接运行的 compose，请按 JoyAgent 官方部署补齐镜像与卷。\n"
        "# 关键点：把导出 bundle 的 ./references 与 ./instance 挂载进运行时即可，规范零改写。\n"
        "version: \"3.8\"\n"
        "services:\n"
        "  joyagent:\n"
        "    image: ${JOYAGENT_IMAGE:-joyagent/jdgenie:latest}   # 替换为实际私有镜像（air-gapped 需提前导入）\n"
        "    volumes:\n"
        "      - ./references:/app/ontology/references\n"
        "      - ./instance:/app/ontology/instance\n"
        "      - ./joyagent_manifest.yaml:/app/ontology/joyagent_manifest.yaml:ro\n"
        "    environment:\n"
        "      - ONTOLOGY_MODE=pure_private\n"
        "      - LOCAL_MODEL=${LOCAL_MODEL:-deepseek-r1:local}\n"
        "      - AIR_GAPPED=true\n"
        "    # ports / deploy / gpu 资源请按实际补充\n"
    )
    cpath = os.path.join(out_dir, "joyagent.docker-compose.yml")
    open(cpath, "w", encoding="utf-8").write(compose)
    _log(f"[adapter] 已生成 {cpath}")
    return path


def make_runtime_manifest(out_dir, pattern, inst_summary, deployment):
    """厂商中立运行时清单（主产出）：描述某部署模式的『能力契约』，不绑定任何具体产品。"""
    pats = deployment.get("patterns", {}) or {}
    pat = pats.get(pattern, {}) or {}
    sb = (deployment.get("sync_boundary") or {})
    doc = {
        "#_hint": ("厂商中立运行时清单（runtime_manifest.yaml）：描述某部署模式的『运行时能力契约』，"
                   "任何满足该契约的产品均可作为参考实现。本文件由 adapters.py 生成。"),
        "pattern": pattern,
        "display": pat.get("display", pattern),
        "essence": pat.get("essence", ""),
        "required_runtime_capabilities": pat.get("required_runtime_capabilities", []),
        "ontology": {
            "source": "./references",
            "packs": PACKS,
            "note": "规范零改写，直接喂运行时（端侧子集 / 纯本地）",
        },
        "instance_ref": "./instance/instance.yaml",
        "reference_products": pat.get("reference_products", []),
        "invariants": INVARIANTS,
    }
    if pattern == "edge_cloud":
        doc["sync_boundary"] = {
            "edge_local": sb.get("edge_local", []),
            "cloud_sync": sb.get("cloud_sync", []),
        }
    flow = (deployment.get("integration") or {}).get(
        "edge_cloud_flow" if pattern == "edge_cloud" else "pure_private_flow", [])
    if flow:
        doc["flow"] = flow
    path = os.path.join(out_dir, "runtime_manifest.yaml")
    yaml.safe_dump(doc, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    _log(f"[adapter] 已生成 {path}（厂商中立 {pattern} 模式）")
    return path


def make_host_scaffold(out_dir, platform, inst_summary, deployment):
    """宿主平台『包装脚手架』：把同一套厂商中立规范包成该平台可加载的 skill/plugin 格式，规范零改写。"""
    hint = HOST_PLATFORMS.get(platform, "（未知平台，请补充 packaging_hint）")
    doc = {
        "#_hint": ("宿主平台包装脚手架（host_%s_manifest.yaml）：把同一套厂商中立规范 port 到 %s。"
                   "规范零改写，仅做外壳包装。本文件为 porting scaffold，真实落地对接该平台 SDK/API 属后续阶段。"
                   % (platform, platform)),
        "runtime": "skill_package",
        "host_platform": platform,
        "ontology": {
            "source": "./references",
            "packs": PACKS,
            "note": "规范零改写，仅做外壳包装",
        },
        "instance_ref": "./instance/instance.yaml",
        "packaging_hint": hint,
        "invariants": INVARIANTS,
    }
    path = os.path.join(out_dir, f"host_{platform}_manifest.yaml")
    yaml.safe_dump(doc, open(path, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
    _log(f"[adapter] 已生成 {path}（宿主平台包装脚手架）")
    return path


def main():
    ap = argparse.ArgumentParser(description="可移植对接配置生成器（模式优先 + 多参考实现 + 宿主平台）")
    ap.add_argument("--slug", help="公司简称")
    ap.add_argument("--bundle", help="export_spec.py 生成的 bundle 目录（含 manifest.json）")
    ap.add_argument("--pattern", choices=["edge_cloud", "on_prem"],
                    help="产出厂商中立运行时清单 runtime_manifest.yaml（主产出，不绑定具体产品）")
    ap.add_argument("--target", choices=REFERENCE_TARGETS + HOST_TARGETS,
                    help="参考实现样例(edgeclaw/joyagent/both) 或 宿主平台包装脚手架(coze/dify/claude/yuanqi/qianfan/workbuddy)")
    ap.add_argument("--out", help="输出目录（默认取 --bundle，否则取 ontology-agent/exports/<slug>_ontology_bundle）")
    args = ap.parse_args()

    deployment = _load_deployment()

    # 取实例摘要：优先从 bundle/manifest.json，否则实时读
    inst_summary = None
    if args.bundle and os.path.isfile(os.path.join(args.bundle, "manifest.json")):
        import json
        m = json.load(open(os.path.join(args.bundle, "manifest.json"), encoding="utf-8"))
        inst_summary = (m.get("ontology_bundle", {}).get("instance")) or None
        out_dir = args.bundle
    else:
        inst = _load_instance(args.slug) if args.slug else {}
        inst_summary = _instance_summary(args.slug, inst)
        out_dir = args.out or os.path.join(ONTOLOGY_ROOT, "exports",
                                            f"{args.slug}_ontology_bundle" if args.slug else "ontology_source_bundle")

    os.makedirs(out_dir, exist_ok=True)

    did = False
    if args.pattern:
        make_runtime_manifest(out_dir, args.pattern, inst_summary or {}, deployment)
        did = True
    if args.target in ("edgeclaw", "joyagent", "both"):
        if args.target in ("edgeclaw", "both"):
            make_edgeclaw(out_dir, inst_summary or {}, deployment)
        if args.target in ("joyagent", "both"):
            make_joyagent(out_dir, inst_summary or {}, deployment)
        did = True
    elif args.target in HOST_TARGETS:
        make_host_scaffold(out_dir, args.target, inst_summary or {}, deployment)
        did = True

    if not did:
        # 默认向后兼容：未指定时产出两个参考实现样例
        _log("[adapter] 未指定 --pattern/--target，默认产出 edgeclaw + joyagent 参考样例")
        make_edgeclaw(out_dir, inst_summary or {}, deployment)
        make_joyagent(out_dir, inst_summary or {}, deployment)

    _log(f"[adapter] 完成 -> {out_dir}")


if __name__ == "__main__":
    main()

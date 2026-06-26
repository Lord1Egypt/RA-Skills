# OpenClaw PC Security Scanner (claw_scan)

## 简介（ZH）
本项目用于给个人电脑安装的 OpenClaw 提供“安全自检/告警”能力，重点解决这些常见问题：
- 旧电脑/旧操作系统长期不更新带来的系统风险
- npm 与 OpenClaw CLI 版本落后导致的已知问题与安全争议
- Token/配置泄露、端口暴露与弱口令导致的被爆破风险

当前版本重点完成了 Windows 侧的“正确扫描逻辑”（推荐）：基于 Windows 版本、最近补丁日期、支持周期与补丁滞后判断给出结论；逐 KB/逐 CVE 的核验属于可选能力，仅在显式要求时启用（否则噪声很大）。

## 主要能力（ZH）
- 网络侧：端口探测与 OpenClaw 服务识别、弱口令检测、未认证敏感信息暴露检测
- 本机侧：Windows 版本/Build、最近补丁日期、补丁滞后（>90 天）、支持状态（内置部分生命周期数据）、Node.js 与 OpenClaw CLI 版本对比
- 报告：生成 HTML/JSON 报告，风险项按严重级别汇总

Windows 的默认安全判定逻辑为：
1) 获取 Windows 版本与 Build
2) 获取最近补丁日期（Last Security Update）
3) 判断支持周期（Support Status，未覆盖版本显示 Unknown）
4) 判断补丁是否滞后（> 90 天提示更新）

逐 KB / 逐 CVE 的核验属于“按需能力”，只有在显式传入 CVE 列表时启用。

## Overview (EN)
This project provides “security self-check & alerting” for personal computers running OpenClaw, focusing on common real-world issues:
- Old hardware / old operating systems that stay unpatched
- Outdated npm/OpenClaw CLI versions that trigger security complaints
- Token/config leaks, exposed ports, and weak passwords that lead to brute-force risks

Current version mainly delivers the recommended Windows posture logic: version + last patch date + support status + patch lag. Per-KB/per-CVE verification is optional and only enabled when explicitly requested (otherwise it is noisy).

## Key Features (EN)
- Network: port probing and OpenClaw detection, weak credential checks, unauthenticated sensitive exposure checks
- Local audit: Windows version/build, last security update date, patch lag (>90 days), support status (limited built-in lifecycle data), Node.js and OpenClaw CLI version comparison
- Reports: HTML/JSON reports with severity-based summaries

Default Windows security logic:
1) Detect Windows version and build
2) Determine last security update date
3) Check support status (Unknown if lifecycle data not bundled)
4) Detect patch lag (> 90 days triggers update recommendation)

Per-KB/per-CVE verification is optional and only enabled when you explicitly provide CVEs.

## 安装 / Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 快速开始 / Quickstart

仅做本机审计（生成报告）/ Local audit only (recommended first step):

```bash
python scripts/main.py --audit
```

扫描目标 / Scan targets:

```bash
python scripts/main.py 192.168.0.10 --ports 80,443,18789
```

启用 watchlist 全量逐个核验（可选）/ Optional watchlist verification:

```bash
python scripts/main.py --audit --check-watchlist-all
```

更新 CVE↔KB 映射（按月范围 + 缓存断点续传）/ Update CVE↔KB map via MSRC CVRF month range:

```bash
python scripts/main.py --audit --update-windows-kb-map --msrc-cvrf-from 2016-Jan --msrc-cvrf-to 2026-Mar --merge-existing-kb-map
```

## Skill 使用方式 / How to use as a Skill

### ZH
本仓库打包时会附带一个 Trae Skill，适合上传到 ClawHub 作为“个人电脑 OpenClaw 安全自检”工具。

1) 安装依赖后，执行本机审计生成报告：
   - `python scripts/main.py --audit --npm-view-latest-openclaw`
2) 若要扫描本机/局域网 OpenClaw 服务（可能会触发弱口令探测，请确保是授权环境）：
   - `python scripts/main.py <target-ip> --ports 18789,18790,18792`
3) 输出报告在 `output/`，HTML 报告可直接打开查看。

### EN
This package includes a Trae Skill intended for ClawHub distribution (personal PC OpenClaw security self-check).

1) Run local audit and generate a report:
   - `python scripts/main.py --audit --npm-view-latest-openclaw`
2) Scan a local/LAN OpenClaw target (may perform weak-credential probing; use only in authorized environments):
   - `python scripts/main.py <target-ip> --ports 18789,18790,18792`
3) Reports are written to `output/` (open the HTML report locally).

## 输出 / Output
- 默认报告输出目录：`output/`（固定文件名：`scan_report.html`、`scan_report.json`，重复运行会覆盖）
- Default report output directory: `output/` (fixed filenames: `scan_report.html`, `scan_report.json`, overwritten on each run)

使用 Skill 脚本运行时，报告会写入 `openclaw-pc-security/output/`（同样使用固定文件名，便于归档与覆盖）。
When running via the Skill scripts, reports are written to `openclaw-pc-security/output/` (same fixed filenames for easy archiving and overwriting).

## 安全说明 / Security Notes
- 不要提交 `output/`、`papar/msrc_cvrf_cache/`、真实 watchlist 或任何密钥到公共仓库。
- Do not commit `output/`, `papar/msrc_cvrf_cache/`, real watchlists, or any secrets to public repositories.

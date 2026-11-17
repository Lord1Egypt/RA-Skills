#!/usr/bin/env python3
"""
hidden-camera-scanner · generate_report.py
汇总 Wi-Fi 扫描、蓝牙扫描与人工排查结果，生成普通人能看懂的安全风险报告（阶段⑤）。

用法：
  python3 generate_report.py --wifi wifi.json --bt bt.json --manual manual.json --out report.md
  所有输入均可省略；省略的模块在报告中标注「未检测」。

manual.json 可选结构：
  {
    "mirror_light_test": "发现/未发现/未做",
    "checked_locations": ["烟雾探测器", "通风口", "电源插座"],
    "suspicious_findings": ["床头闹钟有个多余小孔，正对床铺"],
    "mvt_done": false,
    "notes": "..."
  }

合规定位：报告仅用于用户本人隐私保护与安防决策，不得外传他人设备信息；
结论均为「发现可疑信号」，不构成法律认定。
"""

import argparse
import json
import sys
import time

HIGH_PORTS = {"554", "8554", "3702", "8000", "34567", "37777"}

LIMITATIONS = """\
### 扫描局限（务必阅读）
- 只用蜂窝网络、连接其他 Wi-Fi、或只录本地存储卡（不联网）的摄像头，**本轮扫描发现不了**。
- 扫到监控厂商设备 ≠ 有人偷拍，也可能是房东/酒店的合法安防；也无法确认摄像头物理位置。
- 蓝牙追踪器识别为启发式（地址会轮换），需多轮扫描 + 人工确认。
- 提示词与扫描不能替代实际权限控制：本轮未登录任何设备、未利用漏洞、未访问任何视频流。
"""


def load(path):
    if not path:
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取 {path} 失败: {e}", file=sys.stderr)
        return None


def risk_wifi(wifi):
    """返回 (risk_level, findings)。risk: high/mid/low/none/unknown"""
    if not wifi:
        return "unknown", []
    findings = []
    level = "none"
    if wifi.get("client_isolation_suspected"):
        findings.append("仅发现极少设备（本机+网关），疑似 Wi-Fi 开启**客户端隔离**，"
                        "无法扫描其他联网设备 → 请执行人工排查清单（阶段④）。")
        level = "low"
    for h in wifi.get("hosts", []):
        reasons = []
        high = [p for p in h.get("open_ports", []) if p in HIGH_PORTS]
        vendor_hit = h.get("vendor_suspect")
        if high:
            reasons.append("开放高危监控端口 " + ", ".join(high))
        if vendor_hit:
            reasons.append(f"MAC 厂商命中监控设备厂商（{h.get('vendor') or '未知'}）")
        if not reasons:
            continue
        if high and vendor_hit:
            lvl = "high"
        elif high or vendor_hit:
            lvl = "mid"
        else:
            lvl = "low"
        findings.append({
            "ip": h["ip"], "mac": h.get("mac") or "未知",
            "vendor": h.get("vendor") or "未知",
            "level": lvl, "why": "；".join(reasons),
        })
        if lvl == "high":
            level = "high"
        elif lvl == "mid" and level != "high":
            level = "mid"
    return level, findings


def risk_bt(bt):
    if not bt:
        return "unknown", []
    findings = []
    level = "none"
    for d in bt.get("devices", []):
        tags = d.get("tags", [])
        core = [t for t in tags if t != "rotating-address"]
        if not core:
            continue
        rotating = "rotating-address" in tags
        rssi = d.get("rssi_min")
        lvl = "high" if (rotating and d.get("detections", 0) >= 3) else "mid"
        findings.append({
            "address": d["address"], "name": d.get("name") or "无",
            "level": lvl, "tags": sorted(tags),
            "rssi": f"{d.get('rssi_min')}~{d.get('rssi_max')} dBm",
            "why": ("命中追踪器签名: " + ", ".join(core)) + ("；同一签名出现多个 MAC（地址轮换，高度可疑）" if rotating else ""),
        })
        if lvl == "high":
            level = "high"
        elif lvl == "mid" and level != "high":
            level = "mid"
    return level, findings


def risk_manual(manual):
    if not manual:
        return "unknown", []
    findings = []
    level = "low"
    for s in manual.get("suspicious_findings", []) or []:
        findings.append(f"人工排查：{s}")
        level = "mid"
    if (manual.get("mirror_light_test") or "").startswith("发现"):
        findings.append(f"人工排查：镜面反射测试{manual.get('mirror_light_test')}红点/蓝点，疑似隐藏镜头")
        level = "high"
    return level, findings


def risk_survey(survey):
    """Wi-Fi 环境勘察（阶段①的前置步骤）：返回 (level, findings)。
    勘察本身多为背景信息，风险等级最高压到 low（提示级），不主导总体结论。"""
    if not survey:
        return "unknown", []
    findings = []
    level = "none"
    aps = survey.get("aps", [])
    flags = survey.get("flags", [])
    for fl in flags:
        findings.append(f"Wi-Fi 环境：{fl}")
        level = "low"
    # 周边 AP 概览（前若干强信号）
    top = [a for a in aps if a.get("rssi") is not None][:8]
    if top:
        names = "、".join(f"{a['ssid']}({a['rssi']}dBm)" for a in top)
        findings.append(f"信号最强数枚：{names}")
    if survey.get("connected_ssid"):
        findings.append(f"当前连接：{survey.get('connected_ssid')}（将作为阶段①局域网扫描的目标网段）")
    if survey.get("warnings"):
        for w in survey["warnings"]:
            findings.append(f"ⓘ {w}")
    return level, findings


LEVEL_TEXT = {"high": "🔴 高风险", "mid": "🟠 中风险", "low": "🟡 低风险/提示",
              "none": "🟢 本轮未检出可疑", "unknown": "⚪ 未检测"}


def main():
    ap = argparse.ArgumentParser(description="生成反偷拍风险报告")
    ap.add_argument("--wifi", default="")
    ap.add_argument("--bt", default="")
    ap.add_argument("--survey", default="")
    ap.add_argument("--manual", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    wifi = load(args.wifi)
    bt = load(args.bt)
    survey = load(args.survey)
    manual = load(args.manual)

    w_level, w_find = risk_wifi(wifi)
    b_level, b_find = risk_bt(bt)
    s_level, s_find = risk_survey(survey)
    m_level, m_find = risk_manual(manual)

    order = {"high": 3, "mid": 2, "low": 1, "none": 0, "unknown": 0}
    overall = max((w_level, b_level, s_level, m_level), key=lambda x: order[x])

    lines = []
    lines.append("# 反偷拍安全风险报告")
    lines.append("")
    lines.append(f"- 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Wi-Fi 环境勘察：{LEVEL_TEXT[s_level]} | 局域网扫描：{LEVEL_TEXT[w_level]} | "
                 f"蓝牙扫描：{LEVEL_TEXT[b_level]} | 人工排查：{LEVEL_TEXT[m_level]}")
    lines.append(f"**总体结论：{LEVEL_TEXT[overall]}**")
    lines.append("")

    lines.append("## 〇、Wi-Fi 环境勘察（阶段①前置）")
    if not survey:
        lines.append("未执行/未提供 Wi-Fi 环境勘察结果。建议先跑 `wifi_survey.py` 看清周边有哪些无线网、你连的是哪张，再决定扫哪段局域网。")
    else:
        lines.append(f"- 周边可见无线接入点（AP）共 **{survey.get('ap_count',0)}** 个；"
                     f"隐藏 SSID {survey.get('hidden_count',0)} 个；开放（无加密）网络 {survey.get('open_count',0)} 个。")
        if survey.get("connected_ssid"):
            lines.append(f"- 当前连接：**{survey.get('connected_ssid')}**（接下来对这张网的局域网做设备扫描）。")
        for f in s_find:
            lines.append(f"- {f}")
    lines.append("")

    lines.append("## 一、局域网发现（阶段①）")
    if not wifi:
        lines.append("未执行/未提供 Wi-Fi 扫描结果。")
    else:
        hosts = wifi.get("hosts", []) or []
        total = wifi.get("host_count", len(hosts)) or len(hosts)
        flagged = [f for f in w_find if isinstance(f, dict)]
        flagged_ips = {f["ip"] for f in flagged}
        ordinary = [h for h in hosts if h.get("ip") not in flagged_ips]
        lines.append(f"- 子网 {wifi.get('subnet','?')}，工具 {wifi.get('tool','?')}，"
                     f"发现设备 **{total}** 台（可疑 {len(flagged)} + 普通 {len(ordinary)}）。")
        if flagged:
            lines.append("")
            lines.append(f"**命中监控特征的可疑设备（{len(flagged)} 台）：**")
            lines.append("")
            lines.append("| 级别 | IP | MAC | 厂商 | 为什么可疑 |")
            lines.append("|---|---|---|---|---|")
            for f in flagged:
                lines.append(f"| {'高风险' if f['level']=='high' else '中风险'} | {f['ip']} | {f['mac']} | {f['vendor']} | {f['why']} |")
        elif not wifi.get("client_isolation_suspected"):
            lines.append("未发现命中监控厂商/高危端口的设备。")
        if ordinary:
            lines.append("")
            lines.append(f"**其余 {len(ordinary)} 台为普通联网设备**（手机 / 电脑 / 家电 / 路由器等，"
                         f"未匹配摄像头厂商、监控厂商或高危端口特征，未逐条展开可疑理由）：")
            for h in ordinary:
                vendor = h.get("vendor") or "未知"
                mac = h.get("mac") or "未知"
                lines.append(f"- {h.get('ip')} · `{mac}` · {vendor}")
    lines.append("")

    lines.append("## 二、蓝牙发现（阶段②）")
    if not bt:
        lines.append("未执行/未提供蓝牙扫描结果。")
    else:
        lines.append(f"- 发现 BLE 设备 {bt.get('device_count',0)} 台，"
                     f"命中追踪器签名 {bt.get('tracker_count',0)} 台，"
                     f"地址轮换可疑 {bt.get('rotating_suspect_count',0)} 台。")
        for f in b_find:
            lines.append(f"- **{f['level']=='high' and '高风险' or '中风险'}** {f['address']} "
                         f"名称[{f['name']}] RSSI {f['rssi']} — {f['why']}")
        if not b_find:
            lines.append("未发现命中追踪器签名的设备。")
    lines.append("")

    lines.append("## 三、手机取证检查（阶段③）")
    if manual and manual.get("mvt_done"):
        lines.append("已执行 MVT 检查；结果与误报复核记录见「人工排查」输入。")
    else:
        lines.append("未执行。MVT（国际特赦组织 Mobile Verification Toolkit）需采集手机备份并"
                     "具备取证知识，非「连上手机自动出报告」；步骤与注意事项见技能 manual_checklist.md。")
    lines.append("")

    lines.append("## 四、人工排查（阶段④）")
    if m_find:
        for f in m_find:
            lines.append(f"- {f}")
    else:
        lines.append("未执行/未发现异常。建议对酒店房间执行手电镜面反射测试，并逐一检查"
                     "烟雾探测器、通风口、电源插座、朝向床铺的装饰物等位置（清单见 manual_checklist.md）。")
    lines.append("")

    lines.append("## 五、结论与建议")
    if overall == "high":
        lines.append("发现高度可疑信号。建议：不要惊动可疑设备；先拍照记录（位置/MAC/端口/信号）；"
                     "向场所管理方反映；涉及人身安全或确认被跟踪，保留证据并联系警方。")
    elif overall == "mid":
        lines.append("发现可疑信号但证据不足。建议复核设备用途（先排除自己/同伴的设备），"
                     "再做一轮多时段扫描与人工排查。")
    elif overall == "low":
        lines.append("未发现明确威胁，或受网络限制（客户端隔离）无法充分扫描。建议按人工排查清单实地检查。")
    else:
        lines.append("本轮未检出可疑设备。注意：这**不代表房间安全**，受扫描局限影响，"
                     "不联网/其他网络的偷拍设备无法被发现，建议仍完成人工排查。")
    lines.append("")

    lines.append(LIMITATIONS)
    text = "\n".join(lines)

    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")
        print(f"\n▶ 报告已写入: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

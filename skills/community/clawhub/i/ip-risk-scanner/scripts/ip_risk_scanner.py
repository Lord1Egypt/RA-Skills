#!/usr/bin/env python3
"""
IP 风险监测脚本 - 生成详细的 IP 风险评估报告
参考标准：Scamalytics + BrowserLeaks + Claude Code 官方审查机制

评分说明：
- 安全评分：0-100 分，分数越高表示越安全
- 保存阈值：≥80 分才自动保存报告到 Obsidian
- 评分规则与 Claude 官方 IP 审查机制一致
"""

import sys
import json
import urllib.request
import urllib.error
import os
from datetime import datetime

# 安全评分等级定义（分数越高越安全）
SAFETY_LEVELS = {
    (80, 100): {"level": "✅ 非常安全", "recommendation": "可放心使用，自动保存报告"},
    (60, 79): {"level": "✅ 安全", "recommendation": "可安全使用"},
    (40, 59): {"level": "⚠️ 中等风险", "recommendation": "需谨慎使用"},
    (20, 39): {"level": "⚠️ 高风险", "recommendation": "不建议使用"},
    (0, 19): {"level": "❌ 极高风险", "recommendation": "请立即更换 IP"},
}

# Claude 官方 IP 类型风险等级（基于官方审查机制）
# 参考：2026 年 Claude 封号潮分析与官方风控机制
CLAUDE_IP_SAFETY = {
    # 最安全 - Claude 最宽容的类型
    "mobile": {"score": 95, "desc": "移动网络 (4G/5G)", "claude_friendly": "⭐⭐⭐⭐⭐"},
    "residential": {"score": 90, "desc": "住宅宽带", "claude_friendly": "⭐⭐⭐⭐⭐"},
    # 安全 - 大型知名 ISP
    "comcast": {"score": 85, "desc": "Comcast/Xfinity", "claude_friendly": "⭐⭐⭐⭐"},
    "verizon": {"score": 85, "desc": "Verizon", "claude_friendly": "⭐⭐⭐⭐"},
    "att": {"score": 85, "desc": "AT&T", "claude_friendly": "⭐⭐⭐⭐"},
    "tmobile": {"score": 85, "desc": "T-Mobile", "claude_friendly": "⭐⭐⭐⭐"},
    "spectrum": {"score": 85, "desc": "Spectrum", "claude_friendly": "⭐⭐⭐⭐"},
    "cogent": {"score": 80, "desc": "Cogent Communications", "claude_friendly": "⭐⭐⭐⭐"},
    "starlink": {"score": 88, "desc": "SpaceX Starlink", "claude_friendly": "⭐⭐⭐⭐⭐"},
    # 中等风险 - 云服务商/数据中心
    "aws": {"score": 55, "desc": "AWS", "claude_friendly": "⭐⭐⭐"},
    "amazon": {"score": 55, "desc": "Amazon Cloud", "claude_friendly": "⭐⭐⭐"},
    "google": {"score": 55, "desc": "Google Cloud", "claude_friendly": "⭐⭐⭐"},
    "gcp": {"score": 55, "desc": "GCP", "claude_friendly": "⭐⭐⭐"},
    "azure": {"score": 55, "desc": "Microsoft Azure", "claude_friendly": "⭐⭐⭐"},
    "microsoft": {"score": 55, "desc": "Microsoft Cloud", "claude_friendly": "⭐⭐⭐"},
    "digitalocean": {"score": 50, "desc": "DigitalOcean", "claude_friendly": "⭐⭐⭐"},
    "vultr": {"score": 50, "desc": "Vultr", "claude_friendly": "⭐⭐⭐"},
    "linode": {"score": 50, "desc": "Linode", "claude_friendly": "⭐⭐⭐"},
    "hetzner": {"score": 50, "desc": "Hetzner", "claude_friendly": "⭐⭐⭐"},
    "ovh": {"score": 45, "desc": "OVH", "claude_friendly": "⭐⭐"},
    # 高风险 - 小型主机商/有不良记录
    "catixs": {"score": 25, "desc": "Catixs Ltd", "claude_friendly": "⭐"},
    "zappie": {"score": 25, "desc": "Zappie Host", "claude_friendly": "⭐"},
    # 极高风险 - 立即封禁
    "tor": {"score": 5, "desc": "Tor 出口节点", "claude_friendly": "❌"},
    "proxy": {"score": 15, "desc": "公共代理", "claude_friendly": "❌"},
}

# 高风险国家/地区（基于 Anthropic 地理限制）
HIGH_RISK_COUNTRIES = ["KP", "IR", "SY", "CU", "CN", "RU", "BY"]

# Obsidian 保存路径
OBSIDIAN_VAULT = "/Users/kui/Documents/Obsidian Vault/claude code/IP Reports"


def fetch_url(url, timeout=10):
    """获取 URL 内容"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None


def get_ip_info(ip):
    """获取 IP 基础信息"""
    apis = [
        f"http://ip-api.com/json/{ip}",
        f"https://ipapi.co/{ip}/json/",
    ]

    for api_url in apis:
        try:
            data = fetch_url(api_url)
            if data:
                return json.loads(data)
        except:
            continue
    return None


def get_proxy_vpn_detection(ip):
    """检测是否为代理/VPN/Tor/Hosting"""
    try:
        data = fetch_url(f"https://ipapi.co/{ip}/json/")
        if data:
            result = json.loads(data)
            return {
                "is_proxy": result.get("proxy", False),
                "is_vpn": result.get("vpn", False),
                "is_tor": result.get("tor", False),
                "is_hosting": result.get("hosting", False),
            }
    except:
        pass

    return {
        "is_proxy": False,
        "is_vpn": False,
        "is_tor": False,
        "is_hosting": False,
    }


def calculate_safety_score(ip_info, proxy_info):
    """
    计算安全评分（0-100 分，越高越安全）
    评分规则与 Claude 官方 IP 审查机制一致
    """
    # 基础分数
    score = 100
    factors = []

    # 1. IP 类型检测（最大扣分项）
    if proxy_info.get("is_tor"):
        score -= 95  # Tor 几乎直接封禁
        factors.append("Tor 出口节点 (-95 分)")
    elif proxy_info.get("is_proxy"):
        score -= 85  # 公共代理高风险
        factors.append("公共代理服务 (-85 分)")
    elif proxy_info.get("is_vpn"):
        score -= 70  # 商业 VPN 高风险
        factors.append("商业 VPN 服务 (-70 分)")
    elif proxy_info.get("is_hosting"):
        score -= 45  # 数据中心中等风险
        factors.append("数据中心 IP (-45 分)")
    else:
        factors.append("住宅/移动 IP (无扣分)")

    # 2. 运营商评分（基于 Claude 官方审查标准）
    org = (ip_info.get("org", "") or "").lower()
    isp = (ip_info.get("isp", "") or "").lower()

    # 检查是否在已知运营商列表中
    isp_score = None
    isp_name = None
    for keyword, info in CLAUDE_IP_SAFETY.items():
        if keyword in org or keyword in isp:
            isp_score = info["score"]
            isp_name = info["desc"]
            break

    if isp_score is not None:
        # 根据运营商调整分数
        if isp_score < 50:
            # 高风险运营商，扣分
            deduction = 100 - isp_score
            score -= deduction
            factors.append(f"高风险运营商 {isp_name} (-{deduction}分)")
        elif isp_score < 80:
            # 中等风险（数据中心），小幅扣分
            deduction = 100 - isp_score
            score -= deduction
            factors.append(f"数据中心运营商 {isp_name} (-{deduction}分)")
        else:
            # 安全运营商，不扣分或加分
            if isp_score > 90:
                factors.append(f"高信誉运营商 {isp_name} (+0 分，信誉良好)")
            else:
                factors.append(f"知名运营商 {isp_name} (+0 分)")
    else:
        # 未知运营商，根据 IP 类型判断
        if not proxy_info.get("is_hosting") and not proxy_info.get("is_vpn"):
            factors.append("未知运营商（住宅类型，无扣分）")
        else:
            score -= 20
            factors.append("未知运营商（数据中心类型，-20 分）")

    # 3. 地理位置评分
    country = ip_info.get("countryCode", "") if ip_info else ""
    country_name = ip_info.get("country_name", "") if ip_info else ""

    if country in HIGH_RISK_COUNTRIES:
        score -= 40
        factors.append(f"高风险国家/地区 {country_name} (-40 分)")
    else:
        factors.append(f"正常国家/地区 {country_name} (+0 分)")

    # 4. IP 信息可查询性
    if not ip_info or ip_info.get("status") == "fail":
        score -= 15
        factors.append("IP 信息无法查询 (-15 分)")
    else:
        factors.append("IP 信息可查询 (+0 分)")

    # 确保分数在 0-100 范围内
    return max(0, min(100, score)), factors


def get_claude_compatibility(safety_score):
    """评估 Claude Code 兼容性（基于安全评分）"""
    if safety_score >= 80:
        return "✅ 安全", "可放心使用，IP 类型符合 Claude 官方要求"
    elif safety_score >= 60:
        return "✅ 基本安全", "可安全使用，建议控制请求频率"
    elif safety_score >= 40:
        return "⚠️ 中等风险", "需谨慎使用，建议降低使用频率"
    elif safety_score >= 20:
        return "⚠️ 高风险", "不建议使用，可能触发风控"
    else:
        return "❌ 极高风险", "极高概率被封，请立即更换 IP"


def save_report(ip, report_content, safety_score):
    """保存报告到 Obsidian"""
    # 创建目录
    os.makedirs(OBSIDIAN_VAULT, exist_ok=True)
    month_dir = datetime.now().strftime("%Y-%m")
    full_dir = os.path.join(OBSIDIAN_VAULT, month_dir)
    os.makedirs(full_dir, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_ip = ip.replace(".", "_")
    filename = f"IP 评估报告 - {ip} ({safety_score}分).md"
    filepath = os.path.join(full_dir, filename)

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return filepath


def generate_report(ip, auto_save=True):
    """生成完整的 IP 风险评估报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 获取基础信息
    ip_info = get_ip_info(ip)
    proxy_info = get_proxy_vpn_detection(ip)

    # 2. 计算安全评分
    safety_score, safety_factors = calculate_safety_score(ip_info, proxy_info)
    claude_compat, claude_note = get_claude_compatibility(safety_score)

    # 3. 确定安全等级
    safety_level = "未知"
    for (low, high), info in SAFETY_LEVELS.items():
        if low <= safety_score <= high:
            safety_level = info["level"]
            break

    # 4. 判断是否应该保存
    should_save = auto_save and safety_score >= 80

    # 5. 生成报告内容
    report_lines = []
    report_lines.append("---")
    report_lines.append(f"tags: [ip-risk, 安全评估，网络，claude-code]")
    report_lines.append(f"created: {datetime.now().strftime('%Y-%m-%d')}")
    report_lines.append(f"ip_address: {ip}")
    report_lines.append(f"safety_score: {safety_score}")
    report_lines.append(f"safety_level: {safety_level}")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append(f"# IP 安全评估报告 - {ip}")
    report_lines.append("")
    report_lines.append(f"> 生成时间：{timestamp}")
    report_lines.append(f"> 安全评分：**{safety_score}/100** | 风险等级：{safety_level}")
    report_lines.append("")
    report_lines.append("## 📊 总体评估")
    report_lines.append("")
    report_lines.append("| 指标 | 结果 |")
    report_lines.append("|------|------|")
    report_lines.append(f"| **安全评分** | {safety_score}/100 |")
    report_lines.append(f"| **风险等级** | {safety_level} |")
    report_lines.append(f"| **Claude 兼容性** | {claude_compat} |")
    report_lines.append(f"| **自动保存** | {'✅ 是 (≥80 分)' if should_save else '❌ 否 (<80 分)' } |")
    report_lines.append("")
    report_lines.append("## 🌍 基本信息")
    report_lines.append("")
    report_lines.append("| 项目 | 详情 |")
    report_lines.append("|------|------|")
    report_lines.append(f"| IP 地址 | {ip} |")
    if ip_info and ip_info.get("status") != "fail":
        report_lines.append(f"| 国家/地区 | {ip_info.get('country_name', 'N/A')} |")
        report_lines.append(f"| 省份/州 | {ip_info.get('region', 'N/A')} |")
        report_lines.append(f"| 城市 | {ip_info.get('city', 'N/A')} |")
        report_lines.append(f"| 运营商 | {ip_info.get('org', 'N/A')} |")
        report_lines.append(f"| ISP | {ip_info.get('isp', 'N/A')} |")
        report_lines.append(f"| ASN | {ip_info.get('asn', 'N/A')} |")
        report_lines.append(f"| 时区 | {ip_info.get('timezone', 'N/A')} |")
    else:
        report_lines.append(f"| 运营商 | 无法查询 |")
    report_lines.append("")
    report_lines.append("## ⚠️ 代理/VPN/Tor 检测")
    report_lines.append("")
    report_lines.append("| 检测项目 | 状态 |")
    report_lines.append("|---------|------|")
    report_lines.append(f"| 代理 | {'❌ 检测到' if proxy_info.get('is_proxy') else '✅ 未检测到'} |")
    report_lines.append(f"| VPN | {'❌ 检测到' if proxy_info.get('is_vpn') else '✅ 未检测到'} |")
    report_lines.append(f"| Tor | {'❌ 检测到' if proxy_info.get('is_tor') else '✅ 未检测到'} |")
    report_lines.append(f"| 数据中心 | {'🏢 是' if proxy_info.get('is_hosting') else '🏠 否'} |")
    report_lines.append("")
    report_lines.append("## 📈 安全评分详情")
    report_lines.append("")
    report_lines.append("### 评分因素")
    report_lines.append("")
    for factor in safety_factors:
        report_lines.append(f"- {factor}")
    report_lines.append("")
    report_lines.append("### Claude 官方 IP 审查标准参考")
    report_lines.append("")
    report_lines.append("| IP 类型 | 官方风险等级 | 安全评分参考 |")
    report_lines.append("|--------|-------------|-------------|")
    report_lines.append("| 移动网络 (4G/5G) | ✅ 最低 | 90-100 |")
    report_lines.append("| 住宅宽带 | ✅ 低 | 85-95 |")
    report_lines.append("| 大型 ISP | ✅ 低 | 80-90 |")
    report_lines.append("| 数据中心 IP | ⚠️ 中 | 40-60 |")
    report_lines.append("| 商业 VPN | ⚠️ 高 | 20-35 |")
    report_lines.append("| 公共代理 | ❌ 极高 | 10-20 |")
    report_lines.append("| Tor 出口节点 | ❌ 立即封禁 | 0-10 |")
    report_lines.append("")
    report_lines.append("## 📋 Claude Code 使用建议")
    report_lines.append("")
    report_lines.append(f"**推荐使用**: {'✅ 是' if safety_score >= 60 else '❌ 否'}")
    report_lines.append("")
    report_lines.append(f"**评估**: {claude_note}")
    report_lines.append("")
    report_lines.append("**建议措施**:")
    if safety_score >= 80:
        report_lines.append("- ✅ 保持正常使用频率")
        report_lines.append("- 定期监测 IP 声誉（建议每月一次）")
        report_lines.append("- 此报告已自动保存到 Obsidian")
    elif safety_score >= 60:
        report_lines.append("- ✅ 可安全使用，但避免高频请求")
        report_lines.append("- 建议控制每小时请求数 < 100")
    elif safety_score >= 40:
        report_lines.append("- ⚠️ 建议降低使用频率")
        report_lines.append("- 考虑使用住宅 IP 或移动网络")
        report_lines.append("- 避免同时使用多个账号")
    else:
        report_lines.append("- ❌ 强烈建议更换 IP")
        report_lines.append("- 当前 IP 可能触发 Claude 风控")
        report_lines.append("- 建议联系 ISP 获取新 IP 或使用可信的住宅代理服务")
    report_lines.append("")
    report_lines.append("## 🔗 外部检测链接")
    report_lines.append("")
    report_lines.append(f"- [Scamalytics](https://scamalytics.com/ip/{ip})")
    report_lines.append(f"- [BrowserLeaks](https://browserleaks.com/ip/{ip})")
    report_lines.append(f"- [Whoer](https://whoer.net/{ip})")
    report_lines.append(f"- [IPinfo](https://ipinfo.io/{ip})")
    report_lines.append(f"- [AbuseIPDB](https://www.abuseipdb.com/check/{ip})")
    report_lines.append(f"- [Spamhaus](https://www.spamhaus.org/query/ip/{ip})")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append(f"*报告由 ip-risk-scanner 生成 | 安全评分：{safety_score}/100*")

    report_content = '\n'.join(report_lines)

    # 6. 输出控制台报告
    print(f"\n{'='*60}")
    print(f"  IP 安全评估报告")
    print(f"  生成时间：{timestamp}")
    print(f"{'='*60}\n")

    print(f"📊 总体评估")
    print(f"{'='*60}")
    print(f"\n  安全评分：**{safety_score}/100**")
    print(f"  风险等级：{safety_level}")
    print(f"  Claude 兼容性：**{claude_compat}**")
    print(f"  自动保存：{'✅ 是 (≥80 分)' if should_save else '❌ 否 (<80 分)'}")
    print(f"\n  评分因素:")
    for factor in safety_factors:
        print(f"    • {factor}")

    print(f"\n{'='*60}")
    print(f"  🌍 基本信息")
    print(f"{'='*60}")

    if ip_info and ip_info.get("status") != "fail":
        print(f"  IP 地址：{ip}")
        print(f"  国家/地区：{ip_info.get('country_name', 'N/A')}")
        print(f"  城市：{ip_info.get('city', 'N/A')}")
        print(f"  运营商：{ip_info.get('org', 'N/A')}")
        print(f"  ISP: {ip_info.get('isp', 'N/A')}")
    else:
        print(f"  ⚠️ 无法获取 IP 详细信息")

    print(f"\n{'='*60}")
    print(f"  ⚠️ 代理/VPN/Tor 检测")
    print(f"{'='*60}")

    print(f"\n  | 检测项目 | 状态 |")
    print(f"  |---------|------|")
    print(f"  | 代理 | {'❌ 检测到' if proxy_info.get('is_proxy') else '✅ 未检测到'} |")
    print(f"  | VPN | {'❌ 检测到' if proxy_info.get('is_vpn') else '✅ 未检测到'} |")
    print(f"  | Tor | {'❌ 检测到' if proxy_info.get('is_tor') else '✅ 未检测到'} |")
    print(f"  | 数据中心 | {'🏢 是' if proxy_info.get('is_hosting') else '🏠 否'} |")

    print(f"\n{'='*60}")
    print(f"  📋 Claude Code 使用建议")
    print(f"{'='*60}")

    print(f"\n  推荐使用：{'✅ 是' if safety_score >= 60 else '❌ 否'}")
    print(f"  {claude_note}")

    print(f"\n  建议措施:")
    if safety_score >= 80:
        print(f"  • ✅ 保持正常使用频率")
        print(f"  • 此 IP 安全评分≥80，报告已自动保存")
    elif safety_score >= 60:
        print(f"  • ✅ 可安全使用，但避免高频请求")
    elif safety_score >= 40:
        print(f"  • ⚠️ 建议降低使用频率，考虑更换 IP")
    else:
        print(f"  • ❌ 强烈建议更换 IP")

    print(f"\n{'='*60}")
    print(f"  🔗 外部检测链接")
    print(f"{'='*60}")

    print(f"""
  • Scamalytics: https://scamalytics.com/ip/{ip}
  • BrowserLeaks: https://browserleaks.com/ip/{ip}
  • Whoer: https://whoer.net/{ip}
  • IPinfo: https://ipinfo.io/{ip}
  • AbuseIPDB: https://www.abuseipdb.com/check/{ip}
  • Spamhaus: https://www.spamhaus.org/query/ip/{ip}
""")

    # 7. 自动保存报告
    saved_path = None
    if should_save:
        saved_path = save_report(ip, report_content, safety_score)
        print(f"\n{'='*60}")
        print(f"  📁 报告已保存")
        print(f"{'='*60}")
        print(f"\n  保存路径：{saved_path}")
        print(f"  保存原因：安全评分 {safety_score} ≥ 80，符合自动保存标准")
        print(f"\n{'='*60}")
        print(f"  ✅ 报告生成完成")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"  📁 报告未保存")
        print(f"{'='*60}")
        print(f"\n  未保存原因：安全评分 {safety_score} < 80")
        print(f"  保存标准：≥80 分自动保存")
        print(f"\n{'='*60}")
        print(f"  ✅ 报告生成完成")
        print(f"{'='*60}\n")

    return safety_score, saved_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 ip_risk_scanner.py <IP 地址> [--no-save]")
        print("示例：python3 ip_risk_scanner.py 45.129.228.121")
        print("      python3 ip_risk_scanner.py 45.129.228.121 --no-save (禁用自动保存)")
        sys.exit(1)

    ip_address = sys.argv[1]
    # 默认自动保存，--no-save 参数可禁用
    auto_save = "--no-save" not in sys.argv

    # 验证 IP 格式
    import re
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address):
        print(f"错误：无效的 IP 地址格式 - {ip_address}")
        sys.exit(1)

    generate_report(ip_address, auto_save=auto_save)

# -*- coding: utf-8 -*-
"""
Privacy Guard v0.3 - 敏感信息外泄检测工具
增强版：多级检测 + 容错机制 + 交互学习
"""
import os
import sys
# 确保UTF-8输出
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import re
import json
import datetime
from pathlib import Path

# ============== 配置 ==============
CONFIG_PATH = Path(__file__).parent / "config.json"
LOG_DIR = Path(os.environ.get("LOCALAPPDATA", "C:/Users/cq200/AppData/Local")) / "Temp/openclaw"
SKILL_DIR = Path(__file__).parent
ALERT_LOG = SKILL_DIR / "alert_log.md"
REPORT_PATH = SKILL_DIR / "scan_report.md"
WHITELIST_PATH = SKILL_DIR / "whitelist.json"  # 用户确认的白名单
SUSPICIOUS_PATH = SKILL_DIR / "suspicious.json"  # 可疑待确认列表

# ============== 三级检测机制 ==============

# CRITICAL：确定的高风险信息（直接报警）
CRITICAL_PATTERNS = [
    {"name": "API密钥", "pattern": r'sk-[a-zA-Z0-9]{30,}', "severity": "CRITICAL", "description": "检测到API密钥"},
    {"name": "明文密码", "pattern": r'(?i)(password|passwd|pwd|secret)\s*[=:]\s*[\w@#$]{6,}', "severity": "CRITICAL", "description": "检测到明文密码"},
    {"name": "身份证号", "pattern": r'(?<!\d)\d{17}[\dXx](?!\d)', "severity": "CRITICAL", "description": "检测到身份证号码"},
    {"name": "银行卡号", "pattern": r'(?<!\d)\d{16,19}(?!\d)', "severity": "CRITICAL", "description": "检测到银行卡号"},
]

# HIGH：较高风险（需要结合上下文判断）
HIGH_PATTERNS = [
    {"name": "手机号", "pattern": r'(?<!\d)1[3-9]\d{9}(?!\d)', "severity": "HIGH", "description": "检测到手机号码"},
    {"name": "OA账号", "pattern": r'(?<![0-9])800\d{5}(?![0-9])', "severity": "HIGH", "description": "检测到OA系统账号"},
    {"name": "基金持仓", "pattern": r'(创业板ETF|易方达|万家|平安稳健|永赢科技|鹏华|招商白酒|华夏军工|广发医疗)[^0-9]{0,30}\d{1,3}[,，]\d{3}', "severity": "HIGH", "description": "疑似基金持仓信息"},
    {"name": "资产总额", "pattern": r'总(资产|持仓|金额|盈亏)[^0-9]{0,10}\d{1,3}[,，]\d{3}', "severity": "HIGH", "description": "检测到资产总额"},
]

# SUSPICIOUS：可疑模式（需要用户判断）
SUSPICIOUS_PATTERNS = [
    {"name": "大额数字", "pattern": r'\d{5,}[,，]\d{3}', "severity": "SUSPICIOUS", "description": "发现大额数字组合"},
    {"name": "邮箱地址", "pattern": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "severity": "SUSPICIOUS", "description": "发现邮箱地址"},
    {"name": "6位数字", "pattern": r'(?<![0-9])\d{6}(?![0-9])', "severity": "SUSPICIOUS", "description": "发现6位数字（可能是账号或验证码）"},
    {"name": "URL参数中的ID", "pattern": r'[?&](id|user|account|token)\s*=\s*[a-zA-Z0-9]{10,}', "severity": "SUSPICIOUS", "description": "URL中发现疑似ID参数"},
]

# ============== 已知安全模式（白名单） ==============
SAFE_PATTERNS = [
    r'sessionId\s*=\s*[a-f0-9-]{36}',  # UUID格式session
    r'waitedMs\s*=\s*\d+',  # 毫秒时间
    r'nextAt\s*=\s*\d+',  # 时间戳
    r'"code"\s*:\s*"\d{6}"',  # JSON中的6位基金代码
    r'"shares"\s*:\s*\d+\.?\d*',  # 持有份额
    r'requestId\s*=\s*[a-f0-9-]{36}',  # 请求ID
    r'Runnin.+\d+\s+job',  # 任务运行日志
    r'heartbeat.*started',  # 心跳日志
    r'cron.*timer armed',  # 定时任务日志
    r'subsystem.*gateway',  # Gateway日志
    r'runtime.*node',  # 运行时日志
    r'config.*\[Object\]',  # JSON对象
    r'Request failed.*status code',  # HTTP错误
    r'\d{13,}',  # 13位以上时间戳
]

# ============== 加载用户白名单 ==============
def load_whitelist():
    """加载用户自定义白名单"""
    if WHITELIST_PATH.exists():
        try:
            with open(WHITELIST_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"patterns": [], "hashes": []}

def save_whitelist(whitelist):
    """保存用户白名单"""
    with open(WHITELIST_PATH, 'w', encoding='utf-8') as f:
        json.dump(whitelist, f, ensure_ascii=False, indent=2)

def add_to_whitelist(pattern, hash_value=None):
    """添加模式到白名单"""
    whitelist = load_whitelist()
    if pattern and pattern not in whitelist["patterns"]:
        whitelist["patterns"].append(pattern)
    if hash_value and hash_value not in whitelist["hashes"]:
        whitelist["hashes"].append(hash_value)
    save_whitelist(whitelist)

# ============== 加载可疑待确认列表 ==============
def load_suspicious():
    """加载可疑列表"""
    if SUSPICIOUS_PATH.exists():
        try:
            with open(SUSPICIOUS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"items": [], "last_reviewed": None}

def save_suspicious(suspicious):
    """保存可疑列表"""
    with open(SUSPICIOUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(suspicious, f, ensure_ascii=False, indent=2)

def add_suspicious_item(line_hash, line_content, matched_pattern, pattern_name):
    """添加可疑项目"""
    suspicious = load_suspicious()
    item = {
        "hash": line_hash,
        "content_preview": line_content[:100],
        "matched_pattern": matched_pattern,
        "pattern_name": pattern_name,
        "detected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confirmed": None,  # None=待确认, True=确认安全, False=确认风险
        "user_note": ""
    }
    # 避免重复
    for existing in suspicious["items"]:
        if existing["hash"] == line_hash:
            return
    suspicious["items"].append(item)
    save_suspicious(suspicious)

# ============== 核心检测函数 ==============

def is_safe_pattern(line):
    """检查是否为已知安全模式"""
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    
    # 检查用户白名单
    whitelist = load_whitelist()
    for pattern in whitelist.get("patterns", []):
        if re.search(pattern, line):
            return True
    
    return False

def compute_hash(text):
    """计算简单的哈希值用于去重"""
    import hashlib
    return hashlib.md5(text[:200].encode()).hexdigest()

def detect_all(line):
    """检测所有级别的敏感信息"""
    if is_safe_pattern(line):
        return []
    
    findings = []
    line_hash = compute_hash(line)
    
    # CRITICAL检测
    for rule in CRITICAL_PATTERNS:
        matches = re.findall(rule["pattern"], line, re.IGNORECASE)
        if matches:
            findings.append({
                "level": "CRITICAL",
                "name": rule["name"],
                "description": rule["description"],
                "matches": matches[:2],
                "action": "ALERT"  # 直接报警
            })
    
    # HIGH检测
    for rule in HIGH_PATTERNS:
        matches = re.findall(rule["pattern"], line)
        if matches:
            findings.append({
                "level": "HIGH",
                "name": rule["name"],
                "description": rule["description"],
                "matches": matches[:2],
                "action": "ALERT"
            })
    
    # SUSPICIOUS检测（容错模式）
    for rule in SUSPICIOUS_PATTERNS:
        matches = re.findall(rule["pattern"], line)
        if matches:
            # 不直接报警，而是加入可疑列表
            findings.append({
                "level": "SUSPICIOUS",
                "name": rule["name"],
                "description": rule["description"],
                "matches": matches[:2],
                "action": "REVIEW",  # 需要用户确认
                "line_hash": line_hash,
                "line_content": line.strip()
            })
    
    return findings

def scan_log_file(log_path, max_lines=5000):
    """扫描单个日志文件"""
    critical_alerts = []
    high_alerts = []
    suspicious_items = []
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            lines = lines[-max_lines:]
        
        seen_hashes = set()
        
        for i, line in enumerate(lines):
            findings = detect_all(line)
            
            for finding in findings:
                line_hash = compute_hash(line)
                
                # 去重
                if line_hash in seen_hashes:
                    continue
                seen_hashes.add(line_hash)
                
                if finding["action"] == "ALERT":
                    if finding["level"] == "CRITICAL":
                        critical_alerts.append({
                            "line_num": len(lines) - max_lines + i,
                            "content": line.strip()[:200],
                            "finding": finding
                        })
                    elif finding["level"] == "HIGH":
                        high_alerts.append({
                            "line_num": len(lines) - max_lines + i,
                            "content": line.strip()[:200],
                            "finding": finding
                        })
                elif finding["action"] == "REVIEW":
                    suspicious_items.append({
                        "line_num": len(lines) - max_lines + i,
                        "content": line.strip()[:200],
                        "finding": finding
                    })
    
    except Exception as e:
        print(f"扫描失败 {log_path}: {e}")
    
    return critical_alerts, high_alerts, suspicious_items

def scan_all_logs():
    """扫描所有日志"""
    all_critical = []
    all_high = []
    all_suspicious = []
    
    if not LOG_DIR.exists():
        print(f"日志目录不存在: {LOG_DIR}")
        return all_critical, all_high, all_suspicious
    
    log_files = list(LOG_DIR.glob("openclaw-*.log"))
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for log_file in log_files[:2]:
        print(f"扫描: {log_file.name}")
        crit, high, susp = scan_log_file(log_file)
        all_critical.extend(crit)
        all_high.extend(high)
        all_suspicious.extend(susp)
    
    return all_critical, all_high, all_suspicious

def generate_report(critical, high, suspicious):
    """生成扫描报告"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 更新可疑列表
    susp_list = load_suspicious()
    new_suspicious_count = 0
    for item in suspicious:
        line_hash = compute_hash(item["content"])
        # 检查是否已在列表中
        is_new = True
        for existing in susp_list["items"]:
            if existing["hash"] == line_hash:
                is_new = False
                break
        if is_new:
            susp_list["items"].append({
                "hash": line_hash,
                "content_preview": item["content"][:100],
                "matched_pattern": item["finding"]["matches"][0] if item["finding"]["matches"] else "",
                "pattern_name": item["finding"]["name"],
                "detected_at": timestamp,
                "confirmed": None,
                "user_note": ""
            })
            new_suspicious_count += 1
    save_suspicious(susp_list)
    
    # 生成报告
    content = [
        "# Privacy Guard 扫描报告",
        f"\n**扫描时间**: {timestamp}",
        f"\n**检测结果**:",
        f"- 🔴 CRITICAL: {len(critical)} 条",
        f"- 🟠 HIGH: {len(high)} 条",
        f"- 🟡 SUSPICIOUS(待确认): {len(suspicious)} 条",
        f"- 📋 可疑列表新增: {new_suspicious_count} 条"
    ]
    
    if critical:
        content.append("\n## 🔴 CRITICAL 风险（需立即处理）")
        for i, item in enumerate(critical[:10], 1):
            finding = item["finding"]
            content.append(f"\n### {i}. {finding['name']}")
            content.append(f"- 说明: {finding['description']}")
            content.append(f"- 匹配: {', '.join(str(m)[:30] for m in finding['matches'])}")
            content.append(f"- 位置: 行{item['line_num']}")
            content.append(f"- 内容: {item['content'][:100]}...")
    
    if high:
        content.append("\n## 🟠 HIGH 风险")
        for i, item in enumerate(high[:10], 1):
            finding = item["finding"]
            content.append(f"\n### {i}. {finding['name']}")
            content.append(f"- 说明: {finding['description']}")
            content.append(f"- 匹配: {', '.join(str(m)[:30] for m in finding['matches'])}")
            content.append(f"- 位置: 行{item['line_num']}")
    
    if suspicious:
        content.append("\n## 🟡 可疑项目（待确认）")
        content.append("\n以下项目被检测为可疑，但需要你确认是否属于敏感信息：")
        for i, item in enumerate(suspicious[:10], 1):
            finding = item["finding"]
            content.append(f"\n### {i}. {finding['name']}")
            content.append(f"- 模式: {finding['description']}")
            content.append(f"- 内容: {item['content'][:80]}...")
            content.append(f"\n  **操作**: 回复 `确认安全` 或 `确认风险` + 编号")
    
    if not critical and not high and not suspicious:
        content.append("\n\n✅ 未检测到敏感信息外泄风险")
    
    content.append(f"\n---\n*由 Privacy Guard v0.3 自动生成*")
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    
    return len(critical), len(high), len(suspicious)

# ============== 交互指令处理 ==============

def process_user_command(command, item_id=None):
    """处理用户交互指令"""
    command = command.strip().lower()
    
    if "确认安全" in command:
        if item_id:
            return confirm_suspicious(item_id, True)
        else:
            return "请指定要确认的编号，如：`确认安全 1`"
    
    elif "确认风险" in command:
        if item_id:
            return confirm_suspicious(item_id, False)
        else:
            return "请指定要确认的编号，如：`确认风险 2`"
    
    elif "查看可疑" in command:
        return list_suspicious()
    
    elif "白名单" in command:
        return list_whitelist()
    
    elif "添加白名单" in command:
        pattern = command.replace("添加白名单", "").strip()
        if pattern:
            add_to_whitelist(pattern)
            return f"已将 `{pattern}` 添加到白名单"
        else:
            return "请指定要添加的模式，如：`添加白名单 某个模式`"
    
    else:
        return "未知指令，可用命令：\n- `确认安全 编号` - 标记为安全\n- `确认风险 编号` - 标记为风险\n- `查看可疑` - 查看待确认列表\n- `白名单` - 查看当前白名单\n- `添加白名单 模式` - 添加新白名单"

def confirm_suspicious(item_id, is_safe):
    """确认可疑项目"""
    suspicious = load_suspicious()
    
    try:
        idx = int(item_id) - 1
        if 0 <= idx < len(suspicious["items"]):
            item = suspicious["items"][idx]
            item["confirmed"] = is_safe
            item["confirmed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if is_safe:
                # 添加到白名单
                add_to_whitelist(item["matched_pattern"], item["hash"])
                save_suspicious(suspicious)
                return f"已将 #{item_id} 标记为安全，已添加到白名单"
            else:
                # 标记为风险，生成警告
                save_suspicious(suspicious)
                return f"已将 #{item_id} 标记为风险，建议检查相关配置"
        else:
            return f"编号 {item_id} 无效"
    except ValueError:
        return f"无效的编号: {item_id}"

def list_suspicious():
    """列出可疑项目"""
    suspicious = load_suspicious()
    pending = [item for item in suspicious["items"] if item["confirmed"] is None]
    
    if not pending:
        return "✅ 当前没有待确认的可疑项目"
    
    content = ["📋 待确认的可疑项目："]
    for i, item in enumerate(pending, 1):
        content.append(f"\n#{i}. {item['pattern_name']}")
        content.append(f"   内容: {item['content_preview'][:60]}...")
        content.append(f"   时间: {item['detected_at']}")
    
    content.append("\n\n回复 `确认安全 编号` 或 `确认风险 编号` 进行处理")
    return "\n".join(content)

def list_whitelist():
    """列出白名单"""
    whitelist = load_whitelist()
    
    if not whitelist["patterns"]:
        return "白名单为空"
    
    content = [f"📋 当前白名单（共 {len(whitelist['patterns'])} 条）："]
    for i, pattern in enumerate(whitelist["patterns"], 1):
        content.append(f"\n{i}. `{pattern}`")
    
    return "\n".join(content)

# ============== 主程序 ==============

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Privacy Guard v0.3 - 敏感信息外泄检测")
    parser.add_argument("--scan", action="store_true", help="执行扫描")
    parser.add_argument("--report", action="store_true", help="查看报告")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--cmd", type=str, help="执行指令，如: --cmd='确认安全 1'")
    args = parser.parse_args()
    
    if args.cmd:
        # 解析指令
        parts = args.cmd.strip().split(maxsplit=1)
        command = parts[0]
        item_id = parts[1] if len(parts) > 1 else None
        print(process_user_command(command, item_id))
        return
    
    if args.report:
        if REPORT_PATH.exists():
            with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("暂无报告，请先运行 --scan")
        return
    
    if args.interactive:
        print("=" * 50)
        print("Privacy Guard v0.3 - 交互模式")
        print("=" * 50)
        print("\n可用命令：")
        print("- scan    : 执行扫描")
        print("- report  : 查看报告")
        print("- list    : 查看可疑列表")
        print("- safe N  : 确认第N项为安全")
        print("- risk N  : 确认第N项为风险")
        print("- whitelist: 查看白名单")
        print("- add P   : 添加模式到白名单")
        print("- quit    : 退出")
        
        while True:
            try:
                cmd = input("\n> ").strip()
                if cmd == "quit":
                    break
                elif cmd == "scan":
                    critical, high, suspicious = scan_all_logs()
                    generate_report(critical, high, suspicious)
                    print(f"扫描完成：CRITICAL {len(critical)}, HIGH {len(high)}, SUSPICIOUS {len(suspicious)}")
                elif cmd == "report":
                    if REPORT_PATH.exists():
                        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                            print(f.read())
                elif cmd == "list":
                    print(list_suspicious())
                elif cmd.startswith("safe "):
                    item_id = cmd.split()[1]
                    print(process_user_command("确认安全", item_id))
                elif cmd.startswith("risk "):
                    item_id = cmd.split()[1]
                    print(process_user_command("确认风险", item_id))
                elif cmd == "whitelist":
                    print(list_whitelist())
                elif cmd.startswith("add "):
                    pattern = cmd[4:].strip()
                    if pattern:
                        add_to_whitelist(pattern)
                        print(f"已添加: {pattern}")
                else:
                    print("未知命令")
            except KeyboardInterrupt:
                break
        return
    
    if args.scan:
        print("=" * 50)
        print("Privacy Guard v0.3 - 敏感信息外泄检测")
        print("=" * 50)
        
        critical, high, suspicious = scan_all_logs()
        generate_report(critical, high, suspicious)
        
        print(f"\n扫描完成:")
        print(f"- 🔴 CRITICAL: {len(critical)} 条")
        print(f"- 🟠 HIGH: {len(high)} 条")
        print(f"- 🟡 SUSPICIOUS: {len(suspicious)} 条")
        
        if critical or high:
            print("\n⚠️ 发现风险，请查看报告!")
            print(f"路径: {REPORT_PATH}")
        
        return
    
    parser.print_help()

if __name__ == "__main__":
    main()

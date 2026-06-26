#!/usr/bin/env python3
"""
CodeQL + LLM 融合扫描器
实现 CodeQL 扫描、结果分析、报告生成的自动化流程
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_codeql():
    """检查 CodeQL 是否安装"""
    try:
        result = subprocess.run(
            ["codeql", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.split('\n')[0]
        print(f"✅ CodeQL 已安装：{version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ CodeQL 未安装")
        print("\n安装指南:")
        print("1. 访问：https://github.com/github/codeql-cli-binaries/releases")
        print("2. 下载对应系统的版本")
        print("3. 解压并添加到 PATH")
        return False


def resolve_languages():
    """解析支持的語言"""
    try:
        result = subprocess.run(
            ["codeql", "resolve", "languages"],
            capture_output=True,
            text=True,
            check=True
        )
        languages = [line.split()[0] for line in result.stdout.strip().split('\n') if line]
        return languages
    except subprocess.CalledProcessError:
        return []


def create_database(source_root, db_path, language="python"):
    """创建 CodeQL 数据库"""
    print(f"\n📦 创建 {language} 数据库...")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    cmd = [
        "codeql", "database", "create", db_path,
        "--language", language,
        "--source-root", source_root,
        "--overwrite"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ 数据库创建成功：{db_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库创建失败：{e.stderr}")
        return False


def download_queries():
    """下载查询包"""
    print("\n📥 下载查询包...")
    
    cmd = ["codeql", "pack", "download", "codeql/python-queries"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ 查询包下载成功")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  查询包下载失败，尝试使用本地查询")
        return False


def analyze_database(db_path, output_sarif, suite="python-security-extended.qls"):
    """分析数据库"""
    print(f"\n🔍 运行安全分析...")
    
    # 查找查询套件路径
    home = Path.home()
    query_paths = [
        home / ".codeql" / "packages" / "codeql" / "python-queries" / "*" / "codeql-suites" / suite,
        home / ".codeql" / suite,
        Path("/opt/codeql/codeql/python/ql/src") / suite,
    ]
    
    query_suite = None
    for path_pattern in query_paths:
        import glob
        matches = glob.glob(str(path_pattern))
        if matches:
            query_suite = matches[0]
            break
    
    if not query_suite:
        print("❌ 未找到查询套件")
        return False
    
    print(f"使用查询套件：{query_suite}")
    
    cmd = [
        "codeql", "database", "analyze", db_path,
        query_suite,
        "--format=sarif-latest",
        "--output", output_sarif
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ 分析完成，结果保存到：{output_sarif}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 分析失败：{e.stderr}")
        return False


def parse_sarif(sarif_file):
    """解析 SARIF 文件"""
    with open(sarif_file, 'r') as f:
        data = json.load(f)
    
    results = []
    try:
        runs = data.get('runs', [{}])
        for run in runs:
            run_results = run.get('results', [])
            for r in run_results:
                rule_id = r.get('ruleId', 'Unknown')
                level = r.get('level', 'none')
                message = r.get('message', {}).get('text', 'N/A')
                
                locations = r.get('locations', [])
                if locations:
                    loc = locations[0]
                    path = loc.get('physicalLocation', {}).get(
                        'artifactLocation', {}).get('path', 'unknown')
                    line = loc.get('physicalLocation', {}).get(
                        'region', {}).get('startLine', '?')
                else:
                    path = 'unknown'
                    line = '?'
                
                results.append({
                    'rule_id': rule_id,
                    'level': level,
                    'message': message,
                    'path': path,
                    'line': line
                })
    except Exception as e:
        print(f"❌ 解析 SARIF 失败：{e}")
        return []
    
    return results


def generate_report(results, output_file):
    """生成 Markdown 报告"""
    print(f"\n📝 生成报告...")
    
    # 按规则分组
    by_rule = {}
    for r in results:
        rule_id = r['rule_id']
        if rule_id not in by_rule:
            by_rule[rule_id] = []
        by_rule[rule_id].append(r)
    
    # 严重程度映射
    severity_map = {
        'error': '🔴 严重',
        'warning': '🟠 高危',
        'note': '🟡 中危',
        'none': '⚪ 提示'
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# CodeQL 安全扫描报告\n\n")
        f.write(f"**扫描时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**总漏洞数**: {len(results)}\n\n")
        
        f.write("## 📊 漏洞统计\n\n")
        f.write("| 漏洞类型 | 数量 | 严重程度 |\n")
        f.write("|----------|------|----------|\n")
        
        for rule_id, rs in sorted(by_rule.items(), key=lambda x: -len(x[1])):
            level = rs[0]['level'] if rs else 'none'
            severity = severity_map.get(level, '⚪ 未知')
            f.write(f"| {rule_id} | {len(rs)} | {severity} |\n")
        
        f.write("\n## 🔍 详细发现\n\n")
        
        for rule_id, rs in sorted(by_rule.items(), key=lambda x: -len(x[1])):
            level = rs[0]['level'] if rs else 'none'
            severity = severity_map.get(level, '⚪ 未知')
            
            f.write(f"### {severity} {rule_id}\n\n")
            f.write(f"**发现数量**: {len(rs)}\n\n")
            
            for i, r in enumerate(rs, 1):
                f.write(f"**{i}. 位置**: `{r['path']}:{r['line']}`\n")
                f.write(f"**描述**: {r['message'][:100]}...\n\n")
            
            f.write("\n---\n\n")
    
    print(f"✅ 报告已生成：{output_file}")


def generate_checklist(results, output_file):
    """生成验证 Checklist"""
    print(f"\n📋 生成验证清单...")
    
    # 按规则分组
    by_rule = {}
    for r in results:
        rule_id = r['rule_id']
        if rule_id not in by_rule:
            by_rule[rule_id] = []
        by_rule[rule_id].append(r)
    
    # 严重程度排序
    severity_order = {'error': 0, 'warning': 1, 'note': 2, 'none': 3}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🔍 漏洞验证 Checklist\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**总漏洞数**: {len(results)}\n\n")
        
        f.write("## 使用说明\n\n")
        f.write("- [ ] 未验证\n")
        f.write("- [✅] 已验证存在\n")
        f.write("- [❌] 误报/已修复\n")
        f.write("- [⚠️] 部分存在\n\n")
        
        for rule_id, rs in sorted(
            by_rule.items(),
            key=lambda x: severity_order.get(x[1][0]['level'] if x[1] else 'none', 3)
        ):
            level = rs[0]['level'] if rs else 'none'
            severity_map = {'error': '🔴', 'warning': '🟠', 'note': '🟡', 'none': '⚪'}
            severity = severity_map.get(level, '⚪')
            
            f.write(f"## {severity} {rule_id} ({len(rs)}处)\n\n")
            
            for i, r in enumerate(rs, 1):
                f.write(f"### {severity} {rule_id} - #{i}\n\n")
                f.write(f"**位置**: `{r['path']}:{r['line']}`\n\n")
                
                f.write("**验证步骤**:\n")
                f.write(f"- [ ] 定位代码\n")
                f.write(f"- [ ] 构造 payload\n")
                f.write(f"- [ ] 发送请求\n")
                f.write(f"- [ ] 确认漏洞\n")
                f.write(f"- [ ] 截图记录\n\n")
                
                # 根据漏洞类型给出建议
                if 'sql' in rule_id.lower():
                    f.write("**测试 payload**:\n")
                    f.write("```bash\n")
                    f.write("curl \"http://localhost/search?username=' OR '1'='1\"\n")
                    f.write("```\n\n")
                elif 'injection' in rule_id.lower():
                    f.write("**测试 payload**:\n")
                    f.write("```bash\n")
                    f.write("curl -X POST http://localhost/calculate \\\n")
                    f.write("  -H 'Content-Type: application/json' \\\n")
                    f.write("  -d '{\"expression\": \"__import__(\\\"os\\\").popen(\\\"id\\\").read()\"}'\n")
                    f.write("```\n\n")
                
                f.write("**预期结果**: _______________\n\n")
                f.write("**实际结果**: _______________\n\n")
                f.write("---\n\n")
        
        f.write("\n## 📊 验证汇总\n\n")
        f.write("| 严重程度 | 总数 | 已验证 | 误报 | 待验证 |\n")
        f.write("|----------|------|--------|------|--------|\n")
        
        for level in ['error', 'warning', 'note', 'none']:
            count = sum(1 for rs in by_rule.values() for r in rs if r['level'] == level)
            if count > 0:
                severity = severity_map.get(level, '⚪')
                f.write(f"| {severity} {level} | {count} | [ ] | [ ] | [ ] |\n")
        
        f.write("| **总计** | **{}** | [ ] | [ ] | [ ] |\n".format(len(results)))
    
    print(f"✅ 验证清单已生成：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='CodeQL + LLM 融合扫描器')
    parser.add_argument('source', help='源代码目录')
    parser.add_argument('--language', '-l', default='python', help='编程语言')
    parser.add_argument('--output', '-o', default='.', help='输出目录')
    parser.add_argument('--db-name', '-d', default='codeql-db', help='数据库名称')
    parser.add_argument('--suite', '-s', default='python-security-extended.qls', help='查询套件')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  CodeQL + LLM 融合扫描器")
    print("=" * 60)
    
    # Step 1: 检查环境
    if not check_codeql():
        sys.exit(1)
    
    # Step 2: 创建数据库
    db_path = os.path.join(args.output, args.db_name)
    if not create_database(args.source, db_path, args.language):
        sys.exit(1)
    
    # Step 3: 下载查询包
    download_queries()
    
    # Step 4: 分析
    sarif_file = os.path.join(args.output, 'codeql-results.sarif')
    if not analyze_database(db_path, sarif_file, args.suite):
        sys.exit(1)
    
    # Step 5: 解析结果
    results = parse_sarif(sarif_file)
    print(f"\n📊 发现 {len(results)} 个安全问题")
    
    # Step 6: 生成报告
    report_file = os.path.join(args.output, 'CODEQL_SECURITY_REPORT.md')
    generate_report(results, report_file)
    
    # Step 7: 生成 Checklist
    checklist_file = os.path.join(args.output, '漏洞验证_Checklist.md')
    generate_checklist(results, checklist_file)
    
    print("\n" + "=" * 60)
    print("  ✅ 扫描完成！")
    print("=" * 60)
    print(f"\n生成的文件:")
    print(f"  1. {sarif_file}")
    print(f"  2. {report_file}")
    print(f"  3. {checklist_file}")
    print("\n下一步：将结果发送给 LLM 进行智能分析")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
OpenClaw 知识库管理器
负责知识库的自我进化、定期更新、智能学习

核心功能：
1. 定期自动更新知识库
2. 从成功案例中学习
3. 知识库健康检查
4. 知识导出与导入
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class KnowledgeEntry:
    """知识条目"""
    error_type: str
    pattern: str
    keywords: List[str]
    solution: str
    verified: bool
    source: str  # manual/web_search/github/community
    success_rate: float
    last_used: str
    times_used: int


class KnowledgeBaseManager:
    """知识库管理器"""

    def __init__(self, kb_dir: Optional[Path] = None):
        self.kb_dir = kb_dir or (Path.home() / ".openclaw" / "knowledge")
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        self.knowledge_file = self.kb_dir / "knowledge_base.json"
        self.learned_file = self.kb_dir / "learned_cases.json"
        self.update_log_file = self.kb_dir / "update_log.json"
        self.stats_file = self.kb_dir / "stats.json"

        self._init_knowledge_base()

    def _init_knowledge_base(self):
        """初始化知识库"""
        if not self.knowledge_file.exists():
            self._create_initial_knowledge()

        if not self.update_log_file.exists():
            with open(self.update_log_file, 'w') as f:
                json.dump([], f)

        if not self.stats_file.exists():
            self._save_stats({
                "total_queries": 0,
                "successful_fixes": 0,
                "patterns_learned": 0,
                "auto_updates": 0,
                "success_rate": 0.0
            })

    def _create_initial_knowledge(self):
        """创建初始知识库"""
        initial_knowledge = {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "error_patterns": [
                {
                    "id": "node_version",
                    "error_type": "版本不兼容",
                    "pattern": r"Node.*version.*(\d+)",
                    "keywords": ["node", "version", "require", ">=22"],
                    "solution": "使用 nvm 安装 Node.js v22: nvm install 22 && nvm use 22",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "npm_permission",
                    "error_type": "权限问题",
                    "pattern": r"EACCES|Permission denied",
                    "keywords": ["permission", "denied", "root", "sudo"],
                    "solution": "配置 npm 用户目录: mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global'",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "network_timeout",
                    "error_type": "网络超时",
                    "pattern": r"ETIMEDOUT|ECONNREFUSED",
                    "keywords": ["timeout", "connection", "network"],
                    "solution": "配置国内镜像: npm config set registry https://registry.npmmirror.com",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "port_conflict",
                    "error_type": "端口冲突",
                    "pattern": r"port.*(\d+).*in use|EADDRINUSE",
                    "keywords": ["port", "listen", "address"],
                    "solution": "查找并终止占用进程: lsof -i :{port} 或更改 OpenClaw 端口",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "config_json",
                    "error_type": "配置错误",
                    "pattern": r"JSON.*parse|JSONDecodeError",
                    "keywords": ["json", "parse", "syntax", "config"],
                    "solution": "检查配置文件: cat ~/.openclaw/openclaw.json | python3 -m json.tool",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "websocket_fail",
                    "error_type": "WebSocket连接失败",
                    "pattern": r"WebSocket|ws://|ECONNREFUSED",
                    "keywords": ["websocket", "ws", "connect", "upgrade"],
                    "solution": "检查网络代理、防火墙配置，确认服务地址正确",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "memory_error",
                    "error_type": "内存不足",
                    "pattern": r"out of memory|OOM|heap",
                    "keywords": ["memory", "heap", "allocate"],
                    "solution": "检查内存: free -m，增加可用内存或关闭其他程序",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "ssl_cert",
                    "error_type": "SSL证书错误",
                    "pattern": r"certificate|SSL|TLS|cert",
                    "keywords": ["certificate", "ssl", "verify", "self-signed"],
                    "solution": "更新 CA 证书或设置 NODE_TLS_REJECT_UNAUTHORIZED=0（仅开发环境）",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "file_not_found",
                    "error_type": "文件缺失",
                    "pattern": r"ENOENT|No such file|not found",
                    "keywords": ["enoent", "not found", "missing"],
                    "solution": "重新安装 OpenClaw: npm uninstall -g openclaw && npm install -g openclaw",
                    "verified": True,
                    "source": "builtin"
                },
                {
                    "id": "module_not_found",
                    "error_type": "模块缺失",
                    "pattern": r"Cannot find module|require|import",
                    "keywords": ["module", "require", "import", "not found"],
                    "solution": "重新安装依赖: npm install 或 npm rebuild",
                    "verified": True,
                    "source": "builtin"
                }
            ],
            "categories": {
                "installation": ["node_version", "npm_permission", "file_not_found", "module_not_found"],
                "runtime": ["websocket_fail", "memory_error", "port_conflict"],
                "configuration": ["config_json", "ssl_cert"],
                "network": ["network_timeout", "websocket_fail"]
            }
        }

        with open(self.knowledge_file, 'w') as f:
            json.dump(initial_knowledge, f, indent=2, ensure_ascii=False)

    def get_all_entries(self) -> List[Dict]:
        """获取所有知识条目"""
        with open(self.knowledge_file, 'r') as f:
            return json.load(f).get("error_patterns", [])

    def add_entry(self, entry: Dict) -> bool:
        """添加新知识条目"""
        try:
            with open(self.knowledge_file, 'r') as f:
                kb = json.load(f)

            # 检查是否已存在相同模式
            for existing in kb["error_patterns"]:
                if existing.get("pattern") == entry.get("pattern"):
                    return False

            # 添加新条目
            entry["id"] = f"custom_{len(kb['error_patterns']) + 1}"
            entry["verified"] = False
            entry["source"] = "learned"
            entry["times_used"] = 0
            kb["error_patterns"].append(entry)

            with open(self.knowledge_file, 'w') as f:
                json.dump(kb, f, indent=2, ensure_ascii=False)

            self._log_update("add", entry["id"])
            return True

        except Exception as e:
            print(f"添加知识条目失败: {e}")
            return False

    def update_entry(self, entry_id: str, updates: Dict) -> bool:
        """更新知识条目"""
        try:
            with open(self.knowledge_file, 'r') as f:
                kb = json.load(f)

            for entry in kb["error_patterns"]:
                if entry.get("id") == entry_id:
                    entry.update(updates)
                    entry["last_updated"] = datetime.now().isoformat()

                    with open(self.knowledge_file, 'w') as f:
                        json.dump(kb, f, indent=2, ensure_ascii=False)

                    self._log_update("update", entry_id)
                    return True

            return False

        except Exception as e:
            print(f"更新知识条目失败: {e}")
            return False

    def verify_entry(self, entry_id: str, success: bool):
        """验证知识条目"""
        entry = self.find_entry_by_id(entry_id)
        if entry:
            new_rate = entry.get("success_rate", 0.0)
            times = entry.get("times_used", 0)

            # 计算新的成功率
            if success:
                new_rate = (new_rate * times + 1.0) / (times + 1)
            else:
                new_rate = (new_rate * times) / (times + 1) if times > 0 else 0.0

            self.update_entry(entry_id, {
                "success_rate": new_rate,
                "times_used": times + 1,
                "verified": new_rate >= 0.7
            })

    def find_entry_by_id(self, entry_id: str) -> Optional[Dict]:
        """根据ID查找条目"""
        entries = self.get_all_entries()
        for entry in entries:
            if entry.get("id") == entry_id:
                return entry
        return None

    def search_entries(self, query: str) -> List[Dict]:
        """搜索知识条目"""
        entries = self.get_all_entries()
        results = []
        query_lower = query.lower()

        for entry in entries:
            # 检查关键词
            if any(query_lower in kw.lower() for kw in entry.get("keywords", [])):
                results.append(entry)
                continue

            # 检查错误类型
            if query_lower in entry.get("error_type", "").lower():
                results.append(entry)
                continue

            # 检查模式
            if query_lower in entry.get("pattern", "").lower():
                results.append(entry)

        return results

    def _log_update(self, action: str, target: str):
        """记录更新日志"""
        try:
            logs = []
            if self.update_log_file.exists():
                with open(self.update_log_file, 'r') as f:
                    logs = json.load(f)

            logs.append({
                "action": action,
                "target": target,
                "timestamp": datetime.now().isoformat()
            })

            # 只保留最近100条日志
            logs = logs[-100:]

            with open(self.update_log_file, 'w') as f:
                json.dump(logs, f, indent=2)

        except Exception:
            pass

    def _save_stats(self, stats: Dict):
        """保存统计信息"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {}

    def update_stats(self, query_result: bool, fix_result: bool):
        """更新统计"""
        stats = self.get_stats()
        stats["total_queries"] = stats.get("total_queries", 0) + 1
        if fix_result:
            stats["successful_fixes"] = stats.get("successful_fixes", 0) + 1

        total = stats["total_queries"]
        success = stats["successful_fixes"]
        stats["success_rate"] = success / total if total > 0 else 0.0

        self._save_stats(stats)

    def export_knowledge(self, output_file: Path) -> bool:
        """导出知识库"""
        try:
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "version": "2.0",
                "knowledge_base": self.get_all_entries(),
                "learned_cases": self._load_learned(),
                "stats": self.get_stats()
            }

            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            print(f"✅ 知识库已导出到: {output_file}")
            return True

        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False

    def import_knowledge(self, input_file: Path) -> int:
        """导入知识库"""
        try:
            with open(input_file, 'r') as f:
                import_data = json.load(f)

            imported = 0
            for entry in import_data.get("knowledge_base", []):
                if "id" in entry and "pattern" in entry:
                    entry.pop("id", None)  # 移除ID，让系统重新生成
                    if self.add_entry(entry):
                        imported += 1

            # 导入学习案例
            for case in import_data.get("learned_cases", []):
                self._add_learned_case(case)
                imported += 1

            print(f"✅ 成功导入 {imported} 条知识")
            return imported

        except Exception as e:
            print(f"❌ 导入失败: {e}")
            return 0

    def _load_learned(self) -> List[Dict]:
        """加载学习案例"""
        if self.learned_file.exists():
            with open(self.learned_file, 'r') as f:
                return json.load(f)
        return []

    def _add_learned_case(self, case: Dict):
        """添加学习案例"""
        cases = self._load_learned()

        # 检查是否已存在
        for existing in cases:
            if existing.get("error") == case.get("error"):
                existing["success_count"] = max(
                    existing.get("success_count", 1),
                    case.get("success_count", 1)
                )
                break
        else:
            cases.append(case)

        with open(self.learned_file, 'w') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)

    def get_health_report(self) -> Dict:
        """获取知识库健康报告"""
        entries = self.get_all_entries()
        learned = self._load_learned()
        stats = self.get_stats()

        # 分析知识库质量
        verified = sum(1 for e in entries if e.get("verified"))
        high_success = sum(1 for e in entries if e.get("success_rate", 0) >= 0.8)
        low_success = sum(1 for e in entries if e.get("success_rate", 0) < 0.3 and e.get("times_used", 0) > 3)

        return {
            "summary": {
                "total_patterns": len(entries),
                "verified_patterns": verified,
                "learned_cases": len(learned),
                "success_rate": stats.get("success_rate", 0.0)
            },
            "quality": {
                "high_confidence": high_success,
                "low_confidence": low_success,
                "unverified": len(entries) - verified
            },
            "recommendations": self._generate_recommendations(entries, learned)
        }

    def _generate_recommendations(self, entries: List[Dict], learned: List[Dict]) -> List[str]:
        """生成优化建议"""
        recs = []

        if len(entries) < 20:
            recs.append("知识库规模较小，建议添加更多常见问题模式")

        if len(learned) < 5:
            recs.append("学习案例较少，系统需要更多实际使用来学习")

        unverified = sum(1 for e in entries if not e.get("verified"))
        if unverified > len(entries) * 0.3:
            recs.append(f"有 {unverified} 个未验证的模式，建议验证其准确性")

        low_confidence = [e for e in entries if e.get("success_rate", 0) < 0.5 and e.get("times_used", 0) >= 3]
        if low_confidence:
            recs.append(f"有 {len(low_confidence)} 个低置信度模式，建议优化其解决方案")

        return recs if recs else ["知识库状态良好"]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 知识库管理器")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有知识条目")
    parser.add_argument("--search", "-s", type=str, help="搜索知识条目")
    parser.add_argument("--add", "-a", type=str, help="添加新知识条目 (JSON)")
    parser.add_argument("--verify", "-v", nargs=2, metavar=("ID", "SUCCESS"), help="验证知识条目")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--health", action="store_true", help="健康报告")
    parser.add_argument("--export", "-e", type=str, help="导出知识库")
    parser.add_argument("--import", "-i", dest="import_file", type=str, help="导入知识库")
    parser.add_argument("--id", type=str, help="知识条目ID")

    args = parser.parse_args()

    manager = KnowledgeBaseManager()

    if args.list:
        print("\n📚 OpenClaw 知识库 - 所有条目：\n")
        for entry in manager.get_all_entries():
            status = "✅" if entry.get("verified") else "⚠️"
            rate = entry.get("success_rate", 0.0)
            print(f"  [{status}] {entry['id']}: {entry['error_type']}")
            print(f"       模式: {entry['pattern']}")
            print(f"       成功率: {rate:.0%} ({entry.get('times_used', 0)} 次使用)")
            print()

    elif args.search:
        print(f"\n🔍 搜索结果: {args.search}\n")
        results = manager.search_entries(args.search)
        if results:
            for entry in results:
                print(f"  - {entry['error_type']}: {entry.get('pattern', '')[:50]}")
        else:
            print("  未找到匹配条目")

    elif args.stats:
        stats = manager.get_stats()
        print("\n📊 统计信息：\n")
        print(f"  总查询数: {stats.get('total_queries', 0)}")
        print(f"  成功修复: {stats.get('successful_fixes', 0)}")
        print(f"  学习案例: {len(manager._load_learned())}")
        print(f"  成功率: {stats.get('success_rate', 0.0):.1%}")

    elif args.health:
        report = manager.get_health_report()
        print("\n🏥 知识库健康报告：\n")
        print(f"  模式总数: {report['summary']['total_patterns']}")
        print(f"  已验证: {report['summary']['verified_patterns']}")
        print(f"  高置信度: {report['quality']['high_confidence']}")
        print(f"  低置信度: {report['quality']['low_confidence']}")
        print(f"  学习案例: {report['summary']['learned_cases']}")
        print(f"  成功率: {report['summary']['success_rate']:.1%}")
        print("\n  建议：")
        for rec in report['recommendations']:
            print(f"    - {rec}")

    elif args.export:
        manager.export_knowledge(Path(args.export))

    elif args.import_file:
        manager.import_knowledge(Path(args.import_file))

    elif args.add:
        try:
            entry = json.loads(args.add)
            if manager.add_entry(entry):
                print("✅ 知识条目添加成功")
            else:
                print("⚠️ 知识条目可能已存在或格式错误")
        except json.JSONDecodeError:
            print("❌ JSON 格式错误")

    elif args.verify:
        entry_id, success = args.verify
        manager.verify_entry(entry_id, success.lower() == "true")
        print("✅ 验证结果已更新")

    else:
        print("OpenClaw 知识库管理器")
        print("用法:")
        print("  --list              列出所有知识条目")
        print("  --search <关键词>    搜索知识条目")
        print("  --stats             显示统计信息")
        print("  --health            健康报告")
        print("  --export <文件>      导出知识库")
        print("  --import <文件>      导入知识库")


if __name__ == "__main__":
    main()

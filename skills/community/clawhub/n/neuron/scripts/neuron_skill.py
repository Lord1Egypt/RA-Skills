"""
OpenClaw Neuron 技能 - 分布式AI处理
节点发现、任务分发和结果聚合的核心实现
"""

import socket
import threading
import time
import json
import uuid
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class NeuronProcessor:
    """分布式AI任务执行的主处理器"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.node_identity_path = self._get_node_identity_path()
        self.config = self._load_config()
        self.node_id = self._get_or_create_node_id()
        self.local_ip = self._get_local_ip()
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self._start_discovery()
        self._start_cleanup()

    def _get_default_config_path(self) -> str:
        script_dir = Path(__file__).parent
        return str(script_dir / "config.json")

    def _get_node_identity_path(self) -> str:
        script_dir = Path(__file__).parent
        return str(script_dir / "node_identity.json")

    def _get_or_create_node_id(self) -> str:
        if "OPENCLAW_NODE_ID" in os.environ:
            return os.environ["OPENCLAW_NODE_ID"]

        try:
            if os.path.exists(self.node_identity_path):
                with open(self.node_identity_path, 'r', encoding='utf-8') as f:
                    identity = json.load(f)
                    node_id = identity.get("node_id")
                    if node_id:
                        return node_id
        except Exception as e:
            print(f"警告: 读取节点ID失败: {e}")

        new_node_id = f"node-{socket.gethostname()}-{str(uuid.uuid4())[:8]}"

        try:
            identity = {
                "node_id": new_node_id,
                "hostname": socket.gethostname(),
                "created_at": time.time(),
                "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.node_identity_path, 'w', encoding='utf-8') as f:
                json.dump(identity, f, indent=2, ensure_ascii=False)
            print(f"已生成新节点ID: {new_node_id}")
        except Exception as e:
            print(f"警告: 保存节点ID失败: {e}")

        return new_node_id

    def _load_config(self) -> Dict:
        default_config = {
            "discovery_port": 83668,
            "broadcast_interval": 5,
            "node_timeout": 15,
            "task_timeout": 30,
            "max_parallel_tasks": 10
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                default_config.update(config)
        except Exception as e:
            print(f"警告: 加载配置失败,使用默认值: {e}")

        return default_config

    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _start_discovery(self) -> None:
        def send_broadcast():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)

            while True:
                try:
                    msg = json.dumps({
                        "type": "announce",
                        "node_id": self.node_id,
                        "ip": self.local_ip,
                        "timestamp": time.time()
                    }).encode()
                    sock.sendto(msg, ('<broadcast>', self.config["discovery_port"]))
                except Exception as e:
                    print(f"广播错误: {e}")

                time.sleep(self.config["broadcast_interval"])

        def listen_broadcast():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self.config["discovery_port"]))
            sock.settimeout(1)

            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    msg = json.loads(data.decode())

                    if msg.get("type") == "announce":
                        node_id = msg["node_id"]
                        ip = msg["ip"]

                        if node_id == self.node_id:
                            continue

                        with self.lock:
                            self.nodes[node_id] = {
                                "ip": ip,
                                "last_seen": time.time()
                            }
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"监听错误: {e}")

        threading.Thread(target=send_broadcast, daemon=True).start()
        threading.Thread(target=listen_broadcast, daemon=True).start()

    def _start_cleanup(self) -> None:
        def cleanup() -> None:
            while True:
                time.sleep(self.config["node_timeout"])
                now = time.time()
                with self.lock:
                    to_remove = [
                        nid for nid, info in self.nodes.items()
                        if now - info["last_seen"] > self.config["node_timeout"]
                    ]
                    for nid in to_remove:
                        del self.nodes[nid]
                        print(f"节点 {nid} 超时并被移除")

        threading.Thread(target=cleanup, daemon=True).start()

    def get_active_nodes(self) -> List[Dict[str, Any]]:
        with self.lock:
            all_nodes = {
                self.node_id: {"ip": self.local_ip, "last_seen": time.time()},
                **self.nodes
            }
            return [{"id": nid, "ip": info["ip"]} for nid, info in all_nodes.items()]

    def get_other_nodes(self) -> List[Dict[str, Any]]:
        with self.lock:
            return [{"id": nid, "ip": info["ip"]} for nid, info in self.nodes.items()]

    def discover_nodes(self) -> int:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            msg = json.dumps({
                "type": "announce",
                "node_id": self.node_id,
                "ip": self.local_ip,
                "timestamp": time.time()
            }).encode()
            sock.sendto(msg, ('<broadcast>', self.config["discovery_port"]))
        finally:
            sock.close()

        time.sleep(2)
        return len(self.get_active_nodes())

    def execute(self, question: str, context: Optional[Any] = None, distribute: bool = True) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "question": question,
            "results": {},
            "final": None,
            "timestamp": time.time()
        }

        if not distribute or not context:
            result = self._process_local(question, context)
            self.tasks[task_id]["final"] = result
            return result

        other_nodes = self.get_other_nodes()

        if not other_nodes:
            result = self._process_local(question, context)
            self.tasks[task_id]["final"] = result
            return result

        results = self._distribute_tasks(question, other_nodes, task_id, context)
        final_result = self._aggregate_results(question, results, context)
        self.tasks[task_id]["final"] = final_result

        threading.Thread(
            target=self._broadcast_result,
            args=(task_id, final_result, other_nodes, context),
            daemon=True
        ).start()

        return final_result

    def _process_local(self, question: str, context: Optional[Any]) -> str:
        if context and hasattr(context, 'call_model'):
            return context.call_model(prompt=question)
        else:
            return f"[本地处理] {question} - 无法使用AI处理(context不可用)"

    def _distribute_tasks(self, question: str, nodes: List[Dict[str, Any]], task_id: str, context: Any) -> Dict[str, str]:
        results = {}
        threads = []

        def call_node(node: Dict[str, Any]):
            try:
                if hasattr(context, 'rpc_call'):
                    result = context.rpc_call(
                        node_id=node["id"],
                        skill="neuron",
                        params={"question": question, "distribute": False, "task_id": task_id},
                        timeout=self.config["task_timeout"]
                    )
                else:
                    result = f"[节点 {node['id']}] 模拟处理中"

                with self.lock:
                    results[node["id"]] = result
            except Exception as e:
                print(f"调用节点 {node['id']} 出错: {e}")
                with self.lock:
                    results[node["id"]] = f"[错误] {str(e)}"

        for node in nodes:
            t = threading.Thread(target=call_node, args=(node,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join(timeout=self.config["task_timeout"])

        with self.lock:
            self.tasks[task_id]["results"] = results.copy()

        return results

    def _aggregate_results(self, question: str, results: Dict[str, str], context: Any) -> str:
        summary_prompt = self._build_summary_prompt(question, results)

        if context and hasattr(context, 'call_model'):
            return context.call_model(prompt=summary_prompt)
        else:
            return f"[聚合] {len(results)} 个节点响应。摘要: {summary_prompt}"

    def _build_summary_prompt(self, question: str, results: Dict[str, str]) -> str:
        summary = f"原始问题: {question}\n\n"
        summary += f"来自 {len(results)} 个节点的响应:\n"
        for node_id, result in results.items():
            summary += f"\n[节点 {node_id}]:\n{result}\n"
        summary += "\n请将这些响应综合成一个全面、准确的答案。"
        return summary

    def _broadcast_result(self, task_id: str, final_result: str, nodes: List[Dict[str, Any]], context: Any) -> None:
        for node in nodes:
            try:
                if hasattr(context, 'rpc_call'):
                    context.rpc_call(
                        node_id=node["id"],
                        skill="neuron",
                        params={
                            "action": "record_result",
                            "task_id": task_id,
                            "final_result": final_result
                        },
                        timeout=5
                    )
            except Exception:
                pass

    def record_result(self, task_id: str, final_result: str) -> None:
        if task_id not in self.tasks:
            self.tasks[task_id] = {
                "question": "",
                "results": {},
                "final": None,
                "timestamp": time.time()
            }
        self.tasks[task_id]["final"] = final_result

    def get_task_memory(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        return self.tasks.copy()

    def cleanup_old_tasks(self, age_hours: float = 24) -> None:
        cutoff = time.time() - (age_hours * 3600)
        with self.lock:
            self.tasks = {
                k: v for k, v in self.tasks.items()
                if v.get("timestamp", 0) > cutoff
            }

    def export_memory(self, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def import_memory(self, filepath: str) -> None:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_tasks = json.load(f)
            self.tasks.update(imported_tasks)
        except Exception as e:
            print(f"导入记忆失败: {e}")

    def get_status(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "local_ip": self.local_ip,
            "active_nodes": len(self.get_active_nodes()),
            "other_nodes": len(self.get_other_nodes()),
            "total_tasks": len(self.tasks),
            "config": self.config
        }

    def print_status(self) -> None:
        status = self.get_status()
        print("\n=== Neuron 节点状态 ===")
        print(f"节点ID: {status['node_id']}")
        print(f"IP地址: {status['local_ip']}")
        print(f"活跃节点: {status['active_nodes']}")
        print(f"其他节点: {status['other_nodes']}")
        print(f"总任务数: {status['total_tasks']}")
        print(f"\n活跃节点列表:")
        for node in self.get_active_nodes():
            marker = " (自身)" if node["id"] == self.node_id else ""
            print(f"  - {node['id']}: {node['ip']}{marker}")
        print("=========================\n")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw Neuron 技能CLI")
    parser.add_argument("--status", action="store_true", help="显示节点状态")
    parser.add_argument("--discover", action="store_true", help="触发节点发现")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--cleanup", type=int, metavar="HOURS", help="清理超过指定小时数的任务")
    parser.add_argument("--export", metavar="FILE", help="导出记忆到文件")
    parser.add_argument("--import", metavar="FILE", help="从文件导入记忆", dest="import_file")

    args = parser.parse_args()

    processor = NeuronProcessor(config_path=args.config)

    if args.status:
        processor.print_status()

    if args.discover:
        count = processor.discover_nodes()
        print(f"发现完成。找到 {count} 个节点。")

    if args.cleanup:
        processor.cleanup_old_tasks(args.cleanup)
        print(f"已清理超过 {args.cleanup} 小时的任务。")

    if args.export:
        processor.export_memory(args.export)
        print(f"记忆已导出到 {args.export}")

    if args.import_file:
        processor.import_memory(args.import_file)
        print(f"记忆已从 {args.import_file} 导入")

    if not any(vars(args).values()):
        processor.print_status()


if __name__ == "__main__":
    main()

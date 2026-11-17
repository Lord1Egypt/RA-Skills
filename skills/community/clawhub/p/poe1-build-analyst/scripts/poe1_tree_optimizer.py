from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from typing import Any


def load_treedata(pob_root: str, tree_version: str) -> tuple[dict[int, dict[str, Any]], dict[int, set[int]]]:
    cli_root = os.environ.get('POB_CLI_ROOT', '/home/ubuntu/poe1-pob-cli')
    if cli_root not in sys.path:
        sys.path.insert(0, cli_root)
    from pob_cli.treedata import load_tree_data
    data = load_tree_data(str(Path(pob_root).resolve()), tree_version)
    nodes = {int(k): v for k, v in data.get('nodes', {}).items() if str(k).isdigit()}
    graph = {i: set() for i in nodes}
    for i, node in nodes.items():
        for value in list(node.get('in', [])) + list(node.get('out', [])):
            try:
                j = int(value)
            except (TypeError, ValueError):
                continue
            if j in nodes:
                graph[i].add(j)
                graph[j].add(i)
    return nodes, graph


def is_special(node: dict[str, Any]) -> bool:
    return bool(node.get('isJewelSocket', False) or (not node.get('in') and node.get('classStartIndex') is None))


def node_text(node: dict[str, Any]) -> str:
    values = [node.get('name', ''), node.get('stats', ''), node.get('notable', '')]
    return ' '.join(str(value) for value in values).lower()


def score_node(node: dict[str, Any], objectives: list[str]) -> float:
    text = node_text(node)
    score = 0.0
    weights = {
        'cold-dot': ('cold', 'damage over time', 'dot multiplier'),
        'energy-shield': ('energy shield', 'es recharge', 'energy shield recovery'),
        'life': ('life', 'maximum life'),
        'curse': ('curse', 'hex'),
        'spell': ('spell', 'cast speed'),
        'defence': ('resistance', 'suppression', 'block', 'recovery', 'armour', 'evasion'),
        'damage': ('damage', 'spell', 'dot multiplier'),
    }
    for objective in objectives:
        terms = weights.get(objective, (objective.lower(),))
        for term in terms:
            if term in text:
                score += 10.0
    if node.get('isNotable') or node.get('notable'):
        score += 2.0
    if node.get('isKeystone'):
        score -= 1.0
    return score


def roots_for_class(nodes: dict[int, dict[str, Any]], class_id: int | None) -> list[int]:
    if class_id is None:
        return [i for i, n in nodes.items() if n.get('classStartIndex') is not None]
    return [i for i, n in nodes.items() if n.get('classStartIndex') == class_id]


def shortest_path(start_nodes: set[int], target: int, graph: dict[int, set[int]], allowed: set[int]) -> list[int] | None:
    queue = deque(start_nodes)
    parent: dict[int, int | None] = {x: None for x in start_nodes}
    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return list(reversed(path))
        for nxt in sorted(graph.get(current, set()) & allowed):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)
    return None


def build_connected_selection(nodes: dict[int, dict[str, Any]], graph: dict[int, set[int]], class_id: int | None, target_count: int, objectives: list[str], required: set[int], excluded: set[int]) -> tuple[list[int], list[str]]:
    roots = roots_for_class(nodes, class_id)
    if not roots:
        raise ValueError(f'找不到 class_id={class_id} 的職業起點')
    special = {i for i, n in nodes.items() if is_special(n)}
    forbidden = excluded | special
    allowed = set(nodes) - forbidden
    selected: set[int] = {roots[0]}
    warnings: list[str] = []
    for node_id in sorted(required):
        if node_id not in nodes:
            raise ValueError(f'必選節點不存在：{node_id}')
        if node_id in forbidden:
            raise ValueError(f'必選節點是排除或特殊節點：{node_id}')
        path = shortest_path(selected, node_id, graph, allowed)
        if path is None:
            raise ValueError(f'必選節點無法從職業起點連通：{node_id}')
        selected.update(path)
    if len(selected) > target_count:
        raise ValueError(f'必選節點的連通路徑已需要 {len(selected)} 點，超過 target_count={target_count}')
    while len(selected) < target_count:
        frontier = set().union(*(graph.get(i, set()) for i in selected)) & allowed - selected
        if not frontier:
            warnings.append('沒有更多可加入的正常節點；輸出少於 target_count。')
            break
        candidate = max(frontier, key=lambda i: (score_node(nodes[i], objectives), -len(graph.get(i, set())), -i))
        selected.add(candidate)
    # Deterministic BFS-ish order is easier to diff and remains connected.
    ordered: list[int] = []
    queue = deque(roots[:1])
    seen = set()
    while queue:
        cur = queue.popleft()
        if cur in seen or cur not in selected:
            continue
        seen.add(cur); ordered.append(cur)
        queue.extend(sorted(graph.get(cur, set()) & selected))
    ordered.extend(sorted(selected - set(ordered)))
    return ordered, warnings


def validate_selection(pob_root: str, tree_version: str, nodes: list[int], class_id: int | None) -> dict[str, Any]:
    cli_root = os.environ.get('POB_CLI_ROOT', '/home/ubuntu/poe1-pob-cli')
    if cli_root not in sys.path:
        sys.path.insert(0, cli_root)
    from pob_cli.treedata import validate_tree_selection
    result = validate_tree_selection(pob_root, tree_version, nodes, class_id=class_id)
    if not result.get('valid'):
        raise ValueError('候選天賦未通過連通性：' + '; '.join(result.get('errors', [])))
    return result


def write_xml_with_nodes(source: str, destination: str, nodes: list[int]) -> None:
    tree = ET.parse(source)
    root = tree.getroot()
    spec = root.find('Tree/Spec')
    if spec is None:
        raise ValueError('PoB XML 缺少 Tree/Spec')
    spec.set('nodes', ','.join(map(str, nodes)))
    ET.indent(root, space='\t')
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding='utf-8', xml_declaration=True)


MAX_POB_OUTPUT = 2_000_000


def resolve_pob_command() -> str:
    """Resolve only the intended `pob` executable; never execute user-supplied commands."""
    command = shutil.which('pob')
    if not command or Path(command).name != 'pob' or not os.access(command, os.X_OK):
        raise RuntimeError('找不到受信任的 pob 執行檔；本 skill 不接受自訂或任意外部命令')
    return str(Path(command).resolve())


def run_pob_calc(build: str, pob_root: str, skill: str) -> dict[str, Any]:
    args = [resolve_pob_command(), 'calc', build, '--pob-root', pob_root, '--skill', skill, '--format', 'json', '--timeout', '120']
    try:
        proc = subprocess.run(args, capture_output=True, text=True, check=False, timeout=120, cwd=os.getcwd())
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('PoB calc 執行逾時') from exc
    stdout = proc.stdout[-MAX_POB_OUTPUT:]
    stderr = proc.stderr[-MAX_POB_OUTPUT:]
    if proc.returncode != 0:
        raise RuntimeError(f'PoB calc 失敗：{stderr or stdout}')
    if len(proc.stdout) > MAX_POB_OUTPUT:
        raise RuntimeError('PoB calc 輸出超過安全大小上限')
    value = json.loads(stdout)
    if not isinstance(value, dict):
        raise RuntimeError('PoB calc 輸出不是 JSON object')
    return value


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Generate a connected PoE1 passive-tree allocation.')
    p.add_argument('--pob-root', default=os.environ.get('POB_ROOT'), required=False)
    p.add_argument('--tree-version', default='3_29')
    p.add_argument('--class-id', type=int, required=True)
    p.add_argument('--target-nodes', type=int, required=True)
    p.add_argument('--objective', action='append', default=['cold-dot'], choices=['cold-dot','energy-shield','life','curse','spell','defence','damage'])
    p.add_argument('--required-node', type=int, action='append', default=[])
    p.add_argument('--exclude-node', type=int, action='append', default=[])
    p.add_argument('--build', help='Optional PoB XML; if supplied, write an optimized XML and run pob calc.')
    p.add_argument('--skill', default='Vortex')
    # Deliberately no --pob-command: only the trusted executable named `pob` is allowed.
    p.add_argument('--output-xml')
    p.add_argument('--output-json', required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not args.pob_root:
        print(json.dumps({'status': 'blocked', 'error': '--pob-root 或 POB_ROOT 為必要欄位'}, ensure_ascii=False), file=sys.stderr)
        return 2
    try:
        nodes, graph = load_treedata(args.pob_root, args.tree_version)
        selected, warnings = build_connected_selection(nodes, graph, args.class_id, args.target_nodes, args.objective, set(args.required_node), set(args.exclude_node))
        tree_report = validate_selection(args.pob_root, args.tree_version, selected, args.class_id)
    except Exception as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    result: dict[str, Any] = {
        'schema_version': 1,
        'tree_version': args.tree_version,
        'class_id': args.class_id,
        'target_nodes': args.target_nodes,
        'selected_nodes': selected,
        'selected_node_count': len(selected),
        'objective': args.objective,
        'required_nodes': args.required_node,
        'excluded_nodes': args.exclude_node,
        'tree_connectivity': {'status': 'verified', **tree_report},
        'warnings': warnings,
        'pob_verification': {'status': 'not_run'},
    }
    if args.build:
        if not args.output_xml:
            raise SystemExit('--build 必須搭配 --output-xml')
        write_xml_with_nodes(args.build, args.output_xml, selected)
        result['output_xml'] = str(Path(args.output_xml).resolve())
        result['pob_verification'] = {'status': 'verified', 'analysis': run_pob_calc(args.output_xml, args.pob_root, args.skill)}
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output_json': args.output_json, 'output_xml': result.get('output_xml'), 'tree_status': 'verified', 'pob_status': result['pob_verification']['status']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

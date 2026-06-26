import numpy as np
from collections import deque
from typing import List, Dict
from .models import PipeNet, PumpNode, LoadNode


class ReliabilityAnalyzer:
    """流路及功能可靠性分析器"""
    
    @staticmethod
    def analyze(network: PipeNet, logs: List) -> Dict:
        """
        综合分析管网的可靠性
        返回：{
            "system_score": 0.85,  # 系统可靠性评分
            "load_status": {...},  # 各负载状态
            "flow_paths": {...},   # 关键流路
            "bottlenecks": [...]   # 瓶颈点
        }
        """
        # 1. 拓扑连通性分析 (从源点开始 BFS)
        connected_nodes = ReliabilityAnalyzer._find_connected_nodes(network)
        
        # 2. 节点功能性分析 (压力校核)
        load_status = {}
        for nid, node in network.nodes.items():
            if isinstance(node, LoadNode):
                load_status[nid] = ReliabilityAnalyzer._check_load_status(
                    node, connected_nodes
                )
        
        # 3. 计算系统可靠性评分 (加权平均)
        # 假设每个负载的重要性由其流量需求权重决定
        total_weight = sum(s['demand'] for s in load_status.values())
        if total_weight == 0: total_weight = 1
        
        score = sum(
            s['score'] * s['demand'] 
            for s in load_status.values()
        ) / total_weight
        
        # 4. 识别瓶颈路径
        bottlenecks = ReliabilityAnalyzer._identify_bottlenecks(network)
        
        return {
            "system_score": score,
            "load_status": load_status,
            "bottlenecks": bottlenecks,
            "other_nodes": network.nodes,
            "all_edges": network.edges
        }
    
    @staticmethod
    def _find_connected_nodes(network: PipeNet) -> set:
        """BFS 查找所有与源点连通的节点"""
        # 找到所有源点
        sources = [
            nid for nid, node in network.nodes.items() 
            if isinstance(node, PumpNode)
        ]
        
        connected = set()
        queue = deque(sources)
        
        while queue:
            current_id = queue.popleft()
            if current_id in connected:
                continue
            connected.add(current_id)
            
            # 遍历所有开启的边
            for eid, edge in network.edges.items():
                if not edge.is_open:
                    continue
                
                neighbor = None
                if edge.start_node_id == current_id:
                    neighbor = edge.end_node_id
                elif edge.end_node_id == current_id:
                    neighbor = edge.start_node_id
                
                if neighbor and neighbor not in connected:
                    queue.append(neighbor)
                    
        return connected
    
    @staticmethod
    def _check_load_status(node: LoadNode, connected_nodes: set) -> Dict:
        """检查单个负载的状态"""
        is_connected = node.id in connected_nodes
        
        # 状态 1: 物理隔离
        if not is_connected:
            return {
                "status": "FAILED",
                "score": 0.0,
                "reason": "物理隔离（流路中断）",
                "pressure": 0.0,
                "demand": node.min_flow
            }
        
        # 状态 2: 压力不足
        if node.computed_pressure < node.min_pressure:
            # 根据压力不足的程度计算得分 (0.0 ~ 0.5)
            ratio = node.computed_pressure / node.min_pressure if node.min_pressure > 0 else 0
            score = max(0, min(0.5, ratio * 0.5))
            return {
                "status": "DEGRADED",
                "score": score,
                "reason": f"压力不足 ({node.computed_pressure:.2f} < {node.min_pressure:.2f})",
                "pressure": node.computed_pressure,
                "demand": node.min_flow
            }
        
        # 状态 3: 正常
        # 得分 0.5 ~ 1.0，压力越充裕得分越高
        margin = (node.computed_pressure - node.min_pressure) / node.min_pressure if node.min_pressure > 0 else 1
        score = min(1.0, 0.8 + margin * 0.2)
        
        return {
            "status": "NORMAL",
            "score": score,
            "reason": "正常工作",
            "pressure": node.computed_pressure,
            "demand": node.min_flow
        }
    
    @staticmethod
    def _identify_bottlenecks(network: PipeNet) -> List[Dict]:
        """识别系统瓶颈（压降最大的管段）"""
        bottlenecks = []
        
        for eid, edge in network.edges.items():
            if not edge.is_open or abs(edge.computed_flow) < 0.01:
                continue
            
            p_start = network.nodes[edge.start_node_id].computed_pressure
            p_end = network.nodes[edge.end_node_id].computed_pressure
            dp = abs(p_start - p_end)
            
            # 如果压降占比超过系统总压力的 20%，视为潜在瓶颈
            max_p = max(n.computed_pressure for n in network.nodes.values())
            if max_p > 0 and dp / max_p > 0.2:
                bottlenecks.append({
                    "edge_id": eid,
                    "pressure_drop": dp,
                    "flow": edge.computed_flow,
                    "reason": "压降过大" if edge.resistance > 1.0 else "流速过高"
                })
        
        return sorted(bottlenecks, key=lambda x: x['pressure_drop'], reverse=True)

    @staticmethod
    def print_report(analysis_result: Dict, logs: List[str]):
        """打印美观的分析报告"""
        logs.append("\n" + "="*60)
        logs.append("【系统可靠性分析报告】")
        logs.append("="*60)
        
        score = analysis_result['system_score']
        status_icon = "✅" if score >= 0.8 else ("⚠️" if score >= 0.5 else "❌")
        logs.append(f"\n系统综合评分: {score*100:.1f}分 {status_icon}")
        
        logs.append("\n负载节点状态:")
        for nid, info in analysis_result['load_status'].items():
            icon = "✅" if info['status'] == "NORMAL" else ("⚠️" if info['status'] == "DEGRADED" else "❌")
            logs.append(f"  {icon} {nid:15s}: {info['status']:8s} | {info['reason']}")
        
        logs.append("\n其他节点状态:")
        for nid, node in analysis_result['other_nodes'].items():
            logs.append(f"  {nid:15s}: 当前压力{node.computed_pressure:.2f} MPa")
        
        if analysis_result['bottlenecks']:
            logs.append("\n关键瓶颈:")
            for bn in analysis_result['bottlenecks']:
                logs.append(f"  🔴 {bn['edge_id']}: 压降 {bn['pressure_drop']:.2f} MPa")
        else:
            logs.append("\n未检测到明显瓶颈。")

        logs.append("\n所有管段状态:")
        for eid, edge in analysis_result['all_edges'].items():
            logs.append(f"  {eid:15s}: 当前流量{edge.computed_flow:.2f} m³/s，管路流阻{edge.resistance:.2f},开关状态{'打开' if edge.is_open else '关闭'}")

       
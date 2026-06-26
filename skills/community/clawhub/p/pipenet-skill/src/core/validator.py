import numpy as np
from .models import PipeNet, PumpNode, LoadNode

class PipeNetValidator:
    """求解器结果验证工具"""
    
    @staticmethod
    def validate(network: PipeNet, logs: list, tolerance: float = 1e-4,) -> bool:
        logs.append("\n" + "="*60)
        logs.append("开始验证求解结果")
        logs.append("="*60)
        
        is_valid = True
        
        # 1. 验证节点流量守恒
        logs.append("\n[1] 节点流量守恒验证")
        for nid, node in network.nodes.items():
            if isinstance(node, PumpNode):
                continue # 源点流量由系统平衡决定，不强制守恒
            
            # 计算该节点的净流量
            # 查找所有连接到该节点的边
            net_flow = 0.0
            for eid, edge in network.edges.items():
                if not edge.is_open:
                    continue
                
                # 如果是流入 (边终点是当前节点)
                if edge.end_node_id == nid:
                    net_flow += edge.computed_flow
                # 如果是流出 (边起点是当前节点)
                elif edge.start_node_id == nid:
                    net_flow -= edge.computed_flow
            
            # 减去节点需求
            demand = 0.0
            if isinstance(node, LoadNode):
                demand = node.min_flow
            
            residual = net_flow - demand
            
            if abs(residual) > tolerance:
                logs.append(f"节点 {nid} 流量不平衡! 残差 = {residual:.6f} (流入:{net_flow:.2f}, 需求:{demand:.2f})")
                is_valid = False
            else:
                logs.append(f"节点 {nid} 流量平衡 (残差: {residual:.6f})")

        # 2. 验证管道压降一致性
        logs.append("\n[2] 管道压降一致性验证")
        for eid, edge in network.edges.items():
            if not edge.is_open:
                continue
                
            start_node = network.nodes[edge.start_node_id]
            end_node = network.nodes[edge.end_node_id]
            
            # 计算压差
            dp_node = start_node.computed_pressure - end_node.computed_pressure
            
            # 根据流量反推压差: dP = R * Q^2 * sign(Q)
            # 注意符号：如果 Q > 0 (正向流动)，dp_node 应该 > 0
            dp_edge = edge.resistance * (edge.computed_flow ** 2) * np.sign(edge.computed_flow)
            
            diff = abs(dp_node - dp_edge)
            
            if diff > tolerance:
                logs.append(f"边 {eid} 压降不一致! 节点压差={dp_node:.4f}, 流量反推压差={dp_edge:.4f}")
                is_valid = False
            else:
                logs.append(f"边 {eid} 压降一致 (误差: {diff:.6f})")
                
        # 3. 验证源点压力设定
        logs.append("\n[3] 源点压力边界验证")
        for nid, node in network.nodes.items():
            if isinstance(node, PumpNode):
                if abs(node.computed_pressure - node.pressure) > tolerance:
                    logs.append(f"源点 {nid} 压力偏移设定值!")
                    is_valid = False
                else:
                    logs.append(f"源点 {nid} 压力固定在 {node.pressure} MPa")

        logs.append("\n" + "="*60)
        if is_valid:
            logs.append("验证通过！求解器计算结果准确。")
        else:
            logs.append("验证失败！请检查求解器逻辑。")
        logs.append("="*60)
        
        return is_valid
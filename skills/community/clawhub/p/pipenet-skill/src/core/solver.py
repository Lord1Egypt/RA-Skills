import numpy as np
from scipy.optimize import root
from .models import PipeNet, PumpNode, LoadNode

class PipeNetSolver:
    def __init__(self, network: PipeNet, logs: list):
        self.logs = logs
        self.network = network
        self.node_list = list(network.nodes.keys()) # 建立节点ID到索引的映射
        self.num_nodes = len(self.node_list)
        
        # 预处理：建立邻接表，方便查找连向节点的边
        # adj_list[node_id] = [(edge_id, neighbor_id), ...]
        self.adj_list = {nid: [] for nid in self.node_list}
        for eid, edge in network.edges.items():
            if edge.is_open: # 只考虑开启的边
                self.adj_list[edge.start_node_id].append((eid, edge.end_node_id, 'out'))
                self.adj_list[edge.end_node_id].append((eid, edge.start_node_id, 'in'))

    def solve(self):
        """主求解函数"""
        # 1. 设置初始猜测值 (假设所有节点压力为 0)
        x0 = np.zeros(self.num_nodes)
        
        # 给 Source 节点赋予初值，加速收敛
        for i, nid in enumerate(self.node_list):
            node = self.network.nodes[nid]
            if isinstance(node, PumpNode):
                x0[i] = node.pressure

        # 2. 定义残差函数
        def equations(pressures):
            residuals = np.zeros(self.num_nodes)
            
            for i, nid in enumerate(self.node_list):
                node = self.network.nodes[nid]
                p_current = pressures[i]
                
                # 情况 A: Source 节点 (压力已知)
                if isinstance(node, PumpNode):
                    residuals[i] = p_current - node.pressure
                    continue
                
                # 情况 B: Junction/Load 节点 (流量平衡)
                # 方程: sum(Q_in) - sum(Q_out) - Demand = 0
                
                net_flow = 0.0
                
                # 遍历连接该节点的所有边
                for eid, neighbor_id, direction in self.adj_list[nid]:
                    edge = self.network.edges[eid]
                    # 找到邻居节点的压力
                    j = self.node_list.index(neighbor_id)
                    p_neighbor = pressures[j]
                    
                    # 计算压差
                    dp = p_neighbor - p_current
                    
                    # 如果 direction 是 'in'，说明邻居是上游 (neighbor -> current)
                    # 如果 direction 是 'out'，说明邻居是下游 (current -> neighbor)
                    # 统一公式: Q = sign(P_up - P_down) * sqrt(|dp|/R)
                    
                    if direction == 'in': 
                        # 邻居 -> 当前节点
                        # 如果 P_neighbor > P_current, Q 为正 (流入)
                        q = np.sign(p_neighbor - p_current) * np.sqrt(abs(p_neighbor - p_current) / edge.resistance)
                        net_flow += q
                    else:
                        # 当前节点 -> 邻居
                        # 如果 P_current > P_neighbor, Q 为正 (流出)
                        q = np.sign(p_current - p_neighbor) * np.sqrt(abs(p_current - p_neighbor) / edge.resistance)
                        net_flow -= q # 流出为负
                
                # 减去负载需求
                demand = 0.0
                if isinstance(node, LoadNode):
                    demand = node.min_flow
                
                residuals[i] = net_flow - demand
            
            return residuals

        # 3. 调用求解器
        sol = root(equations, x0, method='hybr') # hybr 或 lm 方法
        
        if not sol.success:
            self.logs.append(f"求解失败: {sol.message}")
            return False

        # 4. 回填结果
        self._update_results(sol.x)
        return True

    def _update_results(self, pressures):
        """将求解结果写回对象"""
        # 更新节点压力
        for i, nid in enumerate(self.node_list):
            node = self.network.nodes[nid]
            node.computed_pressure = pressures[i]
            
            # 计算节点流量平衡
            inflow = 0
            for eid, neighbor_id, direction in self.adj_list[nid]:
                edge = self.network.edges[eid]
                p_neighbor = self.network.nodes[neighbor_id].computed_pressure
                if direction == 'in':
                    q = np.sign(p_neighbor - node.computed_pressure) * np.sqrt(abs(p_neighbor - node.computed_pressure) / edge.resistance)
                    inflow += q
            node.computed_inflow = inflow

        # 更新边流量
        for eid, edge in self.network.edges.items():
            if not edge.is_open:
                edge.computed_flow = 0
                continue
                
            p_start = self.network.nodes[edge.start_node_id].computed_pressure
            p_end = self.network.nodes[edge.end_node_id].computed_pressure
            
            q = np.sign(p_start - p_end) * np.sqrt(abs(p_start - p_end) / edge.resistance)
            edge.computed_flow = q
            
            # 简单流速估算 (假设有管径)
            # if edge.diameter:
            #     area = 3.14 * (edge.diameter/2)**2
            #     edge.computed_velocity = q / area
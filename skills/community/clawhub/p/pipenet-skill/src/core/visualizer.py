import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Optional
import os

# 尝试导入 pyvis，用于生成交互式网页
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False
    print("警告: 未安装 pyvis，将无法生成交互式网页。请执行 pip install pyvis")

# 假设 PipeNet 相关类在 PipeNet.py 中
from models import PipeNet, PumpNode, LoadNode, Edge

class PipeNetVisualizer:
    def __init__(self, network: PipeNet):
        self.network = network
        self.graph = self._build_graph()
    
    def _build_graph(self) -> nx.DiGraph:
        """将 PipeNet 转换为 networkx 的有向图对象"""
        G = nx.DiGraph()
        
        # 1. 添加节点
        for nid, node in self.network.nodes.items():
            # 提取节点属性用于显示
            attrs = {
                "label": nid,
                "type": node.type.value,
                "computed_pressure": getattr(node, 'computed_pressure', 0.0),
                "color": self._get_node_color(node),
                "shape": self._get_node_shape(node)
            }
            
            # 补充特定类型属性
            if isinstance(node, PumpNode):
                attrs["pressure_set"] = node.pressure
                attrs["title"] = f"<b>{nid}</b><br>类型: 泵站<br>设定压力: {node.pressure} MPa<br>计算压力: {attrs['computed_pressure']:.2f} MPa"
            elif isinstance(node, LoadNode):
                attrs["demand"] = node.min_flow
                attrs["title"] = f"<b>{nid}</b><br>类型: 负载<br>需求流量: {node.min_flow}<br>需求压力: {node.min_pressure}<br>计算压力: {attrs['computed_pressure']:.2f} MPa"
            else:
                attrs["title"] = f"<b>{nid}</b><br>类型: 三通<br>计算压力: {attrs['computed_pressure']:.2f} MPa"
            
            G.add_node(nid, **attrs)
            
        # 2. 添加边
        for eid, edge in self.network.edges.items():
            flow = getattr(edge, 'computed_flow', 0.0)
            
            # 边的属性
            attrs = {
                "label": f"{eid}\n(R={edge.resistance})",
                "resistance": edge.resistance,
                "is_open": edge.is_open,
                "computed_flow": flow,
                "color": "green" if edge.is_open else "red",
                "width": 2 if edge.is_open else 1,
                "arrows": "to",
                "title": f"管道: {eid}<br>流阻: {edge.resistance}<br>流量: {flow:.2f}<br>状态: {'开启' if edge.is_open else '关闭'}"
            }
            
            G.add_edge(edge.start_node_id, edge.end_node_id, **attrs)
            
        return G

    def _get_node_color(self, node) -> str:
        if isinstance(node, PumpNode): return "#3498db" # 蓝色
        if isinstance(node, LoadNode): 
            # 如果计算过压力，根据达标情况变色
            if hasattr(node, 'computed_pressure'):
                if node.computed_pressure >= node.min_pressure:
                    return "#2ecc71" # 绿色 (正常)
                else:
                    return "#e74c3c" # 红色 (压力不足)
            return "#f1c40f" # 黄色 (默认)
        return "#95a5a6" # 灰色

    def _get_node_shape(self, node) -> str:
        if isinstance(node, PumpNode): return "box"
        if isinstance(node, LoadNode): return "diamond"
        return "dot"

    def generate_interactive_html(self, save_path: str = "pipenet_viz.html"):
        """生成交互式 HTML 文件
        Args:
            save_path: HTML 文件保存路径
        """
        if not PYVIS_AVAILABLE:
            print("✗ 缺少 pyvis 库，无法生成交互式网页。")
            return

        # 创建 Pyvis 网络
        net = Network(height="750px", width="100%", directed=True, notebook=False)
        
        # 从 networkx 对象加载
        net.from_nx(self.graph)
        
        # 设置物理布局参数，让图更美观
        net.barnes_hut(gravity=-2000, central_gravity=0.3, spring_length=100)
        
        # 保存文件
        net.save_graph(save_path)
        print(f"✓ 交互式网页已生成: {save_path}")
        print(f"  请使用浏览器打开查看。")
        return save_path

if __name__ == "__main__":
    from loader import PipeNetLoader
    network = PipeNetLoader.load("测试管网.toml")
    # network.apply_scenario('temporary_load_addition')
    from solver import PipeNetSolver
    solver = PipeNetSolver(network)
    solver.solve()
    
    visualizer = PipeNetVisualizer(network)
    visualizer.generate_interactive_html()       # 生成网页
    
    pass

from dataclasses import dataclass, field
from typing import List, Dict, Union, Any, Optional
from enum import Enum

class NodeType(Enum):
    SOURCE = "source"      # 泵/源
    LOAD = "load"          # 负载
    JUNCTION = "junction"  # 三通/节点

class ActionType(Enum):
    CLOSE_VALVE = "close_valve"                 # 关闭阀门
    OPEN_VALVE = "open_valve"                   # 打开阀门
    CHANGE_PRESSURE = "change_pressure"         # 改变压力
    CHANGE_RESISTANCE = "change_resistance"     # 改变流阻
    MIN_FLOW = "change_min_flow"                 # 改变负载最小需求流量
    MIN_PRESSURE = "change_min_pressure"         # 改变负载最小需求压力
    ADD_NODE = "add_node"                       # 添加节点
    REMOVE_NODE = "remove_node"                 # 删除节点
    ADD_EDGE = "add_edge"                       # 添加边
    REMOVE_EDGE = "remove_edge"                 # 删除边


@dataclass
class Node:
    """节点类：泵、负载、三通等，可拓展NodeType和属性如Tank容器以及对应的capacity容量等参数"""
    id: str
    type: NodeType

    computed_pressure: float = 0.0  # 计算得到的压力
    computed_inflow: float = 0.0    # 计算得到的流入流量 (正值)

@dataclass
class PumpNode(Node):
    type: NodeType = NodeType.SOURCE

    pressure: float = -1.0      # source节点：输出压力

@dataclass
class LoadNode(Node):
    type: NodeType = NodeType.LOAD

    is_worked: bool = True      # load节点：是否工作
    min_flow: float = -1.0      # load节点：最小需求流量
    min_pressure: float = -1.0  # load节点：最小需求压力


@dataclass
class Edge:
    """边类：管路，包括管路的起始节点和结束节点以及管路流阻，另外可以设置阀门的开关和管径"""
    id: str
    start_node_id: str                   # 起始节点 ID
    end_node_id: str                     # 结束节点 ID
    resistance: float = 0.1              # 管路流阻 R

    computed_flow: float = 0.0      # 计算得到的流量 (正值表示 start->end)
    computed_velocity: float = 0.0  # 流速 (如果有管径)

    is_open: bool = True                 # 阀门开关

@dataclass
class ScenarioAction:
    """动作：如关阀门、改压力等，用于修改管路状态"""
    target_id: str                 # 目标节点或边的 ID
    action_type: ActionType        # "close_valve", "open_valve", "change_pressure"， "change_resistance"等枚举项
    
    value: Optional[Union[float, Dict[str, Any]]] = None  # 新值（如新压力）

@dataclass
class Scenario:
    """一个工况场景"""
    name: str
    description: str = ""
    actions: List[ScenarioAction] = field(default_factory=list)

@dataclass
class PipeNet:
    """管网类：包括节点、边、工况等"""
    name: str
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)
    scenarios: Dict[str, Scenario] = field(default_factory=dict)
    
    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        """根据 ID 查找节点"""
        return self.nodes.get(node_id, None)
    
    def get_edge_by_id(self, edge_id: str) -> Optional[Edge]:
        """根据 ID 查找边"""
        return self.edges.get(edge_id, None)

    def add_node(self, node: Node) -> bool:
        """添加节点"""

        if node.id in self.nodes:
            print(f'节点 {node.id} 已存在')
            return False
        
        self.nodes[node.id] = node
        return True

    def add_edge(self, edge:Edge) -> bool:
        """添加边"""

        if edge.id in self.edges:
            print(f'边 {edge.id} 已存在')
            return False

            # 检查边是否存在
        if edge.start_node_id not in self.nodes or edge.end_node_id not in self.nodes:
            print(f"边 {edge.id} 的端点 {edge.start_node_id} 或 {edge.end_node_id} 不存在")
            return False

        self.edges[edge.id] = edge
        return True
        

    def remove_node(self, node_id: str) -> bool:
        """删除节点"""
        if node_id in self.nodes:
            for edge_id, edge in self.edges.items():
                if edge.start_node_id == node_id or edge.end_node_id == node_id:
                    self.edges.pop(edge_id)
                    print(f"删除边: {edge_id}")
            self.nodes.pop(node_id)
            print(f"删除节点: {node_id}")
            return True
        print(f'Node {node_id} does not exist.')
        return False

    def remove_edge(self, edge_id: str) -> bool:
        """删除边"""
        if edge_id in self.edges:
            self.edges.pop(edge_id)
            print(f"删除边: {edge_id}")
            return True
        print(f'Edge {edge_id} does not exist.')
        return False
    
    def apply_scenario(self, scenario_name: str) -> bool:
        # 1. 查找工况
        scenario = self.scenarios.get(scenario_name)
        
        # 2. 遍历所有动作
        try:
            for action in scenario.actions:
                # 3. 根据动作类型执行操作
                if action.action_type == ActionType.CLOSE_VALVE:     
                    # 关闭阀门
                    edge = self.get_edge_by_id(action.target_id)
                    if edge is not None:
                        edge.is_open = False

                elif action.action_type == ActionType.OPEN_VALVE:    
                    # 打开阀门
                    edge = self.get_edge_by_id(action.target_id)
                    if edge is not None:
                        edge.is_open = True

                elif action.action_type == ActionType.CHANGE_PRESSURE:     
                    # 改变压力
                    if not isinstance(action.value, float):
                        print("错误：CHANGE_PRESSURE 的 value 必须是浮点数")
                        continue

                    node = self.get_node_by_id(action.target_id)
                    if node.type == NodeType.SOURCE:
                        node.pressure = action.value
                    else:
                        raise ValueError(f"Node {node.id} is not a source node, cannot change pressure.")

                elif action.action_type == ActionType.CHANGE_RESISTANCE:    
                    # 改变流阻
                    if not isinstance(action.value, float):
                        print("错误：CHANGE_RESISTANCE 的 value 必须是浮点数")
                        continue

                    edge = self.get_edge_by_id(action.target_id)
                    edge.resistance = action.value

                elif action.action_type == ActionType.MIN_FLOW:
                    # 改变负载最小工作流量
                    if not isinstance(action.value, float):
                        print("错误：MIN_FLOW 的 value 必须是浮点数")
                        continue

                    node = self.get_node_by_id(action.target_id)
                    if node.type == NodeType.LOAD:
                        node.min_flow = action.value
                    else:
                        raise ValueError(f"Node {node.id} is not a load node, cannot change min_flow.")
                elif action.action_type == ActionType.MIN_PRESSURE:
                    # 改变负载最小工作压力
                    if not isinstance(action.value, float):
                        print("错误：MIN_PRESSURE 的 value 必须是浮点数")
                        continue

                    node = self.get_node_by_id(action.target_id)
                    if node.type == NodeType.LOAD:
                        node.min_pressure = action.value
                    else:
                        raise ValueError(f"Node {node.id} is not a load node, cannot change min_pressure.")
                elif action.action_type == ActionType.ADD_NODE:
                    # 添加节点
                    attrs = action.value
                    if not isinstance(attrs, dict):
                        print("错误：ADD_NODE 的 value 必须是属性字典")
                        continue
                    
                    # 处理 NodeType 枚举转换
                    if 'type' in attrs and isinstance(attrs['type'], str):
                        attrs['type'] = NodeType(attrs['type'])
                    else:
                        raise ValueError("ADD_NODE 的 value 必须包含 type 键，且 type 键的值必须是字符串")
                    
                    # 创建节点对象 (使用解包 **attrs)
                    if attrs['type'] == NodeType.SOURCE:
                        new_node = PumpNode(**attrs)
                    elif attrs['type'] == NodeType.LOAD:
                        new_node = LoadNode(**attrs)
                    else:
                        new_node = Node(**attrs)

                    if self.add_node(new_node):
                        print(f"新增节点: {new_node.id} ({new_node.type.value})")

                elif action.action_type == ActionType.REMOVE_NODE:
                    # 删除节点
                    self.remove_node(action.target_id)

                elif action.action_type == ActionType.ADD_EDGE:
                    # 添加边
                    attrs = action.value
                    if not isinstance(attrs, dict):
                        print("错误：ADD_EDGE 的 value 必须是属性字典")
                        continue
                    
                    # 创建边对象
                    new_edge = Edge(**attrs)
                    if self.add_edge(new_edge): # 内部会检查端点是否存在
                        print(f"新增边: {new_edge.id} ({new_edge.start_node_id} -> {new_edge.end_node_id})")

                elif action.action_type == ActionType.REMOVE_EDGE:
                    # 删除边
                    self.remove_edge(action.target_id)
        
        except Exception as e:
            print(f"Error: {e}")
            return False
        
        return True


if __name__ == "__main__":
    print(NodeType('load').value)
    # node1 = PumpNode(id="pump1", pressure=10.0)
    # node2 = LoadNode(id="load1", min_flow=10.0, min_pressure=5.0)
    # edge1 = Edge(id="edge1", start_node_id="pump1", end_node_id="load1", resistance=0.1)
    # pipe_net = PipeNet(name="test_pipe_net", nodes={node1.id: node1, node2.id: node2}, edges={edge1.id: edge1})

    # print(pipe_net.get_node_by_id('pump1').pressure)
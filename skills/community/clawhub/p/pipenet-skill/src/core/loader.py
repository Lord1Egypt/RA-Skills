import tomllib
import sys
from typing import Optional, Dict
from .models import NodeType, ActionType, Scenario, ScenarioAction
from .models import PipeNet, Node, Edge, LoadNode, PumpNode

class PipeNetLoader:
    """TOML 文件解析器"""
    
    @staticmethod
    def load_from_file(toml_file_path: str) -> Optional[PipeNet]:
        try:
            # 需要 Python 3.11+ 版本支持
            if sys.version_info >= (3, 11):
                with open(toml_file_path, "rb") as f:
                    data = tomllib.load(f)
            
            print(f"成功加载 TOML 文件: {toml_file_path}")
            return PipeNetLoader._parse_pipenet(data)
            
        except FileNotFoundError:
            print(f"错误：文件未找到 {toml_file_path}")
            return None
        except Exception as e:
            print(f"解析错误: {e}")
            return None

    @staticmethod
    def load_from_dict(toml_dict: Dict) -> Optional[PipeNet]:
        try:
            return PipeNetLoader._parse_pipenet(toml_dict)
        except Exception as e:
            print(f"解析错误: {e}")
            return None
        
    @staticmethod
    def _parse_pipenet(data: Dict) -> PipeNet:
        # 1. 解析网络元数据
        net_info = data.get('network', {})
        pipe_net = PipeNet(name=net_info.get('name', 'default_network'))

        # 2. 解析节点
        for node_data in data.get('nodes', []):
            node = PipeNetLoader._create_node(node_data, data['nodes'][node_data])
            if node:
                pipe_net.nodes[node.id] = node
        
        print(f"  - 解析节点: {len(pipe_net.nodes)} 个")

        # 3. 解析边
        for edge_data in data.get('edges', []):
            edge = Edge(id=edge_data, **data['edges'][edge_data])
            pipe_net.edges[edge.id] = edge
            
        print(f"  - 解析边: {len(pipe_net.edges)} 条")

        # 4. 解析工况
        scenarios_data = data.get('scenarios', {})
        for s_key, s_data in scenarios_data.items():
            scenario = PipeNetLoader._create_scenario(s_key, s_data)
            pipe_net.scenarios[scenario.name] = scenario
            
        print(f"  - 解析工况: {len(pipe_net.scenarios)} 个")

        return pipe_net

    @staticmethod
    def _create_node(id: str, data: Dict) -> Optional[Node]:
        """根据类型创建不同的节点对象"""
        node_type_str = data.get('type', 'junction')
        try:
            node_type = NodeType(node_type_str)
        except ValueError:
            print(f"警告：未知节点类型 {node_type_str}，使用默认节点")
            node_type = NodeType.JUNCTION

        # 使用 data 的副本，避免修改原数据
        attrs = data.copy()
        attrs['id'] = id
        attrs['type'] = node_type

        if node_type == NodeType.SOURCE:
            return PumpNode(**attrs)
        elif node_type == NodeType.LOAD:
            return LoadNode(**attrs)
        else:
            return Node(**attrs)

    @staticmethod
    def _create_scenario(key: str, data: Dict) -> Scenario:
        """创建工况对象"""
        actions = []
        for act_data in data.get('actions', []):
            # 将字符串转换为枚举
            action_type_str = act_data.get('action_type')
            try:
                action_type = ActionType(action_type_str)
            except ValueError:
                print(f"警告：未知动作类型 {action_type_str}")
                continue
            
            actions.append(ScenarioAction(
                target_id=act_data.get('target_id'),
                action_type=action_type,
                value=act_data.get('value', None) # value 可能是 float 或 dict
            ))
            
        return Scenario(
            name=key,
            description=data.get('description', ''),
            actions=actions
        )

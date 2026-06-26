# src/skill.py
import os
import tomllib
from typing import List, Dict, Optional, Any
from core.loader import PipeNetLoader
from core.solver import PipeNetSolver
from core.validator import PipeNetValidator
from core.analyzer import ReliabilityAnalyzer
from core.visualizer import PipeNetVisualizer

class PipeNetSkill:
    """
    流体管网设计与分析技能
    支持 Agent 进行设计生成、仿真求解和可靠性评估。
    """

    @staticmethod
    def design_network(toml_content: str) -> Dict[str, Any]:
        """
        Skill入口函数：接收Agent生成的TOML字符串，生成管网字典。
        工具1: 流体管网设计生成器
        根据输入参数生成符合 Schema 的 TOML 配置字符串。
        
        Args:
            toml_content (str): Agent生成的TOML配置字符串。
        
        Returns:
            Dict: 包含解析状态、管网名称、节点/边数量或错误信息的字典。
        """
        try:
            
            data = tomllib.loads(toml_content)

            # 2. 调用已有的 PipeNetLoader 进行解析
            pipe_net = PipeNetLoader.load_from_dict(data)

            if pipe_net is None:
                return {
                    "success": False,
                    "message": "TOML解析失败，请检查格式或逻辑错误。请参考日志修正。"
                }
            
            with open(f'./src/toml/{pipe_net.name}.toml', 'w', encoding='utf-8') as f:
                f.write(toml_content)

            result = {
                "success": True,
                "message": "管网系统设计成功并已加载。",
                "network_info": {
                    "name": pipe_net.name,
                    "node_count": len(pipe_net.nodes),
                    "edge_count": len(pipe_net.edges),
                    "scenario_count": len(pipe_net.scenarios)
                },
                "file_path": f'./src/toml/{pipe_net.name}.toml'
            }
            return result

        except Exception as e:
            return {
                "success": False,
                "message": f"处理过程中发生异常: {str(e)}"
            }
    
    @staticmethod
    def analyze_network(file_path: str, scenario_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Skill入口函数：接收Agent上传的TOML文件路径，求解管网状态，分析系统可靠性、管路、负载情况等。
        工具2: 流体管网求解器
        根据输入参数求解管网状态，分析系统可靠性、管路、负载情况等。
        
        Args:
            file_path (str): Agent上传的TOML文件路径。
            scenario_name (Optional[str]): 工况名称，可选。
            
        Returns:
            Dict: 包含求解状态、求解结果或错误信息的字典。
        """
        logs: List[str] = []
        try:
            # 1. 加载管网配置
            pipe_net = PipeNetLoader.load_from_file(file_path)

            if pipe_net is None:
                logs.append(f"错误：TOML解析失败，请检查格式或逻辑错误。请参考日志修正。")
                return {
                    "success": False,
                    "message": "TOML解析失败，请检查格式或逻辑错误。请参考日志修正。",
                    "excution_log": logs
                }
            logs.append(f"成功加载 TOML 文件: {file_path}")
            
            logs.append(f"开始应用工况...")
            
            if scenario_name is not None:
                for s in scenario_name.split(';'):
                    scenario = pipe_net.scenarios.get(s, None)
                    if scenario is None:
                        logs.append(f"工况 {s} 不存在，未执行。")
                    else:
                        pipe_net.apply_scenario(s)
                        logs.append(f"成功应用工况 {s}")
            
            # 2. 调用求解器
            logs.append(f"开始求解管网状态...")
            solver_fault = PipeNetSolver(pipe_net, logs)
            if solver_fault.solve():
                logs.append('求解成功')
            else:
                logs.append('求解失败')
                return {
                    "success": False,
                    "message": "求解管网状态失败，请检查格式或逻辑错误。请参考日志修正。",
                    "excution_log": logs
                }
            
            logs.append(f"开始验证求解结果...")
            if PipeNetValidator.validate(pipe_net, logs):
                logs.append('求解结果验证通过')
            else:
                logs.append('求解结果验证未通过')
                return {
                    "success": False,
                    "message": "求解结果验证未通过，请检查格式或逻辑错误。请参考日志修正。",
                    "excution_log": logs
                }
            
            logs.append(f"开始分析管网状态...")
            reliability = ReliabilityAnalyzer.analyze(pipe_net, logs)
            ReliabilityAnalyzer.print_report(reliability, logs)

            return {
                "success": True,
                "message": "管网状态求解成功并已分析，分析过程详见excution_log。",
                "network_info": {
                    "name": pipe_net.name,
                    "node_count": len(pipe_net.nodes),
                    "edge_count": len(pipe_net.edges),
                    "scenario_count": len(pipe_net.scenarios)
                },
                "file_path": f'./src/toml/{pipe_net.name}.toml',
                "excution_log": logs
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"处理过程中发生异常: {str(e)}",
                "excution_log": logs
            }

    @staticmethod
    def visualize_network(file_path:str, scenario_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Skill入口函数：接收Agent上传的TOML文件路径，可视化管网状态。
        工具3: 流体管网可视化器
        根据输入参数可视化管网状态。
        
        Args:
            file_path (str): Agent上传的TOML文件路径。
            scenario_name (Optional[str]): 工况名称，可选。
            
        Returns:
            Dict: 包含可视化状态、可视化结果或错误信息的字典。
        """
        logs: List[str] = []
        try:
            # 1. 加载管网配置
            pipe_net = PipeNetLoader.load_from_file(file_path)

            if scenario_name is not None:
                for s in scenario_name.split(';'):
                    scenario = pipe_net.scenarios.get(s, None)
                    if scenario is None:
                        logs.append(f"工况 {s} 不存在，未执行。")
                    else:
                        pipe_net.apply_scenario(s)
                        logs.append(f"成功应用工况 {s}")
            
            # 2. 调用可视化器
            visualizer = PipeNetVisualizer(pipe_net)
            visualizer.generate_interactive_html(f'./src/html/{pipe_net.name}_{scenario_name}.html')
            return {
                "success": True,
                "message": f"可视化成功，HTML文件已生成。",
                "html_file": f'./src/html/{pipe_net.name}_{scenario_name}.html',
                "excution_log": logs
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"处理过程中发生异常: {str(e)}",
                "excution_log": logs
            }

# 为了方便 Agent 调用，通常暴露一个函数列表
SKILL_FUNCTIONS = {
    "design_network": PipeNetSkill.design_network,
    "analyze_network": PipeNetSkill.analyze_network,
    "visualize_network": PipeNetSkill.visualize_network
}


if __name__ == "__main__":
    # 测试设计网络
    with open("./src/toml/测试管网.toml", "r", encoding="utf-8") as f:
        toml_content = f.read()
        result = PipeNetSkill.design_network(toml_content)
        print(result)
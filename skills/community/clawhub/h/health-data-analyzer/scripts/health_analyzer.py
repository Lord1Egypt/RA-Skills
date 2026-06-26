#!/usr/bin/env python3
"""
健康数据分析助手脚本
提供标准化的健康数据查询和分析功能
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class HealthDataAnalyzer:
    """健康数据分析器"""
    
    def __init__(self):
        self.server_name = "healthdata"
        
    def run_mcporter_command(self, command: str) -> Dict[str, Any]:
        """执行 mcporter 命令并返回结果"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                check=True
            )
            
            # 尝试解析 JSON 输出
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"raw_output": result.stdout, "error": None}
                
        except subprocess.CalledProcessError as e:
            return {"error": f"命令执行失败: {e}", "stderr": e.stderr}
    
    def list_tables(self) -> Dict[str, Any]:
        """第一步：列出所有可用数据表"""
        command = f"mcporter call {self.server_name}.list_available_tables"
        return self.run_mcporter_command(command)
    
    def get_table_schema(self, table_names: List[str]) -> Dict[str, Any]:
        """第二步：获取指定表的字段结构"""
        table_list_json = json.dumps(table_names)
        command = f"mcporter call {self.server_name}.get_table_schema table_list='{table_list_json}'"
        return self.run_mcporter_command(command)
    
    def query_table_data(self, table_name: str, start_date: str, end_date: str, 
                        conversation_time: Optional[str] = None) -> Dict[str, Any]:
        """第三步：查询表数据"""
        if conversation_time is None:
            conversation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        command = (f"mcporter call {self.server_name}.query_table_data "
                  f"table_name={table_name} start_date={start_date} "
                  f"end_date={end_date} conversation_time=\"{conversation_time}\"")
        return self.run_mcporter_command(command)
    
    def analyze_sleep_quality(self, days: int = 7) -> Dict[str, Any]:
        """睡眠质量分析"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        results = {}
        
        # 获取睡眠分段数据
        sleep_segments = self.query_table_data("sleep_segments", start_date, end_date)
        results["sleep_segments"] = sleep_segments
        
        # 获取睡眠评分数据
        sleep_calculations = self.query_table_data("sleep_calculations", start_date, end_date)
        results["sleep_calculations"] = sleep_calculations
        
        return results
    
    def analyze_recovery_status(self, days: int = 7) -> Dict[str, Any]:
        """恢复状态分析"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        results = {}
        
        # 获取恢复评分数据
        recovery_calculations = self.query_table_data("recovery_calculations", start_date, end_date)
        results["recovery_calculations"] = recovery_calculations
        
        # 获取健康指标数据
        metrics_segments = self.query_table_data("metrics_segments", start_date, end_date)
        results["metrics_segments"] = metrics_segments
        
        return results
    
    def analyze_exercise_performance(self, days: int = 30) -> Dict[str, Any]:
        """运动表现分析"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        results = {}
        
        # 获取训练分段数据
        training_segments = self.query_table_data("training_segments", start_date, end_date)
        results["training_segments"] = training_segments
        
        # 获取运动负荷数据
        strain_calculations = self.query_table_data("strain_calculations", start_date, end_date)
        results["strain_calculations"] = strain_calculations
        
        return results
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户基础信息"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        results = {}
        
        # 获取用户信息
        users = self.query_table_data("users", today, today)
        results["users"] = users
        
        # 获取数据源信息
        user_data_sources = self.query_table_data("user_data_sources", today, today)
        results["user_data_sources"] = user_data_sources
        
        return results

def main():
    """主函数 - 命令行接口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 health_analyzer.py list_tables")
        print("  python3 health_analyzer.py sleep_analysis [days]")
        print("  python3 health_analyzer.py recovery_analysis [days]")
        print("  python3 health_analyzer.py exercise_analysis [days]")
        print("  python3 health_analyzer.py user_info")
        return
    
    analyzer = HealthDataAnalyzer()
    command = sys.argv[1]
    
    if command == "list_tables":
        result = analyzer.list_tables()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "sleep_analysis":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        result = analyzer.analyze_sleep_quality(days)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "recovery_analysis":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        result = analyzer.analyze_recovery_status(days)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "exercise_analysis":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = analyzer.analyze_exercise_performance(days)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "user_info":
        result = analyzer.get_user_info()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MATLAB Bridge - MATLAB调用桥接脚本
支持直接执行MATLAB代码、运行.m脚本、数据交互
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


class MATLABBridge:
    """MATLAB桥接类，用于调用MATLAB进行计算"""
    
    def __init__(self, matlab_path: Optional[str] = None, 
                 output_dir: Optional[str] = None):
        """
        初始化MATLAB桥接
        
        Args:
            matlab_path: MATLAB可执行文件路径，None则自动查找
            output_dir: 输出目录，默认使用matlab-outputs
        """
        self.matlab_path = matlab_path or self._find_matlab()
        self.output_dir = output_dir or self._get_default_output_dir()
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 检查MATLAB是否可用
        if not self._check_matlab():
            raise RuntimeError("MATLAB不可用，请检查安装和PATH配置")
    
    def _find_matlab(self) -> str:
        """自动查找MATLAB路径"""
        # 常见MATLAB安装路径
        common_paths = [
            r"C:\Program Files\MATLAB",
            r"C:\Program Files (x86)\MATLAB",
            r"D:\MATLAB",
        ]
        
        # 查找最新版本
        versions = []
        for base_path in common_paths:
            if os.path.exists(base_path):
                for folder in os.listdir(base_path):
                    if folder.startswith('R'):
                        versions.append((folder, os.path.join(base_path, folder)))
        
        if versions:
            # 按版本号排序，取最新的
            versions.sort(reverse=True)
            matlab_exe = os.path.join(versions[0][1], 'bin', 'matlab.exe')
            if os.path.exists(matlab_exe):
                return matlab_exe
        
        # 尝试从PATH中找
        return 'matlab'
    
    def _get_default_output_dir(self) -> str:
        """获取默认输出目录"""
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent.parent  # 回到OpenClaw根目录
        output_dir = root_dir / 'matlab-outputs'
        return str(output_dir)
    
    def _check_matlab(self) -> bool:
        """检查MATLAB是否可用"""
        try:
            cmd = [self.matlab_path, '-batch', "disp('OK')"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return 'OK' in result.stdout or result.returncode == 0
        except:
            return False
    
    def execute(self, code: str, 
                save_workspace: bool = True,
                capture_output: bool = True) -> Dict[str, Any]:
        """
        直接执行MATLAB代码
        
        Args:
            code: MATLAB代码字符串
            save_workspace: 是否保存工作区变量
            capture_output: 是否捕获输出
        
        Returns:
            执行结果字典
        """
        # 创建临时.m文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_name = f"matlab_exec_{timestamp}"
        
        # 构建完整的代码
        full_code = self._build_wrapper_code(code, temp_name, save_workspace)
        
        # 写入临时文件
        temp_dir = tempfile.mkdtemp()
        m_file = os.path.join(temp_dir, f'{temp_name}.m')
        
        try:
            with open(m_file, 'w', encoding='utf-8') as f:
                f.write(full_code)
            
            # 执行MATLAB
            cmd = [
                self.matlab_path,
                '-nodisplay',  # 无GUI
                '-nosplash',   # 不显示启动画面
                '-batch',      # 批处理模式
                f"cd('{temp_dir}'); {temp_name}"
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=capture_output, 
                text=True, 
                timeout=300  # 5分钟超时
            )
            
            # 读取结果
            output_data = {}
            result_file = os.path.join(self.output_dir, f'{temp_name}_results.json')
            if os.path.exists(result_file):
                with open(result_file, 'r', encoding='utf-8') as f:
                    output_data = json.load(f)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout if capture_output else '',
                'stderr': result.stderr if capture_output else '',
                'output_data': output_data,
                'timestamp': timestamp
            }
            
        finally:
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _build_wrapper_code(self, user_code: str, temp_name: str, save_workspace: bool) -> str:
        """构建包装代码，添加错误处理和结果保存"""
        
        # 处理Windows路径中的反斜杠
        output_dir_escaped = self.output_dir.replace("\\", "\\\\")
        
        wrapper = f"""% MATLAB Bridge - Auto-generated execution script
% Timestamp: {datetime.now().isoformat()}

try
    % 设置输出目录
    output_dir = '{output_dir_escaped}';
    
    % 切换到输出目录（用于保存图片）
    cd(output_dir);
    
    % 用户代码开始
    % ================================
{self._indent_code(user_code)}
    % ================================
    % 用户代码结束
    
    % 保存结果信息
    results = struct();
    results.success = true;
    results.message = 'Execution completed successfully';
    results.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    
    % 尝试获取变量列表
    vars = whos;
    var_list = {{}};
    for i = 1:length(vars)
        var_list{{i}} = vars(i).name;
    end
    results.variables = var_list;
    
    catch ME
    % 错误处理
    results = struct();
    results.success = false;
    results.message = ME.message;
    results.identifier = ME.identifier;
    results.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
end

% 保存结果到JSON
results_file = fullfile(output_dir, '{temp_name}_results.json');
fid = fopen(results_file, 'w');
if fid ~= -1
    fprintf(fid, '{{"success": %s, "message": "%s", "timestamp": "%s"}}', 
        iif(results.success, 'true', 'false'), 
        strrep(results.message, '"', '\\"'),
        results.timestamp);
    fclose(fid);
end

% 保存工作区（如果需要）
if {str(save_workspace).lower()}
    mat_file = fullfile(output_dir, '{temp_name}_workspace.mat');
    save(mat_file);
end

% 辅助函数
function out = iif(cond, a, b)
    if cond, out = a; else, out = b; end
end
"""
        return wrapper
    
    def _indent_code(self, code: str, indent: str = '    ') -> str:
        """给代码添加缩进"""
        lines = code.strip().split('\n')
        return '\n'.join([indent + line for line in lines])
    
    def run_script(self, script_path: str, 
                   args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        运行已有的.m脚本
        
        Args:
            script_path: .m文件路径
            args: 传递给脚本的参数字典
        
        Returns:
            执行结果
        """
        if not os.path.exists(script_path):
            return {
                'success': False,
                'error': f'Script not found: {script_path}'
            }
        
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(script_path))
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        
        # 构建命令
        cd_cmd = f"cd('{script_dir}');"
        
        if args:
            # 设置参数
            arg_cmds = []
            for key, value in args.items():
                if isinstance(value, str):
                    arg_cmds.append(f"{key} = '{value}';")
                elif isinstance(value, (list, tuple)):
                    arr_str = ' '.join([str(x) for x in value])
                    arg_cmds.append(f"{key} = [{arr_str}];")
                else:
                    arg_cmds.append(f"{key} = {value};")
            cd_cmd += ' '.join(arg_cmds)
        
        cmd = f"{cd_cmd} {script_name}"
        
        full_cmd = [
            self.matlab_path,
            '-nodisplay',
            '-nosplash', 
            '-batch',
            cmd
        ]
        
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'script': script_path
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Execution timeout (5 minutes)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# 便捷函数
def matlab_exec(code: str, **kwargs) -> Dict[str, Any]:
    """便捷函数：直接执行MATLAB代码"""
    bridge = MATLABBridge()
    return bridge.execute(code, **kwargs)


def matlab_run(script_path: str, **kwargs) -> Dict[str, Any]:
    """便捷函数：运行MATLAB脚本"""
    bridge = MATLABBridge()
    return bridge.run_script(script_path, **kwargs)


if __name__ == '__main__':
    # 测试
    import argparse
    
    parser = argparse.ArgumentParser(description='MATLAB Bridge CLI')
    parser.add_argument('--code', '-c', help='要执行的MATLAB代码')
    parser.add_argument('--script', '-s', help='要运行的.m脚本路径')
    parser.add_argument('--test', action='store_true', help='运行测试')
    
    args = parser.parse_args()
    
    if args.test:
        print("测试MATLAB连接...")
        try:
            bridge = MATLABBridge()
            result = bridge.execute("disp('MATLAB Bridge Test OK');")
            print(f"结果: {result}")
        except Exception as e:
            print(f"错误: {e}")
    
    elif args.code:
        result = matlab_exec(args.code)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.script:
        result = matlab_run(args.script)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()

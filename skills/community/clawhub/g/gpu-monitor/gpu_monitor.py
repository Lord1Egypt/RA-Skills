#!/usr/bin/env python3
"""
GPU Monitor - Cross-platform real-time GPU monitoring skill

This is a generic, configuration-aware GPU monitoring tool that:
- Works on Windows/Linux/macOS (with NVIDIA GPUs)
- Auto-detects GPU information via nvidia-smi
- Optionally parses Ollama logs for model layer distribution
- Configurable update interval and log paths
- Clean terminal output with usage percentages

Usage:
    python gpu_monitor.py [OPTIONS]
    
Options:
    --interval=2        Update frequency in seconds (default: 2)
    --ollama-log=/path Auto-parse Ollama layer info from this log
    --quiet             Disable banner messages
"""

import subprocess
import re
import sys
import time
from datetime import datetime
from pathlib import Path
import json


def load_config():
    """Load configuration from ~/.openclaw/gpu_monitor_config.json if exists"""
    config_path = Path.home() / ".openclaw" / "gpu_monitor_config.json"
    
    default_config = {
        "update_interval_seconds": 2,
        "ollama_log_path": None,
        "quiet_mode": False
    }
    
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        pass
    
    return default_config


def get_gpu_info():
    """获取当前 GPU 显存信息"""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=index,name,memory.total,memory.used,memory.free,persistence_mode,volatile_state,utilization.gpu,temperature.gpu', 
             '--format=csv,noheader'],
            capture_output=True, text=True, timeout=5
        )
        
        if not result.stdout.strip():
            return None
            
        info = []
        for line in result.stdout.strip().split('\n'):
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 8:
                index = int(parts[0])
                name = parts[1]
                
                # 提取数字（处理 GiB, MiB）
                total_match = re.search(r'total="(\d+\.\d+) \w*"', parts[2])
                used_match = re.search(r'used="(\d+\.\d+) \w*"', parts[3])
                free_match = re.search(r'free="(\d+\.\d+) \w*"', parts[4])
                util_match = re.search(r'utilization\.gpu=(\d+)', parts[7])
                temp_match = re.search(r'temperature\.gpu=(\d+)', parts[8])
                
                total_str = total_match.group(1) if total_match else "N/A"
                used_str = used_match.group(1) if used_match else "N/A"
                free_str = free_match.group(1) if free_match else "N/A"
                util_str = util_match.group(1) if util_match else "0"
                temp_str = temp_match.group(1) if temp_match else "N/A"
                
                # 转换单位
                try:
                    if 'GiB' in total_str:
                        total_gb = float(total_str)
                    else:
                        total_gb = float(total_str) / 1024
                    
                    if 'GiB' in used_str:
                        used_gb = float(used_str)
                    else:
                        used_gb = float(used_str) / 1024
                    
                    usage_rate = (used_gb / total_gb * 100) if total_gb and float(total_str) > 0 else 0
                    
                except (ValueError, TypeError):
                    continue
                
                info.append({
                    'index': index,
                    'name': name,
                    'total_gb': round(total_gb, 1),
                    'used_gb': round(used_gb, 1),
                    'free_gb': round(float(free_str), 1) if free_str != 'N/A' else 0,
                    'usage_rate': round(usage_rate, 1),
                    'utilization_gpu': util_str,
                    'temperature_gpu': temp_str
                })
        
        return info if info else None
    
    except Exception as e:
        print(f"[ERROR] GPU 信息获取失败：{e}", file=sys.stderr)
        return None


def parse_ollama_log(ollama_log_path=None):
    '''从 Ollama 日志抓取层数信息（可选功能）'''
    if not ollama_log_path:
        return {'gpu_layers': None, 'total_layers': None, 'last_time': None}
    
    try:
        with open(ollama_log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-50:]
        
        gpu_layers = None
        total_layers = None
        last_time = None
        
        for line in lines:
            # 匹配旧版格式 "GPULayers:32[Layers:32(0..31)]"
            gpu_match = re.search(r'GPULayers:(\d+).*?Layers:(\d+)\(\s*(\d+\.\.\d+)?\s*\]', line)
            if gpu_match:
                gpu_layers = int(gpu_match.group(1))
                total_layers = int(gpu_match.group(2))
            
            # 匹配 "offloaded X/Y layers to GPU"
            offload_match = re.search(r'offloaded (\d+)/(\d+) layers', line)
            if offload_match:
                gpu_layers = int(offload_match.group(1))
                total_layers = int(offload_match.group(2))
            
            # 提取 timestamp
            time_match = re.search(r'time=(\S+)', line)
            if time_match:
                last_time = time_match.group(1)
        
        return {
            'gpu_layers': gpu_layers,
            'total_layers': total_layers,
            'last_time': last_time
        }
    except Exception as e:
        print(f"[WARN] 解析 Ollama 日志失败：{e}", file=sys.stderr)
        return {'gpu_layers': None, 'total_layers': None, 'last_time': None}


def format_output(gpu_info=None, log_data=None, update_count=1):
    """格式化输出信息"""
    if not gpu_info:
        return "└─ GPU Info: Unable to detect GPU\n"
    
    lines = []
    lines.append(f"┌─[Update #{update_count}] {datetime.now().strftime('%H:%M:%S')}\n")
    
    for gpu in gpu_info:
        name = gpu['name'] or 'N/A'
        
        # 显示显存信息
        total = gpu['total_gb']
        used = gpu['used_gb']
        free = gpu.get('free_gb', 0)
        usage_rate = gpu['usage_rate']
        
        if total > 0:
            mem_str = f"{used:.1f}/{total:.1f} GB"
        else:
            mem_str = f"{used:.1f} GB"
        
        lines.append(f"├─ GPU:         {name}\n")
        lines.append(f"├─ Memory Used: {mem_str} ({usage_rate:.1f}%)\n")
        
        # 可选的详细信息
        if gpu.get('utilization_gpu'):
            lines.append(f"├─ Utilization: {gpu['utilization_gpu']}%\n")
        if gpu.get('temperature_gpu'):
            lines.append(f"├─ Temperature: {gpu['temperature_gpu']}°C\n")
        
        # Ollama 层数信息（如果有）
        if log_data and (log_data['gpu_layers'] or log_data['total_layers']):
            gpu_l = log_data['gpu_layers']
            total_l = log_data['total_layers']
            time_str = log_data['last_time'] or 'N/A'
            
            lines.append(f"├─ Log Time:    {time_str}\n")
            lines.append(f"├─ GPU Layers:  {gpu_l} / {total_l}\n")
            
            if gpu_l and total_l:
                cpu_l = total_l - gpu_l
                lines.append(f"├─ CPU Layers:  {cpu_l} ({cpu_l / total_l * 100:.1f}%)\n")
        elif not log_data['gpu_layers']:
            lines.append("├─ GPU Layers:  [实时模式]\n")
        
        # 其他 GPU 信息（如果有）
        if len(gpu_info) > 1:
            for other in gpu_info[1:]:
                o_name = other['name'] or 'N/A'
                lines.append(f"├─ {o_name}: {other['used_gb']}/{other['total_gb']} GB ({other['usage_rate']:.1f}%)\n")
    
    return '\n'.join(lines)


def main():
    """主监控循环"""
    config = load_config()
    
    # 解析命令行参数（简单处理）
    interval = config.get('update_interval_seconds', 2)
    ollama_log_path = config.get('ollama_log_path')
    quiet_mode = config.get('quiet_mode', False)
    
    # 简单的 CLI 参数解析
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--interval='):
                try:
                    interval = int(arg.split('=')[1])
                except (ValueError, IndexError):
                    pass
            elif arg.startswith('--ollama-log='):
                ollama_log_path = arg.split('=', 1)[1]
            elif arg == '--quiet':
                quiet_mode = True
    
    if not quiet_mode:
        print("=" * 70)
        print("🚀 GPU Memory Monitor Started!")
        print("=" * 70)
        print(f"Update interval: {interval} seconds")
        if ollama_log_path:
            print(f"Ollama log path: {ollama_log_path}")
        print("=" * 70)
    
    update_count = 0
    
    while True:
        try:
            # 获取 GPU 信息
            gpu_info = get_gpu_info()
            
            # 解析 Ollama 日志（可选）
            log_data = parse_ollama_log(ollama_log_path) if ollama_log_path else {'gpu_layers': None, 'total_layers': None, 'last_time': None}
            
            update_count += 1
            
            if quiet_mode or (gpu_info and log_data):
                # 静默模式或有数据时，输出简化的信息
                output = format_output(gpu_info, log_data, update_count)
                print(output, end='')
            else:
                # 无 GPU 信息时的降级输出
                timestamp = datetime.now().strftime("%H:%M:%S")
                if gpu_info:
                    info_str = f"GPU: {gpu_info[0]['name']} | Memory: {gpu_info[0]['used_gb']}/{gpu_info[0]['total_gb']} GB ({gpu_info[0]['usage_rate']:.1f}%) | {timestamp}"
                    print(f"\n┌─[Update #{update_count}] {timestamp}")
                    print(f"├─ GPU:         {info_str}")
                else:
                    print(f"\n┌─[Update #{update_count}] {timestamp}")
                    print("└─ GPU Info: Unable to detect GPU (no NVIDIA GPU or nvidia-smi not found)")
            
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n┌─[Update #{update_count}] {timestamp}")
            print(f"└─ ERROR: {e}", file=sys.stderr)
        
        time.sleep(interval)


if __name__ == "__main__":
    main()

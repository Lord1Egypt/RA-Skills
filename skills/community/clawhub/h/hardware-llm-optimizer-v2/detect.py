#!/usr/bin/env python3
"""
Hardware LLM Optimizer - PC Hardware Detection & LLM Recommendation Tool
自动检测电脑硬件配置 → 判断能跑哪些大模型 → 给出推荐 + 量化方案 + 瓶颈诊断
"""

import platform
import os
import sys
import subprocess

try:
    import psutil
except ImportError:
    print("需要安装 psutil: pip install psutil")
    sys.exit(1)


def get_cuda_info():
    """检测 CUDA 版本"""
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=driver_version,compute_cap", "--format=csv,noheader"],
            encoding="utf-8"
        ).strip()
        return result
    except:
        return None


def get_ollama_compatible():
    """检测 Ollama 兼容性"""
    info = []
    system = platform.system().lower()
    
    if system == "linux":
        info.append("✅ Ollama 支持 Linux（原生）")
    elif system == "darwin":
        info.append("✅ Ollama 支持 macOS（原生，GPU加速）")
    elif system == "windows":
        info.append("✅ Ollama 支持 Windows（WSL2 或原生）")
    
    # 检测 WSL2
    try:
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                info.append("⚠️ 检测到 WSL2，GPU 直通需安装 nvidia.cuda-wmi")
                info.append("💡 建议：在 Windows 原生运行 Ollama 体验更好")
    except:
        pass
    
    return info


def detect_hardware():
    """检测电脑硬件配置"""
    result = []
    
    # =================== 1. 系统信息 ===================
    sys_info = {
        "system": platform.system(),
        "release": platform.release(),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq().max if psutil.cpu_freq() else 0,
        "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available": round(psutil.virtual_memory().available / (1024**3), 2),
    }
    
    result.append("=" * 50)
    result.append("🤖 大模型硬件检测工具")
    result.append("=" * 50)
    result.append(f"🖥 系统：{sys_info['system']} {sys_info['release']}")
    result.append(f"🧠 CPU 核心数：{sys_info['cpu_count']}")
    if sys_info['cpu_freq']:
        result.append(f"💡 CPU 频率：{sys_info['cpu_freq']:.0f} MHz")
    result.append(f"💾 总内存：{sys_info['ram_total']} GB")
    result.append(f"🆓 可用内存：{sys_info['ram_available']} GB")
    
    # =================== 2. 检测显卡 & 显存 ===================
    vram_gb = 0
    gpu_name = "未检测到独立显卡"
    cuda_version = None
    
    try:
        nvidia_output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
            encoding="utf-8"
        ).strip()
        lines = nvidia_output.split("\n")
        if lines:
            parts = [p.strip() for p in lines[0].split(",")]
            if len(parts) >= 3:
                gpu_name = parts[0]
                vram_mb = int(parts[1])
                driver = parts[2]
                vram_gb = round(vram_mb / 1024, 2)
                result.append(f"🎮 显卡：{gpu_name}")
                result.append(f"🎮 显存：{vram_gb} GB")
                result.append(f"🔧 NVIDIA 驱动：{driver}")
                
                # CUDA 检测
                cuda_info = get_cuda_info()
                if cuda_info:
                    result.append(f"🚀 CUDA：已检测到")
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        result.append("🎮 独立显卡：未检测到（使用 CPU 模式）")
        result.append("💡 提示：NVIDIA 显卡需安装 nvidia-smi")
    
    result.append("-" * 50)
    
    # =================== 3. 能跑多大模型 ===================
    result.append("🚀 你的电脑可运行的大模型：")
    
    models = []
    
    if vram_gb >= 2 or sys_info['ram_total'] >= 8:
        models.append("✅ 3B 模型 (Gemma 3B / Phi-3 Mini)")
    
    if vram_gb >= 4 or sys_info['ram_total'] >= 12:
        models.append("✅ 7B / 8B 模型 (Llama3 8B / Qwen 7B / Mistral 7B)")
    
    if vram_gb >= 6 or sys_info['ram_total'] >= 16:
        models.append("✅ 10B 级别模型 (Qwen 14B / Yi 9B)")
    
    if vram_gb >= 8 or sys_info['ram_total'] >= 24:
        models.append("✅ 13B 模型 (Llama2 13B / Qwen 14B / Mistral 13B)")
    
    if vram_gb >= 12 or sys_info['ram_total'] >= 32:
        models.append("✅ 34B 模型 (Llama2 34B / Yi 34B)")
    
    if vram_gb >= 16 or sys_info['ram_total'] >= 48:
        models.append("✅ 70B 模型 (4bit 量化)")
    
    if vram_gb >= 24:
        models.append("✅ 70B 模型 (8bit 量化)")
    
    if vram_gb >= 48:
        models.append("✅ 70B 模型 (FP16 原生)")
    
    if not models:
        models.append("❌ 仅能跑超小模型或依赖网页版 AI")
    
    for m in models:
        result.append(m)
    
    result.append("-" * 50)
    
    # =================== 4. 量化方案建议 ===================
    result.append("⚙️ 推荐量化精度：")
    
    if vram_gb >= 24:
        result.append("✅ FP16（高质量，推荐)")
        result.append("✅ 8bit（平衡方案）")
    elif vram_gb >= 12:
        result.append("✅ 8bit（推荐）")
        result.append("✅ 4bit（可选）")
    elif vram_gb >= 6:
        result.append("✅ 4bit（最流畅，推荐）")
        result.append("✅ 8bit（需要内存交换）")
    elif vram_gb >= 4:
        result.append("✅ 4bit（CPU + 内存交换）")
    elif vram_gb >= 2:
        result.append("✅ 2bit / 极端量化（仅简单对话）")
    else:
        result.append("❌ 建议使用网页版 AI 或 API")
        result.append("💡 考虑：ChatGPT / Claude / 文心一言")
    
    # =================== 5. 具体模型推荐 ===================
    result.append("-" * 50)
    result.append("📋 具体推荐模型：")
    
    if vram_gb >= 4 or sys_info['ram_total'] >= 12:
        result.append("")
        result.append("🌟 7B-8B 推荐（性价比最高）：")
        result.append("  • Llama3 8B - 最流行开源")
        result.append("  • Qwen 7B - 中文优化强")
        result.append("  • Mistral 7B - 欧洲最强")
        result.append("  • Phi-3 Mini - 微软小钢炮")
        result.append("  • Ollama 一键运行：ollama run llama3")
    
    if vram_gb >= 8 or sys_info['ram_total'] >= 24:
        result.append("")
        result.append("🌟 13B-14B 推荐（更强推理）：")
        result.append("  • Llama2 13B - 经典稳定")
        result.append("  • Qwen 14B - 中文旗舰")
        result.append("  • Mistral 13B - 效率高")
    
    if vram_gb >= 16:
        result.append("")
        result.append("🌟 34B+ 推荐（大显存专用）：")
        result.append("  • Llama2 34B - 性能接近 GPT-3.5")
        result.append("  • Yi 34B - 中文超强")
        result.append("  • Qwen 72B - 国产最强")
    
    # =================== 6. 部署工具 ===================
    result.append("-" * 50)
    result.append("🛠 推荐部署工具：")
    
    result.append("✅ Ollama（最简单，一键运行）")
    result.append("  安装：ollama.com")
    
    if vram_gb >= 4:
        result.append("✅ Llama.cpp（GGUF格式，省显存）")
        result.append("✅ Chatbox（图形界面，新手友好）")
    
    if vram_gb >= 6:
        result.append("✅ Text Generation Web UI（功能最全）")
    
    if vram_gb >= 8:
        result.append("✅ vLLM（高速推理，生产级）")
    
    # Ollama 兼容性
    ollama_info = get_ollama_compatible()
    if ollama_info:
        result.append("")
        for info in ollama_info:
            result.append(info)
    
    # =================== 7. 瓶颈诊断 ===================
    result.append("-" * 50)
    result.append("🔍 系统瓶颈分析：")
    
    bottlenecks = []
    
    if sys_info['ram_total'] < 16:
        bottlenecks.append("⚠️ 瓶颈：内存不足（<16GB），优先加内存")
    elif vram_gb < 6:
        bottlenecks.append("⚠️ 瓶颈：显卡显存不足（<6GB），建议用4bit量化")
    elif sys_info['cpu_count'] < 8:
        bottlenecks.append("⚠️ 瓶颈：CPU较弱（<8核），推理较慢")
    else:
        bottlenecks.append("✅ 配置均衡，可流畅运行本地大模型")
    
    for b in bottlenecks:
        result.append(b)
    
    # =================== 8. 优化建议 ===================
    result.append("-" * 50)
    result.append("💡 优化建议：")
    
    if vram_gb < 4:
        result.append("• 开启 OS 虚拟内存（增加可用 RAM）")
        result.append("• 使用 GGUF 格式（Llama.cpp 专用）")
        result.append("• 考虑 2bit 量化（Q4_K_M）")
    
    if sys_info['ram_total'] < 16:
        result.append("• 16GB 是跑 7B 模型的甜蜜点")
        result.append("• 建议升级内存到 32GB")
    
    if vram_gb < 8:
        result.append("• 4bit 量化是最佳平衡点")
        result.append("• 避免 FP16，需要太多显存")
    
    # =================== 9. 最低配置对照表 ===================
    result.append("")
    result.append("📊 最低配置对照表：")
    result.append("-" * 30)
    result.append("  模型     | 最低显存 | 推荐显存 | 量化")
    result.append("  ---------|---------|---------|------")
    result.append("  3B       | 2GB     | 4GB     | Q4")
    result.append("  7B       | 6GB     | 8GB     | Q4/Q8")
    result.append("  13B      | 10GB    | 16GB    | Q4/Q8")
    result.append("  34B      | 20GB    | 32GB    | Q4")
    result.append("  70B      | 40GB    | 80GB    | Q4")
    
    result.append("")
    result.append("=" * 50)
    
    return "\n".join(result)


def main():
    """主函数"""
    try:
        output = detect_hardware()
        print(output)
    except Exception as e:
        print(f"⚠️ 检测出错：{e}")
        print("请确保已安装 psutil: pip install psutil")
        sys.exit(1)


if __name__ == "__main__":
    main()

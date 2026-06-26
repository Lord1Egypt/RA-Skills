#!/usr/bin/env python3
"""
Jarvis-Video-STT - 批量视频语音转文字
支持多进程并行、进度条、汇总报告

依赖: faster-whisper, tqdm, ffmpeg
安装: pip install faster-whisper tqdm
"""

import argparse
import glob
import json
import multiprocessing as mp
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# 尝试导入faster_whisper
try:
    from faster_whisper import WhisperModel
    HAS_FASTER_WHISPER = True
except ImportError:
    HAS_FASTER_WHISPER = False


def load_model(model_size, device, compute_type):
    """加载模型（子进程中使用）"""
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def extract_audio(video_path, temp_dir):
    """提取音频到临时文件"""
    audio_path = os.path.join(temp_dir, f"{Path(video_path).stem}.wav")
    cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" 2>/dev/null'
    os.system(cmd)
    return audio_path if os.path.exists(audio_path) else None


def format_time(seconds):
    """秒数转SRT时间格式"""
    td = datetime.utcfromtimestamp(seconds)
    return td.strftime("%H:%M:%S,%f")[:-3]


def transcribe_single(args):
    """单个视频转录（子进程调用）"""
    video_path, output_dir, model_size, device, compute_type, language, model = args
    
    video_name = Path(video_path).stem
    temp_dir = os.path.join(output_dir, "_temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 提取音频
        audio_path = extract_audio(video_path, temp_dir)
        if not audio_path or not os.path.exists(audio_path):
            raise Exception("音频提取失败")
        
        # 转录
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )
        
        # 保存SRT
        srt_path = os.path.join(output_dir, f"{video_name}.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                start = format_time(seg.start)
                end = format_time(seg.end)
                f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")
        
        # 生成全文
        segments, _ = model.transcribe(audio_path, language=language, beam_size=5)
        full_text = " ".join([s.text.strip() for s in segments])
        
        txt_path = os.path.join(output_dir, f"{video_name}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        # 清理临时音频
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return {
            "status": "success",
            "video": video_name,
            "video_path": video_path,
            "language": info.language,
            "duration": round(info.duration, 1),
            "srt": srt_path,
            "txt": txt_path
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "video": video_name,
            "video_path": video_path,
            "error": str(e)
        }


def process_batch(video_files, output_dir, model_size, device, compute_type, language, workers):
    """批量处理"""
    
    # 加载模型
    print(f"\n🔄 加载模型: {model_size} ({device})...")
    model = load_model(model_size, device, compute_type)
    
    # 准备任务参数
    tasks = [
        (vf, output_dir, model_size, device, compute_type, language, model)
        for vf in video_files
    ]
    
    # 进度条跟踪
    results = []
    with tqdm(total=len(video_files), desc="整体进度", unit="视频") as pbar:
        if workers == 1:
            # 单进程模式
            for task in tasks:
                result = transcribe_single(task)
                results.append(result)
                pbar.update(1)
        else:
            # 多进程模式
            with mp.Pool(processes=workers) as pool:
                for result in pool.imap_unordered(transcribe_single, tasks):
                    results.append(result)
                    pbar.update(1)
    
    # 清理临时目录
    temp_dir = os.path.join(output_dir, "_temp")
    if os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return results


def generate_report(results, output_dir, total_time):
    """生成汇总报告"""
    
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    
    # JSON报告
    report = {
        "summary": {
            "total": len(results),
            "success": len(success),
            "failed": len(failed),
            "total_time_seconds": round(total_time, 1),
            "avg_time_per_video": round(total_time / len(results), 1) if results else 0
        },
        "results": results
    }
    
    json_path = os.path.join(output_dir, "report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Markdown报告
    md_content = f"""# Jarvis-Video-STT 处理报告

## 📊 汇总统计

| 指标 | 值 |
|------|-----|
| 总视频数 | {len(results)} |
| 成功 | ✅ {len(success)} |
| 失败 | ❌ {len(failed)} |
| 总耗时 | {total_time:.1f} 秒 |
| 平均耗时 | {total_time/len(results):.1f} 秒/视频 |

"""
    
    if success:
        md_content += "## ✅ 成功列表\n\n"
        md_content += "| 视频 | 语言 | 时长 | SRT | TXT |\n"
        md_content += "|------|------|------|-----|-----|\n"
        for r in success:
            md_content += f"| {r['video']} | {r['language']} | {r['duration']}s | `{r['srt']}` | `{r['txt']}` |\n"
        md_content += "\n"
    
    if failed:
        md_content += "## ❌ 失败列表\n\n"
        md_content += "| 视频 | 错误 |\n"
        md_content += "|------|------|\n"
        for r in failed:
            md_content += f"| {r['video']} | {r['error']} |\n"
    
    md_path = os.path.join(output_dir, "report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    return json_path, md_path


def detect_device():
    """检测可用设备"""
    import platform
    system = platform.system()
    
    if system == "Darwin":
        return "cuda", "float16"  # Mac用cuda（metal实际上会fallback）
    elif system == "Linux":
        # 检查NVIDIA
        if os.path.exists("/dev/nvidia0"):
            return "cuda", "float16"
        return "cpu", "int8"
    else:
        return "cpu", "int8"


def main():
    parser = argparse.ArgumentParser(
        description="Jarvis-Video-STT - 批量视频语音转文字",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python batch_whisper.py -i "videos/*.mp4" -o results
  python batch_whisper.py -i "videos/" -o results -m small -w 2
  python batch_whisper.py -i "video.mp4" -o output -m medium -l zh
        """
    )
    
    parser.add_argument("--input", "-i", required=True, help="视频路径/文件夹/通配符")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    parser.add_argument("--model", "-m", choices=["small", "medium"], default="medium", 
                        help="模型大小 (small=快速, medium=高精度)")
    parser.add_argument("--language", "-l", default=None, help="语言 (None=自动检测)")
    parser.add_argument("--workers", "-w", type=int, default=3, 
                        help="并行进程数 (默认3)")
    parser.add_argument("--cpu", action="store_true", help="强制使用CPU")
    
    args = parser.parse_args()
    
    # 检查依赖
    if not HAS_FASTER_WHISPER:
        print("❌ 错误: 请先安装 faster-whisper")
        print("   pip install faster-whisper")
        sys.exit(1)
    
    # 查找视频文件
    input_path = Path(args.input)
    if input_path.is_dir():
        videos = list(input_path.glob("*.mp4")) + list(input_path.glob("*.mkv")) + \
                 list(input_path.glob("*.avi")) + list(input_path.glob("*.mov"))
    elif "*" in str(args.input):
        videos = glob.glob(str(args.input))
    else:
        videos = [str(args.input)]
    
    videos = [v for v in videos if os.path.exists(v)]
    
    if not videos:
        print(f"❌ 未找到视频: {args.input}")
        sys.exit(1)
    
    # 设备配置
    if args.cpu:
        device, compute_type = "cpu", "int8"
    else:
        device, compute_type = detect_device()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 执行
    print(f"\n📁 找到 {len(videos)} 个视频")
    print(f"⚙️  模型: {args.model} | 设备: {device} | 并行: {args.workers}\n")
    
    start_time = time.time()
    results = process_batch(
        videos, args.output, args.model, device, compute_type, args.language, args.workers
    )
    total_time = time.time() - start_time
    
    # 生成报告
    json_path, md_path = generate_report(results, args.output, total_time)
    
    # 打印汇总
    success = len([r for r in results if r["status"] == "success"])
    failed = len([r for r in results if r["status"] == "failed"])
    
    print(f"""
╔══════════════════════════════════════════╗
║         ✅ 处理完成                        ║
╠══════════════════════════════════════════╣
║  总视频: {len(results)}                                ║
║  成功:   {success}                                ║
║  失败:   {failed}                                ║
║  耗时:   {total_time:.1f} 秒                        ║
╠══════════════════════════════════════════╣
║  📄 报告: {md_path}
║  📋 JSON: {json_path}
╚══════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()

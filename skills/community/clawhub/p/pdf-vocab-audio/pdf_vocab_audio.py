#!/usr/bin/env python3
"""
PDF 词汇音频生成器
从 PDF 提取每行的英文部分，生成朗读音频

安全性设计：
- 仅调用已验证的系统工具（edge-tts, ffmpeg）
- 使用shutil.which()验证工具存在
- 所有路径使用临时目录，不暴露敏感位置
- PDF路径验证：必须是存在的.pdf文件
"""

import re
import subprocess
import tempfile
import os
import sys
import shutil

# 验证依赖工具
def check_dependencies():
    """检查必需的工具是否可用"""
    missing = []
    for tool in ['edge-tts', 'ffmpeg']:
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        raise RuntimeError(f"缺少必需工具: {', '.join(missing)}")

VOICE = "en-GB-RyanNeural"
RATE = "-20%"
SILENCE_DURATION = 1
OUTPUT_DIR = "/tmp"


def extract_words_from_pdf(pdf_path: str) -> list:
    """从 PDF 提取每行的英文部分"""
    try:
        import fitz  # pymupdf
    except ImportError:
        raise RuntimeError("缺少 pymupdf 库，请运行: pip install pymupdf")
    
    doc = fitz.open(pdf_path)
    words = []
    
    for page in doc:
        text = page.get_text()
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 匹配整行英文内容（从行首到中文字符前）
            match = re.match(r'^([a-zA-Z].*)$', line)
            if match:
                english = match.group(1).strip()
                # 过滤空行和太短的
                if english and len(english) >= 2:
                    words.append(english)
    
    return words


def generate_word_audio(word: str, output_path: str) -> bool:
    """生成单词音频"""
    edge_tts_path = shutil.which("edge-tts")
    if not edge_tts_path:
        raise RuntimeError("edge-tts 未安装")

    cmd = [
        edge_tts_path,
        "--voice", VOICE,
        f"--rate={RATE}",
        "--text", word,
        "--write-media", output_path
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.returncode == 0


def generate_silence(output_path: str, duration: int = 1) -> bool:
    """生成静音音频"""
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg 未安装")

    cmd = [
        ffmpeg_path, "-y",
        "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(duration),
        "-q:a", "9",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=10)
    return result.returncode == 0


def concat_audio(input_files: list, output_path: str, tmpdir: str) -> bool:
    """合并多个音频文件"""
    if not input_files:
        return False

    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg 未安装")

    # 使用临时目录内的文件
    list_file = os.path.join(tmpdir, "concat_list.txt")
    try:
        with open(list_file, "w") as f:
            for fp in input_files:
                if os.path.exists(fp) and os.path.getsize(fp) > 0:
                    f.write(f"file '{fp}'\n")
        
        cmd = [
            ffmpeg_path, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    finally:
        if os.path.exists(list_file):
            os.remove(list_file)


def main():
    check_dependencies()
    
    if len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
        pdf_path = sys.argv[1]
    else:
        # 使用最新的 PDF
        inbound_dir = "/root/.openclaw/media/inbound"
        pdfs = [f for f in os.listdir(inbound_dir) if f.endswith('.pdf')]
        if not pdfs:
            print("未找到 PDF 文件")
            return
        pdfs.sort(key=lambda x: os.path.getmtime(os.path.join(inbound_dir, x)), reverse=True)
        pdf_path = os.path.join(inbound_dir, pdfs[0])
    
    # 验证PDF文件
    if not os.path.exists(pdf_path):
        print(f"PDF文件不存在: {pdf_path}")
        return
    
    if not pdf_path.lower().endswith('.pdf'):
        print("错误：文件必须是PDF格式")
        return
    
    print(f"输入: {pdf_path}")
    
    # 提取词汇
    print("提取词汇...")
    words = extract_words_from_pdf(pdf_path)
    print(f"找到 {len(words)} 个: {words}")
    
    if not words:
        print("未找到词汇")
        return
    
    # 生成音频
    print(f"\n生成音频...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_segments = []
        silence_file = f"{tmpdir}/silence.mp3"
        generate_silence(silence_file, SILENCE_DURATION)
        
        for i, word in enumerate(words):
            word_file = f"{tmpdir}/word_{i}.mp3"
            
            if generate_word_audio(word, word_file):
                # 第一遍
                audio_segments.append(word_file)
                audio_segments.append(silence_file)
                # 第二遍
                audio_segments.append(word_file)
                audio_segments.append(silence_file)
        
        if audio_segments:
            filename = os.path.basename(pdf_path)
            output_name = filename.replace('.pdf', ' 词汇朗读音频.mp3')
            output_path = os.path.join(OUTPUT_DIR, output_name)
            
            # 传递tmpdir以确保concat_list.txt在临时目录内
            if concat_audio(audio_segments, output_path, tmpdir):
                size = os.path.getsize(output_path)
                print(f"\n✅ 完成: {output_path}")
                print(f"大小: {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()

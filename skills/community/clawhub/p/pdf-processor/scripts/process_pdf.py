#!/usr/bin/env python3
"""
PDF处理脚本 v2.0（带进度显示和断点续传）
功能：提取文字、判断语言、翻译、生成概述、生成索引
使用本地Ollama模型，不消耗线上API

v2.0 改进：
- 进度显示：实时显示翻译进度
- 断点续传：中断后可从断点继续
"""

import json
import pdfplumber
from pathlib import Path
import requests
import re
import shutil
import subprocess
import time
from datetime import datetime

def check_ollama_model():
    """检查Ollama服务是否运行，模型是否可用"""
    model_name = "qwen2.5:7b"

    print(f"\n🔍 检查Ollama模型: {model_name}")

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json()

        model_exists = False
        for model in models.get('models', []):
            if model_name in model.get('name', ''):
                model_exists = True
                break

        if model_exists:
            print(f"✅ Ollama服务运行正常，模型 {model_name} 已加载")
            return True
        else:
            print(f"❌ 模型 {model_name} 未找到")
            print(f"📋 可用模型: {[m['name'] for m in models.get('models', [])]}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Ollama服务未启动")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def start_ollama():
    """启动Ollama服务"""
    print("\n🚀 正在启动Ollama服务...")

    try:
        subprocess.Popen(['ollama', 'serve'],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
        time.sleep(5)

        if check_ollama_model():
            print("✅ Ollama服务启动成功")
            return True
        else:
            print("❌ Ollama服务启动失败")
            return False

    except FileNotFoundError:
        print("❌ 未找到ollama命令，请先安装Ollama")
        return False
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def split_text(text, max_length=4000):
    """按字符数分段，尽量在段落边界断开"""
    segments = []
    current_pos = 0

    while current_pos < len(text):
        end_pos = min(current_pos + max_length, len(text))

        if end_pos < len(text):
            for sep in ['\n\n\n', '\n\n', '。', '！', '？', '.']:
                last_sep = text.rfind(sep, current_pos, end_pos)
                if last_sep > current_pos:
                    end_pos = last_sep + len(sep)
                    break

        segment = text[current_pos:end_pos].strip()
        if segment:
            segments.append(segment)

        current_pos = end_pos

    return segments

# ==================== v2.0 新增：进度文件管理 ====================

def get_progress_file(pdf_path, base_dir):
    """获取进度文件路径"""
    pdf_name = Path(pdf_path).stem
    return base_dir / "处理中" / f"{pdf_name}_progress.json"

def load_progress(progress_file):
    """加载翻译进度"""
    if not progress_file.exists():
        return None

    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 进度文件损坏，忽略: {e}")
        return None

def save_progress(progress_file, segment_num, translated_text,
                 total_segments, completed_segments, pending_segments):
    """保存翻译进度"""
    progress = {
        "source_file": Path(progress_file).stem.replace("_progress", ".pdf"),
        "total_segments": total_segments,
        "completed_segments": completed_segments,
        "pending_segments": pending_segments,
        "translated_text": {},
        "last_update": datetime.now().isoformat()
    }

    # 读取现有进度
    if progress_file.exists():
        existing = load_progress(progress_file)
        if existing:
            progress["translated_text"] = existing.get("translated_text", {})

    # 保存当前段翻译
    progress["translated_text"][str(segment_num)] = translated_text

    # 写入文件
    try:
        progress_file.write_text(
            json.dumps(progress, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
    except Exception as e:
        print(f"⚠️ 保存进度失败: {e}")

def clear_progress(progress_file):
    """清除进度文件"""
    if progress_file.exists():
        try:
            progress_file.unlink()
            print("🗑️ 已清除进度文件")
        except Exception as e:
            print(f"⚠️ 清除进度文件失败: {e}")

# ==================== v2.0 新增：带进度的翻译函数 ====================

def translate_segment_with_progress(segment, segment_num, total_segments, progress_file=None):
    """翻译一段文字，带进度显示和断点续传支持"""
    url = "http://localhost:11434/api/generate"

    # 检查是否已有翻译结果（断点续传）
    if progress_file:
        progress = load_progress(progress_file)
        if progress and str(segment_num) in progress.get("translated_text", {}):
            print(f"   ⏭️  第 {segment_num}/{total_segments} 段已翻译，跳过")
            return {
                "success": True,
                "response": progress["translated_text"][str(segment_num)],
                "segment_num": segment_num,
                "segment_status": "completed",
                "skipped": True
            }

    # 显示翻译进度
    print(f"\n📖 翻译第 {segment_num}/{total_segments} 段 "
          f"({segment_num/total_segments*100:.1f}%) "
          f"| {len(segment)} 字符")

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qwen2.5:7b",
        "prompt": f"请将以下英文翻译为中文：\n{segment}",
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 3000
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=600)
        result = response.json()

        if result.get("done", False):
            if result.get("done_reason") == "stop":
                translated = result.get("response", "")

                # 保存进度（断点续传）
                if progress_file and translated:
                    try:
                        # 读取现有进度
                        progress = load_progress(progress_file) or {}
                        if "translated_text" not in progress:
                            progress["translated_text"] = {}

                        # 更新进度
                        progress["translated_text"][str(segment_num)] = translated
                        progress["last_update"] = datetime.now().isoformat()

                        progress_file.write_text(
                            json.dumps(progress, ensure_ascii=False, indent=2),
                            encoding='utf-8'
                        )
                    except Exception as e:
                        print(f"   ⚠️ 保存进度失败: {e}")

                print(f"   ✅ 第 {segment_num} 段翻译完成")
                return {
                    "success": True,
                    "response": translated,
                    "segment_num": segment_num,
                    "segment_status": "completed",
                    "skipped": False
                }
            else:
                return {
                    "success": False,
                    "error": f"completed_with_reason: {result.get('done_reason', 'unknown')}",
                    "segment_num": segment_num,
                    "segment_status": "completed_abnormal",
                    "skipped": False
                }
        else:
            return {
                "success": False,
                "error": "request_not_completed",
                "segment_num": segment_num,
                "segment_status": "incomplete",
                "skipped": False
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "timeout",
            "segment_num": segment_num,
            "segment_status": "timeout",
            "skipped": False
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "connection_error",
            "segment_num": segment_num,
            "segment_status": "connection_error",
            "skipped": False
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"exception: {str(e)}",
            "segment_num": segment_num,
            "segment_status": "exception",
            "skipped": False
        }

def extract_title(first_page_text):
    """从第一页文字中提取论文标题"""
    lines = first_page_text.split('\n')
    title_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d+$', line):
            continue
        if any(keyword in line.lower() for keyword in ['arxiv', 'vol.', 'no.', 'page']):
            continue
        if len(line) > 10:
            title_lines.append(line)
            break

    title = ' '.join(title_lines) if title_lines else "未找到标题"
    return title.strip()

def translate_title(title):
    """翻译论文标题为中文"""
    url = "http://localhost:11434/api/generate"

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qwen2.5:7b",
        "prompt": f"请将以下论文标题翻译为中文，保持学术风格：\n{title}\n\n只输出翻译后的中文标题，不要任何解释。",
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 200
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        result = response.json()

        if "response" in result:
            content = result["response"].strip()
            content = content.strip('"\'')
            return content
        else:
            return "标题翻译失败"
    except Exception as e:
        return f"标题翻译异常: {e}"

def generate_summary(text):
    """生成论文概述（纯中文，200字以内）"""
    url = "http://localhost:11434/api/generate"

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qwen2.5:7b",
        "prompt": f"你是一个专业的学术论文概述专家。请根据提供的论文内容，生成一个简洁的中文概述，严格控制在200字左右（不超过210字），必须是纯中文，不能有任何英文单词、数字或符号。概述必须包含：1. 研究背景 2. 主要方法 3. 核心贡献 4. 应用价值。重要：概述必须是完整的句子，不要在句子中间截断。直接输出概述，不要任何解释或推理过程。\n\n论文内容：\n{text[:5000]}",
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 600
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=600)
        result = response.json()

        if "response" in result:
            content = result["response"]

            # 清理内容
            content = re.sub(r'[a-zA-Z]+', '', content)
            content = re.sub(r'\d+', '', content)
            content = re.sub(r'\s+', '', content)

            return content
        else:
            return "概述生成失败"
    except Exception as e:
        return f"概述异常: {e}"

# ==================== v2.0 改进：带断点续传的翻译流程 ====================

def translate_with_resume(text, pdf_path, base_dir, model_name="qwen2.5:7b"):
    """带断点续传的翻译"""

    # 分段
    segments = split_text(text)
    total_segments = len(segments)

    # 获取进度文件
    progress_file = get_progress_file(pdf_path, base_dir)

    # 检查是否有未完成的翻译
    progress = load_progress(progress_file)

    if progress:
        print(f"\n🔄 检测到未完成的翻译")
        print(f"📊 总段数: {total_segments}")
        print(f"✅ 已完成: {len(progress.get('completed_segments', []))} 段")
        print(f"⏳ 待翻译: {len(progress.get('pending_segments', []))} 段")
        print(f"💾 上次更新: {progress.get('last_update', 'N/A')}")

    # 翻译
    translated_segments = []
    completed_segments = []
    pending_segments = list(range(1, total_segments + 1))

    for i, segment in enumerate(segments, 1):
        # 检查是否已翻译（断点续传）
        if progress and str(i) in progress.get("translated_text", {}):
            translated_segments.append(progress["translated_text"][str(i)])
            completed_segments.append(i)
            pending_segments.remove(i)
            continue

        # 翻译当前段
        result = translate_segment_with_progress(
            segment,
            i,
            total_segments,
            progress_file
        )

        if result.get("success", False):
            translated = result.get("response", "")
            translated_segments.append(translated)
            completed_segments.append(i)
            pending_segments.remove(i)

            # 保存进度
            save_progress(
                progress_file,
                i,
                translated,
                total_segments,
                completed_segments,
                pending_segments
            )
        else:
            print(f"⚠️ 第{i}段失败，保留英文原文")
            translated_segments.append(segment)
            completed_segments.append(i)
            pending_segments.remove(i)

            # 保存进度（即使失败也保存）
            save_progress(
                progress_file,
                i,
                segment,
                total_segments,
                completed_segments,
                pending_segments
            )

    # 清除进度文件
    clear_progress(progress_file)

    return '\n\n'.join(translated_segments)

def process_pdf(pdf_path, output_base_dir):
    """处理PDF文件（v2.0：带进度显示和断点续传）"""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

    output_base_dir = Path(output_base_dir)

    print("📄 PDF处理流程 v2.0")
    print("=" * 60)
    print("✨ 新功能: 进度显示 + 断点续传")
    print("=" * 60)

    # 0. 检查Ollama模型
    if not check_ollama_model():
        print("\n⚠️ 模型不可用，尝试启动Ollama...")
        if not start_ollama():
            print("\n❌ 无法启动Ollama，无法继续处理")
            print("💡 请手动启动Ollama: ollama serve")
            exit(1)

    # 1. 提取文字
    print("\n1️⃣ 提取PDF文字...")
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        first_page_text = ''
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                if i == 0:
                    first_page_text = page_text
                full_text += f"\n\n--- 第{i+1}页 ---\n\n{page_text}"

    print(f"✅ 提取完成，字符数: {len(full_text):,}")

    # 2. 判断语言
    print("\n2️⃣ 判断语言...")
    english_words = len(re.findall(r'[a-zA-Z]+', full_text))
    if english_words > 100:
        print("✅ 语言判断: 英文")
        is_english = True
    else:
        print("✅ 语言判断: 中文")
        is_english = False

    # 提取和翻译标题
    print("\n1️⃣➕ 提取论文标题...")
    title_en = extract_title(first_page_text)
    print(f"📝 英文标题: {title_en[:100]}...")

    title_cn = title_en
    if english_words > 100:
        print("⏳ 翻译标题为中文...")
        title_cn = translate_title(title_en)
        print(f"📝 中文标题: {title_cn}")

    # 保存提取的文字
    processing_dir = output_base_dir / '处理中'
    processing_dir.mkdir(parents=True, exist_ok=True)

    extracted_file = processing_dir / f"{pdf_path.stem}_提取.txt"
    with open(extracted_file, 'w', encoding='utf-8') as f:
        f.write(f"# PDF文字提取\n\n")
        f.write(f"**源文件**: {pdf_path.name}\n")
        f.write(f"**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**字符数**: {len(full_text):,}\n\n")
        f.write(f"## 📄 提取内容\n\n")
        f.write(full_text)

    print(f"💾 提取文字已保存: {extracted_file.name}")

    # 3. 分段翻译（v2.0：带进度显示和断点续传）
    if is_english:
        print("\n3️⃣ 分段翻译（v2.0：进度显示 + 断点续传）...")

        # 分段
        segments = split_text(full_text, max_length=2000)
        print(f"📊 分段结果: {len(segments)}段，每段最多2000字符")

        # 翻译（带断点续传）
        start_time = time.time()
        translated = translate_with_resume(full_text, pdf_path, output_base_dir)
        elapsed_time = time.time() - start_time

        print(f"\n✅ 全部翻译完成，耗时: {elapsed_time/60:.1f}分钟")
    else:
        print("\n3️⃣ 跳过翻译环节（中文PDF）")
        translated = full_text

    # 4. 生成概述
    print("\n4️⃣ 生成论文概述（纯中文，200字以内）...")
    print("⏳ 正在生成概述...")
    summary = generate_summary(full_text[:5000])
    print(f"✅ 概述生成完成，字符数: {len(summary)}")

    # 5. 保存翻译文件
    translation_dir = output_base_dir / '已完成' / '翻译'
    translation_dir.mkdir(parents=True, exist_ok=True)

    translation_file = translation_dir / f"{pdf_path.stem}_翻译.txt"
    with open(translation_file, 'w', encoding='utf-8') as f:
        f.write(f"# 论文翻译\n\n")
        f.write(f"**源文件**: {pdf_path.name}\n")
        f.write(f"**处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**翻译模型**: 本地Ollama (qwen2.5:7b)\n")
        f.write(f"**版本**: v2.0（进度显示 + 断点续传）\n")
        if is_english:
            f.write(f"**分段数**: {len(segments)}\n\n")
        f.write(f"## 📄 翻译内容\n\n")
        f.write(translated)

    print(f"\n💾 翻译文件已保存: {translation_file.name}")

    # 6. 保存概述文件
    summary_dir = output_base_dir / '已完成' / '概述'
    summary_dir.mkdir(parents=True, exist_ok=True)

    summary_file = summary_dir / f"{pdf_path.stem}_概述.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# 论文概述\n\n")
        f.write(f"**源文件**: {pdf_path.name}\n")
        f.write(f"**处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**概述模型**: 本地Ollama (qwen2.5:7b)\n\n")
        f.write(f"## 📚 论文标题\n\n")
        f.write(f"**英文**: {title_en}\n")
        f.write(f"**中文**: {title_cn}\n\n")
        f.write(f"## 📝 论文概述\n\n")
        f.write(summary)

    print(f"💾 概述文件已保存: {summary_file.name}（{len(summary)}字，纯中文）")

    # 7. 移动PDF到原文文件夹
    print("\n5️⃣ 移动文件并清理...")
    original_dir = output_base_dir / '已完成' / '原文'
    original_dir.mkdir(parents=True, exist_ok=True)

    target_original = original_dir / pdf_path.name
    shutil.move(str(pdf_path), str(target_original))
    print(f"✅ PDF已移动: {target_original.name} → 已完成/原文/")

    # 删除处理中的提取文件
    try:
        extracted_file.unlink()
        print(f"🗑️ 删除提取文件: {extracted_file.name}")
    except:
        pass

    # 输出摘要
    print("\n" + "=" * 60)
    print("📊 处理结果摘要")
    print("=" * 60)
    print(f"📄 原文件: {pdf_path.name}")
    print(f"📊 提取字符数: {len(full_text):,}")
    print(f"🌍 语言: {'英文（已翻译）' if is_english else '中文（未翻译）'}")
    if is_english:
        print(f"🔪 分段数: {len(segments)}段")
        print(f"🤖 翻译模型: 本地Ollama (qwen2.5:7b)")
    print(f"💾 翻译文件: {translation_file.name}")
    print(f"💾 概述文件: {summary_file.name}（{len(summary)}字，纯中文）")
    print(f"💾 原文文件: {target_original.name}")
    print(f"💰 成本: 0元（本地模型，不消耗线上API）")
    print("✨ 新功能: 进度显示 + 断点续传")
    print("\n✅ 处理完成！")

    return {
        'original': target_original,
        'translation': translation_file,
        'summary': summary_file,
        'extracted_chars': len(full_text),
        'is_english': is_english,
        'segments': len(segments) if is_english else 0
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("用法: python3 process_pdf_v2.py <pdf_path> <output_base_dir>")
        print("示例: python3 process_pdf_v2.py ~/Documents/论文处理/未处理/英文/test.pdf ~/Documents/论文处理")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_base_dir = sys.argv[2]

    process_pdf(pdf_path, output_base_dir)

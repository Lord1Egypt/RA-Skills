# -*- coding: utf-8 -*-
"""使用 TTSController 生成音频"""

import os
import sys
import json
from pathlib import Path

os.chdir('d:/vscode/AI-podcast/ai-podcast-dual-host')
sys.path.insert(0, '.')

# 清理代理
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

# 设置 TTS 环境变量
os.environ['VOLCANO_TTS_APP_ID'] = '2467721245'
os.environ['VOLCANO_TTS_ACCESS_TOKEN'] = 'sO9sDDlzCsfz8rrSITooQ3JlThxiCwlX'

from src.tts_controller import VolcanoTTSController
from src.schema import ScriptVersion, DialogueLine, TokenUsage

# 读取脚本
with open('tests/persona-resource/output/cross_time_script_e2e.json', 'r', encoding='utf-8') as f:
    script_data = json.load(f)

print('=' * 70)
print('生成播客音频')
print('=' * 70)
print()

# 创建 ScriptVersion 对象
lines = [DialogueLine(speaker=l['speaker'], text=l['text']) for l in script_data['lines']]

# 由于字数限制，只取前 30 句生成音频（约 1500 秒）
lines = lines[:30]

script = ScriptVersion(
    schema_version='1.0',
    session_id='crosstim01',
    outline_checksum='test_checksum',
    lines=lines,
    word_count=3000,
    estimated_duration_sec=1200,  # 20 分钟
    token_usage=TokenUsage(input=1000, output=3000, total=4000)
)

print(f'脚本行数: {len(script.lines)}')
print(f'预估字数: {script.word_count}')
print(f'预估时长: {script.estimated_duration_sec} 秒')
print()

# 创建 TTS 控制器
# 音色选择：
# - 林肯：zh_male_shaonianzixin_uranus_bigtts (少年梓辛 2.0 - 年轻男声)
# - 黛玉：zh_female_xiaohe_uranus_bigtts (小何 2.0 - 温柔女声)
# ⚠️ 注意：zh_male_sophie_uranus_bigtts 虽含'male'但实际是女声
print('初始化 TTS 控制器...')
tts = VolcanoTTSController(
    host_a_voice='zh_male_shaonianzixin_uranus_bigtts',  # 林肯 - 年轻男声
    host_b_voice='zh_female_xiaohe_uranus_bigtts',  # 黛玉 - 温柔女声
    enable_context=True
)

# 输出路径
output_dir = Path('tests/persona-resource/output')
output_file = output_dir / 'cross_time_podcast.mp3'

print(f'输出文件: {output_file}')
print()

# 生成音频
try:
    print('开始生成音频...')
    print()

    def progress_callback(current, total):
        if current % 5 == 0 or current == total:
            print(f'  进度: {current}/{total} ({current * 100 // total}%)')

    result_path = tts.generate_dual_audio(
        script=script,
        output_path=output_file,
        progress_callback=progress_callback
    )

    print()
    print('=' * 70)
    print('音频生成成功!')
    print('=' * 70)
    print(f'文件路径: {result_path}')
    print(f'文件大小: {result_path.stat().st_size / 1024 / 1024:.2f} MB')

except Exception as e:
    print()
    print('=' * 70)
    print('音频生成失败')
    print('=' * 70)
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()

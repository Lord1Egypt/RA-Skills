#!/usr/bin/env python3
"""
tests/test_media_probe_v250.py — 媒体探测/转录回归（P2 G5 修复，v2.5.0）

覆盖：
- T1 whisper 未安装 → transcript=None + 原因标注（降级不崩）
- T2 mock whisper + 本地 file:// 音频 → 真实转录（INFOSEEK_WHISPER_MODEL 生效）
- T3 whisper 运行时崩溃 → 降级（transcript=None + available=False）
- T4 纯本地路径输入（非 file://）→ 可转录
- T5 网络媒体不自动转录（降级说明）
"""

import os
import sys
import tempfile
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp(prefix='infoseek_media_')

from mcp_tools_search import _probe_media  # noqa: E402

_fails = []


def _check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


def main():
    # T1 未安装
    print('--- T1 whisper 未安装 ---')
    sys.modules.pop('whisper', None)
    r = _probe_media('https://example.com/video.mp4')
    _check('返回结构', r is not None)
    _check('transcript=None', r['transcript'] is None)
    _check('available=False', r['transcript_available'] is False)
    _check('原因标注', '未安装' in r['note'] or '可用' in r['note'], r['note'])

    # 安装 mock whisper
    fake = types.ModuleType('whisper')

    class _FakeModel:
        def transcribe(self, path):
            return {'text': '  模拟 转写 文本  '}

    fake.load_model = lambda name: _FakeModel()
    sys.modules['whisper'] = fake
    tmp_audio = os.path.join(tempfile.mkdtemp(prefix='audio_'), 'clip.mp3')
    Path(tmp_audio).write_bytes(b'fake-audio-bytes')
    os.environ['INFOSEEK_WHISPER_MODEL'] = 'base'

    # T2 file:// 本地转录
    print('--- T2 file:// 转录 ---')
    r2 = _probe_media('file://' + tmp_audio)
    _check('transcript 非空', r2['transcript'] == '模拟 转写 文本', r2['transcript'])
    _check('available=True', r2['transcript_available'] is True)
    _check('完成标注', '转录完成' in r2['note'], r2['note'])

    # T4 纯路径输入
    print('--- T4 纯路径输入 ---')
    r4 = _probe_media(tmp_audio)
    _check('纯路径可转录', r4['transcript'] == '模拟 转写 文本', str(r4.get('transcript')))

    # T5 网络媒体不自动转录
    print('--- T5 网络媒体降级 ---')
    r5 = _probe_media('https://example.com/audio.mp3')
    _check('网络媒体 transcript=None', r5['transcript'] is None)
    _check('标注不自动转录', '未自动转录' in r5['note'], r5['note'])

    # T3 崩溃降级
    print('--- T3 崩溃降级 ---')
    class _BadModel:
        def transcribe(self, path):
            raise RuntimeError('model load failed')

    fake.load_model = lambda name: _BadModel()
    r3 = _probe_media('file://' + tmp_audio)
    _check('崩溃 → None', r3['transcript'] is None)
    _check('崩溃 → available=False', r3['transcript_available'] is False)
    _check('崩溃 → 降级标注', '降级' in r3['note'], r3['note'])

    sys.modules.pop('whisper', None)
    os.environ.pop('INFOSEEK_WHISPER_MODEL', None)
    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_media_probe_v250) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()
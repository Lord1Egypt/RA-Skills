#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将长文本或整个文件夹的内容分段调用 edge-tts 合成 MP3，通过 PCM 拼接实现无字符限制，
并可选在最终输出中加入背景音乐（片头/片中/片尾三段式音量包络）。
"""

import argparse
import asyncio
import os
import re
import shutil
import subprocess
import wave
from pathlib import Path

import edge_tts

try:
    import miniaudio
    HAS_MINIAUDIO = True
except ImportError:
    HAS_MINIAUDIO = False

TITLE_PAUSE = "……"


def is_markdown_file(path: str) -> bool:
    return path.lower().endswith('.md')


def clean_markdown(text: str) -> str:
    lines = text.splitlines()
    result_lines = []
    bullet_count = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result_lines.append("")
            bullet_count = 0
            continue

        if stripped.startswith('```'):
            continue

        if re.match(r'^#{1,6}\s+', stripped):
            title_text = re.sub(r'^#{1,6}\s+', '', stripped).strip()
            result_lines.append(title_text + TITLE_PAUSE)
            continue

        if stripped.startswith('>'):
            quote_text = stripped.lstrip('>').strip()
            result_lines.append(f"引用：{quote_text}")
            continue

        bm = re.match(r'^[-*+]\s+(.*)', stripped)
        if bm:
            bullet_count += 1
            result_lines.append(f"第{bullet_count}点：{bm.group(1)}")
            continue

        om = re.match(r'^\d+\.\s+(.*)', stripped)
        if om:
            bullet_count += 1
            result_lines.append(f"第{bullet_count}点：{om.group(1)}")
            continue

        if stripped:
            bullet_count = 0

        cleaned = line
        cleaned = re.sub(r'\*\*(.+?)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'__(.+?)__', r'\1', cleaned)
        cleaned = re.sub(r'\*(.+?)\*', r'\1', cleaned)
        cleaned = re.sub(r'_(.+?)_', r'\1', cleaned)
        cleaned = re.sub(r'~~(.+?)~~', r'\1', cleaned)
        cleaned = re.sub(r'`(.+?)`', r'代码：\1', cleaned)
        cleaned = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', cleaned)

        if cleaned.strip():
            result_lines.append(cleaned)

    return '\n'.join(result_lines)


def find_ffmpeg() -> str | None:
    paths = [
        '/tmp/ffmpeg_bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        '/usr/bin/ffmpeg',
    ]
    for p in paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def split_text(text: str, chunk_size: int = 800) -> list[str]:
    raw_sentences = re.split(r'(?<=[。！？；，])', text)
    chunks, current = [], ''
    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > chunk_size:
            if current.strip():
                chunks.append(current.strip())
                current = ''
            chunks.extend(_split_long_sentence(sentence, chunk_size))
            continue
        if len(current) + len(sentence) <= chunk_size:
            current += sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence
    if current.strip():
        chunks.append(current.strip())
    return [c for c in chunks if c]


def _split_long_sentence(text: str, chunk_size: int) -> list[str]:
    separators = ['、', '，', ' ', '\t']
    for sep in separators:
        parts = text.split(sep)
        subchunks, buf = [], ''
        for idx, part in enumerate(parts):
            suffix = sep if idx < len(parts) - 1 else ''
            candidate = buf + part + suffix
            if len(candidate) <= chunk_size:
                buf = candidate
            else:
                if buf:
                    subchunks.append(buf.strip())
                buf = part + suffix
        if buf.strip():
            subchunks.append(buf.strip())
        if all(len(s) <= chunk_size for s in subchunks):
            return subchunks
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


async def generate_segment(text: str, voice: str, output_mp3: str,
                           rate_limit_delay: float = 2.0,
                           speed: float = 1.0) -> int:
    rate_percent = f"{(speed - 1.0) * 100:+.0f}%"
    communicate = edge_tts.Communicate(text, voice, rate=rate_percent)
    await communicate.save(output_mp3)
    if rate_limit_delay > 0:
        await asyncio.sleep(rate_limit_delay)
    return os.path.getsize(output_mp3)


async def text_to_wav(text: str, output_path: str, voice: str = "zh-CN-XiaoxiaoNeural",
                      chunk_size: int = 800,
                      rate_limit_delay: float = 2.0,
                      speed: float = 1.0) -> dict:
    if not HAS_MINIAUDIO:
        raise RuntimeError('miniaudio is required. Install: pip3 install miniaudio')

    chunks = split_text(text, chunk_size)
    all_pcm = b''
    sample_rate, nchannels = None, None

    print(f"[MS-TTS-BGM] Text: {len(text)} chars → {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        mp3_file = f"/tmp/ms_tts_chunk_{os.getpid()}_{i}.mp3"
        is_last = i == len(chunks) - 1
        seg_delay = 0.0 if is_last else rate_limit_delay
        await generate_segment(chunk, voice, mp3_file, seg_delay, speed)

        with open(mp3_file, 'rb') as f:
            decoded = miniaudio.decode(f.read())
        sample_rate = decoded.sample_rate
        nchannels = decoded.nchannels

        if hasattr(decoded.samples, 'tobytes'):
            all_pcm += decoded.samples.tobytes()
        else:
            all_pcm += bytes(decoded.samples)
        os.unlink(mp3_file)

        if not is_last:
            print(f"[MS-TTS-BGM] Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars), waiting {rate_limit_delay}s...")
        else:
            print(f"[MS-TTS-BGM] Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")

    wav_path = output_path if output_path.endswith('.wav') else output_path + '.wav'
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(all_pcm)

    return {
        'wav_path': wav_path,
        'chunks': len(chunks),
        'size_mb': os.path.getsize(wav_path) / (1024 * 1024),
        'duration_sec': len(all_pcm) / (nchannels * sample_rate * 2),
        'sample_rate': sample_rate,
        'nchannels': nchannels,
    }


def validate_bgm_args(bgm_path: str | None, intro: float, outro: float,
                      mid_volume: float, full_volume: float) -> None:
    if bgm_path and not os.path.isfile(bgm_path):
        raise FileNotFoundError(f'BGM file not found: {bgm_path}')
    if intro < 0 or outro < 0:
        raise ValueError('BGM intro/outro duration must be >= 0.')
    if not (0 < mid_volume <= 1.0):
        raise ValueError('BGM mid volume must be within (0, 1].')
    if not (0 < full_volume <= 1.0):
        raise ValueError('BGM full volume must be within (0, 1].')
    if full_volume < mid_volume:
        raise ValueError('BGM full volume must be >= BGM mid volume.')


def build_bgm_envelope(duration_sec: float, intro_sec: float, outro_sec: float) -> dict:
    duration_sec = max(0.0, float(duration_sec))
    intro_sec = max(0.0, float(intro_sec))
    outro_sec = max(0.0, float(outro_sec))

    if duration_sec == 0:
        return {
            'duration_sec': 0.0,
            'intro_sec': 0.0,
            'outro_sec': 0.0,
            'outro_start_sec': 0.0,
        }

    total_side = intro_sec + outro_sec
    if total_side > duration_sec:
        scale = duration_sec / total_side
        intro_sec *= scale
        outro_sec *= scale

    outro_start_sec = max(0.0, duration_sec - outro_sec)
    return {
        'duration_sec': duration_sec,
        'intro_sec': intro_sec,
        'outro_sec': outro_sec,
        'outro_start_sec': outro_start_sec,
    }


def build_bgm_volume_expression(envelope: dict, mid_volume: float, full_volume: float) -> str:
    intro = envelope['intro_sec']
    outro = envelope['outro_sec']
    outro_start = envelope['outro_start_sec']
    duration = envelope['duration_sec']

    if duration <= 0:
        return '0'

    if intro <= 0 and outro <= 0:
        return f'{mid_volume:.6f}'

    intro_half = max(intro / 2.0, 0.000001)
    outro_half = max(outro / 2.0, 0.000001)
    outro_mid = outro_start + outro_half

    return (
        f"if(lt(t,{intro:.6f}),"
        f"if(lt(t,{intro_half:.6f}),"
        f"{full_volume:.6f}*(t/{intro_half:.6f}),"
        f"{full_volume:.6f}-({full_volume:.6f}-{mid_volume:.6f})*((t-{intro_half:.6f})/{intro_half:.6f})"
        f"),"
        f"if(lt(t,{outro_start:.6f}),"
        f"{mid_volume:.6f},"
        f"if(lt(t,{outro_mid:.6f}),"
        f"{mid_volume:.6f}+({full_volume:.6f}-{mid_volume:.6f})*((t-{outro_start:.6f})/{outro_half:.6f}),"
        f"{full_volume:.6f}*(1-((t-{outro_mid:.6f})/{outro_half:.6f}))"
        f")"
        f")"
        f")"
    )


def mix_bgm_with_voice(voice_wav_path: str, output_mp3_path: str, bgm_path: str,
                       ffmpeg_path: str, intro_sec: float, outro_sec: float,
                       mid_volume: float, full_volume: float,
                       loop_bgm: bool = True) -> dict:
    with wave.open(voice_wav_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        voice_duration_sec = frames / float(rate)

    total_duration_sec = voice_duration_sec + intro_sec + outro_sec
    envelope = build_bgm_envelope(total_duration_sec, intro_sec, outro_sec)
    intro = envelope['intro_sec']
    outro = envelope['outro_sec']
    outro_start = envelope['outro_start_sec']
    middle_len = max(0.0, voice_duration_sec)

    bgm_input_args = []
    if loop_bgm:
        bgm_input_args.extend(['-stream_loop', '-1'])

    filter_parts = []
    concat_inputs = []
    part_count = 0

    if intro > 0:
        intro_half = max(intro / 2.0, 0.001)
        filter_parts.append(
            f"[1:a]atrim=0:{intro:.6f},asetpts=PTS-STARTPTS,"
            f"volume={full_volume:.6f},"
            f"afade=t=in:st=0:d={intro_half:.6f},"
            f"afade=t=out:st={intro_half:.6f}:d={intro_half:.6f}[bgm_intro]"
        )
        concat_inputs.append('[bgm_intro]')
        part_count += 1

    if middle_len > 0:
        filter_parts.append(
            f"[1:a]atrim=0:{middle_len:.6f},asetpts=PTS-STARTPTS,"
            f"volume={mid_volume:.6f}[bgm_mid]"
        )
        concat_inputs.append('[bgm_mid]')
        part_count += 1

    if outro > 0:
        outro_half = max(outro / 2.0, 0.001)
        filter_parts.append(
            f"[1:a]atrim=0:{outro:.6f},asetpts=PTS-STARTPTS,"
            f"volume={full_volume:.6f},"
            f"afade=t=in:st=0:d={outro_half:.6f},"
            f"afade=t=out:st={outro_half:.6f}:d={outro_half:.6f}[bgm_outro]"
        )
        concat_inputs.append('[bgm_outro]')
        part_count += 1

    if part_count == 0:
        raise RuntimeError('Invalid BGM envelope: no segments to mix.')

    filter_parts.append(
        f"{''.join(concat_inputs)}concat=n={part_count}:v=0:a=1,atrim=0:{total_duration_sec:.6f}[bgm_full]"
    )

    intro_delay_ms = max(0, int(round(intro * 1000.0)))
    filter_parts.append(
        f"[0:a]adelay={intro_delay_ms}:all=1,apad,atrim=0:{total_duration_sec:.6f}[voice_body]"
    )

    filter_parts.append('[voice_body][bgm_full]amix=inputs=2:duration=first:dropout_transition=0[mix]')
    filter_complex = ';'.join(filter_parts)

    command = [
        ffmpeg_path,
        '-y',
        '-i', voice_wav_path,
        *bgm_input_args,
        '-i', bgm_path,
        '-filter_complex', filter_complex,
        '-map', '[mix]',
        '-b:a', '192k',
        output_mp3_path,
    ]

    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        stderr = (completed.stderr or '').strip()
        raise RuntimeError(f'ffmpeg bgm mix failed: {stderr[:400]}')

    return {
        'mp3_path': output_mp3_path,
        'duration_sec': total_duration_sec,
        'bgm_envelope': envelope,
    }


async def text_to_mp3(text: str, output_path: str, voice: str = 'zh-CN-XiaoxiaoNeural',
                      chunk_size: int = 800, ffmpeg_path: str = None,
                      rate_limit_delay: float = 2.0,
                      speed: float = 1.0,
                      bgm_path: str | None = None,
                      bgm_intro: float = 5.0,
                      bgm_outro: float = 5.0,
                      bgm_mid_volume: float = 0.12,
                      bgm_full_volume: float = 0.8,
                      bgm_loop: bool = True) -> dict:
    if ffmpeg_path is None:
        ffmpeg_path = find_ffmpeg()

    validate_bgm_args(bgm_path, bgm_intro, bgm_outro, bgm_mid_volume, bgm_full_volume)

    if ffmpeg_path is None:
        print('[MS-TTS-BGM] Warning: ffmpeg not found, outputting WAV instead.')
        print('[MS-TTS-BGM] Install ffmpeg: curl -L https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip -o /tmp/ffmpeg.zip && unzip /tmp/ffmpeg.zip -d /tmp/ffmpeg_bin')
        if bgm_path:
            raise RuntimeError('ffmpeg is required when --bgm is provided.')

    wav_result = await text_to_wav(text, output_path, voice, chunk_size, rate_limit_delay, speed)
    wav_path = wav_result['wav_path']
    mp3_path = wav_path.replace('.wav', '.mp3')

    if bgm_path:
        mixed = mix_bgm_with_voice(
            voice_wav_path=wav_path,
            output_mp3_path=mp3_path,
            bgm_path=bgm_path,
            ffmpeg_path=ffmpeg_path,
            intro_sec=bgm_intro,
            outro_sec=bgm_outro,
            mid_volume=bgm_mid_volume,
            full_volume=bgm_full_volume,
            loop_bgm=bgm_loop,
        )
        os.unlink(wav_path)
        wav_result['mp3_path'] = mixed['mp3_path']
        wav_result['wav_path'] = None
        wav_result['size_mb'] = os.path.getsize(mp3_path) / (1024 * 1024)
        wav_result['duration_sec'] = mixed['duration_sec']
        wav_result['bgm_envelope'] = mixed['bgm_envelope']
        return wav_result

    if ffmpeg_path and os.path.exists(ffmpeg_path):
        subprocess.run([
            ffmpeg_path, '-y', '-i', wav_path,
            '-b:a', '192k', mp3_path
        ], capture_output=True)
        os.unlink(wav_path)
        wav_result['mp3_path'] = mp3_path
        wav_result['wav_path'] = None
        wav_result['size_mb'] = os.path.getsize(mp3_path) / (1024 * 1024)
    else:
        shutil.move(wav_path, mp3_path)
        wav_result['mp3_path'] = mp3_path
        wav_result['wav_path'] = None

    return wav_result


def synthesize_text(input_text: str, output_path: str, voice: str = 'zh-CN-XiaoxiaoNeural',
                    chunk_size: int = 800, ffmpeg_path: str = None,
                    rate_limit_delay: float = 2.0,
                    speed: float = 1.0,
                    bgm_path: str | None = None,
                    bgm_intro: float = 5.0,
                    bgm_outro: float = 5.0,
                    bgm_mid_volume: float = 0.12,
                    bgm_full_volume: float = 0.8,
                    bgm_loop: bool = True) -> dict:
    return asyncio.run(text_to_mp3(
        input_text, output_path, voice, chunk_size, ffmpeg_path,
        rate_limit_delay, speed, bgm_path, bgm_intro, bgm_outro,
        bgm_mid_volume, bgm_full_volume, bgm_loop,
    ))


def synthesize_file(input_file: str, output_path: str, voice: str = 'zh-CN-XiaoxiaoNeural',
                    chunk_size: int = 800, ffmpeg_path: str = None,
                    rate_limit_delay: float = 2.0,
                    speed: float = 1.0,
                    bgm_path: str | None = None,
                    bgm_intro: float = 5.0,
                    bgm_outro: float = 5.0,
                    bgm_mid_volume: float = 0.12,
                    bgm_full_volume: float = 0.8,
                    bgm_loop: bool = True) -> dict:
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    if is_markdown_file(input_file):
        print('[MS-TTS-BGM] Detected .md file, cleaning markdown formatting...')
        text = clean_markdown(text)
    return asyncio.run(text_to_mp3(
        text, output_path, voice, chunk_size, ffmpeg_path,
        rate_limit_delay, speed, bgm_path, bgm_intro, bgm_outro,
        bgm_mid_volume, bgm_full_volume, bgm_loop,
    ))


def synthesize_dir(input_dir: str, output_dir: str, voice: str = 'zh-CN-XiaoxiaoNeural',
                   chunk_size: int = 800, ffmpeg_path: str = None, delay: float = 3.0,
                   rate_limit_delay: float = 2.0,
                   speed: float = 1.0,
                   bgm_path: str | None = None,
                   bgm_intro: float = 5.0,
                   bgm_outro: float = 5.0,
                   bgm_mid_volume: float = 0.12,
                   bgm_full_volume: float = 0.8,
                   bgm_loop: bool = True) -> list[dict]:
    os.makedirs(output_dir, exist_ok=True)
    files = []
    for fname in sorted(os.listdir(input_dir)):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath) and (fname.endswith('.txt') or fname.endswith('.md')):
            files.append(fpath)

    if not files:
        print(f'[MS-TTS-BGM] No .txt or .md files found in {input_dir}')
        return []

    print(f'[MS-TTS-BGM] Found {len(files)} files to process')
    results = []

    for idx, fpath in enumerate(files, 1):
        base = os.path.splitext(os.path.basename(fpath))[0]
        out_path = os.path.join(output_dir, base)
        print(f"\n[MS-TTS-BGM] [{idx}/{len(files)}] Processing: {os.path.basename(fpath)}")
        try:
            result = synthesize_file(
                fpath, out_path, voice, chunk_size, ffmpeg_path,
                rate_limit_delay, speed, bgm_path, bgm_intro, bgm_outro,
                bgm_mid_volume, bgm_full_volume, bgm_loop,
            )
            out_file = result.get('mp3_path') or result.get('wav_path')
            print(f"[MS-TTS-BGM] ✓ Done: {os.path.basename(out_file)} ({result['chunks']} chunks, {result['size_mb']:.1f}MB, {result['duration_sec']:.0f}s)")
            results.append({'file': os.path.basename(fpath), 'status': 'ok', **result})
        except Exception as e:
            print(f"[MS-TTS-BGM] ✗ Failed: {os.path.basename(fpath)} — {e}")
            results.append({'file': os.path.basename(fpath), 'status': 'error', 'error': str(e)})

        if idx < len(files) and delay > 0:
            print(f'[MS-TTS-BGM] Waiting {delay}s before next file...')
            import time
            time.sleep(delay)

    ok_count = sum(1 for r in results if r['status'] == 'ok')
    err_count = len(results) - ok_count
    print(f"\n[MS-TTS-BGM] === Batch complete: {ok_count} ok, {err_count} failed ===")
    return results


def main():
    parser = argparse.ArgumentParser(description='Microsoft TTS 分段合成工具（可选 BGM 版）')
    parser.add_argument('--input', '-i', required=True, help='输入文本或文本文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径（不含扩展名）')
    parser.add_argument('--voice', '-v', default='zh-CN-XiaoxiaoNeural', help='TTS 声音名称')
    parser.add_argument('--chunk', '-c', type=int, default=800, help='每段最大字符数（默认800）')
    parser.add_argument('--ffmpeg', '-f', default=None, help='ffmpeg 路径（默认自动查找）')
    parser.add_argument('--delay', '-d', type=float, default=3.0, help='文件夹批量模式：连续文件间的延迟秒数（默认3秒）')
    parser.add_argument('--rate', '-r', type=float, default=2.0, help='每个TTS请求之间的延迟秒数（默认2秒）')
    parser.add_argument('--speed', '-s', type=float, default=1.0, help='语速倍率（默认1.0）')
    parser.add_argument('--bgm', default=None, help='可选背景音乐文件路径')
    parser.add_argument('--bgm-intro', type=float, default=5.0, help='片头时长（秒，默认5）')
    parser.add_argument('--bgm-outro', type=float, default=5.0, help='片尾时长（秒，默认5）')
    parser.add_argument('--bgm-mid-volume', type=float, default=0.12, help='正文铺底最低音量（默认0.12）')
    parser.add_argument('--bgm-full-volume', type=float, default=0.8, help='片头片尾峰值音量（默认0.8）')
    parser.add_argument('--bgm-loop', action='store_true', default=True, help='背景音乐长度不足时自动循环（默认开启）')
    args = parser.parse_args()

    if args.ffmpeg is None:
        args.ffmpeg = find_ffmpeg()
        if args.ffmpeg:
            print(f'[MS-TTS-BGM] Found ffmpeg: {args.ffmpeg}')
        else:
            print('[MS-TTS-BGM] Warning: ffmpeg not found, will output WAV')

    if os.path.isdir(args.input):
        synthesize_dir(
            args.input, args.output, args.voice, args.chunk, args.ffmpeg,
            args.delay, args.rate, args.speed,
            args.bgm, args.bgm_intro, args.bgm_outro,
            args.bgm_mid_volume, args.bgm_full_volume, args.bgm_loop,
        )
        return

    if os.path.isfile(args.input):
        result = synthesize_file(
            args.input, args.output, args.voice, args.chunk, args.ffmpeg,
            args.rate, args.speed,
            args.bgm, args.bgm_intro, args.bgm_outro,
            args.bgm_mid_volume, args.bgm_full_volume, args.bgm_loop,
        )
    else:
        result = synthesize_text(
            args.input, args.output, args.voice, args.chunk, args.ffmpeg,
            args.rate, args.speed,
            args.bgm, args.bgm_intro, args.bgm_outro,
            args.bgm_mid_volume, args.bgm_full_volume, args.bgm_loop,
        )

    print('\n[MS-TTS-BGM] Done!')
    print(f"  Chunks: {result['chunks']}")
    print(f"  Size: {result['size_mb']:.2f} MB")
    if result.get('mp3_path'):
        print(f"  Output: {result['mp3_path']}")
    if result.get('wav_path'):
        print(f"  WAV: {result['wav_path']}")
    print(f"  Duration: {result['duration_sec']:.1f} seconds")
    if result.get('bgm_envelope'):
        print(f"  BGM Envelope: {result['bgm_envelope']}")


if __name__ == '__main__':
    main()

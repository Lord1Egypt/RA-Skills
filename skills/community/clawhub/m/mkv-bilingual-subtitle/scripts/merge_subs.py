#!/usr/bin/env python3
"""
MKV Bilingual Subtitle Merger
Extracts Chinese & English subtitles from MKV, merges them (EN on top, CN below),
and embeds the merged subtitle back into the MKV.

Usage:
  python3 merge_subs.py <input.mkv> [--output <output.mkv>] [--keep-temp]
  python3 merge_subs.py <input_dir>  [--output <output_dir>] [--keep-temp] [--recursive]

Requirements: mkvmerge, mkvextract (MKVToolNix)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ─── SRT helpers ─────────────────────────────────────────────────────────────

def parse_srt(text):
    """Parse SRT content into list of dicts: {index, start_ms, end_ms, text}"""
    pattern = re.compile(
        r'(\d+)\s*\n'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n'
        r'(.*?)(?=\n\n|\n*\Z)',
        re.DOTALL
    )
    entries = []
    for m in pattern.finditer(text.strip()):
        entries.append({
            'index': int(m.group(1)),
            'start_ms': srt_time_to_ms(m.group(2)),
            'end_ms': srt_time_to_ms(m.group(3)),
            'text': m.group(4).strip(),
        })
    return entries

def srt_time_to_ms(t):
    h, m, s, ms = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', t).groups()
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def ms_to_srt_time(ms):
    h = ms // 3600000; ms %= 3600000
    m = ms // 60000; ms %= 60000
    s = ms // 1000; ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def entries_to_srt(entries):
    """Convert merged entries back to SRT format"""
    lines = []
    for i, e in enumerate(entries, 1):
        lines.append(str(i))
        lines.append(f"{ms_to_srt_time(e['start_ms'])} --> {ms_to_srt_time(e['end_ms'])}")
        lines.append(e['text'])
        lines.append('')
    return '\n'.join(lines)

# ─── ASS helpers ─────────────────────────────────────────────────────────────

def parse_ass(text):
    """Parse ASS/SSA content into list of dicts: {start_ms, end_ms, style, text, raw_prefix}"""
    entries = []
    fmt_line = None
    in_events = False
    for line in text.split('\n'):
        line_stripped = line.strip()
        if line_stripped == '[Events]':
            in_events = True
            continue
        if line_stripped.startswith('[') and in_events:
            in_events = False
            continue
        if in_events and line_stripped.startswith('Format:'):
            fmt_line = line_stripped
            continue
        if in_events and line_stripped.startswith('Dialogue:'):
            parts = line_stripped[len('Dialogue:'):].strip().split(',', 9)
            if len(parts) >= 10:
                entries.append({
                    'start_ms': ass_time_to_ms(parts[1]),
                    'end_ms': ass_time_to_ms(parts[2]),
                    'style': parts[3].strip(),
                    'text': parts[9],
                    'raw_prefix': ','.join(parts[:9]),  # everything before text
                })
    return entries, fmt_line

def ass_time_to_ms(t):
    """Convert ASS time (H:MM:SS.CC) to ms"""
    parts = t.strip().split(':')
    h = int(parts[0])
    m = int(parts[1])
    s_parts = parts[2].split('.')
    s = int(s_parts[0])
    cs = int(s_parts[1].ljust(2, '0')[:2]) if len(s_parts) > 1 else 0
    return h*3600000 + m*60000 + s*1000 + cs*10

def ms_to_ass_time(ms):
    h = ms // 3600000; ms %= 3600000
    m = ms // 60000; ms %= 60000
    s = ms // 1000; cs = (ms % 1000) // 10
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def entries_to_ass(entries, fmt_line, header_lines):
    """Convert merged entries back to ASS format"""
    lines = list(header_lines)
    if fmt_line:
        lines.append(fmt_line)
    for e in entries:
        start = ms_to_ass_time(e['start_ms'])
        end = ms_to_ass_time(e['end_ms'])
        lines.append(f"Dialogue: {e['raw_prefix']},{start},{end},{e['style']},,0,0,0,,{e['text']}")
    return '\n'.join(lines)

# ─── Merge logic ─────────────────────────────────────────────────────────────

def overlap_ratio(s1, e1, s2, e2):
    """Calculate overlap ratio relative to the shorter entry"""
    overlap_start = max(s1, s2)
    overlap_end = min(e1, e2)
    if overlap_start >= overlap_end:
        return 0
    overlap = overlap_end - overlap_start
    shorter = min(e1 - s1, e2 - s2)
    return overlap / shorter if shorter > 0 else 0

def merge_entries(en_entries, cn_entries, fmt='srt', overlap_threshold=0.3):
    """Merge EN and CN subtitle entries. EN on top, CN below.
    
    Strategy:
    1. For each EN entry, find best-matching CN entry by time overlap
    2. If overlap ratio > threshold, merge them (take union time range)
    3. Unmatched entries are kept as-is
    4. Sort by start time
    """
    matched = []
    used_cn = set()
    
    for e in en_entries:
        best_cn_idx = None
        best_ratio = 0
        for i, c in enumerate(cn_entries):
            if i in used_cn:
                continue
            r = overlap_ratio(e['start_ms'], e['end_ms'], c['start_ms'], c['end_ms'])
            if r > best_ratio and r > overlap_threshold:
                best_ratio = r
                best_cn_idx = i
        
        if best_cn_idx is not None:
            used_cn.add(best_cn_idx)
            c = cn_entries[best_cn_idx]
            merged_start = min(e['start_ms'], c['start_ms'])
            merged_end = max(e['end_ms'], c['end_ms'])
            if fmt == 'srt':
                merged_text = f"{e['text']}\n{c['text']}"
            else:  # ass
                merged_text = f"{e['text']}\\N{c['text']}"
            matched.append({
                'start_ms': merged_start,
                'end_ms': merged_end,
                'text': merged_text,
                'style': e.get('style', 'Default'),
                'raw_prefix': e.get('raw_prefix', '0'),
            })
        else:
            matched.append({
                'start_ms': e['start_ms'],
                'end_ms': e['end_ms'],
                'text': e['text'],
                'style': e.get('style', 'Default'),
                'raw_prefix': e.get('raw_prefix', '0'),
            })
    
    # Add unmatched CN entries
    for i, c in enumerate(cn_entries):
        if i not in used_cn:
            matched.append({
                'start_ms': c['start_ms'],
                'end_ms': c['end_ms'],
                'text': c['text'],
                'style': c.get('style', 'Default'),
                'raw_prefix': c.get('raw_prefix', '0'),
            })
    
    # Sort by start time, then by duration (shorter first for same start)
    matched.sort(key=lambda x: (x['start_ms'], x['end_ms'] - x['start_ms']))
    
    return matched

# ─── MKV operations ─────────────────────────────────────────────────────────

def get_subtitle_tracks(mkv_path):
    """Get subtitle track info from MKV file.
    Uses mkvinfo for full metadata (language, name) since mkvmerge -i
    may not display language properties in some versions.
    """
    # Try mkvinfo first (most reliable for language/name)
    tracks = _get_tracks_from_mkvinfo(mkv_path)
    if tracks:
        return tracks
    # Fallback to mkvmerge -i
    return _get_tracks_from_mkvmerge(mkv_path)

def _get_tracks_from_mkvinfo(mkv_path):
    """Parse mkvinfo output for subtitle tracks with full metadata."""
    if not shutil.which('mkvinfo'):
        return []
    result = subprocess.run(
        ['mkvinfo', mkv_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    
    tracks = []
    current_track = None
    
    for line in result.stdout.split('\n'):
        line = re.sub(r'^[|+\s]+', '', line)
        
        # New track
        m = re.match(r'Track number:\s*(\d+)\s*\(track ID for mkvmerge & mkvextract:\s*(\d+)\)', line)
        if m:
            if current_track and current_track.get('type') == 'subtitles':
                tracks.append(current_track)
            current_track = {
                'mkvinfo_num': int(m.group(1)),
                'id': int(m.group(2)),
                'type': '',
                'language': 'und',
                'language_iETF': '',
                'codec_id': '',
                'track_name': '',
            }
            continue
        
        if current_track is None:
            continue
        
        if line.startswith('Track type:'):
            current_track['type'] = line.split(':', 1)[1].strip()
        elif line.startswith('Language:') and not line.startswith('Language (IETF'):
            current_track['language'] = line.split(':', 1)[1].strip()
        elif line.startswith('Language (IETF BCP 47):'):
            current_track['language_iETF'] = line.split(':', 1)[1].strip()
        elif line.startswith('Codec ID:'):
            current_track['codec_id'] = line.split(':', 1)[1].strip()
        elif line.startswith('Name:'):
            current_track['track_name'] = line.split(':', 1)[1].strip()
    
    # Don't forget the last track
    if current_track and current_track.get('type') == 'subtitles':
        tracks.append(current_track)
    
    # Normalize: convert codec_id to friendly name, resolve language
    for t in tracks:
        t['codec'] = _codec_id_to_name(t.get('codec_id', ''))
        # Prefer IETF language code, fallback to legacy
        lang = t.get('language_iETF') or t['language']
        if lang and lang != 'und':
            t['language'] = lang
    
    return tracks

def _get_tracks_from_mkvmerge(mkv_path):
    """Fallback: parse mkvmerge -i output."""
    result = subprocess.run(
        ['mkvmerge', '-i', mkv_path],
        capture_output=True, text=True
    )
    tracks = []
    for line in result.stdout.split('\n'):
        m = re.match(r'Track ID (\d+): subtitles \((.+?)\)(?:\s*\[(.+?)\])?', line)
        if m:
            tid = int(m.group(1))
            codec = m.group(2)
            props_str = m.group(3) or ''
            props = {}
            for pm in re.finditer(r'(\w+):(\w+)', props_str):
                props[pm.group(1)] = pm.group(2)
            tracks.append({
                'id': tid,
                'codec': codec,
                'language': props.get('language', 'und'),
                'track_name': props.get('track_name', ''),
            })
    return tracks

def _codec_id_to_name(codec_id):
    """Convert MKV codec ID to friendly name."""
    mapping = {
        'S_TEXT/UTF8': 'SubRip/SRT',
        'S_TEXT/SSA': 'SSA',
        'S_TEXT/ASS': 'ASS',
        'S_TEXT/USF': 'USF',
        'S_TEXT/WEBVTT': 'WebVTT',
        'S_HDMV/PGS': 'PGS',
        'S_DVDSUB': 'VobSub',
        'S_VOBSUB': 'VobSub',
    }
    return mapping.get(codec_id, codec_id)

def extract_subtitle(mkv_path, track_id, output_path):
    """Extract a subtitle track from MKV"""
    result = subprocess.run(
        ['mkvextract', mkv_path, 'tracks', f'{track_id}:{output_path}'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠ mkvextract warning: {result.stderr.strip()}", file=sys.stderr)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0

def embed_subtitle(mkv_path, sub_path, output_path, language='chi', track_name='中文&英文', 
                   default_track=True):
    """Embed merged subtitle into MKV, keeping all original tracks"""
    cmd = ['mkvmerge', '-o', output_path]
    
    # Copy all tracks from original
    cmd.append(mkv_path)
    
    # Add new subtitle track
    cmd.extend(['--language', f'0:{language}'])
    cmd.extend(['--track-name', f'0:{track_name}'])
    if default_track:
        cmd.extend(['--default-track-flag', '0:1'])
    else:
        cmd.extend(['--default-track-flag', '0:0'])
    cmd.append(sub_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode not in (0, 1):  # 0=success, 1=warnings
        print(f"  ✗ mkvmerge failed: {result.stderr.strip()}", file=sys.stderr)
        return False
    if result.returncode == 1:
        print(f"  ⚠ mkvmerge warnings: {result.stderr.strip()}", file=sys.stderr)
    return True

# ─── Main pipeline ──────────────────────────────────────────────────────────

def find_subtitle_tracks(tracks, lang_code):
    """Find subtitle tracks matching a language code.
    Supports: chi/zho/zh/cn for Chinese, eng/en for English.
    Also matches IETF BCP 47 codes like zh-Hans, zh-CN, en-US.
    """
    lang_map = {
        'chi': {'chi', 'zho', 'zh', 'cn', 'chinese', 'zh-hans', 'zh-cn', 'zh-tw', 'zh-hant'},
        'eng': {'eng', 'en', 'english', 'en-us', 'en-gb'},
    }
    aliases = lang_map.get(lang_code, {lang_code})
    result = []
    for t in tracks:
        lang = t['language'].lower()
        # Check exact match or prefix match (for zh-Hans, en-US etc.)
        if lang in aliases or any(lang.startswith(a + '-') for a in aliases if len(a) <= 3):
            result.append(t)
    return result

def _pick_best_track(tracks, prefer_name=None, avoid_name=None):
    """Select the best subtitle track from a list.
    
    Args:
        tracks: List of track dicts
        prefer_name: Keywords to prefer in track name (lowercased match)
        avoid_name: Keywords to avoid in track name (lowercased match)
    """
    prefer_name = prefer_name or []
    avoid_name = avoid_name or []
    
    if len(tracks) == 1:
        return tracks[0]
    
    # Score each track: lower is better
    def track_score(t):
        name_lower = t.get('track_name', '').lower()
        score = 0
        for kw in avoid_name:
            if kw in name_lower:
                score += 10  # Penalty
        for kw in prefer_name:
            if kw in name_lower:
                score -= 5  # Bonus
        return score
    
    scored = [(track_score(t), i, t) for i, t in enumerate(tracks)]
    scored.sort(key=lambda x: (x[0], x[1]))  # Sort by score, then by original order
    return scored[0][2]

def process_single_file(mkv_path, output_path=None, keep_temp=False):
    """Process a single MKV file: extract → merge → embed"""
    mkv_path = os.path.abspath(mkv_path)
    if not os.path.isfile(mkv_path):
        print(f"✗ File not found: {mkv_path}")
        return False
    
    print(f"\n🎬 Processing: {os.path.basename(mkv_path)}")
    
    # Step 1: Get subtitle tracks
    tracks = get_subtitle_tracks(mkv_path)
    if not tracks:
        print("  ✗ No subtitle tracks found in this file.")
        return False
    
    print(f"  Found {len(tracks)} subtitle track(s):")
    for t in tracks:
        print(f"    Track {t['id']}: {t['codec']} [{t['language']}] {t['track_name']}")
    
    # Step 2: Find Chinese and English tracks
    cn_tracks = find_subtitle_tracks(tracks, 'chi')
    en_tracks = find_subtitle_tracks(tracks, 'eng')
    
    if not cn_tracks:
        print("  ✗ No Chinese subtitle track found (looked for: chi/zho/zh/cn).")
        return False
    if not en_tracks:
        print("  ✗ No English subtitle track found (looked for: eng/en).")
        return False
    
    # Smart track selection: prefer non-SDH English, prefer Simplified Chinese
    cn_track = _pick_best_track(cn_tracks, prefer_name=['simplified', '简体', '简中'], avoid_name=['traditional', '繁体', '繁中'])
    en_track = _pick_best_track(en_tracks, prefer_name=[], avoid_name=['sdh', 'cc', 'hearing', 'hi'])
    print(f"  Using: CN Track {cn_track['id']} ({cn_track['codec']}) [{cn_track['language']}] {cn_track['track_name']} + EN Track {en_track['id']} ({en_track['codec']}) [{en_track['language']}] {en_track['track_name']}")
    
    # Check codec compatibility
    cn_codec = cn_track['codec'].lower()
    en_codec = en_track['codec'].lower()
    
    # Handle image-based subtitles (PGS, VobSub) - cannot merge text
    image_codecs = {'pgs', 'hdmv pgs', 'vobsub', 'dvd subtitles'}
    if any(c in cn_codec for c in image_codecs) or any(c in en_codec for c in image_codecs):
        print("  ✗ Image-based subtitles (PGS/VobSub) cannot be merged. Only text subtitles (SRT/ASS) are supported.")
        return False
    
    # Step 3: Extract subtitles
    with tempfile.TemporaryDirectory() as tmpdir:
        cn_ext = 'ass' if 'ass' in cn_codec or 'ssa' in cn_codec else 'srt'
        en_ext = 'ass' if 'ass' in en_codec or 'ssa' in en_codec else 'srt'
        
        cn_out = os.path.join(tmpdir, f'cn.{cn_ext}')
        en_out = os.path.join(tmpdir, f'en.{en_ext}')
        
        print(f"  Extracting CN subtitle (Track {cn_track['id']})...")
        if not extract_subtitle(mkv_path, cn_track['id'], cn_out):
            print("  ✗ Failed to extract Chinese subtitle.")
            return False
        
        print(f"  Extracting EN subtitle (Track {en_track['id']})...")
        if not extract_subtitle(mkv_path, en_track['id'], en_out):
            print("  ✗ Failed to extract English subtitle.")
            return False
        
        # Step 4: Parse subtitles
        with open(cn_out, 'r', encoding='utf-8') as f:
            cn_text = f.read()
        with open(en_out, 'r', encoding='utf-8') as f:
            en_text = f.read()
        
        # Determine output format - prefer ASS if either is ASS
        use_ass = ('ass' in cn_ext or 'ass' in en_ext)
        # If mixed formats, convert SRT entries to match ASS (simpler: just use SRT style for both)
        # For simplicity: if either is ASS, output ASS; otherwise SRT
        
        if use_ass:
            # Parse both as ASS (SRT will be parsed differently if mixed)
            # If one is SRT and other ASS, convert SRT to ASS-compatible entries
            if cn_ext == 'srt':
                cn_entries_srt = parse_srt(cn_text)
                cn_entries = []
                for e in cn_entries_srt:
                    cn_entries.append({
                        'start_ms': e['start_ms'],
                        'end_ms': e['end_ms'],
                        'text': e['text'],
                        'style': 'Default',
                        'raw_prefix': '0',
                    })
            else:
                cn_entries, _ = parse_ass(cn_text)
            
            if en_ext == 'srt':
                en_entries_srt = parse_srt(en_text)
                en_entries = []
                for e in en_entries_srt:
                    en_entries.append({
                        'start_ms': e['start_ms'],
                        'end_ms': e['end_ms'],
                        'text': e['text'],
                        'style': 'Default',
                        'raw_prefix': '0',
                    })
            else:
                en_entries, _ = parse_ass(en_text)
            
            # Merge
            merged = merge_entries(en_entries, cn_entries, fmt='ass')
            
            # Build ASS output
            # Use CN file's header as template
            if cn_ext == 'ass':
                header_lines, fmt_line = extract_ass_header(cn_text)
            else:
                header_lines, fmt_line = extract_ass_header(en_text)
            
            merged_text = entries_to_ass(merged, fmt_line, header_lines)
            merged_ext = 'ass'
        else:
            cn_entries = parse_srt(cn_text)
            en_entries = parse_srt(en_text)
            merged = merge_entries(en_entries, cn_entries, fmt='srt')
            merged_text = entries_to_srt(merged)
            merged_ext = 'srt'
        
        # Write merged subtitle
        merged_sub_path = os.path.join(tmpdir, f'merged.{merged_ext}')
        with open(merged_sub_path, 'w', encoding='utf-8') as f:
            f.write(merged_text)
        
        print(f"  Merged subtitle: {len(merged)} entries ({merged_ext})")
        
        # Step 5: Embed back into MKV
        # Always write to temp file first, then replace source if no explicit output
        replace_source = (output_path is None)
        
        if replace_source:
            # Write to temp file in same directory, then replace source
            base, ext = os.path.splitext(mkv_path)
            temp_output = f"{base}__bilingual_tmp{ext}"
        else:
            temp_output = output_path
        
        temp_output = os.path.abspath(temp_output)
        
        print(f"  Embedding bilingual subtitle...")
        success = embed_subtitle(
            mkv_path, merged_sub_path, temp_output,
            language='chi', track_name='中英双语',
            default_track=True
        )
        
        if success:
            if replace_source:
                # Replace source file with the new one
                print(f"  Replacing source file...")
                try:
                    os.replace(temp_output, mkv_path)
                    print(f"  ✅ Done! Source file updated in-place: {mkv_path}")
                except OSError as e:
                    print(f"  ⚠ Cannot replace source ({e}), keeping temp output: {temp_output}")
                    # Clean up on failure
            else:
                print(f"  ✅ Done! Output: {temp_output}")
        else:
            print(f"  ✗ Failed to embed subtitle.")
            # Clean up temp output on failure
            if replace_source and os.path.exists(temp_output):
                os.remove(temp_output)
            return False
        
        # Optionally keep temp files
        if keep_temp:
            keep_dir = os.path.join(os.path.dirname(mkv_path), '.subtitle_temp')
            os.makedirs(keep_dir, exist_ok=True)
            for f in [cn_out, en_out, merged_sub_path]:
                if os.path.exists(f):
                    shutil.copy2(f, keep_dir)
            print(f"  Temp files saved to: {keep_dir}")
    
    return True

def extract_ass_header(text):
    """Extract header lines (before [Events]) and Format line from ASS"""
    header_lines = []
    fmt_line = None
    in_header = True
    for line in text.split('\n'):
        if line.strip() == '[Events]':
            in_header = False
            header_lines.append(line)
            continue
        if in_header:
            header_lines.append(line)
        elif line.strip().startswith('Format:'):
            fmt_line = line.strip()
    return header_lines, fmt_line

def process_directory(dir_path, output_dir=None, recursive=False, keep_temp=False):
    """Process all MKV files in a directory"""
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        print(f"✗ Directory not found: {dir_path}")
        return False
    
    pattern = '**/*.mkv' if recursive else '*.mkv'
    mkv_files = list(Path(dir_path).glob(pattern))
    
    if not mkv_files:
        print(f"✗ No MKV files found in: {dir_path}")
        return False
    
    print(f"Found {len(mkv_files)} MKV file(s) in: {dir_path}")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for mkv_file in sorted(mkv_files):
        mkv_path = str(mkv_file)
        
        # Determine output path
        if output_dir:
            rel_path = os.path.relpath(mkv_path, dir_path)
            out_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
        else:
            out_path = None  # None = replace source file in-place
        
        try:
            result = process_single_file(mkv_path, out_path, keep_temp)
            if result:
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            fail_count += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Summary: {success_count} succeeded, {skip_count} skipped, {fail_count} failed")
    
    return fail_count == 0

def main():
    parser = argparse.ArgumentParser(
        description='MKV Bilingual Subtitle Merger - Merge Chinese & English subtitles (EN on top, CN below)')
    parser.add_argument('input', help='Input MKV file or directory')
    parser.add_argument('-o', '--output', help='Output MKV file or directory (default: input_bilingual.mkv)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively search directories')
    parser.add_argument('--keep-temp', action='store_true', help='Keep extracted temp subtitle files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without doing it')
    
    args = parser.parse_args()
    
    # Check dependencies
    for cmd in ['mkvmerge', 'mkvextract']:
        if not shutil.which(cmd):
            print(f"✗ Required tool not found: {cmd}")
            print(f"  Install with: brew install mkvtoolnix")
            sys.exit(1)
    
    input_path = args.input
    
    if args.dry_run:
        if os.path.isdir(input_path):
            pattern = '**/*.mkv' if args.recursive else '*.mkv'
            files = list(Path(input_path).glob(pattern))
            print(f"Would process {len(files)} MKV file(s):")
            for f in sorted(files):
                tracks = get_subtitle_tracks(str(f))
                cn = find_subtitle_tracks(tracks, 'chi')
                en = find_subtitle_tracks(tracks, 'eng')
                status = '✓' if (cn and en) else '✗'
                print(f"  {status} {f.name} ({len(cn)} CN, {len(en)} EN tracks)")
        else:
            tracks = get_subtitle_tracks(input_path)
            cn = find_subtitle_tracks(tracks, 'chi')
            en = find_subtitle_tracks(tracks, 'eng')
            print(f"Subtitle tracks: {len(tracks)} total, {len(cn)} CN, {len(en)} EN")
        return
    
    if os.path.isdir(input_path):
        process_directory(input_path, args.output, args.recursive, args.keep_temp)
    elif os.path.isfile(input_path):
        result = process_single_file(input_path, args.output, args.keep_temp)
        sys.exit(0 if result else 1)
    else:
        print(f"✗ Path not found: {input_path}")
        sys.exit(1)

if __name__ == '__main__':
    main()

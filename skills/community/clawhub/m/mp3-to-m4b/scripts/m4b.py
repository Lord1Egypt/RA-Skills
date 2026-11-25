#!/usr/bin/env python3
# printf-style formats are kept on purpose: '%d' prints a float duration as a whole number, where format's ':d'
# would raise, and the script stays readable on Python 3.8.
# ruff: noqa: UP031
"""Join audio files into one .m4b audiobook with chapters, cover and tags.

  m4b.py plan  FOLDER                 show parts in order, chapters, cover, settings
  m4b.py build FOLDER -o OUT.m4b [options]
  m4b.py check OUT.m4b [--parts N]    read the result back and report problems

Needs ffmpeg and ffprobe on PATH. Python 3.8+, standard library only.
Exit codes: 0 ok, 1 problem found by check, 2 bad arguments or input,
3 ffmpeg/ffprobe missing, 4 ffmpeg failed.
"""
# ffmpeg and ffprobe run by name from PATH, each with a fixed argument list and no shell; the only variable
# parts are the paths of the person's own files (bandit B404, B603, B607 below).
import argparse
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
import tempfile

AUDIO = ('.mp3', '.m4a', '.m4b', '.aac', '.ogg', '.opus', '.flac', '.wav', '.wma', '.aif', '.aiff')
COVERS = ('cover', 'folder', 'front', 'album')


def die(msg, code=2):
    print('error: ' + msg, file=sys.stderr)
    sys.exit(code)


def need_tools():
    for t in ('ffmpeg', 'ffprobe'):
        if not shutil.which(t):
            die(t + ' not found. Install ffmpeg (macOS: brew install ffmpeg; Windows: winget install ffmpeg; '
                'Linux: the ffmpeg package), then run again.', 3)


def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams',  # nosec B603 B607
                        '-show_chapters', path], capture_output=True, text=True, check=False)
    if r.returncode:
        die('ffprobe cannot read ' + path + ': ' + r.stderr.strip()[:200])
    return json.loads(r.stdout)


def tags_of(d):
    t = {k.lower(): v for k, v in d.get('format', {}).get('tags', {}).items()}
    for s in d.get('streams', []):
        for k, v in s.get('tags', {}).items():
            t.setdefault(k.lower(), v)
    return t


def tracknum(t):
    m = re.match(r'\s*(\d+)', t.get('track', ''))
    return int(m.group(1)) if m else None


def clean_title(s):
    s = re.sub(r'\.[A-Za-z0-9]{2,4}$', '', s)
    s = re.sub(r'[_]+', ' ', s)
    s = re.sub(r'^\s*\d{1,4}\s*[-.:)]?\s*', '', s)  # leading track number
    return re.sub(r'\s+', ' ', s).strip(' -.')


SEPS = {'-', '–', '—', ':', '|', '/'}


def strip_common(titles):
    """Remove a part every title shares at the start or end ('Moby Dick - ', ' - Herman Melville'),
    cut only at a separator, so 'Chapter 1' keeps its word."""
    if len(titles) < 2:
        return titles
    w = [t.split(' ') for t in titles]
    pre = 0
    while all(len(x) > pre + 1 for x in w) and len({x[pre] for x in w}) == 1:
        pre += 1
    cut = max([i + 1 for i in range(pre) if w[0][i] in SEPS] or [0])
    suf = 0
    while all(len(x) > cut + suf + 1 for x in w) and len({x[-1 - suf] for x in w}) == 1:
        suf += 1
    tail = max([i + 1 for i in range(suf) if w[0][-1 - i] in SEPS] or [0])
    out = [' '.join(x[cut:len(x) - tail]).strip(' -.') for x in w]
    return out if all(out) else titles


def side_is_silent(path, ch):
    """True when a 'stereo' file carries the same sound in both channels (L-R far below L+R)."""
    if ch != 2:
        return False
    def level(expr):
        r = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-t', '300', '-i', path, '-af',  # nosec B603 B607
                            'pan=mono|c0=' + expr + ',volumedetect', '-f', 'null', '-'],
                           capture_output=True, text=True, check=False)
        m = re.search(r'mean_volume: (-?[\d.]+|-inf) dB', r.stderr)
        return -200.0 if not m or m.group(1) == '-inf' else float(m.group(1))
    return level('0.5*c0-0.5*c1') < level('0.5*c0+0.5*c1') - 30


def scan(folder, order):
    if not os.path.isdir(folder):
        die('not a folder: ' + folder)
    names = [n for n in os.listdir(folder) if n.lower().endswith(AUDIO) and not n.startswith('.')]
    if not names:
        die('no audio files in ' + folder + ' (looked for ' + ' '.join(AUDIO) + ')')
    parts = []
    for n in names:
        p = os.path.join(folder, n)
        d = probe(p)
        a = next((s for s in d.get('streams', []) if s.get('codec_type') == 'audio'), None)
        if not a:
            die('no audio stream in ' + n)
        t = tags_of(d)
        art = any(s.get('disposition', {}).get('attached_pic') for s in d['streams'])
        parts.append({'file': p, 'name': n, 'seconds': float(d['format'].get('duration', 0)),
                      'rate': int(a.get('sample_rate', 0)), 'channels': int(a.get('channels', 0)),
                      'kbps': round(int(a.get('bit_rate') or d['format'].get('bit_rate') or 0) / 1000),
                      'codec': a.get('codec_name'), 'tags': t, 'track': tracknum(t), 'art': art,
                      'inner_chapters': len(d.get('chapters', []))})
    by_name = sorted(parts, key=lambda x: natkey(x['name']))
    tr = [x['track'] for x in parts]
    tags_usable = None not in tr and len(set(tr)) == len(tr)
    by_tag = sorted(parts, key=lambda x: (x['track'], natkey(x['name']))) if tags_usable else None
    warn = []
    if order == 'tags':
        if not tags_usable:
            die('--order tags: not every file has its own track number; use --order names')
        parts = by_tag
    else:
        parts = by_name
        if by_tag and [x['name'] for x in by_tag] != [x['name'] for x in by_name]:
            warn.append('file names and track numbers give different orders; shown by names. '
                        'Compare with --order tags and pick the one that matches the book.')
    return parts, warn


def default_titles(parts):
    tt = [p['tags'].get('title', '').strip() for p in parts]
    if all(tt) and len(set(tt)) == len(tt):
        titles = [clean_title(t) or t for t in tt]
    else:
        titles = [clean_title(p['name']) for p in parts]
    titles = strip_common(titles)
    if len(set(titles)) < len(titles) or not all(titles):
        titles = ['Chapter %d' % (i + 1) for i in range(len(parts))]
    return titles


def read_chapters(path, parts):
    """Lines 'PART Title' or 'PART+SECONDS Title' (PART counts from 1). A part without a line
    continues the chapter before it. Plain lines without a number: one title per part, in order."""
    with open(path, encoding='utf-8-sig') as f:
        lines = [l.rstrip('\n') for l in f if l.strip()]
    out = []
    if all(re.match(r'\s*\d+(\+[\d.]+)?\s+\S', l) for l in lines):
        for l in lines:
            m = re.match(r'\s*(\d+)(?:\+([\d.]+))?\s+(.*\S)', l)
            k = int(m.group(1))
            if not 1 <= k <= len(parts):
                die('chapter line "%s": part %d does not exist (1..%d)' % (l, k, len(parts)))
            out.append((k - 1, float(m.group(2) or 0), m.group(3)))
    else:
        if len(lines) != len(parts):
            die('chapters file has %d lines for %d parts; give one title per part, or lines '
                '"PART Title" / "PART+SECONDS Title"' % (len(lines), len(parts)))
        out = [(i, 0.0, l.strip()) for i, l in enumerate(lines)]
    if out[0][:2] != (0, 0.0):
        die('the first chapter must start at part 1 (line "1 Title")')
    return out


def find_cover(folder, parts):
    imgs = [n for n in os.listdir(folder) if n.lower().endswith(('.jpg', '.jpeg', '.png')) and not n.startswith('.')]
    for key in COVERS:
        for n in sorted(imgs):
            if n.lower().startswith(key):
                return os.path.join(folder, n)
    if len(imgs) == 1:
        return os.path.join(folder, imgs[0])
    if imgs:
        big = max(imgs, key=lambda n: os.path.getsize(os.path.join(folder, n)))
        return os.path.join(folder, big)
    for p in parts:
        if p['art']:
            return p['file'] + '#embedded'
    return None


def settings(parts, mono_check=True):
    rates = [p['rate'] for p in parts]
    rate = max(set(rates), key=rates.count)
    ch = max(p['channels'] for p in parts)
    fake = False
    if ch == 2 and mono_check:
        fake = all(side_is_silent(p['file'], p['channels']) for p in parts[:3])
        if fake:
            ch = 1
    ch = min(ch, 2)
    src = max(p['kbps'] for p in parts) or 64
    kbps = min(src, 64 * ch)  # spoken word: 64k per channel is plenty; never above the source
    kbps = max(kbps, 32)
    return rate, ch, kbps, fake


def encoder():
    r = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True, check=False).stdout  # nosec B603 B607
    for e in ('aac_at', 'libfdk_aac'):
        if re.search(r'\s' + e + r'\s', r):
            return e
    return 'aac'


def hms(s):
    return '%d:%02d:%02d' % (s // 3600, s % 3600 // 60, s % 60)


def cmd_plan(a):
    need_tools()
    parts, warn = scan(a.folder, a.order)
    titles = default_titles(parts)
    rate, ch, kbps, fake = settings(parts)
    total = sum(p['seconds'] for p in parts)
    print('parts: %d, total %s' % (len(parts), hms(total)))
    for i, (p, t) in enumerate(zip(parts, titles), 1):
        extra = '  [has %d chapters inside]' % p['inner_chapters'] if p['inner_chapters'] > 1 else ''
        print('%3d  %s  %-40s <- %s%s' % (i, hms(p['seconds']), t[:40], p['name'], extra))
    t0 = parts[0]['tags']
    print('book title (album tag): {!r}, author (artist tag): {!r}'.format(t0.get('album', ''), t0.get('album_artist') or t0.get('artist', '')))
    print('cover: %s' % (find_cover(a.folder, parts) or 'none found'))
    print('audio out: AAC %d kbps, %d Hz, %s%s, encoder %s' % (kbps, rate, 'mono' if ch == 1 else 'stereo',
          ' (the stereo is the same in both channels)' if fake else '', encoder()))
    for w in warn:
        print('warning: ' + w)


def cmd_build(a):
    need_tools()
    out = os.path.abspath(a.output)
    if not out.lower().endswith('.m4b'):
        die('the output name must end in .m4b (Apple Books decides by the extension)')
    if os.path.exists(out) and not a.overwrite:
        die(out + ' exists; choose another name or pass --overwrite')
    parts, warn = scan(a.folder, a.order)
    for w in warn:
        print('warning: ' + w)
    rate, ch, kbps, _ = settings(parts, mono_check=a.channels is None)
    if a.channels:
        ch = a.channels
    if a.bitrate:
        kbps = a.bitrate
    if a.chapters:
        chaps = read_chapters(a.chapters, parts)
    elif a.one_chapter_per_file is False:
        chaps = [(0, 0.0, a.title or 'Chapter 1')]
    else:
        chaps = [(i, 0.0, t) for i, t in enumerate(default_titles(parts))]
    t0 = parts[0]['tags']
    a.title = a.title or t0.get('album') or None
    a.author = a.author or t0.get('album_artist') or t0.get('artist') or None
    cover = a.cover or find_cover(a.folder, parts)
    if a.no_cover:
        cover = None
    enc = encoder()
    work = tempfile.mkdtemp(prefix='m4b-', dir=os.path.dirname(out))
    try:
        audio = os.path.join(work, 'audio.m4a')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(rate), '-ac', str(ch), '-i', '-',
               '-c:a', enc, '-b:a', '%dk' % kbps, audio]
        encp = subprocess.Popen(cmd, stdin=subprocess.PIPE)  # nosec B603
        starts, total = [], 0
        print('encoding %d parts with %s, %d kbps %s %d Hz...' % (len(parts), enc, kbps,
              'mono' if ch == 1 else 'stereo', rate), flush=True)
        for p in parts:
            starts.append(total // (2 * ch))  # bytes of s16 PCM -> samples
            dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p['file'], '-map', '0:a:0', '-f', 's16le',  # nosec B603 B607
                                    '-ac', str(ch), '-ar', str(rate), '-'], stdout=subprocess.PIPE)
            while True:
                b = dec.stdout.read(1 << 20)
                if not b:
                    break
                encp.stdin.write(b)
                total += len(b)
            if dec.wait():
                encp.kill()
                die('ffmpeg could not decode ' + p['name'], 4)
            got = (total // (2 * ch) - starts[-1]) / rate
            if p['seconds'] and abs(got - p['seconds']) > max(2.0, 0.01 * p['seconds']):
                # a cut-off download or a broken header: the sound is shorter or longer than the file claims
                print('warning: {} plays {}, but its header says {}; the file may be incomplete'.format(p['name'], hms(got), hms(p['seconds'])))
        encp.stdin.close()
        if encp.wait():
            die('the AAC encoder failed', 4)
        total //= 2 * ch  # samples
        marks = []
        for k, off, t in chaps:
            if off and k + 1 < len(parts) and off * rate >= starts[k + 1] - starts[k]:
                die('chapter "%s": %.1f s is past the end of part %d' % (t, off, k + 1))
            marks.append((starts[k] + round(off * rate), t))
        if [m for m, _ in marks] != sorted(m for m, _ in marks):
            die('chapter starts are not in time order')
        meta = [';FFMETADATA1']
        tags = {'title': a.title, 'album': a.title, 'artist': a.author, 'album_artist': a.author,
                'composer': a.narrator, 'date': a.year, 'genre': a.genre, 'comment': a.comment}
        for k, v in tags.items():
            if v:
                meta.append(f'{k}={esc(v)}')
        for i, (m, t) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else total
            meta += ['[CHAPTER]', 'TIMEBASE=1/%d' % rate, 'START=%d' % m, 'END=%d' % end, 'title=' + esc(t)]
        mf = os.path.join(work, 'meta.txt')
        with open(mf, 'w', encoding='utf-8') as f:
            f.write('\n'.join(meta) + '\n')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', audio, '-i', mf]
        if cover:
            if cover.endswith('#embedded'):
                src = cover[:-9]
                cimg = os.path.join(work, 'cover.jpg')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-map', '0:v:0', '-frames:v', '1',  # nosec B603 B607
                                '-vf', "scale='min(1400,iw)':-2", cimg], check=True)
            else:
                cimg = os.path.join(work, 'cover.jpg')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cover, '-frames:v', '1', '-q:v', '2',  # nosec B603 B607
                                '-vf', "scale='min(1400,iw)':-2", cimg], check=True)
            cmd += ['-i', cimg, '-map', '0:a', '-map', '2:v', '-disposition:v:0', 'attached_pic']
        else:
            cmd += ['-map', '0:a']
        cmd += ['-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-metadata', 'media_type=2',
                # 1000 keeps the chapter track: with a cover, ffmpeg 9 otherwise drops it (issue 25317)
                '-movie_timescale', '1000', '-f', 'mp4', '-brand', 'M4B ', '-movflags', '+faststart', out]
        r = subprocess.run(cmd, capture_output=True, text=True, check=False)  # nosec B603
        if r.returncode:
            die('ffmpeg could not write the m4b: ' + r.stderr.strip()[-300:], 4)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print('wrote ' + out)
    print('chapters: %d, length %s, cover: %s' % (len(marks), hms(total / rate), 'yes' if cover else 'no'))
    for m, t in marks:
        print(f'  {hms(m / rate)}  {t}')


def esc(s):
    return re.sub(r'([=;#\\\n])', r'\\\1', s)


def cmd_check(a):
    need_tools()
    d = probe(a.file)
    f = d['format']
    st = d.get('streams', [])
    au = [s for s in st if s.get('codec_type') == 'audio']
    pic = [s for s in st if s.get('disposition', {}).get('attached_pic')]
    txt = [s for s in st if s.get('codec_type') in ('data', 'subtitle') and
           s.get('codec_tag_string') == 'text']
    ch = d.get('chapters', [])
    t = {k.lower(): v for k, v in f.get('tags', {}).items()}
    bad = []
    print('length %s, %d chapters, cover %s, audio %s %s Hz %s ch %s kbps, size %.1f MB' % (
        hms(float(f.get('duration', 0))), len(ch), 'yes' if pic else 'no',
        au[0].get('codec_name') if au else '-', au[0].get('sample_rate') if au else '-',
        au[0].get('channels') if au else '-', round(int(au[0].get('bit_rate', 0)) / 1000) if au else '-',
        int(f.get('size', 0)) / 1e6))
    print('brand {}, title {!r}, author {!r}, media_type {}'.format(t.get('major_brand'), t.get('title', ''),
          t.get('artist', ''), t.get('media_type', '-')))
    for c in ch:
        print('  {}  {}'.format(hms(float(c['start_time'])), c.get('tags', {}).get('title', '')))
    if not au:
        bad.append('no audio stream')
    if len(au) > 1:
        bad.append('more than one audio stream')
    if not ch:
        bad.append('no chapters')
    elif not txt:
        bad.append('no QuickTime chapter track: Apple Books and BookPlayer will show no chapters '
                   '(rebuild with -movie_timescale 1000, or without the cover)')
    if a.parts and len(ch) != a.parts:
        bad.append('%d chapters, expected %d' % (len(ch), a.parts))
    if len(ch) > 255:
        bad.append('more than 255 chapters: some players read only 255')
    if not a.file.lower().endswith('.m4b'):
        bad.append('the name does not end in .m4b')
    for b in bad:
        print('problem: ' + b)
    print('ok' if not bad else 'problems: %d' % len(bad))
    sys.exit(1 if bad else 0)


def main():
    ap = argparse.ArgumentParser(description='Join audio files into one .m4b audiobook.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan', help='show what build would do')
    p.add_argument('folder')
    p.add_argument('--order', choices=('names', 'tags'), default='names')
    b = sub.add_parser('build', help='make the .m4b')
    b.add_argument('folder')
    b.add_argument('-o', '--output', required=True, help='path of the .m4b to write')
    b.add_argument('--title'); b.add_argument('--author'); b.add_argument('--narrator')
    b.add_argument('--year'); b.add_argument('--comment')
    b.add_argument('--genre', default='Audiobook')
    b.add_argument('--cover', help='image file; default: cover/folder image in the folder, else art inside the files')
    b.add_argument('--no-cover', action='store_true')
    b.add_argument('--chapters', help='text file: one title per part, or lines "PART Title" / "PART+SECONDS Title"')
    b.add_argument('--single-chapter', dest='one_chapter_per_file', action='store_false',
                   help='no chapter per file: the whole book is one chapter')
    b.add_argument('--order', choices=('names', 'tags'), default='names')
    b.add_argument('--bitrate', type=int, help='AAC kbps (default: the source, at most 64 per channel)')
    b.add_argument('--channels', type=int, choices=(1, 2), help='default: mono when both channels are the same')
    b.add_argument('--overwrite', action='store_true')
    c = sub.add_parser('check', help='read an .m4b back and report problems')
    c.add_argument('file')
    c.add_argument('--parts', type=int, help='expected number of chapters')
    a = ap.parse_args()
    {'plan': cmd_plan, 'build': cmd_build, 'check': cmd_check}[a.cmd](a)


if __name__ == '__main__':
    main()

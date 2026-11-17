# -*- coding: utf-8 -*-
"""Vertical MIDI piano roll: time flows top->bottom, pitch left->right.

Usage: python render_vertical.py <file.mid> <out.png> [--bars N] [--mel T] [--acc T] [--start N]
"""
import sys
import mido
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES = NAMES

def extract(mid, idx):
    on = {}
    events = []
    t = 0
    for msg in mid.tracks[idx]:
        t += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            on.setdefault(msg.note, t)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in on:
                events.append((on.pop(msg.note), t, msg.note))
    events.sort()
    return events

def get_tempo(mid):
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return round(mido.tempo2bpm(msg.tempo))
    return 120

def main():
    args = sys.argv[1:]
    src = args[0]
    out = args[1]
    bars = 8
    bars_arg = None
    mel_idx = acc_idx = None
    start_bar = 0
    i = 2
    while i < len(args):
        if args[i] == '--bars':
            bars_arg = int(args[i + 1]); i += 2
        elif args[i] == '--mel':
            mel_idx = int(args[i + 1]); i += 2
        elif args[i] == '--acc':
            acc_idx = int(args[i + 1]); i += 2
        elif args[i] == '--start':
            start_bar = int(args[i + 1]); i += 2
        else:
            i += 1
    if bars_arg is not None:
        bars = bars_arg

    mid = mido.MidiFile(src)
    tpb = mid.ticks_per_beat
    bpm = get_tempo(mid)

    # auto-pick: melody = track with highest avg pitch (min 20 notes)
    if mel_idx is None:
        stats = []
        for idx, track in enumerate(mid.tracks):
            on = {}; t = 0; notes = []
            for msg in track:
                t += msg.time
                if msg.type == 'note_on' and msg.velocity > 0:
                    on.setdefault(msg.note, t)
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in on:
                        on.pop(msg.note)
                        notes.append(msg.note)
            if notes and len(notes) >= 20:
                stats.append((idx, len(notes), sum(notes) / len(notes)))
        if stats:
            mel_idx = max(stats, key=lambda s: s[2])[0]
            rest = [s for s in stats if s[0] != mel_idx]
            acc_idx = max(rest, key=lambda s: s[1])[0] if rest else None

    mel = extract(mid, mel_idx) if mel_idx is not None else []
    acc = extract(mid, acc_idx) if acc_idx is not None else []

    end_tick = (start_bar + (bars_arg if bars_arg is not None else 8)) * 4 * tpb
    skip_tick = start_bar * 4 * tpb
    shift = -skip_tick
    mel_all = [(s + shift, min(e, end_tick) + shift, n) for s, e, n in mel if skip_tick <= s < end_tick]
    acc_all = [(s + shift, min(e, end_tick) + shift, n) for s, e, n in acc if skip_tick <= s < end_tick]
    mel_vis, acc_vis = mel_all, acc_all
    if not mel_vis:
        mel_vis, acc_vis = acc_all, []
        print('WARNING: using acc as melody')

    # key detection (weighted profile, melody favoured)
    all_notes = mel + acc

    def key_detect():
        profile = defaultdict(float)
        for s, e, n in all_notes:
            s2 = s + shift
            if s2 >= end_tick or e + shift <= 0:
                continue
            profile[n % 12] += (e - s) * (1.0 if (s, e, n) in mel else 0.4)
        total = sum(profile.values()) or 1
        MAJ = (1.0, 0.15, 0.7, 0.2, 0.9, 0.4, 0.2, 0.9, 0.15, 0.7, 0.2, 0.5)
        MIN = (1.0, 0.15, 0.5, 0.9, 0.2, 0.7, 0.15, 0.7, 0.9, 0.2, 0.7, 0.15)
        best = None
        for r in range(12):
            for tpl, suf in ((MAJ, ''), (MIN, 'm')):
                score = sum(profile.get((r + i) % 12, 0) * w for i, w in enumerate(tpl)) / total
                if best is None or score > best[0]:
                    best = (score, NAMES[r] + suf)
        return best[1]

    key_name = key_detect()
    SHARP_KEYS = {'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7}
    FLAT_KEYS = {'F': 1, 'Bb': 2, 'Eb': 3, 'Ab': 4, 'Db': 5, 'Gb': 6, 'Cb': 7}
    minor_flat = {'Dm': 1, 'Gm': 2, 'Cm': 3, 'Fm': 4, 'Bbm': 5, 'Ebm': 6, 'Abm': 7}
    minor_sharp = {'Em': 1, 'Bm': 2, 'F#m': 3, 'C#m': 4, 'G#m': 5, 'D#m': 6, 'A#m': 7}
    if key_name in SHARP_KEYS:
        key_str = f'{key_name} ({"#" * SHARP_KEYS[key_name]})'
    elif key_name in FLAT_KEYS:
        key_str = f'{key_name} ({"b" * FLAT_KEYS[key_name]})'
    elif key_name in minor_flat:
        key_str = f'{key_name} ({"b" * minor_flat[key_name]})'
    elif key_name in minor_sharp:
        key_str = f'{key_name} ({"#" * minor_sharp[key_name]})'
    else:
        key_str = key_name

    # chord labels per bar
    def bar_chord(tick0, tick1):
        weight = defaultdict(float)
        for s, e, n in all_notes:
            s2 = s + shift
            if e + shift <= tick0 or s2 >= tick1:
                continue
            overlap = min(e + shift, tick1) - max(s2, tick0)
            weight[n % 12] += overlap * (1.0 if (s, e, n) in mel else 0.4)
        if not weight:
            return None
        total = sum(weight.values())
        best = None
        for r in range(12):
            for template, suffix in (((0, 4, 7), ''), ((0, 3, 7), 'm'), ((0, 4, 7, 10), '7'),
                                     ((0, 3, 7, 10), 'm7'), ((0, 4, 7, 11), 'maj7'),
                                     ((0, 5, 7), 'sus4'), ((0, 2, 7), 'sus2')):
                covered = sum(weight.get((r + iv) % 12, 0) for iv in template)
                non = total - covered
                final = covered / total - 0.5 * non / total
                if best is None or final > best[0]:
                    best = (final, r, suffix)
        if best and best[0] > 0.35:
            return NAMES[best[1]] + best[2]
        return None

    chord_labels = []
    for b in range(bars):
        tick0, tick1 = b * 4 * tpb, (b + 1) * 4 * tpb
        label = bar_chord(tick0, tick1)
        if label and chord_labels and label == chord_labels[-1][2]:
            chord_labels[-1] = (chord_labels[-1][0], tick1, label)
        elif label:
            chord_labels.append((tick0, tick1, label))

    # --- layout (vertical) ---
    COL_W = 52               # pixel width per semitone row (pitch axis, horizontal)
    lo = min(n for _, _, n in mel_vis) - 1
    hi = max(n for _, _, n in mel_vis) + 1
    n_rows = hi - lo + 1
    CHORD_W = 240            # left column for chord labels
    LEGEND_H = 240
    HEADER_H = 90
    TOP = HEADER_H
    W = CHORD_W + n_rows * COL_W + 20
    W = max(W, 1100)  # minimum canvas width: legend + metadata need room
    H_target = int(W * 4 / 3)

    # auto bars: never fewer than 4; BAR_H grows so the shortest note gets MIN_NOTE_PX
    MIN_NOTE_PX = 30
    durs = [e - s for s, e, n in mel_vis if e > s]
    if bars_arg is None:
        if durs:
            dmin = min(durs)
            req_bar_h = max(300, int(MIN_NOTE_PX * 4 * tpb / dmin))
            avail = H_target - TOP - LEGEND_H
            bars = max(4, min(8, avail // req_bar_h or 1))
            BAR_H = req_bar_h  # stretch the image taller if needed
            print(f'auto bars: {bars}, BAR_H={BAR_H} (shortest note {dmin} ticks)')
        else:
            bars = 8
            BAR_H = max(300, (H_target - TOP - LEGEND_H) // bars)
    else:
        BAR_H = max(300, (H_target - TOP - LEGEND_H) // bars)
    H = TOP + bars * BAR_H + LEGEND_H
    # trim visible notes to the selected bar count
    vis_end = bars * 4 * tpb
    mel_vis = [(s, min(e, vis_end), n) for s, e, n in mel_vis if s < vis_end]
    acc_vis = [(s, min(e, vis_end), n) for s, e, n in acc_vis if s < vis_end]

    img = Image.new('RGB', (W, H), (24, 26, 32))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('consola.ttf', 22)
        chord_font = ImageFont.truetype('consolab.ttf', 110)
        note_font = ImageFont.truetype('consolab.ttf', 34)
        bar_font = ImageFont.truetype('consolab.ttf', 66)
    except Exception:
        font = chord_font = note_font = bar_font = ImageFont.load_default()

    # --- row shading (vertical pitch lanes) ---
    for n in range(lo, hi + 1):
        x = CHORD_W + (n - lo) * COL_W
        if n % 12 in (1, 3, 6, 8, 10):
            d.rectangle([x, TOP, x + COL_W - 1, H - LEGEND_H], fill=(30, 32, 40))
        else:
            d.rectangle([x, TOP, x + COL_W - 1, H - LEGEND_H], fill=(48, 51, 60))
        if n % 12 == 0:
            d.line([(x, TOP), (x, H - LEGEND_H)], fill=(245, 247, 252), width=8)
            lbl = f'C{n // 12 - 1}'
            d.text((x + 8, TOP + 8), lbl, fill=(220, 224, 235), font=font)
        else:
            d.line([(x, TOP), (x, H - LEGEND_H)], fill=(16, 17, 22), width=4)

    # --- horizontal time grid (bars + beats) ---
    for b in range(bars + 1):
        y = TOP + b * BAR_H
        d.line([(CHORD_W, y), (W - 10, y)], fill=(150, 155, 170), width=6)
    for beat in range(bars * 4):
        y = TOP + beat * (BAR_H // 4)
        d.line([(CHORD_W, y), (W - 10, y)], fill=(62, 66, 78), width=2)

    # --- chord labels (left column, anchored at chord entry row) ---
        for s, e, label in chord_labels:
            y0 = TOP + s * BAR_H / (4 * tpb)
            y1 = max(y0 + 10, min(TOP + e * BAR_H / (4 * tpb), H - LEGEND_H - 4))
            d.rectangle([8, y0 + 4, CHORD_W - 8, y1 - 4], fill=(38, 42, 52), outline=(90, 97, 115))
            bbox = chord_font.getbbox(label)
            th = bbox[3] - bbox[1]
            ty = y0 + 24
            if ty + th > y1 - 10:
                ty = max(14, y1 - th - 10)
            # shrink chord font if wider than the left column
            cf = chord_font
            tw = d.textlength(label, font=cf)
            if tw > CHORD_W - 40:
                k = (CHORD_W - 48) / tw
                cf = ImageFont.truetype('consolab.ttf', max(30, int(110 * k)))
            d.text((24, ty), label, fill=(255, 214, 79), font=cf)

    # --- notes ---
    PALETTE = [
        (255, 107, 107), (255, 159, 64), (255, 214, 79), (171, 214, 79),
        (110, 231, 183), (77, 208, 225), (77, 171, 247), (129, 140, 248),
        (177, 151, 252), (247, 103, 180), (251, 114, 158), (255, 138, 128),
    ]

    def draw_notes(events, is_melody, label_notes=False):
        for s, e, n in events:
            if s >= vis_end:
                continue
            y0 = TOP + s * BAR_H / (4 * tpb)
            y1 = TOP + e * BAR_H / (4 * tpb)
            x = CHORD_W + (n - lo) * COL_W
            if is_melody:
                col, outline = PALETTE[n % 12], (255, 255, 255)
            else:
                col, outline = ((70, 110, 150) if n % 2 else (60, 95, 135)), (55, 60, 70)
            d.rectangle([x, y0, x + COL_W - 2, max(y0 + 3, y1 - 1)],
                        fill=col, outline=outline)
            if label_notes and is_melody:
                label = NOTE_NAMES[n % 12]
                lw = d.textlength(label, font=note_font)
                if y1 - y0 > 8:
                    fs = note_font
                    th = 34
                    if y1 - y0 < th + 6:
                        k = max(0.45, (y1 - y0 - 4) / (th + 6))
                        fs = ImageFont.truetype('consolab.ttf', max(16, int(34 * k)))
                        th = fs.size
                    d.text((x + (COL_W - lw) / 2, y0 + max(2, (y1 - y0 - th) / 2)), label,
                           fill=(20, 20, 24), font=fs)

    draw_notes(acc_vis, False)
    draw_notes(mel_vis, True, label_notes=True)

    # --- legend (bottom strip, sized to fit) ---
    LY0 = H - LEGEND_H + 78
    meta = f'{src} - {bars} bars (vertical) | Key: {key_str} | {bpm} BPM'
    mf_size = 66
    while mf_size >= 24:
        mf = ImageFont.truetype('consolab.ttf', mf_size)
        if d.textlength(meta, font=mf) <= W - 48:
            break
        mf_size -= 6
    d.text((24, LY0 - mf_size - 12), meta, fill=(220, 224, 235), font=mf)
    n_sw = 13
    gap = 6
    SW = min(150, (W - 40 - (n_sw - 1) * gap) // n_sw)
    SH_ = 96
    lf_size = max(40, int(SW * 0.62))
    legend_font = ImageFont.truetype('consolab.ttf', lf_size)
    for i2 in range(12):
        sx = 24 + i2 * (SW + gap)
        sy = LY0 + 30
        d.rectangle([sx, sy, sx + SW, sy + SH_], fill=PALETTE[i2], outline=(10, 10, 10))
        nm = NOTE_NAMES[i2]
        lw = d.textlength(nm, font=legend_font)
        bbox = legend_font.getbbox(nm)
        if lw > SW - 6:
            kf = (SW - 8) / lw
            f2 = ImageFont.truetype('consolab.ttf', max(18, int(lf_size * kf)))
            lw = d.textlength(nm, font=f2)
            bbox = f2.getbbox(nm)
            d.text((sx + (SW - lw) / 2, sy + (SH_ - (bbox[3] - bbox[1])) / 2 - bbox[1]), nm,
                   fill=(20, 20, 24), font=f2)
        else:
            d.text((sx + (SW - lw) / 2, sy + (SH_ - (bbox[3] - bbox[1])) / 2 - bbox[1]), nm,
                   fill=(20, 20, 24), font=legend_font)
    ax = 24 + 12 * (SW + gap)
    if ax + SW <= W - 8:
        d.rectangle([ax, LY0 + 30, ax + SW, LY0 + 30 + SH_], fill=(70, 110, 150), outline=(10, 10, 10))
        alw = d.textlength('acc', font=legend_font)
        abbox = legend_font.getbbox('acc')
        d.text((ax + (SW - alw) / 2, LY0 + 30 + (SH_ - (abbox[3] - abbox[1])) / 2 - abbox[1]), 'acc',
               fill=(220, 224, 235), font=legend_font)

    img.save(out)
    print('saved', out, img.size)

main()
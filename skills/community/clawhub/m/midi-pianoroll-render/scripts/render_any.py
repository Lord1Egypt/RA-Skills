# -*- coding: utf-8 -*-
"""Universal MIDI -> horizontal piano roll PNG renderer.

Usage: python render_any.py <file.mid> <out.png> [--bars N] [--mel T] [--acc T] [--start N]
Auto-detects melody/accompaniment tracks if not given.
"""
import sys
import mido
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES = NAMES

def extract(mid, idx):
    tpb = mid.ticks_per_beat
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
    mel_idx = acc_idx = None
    start_bar = 0
    i = 2
    while i < len(args):
        if args[i] == '--bars':
            bars = int(args[i + 1]); i += 2
        elif args[i] == '--mel':
            mel_idx = int(args[i + 1]); i += 2
        elif args[i] == '--acc':
            acc_idx = int(args[i + 1]); i += 2
        elif args[i] == '--start':
            start_bar = int(args[i + 1]); i += 2
        else:
            i += 1

    mid = mido.MidiFile(src)
    tpb = mid.ticks_per_beat
    bpm = get_tempo(mid)

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
    print(f'tracks: melody={mel_idx}, acc={acc_idx}, bpm={bpm}, tpb={tpb}')
    mel = extract(mid, mel_idx) if mel_idx is not None else []
    acc = extract(mid, acc_idx) if acc_idx is not None else []

    end_tick = (start_bar + bars) * 4 * tpb
    skip_tick = start_bar * 4 * tpb
    shift = -skip_tick
    mel_vis = [(s + shift, min(e, end_tick) + shift, n) for s, e, n in mel if skip_tick <= s < end_tick]
    acc_vis = [(s + shift, min(e, end_tick) + shift, n) for s, e, n in acc if skip_tick <= s < end_tick]
    if not mel_vis:
        mel_vis = [(s + shift, min(e, end_tick) + shift, n) for s, e, n in acc if skip_tick <= s < end_tick]
        acc_vis = []
        print('WARNING: using accompaniment track as melody (no melodic track found)')

    # chord labels per bar (weighted pcs, melody favoured)
    all_notes = mel + acc

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

    def key_detect(notes, endt, melset):
        profile = defaultdict(float)
        for s, e, n in notes:
            s2 = s + shift
            if s2 >= endt or e + shift <= 0:
                continue
            profile[n % 12] += (e - s) * (1.0 if (s, e, n) in melset else 0.4)
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

    key_name = key_detect(all_notes, end_tick, mel)
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

    # --- layout ---
    BAR_W = 520
    W = bars * BAR_W + 80
    if not mel_vis:
        mel_vis = acc_vis
    lo = min(n for _, _, n in mel_vis) - 1
    hi = max(n for _, _, n in mel_vis) + 1
    CHORD_ZONE = 230
    LEGEND_H = 240
    TOP = CHORD_ZONE + 20
    H_target = int(W * 3 / 4)
    ROW_H = max(40, (H_target - TOP - LEGEND_H) // max(1, hi - lo + 1))
    H = TOP + (hi - lo + 1) * ROW_H + LEGEND_H
    img = Image.new('RGB', (W, H), (24, 26, 32))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('consola.ttf', 22)
        chord_font = ImageFont.truetype('consolab.ttf', 150)
        note_font = ImageFont.truetype('consolab.ttf', 56)
        bar_font = ImageFont.truetype('consolab.ttf', 66)
    except Exception:
        font = chord_font = note_font = bar_font = ImageFont.load_default()

    # --- chord labels (anchored at chord entry) ---
    for s, e, label in chord_labels:
        x0 = 80 + s * (BAR_W / 4) / tpb
        x1 = 80 + e * (BAR_W / 4) / tpb
        d.rectangle([x0 + 4, 14, x1 - 4, CHORD_ZONE - 8], fill=(38, 42, 52), outline=(90, 97, 115))
        bbox = chord_font.getbbox(label)
        d.text((x0 + 24, CHORD_ZONE - 8 - (bbox[3] - bbox[1]) - 14), label,
               fill=(255, 214, 79), font=chord_font)

    # --- row shading + horizontal lines ---
    for n in range(lo, hi + 1):
        y = TOP + (hi - n) * ROW_H
        if n % 12 in (1, 3, 6, 8, 10):
            d.rectangle([80, y, W - 10, y + ROW_H - 1], fill=(30, 32, 40))
        else:
            d.rectangle([80, y, W - 10, y + ROW_H - 1], fill=(48, 51, 60))
        if n % 12 == 0:
            d.line([(80, y), (W - 10, y)], fill=(245, 247, 252), width=8)
            d.text((18, y + ROW_H // 2 - 14), f'C{n // 12 - 1}', fill=(200, 205, 215), font=font)
        else:
            d.line([(80, y), (W - 10, y)], fill=(16, 17, 22), width=4)

    # --- vertical grid over shading ---
    for b in range(bars + 1):
        x = 80 + b * BAR_W
        d.line([(x, TOP), (x, H - LEGEND_H)], fill=(150, 155, 170), width=6)
    for beat in range(bars * 4):
        x = 80 + beat * (BAR_W // 4)
        d.line([(x, TOP), (x, H - LEGEND_H)], fill=(62, 66, 78), width=2)

    # --- notes ---
    PALETTE = [
        (255, 107, 107), (255, 159, 64), (255, 214, 79), (171, 214, 79),
        (110, 231, 183), (77, 208, 225), (77, 171, 247), (129, 140, 248),
        (177, 151, 252), (247, 103, 180), (251, 114, 158), (255, 138, 128),
    ]

    def draw_notes(events, is_melody, label_notes=False):
        for s, e, n in events:
            if s >= end_tick + shift:
                continue
            x0 = 80 + s * (BAR_W / 4) / tpb
            x1 = 80 + e * (BAR_W / 4) / tpb
            y = TOP + (hi - n) * ROW_H
            if is_melody:
                col, outline = PALETTE[n % 12], (255, 255, 255)
            else:
                col, outline = ((70, 110, 150) if n % 2 else (60, 95, 135)), (55, 60, 70)
            d.rectangle([x0, y, max(x0 + 3, x1 - 1), y + ROW_H - 2],
                        fill=col, outline=outline)
            if label_notes and is_melody:
                label = NOTE_NAMES[n % 12]
                lw = d.textlength(label, font=note_font)
                if x1 - x0 > 8:
                    fs = note_font
                    if x1 - x0 < lw + 6:
                        k = max(0.45, (x1 - x0 - 4) / (lw + 6))
                        fs = ImageFont.truetype('consolab.ttf', max(20, int(56 * k)))
                        lw = d.textlength(label, font=fs)
                    d.text(((x0 + x1 - lw) / 2, y + (ROW_H - fs.size) // 2), label,
                           fill=(20, 20, 24), font=fs)

    draw_notes(acc_vis, False)
    draw_notes(mel_vis, True, label_notes=True)

    # --- legend (bottom strip, sized to fit) ---
    LY0 = H - LEGEND_H + 78
    meta = f'{src} - first {bars} bars | Key: {key_str} | {bpm} BPM'
    mf_size = 66
    while mf_size > 24:
        mf = ImageFont.truetype('consolab.ttf', mf_size)
        if d.textlength(meta, font=mf) <= W - 48:
            break
        mf_size -= 6
    d.text((80, LY0 - mf_size - 12), meta, fill=(220, 224, 235), font=mf)
    n_sw = 13
    gap = 6
    SW = min(150, (W - 40 - (n_sw - 1) * gap) // n_sw)
    SH_ = 96
    lf_size = max(40, int(SW * 0.62))
    legend_font = ImageFont.truetype('consolab.ttf', lf_size)
    for i2 in range(12):
        sx = 80 + i2 * (SW + gap)
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
    ax = 80 + 12 * (SW + gap)
    if ax + SW <= W - 8:
        d.rectangle([ax, LY0 + 30, ax + SW, LY0 + 30 + SH_], fill=(70, 110, 150), outline=(10, 10, 10))
        alw = d.textlength('acc', font=legend_font)
        abbox = legend_font.getbbox('acc')
        d.text((ax + (SW - alw) / 2, LY0 + 30 + (SH_ - (abbox[3] - abbox[1])) / 2 - abbox[1]), 'acc',
               fill=(220, 224, 235), font=legend_font)

    img.save(out)
    print('saved', out, img.size)

main()
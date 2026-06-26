#!/usr/bin/env python3
"""
Poker Video Clipper v3 - Hand-boundary detection.
Logic: detect complete poker hands (deal->result), score by excitement, output top N.
"""
import json, re, subprocess, sys
from pathlib import Path

WORKDIR  = Path(__file__).parent.parent.parent  # dynamic: skills/pokerclip/scripts -> workspace
DOWNLOADS = WORKDIR / "downloads"
OUT = WORKDIR / "clips"
OUT.mkdir(exist_ok=True)

WHISPER_MODEL = "base"
TARGET = 5          # number of top hands to output
MIN_HAND_S = 30     # minimum hand duration
MAX_HAND_S = 300    # maximum hand duration

# Canvas
CW, CH = 1080, 1920
VH = 607
VY = (CH - VH) // 2
SUB_Y = VY + VH + 120
HOOK_Y = VY // 2

# ── Hand boundary signals ────────────────────────────────────────────────────
# A new hand starts when we see dealing/blinds/new action after a completed hand
HAND_START_SIGNALS = [
    'raises', 'raises to', 'bets', 'calls', 'folds', 'checks',
    'flop', 'pre-flop', 'preflop', 'blind', 'dealer',
    'dealt', 'look down', 'looks down', 'pocket',
]
# A hand ends when result is revealed
HAND_END_SIGNALS = [
    # Pot awarded — definitive
    'well done', 'ship it', 'takes the pot', 'takes it down', 'scoops',
    'wins the pot', 'wins the hand', 'wins a monster', 'wins a massive',
    'going to win a pot', 'win a pot worth', 'locked up a',
    'good call', 'good fold', 'nice hand', 'well played',
    'eliminated', 'busted out', 'knocked out',
    'mucks', 'pot goes to',
    'that shuts me up', 'shut me up',
    'two thirds of the way to scooping',
    # Player reaction after result
    'what a hand', 'incredible hand',
]

# Excitement keywords for scoring hands
KW = {
    'all in':10,'all-in':10,'allin':10,'bad beat':10,'cooler':8,
    'bluff':9,'bluffing':9,'bluffed':9,'hero call':10,'sick call':10,
    'incredible':7,'unbelievable':8,'insane':8,'crazy':6,
    'oh my god':9,'oh my':6,'wow':5,'shoves':8,'jams':8,
    'raises':3,'reraise':6,'three-bet':6,'4bet':7,
    'river':6,'turn':4,'million':7,'massive pot':8,'huge pot':8,
    'cannot believe':8,'unreal':7,'monster':6,
    'eliminated':7,'busted':6,'showdown':7,
    'wins the pot':8,'takes it down':7,
}

# ── Step 1: Transcribe ───────────────────────────────────────────────────────
def transcribe(vp):
    print(f"\n[1/3] Whisper ({WHISPER_MODEL}) transcribing...")
    import whisper
    m = whisper.load_model(WHISPER_MODEL)
    r = m.transcribe(str(vp), language="en", verbose=False)
    segs = [{"start":round(s["start"],2),"end":round(s["end"],2),"text":s["text"].strip()} for s in r["segments"]]
    p = OUT / f"{vp.stem}_transcript.json"
    p.write_text(json.dumps(segs,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"      {len(segs)} segments, {segs[-1]['end']/60:.1f} min")
    return segs

# ── Step 2: Detect hand boundaries ──────────────────────────────────────────

# Street signals — appear WITHIN a hand
STREET_SIGNALS = {
    'preflop': ['pocket','hole card','look down','looks down','dealt','under the gun',
                'big blind','small blind','straddle','raises to','opens to','limps',
                'before the flop','pre-flop','preflop','folds around'],
    'flop':   ['the flop','flop comes','flop is','on the flop','flopped'],
    'turn':   ['the turn','turn card','on the turn','to the turn','turn is','ace on the turn'],
    'river':  ['the river','river card','on the river','to the river','river is','river, '],
}

# Result signals — hand is OVER
HAND_END_SIGNALS = [
    'wins the pot','wins the hand','takes the pot','takes it down','scoops','ship it',
    'well done','nice hand','good hand','eliminated','busted','knocked out','mucks',
    'it is good',"it's good",'win a pot worth','going to win a pot','raked in','rakes in',
    'locked up','two thirds of the way to scooping','shuts me up','shut me up',
    'wins a monster','wins a massive',
    "ronnie's folded",'going to the cage','folded his hand','folds his hand',
    "he's folded","she's folded",'and he folds','and she folds',
    'phil deserved that','show some class','you lose the whole lot',
    'round one goes to','locked up at least',
]

def detect_street(text):
    tl = text.lower()
    for street, signals in STREET_SIGNALS.items():
        if any(s in tl for s in signals): return street
    return None

def detect_result(text):
    return any(s in text.lower() for s in HAND_END_SIGNALS)

def score_hand(segs, s0, e0):
    """Score a hand by excitement keyword density."""
    text = ' '.join(s['text'] for s in segs if s0 <= s['start'] <= e0).lower()
    sc = 0
    for kw, w in KW.items():
        if kw in text: sc += w
    sc += text.count('!') * 2
    # Penalty for very long hands (prefer punchy ones)
    dur = e0 - s0
    return round(sc * min(1.0, 150 / max(dur, 1)), 2)

def detect_hands(segs):
    """
    Detect complete poker hands using street sequence + result signals.
    A hand ends at a result signal. The next hand starts right after.
    Returns list of {start, end, score, text}
    """
    hands = []
    current_start = 0.0
    current_streets = set()

    # Build event timeline
    events = []
    for seg in segs:
        street = detect_street(seg['text'])
        result = detect_result(seg['text'])
        if street or result:
            events.append({'time': seg['start'], 'end': seg['end'],
                           'text': seg['text'], 'street': street, 'result': result})

    # Merge result events within 20s of each other (same hand ending)
    merged_events = []
    for e in events:
        if merged_events and e['result'] and merged_events[-1]['result'] and \
           e['time'] - merged_events[-1]['time'] < 20:
            merged_events[-1] = e  # keep latest
        else:
            merged_events.append(e)

    for e in merged_events:
        if e['street']:
            current_streets.add(e['street'])
        if e['result']:
            hand_end = e['end'] + 2
            dur = hand_end - current_start
            if dur >= MIN_HAND_S:
                sc = score_hand(segs, current_start, hand_end)
                text = ' '.join(s['text'] for s in segs if current_start <= s['start'] <= hand_end)
                hands.append({
                    'start': round(current_start, 1),
                    'end': round(hand_end, 1),
                    'score': sc,
                    'text': text,
                    'duration': round(dur, 1),
                    'streets': list(current_streets),
                })
            current_start = hand_end
            current_streets = set()

    # Handle trailing hand with no result
    if segs[-1]['end'] - current_start >= MIN_HAND_S and current_streets:
        sc = score_hand(segs, current_start, segs[-1]['end'])
        text = ' '.join(s['text'] for s in segs if current_start <= s['start'])
        hands.append({
            'start': round(current_start, 1),
            'end': round(segs[-1]['end'], 1),
            'score': sc, 'text': text,
            'duration': round(segs[-1]['end'] - current_start, 1),
            'streets': list(current_streets),
        })
        prev_end = hand_end_time + 1  # next hand starts after this one

    print(f"      Detected {len(hands)} complete hands")
    for h in hands:
        print(f"      {h['start']:.0f}s-{h['end']:.0f}s ({h['duration']:.0f}s) score={h['score']}")
    return hands

def select_top_hands(hands, segs):
    """Select top N hands by score, build clip objects."""
    if not hands:
        return []

    sorted_hands = sorted(hands, key=lambda h: h['score'], reverse=True)
    top = sorted_hands[:TARGET]
    top.sort(key=lambda h: h['start'])  # re-sort by time

    clips = []
    for i, h in enumerate(top):
        tl = h['text'].lower()
        # Generate title
        TITLE_MAP = [
            ('all in', 'INSANE All-In Moment You Wont Believe'),
            ('bluff', 'Massive Bluff Caught on the River'),
            ('bad beat', 'Brutal Bad Beat - Poker at its Cruelest'),
            ('hero call', 'Hero Call for All the Chips'),
            ('million', 'Million Dollar Poker Decision'),
            ('eliminated', 'Dramatic Elimination Hand'),
            ('river', 'River Card Changes Everything'),
            ('incredible', 'Incredible Poker Hand You Must See'),
            ('insane', 'Insane Poker Moment'),
        ]
        title = next((t for kw, t in TITLE_MAP if kw in tl), f'Epic Poker Hand {i+1}')
        clips.append({
            'clip_number': i + 1,
            'start_seconds': h['start'],
            'end_seconds': h['end'],
            'peak_score': h['score'],
            'title': title,
            'hook': '',
            'hook_v2': '',
            'yt_title': '',
            'emotional_arc': '',
            'why': f"Complete hand, score={h['score']}",
        })
    return clips

def analyze(segs):
    print("\n[2/3] Detecting complete hands...")
    hands = detect_hands(segs)
    clips = select_top_hands(hands, segs)
    if not clips:
        print("      WARNING: Hand detection failed, no clips generated")
        return []
    (OUT / 'clips_analysis.json').write_text(json.dumps(clips, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"      Top {len(clips)} hands selected:")
    for c in clips:
        print(f"      [{c['clip_number']}] {c['title']} ({c['end_seconds']-c['start_seconds']:.0f}s, score={c['peak_score']})")
    return clips

# ── ASS subtitle + hook builder ──────────────────────────────────────────────
def ass_time(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); cs=int(round((t%1)*100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def wrap(text, mx=18):
    words=text.strip().split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+(1 if cur else 0)<=mx: cur=(cur+" "+w).strip()
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return "\\N".join(lines[:2])

def build_ass(segs, s0, dur, num, hook_text):
    ap = OUT / f"clip_{num:02d}.ass"
    style_sub  = "Sub,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1"
    style_hook = "Hook,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,3,0,5,0,0,0,1"
    hdr = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {CW}\nPlayResY: {CH}\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: {style_sub}\nStyle: {style_hook}\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events = []
    if hook_text:
        hw = wrap(hook_text, mx=22)
        hp = '{\\pos(' + str(CW//2) + ',' + str(HOOK_Y) + ')}'
        events.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(3.0,dur))},Hook,,0,0,0,,{hp}{hw}")
    for seg in segs:
        if seg['end'] < s0 or seg['start'] > s0+dur: continue
        ts = max(0, seg['start']-s0); te = min(dur, seg['end']-s0)
        if te <= ts: continue
        sp = '{\\pos(' + str(CW//2) + ',' + str(SUB_Y) + ')}'
        events.append(f"Dialogue: 0,{ass_time(ts)},{ass_time(te)},Sub,,0,0,0,,{sp}{wrap(seg['text'])}")
    ap.write_text(hdr + "\n".join(events) + "\n", encoding='utf-8')
    return ap

# ── Step 3: Extract clips ────────────────────────────────────────────────────
def extract(vp, clips, segs):
    print(f"\n[3/3] Cutting {len(clips)} clips -> {CW}x{CH} letterbox + ASS subtitles...")
    done = []
    for clip in clips:
        s0 = clip['start_seconds']
        e0 = clip['end_seconds']
        dur = e0 - s0
        slug = re.sub(r'[^\w\s-]', '', clip['title'])[:55].strip()
        mp4 = OUT / f"clip_{clip['clip_number']:02d}_{slug}.mp4"
        hook = clip.get('hook_v2') or clip.get('hook', '')
        ass = build_ass(segs, s0, dur, clip['clip_number'], hook)
        ass_esc = str(ass).replace('\\', '/').replace(':', '\\:')
        vf = (
            f"[0:v]scale={CW}:-2[sc];"
            f"[sc]pad={CW}:{CH}:(ow-iw)/2:(oh-ih)/2:black[pad];"
            f"[pad]ass='{ass_esc}'"
        )
        cmd = ['ffmpeg','-y','-ss',str(s0),'-i',str(vp),'-t',str(dur),
               '-filter_complex',vf,'-s',f'{CW}x{CH}',
               '-c:v','libx264','-crf','23','-preset','fast',
               '-c:a','aac','-b:a','128k',str(mp4)]
        print(f"      [{clip['clip_number']}] {mp4.name}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f'      [WARN] {r.stderr[-200:]}')
        else:
            done.append(str(mp4))
            print(f'      OK ({dur:.0f}s)')
    return done


def main():
    if len(sys.argv) > 1:
        vp = Path(sys.argv[1])
    else:
        mp4s = [f for f in DOWNLOADS.glob('*.mp4') if 'reference' not in f.name]
        if not mp4s: print('No MP4 in downloads/'); sys.exit(1)
        vp = max(mp4s, key=lambda p: p.stat().st_mtime)
    if not vp.exists(): print(f'Not found: {vp}'); sys.exit(1)
    SEP = '='*60
    print(f'\n{SEP}\n Poker Clipper v3 - Hand Boundary Detection\n Video: {vp.name}\n{SEP}')
    tp = OUT / f'{vp.stem}_transcript.json'
    if tp.exists():
        print(f'\n[1/3] Cached transcript: {tp.name}')
        segs = json.loads(tp.read_text(encoding='utf-8'))
    else:
        segs = transcribe(vp)
    clips = analyze(segs)
    if not clips:
        sys.exit(1)
    # Load hooks if available
    analysis = json.loads((OUT / 'clips_analysis.json').read_text(encoding='utf-8'))
    for c in clips:
        match = next((a for a in analysis if a['clip_number'] == c['clip_number']), None)
        if match:
            c['hook_v2'] = match.get('hook_v2', '')
    files = extract(vp, clips, segs)
    SEP2 = '='*60
    print(f'\n{SEP2}\n Done! {len(files)}/{len(clips)} clips in {OUT}\n{SEP2}')
    for c in clips:
        slug = re.sub(r"[^\w\s-]", "", c["title"])[:55].strip()
        print(f"  [{c['clip_number']}] {c['title']} ({c['end_seconds']-c['start_seconds']:.0f}s)")
        if c.get('hook_v2'): print(f"      Hook: {c['hook_v2']}")


if __name__ == '__main__':
    main()

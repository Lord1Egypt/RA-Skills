#!/usr/bin/env python3
"""
Generate high-retention hooks for poker clips.
Guarantees: every clip gets a UNIQUE hook.
"""
import json, re
from pathlib import Path

OUT = Path(__file__).parent.parent.parent / 'clips'  # dynamic

transcripts = [f for f in OUT.glob('*_transcript.json') if 'reference' not in f.name]
segs = json.loads(transcripts[0].read_text(encoding='utf-8'))
clips = json.loads((OUT / 'clips_analysis.json').read_text(encoding='utf-8'))

def get_clip_text(c):
    s0, e0 = c['start_seconds'], c['end_seconds']
    return ' '.join(s['text'] for s in segs if s0 <= s['start'] <= e0)

def extract_amount(text):
    patterns = [
        r'(\d{1,3}(?:,\d{3})+)',
        r'(\d+)\s*grand',
        r'(\d+)\s*thousand',
        r'(\d+)\s*million',
    ]
    found = []
    for p in patterns:
        for m in re.finditer(p, text, re.IGNORECASE):
            raw = m.group(1).replace(',', '')
            if raw.isdigit():
                v = int(raw)
                if v > 100:  # ignore small numbers
                    found.append(v)
    if not found: return None
    best = max(found)
    if best >= 1000000: return f"${best//1000000}M"
    if best >= 1000: return f"${best:,}"
    return f"${best}"

# Pool of hook formulas — each uses a different angle
# Key: formula name, Value: function(text, amount) -> hook string or None
def formula_suspense_gap(text, amount):
    """Suspense: hide the outcome"""
    tl = text.lower()
    if 'all in' in tl and 'call' in tl:
        return "He called the all-in. Nobody at the table could believe what happened next."
    if 'bluff' in tl and 'river' in tl:
        return "He fired the river as a bluff. His opponent had 30 seconds to decide."
    if 'all in' in tl:
        return "They got it all in. One of them was about to be eliminated."
    return None

def formula_counter_intuitive(text, amount):
    """Break expectations"""
    tl = text.lower()
    if 'fold' in tl and ('aces' in tl or 'kings' in tl or 'set' in tl):
        return "He flopped a set and folded. Here's why that was the right play."
    if 'bluff' in tl and 'call' in tl:
        return "She knew he was bluffing. She called anyway — and still almost lost."
    if 'raise' in tl and 'bluff' in tl:
        return "Everyone thought it was a bluff. The cards told a different story."
    if 'check' in tl and 'river' in tl:
        return "He checked the river with the nuts. The reason will surprise you."
    return None

def formula_emotional(text, amount):
    """Visceral emotional trigger"""
    tl = text.lower()
    if 'eliminat' in tl or 'bust' in tl:
        return "One player was about to leave the tournament. They didn't know it yet."
    if amount and ('all in' in tl or 'shov' in tl or 'jam' in tl):
        return f"There was {amount} in the middle. Silence fell over the entire table."
    if 'silence' in tl or 'quiet' in tl or 'breath' in tl:
        return "The whole room went quiet. Something extraordinary was about to happen."
    return None

def formula_partial_reveal(text, amount):
    """Give half the result, hide the rest"""
    tl = text.lower()
    if 'full house' in tl:
        return "He flopped trips. By the river, he had a full house. It still wasn't enough."
    if 'four of a kind' in tl:
        return "The board paired. Then it paired again. One player hit four of a kind."
    if 'flush' in tl and 'draw' in tl:
        return "He was on the flush draw the whole time. The river was going to decide everything."
    if amount:
        return f"The pot was already at {amount}. Then someone moved all-in on top."
    return None

def formula_immersion(text, amount):
    """Make viewer imagine themselves in the hand"""
    tl = text.lower()
    if 'bluff' in tl and ('shov' in tl or 'all in' in tl):
        return "You're holding nothing. Your opponent just moved all-in. What do you do?"
    if 'call' in tl and ('all in' in tl or 'shov' in tl):
        return "Your tournament life is on the line. You have 30 seconds to decide."
    if 'raise' in tl and 'reraise' in tl or 'three' in tl and 'bet' in tl:
        return "You 3-bet. He 4-bets. The pot is already massive. Do you fold or shove?"
    if amount:
        return f"Imagine sitting down at a table and winning {amount} in a single hand."
    return None

FORMULAS = [
    formula_suspense_gap,
    formula_counter_intuitive,
    formula_emotional,
    formula_partial_reveal,
    formula_immersion,
]

# Ultimate fallbacks — guaranteed unique, indexed
FALLBACKS = [
    "Everyone at the table knew the right play. Nobody made it.",
    "The river card changed everything. Nobody saw it coming.",
    "He had the best hand. Until he didn't.",
    "She moved all-in as a pure bluff. The whole table held their breath.",
    "This is the hand that players talk about for years.",
    "One decision. One card. One moment that defines a career.",
    "The cage came into play. One player was about to lose it all.",
]

def generate_hook(clip_num, text):
    """Generate a unique hook. Tries formulas in rotation, guarantees no duplicates."""
    amount = extract_amount(text)
    # Try formulas starting from a different offset per clip
    n = len(FORMULAS)
    for i in range(n):
        formula = FORMULAS[(clip_num - 1 + i) % n]
        result = formula(text, amount)
        if result and result not in used_hooks:
            used_hooks.add(result)
            return result
    # All formulas failed or duplicated — use indexed fallback
    for fb in FALLBACKS:
        if fb not in used_hooks:
            used_hooks.add(fb)
            return fb
    # Last resort
    return f"One of the greatest poker hands ever played. Clip {clip_num}."

def generate_tags(text):
    base = ['#poker', '#pokerstars', '#pokerclips', '#pokerhands']
    tl = text.lower()
    if 'bluff' in tl: base.append('#bluff')
    if 'all in' in tl: base.append('#allin')
    if 'river' in tl: base.append('#river')
    base.append('#shorts')
    return ' '.join(base[:7])


print('Generating hooks...\n')
used_hooks = set()
for c in clips:
    text = get_clip_text(c)
    hook = generate_hook(c['clip_number'], text)
    tags = generate_tags(text)

    c['hook_v2'] = hook
    c['yt_title'] = hook
    c['yt_desc'] = tags

    print(f"[{c['clip_number']}] {hook}")
    print(f"     Tags: {tags}")
    print()

(OUT / 'clips_analysis.json').write_text(json.dumps(clips, indent=2, ensure_ascii=False), encoding='utf-8')
print('Saved. Now re-cutting clips with new hooks...')

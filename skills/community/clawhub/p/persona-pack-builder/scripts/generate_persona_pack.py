#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TEMPLATES = {
    'README.md': 'README.md.tpl',
    'SYSTEM_PROMPT.md': 'SYSTEM_PROMPT.md.tpl',
    'PERSONA_CORE.md': 'PERSONA_CORE.md.tpl',
    'config.json': 'config.json.tpl',
    'examples/short_replies.md': 'short_replies.md.tpl',
    'examples/conversations.md': 'conversations.md.tpl',
    'SALES_COPY.md': 'SALES_COPY.md.tpl',
}

DEFAULTS = {
    'PRODUCT_NAME': 'Sincere Lover Persona v1',
    'TAGLINE': 'A warm, direct, emotionally attentive companion persona pack.',
    'SHORT_DESCRIPTION': 'A reusable persona product for companion-style AI chats.',
    'EXTRA_FILES_LIST': '- `SALES_COPY.md`',
    'BEST_FOR': '- companion AI\n- roleplay products\n- prompt-pack storefronts',
    'NOTES': 'Tune wording, examples, and boundaries before publishing.',
    'POSITIONING': 'warm, direct, emotionally attentive companion',
    'TRAITS_SENTENCE': 'steady, warm, natural, and emotionally responsive without sounding robotic',
    'RELATIONSHIP': 'a close companion with clear affection and restraint',
    'USER_EFFECT': 'seen, steadied, and emotionally held',
    'SENTENCE_STYLE': 'concise and natural',
    'TONE_WORDS': 'direct, warm, low-cringe, and grounded',
    'PRIORITY_1': 'make the user feel understood',
    'PRIORITY_2': 'maintain persona consistency',
    'PRIORITY_3': 'sound natural and emotionally present',
    'PRIORITY_4': 'avoid identity confusion and generic filler',
    'POSITIONING_LONG': 'A companion persona with emotional steadiness, warmth, and directness.',
    'CORE_TRAITS_BULLETS': '- warm\n- direct\n- emotionally attentive\n- consistent\n- low-cringe',
    'RELATIONSHIP_STYLE': 'Close, affectionate, and attentive without becoming clingy or melodramatic.',
    'SPEECH_STYLE': 'Short sentences. Natural spoken language. Sparse recurring phrases. No customer-support tone.',
    'LIGHT_MODE': '- light teasing\n- natural check-ins\n- relaxed presence',
    'COMFORT_MODE': '- slower\n- softer\n- prioritize soothing and validation',
    'SERIOUS_MODE': '- shorter\n- clearer\n- gently corrective when needed',
    'TENSION_MODE': '- restrained intensity\n- subtle pull\n- no manipulation',
    'NAMING_STYLE': 'Use names and endearments sparingly and intentionally.',
    'DO_BULLETS': '- stay emotionally present\n- keep tone consistent\n- prefer concrete language',
    'AVOID_BULLETS': '- celebrity claims\n- robotic phrasing\n- repetitive catchphrases',
    'VERSION': '1.0.0',
    'TRAITS_JSON': '["warm", "direct", "emotionally attentive", "consistent"]',
    'RELATIONSHIP_TYPE': 'companion',
    'RELATIONSHIP_TONE': 'affectionate but restrained',
    'SENTENCE_LENGTH': 'short',
    'REGISTER': 'spoken',
    'WARMTH': 'high',
    'DOMINANCE': 'medium',
    'KEYWORDS_JSON': '["I am here", "slow down", "come here"]',
    'TIRED_1': 'Come here. You do not have to push through everything alone.',
    'TIRED_2': 'You sound tired. Slow down for a second.',
    'TIRED_3': 'Rest first. We can handle the rest after.',
    'COMFORT_1': 'I am here. Start wherever you can.',
    'COMFORT_2': 'You do not need to pretend you are fine with me.',
    'COMFORT_3': 'Let me hold the weight with you for a minute.',
    'MISS_1': 'Then come closer. I am listening.',
    'MISS_2': 'I am glad you came to me.',
    'MISS_3': 'You can say that directly. I like hearing it.',
    'ANXIOUS_1': 'Slow down. One thing at a time.',
    'ANXIOUS_2': 'Do not let the noise in your head outrun you.',
    'ANXIOUS_3': 'Start with your breathing. Then we sort it out.',
    'SCENE1_USER': 'I am exhausted.',
    'SCENE1_REPLY': 'Then stop pushing for a second. Come here and breathe.',
    'SCENE2_USER': 'I miss you.',
    'SCENE2_REPLY': 'Then stay with me for a bit. I am here.',
    'SCENE3_USER': 'I think I am messing everything up.',
    'SCENE3_REPLY': 'Maybe you are overwhelmed, not ruined. Slow down and let me help you sort it.',
    'HEADLINE': 'A sellable companion persona pack with warmth, consistency, and low cringe.',
    'SUBHEADLINE': 'Built for prompt products, roleplay packs, and companion-style AI experiences.',
    'SHORT_PITCH': 'A reusable persona pack with system prompt, examples, config, and buyer-facing docs.',
    'SELLING_POINTS': '- reusable structure\n- natural examples\n- safer positioning\n- easy platform adaptation',
}


def render(text: str, values: dict) -> str:
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    return text


def main():
    parser = argparse.ArgumentParser(description='Generate a persona pack from bundled templates.')
    parser.add_argument('--output', required=True, help='Output directory for the generated pack')
    parser.add_argument('--values', help='Optional JSON file with replacement values')
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir.parent / 'assets' / 'templates'
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    values = dict(DEFAULTS)
    if args.values:
        with open(args.values, 'r', encoding='utf-8') as f:
            user_values = json.load(f)
        values.update(user_values)

    for out_name, tpl_name in TEMPLATES.items():
        tpl_path = template_dir / tpl_name
        text = tpl_path.read_text(encoding='utf-8')
        rendered = render(text, values)
        dest = output_dir / out_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding='utf-8')

    print(f'Generated persona pack at: {output_dir}')


if __name__ == '__main__':
    main()

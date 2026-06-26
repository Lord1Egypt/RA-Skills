#!/usr/bin/env python3
"""
Ghostty Voice Profile Builder

Analyzes sent messages (emails, WhatsApp, Slack exports) and generates
a voice profile markdown file that Ghostty uses to draft in your voice.

Usage:
    python3 profile_builder.py --source ./my-emails/ --format eml --output ghostty/voice-profile.md
    python3 profile_builder.py --source ./whatsapp-chat.json --format json --output ghostty/voice-profile.md
    python3 profile_builder.py --source ./slack-export.csv --format csv --output ghostty/voice-profile.md
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path


def extract_text_from_eml(folder_path):
    """Extract message bodies from .eml files."""
    messages = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.eml'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # Extract body after first blank line (skip headers)
                    body = re.split(r'\n\s*\n', content, maxsplit=1)
                    if len(body) > 1:
                        messages.append(body[1].strip())
                except Exception:
                    pass
    return messages


def extract_text_from_json(file_path):
    """Extract message bodies from WhatsApp/Telegram JSON export."""
    import json
    messages = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'text' in item:
                    messages.append(str(item['text']))
                elif isinstance(item, dict) and 'message' in item:
                    messages.append(str(item['message']))
        elif isinstance(data, dict):
            # Try common WhatsApp export structures
            for key in ['messages', 'chat', 'conversation']:
                if key in data and isinstance(data[key], list):
                    for item in data[key]:
                        if isinstance(item, dict):
                            for body_key in ['text', 'message', 'content']:
                                if body_key in item:
                                    messages.append(str(item[body_key]))
                                    break
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
    return messages


def extract_text_from_csv(file_path):
    """Extract message bodies from Slack/CSV export."""
    import csv
    messages = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try common column names for message body
                for col in ['text', 'message', 'content', 'body']:
                    if col in row and row[col]:
                        messages.append(str(row[col]))
                        break
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
    return messages


def analyze_messages(messages):
    """Analyze a collection of messages and extract voice patterns."""
    if not messages:
        return None
    
    # Filter: keep only messages that look like actual written communication
    # (remove auto-replies, system messages, very short grunts)
    filtered = [m for m in messages if len(m.split()) >= 3 and not m.startswith('[')]
    if not filtered:
        filtered = messages
    
    # Basic metrics
    all_words = ' '.join(filtered).split()
    sentence_counts = [len(re.split(r'[.!?]+', m)) for m in filtered]
    
    avg_sentence_len = sum(len(m.split()) for m in filtered) / len(filtered)
    avg_sentences = sum(sentence_counts) / len(sentence_counts)
    
    # Greeting detection
    greeting_patterns = [
        r'^hey[a-z]*\b', r'^hi[a-z]*\b', r'^hello\b', r'^yo\b',
        r'^dear\b', r'^greetings\b', r'^good (morning|afternoon|evening)',
        r'^[a-z]+,\s*$'  # "Hey," as opener
    ]
    greetings = []
    for msg in filtered[:50]:  # Check first 50 messages
        first_line = msg.strip().split('\n')[0]
        for pat in greeting_patterns:
            if re.search(pat, first_line.lower()):
                greetings.append(first_line.strip())
                break
    
    # Sign-off detection
    signoff_patterns = [
        r'(cheers|thanks|best|regards|kind regards|warmly|sincerely|yours|talk soon|let me know|looking forward|kindly)',
        r'(👍|🙏|😊|🔥|💯|😂)',  # emoji sign-offs
    ]
    signoffs = []
    for msg in filtered[:50]:
        lines = msg.strip().split('\n')
        last_line = lines[-1].strip() if lines else ''
        for pat in signoff_patterns:
            if re.search(pat, last_line.lower()):
                signoffs.append(last_line)
                break
    
    # Pet phrases (most common bigrams and trigrams excluding stop words)
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'must', 'shall', 'can', 'to', 'of', 'in',
                  'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'between', 'under',
                  'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
                  'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
                  'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                  'too', 'very', 'just', 'and', 'but', 'or', 'if', 'because', 'until',
                  'while', 'that', 'which', 'who', 'whom', 'this', 'these', 'those',
                  'am', 'it', 'its', 'i', 'me', 'my', 'we', 'us', 'our', 'you', 'your',
                  'he', 'him', 'his', 'she', 'her', 'they', 'them', 'their', 'what',
                  'any', 'both', 'few', 'more', 'most', 'other', 'some', 'such'}
    
    bigrams = []
    for msg in filtered:
        words = [w.lower().strip('.,!?;:"') for w in msg.split()]
        for i in range(len(words) - 1):
            if words[i] not in stop_words and words[i+1] not in stop_words:
                bigrams.append(f"{words[i]} {words[i+1]}")
    
    top_bigrams = Counter(bigrams).most_common(20)
    
    # Emoji detection
    emojis = re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', ' '.join(filtered))
    emoji_freq = len(emojis) / len(filtered)
    top_emojis = Counter(emojis).most_common(10)
    
    # Confidence markers (hedging)
    hedge_words = ['probably', 'perhaps', 'maybe', 'i think', 'i guess', 'might', 'could',
                   'seems', 'appears', 'likely', 'possibly', 'supposedly', 'presumably']
    hedges = sum(1 for msg in filtered for hw in hedge_words if hw in msg.lower())
    hedge_ratio = hedges / len(filtered)
    
    # Exclamation usage
    exclamations = sum(1 for msg in filtered if '!' in msg)
    exclamation_ratio = exclamations / len(filtered)
    
    # Question usage
    questions = sum(1 for msg in filtered if '?' in msg)
    question_ratio = questions / len(filtered)
    
    # ALL CAPS usage
    caps_words = re.findall(r'\b[A-Z]{3,}\b', ' '.join(filtered))
    caps_ratio = len(caps_words) / len(filtered)
    
    return {
        'message_count': len(filtered),
        'avg_sentence_length': round(avg_sentence_len, 1),
        'avg_sentences_per_message': round(avg_sentences, 1),
        'top_greetings': Counter(greetings).most_common(5),
        'top_signoffs': Counter(signoffs).most_common(5),
        'top_bigrams': top_bigrams,
        'emoji_usage': emoji_freq,
        'top_emojis': top_emojis,
        'hedge_ratio': round(hedge_ratio, 2),
        'exclamation_ratio': round(exclamation_ratio, 2),
        'question_ratio': round(question_ratio, 2),
        'caps_ratio': round(caps_ratio, 3),
    }


def generate_profile(analysis, output_path):
    """Write the voice profile markdown file."""
    a = analysis
    
    # Determine style scores
    confidence = max(1, min(10, int(10 - (a['hedge_ratio'] * 20))))
    warmth = max(1, min(10, int(5 + (a['emoji_usage'] * 50) + (a['exclamation_ratio'] * 10))))
    formality = max(1, min(10, int(5 + (a['caps_ratio'] * 50) - (a['emoji_usage'] * 20))))
    
    top_greetings = ', '.join([f'"{g}"' for g, _ in a['top_greetings'][:3]]) or 'varies'
    top_signoffs = ', '.join([f'"{s}"' for s, _ in a['top_signoffs'][:3]]) or 'varies'
    top_phrases = ', '.join([f'"{b}"' for b, _ in a['top_bigrams'][:5]])
    top_emojis_str = ' '.join([e for e, _ in a['top_emojis'][:5]]) if a['top_emojis'] else 'none'
    
    # Determine length category
    if a['avg_sentence_length'] < 10:
        length_cat = "short and punchy (1-3 sentences)"
    elif a['avg_sentence_length'] < 20:
        length_cat = "medium (3-6 sentences)"
    else:
        length_cat = "detailed (5-10 sentences)"
    
    profile = f"""# My Voice Profile

> Auto-generated by Ghostty profile_builder.py
> Analyzed {a['message_count']} messages

## Quick Summary
A {length_cat} writer. {"Terse and direct" if confidence >= 7 else "Considered and careful"}. 
{"Warm and expressive" if warmth >= 7 else "Measured and understated"} in tone. 
{"Formally correct" if formality >= 7 else "Casual and relaxed"} in register.

## Greeting Style
Typical greetings: {top_greetings}

## Sign-off Style
Typical sign-offs: {top_signoffs}

## Typical Length
Average: {a['avg_sentence_length']} words per sentence, {a['avg_sentences_per_message']} sentences per message.
Writing style: {length_cat}.

## Tone Settings
- **Confidence:** {confidence}/10 {"(direct, assertive — says what needs saying)" if confidence >= 7 else "(hedged, careful — leaves room)"}
- **Warmth:** {warmth}/10 {"(expressive, personal — uses emoji and emotional language)" if warmth >= 7 else "(reserved, neutral)"}
- **Formality:** {formality}/10 {"(professional, proper)" if formality >= 7 else "(casual, relaxed)"}
- **Humor:** {"dry and subtle" if a['hedge_ratio'] > 0.1 else "direct, minimal filler"}
- **Question frequency:** {"asks often" if a['question_ratio'] > 0.3 else "asks selectively"}

## Phrases I Use Naturally
Most common patterns: {top_phrases}

## Emoji Usage
{"Frequently uses emoji" if a['emoji_usage'] > 0.3 else "Occasional emoji" if a['emoji_usage'] > 0.1 else "Rarely or never uses emoji"}
Common: {top_emojis_str}

## Structural Habits
- Exclamation usage: {"high (enthusiastic)" if a['exclamation_ratio'] > 0.2 else "moderate" if a['exclamation_ratio'] > 0.05 else "sparingly (reserved)"}
- ALL CAPS: {"used for emphasis occasionally" if a['caps_ratio'] > 0.01 else "rarely or never"}
- Hedging ("probably", "maybe", "I think"): {"frequent" if a['hedge_ratio'] > 0.2 else "moderate" if a['hedge_ratio'] > 0.05 else "minimal"}

## What Makes My Writing Distinctive
1. {"Gets straight to the point — minimal pleasantries" if a['avg_sentences_per_message'] < 3 else "Takes time to build context before the main point"}
2. {"Uses exclamation sparingly — each one lands" if a['exclamation_ratio'] < 0.1 else "Uses exclamation to convey genuine enthusiasm"}
3. {"Sign-offs are brief or absent" if not a['top_signoffs'] else "Always closes with a characteristic sign-off"}

## Phrases I Almost Never Use
- "I hope this email finds you well"
- "Please do not hesitate to reach out"
- "As per our conversation"
- "Kindly note"
- "I would be happy to assist"
- "Great question!" (as an opener)

## Per-Person Overrides
Add person-specific overrides in ghostty/per-person/{{name}}.md
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(profile)
    
    print(f"Voice profile written to: {output_path}")
    print(f"Analyzed {a['message_count']} messages")
    print(f"Summary: {confidence}/10 confidence, {warmth}/10 warmth, {formality}/10 formality")
    
    return profile


def main():
    parser = argparse.ArgumentParser(description='Ghostty Voice Profile Builder')
    parser.add_argument('--source', required=True, help='Path to email folder or export file')
    parser.add_argument('--format', required=True, choices=['eml', 'json', 'csv'],
                        help='Format of the source files')
    parser.add_argument('--output', required=True, help='Output path for voice profile markdown')
    args = parser.parse_args()
    
    print(f"Extracting messages from {args.source} (format: {args.format})...")
    
    if args.format == 'eml':
        messages = extract_text_from_eml(args.source)
    elif args.format == 'json':
        messages = extract_text_from_json(args.source)
    elif args.format == 'csv':
        messages = extract_text_from_csv(args.source)
    
    print(f"Found {len(messages)} messages")
    
    if len(messages) < 5:
        print("ERROR: Not enough messages to build a reliable profile. Need at least 5.",
              file=sys.stderr)
        sys.exit(1)
    
    print("Analyzing voice patterns...")
    analysis = analyze_messages(messages)
    
    print("Generating profile...")
    generate_profile(analysis, args.output)


if __name__ == '__main__':
    main()

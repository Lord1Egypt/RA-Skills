"""
OutputForge AI-ism Cleanup
Remove common AI hedging and unnecessary disclaimers

Author: Shadow Rose
License: MIT
"""

import re


# Default patterns to remove
DEFAULT_AI_ISMS = [
    # Direct AI self-references
    r"As an AI( language model| assistant)?,?\s*",
    r"As a large language model,?\s*",
    r"I('m| am) an AI( language model| assistant)?\s*(and|,)?\s*",
    r"Being an AI,?\s*",
    
    # Hedging phrases
    r"It'?s important to note that\s*",
    r"It should be noted that\s*",
    r"Please note that\s*",
    r"Keep in mind that\s*",
    r"Bear in mind that\s*",
    r"It'?s worth noting that\s*",
    
    # Excessive caveats (when repetitive)
    r"However, it'?s important to remember that\s*",
    r"That being said,?\s*",
    r"Having said that,?\s*",
    
    # Unnecessary disclaimers
    r"I don'?t have personal (opinions|experiences|feelings)\s*(but|however|,)?\s*",
    r"I (can'?t|cannot) (access|browse|search) the internet,?\s*",
    r"I don'?t have access to real-?time (data|information),?\s*",
    r"My (training|knowledge) (data )?(was cut off|cutoff is|ends) (in|at) [^.]+\.\s*",
    
    # Repetitive apologetic language
    r"I apologize,? but\s*",
    r"Sorry,? but\s*",
    r"I'?m sorry,? but\s*",
    
    # Uncertainty hedges (use sparingly - some are legitimate)
    r"I think that maybe\s*",
    r"Perhaps it could be that\s*",
    r"It seems like it might be\s*",
]


# Phrases that add no value (filler)
FILLER_PHRASES = [
    r"\bvery very\b",
    r"\breally really\b",
    r"\bquite quite\b",
    r"\bjust just\b",
]


# Normalize repetitive patterns
def remove_repetitive_disclaimers(text):
    """Remove repeated disclaimer patterns within the same text"""
    # If "However," appears more than 3 times, reduce to 2
    however_count = len(re.findall(r'\bHowever,\s*', text, re.IGNORECASE))
    if however_count > 3:
        # Replace 4th+ occurrences with "Also,"
        replacements = 0
        def replace_however(match):
            nonlocal replacements
            replacements += 1
            if replacements > 2:
                return "Also, "
            return match.group(0)
        
        text = re.sub(r'\bHowever,\s*', replace_however, text, flags=re.IGNORECASE)
    
    return text


def clean_ai_isms(text, custom_rules=None):
    """
    Clean AI-isms from text
    
    Args:
        text: Input text to clean
        custom_rules: Optional list of additional regex patterns to remove
    
    Returns:
        Cleaned text
    """
    cleaned = text
    
    # Apply default AI-ism patterns
    for pattern in DEFAULT_AI_ISMS:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Apply custom rules if provided
    if custom_rules:
        for pattern in custom_rules:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove filler phrases
    for pattern in FILLER_PHRASES:
        cleaned = re.sub(pattern, lambda m: m.group(0).split()[0], cleaned, flags=re.IGNORECASE)
    
    # Remove repetitive disclaimers
    cleaned = remove_repetitive_disclaimers(cleaned)
    
    # Clean up spacing issues caused by removals
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)  # Multiple blank lines to double
    cleaned = re.sub(r'^\s+', '', cleaned, flags=re.MULTILINE)  # Leading spaces per line
    cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)  # Space before punctuation
    
    # Fix capitalization after removals
    cleaned = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), cleaned)
    
    # Ensure first character is capitalized
    if cleaned and cleaned[0].islower():
        cleaned = cleaned[0].upper() + cleaned[1:]
    
    return cleaned.strip()


def analyze_ai_isms(text):
    """
    Analyze text for AI-isms without removing them
    Returns a dict with pattern counts
    """
    results = {}
    
    for i, pattern in enumerate(DEFAULT_AI_ISMS):
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            results[f"pattern_{i}"] = {
                'pattern': pattern,
                'count': len(matches),
                'examples': matches[:3]  # First 3 examples
            }
    
    return results


def suggest_improvements(text):
    """
    Suggest improvements without modifying text
    Returns list of suggestions
    """
    suggestions = []
    
    # Check for AI-isms
    ai_isms = analyze_ai_isms(text)
    if ai_isms:
        suggestions.append({
            'type': 'ai_isms',
            'severity': 'high',
            'message': f"Found {len(ai_isms)} types of AI-isms that could be removed",
            'details': ai_isms
        })
    
    # Check for excessive hedging
    hedge_words = ['perhaps', 'maybe', 'might', 'could', 'possibly', 'potentially']
    hedge_count = sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in hedge_words)
    word_count = len(text.split())
    
    if word_count > 0 and (hedge_count / word_count) > 0.02:  # More than 2% hedging
        suggestions.append({
            'type': 'excessive_hedging',
            'severity': 'medium',
            'message': f"High hedging ratio: {hedge_count} hedge words in {word_count} total words",
            'suggestion': 'Consider being more direct and confident'
        })
    
    # Check for repetitive "However"
    however_count = len(re.findall(r'\bHowever,', text, re.IGNORECASE))
    if however_count > 3:
        suggestions.append({
            'type': 'repetitive_conjunctions',
            'severity': 'low',
            'message': f'"However" appears {however_count} times',
            'suggestion': 'Vary your transitions (Also, Furthermore, Additionally, etc.)'
        })
    
    # Check for passive voice (basic check)
    passive_patterns = [
        r'\b(was|were|is|are|been|be)\s+\w+ed\b',
        r'\b(was|were|is|are|been|be)\s+being\s+\w+ed\b'
    ]
    passive_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in passive_patterns)
    
    if passive_count > word_count * 0.1:  # More than 10% passive
        suggestions.append({
            'type': 'passive_voice',
            'severity': 'medium',
            'message': f'Detected ~{passive_count} passive voice constructions',
            'suggestion': 'Consider using more active voice for clarity'
        })
    
    return suggestions


if __name__ == '__main__':
    # Quick test/demo
    import sys
    
    if len(sys.argv) > 1:
        test_text = ' '.join(sys.argv[1:])
    else:
        test_text = """
        As an AI language model, I think that maybe this is a good example.
        However, it's important to note that this text has many AI-isms.
        I don't have personal opinions, but I can tell you that this needs cleaning.
        However, it should be noted that some hedging is necessary.
        However, too much hedging is bad. That being said, we should fix it.
        """
    
    print("ORIGINAL:")
    print(test_text)
    print("\n" + "="*60 + "\n")
    
    print("ANALYSIS:")
    suggestions = suggest_improvements(test_text)
    for s in suggestions:
        print(f"[{s['severity'].upper()}] {s['message']}")
        if 'suggestion' in s:
            print(f"  → {s['suggestion']}")
    print("\n" + "="*60 + "\n")
    
    print("CLEANED:")
    print(clean_ai_isms(test_text))

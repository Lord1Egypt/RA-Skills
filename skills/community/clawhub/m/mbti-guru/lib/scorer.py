#!/usr/bin/env python3
"""
MBTI Scorer - Calculate personality type from answers
"""

from typing import Dict, Tuple

def calculate_type(answers: list) -> Tuple[str, Dict]:
    """
    Calculate MBTI type from answers
    """
    from lib.questions import get_questions
    
    if not answers:
        return "UNKNOWN", {}
    
    # Get question count
    q_count = len(answers)
    if q_count >= 200:
        version = 200
    elif q_count >= 144:
        version = 144
    elif q_count >= 93:
        version = 93
    else:
        version = 70
    
    questions = get_questions(version)
    
    # Count preferences for each dimension
    dim_counts = {
        "EI": {"E": 0, "I": 0},
        "SN": {"S": 0, "N": 0},
        "TF": {"T": 0, "F": 0},
        "JP": {"J": 0, "P": 0}
    }
    
    dim_totals = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
    
    # Build question lookup
    q_map = {q["id"]: q for q in questions}
    
    for q_id, selected in answers:
        if q_id not in q_map:
            continue
        q = q_map[q_id]
        dim = q["dimension"]
        
        # Get preference based on answer choice
        if selected.upper() == "A":
            pref = q["preference_a"]
        else:
            # The other preference
            first_pref = q["preference_a"]
            all_prefs = {"EI": ["E", "I"], "SN": ["S", "N"], "TF": ["T", "F"], "JP": ["J", "P"]}
            prefs = all_prefs[dim]
            pref = prefs[1] if first_pref == prefs[0] else prefs[0]
        
        dim_counts[dim][pref] += 1
        dim_totals[dim] += 1
    
    # Calculate indices
    scores = {}
    type_letters = []
    
    for dim in ["EI", "SN", "TF", "JP"]:
        first_count = dim_counts[dim][dim[0]]
        total = dim_totals[dim]
        
        if total == 0:
            scores[dim] = 50
            type_letters.append(dim[0])
            continue
        
        # Index for first letter
        index_first = (first_count / total) * 100
        
        scores[dim] = round(index_first, 1)
        
        # Determine preference
        if index_first > 50:
            type_letters.append(dim[0])
        else:
            type_letters.append(dim[1])
    
    type_code = "".join(type_letters)
    
    return type_code, scores


def calculate_clarity(score: float) -> Tuple[float, str]:
    """
    Calculate clarity level from score
    """
    clarity = abs(score - 50) * 2
    
    if clarity <= 25:
        level = "Slight / 轻微"
    elif clarity <= 50:
        level = "Moderate / 中等"
    elif clarity <= 75:
        level = "Clear / 清晰"
    else:
        level = "Very Clear / 非常清晰"
    
    return round(clarity, 1), level


def format_scores(scores: Dict) -> str:
    """Format scores for display"""
    result = []
    for dim, score in scores.items():
        clarity, level = calculate_clarity(score)
        pref = dim[0] if score > 50 else dim[1]
        result.append(f"{dim}: {pref} {score}% ({level})")
    return "\n".join(result)

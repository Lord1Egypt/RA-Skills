#!/usr/bin/env python3
"""Memory archive utility for weekly and monthly reports.

This module reads memory files from a date range and creates an archive
that can be used by weekly/monthly report generators for more accurate LLM analysis.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


def archive_memory_files(
    date_list: List[str],
    memory_dir: str,
    output_path: Optional[str] = None,
    include_fields: Optional[List[str]] = None
) -> Dict:
    """Archive memory files for a date range.
    
    Args:
        date_list: List of date strings (YYYY-MM-DD)
        memory_dir: Directory containing memory files
        output_path: Optional path to save archive JSON
        include_fields: Fields to extract (default: all)
    
    Returns:
        Archive dictionary with aggregated data
    """
    if include_fields is None:
        include_fields = [
            'weight', 'water', 'meals', 'exercise', 
            'medication', 'symptoms', 'custom_sections'
        ]
    
    archive = {
        'archive_date': datetime.now().isoformat(),
        'date_range': {
            'start': date_list[0] if date_list else '',
            'end': date_list[-1] if date_list else '',
            'total_days': len(date_list)
        },
        'daily_records': [],
        'summary': {}
    }
    
    for date_str in date_list:
        file_path = os.path.join(memory_dir, f"{date_str}.md")
        if not os.path.exists(file_path):
            continue
        
        daily_data = {
            'date': date_str,
            'file_exists': True
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract weight
        if 'weight' in include_fields:
            weight_match = content.find('晨起空腹')
            if weight_match != -1:
                line = content[weight_match:weight_match+100]
                import re
                weight_kg_match = re.search(r'(\d+\.?\d*)\s*kg', line)
                weight_jin_match = re.search(r'(\d+\.?\d*)\s*斤', line)
                if weight_kg_match:
                    daily_data['weight_kg'] = float(weight_kg_match.group(1))
                elif weight_jin_match:
                    daily_data['weight_jin'] = float(weight_jin_match.group(1))
        
        # Extract water total
        if 'water' in include_fields:
            water_match = content.rfind('累计：')
            if water_match != -1:
                line = content[water_match:water_match+50]
                import re
                water_match = re.search(r'(\d+)ml', line)
                if water_match:
                    daily_data['water_ml'] = int(water_match.group(1))
        
        # Extract calories
        if 'meals' in include_fields:
            calorie_match = content.rfind('今日累计')
            if calorie_match != -1:
                line = content[calorie_match:calorie_match+50]
                import re
                calorie_match = re.search(r'(\d+)kcal', line)
                if calorie_match:
                    daily_data['calories'] = int(calorie_match.group(1))
        
        # Extract medication
        if 'medication' in include_fields:
            med_start = content.find('## 💊 用药记录')
            if med_start != -1:
                med_end = content.find('##', med_start + 1)
                if med_end == -1:
                    med_end = len(content)
                med_section = content[med_start:med_end]
                daily_data['medication'] = med_section.strip()
        
        # Extract symptoms
        if 'symptoms' in include_fields:
            symptom_start = content.find('## 📝 症状/不适')
            if symptom_start != -1:
                symptom_end = content.find('##', symptom_start + 1)
                if symptom_end == -1:
                    symptom_end = len(content)
                symptom_section = content[symptom_start:symptom_end]
                daily_data['symptoms'] = symptom_section.strip()
        
        archive['daily_records'].append(daily_data)
    
    # Build summary
    weights = [d.get('weight_kg') for d in archive['daily_records'] if d.get('weight_kg')]
    waters = [d.get('water_ml') for d in archive['daily_records'] if d.get('water_ml')]
    calories = [d.get('calories') for d in archive['daily_records'] if d.get('calories')]
    
    archive['summary'] = {
        'avg_weight_kg': sum(weights) / len(weights) if weights else None,
        'weight_change': (weights[-1] - weights[0]) if len(weights) > 1 else None,
        'avg_water_ml': sum(waters) / len(waters) if waters else None,
        'water_compliance_days': sum(1 for w in waters if w >= 2000),
        'avg_calories': sum(calories) / len(calories) if calories else None,
        'total_days': len(archive['daily_records'])
    }
    
    # Save archive if output_path provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(archive, f, ensure_ascii=False, indent=2)
    
    return archive


if __name__ == '__main__':
    # Test usage
    from datetime import timedelta
    
    # Test with last 7 days
    end_date = datetime.now()
    date_list = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    
    archive = archive_memory_files(
        date_list=date_list,
        memory_dir='/root/.openclaw/workspace/memory',
        output_path='/root/.openclaw/workspace/skills/health-mate/data/archive_test.json'
    )
    
    print(f"Archive created: {archive['date_range']['total_days']} days")
    print(f"Summary: {json.dumps(archive['summary'], ensure_ascii=False, indent=2)}")

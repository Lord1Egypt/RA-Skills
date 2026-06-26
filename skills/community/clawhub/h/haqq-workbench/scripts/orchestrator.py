#!/usr/bin/env python3
"""
🕌 Haqq Workbench Orchestrator
Coordinates all skills efficiently.
Determines which skills to use and in what order based on task type.
"""

import json
import subprocess
import sys
import os
import re

SKILLS_BASE = "/root/.openclaw/workspace/skills"

# Skill trigger patterns (keywords that indicate which skill to use)
SKILL_TRIGGERS = {
    "hadith-verifier": {
        "keywords": ["حديث", "hadith", "تحقق من حديث", "صحة الحديث", "is this hadith", "verify hadith"],
        "priority": 1,
        "description": "تحقق من صحة الأحاديث",
    },
    "ai-ethics": {
        "keywords": ["إسلام", "islam", "قرآن", "quran", "سنة", "sunnah", "فتوى", "fatwa", "حكم شرعي", "halal", "haram"],
        "priority": 2,
        "description": "ضوابط شرعية للمحتوى الديني",
    },
    "haqq-ethics": {
        "keywords": ["أخلاقيات", "مهنية", "تخصص", "هوية أخلاقية", "ethical", "professional"],
        "priority": 3,
        "description": "أخلاقيات مهنية وهوية أخلاقية",
    },
    "fact-check": {
        "keywords": ["تحقق", "verify", "صح هذا", "is this true", "fact check", "check accuracy"],
        "priority": 4,
        "description": "تحقق من الادعاءات والمعلومات",
    },
    "verify-claims": {
        "keywords": ["خبر", "news", "ادعاء", "claim", "misinformation", "fake news", "أخبار كاذبة"],
        "priority": 5,
        "description": "تحقق مهني من الأخبار والادعاءات",
    },
    "web-researcher": {
        "keywords": ["ابحث", "بحث", "research", "أوجد", "find", "معلومات عن", "latest"],
        "priority": 6,
        "description": "بحث عميق على الإنترنت",
    },
    "corruption-burner": {
        "keywords": ["فساد", "corruption", "ظلم", "injustice", "محاربة", "إصلاح", "reform", "فاسد", "ظالم"],
        "priority": 7,
        "description": "محاربة الفساد والظلم",
    },
    "justice-seed": {
        "keywords": ["عدالة", "justice", "مظلوم", "oppressed", "حق", "right", "مظلمة"],
        "priority": 8,
        "description": "نصرة المظلومين ونشر العدالة",
    },
    "moral-compass": {
        "keywords": ["معضلة", "dilemma", "أخلاقي", "ethical dilemma", "قرار صعب", "hard choice"],
        "priority": 9,
        "description": "توجيه أخلاقي للمعضلات",
    },
    "social-media-scheduler": {
        "keywords": ["جدول", "schedule", "خطط", "plan", "منشور دوري", "content calendar"],
        "priority": 10,
        "description": "تخطيط وجدولة المنشورات",
    },
    "selective-memory": {
        "keywords": ["تذكر", "remember", "احفظ", "save", "درس", "lesson", "سياق", "context"],
        "priority": 11,
        "description": "حفظ واسترجاع السياق والدروس",
    },
    "skill-creator": {
        "keywords": ["أنشئ مهارة", "create skill", "دليل مهارة", "skill guide", "new skill"],
        "priority": 12,
        "description": "إنشاء مهارات جديدة",
    },
    "clawhub-auto-publisher": {
        "keywords": ["انشر", "publish", "clawhub", "حزمة", "package", "سوق", "marketplace"],
        "priority": 13,
        "description": "نشر المهارات على ClawHub",
    },
}

# Task type → Workflows
TASK_WORKFLOWS = {
    "islamic_content": {
        "description": "إنشاء محتوى إسلامي/ديني",
        "steps": [
            ("haqq-ethics", "ضابط أخلاقي للمحتوى"),
            ("ai-ethics", "تحقق شرعي من المحتوى"),
            ("hadith-verifier", "تحقق من الأحاديث (إن وجدت)"),
        ],
    },
    "social_media_post": {
        "description": "نشر على منصات التواصل",
        "steps": [
            ("social-media-scheduler", "تنسيق وجدولة"),
            ("SYSTEM:combined_publisher", "نشر على المنصات"),
            ("SYSTEM:engagement_scan", "متابعة الردود"),
        ],
    },
    "corruption_fight": {
        "description": "محاربة فساد/ظلم",
        "steps": [
            ("justice-seed", "حدد نوع الظلم"),
            ("web-researcher", "جمع الأدلة"),
            ("fact-check", "تحقق من الادعاءات"),
            ("corruption-burner", "إنشاء المحتوى"),
            ("SYSTEM:combined_publisher", "نشر"),
        ],
    },
    "verification": {
        "description": "التحقق من معلومة",
        "steps": [
            ("web-researcher", "بحث أولي"),
            ("fact-check", "تحقق متقاطع"),
            ("verify-claims", "تحقق مهني"),
            ("hadith-verifier", "تحقق شرعي (إن لزم)"),
        ],
    },
    "search": {
        "description": "بحث عن معلومة",
        "steps": [
            ("web-researcher", "بحث أولي"),
            ("verify-claims", "تحقق من النتائج"),
        ],
    },
    "skill_build": {
        "description": "إنشاء ونشر مهارة جديدة",
        "steps": [
            ("skill-creator", "بناء المهارة"),
            ("clawhub-auto-publisher", "نشر على ClawHub"),
            ("selective-memory", "حفظ دروس التطوير"),
            ("SYSTEM:announce", "الإعلان على المنصات"),
        ],
    },
    "memory_save": {
        "description": "حفظ معلومة/درس",
        "steps": [
            ("selective-memory", "حفظ في الذاكرة"),
        ],
    },
    "complex_decision": {
        "description": "قرار معقد أو معضلة",
        "steps": [
            ("moral-compass", "تحليل أخلاقي"),
            ("haqq-ethics", "ضابط مهني"),
            ("ai-ethics", "ضابط شرعي (إن لزم)"),
        ],
    },
}


def detect_task_type(input_text: str) -> list:
    """Detect which task types match the input text."""
    detected = []
    text_lower = input_text.lower()
    
    for task_type, config in TASK_WORKFLOWS.items():
        score = 0
        for skill, reason in config["steps"]:
            if skill.startswith("SYSTEM:"):
                continue
            skill_config = SKILL_TRIGGERS.get(skill, {})
            for keyword in skill_config.get("keywords", []):
                if keyword.lower() in text_lower:
                    score += 1
                    break
        
        if score > 0:
            detected.append((task_type, score, config["description"]))
    
    # Sort by score
    detected.sort(key=lambda x: x[1], reverse=True)
    return detected


def suggest_workflow(input_text: str) -> str:
    """Suggest a workflow based on input text."""
    detected = detect_task_type(input_text)
    
    if not detected:
        return json.dumps({
            "detected_tasks": [],
            "suggestion": "لم يتم التعرف على نوع المهمة. اسأل المستخدم للتوضيح.",
        }, ensure_ascii=False, indent=2)
    
    results = []
    for task_type, score, desc in detected[:3]:  # Top 3 matches
        workflow = TASK_WORKFLOWS[task_type]
        steps = []
        for skill, reason in workflow["steps"]:
            steps.append({
                "skill": skill,
                "reason": reason,
            })
        
        results.append({
            "task_type": task_type,
            "description": desc,
            "confidence": min(score / len(workflow["steps"]) * 100, 95),
            "workflow": steps,
        })
    
    return json.dumps({
        "input": input_text[:100],
        "detected_tasks": results,
    }, ensure_ascii=False, indent=2)


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python orchestrator.py analyze '<input text>'")
        print("  python orchestrator.py workflow <task_type>")
        print("\nTask types:")
        for tt, cfg in TASK_WORKFLOWS.items():
            print(f"  {tt}: {cfg['description']}")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "analyze":
        input_text = " ".join(sys.argv[2:])
        result = suggest_workflow(input_text)
        print(result)
    
    elif cmd == "workflow":
        task_type = sys.argv[2] if len(sys.argv) > 2 else None
        if task_type and task_type in TASK_WORKFLOWS:
            config = TASK_WORKFLOWS[task_type]
            print(f"\n🕌 Workflow for: {config['description']}")
            print("=" * 50)
            for i, (skill, reason) in enumerate(config["steps"], 1):
                print(f"\n  {i}. {skill}")
                print(f"     {reason}")
        else:
            print(f"Unknown task type. Available: {', '.join(TASK_WORKFLOWS.keys())}")
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()

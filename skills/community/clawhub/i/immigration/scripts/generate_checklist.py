#!/usr/bin/env python3
"""Generate document checklist for visa application."""
import json
import os
import uuid
import argparse
from datetime import datetime

IMMIGRATION_DIR = os.path.expanduser("~/.openclaw/workspace/memory/immigration")
CHECKLISTS_FILE = os.path.join(IMMIGRATION_DIR, "checklists.json")

def ensure_dir():
    os.makedirs(IMMIGRATION_DIR, exist_ok=True)

def load_checklists():
    if os.path.exists(CHECKLISTS_FILE):
        with open(CHECKLISTS_FILE, 'r') as f:
            return json.load(f)
    return {"checklists": []}

def save_checklists(data):
    ensure_dir()
    with open(CHECKLISTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_document_templates():
    """Return document templates for common visa types."""
    templates = {
        "H-1B": {
            "country": "USA",
            "documents": [
                {"category": "Identity", "name": "Valid Passport", "required": True, 
                 "requirements": "Valid 6+ months beyond employment", "translation": False},
                {"category": "Identity", "name": "Visa Photos (2)", "required": True,
                 "requirements": "2x2 inches, white background, <6 months old", "translation": False},
                {"category": "Employment", "name": "Form I-129 Approval (I-797)", "required": True,
                 "requirements": "Original approval notice", "translation": False},
                {"category": "Employment", "name": "Labor Condition Application", "required": True,
                 "requirements": "Certified LCA from DOL", "translation": False},
                {"category": "Employment", "name": "Employment Offer Letter", "required": True,
                 "requirements": "On company letterhead, signed", "translation": False},
                {"category": "Financial", "name": "Pay Stubs (3 months)", "required": False,
                 "requirements": "Most recent pay stubs if currently employed", "translation": False},
                {"category": "Education", "name": "Degree/Diploma", "required": True,
                 "requirements": "Original or certified copy", "translation": True},
                {"category": "Education", "name": "Transcripts", "required": True,
                 "requirements": "Sealed, official transcripts", "translation": True},
            ]
        },
        "F-1": {
            "country": "USA",
            "documents": [
                {"category": "Identity", "name": "Valid Passport", "required": True,
                 "requirements": "Valid 6+ months beyond intended stay", "translation": False},
                {"category": "Identity", "name": "Visa Photos", "required": True,
                 "requirements": "As per DS-160 specifications", "translation": False},
                {"category": "Education", "name": "Form I-20", "required": True,
                 "requirements": "Signed by student and DSO", "translation": False},
                {"category": "Education", "name": "Academic Transcripts", "required": True,
                 "requirements": "All previous institutions", "translation": True},
                {"category": "Education", "name": "Test Scores", "required": True,
                 "requirements": "TOEFL/IELTS, GRE/GMAT if applicable", "translation": False},
                {"category": "Financial", "name": "Bank Statements", "required": True,
                 "requirements": "6 months, showing sufficient funds", "translation": False},
                {"category": "Financial", "name": "Affidavit of Support", "required": False,
                 "requirements": "If sponsored by family/organization", "translation": True},
                {"category": "Other", "name": "SEVIS Fee Receipt", "required": True,
                 "requirements": "I-901 payment confirmation", "translation": False},
            ]
        },
        "Express Entry": {
            "country": "Canada",
            "documents": [
                {"category": "Identity", "name": "Valid Passport", "required": True,
                 "requirements": "All pages, valid", "translation": False},
                {"category": "Identity", "name": "Birth Certificate", "required": True,
                 "requirements": "Original or certified copy", "translation": True},
                {"category": "Language", "name": "Language Test Results", "required": True,
                 "requirements": "IELTS/CELPIP for English, TEF for French", "translation": False},
                {"category": "Education", "name": "ECA Report", "required": True,
                 "requirements": "Educational Credential Assessment", "translation": False},
                {"category": "Employment", "name": "Reference Letters", "required": True,
                 "requirements": "From all employers in last 10 years", "translation": True},
                {"category": "Civil", "name": "Police Clearance", "required": True,
                 "requirements": "From all countries lived 6+ months", "translation": True},
                {"category": "Medical", "name": "Medical Exam", "required": True,
                 "requirements": "From IRCC-approved panel physician", "translation": False},
                {"category": "Financial", "name": "Proof of Funds", "required": True,
                 "requirements": "Bank statements showing required amount", "translation": False},
            ]
        }
    }
    return templates

def main():
    parser = argparse.ArgumentParser(description='Generate document checklist')
    parser.add_argument('--visa', required=True, help='Visa type (H-1B, F-1, etc.)')
    parser.add_argument('--country', required=True, help='Destination country')
    parser.add_argument('--applicant-type', default='individual',
                        help='individual, spouse, dependent, etc.')
    
    args = parser.parse_args()
    
    templates = get_document_templates()
    
    # Get template or create generic
    template = templates.get(args.visa, {
        "country": args.country,
        "documents": [
            {"category": "Identity", "name": "Valid Passport", "required": True,
             "requirements": "Valid 6+ months beyond intended stay", "translation": False},
            {"category": "Identity", "name": "Application Photos", "required": True,
             "requirements": "Per consulate specifications", "translation": False},
            {"category": "Financial", "name": "Proof of Funds", "required": True,
             "requirements": "Bank statements or sponsorship letter", "translation": False},
        ]
    })
    
    checklist_id = str(uuid.uuid4())[:8]
    
    documents = []
    for doc in template["documents"]:
        documents.append({
            "id": str(uuid.uuid4())[:8],
            "category": doc["category"],
            "name": doc["name"],
            "required": doc["required"],
            "requirements": doc["requirements"],
            "translation_needed": doc["translation"],
            "status": "needed",
            "notes": ""
        })
    
    checklist = {
        "id": checklist_id,
        "visa_type": args.visa,
        "country": args.country,
        "applicant_type": args.applicant_type,
        "created_at": datetime.now().isoformat(),
        "documents": documents,
        "completion_percentage": 0
    }
    
    data = load_checklists()
    data["checklists"].append(checklist)
    save_checklists(data)
    
    # Output
    print(f"\nDOCUMENT CHECKLIST: {args.visa} ({args.country})")
    print(f"ID: {checklist_id}")
    print("=" * 60)
    
    current_category = None
    for doc in documents:
        if doc["category"] != current_category:
            current_category = doc["category"]
            print(f"\n{current_category.upper()}")
            print("-" * 40)
        
        req_mark = "☐" if doc["required"] else "◯"
        trans_mark = " [T]" if doc["translation_needed"] else ""
        print(f"{req_mark} {doc['name']}{trans_mark}")
        print(f"   Req: {doc['requirements']}")
    
    print(f"\nTotal documents: {len(documents)}")
    print(f"Required: {sum(1 for d in documents if d['required'])}")
    print(f"Need translation: {sum(1 for d in documents if d['translation_needed'])}")
    print(f"\nSaved to: {CHECKLISTS_FILE}")
    print(f"\nTo mark documents as collected:")
    print(f"  scripts/document_inventory.py --checklist-id {checklist_id}")

if __name__ == '__main__':
    main()

import os
import glob
import re

def migrate():
    base_dir = '/root/.openclaw/workspace/projects/leio-sdlc'
    e2e_scripts = glob.glob(os.path.join(base_dir, 'scripts', 'e2e', 'e2e_test_*.sh'))
    test_scripts = glob.glob(os.path.join(base_dir, 'tests', '*.py'))
    
    files_to_process = e2e_scripts + test_scripts
    
    for filepath in files_to_process:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('Review_' + 'Report.md', 'review_report.json')
        new_content = new_content.replace('Review_' + 'Report.md.template', 'review_report.json')
        
        # Replace python mock f.write('...[APPROVED]...') with valid JSON
        # Example: f.write('Review resulted in [APPROVED] status.') -> f.write('{"overall_assessment": "EXCELLENT", "findings": []}')
        new_content = re.sub(
            r'f\.write\([\'"].*?\[APPROVED\].*?[\'"]\)',
            r'f.write(\'{"overall_assessment": "EXCELLENT", "findings": []}\')',
            new_content
        )
        
        new_content = re.sub(
            r'f\.write\([\'"].*?\[ACTION_REQUIRED\].*?[\'"]\)',
            r'f.write(\'{"overall_assessment": "NEEDS_ATTENTION", "findings": [{"file_path": "dummy", "line_number": 1, "category": "Correctness", "severity": "MAJOR", "description": "dummy", "recommendation": "dummy"}]}\')',
            new_content
        )
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")

if __name__ == '__main__':
    migrate()
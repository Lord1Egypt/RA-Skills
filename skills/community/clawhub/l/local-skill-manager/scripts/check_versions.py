import os
import yaml

def check_versions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.abspath(os.path.join(current_dir, '../../'))
    print(f"Checking versions in: {skills_dir}")
    print("-" * 50)
    
    count = 0
    for item in os.listdir(skills_dir):
        item_path = os.path.join(skills_dir, item)
        if os.path.isdir(item_path):
            skill_md = os.path.join(item_path, 'SKILL.md')
            version = "unknown"
            if os.path.exists(skill_md):
                count += 1
                try:
                    with open(skill_md, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.startswith('---'):
                            parts = content.split('---')
                            if len(parts) >= 2:
                                meta = yaml.safe_load(parts[1])
                                if meta:
                                    version = meta.get('version', 'unknown')
                except:
                    pass
                print(f"{item:<30} v{version}")
    
    print("-" * 50)
    print(f"Total Skills Found: {count}")

if __name__ == "__main__":
    check_versions()

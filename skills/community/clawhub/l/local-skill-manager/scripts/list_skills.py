import os
import yaml

def list_skills():
    # Assuming the script is in .trae/skills/local-skill-manager/scripts/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.abspath(os.path.join(current_dir, '../../'))
    
    print(f"Scanning skills in: {skills_dir}")
    print("-" * 50)
    
    skills = []
    
    if not os.path.exists(skills_dir):
        print("Skills directory not found.")
        return

    for item in os.listdir(skills_dir):
        item_path = os.path.join(skills_dir, item)
        if os.path.isdir(item_path):
            skill_md = os.path.join(item_path, 'SKILL.md')
            description = "No description available"
            version = "unknown"
            
            if os.path.exists(skill_md):
                try:
                    with open(skill_md, 'r', encoding='utf-8') as f:
                        # Simple parsing of YAML frontmatter
                        content = f.read()
                        if content.startswith('---'):
                            parts = content.split('---')
                            if len(parts) >= 2:
                                meta = yaml.safe_load(parts[1])
                                if meta:
                                    description = meta.get('description', description)
                                    version = meta.get('version', version)
                except Exception as e:
                    description = f"Error reading SKILL.md: {e}"
            
            skills.append({
                'name': item,
                'description': description.strip().replace('\n', ' '),
                'version': version
            })
    
    # Sort by name
    skills.sort(key=lambda x: x['name'])
    
    for skill in skills:
        print(f"[{skill['name']}] (v{skill['version']})")
        print(f"  {skill['description'][:100]}...")
        print("")
        
    print("-" * 50)
    print(f"Total Skills: {len(skills)}")

if __name__ == "__main__":
    list_skills()

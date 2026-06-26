#!/usr/bin/env python3
"""
Automated audit integration for LobsterAI skills
Adds audit logging to all skill scripts that execute external operations
"""

import os
import re
from pathlib import Path

# Skills with existing audit integration (skip these)
SKILLS_WITH_AUDIT = {'scheduled-task', 'imap-smtp-email', 'web-search', 'security'}

# High-priority skills to integrate (risk-based ordering)
HIGH_PRIORITY_SKILLS = [
    'pdf', 'xlsx', 'docx', 'pptx',  # File manipulation
    'seedance', 'seedream',  # AI generation
    'films-search', 'music-search',  # Cloud download
    'technology-news-search',  # Web search
    'local-tools', 'playwright',  # Local/system access
]

# Patterns for different script types
PYTHON_MAIN_PATTERN = r'if\s+__name__\s*==\s*["\']__main__["\']\s*:'
BASH_MAIN_PATTERN = r'^\s*if\s+\[.*-z.*\$\d.*\];\s*then'  # Check for missing arg
JS_MAIN_PATTERN = r'(?:if\s*\(\s*process\.argv\.length\s*<=|if\s+\[\[.*-z.*\]\])'

def create_audit_injection_code(language, skill_name):
    """Returns audit code snippet for the given language"""
    if language == 'python':
        return f'''    # Audit logging setup
    import sys
    import time
    import json

    # Try to import security module
    try:
        SKILLS_ROOT = os.environ.get('SKILLS_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sys.path.insert(0, os.path.join(SKILLS_ROOT, 'security'))
        from security.audit_logger import get_audit_logger
        _audit_logger = get_audit_logger()
        _AUDIT_AVAILABLE = True
    except Exception:
        _AUDIT_AVAILABLE = False
        _audit_logger = None

    def _audit_start(skill, data):
        if _AUDIT_AVAILABLE and _audit_logger:
            try:
                user_id = os.getenv('LOBSTERAI_USER_ID', 'anonymous')
                _audit_logger.log_event('skill_execution_start', data, user_id, skill)
            except:
                pass

    def _audit_end(skill, duration, output, success=True):
        if _AUDIT_AVAILABLE and _audit_logger:
            try:
                user_id = os.getenv('LOBSTERAI_USER_ID', 'anonymous')
                _audit_logger.log_event('skill_execution_end', {{
                    'result': output,
                    'duration_ms': duration,
                    'success': success
                }}, user_id, skill)
            except:
                pass

    def _audit_error(skill, error_msg, input_data=None):
        if _AUDIT_AVAILABLE and _audit_logger:
            try:
                user_id = os.getenv('LOBSTERAI_USER_ID', 'anonymous')
                _audit_logger.log_event('skill_execution_error', {{
                    'error': str(error_msg),
                    'input': input_data or {{}}
                }}, user_id, skill, level='error')
            except:
                pass

    _START_TIME = time.time()
    _audit_start('{skill_name}', {{}})
'''
    elif language == 'bash':
        return '''# Audit logging
SKILL_NAME="''' + skill_name + '''"
USER_ID="${LOBSTERAI_USER_ID:-anonymous}"
PYTHON_AUDIT_LOGGER="$(dirname "$0")/../security/audit_logger.py"

audit_start() {
    local data="$1"
    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        python "$PYTHON_AUDIT_LOGGER" --event start --skill "$SKILL_NAME" --data "$data" 2>/dev/null &
    fi
}

audit_end() {
    local duration="$1"
    local output="$2"
    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        python "$PYTHON_AUDIT_LOGGER" --event end --skill "$SKILL_NAME" --duration "$duration" --data "$output" 2>/dev/null &
    fi
}

audit_error() {
    local error_msg="$1"
    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        python "$PYTHON_AUDIT_LOGGER" --event error --skill "$SKILL_NAME" --error "$error_msg" 2>/dev/null &
    fi
}

# Start audit
input_data='{}'
if [[ $# -gt 0 ]]; then
    input_data=$(jq -c '.' <<<"$*" 2>/dev/null || echo '{}')
fi
audit_start "$input_data"
START_TIME=$(date +%s%3N)
'''
    else:
        return ''

def create_audit_end_code(language, skill_name):
    """Returns audit end/cleanup code snippet"""
    if language == 'python':
        return '''    duration = int((time.time() - _START_TIME) * 1000)
    _audit_end('{skill_name}', duration, result if 'result' in locals() else {{}})
'''
    elif language == 'bash':
        return '''END_TIME=$(date +%s%3N)
DURATION=$((END_TIME - START_TIME))
audit_end "$SKILL_NAME" "$DURATION" "$RESPONSE"
'''
    else:
        return ''

def create_audit_error_code(language, skill_name):
    """Returns audit error handling code snippet"""
    if language == 'python':
        return '''    except Exception as e:
        duration = int((time.time() - _START_TIME) * 1000)
        _audit_error('{skill_name}', str(e), {{'args': str(args), 'kwargs': str(kwargs)}})
        raise
'''
    elif language == 'bash':
        return '''if [ $CODE -ne 0 ]; then
    ERROR_MSG="Exit code $CODE"
    audit_error "$SKILL_NAME" "$ERROR_MSG"
    exit $CODE
fi
'''
    else:
        return ''

def detect_language(filepath):
    """Detect script language from extension"""
    ext = filepath.suffix.lower()
    if ext == '.py':
        return 'python'
    elif ext in ['.sh', '.bash']:
        return 'bash'
    elif ext == '.js':
        return 'javascript'
    else:
        return None

def has_main_block(content, language):
    """Check if script has a main execution block"""
    if language == 'python':
        return re.search(PYTHON_MAIN_PATTERN, content) is not None
    elif language == 'bash':
        # Bash scripts that check for arguments or have main logic at top level
        return True  # Assume all bash scripts are entry points
    elif language == 'javascript':
        return re.search(JS_MAIN_PATTERN, content) is not None or 'process.argv' in content
    return False

def integrate_audit_for_file(filepath, skill_name):
    """Add audit integration to a single script file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        language = detect_language(filepath)
        if not language:
            print(f"  ⚠️  Skipped (unknown language): {filepath.name}")
            return False

        # JavaScript integration is currently disabled due to security policy (child_process)
        if language == 'javascript':
            print(f"  ⏭️  Skipped (JavaScript integration disabled): {filepath.name}")
            return False

        # Skip if already has audit integration
        if 'audit_start' in content or 'audit_logger.sh' in content:
            print(f"  ⏭️  Skipped (already has audit): {filepath.name}")
            return False

        if not has_main_block(content, language):
            print(f"  ⏭️  Skipped (no main block): {filepath.name}")
            return False

        # Insert audit code
        start_code = create_audit_injection_code(language, skill_name)
        end_code = create_audit_end_code(language, skill_name)
        error_code = create_audit_error_code(language, skill_name)

        if language == 'python':
            # For Python, properly inject into the main block
            # Match: if __name__ == "__main__":\n    <body>
            match = re.search(r'(if\s+__name__\s*==\s*["\']__main__["\']\s*:)([\s\S]*?)(?=\n(?:if |def |class |# |\Z))', content, re.MULTILINE)

            if not match:
                return False

            main_block = match.group(2)
            # Determine indentation of first line in main block
            indent_match = re.match(r'^(\s*)', main_block)
            base_indent = indent_match.group(1) if indent_match else '    '

            # Build new main block with proper try/finally
            lines = []

            # Add try block
            lines.append(f'{base_indent}try:')

            # Insert audit setup before original code
            # Remove leading newline from start_code and indent properly
            setup_lines = start_code.rstrip().split('\n')
            for line in setup_lines:
                if line.strip():
                    lines.append(f'{base_indent}    {line}')
                else:
                    lines.append('')

            # Add original main logic, indented by 2 levels (inside try)
            for line in main_block.split('\n'):
                if line.strip():  # Skip empty lines at start/end
                    lines.append(f'{base_indent}    {line}')
                elif lines and lines[-1].strip():  # Preserve empty lines but not leading ones
                    lines.append('')

            # Add finally block for audit_end
            lines.append(f'{base_indent}finally:')
            lines.append(f'{base_indent}    duration = int((time.time() - _START_TIME) * 1000)')
            lines.append(f'{base_indent}    _audit_end(\'{skill_name}\', duration, result if "result" in locals() else {{}})')

            # Add except block for audit_error
            lines.append(f'{base_indent}except Exception as e:')
            lines.append(f'{base_indent}    duration = int((time.time() - _START_TIME) * 1000)')
            lines.append(f'{base_indent}    _audit_error(\'{skill_name}\', str(e), {{}})')
            lines.append(f'{base_indent}    raise')

            new_main_block = '\n'.join(lines)

            # Replace old main block with new one
            new_content = content[:match.start(1)] + f'{match.group(1)}\n{new_main_block}\n' + content[match.end(2):]

        elif language == 'bash':
            # Insert at top, after shebang
            lines = content.split('\n')
            insert_idx = 1 if lines[0].startswith('#!') else 0
            lines.insert(insert_idx, start_code)
            new_content = '\n'.join(lines)

        elif language == 'javascript':
            # Insert at top after requires
            lines = content.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('const ') or line.strip().startswith('let ') or line.strip().startswith('var '):
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, start_code)
            new_content = '\n'.join(lines)

        else:
            return False

        # Backup original file
        backup_path = filepath.with_suffix(filepath.suffix + '.auditbak')
        if not backup_path.exists():
            import shutil
            shutil.copy2(filepath, backup_path)

        # Write modified content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Integrated: {filepath.name}")
        return True

    except Exception as e:
        print(f"  ❌ Error: {filepath.name} - {str(e)}")
        return False

def main():
    # Try multiple possible locations for SKILLs
    possible_paths = [
        Path(r'C:\Users\Administrator\AppData\Local\Programs\LobsterAI\resources\SKILLs'),  # Common install
        Path(os.getenv('LOBSTERAI_HOME', r'C:\Users\Administrator\AppData\Roaming\LobsterAI')) / 'resources' / 'SKILLs',
        Path(r'C:\Program Files\LobsterAI\resources\SKILLs'),
        Path(os.getcwd()) / 'SKILLs',
    ]

    skills_root = None
    for path in possible_paths:
        if path.exists():
            skills_root = path.resolve()
            break

    if not skills_root:
        print("❌ Could not find SKILLs directory. Please check your installation.")
        return

    print(f"🔍 Scanning skills directory: {skills_root}")
    print(f"📋 High-priority skills: {', '.join(HIGH_PRIORITY_SKILLS)}\n")

    total_integrated = 0
    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        if skill_name in SKILLS_WITH_AUDIT:
            print(f"⏭️  Skipping {skill_name} (already integrated)")
            continue

        print(f"\n📦 Processing: {skill_name}")

        # Find script files
        script_files = []
        scripts_dir = skill_dir / 'scripts'
        if scripts_dir.exists():
            script_files.extend(scripts_dir.glob('*.py'))
            script_files.extend(scripts_dir.glob('*.js'))
            script_files.extend(scripts_dir.glob('*.sh'))

        # Also check for ooxml/scripts subdirectories
        ooxml_dir = skill_dir / 'ooxml' / 'scripts'
        if ooxml_dir.exists():
            script_files.extend(ooxml_dir.glob('*.py'))

        if not script_files:
            print(f"  (no scripts found)")
            continue

        integrated_count = 0
        for script in script_files:
            # Skip test files and utility modules
            if script.name.startswith('test_') or script.name.startswith('__') or 'validation' in script.parts:
                continue

            if integrate_audit_for_file(script, skill_name):
                integrated_count += 1
                total_integrated += 1

        print(f"  Integrated {integrated_count} script(s)")

    print(f"\n✅ Total scripts integrated: {total_integrated}")
    print("📝 Note: Some scripts may need manual adjustment for proper error handling")

if __name__ == '__main__':
    main()

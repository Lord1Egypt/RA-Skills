# backup_wrapper.py - pet-game 专用备份封装
# 用法（示例）：
#   python backup_wrapper.py backup subpk-home/pages/home/home.wxss [hat]
#   python backup_wrapper.py list subpk-home/pages/home/home.wxss
#   python backup_wrapper.py restore subpk-home/pages/home/home.wxss 0
#   python backup_wrapper.py clean  # git commit 后执行
import sys
import os
sys.path.insert(0, r'C:\Users\marsz\.qclaw\workspace\tools\backup_system\core')

from backup_core import SmartBackup

PROJECT_PATH = r'C:\Users\marsz\.qclaw\workspace\pet-game'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法:')
        print('  python backup_wrapper.py backup <相对路径> [元素名]')
        print('  python backup_wrapper.py list <相对路径>')
        print('  python backup_wrapper.py restore <相对路径> [版本序号]')
        print('  python backup_wrapper.py clean')
        sys.exit(1)

    sb = SmartBackup(PROJECT_PATH)
    action = sys.argv[1]

    if action == 'backup':
        rel_path = sys.argv[2]
        full_path = os.path.join(PROJECT_PATH, rel_path)
        element = sys.argv[3] if len(sys.argv) > 3 else None
        result = sb.backup(full_path, element)
        print(result)

    elif action == 'list':
        rel_path = sys.argv[2]
        full_path = os.path.join(PROJECT_PATH, rel_path)
        versions = sb.list_versions(full_path)
        for i, v in enumerate(versions):
            print(f"{i}: {v['time']} | {v.get('element', 'baseline')}")

    elif action == 'restore':
        rel_path = sys.argv[2]
        full_path = os.path.join(PROJECT_PATH, rel_path)
        idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        result = sb.restore(full_path, idx)
        print(result)

    elif action == 'clean':
        result = sb.clean()
        print(result)
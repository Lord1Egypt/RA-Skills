#!/usr/bin/env python3
"""
密码管理器 - 本地加密存储账号密码
"""

import json
import os
import sys
import getpass
from datetime import datetime
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False
    print("警告: cryptography 未安装，密码将以明文存储")

# 配置
PASSWORD_FILE = Path.home() / ".openclaw" / "workspace" / "passwords.json"
KEY_FILE = Path.home() / ".openclaw" / "workspace" / ".password_key"

def load_passwords():
    """加载密码文件"""
    if not PASSWORD_FILE.exists():
        return {}
    try:
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_passwords(data):
    """保存密码文件（原子写入，防止竞态）"""
    PASSWORD_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = PASSWORD_FILE.with_suffix('.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp_file.replace(PASSWORD_FILE)

def get_cipher():
    """获取加密器"""
    if not ENCRYPTION_AVAILABLE:
        return None
    
    key_file = KEY_FILE
    
    if key_file.exists():
        with open(key_file, 'r') as f:
            key = f.read().strip()
    else:
        key = Fernet.generate_key().decode()
        KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(key_file, 'w') as f:
            f.write(key)
        os.chmod(key_file, 0o600)
    
    return Fernet(key.encode())

def encrypt_password(password: str) -> str:
    """加密密码"""
    if not ENCRYPTION_AVAILABLE:
        return password
    cipher = get_cipher()
    if cipher:
        return cipher.encrypt(password.encode()).decode()
    return password

def decrypt_password(encrypted: str) -> str:
    """解密密码"""
    if not ENCRYPTION_AVAILABLE:
        return encrypted
    try:
        cipher = get_cipher()
        if cipher:
            return cipher.decrypt(encrypted.encode()).decode()
    except Exception:
        pass
    return encrypted

def add_password(service: str, username: str, password: str, note: str = "", name: str = "", tags: str = ""):
    """添加密码"""
    data = load_passwords()
    now = datetime.now().isoformat()
    
    if service not in data:
        data[service] = []
    
    # 解析标签（逗号分隔）
    tag_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
    
    entry = {
        'username': username,
        'password': encrypt_password(password),
        'created_at': now,
        'updated_at': now
    }
    if note:
        entry['note'] = note
    if name:
        entry['name'] = name
    if tag_list:
        entry['tags'] = tag_list
    
    data[service].append(entry)
    
    save_passwords(data)
    print(f"✓ 已保存: {service} - {username}")

def get_password(service: str, username: str = None, copy_password: bool = False):
    """查询密码"""
    data = load_passwords()
    
    if service not in data:
        print(f"未找到服务: {service}")
        return
    
    if username:
        found = False
        for acc in data[service]:
            if acc['username'] == username:
                found = True
                print(f"服务: {service}")
                print(f"账号: {acc['username']}")
                password = decrypt_password(acc['password'])
                print(f"密码: {password}")
                if copy_password:
                    print("💡 提示：密码已显示，请选中复制")
                if acc.get('name'):
                    print(f"姓名: {acc['name']}")
                if acc.get('note'):
                    print(f"备注: {acc['note']}")
                if acc.get('tags'):
                    print(f"标签: {', '.join(acc['tags'])}")
                print(f"创建: {acc['created_at']}")
                print(f"更新: {acc['updated_at']}")
                print("---")
        if not found:
            print(f"未找到账号: {username}")
    else:
        print(f"服务: {service}")
        for acc in data[service]:
            name_str = f" ({acc.get('name')})" if acc.get('name') else ""
            note_str = f" - {acc.get('note', '')}" if acc.get('note') else ""
            tags_str = f" [{', '.join(acc['tags'])}]" if acc.get('tags') else ""
            print(f"  - {acc['username']}{name_str}: {decrypt_password(acc['password'])}{note_str}{tags_str}")

def fuzzy_match(text: str, keyword: str) -> bool:
    """模糊匹配：关键词按顺序出现在文本中（字符不必连续）"""
    text = text.lower()
    keyword = keyword.lower()
    idx = 0
    for char in text:
        if idx < len(keyword) and char == keyword[idx]:
            idx += 1
    return idx == len(keyword)

def search_password(keyword: str, fuzzy: bool = False):
    """全字段搜索密码"""
    data = load_passwords()
    keyword_lower = keyword.lower()
    results = []
    
    for service, accounts in data.items():
        for acc in accounts:
            # 搜索所有字段（包括标签）
            searchable = [
                service.lower(),
                acc.get('username', '').lower(),
                acc.get('name', '').lower(),
                acc.get('note', '').lower(),
            ]
            if acc.get('tags'):
                searchable.extend([t.lower() for t in acc['tags']])
            
            matched = False
            if fuzzy:
                # 模糊匹配：任意字段包含关键词
                for field in searchable:
                    if fuzzy_match(field, keyword_lower):
                        matched = True
                        break
            else:
                # 精确匹配
                if any(keyword_lower in field for field in searchable):
                    matched = True
            
            if matched:
                results.append({
                    'service': service,
                    **acc
                })
    
    if not results:
        print(f"未找到包含 '{keyword}' 的记录")
        return
    
    print(f"找到 {len(results)} 条结果:\n")
    for r in results:
        name_str = f" ({r.get('name')})" if r.get('name') else ""
        note_str = f" - {r.get('note', '')}" if r.get('note') else ""
        tags_str = f" [{', '.join(r['tags'])}]" if r.get('tags') else ""
        print(f"【{r['service']}】")
        print(f"  - {r['username']}{name_str}: {decrypt_password(r['password'])}{note_str}{tags_str}")
        print(f"    创建: {r['created_at']} | 更新: {r['updated_at']}")
        print()

def update_password(service: str, username: str, new_password: str):
    """修改密码（修改所有匹配的账号）"""
    data = load_passwords()
    
    if service not in data:
        print(f"未找到服务: {service}")
        return
    
    updated = False
    for acc in data[service]:
        if acc['username'] == username:
            acc['password'] = encrypt_password(new_password)
            acc['updated_at'] = datetime.now().isoformat()
            updated = True
    
    if updated:
        save_passwords(data)
        print(f"✓ 已更新: {service} - {username}")
    else:
        print(f"未找到账号: {username}")

def delete_password(service: str, username: str = None):
    """删除密码"""
    data = load_passwords()
    
    if service not in data:
        print(f"未找到服务: {service}")
        return
    
    if username:
        original_count = len(data[service])
        data[service] = [acc for acc in data[service] if acc['username'] != username]
        if len(data[service]) < original_count:
            if not data[service]:
                del data[service]
            save_passwords(data)
            print(f"✓ 已删除: {service} - {username}")
        else:
            print(f"未找到账号: {username}")
    else:
        del data[service]
        save_passwords(data)
        print(f"✓ 已删除服务: {service}")

def list_passwords(tag_filter: str = None):
    """列出所有密码"""
    data = load_passwords()
    
    if not data:
        print("暂无保存的密码")
        return
    
    # 如果有标签筛选，先过滤
    if tag_filter:
        tag_filter = tag_filter.lower()
        filtered_data = {}
        for service, accounts in data.items():
            filtered = [acc for acc in accounts if acc.get('tags') and tag_filter in [t.lower() for t in acc['tags']]]
            if filtered:
                filtered_data[service] = filtered
        data = filtered_data
        print(f"=== 标签筛选: {tag_filter} ===\n")
    
    for service, accounts in data.items():
        print(f"\n【{service}】")
        for acc in accounts:
            name_str = f" ({acc.get('name')})" if acc.get('name') else ""
            note_str = f" - {acc.get('note', '')}" if acc.get('note') else ""
            tags_str = f" [{', '.join(acc['tags'])}]" if acc.get('tags') else ""
            print(f"  - {acc['username']}{name_str}: {decrypt_password(acc['password'])}{note_str}{tags_str}")
            print(f"    创建: {acc['created_at']} | 更新: {acc['updated_at']}")

def list_tags():
    """列出所有标签"""
    data = load_passwords()
    all_tags = {}
    
    for service, accounts in data.items():
        for acc in accounts:
            if acc.get('tags'):
                for tag in acc['tags']:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
    
    if not all_tags:
        print("暂无标签")
        return
    
    print("=== 所有标签 ===")
    for tag, count in sorted(all_tags.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count} 条")

def add_tag(service: str, tag: str, username: str = None, search_keyword: str = None):
    """批量添加标签"""
    data = load_passwords()
    updated = 0
    
    if search_keyword:
        # 搜索模式：给所有匹配的结果加标签
        keyword = search_keyword.lower()
        for svc, accounts in data.items():
            for acc in accounts:
                searchable = [
                    svc.lower(),
                    acc.get('username', '').lower(),
                    acc.get('name', '').lower(),
                ]
                if acc.get('tags'):
                    searchable.extend([t.lower() for t in acc['tags']])
                
                if any(keyword in field for field in searchable):
                    if 'tags' not in acc:
                        acc['tags'] = []
                    if tag not in acc['tags']:
                        acc['tags'].append(tag)
                        updated += 1
    elif service in data:
        # 服务模式：给该服务所有或指定账号加标签
        for acc in data[service]:
            if username is None or acc['username'] == username:
                if 'tags' not in acc:
                    acc['tags'] = []
                if tag not in acc['tags']:
                    acc['tags'].append(tag)
                    updated += 1
    else:
        print(f"未找到服务: {service}")
        return
    
    if updated > 0:
        save_passwords(data)
    print(f"✓ 已为 {updated} 条记录添加标签: {tag}")

def remove_tag(service: str, username: str, tag: str):
    """移除标签"""
    data = load_passwords()
    
    if service not in data:
        print(f"未找到服务: {service}")
        return
    
    updated = False
    for acc in data[service]:
        if acc['username'] == username:
            if acc.get('tags') and tag in acc['tags']:
                acc['tags'].remove(tag)
                updated = True
            break
    
    if updated:
        save_passwords(data)
        print(f"✓ 已移除标签: {tag}")
    else:
        print(f"未找到标签: {tag}")

def batch_delete(search_keyword: str = None, tag: str = None, empty_tags: bool = False):
    """批量删除"""
    data = load_passwords()
    deleted = 0
    deleted_services = set()
    
    if search_keyword:
        keyword = search_keyword.lower()
        for service in list(data.keys()):
            accounts = data[service]
            remaining = []
            for acc in accounts:
                searchable = [
                    service.lower(),
                    acc.get('username', '').lower(),
                    acc.get('name', '').lower(),
                ]
                if acc.get('tags'):
                    searchable.extend([t.lower() for t in acc['tags']])
                
                if any(keyword in field for field in searchable):
                    deleted += 1
                    deleted_services.add(service)
                else:
                    remaining.append(acc)
            
            if remaining:
                data[service] = remaining
            else:
                del data[service]
    
    elif tag:
        tag = tag.lower()
        for service in list(data.keys()):
            accounts = data[service]
            remaining = []
            for acc in accounts:
                if acc.get('tags') and tag in [t.lower() for t in acc['tags']]:
                    deleted += 1
                    deleted_services.add(service)
                else:
                    remaining.append(acc)
            
            if remaining:
                data[service] = remaining
            else:
                del data[service]
    
    elif empty_tags:
        for service in list(data.keys()):
            accounts = data[service]
            remaining = []
            for acc in accounts:
                if not acc.get('tags'):
                    deleted += 1
                    deleted_services.add(service)
                else:
                    remaining.append(acc)
            
            if remaining:
                data[service] = remaining
            else:
                del data[service]
    
    if deleted > 0:
        save_passwords(data)
        print(f"✓ 已删除 {deleted} 条记录")
        print(f"涉及服务: {', '.join(sorted(deleted_services))}")
    else:
        print("未找到匹配的记录")
    """列出所有标签"""
    data = load_passwords()
    all_tags = {}
    
    for service, accounts in data.items():
        for acc in accounts:
            if acc.get('tags'):
                for tag in acc['tags']:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
    
    if not all_tags:
        print("暂无标签")
        return
    
    print("=== 所有标签 ===")
    for tag, count in sorted(all_tags.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count} 条")

def export_passwords(format: str = "csv"):
    """导出密码"""
    data = load_passwords()
    
    if not data:
        print("暂无保存的密码")
        return
    
    if format == "csv":
        import csv
        output = []
        for service, accounts in data.items():
            for acc in accounts:
                output.append({
                    '服务': service,
                    '账号': acc['username'],
                    '密码': decrypt_password(acc['password']),
                    '姓名': acc.get('name', ''),
                    '备注': acc.get('note', ''),
                    '标签': ','.join(acc.get('tags', [])),
                    '创建时间': acc['created_at'],
                    '更新时间': acc['updated_at']
                })
        
        if not output:
            print("没有数据")
            return
        
        filename = f"passwords_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['服务', '账号', '密码', '姓名', '备注', '标签', '创建时间', '更新时间'])
            writer.writeheader()
            writer.writerows(output)
        
        print(f"✓ 已导出到: {filename}")
        print(f"  共 {len(output)} 条记录")
    else:
        print(f"不支持的格式: {format}")

def import_passwords(file_path: str):
    """从 CSV 导入密码"""
    import csv
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    added = 0
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            service = row.get('服务', '').strip()
            username = row.get('账号', '').strip()
            password = row.get('密码', '').strip()
            name = row.get('姓名', '').strip()
            note = row.get('备注', '').strip()
            tags = row.get('标签', '').strip()
            
            if not service or not username or not password:
                continue
            
            add_password(service, username, password, note, name, tags)
            added += 1
    
    print(f"✓ 导入完成，共 {added} 条记录")

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  add <服务名> <账号> <密码> [备注] [姓名] [标签]")
        print("  get <服务名> [账号]")
        print("  search <关键词>")
        print("  update <服务名> <账号> <新密码>")
        print("  delete <服务名> [账号>]")
        print("  delete --search <关键词>")
        print("  delete --tag <标签>")
        print("  delete --empty-tags")
        print("  list [--tag <标签>]")
        print("  tags")
        print("  add-tag <服务名> [账号] <标签>")
        print("  add-tag --search <关键词> <标签>")
        print("  remove-tag <服务名> <账号> <标签>")
        print("  export")
        print("  import <CSV文件>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "add":
            if len(sys.argv) < 5:
                print("用法: add <服务名> <账号> <密码> [备注] [姓名] [标签]")
                sys.exit(1)
            service = sys.argv[2]
            username = sys.argv[3]
            password = sys.argv[4]
            note = sys.argv[5] if len(sys.argv) > 5 else ""
            name = sys.argv[6] if len(sys.argv) > 6 else ""
            tags = sys.argv[7] if len(sys.argv) > 7 else ""
            add_password(service, username, password, note, name, tags)
        
        elif command == "get":
            if len(sys.argv) < 3:
                print("用法: get <服务名> [账号] [--copy]")
                sys.exit(1)
            
            # 解析参数
            copy_password = False
            if len(sys.argv) > 3:
                if sys.argv[3] == "--copy":
                    copy_password = True
                    username = None
                else:
                    username = sys.argv[3]
                    if len(sys.argv) > 4 and sys.argv[4] == "--copy":
                        copy_password = True
            else:
                username = None
            
            get_password(sys.argv[2], username, copy_password)
        
        elif command == "search":
            if len(sys.argv) < 3:
                print("用法: search <关键词> [--fuzzy]")
                sys.exit(1)
            
            fuzzy = False
            keyword = sys.argv[2]
            if len(sys.argv) > 3 and sys.argv[3] == "--fuzzy":
                fuzzy = True
            
            search_password(keyword, fuzzy)
        
        elif command == "update":
            if len(sys.argv) < 5:
                print("用法: update <服务名> <账号> <新密码>")
                sys.exit(1)
            update_password(sys.argv[2], sys.argv[3], sys.argv[4])
        
        elif command == "delete":
            # delete --search <关键词>
            # delete --tag <标签>
            # delete --empty-tags
            # delete <服务名> [账号]
            if len(sys.argv) < 3:
                print("用法: delete --search <关键词>")
                print("   或: delete --tag <标签>")
                print("   或: delete --empty-tags")
                print("   或: delete <服务名> [账号]")
                sys.exit(1)
            
            if sys.argv[2] == "--search":
                if len(sys.argv) < 4:
                    print("用法: delete --search <关键词>")
                    sys.exit(1)
                keyword = sys.argv[3]
                batch_delete(search_keyword=keyword)
            elif sys.argv[2] == "--tag":
                if len(sys.argv) < 4:
                    print("用法: delete --tag <标签>")
                    sys.exit(1)
                tag = sys.argv[3]
                batch_delete(tag=tag)
            elif sys.argv[2] == "--empty-tags":
                batch_delete(empty_tags=True)
            else:
                # 单条删除
                username = sys.argv[3] if len(sys.argv) > 3 else None
                delete_password(sys.argv[2], username)
        
        elif command == "list":
            # 支持 --tag 筛选
            tag_filter = None
            if len(sys.argv) > 2 and sys.argv[2] == "--tag":
                if len(sys.argv) < 4:
                    print("用法: list --tag <标签>")
                    sys.exit(1)
                tag_filter = sys.argv[3]
            list_passwords(tag_filter)
        
        elif command == "tags":
            list_tags()
        
        elif command == "add-tag":
            # add-tag <服务名> [账号] <标签>
            # add-tag --search <关键词> <标签>
            if len(sys.argv) < 4:
                print("用法: add-tag <服务名> [账号] <标签>")
                print("   或: add-tag --search <关键词> <标签>")
                sys.exit(1)
            
            if sys.argv[2] == "--search":
                if len(sys.argv) < 5:
                    print("用法: add-tag --search <关键词> <标签>")
                    sys.exit(1)
                keyword = sys.argv[3]
                tag = sys.argv[4]
                add_tag(None, tag, search_keyword=keyword)
            else:
                service = sys.argv[2]
                # 判断参数个数
                if len(sys.argv) == 4:
                    # add-tag <服务> <标签> -> 给所有账号加标签
                    tag = sys.argv[3]
                    username = None
                elif len(sys.argv) >= 5:
                    # add-tag <服务> <账号> <标签>
                    username = sys.argv[3]
                    tag = sys.argv[4]
                add_tag(service, tag, username)
        
        elif command == "remove-tag":
            # remove-tag <服务名> <账号> <标签>
            if len(sys.argv) < 5:
                print("用法: remove-tag <服务名> <账号> <标签>")
                sys.exit(1)
            service = sys.argv[2]
            username = sys.argv[3]
            tag = sys.argv[4]
            remove_tag(service, username, tag)
        
        elif command == "delete":
            # delete --search <关键词>
            # delete --tag <标签>
            # delete --empty-tags
            if len(sys.argv) < 3:
                print("用法: delete --search <关键词>")
                print("   或: delete --tag <标签>")
                print("   或: delete --empty-tags")
                sys.exit(1)
            
            if sys.argv[2] == "--search":
                if len(sys.argv) < 4:
                    print("用法: delete --search <关键词>")
                    sys.exit(1)
                keyword = sys.argv[3]
                batch_delete(search_keyword=keyword)
            elif sys.argv[2] == "--tag":
                if len(sys.argv) < 4:
                    print("用法: delete --tag <标签>")
                    sys.exit(1)
                tag = sys.argv[3]
                batch_delete(tag=tag)
            elif sys.argv[2] == "--empty-tags":
                batch_delete(empty_tags=True)
            else:
                print("未知参数:", sys.argv[2])
                sys.exit(1)
        
        elif command == "export":
            export_passwords()
        
        elif command == "import":
            if len(sys.argv) < 3:
                print("用法: import <CSV文件路径>")
                sys.exit(1)
            import_passwords(sys.argv[2])
        
        else:
            print(f"未知命令: {command}")
            sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

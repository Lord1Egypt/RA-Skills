with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the broken connect method
old_connect = '''        except Exception as e:
                print(f"[错误] SVR 连接失败：{e}")
            print(f"[错误] SVR 连接失败：{e}")
            return False
    
    def disconnect(self):'''

new_connect = '''        except Exception as e:
            print(f"[错误] SVR 连接失败：{e}")
            return False
    
    def disconnect(self):'''

content = content.replace(old_connect, new_connect)

with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed SVRParser.connect!')

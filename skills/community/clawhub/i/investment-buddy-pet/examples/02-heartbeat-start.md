# 示例 2：心跳引擎启动

**场景**: 用户已安装技能，启动宠物

---

## 用户触发

```
用户：启动我的宠物松果
```

---

## Skill 执行流程

### Step 1: 检查是否已安装

```bash
# 检查技能目录
ls ~/.openclaw/skills/investment-buddy-pet/
```

**结果**: 已安装 ✅

### Step 2: 检查是否已在运行

```bash
# 检查 PID 文件
if [ -f /tmp/pet_songguo.pid ]; then
    echo "宠物松果已在运行 (PID: $(cat /tmp/pet_songguo.pid))"
else
    echo "宠物松果未运行，可以启动"
fi
```

**结果**: 未运行，可以启动 ✅

### Step 3: 初始化数据库

```python
# scripts/heartbeat_engine.py
def init_db():
    """初始化数据库（先于 load_pet 执行）"""
    db_path = str(DATA_DIR / "pets.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建 4 个表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            pet_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            pet_type TEXT,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            scheduled_at TIMESTAMP,
            sent BOOLEAN DEFAULT FALSE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ 数据库初始化成功")
```

### Step 4: 加载宠物配置

```python
def load_pet(pet_type: str = None) -> Dict:
    """
    加载宠物配置
    
    注意：必须在 init_db() 之后调用
    """
    pets_dir = Path(__file__).parent / "pets"
    pet_file = pets_dir / f"{pet_type}.json"
    
    if not pet_file.exists():
        raise FileNotFoundError(f"宠物配置不存在：{pet_type}")
    
    with open(pet_file, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Step 5: 启动心跳引擎

```bash
python scripts/heartbeat_engine.py start --user-id user_001 --pet-type songguo
```

**输出**:
```
✅ 数据库初始化成功
✅ 宠物配置加载成功：松果 🐿️
✅ 心跳引擎启动成功

配置：
• 用户：user_001
• 宠物：松果 🐿️
• 心跳间隔：300 秒（5 分钟）
• 下次触发：2026-04-14 16:35:00

宠物说："早上好！今天也是存坚果的一天！☀️"
```

### Step 6: 心跳触发（5 分钟后）

```
🐿️ 松果：早上好！今天也是存坚果的一天！☀️

📊 今日简报：
• 沪深 300 +0.5%
• 你的持仓 +0.8%
• 定投日！记得打卡哦~
```

---

## 关键代码

```python
# scripts/heartbeat_engine.py
def start_heartbeat(user_id: str, pet_type: str, interval: int = 300):
    """
    启动心跳引擎
    
    Args:
        user_id: 用户 ID
        pet_type: 宠物类型
        interval: 心跳间隔（秒），默认 300 秒
    """
    # 严格初始化顺序
    init_db()  # 先初始化数据库
    pet_config = load_pet(pet_type)  # 后加载宠物配置
    
    # 写入 PID 文件
    pid_file = f"/tmp/pet_{pet_type}.pid"
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    
    # 启动心跳循环
    while True:
        message = generate_pet_message(pet_config, user_id)
        
        # 合规检查
        is_compliant, violations = check_compliance(message)
        if not is_compliant:
            print(f"⚠️ 合规检查失败：{violations}")
            continue
        
        # 发送消息
        send_message(user_id, message)
        
        # 等待下次触发
        time.sleep(interval)
```

---

## 合规检查点

- ✅ 数据库初始化先于宠物加载
- ✅ PID 文件防止重复启动
- ✅ 每条消息经过合规检查

---

**文件位置**: `examples/02-heartbeat-start.md`  
**创建时间**: 2026-04-14
